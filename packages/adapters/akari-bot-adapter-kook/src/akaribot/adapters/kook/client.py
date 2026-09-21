from khl import Bot

from akaribot.adapters.kook.config import KookSecretConfig

token = KookSecretConfig.kook_token

bot = Bot(token=token)
