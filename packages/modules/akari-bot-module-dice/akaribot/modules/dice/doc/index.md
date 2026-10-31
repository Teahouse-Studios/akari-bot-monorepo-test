# dice

按表达式投掷骰子，支持标准骰、奖励与惩罚骰、World of Darkness 与 Double Cross 骰池、Fudge 骰，
并可按 DC 判定成功或失败。

模块名 `dice`，别名 `rd`、`roll`。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `dice` | 按会话默认骰子投掷一枚，须先用 `dice set` 设置面数 | 所有用户 |
| `dice <dices> [<dc>]` | 按表达式投骰，可附带 DC 判定 | 所有用户 |
| `dice set <sides>` | 设置当前会话的默认骰子面数，`0` 表示清除 | 会话管理员 |
| `dice rule` | 切换 DC 判定方向 | 会话管理员 |

表达式支持以下写法：

- `XdY` 投 X 枚 Y 面骰；`D%` 等同 `D100`；`XdYKn` 取最高的 n 枚，`XdYQn` 去掉最低的 n 枚。
- `n#表达式` 重复投掷 n 次，n 的上限由 `dice_roll_limit` 决定。
- `nAmK/Q/M` 为 World of Darkness 骰池，`nCm` 为 Double Cross 骰池。
- `B` 与 `P` 分别生成奖励骰与惩罚骰，以 D100 的个位为十位基准取高或取低。
- `F` 与 `nDF` 为 Fudge 骰，结果取 `-`、`0`、`+`。
- 支持加减乘除、括号与 `abs`、`sqrt`、`floor`、`factorial` 等数学函数，由 simpleeval 求值。

完整语法、示例与输出标记见[表达式详解](expressions.md)。

DC 默认按「结果不小于 DC 为成功」判定，`dice rule` 切换后改为「结果不大于 DC 为成功」。多次投掷
且带 DC 时，末尾汇总成功与失败次数。详细投掷明细在总量较小时展示，总量超过 `dice_detail_count`
时只显示结果。
