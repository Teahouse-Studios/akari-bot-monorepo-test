# 命令参考

本文整理了各子命令的用途与选项。

全局选项写在子命令前。例如：

```sh
akaribot --lang en_us init ./bot
akaribot --version
```

`--lang zh_cn|en_us` 只影响本次调用的界面文案，不改变实例默认语言。把它写在子命令后会被当成未知选项。

需要实例的命令接受 `--instance` / `-I`。查找顺序是：显式路径、`AKARI_INSTANCE_DIR`、从当前目录向上找 `akaribot.toml`。找不到实例时命令报错，并提示先初始化或指定实例根。

`--json` 让脚本读取结果。多数命令输出一行 JSON。`docs dev`、`docs serve` 这类长期运行的命令输出事件行。stdout 只放结果或事件，进度与警告走 stderr。

会删除内容的写操作还接受 `--yes` / `-y`，用来跳过确认。只打印操作计划的命令使用 `--dry-run`，不会写文件，也不会调用安装器。

## init

创建实例目录、写入 `akaribot.toml`、安装 core 与适配器，并生成最小配置。

```sh
akaribot init ./bot --locale zh_cn --adapter telegram --adapter discord
```

- `path`：实例目录，默认为当前目录。`--adapter` / `--module` 可重复，默认适配器为 `telegram`。
- `--minimal`：不装 core extras 与表情资源包。`--extra` 追加 extra，两者互斥。
- `--no-venv`：不由 CLI 管理 venv。`--workspace-root` / `--dev`：从本地源码安装。`--python`：创建 venv 时使用的解释器。
- `--skip-config-sync`：跳过安装后的配置同步。core 的配置模块还没就绪时使用。
- `--non-interactive` 不提问。还支持 `--offline`、`--dry-run`、`--force`、`--verbose` / `-v`。

## run

启动、停止、重启或查看实例状态。未知参数原样传给 core 的 `run` 命令。

- `-a` / `--adapter`：只启动指定适配器，可重复。
- 默认在前台运行。`-d` / `--detach` 后台启动，等实例取得 `.bot.lock` 后才报告成功。
- `--stop`、`--restart`、`--status` 互斥。`--restart` 等价于停止后后台启动，`--timeout` 为停止时等待退出的秒数，默认 20。
- `--no-auto-migrate`：启动时跳过数据库结构升级。`--foreground` 显式保持前台，与 `--detach` 互斥。
- 后台控制台输出写入 `logs/RunConsole_<日期>.log`，进程号记在 `.bot.lock`。`--status --json` 输出运行状态、锁文件和控制台日志路径。

## service

把 CLI 装成系统常驻服务，由服务按注册表里的自启与崩溃重启设置守护实例。

- `install [--dry-run] [--force]`：写入并注册服务单元。macOS 写 launchd 单元，Linux 写 systemd 用户单元。Windows 没有受支持的后端。
- `uninstall`：注销服务并删除单元文件。
- `status [--json]`：查看是否安装、是否已注册。
- `supervise [--once] [--interval 5] [--max-restarts 5] [--backoff 2]`：守护循环本身，由服务单元调用。默认每 5 秒检查一次，单个实例最多连续重启 5 次，重启间隔从 2 秒起逐次翻倍。`--once` 只跑一轮。

服务恢复实例时同时检查注册表里的自启策略和上次运行状态。只开崩溃重启、没开自启的实例不会在开机时被拉起。

## test

在实例环境里运行 `akaribot.testing`，缺测试包时提示安装 `akari-bot-testing`。

- `path`：测试文件或目录，省略时跑全部默认根目录。
- `--ci`：非交互模式，跳过需要人工复核的用例，同时设置 `CI=1`。CI 里不会停在 `input()` 等待输入。
- `--coverage`：收集覆盖率。`--case`：只跑名字含该子串的用例，可重复。
- 测试框架不在实例默认依赖中，需要先安装 `akari-bot-testing`。缺包时命令会给出安装提示。

测试由 `tester.py` 启动，和实例里的模块共用配置与临时数据目录。跑单个文件时传包内路径，例如 `packages/akari-bot-core/tests/test_registry.py`。

## module

模块与适配器的安装、卸载、更新与全局加载。

启用分三级，含义各不相同：

- 安装控制代码是否装进本实例。
- 加载控制它是否参与命令匹配。
- 场景启用控制某个群或频道能否使用，需要在机器人里执行 `~module enable`。

- `list`：列出已安装的模块与适配器。`available [--kind module|adapter]`：列出 registry 里可安装的包，并标出已安装项。`status`：列出各模块的全局加载状态。
- `add <名> [-e <目录>] [--git <地址>] [--ref <引用>] [--subdir <目录>] [--dist <分发>]`：安装模块、适配器或本地源码包。
  - 还支持 `--version`、`--extra`、`--kind`、`--force`、`--offline`、`--dry-run`、`--verbose`。
  - 安装过程是：解析包 → 安装前检查 → 安装 → 补配置 → 迁移 → 热加载 → 报告。`-e` 用可编辑模式安装本地目录，可以省略包名。
  - 安装前检查用 `uv pip install --dry-run` 生成安装计划，再检查它是否会破坏已安装的包。只调整依赖版本时给出提示并继续。会破坏已装包或解不出依赖时停止。`--force` 跳过这项检查。
- `remove <名> [--cascade] [--force] [--purge-data] [--yes]`：默认保留配置与数据。`--cascade` 连带卸载依赖它的包，先列清单再确认。`--purge-data` 同时删除该包的数据表与配置文件。
- `update [名…] [--all] [--force] [--offline] [--defer-runtime] [--json]`：更新已装包。工作区模式下等价于按本地源码重装。`--defer-runtime` 把数据库迁移留到下次启动。
- `load <名>` / `unload <名>`：只改全局加载状态，不改安装状态和场景启用状态。

`--json` 的 `update` 只在 stdout 输出一行结果，进度与警告走 stderr。字段包括 `updated`、`failed`、`skipped`、`reload_pending` 与 `restart_required`。

## config

读取、写入与编辑配置。写入由 core 以原子方式完成，值按模板声明的类型转换。

- `list [--json]`：列出已有配置表。`schema --table <表> [--json]`：字段类型、默认值、注释与是否占位。
- `placeholders [--json]`：统计各表待填的占位符。它只做统计，不阻止启动。
- `get <键> --table <表>`、`set <键> <值> --table <表>`：单项读写。`set` 按模板类型转换布尔、数字与列表，密钥字段自动写入 `_secret` 表。
- `open [--table <表>]`：用 `VISUAL` / `EDITOR` 打开配置文件。`edit`：提示三种编辑方式（表单、原始文本、外部编辑器）。
- 表名以 `list` / `schema` 的输出为准。实例表可能带 `-<实例 ID>` 后缀，基表名不能直接当作实例表名使用。

## db

浏览实例数据库并按主键写入。表名取自 `db tables` 的 `table` 列。

- `tables [--json]`：列出数据表。
- `rows <表> [--limit 20] [--offset 0] [-f <条件>] [-q <搜索>][--order-by <列[:asc|desc]>] [--no-count]`：分页读取。每页最多 200 条。筛选可以重复，多个条件之间是 AND 关系。`-q` 在所有文本列上做包含匹配，不区分大小写。
- `-f` 的条件形如 `<列><运算符><值>`，支持 `=`、`!=`、`>`、`>=`、`<`、`<=`、`~`（包含）、`!~`（不包含）、`^`（前缀）、`$`（后缀）。`null` 表示空值。
- `--no-count` 不统计总条数，翻页时省掉全表扫描。输出里不带总数。
- `set <表> --key <主键> --set <列>=<值>…`：在一次 UPDATE 中写入多列。
- `insert <表> --set <列>=<值>…`、`delete <表> --key <主键> [--yes]`。

## instance

管理本机注册表，不移动实例目录。

- 注册表默认在 `~/.akaribot/instances.toml`，可用 `AKARIBOT_HOME` 改目录。
- `list [--json]`：列出本机实例、运行状态与服务设置。
- `add <目录> [--name <名>] [--locale <语言>]`：只记录位置，不创建实例、不装包。
- `remove <名> [--yes]`：从注册表移除条目，实例目录保留。
- `use <名>`：设为默认实例。站在实例目录之外运行界面或命令时，按它选择实例。
- `policy <名> [--autostart|--no-autostart] [--restart-on-crash|--no-restart-on-crash]`：设置服务策略。

## adapter

查看、添加和删除适配器实例。

- `list [--json]`：按平台分组列出适配器实例。JSON 里的 `installed_platforms` 还会列出 core 清单中全部已安装的平台，包括还没有实例配置的平台。
- `instance add <平台> [实例 ID]`：生成 `config/bot_<平台>[-<实例 ID>].toml`，`enable` 显式写 `false`，填完平台要求的账号信息后再开启。
- `instance remove <平台> [实例 ID] [--dry-run]`：只删配置文件，场景与用户数据保留。

实例 ID 只能使用小写字母、数字和下划线，长度为 1–24 个字符。省略表示默认实例。它是 `target_id` 前缀的一部分，一旦使用不可更改。命令不提供改名。改名要迁移多张表和消息前缀。

## venv

管理实例 venv：改为由 CLI 管理、改回你自己管理，或重建。

- `status`：查看当前模式、解释器路径与已装包数量。
- `add <需求串> [--no-save] [--upgrade]`：装入实例环境，默认记进实例清单。`--no-save` 只装不记录，重建时不会自动补装。
- `remove <分发名> [--no-save]`：卸载，默认同时删掉实例清单里的记录。`--no-save` 保留记录。
- `adopt`：改为由 CLI 管理 venv，把当前环境里的包迁进实例 venv。`release`：改回由你自己管理，把实例 venv 里的包迁到当前环境。
- `recreate`：重建实例 venv，用于升级 Python 或修复环境。新环境安装并验证通过后才替换旧目录。

## doctor

检查多个实例之间的端口冲突、重复的登录信息，以及没有对应适配器的配置。`--json` 供 CI 读取，`--strict` 把告警按失败处理。这个命令只覆盖这三项。网络、依赖版本和文档工具链分别由运行、安装和文档命令检查。

## new

- `new module <名>`：生成模块包，支持 `--dir`、`--alias`、`--desc`、`--author`、`--license`、`--platform`、`--component`、`--command`、`--config`、`--database`、`--assets`、`--data-dir`、`--tests`、`--non-interactive`、`--add`、`--force`。
- `new adapter <名>`：生成适配器包，支持 `--platform-name`、`--feature`、`--field`、`--credential-field` 等同类选项。生成后默认执行 `akaribot module add -e .`。
- 生成目录下的包名带 `akari-bot-module-` / `akari-bot-adapter-` 前缀。`--add` 默认开启。只想生成文件时传 `--no-add`。

## docs

收集实例中已安装包的 `docs/`，生成并构建 VitePress 站点。站点配置写在实例根的 `docs.toml`。Node.js 与 VitePress 版本由主题清单声明。

- `list [--query <词>] [--kind <分组>] [--json]`：列出参与构建的包、分类、页面与目录警告。
- `build [--package <key>…] [--all] [--force] [--offline] [--json]`：生成站点并调用 VitePress。不加 `--json` 时，命令实时打印各阶段进度与子进程输出。加 `--json` 时，stdout 只保留结果行，日志写入 stderr。`--package` 可重复或逗号分隔。
- `sync-theme [--repo <路径>] [--json]`：把主题模板 submodule 同步到远端最新提交。只更新工作区，不暂存父仓库 gitlink。
- `install-deps [--json]`：安装主题所需的 Node 依赖，不生成站点。
- `serve [--host 127.0.0.1] [--port 4173] [--open] [--no-build] [--json]`：构建并启动本机静态预览，直到 Ctrl+C。`--json` 先输出 ready 事件行。
- `dev [--host 127.0.0.1] [--port 5173] [--open] [--offline] [--interval 0.6] [--package <key>…] [--json]`：监听文档与主题改动，同步到 `cache/docs/dev` 并运行 VitePress 开发服务器，直到 Ctrl+C。`--json` 输出逐行事件。
- `deploy [--provider vercel|s3] [--dry-run] [--delete] [--yes] [--json]`：把构建产物部署到远端。部署用的密钥只从环境变量读取，`--delete` 只在 S3 下删除目标前缀内多余的对象。
- `status [--json]`：查看工具链、配置、包数与最近一次构建或部署。`clean [--yes]`：删除 `cache/docs`。

生成结果位于实例根目录的 `cache/docs`，开发模式使用其中的 `cache/docs/dev`，构建与部署记录在 `.docs/state.json`。主题由 `docs.toml` 的 `[theme].source` 选择，外部模板需在根目录提供 `docs-theme.json`。配置与部署字段见 [文档引擎](docs-engine.md)。

## tui

启动终端界面。`--self-check` 在无终端环境下检查资源、样式与页面交互，`--headless` 启动后完成基础读取即退出，`--no-mouse` 关闭鼠标追踪。页面与键位见 [终端界面](tui.md)。

## logs

读取实例 `logs/` 下最新的日志文件。

- 日志文件在实例 `logs/` 下，文件名形如 `<进程>[_debug]_<日期>.log`。
- `--process <进程>`：限定进程前缀。`--info` / `--debug`：限定日志级别文件。
- `--lines <N>`：首次输出的末尾行数，默认 50。`--follow`：持续输出新增行，直到 Ctrl+C。
- `--path`：只打印文件路径，便于脚本自行处理。`--json`：输出单行 JSON。

## migrate

```sh
akaribot migrate legacy <旧项目> -I <新实例目录> --dry-run
```

旧项目须含 `bot.py`、`core/`、`modules/` 与 `config/config.toml`。迁移只读取旧目录，不改动它，可以重复执行。报告写到新实例根的 `migration-report.md`。选项：`--workspace-root` / `--dev`、`--skip-install`、`--no-venv`、`--dry-run`、`--force`、`--offline`、`-v`。

## 常见操作组合

### 创建并启动实例

```sh
akaribot init /srv/akaribot --adapter telegram --adapter web --locale zh_cn
akaribot run --status -I /srv/akaribot
akaribot run -d -I /srv/akaribot
```

`init` 结束时会把实例写入注册表。之后站在实例目录外，也可以直接用注册名或 `-I` 指定实例。

### 安装模块

```sh
akaribot module available --kind module -I /srv/akaribot
akaribot module add dice -I /srv/akaribot
akaribot module load dice -I /srv/akaribot
```

`add` 只负责装进实例。`load` 让它参与命令匹配。要让某个群或频道使用，还要在机器人里执行 `~module enable dice`。

### 配置与检查

```sh
akaribot config placeholders -I /srv/akaribot
akaribot config schema --table bot_telegram -I /srv/akaribot
akaribot config set enable true --table bot_telegram -I /srv/akaribot
akaribot doctor --strict
```

`config set` 写入后是否立即生效取决于 core。需要重启的项会在命令输出里说明。`doctor` 只看端口、重复登录信息和孤立配置，不替代完整运行检查。

### 文档站点

```sh
akaribot docs list -I /srv/akaribot
akaribot docs build --force -I /srv/akaribot
akaribot docs serve -I /srv/akaribot
```

`serve` 会先构建再启动本机预览。只改文档时用 `docs dev`，它监听文件变化并在另一个端口启动开发服务器。

## 环境变量

| 变量 | 作用 |
| --- | --- |
| `AKARI_INSTANCE_DIR` | 未传 `--instance` 时使用的实例根。显式参数优先。 |
| `AKARIBOT_HOME` | 实例注册表所在目录，默认 `~/.akaribot`。 |
| `AKARIBOT_PYTHON` | 非托管模式下启动实例子进程使用的解释器。 |
| `AKARIBOT_CLI_BIN` | 终端界面调用 CLI 时使用的命令。冻结产物可据此指向二进制。 |
| `VISUAL` / `EDITOR` | `config open` 调用的外部编辑器，按这个顺序选择。 |

`AKARI_CONFIG_PATH` 由 CLI 在启动 core 子进程时注入，一般不需要手动设置。
