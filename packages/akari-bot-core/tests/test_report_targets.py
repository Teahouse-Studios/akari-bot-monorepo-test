"""上报场景展开单元测试（需要数据库）。

`report_targets` 配置的是场景组，上报须落到该组下的全部平台场景：同一现实场景的多个
平台入口由 pick_channel_heads 归拢为一条并互为后备，配置项所指的那个客户端掉线时仍有
下一跳可换。配置值不能直接当作平台场景 ID 去取会话：组内其余成员不参与时 next_hops 恒为空，
该客户端一掉线整条上报即静默丢失。

组内展开与退役滤除统一收在 fetch_union_target_list，按场景组推送的
send_direct_message_to_union_target 亦走这条路，其行为另由 test_union_push.py 守住。
"""

from datetime import UTC, datetime, timedelta

from akaribot.core.alive import Alive
from akaribot.core.builtins.bot import Bot
from akaribot.core.database.models import JobQueuePeersTable, TargetUnionBind, TargetUnionInfo
from akaribot.testing import func_case, Tester

_CLIENT = "REPORTTEST"


async def _register_client():
    # 取会话时须由拓扑缓存反查场景所属的客户端，未登记者取不出会话。缓存非空时
    # ``Alive.determine_client(None)`` 还会直接抛错，而 ``fetch_target`` 会将其吞下，
    # 表现为无声地少了几个会话。
    metadata = {
        "target_prefix_list": [f"{_CLIENT}|Group"],
        "sender_prefix_list": [_CLIENT],
    }
    lease_until = datetime.now(UTC) + timedelta(seconds=300)
    await JobQueuePeersTable.update_or_create(
        peer_id="TEST-PEER-REPORT",
        defaults={
            "role": "client",
            "service": _CLIENT,
            "state": "ready",
            "capabilities": ["rpc", "signals"],
            "metadata": metadata,
            "heartbeat_at": datetime.now(UTC),
            "lease_until": lease_until,
        },
    )
    Alive.refresh_peer(
        "TEST-PEER-REPORT",
        _CLIENT,
        metadata=metadata,
        lease_until=lease_until,
    )


async def _test_resolves_platform_id_to_union():
    union = await TargetUnionInfo.resolve_union("REPORTTEST|Group|resolve_a")
    return await Bot.resolve_union_targets(["REPORTTEST|Group|resolve_a"]) == [union.union_id]


async def _test_union_id_leaves_no_stray_bind():
    union = await TargetUnionInfo.resolve_union("REPORTTEST|Group|stray")
    await Bot.resolve_union_targets([union.union_id])
    return not await TargetUnionBind.exists(target_id=union.union_id)


async def _test_unbound_target_dropped():
    return await Bot.resolve_union_targets(["REPORTTEST|Group|unbound"]) == []


async def _test_deduplicates_same_union():
    union = await TargetUnionInfo.resolve_union("REPORTTEST|Group|dedup_a")
    await union.bind_id("REPORTTEST|Group|dedup_b")

    resolved = await Bot.resolve_union_targets(["REPORTTEST|Group|dedup_a", "REPORTTEST|Group|dedup_b"])
    return resolved == [union.union_id]


async def _test_fetch_covers_all_union_members():
    await _register_client()
    union = await TargetUnionInfo.resolve_union("REPORTTEST|Group|fetch_a")
    await union.bind_id("REPORTTEST|Group|fetch_b")

    fetched = await Bot.fetch_union_target_list(["REPORTTEST|Group|fetch_a"])
    return {x.target_id for x in fetched} == {"REPORTTEST|Group|fetch_a", "REPORTTEST|Group|fetch_b"}


async def _test_fetch_accepts_single_value():
    await _register_client()
    union = await TargetUnionInfo.resolve_union("REPORTTEST|Group|single")
    fetched = await Bot.fetch_union_target_list(union.union_id)
    return [x.target_id for x in fetched] == ["REPORTTEST|Group|single"]


@func_case
async def test_report_targets(tester: Tester):
    """core: 上报场景按场景组展开"""
    alive = Alive.values.copy()
    try:
        await tester.test(_test_resolves_platform_id_to_union, "平台场景 ID 归一为场景组")
        await tester.test(_test_union_id_leaves_no_stray_bind, "归一组 ID 不留脏映射行")
        await tester.test(_test_unbound_target_dropped, "未登记场景略去")
        await tester.test(_test_deduplicates_same_union, "同组配置值去重")
        await tester.test(_test_fetch_covers_all_union_members, "取会话覆盖组内成员")
        await tester.test(_test_fetch_accepts_single_value, "接受单个场景 ID")
    finally:
        await JobQueuePeersTable.filter(peer_id="TEST-PEER-REPORT").delete()
        Alive.values.clear()
        Alive.values.update(alive)
    return tester
