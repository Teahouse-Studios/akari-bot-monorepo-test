"""测试失败集合对拍：只允许基线里逐名列出的失败存在。

本仓库在拆分前就有 4 个用例失败（`test_parser_args`、`test_parser_recovery`、
`test_qqbot_modern_api`、`test_tos`，其中若干还带子用例）。runner 只要发现任何失败就以非 0 退出，
于是 CI 的第一轮 step 直接变红、后面的「只读包目录」一轮根本不会执行——而「失败集合与基线逐名
一致」这件事从来没有人检查过。

本工具把基线做成**可提交的小清单**而不是整份 junit.xml：新增、消失、错误文本变化都判失败，
因此既不能用 `|| true` 糊过去，也不能靠「失败数量没变」蒙混。既有失败修好后基线必须同步缩小，
否则本工具会因为「基线里还留着已经不会失败的条目」而失败。

用法：
    python tools/check_test_baseline.py --junit junit.xml --baseline tools/test_baseline.txt
    python tools/check_test_baseline.py --junit junit.xml --baseline tools/test_baseline.txt --update

退出码：0 一致；1 集合不一致；2 输入不可读。
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JUNIT = PROJECT_ROOT / "junit.xml"
DEFAULT_BASELINE = PROJECT_ROOT / "tools" / "test_baseline.txt"

FAILURE_TAGS = ("failure", "error")
SEPARATOR = "\t"
HEADER = "# 期望失败的测试：<用例名>\\t<failure|error>\\t<消息>，由 tools/check_test_baseline.py --update 生成。"


@dataclass(frozen=True)
class Failure:
    """一条失败记录。

    :param name: junit 里的用例名（含 ``::`` 子用例后缀）。
    :param kind: ``failure`` 或 ``error``。
    :param message: junit 的 message 属性；缺失时为空串。
    """

    name: str
    kind: str
    message: str

    def line(self) -> str:
        """基线文件里的一行。"""
        return SEPARATOR.join((self.name, self.kind, self.message))


def read_failures(path: Path) -> list[Failure]:
    """从 junit.xml 读出全部失败与错误。

    :param path: junit.xml 路径。
    :return: 失败记录列表，按用例名与类型排序。
    :raises OSError: 文件不可读。
    :raises ET.ParseError: 不是合法 XML。
    """
    root = ET.parse(path).getroot()
    found: list[Failure] = []
    for case in root.iter("testcase"):
        name = str(case.attrib.get("name") or "")
        for child in case:
            if child.tag not in FAILURE_TAGS:
                continue
            found.append(Failure(name=name, kind=child.tag, message=str(child.attrib.get("message") or "")))
    return sorted(found, key=lambda item: (item.name, item.kind, item.message))


def read_baseline(path: Path) -> list[Failure]:
    """读基线清单；空行与 ``#`` 开头的行忽略。

    :param path: 基线文件路径。
    :return: 基线里的失败记录。
    :raises OSError: 文件不可读。
    :raises ValueError: 某行不是三段制。
    """
    entries: list[Failure] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split(SEPARATOR)
        if len(parts) != 3:
            raise ValueError(f"{path}:{number} 不是「用例名\\t类型\\t消息」三段制：{line!r}")
        entries.append(Failure(name=parts[0], kind=parts[1], message=parts[2]))
    return sorted(entries, key=lambda item: (item.name, item.kind, item.message))


def compare(baseline: list[Failure], actual: list[Failure]) -> tuple[list[str], list[str], list[str]]:
    """比较基线与实际失败集合。

    分三类报告：基线里有、实际没有（应缩小基线）；实际有、基线没有（新增失败）；同名但类型或
    消息不同（错误文本变化）。同名用例只进第三类——若同时算进前两类，同一条变化会被报三次，
    真正的「新增」与「消失」也会被淹掉。

    :param baseline: 基线记录。
    :param actual: 实际记录。
    :return: 三元组——消失、新增、文本变化，元素为可读行。
    """
    by_name_baseline: dict[str, list[Failure]] = {}
    by_name_actual: dict[str, list[Failure]] = {}
    for item in baseline:
        by_name_baseline.setdefault(item.name, []).append(item)
    for item in actual:
        by_name_actual.setdefault(item.name, []).append(item)

    shared = set(by_name_baseline) & set(by_name_actual)
    vanished = [
        item.line()
        for name in sorted(set(by_name_baseline) - shared)
        for item in sorted(by_name_baseline[name], key=str)
    ]
    added = [
        item.line() for name in sorted(set(by_name_actual) - shared) for item in sorted(by_name_actual[name], key=str)
    ]
    changed: list[str] = []
    for name in sorted(shared):
        before = sorted((item.kind, item.message) for item in by_name_baseline[name])
        after = sorted((item.kind, item.message) for item in by_name_actual[name])
        if before != after:
            changed.append(f"{name}：基线 {before} → 实际 {after}")
    return vanished, added, changed


def write_baseline(path: Path, failures: list[Failure]) -> None:
    """把失败集合写回基线文件。

    :param path: 基线文件路径。
    :param failures: 要写入的记录。
    """
    lines = [HEADER, *(item.line() for item in failures)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    """命令行入口参数。"""
    parser = argparse.ArgumentParser(description="测试失败集合与基线逐名对拍")
    parser.add_argument("--junit", metavar="PATH", type=Path, default=DEFAULT_JUNIT, help="junit.xml 路径")
    parser.add_argument("--baseline", metavar="PATH", type=Path, default=DEFAULT_BASELINE, help="基线清单路径")
    parser.add_argument("--update", action="store_true", help="用本次实际失败集合重写基线，不判定成败")
    return parser


def main(argv: list[str] | None = None) -> int:
    """入口。返回进程退出码，0 表示失败集合与基线逐名一致。"""
    args = build_parser().parse_args(argv)
    try:
        actual = read_failures(args.junit)
    except (OSError, ET.ParseError) as error:
        print(f"无法读取 {args.junit}：{error}", file=sys.stderr)
        return 2

    if args.update:
        try:
            write_baseline(args.baseline, actual)
        except OSError as error:
            print(f"无法写入 {args.baseline}：{error}", file=sys.stderr)
            return 2
        print(f"已用 {len(actual)} 条失败记录重写 {args.baseline}。")
        return 0

    try:
        baseline = read_baseline(args.baseline)
    except (OSError, ValueError) as error:
        print(f"无法读取 {args.baseline}：{error}", file=sys.stderr)
        return 2

    vanished, added, changed = compare(baseline, actual)
    print(f"基线 {len(baseline)} 条，实际 {len(actual)} 条。")
    if not (vanished or added or changed):
        print("失败集合与基线逐名一致。")
        return 0
    if added:
        print(f"新增失败 {len(added)} 条（基线里没有，必须修掉或说明后更新基线）：")
        for line in added:
            print(f"  + {line}")
    if vanished:
        print(f"基线里有 {len(vanished)} 条本次未失败（修好了就同步缩小基线）：")
        for line in vanished:
            print(f"  - {line}")
    if changed:
        print(f"{len(changed)} 条同名用例的错误文本变化：")
        for line in changed:
            print(f"  ~ {line}")
    print("失败集合与基线不一致，退出码 1。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
