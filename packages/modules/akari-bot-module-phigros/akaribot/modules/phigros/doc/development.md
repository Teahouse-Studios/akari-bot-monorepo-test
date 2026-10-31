---
title: 安装与开发
---

# phigros：安装与开发

本页说明 `phigros` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-phigros
```

安装后在会话中由管理员用 `module enable phigros` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- `update` 仅超级用户可执行。
- `login` 仅限私聊；`bind` 在 Discord 频道、KOOK 群组、Matrix 房间、QQ 群聊、QQBot 群聊与频道、Telegram 群组与超级群组中会先告警并撤回消息。
- `login` 在平台支持图片时展示二维码，否则给出授权链接；`b30` 生成图片，`song` 与 `random` 在曲绘存在时附带曲绘。
- 曲绘渲染依赖 `akari-bot-assets-fonts` 提供的字体资源。

## 数据表

manifest 声明 `owned_tables = ["module_phigros_bind_info"]`，表结构位于 `database/models.py`。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `union_id` | 字符串，主键 | 用户联合 ID |
| `session_token` | 字符串 | 云存档会话令牌 |
| `username` | 字符串 | 玩家昵称 |
| `is_international` | 布尔 | 是否为国际服账号，默认 false |

包内 `migrations/0002_union_id.py` 负责将绑定表主键列改为 `union_id` 并补齐 `is_international` 字段。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`akari-bot-assets-fonts`、`pycryptodome`、`Pillow`、`httpx`、`orjson`、`qrcode`、`tortoise-orm`。
- 云存档：国服 `https://rak3ffdi.cloud.tds1.tapapis.cn`，国际服 `https://kviehlel.cloud.ap-sg.tapapis.com`。
- TapTap 登录：`https://accounts.tapapis.cn` 与 `https://open.tapapis.cn`。
- 曲目资源：`https://raw.githubusercontent.com/7aGiven/Phigros_Resource` 的 `info` 分支。
