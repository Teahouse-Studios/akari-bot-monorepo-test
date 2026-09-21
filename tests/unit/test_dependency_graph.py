"""模块依赖图单元测试。

覆盖 T0.7：拓扑序、发现期的三类校验（缺依赖、版本不满足、成环）、extra 标记过滤，
以及 AST 扫出未声明依赖时的告警与闭包保留。分发 metadata 全部用替身，不安装任何东西。
"""

import importlib.metadata
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import akaribot.core.loader as loader_module
from akaribot.core.loader import ModulesManager
from akaribot.core.registry import (
    CircularDependencyError,
    PackageEntry,
    PackageManifest,
    PackageRegistry,
)
from akaribot.testing import Tester, func_case


class _FakeMetadata:
    """``email.Message`` 的最小替身，只实现 metadata.get_all()。"""

    def __init__(self, fields: dict[str, list[str]]):
        self._fields = fields

    def get_all(self, name: str) -> list[str] | None:
        return self._fields.get(name)


class _FakeDistribution:
    """``importlib.metadata`` 分发对象的最小替身。"""

    def __init__(
        self,
        name: str,
        version: str,
        requires: tuple[str, ...] = (),
        extras: tuple[str, ...] = (),
    ):
        self.version = version
        self.metadata = _FakeMetadata(
            {
                "Name": [name],
                "Version": [version],
                "Requires-Dist": list(requires),
                "Provides-Extra": list(extras),
            }
        )


def _canonicalize(name: str) -> str:
    """分发名的比较形式，与 registry 内部的规范化保持一致。"""
    from packaging.utils import canonicalize_name

    return canonicalize_name(name)


@contextmanager
def _fake_environment(distributions: dict[str, _FakeDistribution]):
    """以替身替换分发查询。

    :param distributions: 分发名到替身的映射。
    """
    normalized = {_canonicalize(name): distribution for name, distribution in distributions.items()}

    def fake_distribution(name: str) -> _FakeDistribution:
        try:
            return normalized[_canonicalize(name)]
        except KeyError:
            raise importlib.metadata.PackageNotFoundError(name) from None

    def fake_version(name: str) -> str:
        distribution = normalized.get(_canonicalize(name))
        if distribution is None:
            raise importlib.metadata.PackageNotFoundError(name)
        return distribution.version

    with (
        patch("importlib.metadata.distribution", side_effect=fake_distribution),
        patch("importlib.metadata.version", side_effect=fake_version),
    ):
        yield


def _entry(kind: str, name: str, dist_name: str = "") -> PackageEntry:
    """构造测试用条目。

    :param kind: 包种类。
    :param name: 包名。
    :param dist_name: 分发名；为空串表示目录扫描兜底的包。
    :return: 条目。
    """
    root = "modules" if kind == "module" else "bots"
    return PackageEntry(
        kind=kind,
        name=name,
        dist_name=dist_name,
        version="0+local" if not dist_name else "1.0.0",
        import_path=f"{root}.{name}",
        root=Path("."),
        manifest=PackageManifest(),
    )


def _fake_entry_points(entries: list[PackageEntry]):
    """条目枚举替身，按种类返回给定条目。

    :param entries: 全部条目。
    :return: 可作 ``_from_entry_points`` 替身的函数。
    """

    def source(kind: str, group: str) -> list[PackageEntry]:
        return [entry for entry in entries if entry.kind == kind]

    return source


def _snapshot() -> tuple:
    """注册表全部可变状态的快照。"""
    return (
        PackageRegistry._entries,
        PackageRegistry._by_import_path,
        PackageRegistry._discovered,
        PackageRegistry._incompatible,
        PackageRegistry._dependency_rejected,
    )


def _restore(saved: tuple) -> None:
    """还原注册表状态。"""
    (
        PackageRegistry._entries,
        PackageRegistry._by_import_path,
        PackageRegistry._discovered,
        PackageRegistry._incompatible,
        PackageRegistry._dependency_rejected,
    ) = saved


@contextmanager
def _discovered_from(entries: list[PackageEntry], distributions: dict[str, _FakeDistribution]):
    """以替身条目与替身分发完整跑一次 discover()，退出时还原注册表。

    :param entries: 发现结果。
    :param distributions: 环境中的分发。
    """
    saved = _snapshot()
    try:
        with (
            _fake_environment(distributions),
            patch.object(PackageRegistry, "_load_frozen", return_value=None),
            patch.object(PackageRegistry, "_from_entry_points", side_effect=_fake_entry_points(entries)),
            patch.object(PackageRegistry, "_from_directory_scan", return_value=[]),
        ):
            PackageRegistry.discover(force=True)
            yield
    finally:
        _restore(saved)


@contextmanager
def _isolated_registry(entries: dict[str, PackageEntry], distributions: dict[str, _FakeDistribution]):
    """直接替换发现结果，跳过 discover() 的收尾校验。

    :param entries: 条目映射，键为 ``种类:包名``。
    :param distributions: 环境中的分发。
    """
    saved = _snapshot()
    try:
        PackageRegistry._entries = dict(entries)
        PackageRegistry._by_import_path = {entry.import_path: entry for entry in entries.values()}
        PackageRegistry._discovered = True
        PackageRegistry._incompatible = {}
        PackageRegistry._dependency_rejected = {}
        with _fake_environment(distributions):
            yield
    finally:
        _restore(saved)


def _test_load_order_is_dependency_first():
    """被依赖的包排在依赖它的包之前，同层按注册表键排序。"""
    entries = [
        _entry("module", "alpha", "akari-bot-module-alpha"),
        _entry("module", "beta", "akari-bot-module-beta"),
        _entry("module", "gamma", "akari-bot-module-gamma"),
        _entry("module", "zeta", "akari-bot-module-zeta"),
    ]
    distributions = {
        "akari-bot-module-alpha": _FakeDistribution("akari-bot-module-alpha", "1.0.0"),
        "akari-bot-module-beta": _FakeDistribution("akari-bot-module-beta", "1.0.0", ("akari-bot-module-zeta>=1.0",)),
        "akari-bot-module-gamma": _FakeDistribution(
            "akari-bot-module-gamma", "1.0.0", ("akari-bot-module-beta>=1.0,<2.0",)
        ),
        "akari-bot-module-zeta": _FakeDistribution("akari-bot-module-zeta", "1.0.0"),
    }
    with _discovered_from(entries, distributions):
        order = [entry.name for entry in PackageRegistry.load_order()]
        declared = {
            entry.name: [dependency.dist_name for dependency in PackageRegistry.dependencies(entry)]
            for entry in entries
        }
        dependents = [entry.name for entry in PackageRegistry.dependents(PackageRegistry.get("module", "zeta"))]
    return (
        order == ["alpha", "zeta", "beta", "gamma"]
        and declared["gamma"] == ["akari-bot-module-beta"]
        and dependents == ["beta"]
    )


def _test_directory_scanned_package_has_no_dependencies():
    """目录扫描的包没有分发 metadata，依赖恒为空元组且不被漏掉。"""
    scanned = _entry("module", "wiki")
    with _isolated_registry({"module:wiki": scanned}, {}):
        dependencies = PackageRegistry.dependencies(scanned)
        order = PackageRegistry.load_order()
    return dependencies == () and order == [scanned]


def _test_missing_dependency_is_rejected():
    """依赖未安装时该包不注册，原因写明缺哪个分发。"""
    entries = [
        _entry("module", "consumer", "akari-bot-module-consumer"),
        _entry("module", "plain", "akari-bot-module-plain"),
    ]
    distributions = {
        "akari-bot-module-consumer": _FakeDistribution(
            "akari-bot-module-consumer", "1.0.0", ("akari-bot-module-absent>=1.0",)
        ),
        "akari-bot-module-plain": _FakeDistribution("akari-bot-module-plain", "1.0.0"),
    }
    with _discovered_from(entries, distributions):
        registered = sorted(PackageRegistry.modules())
        rejected = PackageRegistry.incompatible()
        unresolved = PackageRegistry.by_import_path("modules.consumer")
        reported = PackageRegistry.report_lines()
    return (
        registered == ["plain"]
        and rejected == {"akari-bot-module-consumer": "missing dependency akari-bot-module-absent"}
        and unresolved is None
        and reported == ["akari-bot-module-consumer: missing dependency akari-bot-module-absent"]
    )


def _test_version_mismatch_is_rejected():
    """已装版本不满足描述符时拒绝注册，原因带已装版本与描述符。"""
    entries = [_entry("module", "consumer", "akari-bot-module-consumer")]
    distributions = {
        "akari-bot-module-consumer": _FakeDistribution(
            "akari-bot-module-consumer", "1.0.0", ("akari-bot-module-wiki>=2.0",)
        ),
        "akari-bot-module-wiki": _FakeDistribution("akari-bot-module-wiki", "1.2.0"),
    }
    with _discovered_from(entries, distributions):
        dependency = PackageRegistry.dependencies(entries[0])[0]
        rejected = PackageRegistry.incompatible()
        registered = PackageRegistry.modules()
    return (
        dependency.dist_name == "akari-bot-module-wiki"
        and dependency.specifier == ">=2.0"
        and dependency.installed_version == "1.2.0"
        and dependency.satisfied is False
        and not registered
        and rejected == {"akari-bot-module-consumer": "akari-bot-module-wiki 1.2.0 does not satisfy >=2.0"}
    )


def _test_circular_dependencies_are_rejected():
    """成环的全部包都不注册，原因列出完整环路径。"""
    expected = {
        ("a", "b"): "circular dependency akari-bot-module-a -> akari-bot-module-b -> akari-bot-module-a",
        ("a", "b", "c"): (
            "circular dependency akari-bot-module-a -> akari-bot-module-b -> akari-bot-module-c -> akari-bot-module-a"
        ),
    }
    for names, reason in expected.items():
        entries = [_entry("module", name, f"akari-bot-module-{name}") for name in names]
        distributions = {
            f"akari-bot-module-{names[index]}": _FakeDistribution(
                f"akari-bot-module-{names[index]}",
                "1.0.0",
                (f"akari-bot-module-{names[(index + 1) % len(names)]}>=1.0",),
            )
            for index in range(len(names))
        }
        with _discovered_from(entries, distributions):
            registered = PackageRegistry.modules()
            rejected = PackageRegistry.incompatible()
        if registered or rejected != {f"akari-bot-module-{name}": reason for name in names}:
            return False
    return True


def _test_disjoint_cycles_are_all_rejected():
    """互不相交的多个环全部被发现，每个环各报自己的路径。"""
    names = ("a", "b", "c", "d")
    edges = {"a": "b", "b": "a", "c": "d", "d": "c"}
    entries = [_entry("module", name, f"akari-bot-module-{name}") for name in names]
    distributions = {
        f"akari-bot-module-{name}": _FakeDistribution(
            f"akari-bot-module-{name}", "1.0.0", (f"akari-bot-module-{target}>=1.0",)
        )
        for name, target in edges.items()
    }
    with _discovered_from(entries, distributions):
        registered = PackageRegistry.modules()
        rejected = PackageRegistry.incompatible()
    first = rejected.get("akari-bot-module-a", "")
    second = rejected.get("akari-bot-module-c", "")
    return (
        not registered
        and set(rejected) == {f"akari-bot-module-{name}" for name in names}
        and "akari-bot-module-d" not in first
        and "akari-bot-module-b" not in second
    )


def _test_dependency_on_api_rejected_package_cascades():
    """依赖被 core API 门槛拒绝的包，依赖方也必须一起拒绝，原因指名该依赖。

    条目顺序刻意让依赖方先出现：初始判定时被依赖方尚未登记为拒绝，只有级联才能拦住它。
    """
    alpha = _entry("module", "alpha", "akari-bot-module-alpha")
    beta = PackageEntry(
        kind="module",
        name="beta",
        dist_name="akari-bot-module-beta",
        version="1.0.0",
        import_path="modules.beta",
        root=Path("."),
        manifest=PackageManifest(requires_core_api=">=99"),
    )
    distributions = {
        "akari-bot-module-alpha": _FakeDistribution("akari-bot-module-alpha", "1.0.0", ("akari-bot-module-beta>=1.0",)),
        "akari-bot-module-beta": _FakeDistribution("akari-bot-module-beta", "1.0.0"),
    }
    with _discovered_from([alpha, beta], distributions):
        registered = PackageRegistry.modules()
        rejected = PackageRegistry.incompatible()
        reported = PackageRegistry.report_lines()
    alpha_reason = rejected.get("akari-bot-module-alpha", "")
    return (
        not registered
        and set(rejected) == {"akari-bot-module-alpha", "akari-bot-module-beta"}
        and "akari-bot-module-beta" in alpha_reason
        and "refused" in alpha_reason
        and "requires core API" in rejected.get("akari-bot-module-beta", "")
        and any("akari-bot-module-alpha" in line and "akari-bot-module-beta" in line for line in reported)
    )


def _test_load_order_reports_cycle():
    """直接调用 load_order() 时成环抛异常，异常里列出完整环。"""
    entries = {
        "module:a": _entry("module", "a", "akari-bot-module-a"),
        "module:b": _entry("module", "b", "akari-bot-module-b"),
    }
    distributions = {
        "akari-bot-module-a": _FakeDistribution("akari-bot-module-a", "1.0.0", ("akari-bot-module-b>=1.0",)),
        "akari-bot-module-b": _FakeDistribution("akari-bot-module-b", "1.0.0", ("akari-bot-module-a>=1.0",)),
    }
    with _isolated_registry(entries, distributions):
        try:
            PackageRegistry.load_order()
        except CircularDependencyError as error:
            message = str(error)
            cycles = error.cycles
        else:
            raise AssertionError("成环时未抛 CircularDependencyError")
    return cycles == (("akari-bot-module-a", "akari-bot-module-b", "akari-bot-module-a"),) and (
        "akari-bot-module-a -> akari-bot-module-b -> akari-bot-module-a" in message
    )


def _test_extra_marked_dependencies_follow_installed_extras():
    """未装 extra 的依赖条目被忽略，已装 extra 的照常计入。"""
    consumer = _entry("module", "consumer", "akari-bot-module-consumer")
    distributions = {
        "akari-bot-module-consumer": _FakeDistribution(
            "akari-bot-module-consumer",
            "1.0.0",
            (
                "pytest>=7",
                "akari-bot-module-plain>=1.0",
                'akari-bot-module-optional>=1.0; extra == "dev"',
                'ruff>=0.5; extra == "dev"',
                'akari-bot-module-extra-dep>=1.0; extra == "test"',
                'pytest>=7; extra == "test"',
            ),
            ("dev", "test"),
        ),
        "akari-bot-module-plain": _FakeDistribution("akari-bot-module-plain", "1.0.0"),
        # optional 本身已装，但其所属的 dev extra 缺 ruff，仍视为未装
        "akari-bot-module-optional": _FakeDistribution("akari-bot-module-optional", "1.0.0"),
        "akari-bot-module-extra-dep": _FakeDistribution("akari-bot-module-extra-dep", "1.0.0"),
        "pytest": _FakeDistribution("pytest", "8.0.0"),
    }
    with _isolated_registry({"module:consumer": consumer}, distributions):
        declared = [dependency.dist_name for dependency in PackageRegistry.dependencies(consumer)]
    return declared == ["akari-bot-module-extra-dep", "akari-bot-module-plain"]


def _test_undeclared_ast_dependency_warns_and_stays_in_closure():
    """AST 扫出而 metadata 未声明的依赖告警一次，且仍进入 reload 闭包。"""
    scanned = {"modules.alpha": {"modules.beta"}, "modules.beta": set()}
    entry = _entry("module", "alpha")
    with (
        patch.object(ModulesManager, "modules", {name: object() for name in scanned}),
        patch.object(ModulesManager, "return_py_module", side_effect=lambda name: name),
        patch.object(ModulesManager, "_scan_package_dependencies", side_effect=lambda name: set(scanned[name])),
        patch.object(PackageRegistry, "by_import_path", return_value=entry),
        patch.object(PackageRegistry, "resolved_dependencies", return_value=()),
        patch.object(ModulesManager, "_undeclared_dependency_warned", set()),
        patch.object(loader_module.Logger, "warning") as warned,
    ):
        ModulesManager._rebuild_dependency_graph()
        graph = {name: set(dependencies) for name, dependencies in ModulesManager._dependency_graph.items()}
        closure = ModulesManager._reload_closure("modules.beta")
        ModulesManager._rebuild_dependency_graph()
    message = warned.call_args.args[0]
    return (
        graph == scanned
        and closure == ["modules.beta", "modules.alpha"]
        and warned.call_count == 1
        and "modules.alpha" in message
        and "modules.beta" in message
    )


@func_case
async def test_dependency_graph(tester: Tester):
    """core.registry: 模块依赖图测试"""
    await tester.test(_test_load_order_is_dependency_first, "拓扑序被依赖者在前")
    await tester.test(_test_directory_scanned_package_has_no_dependencies, "目录扫描包无声明依赖")
    await tester.test(_test_missing_dependency_is_rejected, "缺依赖的包被拒绝注册")
    await tester.test(_test_version_mismatch_is_rejected, "版本不满足的包被拒绝注册")
    await tester.test(_test_circular_dependencies_are_rejected, "成环的包全部被拒绝注册")
    await tester.test(_test_disjoint_cycles_are_all_rejected, "互不相交的环各自报出路径")
    await tester.test(_test_load_order_reports_cycle, "load_order 遇环抛异常并列出环")
    await tester.test(_test_dependency_on_api_rejected_package_cascades, "依赖被 API 拒绝的包级联拒绝")
    await tester.test(_test_extra_marked_dependencies_follow_installed_extras, "extra 未装的依赖被忽略")
    await tester.test(
        _test_undeclared_ast_dependency_warns_and_stays_in_closure,
        "未声明依赖告警并保留在闭包",
    )
    return tester
