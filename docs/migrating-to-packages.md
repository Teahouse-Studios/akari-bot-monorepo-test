# 从旧版迁移到按包发布的形态

本文面向**使用旧版 AkariBot 的部署者**。旧版把机器人与全部模块放在同一个仓库里，靠 `git pull`
更新；新版把 core、模块与适配器拆成互相独立的分发包，用 `akaribot` 命令行工具管理实例。

迁移可直接用 `akaribot migrate legacy <旧项目路径>` 完成（见下节）；下面另附手工步骤，供需要
逐项控制或排查问题的场合使用。

## 变化概览

| 项 | 旧版 | 新版 |
| --- | --- | --- |
| 获取更新 | `git pull` + `uv sync`（机器人内的 `~update`） | `akaribot module update --all`（机器人内的 `~update` 已改为委托 CLI） |
| 模块 | 随仓库内置，全部可用 | 按需安装：`akaribot module add <名>`，代码只存在于实例 venv |
| 依赖 | 全仓一份 | 每个包各自声明，实例 venv 内统一解析 |
| 配置与数据 | 仓库根下的 `config/`、`database/`、`data/` | 实例根下的同名目录，位置不变 |
| 多账号 | 一个平台一份配置 | 同一平台可建多个实例：`akaribot adapter instance add <平台> <实例 ID>` |

## 自动迁移

```
akaribot migrate legacy <旧项目路径> --workspace-root <仓库路径>
```

迁移会校验旧项目布局（须含 `bot.py`、`core/`、`modules/` 与 `config/config.toml`），把旧模块名
映射到新的分发包名（**多对一**：`wikilog`/`weekly`/`weekly_rss` 都归入 `akari-bot-module-wiki`），
建新实例、搬配置与数据、装映射到的包、转换数据库版本号，最后在新实例根写出
`migration-report.md`。**一律生成默认实例**（实例 ID 为空、`client_name` 与旧项目相同），因此
`target_id` 前缀不变、场景数据无需改写。

常用开关：`--dry-run`（只输出报告不写文件）、`--skip-install`（只搬文件）、`--force`（覆盖同名文件）。
迁移**不修改旧项目**；失败项会记入报告的「需人工处理」，可重跑续做。

## 手工迁移步骤

以下命令中的 `<实例目录>` 建议新建（例如 `/opt/akaribot`），**不要**在旧仓库里就地升级。

1. **确认 Python 与 uv**：需要 Python 3.12 与 [uv](https://docs.astral.sh/uv)。
2. **建新实例**：

   ```
   akaribot init <实例目录> --locale zh_cn --adapter <平台>
   ```

   `--adapter` 可重复，取值如 `telegram`、`discord`、`qqbot`、`kook`、`matrix`、`onebot`、`web`、
   `milky`。若你的包尚未发布到 PyPI（例如自己从源码构建），加 `--workspace-root <仓库路径>`
   走本地路径安装。
3. **搬运配置**：把旧仓库 `config/` 下的文件复制到 `<实例目录>/config/`。配置表名与文件名一一对应
   （`config.toml`、`bot_telegram.toml`、`module_wiki.toml` …）。复制后逐项核对：

   ```
   akaribot config schema --table bot_telegram      # 查看该表全部键、类型、注释与占位情况
   akaribot config set telegram_token <值> --table bot_telegram
   ```

4. **搬运数据**：把旧仓库的 `database/`、`data/`、`assets/`（若你自建过）复制到实例根下。数据库
   首次启动时会自动执行迁移；旧版本号会由迁移系统转换。
5. **安装你实际用到的模块**：

   ```
   akaribot module add wiki
   akaribot module add dice
   akaribot module list                # 核对已装清单
   ```

   模块不再随仓库内置，旧配置里出现的模块若未安装，其命令不会被注册。
6. **校验**：

   ```
   akaribot doctor                     # 端口冲突、凭据重复、孤立配置
   akaribot run                        # 启动；日志在 <实例目录>/logs/
   ```

   需要交互界面时用 `akaribot tui`（无图形终端的环境请用命令行子命令）。

## 旧版 `~update` 的行为变化

机器人内的 `~update` 不再执行 `git pull` 与 `uv sync`——实例里没有仓库，依赖也装在实例 venv 而非
当前环境。现在它改为委托 `akaribot` 命令行工具执行 `module update`，并把结果回报给发起者；若更新
了模块，按提示 `~restart` 或由运行时热装载。宿主机上也可以直接执行：

```
akaribot module update --all
```

## 已知限制

- **`langconv` 相关包暂不可安装**：`akari-bot-module-langconv`、`akari-bot-module-hitokoto`、
  `akari-bot-module-maimai` 依赖的上游库目前只有 Git 直链（上游停更，修复版 fork 尚未发版），
  而 Git 直链依赖无法随分发包发布。这三个包要等该库正式发版后才能安装。
- **实例 ID 一旦使用请勿更改**：改名需要跨多张核心表与模块表迁移 `target_id` 前缀，收益与风险
  不成比例，故不提供重命名。需要换 ID 时请新建实例并迁移数据。
- **TUI 的终端兼容性**：Textual 界面目前只在 macOS 上做过无头渲染与布局验证，Windows 终端、
  旧 conhost、tmux 与 SSH 窄终端下的实际表现尚未验证；遇到显示问题请改用命令行子命令。
- **配置文件位置**：适配器实例配置写在 `config/<表名>.toml`（扁平布局）。分层布局
  （`config/adapters/`）尚未启用，请勿手工移动这些文件。

## 遇到问题时

```
akaribot doctor                       # 自检
akaribot venv status                  # 实例 venv 的托管模式与已装包数量
akaribot module list                  # 已装清单
akaribot config schema --table <表名>  # 该表的全部键与注释
```

`akaribot` 的每个子命令都支持 `--help`；`--json` 选项（`module list`、`config schema` 等）便于脚本
消费。
