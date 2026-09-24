import importlib
import importlib.util
import asyncio
import ast
import hashlib
import inspect
import re
import sys
import traceback
from pathlib import Path
from typing import Callable

from akaribot.core.builtins.session.info import EventInfo
from akaribot.core.config import CFGManager
from akaribot.core.constants import PrivateData, lang_list
from akaribot.core.database import (
    PreparedDatabaseReload,
    activate_db_reload,
    close_prepared_db_reload,
    close_previous_db_context,
    prepare_db_reload,
)
from akaribot.core.database.base import DBModel
from akaribot.core.database.models import ModuleStatus
from akaribot.core.i18n import build_locale_snapshot, collect_locale_paths
from akaribot.core.logger import Logger
from akaribot.core.module_runtime import ModuleRuntimeManager
from akaribot.core.registry import PackageEntry, PackageRegistry
from akaribot.core.scheduler import SchedulerLifecycle
from akaribot.core.types import Module
from akaribot.core.types.module.component_meta import (
    CommandMeta,
    RegexMeta,
    ScheduleMeta,
    HookMeta,
    EventMeta,
)
from akaribot.core.utils.platform_scope import platform_scope


async def load_modules():
    err_prompt = []

    Logger.info("Attempting to load modules...")

    # 不兼容 core API 的包与依赖不满足的包都在发现阶段一并剔除（core.registry.PackageRegistry.discover）：
    # 依赖校验必须与 API 校验同源，才能把「依赖被 API 门槛拒绝的包」一起剔除，避免其导入期注册的模块进入索引。

    # 按声明依赖的拓扑序导入：被依赖的包先完成注册，依赖它的包才能在导入期取用其公共面。
    for entry in PackageRegistry.load_order():
        if entry.kind != "module":
            continue
        module_py_name = entry.import_path
        old_module_names = ModulesManager._module_names_for_py_module(module_py_name)
        old_modules = {name: ModulesManager.modules[name] for name in old_module_names}
        old_origins = {name: ModulesManager.modules_origin[name] for name in old_module_names}
        try:
            Logger.debug(f"Loading {module_py_name}...")

            importlib.import_module(module_py_name)
            Logger.debug(f"Successfully loaded {module_py_name}!")

            config_module_name = f"{module_py_name}.config"
            try:
                importlib.import_module(config_module_name)
                Logger.debug(f"Successfully loaded {module_py_name}'s config definition!")
            except ModuleNotFoundError as e:
                # 只忽略配置模块本身不存在。配置文件内部缺少依赖同样表现为
                # ModuleNotFoundError，若一概吞掉会让模块在缺少必要配置时半加载。
                if e.name != config_module_name:
                    raise
                Logger.debug(f"Module {module_py_name}'s config definition not found, skipped.")

        except Exception:
            # module() 与各组件装饰器都在导入期登记。若文件在登记一部分内容后
            # 才抛异常，必须撤销该包本轮产生的注册，否则报错模块仍可能接收命令。
            ModulesManager._restore_module_registrations(module_py_name, old_modules, old_origins)
            errmsg = f"Failed to load {module_py_name}: \n{traceback.format_exc()}"
            Logger.error(errmsg)
            err_prompt.append(errmsg)

    ModulesManager.refresh_modules_aliases()
    module_names = list(ModulesManager.modules.keys())
    module_aliases = {
        module_name: ModulesManager.get_module_and_alias_first_words(module_name) for module_name in module_names
    }
    await ModuleStatus.init_modules(module_names, module_aliases)
    # 一次取回全部状态：逐模块查询会退化成 N 次往返，模块多或主库在远端时开销可观
    module_status = dict(await ModuleStatus.all().values_list("module_name", "load"))
    for module_name, module in ModulesManager.modules.items():
        if (module_name in module_status and not module_status[module_name]) or not module.load:
            module._db_load = False
        if module._db_load:
            ModuleRuntimeManager.activate(module_name)
        else:
            await ModuleRuntimeManager.suspend(module_name)

    Logger.success("All modules loaded.")

    PrivateData.ensure()
    loader_cache = PrivateData.path / ".cache_loader"
    with open(loader_cache, "w", encoding="utf-8") as open_loader_cache:
        if err_prompt:
            err_prompt = re.sub(r"  File \"<frozen importlib.*?>\", .*?\n", "", "\n".join(err_prompt))
            open_loader_cache.write(err_prompt)
        else:
            open_loader_cache.write("")
        # 不兼容包不参与加载，其成因在此与加载失败并列，供启动提示与 ~module list 展示。
        for line in PackageRegistry.report_lines():
            open_loader_cache.write(f"\n{line}")

    ModulesManager.refresh()
    for module_name in ModulesManager.modules:
        py_module = ModulesManager.return_py_module(module_name)
        if py_module:
            ModulesManager._locale_fingerprints.setdefault(py_module, ModulesManager._locale_fingerprint(py_module))


class ModulesManager:
    modules: dict[str, Module] = {}
    modules_aliases: dict[str, str] = {}
    modules_hooks: dict[str, Callable] = {}
    modules_hook_modules: dict[str, str] = {}
    # 具名 hook 与 parser hook 统一建立订阅索引，复用共享执行基础的资格与代际机制。
    modules_hook_subscriptions: dict[str, list] = {}
    module_hook_subscriptions: dict[str, list] = {}
    # parser 入口订阅：HookPoint -> 已排序订阅列表；与具名 hook 分索引
    parser_hook_subscriptions: dict = {}
    modules_events: dict[str, list[tuple[str, EventMeta]]] = {}
    modules_origin: dict[str, str] = {}
    _deferred_bindings = []
    _reload_lock = asyncio.Lock()
    _reload_package: str | None = None
    _locale_fingerprints: dict[str, tuple[tuple[str, str], ...]] = {}
    _dependency_graph: dict[str, set[str]] = {}
    # 已告警过的「包对」，避免每次重建依赖图都重复告警同一处未声明依赖。
    _undeclared_dependency_warned: set[tuple[str, str]] = set()

    @classmethod
    def _locale_fingerprint(cls, py_module: str) -> tuple[tuple[str, str], ...]:
        module = sys.modules.get(py_module)
        module_file = getattr(module, "__file__", None)
        if not module_file:
            return ()
        locale_path = Path(module_file).resolve().parent / "locales"
        if not locale_path.is_dir():
            return ()
        fingerprints = []
        for locale_file in sorted(locale_path.rglob("*.json")):
            digest = hashlib.sha256(locale_file.read_bytes()).hexdigest()
            fingerprints.append((str(locale_file.relative_to(locale_path)), digest))
        return tuple(fingerprints)

    @classmethod
    def _sync_config_fields(cls, py_module: str) -> list[str]:
        config_module_name = f"{py_module}.config"
        config_module = sys.modules.get(config_module_name)
        if config_module is None:
            return []

        errors = []
        for value in vars(config_module).values():
            fields = getattr(value, "__config_fields__", None)
            if not isinstance(fields, dict):
                continue
            for field_name, field in fields.items():
                try:
                    if CFGManager.has(field_name, field["secret"], field["table_name"]):
                        continue
                    default = field.get("default")
                    if default is None:
                        errors.append(f"{config_module_name}.{field_name}: missing value requires pre-init generation")
                        continue
                    CFGManager.edit_write(
                        field_name,
                        default,
                        field.get("cfg_type"),
                        field["secret"],
                        field["table_name"],
                    )
                except Exception as e:
                    errors.append(f"{config_module_name}.{field_name}: {e}")
        return errors

    @classmethod
    def _stable_schema_value(cls, value):
        if value is None or isinstance(value, (bool, int, float, str, bytes)):
            return value
        if isinstance(value, type):
            return f"{value.__module__}.{value.__qualname__}"
        if callable(value):
            return f"{getattr(value, '__module__', '')}.{getattr(value, '__qualname__', repr(value))}"
        if isinstance(value, dict):
            return tuple(sorted((str(key), cls._stable_schema_value(item)) for key, item in value.items()))
        if isinstance(value, (set, frozenset)):
            return tuple(sorted((cls._stable_schema_value(item) for item in value), key=repr))
        if isinstance(value, (list, tuple)):
            return tuple(cls._stable_schema_value(item) for item in value)
        return repr(value)

    @classmethod
    def _field_schema_fingerprint(cls, field_obj):
        describe = getattr(field_obj, "describe", None)
        if callable(describe):
            try:
                metadata = describe(serializable=False)
            except TypeError:
                metadata = describe()
            # default 只影响 Python 层赋值，不参与表结构。
            metadata = {
                key: value for key, value in metadata.items() if key not in {"default", "python_type", "docstring"}
            }
            return cls._stable_schema_value(metadata)
        return (
            type(field_obj).__name__,
            str(getattr(field_obj, "max_length", "")),
            bool(getattr(field_obj, "null", False)),
            bool(getattr(field_obj, "pk", False)),
            bool(getattr(field_obj, "unique", False)),
            bool(getattr(field_obj, "index", False)),
        )

    @classmethod
    def _model_schema_fingerprint(cls, py_module: str) -> tuple[tuple, ...]:
        models_module = f"{py_module}.database.models"
        try:
            spec = importlib.util.find_spec(models_module)
        except (ModuleNotFoundError, ValueError):
            return ()
        if spec is None:
            return ()
        try:
            module = importlib.import_module(models_module)
        except ModuleNotFoundError as e:
            if e.name in {f"{py_module}.database", models_module}:
                return ()
            raise

        tables = []
        for _, model in inspect.getmembers(module, inspect.isclass):
            if model is DBModel or not issubclass(model, DBModel):
                continue
            meta = getattr(model, "Meta", None)
            table_name = getattr(meta, "table", None)
            if not table_name:
                continue
            fields = []
            for field_name, field_obj in model._meta.fields_map.items():
                fields.append((field_name, cls._field_schema_fingerprint(field_obj)))
            tables.append(
                (
                    table_name,
                    tuple(sorted(fields)),
                    cls._stable_schema_value(getattr(meta, "unique_together", ())),
                    cls._stable_schema_value(getattr(meta, "indexes", ())),
                    getattr(meta, "table_description", None),
                )
            )
        return tuple(sorted(tables))

    @classmethod
    def add_module(cls, module: Module, py_module_name: str):
        if module.module_name not in cls.modules:
            cls.modules[module.module_name] = module
            cls.modules_origin[module.module_name] = py_module_name
            if cls._reload_package:
                deferred = []
                for deferred_module, meta in cls._deferred_bindings:
                    if deferred_module == module.module_name:
                        cls.bind_to_module(deferred_module, meta)
                    else:
                        deferred.append((deferred_module, meta))
                cls._deferred_bindings = deferred
        else:
            raise ValueError(f'Duplicate bind prefix "{module.module_name}"')

    @classmethod
    def remove_modules(cls, modules):
        for module in modules:
            if module in cls.modules:
                cls.modules.pop(module)
                cls.modules_origin.pop(module)
            else:
                raise ValueError(f'Module "{module}" is not exist.')

    @classmethod
    def refresh_modules_aliases(cls):
        cls.modules_aliases.clear()
        for m in cls.modules:
            module = cls.modules[m]
            if module.alias:
                cls.modules_aliases.update(module.alias)

    @classmethod
    def get_module_and_alias_first_words(cls, module_or_alias: str) -> list[str]:
        """返回模块名及其所有别名的首词。"""
        input_words = module_or_alias.split(maxsplit=1)
        if not input_words:
            return []

        first_word = input_words[0]
        module_name = first_word if first_word in cls.modules else None
        if not module_name:
            for alias, target in cls.modules_aliases.items():
                if alias.split(maxsplit=1)[0] == first_word:
                    module_name = target.split(maxsplit=1)[0]
                    break

        if not module_name or module_name not in cls.modules:
            return []

        result = [module_name]
        for alias, target in cls.modules_aliases.items():
            if target.split(maxsplit=1)[0] != module_name:
                continue
            alias_first_word = alias.split(maxsplit=1)[0]
            if alias_first_word not in result:
                result.append(alias_first_word)
        return result

    @classmethod
    def refresh_modules_hooks(cls):
        from akaribot.core.builtins.parser.hooks import HookPoint, build_subscription

        cls.modules_hooks.clear()
        cls.modules_hook_modules.clear()
        cls.modules_hook_subscriptions.clear()
        cls.module_hook_subscriptions.clear()
        cls.parser_hook_subscriptions.clear()
        point_index: dict = {}
        for m in cls.modules:
            module = cls.modules[m]
            if not module.hooks_list:
                continue
            for index, hook in enumerate(module.hooks_list.set):
                if hook.point:
                    try:
                        point = HookPoint(hook.point)
                    except ValueError:
                        Logger.error(f"Module {module.module_name} registered unknown hook point: {hook.point}")
                        continue
                    point_index.setdefault(point, []).append(build_subscription(module.module_name, hook, index))
                    continue
                hook_name = module.module_name + (("." + hook.name) if hook.name else "")
                cls.modules_hooks.update({hook_name: hook.function})
                cls.modules_hook_modules[hook_name] = module.module_name
                subscription = build_subscription(module.module_name, hook, index)
                cls.modules_hook_subscriptions.setdefault(hook_name, []).append(subscription)
                cls.module_hook_subscriptions.setdefault(module.module_name, []).append(subscription)
        for point, subs in point_index.items():
            subs.sort(key=lambda s: (s.priority, s.module_name, s.subscription_id))
            cls.parser_hook_subscriptions[point] = subs

    @classmethod
    def refresh_modules_events(cls):
        cls.modules_events.clear()
        for module_name, module in cls.modules.items():
            for event in module.events_list.set:
                cls.modules_events.setdefault(event.name, []).append((module_name, event))

    @classmethod
    def refresh(cls):
        cls.refresh_modules_aliases()
        cls.refresh_modules_hooks()
        cls.refresh_modules_events()
        cls._return_cache.clear()

    @classmethod
    async def dispatch_event(cls, event_info: EventInfo):
        if not isinstance(event_info, EventInfo):
            raise TypeError("event_info must be an EventInfo")

        target_from = event_info.target_from
        target_union_info = event_info.target_union_info
        available_modules = (
            cls.return_modules_list(
                target_from,
                event_info.client_name,
                platform_from=event_info.platform_from,
                platform_name=event_info.platform_name,
            )
            if target_from
            else cls.modules
        )
        handler_functions = []
        for module_name, event_meta in cls.modules_events.get(event_info.event_name, []):
            module = cls.modules.get(module_name)
            if not module or not module._db_load or module_name not in available_modules:
                continue
            if event_meta not in module.events_list.get(
                target_from, event_info.client_name, event_info.platform_from, event_info.platform_name
            ):
                continue
            if target_union_info and not module.base and module_name not in (target_union_info.modules or []):
                continue
            handler_functions.append((module_name, event_meta.function))
        if handler_functions:

            async def invoke(module_name: str, function: Callable, event_info: EventInfo):
                async with ModuleRuntimeManager.use(module_name):
                    return await function(event_info)

            # 逐 handler 隔离：单个订阅失败不影响其他订阅，也不向调用方泄漏业务异常
            results = []
            for module_name, function in handler_functions:
                try:
                    results.append(await invoke(module_name, function, event_info))
                except asyncio.CancelledError:
                    raise
                except Exception:
                    Logger.exception(f"Event handler in module {module_name} failed for {event_info.event_name}.")
                    results.append(None)
            return results
        return []

    @classmethod
    def search_related_module(cls, module, include_self=True):
        if module in cls.modules_origin:
            modules = []
            py_module = cls.return_py_module(module)
            for m in cls.modules_origin:
                if cls._origin_belongs_to(cls.modules_origin[m], py_module):
                    modules.append(m)
            if not include_self:
                modules.remove(module)
            return modules
        raise ValueError(f'Could not find "{module}" in modules_origin dict')

    @staticmethod
    def _origin_belongs_to(origin: str, py_module: str) -> bool:
        return origin == py_module or origin.startswith(f"{py_module}.")

    @classmethod
    def _module_names_for_py_module(cls, py_module: str) -> list[str]:
        return [
            module_name
            for module_name, origin in cls.modules_origin.items()
            if cls._origin_belongs_to(origin, py_module)
        ]

    @classmethod
    def _restore_module_registrations(
        cls,
        py_module: str,
        modules: dict[str, Module],
        origins: dict[str, str],
    ):
        for module_name in cls._module_names_for_py_module(py_module):
            cls.modules.pop(module_name, None)
            cls.modules_origin.pop(module_name, None)
        cls.modules.update(modules)
        cls.modules_origin.update(origins)
        cls.refresh()

    @classmethod
    def return_py_module(cls, module):
        """取模块所属的包导入路径。

        :param module: 模块注册名。
        :return: 包导入路径；该模块未注册或所属包未知时为 ``None``。
        """
        origin = cls.modules_origin.get(module)
        if not origin:
            return None
        entry = PackageRegistry.by_import_path(origin)
        if entry is None or entry.kind != "module":
            return None
        return entry.import_path

    @classmethod
    def _namespace_prefix(cls, module_name: str) -> str | None:
        # 按段比较而非字符串前缀：``akaribot.modules_extra`` 与 ``akaribot.modules`` 仅首段相同，
        # 前者不是后者的成员包，不该被归约进来。命名空间本身也在此命中，由调用方判断它是否成包。
        parts = module_name.split(".")
        matched: str | None = None
        for root in cls._import_roots():
            root_parts = root.split(".")
            if parts[: len(root_parts)] != root_parts:
                continue
            if matched is None or len(root_parts) > len(matched.split(".")):
                matched = root
        return matched

    @classmethod
    def _normalize_package_name(cls, module_name: str) -> str | None:
        # 纯字符串归约，不校验该包是否已注册：调用方拿它建依赖图，图上的边会在
        # 与已注册包取交集时被过滤。校验注册状态由 :meth:`return_py_module` 负责。
        prefix = cls._namespace_prefix(module_name)
        if prefix is None:
            return None
        depth = len(prefix.split("."))
        parts = module_name.split(".")
        if len(parts) <= depth:
            # 命名空间只是容器（akaribot.modules 无 __init__.py），不是可注册的包。
            return None
        return ".".join(parts[: depth + 1])

    @classmethod
    def _import_roots(cls) -> set[str]:
        # 用于识别 ``from akaribot.modules import x`` 这类裸包导入：其 AST 只给出
        # ``akaribot.modules``，子模块名在 ``node.names`` 中，需展开成 ``akaribot.modules.x``
        # 后才可能匹配到具体包。
        return PackageRegistry.import_roots("module")

    @classmethod
    def _scan_package_dependencies(cls, package_name: str) -> set[str]:
        module = sys.modules.get(package_name)
        if module is None:
            return set()
        paths = [Path(path) for path in getattr(module, "__path__", ())]
        module_file = getattr(module, "__file__", None)
        if not paths and module_file:
            paths = [Path(module_file)]
        source_files = []
        for path in paths:
            if path.is_dir():
                source_files.extend(path.rglob("*.py"))
            elif path.suffix == ".py":
                source_files.append(path)
        dependencies = set()
        for source_file in source_files:
            if any(part == "locales" for part in source_file.parts):
                continue
            try:
                tree = ast.parse(source_file.read_text(encoding="utf-8"))
            except (OSError, SyntaxError, UnicodeDecodeError):
                continue
            for node in ast.walk(tree):
                imported_names: tuple[str, ...] = ()
                if isinstance(node, ast.Import):
                    imported_names = tuple(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported_names = (node.module,)
                    if cls._namespace_prefix(node.module) is not None:
                        # 裸包导入：AST 只给出命名空间或其子路径，子模块名在 node.names 中。
                        imported_names += tuple(f"{node.module}.{alias.name}" for alias in node.names)
                elif isinstance(node, ast.Call):
                    function = node.func
                    function_name = (
                        function.attr
                        if isinstance(function, ast.Attribute)
                        else function.id
                        if isinstance(function, ast.Name)
                        else None
                    )
                    if function_name not in {"import_module", "__import__"}:
                        continue
                    argument = next(
                        (item for item in node.args if isinstance(item, ast.Constant) and isinstance(item.value, str)),
                        None,
                    )
                    if argument is None:
                        argument = next(
                            (
                                keyword.value
                                for keyword in node.keywords
                                if keyword.arg in {"name", "module"}
                                and isinstance(keyword.value, ast.Constant)
                                and isinstance(keyword.value.value, str)
                            ),
                            None,
                        )
                    if argument is not None:
                        imported_names = (argument.value,)
                for imported_name in imported_names:
                    dependency = cls._normalize_package_name(imported_name)
                    if dependency and dependency != package_name:
                        dependencies.add(dependency)
        return dependencies

    @classmethod
    def _declared_package_dependencies(cls, package_name: str) -> set[str]:
        # 取已注册条目的声明依赖，而非 AST 扫描结果；目录扫描的包没有 metadata，
        # 返回空集，其依赖全部落到 :meth:`_scan_package_dependencies` 补充探测。
        entry = PackageRegistry.by_import_path(package_name)
        if entry is None:
            return set()
        return {dependency.import_path for dependency in PackageRegistry.resolved_dependencies(entry)}

    @classmethod
    def _rebuild_dependency_graph(cls):
        # AST 扫出而 metadata 未声明的耦合仍然计入并告警：静默忽略会让 reload 漏掉该重载
        # 的包，比多一条告警危险。
        packages = {py_module for m in cls.modules if (py_module := cls.return_py_module(m))}
        graph: dict[str, set[str]] = {}
        for package_name in packages:
            declared = cls._declared_package_dependencies(package_name) & packages
            scanned = cls._scan_package_dependencies(package_name) & packages
            cls._warn_undeclared_dependencies(package_name, scanned - declared)
            graph[package_name] = declared | scanned
        cls._dependency_graph = graph

    @classmethod
    def _warn_undeclared_dependencies(cls, package_name: str, undeclared: set[str]) -> None:
        # 热重载每次都会重建依赖图，逐次重复告警会淹没日志，故按「包对」在进程内去重。
        for dependency in sorted(undeclared):
            pair = (package_name, dependency)
            if pair in cls._undeclared_dependency_warned:
                continue
            cls._undeclared_dependency_warned.add(pair)
            Logger.warning(
                f"{package_name} imports {dependency} without declaring it in its distribution metadata; "
                "the dependency is kept in the reload closure."
            )

    @classmethod
    def _reload_closure(cls, py_module: str) -> list[str]:
        # 图源为「声明的依赖图 ∪ AST 扫描结果」。成环的包在 discover() 阶段已被拒绝注册，
        # 能走到此处的图必然无环，闭包内的遇环跳过只作防御。
        cls._rebuild_dependency_graph()
        dependents: dict[str, set[str]] = {package_name: set() for package_name in cls._dependency_graph}
        for package_name, dependencies in cls._dependency_graph.items():
            for dependency in dependencies:
                dependents.setdefault(dependency, set()).add(package_name)

        included = set()
        stack = [py_module]
        while stack:
            package_name = stack.pop()
            if package_name in included:
                continue
            included.add(package_name)
            stack.extend(dependents.get(package_name, ()))

        ordered = []
        visiting = set()
        visited = set()

        def visit(package_name: str):
            if package_name in visited:
                return
            if package_name in visiting:
                return
            visiting.add(package_name)
            for dependency in sorted(cls._dependency_graph.get(package_name, ()) & included):
                visit(dependency)
            visiting.discard(package_name)
            visited.add(package_name)
            ordered.append(package_name)

        for package_name in sorted(included):
            visit(package_name)
        return ordered

    @classmethod
    def _module_names_for_py_modules(cls, py_modules: set[str]) -> list[str]:
        return [
            module_name
            for module_name, origin in cls.modules_origin.items()
            if cls.return_py_module(module_name) in py_modules
        ]

    @classmethod
    def bind_to_module(
        cls,
        module_name: str,
        meta: CommandMeta | RegexMeta | ScheduleMeta | HookMeta | EventMeta,
    ):
        if module_name in cls.modules:
            if isinstance(meta, CommandMeta):
                cls.modules[module_name].command_list.add(meta)
            elif isinstance(meta, RegexMeta):
                cls.modules[module_name].regex_list.add(meta)
            elif isinstance(meta, ScheduleMeta):
                cls.modules[module_name].schedule_list.add(meta)
            elif isinstance(meta, HookMeta):
                cls.modules[module_name].hooks_list.add(meta)
            elif isinstance(meta, EventMeta):
                cls.modules[module_name].events_list.add(meta)
        elif cls._reload_package:
            # 子模块按 sys.modules 顺序重载，扩展兄弟模块的装饰器可能先于目标模块执行。
            # 等目标 module() 重新注册后再绑定，避免命令、Hook 或 Event 静默消失。
            cls._deferred_bindings.append((module_name, meta))

    _return_cache = {}

    @classmethod
    def return_modules_list(
        cls,
        target_from: str | None = None,
        client_name: str | None = None,
        platform_from: str | None = None,
        platform_name: str | None = None,
        use_cache: bool = True,
    ) -> dict[str, Module]:
        """按当前会话的平台判据筛选可用模块。

        :param target_from: 场景前缀，如 ``Telegram|Group``。
        :param client_name: 客户端身份，如 ``Telegram`` / ``Telegram-alt``。
        :param platform_from: 平台场景前缀，如 ``Telegram|Group``；缺省时按 target_from 推导。
        :param platform_name: 平台展示名，如 ``Telegram``；缺省时按 client_name 推导。
        :param use_cache: 是否复用按四元组缓存的结果。
        :return: 模块名到模块的映射。
        """
        # 过滤结果取决于四段判据，缓存键必须全部带上：只按 target_from 建键会让同一场景
        # 配上不同客户端名时取到旧结果，漏掉平台两段则会让一个实例命中另一个实例的缓存。
        cache_key = (target_from, client_name, platform_from, platform_name)
        if target_from and use_cache and cache_key in cls._return_cache:
            return cls._return_cache[cache_key]
        modules = {module_name: cls.modules[module_name] for module_name in sorted(cls.modules)}

        if target_from:
            scope = platform_scope(target_from, client_name, platform_from, platform_name)
            returns = {}
            for m in modules:
                if isinstance(modules[m], Module):
                    available = modules[m].available_for
                    exclude = modules[m].exclude_from
                    if not modules[m].load:
                        continue
                    if scope & set(exclude):
                        continue
                    if scope & set(available) or "*" in available:
                        returns.update({m: modules[m]})
            cls._return_cache[cache_key] = returns
            return returns
        return modules

    @classmethod
    async def load_module(cls, module_name: str):
        """
        全域加载该机器人模块。
        """
        if module_name in cls.modules:
            module = cls.modules[module_name]
            old_load = module._db_load
            async with SchedulerLifecycle.maintenance_window({module_name}):
                try:
                    await ModuleStatus.set_module_loaded(module_name, True)
                    module._db_load = True
                    SchedulerLifecycle.reconcile_modules({module_name}, cls.modules)
                    ModuleRuntimeManager.activate(module_name)
                except BaseException:
                    # Scheduler 注册异常或取消不能留下“数据库显示启用、实际无 Job”状态。
                    try:
                        await asyncio.shield(ModuleStatus.set_module_loaded(module_name, old_load))
                        module._db_load = old_load
                        SchedulerLifecycle.reconcile_modules({module_name}, cls.modules)
                        if old_load:
                            ModuleRuntimeManager.activate(module_name)
                        else:
                            await ModuleRuntimeManager.suspend(module_name)
                    except Exception:
                        Logger.exception(f"Failed to restore module load state for {module_name}:")
                    raise
            return True
        return False

    @classmethod
    async def unload_module(cls, module_name: str):
        """
        全域卸载该机器人模块。
        """
        if module_name in cls.modules:
            from akaribot.core.queue.server import JobQueueServer

            module = cls.modules[module_name]
            old_load = module._db_load
            # 与 reload 保持相同顺序：先排空 Queue handler，再进入 Scheduler 维护。
            # 非独占 Queue 窗口仍允许轮询器回收模块清理产生的响应。
            async with JobQueueServer.maintenance_window(exclusive=False):
                async with SchedulerLifecycle.maintenance_window({module_name}):
                    try:
                        await ModuleStatus.set_module_loaded(module_name, False)
                        module._db_load = False
                        SchedulerLifecycle.reconcile_modules({module_name}, cls.modules)
                        await ModuleRuntimeManager.suspend(module_name)
                    except BaseException:
                        try:
                            await asyncio.shield(ModuleStatus.set_module_loaded(module_name, old_load))
                            module._db_load = old_load
                            SchedulerLifecycle.reconcile_modules({module_name}, cls.modules)
                            if old_load:
                                ModuleRuntimeManager.activate(module_name)
                            else:
                                await ModuleRuntimeManager.suspend(module_name)
                        except Exception:
                            Logger.exception(f"Failed to restore module unload state for {module_name}:")
                        raise
            return True
        return False

    @classmethod
    async def reload_module(cls, module_name: str):
        """
        重载该机器人模块（以及该模块所在文件的其它模块）
        """
        # 此处不能等待另一个重载释放锁，双方会形成死锁。
        # 忙碌时直接失败，保证第二次请求尚未改动模块注册表。
        if cls._reload_lock.locked():
            Logger.warning(f"Another module reload is already in progress, skipped {module_name}.")
            return False, 0

        async with cls._reload_lock:
            # 先排空 Queue handler，再进入 Scheduler 维护，反序会形成永久互锁。
            # Scheduler 窗口仍须覆盖 importlib.reload()。
            from akaribot.core.queue.server import JobQueueServer

            # 长时间保持非独占窗口：停止领取新 action，但让轮询器继续回收
            # 响应、续租与执行模块清理 RPC。数据库替换会在内部再嵌套独占窗口。
            async with JobQueueServer.maintenance_window(exclusive=False):
                async with SchedulerLifecycle.maintenance_window():
                    return await cls._reload_module(module_name)

    @classmethod
    async def _reload_module(cls, module_name: str):
        py_module = cls.return_py_module(module_name)
        reload_packages = cls._reload_closure(py_module)
        reload_package_set = set(reload_packages)
        python_module_snapshot = {
            name: module
            for name, module in sys.modules.items()
            if any(name == package_name or name.startswith(f"{package_name}.") for package_name in reload_packages)
        }
        related_modules = cls._module_names_for_py_modules(reload_package_set)
        locale_fingerprints = {package_name: cls._locale_fingerprint(package_name) for package_name in reload_packages}
        changed_locale_packages = {
            package_name
            for package_name, fingerprint in locale_fingerprints.items()
            if cls._locale_fingerprints.get(package_name, ()) != fingerprint
        }
        old_schema_fingerprints = {
            package_name: cls._model_schema_fingerprint(package_name) for package_name in reload_packages
        }
        runtime_snapshot = ModuleRuntimeManager.prepare_reload(set(related_modules))
        runtime_names = set(related_modules)
        old_modules = {name: cls.modules[name] for name in related_modules}
        old_origins = {name: cls.modules_origin[name] for name in related_modules}
        old_deferred_bindings = cls._deferred_bindings
        old_reload_package = cls._reload_package
        status_names_to_replace = set(related_modules)
        statuses_replaced = False
        registrations_replaced = False
        committed = False
        count = -999
        old_statuses = {}
        scheduler_names_to_replace = set(related_modules)
        old_schedules = SchedulerLifecycle.snapshot_modules(scheduler_names_to_replace)
        schedules_replaced = False

        def restore_registrations():
            for package_name in reversed(reload_packages):
                cls._restore_module_registrations(package_name, old_modules, old_origins)
            # 恢复旧代际注册后必须重建订阅索引，否则旧订阅全部失效。
            # 重建时 staging 尚未撤销，需在 abort_reload 之后再次重建。
            cls.refresh_modules_hooks()

        def restore_python_modules():
            for name in list(sys.modules):
                if any(name == package_name or name.startswith(f"{package_name}.") for package_name in reload_packages):
                    sys.modules.pop(name, None)
            sys.modules.update(python_module_snapshot)

        async def restore_statuses():
            await ModuleStatus.filter(module_name__in=status_names_to_replace).delete()
            if old_statuses:
                await ModuleStatus.bulk_create(
                    [ModuleStatus(module_name=name, load=load) for name, load in old_statuses.items()]
                )

        try:
            old_statuses = dict(
                await ModuleStatus.filter(module_name__in=related_modules).values_list("module_name", "load")
            )

            cls._reload_package = py_module
            cls._deferred_bindings = []
            cls.remove_modules(related_modules)
            registrations_replaced = True
            count = 0
            for package_name in reload_packages:
                package_count = cls.reload_py_module(package_name)
                if package_count < 0:
                    count = -999
                    break
                count += package_count
            if count <= 0:
                runtime_names.update(cls._module_names_for_py_modules(reload_package_set))
                restore_python_modules()
                restore_registrations()
                await ModuleRuntimeManager.abort_reload(runtime_snapshot, runtime_names)
                cls.refresh_modules_hooks()
                return False, count

            reloaded_modules = cls._module_names_for_py_modules(reload_package_set)
            runtime_names.update(reloaded_modules)
            if not reloaded_modules:
                Logger.error(f"Reloaded Python packages {reload_packages}, but they did not register any modules.")
                restore_python_modules()
                restore_registrations()
                await ModuleRuntimeManager.abort_reload(runtime_snapshot, runtime_names)
                cls.refresh_modules_hooks()
                return False, count

            config_errors = []
            for package_name in reload_packages:
                config_errors.extend(cls._sync_config_fields(package_name))
            if config_errors:
                Logger.error(f"Failed to synchronize module configuration for {reload_packages}: {config_errors}")
                restore_python_modules()
                restore_registrations()
                await ModuleRuntimeManager.abort_reload(runtime_snapshot, runtime_names)
                cls.refresh_modules_hooks()
                return False, count

            changed_schema_packages = [
                package_name
                for package_name in reload_packages
                if cls._model_schema_fingerprint(package_name) != old_schema_fingerprints.get(package_name, ())
            ]
            if changed_schema_packages:
                Logger.error(
                    f"Database model schema changed during reload for {changed_schema_packages}; "
                    "restart and run database migration instead."
                )
                restore_python_modules()
                restore_registrations()
                await ModuleRuntimeManager.abort_reload(runtime_snapshot, runtime_names)
                cls.refresh_modules_hooks()
                return False, count

            if cls._deferred_bindings:
                missing_modules = sorted({name for name, _ in cls._deferred_bindings})
                Logger.warning(
                    f"Dropped deferred component bindings for modules not registered by "
                    f"{reload_packages}: {missing_modules}"
                )

            cls.refresh()
            new_statuses = {}
            for name in reloaded_modules:
                module = cls.modules[name]
                load = old_statuses.get(name)
                if load is None:
                    alias_first_words = {alias.split(maxsplit=1)[0] for alias in (module.alias or ())}
                    old_name = next((alias for alias in alias_first_words if alias in old_statuses), None)
                    load = old_statuses[old_name] if old_name else True
                new_statuses[name] = load
                module._db_load = bool(load and module.load)

            status_names_to_replace.update(reloaded_modules)
            scheduler_names_to_replace.update(reloaded_modules)
            # 在首个会修改持久化状态的 await 之前置位。协程可能恰好在 delete()
            # 提交后收到取消；若等 await 返回才置位，取消路径会误判为无需回滚。
            statuses_replaced = True
            await ModuleStatus.filter(module_name__in=status_names_to_replace).delete()
            if new_statuses:
                await ModuleStatus.bulk_create(
                    [ModuleStatus(module_name=name, load=load) for name, load in new_statuses.items()]
                )

            # Scheduler 当前仍处于维护窗口，先把新 Job 准备好但不允许执行；数据库
            # 重载失败时可连同 ModuleStatus 与注册表一起恢复旧 Job。
            SchedulerLifecycle.reconcile_modules(scheduler_names_to_replace, cls.modules)
            schedules_replaced = True

            # 先构建可独立失败的数据库 context；旧 context 和旧 runtime 此时都
            # 保持可用。只有全部校验成功后才进入不可逆 commit。
            prepared_db = await prepare_db_reload()
            if prepared_db is None:
                Logger.error(f"Reloaded Python module {py_module}, but failed to prepare its database models.")
                await restore_statuses()
                statuses_replaced = False
                restore_python_modules()
                restore_registrations()
                SchedulerLifecycle.restore_modules(old_schedules, scheduler_names_to_replace)
                schedules_replaced = False
                await ModuleRuntimeManager.abort_reload(runtime_snapshot, runtime_names)
                cls.refresh_modules_hooks()
                return False, count

            active_modules = {
                name
                for name in runtime_names
                if name in cls.modules and cls.modules[name]._db_load and cls.modules[name].load
            }
            # commit 是代际切换的不可逆边界。取消可以中断构建阶段，但不能在
            # runtime 已切换、旧 generation 已停止后再回滚注册表和数据库。
            from akaribot.core.queue.server import JobQueueServer

            commit_task = asyncio.create_task(
                ModuleRuntimeManager.commit_reload(
                    runtime_snapshot,
                    runtime_names,
                    active_modules,
                    set(cls.modules),
                ),
                name=f"module-reload-runtime-commit:{py_module}",
            )
            reload_cancelled = False
            try:
                await asyncio.shield(commit_task)
            except asyncio.CancelledError:
                reload_cancelled = True
                try:
                    await commit_task
                except BaseException:
                    await close_prepared_db_reload(prepared_db)
                    raise
            try:
                # 旧 runtime 已停止，此时短时独占 Queue 轮询并切换数据库 context，
                # 避免轮询器在旧连接关闭过程中仍发出查询。
                activate_db_reload(prepared_db)
                async with JobQueueServer.maintenance_window(exclusive=True):
                    close_task = asyncio.create_task(
                        close_previous_db_context(prepared_db),
                        name=f"module-reload-close-previous-db:{py_module}",
                    )
                    try:
                        await asyncio.shield(close_task)
                    except asyncio.CancelledError:
                        reload_cancelled = True
                        await close_task
            except BaseException:
                await close_prepared_db_reload(prepared_db)
                raise
            committed = True
            if reload_cancelled:
                raise asyncio.CancelledError()
            if changed_locale_packages:
                try:
                    locale_errors = build_locale_snapshot(list(lang_list.keys()), collect_locale_paths(), "akari-bot")
                    if locale_errors:
                        Logger.warning(
                            f"Failed to rebuild locale snapshot after reloading {reload_packages}: {locale_errors}"
                        )
                    else:
                        for package_name in changed_locale_packages:
                            cls._locale_fingerprints[package_name] = locale_fingerprints[package_name]
                except Exception:
                    Logger.exception(f"Failed to rebuild locale snapshot after reloading {py_module}:")
            return True, count
        except asyncio.CancelledError:
            # Queue action 超时或 Server 关闭都会取消热重载。取消不能被转换成普通
            # 失败，但在继续传播前必须恢复已删改的持久状态与内存注册表。
            if not committed:
                if statuses_replaced:
                    try:
                        await asyncio.shield(restore_statuses())
                    except Exception:
                        Logger.exception(f"Failed to restore ModuleStatus rows for cancelled reload of {py_module}:")
                runtime_names.update(cls._module_names_for_py_modules(reload_package_set))
                restore_python_modules()
                if registrations_replaced:
                    restore_registrations()
                if schedules_replaced:
                    SchedulerLifecycle.restore_modules(old_schedules, scheduler_names_to_replace)
                await ModuleRuntimeManager.abort_reload(runtime_snapshot, runtime_names)
                cls.refresh_modules_hooks()
            raise
        except Exception:
            Logger.exception(f"Failed to reload module package {py_module}:")
            if not committed:
                runtime_names.update(cls._module_names_for_py_modules(reload_package_set))
                if statuses_replaced:
                    try:
                        await restore_statuses()
                    except Exception:
                        Logger.exception(f"Failed to restore ModuleStatus rows for {py_module}:")
                if registrations_replaced:
                    restore_python_modules()
                    restore_registrations()
                if schedules_replaced:
                    SchedulerLifecycle.restore_modules(old_schedules, scheduler_names_to_replace)
                await ModuleRuntimeManager.abort_reload(runtime_snapshot, runtime_names)
                cls.refresh_modules_hooks()
                return False, count
            Logger.exception(f"Reload for {py_module} committed, but post-commit work failed:")
            return True, count
        finally:
            cls._deferred_bindings = old_deferred_bindings
            cls._reload_package = old_reload_package

    @classmethod
    def reload_py_module(cls, module_name: str):
        """
        重载该 Python 模块
        """
        module_names = [name for name in sys.modules if name == module_name or name.startswith(f"{module_name}.")]
        if module_name not in module_names:
            Logger.error(f"Cannot reload unknown Python module {module_name}.")
            return -999
        snapshot = {name: sys.modules[name] for name in module_names}
        try:
            Logger.info(f"Reloading {module_name} with a fresh module namespace ...")
            importlib.invalidate_caches()
            for name in module_names:
                sys.modules.pop(name, None)
            for name in module_names:
                importlib.import_module(name)
            loaded_module_names = [
                name for name in sys.modules if name == module_name or name.startswith(f"{module_name}.")
            ]
            Logger.success(f"Successfully reloaded {module_name}.")
            return len(loaded_module_names)
        except Exception:
            Logger.exception(f"Failed to reload {module_name}:")
            for name in list(sys.modules):
                if name == module_name or name.startswith(f"{module_name}."):
                    sys.modules.pop(name, None)
            sys.modules.update(snapshot)
            return -999

    @classmethod
    def _snapshot_package_index(cls) -> dict[str, object]:
        # PackageRegistry 只有重建缓存（discover）的入口，没有回退点。安装失败后 CLI 会卸载该分发，
        # 索引若停留在含该包的状态，下一次数据库重挂会去导入已经不存在的模型模块。
        return {
            "_entries": dict(PackageRegistry._entries),
            "_by_import_path": dict(PackageRegistry._by_import_path),
            "_incompatible": dict(PackageRegistry._incompatible),
            "_api_refused": dict(PackageRegistry._api_refused),
            "_dependency_rejected": dict(PackageRegistry._dependency_rejected),
        }

    @classmethod
    def _restore_package_index(cls, snapshot: dict[str, object]) -> None:
        for name, value in snapshot.items():
            setattr(PackageRegistry, name, value)

    @classmethod
    def _forget_package(cls, entry: PackageEntry) -> None:
        # 卸载 RPC 先于 uv pip uninstall 执行，重跑 discover() 依旧会看到该分发，故直接改写索引缓存。
        PackageRegistry._entries.pop(f"{entry.kind}:{entry.name}", None)
        indexed = PackageRegistry._by_import_path.get(entry.import_path)
        if indexed is not None and indexed.kind == entry.kind and indexed.name == entry.name:
            PackageRegistry._by_import_path.pop(entry.import_path, None)

    @classmethod
    def _reload_config_view(cls) -> None:
        # 只读进程只认启动时列出的文件，新表必须经 load() 重新枚举才会出现。此处失败不阻断安装，
        # 导入期读取新配置项时会以只读守卫的形式报出。
        try:
            CFGManager.load()
        except Exception:
            Logger.exception("Failed to reload the config directory before installing a package.")

    @classmethod
    def _rebuild_locale_snapshot(cls, py_module: str) -> None:
        try:
            locale_errors = build_locale_snapshot(list(lang_list.keys()), collect_locale_paths(), "akari-bot")
        except Exception:
            Logger.exception(f"Failed to rebuild the locale snapshot for {py_module}:")
            return
        if locale_errors:
            Logger.warning(f"Failed to rebuild the locale snapshot for {py_module}: {locale_errors}")

    @classmethod
    async def install_package(cls, entry: PackageEntry) -> bool:
        """把已装好但尚未接入的模块包热装载进当前进程。

        与 reload_module 的区别：reload_module 替换已注册模块的代码（importlib.reload 加代际切换，
        因此需要回滚快照）；本方法只做首次接入，是纯新增，没有旧代际可回滚，但必须替换数据库
        context 才能纳入新包的模型。两者共用维护窗口与索引刷新，回滚路径完全不同，故不合并。

        :param entry: 发现层给出的模块包条目。
        :return: 是否接入成功；包已注册、正在重载或被发现层拒绝时返回 ``False``。
        :raises Exception: 导入及其后续步骤的异常在完成回滚后继续向上抛出。
        """
        from akaribot.core.queue.server import JobQueueServer

        py_module = entry.import_path
        if entry.kind != "module":
            Logger.error(f"{py_module} is not a module package; only module packages can be hot installed.")
            return False
        if cls._module_names_for_py_module(py_module):
            Logger.warning(f"{py_module} is already registered; use the module reload action to replace its code.")
            return False
        # 与 reload_module 同策略：忙碌时直接失败，不把等待锁的时间算进 RPC 超时。
        if cls._reload_lock.locked():
            Logger.warning(f"Another module reload or package change is in progress, skipped installing {py_module}.")
            return False

        async with cls._reload_lock:
            # 先排空 Queue handler，再进入 Scheduler 维护；数据库替换会在内部再嵌套独占窗口。
            async with JobQueueServer.maintenance_window(exclusive=False):
                async with SchedulerLifecycle.maintenance_window():
                    return await cls._install_package(entry)

    @classmethod
    async def _install_package(cls, entry: PackageEntry) -> bool:
        py_module = entry.import_path
        index_snapshot = cls._snapshot_package_index()
        python_module_snapshot = {
            name: module for name, module in sys.modules.items() if cls._origin_belongs_to(name, py_module)
        }
        prepared_db = None
        new_names: list[str] = []
        statuses_created = False

        async def rollback():
            """撤销本次导入的写入与索引；已切换的数据库 context 不回退。"""
            for name in list(sys.modules):
                if cls._origin_belongs_to(name, py_module):
                    sys.modules.pop(name, None)
            sys.modules.update(python_module_snapshot)
            cls._restore_module_registrations(py_module, {}, {})
            cls._restore_package_index(index_snapshot)
            if statuses_created and new_names:
                try:
                    await asyncio.shield(ModuleStatus.filter(module_name__in=new_names).delete())
                except Exception:
                    Logger.exception(f"Failed to delete ModuleStatus rows created for {py_module}.")
            if new_names:
                SchedulerLifecycle.reconcile_modules(new_names, cls.modules)
                for name in new_names:
                    await ModuleRuntimeManager.suspend(name)
            if prepared_db is not None:
                # 已激活的 context 不会被关闭：数据库切换是本次安装不可逆的一步。
                await close_prepared_db_reload(prepared_db)
            cls.refresh()

        # 新装的 entry point 只有重跑发现才会出现；requires_core_api 与声明依赖的校验已内建于
        # discover()，被它剔除的包在此以拒绝原因报出。
        importlib.invalidate_caches()
        PackageRegistry.discover(force=True)
        fresh = PackageRegistry.by_import_path(py_module)
        if fresh is None or fresh.kind != "module":
            reason = PackageRegistry.incompatible().get(entry.dist_name or entry.name)
            Logger.error(
                f"Refused to install {entry.dist_name or py_module}: {reason or 'not registered by discovery'}"
            )
            cls._restore_package_index(index_snapshot)
            return False
        entry = fresh

        # 新包的配置由 CLI 在可写子进程里补写，本进程须在导入之前重读配置目录。
        cls._reload_config_view()

        try:
            importlib.import_module(py_module)
            new_names = cls._module_names_for_py_module(py_module)
            if not new_names:
                raise RuntimeError(f"{py_module} imported but registered no module.")

            # discover() 已把新包并入索引，故新 context 覆盖「现有 + 新包」的模型。
            prepared_db = await cls._swap_package_database(py_module, "including")
            if prepared_db is None:
                raise RuntimeError(f"Failed to prepare a database context including {py_module}.")

            # init_modules 以传入清单为准删除缺席行，故带上全部已注册模块，而不只是新增名。
            aliases = {name: cls.get_module_and_alias_first_words(name) for name in new_names}
            await ModuleStatus.init_modules(list(cls.modules), aliases)
            statuses_created = True
            statuses = dict(await ModuleStatus.filter(module_name__in=new_names).values_list("module_name", "load"))
            for name in new_names:
                module = cls.modules[name]
                module._db_load = bool(module.load and statuses.get(name, True))

            cls.refresh_modules_aliases()
            cls.refresh()
            cls.refresh_modules_hooks()
            cls._rebuild_locale_snapshot(py_module)
            cls._locale_fingerprints[py_module] = cls._locale_fingerprint(py_module)
            SchedulerLifecycle.reconcile_modules(new_names, cls.modules)
            for name in new_names:
                if cls.modules[name]._db_load:
                    ModuleRuntimeManager.activate(name)
                else:
                    await ModuleRuntimeManager.suspend(name)
            Logger.success(f"Hot installed module package {py_module}: {', '.join(sorted(new_names))}.")
            return True
        except BaseException:
            await rollback()
            raise

    @classmethod
    async def remove_package(cls, entry: PackageEntry) -> bool:
        """把一个模块包从运行中的进程里拆下来，供 CLI 随后真正卸载分发。

        与 reload_module 的区别：reload_module 替换已注册模块的代码并可回滚到旧代际；本方法处理
        整包退出，先停用全部注册名，再从索引移除、重挂不含该包模型的数据库 context，最后清掉
        sys.modules。两者共用维护窗口与索引刷新，回滚路径完全不同，故不合并。

        :param entry: 发现层给出的模块包条目。
        :return: 数据库 context 是否重挂成功；拆除本身按单向操作走完，失败只如实回报。
        """
        from akaribot.core.queue.server import JobQueueServer

        py_module = entry.import_path
        # 与 reload_module 同策略：忙碌时直接失败，不把等待锁的时间算进 RPC 超时。
        if cls._reload_lock.locked():
            Logger.warning(f"Another module reload or package change is in progress, skipped removing {py_module}.")
            return False

        async with cls._reload_lock:
            module_names = [name for name in cls._module_names_for_py_module(py_module) if name in cls.modules]
            async with JobQueueServer.maintenance_window(exclusive=False):
                async with SchedulerLifecycle.maintenance_window():
                    for module_name in module_names:
                        try:
                            await cls.unload_module(module_name)
                        except Exception:
                            # 拆除是单向操作：单个模块停用失败不应留下半拆状态，继续走完索引与 context 清理。
                            Logger.exception(f"Failed to unload {module_name} while removing {py_module}:")
                    cls.remove_modules(module_names)
                    # 卸载 RPC 先于 uv pip uninstall，重跑 discover() 仍会看到该分发，
                    # 故直接把包摘出发现层索引，下面的数据库重挂才不会带上它的模型。
                    cls._forget_package(entry)
                    swapped_db = await cls._swap_package_database(py_module, "without")
                    for name in list(sys.modules):
                        if cls._origin_belongs_to(name, py_module):
                            sys.modules.pop(name, None)
                    cls._locale_fingerprints.pop(py_module, None)
                    cls.refresh()
                    cls._rebuild_locale_snapshot(py_module)
                    if module_names:
                        try:
                            # 与启动期 init_modules 对缺席模块的清理同向：残留的 load=False 会误停重装后的模块。
                            await ModuleStatus.filter(module_name__in=module_names).delete()
                        except Exception:
                            Logger.exception(f"Failed to delete ModuleStatus rows of the removed package {py_module}.")
                    Logger.success(f"Removed module package {py_module} from the running process.")
                    return swapped_db is not None

    @classmethod
    async def _swap_package_database(cls, py_module: str, note: str) -> PreparedDatabaseReload | None:
        # 旧连接关闭期间不得让轮询器发出查询，故与 reload 的切换路径一致地嵌套独占窗口；
        # ``note`` 只用于日志措辞（新 context 是纳入还是去掉该包的模型）。
        from akaribot.core.queue.server import JobQueueServer

        prepared_db = await prepare_db_reload()
        if prepared_db is None:
            Logger.error(f"Failed to prepare a database context {note} {py_module}.")
            return None
        activate_db_reload(prepared_db)
        async with JobQueueServer.maintenance_window(exclusive=True):
            close_task = asyncio.create_task(
                close_previous_db_context(prepared_db),
                name=f"package-change-close-previous-db:{py_module}",
            )
            try:
                await asyncio.shield(close_task)
            except asyncio.CancelledError:
                await close_task
                raise
        return prepared_db
