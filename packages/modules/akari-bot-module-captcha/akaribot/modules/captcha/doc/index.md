# 入群验证码

新成员加入 QQ 群时先行禁言，并发送含 15 个选项的按钮消息要求完成验证；验证通过后解除禁言，
答错则保持禁言并交由管理员处理。本包含两个模块：`captcha` 处理入群与退群事件，`token` 提供验证命令。

## 安装

```bash
akaribot module add akari-bot-module-captcha
```

安装后在群聊中由管理员用 `module enable captcha` 开启。`token` 为基础模块，随安装始终启用。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `token <token> [<answer>]` | 提交验证令牌；点击入群消息的按钮时自动附带所选答案 | 所有用户 |

`token` 仅注册在 `QQBot` 平台，设为基础命令与隐藏命令：不在帮助列表中显示，也不能被关闭。
验证码仅限被禁言的成员本人使用，令牌不存在、已使用或不属于发送者时分别返回对应提示。

## 事件流程

| 事件 | 行为 |
| --- | --- |
| `member_joined` | 已存在信任记录则跳过；否则创建或复用挑战记录，禁言 30 天并发送按钮消息 |
| `member_left` | 删除该成员在当前场景下的挑战与信任记录 |

题目默认为 1 至 100 的随机数字，按钮列出包含答案的 15 个不重复数字，每行 3 个。表情模式下
机器人先发送一张「手持物品」的表情图，按钮为 15 个表情名称。表情素材少于 15 张时回落到数字题目。

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
