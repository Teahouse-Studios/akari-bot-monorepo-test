"""实例目录抽象。

进程在哪个实例里运行的唯一答案。产物路径由实例目录派生，而非相对 cwd 解析，故进程可在任意
目录启动。取值在导入期完成一次，之后只读。

导入期不创建目录，创建由 :meth:`Paths.ensure` 显式触发。
"""

import os
from pathlib import Path

# 实例目录。未设置时取进程 cwd，与历史行为一致。
INSTANCE_DIR_ENV = "AKARI_INSTANCE_DIR"

# 配置目录。优先级高于实例目录下的 config。
CONFIG_PATH_ENV = "AKARI_CONFIG_PATH"

# 测试用例目录。该目录属于源码仓库而非实例，故单独指定。
TESTS_PATH_ENV = "AKARI_TESTS_PATH"


def _env_path(name: str) -> Path | None:
    value = os.environ.get(name)
    if not value:
        return None
    return Path(value).expanduser().resolve()


def _repository_root() -> Path:
    # 判据是「含 ``packages/`` 与 ``pyproject.toml`` 的最近祖先」，不按层数推算——源码根从
    # ``<dist>/akaribot`` 压成 ``<dist>/akaribot`` 后层数会变，数层数会静默指到仓库之外。
    # 打包形态下找不到这样的祖先，退回包内目录：测试目录必然缺席，调用方的存在性判断照常生效。
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "packages").is_dir() and (candidate / "pyproject.toml").is_file():
            return candidate
    return current.parent


class Paths:
    """实例目录及其子目录。"""

    # as_dict() 面向「实例目录」清单；锁是文件，故显式排除。
    _FILES = ("lock",)

    instance: Path = _env_path(INSTANCE_DIR_ENV) or Path(".").resolve()
    """实例根目录。"""

    config: Path = _env_path(CONFIG_PATH_ENV) or instance / "config"
    """配置目录。"""

    assets: Path = instance / "assets"
    """随仓库或分发包提供的只读资源。"""

    data: Path = instance / "data"
    """运行时与部署者产生的可写数据。"""

    cache: Path = instance / "cache"
    """可随时删除的缓存。"""

    database: Path = instance / "database"
    """数据库文件所在目录（SQLite）。"""

    logs: Path = instance / "logs"
    """日志目录。"""

    lock: Path = instance / ".bot.lock"
    """单实例锁文件，供入口进程互斥与 CLI 探测运行状态。"""

    tests: Path = _env_path(TESTS_PATH_ENV) or _repository_root() / "tests"
    """测试用例目录，属源码仓库而非实例。"""

    @classmethod
    def ensure(cls, *names: str) -> None:
        """惰性创建指定子目录。

        :param names: :class:`Paths` 上的属性名，如 ``"cache"``、``"logs"``。
        :raises KeyError: 传入的名称不是实例子目录。
        """
        for name in names:
            value = getattr(cls, name)
            if not isinstance(value, Path):
                raise KeyError(f"{name!r} is not an instance directory")
            value.mkdir(parents=True, exist_ok=True)

    @classmethod
    def as_dict(cls) -> dict[str, str]:
        """列出全部实例目录，供日志与诊断输出。

        :return: 属性名到路径字符串的映射。
        """
        return {
            name: str(value)
            for name, value in vars(cls).items()
            if not name.startswith("_") and name not in cls._FILES and isinstance(value, Path)
        }
