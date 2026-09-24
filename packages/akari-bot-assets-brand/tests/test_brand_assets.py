"""品牌资产包的内容与保真度守卫。

这些文件是**画师提供的原件**，不是可重新导出的构建产物：立绘曾被降采样成 1024px/128 色以压进
core wheel，用户一眼就看出糊了。体积该由使用侧（展示宽度、是否内嵌）来控，不能靠改这些文件。
故此处把「尺寸、色彩模式、体积下限」钉住——允许画师换图，但挡住任何一次静默重新编码。
"""

from pathlib import Path

from akaribot.assets.brand import brand_dir
from akaribot.testing import Tester, func_case

# 原件规格：2000×2000 全彩 RGBA。降采样或转调色板都会让画面明显变糊。
CHARACTER_SIZE = (2000, 2000)
CHARACTER_MODE = "RGBA"
# 体积下限取原件的约七成：正常的重新导出会落在这个区间之上，有损压缩则远低于它。
CHARACTER_MIN_BYTES = 2 * 1024 * 1024

REQUIRED_FILES = ("character_marked.png", "akaribot_logo.png", "credits.txt", "LICENSE")


def _test_brand_dir_holds_every_asset():
    directory = brand_dir()
    return directory.is_dir() and all((directory / name).is_file() for name in REQUIRED_FILES)


def _test_character_artwork_keeps_original_fidelity():
    from PIL import Image

    path = brand_dir() / "character_marked.png"
    with Image.open(path) as image:
        size = image.size
        mode = image.mode
    return size == CHARACTER_SIZE and mode == CHARACTER_MODE and path.stat().st_size >= CHARACTER_MIN_BYTES


def _test_logo_is_a_readable_png():
    from PIL import Image

    path = brand_dir() / "akaribot_logo.png"
    with Image.open(path) as image:
        image.verify()
        size = image.size
    return size[0] > 0 and size[1] > 0 and path.stat().st_size > 1024


def _test_credits_is_not_empty():
    text = (brand_dir() / "credits.txt").read_text(encoding="utf-8").strip()
    return len(text) > 0


def _test_license_is_bundled_with_the_artwork():
    text = (brand_dir() / "LICENSE").read_text(encoding="utf-8")
    return "OasisAkari" in text and "SAWARATSUKI" in text


def _test_no_stray_build_artifacts_beside_the_assets():
    directory = Path(brand_dir())
    allowed = {*REQUIRED_FILES, "__init__.py", "manifest.toml", "__pycache__"}
    return all(child.name in allowed for child in directory.iterdir())


@func_case
async def test_brand_assets(tester: Tester):
    """akaribot.assets.brand: 品牌资产内容与保真度测试"""
    await tester.test(_test_brand_dir_holds_every_asset, "三份资产与许可证齐全")
    await tester.test(_test_character_artwork_keeps_original_fidelity, "立绘保持原件规格")
    await tester.test(_test_logo_is_a_readable_png, "标志可解码且非空")
    await tester.test(_test_credits_is_not_empty, "制作人员名单非空")
    await tester.test(_test_license_is_bundled_with_the_artwork, "许可证随资源一同分发")
    await tester.test(_test_no_stray_build_artifacts_beside_the_assets, "资源目录无打包残留")
    return tester
