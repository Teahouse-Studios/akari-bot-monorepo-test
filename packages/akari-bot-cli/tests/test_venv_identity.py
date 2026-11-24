"""环境（venv）归属判定：区分“同一个环境”与“同一个基础解释器”。

uv 建的 venv 都把 ``bin/python`` 指向同一个基础解释器，按 ``resolve()`` 后的文件比较会把两个
不同的 venv 判成同一个环境，``venv adopt`` / ``venv release`` 因此被误拒。判据因此取环境根目录。
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli.venv import environment_root
from akaribot.testing import Tester, func_case


def _make_venv(root: Path, name: str = ".venv", *, python: str = "python") -> Path:
    # 创建一个带 pyvenv.cfg 的模拟 venv，返回其中的解释器路径。
    bin_dir = root / name / ("Scripts" if python.endswith(".exe") else "bin")
    bin_dir.mkdir(parents=True)
    (root / name / "pyvenv.cfg").write_text("home = /usr/bin\n", encoding="utf-8")
    interpreter = bin_dir / ("python.exe" if python.endswith(".exe") else python)
    interpreter.write_text("", encoding="utf-8")
    return interpreter


async def _test_two_venvs_are_distinct():
    with TemporaryDirectory() as raw:
        base = Path(raw)
        first = _make_venv(base / "one")
        second = _make_venv(base / "two")
        # 使用 resolve() 处理，因为 macOS 临时目录本身为符号链接，环境根目录按真实路径返回。
        one = (base / "one" / ".venv").resolve()
        two = (base / "two" / ".venv").resolve()
        return (
            environment_root(first) == one
            and environment_root(second) == two
            and environment_root(first) != environment_root(second)
        )


async def _test_same_venv_is_identical():
    with TemporaryDirectory() as raw:
        base = Path(raw)
        interpreter = _make_venv(base)
        return environment_root(interpreter) == environment_root(interpreter.parent / "python")


async def _test_bare_interpreter_is_not_a_venv():
    # 不存在 pyvenv.cfg 时不属于虚拟环境，按解释器自身位置归类，以免将系统 Python 误识别为虚拟环境。
    with TemporaryDirectory() as raw:
        base = Path(raw)
        bare = base / "bin" / "python3"
        bare.parent.mkdir(parents=True)
        bare.write_text("", encoding="utf-8")
        return environment_root(bare) == (base / "bin").resolve()


@func_case
async def test_venv_identity(tester: Tester):
    """cli.venv 环境所属范围判定测试"""
    await tester.test(_test_two_venvs_are_distinct, "两个 venv 判为不同环境")
    await tester.test(_test_same_venv_is_identical, "同一 venv 的不同解释器名判为同一环境")
    await tester.test(_test_bare_interpreter_is_not_a_venv, "裸解释器不算 venv")
    return tester
