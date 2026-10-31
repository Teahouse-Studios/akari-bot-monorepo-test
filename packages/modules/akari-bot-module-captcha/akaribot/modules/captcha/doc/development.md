---
title: 安装与开发
---

# captcha：安装与开发

本页说明 `captcha` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-captcha
```

安装后在群聊中由管理员用 `module enable captcha` 开启。`token` 为基础模块，随安装始终启用。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。是否使用表情题目读取 core 的 `use_emote`
与会话数据 `use_emote`（会话未设置时按开启处理）。

## 权限与平台能力

- `captcha` 仅对 `QQBot` 群聊生效，事件模块要求平台可读取全部消息。
- 机器人需具备 `can_send_messages`、`can_send_proactive_messages`、`can_manage_members`、
  `can_restrict_members` 四项平台权限。
- 禁言、发消息等平台操作在 Union 变更锁之外执行；解禁失败时保留 `failed` 状态，便于管理员清理。
- 发送验证消息失败时立即尝试解禁，成功后把挑战标记为 `error`。

## 数据表

manifest 声明的 `owned_tables`：

| 表 | 内容 |
| --- | --- |
| `module_captcha_challenge` | 挑战记录：令牌、答案、选项、状态（`preparing`、`pending`、`failed`、`verified`、`error`）、平台 ID 与 Union ID |
| `module_captcha_trust` | 已通过验证的成员与场景组合，按两个 Union ID 唯一 |

`preparing`、`pending`、`failed` 视为活跃状态，存在活跃挑战的场景或用户解绑会被拒绝。

## 依赖与外部服务

- 依赖：`akari-bot-assets-emotes`（`captcha_held` 表情素材）、`tortoise-orm`、`akari-bot-core`。
- 不使用外部网络服务。
