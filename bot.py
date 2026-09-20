from core.version import check_python_version  # skipcq

check_python_version()  # noqa

from core.constants import config_path, config_filename  # skipcq

import asyncio
import importlib
import multiprocessing
import os
import shutil
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
from loguru import logger

from core.constants import CONFIG_READONLY_ENV, ascii_art, logs_path  # skipcq
from core.registry import PackageRegistry  # skipcq


AKARI_BOT_I18N_CACHE_DIR = str(Path("./data/i18n_cache/").resolve())

load_dotenv()
os.environ.setdefault("PYTHONIOENCODING", "UTF-8")
os.environ.setdefault("PYTHONPATH", str(Path(".").resolve()))
os.environ.setdefault("AKARI_BOT_I18N_CACHE_DIR", AKARI_BOT_I18N_CACHE_DIR)


def _choose_first_run_locale() -> str:
    """首次运行时询问默认语言。

    完整交互式初始化并入 CLI（阶段 5），此处仅保留语言选择。无终端时（容器、CI）
    直接采用默认语言，不阻塞在 input() 上。

    :return: 语言代码。
    """
    from core.constants import default_locale, lang_list

    if not sys.stdin.isatty():
        return default_locale
    print("Hi, it seems you are first time to run AkariBot, what language do you want to use by default?")
    for index, language in enumerate(lang_list, 1):
        print(f"{index}. {lang_list[language]}")
    while True:
        answer = input("Please input the number of the language you want to use: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(lang_list):
            return list(lang_list)[int(answer) - 1]
        print("Invalid input, please try again.")


def _init_first_run_config() -> None:
    """首次运行时写出配置骨架，其余配置项交给 pre_init() 的模板扫描补全。

    骨架只含 default_locale 与 config_version：这两个顶层键不属于任何模板，扫描补不出来。
    注释先以 i18n 标记落盘，待 pre_init() 接上 i18n 快照后由扫描按所选语言翻译。
    """
    from core.constants import config_version

    locale = _choose_first_run_locale()
    config_path.mkdir(parents=True, exist_ok=True)
    (config_path / config_filename).write_text(
        "# {I18N:config.header.line.1}\n"
        "# {I18N:config.header.line.2}\n"
        "# {I18N:config.header.line.3}\n"
        "\n"
        f'default_locale = "{locale}" # {{I18N:config.comments.default_locale}}\n'
        f"config_version = {config_version} # {{I18N:config.comments.config_version}}\n",
        encoding="utf-8",
    )
    print(f'Config skeleton generated at "{config_path}", it will be completed on this startup.')


if not (config_path / config_filename).exists():
    _init_first_run_config()


Logger = logger.bind(name="BotDaemon")

logger_format = (
    "<cyan>[BotDaemon]</cyan>"
    "<yellow>[{name}:{function}:{line}]</yellow>"
    "<green>[{time:YYYY-MM-DD HH:mm:ss}]</green>"
    "<level>[{level}]:{message}</level>"
)
_daemon_logger_initialized = False


def _is_daemon_log(record):
    """守护进程自身及尚未重命名的核心日志均写入 BotDaemon。"""
    return record["extra"].get("name") in {None, "BotDaemon"}


def init_daemon_logger():
    """仅为守护进程与短生命周期 pre-init 进程安装日志处理器。"""
    global _daemon_logger_initialized
    if _daemon_logger_initialized:
        return
    try:
        logger.remove(0)
    except ValueError:
        pass
    Logger.add(
        sys.stdout,
        format=logger_format,
        colorize=True,
        filter=_is_daemon_log,
    )
    Logger.add(
        sink=logs_path / "BotDaemon_debug_{time:YYYY-MM-DD}.log",
        format=logger_format,
        rotation="00:00",
        retention="1 day",
        level="DEBUG",
        filter=lambda record: record["level"].name == "DEBUG" and _is_daemon_log(record),
        encoding="utf8",
    )
    Logger.add(
        sink=logs_path / "BotDaemon_{time:YYYY-MM-DD}.log",
        format=logger_format,
        rotation="00:00",
        retention="10 days",
        level="INFO",
        encoding="utf8",
        filter=_is_daemon_log,
    )
    _daemon_logger_initialized = True


class RestartBot(Exception):
    pass


failed_to_start_attempts = {}
disabled_bots = []
processes: list[multiprocessing.Process] = []
server_stop_event = None
jobqueue_hub_stop_event = None


def warn_if_database_jobqueue_uses_sqlite(jobqueue_backend: object, database_type: object) -> bool:
    """数据库队列与 SQLite 组合使用时输出一次非阻断警告。"""
    if not isinstance(jobqueue_backend, str) or jobqueue_backend.strip().lower() != "database":
        return False
    if not isinstance(database_type, str) or database_type.strip().lower() != "sqlite":
        return False
    Logger.warning(
        "JobQueue is using the database backend with SQLite. SQLite permits only one concurrent writer; "
        "JobQueue delivery, claim, heartbeat, response, and cleanup writes will contend with application data "
        'and may cause "database is locked" errors under load. Set [jobqueue].jobqueue_backend = "websocket" '
        "in config/jobqueue.toml to move JobQueue traffic off SQLite."
    )
    return True


@dataclass(frozen=True)
class AdapterInstance:
    """一个待启动的适配器实例。

    :param platform: 适配器名（entry point 名），如 ``telegram``。
    :param instance_id: 实例 ID；空串表示默认实例。
    :param client_name: 客户端名称，如 ``Telegram`` / ``Telegram-alt``。
    :param table: 该实例的配置表名，如 ``bot_telegram-alt``。
    :param replicas: 同一身份的副本数，供「同一身份多副本」使用；当前恒为 1。
    """

    platform: str
    instance_id: str
    client_name: str
    table: str
    replicas: int = 1


def adapter_platform_name(platform: str) -> str:
    """读取适配器声明的平台展示名。

    ``bots/<platform>/info.py`` 的 ``platform_name`` 是唯一真源，不能从目录名推：``onebot``
    的平台名是 ``QQ``。早于本功能发布的适配器没有该变量，回退到它当时使用的 ``client_name``
    （默认实例下两者相同）；多实例能力则要求适配器同步升级。

    :param platform: 适配器名。
    :return: 平台展示名；无法确定时为空串，调用方应跳过该实例。
    """
    try:
        info = importlib.import_module(f"bots.{platform}.info")
    except Exception:
        Logger.exception(f"Failed to import bots.{platform}.info, skip to launch.")
        return ""
    platform_name = getattr(info, "platform_name", "")
    if platform_name:
        return str(platform_name)
    legacy_name = getattr(info, "client_name", "")
    if legacy_name:
        Logger.warning(
            f"Adapter {platform} does not declare platform_name, falling back to client_name {legacy_name!r}. "
            "Multi-instance support requires the adapter to be updated."
        )
        return str(legacy_name)
    return ""


def discover_adapter_instances() -> list[AdapterInstance]:
    """枚举全部已启用的适配器实例。

    以配置中的 ``bot_*`` 表为索引：表名去前缀后按第一个 ``-`` 拆成 ``(适配器, 实例 ID)``，与已
    安装的适配器核对，再读该表自己的 ``enable``。孤立配置与非法实例 ID 只告警跳过，不中止启动。

    ``enable`` 不回退到基表，否则「新建一个实例文件」等同于「立即上线一个机器人」。

    :return: 已启用的实例，按 ``(适配器, 实例 ID)`` 排序。
    """
    from core.config import CFGManager
    from core.constants import Info

    adapters = PackageRegistry.adapters()
    enabled: list[AdapterInstance] = []
    for table in sorted(CFGManager.values):
        if not table.startswith("bot_") or table.endswith("_secret"):
            continue
        name = table[4:]
        platform, _, instance_id = name.partition("-")
        if not platform:
            Logger.warning(f'Config table "{table}" has an empty adapter name, skip to launch.')
            continue
        if instance_id and not Info.INSTANCE_ID_PATTERN.fullmatch(instance_id):
            Logger.warning(
                f'Config table "{table}" has an invalid instance id "{instance_id}": '
                "it must match [a-z0-9_]{1,24}, skip to launch."
            )
            continue
        if platform not in adapters:
            Logger.warning(f"Bot {name} has config but no adapter is installed, skip to launch.")
            continue
        platform_name = adapter_platform_name(platform)
        if not platform_name:
            Logger.warning(f"Adapter {platform} does not declare a platform name, skip to launch.")
            continue
        if not CFGManager.has("enable", table_name=table):
            Logger.warning(f'Bot {name} cannot found config "enable".')
            disabled_bots.append(name)
            continue
        if not CFGManager.get("enable", table_name=table, _fallback=False):
            Logger.warning(f"Bot {name} is disabled in config, skip to launch.")
            disabled_bots.append(name)
            continue
        enabled.append(
            AdapterInstance(
                platform=platform,
                instance_id=instance_id,
                client_name=Info.resolve_client_name(platform_name, instance_id),
                table=table,
            )
        )
    return enabled


# 监听地址字段。web 的 web_port 与 onebot / milky 的 qq_host 最终都占用一个 TCP 端口，
# 故统一解析出 (主机, 端口) 后比对：web 与 onebot 撞同一个端口同样是致命的。
INSTANCE_LISTEN_FIELDS = ("web_port", "qq_host")

# web_host 缺省时的绑定地址，与 WebConfig 声明的默认值一致。守护进程不能向 CFGManager.get
# 传默认值：那会触发写入，而守护进程是只读的。
DEFAULT_WEB_HOST = "127.0.0.1"


def _split_host_port(value: object) -> tuple[str, int] | None:
    """从监听配置中解析出 ``(主机, 端口)``。

    :param value: 配置值，可能是 ``6485``、``"127.0.0.1:8080"`` 或 ``"http://127.0.0.1:8080"``。
    :return: 主机（小写，可能为空串）与端口；解析不出或端口越界时返回 None。
    """
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        host, port = "", value
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if "://" in text:
            try:
                parsed = urlsplit(text)
                host, port = parsed.hostname or "", parsed.port
            except ValueError:
                return None
        else:
            host, _, tail = text.rpartition(":")
            if not tail.isdigit():
                return None
            port = int(tail)
    else:
        return None
    if port is None or not 0 < port < 65536:
        return None
    return host.lower(), port


def _hosts_conflict(left: str, right: str) -> bool:
    """判断两个监听主机是否会争用同一个端口。

    通配地址与任意主机冲突，其余要求主机相同。``localhost`` 与 ``127.0.0.1`` 视为不同：
    宁可漏报也不误报，误报会让本来可用的部署起不来。

    :param left: 主机一。
    :param right: 主机二。
    :return: 是否争用。
    """
    wildcard = {"", "*", "0.0.0.0", "::", "[::]"}
    return left in wildcard or right in wildcard or left == right


def _listen_resources(instance: AdapterInstance) -> list[tuple[str, int, str]]:
    """收集实例占用的 ``(主机, 端口, 字段名)``。

    ``qq_host`` 在 onebot 是反向 WS 的绑定地址、在 milky 是所连 Milky 服务的目标地址，
    取值形式统一按 ``host:port`` 或 URL 解析；``web_port`` 的绑定主机取自 ``web_host``。

    :param instance: 实例。
    :return: 资源列表。
    """
    from core.config import CFGManager

    resources: list[tuple[str, int, str]] = []
    web = _split_host_port(CFGManager.get("web_port", table_name=instance.table))
    if web is not None:
        host, port = web
        if not host:
            host = str(CFGManager.get("web_host", table_name=instance.table) or DEFAULT_WEB_HOST).lower()
        resources.append((host, port, "web_port"))
    qq = _split_host_port(CFGManager.get("qq_host", table_name=instance.table))
    if qq is not None:
        host, port = qq
        resources.append((host, port, "qq_host"))
    return resources


def _read_credential(instance: AdapterInstance, field: str) -> object:
    """读取实例的某个凭据字段。

    凭据多数落在密钥表，也有落在普通表的（如 ``qq_bot_appid``），两处都试一次。
    未填写的占位符由 ``CFGManager.get`` 归一为 None，不会被误判为重复。

    :param instance: 实例。
    :param field: 凭据字段名。
    :return: 凭据值；两处都没有时返回 None。
    """
    from core.config import CFGManager

    for secret in (True, False):
        value = CFGManager.get(field, secret=secret, table_name=instance.table)
        if value:
            return value
    return None


def check_instance_conflicts(instances: list[AdapterInstance]) -> None:
    """spawn 之前拦截多实例误配。

    端口冲突与同平台凭据重复的症状都是「两个进程抢同一份资源」：前者抢套接字，后者抢账号。
    这类故障从日志几乎诊断不出来，故一律以 ``sys.exit(1)`` 中止启动，并指名道姓是哪两个实例。

    :param instances: 已启用的实例。
    """
    listeners: dict[int, list[tuple[str, AdapterInstance, str]]] = {}
    for instance in instances:
        for host, port, field in _listen_resources(instance):
            for other_host, other, other_field in listeners.get(port, []):
                if not _hosts_conflict(host, other_host):
                    continue
                Logger.critical(
                    f"Instances {other.client_name} ({other.table}.{other_field}) and {instance.client_name} "
                    f"({instance.table}.{field}) are configured to use the same port {port}. "
                    "Two processes cannot bind the same port, aborting."
                )
                sys.exit(1)
            listeners.setdefault(port, []).append((host, instance, field))

    by_platform: dict[str, list[AdapterInstance]] = {}
    for instance in instances:
        by_platform.setdefault(instance.platform, []).append(instance)
    adapters = PackageRegistry.adapters()
    for platform in sorted(by_platform):
        group = by_platform[platform]
        entry = adapters.get(platform)
        if len(group) < 2 or entry is None:
            continue
        for field in entry.manifest.credential_fields:
            owners: dict[str, AdapterInstance] = {}
            for instance in group:
                value = _read_credential(instance, field)
                if not value:
                    continue
                key = str(value)
                if key in owners:
                    owner = owners[key]
                    Logger.critical(
                        f"Instances {owner.client_name} ({owner.table}) and {instance.client_name} "
                        f"({instance.table}) are configured with the same {field!r}, which would make both "
                        "processes log in as the same account. Aborting."
                    )
                    sys.exit(1)
                owners[key] = instance

    seen_client_names: dict[str, AdapterInstance] = {}
    for instance in instances:
        other = seen_client_names.setdefault(instance.client_name, instance)
        if other is not instance:
            # onebot 与 milky 都叫 "QQ"。这不是本功能引入的，但两者的 JobQueue 服务名与启动
            # 失败计数会因此合并，必须留下痕迹。
            Logger.warning(
                f"Instances {other.table} and {instance.table} share client_name {instance.client_name!r}; "
                "their JobQueue services and start-failure counters cannot be told apart."
            )


def pre_init():
    init_daemon_logger()
    Logger.info(ascii_art)
    Logger.info("Akaribot is launching...")
    from tortoise import run_async

    from core.constants import PrivateData, cache_path, lang_list
    from core.i18n import build_locale_snapshot, collect_locale_paths, connect_locale_snapshot
    from core.paths import Paths

    # 目录创建集中在此：导入 core.constants 不再产生副作用。
    Paths.ensure("data", "cache", "logs", "database")
    PrivateData.ensure()
    if cache_path.exists():
        shutil.rmtree(cache_path)
    cache_path.mkdir(parents=True, exist_ok=True)

    Logger.info("Loading i18n...")
    locale_loaded_err = build_locale_snapshot(list(lang_list.keys()), collect_locale_paths(), "akari-bot")
    connect_locale_snapshot("akari-bot")
    if locale_loaded_err:
        Logger.warning(f"I18N loaded with errors: {locale_loaded_err}")

    Logger.info("Generating config...")

    # CoreConfig 的导入须留在函数内：multiprocessing 以 spawn / forkserver 启动子进程时
    # 会以 __mp_main__ 重新导入主模块，置于顶层将使每个子进程再次触发配置模板的生成。
    from core.config.core import CoreConfig
    from core.config.jobqueue import bootstrap_jobqueue_config, JobQueueConfig
    from core.config.scan import scan_config_templates
    from core.constants.version import database_version
    from core.database import close_db, init_db
    from core.database.link import db_type
    from core.database.models import SenderUnionInfo, DBVersion

    # 配置的生成集中在此完成：子进程一律只读，此处遗漏的键将在子进程读取时抛出异常，
    # 因此任何模板加载失败均须中止启动，而非延至运行期才暴露。
    failed_templates = scan_config_templates()
    if failed_templates:
        Logger.critical(f"Failed to load config templates: {failed_templates}. Aborting.")
        sys.exit(1)

    generated_jobqueue_fields = bootstrap_jobqueue_config()
    if generated_jobqueue_fields:
        Logger.info("Generated and saved missing JobQueue configuration values.")

    warn_if_database_jobqueue_uses_sqlite(JobQueueConfig.jobqueue_backend, db_type)

    if CoreConfig.debug:
        Logger.debug("Debug mode is enabled.")

    async def update_db():
        Logger.info("Checking database...")
        if not await init_db(generate_schemas=True):
            raise RuntimeError("Failed to initialize database schemas during pre-init.")

        Logger.info("Verifying database version...")

        query_dbver = await DBVersion.all().first()
        if not query_dbver:
            Logger.warning("Database version not found, converting old database...")
            from core.scripts.convert_database import convert_database

            await close_db()
            await convert_database()
            Logger.success("Database converted successfully!")
        elif query_dbver.version < database_version:
            Logger.info(f"Updating database from {query_dbver.version} to {database_version}...")
            from core.database.update import update_database

            await close_db()
            await update_database()
            Logger.success("Database updated successfully!")
        else:
            await close_db()

        Logger.success("Database check completed successfully!")

        Logger.info("Granting base superuser permission...")
        base_superuser = CoreConfig.base_superuser
        if base_superuser:
            if isinstance(base_superuser, str):
                base_superuser = [base_superuser]
            if not await init_db(load_module_db=False):
                raise RuntimeError("Failed to initialize database while granting base superuser permission.")
            for bu in base_superuser:
                sender_info = await SenderUnionInfo.resolve_union(bu)
                await sender_info.edit_attr("superuser", True)
            await close_db()
            Logger.success("Base superuser permission granted successfully!")
        else:
            Logger.warning("The base superuser is not found, please setup it in the config file.")

    run_async(update_db())
    Logger.success("Pre-init completed successfully!")


def multiprocess_run_until_complete(func):
    mp = multiprocessing.get_context("spawn" if sys.platform in ["win32", "darwin"] else "forkserver")
    # pre_init 是唯一被允许写入配置的进程，须清除 RestartBot 重启循环中残留的只读标记
    os.environ.pop(CONFIG_READONLY_ENV, None)
    p = mp.Process(target=func, daemon=True)
    p.start()

    while True:
        if not p.is_alive():
            break
        time.sleep(1)
    # Process.close() 之后再访问 exitcode 会抛 ValueError，故须在 terminate_process 之前取值
    exitcode = p.exitcode
    terminate_process(p)
    if exitcode != 0:
        Logger.critical(f"Pre-init failed with exit code {exitcode}, aborting.")
        sys.exit(exitcode)


def go(bot_name: str, subprocess: bool = False, binary_mode: bool = False, instance_id: str = ""):
    from core.constants import Info
    from core.logger import Logger

    # instance_id 必须在导入适配器之前置位：bots.<x>.info 在导入期依它派生 client_name。
    Info.instance_id = instance_id
    Info.subprocess = subprocess
    Info.binary_mode = binary_mode

    platform_name = adapter_platform_name(bot_name)
    if not platform_name:
        Logger.critical(f"[{bot_name}] ???, adapter info not found.")
        sys.exit(1)
    # 平台展示名供会话构造使用：多实例下 client_name 带实例后缀，平台名不带。
    Info.platform_name = platform_name
    client_name = Info.resolve_client_name(platform_name)
    Logger.info(f"[{client_name}] Here we go!")

    try:
        importlib.import_module(f"bots.{bot_name}.bot")
    except ModuleNotFoundError:
        # 退出码 78（EX_CONFIG）表示无需重启：入口缺失是部署问题，重试无济于事。
        Logger.error(f"[{client_name}] ???, entry not found.")
        sys.exit(78)


def server_go(
    stop_event,
    subprocess: bool = False,
    binary_mode: bool = False,
    daemon_pid: int | None = None,
    hub_pid: int | None = None,
):
    # Server 依赖树（尤其 WebRender）只应由 Server 子进程加载，守护进程不需要保留一份。
    from core.server.run import run_async

    run_async(subprocess, binary_mode, stop_event, daemon_pid, hub_pid)


def jobqueue_hub_go(stop_event, ready_event):
    """在独立子进程中运行内置 WebSocket JobQueue Hub。"""
    from core.queue.websocket import run_websocket_hub_process

    run_websocket_hub_process(stop_event, ready_event)


binary_mode = not sys.argv[0].endswith(".py")


async def run_bot():
    global server_stop_event, jobqueue_hub_stop_event

    # 自此起 spawn 出的子进程一律只读：配置的生成已在 pre_init 中完成。
    # 须在任何 mp.Process 之前置位，spawn 会继承环境；restart_bot_process() 后续重启子进程时同样适用。
    os.environ[CONFIG_READONLY_ENV] = "1"
    os.environ["AKARI_BOT_I18N_CACHE_DIR"] = AKARI_BOT_I18N_CACHE_DIR

    # CONFIG_READONLY_ENV 必须先于 core.config 的首次导入置位；后者会在导入期执行配置版本迁移。
    from core.config.jobqueue import JobQueueConfig

    mp = multiprocessing.get_context("spawn" if sys.platform in ["win32", "darwin"] else "forkserver")
    # 守护进程与 Hub 非 JobQueue Peer，Server 无从 Registry 获知其 PID。此处随 Process
    # 参数传递而非环境变量：forkserver 于首个子进程启动时快照环境，后续改动不再生效。
    hub_pid = None

    if JobQueueConfig.jobqueue_backend.strip().lower() == "websocket":
        from core.queue.websocket import WebSocketSettings

        websocket_settings = WebSocketSettings.from_config()
    else:
        websocket_settings = None

    if websocket_settings is not None and websocket_settings.embedded:
        jobqueue_hub_stop_event = mp.Event()
        hub_ready_event = mp.Event()
        hub_process = mp.Process(
            target=jobqueue_hub_go,
            args=(jobqueue_hub_stop_event, hub_ready_event),
            name="jobqueue-hub",
            daemon=True,
        )
        hub_process.start()
        processes.append(hub_process)
        hub_ready = await asyncio.to_thread(hub_ready_event.wait, 10)
        if not hub_ready or not hub_process.is_alive():
            exitcode = hub_process.exitcode
            Logger.critical(f"WebSocket JobQueue Hub failed to start, exit code: {exitcode}.")
            terminate_process(hub_process, jobqueue_hub_stop_event)
            processes.remove(hub_process)
            jobqueue_hub_stop_event = None
            raise RuntimeError("Failed to start the WebSocket JobQueue Hub")
        Logger.success("WebSocket JobQueue Hub is ready.")
        hub_pid = hub_process.pid

    def restart_bot_process(instance: AdapterInstance):
        client_name = instance.client_name
        if (
            client_name not in failed_to_start_attempts
            or time.time() - failed_to_start_attempts[client_name]["timestamp"] > 60
        ):
            failed_to_start_attempts[client_name] = {}
            failed_to_start_attempts[client_name]["count"] = 0
            failed_to_start_attempts[client_name]["timestamp"] = time.time()
        failed_to_start_attempts[client_name]["count"] += 1
        failed_to_start_attempts[client_name]["timestamp"] = time.time()
        if failed_to_start_attempts[client_name]["count"] >= 3:
            Logger.error(f"Bot {client_name} failed to start 3 times, abort to restart, please check the log.")
            return

        Logger.warning(f"Restarting bot {client_name}...")
        p = mp.Process(
            target=go,
            args=(
                instance.platform,
                True,
                binary_mode,
                instance.instance_id,
            ),
            name=client_name,
            daemon=True,
        )
        p.akari_instance = instance
        p.start()
        processes.append(p)

    disabled_bots.clear()
    instances = discover_adapter_instances()
    # 误配的实例必须在任何适配器进程启动之前拦下：两个进程抢同一端口或同一账号之后，
    # 症状是随机的消息丢失与重复，从日志无法回溯到配置。
    check_instance_conflicts(instances)

    for instance in instances:
        p = mp.Process(
            target=go,
            args=(instance.platform, True, binary_mode, instance.instance_id),
            name=instance.client_name,
            daemon=True,
        )
        # client_name 不保证跨适配器唯一（onebot 与 milky 同为 "QQ"），重启映射因此挂在进程
        # 对象上而不按名字反查，免得重启时张冠李戴。
        p.akari_instance = instance
        p.start()
        processes.append(p)

    # run the server process
    server_stop_event = mp.Event()
    server_process = mp.Process(
        target=server_go,
        args=(server_stop_event, True, binary_mode, os.getpid(), hub_pid),
        name="server",
        daemon=True,
    )

    server_process.start()
    processes.append(server_process)

    while len(processes) > 1:
        for p in processes:
            if p.is_alive():
                continue
            if p.name == "server":
                if p.exitcode == 0:
                    sys.exit(0)
                if p.exitcode == 33:
                    Logger.warning(f"Process {p.pid} (server) exited with code {p.exitcode}, restart all bots.")
                    raise RestartBot
                Logger.critical(f"Process {p.pid} (server) exited with code {p.exitcode}, please check the log.")
                sys.exit(p.exitcode)
            if p.name == "jobqueue-hub":
                Logger.critical(f"Process {p.pid} (jobqueue-hub) exited with code {p.exitcode}, please check the log.")
                sys.exit(p.exitcode or 1)
            if p.exitcode == 0:
                Logger.warning(f"Process {p.pid} ({p.name}) exited with code 0, abort to restart.")
                processes.remove(p)
                terminate_process(p)
                break
            if p.exitcode == 33:
                Logger.warning(f"Process {p.pid} ({p.name}) exited with code {p.exitcode}, restart all bots.")
                raise RestartBot
            if p.exitcode == 78:  # 已明确没有必要重启的进程异常退出码
                processes.remove(p)
                terminate_process(p)
                break
            Logger.critical(f"Process {p.pid} ({p.name}) exited with code {p.exitcode}, please check the log.")
            processes.remove(p)
            # terminate_process() 会 close() 该进程对象，close 之后读取属性会抛错，故先取出实例记录。
            instance = getattr(p, "akari_instance", None)
            terminate_process(p)
            if instance is None:
                Logger.error(f"Process {p.pid} ({p.name}) has no adapter instance record, skip to restart.")
                break
            restart_bot_process(instance)
            break
        await asyncio.sleep(1)
    Logger.critical("All bots exited unexpectedly, please check the output.")
    sys.exit(1)


def terminate_process(
    process: multiprocessing.Process,
    graceful_event=None,
    graceful_timeout: float = 10,
):
    """优先请求进程自行清理，超时后再逐级终止。"""
    try:
        if process.is_alive() and graceful_event is not None:
            graceful_event.set()
            process.join(graceful_timeout)
        if process.is_alive():
            process.terminate()
            process.join(5)
        if process.is_alive():
            process.kill()
            process.join()
    finally:
        process.close()


def cleanup_processes():
    global server_stop_event, jobqueue_hub_stop_event
    # 先停止平台入口，再停止 Server；WebSocket Hub 最后退出，以便其它进程完成关闭信号与回包。
    shutdown_order = {"server": 1, "jobqueue-hub": 2}
    ordered_processes = sorted(processes, key=lambda ps: shutdown_order.get(ps.name, 0))
    for ps in ordered_processes:
        pid = ps.pid
        name = ps.name
        Logger.warning(f"Terminating process {pid} ({name})...")
        try:
            graceful_event = (
                server_stop_event if name == "server" else jobqueue_hub_stop_event if name == "jobqueue-hub" else None
            )
            terminate_process(ps, graceful_event)
        except Exception:
            Logger.exception(f"Failed to terminate process {pid} ({name}) cleanly.")
    processes.clear()
    server_stop_event = None
    jobqueue_hub_stop_event = None


async def main_async():
    try:
        multiprocess_run_until_complete(pre_init)
        await run_bot()  # Process will block here so
    except RestartBot as e:
        cleanup_processes()
        raise e
    except (KeyboardInterrupt, SystemExit) as e:
        cleanup_processes()
        raise e
    except Exception as e:
        Logger.critical("An error occurred, please check the output.")
        traceback.print_exc()
        cleanup_processes()
        raise e


def main():
    # Capture the base import lists to avoid clearing essential modules when restarting
    def clear_import_cache():
        for m in list(sys.modules):
            if m not in base_import_lists:
                del sys.modules[m]

    base_import_lists = list(sys.modules)

    while True:
        try:
            asyncio.run(main_async())
        except RestartBot:
            clear_import_cache()
            continue
        except SystemExit as exit_signal:
            # 重新抛出而非 break：run_bot() 跑在守护进程自身而非子进程，其 sys.exit(code) 若在此
            # 被吞掉，进程会以 0 退出，把「配置冲突中止」报成正常结束，守护工具因而不会告警。
            raise exit_signal
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    init_daemon_logger()
    # Detect if the program is already running
    lock_file_path = Path("./.bot.lock").resolve()
    if sys.platform == "win32":
        import msvcrt

        lock_file = open(lock_file_path, "w")  # skipcq
        try:
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            Logger.critical("Another instance is already running. Aborting.")
            sys.exit(1)
    else:
        import fcntl

        lock_file = open(lock_file_path, "w")  # skipcq
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            Logger.critical("Another instance is already running. Aborting.")
            sys.exit(1)

    main()
