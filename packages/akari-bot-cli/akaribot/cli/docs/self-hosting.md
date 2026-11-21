# 自搭建指南

搭建自己的小可，需要一台能运行 Python 的机器，以及一个准备接入的平台账号。

这份指南以终端界面（TUI）为主。安装完成后，创建实例、填配置、装适配器、启停和看日志都可以在界面里完成，不需要记命令。命令行只用于安装，以及自动化、无头服务器等场景。

## 先认识几个部分

- **CLI**：`akaribot` 命令和 TUI。它装在实例之外，负责创建、启动和检查实例。
- **实例**：一个独立目录，保存配置、数据库、日志、缓存和实例自己的 Python 环境。
- **core**：机器人的运行时。
- **适配器**：连接具体平台，例如 Telegram、QQ、Discord 或 Web。
- **模块**：提供命令和功能，例如查询、订阅、小游戏。

CLI 通过 core 的子进程入口读写实例。实例可以单独升级，CLI 的环境依赖与实例隔离。

## 准备环境

需要：

- Python。具体版本范围见仓库根目录 `pyproject.toml` 的 `requires-python`。
- [uv](https://docs.astral.sh/uv/)，用于创建实例环境并安装分发包。
- 只在本地构建文档站点时需要 Node.js 和 `npm`。版本要求由主题的 `docs-theme.json` 声明。

默认数据库是 SQLite，连接串为 `sqlite://database/save.db`。需要 MySQL 时，把密钥表中的 `db_path` 换成 MySQL 连接串。core 默认安装的依赖已经包含 MySQL 驱动。

## 安装 CLI

把 CLI 装成独立工具，不要装进实例环境。

```sh
uv tool install akari-bot-cli
akaribot --version
```

这是整份指南里唯一需要手动输入的命令。装好后，后面的操作都在 TUI 里完成。

如果从仓库源码使用，在仓库根目录执行：

```sh
uv sync --all-extras --dev
.venv/bin/akaribot --version
```

后面的 `akaribot` 换成 `.venv/bin/akaribot` 即可。

## 打开 TUI

```sh
akaribot
```

不带子命令运行时，只要终端支持交互，就会进入界面。也可以显式执行 `akaribot tui`。

界面打开后会进入概览页。如果当前目录没有实例，右侧实例列表是空的，按 `n` 新建一个。

### 新建实例

在概览页按 `n`，选择「新建实例」，填写：

| 字段 | 说明 |
| --- | --- |
| 实例目录 | 实例保存位置，例如 `/srv/akaribot`。目录不存在时由界面创建。 |
| 运行环境 | 推荐使用「托管 venv」，由实例自己管理 Python 环境。 |

实例语言跟随当前界面语言。确认后，界面会调用 `akaribot init` 创建目录、建立虚拟环境、安装 core 和默认适配器，并应用数据库迁移。完成后，概览页会出现这个实例，并切换到它。

默认会安装 Telegram 适配器。想从创建时就安装别的适配器，见文末「高阶：命令行」。

## 填写核心配置

进入「配置」页，先选 `config` 表，再按 `f` 打开表单。

需要先填的通常是：

- `base_superuser`：你的发送者 ID。默认值来自上游维护者，自建实例要换成自己的账号，或者清空。
- `db_path`：默认 SQLite 够用，暂时不用改。
- `proxy`、`ffmpeg_path` 等：没有对应环境时留空。

`secret` 表放令牌和密钥。表单会把待填项排在前面，`Enter` 进入下一项，`Ctrl+S` 保存。保存前，界面会提示还没有写入的占位符。

不想用表单时，按 `t` 切换到原始文本，或按 `o` 用外部编辑器打开。保存后如果提示重新加载，按页面提示操作。

## 创建适配器实例

默认的 Telegram 适配器已经安装，但还没有实例。进入「适配器」页：

1. 按 `n` 新建实例。
2. 选择 Telegram。
3. 填一个实例 ID，例如 `main`。这个字段必填。
4. 在配置表单里填 Bot Token。
5. 把 `enable` 改成开启，按 `Ctrl+S` 保存。

实例 ID 只能使用小写字母、数字和下划线，长度 1 到 24。实例配置写在 `config/bot_telegram-main.toml` 这样的文件里。

需要 Web、Discord 或别的平台时：

1. 在「适配器」页按 `i`，选择要安装的平台。
2. 安装完成后按 `n`，按上面的步骤创建实例、填配置、开启。

平台账号、Token 和回调地址的申请方式见各适配器的文档，入口在「适配器」页或左侧文档分类里。

## 启动机器人

进入「运行」页，按 `s` 启动当前实例。启动前会弹出确认框，确认后界面在后台启动进程，状态会自动刷新。

启动后，在群里或私聊里给机器人发一条命令，例如：

```text
~help
```

能看到回复，说明适配器和机器人已经接通。

停止按 `x`，重启按 `Ctrl+R`。退出 TUI 后，机器人仍在后台运行。

## 安装模块

进入「模块」页，按 `i` 安装需要的模块，选择目标后确认。安装完成只是把代码放进实例。

模块要在实例里全局加载，才会参与命令匹配。选中模块后按 `e` 切换加载状态。

某个群或频道是否能用这个模块，还要单独开启。在聊天里执行：

```text
~module enable <模块名>
```

安装只把代码放进实例。全局加载后，命令才会参与匹配。场景启用后，群里才能使用。

## 设置常驻服务

确认机器人能正常启动后，回到「概览」页，按 `m` 打开服务与策略菜单：

- 开启开机自启。
- 开启崩溃后自动重启。
- 安装系统服务，让实例在退出 TUI 后继续运行。

Windows 暂不支持服务安装。需要开机启动时，用任务计划程序或容器编排工具代替。

服务恢复实例时要同时满足两个条件：开机自启已开启，实例上次处于运行状态。

## 更新与备份

### 更新

在「模块」页按 `r` 刷新，再按 `U` 更新已安装的包，包括 core、适配器和模块。更新后界面会尝试重新加载。需要重启才能生效的改动，到「运行」页按 `Ctrl+R`。

更新前先备份配置、数据和数据库。更新失败时先看「日志」页的错误，再判断是否回退。

### 备份

需要备份的内容：

| 路径 | 内容 |
| --- | --- |
| `akaribot.toml` | 实例元数据。 |
| `config/` | 配置表与密钥。 |
| `data/` | 模块数据与实例私有数据。 |
| `database/` | SQLite 数据库。 |
| `assets/private/` | 实例私有资源。 |

`cache/`、`logs/` 和 `.venv/` 可以不备份。恢复时把上面的目录放回实例根目录，再启动实例。

## 排查问题

- 「诊断」页：检查端口冲突、重复的登录信息、没有对应适配器的配置。
- 「日志」页：按 `m` 切换日志文件，按 `/` 过滤关键词。
- 「配置」页：确认适配器的 `enable` 已开启，Token 没有多余空格。
- 「运行」页：确认进程状态，必要时停止后重新启动。

如果启动时提示配置表不存在，先在「适配器」或「模块」页重新安装对应包，让安装流程补配置，再检查配置目录。

## TUI 常用键位

| 键 | 作用 |
| --- | --- |
| `q` / `Ctrl+Q` | 退出界面。 |
| `?` | 查看当前页与全局键位。 |
| `Ctrl+←` / `Ctrl+→` | 上一页 / 下一页。 |
| `↑` / `↓` / `Enter` | 选择并打开。 |
| `←` / `→` | 收起 / 展开侧栏分组。 |
| `r` | 刷新当前页。 |
| `Ctrl+S` | 保存当前编辑内容。 |
| `Esc` | 返回或取消当前操作。 |

各页的完整键位见 [终端界面](tui.md)。

## 高阶：命令行

TUI 覆盖日常操作。下面这些命令适合自动化、批量部署和无头服务器。

创建实例时指定适配器或模块：

```sh
akaribot init /srv/akaribot --adapter telegram --adapter web
akaribot init /srv/akaribot --module wiki
```

后台运行与服务：

```sh
akaribot run -d
akaribot service install
akaribot service status
```

配置与模块：

```sh
akaribot config list
akaribot config schema --table config
akaribot module add wiki
akaribot module update --all
```

实例与诊断：

```sh
akaribot instance list
akaribot doctor
akaribot logs --follow
```

在容器里运行时，实例目录挂载到容器内，用 CLI 启动。容器内没有可用的 TUI。具体参数见 [命令参考](commands.md)。

## 相关文档

- [命令参考](commands.md)：所有子命令与选项。
- [配置](../../../../akari-bot-core/akaribot/core/docs/config.md)：配置表、密钥与默认层。
- [适配器开发](../../../../akari-bot-core/akaribot/core/docs/adapter-development.md)：写一个新的平台适配器。
- [模块开发](../../../../akari-bot-core/akaribot/core/docs/module-development.md)：从第一个模块开始。
- [常见问题](../../../../akari-bot-core/akaribot/core/docs/faq.md)：启动、权限和平台相关的常见问题。
