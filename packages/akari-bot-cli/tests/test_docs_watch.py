"""``akaribot.cli.docs_engine.watch``：路径过滤、事件去重与批量返回。"""

import time
from pathlib import Path
from tempfile import TemporaryDirectory

from akaribot.cli.docs_engine.watch import CONFIG, DOCS, PathWatcher, WatchTarget
from akaribot.testing import Tester, func_case


def _collect(watcher: PathWatcher, predicate, timeout: float = 8.0) -> list:
    seen: list = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        seen.extend(watcher.poll(0.2))
        if predicate(seen):
            break
    return seen


def _test_reports_markdown_and_ignores_noise():
    with TemporaryDirectory(prefix="akari-docs-watch-") as raw:
        root = Path(raw) / "docs"
        (root / "pages").mkdir(parents=True)
        (root / "node_modules" / "pkg").mkdir(parents=True)
        watcher = PathWatcher([WatchTarget(root, DOCS)], debounce=0.05)
        watcher.start()
        try:
            (root / "pages" / "index.md").write_text("# 标题", encoding="utf-8")
            (root / "node_modules" / "pkg" / "readme.md").write_text("x", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git" / "stash.md").write_text("x", encoding="utf-8")
            (root / "pages" / "draft.swp").write_text("x", encoding="utf-8")
            changes = _collect(watcher, lambda seen: any(change.path.name == "index.md" for change in seen))
        finally:
            watcher.stop()
    names = {change.path.name for change in changes}
    return names == {"index.md"} and all(change.kind == DOCS for change in changes)


def _test_file_target_reports_only_its_own_path():
    with TemporaryDirectory(prefix="akari-docs-watch-") as raw:
        root = Path(raw)
        config = root / "docs.toml"
        config.write_text("a = 1", encoding="utf-8")
        sibling = root / "other.toml"
        sibling.write_text("b = 2", encoding="utf-8")
        watcher = PathWatcher([WatchTarget(config, CONFIG, recursive=False)], debounce=0.05)
        watcher.start()
        try:
            sibling.write_text("b = 3", encoding="utf-8")
            config.write_text("a = 2", encoding="utf-8")
            changes = _collect(watcher, lambda seen: any(change.path == config for change in seen))
        finally:
            watcher.stop()
    return [change.path.name for change in changes] == ["docs.toml"] and changes[0].kind == CONFIG


def _test_repeated_edits_collapse_into_one_change():
    with TemporaryDirectory(prefix="akari-docs-watch-") as raw:
        root = Path(raw)
        page = (root / "guide.md").resolve()
        page.write_text("一", encoding="utf-8")
        watcher = PathWatcher([WatchTarget(root, DOCS)], debounce=0.1)
        watcher.start()
        try:
            page.write_text("二", encoding="utf-8")
            page.write_text("三", encoding="utf-8")
            changes = _collect(watcher, lambda seen: any(change.path == page for change in seen))
        finally:
            watcher.stop()
    return len([change for change in changes if change.path == page]) == 1


@func_case
async def test_docs_watch(tester: Tester):
    """cli.docs_engine.watch: 文档目录监听与路径过滤"""
    await tester.test(_test_reports_markdown_and_ignores_noise, "只报告文档目录内的有效改动")
    await tester.test(_test_file_target_reports_only_its_own_path, "文件目标只报告自身改动")
    await tester.test(_test_repeated_edits_collapse_into_one_change, "同一文件的连续改动合并为一条")
    return tester
