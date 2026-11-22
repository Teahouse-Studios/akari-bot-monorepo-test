#!/usr/bin/env python3
"""按 /tmp/split_plan.json 写出 20 册审核稿与总索引。"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path("/Volumes/DATA/akari-bot-monorepo-test")
REVIEW = ROOT / ".review"
KIND = [
    ("md-paragraph", "Markdown 正文段落"),
    ("md-heading", "Markdown 标题"),
    ("md-list", "Markdown 列表项"),
    ("md-table", "Markdown 表格行"),
    ("py-comment", "Python 整行注释"),
    ("py-inline-comment", "Python 行尾注释"),
    ("py-docstring", "Python docstring"),
    ("json-value", "语言文件的字符串值"),
    ("cfg-comment", "配置文件的中文注释"),
]
LEGEND = "\n".join(f"| `{k}` | {d} |" for k, d in KIND)

units = json.loads((REVIEW / "units.json").read_text(encoding="utf-8"))
idx = {u["id"]: u for u in units}
plan = json.loads(Path("/tmp/split_plan.json").read_text(encoding="utf-8"))
names = [f"text-{i:02d}.md" for i in range(1, len(plan) + 1)]
total_chars = sum(len(u["text"]) for u in units)


def part_stats(g):
    us = [idx[i] for _, ids in g for i in ids]
    return min(u["id"] for u in us), max(u["id"] for u in us), len(us), len(g), sum(len(u["text"]) for u in us)


rows = []
for i, g in enumerate(plan, 1):
    a, b, n, nf, ch = part_stats(g)
    rows.append((i, names[i - 1], a, b, n, nf, ch))
part_index = "\n".join(
    f"| [{i:02d}]({f}) | U{a:06d}–U{b:06d} | {n:,} | {nf} | {ch:,} |" for i, f, a, b, n, nf, ch in rows)

seen = {}
for i, g in enumerate(plan, 1):
    for p, ids in g:
        seen.setdefault(p, []).append(i)

for i, g in enumerate(plan, 1):
    a, b, n, nf, ch = part_stats(g)
    head = [
        f"# 全仓可读文本审核稿 · 第 {i:02d} 册 / 共 {len(plan)} 册",
        "",
        f"覆盖 U{a:06d}–U{b:06d}，{nf} 个文件、{n:,} 个单元、{ch:,} 字符。"
        f"全稿 {len(units):,} 个单元、{len(seen):,} 个文件、{total_chars:,} 字符。",
        "",
        "改动只写在 `<<< UNIT … >>>` 与 `<<< END … >>>` 之间。UNIT 行含编号与位置，回填按编号对位，这一行不要动。",
        "",
        "## 分册索引",
        "",
        "| 册 | 覆盖单元 | 单元数 | 文件数 | 字符数 |",
        "| --- | --- | --- | --- | --- |",
        part_index,
        "",
        "## 本册文件",
        "",
        "| 文件 | 单元数 | 单元范围 | 字符数 |",
        "| --- | --- | --- | --- |",
    ]
    for p, ids in g:
        us = [idx[t] for t in ids]
        cont = "（续）" if len(seen[p]) > 1 and seen[p][0] != i else ""
        head.append(f"| `{p}`{cont} | {len(us)} | U{ids[0]:06d}–U{ids[-1]:06d} | {sum(len(u['text']) for u in us):,} |")
    head += ["", "## 单元类型", "", "| 类型 | 含义 |", "| --- | --- |", LEGEND, "", "## 正文", ""]
    body = []
    for p, ids in g:
        for t in ids:
            u = idx[t]
            ctx = f" | ctx={u['ctx']}" if u.get("ctx") else ""
            body.append(f"<<< UNIT U{t:06d} | {u['kind']} | {p}:{u['start']}-{u['end']}{ctx} >>>")
            body.append(u["text"])
            body.append(f"<<< END U{t:06d} >>>")
    (REVIEW / names[i - 1]).write_text("\n".join(head) + "\n".join(body) + "\n", encoding="utf-8")

files = []
for g in plan:
    for p, _ in g:
        if p not in files:
            files.append(p)
master = [
    "# 全仓可读文本审核稿 · 总索引",
    "",
    f"{len(files):,} 个文件、{len(units):,} 个单元、{total_chars:,} 字符，拆为 {len(plan)} 册。"
    f"正文在 `text-01.md` … `{names[-1]}`。",
    "",
    "回填按单元编号对位，只认 `<<< UNIT … >>>` 与 `<<< END … >>>` 之间的文字；UNIT 行不要动。",
    "",
    "## 分册",
    "",
    "| 册 | 覆盖单元 | 单元数 | 文件数 | 字符数 |",
    "| --- | --- | --- | --- | --- |",
    part_index,
    "",
    "## 文件索引",
    "",
    "| 文件 | 单元数 | 首个编号 | 分册 |",
    "| --- | --- | --- | --- |",
]
for p in files:
    ids = [t for g in plan for q, ts in g if q == p for t in ts]
    dst = "、".join(f"[{k:02d}]({names[k - 1]})" for k in seen[p])
    master.append(f"| `{p}` | {len(ids)} | U{ids[0]:06d} | {dst} |")
(REVIEW / "all-text.md").write_text("\n".join(master) + "\n", encoding="utf-8")
for i, f, a, b, n, nf, ch in rows:
    print(f"{f}  U{a:06d}–U{b:06d}  单元 {n:5d}  文件 {nf:4d}  字符 {ch:7d}")
