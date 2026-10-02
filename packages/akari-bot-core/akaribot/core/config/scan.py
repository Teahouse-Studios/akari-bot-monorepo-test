"""配置模板扫描。"""

import importlib

from loguru import logger

from akaribot.core.config import CFGManager
from akaribot.core.registry import PackageRegistry


def iter_config_template_modules() -> list[str]:
    """列出全部配置模板的模块名。

    清单由发现层给出（``PackageRegistry.config_template_paths()``），该处同样以文件是否
    存在判断模板有无，不导入包。

    :return: 配置模板的模块名列表，核心配置排在最前。
    """
    return PackageRegistry.config_template_paths()


def scan_config_templates() -> list[str]:
    """导入全部配置模板，补全配置文件中缺失的键。

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
