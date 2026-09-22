from copy import deepcopy

from attrs import define, field

from akaribot.core.utils.platform_scope import platform_scope, scope_allows
from .component_meta import *


@define
class BaseMatches:
    set: list[ModuleMeta] = field(factory=list)

    def add(self, meta):
        self.set.append(meta)
        return self.set

    @classmethod
    def init(cls):
        return deepcopy(cls())


@define
class CommandMatches(BaseMatches):
    set: list[CommandMeta] = field(factory=list)

    def get(
        self,
        target_from: str | None = None,
        client_name: str | None = None,
        platform_from: str | None = None,
        platform_name: str | None = None,
        show_required_superuser: bool = False,
        show_required_base_superuser: bool = False,
        show_required_admin: bool = True,
    ) -> list[CommandMeta]:
        metas = []
        for meta in self.set:
            if not show_required_base_superuser and meta.required_base_superuser:
                continue
            if not show_required_superuser and meta.required_superuser:
                continue
            if not show_required_admin and meta.required_admin:
                continue
            if not meta.load:
                continue
            if target_from:
                if not scope_allows(
                    platform_scope(target_from, client_name, platform_from, platform_name),
                    meta.available_for,
                    meta.exclude_from,
                ):
                    continue
            metas.append(meta)
        return metas


@define
class RegexMatches(BaseMatches):
    set: list[RegexMeta] = field(factory=list)

    def get(
        self,
        target_from: str | None = None,
        client_name: str | None = None,
        platform_from: str | None = None,
        platform_name: str | None = None,
        show_required_superuser: bool = False,
        show_required_base_superuser: bool = False,
        show_required_admin: bool = True,
    ) -> list[RegexMeta]:
        metas = []
        for meta in self.set:
            if not show_required_base_superuser and meta.required_base_superuser:
                continue
            if not show_required_superuser and meta.required_superuser:
                continue
            if not show_required_admin and meta.required_admin:
                continue
            if not meta.load:
                continue
            if target_from:
                if not scope_allows(
                    platform_scope(target_from, client_name, platform_from, platform_name),
                    meta.available_for,
                    meta.exclude_from,
                ):
                    continue
            metas.append(meta)
        return metas


@define
class ScheduleMatches(BaseMatches):
    set: list[ScheduleMeta] = field(factory=list)


@define
class HookMatches(BaseMatches):
    set: list[HookMeta] = field(factory=list)


@define
class EventMatches(BaseMatches):
    set: list[EventMeta] = field(factory=list)

    def get(
        self,
        target_from: str | None = None,
        client_name: str | None = None,
        platform_from: str | None = None,
        platform_name: str | None = None,
    ) -> list[EventMeta]:
        metas = []
        for meta in self.set:
            if not meta.load:
                continue
            if target_from:
                if not scope_allows(
                    platform_scope(target_from, client_name, platform_from, platform_name),
                    meta.available_for,
                    meta.exclude_from,
                ):
                    continue
            metas.append(meta)
        return metas


__all__ = ["CommandMatches", "RegexMatches", "ScheduleMatches", "HookMatches", "EventMatches"]
