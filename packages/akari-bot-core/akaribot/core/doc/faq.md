# 常见问题

本文整理了常见问题的排查与操作办法。命令与默认值以当前源码为准，权限模型、模块启用与部署细节分别见[权限](permissions.md)、[模块开发](module-development.md)与 [CLI 文档](../../../../akari-bot-cli/akaribot/cli/doc/index.md)。

## 查看帮助与文档

在聊天中发送 `~help` 查看模块列表与入口，发送 `~help <module>` 查看指定模块的命令、参数与权限。`--legacy` 强制输出文字或表格版本，`--img` 强制输出图片版本。平台不支持图片时，命令会改用文字版本。

文档站点由已安装包内的 `doc/` 汇总生成，常用命令：

```sh
akaribot docs list
akaribot docs build
akaribot docs serve
```

构建需要 Node.js 18 或更高版本与 npm。生成物写在实例的 `cache/docs/`，不影响仓库。`~help` 底部的在线文档入口由 `config.toml` 的 `help_url` 与 `help_page_url` 决定。

## 模块没有反应或未启用

先确认模块是否安装、是否全局装载、是否在当前场景启用，这是三个独立状态：

| 状态 | 检查方式 | 修改方式 |
| --- | --- | --- |
| 已安装 | `akaribot module list` | `akaribot module add <名>` |
| 全局装载 | `akaribot module status` | `akaribot module load <名>` |
| 场景启用 | `~module list` | `~module enable <名>` |

`base=True` 的基础模块始终启用，场景内不能关闭。普通模块需要场景管理员执行 `~module enable` 启用。未启用时，机器人会提示启用命令。声明了 `required_superuser` 的模块只有超级用户能启用，`~module enable all` 会跳过它们。

如果模块已启用仍不响应，先检查平台能力与机器人权限：`rss` 模块要求平台支持推送，`regex` 与 `event` 模块要求平台可读取全部消息。`required_bot_permissions` 中的权限缺失时，`~module enable` 会列出缺少项。

场景被禁止发言或用户被封禁时，模块也不会响应。

## 提示权限不足

权限分为普通用户、场景管理员、超级用户与基础超级用户，判定与授予方式见[权限](permissions.md)。常见处理：

- 场景管理命令被拒：请场景管理员执行 `~admin add <用户 ID>`，或由平台原生管理员操作。
- 超级用户命令被拒：请现有超级用户执行 `~superuser add <用户 ID>`。
- 只有某个模块被拒：请超级用户执行 `~auth add <用户 ID> <模块>`，该授权只对声明 `required_superuser` 的模块有效。
- 模块开启被拒：可能是模块级权限、机器人权限或平台能力不足，按提示处理。

`base_superuser` 只能通过 `config.toml` 维护，机器人内没有授予命令。

## 报告问题与贡献

提交 Issue 前先搜索是否已有相同问题。错误报告应包含简要描述、复现步骤、预期结果、实际结果与相关日志。功能建议应说明用途与可能的实现方式。仓库地址与 Issue 模板见 [CONTRIBUTING.md](https://github.com/Teahouse-Studios/akari-bot/blob/master/CONTRIBUTING.md)。

贡献代码的流程是：先 Fork 仓库，再创建分支、修改并提交 PR。分支名使用英文，新功能用 `dev/`，修复用 `fix/`。提交前运行 Ruff、注释检查、边界检查与版本检查，具体命令见贡献指南。

翻译经 Weblate 提交。简体中文以外的翻译问题，不建议在 Issue 里讨论。

<NoticeBox type="warning" title="安全问题不要公开">

涉及敏感信息的安全问题不要提交到 Issue 或其他公开渠道，应按 `SECURITY.md` 的方式私下联系维护者。

</NoticeBox>

## 未开放源代码的模块

公开仓库与 `registry.json` 只包含可分发的包。少数模块涉及第三方版权或平台授权，无法按 AGPL-3.0 发布，因此不随仓库或公开 registry 提供。品牌资产（角色立绘、标志）由画师保留权利，随 `akari-bot-assets-brand` 以 `LicenseRef-Proprietary` 分发，不属于开源部分。

## 许可证

core、官方模块与适配器使用 AGPL-3.0-only。字体资源使用 OFL-1.1，品牌资产使用专有许可，`akari-bot-html2text` 使用 GPL-3.0。每个分发的 `pyproject.toml` 与包内 LICENSE 是最终依据。修改并分发本项目时须遵守对应许可证，AGPL-3.0 还要求向网络用户提供对应源码。

## 更新实例

实例内的 core、模块与适配器统一由 CLI 更新：

```sh
akaribot module update --all
```

机器人内的 `~update` 会委托 CLI 执行 `module update --defer-runtime`，安装完成后按提示执行 `~restart`。`--defer-runtime` 只安装包并同步配置，数据库迁移与代码切换留到下次启动。

在宿主机上直接更新会立即执行迁移并载入新代码。涉及数据结构的升级，应先停止实例，备份数据库与配置。CLI 本身按 `uv tool` 的安装方式升级。

## 自建实例

需要 Python 3.12 或更高版本与 [uv](https://docs.astral.sh/uv/)。基本流程：

```sh
uv tool install akari-bot-cli
akaribot init /opt/akaribot --adapter telegram
cd /opt/akaribot
akaribot config schema --table bot_telegram
akaribot doctor
akaribot run
```

按 `config schema` 的结果填写适配器的登录信息后再启动。`akaribot config set <字段> <值> --table <表名>` 会按模板类型转换。

`akaribot init --minimal` 选择核心最小依赖，不加该参数时默认安装品牌、表情与常规可选依赖。模块用 `akaribot module add <名>` 安装。旧部署的备份、试运行与迁移见 [命令参考中的 migrate](../../../../akari-bot-cli/akaribot/cli/doc/commands.md#migrate)。
