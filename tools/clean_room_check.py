"""净室安装验证：用发布形态的 wheel 验证用户侧安装体验（T6.6）。

workspace 的开发期覆盖会丢弃内部版本约束（`[tool.uv.sources]` 让任何约束都能装上），
因此必须有一处跑「从 wheel 装」的路径：本工具构建全部包，再在全新 venv 里按组合安装，
最后用 ``PackageRegistry.discover()`` 断言发现结果与兼容性。发布前必跑。

用法：:

    python tools/clean_room_check.py                    # 全部组合
    python tools/clean_room_check.py --combo core       # 只跑最小组合
    python tools/clean_room_check.py --combo cli        # 只跑 CLI 组合（P1-1 / P1-9 回归）
    python tools/clean_room_check.py --keep-dist        # 复用已有 dist/
    python tools/clean_room_check.py --offline          # 只用 UV_CACHE_DIR 里的缓存，无外网时用
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from urllib.request import urlopen

from packaging.utils import parse_wheel_filename

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
CORE = "akari-bot-core"
CLI = "akari-bot-cli"

# CLI 组合名：只装 CLI wheel，装完逐条跑冒烟命令。这条守的是 P1-1（wheel 干净安装后不得缺依赖）
# 与 P1-9（--version 可用）；tui --self-check 覆盖包内资源与样式表，冻结产物最容易在这里失败。
CLI_COMBO = "cli"
CLI_SMOKE_COMMANDS: tuple[tuple[str, ...], ...] = (
    ("--version",),
    ("--help",),
    ("new", "--help"),
    ("tui", "--self-check"),
    ("new", "module", "release_probe", "--non-interactive", "--no-add"),
    ("new", "adapter", "release_probe", "--non-interactive", "--no-add"),
)

# 发现阶段要读实例配置（真实用户也先跑 akaribot init），故探针自带一份最小配置。
MINIMAL_CONFIG = """default_locale = "zh_cn"
config_version = 5

[config]
debug = false

[secret]
db_path = "sqlite://database/save.db"
"""

# 断言脚本：在新环境里执行，输出 JSON 供本工具判定。
PROBE = """
import json
from akaribot.core.registry import PackageRegistry as R
R.discover()
print(json.dumps({
    "modules": sorted(R.modules()),
    "adapters": sorted(R.adapters()),
    "incompatible": {k: str(v) for k, v in R.incompatible().items()},
}))
"""


def venv_python(venv: Path) -> Path:
    """返回 venv 里的解释器路径。

    :param venv: venv 根目录。
    :return: 解释器路径；Windows 为 ``Scripts/python.exe``。
    """
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def venv_script(venv: Path, name: str) -> Path:
    """返回 venv 里的可执行脚本路径。

    :param venv: venv 根目录。
    :param name: 脚本名，如 ``akaribot``。
    :return: 脚本路径；Windows 带 ``.exe`` 后缀。
    """
    if os.name == "nt":
        return venv / "Scripts" / f"{name}.exe"
    return venv / "bin" / name


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    """执行命令并捕获输出。

    :param cmd: 命令与参数。
    :return: 完成结果。
    """
    return subprocess.run(cmd, capture_output=True, text=True, check=False, **kwargs)


def uv_cmd(arguments: list[str], offline: bool) -> list[str]:
    """拼一条 uv 命令。

    :param arguments: uv 的子命令与参数。
    :param offline: 是否只用本地缓存，无外网时用。
    :return: 完整命令行。
    """
    return ["uv", *(["--offline"] if offline else []), *arguments]


def workspace_members() -> tuple[list[str], list[str]]:
    """列出 workspace 的模块包与适配器包。

    :return: ``(模块分发包名， 适配器分发包名)``。
    """
    modules: list[str] = []
    adapters: list[str] = []
    for pyproject in sorted((REPO_ROOT / "packages").glob("**/pyproject.toml")):
        text = pyproject.read_text(encoding="utf-8")
        name = next((line.split('"')[1] for line in text.splitlines() if line.startswith("name = ")), "")
        if name.startswith("akari-bot-module-"):
            modules.append(name)
        elif name.startswith("akari-bot-adapter-"):
            adapters.append(name)
    return modules, adapters


def stage_fresh_wheels(tmp: Path, source: Path | None = None) -> Path:
    """把本次构建的 wheel 复制到临时目录，作为安装时的 find-links 源。

    uv 对 ``--find-links`` 的本地 wheel 按来源路径缓存：同一路径上重建的同名同版本 wheel 会命中
    旧缓存，净室检查因此可能装到上一次的产物（实测把修好的 instance.py 装成了旧内容，检查结果
    既可能假绿也可能假红）。每次跑换一个全新目录即可绕开缓存；不封索引，依赖仍走 UV_CACHE_DIR，
    故离线可用。

    :param tmp: 本次组合的临时目录。
    :param source: wheel 来源目录；缺省为本仓库的 ``dist/``，TestPyPI 演练传下载目录。
    :return: 存放 wheel 的目录。
    """
    staged = tmp / "wheels"
    staged.mkdir()
    constraints = []
    for wheel in sorted((source or DIST_DIR).glob("*.whl")):
        target = staged / wheel.name
        shutil.copy2(wheel, target)
        distribution, _, _, _ = parse_wheel_filename(wheel.name)
        constraints.append(f"{distribution} @ {target.resolve().as_uri()}")
    (staged / "constraints.txt").write_text("\n".join(constraints) + "\n", encoding="utf-8")
    return staged


def fetch_url(url: str, attempts: int = 6) -> bytes:
    """带重试地取一个 URL，尊重 429/5xx 的 Retry-After。

    :param url: 目标地址。
    :param attempts: 最大尝试次数。
    :return: 响应内容。
    """
    from urllib.error import HTTPError

    for attempt in range(attempts):
        try:
            with urlopen(url, timeout=60) as response:
                return response.read()
        except HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt + 1 >= attempts:
                raise
            header = error.headers.get("Retry-After") if error.headers else None
            try:
                delay = max(1.0, float(header)) if header else min(300.0, 30.0 * (2**attempt))
            except ValueError:
                delay = min(300.0, 30.0 * (2**attempt))
            print(f"[{url}] 返回 {error.code}，{delay:.0f}s 后重试（第 {attempt + 1} 次）", file=sys.stderr)
            time.sleep(delay)
    raise RuntimeError(f"重试耗尽：{url}")


def download_release_files(index_url: str, manifest_path: Path, output: Path) -> bool:
    """从索引下载一批已发布产物，并按发行清单核验名称与 SHA256。

    这是「从索引取真实文件再安装」的前半段：TestPyPI 演练必须先证明远端文件与本次构建逐字节一致，
    否则后续安装验证的可能是别的产物。

    :param index_url: 索引根地址，如 ``https://test.pypi.org``。
    :param manifest_path: 批量发行清单。
    :param output: 下载目录。
    :return: 是否全部通过。
    """
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    dists = manifest.get("dists")
    if not isinstance(dists, dict) or not dists:
        print("发行清单缺少 dists", file=sys.stderr)
        return False
    output.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    for name, expected in sorted(dists.items()):
        version = expected["version"]
        url = f"{index_url.rstrip('/')}/pypi/{name}/{version}/json"
        try:
            payload = json.loads(fetch_url(url))
        except Exception as error:  # noqa: BLE001 - 单个分发失败记入清单后统一判定
            failures.append(f"{name}: 查询失败 {type(error).__name__}: {error}")
            continue
        files = {item["filename"]: item["digests"]["sha256"] for item in payload.get("urls", [])}
        if files != expected["files"]:
            failures.append(f"{name}: 索引文件集合或 SHA256 与清单不符")
            continue
        for item in payload["urls"]:
            contents = fetch_url(item["url"])
            if hashlib.sha256(contents).hexdigest() != files[item["filename"]]:
                failures.append(f"{name}: 下载 {item['filename']} 的 SHA256 不符")
                break
            (output / item["filename"]).write_bytes(contents)
        else:
            print(f"[{name}] {len(files)} 个文件核验通过")
    if failures:
        print("索引产物核验失败：", file=sys.stderr)
        for line in failures:
            print(f"    {line}", file=sys.stderr)
        return False
    print(f"索引产物核验通过：{len(dists)} 个分发")
    return True


def check_index_combo(index_url: str, offline: bool = False) -> bool:
    """直接从索引安装典型组合，验证索引本身可用（不借助本地 wheel）。

    :param index_url: 索引根地址。
    :param offline: 是否只用本地缓存；对索引安装无意义，保留以统一签名。
    :return: 是否通过。
    """
    name = "index"
    with tempfile.TemporaryDirectory(prefix="akari-clean-") as tmp:
        venv = Path(tmp) / "venv"
        created = run(uv_cmd(["venv", str(venv), "--python", "3.12"], offline), cwd=REPO_ROOT)
        if created.returncode != 0:
            print(f"[{name}] 建 venv 失败：{created.stderr[-400:]}")
            return False
        installed = run(
            uv_cmd(
                [
                    "pip",
                    "install",
                    "--python",
                    str(venv_python(venv)),
                    # 内部包来自被测索引，第三方依赖仍走正式 PyPI；同名冲突时按索引优先级解析。
                    "--index-url",
                    f"{index_url.rstrip('/')}/simple/",
                    "--extra-index-url",
                    "https://pypi.org/simple/",
                    "--index-strategy",
                    "unsafe-best-match",
                    CORE,
                    "akari-bot-adapter-telegram",
                    "akari-bot-module-wiki",
                ],
                offline,
            ),
            cwd=REPO_ROOT,
        )
        if installed.returncode != 0:
            print(f"[{name}] 从索引安装失败：")
            print(installed.stderr[-1500:], file=sys.stderr)
            return False
        (Path(tmp) / "config").mkdir(exist_ok=True)
        (Path(tmp) / "config" / "config.toml").write_text(MINIMAL_CONFIG, encoding="utf-8")
        probe = run(
            [str(venv_python(venv)), "-c", PROBE],
            cwd=tmp,
            env={
                **os.environ,
                "AKARI_INSTANCE_DIR": tmp,
                "AKARI_CONFIG_PATH": str(Path(tmp) / "config"),
                "AKARI_CONFIG_READONLY": "",
            },
        )
        if probe.returncode != 0:
            print(f"[{name}] 发现阶段失败：{probe.stderr[-800:]}", file=sys.stderr)
            return False
        data = json.loads(probe.stdout.strip().splitlines()[-1])
        ok = not data["incompatible"] and "wiki" in data["modules"]
        print(f"[{name}] 从索引装到 {len(data['modules'])} 个模块、{len(data['adapters'])} 个适配器")
        return ok


def build_all(offline: bool = False) -> bool:
    """构建全部包的 wheel。

    :param offline: 是否只用本地缓存，无外网时用。
    :return: 是否成功。
    """
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    result = run(uv_cmd(["build", "--all-packages", "--out-dir", str(DIST_DIR)], offline), cwd=REPO_ROOT)
    if result.returncode != 0:
        print(result.stdout[-2000:])
        print(result.stderr[-2000:], file=sys.stderr)
        return False
    wheels = sorted(DIST_DIR.glob("*.whl"))
    print(f"已构建 {len(wheels)} 个 wheel 到 {DIST_DIR}")
    return True


def check_combo(
    name: str, packages: list[str], extras: str = "", offline: bool = False, source: Path | None = None
) -> bool:
    """在全新 venv 里安装一组包并断言发现结果。

    :param name: 组合名，用于输出。
    :param packages: 要安装的分发包名。
    :param extras: 追加在 core 上的 extras，如 ``[s3]``。
    :param offline: 是否只用本地缓存，无外网时用。
    :param source: wheel 来源目录；缺省取本仓库 ``dist/``。
    :return: 是否通过。
    """
    with tempfile.TemporaryDirectory(prefix="akari-clean-") as tmp:
        venv = Path(tmp) / "venv"
        created = run(uv_cmd(["venv", str(venv), "--python", "3.12"], offline), cwd=REPO_ROOT)
        if created.returncode != 0:
            print(f"[{name}] 建 venv 失败：{created.stderr[-400:]}")
            return False
        targets = [f"{CORE}{extras}" if pkg == CORE else pkg for pkg in packages]
        staged = stage_fresh_wheels(Path(tmp), source)
        installed = run(
            uv_cmd(
                [
                    "pip",
                    "install",
                    "--python",
                    str(venv_python(venv)),
                    # 外部依赖从索引解析，内部约束同时限定到本次 wheel，防止远端版本掩盖源码遗漏。
                    "--find-links",
                    str(staged),
                    "--constraint",
                    str(staged / "constraints.txt"),
                    *targets,
                ],
                offline,
            ),
            cwd=REPO_ROOT,
        )
        if installed.returncode != 0:
            print(f"[{name}] 安装失败（这正是净室验证要拦的情况）：")
            print(installed.stderr[-1500:], file=sys.stderr)
            return False
        (Path(tmp) / "config").mkdir(exist_ok=True)
        (Path(tmp) / "config" / "config.toml").write_text(MINIMAL_CONFIG, encoding="utf-8")
        probe = run(
            [str(venv_python(venv)), "-c", PROBE],
            cwd=tmp,
            env={
                **os.environ,
                "AKARI_INSTANCE_DIR": tmp,
                "AKARI_CONFIG_PATH": str(Path(tmp) / "config"),
                "AKARI_CONFIG_READONLY": "",
            },
        )
        if probe.returncode != 0:
            print(f"[{name}] 发现阶段失败：{probe.stderr[-800:]}", file=sys.stderr)
            return False
        try:
            data = json.loads(probe.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            print(f"[{name}] 探针输出无法解析：{probe.stdout[-400:]}")
            return False

    modules, adapters = data["modules"], data["adapters"]
    expected = {pkg.removeprefix("akari-bot-module-") for pkg in packages if pkg.startswith("akari-bot-module-")}
    missing = expected - set(modules)
    ok = not data["incompatible"] and not missing
    print(
        f"[{name}] 模块 {len(modules)} 个、适配器 {len(adapters)} 个、不兼容 {len(data['incompatible'])} 个"
        + ("" if ok else " ← 失败")
    )
    if data["incompatible"]:
        print(f"    不兼容：{data['incompatible']}")
    if missing:
        print(f"    未发现：{sorted(missing)}")
    return ok


def check_cli_combo(offline: bool = False, source: Path | None = None) -> bool:
    """只装 CLI wheel，跑命令冒烟并做依赖一致性检查。

    这条与其它组合不同：CLI 不依赖 core，验证点是「干净环境里 CLI 自己能不能跑起来」，
    安装时缺哪个依赖都会在这里暴露（P1-1 的 click 缺失即此类）。冒烟命令都在临时实例
    目录下执行，不读运行者的真实实例配置。

    :param offline: 是否只用本地缓存，无外网时用。
    :param source: wheel 来源目录；缺省取本仓库 ``dist/``。
    :return: 是否通过。
    """
    name = CLI_COMBO
    with tempfile.TemporaryDirectory(prefix="akari-clean-") as tmp:
        venv = Path(tmp) / "venv"
        created = run(uv_cmd(["venv", str(venv), "--python", "3.12"], offline), cwd=REPO_ROOT)
        if created.returncode != 0:
            print(f"[{name}] 建 venv 失败：{created.stderr[-400:]}")
            return False
        staged = stage_fresh_wheels(Path(tmp), source)
        installed = run(
            uv_cmd(
                [
                    "pip",
                    "install",
                    "--python",
                    str(venv_python(venv)),
                    "--find-links",
                    str(staged),
                    "--constraint",
                    str(staged / "constraints.txt"),
                    CLI,
                ],
                offline,
            ),
            cwd=REPO_ROOT,
        )
        if installed.returncode != 0:
            print(f"[{name}] 安装失败（这正是净室验证要拦的情况），uv 的解析错误会点名取不到的分发：")
            print(installed.stderr[-2000:], file=sys.stderr)
            if not offline:
                print("    无外网时加 --offline，并确认 UV_CACHE_DIR 里已有全部依赖。")
            return False

        binary = venv_script(venv, "akaribot")
        for arguments in CLI_SMOKE_COMMANDS:
            smoke = run(
                [str(binary), *arguments],
                cwd=tmp,
                env={**os.environ, "AKARI_INSTANCE_DIR": tmp, "AKARIBOT_HOME": str(Path(tmp) / "cli-home")},
            )
            label = " ".join(("akaribot", *arguments))
            if smoke.returncode != 0:
                print(f"[{name}] {label} 退出 {smoke.returncode}：")
                print(f"    stdout: {smoke.stdout[-500:]}")
                print(f"    stderr: {smoke.stderr[-800:]}", file=sys.stderr)
                return False
            print(f"[{name}] {label} 退出 0")

        checked = run(uv_cmd(["pip", "check", "--python", str(venv_python(venv))], offline), cwd=REPO_ROOT)
        if checked.returncode != 0:
            print(f"[{name}] uv pip check 未通过：{checked.stdout[-500:]}", file=sys.stderr)
            print(checked.stderr[-800:], file=sys.stderr)
            return False

    print(f"[{name}] CLI wheel 冒烟 {len(CLI_SMOKE_COMMANDS)} 条全部退出 0，uv pip check 通过")
    return True


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    parser = argparse.ArgumentParser(description="用发布形态的 wheel 验证净室安装（T6.6）。")
    parser.add_argument(
        "--combo", choices=["core", "core-full", "typical", "all", "random", "index", CLI_COMBO], default=None
    )
    parser.add_argument("--random-count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--keep-dist", action="store_true", help="复用已有 dist/，不重新构建")
    parser.add_argument(
        "--index-url",
        default=None,
        help="从该索引拉取已发布产物再安装（如 https://test.pypi.org），此时不重新构建",
    )
    parser.add_argument("--manifest", type=Path, help="索引模式必填：批量发行清单，用于核验远端文件 SHA256")
    parser.add_argument("--download-dir", type=Path, default=Path("dist-indexed"), help="索引产物的下载目录")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="所有 uv 调用加 --offline，只用 UV_CACHE_DIR 里的缓存；无外网时用，缺包会直接点名",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="排除的分发包，可重复；用于隔离已知阻塞后验证其余组合",
    )
    args = parser.parse_args(argv)

    wheel_source = DIST_DIR
    if args.index_url:
        if args.manifest is None:
            print("--index-url 需要同时提供 --manifest", file=sys.stderr)
            return 1
        if args.download_dir.exists():
            shutil.rmtree(args.download_dir)
        if not download_release_files(args.index_url, args.manifest, args.download_dir):
            return 1
        wheel_source = args.download_dir
    elif not args.keep_dist or not DIST_DIR.exists():
        if not build_all(offline=args.offline):
            return 1

    modules, adapters = workspace_members()
    if args.exclude:
        excluded = set(args.exclude)
        modules = [name for name in modules if name not in excluded]
        adapters = [name for name in adapters if name not in excluded]
        print(f"已排除 {sorted(excluded)}")

    rng = random.Random(args.seed)
    sample = sorted(rng.sample(modules, min(args.random_count, len(modules))))
    combos: dict[str, tuple[list[str], str]] = {
        "core": ([CORE], ""),
        "core-full": ([CORE], "[full]"),
        "typical": ([CORE, "akari-bot-adapter-telegram", "akari-bot-module-wiki"], ""),
        "all": ([CORE, *modules, *adapters], ""),
        "random": ([CORE, *sample], ""),
    }

    combos["index"] = ([CORE], "")
    selected = [args.combo] if args.combo else [*combos, CLI_COMBO]
    if "index" in selected and not args.index_url:
        print("index 组合需要 --index-url", file=sys.stderr)
        return 1

    if not modules and any(name != CLI_COMBO for name in selected):
        print("没有发现模块包，检查 packages/ 布局。", file=sys.stderr)
        return 1

    failures: list[str] = []
    for name in selected:
        if name == CLI_COMBO:
            # CLI 组合只装 CLI wheel，与发现阶段的探针无关，单独走一条检查路径。
            passed = check_cli_combo(offline=args.offline, source=wheel_source)
        elif name == "index":
            passed = check_index_combo(args.index_url, offline=args.offline)
        else:
            passed = check_combo(name, *combos[name], offline=args.offline, source=wheel_source)  # (包列表， extras)
        if not passed:
            failures.append(name)
    print()
    if failures:
        print(f"净室验证失败：{failures}")
        return 1
    print(f"净室验证通过：{selected}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
