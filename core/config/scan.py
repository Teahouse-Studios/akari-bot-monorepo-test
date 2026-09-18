"""配置模板扫描。

配置的生成统一在 bot.py 的 pre_init() 中完成，bot 与 server 子进程一律只读，
因此这里必须把全部模板扫全：任何遗漏的键都会在子进程读取时抛出 ConfigOperationError。
"""

import importlib

from loguru import logger

from core.config import CFGManager
from core.registry import PackageRegistry


def iter_config_template_modules() -> list[str]:
    """列出全部配置模板的模块名。

    清单由发现层给出（``PackageRegistry.config_template_paths()``）。该处以文件是否存在
    判断模板有无，而非在导入时捕获 ModuleNotFoundError：后者无法区分「该包未提供 config.py」
    与「模板自身导入了不存在的依赖」两种情形，后一种会被静默跳过，形成本设计所要杜绝的漏键。

    :return: 配置模板的模块名列表，核心配置排在最前。
    """
    return PackageRegistry.config_template_paths()


def scan_config_templates() -> list[str]:
    """导入全部配置模板，补全配置文件中缺失的键。

    扫描不区分 bot 与模块的启用状态：配置项一律补全，否则用户先禁用再启用便会撞上缺键。

    :return: 加载失败的配置模板模块名列表，空列表表示全部成功。
    """
    failed = []
    for module_name in iter_config_template_modules():
        try:
            importlib.import_module(module_name)
        except Exception:
            failed.append(module_name)
            logger.exception(f"[Config] Failed to load config template {module_name}: ")
    repaired_comments = CFGManager.repair_i18n_comments()
    if repaired_comments:
        logger.info(f"[Config] Repaired {repaired_comments} unresolved i18n comments.")
    CFGManager.save()
    return failed
