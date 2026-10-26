"""CLI 文档引擎：目录、生成、构建、预览。

对外契约集中在 :mod:`akaribot.cli.docs.model`；命令层只经由本包入口调用，不直接操作 VitePress。
"""

from .builder import build, fingerprint_catalog
from .catalog import load_catalog
from .config import DocsBuildConfig, DocsConfig, DocsSiteConfig, load_config, normalize_base
from .generator import generate
from .model import BuildResult, DocCatalog, DocPackage, DocPage, DocsError, ToolchainInfo
from .server import StaticServer
from .state import load_state, record_deploy, save_build_state, state_path
from .toolchain import detect, ensure_toolchain, run_build

__all__ = [
    "BuildResult",
    "DocCatalog",
    "DocPackage",
    "DocPage",
    "DocsBuildConfig",
    "DocsConfig",
    "DocsError",
    "DocsSiteConfig",
    "StaticServer",
    "ToolchainInfo",
    "build",
    "detect",
    "ensure_toolchain",
    "fingerprint_catalog",
    "generate",
    "load_catalog",
    "load_config",
    "load_state",
    "normalize_base",
    "record_deploy",
    "run_build",
    "save_build_state",
    "state_path",
]
