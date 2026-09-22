"""更新并重启：更新委托 CLI，重启沿用既有逻辑。

``git pull`` + ``uv sync`` 在拆包后失去意义（实例里装的是分发包，不是仓库工作树，且 uv 该同步的是
实例 venv 而非源码目录），故更新部分与 ``~update`` 共用 :func:`delegate_update`；本模块只保留重启
编排：确认、写重启缓存、触发 :func:`restart`。
"""

import time
import traceback

from akaribot.core.builtins.bot import Bot
from akaribot.core.builtins.message.internal import I18NContext, Plain
from akaribot.core.component import module
from akaribot.core.logger import Logger
from akaribot.core.server.terminate import restart
from akaribot.modules.core.su_tools.restart import restart_time, wait_for_restart, write_restart_cache
from akaribot.modules.core.su_tools.update import delegate_update, format_update_report

upds = module(
    "update&restart",
    required_superuser=True,
    alias="u&r",
    base=True,
    doc=True,
    exclude_from=["Web"],
    load=Bot.Info.subprocess,
)


@upds.command(
    "[--force] {{I18N:core.help.update&restart}}",
    options_desc={"--force": "{I18N:core.help.update&restart.option.force}"},
)
async def _(msg: Bot.MessageSession, force: bool = False):
    if Bot.Info.binary_mode:
        await msg.finish(I18NContext("core.message.update.binary_mode"))
    if force:
        await msg.send_message(I18NContext("core.message.restart.restarting"))
    else:
        try:
            if not await msg.wait_confirm(append_instruction=False):
                await msg.finish()
            else:
                if not restart_time:
                    restart_time.append(time.time())
                await wait_for_restart(msg)
        except Exception:
            Logger.critical("Failed to send restart confirmation message, perhaps bug? Force restart...")
            Logger.critical(traceback.format_exc())
    try:
        restart_time.append(time.time())
        write_restart_cache(msg)
    except Exception:
        Logger.critical("Failed to write restart info cache, perhaps bug? Continue...")
        Logger.critical(traceback.format_exc())
    try:
        outcome = await delegate_update(force=force)
        await msg.send_message(Plain(format_update_report(outcome), disable_joke=True))
    except Exception:
        Logger.critical("Failed to send update result message, perhaps bug? Continue...")
        Logger.critical(traceback.format_exc())
    await restart()
