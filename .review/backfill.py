#!/usr/bin/env python3
"""按审核稿回填原文件。--check 只做恒等校验，--apply 读回改动。"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path("/Volumes/DATA/akari-bot-monorepo-test")
REVIEW = ROOT / ".review"
UNIT_HDR = re.compile(r"^<<< UNIT U(\d{6}) \| [^|]+ \| (.+?):(\d+)-(\d+)(?: \| ctx=.*)? >>>$")

def load_units():
    return json.loads((REVIEW / "units.json").read_text(encoding="utf-8"))

def parse_review(path: Path):
    """返回 {uid: text}，text 为 UNIT 与 END 之间的原文。"""
    out, cur, buf = {}, None, []
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = UNIT_HDR.match(line)
        if m:
            if cur is not None: raise SystemExit(f"嵌套 UNIT: U{cur}")
            cur = int(m.group(1)); buf = []; continue
        if line.startswith("<<< END U") and cur is not None:
            out[cur] = "\n".join(buf); cur = None; buf = []; continue
        if cur is not None: buf.append(line)
    if cur is not None: raise SystemExit(f"未闭合的单元 U{cur}")
    return out

def rebuild_doc(text: str, meta: dict) -> str:
    ind, q = meta["indent"], meta["quote"]
    if not meta["multi"]:
        return f"{ind}{q}{text}{q}"
    body = "\n".join((ind + ln) if ln.strip() else "" for ln in text.split("\n"))
    return f"{ind}{q}\n{body}\n{ind}{q}"

def apply_file(path: Path, units: list[dict], new_texts: dict[int, str]) -> str:
    src = path.read_text(encoding="utf-8")
    if path.suffix == ".json" and any(u["kind"] == "json-value" for u in units):
        chars = list(src)
        for u in sorted(units, key=lambda x: -x["json"]["span"][0]):
            s, e = u["json"]["span"]
            t = new_texts.get(u["id"], u["text"])
            chars[s:e] = list(json.dumps(t, ensure_ascii=False)[1:-1])
        return "".join(chars)
    lines = src.split("\n")
    for u in sorted(units, key=lambda x: -x["start"]):
        t = new_texts.get(u["id"], u["text"])
        if u["kind"] in ("py-comment", "py-inline-comment"):
            lines = patch_comment(lines, u, t)
            continue
        if u["kind"] == "py-docstring":
            block = rebuild_doc(t, u["doc"]).split("\n")
        else:
            block = t.split("\n")
        lines[u["start"] - 1:u["end"]] = block
    return "\n".join(lines)

def _dedent(rows: list[str]) -> list[str]:
    ws = [len(r) - len(r.lstrip()) for r in rows if r.strip()]
    cut = min(ws) if ws else 0
    return [r[cut:] if r.strip() else "" for r in rows]

def patch_comment(lines: list[str], u: dict, text: str) -> list[str]:
    """按注释记号列区间改写，代码前缀保持不动。"""
    spans = u["spans"]
    new = _dedent(text.split("\n"))
    if u["kind"] == "py-inline-comment" and len(new) != 1:
        raise SystemExit(f"行尾注释只能单行：{u['path']}:{spans[0][0]}")
    for i in range(len(spans) - 1, -1, -1):
        row, c0, c1 = spans[i]
        ln = lines[row - 1]
        if i < len(new):
            lines[row - 1] = ln[:c0] + new[i] + ln[c1:]
        else:
            rest = ln[:c0] + ln[c1:]
            if rest.strip():
                lines[row - 1] = rest
            else:
                del lines[row - 1]
    if len(new) > len(spans):
        row, c0, _ = spans[-1]
        indent = " " * c0 if not lines[row - 1][:c0].strip() else lines[row - 1][:c0]
        for k, extra in enumerate(new[len(spans):]):
            lines.insert(row + k, indent + extra)
    return lines

def collect(paths):
    """合并多册审核稿，返回 {uid: text}；重复编号直接报错。"""
    out = {}
    for path in paths:
        for uid, text in parse_review(Path(path)).items():
            if uid in out and out[uid] != text:
                raise SystemExit(f"单元 U{uid:06d} 在多册里内容不同")
            out[uid] = text
    return out


def reviews(argv):
    if argv:
        return [Path(a) for a in argv]
    return sorted(REVIEW.glob("text-[0-9][0-9].md"))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    units = load_units()
    by_file: dict[str, list[dict]] = {}
    for u in units: by_file.setdefault(u["path"], []).append(u)
    if mode == "--check":
        bad = []
        for path, us in by_file.items():
            out = apply_file(ROOT / path, us, {})
            if out != (ROOT / path).read_text(encoding="utf-8"):
                bad.append(path)
        print(f"文件 {len(by_file)}，units.json 与源文件不一致 {len(bad)}")
        for b in bad[:10]: print("  ", b)
        return
    edited = collect(reviews(sys.argv[2:]))
    new_texts = {}
    for u in units:
        if u["id"] not in edited: raise SystemExit(f"缺少单元 U{u['id']:06d}")
        if edited[u["id"]] != u["text"]: new_texts[u["id"]] = edited[u["id"]]
    changed_files = [p for p, us in by_file.items() if any(u["id"] in new_texts for u in us)]
    print(f"单元 {len(units)}，改动 {len(new_texts)}，涉及文件 {len(changed_files)}")
    if mode == "--plan":
        per = {}
        base = {u["id"]: u["text"] for u in units}
        for path in reviews(sys.argv[2:]):
            us = parse_review(Path(path))
            per[Path(path).name] = sum(1 for i, t in us.items() if base[i] != t)
        for name, n in per.items():
            print(f"  {name}  改动 {n}")
        for p in changed_files[:20]: print("  ", p)
        return
    if mode != "--apply":
        raise SystemExit("用法：--check | --plan [手册…] | --apply [手册…]")
    for path in changed_files:
        p = ROOT / path
        p.write_text(apply_file(p, by_file[path], new_texts), encoding="utf-8")
    print(f"回填文件 {len(changed_files)}")


if __name__ == "__main__":
    main()
