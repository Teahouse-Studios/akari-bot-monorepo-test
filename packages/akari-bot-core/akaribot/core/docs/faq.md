# 常见问题

本文汇总常见问题的排查与解决方案。相关命令与默认配置均以当前源码实现为准。权限模型、模块启用及部署细节分别参见[权限](permissions.md)、[模块开发](module-development.md)与 [CLI 文档](../../../../akari-bot-cli/akaribot/cli/docs/index.md)。

## 查看帮助与文档

在会话中发送 `~help` 可查看可用模块列表与命令入口。发送 `~help <module>` 可获取指定模块的详细命令语法、参数定义及权限要求。

- `--legacy`：显式输出纯文本或表格版本。
- `--img`：显式输出图片渲染版本。
- 若当前平台未声明图片支持能力，帮助命令将自动降级输出文本版本。

文档站点由已安装成员包内的 `docs/` 资源聚合构建生成，常用运维命令如下：

```sh
akaribot docs list
akaribot docs build
akaribot docs serve
```

文档构建依赖 Node.js 与 npm 环境，具体版本要求以主题清单声明为准。站点生成产物存放于实例目录 `cache/docs/`。`~help` 面板底部的在线文档链接读取自 `config.toml` 中的 `help_url` 与 `help_page_url` 配置项。

## 模块没有反应或未启用

首先确认目标模块是否已安装、是否已全局加载以及是否在当前场景中启用。这三项状态相互独立：

| 状态 | 检查方式 | 修改方式 |
| --- | --- | --- |
| 已安装 | `akaribot module list` | `akaribot module add <名>` |
| 全局加载 | `akaribot module status` | `akaribot module load <名>` |
| 场景启用 | `~module list` | `~module enable <名>` |

声明 `base=True` 的核心基础模块始终处于启用状态。普通功能模块需要由场景管理员执行 `~module enable` 手动启用。

- 未启用时，机器人会提示启用命令。
- 声明了 `required_superuser` 的模块仅超级用户可以启用。`~module enable all` 会跳过此类模块。

若模块处于启用状态但仍未响应指令，请排查平台能力支持与机器人权限：

- `rss` 模块要求平台具备主动推送能力（`support_rss`）。
- `regex` 与 `event` 模块要求平台具备全部消息接收权限（`read_all_messages`）。
- 当机器人缺失 `required_bot_permissions` 声明的必要权限时，`~module enable` 将列出缺失的权限项。

当机器人被限制发言或发送者处于封禁状态时，各模块将静默拒绝响应。

## 提示权限不足

权限层级划分为普通用户、场景管理员、超级用户与基础超级用户，鉴权逻辑与授权机制参见[权限说明](permissions.md)。常见处理方案如下：

- 若场景管理命令被拒绝，可由场景管理员执行 `~admin add <用户 ID>`，或由平台原生管理员操作。
- 若超级用户命令被拒绝，可由现有超级用户执行 `~superuser add <用户 ID>`。
- 若仅特定模块被拒绝，可由超级用户执行 `~auth add <用户 ID> <模块>`，该授权仅对声明 `required_superuser` 的模块生效。
- 若模块开启被拒绝，通常由模块级权限门槛、机器人权限缺失或平台能力不满足导致，请根据返回的提示排查。

`base_superuser` 仅能通过 `config.toml` 维护。

## 报告问题与贡献

提交 Issue 前必须检索是否已存在同类问题。缺陷报告应当包含简要描述、复现步骤、预期结果、实际表现与相关日志。新功能建议应当阐明应用场景与设计思路。仓库地址与 Issue 模板参见 [CONTRIBUTING.md](https://github.com/Teahouse-Studios/akari-bot/blob/master/CONTRIBUTING.md)。

代码贡献流程包括 Fork 仓库后创建特性分支，完成改动后发起拉取请求（PR）。分支命名必须采用英文，新功能分支以 `dev/` 为前缀，缺陷修复分支以 `fix/` 为前缀。发起提交前必须执行 Ruff、注释检查、边界检查与版本一致性检查，对应命令参见贡献指南。

多语言翻译统一通过 Weblate 平台提交。简体中文以外的翻译词句讨论，请勿在 GitHub Issue 中提出。

<NoticeBox type="warning" title="安全问题不要公开">

涉及安全漏洞与敏感信息的缺陷不得提交至公开 Issue 或公开讨论区，请通过 `SECURITY.md` 中列出的私密沟通渠道联系维护团队。

</NoticeBox>

## 许可证

core、官方内置模块及平台适配器采用 AGPL-3.0-only 开源许可证。字体资产采用 OFL-1.1 协议，品牌视觉资产采用专有商业授权，`akari-bot-html2text` 采用 GPL-3.0 协议。各成员包所适用的具体许可协议，以该包内 `pyproject.toml` 及 LICENSE 文件中的明确声明为准。

修改并分发本项目衍生版本时，必须严格遵守对应的开源许可协议约束。AGPL-3.0 许可证额外要求通过网络向服务终端用户公开对应的完整源代码。

## 更新实例

实例环境中的 core、功能模块及适配器均通过 CLI 统一更新：

```sh
akaribot module update --all
```

在线执行 `~update` 时，系统将调用 CLI 的 `module update --defer-runtime` 命令。软件包安装完成后，按提示执行 `~restart`。指定 `--defer-runtime` 参数时，该阶段仅下载并安装软件包、同步配置，数据库迁移与代码生效将推迟至下一次启动时执行。

在宿主机环境直接执行升级时，数据库迁移与新版代码将立即生效。若升级涉及底层数据结构变更，必须首先停止实例进程，并完整备份数据库文件与配置目录。CLI 工具自身请按照 `uv tool` 的标准更新方式升级。

## 自建实例

运行环境需要满足仓库 `pyproject.toml` 中声明的 Python 版本及 [uv](https://docs.astral.sh/uv/) 包管理器要求。基础搭建流程如下：

```sh
uv tool install akari-bot-cli
akaribot init /opt/akaribot --adapter telegram
cd /opt/akaribot
akaribot config schema --table bot_telegram
akaribot doctor
akaribot run
```

依据 `config schema` 输出的字段定义配置适配器的登录信息，随后启动机器人实例。使用 `akaribot config set <字段> <值> --table <表名称>` 命令写入的配置值，将依据对应配置模板所声明的类型执行自动转换。

`akaribot init` 默认安装品牌资产、表情与常规可选依赖。指定 `--minimal` 时仅安装核心所需的最小依赖。模块通过 `akaribot module add <名>` 安装。历史部署的备份、试运行与迁移参见 [命令参考中的 migrate](../../../../akari-bot-cli/akaribot/cli/docs/commands.md#migrate)。
