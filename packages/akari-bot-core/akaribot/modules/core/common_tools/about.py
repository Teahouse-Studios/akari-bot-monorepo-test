from pathlib import Path

from akaribot.core.utils.platform_scope import platform_name_of
from akaribot.core.api import find_brand_asset
from akaribot.core.builtins.bot import Bot
from akaribot.core.builtins.message.chain import MessageChain
from akaribot.core.builtins.message.elements import ButtonRows
from akaribot.core.builtins.message.internal import Button, ButtonFrame, I18NContext, Image, Markdown, Plain, Url
from akaribot.core.builtins.utils import command_prefix
from akaribot.core.component import module
from akaribot.core.config.base import CoreConfig
from akaribot.core.logger import Logger

about = module(
    "about",
    base=True,
    doc=True,
    alias={
        "version": "about version",
        "ping": "about ping",
        "status": "about status",
    },
)

CHARACTER_IMAGE_MAX_WIDTH = 512


def read_credits(path: Path | None = None) -> str | None:
    """读取制作人员名单；文件不存在、不可读或内容为空时不展示。

    :param path: 名单文件；缺省按品牌资产顺序查找，两处都没有时为 ``None``。
    :return: 名单正文；取不到时返回 ``None``。
    """
    resolved = find_brand_asset("credits.txt") if path is None else path
    if resolved is None or not resolved.is_file():
        return None
    try:
        return resolved.read_text(encoding="utf-8").strip() or None
    except OSError as e:
        Logger.warning(f"Unable to read credits file {resolved}: {e}")
        return None


def build_credits_message(msg: Bot.MessageSession) -> MessageChain:
    """构造制作人员名单消息。"""
    result = MessageChain.create()
    if not (credits := read_credits()):
        result.append(I18NContext("core.message.about.credits.unavailable"))
        return result

    title = msg.session_info.locale.t("core.message.about.credits")
    result.append(Markdown(f"```{title}\n{credits}\n```", disable_joke=True))
    return result


def build_about_message(msg: Bot.MessageSession) -> MessageChain:
    """根据平台能力构造关于菜单。"""
    locale = msg.session_info.locale
    support_markdown = msg.session_info.support_markdown
    result = MessageChain.create()
    # 品牌资产包缺失（或部署者删掉了图）时跳过配图：少一张图不该让整条 `~about` 失败。
    character = find_brand_asset("character_marked.png")
    if character is not None:
        result.append(Image(character, max_h=CHARACTER_IMAGE_MAX_WIDTH))
    else:
        Logger.warning("Character artwork not found; sending the about menu without it.")

    introduction = locale.t("core.message.about.introduction")
    result.append(Plain(introduction, disable_joke=True))

    credits = read_credits()

    if CoreConfig.repo_url:
        repository_label = locale.t("core.message.about.button.repository")
        if support_markdown and platform_name_of(msg.session_info) == "QQBot":
            result.append(Plain("\n"))
        result.append(Plain(f"{repository_label}：", disable_joke=True))
        result.append(
            Url(
                CoreConfig.repo_url,
                trusted=True,
            )
        )

    links = [
        ("core.message.about.button.issue", CoreConfig.issue_url),
    ]
    if platform_name_of(msg.session_info) == "QQBot" and CoreConfig.qq_test_group_url:
        links.append(("core.message.about.button.qq_group", CoreConfig.qq_test_group_url))
    links.append(("core.message.about.button.donate", CoreConfig.donate_url))
    links = [(label_key, value) for label_key, value in links if value]

    if msg.session_info.support_button:
        rows = []
        if credits:
            rows.append(
                ButtonRows.assign([Button(locale.t("core.message.about.credits"), f"{command_prefix[0]}about credits")])
            )
        for label_key, value in links:
            rows.append(ButtonRows.assign([Button(locale.t(label_key), value)]))
        if rows:
            result.append(ButtonFrame(rows))
    else:
        for label_key, value in links:
            result.append(Plain(f"{locale.t(label_key)}：{value}", disable_joke=True))

    return result


@about.command("{{I18N:core.help.about}}")
async def _(msg: Bot.MessageSession):
    await msg.finish(build_about_message(msg))


@about.command("credits {{I18N:core.help.about.credits}}")
async def _(msg: Bot.MessageSession):
    await msg.finish(build_credits_message(msg))
