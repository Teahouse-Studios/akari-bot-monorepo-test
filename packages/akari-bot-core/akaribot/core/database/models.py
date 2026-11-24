from __future__ import annotations

import asyncio
import uuid
from collections import Counter
from contextlib import asynccontextmanager
from datetime import datetime, UTC, timedelta
from decimal import Decimal
from typing import Any, ClassVar, Literal, Self, overload

from tortoise import fields
from tortoise.expressions import F
from tortoise.functions import Count
from tortoise.models import Model
from tortoise.transactions import in_transaction

from akaribot.core.config.base import BaseConfig
from akaribot.core.queue.transport import DEFAULT_TIMEOUT_SECONDS
from akaribot.core.utils.func import convert_list
from .base import DBModel, extract_session_id
from ..logger import Logger


default_locale = BaseConfig.default_locale

UNION_SCOPE_SENDER = "sender"
UNION_SCOPE_TARGET = "target"

# 新建 union ID 的域前缀。升级与转换脚本会将历史数据的平台 ID 直接沿用为 union ID，
# 附加前缀后，新生成的 ID 不会与平台原生 ID 混淆，且可明确区分账号组与场景组。
UNION_ID_PREFIXES = {
    UNION_SCOPE_SENDER: "USID",
    UNION_SCOPE_TARGET: "UTID",
}

# Union 的绑定、合并、删除与更新属于同一 mutation 域，共用单一进程内互斥锁。
# MySQL 路径仍将在事务内锁定核心行，兼顾 Web 与 Server 分属不同进程的场景。
_union_mutation_lock = asyncio.Lock()


@asynccontextmanager
async def union_mutation():
    """串行执行一段 Union 状态变更。调用方不得在其内部再次进入该上下文。"""
    async with _union_mutation_lock:
        yield


class UnionDeleteBlocked(RuntimeError):
    """Union 仍被模块记录引用，必须先解除外部状态才能删除。"""

    def __init__(self, union_id: str, model: type[Model], reason: str):
        self.union_id = union_id
        self.model = model
        self.reason = reason
        super().__init__(f"Cannot delete union {union_id}: {get_table_name(model)}: {reason}")


def _get_module_and_alias_first_words(module_names: str | list[str] | tuple[str, ...]) -> list[str]:
    from akaribot.core.loader import ModulesManager

    result = []
    for module_name in convert_list(module_names):
        related_names = ModulesManager.get_module_and_alias_first_words(module_name) or [module_name]
        for related_name in related_names:
            if related_name not in result:
                result.append(related_name)
    return result


def get_table_name(model: type[Model]) -> str:
    """获取模型对应的数据表名称。"""
    meta = getattr(model, "Meta", None)
    return getattr(meta, "table", None) or model.__name__


def get_union_module_name(model: type[Model]) -> str:
    """获取模块表所属的模块名称，供面向用户的提示使用。无法识别时改用数据表名称。"""
    parts = model.__module__.split(".")
    if len(parts) > 2 and parts[:2] == ["akaribot", "modules"]:
        return parts[2]
    return get_table_name(model)


def iter_union_models(scope: str | None = None) -> list[type[Model]]:
    from tortoise import Tortoise

    core_models = {SenderUnionInfo, TargetUnionInfo, SenderUnionBind, TargetUnionBind}
    result = []
    for app in Tortoise.apps.values():
        for model in app.values():
            if model in core_models or model in result:
                continue
            if "union_id" not in getattr(model._meta, "fields_map", {}):
                continue
            model_scope = getattr(model, "union_scope", None)
            if not model_scope:
                Logger.warning(
                    f"Table {get_table_name(model)} is keyed by union_id but declares no union_scope, "
                    "so it is excluded from union merge and backfill. "
                    "Declare union_scope = UNION_SCOPE_SENDER or UNION_SCOPE_TARGET on the model."
                )
                continue
            if scope and model_scope != scope:
                continue
            result.append(model)
    return result


def iter_union_reference_models() -> list[type[Model]]:
    from tortoise import Tortoise

    handlers = (
        "validate_union_delete",
        "migrate_union_reference",
        "migrate_unbound_union_reference",
        "delete_union_reference",
    )
    result = []
    for app in Tortoise.apps.values():
        for model in app.values():
            if model in result:
                continue
            if any(callable(getattr(model, handler, None)) for handler in handlers):
                result.append(model)
    return result


async def validate_union_delete(scope: str, union_id: str) -> None:
    for model in iter_union_reference_models():
        handler = getattr(model, "validate_union_delete", None)
        if not callable(handler):
            continue
        if reason := await handler(scope, union_id):
            raise UnionDeleteBlocked(union_id, model, str(reason))


async def migrate_union_references(scope: str, from_union: str, to_union: str) -> None:
    """迁移明确声明协议的模块 Union 引用。"""
    for model in iter_union_reference_models():
        handler = getattr(model, "migrate_union_reference", None)
        if callable(handler):
            await handler(scope, from_union, to_union)


async def migrate_unbound_union_references(
    scope: str,
    platform_id: str,
    from_union: str,
    to_union: str,
) -> None:
    for model in iter_union_reference_models():
        handler = getattr(model, "migrate_unbound_union_reference", None)
        if callable(handler):
            await handler(scope, platform_id, from_union, to_union)


async def delete_union_references(scope: str, union_id: str) -> None:
    for model in iter_union_reference_models():
        handler = getattr(model, "delete_union_reference", None)
        if callable(handler):
            await handler(scope, union_id)


async def collect_union_conflicts(from_union: str, to_union: str, scope: str | None = None) -> list[type[Model]]:
    """
    :param from_union: 来源 union ID。
    :param to_union: 目标 union ID。
    :param scope: 限定 union 作用域。

    列出两个 union 在模块表上相互冲突（双方均存在数据）的模型。
    """
    conflicts = []
    for model in iter_union_models(scope):
        if await model.filter(union_id=from_union).exists() and await model.filter(union_id=to_union).exists():
            conflicts.append(model)
    return conflicts


async def move_union_rows(model: type[Model], from_union: str, to_union: str) -> None:
    if model._meta.pk_attr != "union_id":
        await model.filter(union_id=from_union).update(union_id=to_union)
        return

    rows = await model.filter(union_id=from_union)
    if not rows:
        return

    columns = list(model._meta.fields_db_projection)
    moved = []
    for row in rows:
        data = {column: getattr(row, column) for column in columns}
        data["union_id"] = to_union
        moved.append(model(**data))

    # 删除与重建之间若中断，绑定数据将全部丢失，因此必须纳入同一个事务执行。
    # 模块表可能关联在 local 连接上，事务必须与表所在的连接一致，不可直接使用 default 连接。
    async with in_transaction(model._meta.default_connection):
        await model.filter(union_id=from_union).delete()
        await model.bulk_create(moved)


async def migrate_union_tables(
    from_union: str,
    to_union: str,
    keep_other_tables: set[str] | None = None,
    scope: str | None = None,
) -> None:
    keep_other_tables = keep_other_tables or set()
    for model in iter_union_models(scope):
        if not await model.filter(union_id=from_union).exists():
            continue
        if await model.filter(union_id=to_union).exists():
            if get_table_name(model) in keep_other_tables:
                await model.filter(union_id=to_union).delete()
            else:
                await model.filter(union_id=from_union).delete()
                continue
        await move_union_rows(model, from_union, to_union)


async def rewrite_sender_union_refs(from_union: str, to_union: str) -> None:
    # 调用方位于 Union mutation 事务中。锁定权限列表所属的 Target 行，避免 Web 与 Server
    # 分属不同进程时，因并发修改 Union 引用与追加管理员而相互覆盖完整的 JSON 列表。
    for target in await TargetUnionInfo.all().order_by("union_id").select_for_update():
        changed = False
        update_fields = []
        for field in ("custom_admins", "banned_users"):
            value = getattr(target, field) or []
            if from_union in value:
                setattr(target, field, list(dict.fromkeys(to_union if v == from_union else v for v in value)))
                changed = True
                update_fields.append(field)
        if changed:
            await target.save(update_fields=update_fields)


async def inherit_banned_union_refs(from_union: str, to_union: str) -> None:
    for target in await TargetUnionInfo.all().order_by("union_id").select_for_update():
        banned_users = target.banned_users or []
        if from_union in banned_users and to_union not in banned_users:
            target.banned_users = banned_users + [to_union]
            await target.save(update_fields=["banned_users"])


async def remove_sender_union_refs(union_id: str) -> None:
    for target in await TargetUnionInfo.all().order_by("union_id").select_for_update():
        update_fields = []
        for field in ("custom_admins", "banned_users"):
            value = list(getattr(target, field) or [])
            filtered = [entry for entry in value if entry != union_id]
            if filtered != value:
                setattr(target, field, filtered)
                update_fields.append(field)
        if update_fields:
            await target.save(update_fields=update_fields)


async def backfill_union_binds() -> None:
    """为缺少映射行的 union 补充创建 ID 映射。"""
    for info_model in (SenderUnionInfo, TargetUnionInfo):
        bind_model = info_model.bind_model
        union_ids = set(await info_model.all().values_list("union_id", flat=True))
        # iter_union_models 已按 union_scope 过滤，此处获取的数据表必定属于相同作用域，
        # 避免将场景 ID 误作为用户 ID 创建记录。
        for model in iter_union_models(info_model.union_scope):
            union_ids |= set(await model.all().values_list("union_id", flat=True))

        missing = union_ids - set(await bind_model.all().values_list(bind_model.id_field, flat=True))
        if missing:
            await bind_model.bulk_create([bind_model(**{bind_model.id_field: i, "union_id": i}) for i in missing])


def normalize_peer_bots(value: Any) -> dict[str, dict[str, str]]:
    if not isinstance(value, dict):
        return {}
    return {
        observer: {peer: bot_id for peer, bot_id in entries.items() if bot_id}
        for observer, entries in value.items()
        if isinstance(entries, dict)
    }


class UnionBind(DBModel):
    # 子类中作为主键的平台 ID 列名称，供按域泛化的查询与补充创建逻辑使用。
    id_field: str

    union_id = fields.CharField(max_length=512, db_index=True)
    bound_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @classmethod
    async def list_ids(cls, union_id: str | list[str] | tuple[str, ...]) -> list[str]:
        """列出绑定至给定 union ID 的平台账号。"""
        return list(await cls.filter(union_id__in=convert_list(union_id)).values_list(cls.id_field, flat=True))


class SenderUnionBind(UnionBind):
    """
    用户 ID 与 union 的映射关系。

    :param sender_id: 用户 ID（平台账号）。
    """

    id_field = "sender_id"

    sender_id = fields.CharField(max_length=512, primary_key=True)

    class Meta:
        table = "sender_union_bind"


class TargetUnionBind(UnionBind):
    """
    场景 ID 与 union 的映射关系。

    :param target_id: 场景 ID。
    :param channel_id: 所属消息通道编号，同组内消息通道编号相同的场景被视为同一现实场景。
    :param push_priority: 主动推送优先级，数值越大越优先。
    """

    id_field = "target_id"

    target_id = fields.CharField(max_length=512, primary_key=True)
    channel_id = fields.IntField(default=1)
    push_priority = fields.IntField(default=0)

    class Meta:
        table = "target_union_bind"

    @classmethod
    async def next_channel_id(cls, union_id: str) -> int:
        """取该 union 下一个可用的消息通道号。

        :param union_id: 场景 union ID。
        """
        channels = await cls.filter(union_id=union_id).values_list("channel_id", flat=True)
        return max(channels) + 1 if channels else 1

    @classmethod
    async def list_channels(cls, union_id: str) -> dict[str, int]:
        """
        获取该 union 下“平台场景 ID → 消息通道编号”的映射。

        :param union_id: 场景 union ID。
        """
        binds = await cls.filter(union_id=union_id).values_list("target_id", "channel_id")
        return dict(binds)

    @classmethod
    async def list_push_order(cls, union_id: str) -> list[tuple[str, int, int]]:
        """取该 union 下各场景按主动推送顺序排列的绑定行。

        :param union_id: 场景 union ID。
        :return: 由场景 ID、消息通道号与推送优先级构成的列表，顺序即推送顺序。
        """
        rows = await (
            cls.filter(union_id=union_id)
            .order_by("-push_priority", "bound_at", "target_id")
            .values_list("target_id", "channel_id", "push_priority")
        )
        return list(rows)

    @classmethod
    async def set_push_priority(cls, target_id: str, priority: int) -> bool:
        """设置单个场景的主动推送优先级。

        :param target_id: 场景 ID。
        :param priority: 优先级，数值越大越优先。
        :return: 是否命中了绑定行。
        """
        return bool(await cls.filter(target_id=target_id).update(push_priority=priority))


def new_union_id(scope: str) -> str:
    return f"{UNION_ID_PREFIXES[scope]}|{uuid.uuid4().hex.upper()}"


class UnionInfo(DBModel):
    # 所属 union 作用域（``sender`` / ``target``）。
    union_scope: str
    # 配套的 ID 映射表。
    bind_model: type[UnionBind]

    # 由 resolve_union() 附加的映射行，并非数据库持久化字段。
    # 若未通过解析直接执行查询（如 all() / filter()），获取的实例中该字段值为 None。
    bind: UnionBind | None = None

    union_id = fields.CharField(max_length=512, primary_key=True)
    # 封禁状态仅记录于此处。union 下的全部平台 ID 共享此行，因而封禁设置直接对组内所有平台 ID 生效，
    # 映射行无需重复保存标记，避免产生组状态与单个 ID 状态不一致的问题。
    blocked = fields.BooleanField(default=False)

    class Meta:
        abstract = True

    @overload
    @classmethod
    async def resolve_union(cls, platform_id: str, create: Literal[True] = True) -> Self: ...

    @overload
    @classmethod
    async def resolve_union(cls, platform_id: str, create: bool) -> Self | None: ...

    @classmethod
    async def resolve_union(cls, platform_id: str, create: bool = True) -> Self | None:
        """按平台账号查找 union 记录，不存在时按需创建。"""
        bind_model = cls.bind_model
        bind = await bind_model.get_or_none(**{bind_model.id_field: platform_id})
        if bind:
            union = await cls.get_or_none(union_id=bind.union_id)
            if union:
                union.bind = bind
                return union
            if not create:
                return None
        elif not create:
            return None

        # 仅当映射路径缺失或损坏时才进入 mutation 域。常规消息解析仍保持无锁查询。
        async with union_mutation():
            bind = await bind_model.get_or_none(**{bind_model.id_field: platform_id})
            if not bind:
                # 自动兼容处理，允许存在 union_id 与平台 ID 相同但缺少映射行的历史数据。
                exist = await cls.get_or_none(union_id=platform_id)
                union_id = platform_id if exist else new_union_id(cls.union_scope)
                bind, _ = await bind_model.get_or_create(
                    defaults={"union_id": union_id},
                    **{bind_model.id_field: platform_id},
                )

            union, _ = await cls.get_or_create(union_id=bind.union_id)
            union.bind = bind
            return union

    async def list_bound_ids(self) -> list[str]:
        """列出该 union 记录绑定的平台账号。"""
        return await self.bind_model.list_ids(self.union_id)

    @overload
    @classmethod
    async def _resolve_session(cls, value: Any, create: Literal[True] = True) -> Self: ...

    @overload
    @classmethod
    async def _resolve_session(cls, value: Any, create: bool) -> Self | None: ...

    @classmethod
    async def _resolve_session(cls, value: Any, create: bool = True) -> Self | None:
        # 从平台 ID 字符串或会话对象解析 union 信息，供按会话获取记录的入口复用。
        id_field = cls.bind_model.id_field
        platform_id = extract_session_id(value, id_field)
        if not platform_id:
            raise ValueError(
                f"{id_field} must be a str or a MessageSession/FetchedMessageSession instance, "
                "or exports are unavailable."
            )
        return await cls.resolve_union(platform_id, create)

    async def edit_attr(self, key: str, value: Any) -> bool:
        """修改 union 记录中除主键外的指定字段值。"""
        if key not in self._meta.fields_map or key == self._meta.pk_attr:
            raise ValueError(f"Unsupported Union field: {key}")
        async with union_mutation():
            updated = await type(self).filter(union_id=self.union_id).update(**{key: value})
            if not updated:
                return False
            setattr(self, key, value)
            return True

    async def delete_union(self) -> bool:
        """删除 union 记录及其关联的映射和会话数据。"""
        async with union_mutation():
            async with in_transaction("default"):
                current = await type(self).filter(union_id=self.union_id).select_for_update().first()
                if not current:
                    return False

                await validate_union_delete(self.union_scope, self.union_id)

                if self.union_scope == UNION_SCOPE_SENDER:
                    await remove_sender_union_refs(self.union_id)

                for model in iter_union_models(self.union_scope):
                    await model.filter(union_id=self.union_id).delete()
                await delete_union_references(self.union_scope, self.union_id)
                await self.bind_model.filter(union_id=self.union_id).delete()
                await current.delete()
        return True


class SenderUnionInfo(UnionInfo):
    """用户信息。

    :param union_id: 用户 union ID。
    :param blocked: 是否为黑名单用户。
    :param trusted: 是否为白名单用户。
    :param superuser: 是否为超级用户。
    :param warns: 用户警告次数。
    :param petal: 用户花瓣数量。
    :param sender_data: 用户数据。
    """

    union_scope = UNION_SCOPE_SENDER
    bind_model = SenderUnionBind

    trusted = fields.BooleanField(default=False)
    superuser = fields.BooleanField(default=False)
    warns = fields.IntField(default=0)
    petal = fields.IntField(default=0)
    sender_data = fields.JSONField(default={})

    class Meta:
        table = "sender_union_info"

    @overload
    @classmethod
    async def get_by_sender_id(cls, sender_id: Any, create: Literal[True] = True) -> "SenderUnionInfo": ...

    @overload
    @classmethod
    async def get_by_sender_id(cls, sender_id: Any, create: bool) -> "SenderUnionInfo | None": ...

    @classmethod
    async def get_by_sender_id(cls, sender_id: Any, create: bool = True) -> "SenderUnionInfo | None":
        """
        获取平台账号所属的 union 记录行，为 :meth:`UnionInfo.resolve_union` 的会话便捷封装。
        方法接受 MessageSession 或 FetchedMessageSession，并自动提取 ``sender_id``。
        """
        return await cls._resolve_session(sender_id, create)

    async def switch_identity(self, trust: bool, enable: bool = True) -> bool:
        """
        修改用户身份。

        :param trust: 是否为白名单模式，若 False 则为黑名单模式。
        :param enable: 是否授予身份。若为 False 则撤销身份。
        """
        trusted = trust if enable else False
        blocked = not trust if enable else False
        async with union_mutation():
            updated = await SenderUnionInfo.filter(union_id=self.union_id).update(
                trusted=trusted,
                blocked=blocked,
            )
            if not updated:
                return False
            self.trusted = trusted
            self.blocked = blocked
            return True

    async def warn_user(self, amount: int = 1) -> bool:
        """
        警告用户。

        :param amount: 警告增加次数。
        """
        async with union_mutation():
            updated = await SenderUnionInfo.filter(union_id=self.union_id).update(warns=F("warns") + amount)
            if not updated:
                return False
            fresh = await SenderUnionInfo.get(union_id=self.union_id)
            self.warns = fresh.warns
            return True

    async def modify_petal(self, amount: str | int | Decimal) -> bool:
        """
        修改用户花瓣数量。

        :param amount: 增加或扣除的花瓣数量。
        """
        async with union_mutation():
            updated = await SenderUnionInfo.filter(union_id=self.union_id).update(petal=F("petal") + int(amount))
            if not updated:
                return False
            fresh = await SenderUnionInfo.get(union_id=self.union_id)
            self.petal = fresh.petal
            return True

    async def clear_petal(self) -> bool:
        """清空用户的花瓣余额。"""
        return await self.edit_attr("petal", 0)

    async def edit_sender_data(self, key: str, value: Any | None = None) -> bool:
        """
        设置用户数据。

        :param key: 键名称。
        :param value: 值，若留空则删除该键值对。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                current = await (
                    SenderUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False
                sender_data = dict(current.sender_data or {})
                if value is None:
                    sender_data.pop(key, None)
                else:
                    sender_data[key] = value
                await (
                    SenderUnionInfo.filter(union_id=self.union_id).using_db(connection).update(sender_data=sender_data)
                )
                self.sender_data = sender_data
                return True

    async def bind_id(self, sender_id: str) -> bool:
        """
        将平台账号绑定至该 union。

        :param sender_id: 平台账号 ID。
        :return: 是否绑定成功，若该账号已绑定至其他 union 则返回 False。
        """
        async with union_mutation():
            async with in_transaction("default"):
                current = await SenderUnionInfo.filter(union_id=self.union_id).select_for_update().first()
                if not current:
                    return False
                bind, _ = await SenderUnionBind.get_or_create(
                    sender_id=sender_id,
                    defaults={"union_id": self.union_id},
                )
                return bind.union_id == self.union_id

    async def unbind_id(self, sender_id: str) -> "SenderUnionInfo | None":
        """将一个平台账号从该 union 中拆出，数据留在原 union，该账号从零开始。

        :param sender_id: 平台账号 ID。
        :return: 拆出后该账号所属的新 union，若无法解绑则为 None。
        """
        async with union_mutation():
            # 创建新组、重新关联映射和继承场景限制名单必须以原子操作完成。否则最后一步执行失败会导致残留
            # 孤立的新 union，并使账号脱离原组后未能继承全部限制状态。
            async with in_transaction("default"):
                current = await SenderUnionInfo.filter(union_id=self.union_id).select_for_update().first()
                if not current:
                    return None
                binds = await SenderUnionBind.filter(union_id=self.union_id).values_list("sender_id", flat=True)
                if sender_id not in binds or len(binds) <= 1:
                    return None

                union = await SenderUnionInfo.create(
                    union_id=new_union_id(UNION_SCOPE_SENDER),
                    blocked=current.blocked,
                    warns=current.warns,
                )
                # 首先创建新组，随后重新关联映射行，全程避免出现“账号缺少映射行”的中间状态。
                # union_id 并非主键，可通过单条 UPDATE 语句完成重新关联。
                await SenderUnionBind.filter(sender_id=sender_id, union_id=self.union_id).update(
                    union_id=union.union_id
                )
                await migrate_unbound_union_references(
                    UNION_SCOPE_SENDER,
                    sender_id,
                    self.union_id,
                    union.union_id,
                )
                await inherit_banned_union_refs(self.union_id, union.union_id)
                return union

    async def merge_union(
        self, other: "SenderUnionInfo", keep_other_tables: set[str] | None = None
    ) -> "SenderUnionInfo | None":
        """把两个 union 合并成一个全新的 union，随后删除原有的两个。

        :param other: 参与合并的另一方。
        :param keep_other_tables: 模块表冲突时以 ``other`` 为准的表名集合，其余情况保留自身。
        :return: 合并后的新 union，两侧本就同组时为 None。
        """
        if other.union_id == self.union_id:
            return None

        # 合并操作同时涉及核心表、平台映射、权限引用与若干模块表的改写。任何步骤失败均必须整体回滚，
        # 避免出现新旧 union 并存或仅部分模块数据完成迁移的不可恢复状态。
        async with union_mutation():
            async with in_transaction("default") as connection:
                union_ids = [self.union_id, other.union_id]
                fresh_rows = await (
                    SenderUnionInfo.filter(union_id__in=union_ids)
                    .using_db(connection)
                    .order_by("union_id")
                    .select_for_update()
                )
                fresh_by_id = {row.union_id: row for row in fresh_rows}
                fresh_self = fresh_by_id.get(self.union_id)
                fresh_other = fresh_by_id.get(other.union_id)
                if not fresh_self or not fresh_other:
                    return None

                merged = await SenderUnionInfo.create(
                    union_id=new_union_id(UNION_SCOPE_SENDER),
                    blocked=fresh_self.blocked or fresh_other.blocked,
                    trusted=fresh_self.trusted or fresh_other.trusted,
                    superuser=fresh_self.superuser or fresh_other.superuser,
                    warns=max(fresh_self.warns, fresh_other.warns),
                    petal=fresh_self.petal + fresh_other.petal,
                    sender_data={**fresh_other.sender_data, **fresh_self.sender_data},
                    using_db=connection,
                )

                # 首先依据冲突解决策略将两侧模块数据合并至一处，随后整体重新关联至新组。新组初始为空，第二阶段不再产生冲突。
                await migrate_union_tables(
                    fresh_other.union_id,
                    fresh_self.union_id,
                    keep_other_tables,
                    scope=UNION_SCOPE_SENDER,
                )
                await migrate_union_tables(fresh_self.union_id, merged.union_id, scope=UNION_SCOPE_SENDER)

                for old_union in (fresh_self.union_id, fresh_other.union_id):
                    await migrate_union_references(UNION_SCOPE_SENDER, old_union, merged.union_id)
                    await rewrite_sender_union_refs(old_union, merged.union_id)
                    await (
                        SenderUnionBind.filter(union_id=old_union).using_db(connection).update(union_id=merged.union_id)
                    )

                await fresh_self.delete(using_db=connection)
                await fresh_other.delete(using_db=connection)
                return merged


class TargetUnionInfo(UnionInfo):
    """场景信息。

    :param union_id: 场景 union ID。
    :param blocked: 是否为黑名单场景。
    :param muted: 是否禁用机器人。
    :param locale: 场景语言。
    :param modules: 场景内可用模块。
    :param custom_admins: 场景内自定义管理员列表（存 union ID）。
    :param banned_users: 场景内已限制用户（存 union ID）。
    :param target_data: 场景数据。
    """

    union_scope = UNION_SCOPE_TARGET
    bind_model = TargetUnionBind

    muted = fields.BooleanField(default=False)
    locale = fields.CharField(max_length=32, default=default_locale)
    modules = fields.JSONField(default=[])
    custom_admins = fields.JSONField(default=[])
    banned_users = fields.JSONField(default=[])
    target_data = fields.JSONField(default={})

    class Meta:
        table = "target_union_info"

    @overload
    @classmethod
    async def get_by_target_id(cls, target_id: Any, create: Literal[True] = True) -> "TargetUnionInfo": ...

    @overload
    @classmethod
    async def get_by_target_id(cls, target_id: Any, create: bool) -> "TargetUnionInfo | None": ...

    @classmethod
    async def get_by_target_id(cls, target_id: Any, create: bool = True) -> "TargetUnionInfo | None":
        """
        获取平台场景所属的 union 记录行，为 :meth:`UnionInfo.resolve_union` 的会话便捷封装。
        方法接受 MessageSession 或 FetchedMessageSession，并自动提取 ``target_id``。
        """
        return await cls._resolve_session(target_id, create)

    def list_peer_bots(self, target_id: str) -> list[str]:
        """
        获取指定平台场景视角下、同一现实场景中其他机器人的账号。

        :param target_id: 观察方的平台场景 ID。
        """
        return list(normalize_peer_bots(self.target_data.get("bots_id")).get(target_id, {}).values())

    async def _link_peer_bots_unlocked(
        self,
        links: dict[str, dict[str, str]],
        current: "TargetUnionInfo",
        connection,
    ) -> bool:
        target_data = dict(current.target_data or {})
        peers = normalize_peer_bots(target_data.get("bots_id"))
        for observer, entries in links.items():
            peers.setdefault(observer, {}).update({peer: bot_id for peer, bot_id in entries.items() if bot_id})
        target_data["bots_id"] = peers
        await TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).update(target_data=target_data)
        self.target_data = target_data
        current.target_data = target_data
        return True

    async def link_peer_bots(self, links: dict[str, dict[str, str]]) -> bool:
        """
        记录机器人互认关系。

        :param links: ``{观察方场景 ID: {对端场景 ID: 对端机器人在观察方平台的账号}}``。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False
                return await self._link_peer_bots_unlocked(links, current, connection)

    async def _forget_peer_bots_unlocked(
        self,
        target_id: str,
        current: "TargetUnionInfo",
        connection,
    ) -> bool:
        target_data = dict(current.target_data or {})
        peers = normalize_peer_bots(target_data.get("bots_id"))
        peers.pop(target_id, None)
        for entries in peers.values():
            entries.pop(target_id, None)
        target_data["bots_id"] = {observer: entries for observer, entries in peers.items() if entries}
        await TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).update(target_data=target_data)
        self.target_data = target_data
        return True

    async def forget_peer_bots(self, target_id: str) -> bool:
        """将某个平台场景从机器人互认记录中完全移除，包含它自身的记录与其它场景对它的记录。

        :param target_id: 要移除的平台场景 ID。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False
                return await self._forget_peer_bots_unlocked(target_id, current, connection)

    @classmethod
    async def reassign_channel(cls, target_id: str, channel_id: int | None = None) -> int | None:
        """原子地把单个平台场景移到另一条消息通道。

        :param target_id: 要移动的平台场景 ID。
        :param channel_id: 目标通道号，为 ``None`` 时新建一条通道。
        :return: 实际通道号，场景或所属 Union 已不存在时为 ``None``。
        """
        async with union_mutation():
            # Union 事务统一先锁定核心行，再锁定映射行。逆序加锁将在 MySQL 环境下导致循环死锁。
            # 锁定核心行后必须重新读取映射并验证其未被重新关联。
            for _attempt in range(2):
                candidate = await TargetUnionBind.get_or_none(target_id=target_id)
                if not candidate:
                    return None
                retry = False
                async with in_transaction("default") as connection:
                    current = await (
                        cls.filter(union_id=candidate.union_id).using_db(connection).select_for_update().first()
                    )
                    if not current:
                        retry = True
                    else:
                        bind = await (
                            TargetUnionBind.filter(target_id=target_id).using_db(connection).select_for_update().first()
                        )
                        if not bind:
                            return None
                        if bind.union_id != candidate.union_id:
                            retry = True
                        else:
                            assigned_channel = channel_id
                            if assigned_channel is None:
                                channels = await (
                                    TargetUnionBind.filter(union_id=bind.union_id)
                                    .using_db(connection)
                                    .values_list("channel_id", flat=True)
                                )
                                assigned_channel = max(channels) + 1 if channels else 1
                            assigned_channel = int(assigned_channel)
                            if bind.channel_id == assigned_channel:
                                return assigned_channel

                            await (
                                TargetUnionBind.filter(target_id=target_id, union_id=bind.union_id)
                                .using_db(connection)
                                .update(channel_id=assigned_channel)
                            )
                            await current._forget_peer_bots_unlocked(target_id, current, connection)
                            return assigned_channel
                if not retry:
                    break
            return None

    @classmethod
    async def unify_channels(cls, anchor_target_id: str, other_target_id: str) -> int | None:
        """原子地把两个场景当前所在的完整消息通道合并为一条。

        :param anchor_target_id: 保留其通道号的平台场景 ID。
        :param other_target_id: 将其完整通道并入锚点通道的平台场景 ID。
        :return: 合并后的通道号，任一绑定或所属 Union 已不存在、或两者不同组时为 ``None``。
        """
        target_ids = list(dict.fromkeys([anchor_target_id, other_target_id]))
        async with union_mutation():
            async with in_transaction("default") as connection:
                binds = await (
                    TargetUnionBind.filter(target_id__in=target_ids)
                    .using_db(connection)
                    .order_by("target_id")
                    .select_for_update()
                )
                by_id = {bind.target_id: bind for bind in binds}
                anchor = by_id.get(anchor_target_id)
                other = by_id.get(other_target_id)
                if not anchor or not other or anchor.union_id != other.union_id:
                    return None
                current = await cls.filter(union_id=anchor.union_id).using_db(connection).select_for_update().first()
                if not current:
                    return None
                if anchor.channel_id == other.channel_id:
                    return anchor.channel_id

                await (
                    TargetUnionBind.filter(union_id=anchor.union_id, channel_id=other.channel_id)
                    .using_db(connection)
                    .update(channel_id=anchor.channel_id)
                )
                return anchor.channel_id

    async def bind_id(self, target_id: str) -> bool:
        """
        将平台场景绑定至该 union。

        :param target_id: 平台场景 ID。
        :return: 是否绑定成功，若该场景已绑定至其他 union 则返回 False。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                # MySQL 环境下锁定 union 数据行，使不同 Server 进程无法同时依据相同最大通道号分配通道编号。
                # SQLite 会忽略行锁语义，由外层 asyncio.Lock 保证单 Server 进程内的顺序。
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False

                bind = await TargetUnionBind.filter(target_id=target_id).using_db(connection).first()
                if bind:
                    return bind.union_id == self.union_id

                channels = await (
                    TargetUnionBind.filter(union_id=self.union_id)
                    .using_db(connection)
                    .values_list("channel_id", flat=True)
                )
                channel_id = max(channels) + 1 if channels else 1
                bind, _ = await TargetUnionBind.get_or_create(
                    target_id=target_id,
                    defaults={"union_id": self.union_id, "channel_id": channel_id},
                    using_db=connection,
                )
                return bind.union_id == self.union_id

    async def unbind_id(self, target_id: str) -> "TargetUnionInfo | None":
        """
        将指定平台场景自该 union 中拆分，历史数据保留于原 union，该场景重置为空白状态。

        :param target_id: 平台场景 ID。
        :return: 拆分后该场景所属的新 union，若无法解绑则为 None。
        """
        async with union_mutation():
            # 新组创建、平台映射重新关联与互认记录迁移属于同一次解绑事务。任何步骤失败均必须完整回滚，严禁数据库处于部分迁移状态。
            async with in_transaction("default") as connection:
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return None
                binds = await (
                    TargetUnionBind.filter(union_id=self.union_id)
                    .using_db(connection)
                    .values_list("target_id", flat=True)
                )
                if target_id not in binds or len(binds) <= 1:
                    return None

                # 封禁状态随场景一并转移，避免通过解绑规避限制。
                union = await TargetUnionInfo.create(
                    union_id=new_union_id(UNION_SCOPE_TARGET),
                    blocked=current.blocked,
                    locale=current.locale,
                    using_db=connection,
                )
                # 首先创建新组，随后重新关联映射行，全程避免出现“场景缺少映射行”的中间状态。
                # 新组初始仅包含该场景，其消息通道编号重置为 1。
                moved = await (
                    TargetUnionBind.filter(target_id=target_id, union_id=self.union_id)
                    .using_db(connection)
                    .update(union_id=union.union_id, channel_id=1)
                )
                if not moved:
                    await union.delete(using_db=connection)
                    return None
                await migrate_unbound_union_references(
                    UNION_SCOPE_TARGET,
                    target_id,
                    self.union_id,
                    union.union_id,
                )
                # 拆分出的场景与原组内的机器人不再对应同一现实场景，互认记录必须一并清除。
                # 新组的 target_data 初始为空，仅需清理保留的一侧。调用内部方法避免重复获取全局锁。
                await self._forget_peer_bots_unlocked(target_id, current, connection)
                return union

    async def merge_union(
        self, other: "TargetUnionInfo", keep_other_tables: set[str] | None = None
    ) -> "TargetUnionInfo | None":
        """把两个 union 合并成一个全新的 union，随后删除原有的两个。

        :param other: 参与合并的另一方。
        :param keep_other_tables: 模块表冲突时以 ``other`` 为准的表名集合，其余情况保留自身。
        :return: 合并后的新 union，两侧本就同组时为 None。
        """
        if other.union_id == self.union_id:
            return None

        async with union_mutation():
            async with in_transaction("default") as connection:
                union_ids = [self.union_id, other.union_id]
                fresh_rows = await (
                    TargetUnionInfo.filter(union_id__in=union_ids)
                    .using_db(connection)
                    .order_by("union_id")
                    .select_for_update()
                )
                fresh_by_id = {row.union_id: row for row in fresh_rows}
                fresh_self = fresh_by_id.get(self.union_id)
                fresh_other = fresh_by_id.get(other.union_id)
                if not fresh_self or not fresh_other:
                    return None

                # bots_id 为二级嵌套结构，若随 target_data 执行浅合并，将导致 other 一侧的互认记录被整体覆盖，
                # 因此必须单独计算并集。
                peer_bots = normalize_peer_bots(fresh_other.target_data.get("bots_id"))
                for observer, entries in normalize_peer_bots(fresh_self.target_data.get("bots_id")).items():
                    peer_bots.setdefault(observer, {}).update(entries)

                merged = await TargetUnionInfo.create(
                    union_id=new_union_id(UNION_SCOPE_TARGET),
                    blocked=fresh_self.blocked or fresh_other.blocked,
                    muted=fresh_self.muted or fresh_other.muted,
                    locale=fresh_self.locale,
                    modules=list(dict.fromkeys([*(fresh_self.modules or []), *(fresh_other.modules or [])])),
                    custom_admins=list(
                        dict.fromkeys([*(fresh_self.custom_admins or []), *(fresh_other.custom_admins or [])])
                    ),
                    banned_users=list(
                        dict.fromkeys([*(fresh_self.banned_users or []), *(fresh_other.banned_users or [])])
                    ),
                    target_data={**fresh_other.target_data, **fresh_self.target_data, "bots_id": peer_bots},
                    using_db=connection,
                )

                # 首先依据冲突解决策略将两侧模块数据合并至一处，随后整体重新关联至新组。新组初始为空，第二阶段不再产生冲突。
                await migrate_union_tables(
                    fresh_other.union_id,
                    fresh_self.union_id,
                    keep_other_tables,
                    scope=UNION_SCOPE_TARGET,
                )
                await migrate_union_tables(fresh_self.union_id, merged.union_id, scope=UNION_SCOPE_TARGET)
                for old_union in (fresh_self.union_id, fresh_other.union_id):
                    await migrate_union_references(UNION_SCOPE_TARGET, old_union, merged.union_id)

                # 自身一侧通道编号保持不变，并入方执行整体平移，严禁逐条分配新编号。
                # 通道平移必须依据原通道编号建立映射，确保并入方内部处于同一通道的场景在平移后继续归属于同一通道。
                await (
                    TargetUnionBind.filter(union_id=fresh_self.union_id)
                    .using_db(connection)
                    .update(union_id=merged.union_id)
                )
                moved_channels: dict[int, int] = {}
                for bind in await (
                    TargetUnionBind.filter(union_id=fresh_other.union_id).using_db(connection).order_by("bound_at")
                ):
                    if bind.channel_id not in moved_channels:
                        moved_channels[bind.channel_id] = await TargetUnionBind.next_channel_id(merged.union_id)
                    bind.union_id = merged.union_id
                    bind.channel_id = moved_channels[bind.channel_id]
                    await bind.save(using_db=connection)

                await fresh_self.delete(using_db=connection)
                await fresh_other.delete(using_db=connection)
                return merged

    async def config_module(self, module_name: str | list | tuple, enable: bool = True) -> bool:
        """
        设置场景内可用模块。

        :param module_name: 指定的模块名称。
        :param enable: 是否启用该模块。若为 False 则禁用。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False
                modules = list(current.modules or [])
                for mname in convert_list(module_name):
                    related_names = _get_module_and_alias_first_words(mname)
                    canonical_name = related_names[0]
                    modules = [name for name in modules if name not in related_names]
                    if enable:
                        modules.append(canonical_name)
                modules = list(dict.fromkeys(modules))
                await TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).update(modules=modules)
                self.modules = modules
                return True

    async def switch_mute(self) -> bool:
        """
        切换场景内机器人禁止发言与禁用状态。

        :return: 机器人是否被禁用。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False
                muted = not current.muted
                await TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).update(muted=muted)
                self.muted = muted
                return muted

    async def edit_target_data(self, key: str, value: Any | None = None) -> bool:
        """
        设置场景数据。

        :param key: 键名称。
        :param value: 值，若留空则删除该键值对。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False
                target_data = dict(current.target_data or {})
                if value is None:
                    target_data.pop(key, None)
                else:
                    target_data[key] = value
                await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).update(target_data=target_data)
                )
                self.target_data = target_data
                return True

    async def config_custom_admin(self, sender_union_id: str, enable: bool = True) -> bool:
        """
        设置场景内管理员。

        :param sender_union_id: 指定的用户 union ID。
        :param enable: 是否授予场景管理员权限。若为 False 则撤销权限。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False
                custom_admins = list(current.custom_admins or [])
                if enable:
                    if sender_union_id in custom_admins:
                        return False
                    custom_admins.append(sender_union_id)
                elif sender_union_id in custom_admins:
                    custom_admins.remove(sender_union_id)
                else:
                    return False

                await (
                    TargetUnionInfo.filter(union_id=self.union_id)
                    .using_db(connection)
                    .update(custom_admins=custom_admins)
                )
                self.custom_admins = custom_admins
                return True

    async def config_banned_user(self, sender_union_id: str, enable: bool = True) -> bool:
        """
        设置场景内被限制用户。

        :param sender_union_id: 指定的用户 union ID。
        :param enable: 是否限制该用户在场景内使用机器人。若为 False 则解除限制。
        """
        async with union_mutation():
            async with in_transaction("default") as connection:
                current = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False
                banned_users = list(current.banned_users or [])
                if enable:
                    if sender_union_id in banned_users:
                        return False
                    banned_users.append(sender_union_id)
                elif sender_union_id in banned_users:
                    banned_users.remove(sender_union_id)
                else:
                    return False

                await (
                    TargetUnionInfo.filter(union_id=self.union_id)
                    .using_db(connection)
                    .update(banned_users=banned_users)
                )
                self.banned_users = banned_users
                return True

    @classmethod
    async def get_target_list_by_module(
        cls, module_name: str | list[str] | tuple[str, ...] | None, id_prefix: str | None = None
    ) -> list[TargetUnionInfo]:
        """
        获取已启用该模块的全部场景列表。

        :param module_name: 指定的模块名称。
        :param id_prefix: 指定的 ID 前缀，按 union 下绑定的平台场景 ID 匹配。
        :return: 符合要求的场景 union 列表。
        """
        if id_prefix:
            union_ids = await TargetUnionBind.filter(target_id__startswith=id_prefix).values_list("union_id", flat=True)
            all_targets = await cls.filter(union_id__in=list(set(union_ids)))
        else:
            all_targets = await cls.all()

        if module_name:
            module_names = _get_module_and_alias_first_words(module_name)
            result = []
            for target in all_targets:
                modules = target.modules or []
                if any(mod in modules for mod in module_names):
                    result.append(target)
            return result

        return list(all_targets)

    @classmethod
    async def get_target_id_list_by_module(
        cls, module_name: str | list[str] | tuple[str, ...] | None, id_prefix: str | None = None
    ) -> list[str]:
        """获取开启此模块的所有平台场景 ID 列表。

        :param module_name: 指定的模块名称。
        :param id_prefix: 指定的 ID 前缀。
        :return: 符合要求的平台场景 ID 列表。
        """
        unions = await cls.get_target_list_by_module(module_name, id_prefix)
        if not unions:
            return []
        query = TargetUnionBind.filter(union_id__in=[t.union_id for t in unions])
        if id_prefix:
            query = query.filter(target_id__startswith=id_prefix)
        return list(await query.values_list("target_id", flat=True))


class StoredData(DBModel):
    """
    持久化数据存储。

    :param stored_key: 存储键名称。
    :param value: 存储值。
    """

    stored_key = fields.CharField(max_length=512, primary_key=True)
    value = fields.JSONField(default=[])

    class Meta:
        table = "stored_data"


class AnalyticsData(DBModel):
    """
    统计数据。

    :param module_name: 模块名称。
    :param module_type: 模块类型。
    :param target_id: 场景 ID。
    :param sender_id: 用户 ID。
    :param target_union_id: 场景所属 union ID。
    :param sender_union_id: 用户所属 union ID。
    :param command: 命令名称。
    :param timestamp: 时间戳。
    """

    id = fields.IntField(primary_key=True)
    module_name = fields.CharField(max_length=512)
    module_type = fields.CharField(max_length=512)
    target_id = fields.CharField(max_length=512)
    sender_id = fields.CharField(max_length=512, null=True, default=None)
    target_union_id = fields.CharField(max_length=512, null=True, default=None)
    sender_union_id = fields.CharField(max_length=512, null=True, default=None)
    command = fields.TextField()
    # 统计命令按时间区间频繁聚合，缺少索引时每次均会执行全表扫描。
    timestamp = fields.DatetimeField(auto_now_add=True, db_index=True)

    class Meta:
        table = "analytics_data"

    @classmethod
    async def get_data_by_times(cls, new, old, module_name=None):
        """按时间范围获取统计数据。"""
        query = cls.filter(timestamp__gte=old, timestamp__lte=new)
        if module_name is not None:
            query = query.filter(module_name=module_name)
        return await query.all()

    @classmethod
    async def get_values_by_times(cls, new, old, module_name=None):
        """按时间范围获取数值。"""
        query = cls.filter(timestamp__gte=old, timestamp__lte=new)
        if module_name is not None:
            query = query.filter(module_name=module_name)
        return await query.values()

    @classmethod
    async def get_count_by_times(cls, new, old, module_name=None):
        """按时间范围统计数量。"""
        query = cls.filter(timestamp__gte=old, timestamp__lte=new)
        if module_name is not None:
            query = query.filter(module_name=module_name)
        return await query.count()

    @classmethod
    async def get_modules_count(cls):
        """获取按模块统计的数量。"""
        analytics = await cls.all().values("module_name")
        module_counter = Counter([entry["module_name"] for entry in analytics])
        return dict(module_counter)

    @classmethod
    async def get_modules_count_by_times(cls, new, old) -> dict[str, int]:
        """按时间区间统计各模块的调用次数。

        :param new: 区间起点（含）。
        :param old: 区间终点（含）。
        :return: 模块名到调用次数的映射。
        """
        rows = (
            await cls.filter(timestamp__gte=old, timestamp__lte=new)
            .group_by("module_name")
            .annotate(count=Count("id"))
            .values("module_name", "count")
        )
        return {row["module_name"]: row["count"] for row in rows if row["module_name"] is not None}


class ModuleStatus(DBModel):
    """
    模块状态。

    :param module_name: 模块名称。
    :param load: 是否已加载。
    """

    module_name = fields.CharField(primary_key=True, max_length=255, unique=True)
    load = fields.BooleanField(default=False)

    class Meta:
        table = "module_status"

    @classmethod
    async def init_modules(cls, modules_list: list[str], module_aliases: dict[str, list[str]] | None = None):
        """初始化模块状态记录。"""
        async with in_transaction("default"):
            existing = dict(await cls.all().values_list("module_name", "load"))
            existing_set = set(existing)
            input_set = set(modules_list)

            to_add = input_set.difference(existing_set)
            to_remove = existing_set.difference(input_set)

            if to_add:
                migrated_load = {}
                for module_name in to_add:
                    for alias in (module_aliases or {}).get(module_name, []):
                        if alias in existing:
                            migrated_load[module_name] = existing[alias]
                            break
                await cls.bulk_create([cls(module_name=m, load=migrated_load.get(m, True)) for m in to_add])

            if to_remove:
                await cls.filter(module_name__in=to_remove).delete()

    @classmethod
    async def set_module_loaded(cls, module_name: str, load: bool = True):
        """设置模块的加载状态。"""
        module = await cls.filter(module_name=module_name).first()
        if module:
            module.load = load
            await module.save()
        else:
            raise ValueError(f"Module '{module_name}' not found")

    @classmethod
    async def get_all_modules(cls) -> list[str]:
        """获取全部模块状态。"""
        return await cls.all().values_list("module_name", flat=True)

    @classmethod
    async def get_loaded_modules(cls) -> list[str]:
        """获取已加载的模块列表。"""
        return await cls.filter(load=True).values_list("module_name", flat=True)

    @classmethod
    async def get_unloaded_modules(cls) -> list[str]:
        """获取未加载的模块列表。"""
        return await cls.filter(load=False).values_list("module_name", flat=True)


class DBVersion(DBModel):
    """
    数据库版本。

    :param version: 数据库版本号。
    """

    version = fields.IntField(primary_key=True)

    class Meta:
        table = "database_version"


class UnfriendlyActionRecords(DBModel):
    """
    不友好行为记录。

    :param target_id: 场景 ID。
    :param sender_id: 用户 ID。
    :param target_union_id: 场景所属 union ID。
    :param sender_union_id: 用户所属 union ID。
    :param action: 行为类型。
    :param detail: 行为详情。
    :param timestamp: 时间戳。
    """

    id = fields.IntField(primary_key=True)
    target_id = fields.CharField(max_length=512)
    sender_id = fields.CharField(max_length=512)
    target_union_id = fields.CharField(max_length=512, null=True, default=None)
    sender_union_id = fields.CharField(max_length=512, null=True, default=None)
    action = fields.CharField(max_length=512)
    detail = fields.CharField(max_length=512)
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "unfriendly_actions"

    @classmethod
    async def check_mute(cls, target_id) -> bool:
        """检查场景的禁言行为记录。

        :return: 如果：
        - 场景在过去 5 天内有超过 5 条记录
        - 场景内某一用户的记录（在过去 1 天内）超过 3 次
        - 场景内的不同用户的记录（在过去 1 天内）有 3 个以上
        """
        target_union_info = await TargetUnionInfo.resolve_union(target_id, create=False)
        if target_union_info:
            records = await cls.filter(target_union_id=target_union_info.union_id, action="mute").all()
        else:
            records = await cls.filter(target_id=target_id, action="mute").all()
        unfriendly_list = [
            record
            for record in records
            if (datetime.now(UTC) - record.timestamp).total_seconds() < 432000  # 5 days
        ]

        if len(unfriendly_list) > 5:
            return True

        count = {}
        for record in unfriendly_list:
            if (datetime.now(UTC) - record.timestamp).total_seconds() < 86400:  # 1 day
                key = record.sender_union_id or record.sender_id
                count[key] = count.get(key, 0) + 1

        if len(count) >= 3 or any(c >= 3 for c in count.values()):
            return True

        return False


class JobQueuesTable(DBModel):
    """
    任务队列表。

    :param task_id: 任务 ID。
    :param target_peer: 目标节点进程实例或服务。
    :param expects_response: 调用方是否等待终态结果。
    :param action: 操作类型。
    :param args: 参数。
    :param status: 任务状态。
    :param result: 任务结果。
    :param timestamp: 时间戳。
    """

    ACTIVE_TIMEOUT_SECONDS: ClassVar[int] = DEFAULT_TIMEOUT_SECONDS

    task_id = fields.UUIDField(primary_key=True)
    correlation_id = fields.UUIDField(null=True, index=True)
    source_peer_id = fields.CharField(max_length=128, null=True, index=True)
    target_peer = fields.CharField(max_length=512)
    message_kind = fields.CharField(max_length=16, default="rpc")
    expects_response = fields.BooleanField(default=True)
    action = fields.CharField(max_length=512)
    args = fields.JSONField(default={})
    status = fields.CharField(max_length=32, default="pending")
    claimed_by = fields.CharField(max_length=128, null=True, index=True)
    result = fields.JSONField(default={})
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "job_queues"
        # 每个进程每 100 毫秒依据该两列轮询一次，缺少索引时开销将随表内行数线性增长。
        # status / timestamp 索引用于低成本回收调用方异常退出后遗留的终态记录。
        indexes = (("target_peer", "status"), ("status", "timestamp"))

    @classmethod
    async def add_task(cls, target_peer: str, action: str, args: dict) -> str:
        """向任务队列表添加任务。"""
        task_id = str(uuid.uuid4())
        await cls.create(task_id=task_id, target_peer=target_peer, action=action, args=args)
        return task_id

    async def set_val(self, value, status) -> bool:
        """更新任务的执行结果与关联属性。"""
        self.result = value
        self.status = status
        await self.save()
        return True

    async def set_status(self, status):
        """设置任务状态。"""
        self.status = status
        await self.save()
        return True

    async def claim(self, peer_id: str | None = None) -> bool:
        """以原子操作将 pending 状态的任务认领为 processing 状态。"""
        updated = (
            await type(self)
            .filter(task_id=self.task_id, status="pending")
            .update(status="processing", claimed_by=peer_id)
        )
        if updated:
            self.status = "processing"
            self.claimed_by = peer_id
            return True
        return False

    @classmethod
    async def clear_task(cls, time=3600, include_active=False) -> bool:
        """清理或删除任务记录。"""
        now = datetime.now(UTC)
        timestamp = now - timedelta(seconds=time)
        Logger.debug(f"Clearing tasks older than {timestamp}...")

        if include_active:
            await cls.filter(timestamp__lt=timestamp).delete()
            return True

        # 定时清理仅删除已进入终态且超过保留期的任务。pending 与 processing 状态最长可执行两小时，
        # 若沿用无条件删除，对应任务将在等待方与执行方超时机制生效前提前被清理。
        await cls.filter(timestamp__lt=timestamp, status__in=["done", "failed", "timeout"]).delete()

        # 超过全局执行上限的活跃任务已无法正常完成，无需响应的任务直接删除。
        # 等待型任务先标记为 timeout 供轮询机制获取终态。终态删除必须在本步骤之前完成。
        active_timeout = now - timedelta(seconds=cls.ACTIVE_TIMEOUT_SECONDS)
        stale_active = cls.filter(timestamp__lt=active_timeout, status__in=["pending", "processing"])
        await stale_active.filter(expects_response=False).delete()
        await stale_active.filter(expects_response=True).update(status="timeout", result={})
        return True

    @classmethod
    async def get_first(cls, target_peers: str | list[str]):
        """获取队列表中的首个任务。"""
        if isinstance(target_peers, str):
            target_peers = [target_peers]
        return await cls.filter(target_peer__in=target_peers, status="pending").first()

    @classmethod
    async def get_all(cls, target_peers: str | list[str], limit: int | None = None):
        """获取全部任务记录。"""
        if isinstance(target_peers, str):
            target_peers = [target_peers]
        # 此处不附加 ORDER BY 排序，复用既有 (target_peer, status) 索引可在匹配至 limit 阈值后提前终止扫描。
        # JobQueue 本身不承诺严格 FIFO 语义，以此避免在获取候选批次时对全量积压记录生成临时排序表。
        query = cls.filter(target_peer__in=target_peers, status="pending")
        if limit is not None:
            query = query.limit(limit)
        return await query.all()


class JobQueuePeersTable(DBModel):
    """JobQueue 进程注册表。租约是在线状态的唯一来源。"""

    peer_id = fields.CharField(max_length=128, primary_key=True)
    node_id = fields.CharField(max_length=128, null=True, index=True)
    role = fields.CharField(max_length=32, index=True)
    service = fields.CharField(max_length=128, index=True)
    state = fields.CharField(max_length=16, default="starting", index=True)
    capabilities = fields.JSONField(default=list)
    metadata = fields.JSONField(default=dict)
    started_at = fields.DatetimeField(auto_now_add=True)
    heartbeat_at = fields.DatetimeField(auto_now=True)
    lease_until = fields.DatetimeField(index=True)

    class Meta:
        table = "job_queue_peers"
        indexes = (("role", "service", "state"), ("state", "lease_until"))

    @classmethod
    async def active(cls):
        return await cls.filter(state="ready", lease_until__gt=datetime.now(UTC)).all()


class MaliciousLoginRecords(DBModel):
    """
    恶意登录行为记录。

    :param id: 记录 ID。
    :param ip_address: IP 地址。
    :param blocked_until: 封禁截止时间。
    :param created_date: 创建日期。
    """

    id = fields.IntField(primary_key=True)
    ip_address = fields.CharField(max_length=45)
    blocked_until = fields.DatetimeField()
    created_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "malicious_login"

    @classmethod
    async def check_blocked(cls, ip_address: str) -> bool:
        """检查登录来源是否已被封禁拦截。"""
        return await cls.filter(ip_address=ip_address, blocked_until__gt=datetime.now(UTC)).exists()


class SchemaMigration(DBModel):
    """
    已应用的数据库迁移记录。

    每个成员包的每条 revision 在此各记录一行，取代全局唯一的数据库版本号。MySQL 的 DDL 会自动
    提交，无法将“执行 DDL”与“写入版本记录”纳入同一事务，因此判断某条 revision 是否已应用
    仅查询本表，迁移必须自行保证可重复执行。

    :param package: 包名称，``core`` 或其他包名称。
    :param revision: revision 标识符。
    :param applied_at: 应用时间。
    :param checksum: 迁移文件源码的 SHA-256 哈希值，用于发现已应用的迁移被改写。
    """

    package = fields.CharField(max_length=255)
    revision = fields.CharField(max_length=255)
    applied_at = fields.DatetimeField(auto_now_add=True)
    checksum = fields.CharField(max_length=64, null=True)

    class Meta:
        table = "schema_migrations"
        unique_together = (("package", "revision"),)
