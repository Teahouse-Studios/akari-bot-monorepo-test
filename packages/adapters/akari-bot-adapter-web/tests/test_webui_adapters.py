"""akaribot.adapters.web.api 适配器管理接口单元测试。"""

import inspect
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException

import akaribot.adapters.web.api.adapters as adapters_api
from akaribot.adapters.web.api.cli_bridge import CliResult, write_lock
from akaribot.testing import Tester, func_case


class _FakeRequest:
    def __init__(self, body=None):
        self._body = body

    async def json(self):
        return self._body


async def _call(name, *args, run=None):
    endpoint = inspect.unwrap(getattr(adapters_api, name))
    run = run or AsyncMock(return_value=CliResult(0, "", ""))
    with (
        patch.object(adapters_api, "verify_jwt", lambda request: None),
        patch.object(adapters_api, "get_client_ip", lambda request: "test"),
        patch.object(adapters_api, "run_cli", run),
    ):
        try:
            result = await endpoint(*args)
        except HTTPException as exc:
            return exc.status_code, exc.detail, run
    return getattr(result, "status_code", 200), result, run


async def _test_list_adapters_reads_cli_json():
    run = AsyncMock(return_value=CliResult(0, 'note\n{"instances": [], "installed_platforms": ["web"]}', ""))
    status, result, run = await _call("list_adapters", _FakeRequest(), run=run)
    failed = AsyncMock(return_value=CliResult(1, "", "boom"))
    failed_status, _, _ = await _call("list_adapters", _FakeRequest(), run=failed)
    return (
        status == 200
        and result == {"instances": [], "installed_platforms": ["web"]}
        and run.await_args.args == ("adapter", "list", "--json")
        and failed_status == 502
    )


async def _test_instance_add_and_remove_build_commands():
    add_status, _, add_run = await _call(
        "add_adapter_instance", _FakeRequest({"platform": "telegram", "instance_id": "alt"})
    )
    default_status, _, default_run = await _call("add_adapter_instance", _FakeRequest({"platform": "web"}))
    remove_status, _, remove_run = await _call("remove_adapter_instance", _FakeRequest(), "telegram", "alt")
    return (
        add_status == 204
        and add_run.await_args.args == ("adapter", "instance", "add", "telegram", "alt")
        and default_status == 204
        and default_run.await_args.args == ("adapter", "instance", "add", "web")
        and remove_status == 204
        and remove_run.await_args.args == ("adapter", "instance", "remove", "telegram", "alt")
    )


async def _test_instance_rejects_unsafe_names():
    for platform in ("--help", "Tele", "a b", "", None, "x" * 30):
        status, _, run = await _call("add_adapter_instance", _FakeRequest({"platform": platform}))
        if status != 422 or run.await_count:
            return False
    for instance_id in ("Alt", "a-b", "--yes", "x" * 30):
        status, _, run = await _call(
            "add_adapter_instance", _FakeRequest({"platform": "telegram", "instance_id": instance_id})
        )
        if status != 422 or run.await_count:
            return False
    status, _, run = await _call("remove_adapter_instance", _FakeRequest(), "telegram", "--yes")
    return status == 422 and not run.await_count


async def _test_enable_and_config_write_through_cli():
    enable_status, enable_result, enable_run = await _call(
        "set_adapter_enable", _FakeRequest({"table": "bot_telegram-alt", "enable": True})
    )
    config_status, config_result, config_run = await _call(
        "set_adapter_config",
        _FakeRequest({"table": "bot_web", "key": "web_port", "value": 6486}),
    )
    list_status, _, list_run = await _call(
        "set_adapter_config",
        _FakeRequest({"table": "bot_web", "key": "allow_origins", "value": ["https://example.com"]}),
    )
    return (
        enable_status == 200
        and enable_result == {"restart_required": True}
        and enable_run.await_args.args == ("config", "set", "enable", "true", "--table", "bot_telegram-alt")
        and config_status == 200
        and config_result == {"restart_required": True}
        and config_run.await_args.args == ("config", "set", "web_port", "6486", "--table", "bot_web")
        and list_status == 200
        and list_run.await_args.args[3] == '["https://example.com"]'
    )


async def _test_enable_and_config_reject_invalid_input():
    cases = [
        ("set_adapter_enable", {"table": "bot_web", "enable": "true"}, 400),
        ("set_adapter_enable", {"table": "module_dice", "enable": True}, 422),
        ("set_adapter_enable", {"table": "--table", "enable": True}, 422),
        ("set_adapter_config", {"table": "bot_web", "key": "--json", "value": 1}, 422),
        ("set_adapter_config", {"table": "bot_web", "key": "web_port", "value": None}, 422),
    ]
    for name, body, expected in cases:
        status, _, run = await _call(name, _FakeRequest(body))
        if status != expected or run.await_count:
            return False
    return True


async def _test_cli_failure_and_concurrency():
    failed = AsyncMock(return_value=CliResult(2, "", "unknown table"))
    status, detail, _ = await _call(
        "add_adapter_instance", _FakeRequest({"platform": "web", "instance_id": "alt"}), run=failed
    )
    await write_lock.acquire()
    try:
        busy, _, run = await _call("add_adapter_instance", _FakeRequest({"platform": "web"}))
    finally:
        write_lock.release()
    return status == 422 and detail == "unknown table" and busy == 409 and not run.await_count


@func_case
async def test_webui_adapters(tester: Tester):
    """akaribot.adapters.web.api 适配器管理接口测试"""
    await tester.test(_test_list_adapters_reads_cli_json, "适配器列表读取 CLI 输出测试")
    await tester.test(_test_instance_add_and_remove_build_commands, "实例新增与移除命令测试")
    await tester.test(_test_instance_rejects_unsafe_names, "实例名称校验测试")
    await tester.test(_test_enable_and_config_write_through_cli, "启用与配置写入命令测试")
    await tester.test(_test_enable_and_config_reject_invalid_input, "配置写入参数拦截测试")
    await tester.test(_test_cli_failure_and_concurrency, "CLI 失败与并发拦截测试")

    return tester
