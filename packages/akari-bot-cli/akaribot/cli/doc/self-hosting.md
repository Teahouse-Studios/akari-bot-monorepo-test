# 自建实例

`akaribot` 把 core、适配器、模块与配置装进独立实例目录，CLI 本身安装在实例之外，通过子进程管理
实例。本文覆盖从安装到日常维护的流程。

## 前置条件

- Python 3.12 或更高版本，CLI 与实例环境要求一致。
- [uv](https://docs.astral.sh/uv/)：创建实例 venv 并安装分发包。
- Node.js 18 或更高版本：仅构建文档站点时需要，且 `npm` 须在 `PATH` 中。

默认数据库为 SQLite，连接串 `sqlite://database/save.db`。默认安装的 core 已带 MySQL 驱动，可在
密钥表把 `db_path` 换成 MySQL 连接串。

## 安装 CLI

```sh
uv tool install akari-bot-cli
akaribot --version
```

## 创建实例

```sh
akaribot init /opt/akaribot --adapter telegram --adapter web --locale zh_cn
```

`init` 依次创建目录、写入 `akaribot.toml`、建立 `.venv`、安装 core 与适配器、生成配置骨架并同步
各包配置、应用数据库迁移，最后验证 core 可导入。未指定适配器时默认安装 `telegram`。

- `--minimal`：只装裸 core，跳过 `full` extra 的品牌、表情、MySQL、S3 与图像依赖。
- `--no-venv`：不创建实例 venv，改用当前环境或系统 Python；可用 `AKARIBOT_PYTHON` 指定解释器。
- `--workspace-root` / `--dev` 从本地源码安装；`--non-interactive` 不提问。

实例根下，`akaribot.toml` 记录名称、语言、venv 与来源；`config/` 放扁平配置表；`data/` 放模块数据
与私有资产；`database/` 放默认 SQLite 数据库；`logs/` 与 `cache/` 放日志和可丢弃的缓存；
`assets/private/` 放实例私有资源；`.bot.lock` 记录运行锁与持锁进程。

## 配置

核心配置在 `config/config.toml`：`[config]` 是公开项，`[secret]` 是密钥项，顶层另有
`default_locale` 与 `config_version`。适配器配置为 `config/bot_<平台>.toml`，公开项与 `_secret`
密钥项同文件。

```sh
akaribot config schema --table bot_telegram
akaribot config set telegram_token <令牌> --table bot_telegram
akaribot config set enable true --table bot_telegram
```

`config set` 按模板声明的类型转换取值；字段在模板中标记为密钥时写入同文件的 `_secret` 表，无需
手工指定表名。`config placeholders` 统计待填写的占位符，`config open --table <表>` 用
`VISUAL` / `EDITOR` 打开配置文件。

`base_superuser` 位于 `[config]`，取值为发送者 ID 列表（如 `QQ|2596322644`、
`Telegram|User|<用户 ID>`），启动时逐项写入数据库并授予超级管理员。默认值包含上游维护者的账号，
自建实例应改为自己的账号或清空。

## 运行

```sh
akaribot run                 # 前台运行
akaribot run -d              # 后台运行，日志写入 logs/RunConsole_<日期>.log
akaribot run --status        # 也可用 --stop 或 --restart
```

`-a` / `--adapter` 只启动指定适配器。后台启动在实例取得 `.bot.lock` 后才报告成功；停止默认等待
20 秒，可用 `--timeout` 调整。`--no-auto-migrate` 跳过启动时的数据库结构升级。

## 常驻服务

`init` 会把实例登记到本机注册表 `~/.akaribot/instances.toml`（`AKARIBOT_HOME` 可改位置）。服务
由 CLI 守护，按注册表中的策略恢复实例：

```sh
akaribot instance policy <实例名> --autostart --restart-on-crash
akaribot service install
```

`service install` 在 macOS 写入 launchd 单元，在 Linux 写入 systemd 用户单元；Windows 没有受支持
的后端。`service supervise` 是单元实际执行的循环，默认每 5 秒检查一次，单个实例最多连续重启 5 次，
退避基数 2 秒。`service uninstall` 注销并删除单元文件。

## venv 管理

默认由 CLI 托管实例的 `.venv`。`venv status` 显示模式与已装包；`venv recreate` 在新环境安装并验证
通过后才替换旧目录，适用于升级 Python 之后；`venv adopt` 接管当前环境，`venv release` 把包迁回
当前环境；`venv add <需求串>` 装入额外的运行库，`--save` 会记入 `akaribot.toml` 供重建时补装。

## 检查与日志

```sh
akaribot doctor
akaribot doctor --strict
akaribot logs --follow
```

`doctor` 只做多实例三查：端口冲突、同一平台凭据重复、适配器未安装导致的孤立配置。`--strict` 把
告警也按失败处理，`--json` 供脚本消费；其余环境诊断不在该命令范围内。`logs` 另有 `--debug`、
`--info`、`--lines` 与 `--path`。

## 更新与备份

```sh
akaribot module update --all
akaribot db tables
```

`module update` 更新实例内已安装的模块与适配器，并尝试通知运行中的实例热装载。数据库结构升级在
实例启动的 pre-init 阶段执行；`akaribot db` 用于浏览表与按主键写入，不代替升级。备份时先执行
`akaribot run --stop`，再复制 `config/`、`data/`、`database/` 与 `assets/private/`；`cache/`、
`logs/` 与 `.bot.lock` 无需备份。

## Docker

仓库根的 `Dockerfile` 构建源码工作区镜像：`uv sync --frozen --no-dev --all-extras` 安装全部成员，
容器以 `python -m akaribot.core.entrypoints.run` 启动，`AKARI_INSTANCE_DIR` 固定为 `/akari-bot`；
构建命令为 `docker build -t akari-bot .`。配置、数据库、日志与私有资产都写在 `/akari-bot` 下；
需要跨容器保留时，分别挂载 `config/`、`data/`、`database/`、`logs/` 与 `assets/private/`。镜像以
core 的 `run` 入口直接启动，运行参数直接传给该入口。
