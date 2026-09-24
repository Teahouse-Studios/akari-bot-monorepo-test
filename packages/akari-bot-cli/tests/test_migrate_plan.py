"""``migrate legacy`` 的安装候选与跳过诊断测试。

旧版单仓库的 ``modules/`` 本来就含全部官方模块，按目录决定安装会把四十余个用户从未启用的模块
连同重依赖一起装进新实例，还会把「未映射」与「未启用」混成同一类诊断。此处固定：候选只取旧库
``module_status.load = 1``，目录只用于诊断；库读不到时不得退化成「安装全部目录」。
"""

import sqlite3
import tempfile
from pathlib import Path

from akaribot.cli.commands.migrate import LegacyProject, _enabled_modules, _plan_migration
from akaribot.cli.venv import RegistryCatalog, RegistryEntry
from akaribot.testing import Tester, func_case

# 旧版 modules/ 里的目录：42 个官方模块，用户只装载过 dice 与 wiki 家族。
ALL_DIRS = (
    "dice",
    "wiki",
    "wikilog",
    "maimai",
    "phigros",
    "cytoid",
    "wordle",
    "color",
    "coin",
    "random",
    "bilibili",
    "github",
    "tweet",
    "ncmusic",
    "ip",
    "whois",
    "idlist",
    "exchange_rate",
    "convert",
    "chemical_code",
    "emojimix",
    "twenty_four",
    "mcv",
    "mcv_rss",
    "mcmod",
    "mcplayer",
    "mcserver",
    "minecraft_news",
    "mojang_status",
    "nintendo_err",
    "oba",
    "threedsdb",
    "wolframalpha",
    "mkey",
    "mod_dl",
    "bugtracker",
    "image",
    "nbnhhsh",
    "arcaea",
    "arcaea_rss",
    "ai",
    "captcha",
)


def _catalog() -> RegistryCatalog:
    # 未装载的模块也要在 registry 里有映射：否则「不安装」可能只是因为查不到分发，用例就分不清
    # 「按启用状态筛选」与「碰巧映射不到」。
    entries = {}
    for name in ("dice", "wiki", "maimai", "phigros"):
        provides = ("wiki", "wikilog") if name == "wiki" else (name,)
        entries[f"akari-bot-module-{name}"] = RegistryEntry(
            name=name,
            dist=f"akari-bot-module-{name}",
            kind="module",
            provides_modules=provides,
            legacy_module_map=provides,
        )
    return RegistryCatalog(entries=entries)


def _legacy(enabled: tuple[str, ...], *, readable: bool) -> LegacyProject:
    return LegacyProject(
        root=Path("/nonexistent-legacy"),
        module_dirs=ALL_DIRS,
        enabled_modules=enabled,
        module_status_readable=readable,
    )


def _test_only_loaded_modules_are_installed():
    plan = _plan_migration(_legacy(("dice", "wiki", "wikilog"), readable=True), _index(), _catalog())
    return plan.module_dists == ["akari-bot-module-dice", "akari-bot-module-wiki"]


def _test_wiki_family_collapses_to_one_distribution():
    plan = _plan_migration(_legacy(("dice", "wiki", "wikilog"), readable=True), _index(), _catalog())
    names = [name for name, _, _ in plan.modules]
    return names == ["dice", "wiki", "wikilog"] and len(plan.module_dists) == 2


def _test_unloaded_directories_are_reported_not_installed():
    plan = _plan_migration(_legacy(("dice",), readable=True), _index(), _catalog())
    return (
        plan.module_dists == ["akari-bot-module-dice"]
        and plan.unmapped == []
        and len(plan.skipped) == len(ALL_DIRS) - 1
        and "wiki" in plan.skipped
        and "maimai" in plan.skipped
    )


def _test_unreadable_database_installs_nothing():
    plan = _plan_migration(_legacy((), readable=False), _index(), _catalog())
    return plan.module_dists == [] and plan.status_readable is False and len(plan.skipped) == len(ALL_DIRS)


def _test_readable_but_empty_database_also_installs_nothing():
    plan = _plan_migration(_legacy((), readable=True), _index(), _catalog())
    return plan.module_dists == [] and plan.status_readable is True and len(plan.skipped) == len(ALL_DIRS)


def _index() -> dict[str, str]:
    index: dict[str, str] = {}
    for entry in _catalog().entries.values():
        for name in (*entry.provides_modules, *entry.legacy_module_map):
            index.setdefault(name.replace("-", "_"), entry.dist)
    return index


def _test_enabled_modules_reads_load_flag():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "save.db"
        with sqlite3.connect(path) as conn:
            conn.execute("CREATE TABLE module_status (module_name TEXT, load INTEGER)")
            conn.executemany("INSERT INTO module_status VALUES (?, ?)", [("dice", 1), ("maimai", 0), ("wiki", 1)])
        names, readable = _enabled_modules((path,))
    return names == ("dice", "wiki") and readable is True


def _test_missing_status_table_is_reported_unreadable():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "save.db"
        with sqlite3.connect(path) as conn:
            conn.execute("CREATE TABLE other (x INTEGER)")
        names, readable = _enabled_modules((path,))
    return names == () and readable is False


def _test_absent_database_is_reported_unreadable():
    names, readable = _enabled_modules((Path("/nonexistent") / "save.db",))
    return names == () and readable is False


@func_case
async def test_migrate_plan(tester: Tester):
    """cli.commands.migrate: 迁移候选与跳过诊断测试"""
    await tester.test(_test_only_loaded_modules_are_installed, "只安装旧库启用过的模块")
    await tester.test(_test_wiki_family_collapses_to_one_distribution, "wiki 家族多对一去重")
    await tester.test(_test_unloaded_directories_are_reported_not_installed, "未装载目录进跳过清单")
    await tester.test(_test_unreadable_database_installs_nothing, "库不可读时不安装任何普通模块")
    await tester.test(_test_readable_but_empty_database_also_installs_nothing, "库可读且为空时同样不安装")
    await tester.test(_test_enabled_modules_reads_load_flag, "只读 load = 1 的记录")
    await tester.test(_test_missing_status_table_is_reported_unreadable, "缺 module_status 表算不可读")
    await tester.test(_test_absent_database_is_reported_unreadable, "缺库文件算不可读")
    return tester
