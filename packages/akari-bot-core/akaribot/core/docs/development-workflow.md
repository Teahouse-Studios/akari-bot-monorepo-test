# 开发流程

本文介绍克隆仓库后的环境准备、日常检查、测试命令与提交约定。包结构、API 与测试的细节分别见 [模块开发](module-development.md)、[公共 API](public-api.md) 与测试框架的[运行入口](../../../../akari-bot-testing/akaribot/testing/docs/index.md)。

## 环境准备

仓库是 uv workspace，仓库根目录的 `pyproject.toml` 只声明工作区中的包与工具配置，没有 `[project]` 表。

```sh
export UV_CACHE_DIR="$PWD/.uvcache"
uv sync --all-extras --dev
```

缓存与 `.venv` 都放在工作区内。新增依赖时按包添加：

```sh
uv add --package akari-bot-core <包名>
```

`uv add` 要把依赖写进 `[project]` 表，而仓库根目录的 `pyproject.toml` 没有这个表。因此新增依赖时，要按上面的命令用 `--package` 指定包。

依赖版本以 `uv.lock` 为准。`pre-commit` 的 `uv-export` 从这个文件导出依赖清单，结果不包含 hash。

CI 使用 `--locked --all-extras --dev` 安装。`uv.lock` 与声明的依赖不一致时，安装失败。

## 日常命令

| 用途 | 命令 |
| --- | --- |
| 全量测试 | `CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing` |
| 单个文件 | `.venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_registry.py` |
| 静态检查 | `.venv/bin/ruff check .` 与 `.venv/bin/ruff format --check .` |
| 注释与排版 | `.venv/bin/python tools/lint_comments.py` |
| 分层与依赖 | `.venv/bin/python tools/lint_boundaries.py` |
| 内部版本要求 | `.venv/bin/python tools/lint_versions.py` |

全量测试跑完后，失败的用例清单必须与 `tools/test_baseline.txt` 中列出的用例按名称一一对应。运行结束后，用 `tools/check_test_baseline.py --junit junit.xml --baseline tools/test_baseline.txt` 检查两者是否一致。

只读测试使用另一份清单 `tools/test_baseline_readonly.txt`。这份清单由 `tools/check_test_baseline.py` 的 `--update` 参数重新生成。

## 提交前检查

提交前要执行下列检查，每一项都覆盖整个仓库：

- `ruff check .`
- `ruff format --check .`
- `tools/lint_comments.py`
- `tools/lint_boundaries.py`
- `tools/lint_versions.py`

`pre-commit install` 安装的钩子与上面的检查项不同：`comment-lint` 与 `boundary-lint` 带 `--diff HEAD`，只检查改动行，这样仓库中已有的违规不会阻止提交。推送前仍要执行全部检查。其余钩子为 `uv-export`、`ruff-check --fix` 与 `ruff-format`。

## 代码风格

Ruff 行宽 120、双引号、目标版本 `py312`，忽略 `E402`、`F405`、`F403`、`E741`、`E721`。导入按标准库、第三方、项目内部分组。

模块与适配器只从 `akaribot.core.api` 取公开接口，核心内部出现循环依赖时，改用 `akaribot.core.exports` 注册，需要时按名称取回。

注释写清这段代码为何这样写，单条一般不超过三行。含义清楚的代码不加注释，非公开 API 不加 docstring。

注释、文档与配置说明一律用正式书面语。中文与拉丁字母之间加空格，使用全角标点与弯引号。面向用户的文案称呼对方为“你”，机器人自称“机器人”。

文档、注释与配置说明只描述当前状态。设计取舍写当前为何如此，变更过程交给 git 历史。为迁移历史数据保留的兼容逻辑注明适用范围。

## 分支与提交

- 新功能用 `dev/` 前缀，修复用 `fix/` 前缀，分支名使用英文。
- 未经授权不执行 `git commit`、`git add`、`git push`、`git reset` 或 `git checkout -- <文件>`。授权只对当次请求有效。
- 提交信息用英文书面语，正文写清证据：实跑输出、失败用例的对比与检查结果。
- 移动文件用 `git mv`，保留文件的修改历史。根目录保留同名兼容文件时 git 不记为 rename，按“先纯移动、再改内容”两段提交。
- 包内有源码改动时，要提升该包的 `version`。不升版本时，在提交信息的最后一段单独写一行 `Skip-Version: true`，跳过全部包。只想跳过部分包时，写 `Skip-Version: <分发名>[, <分发名>]`，列出要跳过的包。`tools/check_versions.py` 负责检查这项约定，由 CI 在 PR 阶段以目标分支为基准运行，日常检查不包含它。

## 文档

每个包的导入包目录下都有 `docs/`。目录中的 `docs/config/global/docs.global.toml` 声明文档的标题、简介与排序。包在 `pyproject.toml` 的 `[project.entry-points."akaribot.docs"]` 中声明文档所在的导入路径，站点按这条声明收录该包的文档。

文档站的命令为 `akaribot docs list|build|serve|deploy|status|clean`。站点配置写在实例根目录的 `docs.toml`，生成的文件放在实例的 `cache/docs/` 目录。包文档需要哪些字段、目录如何组织，见仓库根目录的 `docs/package-docs.md`。
