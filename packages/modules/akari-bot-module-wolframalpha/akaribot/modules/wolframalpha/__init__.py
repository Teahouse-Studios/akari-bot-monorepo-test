import urllib.parse

from PIL import Image as PILImage

from akaribot.core.api import (
    Bot,
    I18NContext,
    Image as BImage,
    module,
    ConfigValueError,
    ExternalException,
    rickroll,
    download,
    get_url,
)
from akaribot.modules.wolframalpha.config import WolframalphaConfig
from .check import secret_check

appid = WolframalphaConfig.wolfram_alpha_appid

w = module(
    "wolframalpha",
    alias=["wolfram", "wa"],
    desc="{I18N:wolframalpha.help.desc}",
    support_languages=["en_us"],
    doc=True,
)


@w.command("<query> {{I18N:wolframalpha.help}}")
async def _(msg: Bot.MessageSession, query: str):
    if await secret_check(query):
        await msg.finish(rickroll())
    url_query = urllib.parse.quote(query)
    if not appid:
        raise ConfigValueError("{I18N:error.config.secret.not_found}")
    url = f"http://api.wolframalpha.com/v1/simple?appid={appid}&i={url_query}&units=metric"

    try:
        img_path = await download(url, status_code=200)
        if img_path:
            with PILImage.open(img_path) as img:
                output = f"{img_path}.png"
                img.save(output, "PNG")
            img_path.unlink()
            await msg.finish([BImage(output)])
    except ExternalException as e:
        if str(e).startswith("501"):
            await msg.finish(I18NContext("wolframalpha.message.incomprehensible"))
        else:
            raise e
    except Exception as e:
        raise e


@w.command("ask <question> {{I18N:wolframalpha.help.ask}}")
async def _(msg: Bot.MessageSession, question: str):
    if await secret_check(question):
        await msg.finish(rickroll())
    url_query = urllib.parse.quote(question)
    if not appid:
        raise ConfigValueError("{I18N:error.config.secret.not_found}")
    url = f"http://api.wolframalpha.com/v1/result?appid={appid}&i={url_query}&units=metric"
    try:
        data = await get_url(url, 200)
        await msg.finish(data)
    except ExternalException as e:
        if str(e).startswith("501"):
            await msg.finish(I18NContext("wolframalpha.message.incomprehensible"))
        else:
            raise e
    except Exception as e:
        raise e
