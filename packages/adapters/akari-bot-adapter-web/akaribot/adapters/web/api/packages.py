import re
from collections.abc import AsyncIterator
from typing import Any, Literal

import orjson
from fastapi import HTTPException, Request
from fastapi.responses import StreamingResponse

from akaribot.adapters.web.client import app, get_client_ip, limiter
from akaribot.core.api import Logger
from .auth import verify_jwt
from .cli_bridge import CliTimeout, CliUnavailable, parse_json, run_cli, stream_cli, write_lock

PACKAGE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
GIT_PREFIXES = ("git+", "git@", "ssh://", "git://", "https://", "http://")
PACKAGE_KINDS = ("module", "adapter")
UNINSTALL_MODES = {"keep": (), "purge": ("--purge-data",), "cascade": ("--cascade",)}


def _sse(event: str, data: dict[str, Any]) -> str:
    return f"event: {event}\ndata: {orjson.dumps(data).decode()}\n\n"


async def _read_body(request: Request) -> dict:
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid_json")
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="invalid_body")
    return body


def _package_name(value: Any) -> str:
    if not isinstance(value, str) or not PACKAGE_NAME_PATTERN.fullmatch(value):
        raise HTTPException(status_code=422, detail="invalid_package_name")
    return value


def _git_option(body: dict) -> list[str]:
    address = body.get("git")
    if not isinstance(address, str) or not address.startswith(GIT_PREFIXES):
        raise HTTPException(status_code=422, detail="invalid_git_address")
    args = ["--git", address]
    for key in ("ref", "subdir"):
        value = body.get(key)
        if value is None or value == "":
            continue
        if not isinstance(value, str) or value.startswith("-"):
            raise HTTPException(status_code=422, detail=f"invalid_{key}")
        args += [f"--{key}", value]
    return args


async def _query(*args: str) -> Any:
    try:
        result = await run_cli(*args)
    except CliUnavailable:
        raise HTTPException(status_code=503, detail="cli_unavailable")
    except CliTimeout:
        raise HTTPException(status_code=504, detail="cli_timeout")
    if result.returncode != 0:
        Logger.warning(f"[WebUI] CLI query failed ({' '.join(args)}): {result.stderr[-400:]}")
        raise HTTPException(status_code=502, detail="cli_failed")
    try:
        return parse_json(result.stdout)
    except ValueError:
        raise HTTPException(status_code=502, detail="cli_bad_output")


async def _write_events(args: list[str], label: str, ip: str) -> AsyncIterator[str]:
    success = False
    try:
        async with write_lock:
            yield _sse("start", {"action": label})
            returncode = -1
            async for kind, payload in stream_cli(*args):
                if kind == "line":
                    yield _sse("output", {"line": payload})
                else:
                    returncode = int(payload)
            success = returncode == 0
            yield _sse("done", {"success": success, "returncode": returncode})
    except Exception:
        Logger.exception(f"[WebUI] {ip} failed to {label}.")
        yield _sse("error", {"code": "internal_error"})
        yield _sse("done", {"success": False, "returncode": -1})
    finally:
        level = Logger.info if success else Logger.warning
        level(f"[WebUI] {ip} {'finished' if success else 'failed'} package action: {label}")


def _write_response(args: list[str], label: str, ip: str) -> StreamingResponse:
    if write_lock.locked():
        raise HTTPException(status_code=409, detail="operation_in_progress")
    Logger.info(f"[WebUI] {ip} started package action: {label}")
    return StreamingResponse(
        _write_events(args, label, ip),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _kind_args(request: Request) -> list[str]:
    kind = request.query_params.get("kind")
    if kind is None:
        return []
    if kind not in PACKAGE_KINDS:
        raise HTTPException(status_code=422, detail="invalid_kind")
    return ["--kind", kind]


@app.get("/api/packages")
@limiter.limit("20/minute")
async def list_packages(request: Request):
    verify_jwt(request)
    return {"packages": await _query("module", "list", "--json", *_kind_args(request))}


@app.get("/api/packages/available")
@limiter.limit("10/minute")
async def list_available_packages(request: Request, search: str = "", refresh: bool = False):
    verify_jwt(request)
    args = ["module", "available", "--json", *_kind_args(request)]
    if search.strip():
        args += ["--search", search.strip()]
    if refresh:
        args.append("--refresh")
    return {"packages": await _query(*args)}


@app.get("/api/packages/status")
@limiter.limit("20/minute")
async def get_module_load_status(request: Request):
    verify_jwt(request)
    return await _query("module", "status", "--json")


@app.post("/api/packages/install")
@limiter.limit("3/minute")
async def install_package(request: Request):
    ip = get_client_ip(request)
    verify_jwt(request)
    body = await _read_body(request)
    if body.get("git"):
        args = ["module", "add", *_git_option(body)]
        label = f"install {body['git']}"
    else:
        name = _package_name(body.get("name"))
        args = ["module", "add", name]
        label = f"install {name}"
    if body.get("force") is True:
        args.append("--force")
    return _write_response(args, label, ip)


@app.post("/api/packages/uninstall")
@limiter.limit("3/minute")
async def uninstall_package(request: Request):
    ip = get_client_ip(request)
    verify_jwt(request)
    body = await _read_body(request)
    name = _package_name(body.get("name"))
    mode: Literal["keep", "purge", "cascade"] = body.get("mode", "keep")
    if mode not in UNINSTALL_MODES:
        raise HTTPException(status_code=422, detail="invalid_mode")
    args = ["module", "remove", name, *UNINSTALL_MODES[mode], "--yes"]
    return _write_response(args, f"uninstall {name} ({mode})", ip)


@app.post("/api/packages/update")
@limiter.limit("3/minute")
async def update_packages(request: Request):
    ip = get_client_ip(request)
    verify_jwt(request)
    body = await _read_body(request)
    names = body.get("names") or []
    if not isinstance(names, list):
        raise HTTPException(status_code=422, detail="invalid_names")
    if body.get("all") is True:
        args = ["module", "update", "--all"]
    elif names:
        args = ["module", "update", *(_package_name(name) for name in names)]
    else:
        raise HTTPException(status_code=422, detail="missing_target")
    if body.get("force") is True:
        args.append("--force")
    args.append("--yes")
    return _write_response(args, "update", ip)
