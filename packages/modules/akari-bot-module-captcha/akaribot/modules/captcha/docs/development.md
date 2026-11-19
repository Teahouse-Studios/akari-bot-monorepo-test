---
title: 安装与开发
---

# captcha：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-captcha
```

安装后，管理员需要在群聊中执行 `module enable captcha`。`token` 是基础模块，安装后始终启用。

## 配置项

<ModuleConfig />

是否使用表情题目，由 core 的 `use_emote` 与会话数据的 `use_emote` 共同决定。会话没有设置这一项时，按开启处理。

## 权限与平台能力

`captcha` 是事件模块，只在 `QQBot` 群聊中生效，并要求平台可以读取全部消息。机器人需要具备 `can_send_messages`、`can_send_proactive_messages`、`can_manage_members`、`can_restrict_members` 四项平台权限。

禁言、发消息等平台操作在 Union 变更锁之外执行。解禁失败时保留 `failed` 状态，便于管理员清理。发送验证消息失败时，机器人立即尝试解禁，解禁成功后把挑战标记为 `error`。

## 数据表

<ModuleData tables="module_captcha_challenge,module_captcha_trust" :list="false" />

| 表 | 内容 |
| --- | --- |
| `module_captcha_challenge` | 挑战记录：令牌、答案、选项、状态（`preparing`、`pending`、`failed`、`verified`、`error`）、平台 ID 与 Union ID |
| `module_captcha_trust` | 已通过验证的成员与场景组合，按两个 Union ID 唯一 |

`preparing`、`pending`、`failed` 视为活跃状态。存在活跃挑战时，场景或用户解绑会被拒绝。

## 依赖与外部服务

依赖 `akari-bot-assets-emotes`（`captcha_held` 表情素材）、`tortoise-orm`、`akari-bot-core`。不使用外部网络服务。
