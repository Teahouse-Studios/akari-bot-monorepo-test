import importlib

from akaribot.core.constants import lang_list
from akaribot.core.i18n import build_locale_snapshot, collect_locale_paths, connect_locale_snapshot
from akaribot.core.loader import ModulesManager
from akaribot.core.logger import Logger
from akaribot.core.registry import PackageRegistry

_locale_snapshot_errors: list[str] | None = None


def _load_locale_snapshot() -> list[str]:
    # 语言包快照在同一进程内仅构建一次，因为重建要重新哈希全部语料，是每个入口固定成本的
    # 主要来源。连接仍逐次重置，用例才能从空白的翻译状态开始。
    global _locale_snapshot_errors
    if _locale_snapshot_errors is None:
        _locale_snapshot_errors = build_locale_snapshot(list(lang_list.keys()), collect_locale_paths(), "akari-bot")
    connect_locale_snapshot("akari-bot")
    return _locale_snapshot_errors


def apply_monkey_patch(module, monkey_patches: dict[str, object] | None):
    if not monkey_patches:
        return

    for name, mock_obj in monkey_patches.items():
        if hasattr(module, name):
            setattr(module, name, mock_obj)


async def load_modules(show_logs=True, monkey_patches: dict[str, object] | None = None, load_fixtures: bool = True):
    # 测试显式配置默认 RPC 节点，与生产入口一致，避免依赖模块导入顺序。
    from akaribot.core.queue.server import JobQueueServer
    from akaribot.core.queue.rpc import set_default_peer

    set_default_peer(JobQueueServer)

    err_prompt = []
    locale_loaded_err = _load_locale_snapshot()
    if locale_loaded_err:
        err_prompt.append("I18N loaded failed:")
        err_prompt.append("\n".join(locale_loaded_err))

    # Load HTTP fixtures if available
    if load_fixtures:
        try:
            from akaribot.testing.mock.fixtures import load_http_fixtures

            count = load_http_fixtures()
            if count > 0 and show_logs:
                Logger.info(f"Loaded {count} HTTP fixtures.")
        except Exception:
            if show_logs:
                Logger.exception("Failed to load HTTP fixtures:")

        try:
            from akaribot.testing.mock.webrender import load_webrender_fixtures

            count = load_webrender_fixtures()
            if count > 0 and show_logs:
                Logger.info(f"Loaded {count} WebRender fixtures.")
        except Exception:
            if show_logs:
                Logger.exception("Failed to load WebRender fixtures:")

    if show_logs:
        Logger.info("Attempting to load modules...")

    # 测试不检查模块是否已启用，因此直接读取发现层的清单，与生产入口同源。刻意不使用
    # load_order()，因为测试不校验跨包依赖声明，按包名称字典序枚举即可，测试框架不必依赖依赖图机制。
    for entry in PackageRegistry.modules().values():
        module_py_name = entry.import_path

        try:
            if show_logs:
                Logger.debug(f"Loading {module_py_name}...")

            module = importlib.import_module(module_py_name)
            apply_monkey_patch(module, monkey_patches)

            if show_logs:
                Logger.debug(f"Successfully loaded {module_py_name}!")

            try:
                importlib.import_module(f"{module_py_name}.config")
                if show_logs:
                    Logger.debug(f"Successfully loaded {module_py_name}'s config definition!")
            except ModuleNotFoundError:
                if show_logs:
                    Logger.debug(f"Module {module_py_name}'s config definition not found, skipped.")

        except Exception:
            if show_logs:
                Logger.exception(f"Failed to load {module_py_name}:")

    if show_logs:
        Logger.success("All modules loaded.")
    ModulesManager.refresh()
