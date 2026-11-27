# 开发流程

本文介绍开发环境搭建、日常质量检查、测试执行命令及代码提交约定。包结构、API 与测试框架的详细说明分别参见[模块开发](module-development.md)、[公共 API](public-api.md)及[测试框架运行入口](../../../../akari-bot-testing/akaribot/testing/docs/index.md)。

## 环境准备

仓库采用 uv workspace 结构，仓库根目录的 `pyproject.toml` 仅声明工作区中的包与工具配置，未包含 `[project]` 表。

```sh
export UV_CACHE_DIR="$PWD/.uvcache"
uv sync --all-extras --dev
```

工具缓存与虚拟环境 `.venv` 均置于工作区内部。新增依赖项时必须按成员包维度添加：

```sh
uv add --package akari-bot-core <包名>
```

`uv add` 默认将依赖写入 `[project]` 表，而仓库根目录的 `pyproject.toml` 仅声明工作区且未包含该表。因此新增依赖时，必须通过 `--package` 参数指定具体目标包。

依赖版本以 `uv.lock` 为准。`pre-commit` 的 `uv-export` 从该文件导出依赖清单，输出结果不包含哈希值。

CI 环境使用 `--locked --all-extras --dev` 执行安装。若 `uv.lock` 与声明的依赖不一致，安装流程将直接失败。

## 日常命令

| 用途 | 命令 |
| --- | --- |
| 全量测试 | `CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing` |
| 单个文件 | `.venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_registry.py` |
| 静态检查 | `.venv/bin/ruff check .` 与 `.venv/bin/ruff format --check .` |
| 注释与排版 | `.venv/bin/python tools/lint_comments.py` |
| 分层与依赖 | `.venv/bin/python tools/lint_boundaries.py` |
| 内部版本要求 | `.venv/bin/python tools/lint_versions.py` |

全量测试运行完成后，失败用例清单必须与 `tools/test_baseline.txt` 中的基准用例按名称一一对应。测试执行完毕后，调用 `tools/check_test_baseline.py --junit junit.xml --baseline tools/test_baseline.txt` 验证两者的一致性。

只读测试使用另一份清单 `tools/test_baseline_readonly.txt`。该清单由 `tools/check_test_baseline.py` 的 `--update` 参数重新生成。

## 提交前检查

提交前需要执行下列检查，每一项均覆盖整个仓库：

- `ruff check .`
- `ruff format --check .`
- `tools/lint_comments.py`
- `tools/lint_boundaries.py`
- `tools/lint_versions.py`

`pre-commit install` 安装的钩子与上述检查项不同，`comment-lint` 与 `boundary-lint` 带有 `--diff HEAD` 参数，仅检查改动行，避免仓库中已有的存量违规阻止提交。推送前仍需要执行全部检查。其余钩子为 `uv-export`、`ruff-check --fix` 与 `ruff-format`。

## 代码风格

Ruff 行宽 120、双引号、目标版本 `py312`，忽略 `E402`、`F405`、`F403`、`E741`、`E721`。导入按标准库、第三方、项目内部分组。

模块与适配器仅从 `akaribot.core.api` 获取公开接口。核心内部出现循环依赖时，改用 `akaribot.core.exports` 注册，需要时按名称取回。

注释旨在阐释代码背后的设计意图与边界约束，单条长度通常不超过三行。逻辑清晰且含义明确的代码无需添加注释，非公开 API 严禁添加 docstring。

注释、文档及配置说明一律采用严谨的书面中文。中文与西文字符之间必须保留空格，标点统一采用全角符号。面向用户的交互文案称呼对方为“你”，机器人自称为“机器人”。

文档、注释与配置说明仅描述当前状态。阐释设计取舍时直接陈述当前逻辑与约束，历史演进交由 git 记录。为迁移历史数据保留的兼容逻辑需注明适用范围。

## 分支与提交

- 新功能分支使用 `dev/` 前缀，修复分支使用 `fix/` 前缀，分支名称使用英文。
- 未获得明确授权不可执行 `git commit`、`git add`、`git push`、`git reset` 或 `git checkout -- <文件>`。授权仅对当次请求有效。
- 提交信息使用英文书面语，正文写明实际运行输出、失败用例的对比与检查结果等证据。
- 移动文件必须使用 `git mv` 以保留历史追溯记录。当根目录保留同名兼容文件时，git 无法自动判定为重命名，必须拆分为“先纯移动文件、后修改内容”两次独立提交。
- 当成员包内存在源码修改时，必须递增该包 `pyproject.toml` 中的 `version`。若无需升级版本，必须在提交信息的最后一段单独声明 `Skip-Version: true`（豁免全部成员包），或填写 `Skip-Version: <包名称>[, <包名称>]`（列出特定豁免包）。版本检查脚本 `tools/check_versions.py` 负责验证该约束，由 CI 在拉取请求（PR）阶段以目标分支为基准执行检查。

## 文档

每个成员包的导入包根目录下均包含 `docs/` 目录，通过 `docs/config/global/docs.global.toml` 声明文档标题、简介及排序权重。在 `pyproject.toml` 的 `[project.entry-points."akaribot.docs"]` 中声明文档导入路径，文档构建引擎据此收录该包的文档页面。

文档站点管理命令涵盖 `akaribot docs list|build|sync-theme|install-deps|serve|dev|deploy|status|clean`。站点配置定义于实例根目录的 `docs.toml`，构建产物输出至 `cache/docs/` 目录。包文档所需的元数据字段及目录结构规范参见 `docs/package-docs.md`。
