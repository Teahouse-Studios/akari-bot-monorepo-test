# OpenBMCLAPI 数据

查询 OpenBMCLAPI 的实时仪表盘、节点排行、节点搜索与赞助商信息，数据来自公共接口。

模块名 `oba`，没有别名。

## 安装

```bash
akaribot module add akari-bot-module-oba
```

安装后在会话中由管理员用 `module enable oba` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `oba status` | 获取仪表盘数据 | 所有用户 |
| `oba node [<rank>]` | 获取指定排名节点的状态，省略排名时取第 1 名 | 所有用户 |
| `oba top [<rank>]` | 从指定排名开始列出至多 10 个节点，省略排名时从第 1 名开始 | 所有用户 |
| `oba search <keyword>` | 按名称或赞助商名称搜索节点，至多显示 10 条 | 所有用户 |
| `oba sponsor` | 获取随机节点赞助商 | 所有用户 |

字段说明：

- `status` 展示当前在线节点数、5 分钟负载百分比、总带宽、当前出网带宽、当日请求数、当日全网总流量，并附上 OpenBMCLAPI 版本与提交短哈希（可获取时）。
- `node` 与 `top` 以绿、红方块表示节点启用状态，展示节点名称、ID、当日流量、当日请求数与赞助商。`node` 的赞助商信息单独发送，并尝试附带横幅图片。
- `top` 从指定名次起列出至多 10 个节点并附带折叠提示；`search` 的排名沿用完整排行榜名次，超过 10 条时截断并提示折叠数量。
- `node` 的排名小于 1 或超出排行榜范围时返回无效节点提示；`top` 的排名小于 1 时按第 1 名处理。
- `search` 对节点名称与赞助商名称做不区分大小写的正则匹配，未找到时返回未找到提示。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 横幅图片发送失败时，赞助商消息退化为纯文本。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`。
- 外部服务：`https://bd.bangbang93.com/openbmclapi` 的 `metric/dashboard`、`metric/version`、`metric/rank`、`sponsor` 与 `sponsor/<id>` 接口。
