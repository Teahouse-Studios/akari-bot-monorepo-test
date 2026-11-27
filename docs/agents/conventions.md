# 项目约定

本文记录文档、注释、文案与界面层必须遵守的约定。命令与提交细则参见
`packages/akari-bot-core/akaribot/core/docs/development-workflow.md`。

## 仅描述当前状态

- 文档、注释和配置说明仅描述当前状态，不记录“从前如何”。不写“原本是 X，现在改为 Y”
  “已迁移到 Z”“不再使用 W”这类对照式表述，直接陈述当下的事实与约束。
- 变更历史由 git 记录。需要解释设计取舍时，说明当前为何如此，而不是叙述它从什么演变而来。
- 例外：为迁移历史数据而保留的兼容逻辑（旧配置表名、数据库版本升级路径、退役客户端的数据迁移）
  应当保留，并注明适用范围。这类兼容属于当前行为的一部分。标注某个 API 已弃用同样属于陈述当前状态，可以保留。

## 注释

- 不要为含义清楚的代码编写注释。注释解释“为什么”，不解释“是什么”或实现细节。仅在逻辑涉及
  容易引起误解的边界情况、hack、复杂算法或特定业务规则时才写。
- 单条注释一般不超过三行。若三行无法容纳，说明应当抽取为独立函数或补充文档，不要在代码里堆叠长篇说明。
- 一律使用正式书面语，不得出现口语化表达、语气词、感叹号或调侃。
- 不要为非公开 API 的模块、类、函数添加 docstring。公开 API 的 docstring 仅说明用途、参数与返回值，
  不复述签名已经表达的信息。

## 文档

- 文档面向技术用户与维护者，不面向初学者。
- 仅覆盖功能概述、基本使用步骤和接口实现，不逐步讲解内部工作原理。

## 包文档与文档站点

- 每个包的导入包目录下带有 `docs/`，其中 `docs/config/global/docs.global.toml` 声明标题、简介与排序，
  `docs/config/docs.toml` 可覆盖默认值，Markdown 页面仅记录当前行为。在 pyproject 的
  `[project.entry-points."akaribot.docs"]` 声明 `<key> = "<import path>"`。第三方包以同一种方式接入，
  目录仅包含已安装的包。
- `akaribot docs list|build|sync-theme|install-deps|serve|dev|deploy|status|clean`。工具链要求由主题清单确定，内置主题与
  `akari-bot-docs-template` 各自在 `docs-theme.json` 中声明 Node.js 与 VitePress 版本范围。
  生成产物在实例 `cache/docs/`，构建与部署记录在 `.docs/state.json`。
- 站点配置保存在实例根目录的 `docs.toml` 中。主题使用 `[theme].source` 选择，外部主题仅通过根目录的
  `docs-theme.json` 声明主题目录、依赖、VitePress/Node 要求与生成配置选项，引擎不导入主题代码。
  本仓库的主题是 `vendor/akari-bot-docs-template` submodule，克隆后必须初始化 submodule。
  部署登录信息仅从环境变量读取，不写入配置、日志或状态文件。
- 文档仅使用简体中文，并仅描述当前状态。命令、配置字段与默认值以源码为准。跨包链接可填写源码相对路径，
  生成器会转换为站点 URL。
- 模块页的属性卡来自 `docs/config/global/docs.global.toml` 的 `[[meta.modules]]`，由生成器自动注入。
  `ModuleMeta`、`NoticeBox`、`CommandUsage` 组件的正式位置是 `akari-bot-docs-template`，
  内置主题保留同名回退实现。正文仍以 Markdown 为主。
- 能被源码唯一确定的内容由构建期组件渲染，例如命令选项、配置字段与适配器能力。正文仅保留解释与适用条件，
  可计算内容由组件渲染。判定标准、数据通道与组件清单参见 `docs/agents/generated-content.md`。

## i18n 与本地化

- i18n 强制：面向用户的固定文案一律使用 `I18NContext("key", **参数)`，仅在所属包的
  `locales/zh_cn.json` 中创建条目。插值语法是 `${name}`，占位符名称不得与 `t()` 的形参同名。
- 本地化文本仅使用简体中文。
- 禁止改动其他语言文件：除非用户明确要求处理翻译或 Weblate 同步结果，不得创建、修改、删除或补充任何
  包内 `locales/` 下 `zh_cn.json` 以外的语言 JSON。其他语言由 Weblate bot 自动提交，
  即使缺少新增的键也不要复制简体中文或自行翻译。`assets/config_store/<语言>/` 由配置模板生成，
  非 `zh_cn` 版本同样交给自动化生成。
- 新增配置字段必须补充注释：字段在模板类中声明（`akaribot/core/config/decorator.py` 的
  `@on_base_config` / `@on_config` / `@on_bot_config` / `@on_module_config`），同时在模板所属包的
  `zh_cn.json` 中补充 `config.comments.<表名>.<字段名>`。表名随装饰器而定（`config` / `secret` /
  `bot_<平台>` / `module_<模块>`，`secret=True` 时带 `_secret` 后缀）。
- 配置项注释视作文档：仅描述该项的用途，不描述技术细节。

## TUI 键位与交互

- 破坏性操作不使用单字母键，且必须弹出模态确认框。删除、移除、清空数据一类操作使用 `ctrl+<字母>`
  或专用字母键（卸载使用 `u`）。不可逆操作（清空实例数据、重建 venv、迁移旧项目）额外要求打字确认
  或“先试运行”。
- 单字母键仅留给浏览与无副作用的切换（`r` 刷新、`/` 搜索、`space` 选择等）。有副作用的单字母键必须先
  弹出确认框。
- 确认操作一律弹出模态框，不使用状态栏“再按一次 X 确认”，该方式既容易被鼠标双击与键盘重复按键误触发，
  也无法让用户看清将要改动的内容。弹出确认框前通过 `_compat.PendingConfirm.accept(key)` 校验，
  防抖窗口内忽略连续触发，避免连续叠加两层模态框。切换页面、刷新、更换选中项时调用页面的
  `reset_pending()` 重置状态。
- 页脚仅显示高频快捷键：低频与危险操作在 `compat.bindings()` 中用四元组第 4 项 `False` 隐藏，
  转为通过按钮或页内提示展示，80 列宽度下页脚不得溢出。
- 键位遵循统一语法（表参见 `akaribot/cli/tui/README.md`“键位语法”），相同含义的操作在各页面仅使用
  同一个键，调整页面键位时不得另起新义。按钮文字通过 `compat.key_hint()` 附带快捷键提示。
  低频操作收入 `m` 菜单，不占用按钮栏。

## CLI 与 TUI 的分工

- 写入操作一律通过 `akaribot <子命令>` 子进程执行，界面使用已有的 `--yes` 自动确认。CLI 是唯一的
  写入入口，从而保证参数解析、校验与确认逻辑仅保留一份。进程内直接写入会导致命令层的前置校验在界面上失效。
- 读取操作允许在进程内直接读取，但限于不含业务判断的本机状态（注册表、锁文件、日志文件、`akaribot.toml`）。
  需要 core 参与判断的读取操作（配置 schema、数据项、模块清单、环境体检）一律通过子进程执行。
- 界面不得拥有 CLI 没有的能力：新增界面功能前先确认“对应的命令是什么”，若不存在则先补充命令。
  日志页的解析规则因此在 `akaribot/cli/logs.py`，界面复用它。

## 代码风格与其他约束

- Ruff：行宽 120、双引号，忽略 E402、F405、F403、E741、E721。
- 中文排版：中英文之间增加空格，使用全角标点，称呼用户统一为“你”（不使用“我”），机器人自称统一为“机器人”，
  第三人称统一为“它”。
- 默认命令前缀 `~` / `～`。
- 获取时间统一使用 `akaribot.core.utils.timezone` 或 `SessionInfo.now()`、`today()`，业务代码中不得
  直接使用 `datetime.datetime.now()`、`date.today()`、`time.localtime()`。面向用户展示使用
  `msg.format_time()` 或 `FormattedTime`。
- 注释检查会拦截：装饰性分隔注释、连续 3 行以上的行注释块、对照式表述、中文里的半角标点与
  中英文之间缺失的空格。
