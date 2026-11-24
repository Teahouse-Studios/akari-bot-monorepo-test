import re

from akaribot.core.builtins.bot import Bot
from akaribot.core.builtins.message.internal import ActionText, I18NContext
from akaribot.core.component import module
from akaribot.core.config.base import CoreConfig
from akaribot.core.database.models import (
    UNION_SCOPE_SENDER,
    UNION_SCOPE_TARGET,
    SenderUnionInfo,
    TargetUnionBind,
    TargetUnionInfo,
)
from akaribot.core.utils.retired import RETIRED_SOURCES, RETIRED_TARGETS, enqueue_notice, is_merge_route_allowed
from akaribot.core.utils.container import ExpiringTempDict
from akaribot.modules.core.common_tools._union_merge import (
    BIND_CODE_EXPIRED,
    apply_sender_merge,
    apply_target_merge,
    choose_conflicts,
    id_lines,
    issue_code,
    merge_target_unions,
    plan_sender_merge,
    plan_target_merge,
    reserve_sender_merge,
    take_code,
    target_lines,
)
from akaribot.modules.core.common_tools.bind import b

# 迁移码与 bind 的绑定码分开存储，两者不可混用，因为
# 迁移码用于将退役实例上的数据迁移至新实例，与常规跨平台绑定在语义上属于不同操作。
_sender_merge_codes = ExpiringTempDict(exp=BIND_CODE_EXPIRED)
_target_merge_codes = ExpiringTempDict(exp=BIND_CODE_EXPIRED)

# ``merge`` 是 ``bind`` 的别名，此处保留同名隐藏模块，仅承载退役公告触发器，因为
# 退役策略的白名单按模块名称放行，公告正则需要挂载在白名单模块上方可在退役场景中继续匹配。
m = module("merge", base=True, hidden=True, load=bool(CoreConfig.retired_clients))


def _take_merge_code(code: str) -> tuple[str, dict] | None:
    # 读取并核销一项通过 ``merge`` 签发的迁移码。
    return take_code(
        code,
        ((UNION_SCOPE_SENDER, _sender_merge_codes), (UNION_SCOPE_TARGET, _target_merge_codes)),
    )


async def _unify_channel(initiator_target_id: str, current_target_id: str) -> int:
    # 两个场景并入同一条通道，使命令执行与消息推送仅转交其中一方承担。如果两个机器人回到共作状态，
    # 不同通道会导致两个机器人各自通过通道认领的快速路径，同一条命令被响应两次，统一通道能够为此类回退场景提供保障。
    # 通道编号使用发起方的现有编号。两个场景所属的完整通道均保留等价关系，避免拆分第三个入口。
    channel_id = await TargetUnionInfo.unify_channels(initiator_target_id, current_target_id)
    if channel_id is not None:
        return channel_id

    binds = await TargetUnionBind.filter(target_id__in=[initiator_target_id, current_target_id])
    by_id = {row.target_id: row for row in binds}
    initiator_bind = by_id.get(initiator_target_id)
    current_bind = by_id.get(current_target_id)
    if initiator_bind and current_bind:
        # 两行均存在却无法统一，说明迁移后的 Target Union 拓扑与调用约定不符。
        # 此时不可将其中一侧静默移动至其他通道，避免掩盖未完成的 Union 合并。
        raise RuntimeError("Unable to unify migrated target channels.")

    fallback_channel = initiator_bind.channel_id if initiator_bind else 1
    if current_bind and current_bind.channel_id != fallback_channel:
        return await TargetUnionInfo.reassign_channel(current_target_id, fallback_channel) or fallback_channel
    return fallback_channel


@b.command("merge {{I18N:core.help.bind.merge}}", available_for=RETIRED_SOURCES)
async def _(msg: Bot.MessageSession):
    session_info = msg.session_info
    # 迁移码需要记录签发方的客户端与场景，前者用于核销时校验迁移目标，
    # 后者用于迁移完成后统一两侧的消息通道编号。
    origin = {"source_client": session_info.client_name, "holder_target_id": session_info.target_id}

    if session_info.is_private:
        # 私聊中的用户身份与私聊场景属于同一数据边界，应当一并迁移，
        # 否则用户的个人数据仍残留在退役实例中。
        await issue_code(
            msg,
            _sender_merge_codes,
            session_info.sender_union_info.union_id,
            session_info.sender_id,
            "core.message.bind.merge.start.private.prompt",
            extra={
                "target_union_id": session_info.target_union_info.union_id,
                "is_private": True,
                **origin,
            },
            code_key="core.message.bind.merge.code",
            command="merge token",
        )
    # 场景迁移会改动整个场景的数据，需要管理员权限。私聊场景无此限制，校验在此处执行。
    if not await msg.check_permission():
        await msg.finish(I18NContext("parser.admin.permission.denied.command"))
    await issue_code(
        msg,
        _target_merge_codes,
        session_info.target_union_info.union_id,
        session_info.target_id,
        "core.message.bind.merge.start.prompt",
        extra={"is_private": False, **origin},
        code_key="core.message.bind.merge.code",
        command="merge token",
    )


async def _merge_private(msg: Bot.MessageSession, entry: dict) -> None:
    # 完成一次私聊迁移，将账号数据与私聊场景数据一并合并。
    # 私聊中“该账号”与“该私聊场景”在表现上一致。仅合并其中一项会导致另一部分数据残留在退役实例中。
    # 两者共用一次确认后统一执行，避免用户在第二次确认时取消而处于仅部分迁移的不一致状态。
    session_info = msg.session_info
    sender_current = session_info.sender_union_info
    target_current = session_info.target_union_info

    # 签发迁移码的一方为发起方，冲突数据默认以发起方为准。
    sender_initiator = await SenderUnionInfo.get_or_none(union_id=entry["union_id"])
    target_initiator = await TargetUnionInfo.get_or_none(union_id=entry["target_union_id"])
    if not sender_initiator or not target_initiator:
        await msg.finish(
            I18NContext(
                "core.message.bind.merge.code.invalid",
                prefix=session_info.prefixes[0],
                cmd=ActionText(f"{session_info.prefixes[0]}merge"),
            )
        )

    sender_plan = (
        await plan_sender_merge(sender_initiator, sender_current)
        if sender_initiator.union_id != sender_current.union_id
        else None
    )
    target_plan = (
        await plan_target_merge(msg, target_initiator, target_current)
        if target_initiator.union_id != target_current.union_id
        else None
    )
    if not sender_plan and not target_plan:
        await msg.finish(I18NContext("core.message.bind.merge.same"))

    lines = [I18NContext("core.message.bind.merge.private.confirm")]
    for plan in (sender_plan, target_plan):
        if plan:
            lines += plan["lines"]
    if not await msg.wait_confirm(lines):
        await msg.finish()

    # 场景选择需要在建立 sender barrier 前完成。普通 wait_confirm 会释放执行
    # lease。sender barrier 建立后，其冲突选择保持 lease，直到合并写入结束。
    target_keep = await choose_conflicts(msg, target_plan["conflicts"]) if target_plan else set()
    if sender_plan:
        sender_plan = await reserve_sender_merge(msg, sender_plan)
    sender_keep = (
        await choose_conflicts(msg, sender_plan["conflicts"], preserve_execution_lock=True) if sender_plan else set()
    )

    merged_sender = await apply_sender_merge(sender_plan, sender_keep, msg) if sender_plan else sender_current
    merged_target = await apply_target_merge(target_plan, target_keep) if target_plan else target_current
    if not merged_sender or not merged_target:
        await msg.finish(I18NContext("core.message.bind.merge.private.failed"))

    await _unify_channel(entry["holder_target_id"], session_info.target_id)
    await session_info.refresh_info()

    sender_ids = await merged_sender.list_bound_ids()
    target_ids = await merged_target.list_bound_ids()
    await msg.finish(
        [
            I18NContext("core.message.bind.merge.self.success", id=merged_sender.union_id, disable_joke=True),
            I18NContext("core.message.bind.self.info.bound", count=len(sender_ids)),
        ]
        + id_lines(sender_ids)
        + [
            I18NContext("core.message.bind.merge.target.success", id=merged_target.union_id, disable_joke=True),
            I18NContext("core.message.bind.target.info.bound", count=len(target_ids)),
        ]
        + await target_lines(msg, merged_target.union_id, target_ids)
    )


# 命令字面量按“位置无关的标志”匹配，因为沿用 merge token 作为命令路径会被 bind token 抢先匹配
# （``<code>`` 匹配并解析占用 "merge"），源平台便无法避让。用户端命令不变，通过别名映射至此处。
@b.command("merge-token <code> {{I18N:core.help.bind.merge.token}}", available_for=RETIRED_TARGETS)
async def _(msg: Bot.MessageSession, code: str):
    taken = _take_merge_code(code)
    if not taken:
        await msg.finish(
            I18NContext(
                "core.message.bind.merge.code.invalid",
                cmd=ActionText(f"{msg.session_info.prefixes[0]}merge"),
            )
        )
    scope, entry = taken

    # 迁移码仅可在其所属迁移关系的目标平台核销。命令级 available_for 仅能表明当前平台为
    # 某条关系的目标，配置多条关系时无法防止使用第一种关系的迁移码在第二种关系的目标平台中核销。
    if not is_merge_route_allowed(entry.get("source_client"), msg.session_info.client_name):
        await msg.finish(I18NContext("core.message.bind.merge.route.mismatch"))

    # 迁移码的签发与使用需要处于同类场景。私聊绑定码绑定发起方的场景组，如果在群聊中核销，
    # 会将私聊场景的数据合并至群聊场景中，群聊迁移码在私聊中核销的规则亦相同。
    if entry["is_private"] != msg.session_info.is_private:
        await msg.finish(I18NContext("core.message.bind.merge.context.mismatch"))

    if scope == UNION_SCOPE_SENDER:
        await _merge_private(msg, entry)

    # 场景迁移会修改整个场景的数据，与签发迁移码时相同，均需要管理员权限。
    if not await msg.check_permission():
        await msg.finish(I18NContext("parser.admin.permission.denied.command"))

    current = msg.session_info.target_union_info
    if entry["union_id"] == current.union_id:
        await msg.finish(I18NContext("core.message.bind.merge.same"))
    initiator = await TargetUnionInfo.get_or_none(union_id=entry["union_id"])
    if not initiator:
        await msg.finish(
            I18NContext(
                "core.message.bind.merge.code.invalid",
                cmd=ActionText(f"{msg.session_info.prefixes[0]}merge"),
            )
        )

    merged = await merge_target_unions(msg, initiator, current, "core.message.bind.merge.target.confirm.inherit")
    if not merged:
        await msg.finish()

    channel_id = await _unify_channel(entry["holder_target_id"], msg.session_info.target_id)
    await msg.session_info.refresh_info()

    bound_ids = await merged.list_bound_ids()
    await msg.finish(
        [
            I18NContext("core.message.bind.merge.target.success", id=merged.union_id, disable_joke=True),
            I18NContext("core.message.bind.target.info.bound", count=len(bound_ids)),
        ]
        + await target_lines(msg, merged.union_id, bound_ids)
        + [I18NContext("core.message.bind.merge.channel.unified", channel=channel_id)]
    )


@m.regex(
    re.compile(r".+"),
    mode="M",
    show_typing=False,
    logging=False,
    trigger_once_startup=True,
    available_for=RETIRED_SOURCES,
)
async def _(msg: Bot.MessageSession):
    # 仅负责排队，不向场景发送内容，公告通过延时任务在数分钟后推送。如果挂载在命令拦截上，退役后用户
    # 一旦停止发送命令，该场景便永远收不到公告。单次触发使每个场景仅执行一次，避免对每条消息都查询数据库。
    await enqueue_notice(msg.session_info)
