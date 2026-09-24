"""模块作者的声明处与读取路径。

作者写在各包 ``pyproject.toml`` 的 ``[project] authors``，不再出现在 ``module()`` 定义里；运行时
由发现层按包根目录读回。本文件固定：解析器认得出正确的 pyproject、不被无关文件误取、wheel 场景
退回分发元数据，以及定义层确实不再接受 ``developers``。
"""

import inspect
import tomllib
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.instance import PackageInfo
from akaribot.cli.tui.modules import ModuleRecord, normalize_records
from akaribot.core.component import module as module_factory
from akaribot.core.registry import declared_authors
from akaribot.testing import Tester, func_case

REPO_ROOT = Path(__file__).resolve().parents[3]


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _write_package(root: Path, dist: str, authors: list[str]) -> Path:
    package = root / dist
    (package / "akaribot" / "modules" / "demo").mkdir(parents=True)
    entries = "".join(f'    {{ name = "{name}" }},\n' for name in authors)
    (package / "pyproject.toml").write_text(
        f'[project]\nname = "{dist}"\nversion = "0.1.0"\nauthors = [\n{entries}]\n', encoding="utf-8"
    )
    return package


def _test_definition_layer_no_longer_accepts_developers():
    return "developers" not in inspect.signature(module_factory).parameters


def _test_definition_layer_has_no_hand_written_authors():
    offenders: list[str] = []
    for base in (REPO_ROOT / "packages" / "modules", REPO_ROOT / "packages" / "adapters"):
        if not base.is_dir():
            continue
        for path in base.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            if "developers=" in path.read_text(encoding="utf-8"):
                offenders.append(path.name)
    return offenders == []


def _test_authors_read_from_package_pyproject():
    with TemporaryDirectory(prefix="akari-authors-") as raw:
        root = Path(raw)
        package = _write_package(root, "akari-bot-module-demo", ["Alice", "Bob"])
        found = declared_authors(package / "akaribot" / "modules" / "demo", "akari-bot-module-demo")
    return found == ["Alice", "Bob"]


def _test_unrelated_pyproject_is_not_used():
    with TemporaryDirectory(prefix="akari-authors-") as raw:
        root = Path(raw)
        _write_package(root, "akari-bot-module-demo", ["Alice"])
        (root / "akaribot" / "modules" / "other").mkdir(parents=True)
        wrong_name = declared_authors(root / "akaribot" / "modules" / "other", "akari-bot-module-other")
    return wrong_name == []


def _test_declared_packages_carry_authors():
    samples = {
        "akari-bot-module-coin": ["Light-Beacon"],
        "akari-bot-module-oba": ["WorldHim"],
    }
    for dist, expected in samples.items():
        pyproject = REPO_ROOT / "packages" / "modules" / dist / "pyproject.toml"
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        if [entry["name"] for entry in data["project"]["authors"]] != expected:
            return False
        root = pyproject.parent / "akaribot" / "modules" / dist.removeprefix("akari-bot-module-")
        if declared_authors(root, dist) != expected:
            return False
    return True


def _test_missing_metadata_yields_empty():
    with TemporaryDirectory(prefix="akari-authors-") as raw:
        return declared_authors(Path(raw), "akari-bot-module-definitely-absent") == []


def _test_cli_package_info_carries_authors():
    info = PackageInfo.from_mapping({"dist": "akari-bot-module-demo", "developers": ["Alice", "Bob"]})
    return info.developers == ("Alice", "Bob")


def _test_cli_reads_authors_from_workspace_pyproject():
    with TemporaryDirectory(prefix="akari-authors-") as raw:
        package = _write_package(Path(raw), "akari-bot-module-demo", ["Alice"])
        return engine.package_authors(package) == ("Alice",)


def _test_registry_entry_carries_authors():
    entry = engine.RegistryEntry.from_mapping(
        {"name": "demo", "dist": "akari-bot-module-demo", "developers": ["Alice", "Bob"]}
    )
    return entry.developers == ("Alice", "Bob")


def _test_tui_record_and_detail_use_authors():
    record = normalize_records([{"dist": "akari-bot-module-demo", "name": "demo", "developers": ["Alice", "Bob"]}])[0]
    return record.developers == ("Alice", "Bob") and record == ModuleRecord(
        **{**record.__dict__, "developers": ("Alice", "Bob")}
    )


def _test_defined_module_resolves_its_own_package():
    # ``module()`` 从调用帧取模块名再交给发现层；多退一层会取到 ``importlib._bootstrap``，
    # ``_py_module_name`` 与作者一起变成空串，热重载、locale 指纹与依赖图同样失去依据。
    import akaribot.modules.coin  # noqa: F401 - 导入即执行 module() 注册
    from akaribot.core.loader import ModulesManager

    registered = ModulesManager.modules.get("coin")
    if registered is None:
        return False
    return registered._py_module_name == "coin" and list(registered.developers) == ["Light-Beacon"]


@func_case
async def test_module_authors(tester: Tester):
    """模块作者：pyproject 声明与读取链路测试"""
    _use_cli_locale()
    await tester.test(_test_definition_layer_no_longer_accepts_developers, "module() 不再接 developers")
    await tester.test(_test_definition_layer_has_no_hand_written_authors, "定义层无手写作者")
    await tester.test(_test_authors_read_from_package_pyproject, "按包根读 pyproject 作者")
    await tester.test(_test_unrelated_pyproject_is_not_used, "名字不符的 pyproject 不误取")
    await tester.test(_test_declared_packages_carry_authors, "仓库内声明与读取一致")
    await tester.test(_test_missing_metadata_yields_empty, "无声明时返回空")
    await tester.test(_test_cli_package_info_carries_authors, "CLI 包信息带作者")
    await tester.test(_test_cli_reads_authors_from_workspace_pyproject, "CLI 读工作区 pyproject")
    await tester.test(_test_registry_entry_carries_authors, "registry 条目带作者")
    await tester.test(_test_tui_record_and_detail_use_authors, "TUI 记录认作者字段")
    await tester.test(_test_defined_module_resolves_its_own_package, "定义模块认出所属包并取到作者")
    return tester
