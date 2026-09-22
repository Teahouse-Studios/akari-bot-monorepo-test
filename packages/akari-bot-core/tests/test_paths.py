"""core.paths 实例目录单元测试。"""

import subprocess
import sys
import tempfile
from pathlib import Path

import akaribot.core
from akaribot.core.constants.path import PrivateData
from akaribot.core.paths import INSTANCE_DIR_ENV, Paths
from akaribot.testing import Tester, func_case


# 仓库根从 core 包的位置向上推算（判据见 _repository_root），
# 既不依赖测试文件所处位置，也不取自 Paths.tests——后者正是本用例要断言的取值。
def _repository_root() -> Path:
    """独立推算仓库根：向上找含 packages/ 与 pyproject.toml 的目录。

    不按层数推算（源码根从 <dist>/src/akaribot 压成 <dist>/akaribot 后层数会变），也不取
    Paths.tests——后者正是本用例要断言的取值。
    """
    for candidate in Path(akaribot.core.__file__).resolve().parents:
        if (candidate / "packages").is_dir() and (candidate / "pyproject.toml").is_file():
            return candidate
    raise AssertionError("找不到仓库根")


PROJECT_ROOT = _repository_root()

# 子进程脚本：取出实例目录相关取值并打印，用于验证环境变量在导入期生效。
PROBE = (
    "from akaribot.core.paths import Paths; "
    "print('INSTANCE', Paths.instance); "
    "print('CONFIG', Paths.config); "
    "print('DATA', Paths.data); "
    "print('TESTS', Paths.tests)"
)


def _probe(env_overrides: dict[str, str]) -> dict[str, str]:
    """在子进程中解析路径取值。

    :param env_overrides: 追加的环境变量。
    :return: 探针输出的键值对。
    """
    import os

    env = os.environ.copy()
    env.update(env_overrides)
    result = subprocess.run(
        [sys.executable, "-c", PROBE],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    parsed = {"_returncode": str(result.returncode), "_stderr": result.stderr[-400:]}
    for line in result.stdout.splitlines():
        if line.startswith(("INSTANCE ", "CONFIG ", "DATA ", "TESTS ")):
            key, _, value = line.partition(" ")
            parsed[key] = value
    return parsed


def _test_defaults_to_process_cwd():
    """未设置 AKARI_INSTANCE_DIR 时实例目录为进程 cwd，与历史行为一致。"""
    values = _probe({INSTANCE_DIR_ENV: ""})
    return values.get("INSTANCE") == str(PROJECT_ROOT.resolve()) and values.get("DATA") == str(
        PROJECT_ROOT.resolve() / "data"
    )


def _test_instance_dir_env_selects_instance():
    """AKARI_INSTANCE_DIR 指向的目录即实例根，data 等子目录由其派生。

    config 的断言只在未设置 AKARI_CONFIG_PATH 时成立：测试基座会为该变量指向一份临时
    配置，此处显式清空它，避免用例结论取决于外层环境。
    """
    with tempfile.TemporaryDirectory() as tmp:
        instance = Path(tmp) / "inst"
        values = _probe({INSTANCE_DIR_ENV: str(instance), "AKARI_CONFIG_PATH": ""})
        if (
            values.get("INSTANCE") == str(instance.resolve())
            and values.get("CONFIG") == str(instance.resolve() / "config")
            and values.get("DATA") == str(instance.resolve() / "data")
        ):
            return True
        raise AssertionError(f"probe returned {values}")


def _test_config_path_env_wins_over_instance():
    """AKARI_CONFIG_PATH 优先于实例目录下的 config，两个变量可各自指向不同位置。"""
    with tempfile.TemporaryDirectory() as tmp:
        instance = Path(tmp) / "inst"
        config = Path(tmp) / "cfg"
        values = _probe({INSTANCE_DIR_ENV: str(instance), "AKARI_CONFIG_PATH": str(config)})
        return values.get("CONFIG") == str(config.resolve()) and values.get("INSTANCE") == str(instance.resolve())


def _test_tests_dir_is_not_instance_relative():
    """测试目录属源码仓库，不随实例目录变化。"""
    with tempfile.TemporaryDirectory() as tmp:
        instance = Path(tmp) / "inst"
        values = _probe({INSTANCE_DIR_ENV: str(instance)})
        return values.get("TESTS") == str(PROJECT_ROOT.resolve() / "tests")


def _test_import_does_not_create_directories():
    """导入 akaribot.core.constants 不得在任何目录产生副作用。"""
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; sys.path.insert(0, sys.argv[1]); import akaribot.core.constants",
                str(PROJECT_ROOT),
            ],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60,
            check=True,
        )
        return list(cwd.iterdir()) == []


def _test_ensure_creates_only_named_directories():
    """ensure() 只创建指定子目录。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        original = {name: getattr(Paths, name) for name in ("instance", "data", "cache", "logs", "database")}
        try:
            for name in original:
                setattr(Paths, name, root / name)
            Paths.ensure("cache", "logs")
            created = sorted(path.name for path in root.iterdir())
        finally:
            for name, value in original.items():
                setattr(Paths, name, value)
    return created == ["cache", "logs"]


def _test_ensure_rejects_non_directory_names():
    """ensure() 拒绝不是路径的属性名，避免把方法名当目录。"""
    try:
        Paths.ensure("as_dict")
    except KeyError:
        return True
    return False


def _test_as_dict_lists_every_instance_directory():
    """as_dict() 覆盖全部实例子目录，供诊断输出使用。"""
    listing = Paths.as_dict()
    expected = {"instance", "config", "assets", "data", "cache", "database", "logs", "tests"}
    return set(listing) == expected and all(isinstance(value, str) for value in listing.values())


def _test_private_data_is_lazy():
    """PrivateData 的目录不在导入期创建，且路径位于实例 data 之下。"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        original = PrivateData.path
        try:
            PrivateData.path = root / "private" / "default"
            # 判定须在临时目录销毁之前完成，否则退出 with 后 is_dir() 必然为假。
            before = PrivateData.path.exists()
            created = PrivateData.ensure()
            after = created.is_dir()
            result = (before, created, after)
        finally:
            PrivateData.path = original
    before, created, is_directory = result
    return not before and created == root / "private" / "default" and is_directory


def _test_private_data_lives_under_data():
    """私有目录位于实例 data/private 之下。

    末级目录名取决于当前客户端（default 或 client_name 的小写），不在此断言其取值。
    """
    path = PrivateData.path
    if not isinstance(path, Path) or Paths.data / "private" not in path.parents:
        raise AssertionError(f"PrivateData.path={path!r} type={type(path).__name__}")
    return True


@func_case
async def test_paths(tester: Tester):
    """core.paths: 实例目录测试"""
    await tester.test(_test_defaults_to_process_cwd, "缺省实例目录为进程 cwd")
    await tester.test(_test_instance_dir_env_selects_instance, "AKARI_INSTANCE_DIR 指定实例目录")
    await tester.test(_test_config_path_env_wins_over_instance, "AKARI_CONFIG_PATH 优先于实例目录")
    await tester.test(_test_tests_dir_is_not_instance_relative, "测试目录不随实例目录变化")
    await tester.test(_test_import_does_not_create_directories, "导入 akaribot.core.constants 无副作用")
    await tester.test(_test_ensure_creates_only_named_directories, "ensure 只创建指定子目录")
    await tester.test(_test_ensure_rejects_non_directory_names, "ensure 拒绝非目录属性名")
    await tester.test(_test_as_dict_lists_every_instance_directory, "as_dict 覆盖全部子目录")
    await tester.test(_test_private_data_is_lazy, "私有目录惰性创建")
    await tester.test(_test_private_data_lives_under_data, "私有目录位于 data/private 之下")
    return tester
