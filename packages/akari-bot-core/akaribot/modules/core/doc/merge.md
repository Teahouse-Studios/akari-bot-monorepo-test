---
order: 41
---

# merge

隐藏模块，仅在 `retired_clients` 非空时加载。命令注册在 `bind` 上，模块本身只承载退役公告的正则触发器。

### `bind merge`

<CommandUsage usage="bind merge" permission="public" />

仅退役来源客户端注册。在旧客户端上生成迁移码。私聊中一并迁移发送者与私聊场景，群内执行要求场景管理员权限。

### `bind merge-token`

<CommandUsage usage="bind merge-token <code>" :params="['code=另一处生成的迁移码']" permission="public" />

仅目标客户端注册。在目标客户端兑换迁移码，合并用户与场景数据。迁移码与绑定码分开存放，互不消费。

迁移会改写模块表中以平台 ID 为主键的数据，并同步场景管理员、封禁列表与消息通道。`retired_clients` 的格式为 `<源客户端> -> <目标客户端>`，只写源客户端表示不提供迁移，此时不注册迁移命令，仅保留退役公告。
