# 命令参考

全局选项置于子命令之前。例如：

```sh
akaribot --lang en_us init ./bot
akaribot --version
```

``--lang zh_cn|en_us`` 仅影响本次调用的界面文案，不改变实例默认语言。若置于子命令之后，会被视为未知选项。

需要实例的命令接受 `--instance` / `-I` 参数。定位顺序依次为显式路径、`AKARI_INSTANCE_DIR` 与向上逐级查找 `akaribot.toml`。未找到实例时命令输出错误提示，并引导先执行初始化或明确指定实例根目录。

``--json`` 供脚本读取结果，多数命令输出单行 JSON。`docs dev`、`docs serve` 这类长期运行的命令输出事件行。stdout 仅输出结果或事件，进度与警告一律输出至 stderr。

会删除内容的写入操作支持传入 `--yes` / `-y` 用于跳过交互确认。仅输出操作计划的命令使用 `--dry-run`，不会写入文件，亦不调用安装器。

## init

创建实例目录、写入 `akaribot.toml`、安装 core 与适配器，并生成最小配置。

```sh
akaribot init ./bot --locale zh_cn --adapter telegram --adapter discord
```

- `path`：实例目录，默认为当前目录。`--adapter` / `--module` 可多次指定，默认适配器为 `telegram`。
- `--minimal`：不安装 core extras 与表情资源包。`--extra` 追加 extra，两者互斥。
- `--no-venv`：不由 CLI 管理 venv。`--workspace-root` / `--dev`：从本地源码安装。`--python`：创建 venv 时使用的解释器。
- `--skip-config-sync`：跳过安装后的配置同步。core 的配置模块尚未就绪时使用。
- `--non-interactive`：跳过交互式提问。还支持 `--offline`、`--dry-run`、`--force`、`--verbose` / `-v`。

## run

启动、停止、重启或查看实例状态。未知参数原样传递给 core 的 `run` 命令。

- `-a` / `--adapter`：仅启动指定适配器，可多次指定。
- 默认在前台运行。`-d` / `--detach` 在后台启动，等待实例获取 `.bot.lock` 后才判定为启动成功并报告。
- `--stop`、`--restart`、`--status` 互斥。`--restart` 等价于停止后在后台启动，`--timeout` 为停止时等待退出的秒数，默认值为 20。
- `--no-auto-migrate`：启动时跳过数据库结构升级。`--foreground` 显式保持前台，与 `--detach` 互斥。
- 后台控制台输出写入 `logs/RunConsole_<日期>.log`，进程号记录在 `.bot.lock` 中。`--status --json` 输出运行状态、锁文件和控制台日志路径。

## service

将 CLI 安装为系统常驻服务，由服务根据注册表中的自启与崩溃重启设置守护实例。

- `install [--dry-run] [--force]`：写入并注册服务单元。macOS 写入 launchd 单元，Linux 写入 systemd 用户单元。Windows 没有受支持的后端。
- `uninstall`：注销服务并删除单元文件。
- `status [--json]`：查看是否安装、是否已注册。
- `supervise [--once] [--interval 5] [--max-restarts 5] [--backoff 2]`：守护循环本身，由服务单元调用。默认每 5 秒检查一次，单个实例最多连续重启 5 次，重启间隔从 2 秒起逐次翻倍。`--once` 仅运行一轮。

服务恢复实例时同时检查注册表中的自启策略和上次运行状态。仅开启崩溃重启、未开启自启的实例不会在开机时被自动启动。

## test

在实例环境中运行 `akaribot.testing`，缺少测试包时提示安装 `akari-bot-testing`。

- `path`：测试文件或目录，省略时运行全部默认根目录。
- `--ci`：非交互模式，跳过需要人工复核的用例，同时设置 `CI=1`。CI 环境中不会停在 `input()` 等待输入。
- `--coverage`：收集覆盖率。`--case`：仅运行名称包含该子串的用例，可多次指定。
- 测试框架不在实例默认依赖中，需要先安装 `akari-bot-testing`。缺少该包时命令会给出明确安装提示。

测试由 `tester.py` 启动，与实例中的模块共用配置与临时数据目录。运行单个文件时传入包内路径，例如 `packages/akari-bot-core/tests/test_registry.py`。

## module

模块与适配器的安装、卸载、更新与全局加载。

启用状态分为三个层级，各自具有独立的控制范围：

- 安装控制代码是否安装至本实例。
- 加载控制模块是否参与命令匹配。
- 场景启用控制特定群聊或频道能否使用，需要在机器人会话中执行 `~module enable`。

- `list [--kind <分组>] [--json]`：列出已安装的模块与适配器。
- `available [--kind <分组>] [--search <词>] [--refresh] [--offline] [--json]`：列出可安装的模块与适配器，并标出已装项。
- `add <包名或路径>… [--save] [--no-load]`：安装模块或适配器。`--save` 写入实例清单，环境重建时自动补充安装。`--no-load` 安装后不写入加载列表。
- `remove <名>… [--save] [--purge] [--yes]`：卸载。`--save` 同时从实例清单删除。`--purge` 一并清理该模块的配置与数据，执行前弹出模态确认框或要求传入 `--yes`。
- `update [名…] [--dry-run]`：更新已安装的包。省略名称时更新全部已安装包。
- `status [--json]`：列出各模块的全局加载状态。
- `load <名>…`：开启全局加载。
- `unload <名>…`：关闭全局加载，配置保留。

`--json` 的 `update` 仅在 stdout 输出单行结果，进度与警告输出至 stderr。字段包括 `updated`、`failed`、`skipped`、`reload_pending` 与 `restart_required`。

## config

- `list [--json]`：列出已有配置表。`schema --table <表> [--json]`：字段类型、默认值、注释与是否占位。
- `placeholders [--json]`：统计各表待填的占位符。其仅负责统计，不阻止启动。
- `get <键> --table <表>`、`set <键> <值> --table <表>`：单项读写。`set` 按模板类型转换布尔、数字与列表，密钥字段自动写入 `_secret` 表。
- `open [--table <表>]`：使用 `VISUAL` / `EDITOR` 打开配置文件。`edit`：提示三种编辑方式（表单、原始文本、外部编辑器）。
- 表名以 `list` / `schema` 的输出为准。实例表可能带 `-<实例 ID>` 后缀，基础表名不能直接当作实例表名使用。

## db

- `tables [--json]`：列出数据表。
- `rows <表> [--limit 20] [--offset 0] [-f <条件>] [-q <搜索>][--order-by <列[:asc|desc]>] [--no-count]`：分页读取。每页最多 200 条。筛选可以重复，多个条件之间是 AND 关系。`-q` 在所有文本列中按包含方式匹配，不区分大小写。
- `-f` 的条件形如 `<列><运算符><值>`，支持 `=`、`!=`、`>`、`>=`、`<`、`<=`、`~`（包含）、`!~`（不包含）、`^`（前缀）、`$`（后缀）。`null` 表示空值。
- `--no-count` 不统计总条数，翻页时避免全表扫描。输出里不带总数。
- `set <表> --key <主键> --set <列>=<值>…`：在一次 UPDATE 中写入多列。
- `insert <表> --set <列>=<值>…`、`delete <表> --key <主键> [--yes]`。

## instance

- 注册表默认在 `~/.akaribot/instances.toml`，可用 `AKARIBOT_HOME` 修改目录。
- `list [--json]`：列出本机实例、运行状态与服务设置。
- `add <目录> [--name <名>] [--locale <语言>]`：仅记录位置，不创建实例、不安装包。
- `remove <名> [--yes]`：从注册表移除条目，实例目录保留。
- `use <名>`：设为默认实例。在实例目录之外运行界面或命令时，依此选择目标实例。
- `policy <名> [--autostart|--no-autostart] [--restart-on-crash|--no-restart-on-crash]`：设置服务策略。

## adapter

- `list [--json]`：按平台分组列出适配器实例。JSON 中的 `installed_platforms` 亦会列出 core 清单中全部已安装的平台，包含尚未配置实例的平台。
- `instance add <平台> [实例 ID]`：生成 `config/bot_<平台>[-<实例 ID>].toml`，`enable` 明确设为 `false`，填写完平台要求的账号信息后再开启。
- `instance remove <平台> [实例 ID] [--dry-run]`：仅删除配置文件，保留场景与用户数据。

实例 ID 仅可使用小写字母、数字和下划线，长度为 1–24 个字符。省略表示默认实例。它是 `target_id` 前缀的一部分，一旦使用不可更改。命令不提供重命名功能，因为修改名称需要迁移多张表和消息前缀。

## venv

管理实例 venv，支持切换为 CLI 托管、恢复为自行管理或重新构建。

- `status [--json]`：查看解释器路径、托管模式、已安装包与清单中记录的运行库。
- `add <spec>… [--save]`：安装运行库。`--save` 写入实例清单。
- `remove <包名>… [--save]`：卸载运行库。`--save` 从清单中移除。
- `adopt [--python <路径>] [--yes]`：切换为 CLI 托管 venv。会先复制现有环境的包并安装缺失项，验证通过后才移除旧环境中的包。
- `release [--yes]`：放弃托管，将实例 venv 中的包迁移到目标环境。
- `recreate [--python <路径>] [--yes]`：根据实例清单重建 venv。Python 次版本升级后用于修复损坏的环境。

## doctor

检查多个实例之间的端口冲突、重复登录信息，以及缺少对应适配器的配置。`--json` 供 CI 读取，`--strict` 将告警判定为失败。该命令仅覆盖上述三项检查。网络、依赖版本和文档工具链分别由运行、安装和文档命令检查。

## new

- `module|adapter <名> [--dest <目录>] [--no-add]`：生成包模板结构并创建 git 仓库。默认直接安装至当前实例并开启全局加载与开机自启。仅需生成文件时传入 `--no-add`。

## docs

收集实例中已安装包的 `docs/`，生成并构建 VitePress 站点。站点配置保存在实例根目录的 `docs.toml` 中。Node.js 与 VitePress 版本由主题清单声明。

- `list [--query <词>] [--kind <分组>] [--json]`：列出参与构建的包、分类、页面与目录警告。
- `build [--package <key>…] [--all] [--force] [--offline] [--json]`：生成站点并调用 VitePress。不加 `--json` 时，命令实时打印各阶段进度与子进程输出。加 `--json` 时，stdout 仅保留结果行，日志写入 stderr。`--package` 可重复或逗号分隔。
- `sync-theme [--repo <路径>] [--json]`：将主题模板 submodule 同步至远端最新提交。仅更新工作区，不暂存父仓库 gitlink。
- `install-deps [--json]`：安装主题所需的 Node 依赖，不生成站点。
- `serve [--host 127.0.0.1] [--port 4173] [--open] [--no-build] [--json]`：构建并启动本机静态预览，直到 Ctrl+C。`--json` 先输出 ready 事件行。
- `dev [--host 127.0.0.1] [--port 5173] [--open] [--offline] [--interval 0.6] [--package <key>…] [--json]`：监听文档与主题改动，同步至 `cache/docs/dev` 并运行 VitePress 开发服务器，直到 Ctrl+C。`--json` 输出逐行事件。
- `deploy [--provider vercel|s3] [--dry-run] [--delete] [--yes] [--json]`：将构建产物部署至远端。部署使用的密钥仅从环境变量读取，`--delete` 仅在 S3 下删除目标前缀内多余的对象。
- `status [--json]`：查看工具链、配置、包数与最近一次构建或部署。`clean [--yes]`：删除 `cache/docs`。

生成结果位于实例根目录的 `cache/docs`，开发模式使用其中的 `cache/docs/dev`，构建与部署记录在 `.docs/state.json`。主题由 `docs.toml` 的 `[theme].source` 选择，外部模板需要在根目录提供 `docs-theme.json`。配置与部署字段参见 [文档引擎](docs-engine.md)。

## tui

启动终端界面。`--self-check` 在无终端环境下检查资源、样式与页面交互，`--headless` 启动后完成基础读取即退出，`--no-mouse` 关闭鼠标追踪。页面与键位参见 [终端界面](tui.md)。

## logs

读取实例 `logs/` 目录下最新的日志文件。

- 日志文件在实例 `logs/` 下，文件名形如 `<进程>[_debug]_<日期>.log`。
- `--process <进程>`：限定进程前缀。`--info` / `--debug`：限定日志级别文件。
- `--lines <N>`：首次输出的末尾行数，默认 50。`--follow`：持续输出新增行，直到 Ctrl+C。
- `--path`：仅输出文件路径，便于脚本自行处理。`--json`：输出单行 JSON。

## migrate

```sh
akaribot migrate legacy <旧项目> -I <新实例目录> --dry-run
```

旧项目必须包含 `bot.py`、`core/`、`modules/` 与 `config/config.toml`。迁移仅读取旧目录，不修改原有内容，可重复执行。报告写入新实例根目录的 `migration-report.md`。选项：`--workspace-root` / `--dev`、`--skip-install`、`--no-venv`、`--dry-run`、`--force`、`--offline`、`-v`。

## 常见操作组合

### 创建并启动实例

```sh
akaribot init /srv/akaribot --adapter telegram --adapter web --locale zh_cn
akaribot run --status -I /srv/akaribot
akaribot run -d -I /srv/akaribot
```

`init` 执行完成时会将实例写入注册表。之后在实例目录之外，亦可直接使用注册名称或 `-I` 指定实例。

### 安装模块

```sh
akaribot module available --kind module -I /srv/akaribot
akaribot module add dice -I /srv/akaribot
akaribot module load dice -I /srv/akaribot
```

`add` 仅负责安装至实例。`load` 使其参与命令匹配。若需要特定群聊或频道使用，还需要在机器人中执行 `~module enable dice`。

### 配置与检查

```sh
akaribot config placeholders -I /srv/akaribot
akaribot config schema --table bot_telegram -I /srv/akaribot
akaribot config set enable true --table bot_telegram -I /srv/akaribot
akaribot doctor --strict
```

`config set` 写入后是否立即生效取决于 core。需要重启的项会在命令输出中说明。`doctor` 仅检查端口、重复登录信息和孤立配置，不替代完整运行检查。

### 文档站点

```sh
akaribot docs list -I /srv/akaribot
akaribot docs build --force -I /srv/akaribot
akaribot docs serve -I /srv/akaribot
```

`serve` 会先构建再启动本机预览。仅修改文档时可使用 `docs dev`，其监听文件变化并在另一个端口启动开发服务器。

## 环境变量

| 变量 | 作用 |
| --- | --- |
| `AKARI_INSTANCE_DIR` | 未传入 `--instance` 时使用的实例根目录。显式参数优先。 |
| `AKARIBOT_HOME` | 实例注册表所在目录，默认 `~/.akaribot`。 |
| `AKARIBOT_PYTHON` | 非托管模式下启动实例子进程使用的解释器。 |
| `AKARIBOT_CLI_BIN` | 终端界面调用 CLI 时使用的命令。打包产物可据此指向二进制文件。 |
| `VISUAL` / `EDITOR` | `config open` 调用的外部编辑器，按此顺序依序选择。 |

`AKARI_CONFIG_PATH` 由 CLI 在启动 core 子进程时注入，一般不需要手动设置。
