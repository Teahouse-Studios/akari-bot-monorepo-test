# 配置

本文介绍配置文件与表的布局、模板声明、读写接口与只读限制。

`core.config.CFGManager` 负责配置的读取与持久化。配置模板类在模块导入阶段确定各字段的解析规则与转换方式。

用户配置文件位于 `config/` 目录，全局默认配置位于 `config/global/`。`CFGManager.load()` 会同时读取两个路径，由全局配置提供备用默认值，用户配置文件中的同名项优先覆盖默认值。

## 文件与表布局

| 文件 | 表 | 用途 |
| --- | --- | --- |
| `config.toml` | `[config]`、`[secret]`，另有顶层 `default_locale`、`config_version` | 核心配置与核心密钥 |
| `jobqueue.toml` | `[jobqueue]`、`[jobqueue_secret]` | 通信后端与 Hub 令牌 |
| `s3.toml` | `[s3]`、`[s3_secret]` | 对象存储 |
| `smtp.toml` | `[smtp]`、`[smtp_secret]` | 邮件上报 |
| `webrender.toml` | `[webrender]` | 网页渲染 |
| `bot_<平台>.toml` | `[bot_<平台>]`、`[bot_<平台>_secret]` | 适配器配置 |
| `module_<模块>.toml` | `[module_<模块>]`、`[module_<模块>_secret]` | 模块配置 |

密钥配置与公开配置保存在同一文件内，通过 `_secret` 配置表名称后缀予以区分。

## 全局默认层

`config/global/` 存放只读的默认配置，文件名称与用户配置对应：

| 文件 | 用途 |
| --- | --- |
| `<表名称>.global.toml` | TOML 格式的全局默认值 |
| `<表名称>.global.json` | JSON 格式的全局默认值 |

加载时，`CFGManager` 首先读取全局配置，随后加载 `config/<表名称>.toml`。

两层配置执行递归合并。用户配置优先覆盖同名的标量、列表及子表。用户文件仅需声明需要调整的项，未声明项自动继承全局配置值。

写入、删除与配置注释修复仅修改用户文件，不改动 `config/global/`。

删除用户配置文件中的某个键后，该配置键将回退至全局默认值。

若删除整个用户配置文件，该配置表仅使用全局文件。当全局文件缺失时，实例启动不受影响。

```toml
# config/global/config.global.toml
[config]
command_prefix = ["~"]

# config/config.toml
[config]
command_prefix = ["!"]  # 只覆盖这一项，其余键仍取全局值
```

在多实例部署下，适配器配置表名称带有实例后缀（如 `bot_telegram-alt`）。若实例表不存在，读取操作将回退至该平台的基础配置表。写入操作则仅作用于对应的实例表。

## 模板声明

模板类在所属成员包内声明，装饰器用于指定表名称：

| 装饰器 | 表名称 | 使用方 |
| --- | --- | --- |
| `@on_base_config()` | 配置表之外的顶层键 | `config.toml` 的 `default_locale`、`config_version` |
| `@on_config("config")` | `[config]` | 核心公开配置 |
| `@on_config("config", secret=True)` | `[secret]` | 核心密钥 |
| `@on_bot_config("telegram")` | `bot_telegram` | 适配器 |
| `@on_module_config("dice")` | `module_dice` | 模块 |

生成的内容取决于字段的类型标注与默认值：

- 支持的类型为 `bool`、`datetime`、`date`、`float`、`int`、`list`、`str`。列表默认值写成 `[]`。
- 无默认值的必填项生成 `<Replace me with <type> value>` 占位符，读取时返回 `None`。
- 联合类型中包含不受支持的成员时（如 `str | None`），生成通用占位符 `<Replace me>`。
- 键名称统一转换为小写后执行读写操作。

## 读取与写入

模板类通过元类机制依据属性名解析配置值，访问未声明的字段将直接抛出 `AttributeError`：

```python
from akaribot.core.api import CoreConfig

if CoreConfig.enable_analytics:
    ...
```

底层接口：

| 方法 | 说明 |
| --- | --- |
| `CFGManager.get(q, default=None, cfg_type=None, secret=False, table_name=None)` | 读取配置项数值，缺失时写入默认值 |
| `CFGManager.has(q, secret=False, table_name=None)` | 检查配置键是否存在 |
| `CFGManager.write(...)` | 执行配置写入（受只读约束） |
| `CFGManager.edit_write(...)`、`edit_delete(...)` | 交互式编辑写入与删除（必须获得明确授权） |
| `CFGManager.save()` | 仅持久化内容发生变动的配置文件 |

若读取到的值为模板写入的占位符（如 `<Replace me with <type> value>` 或 `<Replace me>`），返回 `None`。若配置值类型与模板不符，系统给出警告并返回原值。

## 字段注释

在模板类中声明字段后，必须在所属成员包的 `locales/zh_cn.json` 中为其补充对应的配置注释项：

```text
config.comments.<表名>.<字段名>
```

表名称取值：

- 核心公开表为 `config`，核心密钥表为 `secret`。
- 适配器表为 `bot_<平台>`，适配器密钥表为 `bot_<平台>_secret`。
- 模块表为 `module_<模块>`，模块密钥表为 `module_<模块>_secret`。

配置注释用于说明对应字段的用途。生成配置文件时，注释与字段一并写入。切换 `default_locale` 后，`CFGManager.repair_i18n_comments()` 会按新语言重写注释。

## 只读约束

- 守护进程在启动子进程前将 `AKARI_CONFIG_READONLY` 设置为 `1`，平台进程与 Server 均设为只读模式。
- 在只读进程中调用 `write()` 或 `save()` 会抛出 `ConfigOperationError`。`edit_write()`、`edit_delete()` 仅能在明确授权的范围内使用。`~config` 命令和启动阶段补充缺失的配置与密钥时会调用这两个方法。
- 缺失项仅在启动前的准备阶段写入。
- 配置写入前必须获取文件锁 `config/.config.lock`。重新加载、内存修改与文件保存均在持有该锁期间执行，同一时间仅允许单一进程执行写入操作。获取锁的最长等待时间为 10 秒，锁文件超过 60 秒未更新即视为过期。
- 写入过程采用临时文件加 `os.replace` 执行原子替换。
- 当文件 mtime 发生变更后，系统最多延迟 1 秒触发重新加载。若磁盘文件被清空但内存缓存有效，则继续保留内存中的当前配置值。

## 配置版本

`config.toml` 的 `config_version` 由 `core.config.update` 执行升级。

其余配置文件的版本由所属成员包维护。配置迁移脚本存放于包内 `config_migrations/` 目录，文件名称以四位数字编号开头。迁移执行完成后，当前迁移编号将写回该配置文件的 `config_version` 字段。

新生成的配置文件将 `manifest.toml` 中的 `config_schema_version` 作为初始 `config_version`。首个迁移脚本的编号必须为 `config_schema_version` 数值加 1，后续迁移编号依次单调递增。
