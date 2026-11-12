# dice

按表达式投掷骰子，支持标准骰、奖励与惩罚骰、World of Darkness 与 Double Cross 骰池、Fudge 骰，并可按 DC 判定成功或失败。

## 命令

<ModuleAlias names="rd, roll" />

### `dice`

<CommandUsage :usage="['dice', 'dice <dices> [<dc>]']" :params="['dices=骰子投掷表达式', 'dc=判定成功的目标值']" permission="public" />

投掷骰子。不带参数时按会话默认骰子投掷一枚，须先用 `dice set` 设置面数；带 `<dices>` 时按表达式投掷，`<dc>` 为可选的判定值。表达式支持以下写法：

- `XdY` 投 X 枚 Y 面骰；`D%` 等同 `D100`；`XdYKn` 取最高的 n 枚，`XdYQn` 去掉最低的 n 枚。
- `n#表达式` 重复投掷 n 次，n 超出上限时返回范围错误。
- `nAmK/Q/M` 为 World of Darkness 骰池，`nCm` 为 Double Cross 骰池。
- `B` 与 `P` 分别生成奖励骰与惩罚骰，以 D100 的个位为十位基准取高或取低。
- `F` 与 `nDF` 为 Fudge 骰，结果取 `-`、`0`、`+`。
- 支持加减乘除、括号与 `abs`、`sqrt`、`floor`、`factorial` 等数学函数。

完整语法、示例与输出标记见[表达式详解](expressions.md)。

多次投掷且带 DC 时，末尾汇总成功与失败次数。详细投掷明细在总量较小时展示，总量较大时只显示汇总结果。

### `dice set`

<CommandUsage usage="dice set <sides>" :params="['sides=会话默认骰子的面数']" permission="admin" />

设置当前会话的默认骰子面数。面数大于 1 时保存为会话默认值，`0` 表示清除默认值，其余取值返回无效提示；设置只对当前会话生效。

### `dice rule`

<CommandUsage usage="dice rule" permission="admin" />

切换当前会话的 DC 判定方向。默认按“结果不小于 DC 为成功”判定，切换后改为“结果不大于 DC 为成功”。
