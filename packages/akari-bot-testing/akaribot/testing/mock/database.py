import importlib
import time
import traceback

from tortoise import Tortoise
from tortoise.context import TortoiseContext

from akaribot.core.database import fetch_module_db, close_db
from akaribot.core.logger import Logger

_last_init_error = ""
_last_init_timings: dict[str, float] = {}


def get_last_init_error() -> str:
    """返回最近一次测试数据库初始化失败的诊断信息。"""
    return _last_init_error


def get_last_init_timings() -> dict[str, float]:
    """返回最近一次初始化测试数据库各阶段的耗时与模型模块数。"""
    return dict(_last_init_timings)


async def init_db(load_module_db: bool = True) -> bool:
    global _last_init_error, _last_init_timings

    # 建立连接本身很快，可能拖慢准备阶段的是模型模块导入、建立连接与建表，因此分四段计时，
    # 使准备耗时日志标明耗时偏高的阶段。模型模块由 Tortoise 自行导入，这里先导入并计时，
    # 之后的导入命中模块缓存，模块仅加载一次。
    timings = {"models": 0.0, "fetch_db": 0.0, "import_models": 0.0, "tortoise_init": 0.0, "schemas": 0.0}
    context = None
    stage = "discovering module database models"
    started = time.perf_counter()
    try:
        database_list = fetch_module_db() if load_module_db else []
        timings["models"] = float(len(database_list))
        timings["fetch_db"] = time.perf_counter() - started

        stage = "importing model modules"
        started = time.perf_counter()
        for module_path in ("akaribot.core.database.models", *database_list, "akaribot.core.database.local"):
            importlib.import_module(module_path)
        timings["import_models"] = time.perf_counter() - started

        stage = "initializing Tortoise ORM"
        started = time.perf_counter()
        context = await Tortoise.init(
            config={
                "connections": {
                    "default": "sqlite://:memory:",
                    "local": "sqlite://:memory:",
                },
                "apps": {
                    "models": {
                        "models": ["akaribot.core.database.models"] + database_list,
                        "default_connection": "default",
                    },
                    "local_models": {
                        "models": ["akaribot.core.database.local"],
                        "default_connection": "local",
                    },
                },
            },
            _enable_global_fallback=True,
        )

        timings["tortoise_init"] = time.perf_counter() - started
        stage = "generating SQLite schemas"
        started = time.perf_counter()
        await Tortoise.generate_schemas(safe=True)
        timings["schemas"] = time.perf_counter() - started
        _last_init_error = ""
        return True
    except Exception:
        _last_init_error = f"Test database initialization failed while {stage}:\n{traceback.format_exc()}"
        Logger.exception()
        return False
    finally:
        _last_init_timings = timings
        if isinstance(context, TortoiseContext):
            context.__exit__(None, None, None)


__all__ = ["init_db", "get_last_init_error", "get_last_init_timings", "close_db"]
