"""品牌资产定位的回退链：资源包 → 实例 assets → 无。

品牌资产进的是 core 的 ``full`` extra，裸 core（``akaribot init --minimal``）下资源包根本不存在；
部署者还可能把图放在实例 ``assets/`` 里覆盖默认值。这两条路径都要能走通，且两处都没有时必须
返回 ``None`` 让调用方降级——`~about` 少一张图不该让整条命令失败，SMTP 报告少个标志也不该让
邮件发不出去。
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

from akaribot.core.utils import brand
from akaribot.testing import Tester, func_case

ASSET = "character_marked.png"


def _test_package_asset_wins():
    """资源包存在时优先取包内的那份（默认值来自随包分发的原件）。"""
    with tempfile.TemporaryDirectory(prefix="akari-brand-") as raw:
        package_dir = Path(raw) / "package"
        instance_dir = Path(raw) / "instance"
        for directory in (package_dir, instance_dir):
            directory.mkdir()
            (directory / ASSET).write_text("x", encoding="utf-8")
        with (
            patch.object(brand, "_package_brand_dir", return_value=package_dir),
            patch.object(brand.Paths, "assets", instance_dir),
        ):
            found = brand.find_brand_asset(ASSET)
    return found == package_dir / ASSET


def _test_instance_asset_is_the_fallback():
    """资源包缺席时回退到实例 assets/，部署者据此覆盖默认图。"""
    with tempfile.TemporaryDirectory(prefix="akari-brand-") as raw:
        instance_dir = Path(raw) / "instance"
        instance_dir.mkdir()
        (instance_dir / ASSET).write_text("x", encoding="utf-8")
        with (
            patch.object(brand, "_package_brand_dir", return_value=None),
            patch.object(brand.Paths, "assets", instance_dir),
        ):
            found = brand.find_brand_asset(ASSET)
    return found == instance_dir / ASSET


def _test_missing_everywhere_returns_none():
    """两处都没有时返回 None，而不是抛异常或返回一个不存在的路径。"""
    with tempfile.TemporaryDirectory(prefix="akari-brand-") as raw:
        instance_dir = Path(raw) / "instance"
        instance_dir.mkdir()
        with (
            patch.object(brand, "_package_brand_dir", return_value=None),
            patch.object(brand.Paths, "assets", instance_dir),
        ):
            found = brand.find_brand_asset(ASSET)
    return found is None


def _test_package_without_the_named_asset_falls_through():
    """资源包在、但里面没有该文件时继续回退，不把包目录当成万能来源。"""
    with tempfile.TemporaryDirectory(prefix="akari-brand-") as raw:
        package_dir = Path(raw) / "package"
        instance_dir = Path(raw) / "instance"
        for directory in (package_dir, instance_dir):
            directory.mkdir()
        (instance_dir / ASSET).write_text("x", encoding="utf-8")
        with (
            patch.object(brand, "_package_brand_dir", return_value=package_dir),
            patch.object(brand.Paths, "assets", instance_dir),
        ):
            found = brand.find_brand_asset(ASSET)
    return found == instance_dir / ASSET


def _test_uninstalled_package_is_not_an_error():
    """资源包没装时定位函数不抛异常——裸 core 是受支持的安装形态。"""
    with tempfile.TemporaryDirectory(prefix="akari-brand-") as raw:
        instance_dir = Path(raw) / "instance"
        instance_dir.mkdir()
        with (
            patch.object(brand, "_package_brand_dir", return_value=None),
            patch.object(brand.Paths, "assets", instance_dir),
        ):
            try:
                brand.find_brand_asset("akaribot_logo.png")
            except Exception:  # noqa: BLE001 - 任何异常都算失败
                return False
    return True


def _test_real_install_resolves_the_shipped_assets():
    """当前环境装了品牌资源包时，三份资产都应能定位到（CI 用 --all-extras）。"""
    directory = brand._package_brand_dir()
    if directory is None:
        return True
    return all(
        brand.find_brand_asset(name) is not None
        for name in ("character_marked.png", "akaribot_logo.png", "credits.txt")
    )


@func_case
async def test_brand_lookup(tester: Tester):
    """core.utils.brand: 品牌资产回退链测试"""
    await tester.test(_test_package_asset_wins, "资源包优先")
    await tester.test(_test_instance_asset_is_the_fallback, "实例 assets 作为回退")
    await tester.test(_test_missing_everywhere_returns_none, "两处都没有时返回 None")
    await tester.test(_test_package_without_the_named_asset_falls_through, "包内缺该文件时继续回退")
    await tester.test(_test_uninstalled_package_is_not_an_error, "资源包未安装不抛异常")
    await tester.test(_test_real_install_resolves_the_shipped_assets, "已装环境下三份资产均可定位")
    return tester
