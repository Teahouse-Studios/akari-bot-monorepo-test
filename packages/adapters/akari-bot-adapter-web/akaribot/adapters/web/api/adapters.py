import json
import re
from typing import Any

from fastapi import HTTPException, Request
from fastapi.responses import Response

from akaribot.adapters.web.client import app, get_client_ip, limiter
from akaribot.core.api import Logger
from .auth import verify_jwt
from .cli_bridge import CliTimeout, CliUnavailable, parse_json, run_cli, write_lock

PLATFORM_PATTERN = re.compile(r"^[a-z0-9_]{1,24}$")
INSTANCE_ID_PATTERN = re.compile(r"^[a-z0-9_]{1,24}$")
TABLE_PATTERN = re.compile(r"^bot_[a-z0-9_]{1,24}(-[a-z0-9_]{1,24})?$")
CONFIG_KEY_PATTERN = re.compile(r"^[A-Za-z0-9_]{1,64}$")


async def _read_body(request: Request) -> dict:
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid_json")
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="invalid_body")
    return body


def _platform(value: Any) -> str:
    if not isinstance(value, str) or not PLATFORM_PATTERN.fullmatch(value):
        raise HTTPException(status_code=422, detail="invalid_platform")
    return value


def _instance_id(value: Any) -> str:
    if value in (None, ""):
        return ""
    if not isinstance(value, str) or not INSTANCE_ID_PATTERN.fullmatch(value):
        raise HTTPException(status_code=422, detail="invalid_instance_id")
    return value


def _table(value: Any) -> str:
    if not isinstance(value, str) or not TABLE_PATTERN.fullmatch(value):
        raise HTTPException(status_code=422, detail="invalid_table")
    return value


def _config_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float, str)):
        return str(value)
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    raise HTTPException(status_code=422, detail="invalid_value")


async def _run_write(*args: str) -> str:
    if write_lock.locked():
        raise HTTPException(status_code=409, detail="operation_in_progress")
    async with write_lock:
        try:
            result = await run_cli(*args)
        except CliUnavailable:
            raise HTTPException(status_code=503, detail="cli_unavailable")
        except CliTimeout:
            raise HTTPException(status_code=504, detail="cli_timeout")
    if result.returncode != 0:
        detail = (result.stderr or result.stdout)[-400:]
        raise HTTPException(status_code=422, detail=detail or "cli_failed")
    return result.stdout


@app.get("/api/adapters")
@limiter.limit("20/minute")
async def list_adapters(request: Request):
    verify_jwt(request)
    try:
        result = await run_cli("adapter", "list", "--json")
    except CliUnavailable:
        raise HTTPException(status_code=503, detail="cli_unavailable")
    except CliTimeout:
        raise HTTPException(status_code=504, detail="cli_timeout")
    if result.returncode != 0:
        Logger.warning(f"[WebUI] adapter list failed: {result.stderr[-400:]}")
        raise HTTPException(status_code=502, detail="cli_failed")
    try:
        return parse_json(result.stdout)
    except ValueError:
        raise HTTPException(status_code=502, detail="cli_bad_output")


@app.post("/api/adapters/instance")
@limiter.limit("10/minute")
async def add_adapter_instance(request: Request):
    ip = get_client_ip(request)
    verify_jwt(request)
    body = await _read_body(request)
    platform = _platform(body.get("platform"))
    instance_id = _instance_id(body.get("instance_id"))
    await _run_write("adapter", "instance", "add", platform, *([instance_id] if instance_id else []))
    Logger.info(f"[WebUI] {ip} added adapter instance: {platform}/{instance_id or 'default'}")
    return Response(status_code=204)


@app.delete("/api/adapters/instance")
@limiter.limit("10/minute")
async def remove_adapter_instance(request: Request, platform: str, instance_id: str = ""):
    ip = get_client_ip(request)
    verify_jwt(request)
    platform = _platform(platform)
    instance_id = _instance_id(instance_id)
    await _run_write("adapter", "instance", "remove", platform, *([instance_id] if instance_id else []))
    Logger.info(f"[WebUI] {ip} removed adapter instance: {platform}/{instance_id or 'default'}")
    return Response(status_code=204)


@app.patch("/api/adapters/enable")
@limiter.limit("10/minute")
async def set_adapter_enable(request: Request):
    ip = get_client_ip(request)
    verify_jwt(request)
    body = await _read_body(request)
    table = _table(body.get("table"))
    enable = body.get("enable")
    if not isinstance(enable, bool):
        raise HTTPException(status_code=400, detail='"enable" must be bool')
    await _run_write("config", "set", "enable", "true" if enable else "false", "--table", table)
    Logger.info(f"[WebUI] {ip} set enable={str(enable).lower()} for adapter table: {table}")
    return {"restart_required": True}


@app.put("/api/adapters/config")
@limiter.limit("20/minute")
async def set_adapter_config(request: Request):
    ip = get_client_ip(request)
    verify_jwt(request)
    body = await _read_body(request)
    table = _table(body.get("table"))
    key = body.get("key")
    if not isinstance(key, str) or not CONFIG_KEY_PATTERN.fullmatch(key):
        raise HTTPException(status_code=422, detail="invalid_key")
    value = _config_value(body.get("value"))
    await _run_write("config", "set", key, value, "--table", table)
    Logger.info(f"[WebUI] {ip} edited adapter config: {table}.{key}")
    return {"restart_required": True}
