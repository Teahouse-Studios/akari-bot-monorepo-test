# 模块开发

## 目录

- [核心原则](#核心原则)
- [模块包、模块与三级启用](#模块包模块与三级启用)
- [创建模块包](#创建模块包)
- [包元数据与包内清单](#包元数据与包内清单)
- [导入边界](#导入边界)
- [本地化文件](#本地化文件)
- [基本结构与最小示例](#基本结构与最小示例)
- [命令模板详解](#命令模板详解)
- [正则匹配](#正则匹配)
- [权限控制](#权限控制)
- [模块配置](#模块配置)
- [数据库模型](#数据库模型)
- [定时任务](#定时任务)
- [模块钩子](#模块钩子)
- [国际化（i18n）](#国际化i18n)
- [主动发送消息](#主动发送消息)
- [冷却、花瓣与游戏状态](#冷却花瓣与游戏状态)
- [等待用户交互](#等待用户交互)
- [模块测试](#模块测试)
- [常见开发任务速查](#常见开发任务速查)

修改模块配置或数据库模型时，同时读取 `infrastructure.md`。修改 `MessageSession`、消息元素或
parser 行为时，同时读取 `messaging-and-parser.md`。测试规则只以 `testing.md` 为准。包与适配器的
分发形态见 `architecture.md`。

---

## 核心原则

> **国际化优先**：模块内不编写面向用户的纯文本消息，所有面向用户的文本使用 `I18NContext`
> 组件。编写代码时只在对应模块包的 `locales/zh_cn.json` 添加或修改本地化节点；简体中文是基础
> 语言。
>
> 例外情况：调试日志、内部逻辑字符串等不面向用户的场景可使用纯文本。
>
> **翻译文件归属**：除非用户明确要求处理翻译或 Weblate 同步结果，否则禁止创建、修改、删除或
> 机械同步任何包 `locales/` 目录下 `zh_cn.json` 以外的语言 JSON，包括 `en_us.json`、
> `zh_tw.json`、`ja_jp.json`、`ko_kr.json` 等。其他语言由 Weblate 及其 bot 自动提交；即使现有
> 翻译缺少新键，也只更新 `zh_cn.json`，不要复制简体中文或自行翻译补齐。
>
> **导入面**：模块代码从 `akaribot.core.api` 取用公共设施，不引用 `akaribot.core` 的内部路径，
> 不引用 `akaribot.adapters.*`，也不引用 `akaribot.core.api.adapters`。规则细节与检查工具见
> 「导入边界」。
>
> **包与模块的对应**：一个模块包可以注册多个模块（`module()` 的注册名），模块名是命令前缀、
> locale 键前缀与配置表名后缀；包名是分发单位，取 `akari-bot-module-<名>`。热重载、安装与卸载
> 都以包为单位。

---

## 模块包、模块与三级启用

拆包之后，一个概念的三个层次必须分开理解，混用会得到错误的排查方向：

| 层次 | 载体与判据 | 操作方式 |
|------|-----------|----------|
| 安装 | 实例 venv 中的 distribution，决定代码是否存在 | `akaribot module add` / `remove` / `update` |
| 全局装载 | `module_status.load`，决定模块是否参与命令匹配 | `akaribot module load` / `unload`；机器人内 `~module load` / `unload`（超级用户） |
| 场景启用 | 场景的 `enabled_modules`，决定某个群或频道能否使用 | 机器人内 `~module enable` / `~module disable`（场景管理员） |

模块之外的**运行库**（httpx 这类依赖或自己加的第三方包）走环境页与 `akaribot venv add` /
`venv remove`：`--save` 记进实例清单的 `runtime.requirements`，环境重建时按它补装，`--no-save`
只装进当前环境。`venv status --json` 的 `installed` 是环境里的全部分发，`packages` 只是其中的
AkariBot 包。

命令行的 `akaribot module` 子命令组不使用 `enable` / `disable` 表示全局装载，这两个词在 CLI 中
只对应场景级开关。三级的完整命令：

```
akaribot module list                    # 列出已安装的模块与适配器
akaribot module add <模块名>             # 安装；解析 → 预检 → 安装 → 补配置 → 迁移 → 热装载 → 报告
akaribot module add -e <本地包目录>      # 以可编辑方式安装本地目录，开发期使用
akaribot module remove <模块名>          # 卸载；默认保留配置与数据，并做反向依赖检查
akaribot module update <模块名> | --all  # 更新已安装的包
akaribot module load <模块名>            # 全局装载：让它参与命令匹配
akaribot module unload <模块名>          # 全局卸载：退出命令匹配，代码与配置都保留
```

`remove` 的 `--purge-data` 会连带删除该包的数据表与配置文件，清理范围取自包内 `manifest.toml`
的 `owned_tables` 与 `config_table`，因此新增数据表后必须把表名补进 `owned_tables`。`--cascade`
连带卸载依赖它的包，`--force` 无视反向依赖强行卸载。

安装一个包并不等于它会被装载，也不等于任何场景能用它。旧实例升级后出现「模块已安装但命令无
响应」时，先查 `module_status.load`，再查该场景的 `enabled_modules`。

---

## 创建模块包

`akaribot new module <名>` 是 Typer 脚手架，源码位于
`packages/akari-bot-cli/akaribot/cli/commands/new.py`，渲染输入是仓库根下的
`templates/module/`。模板占位符语法、渲染顺序与目录契约见 `templates/README.md`。

生成目录为 `<--dir 指定目录>/akari-bot-module-<名>/`；缺省 `--dir .`，因此默认在当前目录下
生成 `akari-bot-module-<名>/`。该产物与 `packages/modules/akari-bot-module-<名>/` 同构，官方
模块包与第三方包共用同一套布局与元数据写法。

选项清单（`akaribot new module --help` 的输出）：

| 选项 | 含义 |
|------|------|
| `name` | 位置参数，模块名：小写字母、数字与下划线，如 `dice` |
| `--dir` / `-d` | 生成目录，包目录为 `<生成目录>/akari-bot-module-<name>`，默认 `.` |
| `--template-dir` | 模板目录，默认自动定位 |
| `--alias` | 命令别名，可重复 |
| `--desc` | 一句话说明，写入 `module()` 的 `desc` 与 locale 的 `help.desc` |
| `--author` | 作者名，只写入 `pyproject` 的 `authors`；`module()` 不再接 `developers` |
| `--license` | 许可证标识，写入 `pyproject` |
| `--platform` / `--exclude-platform` | `available_for` / `exclude_from`，可重复；留空表示全部平台 |
| `--component` | 组件：`command` / `regex` / `schedule` / `hook` / `event`，可重复 |
| `--command` | 命令模板，可重复；模板与说明用 `::` 分隔 |
| `--config` / `--no-config` | 是否生成 `config.py` 与配置注释键 |
| `--database` / `--no-database` | 是否生成 `database/` 与 `migrations/` |
| `--assets` / `--no-assets` | 是否生成包内只读资源目录 `assets/` |
| `--data-dir` / `--no-data-dir` | 是否生成 `data_dir()` 使用示例 |
| `--tests` / `--no-tests` | 是否生成 `tests/test_<name>.py` |
| `--non-interactive` | 不提问，未给出的选项取默认值 |
| `--add` / `--no-add` | 生成后执行 `akaribot module add -e .`，默认 `--add` |
| `--force` | 目标目录非空时覆盖 |

未勾选 `command` 组件时不会生成测试文件，脚手架会打印跳过原因。`--add` 的默认行为是在生成目录
内执行一次 `akaribot module add -e .`；该命令失败时脚手架打印可手工执行的完整命令，不中断生成。

生成后的典型目录：

```
akari-bot-module-my_module/
├── .github/workflows/publish.yml     # 第三方作者用的发布工作流
├── README.md
├── pyproject.toml                    # 分发元数据与 entry point
├── akaribot/modules/my_module/
│   ├── __init__.py                   # module() 注册与命令、组件骨架
│   ├── manifest.toml                 # 包级能力声明
│   ├── config.py                     # 模块配置字段声明（可选）
│   ├── database/
│   │   ├── __init__.py
│   │   └── models.py                 # 数据库模型（可选）
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py           # 迁移链起点（可选）
│   ├── locales/zh_cn.json            # 文案，只含简体中文
│   └── assets/                       # 包内只读资源（可选）
└── tests/test_my_module.py           # 集成测试（可选）
```

命名占位符的取值规则：`[@module_name@]` 必须匹配 `[a-z0-9_]+`，同时用作 `module()` 注册名、
locale 键前缀、表名前缀、目录名与 entry point 名；`[@module_class@]` 是模块名的大驼峰形式，用于
数据库模型类名。模块名不含 `-` 有两处硬性原因：适配器与模块的 entry point 名不得含 `-`（多实例
的 `client_name` 以 `-` 作分隔符，门禁 B9），TOML 的裸键同样拒绝 `-`。

---

## 包元数据与包内清单

### pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "akari-bot-module-my_module"
version = "0.1.0"
authors = [{ name = "YourName" }]
description = "一句话说明。"
requires-python = ">=3.12,<4.0"
dependencies = [
    "akari-bot-core>=0.1.0,<1.0",
]

[project.entry-points."akaribot.modules"]
"my_module" = "akaribot.modules.my_module"

[tool.hatch.build.targets.wheel]
packages = ["akaribot"]
```

- `authors` 是模块作者的唯一声明处：运行时从包根目录的这份 pyproject 读回，`module()` 不接
  `developers`。`~help` 的作者行、`akaribot module list` 的作者列与 TUI 详情都取自这里；作者按
  **包**声明，同一个包里多个模块共用这一份列表。wheel 安装不带 pyproject，此时退回分发元数据的
  `Author`，构建后端只保留首位作者。
- entry point 组名固定为 `akaribot.modules`，键是模块名，值是导入包目录的模块路径
  `akaribot.modules.<名>`。发现层优先读 entry points，目录扫描只是兜底。
- `locales/`、`assets/`、`migrations/` 都位于导入包目录内，随 `packages = ["akaribot"]`
  纳入 wheel。脚手架额外生成 `[tool.hatch.build.targets.wheel.force-include]` 段落，把这三个
  目录显式映射到 wheel 内的对应路径；两种写法都能让资源随包分发，新增包内资源目录时保持与
  `akaribot/modules/<名>/` 的路径一致。
- 内部依赖约束必须与仓库其余包字面一致，当前写法是 `akari-bot-core>=0.1.0,<1.0`。
  `tools/lint_versions.py` 以两条 error 规则检查：V2 要求各包对 `akari-bot-core` 的约束字符串
  一致，V1 要求约束区间包含目标成员的实际版本；V3 把钉到具体版本的写法记为 warn。
- 模块直接 `import tortoise`、`import apscheduler` 等库时，把对应依赖写进 `dependencies`，
  与 `akari-bot-core` 的约束并列。
- 模块包的 `version` 由版本守卫维护：包内有源码改动时递增，或在提交信息写 `[skip-version]`。

### manifest.toml

包内清单放在导入包目录的根部，文件名为 `manifest.toml`，由发现层按包根读取，locales、assets、
migrations 都相对它解析。字段与 `akaribot/core/registry.py` 的 `PackageManifest` 一一对应，未
声明的字段取该数据类的默认值，未声明的键会被忽略。

| 字段 | 类型 | 含义 |
|------|------|------|
| `schema` | int | 清单自身的结构版本，当前为 `1` |
| `requires_core_api` | str | 所需 core 公共 API 区间，PEP 440 描述符，当前为 `">=1"` |
| `locales` | str | 包内 locale 目录的相对路径，默认 `"locales"` |
| `assets` | str | 包内只读静态资源的相对路径，未声明表示不提供 |
| `migrations` | str | 数据库迁移目录的相对路径，未声明表示无迁移 |
| `config_migrations` | str | 配置迁移目录的相对路径，未声明表示无配置迁移 |
| `config_table` | str | 配置文件中的表名，如 `module_wiki`，未声明表示无配置 |
| `config_schema_version` | int | 该包配置的表结构版本，默认 `1` |
| `provides_modules` | list | 该包注册的全部模块名 |
| `owned_tables` | list | 该包拥有的数据表，供 `--purge-data` 清理 |
| `credential_fields` | list | 配置中属于凭据的字段名，供重复凭据检查 |

清单不写版本号，也不写依赖清单：这两者的真源是 distribution metadata。`requires_core_api` 与
当前 core API 版本不兼容的包会被 `reject_incompatible()` 拒绝注册，`CORE_API_VERSION` 定义在
`akaribot/core/registry.py`。

模块包的实例（`packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/manifest.toml`）：

```toml
# akari-bot-module-wiki 的包清单。
schema = 1
requires_core_api = ">=1"
locales = "locales"
migrations = "migrations"
# config.py 的 on_module_config("wiki") 登记的表。
config_table = "module_wiki"
config_schema_version = 1
# 本包 module() 注册的全部模块名。
provides_modules = [
    "wiki",
    "wikilog",
]
# 供 --purge-data 使用；取自 database/models.py 的 Meta.table。
owned_tables = [
    "module_wiki_site_info",
    "module_wikilog_target_set_info",
]
```

适配器包的清单使用同一结构，另有适配器专属字段，见
`packages/adapters/akari-bot-adapter-telegram/akaribot/adapters/telegram/manifest.toml`。

包级公共 API 的专用声明字段（`public_api`）尚未落地：`PackageManifest` 没有该字段，发现层与门禁
都不读取它。跨模块能力当前经具名 hook 与模块的 `.api` 命名空间表达，见「导入边界」。

---

## 导入边界

### core 门面

模块代码从门面取用公共设施：

```python
from akaribot.core.api import Bot, CoolDown, I18NContext, IntervalTrigger, on_module_config, module
```

门面由 `akaribot/core/api/__init__.py` 与 `akaribot/core/api/base.py` 组成，`base.py` 的
`__all__` 是承诺的完整名字清单。导入期不依赖实例配置：`core.api.base` 的导入块在配置缺失时
整体中断，未绑定的名字由门面的 `__getattr__` 在首次访问时重试，因此 CLI 与发现层可以在配置
就绪之前安全导入门面并读取 `__api_version__`。

三个禁止项：

- 不 import `akaribot.core` 的内部深路径。既有模块包中仍存在深路径写法，门禁 B8 对这类写法按
  符号判定：深路径取到的符号已收录进门面时只记为「写法未迁移」，不报违规；符号未收录时记
  warn。新代码直接使用门面。
- 不 import `akaribot.adapters.*`（门禁 B2，error）。平台能力经 `SessionInfo`、`Features` 等
  声明式接口获取，模块不直接依赖某个平台适配器。
- 不 import `akaribot.core.api.adapters`（门禁 B3，error）。该面只供适配器使用，其文档字符串
  明确说明模块导入它通常意味着做了本应交给适配器的事。

`akaribot`、`akaribot.modules`、`akaribot.adapters` 是 PEP 420 命名空间目录，不得在其中放置
`__init__.py`（门禁 B7，error）；`akaribot.core`、`akaribot.testing` 与各模块包是常规包。

### 模块之间的依赖

- 官方模块包（`packages/modules/*`）之间不得互相依赖，门禁 B10 记为 error。官方包连对方的
  `.api` 也不许依赖，跨模块能力一律经具名 hook 表达。
- 第三方模块包之间允许依赖：`from akaribot.modules.<对方>.api import <名字>`，其中 `.api` 是
  对方承诺的公开段（门禁 B1 只对非 `.api` 的内部路径报违规，官方包升级为 error，第三方包记
  warn）。
- 使用方必须在自身 `pyproject.toml` 的 `dependencies` 里声明对方分发名（门禁 B6，error）。
- 声明了依赖的包会进入运行时依赖图，成环时发现层抛 `CircularDependencyError`。参与依赖图的
  分发名前缀是 `akari-bot-module-` 与 `akari-bot-adapter-`，其余 `Requires-Dist` 是普通 PyPI
  依赖，由安装器解析。

---

## 本地化文件

- 只创建与修改 `akaribot/modules/<名>/locales/zh_cn.json`。
- 其他语言文件由 Weblate 自动提交，不手工新增、补键、翻译或同步。
- 运行时按语言加载，缺失键回退到基础语言，基础语言是 `zh_cn`。
- 配置字段的注释写在 `config.comments.<表名>.<字段名>`，表名即 `on_module_config()` 声明的
  `module_<模块名>`。缺少该键时该字段在生成的配置文件里没有行尾注释。
- 命令模板的描述位、模块 `desc` 也取自同一文件，键名规则见「国际化（i18n）」。

---

## 基本结构与最小示例

```python
from akaribot.core.api import Bot, I18NContext, module

my_mod = module(
    "my_module",
    alias={"mm": "my_module"},
    desc="{I18N:my_module.help.desc}",
    doc=True,
)


@my_mod.command("hello {{I18N:my_module.help.hello}}")
async def _(msg: Bot.MessageSession):
    await msg.finish(I18NContext("my_module.message.hello"))


@my_mod.command("echo <text> {{I18N:my_module.help.echo}}")
async def _(msg: Bot.MessageSession, text: str):
    await msg.finish(I18NContext("my_module.message.echo", text=text))
```

```json
{
    "my_module.help.desc": "示例模块",
    "my_module.help.hello": "打个招呼",
    "my_module.help.echo": "重复用户输入的内容",
    "my_module.message.hello": "你好，世界！",
    "my_module.message.echo": "复读：${text}"
}
```

`module()` 的完整签名（`akaribot/core/component.py`）：

```python
def module(
    module_name: str,
    alias: str | list | tuple | dict | None = None,
    desc: str | None = None,
    recommend_modules: str | list | tuple | None = None,
    required_admin: bool = False,
    base: bool = False,
    doc: bool = False,
    hidden: bool = False,
    load: bool = True,
    rss: bool = False,
    regex: bool = False,
    event: bool = False,
    required_superuser: bool = False,
    required_base_superuser: bool = False,
    required_bot_permissions: str | list | tuple = (),
    suppress_invalid_prompt: bool = False,
    available_for: str | list | tuple = "*",
    exclude_from: str | list | tuple = "",
    support_languages: str | list | tuple | None = None,
):
```

包归属由发现层解析：`module()` 依据调用方的模块名经 `PackageRegistry.by_import_path()` 取得包
条目，因此模块代码不必声明自己属于哪个包。`base=True` 把模块设为基础命令（强制开启），
`hidden=True` 使其在帮助列表中不可见。

> **注意**：模块 `desc` 与 `options_desc` 使用 `{I18N:...}` 单花括号语法，命令模板的描述位使用
> `{{I18N:...}}` 双花括号语法；代码中通过 `I18NContext(key, **kwargs)` 发送国际化消息。消息参数
> 使用 `string.Template` 格式的 `${param_name}` 占位符传入，不是 `{param_name}`。

---

## 命令模板详解

```python
# 基本命令
@my_mod.command("hello")
async def _(msg): ...

# 带必需参数
@my_mod.command("echo <text>")
async def _(msg, text: str): ...

# 带可选参数
@my_mod.command("search <query> [-l <lang>]")
async def _(msg, query: str):
    lang = msg.parsed_msg.get("-l", {}).get("<lang>")
    # parsed_msg = {"<query>": "...", "-l": {"<lang>": "..."}}

# 变长参数
@my_mod.command("choice <items> ...")
async def _(msg):
    items = [msg.parsed_msg.get("<items>")] + msg.parsed_msg.get("...", [])

# 无参数命令（默认处理）
@my_mod.command()
async def _(msg): ...

# 多个命令模板（同一个函数）——传列表
@my_mod.command([
    "add <alias> <command> {{I18N:my_module.help.add}}",
    "remove <alias> {{I18N:my_module.help.remove}}",
])
async def _(msg): ...

# i18n 描述（双花括号）
@my_mod.command("hello {{I18N:my_module.help.hello}}")

# 带选项描述（options_desc 的值用单花括号 {I18N:...}）
@my_mod.command(
    "search <query> [-l <lang>] {{I18N:my_module.help.search}}",
    options_desc={"-l": "{I18N:my_module.help.option.l}"},
)
```

### 参数如何注入函数

参数注入基于函数签名，规则要点：

```python
@bilibili.command("<bid> [-i] {{I18N:...}}", options_desc={"-i": "{I18N:...}"})
async def _(msg: Bot.MessageSession, bid: str, get_detail=False):
    ...
```

| 情况 | 行为 |
|------|------|
| 函数只有 1 个参数 | 无视注解，直接把 `msg` 传进去 |
| 函数有多个参数 | 逐个按名字去 `parsed_msg` 里找 |
| 参数注解为 `Bot.MessageSession` | 收到 `msg` |
| 参数名 `foo` | 先找 `parsed_msg["<foo>"]`，再找 `parsed_msg["foo"]` |
| 注解为 `int` / `float` / `bool` | 自动转换；转换失败抛 `InvalidCommandFormatError` |
| 找不到对应值 | 用函数默认值；没有默认值就传 `None` |
| 注解为 `Param("<名字>", 类型)` | 显式指定要取哪个 key（参数名与模板名不一致时使用） |

> **`MessageSession` 参数必须注解成 `Bot.MessageSession`**。框架按
> `param_obj.annotation == bot.MessageSession` 判定；直接
> `from akaribot.core.builtins.session.internal import MessageSession` 再拿它当注解不生效，
> 日志会打出 `has no Bot.MessageSession parameter, did you forgot to add it?`，运行时行为也会
> 错乱。源码中的原话是「Remember: MessageSession IS NOT Bot.MessageSession」。
>
> 注入只在 `parsed_msg` 非空时发生。裸 `@my_mod.command()`（无模板）的函数只能有一个参数。

`Param` 用法：

```python
@echo.command("<display_msg>")
async def _(msg: Bot.MessageSession, dis: Param("<display_msg>", str)):
    ...
```

`Param` 由门面导出，与 `module`、`Bot` 同属公共面。

---

## 正则匹配

```python
@my_mod.regex(r"正则模式", mode="M", desc="{I18N:my_module.help.regex}")
async def _(msg: Bot.MessageSession):
    # msg.matched_msg 包含匹配结果
    await msg.finish(I18NContext("my_module.message.matched"))
```

完整签名（`akaribot/core/component.py`）：

```python
def regex(self, pattern, mode="M", flags=re.NOFLAG, desc=None,
          required_admin=False, required_superuser=False, required_base_superuser=False,
          available_for="*", exclude_from="", load=True,
          logging=True,                    # 是否记录日志
          show_typing=True,                # 是否显示“正在输入”，同时决定是否走 TOS 计数
          text_only=True,                  # 是否只对纯文本消息生效
          element_filter=None,             # 只在消息含指定元素类型时触发
          trigger_once_startup=False,      # 启动后是否只触发一次
          skip_long_message_confirm=False) # 长消息是否跳过确认
```

mode 参数（默认为 `"M"`，注册期做 `mode.upper()` 归一）：

| 值 | 行为 |
| --- | --- |
| `"M"` / `"MATCH"` | `re.match`，`msg.matched_msg` 是 `Match` 对象 |
| `"A"` / `"FINDALL"` | `re.findall`，`msg.matched_msg` 是列表 |

正则模块需要在 `module()` 上声明 `regex=True`，事件模块声明 `event=True`，RSS 模块声明
`rss=True`；模块受限时的启用提示由核心模块按 `unsupported_reason()` 的返回值给出。

---

## 权限控制

```python
# 模块级别
my_mod = module("my_module", required_admin=True)        # 需要场景管理员
my_mod = module("my_module", required_superuser=True)    # 需要超级用户

# 命令级别
@my_mod.command("set <sides>", required_admin=True)
async def _(msg, sides: int): ...

# 运行时检查
@my_mod.command("dangerous")
async def _(msg):
    if not msg.check_super_user():                 # 同步
        await msg.finish(I18NContext("my_module.error.permission"))
    if not await msg.check_permission():           # 异步，必须 await
        await msg.finish(I18NContext("my_module.error.permission"))
```

`check_permission()` 覆盖群组管理员、自定义管理员、超级用户三类；`check_native_permission()` 才是
向平台请求原生权限。`msg.finish()` 抛 `SessionFinished`，其后不需要 `return`。

`module()` 的 `required_admin` / `required_superuser` / `required_base_superuser` 与命令装饰器的
同名参数叠加生效；`required_bot_permissions` 声明开启模块前要求机器人具备的平台权限字段。

---

## 模块配置

配置写在包内 `config.py`，由加载器自动 import。`on_module_config(module_name, secret=False,
standalone_comments=None)` 把类里带类型注解的字段与默认值写进配置文件的 `module_<模块名>` 表。

```python
from akaribot.core.api import on_module_config


@on_module_config("my_module")
class MyModuleConfig:
    """模块配置的字段声明。"""

    my_module_limit: int = 100


@on_module_config("my_module", secret=True)
class MyModuleSecretConfig:
    """敏感配置写进 module_my_module_secret 表。"""

    my_module_api_key: str = ""
```

读取直接取类属性，键名、默认值、类型、表名都不必重写：

```python
from akaribot.modules.my_module.config import MyModuleConfig, MyModuleSecretConfig

limit = MyModuleConfig.my_module_limit
api_key = MyModuleSecretConfig.my_module_api_key
```

- 模板类不依赖模块对象，因而是叶子模块，同包内任何文件都可以在顶层导入它；用
  `Bind.Module.config()` 声明会因 `from . import <模块变量>` 造成循环导入。
- 传给 `on_module_config()` 的模块名须与 `module()` 声明的一致；由下划线迁为连字符的模块可沿用
  作为命令别名的旧名，避免已有配置表失效。其它不一致会被测试拦下。
- 配置类不会被实例化，只作为声明式 schema 使用；不要在其中写方法或 `__init__`。
- 默认值决定类型校验，`my_module_timeout: float = 60` 这类写法不要写成 `int`。
- 字段名以模块名作前缀；行尾注释取自 locale 的 `config.comments.module_<模块名>.<字段名>`。
- 该包的 `manifest.toml` 需要声明 `config_table = "module_<模块名>"` 与 `config_schema_version`。

配置文件位于实例根下的 `config/module_<模块名>.toml`，由 `akaribot config` 子命令维护：

```
akaribot config schema --table module_my_module    # 查看该表的全部键、类型、注释与占位情况
akaribot config set my_module_limit 200 --table module_my_module
```

---

## 数据库模型

模块模型放在包内 `database/models.py`。发现层按包根判断该文件是否存在，存在即把
`<导入路径>.database.models` 交给 `init_db()` 导入并注册到 Tortoise 的 `models` app，不需要
手动登记；`database/__init__.py` 可以为空，但目录中需要该文件。

表名约定：模块内定义 `table_prefix = "module_<模块名>_"`，各表用 f-string 拼。

```python
from tortoise import fields

from akaribot.core.api import DBModel, UNION_SCOPE_SENDER

table_prefix = "module_my_module_"


class MyModuleBindInfo(DBModel):
    """
    用户绑定信息。

    :param union_id: 绑定的用户联合 ID。
    :param username: 绑定的用户名。
    """

    union_scope = UNION_SCOPE_SENDER
    union_id = fields.CharField(max_length=512, primary_key=True)
    username = fields.CharField(max_length=512)

    class Meta:
        table = f"{table_prefix}bind_info"

    @classmethod
    async def set_bind_info(cls, union_id: str, username: str):
        ...
```

- 继承 `DBModel`（不是 `tortoise.Model`），它提供 `get_by_target_id` 与 `get_by_sender_id` 等
  便利方法。
- 会话归属数据用 `union_id = fields.CharField(max_length=512, primary_key=True)`，并按归属声明
  `union_scope = UNION_SCOPE_SENDER` 或 `UNION_SCOPE_TARGET`；不要新增 `sender_id` / `target_id`
  状态列把同一用户或场景按平台割裂。
- 业务逻辑习惯写成模型上的 `@classmethod`，而不是散在命令函数里。
- 表名不得含 `-`；新增表的表名补进包内 `manifest.toml` 的 `owned_tables`，
  `akaribot module remove --purge-data` 才会清理它。

```python
from akaribot.modules.my_module.database.models import MyModuleData

data = await MyModuleData.get_by_target_id(msg)
data.data["key"] = "value"
await data.save()
```

用户归属模型对应使用 `await MyModuleData.get_by_sender_id(msg)`。两个方法先把平台 ID 解析为
union，再按 `union_id` 查询或创建。需要围绕多张表做一致性写入时使用
`akaribot.core.api` 导出的 `union_mutation` 与显式事务。

### 迁移

结构变更以包内 `migrations/NNNN_<说明>.py` 表达，每个 revision 声明 `REVISION` 与
`DEPENDS_ON`。初始 `0001_initial.py` 不写 DDL：`db upgrade` 在全部 revision 执行完毕后调用
`generate_schemas()` 建表，该文件只作为迁移链的起点存在。

```python
from akaribot.core.api import MigrationContext

REVISION = "0002_union_id"
DEPENDS_ON = "0001_initial"


async def upgrade(ctx: MigrationContext) -> None:
    """幂等地改写既有表结构。"""
```

硬规则是幂等：MySQL 的 DDL 自动提交，无法把「执行 DDL」与「写 schema_migrations」放进同一
事务，中途失败重跑时非幂等的迁移会重复施加变更，因此每一步都先探测再执行。执行顺序固定为
core 的全部待应用 revision，再按包名依次执行各模块包。迁移记录以分发名为键，包名变化不影响
已登记的 revision。

---

## 定时任务

`Scheduler` 是全局 `AsyncIOScheduler` 实例，由 server 进程启动。`@my_mod.schedule(trigger)`
接受任意 APScheduler trigger：

```python
from akaribot.core.api import Bot, CronTrigger, I18NContext, IntervalTrigger


@my_mod.schedule(IntervalTrigger(hours=1))
async def hourly_task():
    # 定时任务没有 msg，主动发消息走 Bot.post_message
    await Bot.post_message("my_module", I18NContext("my_module.message.hourly"))


@my_mod.schedule(CronTrigger(hour=0, minute=0))
async def daily_task():
    pass
```

定时任务函数不接收参数。需要给用户发消息时使用 `Bot.post_message(模块名, ...)`，框架只发给
开启了该模块的场景。`IntervalTrigger`、`CronTrigger`、`DateTrigger`、`AndTrigger`、`OrTrigger`
都由门面导出。热重载的重载窗口覆盖 Scheduler 维护，重启与热重载都不会遗留重复任务。

---

## 模块钩子

钩子用于跨模块调用：一个模块注册能力，另一个模块按名字触发。回调固定收一个
`Bot.ModuleHookContext`：

```python
@define
class ModuleHookContext:
    args: dict                               # 触发方传入的参数
    session_info: SessionInfo | None = None  # 触发方所在会话（可能为 None）
```

```python
# 注册方
@wiki.hook("autosearch")
async def auto_search(ctx: Bot.ModuleHookContext):
    title = ctx.args["title"]
    ...
    return [...]        # 返回值会回传给触发方


# 触发方
result = await Bot.Hook.trigger("wiki.autosearch", session_info, args={"title": "Foo"})
```

钩子名在注册表里是 `<模块名>.<钩子名>`，触发时要带模块名前缀。`Bot.Hook.trigger` 的签名是
`(module_or_hook_name, session_info=None, args=None, timeout=None)`。

具名 hook 与 parser 入口 hook 共享执行基础：模块加载状态、平台过滤、runtime generation、超时
与取消收尾均由统一执行器处理。调用具名能力使用 `Bot.Hook.trigger("module.hook", session_info=...,
args=...)`；调用模块名则按优先级广播该模块全部具名 hook，单个回调失败会记录并继续。具名 hook
的 `timeout` 默认 5 秒，传入 `timeout <= 0` 可显式取消限制。测试与计划任务应走
`akaribot.core.builtins.hooks.dispatch_module_hook()`，不要直接调用注册表中的函数。

### 入口订阅

`@mod.hook(point=...)` 注册 parser 或出站生命周期入口的订阅，入口常量取
`akaribot.core.api` 导出的 `HookPoint`，取值包括 `HookPoint.MESSAGE_NORMALIZED`、
`HookPoint.COMMAND_BEFORE_EXECUTE`、`HookPoint.OUTGOING_BEFORE_SEND` 等。装饰器参数为
`(name=None, *, point=None, priority=100, available_for="*", exclude_from="", load=True,
timeout=5.0, server_scope=False)`；`priority` 升序执行，`server_scope=True` 表示系统扩展作用域，
免场景 `enabled_modules` 限制。

```python
from akaribot.core.api import Bot, HookPoint


@mod.hook(point=HookPoint.MESSAGE_NORMALIZED)
async def _(ctx: Bot.ModuleHookContext):
    # 返回 None 表示不干预；需要截断或改写消息时返回 HookResult 类型化结果
    return None
```

### 事件模块

```python
@mod.event("member_joined")
async def _(event: EventInfo):
    # 事件名由平台适配器定义，不同平台可用的名称不同
    return None
```

`@mod.event(name, available_for="*", exclude_from="", load=True)` 的入口收 `EventInfo`，模块需在
`module()` 上声明 `event=True`，并要求平台可读取全部消息。

---

## 国际化（i18n）

### 规则

- 所有面向用户的文本使用 `I18NContext`，不使用 `Plain("纯文本")`。
- 只编辑 `locales/zh_cn.json`；其他语言文件由 Weblate bot 维护。
- 命令模板中的描述使用 `{{I18N:key}}` 语法。
- 模块 `desc` 参数使用 `{I18N:key}` 语法（单花括号）。
- 参数化消息使用 `string.Template` 格式的 `${param}` 占位符。

### 语言文件格式

```json
{
    "my_module.help.desc": "这是一个示例模块",
    "my_module.help.hello": "打个招呼",
    "my_module.help.echo": "重复用户输入的内容",
    "my_module.help.option.l": "语言",
    "my_module.message.success": "操作成功！",
    "my_module.message.greeting": "你好，${name}！",
    "my_module.error.not_found": "未找到结果。",
    "my_module.error.permission": "权限不足。",
    "config.comments.module_my_module.my_module_limit": "单次操作的条数上限。"
}
```

### 命名约定

```
{module_name}.{category}.{key}

category 常用值:
  help.desc       - 模块描述
  help.xxx        - 命令帮助文本
  help.option.xxx - 选项描述
  message.xxx     - 正常输出消息
  error.xxx       - 错误消息

config.comments.<表名>.<字段名> - 配置字段的行尾注释
```

### 代码中使用

```python
from akaribot.core.api import Bot, I18NContext

# 简单消息
await msg.finish(I18NContext("my_module.message.success"))

# 带参数的消息
await msg.finish(I18NContext("my_module.message.greeting", name="World"))

# 命令模板中的 i18n
@my_mod.command("hello {{I18N:my_module.help.hello}}")
async def _(msg: Bot.MessageSession):
    await msg.finish(I18NContext("my_module.message.hello"))
```

### 错误示例（禁止）

```python
# 错误：使用纯文本
await msg.finish("操作成功！")
await msg.finish(f"你好，{name}！")

# 正确：使用 I18NContext
await msg.finish(I18NContext("my_module.message.success"))
await msg.finish(I18NContext("my_module.message.greeting", name=name))
```

---

## 主动发送消息

```python
from akaribot.core.api import Bot, I18NContext

# 发送到所有启用了该模块的场景（session_list=None 时自动查库）
await Bot.post_message("my_module", I18NContext("my_module.message.broadcast"))

# message 传 dict 可按平台分发，"default" 为兜底
await Bot.post_message("my_module", {
    "default": I18NContext("my_module.message.broadcast"),
    "Discord": embed_chain,
})

# 发送到特定目标
target = await Bot.fetch_target("QQ|Group|123456789")   # 返回 FetchedSessionInfo | None
if target:
    await Bot.send_direct_message(target, I18NContext("my_module.message.hello"))

# 批量
targets = await Bot.fetch_target_list(["QQ|Group|1", "Discord|Channel|2"])
# 查出开启了某模块的全部场景
targets = await Bot.get_enabled_this_module("my_module")
```

`module_name` 传 `"*"` 表示全局，也可以直接使用 `Bot.post_global_message()`。

---

## 冷却、花瓣与游戏状态

### 冷却

```python
from akaribot.core.api import CoolDown, I18NContext

# CoolDown(key, msg, delay, whole_target=False)
# whole_target=True 时冷却作用于整个对话而非单个用户
cd = CoolDown("my_command", msg, delay=60)

remaining = cd.check()  # 返回剩余秒数（float），0 表示可用
if remaining > 0:
    await msg.finish(I18NContext("my_module.message.cooldown", time=int(remaining)))

# 执行命令...
cd.reset()  # 重新计时
```

### 花瓣

```python
from akaribot.core.api import I18NContext, cost_petal, gained_petal, lost_petal, sign_get_petal

# 花费花瓣：余额不足返回 False，send_prompt=True 时自动发提示
if await cost_petal(msg, 10):
    ...  # 执行操作

# 增减花瓣，返回一个可直接拼进消息链的 I18NContextElement（或 None）
prompt = await gained_petal(msg, 5)
prompt = await lost_petal(msg, 5)
if prompt:
    await msg.finish([I18NContext("my_module.message.done"), prompt])

# 签到奖励
await sign_get_petal(msg)
```

### 游戏状态

`PlayState` 按 `(target_id, game)` 两级维度隔离游戏状态，底层是 `ExpiringTempDict`，1 小时
（`GAME_EXPIRED`）自动过期，卡死的对局会自愈。

```python
from akaribot.core.api import I18NContext, PlayState

play_state = PlayState("my_game", msg)  # 构造：游戏名 + 消息会话

if play_state.check():  # 该场景下这个游戏是否正在进行
    await msg.finish(I18NContext("my_module.message.playing"))

play_state.enable()  # 开局
play_state.update(answer="42", tries=0)  # 存任意局内数据
...
answer = play_state.get("answer")  # 取局内数据，可带 default
if not play_state.check():  # 每次异步等待回来都要重新确认没被中断
    return
play_state.disable()  # 结束
```

| 方法 | 作用 |
| --- | --- |
| `enable()` | 开启游戏事件并刷新过期时间 |
| `disable()` | 关闭游戏事件 |
| `check() -> bool` | 读取 `_status`，未开启或已过期返回 `False` |
| `update(**kwargs)` | 写入局内数据 |
| `get(key, default)` | 读取局内数据 |

> 状态是进程内内存（不落库），server 进程重启即丢失。`_status` 是保留键，不要用
> `update(_status=...)` 覆盖。

---

## 等待用户交互

四个方法都在 `MessageSession` 上，`timeout` 接受 `float | None`，缺省 120 秒。

```python
# 返回 bool
wait_confirm(message_chain=None, quote=True, delete=True, timeout=120,
             append_instruction=True, no_confirm_action=True,
             release_execution_lock=True, consume_any_message=False)

# 返回 MessageSession
wait_next_message(message_chain=None, quote=True, delete=False, timeout=120,
                  append_instruction=True, possibly_choices=None)

# 返回 MessageSession，message_chain 必填
wait_reply(message_chain, quote=True, delete=False, timeout=120,
           all_=False, append_instruction=True)

# 返回 MessageSession
wait_anyone(message_chain=None, quote=False, delete=False, timeout=120)
```

```python
# 等待确认（平台支持则用反应，否则用文本）
if await msg.wait_confirm(I18NContext("my_module.message.confirm")):
    await msg.finish(I18NContext("my_module.message.confirmed"))
else:
    await msg.finish(I18NContext("my_module.message.cancelled"))

# 等待下一条消息
next_msg = await msg.wait_next_message(I18NContext("my_module.message.ask"))
await msg.finish(I18NContext("my_module.message.echo", text=next_msg.as_display()))

# 发送并等待回复（message_chain 是必填参数）
reply = await msg.wait_reply(I18NContext("my_module.message.ask_name"), timeout=60)
await msg.finish(I18NContext("my_module.message.greeting", name=reply.as_display()))

# 等待场景内任意成员发言（多人游戏抢答用）
answer = await msg.wait_anyone(timeout=30)
```

> **超时不返回 `None`，而是抛 `WaitCancelException`**。超时时走不到 `if next_msg:` 的判断行。
> `WaitCancelException` 继承自 `BaseException`，框架在外层捕获并给用户发提示，模块中通常不要
> 自行 catch。
>
> 其他共同行为：
> - 进入等待前会 `ExecutionLockList.remove(self)` 并 `end_typing()`，等待期间用户可以触发别的
>   命令
> - `wait_confirm` 在配置 `no_confirm` 为真时直接返回 `no_confirm_action`（默认 `True`），不发
>   消息也不等待；写破坏性操作时要意识到确认可能被全局跳过
> - `append_instruction=True` 会自动追加平台相关的操作提示（反应 / 回复 / 文本），一般不要关闭
> - `message_chain` 不填就只等不发；`wait_reply` 例外，它是必填的

---

## 模块测试

模块自带用例放在 `packages/modules/akari-bot-module-<名>/tests/`（第三方包对应自身包目录下的
`tests/`），使用自研框架而非 pytest。

```python
from akaribot.testing import Contains, Tester, func_case


@func_case
async def test_my_module_hello(tester: Tester):
    """hello 命令：回复应包含问候文案"""
    await tester.integrate("~my_module hello", Contains("你好，世界！"), "hello 应回复问候文案")
    return tester
```

- `@func_case` 标记测试入口，框架在测试时调用它；`@case(input_, expected=None, note=None,
  timeout=None)` 直接注册单个交互案例。
- `tester.integrate(input_, expected=None, note=None, timeout=None)` 发送真实命令并断言回复，
  期望值使用 `Contains` 等期望匹配器；手动复核时把期望值留空。
- 集成用例的前提是测试发送者具有超级用户身份、模块处于已加载状态，且该模块的 `config.py`
  已被扫描。断言文案与 locale 中的文案一致，改文案时两处一起改。
- 只做单元求证（求解器、纯函数）时不需要 `Tester`，可直接 import 模块内的函数。

运行单个入口：

```
CI=1 PYTHONIOENCODING=UTF-8 python tests/run_one.py packages/modules/akari-bot-module-<名>/tests/test_<名>.py [入口函数名]
```

缺省入口参数时运行该文件中全部 `test_` 开头的函数。等价入口：

```
akaribot test [path] --case <用例名> --ci
```

`akaribot test` 不带参数时跑全部测试，`--coverage` 统计覆盖率。根 `pyproject.toml` 的
`testpaths` 已包含 `packages`，pytest 是同一框架的第二个前端，`@func_case` 入口由
`akaribot.testing.pytest_plugin` 接管。

---

## 常见开发任务速查

### 创建新模块

1. 运行 `akaribot new module <名>`，按需给出 `--desc`、`--author`、`--component`、`--command`
   等选项；脚本化调用加 `--non-interactive`。
2. 脚手架在 `<--dir>/akari-bot-module-<名>/` 生成完整包，并默认执行一次
   `akaribot module add -e .`；该命令未成功时在生成目录内手工执行。
3. 在 `akaribot/modules/<名>/__init__.py` 补命令、正则、定时任务或 hook。
4. 修改配置字段时编辑 `config.py` 并在 locale 中补
   `config.comments.module_<名>.<字段名>`。
5. 面向用户的文本一律写入 `locales/zh_cn.json`，不编辑其他语言文件。

### 添加新命令

```python
@my_mod.command("command_name <arg> {{I18N:my_module.help.text}}")
async def _(msg: Bot.MessageSession, arg: str):
    await msg.finish(I18NContext("my_module.message.result", arg=arg))
```

同时在 `akaribot/modules/my_module/locales/zh_cn.json` 补上 `my_module.help.text` 与
`my_module.message.result` 两个键。

### 热重载

```python
status, reload_count = await ModulesManager.reload_module("module_name")
```

或通过命令：`~module reload <module> ...`（别名 `~reload`，需超级用户）。热重载按 Python 文件
而不是按模块名进行：同一个 `.py` 里定义的其他模块会一起重载，`reload_count` 是实际重载的模块
数。重载进行中再次请求会直接返回 `(False, 0)` 并记一条 warning，不会排队。重载窗口覆盖
Scheduler 维护与队列排空，模块的定时任务不会因此重复注册。

### 修改配置

直接编辑实例根下 `config/module_<模块名>.toml`，不需要重载命令：配置读取会触发
`CFGManager.watch()`，它按 `WATCH_INTERVAL`（1 秒）扫描一次目录 mtime，发现变动就调用
`load()`，因此改动可能延迟至多一个扫描间隔生效。也可以用
`akaribot config set <键> <值> --table module_<模块名>` 写入，写入前会按模板声明的类型转换。

### 修改数据库表结构

1. 在包内 `migrations/` 新增 `NNNN_<说明>.py`，声明 `REVISION` 与 `DEPENDS_ON`，在
   `upgrade(ctx)` 中写幂等 DDL。
2. 把新增表名补进包内 `manifest.toml` 的 `owned_tables`。
3. 迁移在实例启动的 `db upgrade` 阶段执行；表结构变更需要新的进程周期，热重载不覆盖数据库
   迁移。

### 修改 locale 文案

编辑 `locales/zh_cn.json` 后需要 `~module reload <模块名>`：locale 在模块加载时收集并计算指纹，
文件改动不会自动进入已加载的模块。
