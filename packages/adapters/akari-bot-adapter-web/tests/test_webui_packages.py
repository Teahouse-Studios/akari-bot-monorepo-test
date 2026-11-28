"""akaribot.adapters.web.api 包管理接口单元测试。"""

import inspect
from unittest.mock import AsyncMock, patch

import orjson
from fastapi import HTTPException

import akaribot.adapters.web.api.packages as packages_api
from akaribot.adapters.web.api.cli_bridge import CliResult, write_lock
from akaribot.testing import Tester, func_case


class _FakeRequest:
    def __init__(self, body=None, query=None):
        self._body = body
        self.query_params = query or {}

    async def json(self):
        return self._body


async def _call(name, request):
    endpoint = inspect.unwrap(getattr(packages_api, name))
    with (
        patch.object(packages_api, "verify_jwt", lambda request: None),
        patch.object(packages_api, "get_client_ip", lambda request: "test"),
    ):
        try:
            return 200, await endpoint(request)
        except HTTPException as exc:
            return exc.status_code, exc.detail


def _parse_events(chunks):
    events = []
    for chunk in chunks:
        lines = chunk.strip().splitlines()
        event = next(line.removeprefix("event: ") for line in lines if line.startswith("event: "))
        data = next(line.removeprefix("data: ") for line in lines if line.startswith("data: "))
        events.append((event, orjson.loads(data)))
    return events


async def _stream(name, body):
    calls = []

    async def fake_stream(*args, **kwargs):
        calls.append(args)
        yield "line", "working"
        yield "exit", 0

    with patch.object(packages_api, "stream_cli", fake_stream):
        status, response = await _call(name, _FakeRequest(body))
        if status != 200:
            return status, response, calls
        chunks = [chunk async for chunk in response.body_iterator]
    return 200, _parse_events(chunks), calls


async def _test_list_packages_reads_cli_json():
    payload = [{"dist": "akari-bot-module-dice", "kind": "module"}]
    run = AsyncMock(
        return_value=CliResult(0, 'warning line\n[{"dist": "akari-bot-module-dice", "kind": "module"}]', "")
    )
    with patch.object(packages_api, "run_cli", run):
        status, result = await _call("list_packages", _FakeRequest(query={"kind": "module"}))
        invalid, _ = await _call("list_packages", _FakeRequest(query={"kind": "--json"}))
    return (
        status == 200
        and result == {"packages": payload}
        and run.await_args.args == ("module", "list", "--json", "--kind", "module")
        and invalid == 422
    )


async def _test_install_rejects_option_injection():
    bad_names = ["--git", "-e", "a b", "", None, "../x", "x" * 200]
    for name in bad_names:
        status, _, calls = await _stream("install_package", {"name": name})
        if status != 422 or calls:
            return False
    for body in ({"git": "file:///etc/passwd"}, {"git": "https://example.com/a.git", "ref": "--upload-pack"}):
        status, _, calls = await _stream("install_package", body)
        if status != 422 or calls:
            return False
    return True


async def _test_install_builds_command_and_streams_output():
    status, events, calls = await _stream("install_package", {"name": "akari-bot-module-dice", "force": True})
    git_status, _, git_calls = await _stream(
        "install_package", {"git": "https://example.com/a.git", "ref": "main", "subdir": "pkg"}
    )
    return (
        status == 200
        and calls == [("module", "add", "akari-bot-module-dice", "--force")]
        and [name for name, _ in events] == ["start", "output", "done"]
        and events[-1][1] == {"success": True, "returncode": 0}
        and git_status == 200
        and git_calls == [("module", "add", "--git", "https://example.com/a.git", "--ref", "main", "--subdir", "pkg")]
    )


async def _test_uninstall_confirms_and_maps_mode():
    expected = {
        "keep": ("module", "remove", "akari-bot-module-dice", "--yes"),
        "purge": ("module", "remove", "akari-bot-module-dice", "--purge-data", "--yes"),
        "cascade": ("module", "remove", "akari-bot-module-dice", "--cascade", "--yes"),
    }
    for mode, argv in expected.items():
        status, _, calls = await _stream("uninstall_package", {"name": "akari-bot-module-dice", "mode": mode})
        if status != 200 or calls != [argv]:
            return False
    status, _, calls = await _stream("uninstall_package", {"name": "akari-bot-module-dice", "mode": "force"})
    return status == 422 and not calls


async def _test_update_requires_target():
    status, _, calls = await _stream("update_packages", {"all": True})
    names_status, _, names_calls = await _stream("update_packages", {"names": ["akari-bot-module-dice"]})
    missing, _, missing_calls = await _stream("update_packages", {})
    bad, _, bad_calls = await _stream("update_packages", {"names": ["--all"]})
    return (
        status == 200
        and calls == [("module", "update", "--all", "--yes")]
        and names_status == 200
        and names_calls == [("module", "update", "akari-bot-module-dice", "--yes")]
        and missing == 422
        and bad == 422
        and not missing_calls
        and not bad_calls
    )


async def _test_write_rejects_concurrent_operation():
    await write_lock.acquire()
    try:
        status, _, calls = await _stream("install_package", {"name": "akari-bot-module-dice"})
    finally:
        write_lock.release()
    return status == 409 and not calls


@func_case
async def test_webui_packages(tester: Tester):
    """akaribot.adapters.web.api 包管理接口测试"""
    await tester.test(_test_list_packages_reads_cli_json, "包列表读取 CLI 输出测试")
    await tester.test(_test_install_rejects_option_injection, "安装参数拦截测试")
    await tester.test(_test_install_builds_command_and_streams_output, "安装命令与流式输出测试")
    await tester.test(_test_uninstall_confirms_and_maps_mode, "卸载模式映射测试")
    await tester.test(_test_update_requires_target, "更新目标校验测试")
    await tester.test(_test_write_rejects_concurrent_operation, "并发写入拦截测试")

    return tester
