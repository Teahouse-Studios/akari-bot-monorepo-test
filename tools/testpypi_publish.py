"""按依赖顺序把一批产物串行发布到索引，并对限速做退避与限批。

索引对上传有速率限制（429）。本工具把三件事固定下来：一批只传一个分发、尊重响应里的
``Retry-After``、按「本次最多上传文件数」限批；中断后用同一批清单重跑即可续传（只补缺失文件）。

用法：::

    python tools/testpypi_publish.py --manifest release-batch.json --dist-dir dist \
        --token "$TESTPYPI_TOKEN" --summary publish-summary.json

    python tools/testpypi_publish.py --manifest release-batch.json --dist-dir dist --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLISH_REGISTRY = REPO_ROOT / "tools" / "publish_registry.py"
RETRY_HINT = re.compile(r"Retry-After[:\s]+(\d+)", re.IGNORECASE)
RATE_LIMITED = ("429", "Too Many Requests", "rate limit")


class RateLimited(RuntimeError):
    """索引要求等待超过本次可接受时长，留待下一窗口续传。"""

    def __init__(self, delay: int) -> None:
        super().__init__(f"索引限速，建议 {delay}s 后重跑")
        self.delay = delay


def check_tools(require_twine: bool = True) -> str | None:
    """确认发布脚本的依赖与 twine 可用。

    :param require_twine: 是否需要校验 twine；dry-run 不需要。
    :return: 缺失说明；齐备时返回 ``None``。
    """
    probe = subprocess.run([sys.executable, "-c", "import packaging"], capture_output=True, text=True, check=False)
    if probe.returncode != 0:
        return "缺少 packaging：先执行 python -m pip install packaging"
    if require_twine and shutil.which("twine") is None:
        return "缺少 twine：先执行 python -m pip install twine"
    return None


def publish_order(names: list[str]) -> list[str]:
    """按发布依赖顺序排列分发。

    :param names: 分发名列表。
    :return: 排好序的列表：资源与 html2text 在前，core、testing 次之，模块/适配器随后，CLI 最后。
    """

    def rank(name: str) -> tuple[int, str]:
        if name.startswith("akari-bot-assets-") or name == "akari-bot-html2text":
            return 0, name
        if name == "akari-bot-core":
            return 1, name
        if name == "akari-bot-testing":
            return 2, name
        if name == "akari-bot-cli":
            return 4, name
        return 3, name

    return sorted(names, key=rank)


def stage(directory: Path, entry: dict, dist_dir: Path) -> None:
    """把单个分发的产物复制到独立目录。

    :param directory: 暂存目录。
    :param entry: 清单中该分发的记录。
    :param dist_dir: 全部产物目录。
    """
    shutil.rmtree(directory, ignore_errors=True)
    directory.mkdir(parents=True)
    for name in entry["files"]:
        shutil.copy2(dist_dir / name, directory / name)


def project_exists(index_url: str, name: str) -> bool:
    """判断分发名是否已在索引上创建。

    新项目配额只对首次创设计数；已存在的项目发新版本不占该配额。

    :param index_url: 索引根地址。
    :param name: 分发名。
    :return: 已创建时为 ``True``。
    """
    url = f"{index_url.rstrip('/')}/pypi/{name}/json"
    for attempt in range(4):
        try:
            with urlopen(url, timeout=30) as response:  # noqa: S310 - 固定 https 索引地址
                response.read()
                return True
        except HTTPError as error:
            if error.code == 404:
                return False
            if error.code not in {429, 500, 502, 503, 504} or attempt + 1 >= 4:
                raise
            header = error.headers.get("Retry-After") if error.headers else None
            try:
                delay = max(1.0, float(header)) if header else min(300.0, 30.0 * (2**attempt))
            except ValueError:
                delay = min(300.0, 30.0 * (2**attempt))
            print(f"  项目探测返回 {error.code}，{delay:.0f}s 后重试", file=sys.stderr)
            time.sleep(delay)
    raise RuntimeError(f"项目探测重试耗尽：{name}")


def missing_files(dist: str, version: str, staged: Path, entry: dict, index_url: str) -> tuple[int, Path]:
    """调用发布清单工具计算本次待上传文件数。

    :param dist: 分发名。
    :param version: 版本。
    :param staged: 暂存目录。
    :param entry: 清单记录。
    :param index_url: 索引根地址。
    :return: 待上传文件数与暂存目录。
    """
    expected = Path(staged.parent) / "expected.json"
    expected.write_text(json.dumps({"dist": dist, **entry}), encoding="utf-8")
    output = Path(staged.parent) / "upload"
    shutil.rmtree(output, ignore_errors=True)
    result = subprocess.run(
        [
            sys.executable,
            str(PUBLISH_REGISTRY),
            "prepare-upload",
            "--dist",
            dist,
            "--version",
            version,
            "--dist-dir",
            str(staged),
            "--manifest",
            str(expected),
            "--index-url",
            index_url,
            "--output",
            str(output),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "prepare-upload 失败")
    return (len(list(output.iterdir())) if output.exists() else 0), output


def upload(staged: Path, repository_url: str, token: str, retries: int, max_wait: int) -> None:
    """上传一个分发的全部文件，遇到限速按 Retry-After 或指数退避重试。

    :param staged: 待上传目录。
    :param repository_url: 上传端点。
    :param token: API token。
    :param retries: 最大尝试次数。
    :param max_wait: 单次可接受的最长等待秒数；超过则留待下一窗口。
    """
    for attempt in range(retries):
        result = subprocess.run(
            [
                "twine",
                "upload",
                "--non-interactive",
                "--skip-existing",
                "--repository-url",
                repository_url,
                "--username",
                "__token__",
                "--password",
                token,
                *sorted(str(path) for path in staged.glob("*")),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return
        message = f"{result.stdout}\n{result.stderr}"
        if not any(marker.lower() in message.lower() for marker in RATE_LIMITED) or attempt + 1 >= retries:
            raise RuntimeError(message.strip()[-1500:])
        hint = RETRY_HINT.search(message)
        delay = int(hint.group(1)) if hint else min(300, 30 * (2**attempt))
        if delay > max_wait:
            raise RateLimited(delay)
        print(f"  被限速，{delay}s 后重试（第 {attempt + 1}/{retries} 次）", file=sys.stderr)
        time.sleep(delay)


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(description="按依赖顺序串行发布一批产物，内置限速退避与限批。")
    parser.add_argument("--manifest", type=Path, required=True, help="批量发行清单")
    parser.add_argument("--dist-dir", type=Path, required=True, help="本地产物目录")
    parser.add_argument("--index-url", default="https://test.pypi.org", help="查询索引根地址")
    parser.add_argument("--repository-url", default="https://test.pypi.org/legacy/", help="上传端点")
    parser.add_argument("--token", default=os.environ.get("TESTPYPI_TOKEN", ""), help="API token")
    parser.add_argument("--delay", type=float, default=3.0, help="两个分发之间的等待秒数")
    parser.add_argument("--max-dists", type=int, default=0, help="本次最多上传的分发数；0 表示不限")
    parser.add_argument(
        "--max-new-projects",
        type=int,
        default=18,
        help="本次最多创建的新项目数（配额单位）；已存在项目的版本上传不计入，0 表示不限",
    )
    parser.add_argument("--max-files", type=int, default=0, help="本次最多上传的文件数；0 表示不限")
    parser.add_argument("--max-wait", type=int, default=300, help="被限速时单次最长等待秒数，超过则留待下一窗口")
    parser.add_argument("--retries", type=int, default=6, help="单个分发的最大上传尝试次数")
    parser.add_argument("--dry-run", action="store_true", help="只列出本次会传什么")
    parser.add_argument("--summary", type=Path, help="把上传结果写成 JSON")
    args = parser.parse_args(argv)

    problem = check_tools(require_twine=not args.dry_run)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    dists = manifest.get("dists") or {}
    if not dists:
        print("发行清单缺少 dists", file=sys.stderr)
        return 1
    if not args.dry_run and not args.token:
        print("需要 --token 或 TESTPYPI_TOKEN", file=sys.stderr)
        return 1

    summary: dict = {
        "batch_id": manifest.get("batch_id", ""),
        "uploaded": [],
        "skipped": [],
        "remaining": [],
        "errors": [],
    }
    order = publish_order(list(dists))
    uploaded_files = 0
    uploaded_dists = 0
    new_projects = 0
    capped = False
    with tempfile.TemporaryDirectory(prefix="akari-testpypi-") as tmp:
        base = Path(tmp)
        for position, dist in enumerate(order, start=1):
            entry = dists[dist]
            version = entry["version"]
            try:
                is_new = not project_exists(args.index_url, dist)
                if is_new and args.max_new_projects and new_projects >= args.max_new_projects:
                    summary["remaining"].append(dist)
                    capped = True
                    print(f"[{position}/{len(order)}] {dist}: 新项目配额已用完（本次 {new_projects} 个），留待下一窗口")
                    continue
                stage(base / "dist", entry, args.dist_dir)
                count, upload_dir = missing_files(dist, version, base / "dist", entry, args.index_url)
            except RuntimeError as error:
                summary["errors"].append({"dist": dist, "message": str(error)})
                print(f"[{position}/{len(order)}] {dist}: 查询失败：{error}", file=sys.stderr)
                capped = True
                break
            if count == 0:
                summary["skipped"].append(dist)
                print(f"[{position}/{len(order)}] {dist} {version}: 已存在，跳过")
                continue
            if args.max_dists and uploaded_dists >= args.max_dists:
                summary["remaining"] = order[position - 1 :]
                capped = True
                print(
                    f"[{position}/{len(order)}] 达到本次分发上限（{args.max_dists} 个），"
                    f"剩余 {len(summary['remaining'])} 个分发留待下次运行"
                )
                break
            if args.max_files and uploaded_files + count > args.max_files:
                summary["remaining"] = order[position - 1 :]
                capped = True
                print(
                    f"[{position}/{len(order)}] 达到本次上限（{args.max_files} 个文件），"
                    f"剩余 {len(summary['remaining'])} 个分发留待下次运行"
                )
                break
            if args.dry_run:
                summary["uploaded"].append({"dist": dist, "files": count, "dry_run": True})
                print(f"[{position}/{len(order)}] {dist} {version}: 将上传 {count} 个文件")
                uploaded_files += count
                uploaded_dists += 1
                if is_new:
                    new_projects += 1
                continue
            try:
                upload(upload_dir, args.repository_url, args.token, args.retries, args.max_wait)
            except RateLimited as error:
                summary["remaining"] = order[position - 1 :]
                summary["rate_limited_after"] = error.delay
                print(f"[{position}/{len(order)}] {dist}: {error}；下一次运行会从该分发继续", file=sys.stderr)
                break
            except RuntimeError as error:
                summary["errors"].append({"dist": dist, "message": str(error)})
                summary["remaining"] = order[position - 1 :]
                print(f"[{position}/{len(order)}] {dist}: 上传失败：{error}", file=sys.stderr)
                break
            summary["uploaded"].append({"dist": dist, "files": count})
            uploaded_files += count
            uploaded_dists += 1
            if is_new:
                new_projects += 1
            print(f"[{position}/{len(order)}] {dist} {version}: 上传 {count} 个文件")
            if args.delay:
                time.sleep(args.delay)

    if args.summary:
        args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary["new_projects"] = new_projects
    print(
        f"上传 {len(summary['uploaded'])} 个分发 / {uploaded_files} 个文件（其中新建项目 {new_projects} 个），"
        f"跳过 {len(summary['skipped'])} 个，待续 {len(summary['remaining'])} 个，失败 {len(summary['errors'])} 个"
    )
    if capped or summary["remaining"]:
        print("本次未传完：用同一批清单再跑一次即可续传（只补缺失文件）。")
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
