# 配置

配置由 `core.config.CFGManager` 统一读写，配置模板类在导入期为每个字段登记读取参数。所有配置文件
平铺在 `config/` 下，`CFGManager.load()` 只扫描 `config/*.toml`。

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

密钥始终与公开配置同文件，以 `_secret` 后缀区分。多实例部署下适配器表名带实例后缀，例如
`bot_telegram-alt`；读取时若实例表缺失可回退到基表，写入一律落到实例表，避免串改另一个实例。

## 模板声明

模板类在所属包内声明，装饰器决定表名：

| 装饰器 | 表名 | 使用方 |
| --- | --- | --- |
| `@on_base_config()` | 表外顶层键 | `config.toml` 的 `default_locale`、`config_version` |
| `@on_config("config")` | `[config]` | 核心公开配置 |
| `@on_config("config", secret=True)` | `[secret]` | 核心密钥 |
| `@on_bot_config("telegram")` | `bot_telegram` | 适配器 |
| `@on_module_config("dice")` | `module_dice` | 模块 |

字段的类型标注与默认值决定生成内容：

- 支持的类型为 `bool`、`datetime`、`date`、`float`、`int`、`list`、`str`；列表默认值写成 `[]`。
- 无默认值的必填项生成 `<Replace me with <type> value>` 占位符，读取时统一返回 `None`。
- 含不受支持成员的联合类型（如 `str | None`）生成通用占位符 `<Replace me>`。
- 键名统一转为小写后存取。

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
| `CFGManager.get(q, default=None, cfg_type=None, secret=False, table_name=None)` | 读值，缺失时按默认值补写 |
| `CFGManager.has(q, secret=False, table_name=None)` | 判断键是否存在 |
| `CFGManager.write(...)` | 写入，受只读约束 |
| `CFGManager.edit_write(...)`、`edit_delete(...)` | 交互式编辑授权写入 |
| `CFGManager.save()` | 仅重写内容有变化的文件 |

读取到占位符时返回 `None`；值类型与模板不符时记录警告并原样返回。

## 字段注释

字段在模板类中声明后，须在所属包的 `locales/zh_cn.json` 增加注释键：

```text
config.comments.<表名>.<字段名>
```

表名取值：核心公开项与密钥项分别为 `config`、`secret`；适配器为 `bot_<平台>`，密钥为
`bot_<平台>_secret`；模块为 `module_<模块>`，密钥为 `module_<模块>_secret`。注释只描述用途，
不描述实现细节。生成配置时注释随字段写入，切换 `default_locale` 后由
`CFGManager.repair_i18n_comments()` 按新语言重写。

## 只读约束

- 守护进程在派生子进程前置位 `AKARI_CONFIG_READONLY`，平台进程与 Server 均只读。
- 只读进程调用 `write()` 或 `save()` 抛出 `ConfigOperationError`；`edit_write()`、`edit_delete()`
  在显式授权范围内放行，供 `~config` 与启动期密钥自举使用。
- 缺失项只在 pre-init 阶段补写，普通进程不会因读取而改写磁盘。
- 读改写以 `config/.config.lock` 做进程间互斥，等待上限 10 秒，锁文件超过 60 秒视为陈旧。
- 写入使用临时文件加 `os.replace` 原子替换。
- 文件 mtime 变化时在 1 秒节流窗口内重新加载；磁盘文件被清空而内存仍有内容时保留内存值。

## 配置版本

`config.toml` 的 `config_version` 当前为 6，由 `core.config.update` 执行升级。其余配置文件的版本随包
维护：迁移脚本放在包的 `config_migrations/`，文件名以四位号段开头，升级后把号段写回该文件的
`config_version`。新生成的配置写入 `manifest.toml` 的 `config_schema_version`，首个迁移号段须从
该值加一开始，号段不得复用或跳号。
