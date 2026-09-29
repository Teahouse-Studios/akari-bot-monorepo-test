# AGENTS.md

本文件面向在本仓库工作的 AI 代理与协作者。仓库是 uv workspace：core、模块、适配器各自独立发包，
运行时靠 entry points 发现。

## 深入文档

`.agents/skills/akaribot-dev/SKILL.md` 是本仓库的完整开发手册（架构详解、模块开发、平台适配器、
i18n 规范等）。**本文件只记录高频命令、跨文件才能看清的架构脉络与强制约定**；需要 API 细节时读
那份技能文件，不要重复其内容。

## 常用命令

```bash
export UV_CACHE_DIR="$PWD/.uvcache"      # 缓存与 venv 都在工作区内，安装无需额外权限
uv sync --all-extras --dev               # 重建环境（口径与 CI 的 --locked --all-extras --dev 一致）

CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing   # 全量，约 80~100 秒
.venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_registry.py               # 单个用例文件（包内路径）
.venv/bin/python tester.py                                                                     # 兼容层，等价于模块入口

.venv/bin/ruff check . && .venv/bin/ruff format --check .
.venv/bin/python tools/lint_comments.py      # 注释书面语、块长与文字排版
.venv/bin/python tools/lint_boundaries.py    # 分层、命名空间、依赖声明、B11
.venv/bin/python tools/lint_versions.py      # 内部版本约束一致性
```

CLI：`.venv/bin/akaribot <子命令> --help`（init / run / test / module / config / adapter / db /
instance / service / venv / logs / doctor / new / tui / migrate）。`migrate legacy` 把旧版布局的部署
搬进新实例目录；`logs` 读实例的日志文件（界面日志页与它共用解析规则）。

## 架构脉络

```
packages/
  akari-bot-core/        akaribot.core（运行时与公共设施）+ akaribot.modules.core（内置模块）
  akari-bot-testing/     akaribot.testing（自研测试框架与运行器）
  akari-bot-cli/         akaribot.cli（实例管理 CLI 与 TUI，**不依赖 core**）
  akari-bot-html2text/   html2text（独立分发的内嵌副本）
  akari-bot-assets-*/    字体、表情、品牌资产，各自一个分发
  modules/…              akaribot.modules.<名>，各自一个分发
  adapters/…             akaribot.adapters.<名>，各自一个分发
```

- `akaribot`、`akaribot.modules`、`akaribot.adapters`、`akaribot.assets` 是 **PEP 420 命名空间目录**
  （不得有 `__init__.py`）；`akaribot.core`、`akaribot.testing`、各模块/适配器/资源包是常规包。
- 包发现走 entry points（`akaribot.modules` / `akaribot.adapters`），目录扫描只是兜底；每个包在
  自己的导入包目录下有 `manifest.toml`，locales、assets、migrations 都相对它解析。
- 模块只应 import `akaribot.core.api` 的公共面；适配器另有 `akaribot.core.api.adapters`。
- CLI 与 core 之间**只经子进程**：`python -m akaribot.core.entrypoints.{run,registry,config,db,peers,modules,rpc}`。

## 项目约定

### 只描述当前状态

- **文档、注释和配置说明只描述当前状态，不记录「从前如何」。** 不写「原本是 X，现在改为 Y」
  「已迁移到 Z」「不再使用 W」这类对照式表述，直接陈述当下的事实与约束。
- 变更历史由 git 承载。需要解释设计取舍时，说明当前为何如此，而不是叙述它从什么演变而来。
- **例外**：为迁移历史数据而保留的兼容逻辑（旧配置表名、数据库版本升级路径、退役客户端的数据
  迁移）应当保留，并注明适用范围——这类兼容是当前行为的一部分。标注某个 API 已弃用同样属于
  陈述当前状态，可以保留。

### 注释

- **不要给自明的代码写注释。** 注释解释「为什么」，不解释「是什么」或实现细节；只在逻辑涉及
  反直觉的边界情况、hack、复杂算法或特定业务规则时才写。
- **单条注释一般不超过三行。** 写不下说明该抽函数或补文档，不要在代码里堆长篇说明。
- **一律使用正式书面语**，不得出现口语化表达、语气词、感叹号或调侃。
- **不要给非公开 API 的模块、类、函数加 docstring。** 公开 API 的 docstring 只写用途、参数与
  返回值，不复述签名已经表达的信息。

### 文档

- 文档面向技术用户与维护者，不面向初学者。
- 只覆盖功能概述、基本使用步骤和接口实现，不逐步讲解内部工作原理。

### i18n 与本地化

- **i18n 强制**：面向用户的固定文案一律 `I18NContext("key", **参数)`，只在所属包的
  `locales/zh_cn.json` 建节点。插值语法是 `${name}`，占位符名不得与 `t()` 的形参同名。
- **本地化文本只写简体中文。**
- **禁止改动其他语言文件**：除非用户明确要求处理翻译或 Weblate 同步结果，不得创建、修改、删除
  或补齐任何包内 `locales/` 下 `zh_cn.json` 以外的语言 JSON。其他语言由 Weblate bot 自动提交，
  **即使缺少新键也不要复制简体中文或自行翻译**。`assets/config_store/<语言>/` 是配置模板派生物，
  非 `zh_cn` 版本同样交给自动化生成。
- **新增配置字段必须补注释**：字段在模板类里声明（`akaribot/core/config/decorator.py` 的
  `@on_base_config` / `@on_config` / `@on_bot_config` / `@on_module_config`），同时在模板所属包的
  `zh_cn.json` 里加 `config.comments.<表名>.<字段名>`。表名随装饰器而定（`config` / `secret` /
  `bot_<平台>` / `module_<模块>`，`secret=True` 时带 `_secret` 后缀）。
- **配置项注释视作文档**：只描述该项的用途，不描述技术细节。

### TUI 键位与交互

- **破坏性动作不用单字母键，且必须弹模态确认。** 删除、移除、清数据一类动作走 `ctrl+<字母>`
  或专用字母键（卸载用 `u`）；不可逆动作（清空实例数据、重建 venv、迁移旧项目）额外要求
  **打字确认**或「先预演」。
- **单字母键只留给浏览与无副作用的切换**（`r` 刷新、`/` 搜索、`space` 选择、`n`/`p` 翻页等）。
  `d` 只保留给无害动作（日志页切换 debug）。
- **确认一律弹模态框**：不再用状态栏「再按一次 X 确认」——它既容易被鼠标双击与键盘连发穿透，
  也让人看不清将改动什么。弹框前过 `_compat.PendingConfirm.accept(key)`：防抖窗口内忽略连发，
  避免叠出两层模态。切页、刷新、换选中项调用页面的 `reset_pending()` 复位。
- **页脚只放高频键位**：低频与危险动作在 `compat.bindings()` 里用四元组第 4 项 `False` 隐藏，
  由按钮或页内提示承载；80 列下页脚不得溢出。

### CLI 与 TUI 的分工

- **写操作一律经 `akaribot <子命令>` 子进程**（界面用已有的 `--yes` 代答确认）：CLI 是唯一写入口，
  参数、校验与确认只有一份。进程内直写会让命令层的前置校验在界面上失效。
- **读操作允许进程内直读**，但限于不含业务判断的本机状态：注册表、锁文件、日志文件、`akaribot.toml`。
  需要 core 参与判断的读取（配置 schema、数据项、模块清单、体检）一律经子进程。
- **界面不得拥有 CLI 没有的能力**：新增界面功能前先问「对应的命令是什么」，没有就先补命令；
  日志页的解析规则因此在 `akaribot/cli/logs.py`，界面复用它。

### 版本控制

- **不要擅自 commit。** 所有改动留在未提交的工作区，交由用户自行检视与提交。
- 除非用户明确授权自动提交，否则不执行 `git commit`；`git add`、`git push`、`git reset`、
  `git checkout -- <file>` 等会改动暂存区、历史或丢弃工作区内容的操作同样需要用户授权。
- 授权仅对当次请求有效，不要据此推定后续改动也可以自动提交。
- 新功能分支用 `dev/`，修复分支用 `fix/`，分支名使用英文。

### 其他

- 提交信息使用中文书面语，正文写清**证据**（实跑输出、失败集合对比、门禁结果）。
- 移动文件用 `git mv` 以保住 blame；根目录同时保留同名兼容层时 git 不记为 rename，需要
  「先纯移动、再改内容」两段提交。
- 全量测试的失败集合须与基线**逐名一致**（`tools/test_baseline.txt`，用
  `tools/check_test_baseline.py` 对拍）。
- 内部依赖约束必须**字面一致**（`akari-bot-core>=0.1.0,<1.0`）；官方模块包之间不得互相依赖。

## 陷阱

以下均为当前必须遵守的约束，改动相关代码时请勿回退：

- `akaribot/testing/__init__.py` **不得静态导入 `.tester`**：会牵出 core，使合并日志目录在隔离
  环境变量就位之前被固化到仓库 `data/`。公开名按需解析。
- 惰性公开面里**不得引入同名辅助名**：`from typing import Any` 会经
  `from akaribot.testing import Any` 遮住框架自己的 `Any` 匹配器（辅助名一律下划线开头）。
- 根 `bot.py` / `tester.py` 兼容层用 `sys.modules` **模块别名**，不要逐名再导出——用例会给模块级
  变量赋值再由同模块函数读取，逐名再导出时赋值落在兼容层上。
- `CFGManager.load()` 只扫描 `config/*.toml`：适配器实例配置必须写**扁平路径**
  （`config/<表名>.toml`）；写到 `config/adapters/` 的表对 core 不可见。
- `config set` 需按模板声明的类型转换，否则布尔项会被写成字符串 `"true"`；实例表名
  （`bot_telegram-alt`）由基表（`bot_telegram`）派生，查声明时要按前缀匹配。
- **Nuitka 冻结后 `sys.executable` 指向二进制自身**：CLI 包内禁止用它启动实例进程（门禁 B11），
  解释器一律经 `akaribot.cli.instance.system_python()`。
- Textual：页面自有方法/属性**不得占用基类名**（`_render`、`offset` 等，覆盖 `Widget._render()`
  会让容器 visual 为 `None`）；切页后要把焦点交给该页，否则页级键位不生效；隐藏页要跳过定时轮询。
- `i18n.t()` 的**占位符名不得与形参同名**：`${key}` 配 `t(key=…)` 会抛
  `TypeError: t() got multiple values for argument 'key'`；占位符与实参一律用语义名
  （`${field}` / `field=`），改键后跑一次「调用点关键字 ↔ 模板占位符」对拍。
- 注释门禁会拦：装饰性分隔注释、连续 3 行以上的行注释块、对照式表述、中文里的半角标点与
  中英文之间缺失的空格。
- 品牌资产（立绘、标志、制作人员名单）是画师提供的原件，**不得为压体积重新编码**；
  它们随 `akari-bot-assets-brand` 分发，属 core 的 `full` extra，缺失时使用侧降级而不是报错。
- `uv.lock` 是单一真源：workspace 覆盖会丢弃内部约束，只有从 wheel 安装才走真解析器
  （`tools/clean_room_check.py` 负责这条）。

## 提交与验证约定

- 版本守卫（`tools/check_versions.py`）要求包内有源码改动即升 `version`，或在提交信息**最后一段**
  写独立的 trailer：`Skip-Version: true` 豁免全部成员，`Skip-Version: <分发名>[, <分发名>]` 只豁免
  列出的成员。正文中间或缩进提到该 token 不算声明。
- 版本守卫由 CI 在 PR 阶段以 base 为基准运行，**不属于日常五道门禁**；本分支是整体重构，以
  `master` 为基准时各包都是新增成员，以拆分后某提交为基准时会报出未升版本包。发布前逐包升
  `version` 或写 trailer，不要为让它变绿而放宽守卫。
