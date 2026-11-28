# AGENTS.md

本文件是开发流程大纲，写明工作顺序与每一步参考的文档。仓库约定按主题分列在 `docs/agents/`，
领域手册是各包的 `docs/` 页面，路由表在 `.agents/skills/akaribot-dev/SKILL.md`。

## 工作流程

### 一、读技能

先读 `.agents/skills/akaribot-dev/SKILL.md`。路由表把任务映射到对应文档页，强制规则列出必须遵守的约束。
任务涉及多个领域时逐个查阅，不要凭记忆写接口。

### 二、确定作用范围

列清楚这次会改动哪些包、哪些源码文件、哪些文档页、哪些用例与 fixture，是否需要新增 locale 条目与
配置注释。跨包改动先确认依赖方向，即模块与适配器仅导入 `akaribot.core.api`，CLI 与 core 仅通过子进程
通信（参见 `docs/agents/architecture.md`）。

范围里有不确定的文件时先搜索确认，不要根据文件名推断。

### 三、规划内容方案

- 行为改动：先用 `grep` 查现有用例，已覆盖就扩展原用例，未覆盖才新增（参见 `docs/agents/testing.md`）。
- 文档改动：确认内容写入哪个页面，包内 `docs/` 与 `docs/agents/` 分工不同，仅写当前状态。
- 方案写到可以直接执行的程度，写明改动哪些文件、按什么顺序修改、用哪些命令验证。涉及多个包或多种文件类型时先说明
  先后顺序，避免中途返工。

### 四、编写内容

开始写之前读同目录的既有写法，保持术语与结构一致。遵守 `docs/agents/conventions.md`：

- 注释解释为什么，不为含义清楚的代码写注释。docstring 仅用于公开接口。
- 文档、注释与配置说明仅描述当前状态，不写“原本是 X，现在改为 Y”这一类对照。
- 面向用户的固定文案使用 `I18NContext`，条目仅写入所属包的 `locales/zh_cn.json`。
- 中文排版：中英文之间留空格，使用全角标点，称呼用户为“你”，机器人自称“机器人”，第三人称用“它”。

写注释与 docstring 时按“注释书写提示词”一节执行。

### 五、文风审核

正文改完以后派发一个子代理专门审文风。它读压缩风格卡，对本次改动的语句逐句核对，仅报告，不修改文件。

派发时按下面的提示词交代：

```text
任务：审核本次改动的中文文风，只报告，不修改文件。

先读 docs/style-cards/akaribot-stylecard.compact.md，按其中的 S1 至 S18 与词表逐句核对。

审核范围：
- git diff --name-only 列出的已跟踪文件；
- 未跟踪的新文件，即 git status --short 中以 ?? 开头的路径；
- 只看本次改动的行及其上下文，不审全文。

审核对象：文档正文、代码注释、docstring、locales/zh_cn.json 中的文案、提交信息草稿。

不评价冻结区：代码块、字符串字面量、表格结构与行列、front matter、组件标签与属性、示例对话、
上游副本与数据文件。

输出每条一行：
文件:行  原句 ⇒ 建议句  [命中：S 编号或词表分节]

同一处问题只报一次，按文件分组。末尾一行写结论：无问题，或需改 N 处。
```

收到报告后逐条判断，采纳的改完仅对改过的行再核对一次，不采纳的写明理由。

### 六、提交前验证

```bash
.venv/bin/ruff check . && .venv/bin/ruff format --check .
.venv/bin/python tools/lint_comments.py
.venv/bin/python tools/lint_boundaries.py
.venv/bin/python tools/lint_versions.py
```

- 五道检查均覆盖整个仓库，任何一项未通过都不提交。
- 全量用例的失败清单与 `tools/test_baseline.txt` 按名称一一对应。
- 包内有源码改动即升级该包 `version`，或在提交信息最后一段写 `Skip-Version: true`、
  `Skip-Version: <包名>[, <包名>]`。
- 修改 `pyproject.toml` 中的 `version` 后必须执行 `uv lock`，让 `uv.lock` 记录的成员版本同步。
- 不擅自提交，改动保留在工作区，等用户检视（参见 `docs/agents/release.md`）。

## 注释书写提示词

写行注释、docstring 与配置注释时，默认按下面的提示词约束草稿。提示词按
`docs/style-cards/akaribot-stylecard.compact.md` 的 S2、S3、S8、S8.1、S9、S11、S13、S17 与词表整理。
细节以该文件为准，其余注释约定参见 `docs/agents/conventions.md`。

```text
任务：为本次改动编写或修改注释。只改注释行，不改代码逻辑、字符串字面量与测试断言。

范围：行注释、docstring、配置注释、常量说明。docstring 仅用于公开接口。

内容
- 解释为什么，不复述代码已写明的动作。含义清楚的代码不写注释。
- 仅描述当前状态，不写“原本是……”“改为……后”“不再……”“暂时”“待补”“后续会”。
- 不解释“不做什么”。确有约束时写成可执行的条件与结果。
- 公开接口的 docstring 只写用途、参数与返回值，不复述签名。
- 配置项注释只描述用途，不写技术细节。
- 常量写清它约束什么，如“单次命令最长等待 5 秒”，不写“超时 5 秒”。
- 不新增未核实的行为、参数或默认值。

句子
- 单条不超过 120 个字符，连续行注释不超过 3 行。写不下就抽取为独立函数，或把说明移到文档页。
- 一句写一件事，不用分号串两句，不用“xxxx：yyyy”说明式冒号。
- 完整中文陈述句的行注释以“。”结尾，不以汉字或英文单词悬空截断。
- 数值与单位之间留空格，如“50 ms”“1000 s”。

用词
- 书面语，不出现“我们”“你”，直陈对象、条件与结果。
- 不用“做/进行 + 动词”，直接用具体动词。
- 排他限制用“仅”，不用“只允许”“只能”“只会”。判断类型或状态写“是否为”。
- 用“必须”“通过”或“由”，不用单字“须”“经”。
- 不压缩成电报体，“落盘”“落库”“未装”“仓库根”按书面语展开。
- 指代当前函数或方法写“该函数”“该方法”，不写“本函数”“本方法”。
- 注释不展开缩写，AST、RPC、ORM 等维护者语境已清楚。
- 内部逻辑注释不泛化称“用户”，按实际客体写“手动键入”“当前输入操作”“弹窗确认”。

格式
- 不加装饰性分隔线，不写“===== 配置 =====”这类分组注释，分组靠文件与函数结构。
- 测试用例 docstring 不用“模块/类: 测试内容”，写成“core.loader 模块加载器测试”。

不写比喻、拟人、感叹号与表情符号。
```

写完后运行 `.venv/bin/python tools/lint_comments.py`，该脚本检查新增与修改的行。机械项由脚本拦截，
语义项在第五步“文风审核”中按压缩风格卡复核。

## 常用命令

```bash
export UV_CACHE_DIR="$PWD/.uvcache"
uv sync --all-extras --dev

.venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_registry.py   # 改动相关的用例
.venv/bin/python -m pytest tests/unit                                               # 单元测试，约 5 秒
CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing   # 全量，约 80 至 100 秒
```

## 文档索引

| 内容 | 位置 |
| --- | --- |
| 环境搭建、命令、检查项、分支与提交 | `packages/akari-bot-core/akaribot/core/docs/development-workflow.md` |
| 领域路由表与强制规则 | `.agents/skills/akaribot-dev/SKILL.md` |
| 包布局、导入边界、CLI 子命令 | `docs/agents/architecture.md` |
| 文档、注释、i18n、TUI、CLI 分工 | `docs/agents/conventions.md` |
| 可自动生成的文档内容与组件 | `docs/agents/generated-content.md` |
| 用例编写与运行 | `docs/agents/testing.md` |
| 已知陷阱 | `docs/agents/pitfalls.md` |
| 提交授权、版本尾注、重命名 | `docs/agents/release.md` |
| 文风卡压缩版（注入用） | `docs/style-cards/akaribot-stylecard.compact.md` |
| 文风卡原版 | `docs/style-cards/akaribot-stylecard.md` |
| 页面结构卡 | `docs/style-cards/akaribot-structure.md` |
| 包文档规范 | `docs/package-docs.md` |
| 从旧版迁移 | `docs/migrating-to-packages.md` |
| 各包领域手册 | `packages/*/akaribot/**/docs/` |
