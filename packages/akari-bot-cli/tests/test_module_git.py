"""``module add --git``：从 git 仓库直引安装。

git 直引用在装完之前拿不到 manifest，因此预检、分发名与兼容性校验都要另想办法：名字靠安装前后的
差集认领，core API 校验挪到安装之后、不满足即卸载回滚。本文件固定这几条，以及地址拼接的各种写法。
"""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from akaribot.cli import i18n
from akaribot.cli import venv as engine
from akaribot.cli.commands import module as module_command
from akaribot.cli.instance import CliError, Instance, PackageInfo
from akaribot.cli.venv import git_spec
from akaribot.testing import Tester, func_case

DEMO_DIST = "akari-bot-module-demo"


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _make_instance(root: Path, packages: dict[str, PackageInfo]) -> Instance:
    (root / "akaribot.toml").write_text("", encoding="utf-8")
    instance = Instance(root)
    instance.installed = lambda **kwargs: dict(packages)  # type: ignore[method-assign]
    return instance


def _test_spec_forms():
    return (
        git_spec("https://h/r.git") == "git+https://h/r.git"
        and git_spec("git+https://h/r.git") == "git+https://h/r.git"
        and git_spec("https://h/r.git", ref="v1.2") == "git+https://h/r.git@v1.2"
        and git_spec("https://h/r.git", ref="main", subdir="pkgs/a") == "git+https://h/r.git@main#subdirectory=pkgs/a"
        and git_spec("https://h/r.git", subdir="pkgs/a") == "git+https://h/r.git#subdirectory=pkgs/a"
        and git_spec("https://h/r.git", ref="main", dist=DEMO_DIST) == f"{DEMO_DIST} @ git+https://h/r.git@main"
        and git_spec("https://h/r.git", dist=DEMO_DIST) == f"{DEMO_DIST} @ git+https://h/r.git"
    )


def _test_spec_keeps_userinfo_at():
    return git_spec("ssh://git@github.com/u/r.git", ref="dev") == "git+ssh://git@github.com/u/r.git@dev"


def _test_spec_conflicts():
    cases = (
        lambda: git_spec("https://h/r.git@main", ref="dev"),
        lambda: git_spec("https://h/r.git#subdirectory=a", subdir="b"),
        lambda: git_spec("   "),
    )
    for build in cases:
        try:
            build()
        except CliError:
            continue
        return False
    return True


def _test_resolve_git_rejects_conflicting_options():
    def resolve(*, editable=None, version=None):
        return module_command._resolve_git(
            "demo", dist=None, editable=editable, version=version, git="https://h/r.git", ref=None, subdir=None
        )

    rejected = 0
    for call in (lambda: resolve(editable=Path("/tmp/x")), lambda: resolve(version="1.0")):
        try:
            call()
        except CliError:
            rejected += 1
    return rejected == 2


def _test_resolve_git_builds_target():
    named = module_command._resolve_git(
        "demo", dist=None, version=None, editable=None, git="https://h/r.git", ref="main", subdir=None
    )
    anonymous = module_command._resolve_git(
        None, dist=None, version=None, editable=None, git="https://h/r.git", ref=None, subdir=None
    )
    return (
        named.source == "git"
        and named.dist == "demo"
        and named.specs == ("demo @ git+https://h/r.git@main",)
        and anonymous.dist == ""
        and anonymous.specs == ("git+https://h/r.git",)
    )


def _test_dist_resolution_by_difference():
    with TemporaryDirectory(prefix="akari-cli-git-") as directory:
        instance = _make_instance(Path(directory), {"akari-bot-core": PackageInfo(dist="akari-bot-core")})
        before = {"akari-bot-core"}
        instance.installed = lambda **kwargs: {  # type: ignore[method-assign]
            "akari-bot-core": PackageInfo(dist="akari-bot-core"),
            "akari-bot-module-demo": PackageInfo(dist="akari-bot-module-demo"),
        }
        return module_command._dist_from_git_install(instance, before, requested="") == DEMO_DIST


def _test_dist_resolution_prefers_requested():
    with TemporaryDirectory(prefix="akari-cli-git-") as directory:
        instance = _make_instance(Path(directory), {DEMO_DIST: PackageInfo(dist=DEMO_DIST)})
        before = {engine.canonical(DEMO_DIST)}
        return module_command._dist_from_git_install(instance, before, requested=DEMO_DIST) == DEMO_DIST


def _test_dist_resolution_reports_empty_and_ambiguous():
    with TemporaryDirectory(prefix="akari-cli-git-") as directory:
        root = Path(directory)
        empty = _make_instance(root, {})
        before: set[str] = set()
        try:
            module_command._dist_from_git_install(empty, before, requested="")
        except CliError as error:
            empty_ok = "没有发现新增分发" in str(error)
        else:
            return False
        many = _make_instance(root, {})
        many.installed = lambda **kwargs: {  # type: ignore[method-assign]
            "a": PackageInfo(dist="a"),
            "b": PackageInfo(dist="b"),
        }
        try:
            module_command._dist_from_git_install(many, before, requested="")
        except CliError as error:
            return empty_ok and "多个分发" in str(error)
        return False


def _test_post_install_api_check_rolls_back():
    with TemporaryDirectory(prefix="akari-cli-git-") as directory:
        root = Path(directory)
        (root / "akaribot.toml").write_text("", encoding="utf-8")
        instance = Instance(root)
        package = PackageInfo(dist=DEMO_DIST, requires_core_api=">=99")
        instance.find_package = lambda dist: package  # type: ignore[method-assign]
        instance.api_version = lambda: "1"  # type: ignore[method-assign]

        calls: list[list[str]] = []

        class _Runner:
            def run_checked(self, argv, *, what, env=None, stream=False):
                calls.append(list(argv))

        try:
            module_command._check_git_api(instance, DEMO_DIST, runner=_Runner())
        except Exception as error:  # noqa: BLE001 - fail() 抛 typer.Exit
            from typer import Exit

            if not isinstance(error, Exit):
                raise
        return any("uninstall" in call for call in calls)


def _test_post_install_api_check_accepts_compatible():
    with TemporaryDirectory(prefix="akari-cli-git-") as directory:
        root = Path(directory)
        (root / "akaribot.toml").write_text("", encoding="utf-8")
        instance = Instance(root)
        package = PackageInfo(dist=DEMO_DIST, requires_core_api=">=1")
        instance.find_package = lambda dist: package  # type: ignore[method-assign]
        instance.api_version = lambda: "1"  # type: ignore[method-assign]

        calls: list[list[str]] = []

        class _Runner:
            def run_checked(self, argv, *, what, env=None, stream=False):
                calls.append(list(argv))

        module_command._check_git_api(instance, DEMO_DIST, runner=_Runner())
        return calls == []


def _test_dry_run_prints_spec_without_touching_instance():
    from typer.testing import CliRunner

    from akaribot.cli import main

    with TemporaryDirectory(prefix="akari-cli-git-") as directory:
        root = Path(directory)
        (root / "akaribot.toml").write_text("", encoding="utf-8")
        instance = Instance(root)
        result = None
        with patch.object(module_command, "require_instance", return_value=instance):
            result = CliRunner().invoke(
                main.app,
                [
                    "module",
                    "add",
                    "--git",
                    "https://h/r.git",
                    "--ref",
                    "main",
                    "-I",
                    str(root),
                    "--dry-run",
                ],
            )
    text = result.stdout if result is not None else ""
    return result is not None and result.exit_code == 0 and "git+https://h/r.git@main" in text


@func_case
async def test_module_git(tester: Tester):
    """cli.commands.module: git 直引安装测试"""
    _use_cli_locale()
    await tester.test(_test_spec_forms, "地址拼接的各种写法")
    await tester.test(_test_spec_keeps_userinfo_at, "userinfo 的 @ 不算 ref")
    await tester.test(_test_spec_conflicts, "自带 ref 或子目录时拒绝重复指定")
    await tester.test(_test_resolve_git_rejects_conflicting_options, "--git 与 -e/--version 互斥")
    await tester.test(_test_resolve_git_builds_target, "解析出带 git 来源的安装目标")
    await tester.test(_test_dist_resolution_by_difference, "按差集认领分发名")
    await tester.test(_test_dist_resolution_prefers_requested, "同名重装时采用给定名字")
    await tester.test(_test_dist_resolution_reports_empty_and_ambiguous, "差集为空或不唯一时报错")
    await tester.test(_test_post_install_api_check_rolls_back, "core API 不满足时卸载回滚")
    await tester.test(_test_post_install_api_check_accepts_compatible, "core API 满足时放行")
    await tester.test(_test_dry_run_prints_spec_without_touching_instance, "--dry-run 只打印参数")
    return tester
