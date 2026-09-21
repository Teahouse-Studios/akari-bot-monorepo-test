from copy import deepcopy
from datetime import datetime, UTC

import orjson
from tortoise import fields
from tortoise.transactions import in_transaction

from core.database.base import DBModel
from core.database.models import TargetUnionInfo, UNION_SCOPE_TARGET, union_mutation

table_prefix = "module_wiki_"


class WikiTargetInfo(DBModel):
    """
    场景内 Wiki 绑定信息表。

    :param union_id: 场景 union ID
    :param api_link: API 链接
    :param interwikis: 自定义 iw 信息
    :param headers: 自定义请求头
    :param prefix: 自定义请求前缀
    """

    union_scope = UNION_SCOPE_TARGET
    union_id = fields.CharField(max_length=512, primary_key=True)
    api_link = fields.CharField(max_length=512, null=True)
    interwikis = fields.JSONField(default={})
    headers = fields.JSONField(default={"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"})
    prefix = fields.CharField(max_length=512, null=True)

    class Meta:
        table = f"{table_prefix}target_set_info"

    async def _mutate(self, mutation) -> bool:
        """在 Union 与模块行均存在时，基于数据库中的最新值执行一次定向更新。"""
        async with union_mutation():
            async with in_transaction("default") as connection:
                target = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not target:
                    return False

                current = await (
                    type(self).filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False

                updates = mutation(current)
                if updates is None:
                    return False
                await type(self).filter(union_id=self.union_id).using_db(connection).update(**updates)
                for field_name, value in updates.items():
                    setattr(self, field_name, deepcopy(value))
                return True

    async def add_start_wiki(self, url: str):
        return await self._mutate(lambda _: {"api_link": url})

    async def config_interwikis(self, iw: str, iwlink: str | None = None):
        def mutate(current):
            interwikis = deepcopy(current.interwikis or {})
            if iwlink:
                interwikis[iw] = iwlink
            else:
                interwikis.pop(iw, None)
            return {"interwikis": interwikis}

        return await self._mutate(mutate)

    async def config_headers(self, headers: str | None = None, add: bool = True):
        try:
            parsed_headers = orjson.loads(headers) if headers and add else None
            if parsed_headers is not None and not isinstance(parsed_headers, dict):
                return False

            def mutate(current):
                current_headers = deepcopy(current.headers or {})
                if parsed_headers is not None:
                    current_headers.update(parsed_headers)
                elif headers:
                    current_headers = {key: value for key, value in current_headers.items() if key != headers}
                else:
                    current_headers = {}
                return {"headers": current_headers}

            return await self._mutate(mutate)
        except Exception:
            return False

    async def config_prefix(self, prefix: str | None = None):
        return await self._mutate(lambda _: {"prefix": prefix})


class WikiSiteInfo(DBModel):
    """
    Wiki 站点信息表。

    :param api_link: API 链接
    :param site_info: 站点信息
    :param timestamp: 更新时间
    """

    api_link = fields.CharField(max_length=512, primary_key=True)
    site_info = fields.JSONField(default={})
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = f"{table_prefix}site_info"

    async def update(self, info: dict):
        timestamp = datetime.now(UTC)
        await type(self).update_or_create(
            api_link=self.api_link,
            defaults={"site_info": info, "timestamp": timestamp},
        )
        self.site_info = deepcopy(info)
        self.timestamp = timestamp
        return True

    @classmethod
    async def get_like_this(cls, t: str):
        return await (cls.filter(api_link__contains=t)).first()


class WikiBotAccountList(DBModel):
    """
    Wiki Bot 账号列表。

    :param api_link: API 链接
    :param bot_account: Bot 账号
    :param bot_password: Bot 密码
    """

    api_link = fields.CharField(max_length=512, primary_key=True)
    bot_account = fields.CharField(max_length=512)
    bot_password = fields.CharField(max_length=512)

    class Meta:
        table = f"{table_prefix}bot_account_list"

    @classmethod
    async def add(cls, api_link: str, bot_account: str, bot_password: str):
        _, created = await cls.get_or_create(
            api_link=api_link,
            defaults={"bot_account": bot_account, "bot_password": bot_password},
        )
        return created

    @classmethod
    async def remove(cls, api_link):
        return bool(await cls.filter(api_link=api_link).delete())


# WikiLog 的表名沿用合并前的模块前缀，既有数据库无需迁移。
wikilog_table_prefix = "module_wikilog_"


class WikiLogTargetSetInfo(DBModel):
    union_scope = UNION_SCOPE_TARGET
    union_id = fields.CharField(max_length=512, primary_key=True)
    infos = fields.JSONField(default={})

    class Meta:
        table = f"{wikilog_table_prefix}target_set_info"

    async def _mutate_infos(self, mutation) -> bool:
        """锁住所属 Union 与模块行后，基于最新的嵌套配置执行修改。"""
        async with union_mutation():
            async with in_transaction("default") as connection:
                target = await (
                    TargetUnionInfo.filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not target:
                    return False

                current = await (
                    type(self).filter(union_id=self.union_id).using_db(connection).select_for_update().first()
                )
                if not current:
                    return False

                infos = deepcopy(current.infos or {})
                if not mutation(infos):
                    return False
                await type(self).filter(union_id=self.union_id).using_db(connection).update(infos=infos)
                self.infos = deepcopy(infos)
                return True

    async def conf_wiki(self, api_link: str, add=False, reset=False):
        def mutate(infos):
            if add or reset:
                if api_link in infos and not reset:
                    return False
                infos[api_link] = {}
                infos[api_link].setdefault("AbuseLog", {"enable": False, "filters": ["*"]})
                infos[api_link].setdefault(
                    "RecentChanges",
                    {"enable": False, "filters": ["*"], "rcshow": ["!bot"]},
                )
                infos[api_link].setdefault("use_bot", False)
                infos[api_link].setdefault("keep_alive", False)
                infos[api_link].setdefault("note", "")
                return True
            if api_link not in infos:
                return False
            del infos[api_link]
            return True

        return await self._mutate_infos(mutate)

    async def conf_log(self, api_link: str, log_name: str, enable=False):
        def mutate(infos):
            if api_link not in infos or log_name not in infos[api_link]:
                return False
            infos[api_link][log_name]["enable"] = enable
            return True

        return await self._mutate_infos(mutate)

    async def set_filters(self, api_link: str, log_name: str, filters: list[str]):
        def mutate(infos):
            if api_link not in infos or log_name not in infos[api_link]:
                return False
            infos[api_link][log_name]["filters"] = list(filters)
            return True

        return await self._mutate_infos(mutate)

    async def get_filters(self, api_link: str, log_name: str):
        infos = self.infos
        if api_link in infos:
            if log_name in infos[api_link]:
                return infos[api_link][log_name].get("filters")
        return []

    async def set_rcshow(self, api_link: str, rcshow: list[str]):
        def mutate(infos):
            if api_link not in infos or "RecentChanges" not in infos[api_link]:
                return False
            infos[api_link]["RecentChanges"]["rcshow"] = list(rcshow)
            return True

        return await self._mutate_infos(mutate)

    async def get_rcshow(self, api_link: str):
        infos = self.infos
        if api_link in infos:
            if "RecentChanges" in infos[api_link]:
                return infos[api_link]["RecentChanges"].get("rcshow")
        return []

    async def set_use_bot(self, api_link: str, use_bot: bool):
        def mutate(infos):
            if api_link not in infos:
                return False
            infos[api_link]["use_bot"] = use_bot
            return True

        return await self._mutate_infos(mutate)

    async def get_use_bot(self, api_link: str):
        infos = self.infos
        if api_link in infos:
            return infos[api_link].get("use_bot")
        return False

    async def set_keep_alive(self, api_link: str, keep_alive: bool):
        def mutate(infos):
            if api_link not in infos:
                return False
            infos[api_link]["keep_alive"] = keep_alive
            return True

        return await self._mutate_infos(mutate)

    async def get_keep_alive(self, api_link: str):
        infos = self.infos
        if api_link in infos:
            return infos[api_link].get("keep_alive")
        return False

    async def conf_note(self, api_link: str, note: str):
        def mutate(infos):
            if api_link not in infos:
                return False
            infos[api_link]["note"] = note
            return True

        return await self._mutate_infos(mutate)

    @classmethod
    async def return_all_data(cls):
        """
        返回全部配置，键为场景 union ID（推送时需展开为该 union 下的全部平台场景 ID）。
        """
        all_data = await cls.all()
        data_d = {x.union_id: x.infos for x in all_data}
        return data_d
