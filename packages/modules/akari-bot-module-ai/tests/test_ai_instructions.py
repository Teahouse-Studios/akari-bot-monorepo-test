import importlib
import tempfile
from pathlib import Path
from unittest.mock import patch

from akaribot.core.registry import PackageRegistry
from akaribot.testing import Tester, func_case
from akaribot.modules.ai import setting


def _test_instance_instructions_override_bundled_default():
    with tempfile.TemporaryDirectory(prefix="akari-ai-instructions-") as raw:
        root = Path(raw)
        custom = "部署者的全局系统提示词。"
        (root / "instructions.txt").write_text(custom, encoding="utf-8")
        try:
            with patch.object(PackageRegistry, "package_data", return_value=root):
                importlib.reload(setting)
                overridden = setting.INSTRUCTIONS.template == custom
                overridden = overridden and setting.instructions_path == root / "instructions.txt"
                (root / "instructions.txt").unlink()
                importlib.reload(setting)
                fallback = setting.instructions_path == setting.ai_module_path / "assets" / "instructions.txt"
                fallback = fallback and setting.INSTRUCTIONS.template == setting.instructions_path.read_text(
                    encoding="utf-8"
                )
            return overridden and fallback
        finally:
            importlib.reload(setting)


def _test_instance_persona_override_bundled_default():
    with tempfile.TemporaryDirectory(prefix="akari-ai-persona-") as raw:
        root = Path(raw)
        custom = "部署者的人格化提示词。"
        (root / "persona.txt").write_text(custom, encoding="utf-8")
        try:
            with patch.object(PackageRegistry, "package_data", return_value=root):
                importlib.reload(setting)
                overridden = setting.PERSONA == custom and setting.persona_path == root / "persona.txt"
                (root / "persona.txt").unlink()
                importlib.reload(setting)
                fallback = setting.persona_path == setting.ai_module_path / "assets" / "persona.txt"
                fallback = fallback and setting.PERSONA == setting.persona_path.read_text(encoding="utf-8")
            return overridden and fallback
        finally:
            importlib.reload(setting)


@func_case
async def test_ai_instructions(tester: Tester):
    await tester.test(_test_instance_instructions_override_bundled_default, "实例全局提示词优先且缺失时使用包内默认")
    await tester.test(_test_instance_persona_override_bundled_default, "实例人格化提示词优先且缺失时使用包内默认")
    return tester
