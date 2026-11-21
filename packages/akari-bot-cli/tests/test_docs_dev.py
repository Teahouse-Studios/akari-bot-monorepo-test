"""``akaribot.cli.docs_engine.dev``：镜像同步、变更归类与运行锁。"""

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli.docs_engine.dev import CONTENT, STRUCTURE, classify, lock_active, read_lock_at, sync_tree
from akaribot.cli.docs_engine.watch import CONFIG, DOCS, MANIFEST, THEME, Change
from akaribot.testing import Tester, func_case


def _test_sync_tree_mirrors_changes_and_keeps_node_modules():
    with TemporaryDirectory(prefix="akari-docs-dev-") as raw:
        base = Path(raw)
        source = base / "src"
        target = base / "mirror"
        (source / "a").mkdir(parents=True)
        (source / "a" / "x.md").write_text("一", encoding="utf-8")
        (source / ".vitepress").mkdir()
        (source / ".vitepress" / "config.mts").write_text("export default {}", encoding="utf-8")
        (target / "node_modules" / "pkg").mkdir(parents=True)
        (target / "node_modules" / "pkg" / "index.js").write_text("module", encoding="utf-8")
        (target / ".vitepress" / "cache" / "deps").mkdir(parents=True)
        (target / ".vitepress" / "cache" / "deps" / "vite.js").write_text("dep", encoding="utf-8")
        (target / "stale.md").write_text("旧", encoding="utf-8")

        first = sync_tree(source, target)
        second = sync_tree(source, target)
        (source / "a" / "x.md").write_text("二", encoding="utf-8")
        third = sync_tree(source, target)

        content = (target / "a" / "x.md").read_text(encoding="utf-8")
        kept = (target / "node_modules" / "pkg" / "index.js").exists()
        cached = (target / ".vitepress" / "cache" / "deps" / "vite.js").exists()
        stale = (target / "stale.md").exists()
    return (
        set(first.written) == {"a/x.md", ".vitepress/config.mts"}
        and first.written[-1] == ".vitepress/config.mts"
        and first.removed == ("stale.md",)
        and second.written == ()
        and second.removed == ()
        and third.written == ("a/x.md",)
        and content == "二"
        and kept
        and cached
        and not stale
    )


def _test_classify_orders_manifest_config_theme_structure():
    cases = (
        ([Change(Path("docs-theme.json"), "modified", MANIFEST)], MANIFEST),
        ([Change(Path("docs.toml"), "modified", CONFIG)], CONFIG),
        ([Change(Path("index.ts"), "modified", THEME)], THEME),
        ([Change(Path("guide.md"), "deleted", DOCS)], STRUCTURE),
        ([Change(Path("guide.md"), "modified", DOCS)], CONTENT),
    )
    return [classify(changes) for changes, _ in cases] == [expected for _, expected in cases]


def _test_lock_roundtrip_and_pid_check():
    with TemporaryDirectory(prefix="akari-docs-dev-") as raw:
        path = Path(raw) / ".dev.lock"
        missing = read_lock_at(path)
        path.write_text(
            json.dumps(
                {"pid": os.getpid(), "host": "127.0.0.1", "port": 5173, "base": "/", "started_at": 0},
            ),
            encoding="utf-8",
        )
        lock = read_lock_at(path)
        active = lock_active(lock)
        path.write_text(
            json.dumps(
                {"pid": 1_000_000_000, "host": "127.0.0.1", "port": 0, "base": "/", "started_at": 0},
            ),
            encoding="utf-8",
        )
        stale = lock_active(read_lock_at(path))
        path.write_text("not json", encoding="utf-8")
        broken = read_lock_at(path)
    return (
        missing is None
        and lock is not None
        and lock.pid == os.getpid()
        and lock.port == 5173
        and active
        and not stale
        and broken is None
        and not lock_active(None)
    )


@func_case
async def test_docs_dev(tester: Tester):
    """cli.docs_engine.dev: 镜像同步、变更归类与运行锁"""
    await tester.test(_test_sync_tree_mirrors_changes_and_keeps_node_modules, "差分同步只写变化并保留运行时目录")
    await tester.test(_test_classify_orders_manifest_config_theme_structure, "变更归类按清单、配置、主题、结构排序")
    await tester.test(_test_lock_roundtrip_and_pid_check, "运行锁读写与进程存活判断")
    return tester
