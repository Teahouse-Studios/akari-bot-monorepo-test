# 工作流与风格

## 目录

- [包布局与导入边界](#包布局与导入边界)
- [测试](#测试)
- [导入与注释](#导入与注释)
- [只描述当前状态](#只描述当前状态)
- [中文排版](#中文排版)
- [本地化](#本地化)
- [新增模块包](#新增模块包)
- [提交](#提交)

## 包布局与导入边界

- `packages/akari-bot-core/`：`akaribot.core`（运行时与公共设施）+ `akaribot.modules.core`（内置模块）。
- `packages/modules/akari-bot-module-<名>/`：`akaribot.modules.<名>`；`packages/adapters/akari-bot-adapter-<名>/`：`akaribot.adapters.<名>`。
- `packages/akari-bot-testing/`：`akaribot.testing`（测试框架）；`packages/akari-bot-cli/`：`akaribot.cli`（**不依赖 core**）。
- `packages/akari-bot-assets-<类>/`：字体、表情、品牌资产；`akaribot.assets.<类>` 只暴露一个定位函数。
- `akaribot`、`akaribot.modules`、`akaribot.adapters`、`akaribot.assets` 是 PEP 420 命名空间目录，
  **不得**放 `__init__.py`。
- 模块只 import `akaribot.core.api` 的公共面；适配器另有 `akaribot.core.api.adapters`；模块包之间不得互相依赖。
- 每个包在自己的导入包目录下有 `manifest.toml`，locales/assets/migrations 相对它解析。
- CLI 与 core 只经子进程：`python -m akaribot.core.entrypoints.{run,registry,config,db,peers,modules,rpc}`。

## 测试

- 用例随包归位：`packages/*/tests/`、`packages/*/*/tests/`；跨包用例在 `tests/unit/`、`tests/integration/`。
- 全量：`CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing`（约 80~100 秒）。
  `CI=1` 必需，否则无 Expectation 的用例会挂起；根目录 `tester.py` 是等价的兼容层。
- 单文件/单入口：`.venv/bin/python tests/run_one.py <包内用例路径> [入口名]`。
- 全量失败集合须与基线**逐名一致**：`tools/test_baseline.txt`（普通轮）与
  `tools/test_baseline_readonly.txt`（只读包目录轮），用 `tools/check_test_baseline.py` 对拍。
  新增、消失或错误文本变化都判失败；既有失败修好后必须同步缩小基线。

## 导入与注释

### 导入

按标准库、第三方库、项目内部模块分组导入，组间空一行。

模块包与适配器包只从门面导入：`from akaribot.core.api import ...`，适配器另可用
`from akaribot.core.api.adapters import ...`。不得写 `akaribot.core.builtins.*` 这类深路径
（门禁 B8 以 warn 记录），也不得让模块 import `akaribot.adapters.*`（B2）或
`akaribot.core.api.adapters`（B3）。包内跨模块引用用相对导入。

遇到核心循环依赖时使用 `akaribot.core.exports` 的导出机制，不要仅靠调整导入顺序掩盖问题。

### 注释总则

**注释解释「为什么」，不复述「做了什么」。** 判据只有一条：删掉这条注释，读代码的人会不会失去某个
从代码本身读不出来的信息？不会，就删掉。

值得写的信息只有四类：

1. **约束**——为什么必须是这个顺序、这个位置、这个类型；
2. **原因**——为什么不用那个更显然的写法；
3. **陷阱**——这里改动会在别处以什么方式出错；
4. **外部契约**——平台 API、协议、数据库的行为约定。

### 硬性规则

| # | 规则 | 说明 |
| --- | --- | --- |
| 1 | 行注释控制在**一行**以内 | 上限 120 字符（含缩进），与 Ruff 的 `line-length` 一致；确需展开的写入 docstring |
| 2 | 不使用第一/第二人称 | 陈述事实，不对读者说话。「先取锁」而非「这里我们先取锁」 |
| 3 | 不使用语气词与情绪标点 | 吧、呗、啦、嘛、哦、呢；`!`、`?!`、`……` |
| 4 | 不使用口语词 | 搞／弄→处理、设置；踩坑／炸了／挂了→失败、中断、异常；懒得／反正／干脆→删除该句 |
| 5 | **不复述代码** | `# 返回本地路径` 配 `return self.path` 属于噪音，删除 |
| 6 | **不新增装饰性分隔注释** | `# ===== 步骤 3 =====`、`# ---- 标题 ----` 一律不写；需要分段时拆函数，或用 docstring 的结构化段落 |
| 7 | 不写流水账 | 「先……然后……最后……」属于 docstring 的职责，不属于行注释 |
| 8 | 不留时间性表述 | 「暂时」「先这样」「以后再改」；确有待办写 `# TODO(#<issue 号>): <一句话>` |
| 9 | **不叙述变更** | 不写「原本是 X，现在改为 Y」；见下一节 |
| 10 | 沿用中文排版 | 中英文之间加空格、全角标点、专有名词正确大小写（GitHub、Minecraft、SQLite） |
| 11 | **非公开 API 不写 docstring** | 名字以 `_` 开头的函数与类不写 docstring，其说明归行注释；双下划线方法实现语言协议，属公开面 |

行注释块**连续不超过三行**（四行起 `R7` 警告）；整条注释用中文书面语。

### 正例与反例

```python
# 反例：复述代码
# 创建类型转换器实例
converter = Converter()

# 正例：删除该注释，代码自解释
converter = Converter()
```

```python
# 反例：口语、多行、情绪
# 这里千万别改成先 mkdir！之前踩过坑，
# 导入的时候就建目录会让只想读个版本号的调用也在当前目录拉一坨文件夹……

# 正例：一行，陈述约束与原因
# 目录创建须惰性执行：导入期建目录会使只读取版本号的调用也在 cwd 产生副作用。
```

```python
# 反例：装饰性分隔 + 流水账
# ========== 步骤 3: 收集可能匹配的别名 ==========
# 先看第一个词是不是模块名，然后决定检查范围，最后取最长匹配

# 正例：说明并入 docstring，行注释只保留读不出的判据
# 首词为模块名时仅检查该模块的别名，避免跨模块误匹配。
```

```python
# 反例：时间性表述
# 暂时先这么写，等 registry 做好了再改

# 正例
# TODO(#2210): registry 就绪后改为按 entry point 解析。
```

```python
# 反例：叙述变更
# 旧实现按 provides_modules 猜文件名，那条路径下永远没有文件，现改为按 config_table 定位。

# 正例：只陈述当下的事实与约束
# 配置文件按 manifest.config_table 定位：CFGManager.load() 只扫描 config/*.toml。
```

### 可执行检查

`tools/lint_comments.py` 是这条规范的可执行部分，与 Ruff 同级在 CI 必过。检查范围含行注释与
docstring；docstring 里的示例代码行、整行不含中文的外部引用文本、行内代码与 URL 不适用排版规则。

- **error**：行注释或 docstring 超过 120 字符、口语词、语气词与情绪标点、第一/第二人称、
  装饰性分隔注释、**叙述变更**、中文里的半角标点、中英文之间缺失的空格、**非公开符号带 docstring**；
- **warn**：时间性表述、连续 4 行以上的行注释块；
- **豁免**：`# noqa`、`# type:`、`# skipcq`、`# ruff:`、`# fmt:` 等工具指令注释；
  内嵌的第三方副本（`packages/akari-bot-html2text/`）与移植代码的原始文档整体不在约束内；
- **基线**：既有违规记录在 `tools/comment_lint_baseline.txt`；`--diff <ref>` 只检查该基准之后新增与修改的行。
  基线随清理逐步缩小，只禁止新增，不要求一次性清理；清理掉一批后用 `--generate-baseline` 重建。

```bash
.venv/bin/python tools/lint_comments.py              # 全量
.venv/bin/python tools/lint_comments.py --diff HEAD~1  # 只查新增与修改行
```

## 只描述当前状态

文档、注释和配置说明只描述当前状态，不记录「从前如何」。不写「原本是 X，现在改为 Y」「已迁移到 Z」
「不再使用 W」这类对照式表述，直接陈述当下的事实与约束；变更历史由 git 承载。需要解释设计取舍时，
说明当前为何如此，而不是叙述它从什么演变而来。

**例外**：为迁移历史数据而保留的兼容逻辑（旧配置表名、数据库版本升级路径、退役客户端的数据迁移）
应当保留，并注明适用范围——这类兼容是当前行为的一部分。标注某个 API 已弃用同样属于陈述当前状态。

这条规则同时约束提交信息、`AGENTS.md`、技能文档与代码注释。

## 中文排版

- 中英文之间加空格，但链接前后不额外加空格。
- 使用全角中文标点；简体中文使用弯引号“”。
- 专有名词保持正确大小写，如 GitHub、Minecraft、JavaScript、SQLite。
- 称呼用户使用“你”，不用“您”。
- 机器人自称避免“我”，使用“机器人”；第三人称使用“它”。
- 尽可能避免第一人称描述。

这些规则适用于 `zh_cn.json` 中所有面向用户的文案，也适用于注释、文档与提交信息。

## 本地化

只允许手工编辑各包 `locales/` 下的 `zh_cn.json`，其余语言由 Weblate 自动提交——**即使缺少新键也不要
复制简体中文或自行翻译**，也不要删除或补齐既有语言文件。配置模板由各包的 `config.py` 与 locale 注释
派生，`akaribot config schema --table <表名>` 可查看某个表的全部键与注释；配置字段注释写在
`locales/zh_cn.json` 的 `config.comments.<表名>.<字段名>`，只描述用途，不描述技术细节。

插值语法是 `${name}`；占位符名不得与 `i18n.t()` 的形参同名。

## 新增模块包

```
akaribot new module <名>        # 交互问卷；或 --non-interactive 配合逐项参数
akaribot module add -e .
```

生成后核对：只用 `akaribot.core.api`；locale 只提交 zh_cn 且键名前缀与模块名一致；对 core 的约束
字面必须是 `akari-bot-core>=0.1.0,<1.0`（`tools/lint_versions.py` 检查）；迁移可重复执行；包内不得
出现 `akaribot/__init__.py`。详见 `CONTRIBUTING.md` 的「新增模块包」。

## 提交

- **不要擅自 commit**：改动留在未提交的工作区，交由用户检视与提交；`git add`、`git push`、
  `git reset`、`git checkout -- <file>` 同样需要用户授权，且授权仅对当次请求有效。
- 中文书面语提交信息，正文写清证据（实跑输出、失败集合对比、门禁结果）。
- 移动文件用 `git mv`；根目录同时保留同名兼容层时 git 不记为 rename，需「先纯移动、再改内容」两段提交。
- 版本守卫要求包内有源码改动即升 `version`，或在提交信息**最后一段**写独立的
  `Skip-Version: true` / `Skip-Version: <分发名>[, <分发名>]` trailer。
