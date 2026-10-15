import copy
import hashlib
import io
import json
import tempfile
import zipfile
from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch

from akaribot.testing import Tester, func_case
from tools import publish_registry as tool


def _wheel(dist="akari-bot-module-sample", version="0.1.0", *, console=False):
    stream = io.BytesIO()
    prefix = dist.replace("-", "_") + "-" + version + ".dist-info/"
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr(prefix + "METADATA", f"Name: {dist}\nVersion: {version}\nSummary: 示例\n")
        archive.writestr(
            prefix + "entry_points.txt",
            "[console_scripts]\nexample = example:main\n"
            if console
            else "[akaribot.modules]\nsample = akaribot.modules.sample\n",
        )
        archive.writestr(
            "akaribot/modules/sample/manifest.toml",
            'schema = 1\nrequires_core_api = ">=1,<2"\nprovides_modules = ["sample"]\n',
        )
        archive.writestr("akaribot/modules/sample/locales/zh_cn.json", '{"sample.help.desc":"示例模块"}')
    return stream.getvalue()


def _record(dist="akari-bot-module-sample", version="0.1.0"):
    return {
        "dist": dist,
        "version": version,
        "published_at": "2026-01-01T00:00:00Z",
        "files": {"sample.whl": "abc"},
        "wheel_url": "https://files.pythonhosted.org/sample.whl",
        "wheel_sha256": "abc",
        "section": "modules",
        "entry": {"dist": dist, "latest": version, "requires_core_api": ">=1,<2"},
    }


def _ledger():
    core = _record("akari-bot-core")
    core.update(section="core", entry={"dist": "akari-bot-core", "latest": "0.1.0", "api_version": 1})
    return {"schema": 1, "channels": {"stable": {"akari-bot-core": core}}}


def _remote(contents):
    wheel = "akari_bot_module_sample-0.1.0-py3-none-any.whl"
    sdist = "akari_bot_module_sample-0.1.0.tar.gz"
    payload = {
        "info": {"name": "akari-bot-module-sample", "version": "0.1.0"},
        "urls": [
            {
                "filename": name,
                "packagetype": kind,
                "url": "https://files.pythonhosted.org/" + name,
                "digests": {"sha256": hashlib.sha256(data).hexdigest()},
                "upload_time_iso_8601": "2026-01-01T00:00:00Z",
                "yanked": False,
            }
            for name, kind, data in ((wheel, "bdist_wheel", contents), (sdist, "sdist", b"sdist"))
        ],
    }
    expected = {
        "dist": "akari-bot-module-sample",
        "version": "0.1.0",
        "files": {item["filename"]: item["digests"]["sha256"] for item in payload["urls"]},
    }
    responses = {
        "https://pypi.org/pypi/akari-bot-module-sample/0.1.0/json": json.dumps(payload).encode(),
        "https://files.pythonhosted.org/" + wheel: contents,
        "https://files.pythonhosted.org/" + sdist: b"sdist",
    }
    return payload, expected, responses


def _test_verified_artifacts_provide_metadata():
    contents = _wheel()
    _, expected, responses = _remote(contents)
    with patch.object(tool, "_download", side_effect=responses.__getitem__):
        record, wheel = tool._published("akari-bot-module-sample", "0.1.0", expected)
    section, entry = tool._entry(record, wheel)
    return (
        section == "modules"
        and entry["summary"] == {"zh_cn": "示例模块"}
        and entry["sha256"] == hashlib.sha256(contents).hexdigest()
    )


def _test_partial_upload_is_rejected():
    contents = _wheel()
    payload, expected, responses = _remote(contents)
    payload["urls"].pop()
    responses[next(iter(responses))] = json.dumps(payload).encode()
    with patch.object(tool, "_download", side_effect=responses.__getitem__):
        try:
            tool._published("akari-bot-module-sample", "0.1.0", expected)
        except tool.ReleaseError:
            return True
    return False


def _test_corrupt_download_is_rejected():
    contents = _wheel()
    _, expected, responses = _remote(contents)
    responses["https://files.pythonhosted.org/akari_bot_module_sample-0.1.0-py3-none-any.whl"] = b"corrupt"
    with patch.object(tool, "_download", side_effect=responses.__getitem__):
        try:
            tool._published("akari-bot-module-sample", "0.1.0", expected)
        except tool.ReleaseError:
            return True
    return False


def _test_non_registry_distribution_is_recorded():
    record = _record("akari-bot-cli")
    record["section"], record["entry"] = tool._entry(record, _wheel("akari-bot-cli", console=True))
    ledger = tool._merge(_ledger(), record)
    return "akari-bot-cli" in ledger["channels"]["stable"] and not tool._registry(ledger, "stable")["modules"]


def _test_neighbor_release_is_preserved():
    ledger = tool._merge(_ledger(), _record("akari-bot-module-neighbor", "0.2.0"))
    original = copy.deepcopy(ledger["channels"]["stable"]["akari-bot-module-neighbor"])
    ledger = tool._merge(ledger, _record())
    return ledger["channels"]["stable"]["akari-bot-module-neighbor"] == original


def _test_old_version_and_changed_hash_are_rejected():
    ledger = tool._merge(_ledger(), _record(version="0.2.0"))
    errors = 0
    altered = _record(version="0.2.0")
    altered["files"] = {"sample.whl": "different"}
    for candidate in (_record(), altered):
        try:
            tool._merge(copy.deepcopy(ledger), candidate)
        except tool.ReleaseError:
            errors += 1
    return errors == 2


def _test_same_release_is_idempotent():
    ledger = tool._merge(_ledger(), _record())
    original = copy.deepcopy(ledger)
    return tool._merge(ledger, _record()) == original


def _test_prerelease_keeps_stable_index():
    ledger = tool._merge(_ledger(), _record())
    stable = tool._registry(ledger, "stable")
    tool._merge(ledger, _record(version="0.2.0rc1"))
    prerelease = tool._registry(ledger, "prerelease")
    return tool._registry(ledger, "stable") == stable and prerelease["modules"][0]["latest"] == "0.2.0rc1"


def _test_index_requires_published_compatible_core():
    empty = tool._merge({"schema": 1, "channels": {}}, _record())
    incompatible = _ledger()
    incompatible["channels"]["stable"]["akari-bot-core"]["entry"]["api_version"] = 2
    tool._merge(incompatible, _record())
    return not tool._registry(empty, "stable")["modules"] and not tool._registry(incompatible, "stable")["modules"]


def _test_build_manifest_rejects_mixed_packages():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "akari_bot_module_sample-0.1.0-py3-none-any.whl").write_bytes(_wheel())
        (root / "akari_bot_module_other-0.1.0.tar.gz").write_bytes(b"sdist")
        try:
            tool._manifest(root, "akari-bot-module-sample", "0.1.0")
        except tool.ReleaseError:
            return True
    return False


def _test_missing_full_assets_delay_core_index():
    ledger = _ledger()
    ledger["channels"]["stable"]["akari-bot-core"]["dependencies"] = [
        'akari-bot-assets-brand>=0.1.0,<1.0; extra == "full"',
        'akari-bot-assets-emotes>=0.1.0,<1.0; extra == "full"',
    ]
    tool._merge(ledger, _record())
    before = tool._registry(ledger, "stable")
    for name in ("akari-bot-assets-brand", "akari-bot-assets-emotes"):
        record = _record(name)
        record.update(section=None, entry=None)
        tool._merge(ledger, record)
    after = tool._registry(ledger, "stable")
    return not before["core"] and not before["modules"] and after["core"]["latest"] == "0.1.0" and after["modules"]


def _test_dependency_version_mismatch_delays_module():
    ledger = _ledger()
    record = _record()
    record["dependencies"] = ["akari-bot-html2text>=0.2.0,<1.0"]
    tool._merge(ledger, record)
    dependency = _record("akari-bot-html2text", "0.1.0")
    dependency.update(section=None, entry=None)
    tool._merge(ledger, dependency)
    unavailable = tool._registry(ledger, "stable")
    dependency = copy.deepcopy(dependency)
    dependency["version"] = "0.2.0"
    tool._merge(ledger, dependency)
    return not unavailable["modules"] and len(tool._registry(ledger, "stable")["modules"]) == 1


def _test_merge_uses_verified_record_without_network():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        record = _record("akari-bot-cli")
        record.update(section=None, entry=None)
        source = root / "verified.json"
        source.write_text(json.dumps(record))
        with patch.object(tool, "_download", side_effect=AssertionError("merge 不应重新下载")):
            code = tool.main(
                [
                    "merge",
                    "--dist",
                    "akari-bot-cli",
                    "--version",
                    "0.1.0",
                    "--record",
                    str(source),
                    "--output",
                    str(root / "pages"),
                ]
            )
        ledger = json.loads((root / "pages/releases.json").read_text())
    return code == 0 and "akari-bot-cli" in ledger["channels"]["stable"]


def _test_unready_core_upgrade_keeps_available_version():
    ledger = tool._merge(_ledger(), _record())
    core = _record("akari-bot-core", "0.2.0")
    core.update(
        section="core",
        entry={"dist": "akari-bot-core", "latest": "0.2.0", "api_version": 1},
        dependencies=['akari-bot-assets-brand>=0.2.0,<1.0; extra == "full"'],
    )
    tool._merge(ledger, core)
    unavailable = tool._registry(ledger, "stable")
    brand = _record("akari-bot-assets-brand", "0.2.0")
    brand.update(section=None, entry=None)
    tool._merge(ledger, brand)
    available = tool._registry(ledger, "stable")
    return unavailable["core"]["latest"] == "0.1.0" and available["core"]["latest"] == "0.2.0"


def _test_failed_index_calculation_does_not_write_ledger():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "verified.json"
        source.write_text(json.dumps(_record("akari-bot-cli")))
        with patch.object(tool, "_registry", side_effect=tool.ReleaseError("invalid registry")):
            code = tool.main(
                [
                    "merge",
                    "--dist",
                    "akari-bot-cli",
                    "--version",
                    "0.1.0",
                    "--record",
                    str(source),
                    "--output",
                    str(root / "pages"),
                ]
            )
        return code == 2 and not (root / "pages/releases.json").exists()


def _test_module_upgrade_keeps_installable_history():
    ledger = tool._merge(_ledger(), _record())
    upgrade = _record(version="0.2.0")
    upgrade["dependencies"] = ["akari-bot-assets-fonts>=0.2.0,<1.0"]
    tool._merge(ledger, upgrade)
    before = tool._registry(ledger, "stable")
    fonts = _record("akari-bot-assets-fonts", "0.2.0")
    fonts.update(section=None, entry=None)
    tool._merge(ledger, fonts)
    after = tool._registry(ledger, "stable")
    return before["modules"][0]["latest"] == "0.1.0" and after["modules"][0]["latest"] == "0.2.0"


def _test_historical_dependency_keeps_core_installable():
    ledger = _ledger()
    ledger["channels"]["stable"]["akari-bot-core"]["dependencies"] = [
        'akari-bot-assets-brand>=0.1.0,<0.2.0; extra == "full"'
    ]
    for version in ("0.1.0", "0.2.0"):
        brand = _record("akari-bot-assets-brand", version)
        brand.update(section=None, entry=None)
        tool._merge(ledger, brand)
    return tool._registry(ledger, "stable")["core"]["latest"] == "0.1.0"


def _upload_case(existing, *, bad_hash=False):
    contents = _wheel()
    payload, expected, _ = _remote(contents)
    if bad_hash:
        payload["urls"][0]["digests"]["sha256"] = "different"
    payload["urls"] = payload["urls"][:existing]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        dist = root / "dist"
        dist.mkdir()
        (dist / "akari_bot_module_sample-0.1.0-py3-none-any.whl").write_bytes(contents)
        (dist / "akari_bot_module_sample-0.1.0.tar.gz").write_bytes(b"sdist")
        with patch.object(tool, "_download", return_value=json.dumps(payload).encode()):
            try:
                count = tool._prepare_upload(dist, expected, root / "upload")
            except tool.ReleaseError:
                return bad_hash and not (root / "upload").exists()
        names = {p.name for p in (root / "upload").iterdir()}
        return count == 2 - existing and names == set(expected["files"]) - {
            item["filename"] for item in payload["urls"]
        }


def _test_partial_upload_selects_only_missing():
    return _upload_case(1)


def _test_existing_changed_hash_blocks_upload():
    return _upload_case(1, bad_hash=True)


def _test_complete_existing_upload_is_noop():
    return _upload_case(2)


def _test_new_release_requires_404_for_empty_remote():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        dist = root / "dist"
        dist.mkdir()
        (dist / "akari_bot_module_sample-0.1.0-py3-none-any.whl").write_bytes(_wheel())
        (dist / "akari_bot_module_sample-0.1.0.tar.gz").write_bytes(b"sdist")
        expected = tool._manifest(dist, "akari-bot-module-sample", "0.1.0")
        with patch.object(tool, "_download", side_effect=HTTPError("url", 404, "missing", {}, None)):
            new = tool._prepare_upload(dist, expected, root / "new")
        with patch.object(tool, "_download", side_effect=HTTPError("url", 403, "forbidden", {}, None)):
            try:
                tool._prepare_upload(dist, expected, root / "forbidden")
            except HTTPError:
                return new == 2 and not (root / "forbidden").exists()
    return False


@func_case
async def test_publish_registry(tester: Tester):
    """发布产物、增量账本与渠道隔离验证。"""
    for function, label in (
        (_test_verified_artifacts_provide_metadata, "索引元数据取自哈希核验后的 wheel"),
        (_test_partial_upload_is_rejected, "部分上传不进入发布账本"),
        (_test_corrupt_download_is_rejected, "下载文件哈希不符时拒绝发布记录"),
        (_test_non_registry_distribution_is_recorded, "CLI 分发可以核验和登记"),
        (_test_neighbor_release_is_preserved, "增量发布保留其他分发记录"),
        (_test_old_version_and_changed_hash_are_rejected, "旧版本与同版本异哈希不能覆盖账本"),
        (_test_same_release_is_idempotent, "同一发布记录重复执行不产生变更"),
        (_test_prerelease_keeps_stable_index, "预发布不改变稳定索引"),
        (_test_index_requires_published_compatible_core, "索引仅提供与已发布 core 兼容的模块"),
        (_test_build_manifest_rejects_mixed_packages, "上传目录不得混入其他分发"),
        (_test_missing_full_assets_delay_core_index, "core 的 full 资源齐备后才启用索引"),
        (_test_dependency_version_mismatch_delays_module, "内部依赖版本满足后才提供模块"),
        (_test_merge_uses_verified_record_without_network, "并发重试复用核验记录并合并当前账本"),
        (_test_unready_core_upgrade_keeps_available_version, "core 升级依赖未齐时保留可安装版本"),
        (_test_failed_index_calculation_does_not_write_ledger, "索引计算失败时不落盘发布账本"),
        (_test_module_upgrade_keeps_installable_history, "模块升级依赖未齐时保留可安装版本"),
        (_test_historical_dependency_keeps_core_installable, "内部依赖可以使用符合约束的已发布历史版本"),
        (_test_partial_upload_selects_only_missing, "部分上传仅补传缺失文件"),
        (_test_existing_changed_hash_blocks_upload, "已存在异哈希产物拒绝补传"),
        (_test_complete_existing_upload_is_noop, "文件全部存在且同哈希时无需上传"),
        (_test_new_release_requires_404_for_empty_remote, "新版本仅允许明确的 PyPI 404 作为空发布状态"),
    ):
        await tester.test(function, label)
    return tester
