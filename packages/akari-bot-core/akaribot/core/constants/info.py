import re
from typing import Iterable


class Secret:
    """敏感配置值。"""

    data: set[str] = set()
    ip_address: str | None = None
    ip_country: str | None = None

    @classmethod
    def add(cls, secret: str):
        """加入敏感值。"""
        if secret:
            cls.data.add(secret.upper())

    @classmethod
    def check(cls, text: str) -> str | bool:
        """检查敏感值是否存在。"""
        for secret in cls.data:
            if secret in text.upper():
                return secret
        return False

    @classmethod
    def remove(cls, secret: str):
        """删除敏感值。"""
        if secret and cls.check(secret):
            cls.data.discard(secret.upper())

    @classmethod
    def update(cls, secret: Iterable):
        """替换敏感值。"""
        if secret:
            # union 返回新集合、并不就地修改，此处必须用 update 才能记录批量密钥。
            cls.data.update({s.upper() for s in secret})


class Info:
    """
    机器人信息。

    :param version: 机器人版本。
    :param subprocess: 是否为子进程。
    :param binary_mode: 是否为二进制模式。
    :param command_parsed: 已处理命令数量。
    :param message_parsed: 已处理消息数量。
    :param platform_name: 平台展示名，如 ``Telegram``，同一平台的全部实例共用。
    :param instance_id: 实例 ID，空字符串表示默认实例。
    :param client_name: 客户端名称，由平台展示名与实例 ID 生成。
    :param peer_id: 当前 JobQueue 进程实例 ID。
    :param peer_role: 当前 JobQueue 进程角色。
    :param daemon_pid: 守护进程 PID，由守护进程显式传入，独立运行时为 None。
    :param hub_pid: 内置 JobQueue Hub 子进程 PID，未启用内置 Hub 时为 None。
    :param dirty_word_check: 是否启用文本过滤。
    :param web_render_status: WebRender 状态。
    :param use_url_manager: 是否启用 URLManager。
    :param use_url_md_format: 是否启用 URL Markdown 格式。
    """

    version = None
    subprocess = False
    binary_mode = False
    command_parsed = 0
    message_parsed = 0
    platform_name = ""
    # 空字符串表示默认实例。非空时必须匹配 INSTANCE_ID_PATTERN。
    instance_id = ""
    client_name = ""
    # JobQueue 运行实例 ID 在每次进程启动时均不相同。client_name 仍表示可竞争处理任务的服务组。
    peer_id = ""
    peer_role = ""
    # 守护进程与内置 Hub 非 JobQueue 节点，其 PID 必须由守护进程在启动时显式传入。
    daemon_pid: int | None = None
    hub_pid: int | None = None
    dirty_word_check = False
    web_render_status = False
    use_url_manager = False
    use_url_md_format = False
    http_mock_enabled = False
    # 启用后，mock 未命中的请求直接失败，不改用真实网络。
    # 使用真实网络会引入重试与超时（默认 3 次 × 20 秒），足以让单个未录制的 URL 拖慢测试逾一分钟。
    http_mock_strict = False

    # 实例 ID 的合法形式。限制字符集是为了让它能安全地拼进 target_id 前缀与配置文件名。
    INSTANCE_ID_PATTERN = re.compile(r"^[a-z0-9_]{1,24}$")

    @classmethod
    def resolve_client_name(cls, platform_name: str, instance_id: str | None = None) -> str:
        """由平台展示名与实例 ID 生成客户端名称。

        分隔符固定为 ``-``：``|`` 是 target_id 的段分隔符，``#`` 在 TOML 中是注释起始符。
        默认实例（实例 ID 为空）必须逐字节保持历史取值 —— target_id 前缀已写入既有的用户
        数据库，任何变动都会让现存部署的场景与用户数据失联。

        :param platform_name: 平台展示名，如 ``Telegram``。
        :param instance_id: 实例 ID，省略时取 ``cls.instance_id``。守护进程枚举各实例身份时
            必须显式传入，该对象本身不是任何实例，其 ``cls.instance_id`` 恒为空。
        :return: 默认实例返回平台展示名本身，否则返回 ``<平台>-<实例 ID>``。
        """
        resolved = cls.instance_id if instance_id is None else instance_id
        if not resolved:
            return platform_name
        return f"{platform_name}-{resolved}"
