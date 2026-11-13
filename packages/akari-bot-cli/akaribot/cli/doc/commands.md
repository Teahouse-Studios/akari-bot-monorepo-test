# 命令参考

本文整理了各子命令的用途与选项。

所有子命令接受全局选项 `--lang zh_cn|en_us`。需要实例的命令还接受 `--instance` / `-I`。

`--json` 表示以单行 JSON 输出，供脚本或界面读取。会删除内容的写操作还接受 `--yes` / `-y`，用来跳过确认。

## init

创建实例目录、写入 `akaribot.toml`、安装 core 与适配器，并生成最小配置。

```sh
akaribot init ./bot --locale zh_cn --adapter telegram --adapter discord
```

- `path`：实例目录，默认为当前目录。`--adapter` / `--module` 可重复，默认适配器为 `telegram`。
- `--minimal`：不装 core extras 与表情资源包。`--extra` 追加 extra，两者互斥。
- `--no-venv`：不托管 venv。`--workspace-root` / `--dev`：从本地源码安装。`--python`：创建 venv 时使用的解释器。
- `--non-interactive` 不提问。还支持 `--offline`、`--dry-run`、`--force`、`--verbose` / `-v`。

## run

启动、停止、重启或查看实例状态。未知参数原样传给 core 的 `run` 入口。

- `-a` / `--adapter`：只启动指定适配器，可重复。
- 默认在前台运行。`-d` / `--detach` 后台启动并立即返回。
- `--stop`、`--restart`、`--status` 互斥。`--restart` 等价于停止后后台启动，`--timeout` 为停止时等待退出的秒数，默认 20。
- 后台控制台输出写入 `logs/RunConsole_<日期>.log`，进程号记在 `.bot.lock`。

## service

把 CLI 装成系统常驻服务，由服务按注册表策略守护实例。

- `install [--dry-run] [--force]`：写入并注册服务单元。`uninstall`：注销并删除单元文件。
- `status [--json]`：查看是否安装、是否已注册。
- `supervise [--once] [--interval 5] [--max-restarts 5] [--backoff 2]`：守护循环本身，由服务单元调用。`--once` 只跑一轮。

## test

在实例环境里运行 `akaribot.testing`，缺测试包时提示安装 `akari-bot-testing`。

- `path`：测试文件或目录，省略时跑全部默认根目录。
- `--ci`：非交互模式，跳过需要人工复核的用例，同时设置 `CI=1`。
- `--coverage`：收集覆盖率。`--case`：只跑名字含该子串的用例，可重复。

## module

模块与适配器的安装、卸载、更新与全局装载。

“启用”分三级，含义各不相同：安装决定代码是否装进本实例，装载决定它是否参与命令匹配，场景启用则需要在机器人里执行 `~module enable`。

- `list`、`available [--kind module|adapter]`、`status`：查看清单与装载状态。
- `add <名> [-e <目录>] [--git <地址>] [--ref <引用>] [--subdir <目录>] [--dist <分发>]`：安装。
  - 还支持 `--version`、`--extra`、`--kind`、`--force`、`--offline`、`--dry-run`。
  - 安装前，命令先用 `uv pip install --dry-run` 生成安装计划，再检查它是否会破坏已安装的包。安装计划只调整依赖版本时，命令给出提示并继续安装。安装计划会破坏已安装的包，或解不出依赖方案时，命令停止安装。
  - `--force` 可以跳过这项检查。
- `remove <名> [--cascade] [--force] [--purge-data] [--yes]`：默认保留配置与数据。
- `update [名…] [--all] [--force] [--offline] [--defer-runtime] [--json]`：更新已装包。
- `load <名>` / `unload <名>`：只改全局装载状态，不改配置。

## config

读取、写入与编辑配置。写入由 core 以原子方式完成，值按模板声明的类型转换。

- `list [--json]`：列出已有配置表。`schema --table <表> [--json]`：字段类型、默认值、注释与是否占位。
- `placeholders [--json]`：统计各表待填的占位符。
- `get <键> --table <表>`、`set <键> <值> --table <表>`：单项读写。
- `open [--table <表>]`：用 `VISUAL` / `EDITOR` 打开配置文件。`edit`：提示三种编辑方式。

## db

浏览实例数据库并按主键写入。表名取自 `db tables` 的 `table` 列。

- `tables [--json]`：列出数据表。
- `rows <表> [--limit 20] [--offset 0] [-f <条件>] [-q <搜索>][--order-by <列[:asc|desc]>] [--no-count]`：分页读取。筛选条件可以重复，多个条件之间是 AND 关系。
- `set <表> --key <主键> --set <列>=<值>…`：在一次 UPDATE 中写入多列。
- `insert <表> --set <列>=<值>…`、`delete <表> --key <主键> [--yes]`。

## instance

管理本机注册表，不移动实例目录。

- `list [--json]`：列出本机实例、运行状态与服务策略。
- `add <目录> [--name <名>] [--locale <语言>]`：只记录位置。
- `remove <名> [--yes]`：从注册表移除条目，目录保留。
- `use <名>`：设为默认实例。
- `policy <名> [--autostart|--no-autostart] [--restart-on-crash|--no-restart-on-crash]`。

## adapter

查看、添加和删除适配器实例。

- `list [--json]`：按平台分组列出适配器实例。JSON 里的 `installed_platforms` 还会列出 core 清单中全部已安装的平台，包括还没有实例配置的平台。
- `instance add <平台> [实例 ID]`：生成实例配置，`enable` 显式写 `false`，填完平台要求的账号信息后再开启。
- `instance remove <平台> [实例 ID] [--dry-run]`：只删配置，场景与用户数据保留。

实例 ID 是 `target_id` 前缀的一部分，一旦使用不可更改。命令不提供改名。

## venv

管理实例 venv：接管、放弃托管或重建。

- `status`：查看当前模式、解释器路径与已装包数量。
- `add <需求串> [--no-save] [--upgrade]`：装入实例环境，默认记进实例清单。
- `remove <分发名> [--no-save]`：卸载，默认同时删掉实例清单里的记录。
- `adopt`：改为由 CLI 托管 venv，把当前环境里的包迁进实例 venv。`release`：取消托管，把实例 venv 里的包迁到当前环境。`recreate`：重建实例 venv。

## doctor

检查多个实例之间的端口冲突、重复的登录信息，以及没有对应适配器的配置。`--json` 供 CI 读取，`--strict` 把告警按失败处理。

## new

- `new module <名>`：生成模块包，支持 `--dir`、`--alias`、`--desc`、`--author`、`--license`、`--platform`、`--component`、`--command`、`--config`、`--database`、`--assets`、`--tests`、`--non-interactive`、`--add`、`--force`。
- `new adapter <名>`：生成适配器包，支持 `--platform-name`、`--feature`、`--field`、`--credential-field` 等同类选项。生成后默认执行 `akaribot module add -e .`。

## docs

汇总实例中已安装包的 `doc/`，生成并构建 VitePress 站点。站点配置写在实例根的 `docs.toml`。Node.js 与 VitePress 版本由主题清单决定，内置主题要求 Node >= 18，`akari-bot-docs-template` 要求 Node >= 22.12。

- `list [--query <词>] [--kind <分组>] [--json]`：列出参与构建的包、分类、页面与目录警告。
- `build [--package <key>…] [--all] [--force] [--offline] [--json]`：生成站点并调用 VitePress。不加 `--json` 时，命令实时打印各阶段进度与子进程输出。加 `--json` 时，stdout 只保留结果行，日志写入 stderr。`--package` 可重复或逗号分隔。
- `sync-theme [--repo <路径>] [--json]`：把主题模板 submodule 同步到远端最新提交。只更新工作区，不暂存父仓库 gitlink。
- `install-deps [--json]`：安装主题所需的 Node 依赖，不生成站点。
- `serve [--host 127.0.0.1] [--port 4173] [--open] [--no-build] [--json]`：构建并启动本机静态预览，直到 Ctrl+C。`--json` 先输出 ready 事件行。
- `deploy [--provider vercel|s3] [--dry-run] [--delete] [--yes] [--json]`：把构建产物部署到远端。部署用的密钥只从环境变量读取，`--delete` 只在 S3 下删除目标前缀内多余的对象。
- `status [--json]`：查看工具链、配置、包数与最近一次构建或部署。`clean [--yes]`：删除 `cache/docs`。

生成结果位于实例根目录的 `cache/docs`，构建与部署记录在 `.docs/state.json`。主题由 `docs.toml` 的 `[theme].source` 选择，外部模板需在根目录提供 `docs-theme.json`。配置与部署字段见 [文档引擎](docs-engine.md)。

## tui

启动终端界面。`--self-check` 在无终端环境下检查资源、样式与页面交互，`--headless` 启动后完成基础读取即退出，`--no-mouse` 关闭鼠标追踪。页面与键位见 [终端界面](tui.md)。

## logs

读取实例 `logs/` 下最新的日志文件。

- `--process <进程>`：限定进程前缀。`--info` / `--debug`：限定日志级别文件。
- `--lines <N>`：首次输出的末尾行数，默认 50。`--follow`：持续输出新增行，直到 Ctrl+C。
- `--path`：只打印文件路径。`--json`：结构化输出。

## migrate

```sh
akaribot migrate legacy <旧项目> -I <新实例目录> --dry-run
```

旧项目须含 `bot.py`、`core/`、`modules/` 与 `config/config.toml`。迁移只读取旧目录，不改动它，可以重复执行。报告写到新实例根的 `migration-report.md`。选项：`--workspace-root` / `--dev`、`--skip-install`、`--no-venv`、`--dry-run`、`--force`、`--offline`、`-v`。
