---
title: 安装与开发
---

# ncmusic：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-ncmusic
```

安装后在会话中由管理员用 `module enable ncmusic` 开启。

## 配置项

<ModuleConfig table="module_ncmusic" />

`ncmusic_api` 声明为敏感项，写入同一文件的 `module_ncmusic_secret` 表。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ncmusic_enable_card` | bool | false | 是否在 QQ 客户端发送音乐卡片 |
| `ncmusic_api`（`module_ncmusic_secret`） | str | 空 | 网易云音乐 API 服务地址 |

`ncmusic_api` 为空时所有需要访问接口的命令返回配置缺失错误。搜索请求访问 `<ncmusic_api>/search?keywords=<keyword>`，详情请求访问 `<ncmusic_api>/song/detail?ids=<sid>`。`manifest.toml` 将 `ncmusic_api` 登记为重复凭据检查字段。

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块声明支持语言为简体中文。按 ID 获取音乐的命令仅对 QQ 群聊与 QQ 私聊开放，其他平台仍可使用搜索与详情命令；卡片消息仅在 QQ 且开启 `ncmusic_enable_card` 时发送，形式为 `[CQ:music,type=163,id=<sid>]`。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `akari-bot-core`。外部服务为由 `ncmusic_api` 指定的网易云音乐 API 服务。
