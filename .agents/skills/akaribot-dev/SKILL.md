---
name: akaribot-dev
description: AkariBot 开发指南。用于修改核心框架、消息与会话系统、命令模块、平台适配器、配置、数据库、队列、i18n、测试或项目约定。先读本页路由表，再按领域读取 packages/ 下的文档页。
---

# AkariBot 开发

完整手册是随源码维护的文档页（`packages/*/akaribot/**/docs/`），也是文档站点的内容来源。本技能仅提供
入口与必须遵守的规则，不复制页面内容。

## 开始工作

1. 阅读仓库根目录 `AGENTS.md`（流程大纲与文档索引），按需查阅 `docs/agents/` 下的架构、文档与注释、
   测试、陷阱、提交与版本约定。
2. 按照下表查找对应的文档页。涉及多个领域时请查阅对应页面。
3. 修改代码前先检查 `tests/` 与包内 `tests/` 是否已覆盖该行为。
4. 提交前运行五道检查，参见下方“高频命令”与开发流程页。

## 文档路由

| 任务 | 文档页 |
| --- | --- |
| 代码结构、进程拓扑、启动、退出码、消息链路 | `packages/akari-bot-core/akaribot/core/docs/architecture.md` |
| 配置表、模板、只读约束、配置版本 | `packages/akari-bot-core/akaribot/core/docs/config.md` |
| 数据库、union 数据、迁移、热重载 | `packages/akari-bot-core/akaribot/core/docs/database.md` |
| JobQueue 后端、节点、RPC 与信号 | `packages/akari-bot-core/akaribot/core/docs/queue.md` |
| 新建模块、命令解析、hook、权限、工具 | `packages/akari-bot-core/akaribot/core/docs/module-development.md` |
| 消息链、消息元素、等待接口、执行锁 | `packages/akari-bot-core/akaribot/core/docs/message-api.md` |
| 角色与权限判定 | `packages/akari-bot-core/akaribot/core/docs/permissions.md` |
| 新建适配器、Features、ContextManager、多实例 | `packages/akari-bot-core/akaribot/core/docs/adapter-development.md` |
| 公开 API 与版本约束 | `packages/akari-bot-core/akaribot/core/docs/public-api.md` |
| i18n 与占位符 | `packages/akari-bot-core/akaribot/core/docs/i18n.md`、`packages/akari-bot-core/akaribot/core/docs/placeholders.md` |
| 测试框架与用例写法 | `packages/akari-bot-testing/akaribot/testing/docs/index.md`、`packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md` |
| 环境、检查、基准、分支与提交、文档工具链 | `packages/akari-bot-core/akaribot/core/docs/development-workflow.md` |

## 强制规则

- 面向用户的固定文案一律使用 `I18NContext("key", **参数)`，且仅在所属包的 `locales/zh_cn.json` 中创建条目。
  其他语言由 Weblate 提交，不得改动或补充翻译。
- 新增配置字段必须在模板类中声明，并在 `config.comments.<表名>.<字段名>` 中补充注释。
- 模块与适配器仅导入 `akaribot.core.api`（适配器额外导入 `akaribot.core.api.adapters`）。
  核心内部出现循环依赖时通过 `akaribot.core.exports` 处理。
- union 数据按 `union_id` 分组，模型必须声明 `union_scope`。跨表写入同一 union 时使用 `union_mutation()` 与
  `select_for_update()` 包裹事务。
- `Features(...)` 在 `features.py` 创建实例，不在 `ContextManager` 中子类化。
- `SessionInfo` 必须可序列化，仅包含基础类型。构造时传入 `ctx_slot`、`message_id`、`reply_id` 等字段。
- 跨进程通信仅通过 JobQueue 完成。CLI 与 core 之间仅通过子进程交互。
- 全量测试必须设置 `CI=1`，常规测试轮次的失败清单必须与基准按名称一一对应，参见开发流程页。
- 注释、文档与配置说明仅描述当前状态，使用中文书面语并遵守排版检查规则。
- 不擅自提交。新功能分支使用 `dev/` 前缀，修复分支使用 `fix/` 前缀。

## 高频命令

```bash
export UV_CACHE_DIR="$PWD/.uvcache"
uv sync --all-extras --dev
uv run ruff check . && uv run ruff format --check .
uv run python tools/lint_comments.py
uv run python tools/lint_boundaries.py
uv run python tools/lint_versions.py
CI=1 uv run python -m akaribot.testing
uv run python tests/run_one.py packages/akari-bot-core/tests/test_registry.py
```

## 维护

文档页是唯一来源。改动行为后应先更新对应页面，再核对本页路由表是否仍然准确。不要在本技能内重复页面内容。修改本文件后运行：

```bash
uv run python .agents/skills/akaribot-dev/scripts/validate_skill.py
```
