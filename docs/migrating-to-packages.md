# 从旧版迁移到按包发布

本文面向**使用旧版 AkariBot 的部署者**。旧版将机器人与全部模块置于同一个仓库中，通过 `git pull` 更新。新版将 core、模块与适配器拆分为互相独立的包，使用 `akaribot` 命令行工具（CLI）管理实例。

迁移可以直接使用 `akaribot migrate legacy <旧项目路径>` 完成（参见下节）。下面另附手动步骤，供需要逐项控制或排查问题时使用。

## 变化概览

| 项 | 旧版 | 新版 |
| --- | --- | --- |
| 获取更新 | `git pull` + `uv sync`（机器人内的 `~update`） | `akaribot module update --all`（机器人内的 `~update` 转由 CLI 执行） |
| 模块 | 随仓库内置，全部可用 | 按需安装：`akaribot module add <名>`，代码仅存在于实例虚拟环境（venv） |
| 依赖 | 整个仓库一份 | 每个包各自声明，实例 venv 内统一解析 |
| 配置与数据 | 仓库根目录下的 `config/`、`database/`、`data/` | 实例根目录下的同名目录，位置不变 |
| 多账号 | 一个平台一份配置 | 同一平台可创建多个实例：`akaribot adapter instance add <平台> <实例 ID>` |

## 自动迁移

```sh
akaribot migrate legacy <旧项目路径> --workspace-root <仓库路径>
```

迁移会校验旧项目布局（必须包含 `bot.py`、`core/`、`modules/` 与 `config/config.toml`）。旧模块名按多对一映射到新的包名，例如 `wikilog`/`weekly`/`weekly_rss` 都归入 `akari-bot-module-wiki`。

随后创建新实例、迁移配置与数据、安装映射后的包、转换数据库版本号，最后在新实例根目录写入 `migration-report.md`。**一律生成默认实例**（实例 ID 为空、`client_name` 与旧项目相同），因此 `target_id` 前缀不变、场景数据无需改写。

常用选项包括 `--dry-run`（仅输出报告，不写入文件）、`--skip-install`（仅迁移文件）、`--force`（覆盖同名文件）。迁移**不修改旧项目**。失败项会记入报告的“需人工处理”部分，可重新运行命令继续处理。

执行真实迁移前必须停止源实例并保存配置、数据库和 `data/` 的备份。

复制期间迁移程序会持有源目录的 `.bot.lock`，并将 SQLite 主数据库与已提交的预写日志（WAL）数据通过独立快照复制到目标目录，同时将目标配置中的数据库地址指向该副本。缺少 `.bot.lock` 的旧目录应先正常启动并停止一次以生成锁文件，试运行模式下则允许该锁文件不存在。

MySQL 等外部数据库不支持自动复制迁移，需要先导出到独立目标并按手动步骤处理。SQLite 外部文件的其他写入者同样必须停止。

迁移复制根 `data/`，历史 `assets/` 内容仅补充缺失项。已有目标配置和数据库在未使用 `--force` 时保留。数据库绑定冲突或目标路径含符号链接时拒绝继续。`--skip-install` 不执行数据库升级。

## 手工迁移步骤

以下命令中的 `<实例目录>` 建议新建（例如 `/opt/akaribot`），**不要**在旧仓库里就地升级。

1. **确认 Python 与 uv**：需要 Python 3.12 或更高版本与 [uv](https://docs.astral.sh/uv/)。
2. **创建新实例**：

```sh
   akaribot init <实例目录> --locale zh_cn --adapter <平台>
   ```

   `--adapter` 可多次指定，取值如 `telegram`、`discord`、`qqbot`、`kook`、`matrix`、`onebot`、`web`、`milky`。若你的包尚未发布到 PyPI（例如自己从源码构建），加 `--workspace-root <仓库路径>` 按本地路径安装。
3. **迁移配置**：将旧仓库 `config/` 下的文件复制到 `<实例目录>/config/`。配置表名与文件名一一对应（`config.toml`、`bot_telegram.toml`、`module_wiki.toml` …）。复制后逐项核对：

```sh
   akaribot config schema --table bot_telegram      # 查看该表全部键、类型、注释与占位情况
   akaribot config set telegram_token <值> --table bot_telegram
   ```

   在安装模块或升级数据库之前，将 `[secret].db_path` 设置为目标副本或独立目标数据库的地址。绝对 SQLite 路径和远程连接地址不得继续指向源部署。

4. **迁移数据**：将旧仓库的 `database/`、`data/`、`assets/`（若存在自定义内容）复制到实例根目录下。数据库首次启动时会自动执行迁移，旧版本号由迁移系统转换。

```sh
   akaribot module available            # 列出可安装的包及其「已安装／可安装」状态
   akaribot module add wiki
   akaribot module add dice
   akaribot module list                # 核对已装清单
   ```

   模块按需安装，不随仓库内置。旧配置中出现的模块若未安装，其命令不会被注册。自建模块可以直接从 git 仓库安装：

```sh
   akaribot module add --git https://github.com/<你>/<仓库>.git
   akaribot module add --git https://github.com/<你>/<仓库>.git --ref v1.0   # 钉到分支、标签或提交
   akaribot module add --git https://github.com/<你>/<仓库>.git --subdir packages/my-mod
   ```

   仓库里包的 `pyproject.toml` 必须声明 `akaribot.modules` 或 `akaribot.adapters` entry point。

   自建包升级数据库结构后重启实例，启动阶段会按包的迁移记录升级数据库：

```sh
   akaribot run --stop
   akaribot run --detach
   ```

6. **校验**：

```sh
   akaribot doctor                     # 端口冲突、凭据重复、孤立配置
   akaribot run --detach               # 后台启动；控制台输出在 <实例目录>/logs/RunConsole_<日期>.log
   akaribot run --status               # 运行状态与进程号
   akaribot run --stop                 # 停止（含由界面或系统服务启动的实例）
   ```

   在前台运行请使用 `akaribot run`。要在后台以服务方式常驻，参见下文“注册常驻服务”。

   实例的进程号记录在实例级锁 `<实例目录>/.bot.lock` 中，`run --stop` 据此终止进程，因此无论实例是谁启动的都能正常停止。后台实例自建会话，启动它的终端退出后继续运行。

   要使用终端界面管理实例、模块、配置与环境，运行 `akaribot tui`。若无实例，会先询问是否就地创建新实例或写入已有实例目录。

   界面启动时会将当前所在的实例写入注册表，记录保存在 `~/.akaribot/instances.toml`。

   在实例目录之外启动界面且下级目录中仅有一个实例时，界面会自动将其写入注册表并切换到该实例，因此从项目根目录启动也能直接管理该实例。无图形终端的环境请使用命令行子命令。

   单台机器可管理多个实例，使用 `akaribot instance add <名> <路径>` 将其他目录加入列表。

   界面概览页的实例清单提供相同操作，在条目上回车即切换当前管理的实例。按 `n` 添加时输入框已预先填充当前实例目录，回车即写入注册表。

   额外需要的运行库（第三方 SDK、自行打包的包）可使用 `akaribot venv add <依赖声明>` 安装至实例环境。`--save`（默认）会同时写入 `akaribot.toml` 的 `runtime.requirements`，`venv recreate` 与 `venv adopt` 会按此列表补充安装。`--no-save` 仅安装至当前环境，重建后不保留。

   卸载请使用 `akaribot venv remove <包名>`，加上 `--no-save` 则仅卸载包但保留记录。界面环境页提供相同功能，并列出环境中**全部**已安装包（包含 httpx 这类间接依赖）以及各记录的来源。

   要让实例随机器启动、崩溃后自动重启，先执行 `akaribot service install` 安装常驻服务（macOS 写 `~/Library/LaunchAgents`，Linux 写 systemd 用户单元），再用 `akaribot instance policy <名> --autostart --restart-on-crash` 逐实例启用策略。

   服务启动时仅恢复**已启用开机自启**且上次处于运行状态的实例，停电前正在运行但未启用自启的实例不会被自动启动。崩溃后自动重启由另一个独立开关控制。

## 同一平台运行多个账号

迁移一律生成**默认实例**，它的 `client_name` 与旧项目完全一致，因此历史场景数据（`target_id` 前缀）原样可用。需要在同一平台新增账号时创建新实例：

```sh
akaribot adapter list                          # 按平台列出全部实例
akaribot adapter instance add telegram work    # 新实例：写 config/bot_telegram-work.toml 的 [bot_telegram-work]
akaribot doctor                                # 检测监听端口冲突与两个实例配了同一账号
```

新实例的 `client_name` 带 `-<实例 ID>` 后缀（如 `Telegram-work`），`target_id` / `sender_id` 因此带新的前缀，与默认实例的历史数据互相独立。

实例 ID 一旦分配使用即**不可更改**，因为修改名称需要跨多张核心表与模块表迁移前缀，需要更换 ID 时按“新建实例并迁移数据”处理。`add` 生成的配置中 `enable` 默认设为 `false`，填写登录信息后再启用。

## 机器人内更新

机器人内的 `~update` 会交由 CLI 执行 `module update --all --defer-runtime`，安装包并同步配置后返回结果。数据库迁移和运行代码切换会在下一次启动时完成，因此更新后需要按提示执行 `~restart`。若使用 `~update&restart`，则会在更新完成后自动执行重启。宿主机上也可直接执行：

```sh
akaribot module update --all
```

宿主机更新会执行数据库迁移和模块热加载。涉及数据结构的升级应先停止实例并保留备份。若仅需安装包并等待后续重启生效，请使用 `--defer-runtime`。

`akaribot venv recreate` 在独立的新环境中安装并验证后再替换原环境，最终路径验证失败时恢复旧环境。失败的 `.new` 目录保留供检查，已有 `.old` 备份不会自动删除。

## 已知限制

- **实例 ID 一旦使用请勿更改**：修改名称需要跨多张核心表与模块表迁移 `target_id` 前缀，改动成本与风险过高，因此不提供重命名功能。需要更换 ID 时请新建实例并迁移数据。
- **终端界面（TUI）兼容性**：Textual 界面目前仅在 macOS 上完成过无界面渲染与布局测试，在 Windows 终端、旧版控制台（conhost）、tmux 以及窄屏幕 SSH 终端下的实际表现尚未验证。遇到显示问题请改用命令行子命令。
- **配置文件位置**：适配器实例配置保存在 `config/<表名>.toml`（扁平布局）。分层布局（`config/adapters/`）尚未启用，请勿手动移动相关文件。

## 遇到问题时

```sh
akaribot doctor                       # 自检
akaribot venv status                  # 实例 venv 的托管模式与已装包数量
akaribot module list                  # 已装清单
akaribot config schema --table <表名>  # 该表的全部键与注释
```

`akaribot` 的每个子命令都支持 `--help`。`--json` 选项（`module list`、`config schema` 等）便于脚本处理。
