---
order: 41
---

# merge

此模块属于隐藏模块，仅在 `retired_clients` 非空时加载。命令注册在 `bind` 上，模块本身只保留退役公告的正则触发器。

### `bind merge`

<CommandUsage usage="bind merge" permission="public" />

此命令只在已退役的源客户端上注册，并在该客户端生成迁移码。在私聊中执行时，发送者和私聊场景的数据一并迁移。在群内执行时要求场景管理员权限。

### `bind merge-token`

<CommandUsage usage="bind merge-token <code>" :params="['code=另一处生成的迁移码']" permission="public" />

此命令仅在目标客户端注册，用迁移码合并用户和场景数据。迁移码和绑定码分开存放，使用其中一种不会消耗另一种。

迁移会改写模块表中以平台 ID 为主键的数据，并同步场景管理员、封禁列表和消息通道。

`retired_clients` 的格式为 `<源客户端> -> <目标客户端>`。只写源客户端表示不提供迁移，此时不注册迁移命令，只保留退役公告。
