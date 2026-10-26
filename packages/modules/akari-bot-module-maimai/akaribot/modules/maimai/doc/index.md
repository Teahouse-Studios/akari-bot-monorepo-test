# 舞萌 DX 与 CHUNITHM

查询舞萌 DX 与 CHUNITHM 的曲目资料、谱面成绩、B50/B30、名牌板、段位与评级进度，并支持绑定水鱼查分器与落雪咖啡屋账号。包内注册三个模块：`maimai`、`chunithm` 与 `maimai-regex`。

## 安装

```bash
akaribot module add akari-bot-module-maimai
```

| 模块 | 命令前缀 | 别名 | 说明 |
| --- | --- | --- | --- |
| `maimai` | `maimai` | `mai` | 舞萌 DX 查询 |
| `chunithm` | `chunithm` | `chu` | CHUNITHM 查询 |
| `maimai-regex` | 无命令前缀 | `maimai_regex`、`mai_regex` | 以自然语言句式触发的正则模块 |

## 命令

常用命令见下表；按用途分列的全部命令、选项与权限见[完整命令](commands.md)，自然语言触发句式见[正则句式](regex.md)，CHUNITHM 的命令与差异见 [CHUNITHM](chunithm.md)。

| 命令 | 说明 |
| --- | --- |
| `maimai b50 [<user>]` | 查询玩家 B50 |
| `maimai score <id_or_alias>` | 查询歌曲成绩 |
| `maimai bind df` / `maimai bind lx` | 绑定水鱼 / 落雪账号 |
| `maimai switch` | 切换成绩数据源（超级用户） |
| `chunithm b30 [<user>]` | 查询玩家 B30 |
| `maimai <ID>是什么歌` | 正则：按 ID 或别名查询歌曲 |

## 配置项

配置文件为 `config/module_maimai.toml`。

| 表 | 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `module_maimai` | `diving_fish_client_id` | str | 空 | 水鱼账号 OAuth 应用的 client_id |
| `module_maimai` | `lxns_client_id` | str | 空 | 落雪咖啡屋 OAuth 应用的 client_id |
| `module_maimai_secret` | `diving_fish_client_secret` | str | 空 | 水鱼账号 OAuth 应用的 client_secret，公开客户端可留空 |
| `module_maimai_secret` | `lxns_client_secret` | str | 空 | 落雪咖啡屋 OAuth 应用的 client_secret |
| `module_maimai_secret` | `lxns_developer_token` | str | 空 | 落雪咖啡屋查分器的开发者令牌 |

`module_maimai_secret` 为敏感表，字段值加密存储。未填写落雪 `lxns_client_id` 时落雪数据源不可用，CHUNITHM 默认回落到水鱼。开发者令牌用于按好友码查询任意玩家的成绩。

## 权限与平台能力

- `maimai switch`、`maimai update`、`chunithm update` 要求机器人超级用户，其余命令对普通用户开放。
- `maimai-regex` 声明为正则模块，启用该模块的平台需允许机器人读取全部消息。
- 声明支持语言：`maimai`、`chunithm` 为 `zh_cn`，`maimai-regex` 为 `zh_cn`、`zh_tw`。
- B50、B30、名牌板与进度图由 Pillow 生成，平台需支持图片消息；无图片能力时部分命令退化为文本列表。

## 数据表

| 表 | 用途 |
| --- | --- |
| `module_maimai_diving_prober_bind_info` | 水鱼绑定：用户名、refresh token、水鱼用户 ID |
| `module_maimai_lxns_prober_bind_info` | 落雪绑定：refresh token |

两表均以用户联合 ID 为主键，绑定数据随用户而非场景存储。`--purge-data` 依据 `manifest.toml` 的 `owned_tables` 清理这两张表。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`akari-bot-assets-fonts`、`Pillow`、`langconv`、`orjson`、`tortoise-orm`。
- 水鱼查分器：`https://www.diving-fish.com`，用于成绩、排行与曲绘。
- 落雪咖啡屋：`https://maimai.lxns.net`，用于成绩查询与 OAuth 授权。
- 别名数据：`https://www.yuzuchan.moe`。
- 包内 `assets/` 存放段位认定与宴会场资料，`migrations/` 存放绑定表迁移。
- 每日 0 点通过定时任务更新曲目别名。
