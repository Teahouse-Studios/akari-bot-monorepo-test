# cytoid

查询 Cytoid 玩家资料，生成 B30（最佳 30 首）与 R10（最近 10 首）成绩图，并按发送者保存账号绑定。

模块名 `cytoid`，别名 `ctd`。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `cytoid profile [<username>]` | 查询用户资料，输出头像与经验、等级、Rating、评级分布 | 所有用户 |
| `cytoid b30 [<username>]` | 生成 B30 成绩图 | 所有用户 |
| `cytoid r10 [<username>]` | 生成 R10 成绩图 | 所有用户 |
| `cytoid bind <username>` | 绑定 Cytoid 用户名 | 所有用户 |
| `cytoid unbind` | 解除绑定 | 所有用户 |

省略用户名时使用发送者的绑定账号；未绑定时提示先执行 `cytoid bind`。绑定按发送者 Union 保存，
同一用户在任意会话中都可使用。用户不存在时返回未找到提示，取数失败时返回获取失败提示。
