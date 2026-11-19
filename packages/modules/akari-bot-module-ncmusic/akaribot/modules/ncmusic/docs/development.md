---
title: 安装与开发
---

# ncmusic：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-ncmusic
```

安装后，管理员需要在会话中执行 `module enable ncmusic` 开启模块。

## 配置项

<ModuleConfig table="module_ncmusic" />

`ncmusic_api` 声明为敏感项，实际写入同一文件的 `module_ncmusic_secret` 表。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ncmusic_enable_card` | bool | false | 是否在 QQ 客户端发送音乐卡片 |
| `ncmusic_api`（`module_ncmusic_secret`） | str | 空 | 网易云音乐 API 服务地址 |

`ncmusic_api` 为空时，所有需要访问接口的命令都会返回配置缺失错误。搜索请求访问 `<ncmusic_api>/search?keywords=<keyword>`，详情请求访问 `<ncmusic_api>/song/detail?ids=<sid>`。`manifest.toml` 把 `ncmusic_api` 列为重复登录信息检查字段。

## 权限与平台能力

此模块的命令对普通用户开放，不要求管理员或超级用户权限。模块声明的支持语言为简体中文。

按 ID 获取音乐的命令只对 QQ 群聊与 QQ 私聊开放，其他平台仍可使用搜索与详情命令。卡片消息只在 QQ 上发送，且要求开启 `ncmusic_enable_card`，形式为 `[CQ:music,type=163,id=<sid>]`。

## 数据表

<ModuleData />

## 依赖与外部服务

此模块依赖 `akari-bot-core`。外部服务是 `ncmusic_api` 指定的网易云音乐 API 服务。
