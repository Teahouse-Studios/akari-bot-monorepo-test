from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from akaribot.core.config.base import CoreSecretConfig
from akaribot.core.constants import database_path
from akaribot.core.paths import Paths

SQLITE_CONNECTION_DEFAULTS = {
    # Tortoise 按照参数顺序执行 PRAGMA。先延长锁等待时间，再尝试切换至 WAL 模式，
    # 避免多个进程并发启动时 journal_mode 尚未获得 30 秒等待策略的保护。
    "busy_timeout": "30000",
    "journal_mode": "WAL",
}


def _is_absolute_target(target: str) -> bool:
    # 路径可能直接复制自 Windows 配置，``Path`` 在其他平台上无法识别盘符与反斜杠开头的写法，
    # 因此按字面补充判断，以免把绝对路径误判定为相对实例根目录。
    if Path(target).is_absolute() or target.startswith(("/", "\\")):
        return True
    return len(target) > 1 and target[1] == ":"


def _resolve_sqlite_path(link: str) -> Path | None:
    # 默认连接为 ``sqlite://database/save.db`` 等相对路径，驱动默认按进程工作目录解析，
    # 导致从实例外部启动时将数据库创建至调用目录。实例内的相对路径统一以
    # :class:`akaribot.core.paths.Paths` 记录的实例根目录为基准，与 ``AKARI_INSTANCE_DIR`` 保持一致。
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
# 内存数据库无需创建文件，因此不预先创建目录。其他后端预先创建目录，驱动本身不负责自动创建。
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
    # busy_timeout 必须在可能获取写锁的 PRAGMA（尤其是 journal_mode）生效前执行。
    # 即使调用方显式提供了参数并采用其他顺序，亦统一优先执行等待策略。
    query.sort(key=lambda item: item[0].lower() != "busy_timeout")
    return urlunsplit(parsed._replace(query=urlencode(query)))


def get_db_link():
    return prepare_db_link(db_link)
