"""``doc_facts`` 采集的单元测试。

每个用例只在 ``tmp_path`` 下构造最小包目录，不导入被扫描的包，也不依赖仓库内实际安装的包。
"""

import json
from pathlib import Path

from akaribot.core.entrypoints import docs
from akaribot.core.entrypoints.doc_facts import collect_package_facts


class _Spec:
    def __init__(self, location: Path):
        self.submodule_search_locations = [str(location)]


def _write(package_dir: Path, name: str, text: str) -> None:
    path = package_dir / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_comments(package_dir: Path, comments: dict[str, str]) -> None:
    _write(package_dir, "locales/zh_cn.json", json.dumps(comments, ensure_ascii=False))


def test_collect_config_tables(tmp_path: Path):
    """core.entrypoints.doc_facts 配置表与敏感表采集测试。"""
    package_dir = tmp_path / "modules" / "demo"
    _write(
        package_dir,
        "config.py",
        "from akaribot.core.api import on_module_config\n"
        "\n"
        "\n"
        '@on_module_config("demo")\n'
        "class DemoConfig:\n"
        "    enable: bool = True\n"
        '    demo_names: list = ["alpha", "beta"]\n'
        "    demo_ratio: float = 0.5\n"
        '    demo_label = "演示"\n'
        "\n"
        "\n"
        '@on_module_config("demo", secret=True)\n'
        "class DemoSecretConfig:\n"
        '    demo_token: str = ""\n',
    )
    _write_comments(
        package_dir,
        {
            "config.comments.module_demo.enable": "是否启用演示模块。",
            "config.comments.module_demo.demo_names": "演示名单。",
            "config.comments.module_demo.demo_ratio": "演示比例。",
            "config.comments.module_demo.demo_label": "演示标签。",
            "config.comments.module_demo_secret.demo_token": "演示令牌。",
            "config.comments.module_demo.note": "未声明的字段。",
        },
    )

    facts = collect_package_facts(package_dir, [])

    assert facts["config"] == [
        {
            "table": "module_demo",
            "file": "config/module_demo.toml",
            "secret": False,
            "fields": [
                {
                    "name": "enable",
                    "type": "bool",
                    "default": True,
                    "secret": False,
                    "comment": "是否启用演示模块。",
                    "required": False,
                },
                {
                    "name": "demo_names",
                    "type": "list",
                    "default": ["alpha", "beta"],
                    "secret": False,
                    "comment": "演示名单。",
                    "required": False,
                },
                {
                    "name": "demo_ratio",
                    "type": "float",
                    "default": 0.5,
                    "secret": False,
                    "comment": "演示比例。",
                    "required": False,
                },
                {
                    "name": "demo_label",
                    "type": "",
                    "default": "演示",
                    "secret": False,
                    "comment": "演示标签。",
                    "required": False,
                },
            ],
        },
        {
            "table": "module_demo_secret",
            "file": "config/module_demo.toml",
            "secret": True,
            "fields": [
                {
                    "name": "demo_token",
                    "type": "str",
                    "default": "",
                    "secret": True,
                    "comment": "演示令牌。",
                    "required": False,
                }
            ],
        },
    ]
    assert facts["features"] == {}


def test_collect_config_fallback_and_required(tmp_path: Path):
    """core.entrypoints.doc_facts 表名兜底、必填字段与无用例文件测试。"""
    package_dir = tmp_path / "demo"
    _write(
        package_dir,
        "config.py",
        "from akaribot.core.api import on_module_config\n"
        "\n"
        "\n"
        "class PlainConfig:\n"
        "    plain_value = 1\n"
        "\n"
        "\n"
        '@on_module_config("demo")\n'
        "class DemoConfig:\n"
        "    required_value: str\n"
        "    counter: int = 1\n",
    )
    _write(package_dir, "features.py", "features = object()\n")

    warnings: list[str] = []
    facts = collect_package_facts(package_dir, warnings)

    assert warnings == []
    assert [item["table"] for item in facts["config"]] == ["module_demo"]
    assert facts["config"][0]["file"] == "config/module_demo.toml"
    assert facts["config"][0]["fields"] == [
        {
            "name": "required_value",
            "type": "str",
            "default": None,
            "secret": False,
            "comment": "",
            "required": True,
        },
        {"name": "counter", "type": "int", "default": 1, "secret": False, "comment": "", "required": False},
    ]
    assert facts["features"] == {}


def test_collect_adapter_features(tmp_path: Path):
    """core.entrypoints.doc_facts 适配器平台表与能力采集测试。"""
    package_dir = tmp_path / "adapters" / "demo"
    _write(
        package_dir,
        "config.py",
        "from akaribot.core.api import on_bot_config\n"
        "\n"
        "\n"
        '@on_bot_config("demo")\n'
        "class DemoConfig:\n"
        "    enable: bool = False\n",
    )
    _write(
        package_dir,
        "features.py",
        "from akaribot.core.builtins.session.features import Features\n"
        "from akaribot.core.config.base import CoreConfig\n"
        "\n"
        "features = Features(\n"
        "    support_image=True,\n"
        "    support_audio=False,\n"
        "    use_url_manager=CoreConfig.enable_urlmanager,\n"
        ")\n",
    )

    facts = collect_package_facts(package_dir, [])

    assert facts["config"][0]["table"] == "bot_demo"
    assert facts["config"][0]["file"] == "config/bot_demo.toml"
    assert facts["features"] == {"support_image": True, "support_audio": False}
    assert all(isinstance(value, bool) for value in facts["features"].values())
    assert facts["features_dynamic"] == ["use_url_manager"]


def test_collect_config_syntax_error(tmp_path: Path):
    """core.entrypoints.doc_facts 配置语法错误时的告警测试。"""
    package_dir = tmp_path / "demo"
    _write(package_dir, "config.py", "class Broken(:\n    pass\n")

    warnings: list[str] = []
    facts = collect_package_facts(package_dir, warnings)

    assert facts == {"config": [], "features": {}}
    assert len(warnings) == 1
    assert "demo" in warnings[0]
    assert "config.py" in warnings[0]


def test_collect_missing_files(tmp_path: Path):
    """core.entrypoints.doc_facts 缺少配置与能力文件时的空结果测试。"""
    warnings: list[str] = []

    assert collect_package_facts(tmp_path / "empty", warnings) == {"config": [], "features": {}}
    assert warnings == []


def test_build_package_includes_facts(tmp_path: Path):
    """core.entrypoints.docs 包清单包含事实数据测试。"""
    package_dir = tmp_path / "akaribot" / "modules" / "demo"
    _write(package_dir, "docs/index.md", "# 演示\n")
    _write(
        package_dir,
        "config.py",
        "from akaribot.core.api import on_module_config\n"
        "\n"
        "\n"
        '@on_module_config("demo")\n'
        "class DemoConfig:\n"
        "    enable: bool = True\n",
    )

    warnings: list[str] = []
    item = docs._build_package(
        "module-demo",
        "akaribot.modules.demo",
        dist_name="akari-bot-module-demo",
        version="0.1.0",
        summary="",
        dependencies=[],
        editable=True,
        find_spec=lambda name: _Spec(package_dir),
        warnings=warnings,
    )

    assert item is not None
    assert item["facts"]["config"][0]["table"] == "module_demo"
    assert item["facts"]["features"] == {}
    assert warnings == []
