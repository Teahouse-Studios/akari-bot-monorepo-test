"""临时的单测运行脚本，仅用于开发期跑单个测试入口。"""

import asyncio
import importlib.util
import os
import sys
import traceback
from pathlib import Path

# 以文件路径直接启动时，sys.path 首位是 tests/ 而非项目根，须先补上项目根；akaribot 本身
# 由已安装分发解析，此处仅为与 tester.py 保持一致的导入环境。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# 导入 runner 即完成测试环境铺设（配置目录、合并日志目录、语言快照缓存），须早于任何
# akaribot.core.* 导入。单入口运行与全量运行因此共用同一份隔离规则。
from akaribot.testing.runner import cleanup_test_environment  # noqa: E402

from akaribot.testing.mock.database import close_db, init_db  # noqa: E402
from akaribot.testing.mock.loader import load_modules  # noqa: E402
from akaribot.testing.mock.random import Random  # noqa: E402
from akaribot.testing.process import run_function_entry  # noqa: E402


async def main(path: str, entry: str) -> int:
    """跑单个测试入口并打印每条用例的结果。

    :param path: 测试文件路径。
    :param entry: 入口函数名。
    :return: 进程退出码，全部通过为 0。
    """
    await init_db()
    await load_modules(show_logs=False, monkey_patches={"Random": Random()})

    spec = importlib.util.spec_from_file_location("one", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["one"] = mod
    spec.loader.exec_module(mod)

    failed = 0
    entries = [entry] if entry else [n for n in dir(mod) if n.startswith("test_")]
    for name in entries:
        res = await run_function_entry(getattr(mod, name), is_ci=True)
        print(f"=== {name} ===")
        if res.get("timeout"):
            failed += 1
            detail = f"no progress for {res.get('timeout_limit')} seconds"
            if active_test := res.get("active_test"):
                detail += f" while running {active_test!r}"
            print(f"  ERROR: {detail}; completed subtests: {res.get('completed_tests', 0)}")
            continue
        if res.get("skipped"):
            failed += 1
            print("  ERROR: test infrastructure skipped this entry")
            continue
        for r in res.get("results", []):
            status = "PASS" if r.get("match") else "FAIL"
            if not r.get("match"):
                failed += 1
            label = r.get("note") or r.get("input") or r.get("expected") or "?"
            print(f"  [{status}] {label}")
            if not r.get("match"):
                print(f"         action={r.get('action')} detail={r}")
        if res.get("error"):
            failed += 1
            print(f"  ERROR: {res.get('error')}")

    await close_db()
    return 1 if failed else 0


if __name__ == "__main__":
    target_path = sys.argv[1]
    target_entry = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        code = asyncio.run(main(target_path, target_entry))
    except Exception:
        traceback.print_exc()
        code = 1
    # 框架加载的模块会留下未完成的后台任务，正常返回会挂起，故强制退出
    cleanup_test_environment()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(code)
