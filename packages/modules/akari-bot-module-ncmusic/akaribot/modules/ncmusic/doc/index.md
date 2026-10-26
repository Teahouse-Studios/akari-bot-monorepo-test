# 网易云音乐

搜索网易云音乐歌曲，按编号选择后查看歌曲详情，或在支持的平台上直接发送音乐卡片。

模块名 `ncmusic`，没有别名。

## 安装

```bash
akaribot module add akari-bot-module-ncmusic
```

安装后在会话中由管理员用 `module enable ncmusic` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 | 平台 |
| --- | --- | --- | --- |
| `ncmusic search <keyword> [--legacy]` | 搜索歌曲，回复编号选择；`--legacy` 强制使用文本列表 | 所有用户 | 全部 |
| `ncmusic <sid>` | 按歌曲 ID 获取音乐；开启卡片时发送音乐卡片，否则返回详情 | 所有用户 | QQ 群聊、QQ 私聊 |
| `ncmusic info <sid>` | 获取歌曲详细信息 | 所有用户 | 全部 |

搜索结果取前 10 首。平台支持图片且未指定 `--legacy` 时以表格图片展示编号、歌名、歌手、专辑与 ID，图片渲染没有产出时回退为文本列表。

选择流程：

- 只有一首结果时先询问是否查看详情。
- 多首结果时等待回复序号；序号非数字或超出范围时返回对应错误。
- 选中后返回封面、歌曲链接、歌名、ID、歌手与专辑信息。

`ncmusic <sid>` 在 `ncmusic_enable_card` 开启时向 QQ 发送 `[CQ:music,type=163,id=<sid>]` 音乐卡片；关闭时与 `info` 一致。

## 配置项

普通配置在 `module_ncmusic` 表（`config/module_ncmusic.toml`），敏感项在 `module_ncmusic_secret`。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ncmusic_enable_card` | bool | false | 是否在 QQ 客户端发送音乐卡片 |
| `ncmusic_api`（`module_ncmusic_secret`） | str | 空 | 网易云音乐 API 服务地址 |

`ncmusic_api` 为空时所有需要访问接口的命令返回配置缺失错误。搜索请求访问 `<ncmusic_api>/search?keywords=<keyword>`，详情请求访问 `<ncmusic_api>/song/detail?ids=<sid>`。`manifest.toml` 将 `ncmusic_api` 登记为重复凭据检查字段。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 模块声明支持语言为简体中文。
- 按 ID 获取音乐的命令仅对 QQ 群聊与 QQ 私聊开放；其他平台仍可使用搜索与详情命令。
- 卡片消息仅在 QQ 且开启 `ncmusic_enable_card` 时发送。

## 数据表

无。manifest 未声明 `owned_tables`，搜索与详情结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`。
- 外部服务：由 `ncmusic_api` 指定的网易云音乐 API 服务。
