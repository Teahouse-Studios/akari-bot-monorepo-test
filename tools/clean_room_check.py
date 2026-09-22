"""净室安装验证：用发布形态的 wheel 验证用户侧安装体验（T6.6）。

workspace 的开发期覆盖会丢弃内部版本约束（`[tool.uv.sources]` 让任何约束都能装上），
因此必须有一处跑「从 wheel 装」的路径：本工具构建全部包，再在全新 venv 里按组合安装，
最后用 ``PackageRegistry.discover()`` 断言发现结果与兼容性。发布前必跑。

用法::

    python tools/clean_room_check.py                    # 全部组合
    python tools/clean_room_check.py --combo core       # 只跑最小组合
    python tools/clean_room_check.py --combo cli        # 只跑 CLI 组合（P1-1 / P1-9 回归）
    python tools/clean_room_check.py --keep-dist        # 复用已有 dist/
    python tools/clean_room_check.py --offline          # 只用 UV_CACHE_DIR 里的缓存，无外网时用
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

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

    :return: ``(模块分发包名, 适配器分发包名)``。
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


def stage_fresh_wheels(tmp: Path) -> Path:
    """把本次构建的 wheel 复制到临时目录，作为安装时的 find-links 源。

    uv 对 ``--find-links`` 的本地 wheel 按来源路径缓存：同一路径上重建的同名同版本 wheel 会命中
    旧缓存，净室检查因此可能装到上一次的产物（实测把修好的 instance.py 装成了旧内容，检查结果
    既可能假绿也可能假红）。每次跑换一个全新目录即可绕开缓存；不封索引，依赖仍走 UV_CACHE_DIR，
    故离线可用。

    :param tmp: 本次组合的临时目录。
    :return: 存放 wheel 的目录。
    """
    staged = tmp / "wheels"
    staged.mkdir()
    for wheel in sorted(DIST_DIR.glob("*.whl")):
        shutil.copy2(wheel, staged / wheel.name)
    return staged


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


def check_combo(name: str, packages: list[str], extras: str = "", offline: bool = False) -> bool:
    """在全新 venv 里安装一组包并断言发现结果。

    :param name: 组合名，用于输出。
    :param packages: 要安装的分发包名。
    :param extras: 追加在 core 上的 extras，如 ``[s3]``。
    :param offline: 是否只用本地缓存，无外网时用。
    :return: 是否通过。
    """
    with tempfile.TemporaryDirectory(prefix="akari-clean-") as tmp:
        venv = Path(tmp) / "venv"
        created = run(uv_cmd(["venv", str(venv), "--python", "3.12"], offline), cwd=REPO_ROOT)
        if created.returncode != 0:
            print(f"[{name}] 建 venv 失败：{created.stderr[-400:]}")
            return False
        targets = [f"{CORE}{extras}" if pkg == CORE else pkg for pkg in packages]
        installed = run(
            uv_cmd(
                [
                    "pip",
                    "install",
                    "--python",
                    str(venv / "bin" / "python"),
                    # 不封索引：akari-bot-i18n / webrender / webui 是发布在 PyPI 的独立库，
                    # 封了索引连最小组合都解不开；被验证的官方包本身不在 PyPI，仍只来自本地 wheel。
                    "--find-links",
                    str(stage_fresh_wheels(Path(tmp))),
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
            [str(venv / "bin" / "python"), "-c", PROBE],
            cwd=tmp,
            env={**os.environ, "AKARI_INSTANCE_DIR": tmp},
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


def check_cli_combo(offline: bool = False) -> bool:
    """只装 CLI wheel，跑命令冒烟并做依赖一致性检查。

    这条与其它组合不同：CLI 不依赖 core，验证点是「干净环境里 CLI 自己能不能跑起来」，
    安装时缺哪个依赖都会在这里暴露（P1-1 的 click 缺失即此类）。冒烟命令都在临时实例
    目录下执行，不读运行者的真实实例配置。

    :param offline: 是否只用本地缓存，无外网时用。
    :return: 是否通过。
    """
    name = CLI_COMBO
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
                    str(venv / "bin" / "python"),
                    "--find-links",
                    str(stage_fresh_wheels(Path(tmp))),
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

        binary = venv / "bin" / "akaribot"
        for arguments in CLI_SMOKE_COMMANDS:
            smoke = run([str(binary), *arguments], cwd=tmp, env={**os.environ, "AKARI_INSTANCE_DIR": tmp})
            label = " ".join(("akaribot", *arguments))
            if smoke.returncode != 0:
                print(f"[{name}] {label} 退出 {smoke.returncode}：")
                print(f"    stdout: {smoke.stdout[-500:]}")
                print(f"    stderr: {smoke.stderr[-800:]}", file=sys.stderr)
                return False
            print(f"[{name}] {label} 退出 0")

        checked = run(uv_cmd(["pip", "check", "--python", str(venv / "bin" / "python")], offline), cwd=REPO_ROOT)
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
    parser.add_argument("--combo", choices=["core", "core-full", "typical", "all", "random", CLI_COMBO], default=None)
    parser.add_argument("--random-count", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--keep-dist", action="store_true", help="复用已有 dist/，不重新构建")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="所有 uv 调用加 --offline，只用 UV_CACHE_DIR 里的缓存；无外网时用，缺包会直接点名",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="排除的分发包，可重复；用于隔离已知阻塞（如 langconv 的 git 直链依赖）后验证其余组合",
    )
    args = parser.parse_args(argv)

    if not args.keep_dist or not DIST_DIR.exists():
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
        "core-full": ([CORE], "[s3,image]"),
        "typical": ([CORE, "akari-bot-adapter-telegram", "akari-bot-module-wiki"], ""),
        "all": ([CORE, *modules, *adapters], ""),
        "random": ([CORE, *sample], ""),
    }

    selected = [args.combo] if args.combo else [*combos, CLI_COMBO]
    if not modules and any(name != CLI_COMBO for name in selected):
        print("没有发现模块包，检查 packages/ 布局。", file=sys.stderr)
        return 1

    failures: list[str] = []
    for name in selected:
        if name == CLI_COMBO:
            # CLI 组合只装 CLI wheel，与发现阶段的探针无关，单独走一条检查路径。
            passed = check_cli_combo(offline=args.offline)
        else:
            passed = check_combo(name, *combos[name], offline=args.offline)  # (包列表, extras)
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
