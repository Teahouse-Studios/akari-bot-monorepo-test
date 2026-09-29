---
name: akaribot-dev
description: AkariBot monorepo 开发指南。用于改动 core 框架、消息与会话、命令模块包、平台适配器、测试、注释规范或新增模块包；按任务领域读取对应 reference，不要一次加载全部文档。
---

# AkariBot 开发指南

本仓库是 uv workspace：core、模块、适配器各自独立发包，运行时靠 entry points 发现。先确定任务领域，再完整读取对应的一级参考文件；不要为了「了解项目」一次性加载全部 references。

## 开始工作

1. 先读本文件中的强制规则。
2. 根据下方路由选择 reference，并完整读完所选文件后再改代码。
3. reference 中的路径、默认值和 API 只是工作入口；涉及具体实现时仍以当前源码为准，用 `rg` 核对。
4. 改动前读 `AGENTS.md` 的「架构脉络」与「陷阱」；提交前跑五道门禁。

## 强制规则

- **只描述当前状态**：文档、注释与配置说明不记录「从前如何」，不写「原本是 X，现在改为 Y」这类对照式表述；变更历史由 git 承载。
- 面向用户的固定文案使用 `I18NContext`，只在所属包的 `locales/zh_cn.json` 新增或修改节点。参数占位符使用 `${name}`。
- 除非用户明确要求处理翻译或 Weblate 同步结果，禁止创建、修改、删除或补齐任何包内 `locales/` 下非 `zh_cn.json` 的语言 JSON。其他语言由 Weblate bot 自动提交。
- 配置字段注释写在所属包 `locales/zh_cn.json` 的 `config.comments.<表名>.<字段名>`；未指定 `table_name` 时表名为 `config`。
- 会话归属的模块数据使用 `union_id` 和正确的 `union_scope`；不要新增按平台割裂的 `sender_id` / `target_id` 状态列。
- 平台能力必须使用 `Features(...)` 实例声明。不要子类化 `Features`，也不要把类对象赋给 `ContextManager.features`。
- `SessionInfo` 会跨进程传输，新增字段必须可序列化；模块代码运行在 server 进程，平台 SDK 操作必须通过 JobQueue / `ContextManager` 返回 bot 进程。
- 遇到循环导入时优先使用 `akaribot.core.exports` 的导出机制，不要通过随意重排 import 掩盖问题。
- 模块与适配器只 import `akaribot.core.api`（适配器另有 `akaribot.core.api.adapters`）的公共面；不得 import core 内部深路径、`akaribot.adapters.*` 或 `akaribot.core.api.adapters`（模块侧）。
- 新增包必须在自己的 `pyproject.toml` 声明 entry point 与依赖；对 core 的约束字面必须与其余包一致。
- 测试使用自研框架而非 pytest。自动化运行必须设置 `CI=1`；否则人工复核和等待输入可能挂起。
- **不要擅自 commit**：改动留在未提交的工作区，交由用户检视与提交；`git add`、`git push`、`git reset`、`git checkout -- <file>` 同样需要用户授权。
- 新功能分支用 `dev/`，修复分支用 `fix/`；分支名使用英文。

## 按领域读取

| 任务 | 必须读取 | 典型内容 |
| --- | --- | --- |
| 理解整体架构、启动、进程、消息流或目录 | [architecture.md](references/architecture.md) | 包布局、双进程、JobQueue、启动与重启、收发消息全链路 |
| 修改消息、会话、Bot 或 parser | [messaging-and-parser.md](references/messaging-and-parser.md) | Bot、消息元素、SessionInfo、MessageSession、ContextManager、parser、等待与控制流 |
| 修改 loader、component、配置、数据库或队列 | [infrastructure.md](references/infrastructure.md) | 包发现与 manifest、模块加载、配置模板、union 数据、双连接、JobQueue、exports、热重载 |
| 新建或修改命令模块包 | [module-development.md](references/module-development.md) | 模块包脚手架、manifest、module/command/regex、权限、配置、数据库、i18n、定时任务、hook |
| 新建或修改平台适配器 | [platform-adapters.md](references/platform-adapters.md) | 包结构、info、Features、bot 入口、ContextManager、多实例与配置表 |
| 编写、运行或诊断测试 | [testing.md](references/testing.md) | `@func_case`、`@case`、Expectation、mock parser、fixture、单测命令 |
| 依赖、格式化、注释、分支或文字排版 | [workflow-and-style.md](references/workflow-and-style.md) | Ruff、pre-commit、依赖约束、分支、中文排版、导入与注释规范 |

## 组合读取规则

- 修改普通命令：读 `module-development.md` + `messaging-and-parser.md`；补测试时再读 `testing.md`。
- 修改模块配置或数据库：读 `module-development.md` + `infrastructure.md`；若涉及消息入口，再读 `messaging-and-parser.md`。
- 修改消息元素、会话能力或 parser：读 `messaging-and-parser.md`；若行为影响命令模块，再读 `module-development.md` 和 `testing.md`。
- 修改平台发送、消息渲染或私信：读 `platform-adapters.md` + `architecture.md` + `messaging-and-parser.md`；涉及配置或队列细节时再读 `infrastructure.md`。
- 修改启动、包发现、队列或跨进程行为：读 `architecture.md` + `infrastructure.md`。
- 修改热重载：读 `infrastructure.md`；涉及守护进程重启时再读 `architecture.md`。
- 只改依赖、格式、分支或文案排版：读 `workflow-and-style.md`，不要加载其他大文件。

## 高频命令

```bash
export UV_CACHE_DIR="$PWD/.uvcache"
uv sync --all-extras --dev

CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing   # 全量
.venv/bin/python tests/run_one.py packages/akari-bot-module-wiki/tests/test_wiki_markdown.py    # 单个入口

.venv/bin/ruff check . && .venv/bin/ruff format --check .
.venv/bin/python tools/lint_comments.py
.venv/bin/python tools/lint_boundaries.py
.venv/bin/python tools/lint_versions.py
```

`python -m akaribot.testing` 不解析命令行参数；按入口筛选用 `tests/run_one.py`，用法见 `testing.md`。CLI 用法见 `akaribot --help`。

## 常见陷阱

- `akaribot/testing/__init__.py` 不得静态导入 `.tester`，否则合并日志目录会在隔离环境变量就位之前被固化到仓库 `data/`。
- 根 `bot.py` / `tester.py` 兼容层用 `sys.modules` 模块别名，不要逐名再导出。
- `CFGManager.load()` 只扫描 `config/*.toml`：适配器实例配置写扁平路径 `config/<基表>.toml`，写到 `config/adapters/` 的表对 core 不可见。
- 内部依赖约束必须字面一致（当前 `akari-bot-core>=0.1.0,<1.0`），由 `tools/lint_versions.py` 检查。
- 官方模块包之间不得互相依赖（门禁 B10）；第三方模块跨包依赖只能用对方 `.api` 并在自身 pyproject 声明。
- 完整清单见 `AGENTS.md` 的「陷阱」一节。

## 参考文件维护

- 新增知识时放入最匹配的一个 reference，避免在多个文件复制同一段内容。
- 所有 reference 保持为本文件的直接链接，不再建立二级引用链；新增或删除 reference 时同步更新本文件，并跑
  `.venv/bin/python .agents/skills/akaribot-dev/scripts/validate_references.py` 校验结构与路径。
- reference 超过 100 行时保留顶部 `## 目录`，且目录须落在文件前 10 行内。
- 修改 reference 后检查本文件中的全部相对链接，并确认 `references/` 下没有孤儿文件。
