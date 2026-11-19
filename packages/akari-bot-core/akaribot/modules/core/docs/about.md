---
order: 50
---

# about

此模块输出机器人的简介、版本、制作人员、权限配置链接与运行状态。别名 `version`、`ping`、`status` 指向对应子命令。

### `about`

<CommandUsage usage="about" permission="public" />

此命令输出机器人简介、仓库与反馈链接，以及制作人员入口。配图取自品牌资产，链接取自 `repo_url`、`issue_url`、`donate_url` 配置。平台支持按钮时，这些入口显示为按钮。

<ChatExample
  :log="[
    '用户：~about',
    '机器人：小可是由 Teahouse Studios 出品的多功能、跨平台、可自由扩展的聊天机器人助手，基于 AGPL-3.0 协议开源。',
    '请支持我们的工作以便持续开发与维护。',
    '开源存储库地址：https://github.com/Teahouse-Studios/akari-bot',
  ]"
/>

### `about version`

<CommandUsage usage="about version" permission="public" />

此命令输出机器人版本。从源码运行时附带对应的提交链接，发行版附带发行标签链接。版本号未知时给出提示。链接是否附带由 `enable_commit_url` 控制。

<ChatExample
  :log="[
    '用户：~about version',
    '机器人：当前机器人版本号：`1a2b3c4`',
    'https://github.com/Teahouse-Studios/akari-bot/commit/1a2b3c4',
  ]"
/>

### `about credits`

<CommandUsage usage="about credits" permission="public" />

此命令输出制作人员名单。品牌资产中缺少名单文件，或名单内容为空时，机器人提示不可用。

<ChatExample
  :log="[
    '用户：~about credits',
    '机器人：```开发人员名单',
    '……',
    '```',
  ]"
/>

### `about permissions`

<CommandUsage usage="about permissions [<qq_group_id>]" :params="['qq_group_id=QQ 群号，用于生成权限链接']" permission="public" platforms="QQBot" />

此命令仅在 QQBot 平台可用，用于生成群聊的权限配置链接。省略群号时返回带占位提示的命令补全入口。群号不是数字时返回提示。

<ChatExample
  :log="[
    '用户：~about permissions 123456789',
    '机器人：使用 Android 手机点击以下按钮可快速设置权限：',
  ]"
/>

### `about ping`

<CommandUsage usage="about ping" permission="public" />

此命令返回 Pong，以及运行时长、CPU、内存与磁盘占用。

<ChatExample
  :log="[
    '用户：~about ping',
    '机器人：Pong!',
    '机器人已运行：03:12:45',
    '处理器使用率：7.4%',
  ]"
/>

### `about status`

<CommandUsage usage="about status" permission="superuser" />

此命令输出系统与运行时详情，包含进程占用与 WebRender 状态。

<ChatExample
  :log="[
    '用户：~about status',
    '机器人：系统启动时间：2026-11-01 08:03:11 (UTC+8)',
    '机器人已运行：03:12:45',
    'Python 版本：3.12.7',
  ]"
/>
