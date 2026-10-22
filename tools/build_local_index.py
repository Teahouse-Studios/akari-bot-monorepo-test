"""由本地产物目录生成 PEP 503 静态索引，用于不依赖外部仓库的全量安装验证。

TestPyPI 对新项目有窗口配额，57 个分发无法在一天内建齐；本工具把 ``dist/`` 建成一个静态
``/simple/`` 索引，配合 ``python -m http.server`` 即可让 uv/pip 按索引地址安装，验证与真实仓库
相同的解析、下载、元数据链路，且不消耗任何外部配额。

用法：::

    python tools/build_local_index.py --dist-dir dist --output local-index
    python tools/build_local_index.py --dist-dir dist --output local-index --serve 8123
"""

from __future__ import annotations

import argparse
import hashlib
import html
import shutil
import sys
from pathlib import Path

from packaging.utils import canonicalize_name, parse_sdist_filename, parse_wheel_filename


def _ensure_utf8_stdout() -> None:
    # Windows 控制台默认 cp1252，中文输出会抛 UnicodeEncodeError。
    if sys.stdout.encoding and sys.stdout.encoding.lower().replace("-", "") in ("utf8", "utf_8"):
        return
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def file_identity(path: Path) -> tuple[str, str]:
    """返回产物的规范化分发名与版本。

    :param path: wheel 或 sdist 路径。
    :return: ``(规范化名, 版本)``。
    """
    if path.name.endswith(".whl"):
        name, version, _, _ = parse_wheel_filename(path.name)
    else:
        name, version = parse_sdist_filename(path.name)
    return canonicalize_name(name), str(version)


def build(dist_dir: Path, output: Path) -> dict[str, list[Path]]:
    """把产物目录建成 ``simple/`` + ``files/`` 结构。

    :param dist_dir: 产物目录。
    :param output: 索引输出目录。
    :return: 规范化名到产物路径的映射。
    """
    if output.exists():
        shutil.rmtree(output)
    files_dir = output / "files"
    files_dir.mkdir(parents=True)
    projects: dict[str, list[Path]] = {}
    for path in sorted(dist_dir.iterdir()):
        if path.suffix != ".whl" and not path.name.endswith(".tar.gz"):
            continue
        name, _ = file_identity(path)
        target = files_dir / path.name
        shutil.copy2(path, target)
        projects.setdefault(name, []).append(target)

    simple = output / "simple"
    simple.mkdir()
    rows = []
    for name, paths in sorted(projects.items()):
        project_dir = simple / name
        project_dir.mkdir()
        links = []
        for path in paths:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            links.append(
                f'<a href="../../files/{html.escape(path.name)}#sha256={digest}">{html.escape(path.name)}</a><br>'
            )
        (project_dir / "index.html").write_text(
            "<!DOCTYPE html><html><body>\n" + "\n".join(links) + "\n</body></html>\n", encoding="utf-8"
        )
        rows.append(f'<a href="{html.escape(name)}/">{html.escape(name)}</a><br>')
    (simple / "index.html").write_text(
        "<!DOCTYPE html><html><body>\n" + "\n".join(rows) + "\n</body></html>\n", encoding="utf-8"
    )
    return projects


def main(argv: list[str] | None = None) -> int:
    """入口。

    :param argv: 命令行参数；缺省取 ``sys.argv[1:]``。
    :return: 进程退出码。
    """
    _ensure_utf8_stdout()
    parser = argparse.ArgumentParser(description="由本地产物目录生成 PEP 503 静态索引。")
    parser.add_argument("--dist-dir", type=Path, default=Path("dist"), help="产物目录")
    parser.add_argument("--output", type=Path, default=Path("local-index"), help="索引输出目录")
    parser.add_argument("--serve", type=int, default=0, help="生成后在改端口起 http.server（前台运行）")
    args = parser.parse_args(argv)

    if not args.dist_dir.is_dir():
        print(f"产物目录不存在：{args.dist_dir}", file=sys.stderr)
        return 1
    projects = build(args.dist_dir, args.output)
    total = sum(len(paths) for paths in projects.values())
    print(f"静态索引已生成：{args.output}（{len(projects)} 个分发 / {total} 个文件）")
    print(f"索引地址：http://127.0.0.1:{args.serve or 8000}/simple/")
    if args.serve:
        from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, format, *args) -> None:  # noqa: A002 - 覆盖父类签名
                pass

        handler = lambda *a, **kw: QuietHandler(*a, directory=str(args.output), **kw)  # noqa: E731
        with ThreadingHTTPServer(("127.0.0.1", args.serve), handler) as server:
            print(f"正在提供静态索引：http://127.0.0.1:{args.serve}/simple/（Ctrl+C 结束）")
            server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
