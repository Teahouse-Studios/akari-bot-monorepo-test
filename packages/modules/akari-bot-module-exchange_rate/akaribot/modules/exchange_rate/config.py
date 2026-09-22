from akaribot.core.api import on_module_config


@on_module_config("exchange_rate", secret=True)
class ExchangeRateConfig:
    exchange_rate_api_key: str = ""
