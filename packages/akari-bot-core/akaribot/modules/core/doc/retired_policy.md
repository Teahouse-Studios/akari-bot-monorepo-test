---
order: 36
submenu: 钩子
---

# retired_policy

配合 `config.toml` 的 `retired_clients` 处理退役客户端：

- 退役客户端的消息只放行 `merge` 白名单命令，模块别名改写前实际输入的首词也参与判定。
- 同一消息通道存在未退役场景时，退役场景让出等待任务与命令认领。
- `retired_clients` 为空时策略不生效；非空的 `merge` 模块据此加载，见[merge](merge.md)。

配置格式为 `<源客户端> -> <目标客户端>`，仅填写源客户端表示不提供迁移。
