---
name: akaribot-dev
description: AkariBot 开发指南。用于修改核心框架、消息与会话系统、命令模块、平台适配器、配置、数据库、队列、i18n、测试或项目约定；先读本页路由表，再按领域读取 packages/ 下的文档页。
---

# AkariBot 开发

完整手册是随源码维护的文档页（`packages/*/akaribot/**/doc/`），也是文档站点的内容源。本技能只给
入口与不可越过的规则，不复制页面内容。

## 开始工作

1. 读仓库根 `AGENTS.md`：常用命令、架构脉络、陷阱与提交约定。
2. 按下表找到对应文档页；跨域改动读多页。
3. 改代码前先查 `tests/` 与包内 `tests/` 是否已覆盖该行为。
4. 提交前跑五道门禁，见下方「高频命令」与开发流程页。

## 文档路由

| 任务 | 文档页 |
| --- | --- |
| 代码结构、进程拓扑、启动、退出码、消息链路 | `packages/akari-bot-core/akaribot/core/doc/architecture.md` |
| 配置表、模板、只读约束、配置版本 | `packages/akari-bot-core/akaribot/core/doc/config.md` |
| 数据库、union 数据、迁移、热重载 | `packages/akari-bot-core/akaribot/core/doc/database.md` |
| JobQueue 后端、Peer、RPC 与信号 | `packages/akari-bot-core/akaribot/core/doc/queue.md` |
| 新建模块、命令解析、hook、权限、工具 | `packages/akari-bot-core/akaribot/core/doc/module-development.md` |
| 消息链、消息元素、等待接口、执行锁 | `packages/akari-bot-core/akaribot/core/doc/message-api.md` |
| 角色与权限判定 | `packages/akari-bot-core/akaribot/core/doc/permissions.md` |
| 新建适配器、Features、ContextManager、多实例 | `packages/akari-bot-core/akaribot/core/doc/adapter-development.md` |
| 公共 API 面与版本约束 | `packages/akari-bot-core/akaribot/core/doc/public-api.md` |
| i18n 与占位符 | `packages/akari-bot-core/akaribot/core/doc/i18n.md`、`packages/akari-bot-core/akaribot/core/doc/placeholders.md` |
| 测试框架与用例写法 | `packages/akari-bot-testing/akaribot/testing/doc/index.md`、`packages/akari-bot-testing/akaribot/testing/doc/writing-tests.md` |
| 环境、门禁、基线、分支与提交、文档工具链 | `packages/akari-bot-core/akaribot/core/doc/development-workflow.md` |

## 强制规则

- 面向用户的固定文案用 `I18NContext("key", **参数)`，只在所属包 `locales/zh_cn.json` 建节点；其他
  语言由 Weblate 提交，不得改动或补译。
- 新增配置字段须在模板类声明，并在 `config.comments.<表名>.<字段名>` 补注释。
- 模块与适配器只导入 `akaribot.core.api`（适配器另加 `akaribot.core.api.adapters`）；核心内部出现
  循环依赖时经 `akaribot.core.exports` 处理。
- union 数据以 `union_id` 归属，模型声明 `union_scope`；跨表写同一 union 用 `union_mutation()` 与
  `select_for_update()` 包住事务。
- `Features(...)` 在 `features.py` 建实例，不在 `ContextManager` 子类化。
- `SessionInfo` 必须可序列化，只放基础类型；构造时传齐 `ctx_slot`、`message_id`、`reply_id` 等字段。
- 跨进程只经 JobQueue；CLI 与 core 之间只经子进程。
- 全量测试用 `CI=1`，普通轮次的失败集合必须与基线逐名一致，见开发流程页。
- 注释、文档与配置说明只描述当前状态，用中文书面语并遵守排版门禁。
- 不擅自 commit；新功能分支用 `dev/`，修复用 `fix/`。

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

文档页是唯一真源。改动行为后先更新对应页面，再回看本页路由是否仍然准确；不要在本技能内重复页面
内容。修改本文件后运行：

```bash
uv run python .agents/skills/akaribot-dev/scripts/validate_skill.py
```
