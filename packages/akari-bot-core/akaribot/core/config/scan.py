"""配置模板扫描的既有导入路径。

实现位于 :mod:`akaribot.core.builtins.config.scan`。
"""

from akaribot.core.builtins.config.scan import iter_config_template_modules, scan_config_templates

__all__ = ["iter_config_template_modules", "scan_config_templates"]
