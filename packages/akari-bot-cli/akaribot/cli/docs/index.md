# CLI 与 TUI

`akaribot` 是 AkariBot 的实例管理工具，提供命令行子命令与终端交互界面（TUI）。它安装在实例的 venv 之外，可以使用系统解释器安装，也可以安装为独立工具。实例中的机器人、模块与适配器，由 CLI 通过子进程启动。

自搭建实例的完整流程参见 [自搭建指南](self-hosting.md)。

## 安装

先将 CLI 安装为独立工具，再确认版本。

```sh
uv tool install akari-bot-cli
akaribot --version
```

运行环境必须满足仓库 `pyproject.toml` 声明的 Python 版本。CLI 不依赖 `akaribot.core`。实例所需的 core、适配器与模块，由 `akaribot init` 安装至实例独立的 venv 中。

## 实例解析

多数子命令需要一个实例根目录（含 `akaribot.toml` 的目录）。解析顺序固定为：

1. `--instance` / `-I` 给出的路径。
2. 环境变量 `AKARI_INSTANCE_DIR`。
3. 自当前目录向上查找 `akaribot.toml`。

若上述三种方式均未找到实例，命令会输出错误提示，并提示先执行初始化或指定实例根目录。

直接运行 `akaribot` 或 `akaribot tui` 时属于例外情况。若上述三种方式均未找到实例，界面会改用注册表中的默认实例，即未明确指定实例时的目标实例。注册表位于 `~/.akaribot/instances.toml`，由 `akaribot instance` 子命令维护。

## 目录结构

实例根目录下的关键路径：

| 路径 | 内容 |
| --- | --- |
| `akaribot.toml` | 实例元数据（包含名称、语言、venv、解释器与来源） |
| `config/` | 扁平配置表，`<表名>.toml` |
| `data/` | 模块数据与实例私有资产 |
| `database/` | 默认 SQLite 数据库 |
| `logs/` | 进程日志，文件名形如 `<进程>[_debug]_<日期>.log` |
| `cache/` | 可清理的缓存，包括文档站点生成产物 |
| `.bot.lock` | 运行锁，记录持锁进程与启动参数 |

## 命令总览

| 子命令 | 用途 |
| --- | --- |
| `init` | 创建实例、写入元数据、安装 core 与适配器 |
| `run` | 前台或后台启动、停止、重启、查看状态 |
| `service` | 安装常驻服务并守护本机实例 |
| `test` | 在实例环境中运行自研测试框架 |
| `module` | 模块与适配器的安装、卸载、更新与全局加载 |
| `config` | 配置表、字段、读写与外部编辑器 |
| `db` | 浏览数据库表与数据项，按主键写入 |
| `instance` | 本机实例列表、默认实例与服务策略 |
| `adapter` | 查看、添加和删除适配器实例 |
| `venv` | 管理实例 venv（接管、交还或重建） |
| `doctor` | 检查端口冲突、重复的登录信息，以及没有对应适配器的配置 |
| `docs` | 汇总已安装包的文档，构建、预览与部署 VitePress 站点 |
| `new` | 生成模块包或适配器包的脚手架 |
| `tui` | 启动交互界面，或执行界面自检 |
| `logs` | 查看、跟踪与按级别筛选实例日志 |
| `migrate` | 将旧版布局的项目迁移为新实例 |

每个子命令的选项参见 [命令参考](commands.md)。

## 与 core 的子进程边界

CLI 进程不导入 core。需要 core 参与的读写操作，一律交由实例的解释器执行：

```sh
<实例>/.venv/bin/python -m akaribot.core.entrypoints.<入口> ...
```

CLI 向子进程传入 `AKARI_INSTANCE_DIR` 与 `AKARI_CONFIG_PATH` 两个环境变量，标准输出与退出码由命令层解析。

读取目录、锁文件与注册表等本地状态时，CLI 支持直接读取本地文件。

涉及配置结构、模块清单、数据库或环境检查的判断，则交由子进程完成。

使用 Nuitka 打包后，`sys.executable` 指向二进制文件本身，CLI 因此不使用其启动实例进程。非托管模式下所需的解释器由 `system_python()` 解析，支持使用 `AKARIBOT_PYTHON` 覆盖。

## 界面与命令的关系

直接运行 `akaribot`（可交互终端）或 `akaribot tui` 进入界面。界面的写入操作同样交由 `akaribot <子命令>` 子进程执行，不重复实现命令层的校验与确认逻辑。详情参见 [终端界面](tui.md)。

## 本地化

界面文案由 CLI 自带的语言文件提供，`--lang zh_cn` / `--lang en_us` 指定本次调用的语言。实例的默认语言在 `akaribot init --locale` 时写入元数据，`--lang` 仅影响本次调用。
