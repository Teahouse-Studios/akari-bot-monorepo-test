# 加载、配置、数据库与队列
## 目录
- [模块加载系统](#55-模块加载系统-akaribotcoreloaderpy)
- [组件注册系统](#56-组件注册系统-akaribotcorecomponentpy)
- [配置系统](#57-配置系统-akaribotcoreconfig)
- [数据库系统](#58-数据库系统-akaribotcoredatabase)
- [队列系统](#59-队列系统-akaribotcorequeue)
- [导出系统](#121-导出系统避免循环导入)
- [热重载](#127-热重载)

配置与数据库的模块侧调用示例位于 `module-development.md`，两份文件都由主 `SKILL.md` 直接路由。涉及启动或跨进程生命周期时，再读取 `architecture.md`。

**路径写法**：下文用两种写法指代文件。仓库相对路径从 `packages/` 起，例如 `packages/akari-bot-core/akaribot/core/queue/README.md`；包内路径以导入包名为根，例如 `akaribot/core/config/__init__.py`，其完整路径为 `packages/akari-bot-core/akaribot/core/config/__init__.py`。包布局为：core 在 `packages/akari-bot-core/akaribot/core/`，内置模块在 `packages/akari-bot-core/akaribot/modules/core/`，模块包在 `packages/modules/akari-bot-module-<名>/akaribot/modules/<名>/`，适配器包在 `packages/adapters/akari-bot-adapter-<平台>/akaribot/adapters/<平台>/`。模块与适配器只应 import `akaribot.core.api` 门面，适配器另有 `akaribot.core.api.adapters`。

---

### 5.5 模块加载系统 (`akaribot/core/loader.py`)

```python
class ModulesManager:
    modules: dict[str, Module] = {}            # 模块名 → Module
    modules_aliases: dict[str, str] = {}       # 别名 → 模块名
    modules_hooks: dict[str, Callable] = {}    # 具名钩子 → 函数
    modules_events: dict[str, list[tuple[str, EventMeta]]] = {}
    modules_origin: dict[str, str] = {}        # 模块名 → 所属包的导入路径

    @classmethod
    async def reload_module(cls, module_name) -> tuple[bool, int]
    # 维护窗口 → 依赖闭包 → 重建注册 → 切换运行时与数据库 context → 失败回滚
```

**发现层先行**。`load_modules()` 不再遍历模块目录，而是消费 `akaribot.core.registry.PackageRegistry` 的发现结果。该注册表是「系统里有哪些模块与适配器」的唯一答案来源，按下列顺序合成，最后按条目名去重（entry point 胜出，冲突记警告）：

1. `akaribot/core/_frozen_registry.py` 存在时直接采用其中的 `PACKAGES`（二进制构建产物，当前未生成）；
2. 枚举 entry point 组 `akaribot.modules` 与 `akaribot.adapters`，拆包后各包以 wheel 安装，此路径为主；
3. 兜底扫描命名空间包 `akaribot.modules` 与 `akaribot.adapters`，合成 `dist_name` 为空的条目；
4. 收尾校验 core API 兼容性与声明依赖（缺失、版本不满足、成环、依赖了被 API 门槛拒绝的包），两道都通过的包才注册。

每个包的导入包目录下有 `manifest.toml`，`PackageManifest` 认识 schema、requires_core_api、locales、assets、migrations、config_migrations、config_table、config_schema_version、provides_modules、owned_tables、credential_fields。适配器当前声明 config_table 与 credential_fields，后者供启动前检测重复账号；`listen_fields`、`id_columns`、`supports_replicas`、`public_api` 属规划字段，manifest 解析器不读取。`CORE_API_VERSION = 1`（`akaribot/core/registry.py:39`），requires_core_api 不满足的包由 `reject_incompatible()` 拒绝注册。

加载流程（`load_modules()`，`akaribot/core/loader.py:41`）：

1. `PackageRegistry.load_order()` 给出按声明依赖拓扑排序的包，被依赖者在前；只处理 `kind == "module"` 的条目。
2. `importlib.import_module(entry.import_path)` 导入包本身（如 `akaribot.modules.wiki`，内置模块为 `akaribot.modules.core`）。
3. 尝试导入 `<导入路径>.config`：只有 `ModuleNotFoundError.name` 恰等于该配置模块名时才静默跳过，包内缺依赖同样表现为该异常，照常上抛。
4. 包的 `__init__.py` 在导入期调用 `module()` 完成注册，各组件装饰器同样在导入期登记。
5. 单个包失败时 `_restore_module_registrations()` 撤销该包本轮已产生的注册，部分登记后抛异常的包不会继续接收命令。
6. `ModuleStatus.init_modules()` 以传入清单为准重建状态行（缺席行被删除），随后一次 `ModuleStatus.all()` 取回状态写入 `module._db_load`。
7. `ModuleRuntimeManager.activate()/suspend()` 按 `_db_load` 挂载或暂停模块运行时。
8. `refresh()` 重建别名、hook 与事件索引，并记录各包 locale 文件指纹，供热重载判断是否重建 i18n 快照。

**单个模块加载失败不会中断整体流程**：异常文本写入 `PrivateData.path / ".cache_loader"`（即 `data/private/default/.cache_loader`），随后追加 `PackageRegistry.report_lines()` 给出的不兼容包说明，`~module list` 等命令读取该文件。发现阶段被剔除的包与导入期失败的包因此都在同一处可见。`return_modules_list()` 按 `(target_from, client_name, platform_from, platform_name)` 四元组缓存平台筛选结果。

### 5.6 组件注册系统 (`akaribot/core/component.py`)

```python
def module(
    module_name: str,
    alias=None,                        # 命令别名（str/list/tuple/dict）
    desc=None,                         # 模块描述，用 {I18N:key} 单花括号语法
    recommend_modules=None,            # 推荐一并开启的模块
    required_admin=False,              # 需要群组管理员权限
    base=False,                        # 基础模块，强制启用，无法被 ~module disable
    doc=False,                         # 有线上文档
    hidden=False,                      # 隐藏模块，不出现在 ~help 列表
    load=True,                         # 是否加载
    rss=False,                         # RSS 模块
    regex=False,                       # 正则模块
    event=False,                       # 事件模块，要求平台可读取全部消息
    required_superuser=False,
    required_base_superuser=False,
    required_bot_permissions=(),       # 开启模块前要求机器人具备的平台权限字段
    suppress_invalid_prompt=False,     # 命令匹配不上任何模板时抑制语法提示
    available_for="*",                 # 可用平台（"*" = 全部）
    exclude_from="",                   # 排除平台
    support_languages=None,
) -> Bind.Module
```

`module()` 定义于 `akaribot/core/component.py:373`，返回 `Bind.Module`（同一文件的 `class Bind`）。包归属由 `PackageRegistry.by_import_path(caller_module)` 解析为「命名空间 + 包名」的包条目，不再从调用方的文件路径推导。

返回的 `Bind.Module` 提供装饰器：

```python
@my_mod.command("template {{I18N:desc}}", *more_templates,
                options_desc=None, required_admin=False,
                required_superuser=False, required_base_superuser=False,
                available_for="*", exclude_from="", load=True, priority=1)
@my_mod.regex(r"pattern", mode="M", flags=re.NOFLAG, desc="...",
              text_only=True, element_filter=None,
              trigger_once_startup=False, skip_long_message_confirm=False)
@my_mod.schedule(trigger)                          # 注册定时任务
@my_mod.hook(name=None, *, point=None, priority=100,
             timeout=5.0, server_scope=False)      # 具名钩子或 parser 入口订阅
@my_mod.event(name, available_for="*", exclude_from="", load=True)
@my_mod.handle(...)                                # 重载版，自动识别 command/regex/schedule
@my_mod.config(cls=None, secret=False)             # 已弃用，改用 on_module_config，见 §5.7
```

`on_command`、`on_regex`、`on_schedule`、`on_hook`、`on_event` 是上述装饰器的别名；命令模板语法与参数映射规则见 `my_mod.command` 的 docstring。模块的常驻状态与后台资源另有 `state()` / `cache()` / `resource()` / `cache_path()` / `cleanup()` / `spawn()` 一组声明式入口，由 `akaribot.core.module_runtime.ModuleRuntimeManager` 在启用、停用、热重载与关闭时接管生命周期；`state()` 的 `preserve=True` 让取值跨代际保留，`version` 变化即作废旧值。`Bind` 由 `akaribot.core.api` 门面导出。

### 5.7 配置系统 (`akaribot/core/config/`)

基于 TOML 的配置系统，支持热重载。核心是 `CFGManager`（`akaribot/core/config/__init__.py:49`），模块末尾在导入期执行一次 `CFGManager.load()`，读取 `config` 目录下顶层的 `*.toml`。

#### 配置项只在模板里声明，取值处直读类属性

**每个配置项有且只有一处定义，即配置模板类。** 取值处不再重复书写键名、默认值、类型与表名：

```python
# 声明：packages/adapters/akari-bot-adapter-onebot/akaribot/adapters/onebot/config.py
@on_bot_config("onebot")
class AiocqhttpConfig:
    qq_typing_emoji: int = 181

# 取值：同包 context.py —— 每次属性访问都走 CFGManager.get()，支持热重载
from akaribot.adapters.onebot.config import AiocqhttpConfig

qq_typing_emoji = str(AiocqhttpConfig.qq_typing_emoji)
```

模板类由 `ConfigMeta` 元类接管属性访问（`akaribot/core/config/decorator.py:26`），读到的是**配置文件里的当前值**而非静态默认值；访问未声明的字段会抛 `AttributeError`，键名拼错当场暴露。

四个声明入口，全部集中在 `akaribot/core/config/decorator.py`：

| 场景 | 写法 | 落在哪 | 模板类 |
|---|---|---|---|
| 表外顶层键 | `@on_base_config()` | `config.toml` 的表外顶层 | `BaseConfig` |
| 核心配置 | `@on_config("config")` / `@on_config("config", secret=True)` | `config.toml` 的 `[config]` / `[secret]` | `CoreConfig` |
| 独立核心配置 | `@on_config("jobqueue")` / `@on_config("jobqueue", secret=True)` | `jobqueue.toml` 的 `[jobqueue]` / `[jobqueue_secret]` | `JobQueueConfig` |
| 平台配置 | `@on_bot_config("onebot")` / `@on_bot_config("onebot", secret=True)` | `bot_onebot.toml` 的 `[bot_onebot]` / `[bot_onebot_secret]` | `AiocqhttpConfig` 等 |
| 模块配置 | `@on_module_config("dice")` / `@on_module_config("dice", secret=True)` | `module_dice.toml` 的 `[module_dice]` / `[module_dice_secret]` | `DiceConfig` 等 |

`on_config()` 是底层入口，只有独立核心配置直接用它；平台与模块各有专用装饰器把表名前缀固定住，不必再手写 `table_type`。四个入口都接受 `standalone_comments` 参数。传入的名称都有约束：

- `on_bot_config("<平台名>")` 的平台名须与 `akaribot/adapters/` 下的**末级目录名**一致——守护进程正是以 `bot_<目录名>` 的表名去查找该平台的 `enable` 配置的，对不上该平台会被判定为禁用。多实例部署下 `CFGManager._resolve_table()` 把 `bot_telegram` 解析为 `bot_telegram-<实例 ID>`，读取可回退基表，写入与删除不回退。
- `on_module_config("<模块名>")` 的模块名通常须与包内 `module()` 声明的一致。若模块主名由下划线迁为连字符，且下划线旧名保留为命令别名，可继续沿用旧配置表名以兼容已有配置。

模块配置**必须**用 `on_module_config`，不要用 `Bind.Module.config()`：后者要求模板反向导入模块对象（`from . import dice`），同包内任何文件在顶层读取该模板都会与包的初始化互相等待而形成循环导入。`on_module_config` 不依赖模块对象，模板因而是叶子模块。

核心模板按职责分布在 `akaribot/core/config/`：表外元数据位于 `base.py`，通用核心项位于 `core.py`，JobQueue、S3、SMTP 与 WebRender 分别位于 `jobqueue.py`、`s3.py`、`smtp.py` 和 `webrender.py`。`JobQueueConfig` 与 `JobQueueSecretConfig` 读取独立 `jobqueue.toml` 的 `[jobqueue]` 与 `[jobqueue_secret]`；S3、SMTP 与 WebRender 同样分别使用各自的 TOML 文件。`base.py` 保留历史类名的兼容重导出；项目内部新增调用应直接从所属领域模块导入，避免重新形成单一配置入口。

`default_locale`、`config_version` 这类位于 `config.toml` 中任何表之外的键归 `BaseConfig` 管（`akaribot/core/config/base.py`）。它们由首次运行骨架 `_init_first_run_config()`（`akaribot/core/entrypoints/run.py:112`）写入、由 `akaribot/core/config/update.py` 的版本迁移维护，模板声明只是提供一个带类型的读取入口：

```python
from akaribot.core.config.base import BaseConfig

default_locale = BaseConfig.default_locale
```

不要改用 `@on_config("config")` 声明它们——那会把键挪进 `[config]` 表内，改变配置文件结构。

#### 配置的生成只发生在 pre_init

`akaribot/core/entrypoints/run.py` 的 `pre_init()` 会调用 `akaribot.core.config.scan.scan_config_templates()` 导入全部配置模板、补全缺失的键，任一模板加载失败即中止启动。`pre_init()` 在独立子进程中执行，随后守护进程置位环境变量 `AKARI_CONFIG_READONLY=1` 再 spawn 子进程，**bot 与 server 子进程一律只读**：

| 方法 | 只读进程中的行为 |
|---|---|
| `CFGManager.write()` / `delete()` / `save()` | 抛 `ConfigOperationError` |
| `CFGManager.get()` 读到缺失的键 | 经 `write()` 回写默认值时抛错；无默认值时返回 `None` 不抛 |
| `CFGManager.load()` / `watch()` | 正常，热重载不受影响 |
| 配置模板导入 | `__config_fields__` 照常登记，不补写配置文件 |

之所以要这道闸门：`multiprocessing` 以 spawn / forkserver 启动子进程时会把主模块以 `__mp_main__` 重新导入一遍，每个子进程都会再跑一次入口模块顶层的模板导入，而 `akaribot/core/config/update.py` 的版本迁移又是导入期执行的（`if not CONFIG_READONLY: import akaribot.core.config.update`）；不隔离会让同一批配置项被多个进程反复补写。

因此**新增配置项后必须重启机器人**，否则子进程读到该键时会抛 `ConfigOperationError`——这是刻意的，用来把「模板漏声明」当场暴露出来，而不是静默退化成默认值。

需要在运行期写配置的只有交互式编辑命令、启动期的共享身份与密钥自举、以及模块热重载补键三类，一律走授权接口：

```python
CFGManager.edit_write("jwt_secret", value, secret=True, table_name="bot_web")
CFGManager.edit_delete("some_key", "module_wiki")
```

`edit_write()` / `edit_delete()` 通过可重入的 `_writable()` 作用域临时解除只读限制，是只读进程中唯一合法的写入途径；`edit_*` 的命名使全部合法写入点可经检索穷举。CLI 侧经子进程调用 `python -m akaribot.core.entrypoints.config schema|get|set|sync` 读写配置。启动期自举见 `bootstrap_jobqueue_config()`（`akaribot/core/config/jobqueue.py:39`），热重载补键见 `ModulesManager._sync_config_fields()`（`akaribot/core/loader.py:155`）。

#### Config() 门面函数

`Config()`（`akaribot/core/config/__init__.py:763`）仅保留给**键名在运行时才确定**的场景。目前生产代码里已无任何 `Config()` 调用，全部配置项都经模板类属性读取；新增调用前先确认真的无法用模板表达。这类调用不得带 `default` 或 `table_name` 参数。

```python
def Config(
    q: str,                              # 配置项键名
    default: Any | None = None,          # 默认值（读不到时写回配置文件）
    cfg_type: type | tuple | None = None, # 类型约束
    secret: bool = False,                # 是否写入 *_secret 表
    table_name: str | None = None,       # 配置表名，模块用 "module_<name>"
    get_url: bool = False,               # 按 URL 处理（补全协议头与尾部斜杠）
    _global: bool = False,               # 内部用：跨所有表查找
    _generate: bool = False,             # 内部用：仅生成不读取
) -> Any
```

需要对模板取到的地址做 URL 补全时，用 `akaribot.core.config.format_url()`，不要另写一遍正则：

```python
from akaribot.core.config import format_url
from akaribot.core.config.webrender import WebRenderConfig

remote_web_render_url = format_url(WebRenderConfig.remote_web_render_url)
```

#### 配置注释规范

**在模板中新增字段时，必须在对应的 locale 文件中添加注释说明。** 键名格式为：

```
`config.comments.<表名>.<字段名>`
```

注释所在的文件按模板归属，随所在包分发：核心配置写 `packages/akari-bot-core/akaribot/core/locales/zh_cn.json`，平台配置写 `packages/adapters/akari-bot-adapter-<平台>/akaribot/adapters/<平台>/locales/zh_cn.json`，模块配置写 `packages/modules/akari-bot-module-<模块>/akaribot/modules/<模块>/locales/zh_cn.json`。生成期把本地化文本写成行尾注释，遗留的 `{I18N:key}` 标记由 `CFGManager.repair_i18n_comments()` 翻译；取不到翻译时跳过该行，不把原始 i18n 键写进配置。

示例：

```json
{
    "config.comments.config.typo_check_module_score": "模块拼写检查容许相似度，范围 0 到 1 之间。",
    "config.comments.bot_telegram.enable": "是否开启 Telegram 客户端。"
}
```

- `@on_config("config")` → `config.comments.config.<字段名>`
- `@on_config("config", secret=True)` → `config.comments.secret.<字段名>`
- `@on_base_config()` → `config.comments.<字段名>`（表外顶层键，没有表名这一层）
- `@on_bot_config("<平台>")` → `config.comments.bot_<平台>.<字段名>`，`secret=True` 时为 `config.comments.bot_<平台>_secret.<字段名>`
- `@on_module_config("<模块>")` → `config.comments.module_<模块>.<字段名>`，`secret=True` 时为 `config.comments.module_<模块>_secret.<字段名>`

当字段需要说明多个选项的差异、限制或故障边界，行尾注释不足以清晰表达时，可通过 `standalone_comments` 在字段前生成多行独立注释块。映射键必须是同一模板中已声明的字段名，值必须是按展示顺序排列的非空 i18n 键元组；字段名或参数形式无效时，模板导入会明确失败。找不到翻译的说明行会被跳过，不会将原始 i18n 键写入 TOML：

```python
@on_config(
    "jobqueue",
    standalone_comments={
        "jobqueue_backend": (
            "config.notes.jobqueue.backend.intro",
            "config.notes.jobqueue.backend.database",
            "config.notes.jobqueue.backend.websocket",
        )
    },
)
class JobQueueConfig:
    jobqueue_backend: str = "websocket"
```

独立注释文本仍存放在模板所属的 `zh_cn.json` 中。普通字段说明继续使用 `config.comments.<配置表名>.<字段名>`；独立说明建议使用 `config.notes.<领域>.<主题>.<说明行>`，以免与行尾注释混淆。

配置文件结构：实例配置目录下每个表一个文件，`CFGManager.load()` 只扫描顶层的 `*.toml`。

```
config/
├── config.toml        # 主配置
├── jobqueue.toml      # JobQueue 后端、Peer 与 Hub 配置
├── s3.toml            # S3 兼容对象存储配置
├── smtp.toml          # 邮件配置
├── webrender.toml     # WebRender 配置
├── bot_onebot.toml    # 平台配置
├── bot_discord.toml   # 平台配置
├── module_wiki.toml   # 模块配置
└── ...
```

CLI 创建实例时还会预留 `config/core`、`config/adapters`、`config/modules` 三个分层子目录，其中 `config/adapters/` 的分层布局尚未启用：适配器的实例配置必须写成扁平路径 `config/<表名>.toml`，写到 `config/adapters/` 的表对 core 不可见。按包的配置迁移（`akaribot/core/config/migration.py`，只认 manifest 的 `config_migrations` 字段显式声明的目录）同样属规划中的能力，当前没有任何包声明该字段，运行器在生产代码中没有调用点。

### 5.8 数据库系统 (`akaribot/core/database/`)

使用 Tortoise ORM，支持 SQLite 和 MySQL。所有模型继承 `akaribot/core/database/base.py:28` 的 `DBModel`（抽象基类，额外提供 `get_by_target_id(target_id, create=True)` 与 `get_by_sender_id(...)`，可以直接传 `MessageSession`）。

**双连接架构**（`init_db()` 里配置两个连接与两个 Tortoise app）：

| 连接 | app 名 | 模型模块 | 用途 |
| --------- | -------------- | ------------------------------------- | ----------------------------- |
| `default` | `models` | `akaribot.core.database.models` + 各模块模型 | 主数据库，可配置为 MySQL |
| `local` | `local_models` | `akaribot.core.database.local` | 永远本地 SQLite（缓存类数据） |

`local` 里目前只有 `DirtyWordCache`（内容审核结果缓存）和 `CrowdinActivityRecords`。这类数据不该跟着主库走，所以单独放。SQLite 连接在建立时先设置 30 秒 `busy_timeout` 再启用 WAL（`akaribot/core/database/link.py`）。

**核心模型** (`akaribot/core/database/models.py`，共 13 个):

union 化之后，用户与场景的数据不再挂在平台 ID 上，而是挂在 **union**（账号组 / 场景组）上，平台 ID 与 union 之间隔着一张映射表。所以核心表分成两层：

| 层 | 模型 | 主键 | 说明 |
|---|---|---|---|
| 数据层 | `SenderUnionInfo` | `union_id` | 用户组数据（权限、花瓣、`sender_data`），表 `sender_union_info` |
| 数据层 | `TargetUnionInfo` | `union_id` | 场景组数据（模块开关、管理员、语言），表 `target_union_info` |
| 映射层 | `SenderUnionBind` | `sender_id` | 平台账号 → union，表 `sender_union_bind` |
| 映射层 | `TargetUnionBind` | `target_id` | 平台场景 → union，附 `channel_id`，表 `target_union_bind` |

两个数据层模型都继承抽象基类 `UnionInfo`，两个映射层模型都继承 `UnionBind`；共用的解析、展开逻辑写在基类上，子类只声明自己的字段与 `union_scope` / `bind_model`。**映射层只回答「这个平台 ID 属于哪个 union」，不承载任何状态**——状态若下放到单个 ID，换用组内另一个 ID 即可绕过。

其余核心模型：

- `StoredData` - 通用键值存储
- `AnalyticsData` - 命令使用统计（同时记原始 ID 与 union ID）
- `ModuleStatus` - 模块加载状态
- `DBVersion` - 数据库版本
- `UnfriendlyActionRecords` - 违规记录（同时记原始 ID 与 union ID）
- `JobQueuesTable` - 任务队列表（跨进程通信的载体）
- `JobQueuePeersTable` - Peer 注册表，以 `peer_id` 为主键
- `MaliciousLoginRecords` - WebUI 恶意登录记录
- `SchemaMigration` - 已应用的迁移 revision 记录，`(package, revision)` 唯一

**union 解析的唯一入口是 `UnionInfo.resolve_union(平台 ID, create=True)`**：它查映射表拿到 union，取出数据行，并把映射行挂到实例的 `.bind` 上。`get_by_target_id()` / `get_by_sender_id()` 是它的会话友好包装（多接受 `MessageSession`），模块表继承 `DBModel` 拿到的同名方法则是「先解析 union，再按 union 取本表的行」。进程内的 union 变更由 `union_mutation()` 上下文串行化。

两个必须记住的约定：

- **封禁只有 `UnionInfo.blocked` 一个字段，不存在「某个 ID 单独被封」这回事。** union 下的全部平台 ID
  共享同一行，所以封禁天然对组内所有 ID 生效，映射表上不需要、也不该再放一份标记。
  封了之后也洗不白：能改变 ID 所属 union 的路径只有 `merge_union`（`blocked` 取并集，只会把封禁
  传染给对方）、`unbind_id`（新组继承 `self.blocked`，且映射行是**改挂**不是删建，任何时刻都不会
  出现「没有映射行」的中间态）和 `bind_id`（已有映射行的 ID 直接拒绝迁组）。`resolve_union()` 只为
  从未见过的 ID 建新组，有映射行的永远解析回原组。
- **模块表若以 `union_id` 为键，必须声明 `union_scope`**（`UNION_SCOPE_SENDER` / `UNION_SCOPE_TARGET`）。
  未声明的表会被 `iter_union_models()` 跳过并告警，即不参与 union 合并与映射补建——
  因为无从判断它存的是账号数据还是场景数据，两个域都处理会把二者互相搬走。

**模块数据库**: 模块可以在包内 `database/models.py` 中定义自己的模型，`init_db()` 通过 `fetch_module_db()`（`akaribot/core/database/__init__.py:33`）自动发现并注册到 `models` app。发现走 `PackageRegistry.db_model_paths()`，按「包根目录下 `database/models.py` 是否存在」判定，只列模块包，不导入文件；文件内部缺依赖时错误在 `init_db()` 真正导入它时抛出。当前有 5 个模块包提供模型：captcha、cytoid、maimai、phigros、wiki。

**按包登记的迁移**（`akaribot/core/database/migration.py`）：迁移文件放在导入包目录下的 `migrations/`（manifest 的 `migrations` 字段可改名），文件名以四位号段开头，模块级声明 `REVISION`，可选 `DEPENDS_ON`，实现 `async def upgrade(ctx)`。`MigrationRunner` 固定先执行 core 的全部待应用 revision，再按包名依次执行各模块包；包名取**分发名**（如 `akari-bot-module-wiki`），因此包名变化不会让旧库已登记的 revision 重新变为待应用。已应用的 revision 记在 `schema_migrations` 表，重复执行按 no-op 处理；MySQL 的 DDL 自动提交，硬规则是每条 revision 的每一步都必须先探测再执行。迁移只在建表的写入进程中执行：`init_db(generate_schemas=True)` 建表后调用 `run_startup_migrations()`，只读进程不建表也不改库结构。CLI 侧入口为 `python -m akaribot.core.entrypoints.db status|upgrade`。

**JobQueue 协议 v2 的数据库升级约束**：旧库从 v4 升级至 v5 时不迁移旧任务记录，而是执行 `DROP TABLE IF EXISTS job_queues`，随后通过 `Tortoise.generate_schemas(safe=True)` 按当前模型重建任务队列表。这一步既是历史升级路径 `akaribot/core/database/legacy.py` 的 v5 步骤，也是 revision `packages/akari-bot-core/akaribot/core/database/migrations/0005_rebuild_job_queues.py`，旧版本号经 `LEGACY_MAP` 映射到该 revision。JobQueue 记录属于临时在途数据，升级后不予保留；执行迁移前必须停止全部 Bot 与 Server 进程。当前数据库版本为 6（`akaribot/core/constants/version.py`），`0004` 号段由模块包承担，core 目录内没有对应文件。

### 5.9 队列系统 (`akaribot/core/queue/`)

可配置后端支撑的 Peer RPC 与信号总线，用于 Client、Server 以及未来其它 Worker 进程之间的异步通信。`jobqueue.toml` 中的 `[jobqueue].jobqueue_backend` 选择一套完整的 `JobQueueBackend`（`backend.py` 的 Protocol 与 `create_jobqueue_backend()` 工厂），其 `PeerRegistry` 与 `MessageTransport` 不得跨后端组合。生产实现包括 `database` 和 `websocket`；未知值、WebSocket 连接失败或鉴权失败时须明确终止初始化，不得自动回退。进程内 `Alive`（`akaribot/core/alive.py`）只作为同步查询缓存，不得作为在线凭据，权威判断以 Registry 为准。代码通过 `akaribot.core.config.jobqueue.JobQueueConfig` 与 `JobQueueSecretConfig` 读取这些配置，不再将 JobQueue 字段并入通用 `CoreConfig`；`akaribot/core/queue/README.md` 是该子系统的权威说明。

新生成的配置默认使用 `websocket`，该后端亦是项目推荐选项。已有 `database` 配置不会被自动改写；当主数据库为 SQLite 时，守护进程会在启动阶段输出非阻断警告。SQLite 连接默认先设置 30 秒 `busy_timeout` 再启用 WAL，数据库传输每轮最多领取 100 条任务；这些措施只减少锁冲突，不改变 SQLite 的单写者边界。

```
Client 进程                    共享数据库                     Server 进程
    │                              │                              │
    │ register(peer_id, service)   │   register(peer_id, service) │
    │ ───────────────────────────> │ <─────────────────────────── │
    │ peer.ready / peer.welcome    │                              │
    │ <────── 独立实例投递 ───────> │                              │
    │                              │                              │
    │ receive_message RPC          │                              │
    │ ───────────────────────────> │ ───── 原子领取 ────────────> │
    │                              │                       parser(msg)
    │ platform.* RPC               │                              │
    │ <─────────────────────────── │ <─────────────────────────── │
```

**核心类**（`akaribot/core/queue/`）:

| 类 / 声明 | 文件 | 说明 |
| --- | --- | --- |
| `JobQueueBase` | `base.py` | 对称的 RPC 调用、结果关联、信号 fan-out、轮询和生命周期 |
| `JobQueueClient` | `client.py` | 平台进程的 RPC handler 与上下文解析 |
| `JobQueueServer` | `server.py` | Server 进程的 parser、事件、模块与查询 handler |
| `JobQueueBackend` | `backend.py` | 后端协议、配置选择及 Registry/Transport 整套装配 |
| `PeerIdentity` / `PeerRegistry` | `peer.py` | 唯一实例身份、状态和权威发现协议 |
| `DatabasePeerRegistry` | `database.py` | 数据库租约、状态、发现及实例失效事务 |
| `MessageTransport` | `transport.py` | 介质无关的请求、响应、批量投递和放弃等待协议 |
| `DatabaseMessageTransport` / `DatabaseJobQueueBackend` | `database.py` | 数据库任务投递、原子领取、回包与整套装配 |
| `WebSocketJobQueueBackend` | `websocket.py` | `httpx-ws` 客户端、ASGI Hub、实时路由、鉴权与背压控制 |
| `InMemoryJobQueueBackend` | `memory.py` | 不依赖 ORM 的后端契约测试基座，不属于生产配置选项 |
| `PeerSelector` / `ServiceRoute` | `peer.py` | 逐实例 fan-out 筛选；按业务键稳定选路 |
| `SignalReceipt` / `SignalReport` | `peer.py` | 信号投递结果与逐实例 ACK 汇总 |
| `RpcMethod` / `SignalMethod` | `rpc.py` | 强类型调用契约、编解码、绑定和信号声明 |
| `PlatformAPI` / `ProcessAPI` / `ServerAPI` | `contracts.py` | 稳定的方法名、调用签名、路由规则与默认超时 |
| 异常、诊断与上报 | `errors.py` / `diagnostics.py` / `reporting.py` | 可跨进程识别的异常类型、进程用量采集与错误上报 |

平台能力在 `contracts.py` 以 `context_method(ContextManager.<能力>)` 声明，客户端启动时按 `ContextManager` 的签名自动绑定并解析上下文；服务端方法以 `@remote()` 声明，在接收进程用 `.bind(JobQueueServer)` 注册实现。直接 `await method(...)` 等待远端结果；`.submit(...)` 只等待当前后端接受投递，不保证最终执行成功。会话绑定的平台操作优先使用 `owner_peer_id` 回到最初接收消息的 Client；主动会话没有 owner 时，使用 `ServiceRoute(service, routing_key, role)` 选择一个稳定实例。

每个进程启动时生成唯一 `peer_id`，以 `role / service / node_id / capabilities / metadata` 注册，并经历 `starting → ready → maintenance/draining → stopped`。运行中每 15 秒续租，每 10 秒按权威 Registry 对账一次，异常退出由租约过期识别。正常启动的 `pre_init` 会在 spawn 任何子进程前检查 `[jobqueue].jobqueue_node_id`；该值缺失、为占位符或仅含空白时，生成 UUID 并写回配置（`bootstrap_jobqueue_config()`）。共用同一配置目录的进程因而共享稳定的部署节点标签，进程级唯一性仍由 `peer_id` 提供。`configure_peer()` 显式参数可覆盖配置；绕过守护进程的入口在配置为空时仍以进程级 UUID 防御性回退，不得从计算机名或其它宿主机信息推导节点标识。配置变更须在相关进程重启后才会反映到 Registry。`peer.ready` 与定向 `peer.welcome` 让新旧进程互相辨认；实际在线判断仍以 Registry 为准，信号只负责降低拓扑变化的传播延迟。

JobQueue 层面的广播用 `@signal()` 声明。发送端先用 `PeerSelector` 快照所有 ready 实例，再为每个目标创建独立逻辑投递；数据库后端为每个目标建立独立队列行。这些投递共享 `correlation_id`，但有各自的 `task_id / ACK / error`，数据库行还分别记录 `claimed_by`。因此一个目标失败不会吞掉或覆盖其它目标的结果：

```python
from akaribot.core.queue.peer import PeerSelector
from akaribot.core.queue.rpc import signal


@signal("cache.invalidate", timeout=30)
async def invalidate(version: int) -> None: ...


@invalidate.bind(JobQueueServer)
async def invalidate_local(version: int) -> None:
    ...


receipt = await invalidate.emit(PeerSelector.role("server"), version=8)
report = await invalidate.gather(PeerSelector.service("Server"), version=8)
```

队列行仅承担投递和回包，不作为审计记录长期保存。`.submit()` / `.emit()` 创建的任务将 `expects_response` 设为 False，处理完成后由接收方直接删除；普通等待型 RPC 与 `.gather()` 的结果由发起方通过 `consume_responses()` 读取后删除。调用方异常退出所遗留的终态行由定时任务兜底清理，`(status, timestamp)` 复合索引用于避免清理查询退化为全表扫描。等待型调用在本地取消或超时后通过 `abandon()` 要求后端尽力清理；数据库后端会删除仍存在的相应队列行。该操作不会取消已经开始的远端处理器，也不得据此推断外部副作用未发生或可以安全重试。

批量投递返回逐任务的 `accepted / rejected / unknown`。`SignalReceipt.deliveries` 只包含后端明确接受的目标，拒绝原因和接受状态未知的 Peer 分别位于 `errors` 与 `unknown`。接收端通过 `respond(request, response)` 回包，原请求为 WebSocket 等无状态响应帧提供来源路由上下文。新增生产后端前，先使用共享 `InMemoryBroker` 的 `InMemoryJobQueueBackend` 运行相同的双向 RPC、信号 fan-out 和 Peer 失效测试，以确认 Runtime 没有重新依赖 ORM；不得将 `memory` 暴露为用户配置值。

WebSocket 后端使用独立 Hub 同时承担 Registry 与 Transport。内置模式由 `akaribot.core.entrypoints.run` 在 Bot 和 Server 之前启动名为 `jobqueue-hub` 的子进程（`run_websocket_hub_process`），关闭顺序则相反；外部模式只连接配置的 Hub URL，项目所附 Hub 可用 `python -m akaribot.core.queue.websocket` 独立启动。`jobqueue_websocket_mode = "embedded" | "external"` 明确部署模式，不根据 URL 主机推断；`jobqueue_websocket_url` 是唯一地址来源：内置模式从它解析监听主机、端口与路径，要求使用回环 `ws` 地址；外部模式把它仅作为连接地址，非回环连接必须使用 `wss` 并配置共享令牌。需要区分监听地址与公开连接地址的多节点或反向代理部署应使用外部模式，不得增加重复的 bind host/port 配置。`pre_init` 会为缺失、占位或空白的 `jobqueue_websocket_token` 生成 256 位安全随机密钥并写回密钥表，确保随后启动的 Hub、Bot 和 Server 读取同一值；外部 Hub 与多配置目录部署必须显式分发同一密钥，清空字段会在下次启动时触发密钥轮换。Hub 以握手身份覆盖请求自报的 `source_peer_id`，拒绝重复 Peer、越权状态修改和非目标回包；每个 Peer 的出站队列与协议帧大小有上限，队列满时明确拒绝新投递，控制命令超时按 unknown 处理。Hub 不持久化离线任务或在途结果，目标断线后将直投任务终结为 unavailable，且不得重新分配可能已经执行的副作用请求；超过 deadline 的请求关联状态及时释放并向仍在线的来源返回 timeout，该清理不表示已经开始的远端副作用被撤销。

多实例语义必须区分：service 字符串是竞争消费的 anycast；`peer_id` 是实例直投；`ServiceRoute` 是按业务键稳定分流；`PeerSelector` 是逐实例 fan-out。不要用一条 service 队列记录模拟广播，否则只会被一个实例领取。

当前 JobQueue 已预留同类型多 Client / Server 的发现、分流、回源、摘流和广播能力，但真正开启多 Server 还需要 Scheduler leader election、模块热重载的共享 epoch、Server 内存会话故障策略及副作用幂等。模块热重载不能直接在当前 Queue handler 内同步广播到所有 Server：目标实例进入维护窗口时可能等待发起 handler，而发起 handler 又等待广播 ACK，形成分布式死锁；跨实例控制操作应由稳定协调者或独立控制面发起。同账号多 Client 的平台 SDK 入口还需适配器层实现分片、租约或事件去重，JobQueue 只能分流已经进入系统的任务。广播是发送时的在线实例快照，不负责向离线实例重放；必须补齐的状态应持久化 version / epoch，实例启动后主动对账。

> **注意**：数据库后端以轮询而非共享内存传递任务，两个进程之间**不共享任何 Python 对象**。要跨进程传的东西必须能序列化（`MessageChain.to_list()` / `SessionInfo` 的 cattrs 序列化就是为此），未经登记的对象不会经 pickle 或动态导入在进程之间传递。

相关验证入口位于 `packages/akari-bot-core/tests/`：`test_jobqueue_backend.py`、`test_jobqueue_memory_backend.py`、`test_jobqueue_websocket_backend.py`、`test_jobqueue_daemon.py`、`test_rpc_contracts.py`、`test_rpc_transport.py`、`test_rpc_process.py`、`test_queue_lifecycle.py`、`test_peer_signals.py`，执行时设置 `CI=1` 与 `PYTHONIOENCODING=UTF-8`。

---

### 12.1 导出系统（避免循环导入）

```python
# akaribot/core/exports.py
class Exports(dict):
    def register(self, exporter: Type[T], name=None):
        self[exporter.__name__ if not name else name] = exporter

    def get(self, name, default: T = None) -> T:
        return self[name] if name in self else default


exports = Exports()
add_export = exports.register
```

```python
# 注册（在被导出对象定义处）
from akaribot.core.exports import add_export
add_export(Bot)

# 使用（在会造成循环导入的地方）
from akaribot.core.exports import exports
Bot = exports["Bot"]              # 或 exports.get("Bot") 拿可选值
```

注意 `exports.get()` 覆盖了 `dict.get` 的类型签名以便类型标注，行为一致（缺失返回 `default`）。取用要放在函数体里、而不是模块顶层，否则可能在注册之前就取到 `None`。core 自身的 `DBModel.get_by_target_id()` 经 `exports.get("Bot")` 取会话类型，`Bot`、`MessageSession`、`MessageChain`、`CFGManager` 与被 `add_export(_process_class)` 登记的配置模板处理函数则在定义处注册。

---

### 12.7 热重载

```python
ok, count = await ModulesManager.reload_module("module_name")
# count 为重新导入的 Python 模块数；重载失败或整体回滚时 ok 为 False
```

重载按下述顺序推进。忙碌时直接返回 `(False, 0)`，不排队等待另一场重载释放锁；先排空 Queue handler 再进入 Scheduler 维护窗口，反序会形成互锁。`return_py_module()` 定位所属包，`_reload_closure()` 取依赖优先的重载闭包，图源是「分发包声明的依赖 ∪ AST 扫描结果」，AST 扫出而 metadata 未声明的耦合仍然计入并只告警一次。随后快照 `sys.modules`、模块注册、hook 订阅、运行时资源、`ModuleStatus` 与 Scheduler Job，`remove_modules()` 后逐包 `reload_py_module()`：清空 `sys.modules` 中的包前缀再重新导入，而不是对单个模块做 `importlib.reload()`。提交前校验新包已注册模块、配置模板已补键、ORM 模型结构未变，最后重建 `ModuleStatus`、重挂数据库 context、切换运行时代际并关闭旧连接。

`reload_py_module()` 失败时返回 `-999`（不是抛异常），`count <= 0` 即视为失败，调用方要判 `ok`。重载过程中模块的状态、资源与后台任务由 `ModuleRuntimeManager` 的代际机制接管（`prepare_reload()` 冻结旧代际，`commit_reload()` 切换并停止旧任务，`abort_reload()` 在失败路径恢复）。locale 指纹变化的包触发 `build_locale_snapshot()` 重建 i18n 快照；ORM 模型结构指纹变化的包被拒绝重载并提示重启后执行数据库迁移。数据库挂载点重建失败、模板补键失败或新包没有注册任何模块时，注册表、`sys.modules`、`ModuleStatus`、Scheduler Job 与运行时资源都会回滚到快照；重载协程被取消时同样先回滚再继续传播取消。

包级装载与拆卸走同一把锁与同一套维护窗口：`install_package()` 首次导入已装好但尚未接入的模块包（会重挂数据库 context 以纳入新包的模型），`remove_package()` 停用全部注册名、把包摘出发现层索引、重挂不含该包模型的数据库 context 并清理 `sys.modules`。两者与 `reload_module()` 共用 `JobQueueServer.maintenance_window(exclusive=False)` 与 `SchedulerLifecycle.maintenance_window()`；数据库 context 的切换与旧连接关闭在独占窗口内完成，避免轮询器在旧连接关闭过程中仍发出查询。`load_module()` / `unload_module()` 只改单个模块的启用状态，同样在维护窗口中写入 `ModuleStatus`，失败时按旧值回滚。

**常用验证命令**（仓库根目录执行）：

```bash
uv sync --all-extras --dev                 # CI 的口径为 --locked --all-extras --dev

CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing
.venv/bin/python tester.py                 # 兼容层，等价于上一行的模块入口
.venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_loader.py

.venv/bin/ruff check . && .venv/bin/ruff format --check .
.venv/bin/python tools/lint_comments.py    # 注释书面语与块长
.venv/bin/python tools/lint_boundaries.py  # 分层、命名空间、依赖声明
.venv/bin/python tools/lint_versions.py    # 内部版本约束一致性
.venv/bin/python tools/check_versions.py --base <ref>   # 版本守卫，CI 在 PR 阶段以 base 为基准运行
```

门禁与 CI 步骤同源，见 `.github/workflows/run-builtin-tester.yml`。`bot.py` 与 `tester.py` 只是根目录兼容层：前者转发到 `akaribot.core.entrypoints.run`，后者转发到 `akaribot.testing.runner`，真实入口分别是 `python -m akaribot.core.entrypoints.run` 与 `python -m akaribot.testing`。core 的命令行入口统一为 `python -m akaribot.core.entrypoints.<名>`（run / registry / config / db / peers / modules），CLI 与 core 之间只经子进程交互，每个入口自行解析 `AKARI_INSTANCE_DIR`。`tests/run_one.py` 单入口脚本的第二个参数是入口函数名，缺省时运行该文件内全部 `test_*` 函数。
