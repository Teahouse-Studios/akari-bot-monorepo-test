# 配置

本文介绍配置文件与表的布局、模板声明、读写接口与只读限制。

`core.config.CFGManager` 负责读写配置。配置模板类在导入时确定每个字段的读取方式。

用户配置放在 `config/` 根目录，全局默认值放在 `config/global/`。`CFGManager.load()` 会同时读取这两个位置。全局文件提供默认值，用户文件中的同名配置覆盖这些默认值。

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

密钥始终与公开配置同文件，以 `_secret` 后缀区分。

## 全局默认层

`config/global/` 存放只读的默认配置，文件名与用户配置对应：

| 文件 | 用途 |
| --- | --- |
| `<表名>.global.toml` | TOML 格式的全局默认值 |
| `<表名>.global.json` | JSON 格式的全局默认值 |

加载时，`CFGManager` 先读全局文件，再读 `config/<表名>.toml`。

两层配置会递归合并。用户配置覆盖同名的标量、列表和子表。用户文件只写需要修改的字段即可，其余字段继续使用全局值。

写入、删除与配置注释修复只修改用户文件，不修改 `config/global/`。

删除用户文件里的某个键后，这个键会回到全局默认值。

删除整个用户文件后，这个表只使用全局文件。全局文件缺失时，启动不受影响。

```toml
# config/global/config.global.toml
[config]
command_prefix = ["~"]

# config/config.toml
[config]
command_prefix = ["!"]  # 只覆盖这一项，其余键仍取全局值
```

多实例部署下，适配器表名带实例后缀，例如 `bot_telegram-alt`。如果实例表不存在，读取时会改用该平台的基础表。写入只落到实例表。

## 模板声明

模板类在所属包内声明，装饰器用来指定表名：

| 装饰器 | 表名 | 使用方 |
| --- | --- | --- |
| `@on_base_config()` | 表外顶层键 | `config.toml` 的 `default_locale`、`config_version` |
| `@on_config("config")` | `[config]` | 核心公开配置 |
| `@on_config("config", secret=True)` | `[secret]` | 核心密钥 |
| `@on_bot_config("telegram")` | `bot_telegram` | 适配器 |
| `@on_module_config("dice")` | `module_dice` | 模块 |

生成的内容取决于字段的类型标注与默认值：

- 支持的类型为 `bool`、`datetime`、`date`、`float`、`int`、`list`、`str`。列表默认值写成 `[]`。
- 无默认值的必填项生成 `<Replace me with <type> value>` 占位符，读取时返回 `None`。
- 联合类型中含不受支持的成员时（如 `str | None`），生成通用占位符 `<Replace me>`。
- 键名会先转成小写，再读写。

## 读取与写入

模板类通过元类按属性名取值，未声明的字段直接抛 `AttributeError`：

```python
from akaribot.core.api import CoreConfig

if CoreConfig.enable_analytics:
    ...
```

底层接口：

| 方法 | 说明 |
| --- | --- |
| `CFGManager.get(q, default=None, cfg_type=None, secret=False, table_name=None)` | 读值，缺失时按默认值写入 |
| `CFGManager.has(q, secret=False, table_name=None)` | 判断键是否存在 |
| `CFGManager.write(...)` | 写入，受只读限制 |
| `CFGManager.edit_write(...)`、`edit_delete(...)` | 交互式编辑写入，需明确授权 |
| `CFGManager.save()` | 仅重写内容有变化的文件 |

读取到的值是模板写入的占位符（如 `<Replace me with <type> value>` 或 `<Replace me>`）时，返回 `None`。值类型与模板不符时，给出警告并返回原值。

## 字段注释

字段在模板类中声明后，须在所属包的 `locales/zh_cn.json` 中为它写一条配置注释：

```text
config.comments.<表名>.<字段名>
```

表名取值：

- 核心公开表为 `config`，核心密钥表为 `secret`。
- 适配器表为 `bot_<平台>`，适配器密钥表为 `bot_<平台>_secret`。
- 模块表为 `module_<模块>`，模块密钥表为 `module_<模块>_secret`。

配置注释用于说明这个字段的作用。生成配置时，注释和字段一起写入。切换 `default_locale` 后，`CFGManager.repair_i18n_comments()` 会按新语言重写注释。

## 只读限制

- 守护进程在启动子进程前把 `AKARI_CONFIG_READONLY` 设为 `1`，平台进程与 Server 均只读。
- 只读进程中调用 `write()` 或 `save()` 会抛出 `ConfigOperationError`。`edit_write()`、`edit_delete()` 只能在明确授权的范围内使用。`~config` 命令和启动阶段补充缺失的配置与密钥时会调用这两个方法。
- 缺失项只在启动前的准备阶段写入。
- 写入时会先获取 `config/.config.lock` 的锁。重新加载、修改与保存都在持有锁的期间完成，同一时间只有一个进程可以执行。最多等待 10 秒。锁文件超过 60 秒没有更新时，视为过期锁。
- 写入使用临时文件加 `os.replace` 原子替换。
- 文件 mtime 变化后，最多延迟 1 秒重新加载。磁盘文件被清空而内存仍有内容时，保留内存中的值。

## 配置版本

`config.toml` 的 `config_version` 当前为 6，由 `core.config.update` 执行升级。

其他配置文件的版本由所属包维护。迁移脚本放在包的 `config_migrations/` 下，文件名以四位编号开头。迁移执行后，迁移编号会写回该配置文件的 `config_version`。

新生成的配置文件会把 `manifest.toml` 的 `config_schema_version` 写入自身的 `config_version`。第一次迁移的编号必须是 `config_schema_version` 的值加 1，后续每次迁移的编号依次递增。
