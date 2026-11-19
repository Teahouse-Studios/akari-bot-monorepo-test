---
order: 40
---

# bind

此模块把不同平台上的同一用户、同一现实场景归入同一个 union（用户组或场景组）。别名 `whoami`、`merge`、`merge token` 指向对应子命令。

### `bind`

<CommandUsage usage="bind" permission="public" />

此命令查看当前用户与当前场景各自所属的 union，以及其中已绑定的平台账号。

<ChatExample
  :log="[
    '用户：~bind',
    '机器人：当前用户所属的用户组：`USID|7C4F0B2E9A1D4E6B8C3A5F7D1E9B2C4A`',
    '已绑定 1 个用户：',
    '`QQ|Group|123456789`',
  ]"
/>

### `bind whoami`

<CommandUsage usage="bind whoami" permission="public" />

此命令显示发送者的平台 ID、union ID 与权限身份，同时列出当前场景的平台 ID 与 union ID。场景管理员、平台原生管理员与超级用户身份分别标注。

<ChatExample
  :log="[
    '用户：~bind whoami',
    '机器人：你的 ID：`QQ|Group|123456789`',
    '本群聊的 ID：`QQ|Group|123456789`',
    '当前用户所属的用户组：`USID|7C4F0B2E9A1D4E6B8C3A5F7D1E9B2C4A`',
  ]"
/>

### `bind self`

<CommandUsage usage="bind self" permission="public" />

此命令列出当前用户绑定的全部账号。

<ChatExample
  :log="[
    '用户：~bind self',
    '机器人：当前用户所属的用户组：`USID|7C4F0B2E9A1D4E6B8C3A5F7D1E9B2C4A`',
    '已绑定 1 个用户：',
    '`QQ|Group|123456789`',
  ]"
/>

### `bind start`

<CommandUsage usage="bind start" permission="public" />

此命令生成绑定码。在群内执行需要场景管理员权限。私聊中生成的绑定码同时包含发送者与私聊场景，使用后两者一起绑定。在群内生成的绑定码只合并场景组。

<ChatExample
  :log="[
    '用户：~bind start',
    '机器人：绑定码已通过私信发送，请注意查收。（请注意给新的机器人开启必要的权限，如获取全部消息和主动消息权限）',
  ]"
/>

### `bind token`

<CommandUsage usage="bind token <code>" :params="['code=另一处生成的绑定码']" permission="public" />

此命令用绑定码完成绑定。在群内执行需要场景管理员权限。绑定码只能在同类场景中使用，跨类型使用会被拒绝。绑定码失效时会返回提示。

<ChatExample
  :log="[
    '用户：~bind token 7K3M9Q',
    '机器人：绑定成功，新的场景组：`UTID|3E8C1A5F7B9D2E4C6A8B0D2F4E6C8A1B`',
    '已绑定 2 个群聊：',
    '`QQ|Group|123456789`[消息通道 1]',
  ]"
/>

### `bind self remove`

<CommandUsage usage="bind self remove <user>" :params="['user=带平台前缀的用户完整 ID']" permission="public" />

此命令解绑当前用户的某个账号，执行前须确认。最后一个账号不可解绑。

<ChatExample
  :log="[
    '用户：~bind self remove QQ|Group|123456789',
    '机器人：即将把 `QQ|Group|123456789` 移出当前用户组，该用户将不再共享组内数据且无法自动恢复，是否继续？',
    '用户：是',
    '机器人：已将 `QQ|Group|123456789` 移出当前用户组。',
  ]"
/>

### `bind target`

<CommandUsage usage="bind target" permission="admin" />

此命令查看当前场景绑定的平台入口。

<ChatExample
  :log="[
    '用户：~bind target',
    '机器人：当前群聊所属的场景组：`UTID|3E8C1A5F7B9D2E4C6A8B0D2F4E6C8A1B`',
    '已绑定 2 个群聊：',
    '`QQ|Group|123456789`[消息通道 1]',
  ]"
/>

### `bind target remove`

<CommandUsage usage="bind target remove <target>" :params="['target=带平台前缀的场景完整 ID']" permission="admin" />

此命令解绑当前场景的某个平台入口，执行前须确认。最后一个入口不可解绑。

<ChatExample
  :log="[
    '用户：~bind target remove QQ|Group|987654321',
    '机器人：即将把 `QQ|Group|987654321` 移出当前场景组，该群聊将不再共享组内数据且无法自动恢复，是否继续？',
    '用户：是',
    '机器人：已将 `QQ|Group|987654321` 移出当前场景组。',
  ]"
/>

### `bind channel`

<CommandUsage usage="bind channel" permission="admin" />

此命令查看当前场景的消息通道号，以及共用该通道的其它场景的数量与编号。

<ChatExample
  :log="[
    '用户：~bind channel',
    '机器人：当前群聊的消息通道：1 号',
    '同通道的群聊共 1 个：',
    '`QQ|Group|123456789`',
  ]"
/>

### `bind channel set`

<CommandUsage usage="bind channel set <channel>" :params="['channel=消息通道号']" permission="admin" />

此命令设置当前场景的消息通道号。通道号相同的场景在命令执行与消息推送时会去重。

<ChatExample
  :log="[
    '用户：~bind channel set 2',
    '机器人：已将当前群聊的消息通道设为 2 号。同一号的群聊会被视为现实中的同一个群聊（例如一个群聊里同时有两个机器人），命令只由其中一个机器人执行，推送只发送一次。',
  ]"
/>

### `bind channel reset`

<CommandUsage usage="bind channel reset" permission="admin" />

此命令把当前场景的消息通道号重置为默认值。

<ChatExample
  :log="[
    '用户：~bind channel reset',
    '机器人：已让当前群聊脱离原有通道，现单独占用 3 号通道。',
  ]"
/>

### `bind auto`

<CommandUsage usage="bind auto" permission="admin" />

仅当 `enable_bind_auto` 开启时才注册此命令。此命令与同一场景内的其它机器人实例自动配对。配对完成后，两个实例合并场景组、统一消息通道号，并互相记录对方的账号，用来屏蔽对方的消息。

### `bind channel probe`

<CommandUsage usage="bind channel probe <token>" :params="['token=一次性握手口令']" permission="public" />

这是内部命令，不需要手动执行。它由 `bind auto` 自动发出，用于响应握手请求。口令只能使用一次，使用后失效。

### `bind channel confirm`

<CommandUsage usage="bind channel confirm <token>" :params="['token=一次性握手口令']" permission="public" />

这是内部命令，不需要手动执行。它由 `bind auto` 自动发出，用于结束握手。双方确认处于同一场景后，机器人把两个场景合并到同一条消息通道。

绑定码为 6 位大写字母与数字，有效期 300 秒，只保存在 Server 进程的内存中，重启即失效。场景数据中的 `command_prefix` 与 `command_alias` 随场景 union 一起迁移，绑定后由合并结果统一维护。
