"""构建产物的本机静态服务器。

预览只绑定调用方显式给出的地址，默认回环地址；解析规则与 VitePress 的 ``cleanUrls`` 一致，
``/foo`` 找不到文件时回落到 ``foo.html``，目录请求回落到 ``index.html``，其余交给 ``404.html``。
"""

from __future__ import annotations

import mimetypes
import posixpath
import threading
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

DEFAULT_HOST = "127.0.0.1"
_TEXTUAL_TYPES = frozenset({"application/javascript", "application/json", "image/svg+xml"})


class StaticServer:
    """一个目录的只读 HTTP 服务。

    :param directory: 站点根目录。
    :param host: 绑定地址。
    :param port: 端口，``0`` 表示由系统分配。
    """

    def __init__(self, directory: Path, host: str = DEFAULT_HOST, port: int = 0) -> None:
        self.directory = Path(directory).expanduser().resolve()
        self.host = host or DEFAULT_HOST
        self.port = int(port)
        self._httpd: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def url(self) -> str:
        """服务根 URL；未启动时抛出 ``RuntimeError``。"""
        if self._httpd is None:
            raise RuntimeError("server is not started")
        address = self._httpd.server_address
        host = str(address[0])
        display = f"[{host}]" if ":" in host else host
        return f"http://{display}:{address[1]}/"

    def start(self) -> str:
        """启动服务并返回根 URL；重复调用返回同一地址。"""
        if self._httpd is not None:
            return self.url
        handler = partial(_DocsRequestHandler, directory=self.directory)
        httpd = _ThreadingHTTPServer((self.host, self.port), handler)
        httpd.daemon_threads = True
        thread = threading.Thread(target=httpd.serve_forever, name="akaribot-docs-preview", daemon=True)
        thread.start()
        self._httpd = httpd
        self._thread = thread
        return self.url

    def stop(self) -> None:
        """停止服务并释放端口。"""
        if self._httpd is None:
            return
        self._httpd.shutdown()
        self._httpd.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)
        self._httpd = None
        self._thread = None

    def wait(self) -> None:
        """阻塞到服务停止。"""
        if self._thread is not None:
            self._thread.join()

    def __enter__(self) -> StaticServer:
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.stop()


class _ThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


class _DocsRequestHandler(BaseHTTPRequestHandler):
    server_version = "AkariDocs/1"

    def __init__(self, *args: Any, directory: Path, **kwargs: Any) -> None:
        self.directory = Path(directory)
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler 的协议方法名
        self._serve(head=False)

    def do_HEAD(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler 的协议方法名
        self._serve(head=True)

    def log_message(self, format: str, *args: Any) -> None:
        return None

    def _serve(self, *, head: bool) -> None:
        target = self._resolve()
        if target is None:
            self._send_not_found(head=head)
            return
        self._send_file(target, head=head)

    def _resolve(self) -> Path | None:
        raw = urlsplit(self.path).path
        relative = posixpath.normpath(unquote(raw))
        parts = [part for part in relative.split("/") if part not in ("", ".")]
        if any(part == ".." for part in parts):
            return None
        candidate = self.directory.joinpath(*parts)
        try:
            resolved = candidate.resolve()
            resolved.relative_to(self.directory)
        except (OSError, ValueError):
            return None
        if resolved.is_dir():
            index = resolved / "index.html"
            return index if index.is_file() else None
        if resolved.is_file():
            return resolved
        clean = resolved.with_name(f"{resolved.name}.html")
        return clean if clean.is_file() else None

    def _send_file(self, path: Path, *, head: bool, status: int = 200) -> None:
        try:
            body = path.read_bytes()
        except OSError:
            self._send_not_found(head=head)
            return
        content_type = self._content_type(path)
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if head:
            return
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            return

    def _send_not_found(self, *, head: bool) -> None:
        fallback = self.directory / "404.html"
        if fallback.is_file():
            self._send_file(fallback, head=head, status=404)
            return
        body = b"404 Not Found\n"
        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def _content_type(self, path: Path) -> str:
        guessed = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if guessed.startswith("text/") or guessed in _TEXTUAL_TYPES:
            return f"{guessed}; charset=utf-8"
        return guessed
