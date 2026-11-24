---
title: 安装与开发
---

# maimai：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-maimai
```

| 模块 | 命令首词 | 别名 | 说明 |
| --- | --- | --- | --- |
| `maimai` | `maimai` | `mai` | 舞萌 DX 查询 |
| `chunithm` | `chunithm` | `chu` | CHUNITHM 查询 |
| `maimai-regex` | 无 | `maimai_regex`、`mai_regex` | 以自然语言句式触发的正则表达式模块 |

## 配置项

<ModuleConfig table="module_maimai" />

| 表 | 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `module_maimai` | `diving_fish_client_id` | str | 空 | 水鱼账号 OAuth 应用的 client_id |
| `module_maimai` | `lxns_client_id` | str | 空 | 落雪咖啡屋 OAuth 应用的 client_id |
| `module_maimai_secret` | `diving_fish_client_secret` | str | 空 | 水鱼账号 OAuth 应用的 client_secret，公开客户端可以留空 |
| `module_maimai_secret` | `lxns_client_secret` | str | 空 | 落雪咖啡屋 OAuth 应用的 client_secret |
| `module_maimai_secret` | `lxns_developer_token` | str | 空 | 落雪咖啡屋查分器的开发者令牌 |

`module_maimai_secret` 为敏感配置表，字段值加密存储。未填写落雪的 `lxns_client_id` 时，落雪数据源不可用，CHUNITHM 的默认数据源为水鱼。开发者令牌用于按照好友码查询任意玩家的成绩。

## 权限与平台能力

`maimai switch`、`maimai update`、`chunithm update` 要求超级用户权限，其余命令对普通用户开放。`maimai-regex` 为正则表达式模块，启用该模块的平台需要允许机器人读取全部消息。

支持语言按模块声明，其中 `maimai` 与 `chunithm` 为 `zh_cn`，`maimai-regex` 为 `zh_cn` 与 `zh_tw`。

B50、B30、名牌板与进度图由 Pillow 生成，平台需要支持图片消息。若目标平台不具备图片发送能力，部分命令改用文本列表返回。

## 数据表

<ModuleData tables="module_maimai_diving_prober_bind_info,module_maimai_lxns_prober_bind_info" :list="false" />

| 表 | 用途 |
| --- | --- |
| `module_maimai_diving_prober_bind_info` | 水鱼绑定信息（用户名、refresh token、水鱼用户 ID） |
| `module_maimai_lxns_prober_bind_info` | 落雪绑定信息（refresh token） |

两张数据表均以 union ID 为主键，绑定数据按用户保存，不区分会话场景。`--purge-data` 依据 `manifest.toml` 中的 `owned_tables` 清理这两张表。

## 依赖与外部服务

运行依赖 `akari-bot-core`、`akari-bot-assets-fonts`、`Pillow`、`langconv`、`orjson`、`tortoise-orm`。

水鱼查分器的服务地址为 `https://www.diving-fish.com`，用于获取成绩、排行与曲绘资源。落雪咖啡屋的服务地址为 `https://maimai.lxns.net`，用于成绩查询与 OAuth 授权。别名数据来源于 `https://www.yuzuchan.moe`。

包内 `assets/` 存放段位认定与宴会场资料，`migrations/` 存放绑定表的迁移。每日 0 点由定时任务更新曲目别名。
