# GitHub 查询

通过 GitHub REST API 查询仓库、用户或组织信息，并按关键词搜索仓库。仓库结果包含 Star、Fork、语言与许可证，用户结果包含关注数、公开仓库数与最近活跃时间。

## 安装

```bash
akaribot module add akari-bot-module-github
```

模块名为 `github`，命令前缀为 `github`，别名为 `gh`。

## 命令

| 命令 | 说明 |
| --- | --- |
| `github <name>` | 自动识别：名称含 `/` 时查询仓库，否则查询用户或组织 |
| `github repo <name>` | 查询仓库信息，并附带 OpenGraph 预览图 |
| `github user <name>` | 查询用户或组织信息 |
| `github search <keyword>` | 搜索仓库，最多列出 5 条结果 |

仓库、用户与搜索接口共用同一个可选令牌；未配置令牌时以匿名身份请求。仓库或用户不存在时返回未找到提示。

## 配置项

配置文件为 `config/module_github.toml`。

| 表 | 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `module_github_secret` | `github_pat` | str | 空 | GitHub 的 Personal Access Token，用于提高 API 请求速率限制 |

`module_github_secret` 是敏感表，字段值加密存储。留空时按匿名请求处理，速率限制更低。

## 权限与平台能力

- 所有命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 查询结果会经过内容安全检查，命中风险规则时返回占位内容。
- `repo` 会发送 OpenGraph 预览图，平台需支持图片消息。

## 数据表

无。查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`。
- GitHub REST API：`https://api.github.com`，用于仓库、用户与仓库搜索接口。
- OpenGraph 预览图：`https://opengraph.githubassets.com`。
