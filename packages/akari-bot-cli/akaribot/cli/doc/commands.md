# 命令参考

所有子命令接受全局选项 `--lang zh_cn|en_us`。需要实例的命令还接受 `--instance` / `-I`；`--json`
表示以单行 JSON 输出，供脚本或界面消费。会删除内容的写操作另有 `--yes` / `-y` 跳过确认。

## init
创建实例目录、写 `akaribot.toml`、安装 core 与适配器，并生成最小配置。

```sh
akaribot init ./bot --locale zh_cn --adapter telegram --adapter discord
```

- `path`：实例目录，缺省为当前目录；`--adapter` / `--module` 可重复，缺省适配器为 `telegram`。
- `--minimal`：不装 core extras 与表情资源包；`--extra` 追加 extra，两者互斥。
- `--no-venv`：不托管 venv；`--workspace-root` / `--dev`：从本地源码安装；`--python`：建 venv
  用的解释器。
- `--non-interactive` 不提问；另有 `--offline`、`--dry-run`、`--force`、`--verbose` / `-v`。

## run
启动、停止、重启或查看实例状态；未知参数原样透传给 core 的 `run` 入口。

- `-a` / `--adapter`：只启动指定适配器，可重复。
- 前台为默认行为；`-d` / `--detach` 后台启动并立即返回。
- `--stop`、`--restart`、`--status` 互斥，`--restart` 等价于停止后后台启动；`--timeout` 为停止
  时等待退出的秒数，默认 20。
- 后台控制台输出写入 `logs/RunConsole_<日期>.log`，进程号记在 `.bot.lock`。

## service
把 CLI 装成系统常驻服务，由服务按注册表策略守护实例。

- `install [--dry-run] [--force]`：写入并注册服务单元；`uninstall`：注销并删除单元文件。
- `status [--json]`：查看是否安装、是否已注册。
- `supervise [--once] [--interval 5] [--max-restarts 5] [--backoff 2]`：守护循环本体，由服务
  单元调用；`--once` 只跑一轮。

## test
在实例环境里运行 `akaribot.testing`，缺测试包时提示安装 `akari-bot-testing`。

- `path`：测试文件或目录，缺省跑全部默认根。
- `--ci`：非交互模式，跳过需要人工复核的用例，同时设置 `CI=1`。
- `--coverage`：收集覆盖率；`--case`：只跑名字含该子串的用例，可重复。

## module
模块与适配器的安装、卸载、更新与全局装载。三级「启用」互不相同：安装决定代码是否在本实例，
装载决定是否参与命令匹配，场景启用由机器人内的 `~module enable` 负责。

- `list`、`available [--kind module|adapter]`、`status`：查看清单与装载状态。
- `add <名> [-e <目录>] [--git <地址>] [--ref <引用>] [--subdir <目录>] [--dist <分发>]`：
  安装；另支持 `--version`、`--extra`、`--kind`、`--force`、`--offline`、`--dry-run`。
- `remove <名> [--cascade] [--force] [--purge-data] [--yes]`：默认保留配置与数据。
- `update [名…] [--all] [--force] [--offline] [--defer-runtime] [--json]`：更新已装包。
- `load <名>` / `unload <名>`：只改全局装载状态，不触碰配置。

## config
读取、写入与编辑配置；写入经 core 的原子路径，按模板声明的类型转换。

- `list [--json]`：已有配置表；`schema --table <表> [--json]`：字段类型、默认值、注释与占位。
- `placeholders [--json]`：各表待填占位符统计。
- `get <键> --table <表>`、`set <键> <值> --table <表>`：单项读写。
- `open [--table <表>]`：用 `VISUAL` / `EDITOR` 打开配置文件；`edit`：提示三种编辑方式。

## db
浏览实例数据库并按主键写入；表名取自 `db tables` 的 `table` 列。

- `tables [--json]`；`rows <表> [--limit 20] [--offset 0] [-f <条件>] [-q <搜索>]
  [--order-by <列[:asc|desc]>] [--no-count]`：分页读取，筛选可重复且多条之间为 AND。
- `set <表> --key <主键> --set <列>=<值>…`：同一次 UPDATE 写入多列。
- `insert <表> --set <列>=<值>…`；`delete <表> --key <主键> [--yes]`。

## instance
管理本机注册表，不移动实例目录。

- `list [--json]`：登记项、运行状态与服务策略。
- `add <目录> [--name <名>] [--locale <语言>]`：只登记位置；`remove <名> [--yes]`：删除登记，
  目录保留；`use <名>`：设为缺省实例。
- `policy <名> [--autostart|--no-autostart] [--restart-on-crash|--no-restart-on-crash]`。

## adapter
- `list [--json]`：按平台分组列出适配器实例。
- `instance add <平台> [实例 ID]`：生成实例配置，`enable` 显式写 `false`，填完凭据后开启。
- `instance remove <平台> [实例 ID] [--dry-run]`：只删配置，场景与用户数据保留。

实例 ID 是 `target_id` 前缀的一部分，一旦使用不可更改；命令不提供改名。

## venv
- `status`：当前模式、解释器路径与已装包数量。
- `add <需求串> [--no-save] [--upgrade]`：装入实例环境，缺省记进实例清单。
- `remove <分发名> [--no-save]`：卸载，缺省同时删除记录。
- `adopt` / `release`：接管或交还 venv；`recreate`：重建实例 venv。

## doctor
检查多实例的端口冲突、凭据重复与孤立配置。`--json` 供 CI 消费，`--strict` 把告警按失败处理。

## new
- `new module <名>`：生成模块包，支持 `--dir`、`--alias`、`--desc`、`--author`、`--license`、
  `--platform`、`--component`、`--command`、`--config`、`--database`、`--assets`、`--tests`、
  `--non-interactive`、`--add`、`--force`。
- `new adapter <名>`：生成适配器包，支持 `--platform-name`、`--feature`、`--field`、
  `--credential-field` 等同类选项。生成后默认执行 `akaribot module add -e .`。

## docs
汇总实例中已安装包的 `doc/`，生成并构建 VitePress 站点。构建需要 Node.js >= 18 与 npm，
站点配置写在实例根的 `docs.toml`。

- `list [--query <词>] [--kind <分组>] [--json]`：列出参与构建的包、页面与目录警告。
- `build [--package <key>…] [--all] [--force] [--offline] [--json]`：生成站点并调用 VitePress；
  `--package` 可重复或逗号分隔。
- `serve [--host 127.0.0.1] [--port 4173] [--open] [--no-build] [--json]`：构建并启动本机静态
  预览，直到 Ctrl+C；`--json` 先输出 ready 事件行。
- `deploy [--provider vercel|s3] [--dry-run] [--delete] [--yes] [--json]`：把构建产物部署到远端；
  凭据只从环境变量读取，`--delete` 只在 S3 下删除目标前缀内多余的对象。
- `status [--json]`：工具链、配置、包数与最近构建/部署；`clean [--yes]`：删除 `cache/docs`。

生成物位于实例根的 `cache/docs`，构建与部署记录在 `.docs/state.json`。配置与部署字段见
[文档引擎](docs-engine.md)。

## tui
启动终端界面。`--self-check` 在无终端环境下检查资源、样式与页面交互，`--headless` 启动后完成
基础读取即退出，`--no-mouse` 关闭鼠标追踪。页面与键位见 [终端界面](tui.md)。

## logs
读取实例 `logs/` 下最新的日志文件。

- `--process <进程>`：限定进程前缀；`--info` / `--debug`：限定日志级别文件。
- `--lines <N>`：首次输出的末尾行数，默认 50；`--follow`：持续输出新增行，直到 Ctrl+C。
- `--path`：只打印文件路径；`--json`：结构化输出。

## migrate
```sh
akaribot migrate legacy <旧项目> -I <新实例目录> --dry-run
```

旧项目须含 `bot.py`、`core/`、`modules/` 与 `config/config.toml`。迁移只读旧目录，可重复执行；
报告写到新实例根的 `migration-report.md`。选项：`--workspace-root` / `--dev`、`--skip-install`、
`--no-venv`、`--dry-run`、`--force`、`--offline`、`-v`。
