# mojang-status

此模块用于查询玩家信息、正版验证与 Mojang 服务三项的在线情况。

## 命令

<ModuleAlias names="mojang_status, mcstatus, mjs, mjsb" />

### `mojang-status`

<CommandUsage usage="mojang-status" permission="public" />

此命令按固定顺序输出三项的在线情况：

- 玩家信息
- 正版验证
- Mojang 服务

三项的状态取值为在线、离线或未知。

<ChatExample
  :log="[
    '用户：~mojang-status',
    '机器人：玩家信息：在线',
    '正版验证：在线',
    'Mojang 服务：在线',
  ]"
/>
