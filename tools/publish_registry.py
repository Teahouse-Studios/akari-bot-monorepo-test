"""由 PyPI 已发布产物维护发布账本和稳定、预发布索引。"""

from __future__ import annotations

import argparse
import configparser
import hashlib
import io
import json
import shutil
import sys
import tempfile
import zipfile
from email.parser import BytesParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name, parse_sdist_filename, parse_wheel_filename
from packaging.version import Version

if __package__:
    from . import build_registry
else:
    import build_registry


class ReleaseError(RuntimeError):
    pass


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    contents = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(contents)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _identity(filename: str) -> tuple[str, Version]:
    if filename.endswith(".whl"):
        name, version, _, _ = parse_wheel_filename(filename)
    else:
        name, version = parse_sdist_filename(filename)
    return canonicalize_name(name), version


def _manifest(directory: Path, dist: str, version: str) -> dict:
    files = {}
    for path in sorted(directory.iterdir()):
        if path.suffix != ".whl" and not path.name.endswith(".tar.gz"):
            continue
        if _identity(path.name) != (canonicalize_name(dist), Version(version)):
            raise ReleaseError(f"产物不是本次分发：{path.name}")
        files[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not any(name.endswith(".whl") for name in files) or not any(name.endswith(".tar.gz") for name in files):
        raise ReleaseError("本次发布必须同时具有 wheel 和 sdist")
    return {"dist": canonicalize_name(dist), "version": version, "files": files}


def _download(url: str) -> bytes:
    if not url.startswith("https://"):
        raise ReleaseError("发布产物地址必须使用 HTTPS")
    with urlopen(url, timeout=60) as response:
        return response.read()


def _prepare_upload(directory: Path, expected: dict, output: Path) -> int:
    if _manifest(directory, expected["dist"], expected["version"]) != expected:
        raise ReleaseError("本地产物与保存的构建清单不符")
    url = f"https://pypi.org/pypi/{expected['dist']}/{Version(expected['version'])}/json"
    try:
        payload = json.loads(_download(url))
    except HTTPError as error:
        if error.code != 404:
            raise
        payload = None
    if payload is not None:
        info = payload["info"]
        if canonicalize_name(info.get("name", "")) != expected["dist"] or Version(info.get("version", "")) != Version(
            expected["version"]
        ):
            raise ReleaseError("PyPI 版本身份与上传目标不符")
    files = payload["urls"] if payload is not None else []
    if any(item.get("yanked") for item in files):
        raise ReleaseError("不能补传已撤回版本")
    existing = {item["filename"]: item["digests"]["sha256"] for item in files}
    if any(expected["files"].get(name) != digest for name, digest in existing.items()):
        raise ReleaseError("已存在的 PyPI 文件与保存产物的名称或 SHA256 不符；拒绝补传")
    if output.exists():
        raise ReleaseError("待上传目录必须尚未存在")
    output.mkdir(parents=True)
    missing = set(expected["files"]) - set(existing)
    for name in sorted(missing):
        shutil.copy2(directory / name, output / name)
    return len(missing)


def _published(dist: str, version: str, expected: dict | None = None) -> tuple[dict, bytes]:
    name = canonicalize_name(dist)
    payload = json.loads(_download(f"https://pypi.org/pypi/{name}/{Version(version)}/json"))
    info = payload.get("info", {})
    if canonicalize_name(info.get("name", "")) != name or Version(info.get("version", "")) != Version(version):
        raise ReleaseError("PyPI 返回的分发或版本与发布目标不符")
    files = payload.get("urls", [])
    if not files or any(item.get("yanked") for item in files):
        raise ReleaseError("发布版本缺少文件或已撤回")
    hashes = {item["filename"]: item["digests"]["sha256"] for item in files}
    if expected is not None:
        if expected.get("dist") != name or Version(expected.get("version", "")) != Version(version):
            raise ReleaseError("构建清单与发布目标不符")
        if hashes != expected.get("files"):
            raise ReleaseError("PyPI 文件集合或 SHA256 与本次构建清单不符")
    wheels = [item for item in files if item.get("packagetype") == "bdist_wheel"]
    if len(wheels) != 1 or not any(item.get("packagetype") == "sdist" for item in files):
        raise ReleaseError("发布版本必须具有一个通用 wheel 和 sdist")
    wheel = b""
    for item in files:
        if _identity(item["filename"]) != (name, Version(version)):
            raise ReleaseError("PyPI 文件名与发布目标不符")
        if not item["url"].startswith("https://files.pythonhosted.org/"):
            raise ReleaseError("PyPI 产物不在官方文件服务上")
        contents = _download(item["url"])
        if hashlib.sha256(contents).hexdigest() != hashes[item["filename"]]:
            raise ReleaseError(f"下载产物 SHA256 不符：{item['filename']}")
        if item is wheels[0]:
            wheel = contents
    record = {
        "dist": name,
        "version": version,
        "published_at": max(item["upload_time_iso_8601"] for item in files),
        "files": hashes,
        "wheel_url": wheels[0]["url"],
        "wheel_sha256": hashes[wheels[0]["filename"]],
    }
    return record, wheel


def _entry(record: dict, contents: bytes) -> tuple[str | None, dict | None]:
    with zipfile.ZipFile(io.BytesIO(contents)) as archive:
        metadata_paths = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(metadata_paths) != 1:
            raise ReleaseError("wheel 缺少唯一的 METADATA")
        metadata = BytesParser().parsebytes(archive.read(metadata_paths[0]))
        if canonicalize_name(metadata["Name"]) != record["dist"] or Version(metadata["Version"]) != Version(
            record["version"]
        ):
            raise ReleaseError("wheel 元数据与发布目标不符")
        record["dependencies"] = metadata.get_all("Requires-Dist", [])
        prefix = metadata_paths[0].removesuffix("METADATA")
        if prefix + "entry_points.txt" not in archive.namelist():
            return None, None
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read_string(archive.read(prefix + "entry_points.txt").decode())
        entries = [
            (kind, name, target)
            for kind, group in (("module", "akaribot.modules"), ("adapter", "akaribot.adapters"))
            if config.has_section(group)
            for name, target in config.items(group)
        ]
        if not entries:
            return None, None
        if len(entries) != 1:
            raise ReleaseError("模块或适配器 wheel 必须声明唯一的 entry point")
        kind, name, target = entries[0]
        root = target.replace(".", "/")
        if ":" in root:
            raise ReleaseError("模块或适配器 entry point 必须指向导入包")
        with tempfile.TemporaryDirectory(prefix="akari-release-metadata-") as tmp:
            base = Path(tmp)
            for item in archive.infolist():
                path = base / item.filename
                if not path.resolve().is_relative_to(base.resolve()):
                    raise ReleaseError("wheel 含有越界路径")
                if not item.is_dir() and (item.filename.startswith(root + "/") or record["dist"] == "akari-bot-core"):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(archive.read(item))
            package_root = base / root
            manifest = build_registry.read_manifest("wheel", package_root)
            package = build_registry.Package(
                kind,
                name,
                record["dist"],
                record["version"],
                metadata.get("Summary", ""),
                target,
                "wheel",
                package_root,
                manifest,
            )
            if record["dist"] == "akari-bot-core":
                return "core", {
                    "dist": record["dist"],
                    "latest": record["version"],
                    "api_version": build_registry.core_api_version([package]),
                }
            entry = build_registry.build_entry(package, {record["dist"]: (record["wheel_url"], record["wheel_sha256"])})
            return "modules" if kind == "module" else "adapters", entry


def _merge(ledger: dict, record: dict) -> dict:
    if ledger.get("schema") != 1:
        raise ReleaseError("发布账本 schema 不受支持")
    channel = "prerelease" if Version(record["version"]).is_prerelease else "stable"
    releases = ledger.setdefault("channels", {}).setdefault(channel, {})
    previous = releases.get(record["dist"])
    if previous is not None:
        if Version(previous["version"]) > Version(record["version"]):
            raise ReleaseError("拒绝用旧版本回退发布账本")
        if Version(previous["version"]) == Version(record["version"]) and previous["files"] != record["files"]:
            raise ReleaseError("同版本发布产物 SHA256 与账本不符")
    releases[record["dist"]] = record
    history = ledger.setdefault("history", {}).setdefault(channel, {}).setdefault(record["dist"], {})
    if previous is not None:
        history.setdefault(previous["version"], previous)
    history[record["version"]] = record
    return ledger


def _registry(ledger: dict, channel: str) -> dict:
    releases = dict(ledger.get("channels", {}).get("stable", {}))
    if channel == "prerelease":
        for name, record in ledger.get("channels", {}).get("prerelease", {}).items():
            if name not in releases or Version(record["version"]) > Version(releases[name]["version"]):
                releases[name] = record
    history = {name: dict(versions) for name, versions in ledger.get("history", {}).get("stable", {}).items()}
    if channel == "prerelease":
        for name, versions in ledger.get("history", {}).get("prerelease", {}).items():
            history.setdefault(name, {}).update(versions)
    candidates = dict(ledger.get("history", {}).get("stable", {}).get("akari-bot-core", {}))
    if channel == "prerelease":
        candidates.update(ledger.get("history", {}).get("prerelease", {}).get("akari-bot-core", {}))
    if "akari-bot-core" in releases:
        candidate = releases["akari-bot-core"]
        candidates[candidate["version"]] = candidate
    core = {}
    for _, candidate in sorted(candidates.items(), key=lambda item: Version(item[0]), reverse=True):
        releases["akari-bot-core"] = candidate
        if _installable("akari-bot-core", releases, extras=("full",), history=history):
            core = candidate.get("entry") or {}
            break
    result = {
        "schema": 1,
        "generated_at": max((record["published_at"] for record in releases.values()), default=""),
        "core": core,
        "modules": [],
        "adapters": [],
    }
    for _, record in sorted(releases.items()):
        entry, section = record.get("entry"), record.get("section")
        if section not in ("modules", "adapters") or not core:
            continue
        versions = {**history.get(record["dist"], {}), record["version"]: record}
        for _, candidate in sorted(versions.items(), key=lambda item: Version(item[0]), reverse=True):
            entry = candidate.get("entry")
            selected = {**releases, record["dist"]: candidate}
            if entry and _installable(record["dist"], selected, history=history):
                if SpecifierSet(entry["requires_core_api"]).contains(str(core["api_version"])):
                    result[section].append(entry)
                    break
    return result


def _installable(
    name: str, releases: dict, extras: tuple = (), seen: frozenset = frozenset(), history: dict | None = None
) -> bool:
    record = releases.get(name)
    if record is None:
        return False
    identity = (name, record["version"], extras)
    if identity in seen:
        return True
    seen = seen | {identity}
    for text in record.get("dependencies", []):
        requirement = Requirement(text)
        if requirement.marker is not None and not any(
            requirement.marker.evaluate({"extra": extra}) for extra in ("", *extras)
        ):
            continue
        dependency = canonicalize_name(requirement.name)
        if dependency not in {
            "akari-bot-core",
            "akari-bot-cli",
            "akari-bot-html2text",
            "akari-bot-testing",
        } and not dependency.startswith(("akari-bot-assets-", "akari-bot-module-", "akari-bot-adapter-")):
            continue
        target = releases.get(dependency)
        candidates = dict((history or {}).get(dependency, {}))
        if target is not None:
            candidates[target["version"]] = target
        if not any(
            requirement.specifier.contains(candidate["version"], prereleases=True)
            and _installable(
                dependency,
                {**releases, dependency: candidate},
                tuple(sorted(requirement.extras)),
                seen,
                history,
            )
            for candidate in candidates.values()
        ):
            return False
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="核验 PyPI 产物并更新发布账本")
    parser.add_argument("action", choices=("manifest", "prepare-upload", "verify", "merge", "record"))
    parser.add_argument("--dist", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--dist-dir", type=Path, default=Path("dist"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--record", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == "manifest":
            _write(args.output, _manifest(args.dist_dir, args.dist, args.version))
        elif args.action == "prepare-upload":
            if args.manifest is None:
                raise ReleaseError("prepare-upload 必须提供原始构建清单")
            expected = _json(args.manifest)
            if expected["dist"] != canonicalize_name(args.dist) or Version(expected["version"]) != Version(
                args.version
            ):
                raise ReleaseError("原始构建清单与上传目标不符")
            missing = _prepare_upload(args.dist_dir, expected, args.output)
            print(f"本次待上传文件：{missing}")
        elif args.action != "merge":
            record, contents = _published(args.dist, args.version, _json(args.manifest) if args.manifest else None)
            record["section"], record["entry"] = _entry(record, contents)
            if args.action == "verify":
                _write(args.output, record)
        if args.action in ("merge", "record"):
            if args.action == "merge":
                if args.record is None:
                    raise ReleaseError("merge 必须提供核验记录")
                record = _json(args.record)
                if record["dist"] != canonicalize_name(args.dist) or Version(record["version"]) != Version(
                    args.version
                ):
                    raise ReleaseError("核验记录与发布目标不符")
            ledger_path = args.output / "releases.json"
            ledger = _json(ledger_path) if ledger_path.is_file() else {"schema": 1, "channels": {}}
            ledger = _merge(ledger, record)
            stable = _registry(ledger, "stable")
            prerelease = _registry(ledger, "prerelease")
            _write(ledger_path, ledger)
            _write(args.output / "registry.json", stable)
            _write(args.output / "registry-prerelease.json", prerelease)
    except (
        ReleaseError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        zipfile.BadZipFile,
        configparser.Error,
        build_registry.ConfigError,
    ) as error:
        print(f"发布核验失败：{error}", file=sys.stderr)
        return 2
    print(f"发布核验通过：{args.dist} {args.version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
