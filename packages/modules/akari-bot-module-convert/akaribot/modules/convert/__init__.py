from decimal import Decimal

from pint import UnitRegistry

from akaribot.core.api import Bot, I18NContext, module

ureg = UnitRegistry(non_int_type=Decimal)
i = module(
    "convert",
    alias=["conv", "unit"],
    desc="{I18N:convert.help.desc}",
    doc=True,
    support_languages=["en_us"],
)


@i.command("<from_val> <to_unit> {{I18N:convert.help}}")
async def _(msg: Bot.MessageSession, from_val: str, to_unit: str):
    try:
        ori = ureg.parse_expression(from_val)
        res = ureg.parse_expression(from_val).to(to_unit)
    except Exception:
        await msg.finish(I18NContext("convert.message.invalid"))

    await msg.finish(f"{ori:~Pg} = {res:~Pg}")
