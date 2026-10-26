# CLI 与 TUI

`akaribot` 是 AkariBot 的实例管理工具，提供命令行子命令与终端交互界面（TUI）。它运行在实例的
venv 之外，用系统解释器或独立工具安装都能工作；实例内的机器人、模块与适配器由子进程驱动。

自建实例的安装、运行与维护流程见 [自建实例](self-hosting.md)。

## 安装

```sh
uv tool install akari-bot-cli
akaribot --version
```

要求 Python 3.12 或更高版本。CLI 不依赖 `akaribot.core`，实例需要的 core、适配器与模块由
`akaribot init` 装进实例自己的 venv。

## 实例解析

多数子命令需要一个实例根（含 `akaribot.toml` 的目录）。解析顺序固定为：

1. `--instance` / `-I` 给出的路径；
2. 环境变量 `AKARI_INSTANCE_DIR`；
3. 自当前目录向上查找 `akaribot.toml`。

上述三级都取不到实例时，命令报错并提示先初始化或指定实例根。裸运行 `akaribot` 或 `akaribot tui`
例外：界面在三级都落空时还会回落到注册表里的缺省实例，因为那正是「这台机器上要管哪一个」的
答案。注册表位于 `~/.akaribot/instances.toml`，由 `akaribot instance` 子命令维护。

## 目录结构

实例根下的关键路径：

| 路径 | 内容 |
| --- | --- |
| `akaribot.toml` | 实例元数据：名、语言、venv、解释器与来源 |
| `config/` | 扁平配置表，`<表名>.toml` |
| `data/` | 模块数据与实例私有资产 |
| `database/` | 默认 SQLite 数据库 |
| `logs/` | 进程日志，文件名形如 `<进程>[_debug]_<日期>.log` |
| `cache/` | 可丢弃的缓存，包括文档站点生成物 |
| `.bot.lock` | 运行锁，记录持锁进程与启动参数 |

## 命令总览

| 子命令 | 用途 |
| --- | --- |
| `init` | 创建实例、写元数据、安装 core 与适配器 |
| `run` | 前台或后台启动、停止、重启、查看状态 |
| `service` | 安装常驻服务并守护本机实例 |
| `test` | 在实例环境里运行自研测试框架 |
| `module` | 模块与适配器的安装、卸载、更新与全局装载 |
| `config` | 配置表、字段、读写与外部编辑器 |
| `db` | 浏览数据库表与数据项，按主键写入 |
| `instance` | 本机实例登记、缺省实例与服务策略 |
| `adapter` | 适配器实例的列出与增删 |
| `venv` | 实例 venv 的托管、接管、交还与重建 |
| `doctor` | 端口冲突、凭据重复与孤立配置检查 |
| `docs` | 汇总已安装包的文档，构建、预览与部署 VitePress 站点 |
| `new` | 生成模块包或适配器包的脚手架 |
| `tui` | 启动交互界面，或执行界面自检 |
| `logs` | 查看、跟随与按级别筛选实例日志 |
| `migrate` | 把旧版布局的项目迁移成新实例 |

每个子命令的选项见 [命令参考](commands.md)。

## 与 core 的子进程边界

CLI 进程不 import core。需要 core 参与的读写一律经实例解释器执行：

```sh
<实例>/.venv/bin/python -m akaribot.core.entrypoints.<入口> ...
```

子进程环境注入 `AKARI_INSTANCE_DIR` 与 `AKARI_CONFIG_PATH`，标准输出与退出码由命令层解释。
读取目录、锁文件与注册表这类本机状态时，CLI 可以直接读文件；涉及配置 schema、模块清单、
数据库或体检的判断都在子进程内完成。

冻结分发（Nuitka）下 `sys.executable` 指向二进制自身，CLI 因此不拿它启动实例进程；非托管
模式需要的解释器由 `system_python()` 解析，可用 `AKARIBOT_PYTHON` 覆盖。

## 界面与命令的关系

直接运行 `akaribot`（可交互终端）或 `akaribot tui` 进入界面。界面的写操作同样以
`akaribot <子命令>` 子进程执行，不复制命令层的校验与确认逻辑；详情见 [终端界面](tui.md)。

## 本地化

界面文案由 CLI 自带的语言文件提供，`--lang zh_cn` / `--lang en_us` 指定本次调用的语言。
实例的默认语言在 `akaribot init --locale` 时写入元数据，两者互不覆盖。
