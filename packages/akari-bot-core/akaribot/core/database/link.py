from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from akaribot.core.config.base import CoreSecretConfig
from akaribot.core.constants import database_path
from akaribot.core.paths import Paths

SQLITE_CONNECTION_DEFAULTS = {
    # Tortoise 按参数顺序执行 PRAGMA。先延长锁等待时间，再尝试切换 WAL，
    # 避免多个进程并发启动时 journal_mode 尚未受到 30 秒等待策略保护。
    "busy_timeout": "30000",
    "journal_mode": "WAL",
}


def _is_absolute_target(target: str) -> bool:
    """链接中的目标文件是否按绝对路径给出。

    路径可能照抄自 Windows 配置，``Path`` 在其它平台上判不出盘符与反斜杠开头的写法，
    故按字面补判，免得把绝对路径锚到实例根。

    :param target: 链接中 ``://`` 之后、查询串之前的路径部分。
    :return: 绝对路径为 ``True``。
    """
    if Path(target).is_absolute() or target.startswith(("/", "\\")):
        return True
    return len(target) > 1 and target[1] == ":"


def _resolve_sqlite_path(link: str) -> Path | None:
    """解析 SQLite 链接指向的数据库文件，相对路径锚定到实例根。

    默认链接是 ``sqlite://database/save.db`` 这样的相对路径，驱动按进程 cwd 解析它，
    从实例外启动的入口因此会把库建到调用目录。实例内的相对路径一律以
    :class:`akaribot.core.paths.Paths` 记录的实例根为基准，与 ``AKARI_INSTANCE_DIR`` 一致。

    :param link: 数据库链接。
    :return: 数据库文件路径；非 SQLite 链接与 ``:memory:`` 等无文件链接为 ``None``。
    """
    parts = link.split("://", 1)
    if len(parts) < 2 or parts[0].split("+")[0] != "sqlite":
        return None
    target = parts[1].partition("?")[0]
    if not target or target == ":memory:":
        return None
    if _is_absolute_target(target):
        return Path(target)
    return Paths.instance / target


def _anchor_sqlite_link(link: str) -> str:
    """把 SQLite 链接里的相对文件路径改写为实例根下的绝对路径。

    :param link: 数据库链接。
    :return: 改写后的链接；无需改写时为原值。
    """
    resolved = _resolve_sqlite_path(link)
    if resolved is None:
        return link
    prefix, remainder = link.split("://", 1)
    _, separator, query = remainder.partition("?")
    return f"{prefix}://{resolved.as_posix()}{separator}{query}"


db_link = CoreSecretConfig.db_path
db_parts = db_link.split("://")
db_type = db_parts[0].split("+")[0] if db_parts else "sqlite"
db_path = database_path

_sqlite_file = _resolve_sqlite_path(db_link)
if _sqlite_file is not None:
    db_path = _sqlite_file.parent
# 内存库没有文件可建，保持不预建目录的既有行为；其余后端先建好目录，驱动不会代建。
if _sqlite_file is not None or db_type != "sqlite":
    db_path.mkdir(parents=True, exist_ok=True)


def prepare_db_link(link: str) -> str:
    parts = link.split("://", 1)
    link_type = parts[0].split("+")[0] if parts else "sqlite"
    normalized_link = f"{link_type}://{parts[1]}" if len(parts) > 1 else link
    if link_type != "sqlite":
        return normalized_link

    normalized_link = _anchor_sqlite_link(normalized_link)
    parsed = urlsplit(normalized_link)
    query = parse_qsl(parsed.query, keep_blank_values=True)
    existing_fields = {key.lower() for key, _ in query}
    query.extend((key, value) for key, value in SQLITE_CONNECTION_DEFAULTS.items() if key not in existing_fields)
    # busy_timeout 必须在可能取得写锁的 PRAGMA（尤其 journal_mode）之前生效；
    # 即使调用方显式提供了参数并采用其它排列，也统一提前执行等待策略。
    query.sort(key=lambda item: item[0].lower() != "busy_timeout")
    return urlunsplit(parsed._replace(query=urlencode(query)))


def get_db_link():
    return prepare_db_link(db_link)
