"""出站网络请求使用的代理与 TLS 校验设置。"""

from akaribot.core.config.core import CoreConfig, CoreSecretConfig

# 各 SDK 的代理参数均以 None 表示直接连接，配置未填写时获取到的值为空字符串。
proxy = CoreSecretConfig.proxy or None
ssl_verify = not CoreConfig.proxy_disable_ssl

__all__ = ["proxy", "ssl_verify"]
