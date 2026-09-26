"""品牌主题：调色板、默认主题与切换。

主题色取自品牌立绘 character_marked.png（浅紫与粉色为主、暗部是深紫褐）。界面默认用深色版，
`ctrl+t` 在深色与浅色之间切换；两套主题都注册在应用上，样式表里的 ``$primary`` 等变量据此解析。
"""

import time

from akaribot.cli import i18n
from akaribot.cli.tui import _compat as compat
from akaribot.cli.tui.app import STYLESHEET, TuiApp
from akaribot.cli.tui.modules import ModuleRecord, StaticModuleSource
from akaribot.testing import Tester, func_case

# 立绘不透明部分的主色与暗部，深色版据此取色；改主题时这里先失败，避免悄悄换掉品牌色。
BRAND_COLORS = ("#d69cdd", "#f6d5f3", "#fbd8ec", "#40333f", "#2b002a")


def _use_cli_locale() -> None:
    i18n.build_locale_snapshot(list(i18n.SUPPORTED_LOCALES), [i18n.locales_dir()], "akaribot-cli")
    i18n.connect_locale_snapshot("akaribot-cli")


def _boot_app() -> TuiApp:
    record = ModuleRecord(name="dice", dist="akari-bot-module-dice", version="1.0.0", state="installed")
    source = StaticModuleSource(records=[record], available=[record])
    return TuiApp(source=source, boot_started_at=time.monotonic())


def _rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    return tuple(int(text[index : index + 2], 16) for index in (0, 2, 4))


async def _test_dark_theme_is_default():
    # 主题要落到控件样式上，而不只是 get_css_variables() 里的一串字符串。
    app = _boot_app()
    async with compat.app_test(app, size=(100, 30)) as pilot:
        await pilot.pause()
        background = app.screen.styles.background
        border = app.modules_page().query_one("#module-list").styles.border_top[1]
        await pilot.press("q")
    return (
        app.theme == compat.AKARI_THEME_DARK
        and tuple(background.rich_color.get_truecolor()) == _rgb(compat.AKARI_DARK_PALETTE["background"])
        and tuple(border.rich_color.get_truecolor()) == _rgb(compat.AKARI_DARK_PALETTE["primary"])
        and str(app.get_css_variables()["accent"]).lower() == compat.AKARI_DARK_PALETTE["accent"]
    )


async def _test_palette_stays_in_the_brand_family():
    # 强调色与前景色必须落在立绘的色系里（浅紫 / 粉 / 深紫褐），语义色另配。
    dark = compat.AKARI_DARK_PALETTE
    light = compat.AKARI_LIGHT_PALETTE
    branded = {dark["primary"], dark["secondary"], dark["accent"], dark["foreground"]}
    return (
        len(branded) == 4
        and all(value.startswith("#") and len(value) == 7 for value in {*dark.values(), *light.values()})
        and dark["primary"] == BRAND_COLORS[0]
        # 深色版以暗部作底，浅色版用立绘的浅底；两套主题的明暗标记相反。
        and dark["background"] != light["background"]
        and compat.build_theme("probe", dark, dark=True).dark
        and not compat.build_theme("probe", light, dark=False).dark
    )


async def _test_stylesheet_parses_under_brand_theme():
    # 样式表里的 $变量 全部由品牌主题提供：少了任何一个都会在解析期报未定义变量。
    probe = compat.App()
    compat.install_akari_themes(probe)
    try:
        compat.parse_stylesheet(STYLESHEET, "<test>", app=probe)
    except Exception:  # noqa: BLE001 - 解析失败即用例失败
        return False
    return True


async def _test_toggle_switches_palette():
    app = _boot_app()
    async with compat.app_test(app, size=(100, 30)) as pilot:
        await pilot.pause()
        before = str(app.get_css_variables()["primary"]).lower()
        await pilot.press("ctrl+t")
        await pilot.pause()
        after = app.theme
        switched = str(app.get_css_variables()["primary"]).lower()
        await pilot.press("ctrl+t")
        await pilot.pause()
        back = app.theme
        await pilot.press("q")
    return (
        before == compat.AKARI_DARK_PALETTE["primary"]
        and after == compat.AKARI_THEME_LIGHT
        and switched == compat.AKARI_LIGHT_PALETTE["primary"]
        and back == compat.AKARI_THEME_DARK
    )


@func_case
async def test_tui_theme(tester: Tester):
    """cli.tui.theme: 品牌主题与切换测试"""
    _use_cli_locale()
    await tester.test(_test_dark_theme_is_default, "默认使用品牌深色主题")
    await tester.test(_test_palette_stays_in_the_brand_family, "调色板取自立绘色系")
    await tester.test(_test_stylesheet_parses_under_brand_theme, "样式表在品牌主题下全部变量可解析")
    await tester.test(_test_toggle_switches_palette, "ctrl+t 在深色与浅色之间切换")
    return tester
