---
title: 安装与开发
---

# phigros：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-phigros
```

安装后在会话中由管理员用 `module enable phigros` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

`update` 仅超级用户授权使用。`login` 仅限私聊；`bind` 在 Discord 频道、KOOK 群组、Matrix 房间、QQ 群聊、QQBot 群聊与频道、Telegram 群组与超级群组中会先告警并撤回消息。`login` 在平台支持图片时展示二维码，否则给出授权链接；`b30` 生成图片，`song` 与 `random` 在曲绘存在时附带曲绘。曲绘渲染依赖 `akari-bot-assets-fonts` 提供的字体资源。

## 数据表

<ModuleData tables="module_phigros_bind_info" />

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `union_id` | 字符串，主键 | 用户联合 ID |
| `session_token` | 字符串 | 云存档会话令牌 |
| `username` | 字符串 | 玩家昵称 |
| `is_international` | 布尔 | 是否为国际服账号，默认 false |

包内 `migrations/0002_union_id.py` 将绑定表主键列重命名为 `union_id`，并补齐 `is_international` 字段。

曲目资源存放在模块的包数据目录：`song_info.json` 为曲目信息，`illustration/` 为曲绘目录，`resource_version.txt` 记录已下载的资源版本。定时任务每小时检查一次资源版本，自动更新失败只记录警告，等待下一轮重试。

## 依赖与外部服务

依赖 `akari-bot-core`、`akari-bot-assets-fonts`、`pycryptodome`、`Pillow`、`httpx`、`orjson`、`qrcode` 与 `tortoise-orm`。云存档使用国服 `https://rak3ffdi.cloud.tds1.tapapis.cn` 与国际服 `https://kviehlel.cloud.ap-sg.tapapis.com`，TapTap 登录使用 `https://accounts.tapapis.cn` 与 `https://open.tapapis.cn`，曲目资源来自 `https://raw.githubusercontent.com/7aGiven/Phigros_Resource` 的 `info` 分支。
