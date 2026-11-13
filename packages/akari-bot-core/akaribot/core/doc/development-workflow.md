# 开发流程

本文将会介绍检出源码后的环境准备、日常检查、测试入口与提交约定。包结构、API 与测试的细节分别见 [模块开发](module-development.md)、[公共 API](public-api.md) 与测试框架的[运行入口](../../../../akari-bot-testing/akaribot/testing/doc/index.md)。

## 环境准备

仓库是 uv workspace，根 `pyproject.toml` 只声明成员与工具配置，不含 `[project]`。

```sh
export UV_CACHE_DIR="$PWD/.uvcache"
uv sync --all-extras --dev
```

缓存与 `.venv` 都落在工作区内，安装不需要额外写权限。新增依赖按分发添加：

```sh
uv add --package akari-bot-core <包名>
```

在仓库根目录执行 `uv add` 会因缺少 `[project]` 直接失败。`uv.lock` 是依赖解析的唯一来源，不要手写 `requirements.txt`。pre-commit 的 `uv-export` 从锁文件导出不含 hash 的依赖清单。

CI 使用 `--locked --all-extras --dev` 安装。锁文件与声明不一致时，安装失败。

## 日常命令

| 用途 | 命令 |
| --- | --- |
| 全量测试 | `CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing` |
| 单个文件 | `.venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_registry.py` |
| 静态检查 | `.venv/bin/ruff check .` 与 `.venv/bin/ruff format --check .` |
| 注释与排版 | `.venv/bin/python tools/lint_comments.py` |
| 分层与依赖 | `.venv/bin/python tools/lint_boundaries.py` |
| 内部版本要求 | `.venv/bin/python tools/lint_versions.py` |

全量测试的失败集合必须与 `tools/test_baseline.txt` 逐名一致。运行结束后，用 `tools/check_test_baseline.py --junit junit.xml --baseline tools/test_baseline.txt` 对比。

只读测试另用 `tools/test_baseline_readonly.txt`。这份失败清单由 `--update` 生成，不要为了通过检查而手工删行。

## 提交前检查

五道检查是 `ruff check .`、`ruff format --check .`、`tools/lint_comments.py`、`tools/lint_boundaries.py` 与 `tools/lint_versions.py`，均检查全仓。

`pre-commit install` 安装的钩子不等同于检查项：`comment-lint` 与 `boundary-lint` 带 `--diff HEAD`，只检查改动行，用于避免既有违规阻塞提交。推送前仍应跑一遍全量检查。其余钩子为 `uv-export`、`ruff-check --fix` 与 `ruff-format`。

## 代码风格

Ruff 行宽 120、双引号、目标版本 `py312`，忽略 `E402`、`F405`、`F403`、`E741`、`E721`。导入按标准库、第三方、项目内部分组。

模块与适配器只从 `akaribot.core.api` 取公开接口，核心内部出现循环依赖时，改用 `akaribot.core.exports` 注册，需要时按名字取回。

注释解释“为什么”，单条一般不超过三行。不给自明的代码写注释，不给非公开 API 加 docstring。

注释、文档与配置说明一律用正式书面语。中文与拉丁字母之间加空格，使用全角标点与弯引号。面向用户的文案称呼对方为“你”，机器人自称“机器人”。

文档、注释与配置说明只描述当前状态。设计取舍写当前为何如此，变更过程交给 git 历史。为迁移历史数据保留的兼容逻辑注明适用范围。

## 分支与提交

- 新功能用 `dev/` 前缀，修复用 `fix/` 前缀，分支名使用英文。
- 未经授权不执行 `git commit`、`git add`、`git push`、`git reset` 或 `git checkout -- <文件>`。授权只对当次请求有效。
- 提交信息用中文书面语，正文写清证据：实跑输出、失败集合对比与检查结果。
- 移动文件用 `git mv` 保住 blame。根目录保留同名旧入口时 git 不记为 rename，按“先纯移动、再改内容”两段提交。
- 包内有源码改动即升 `version`，或在提交信息最后一段写独立的 `Skip-Version: true`，或写 `Skip-Version: <分发名>[, <分发名>]` 只豁免列出的成员。版本守卫 `tools/check_versions.py` 由 CI 在 PR 阶段以基准分支运行，不属于日常检查。

## 文档

每个分发的导入包目录下带 `doc/`，`doc.toml` 声明标题、简介与排序。pyproject 用 `[project.entry-points."akaribot.docs"]` 声明文档入口，站点据此收录该目录。

站点命令为 `akaribot docs list|build|serve|deploy|status|clean`，实例配置写根目录 `docs.toml`，生成物在实例 `cache/docs/`。包文档的字段与目录要求见仓库根的 `docs/package-docs.md`。
