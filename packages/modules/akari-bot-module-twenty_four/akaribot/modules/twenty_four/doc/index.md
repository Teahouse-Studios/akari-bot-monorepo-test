# twenty-four

随机给出四个 1 到 13 的整数，要求用加、减、乘、除与括号使结果为 24。也可先判断组合是否无解，或直接查询全部解。

## 命令

<ModuleAlias names="twenty_four, twentyfour, 24" />

### `twenty-four`

<CommandUsage usage="twenty-four" permission="public" />

开始新游戏，随机给出四个 1 到 13 的整数。存在进行中的对局时返回对局进行中提示。

### `twenty-four stop`

<CommandUsage usage="twenty-four stop" permission="public" />

结束当前对局；没有进行中的对局时返回停止失败提示。

### `twenty-four solve`

<CommandUsage usage="twenty-four solve <num1> <num2> <num3> <num4>" :params="['num1=第一个数，取值 1 到 13', 'num2=第二个数，取值 1 到 13', 'num3=第三个数，取值 1 到 13', 'num4=第四个数，取值 1 到 13']" permission="public" />

列出四个数字的全部解。四个数字均须在 1 到 13 之间，存在进行中的对局时拒绝执行。非超级用户需支付 4 花瓣，实例未开启花瓣系统时不扣除，余额不足时终止；存在解时逐条列出，不存在解时返回无解提示。

## 游戏规则

- 每个数字必须且只能使用一次，只允许四则运算与括号。
- 回答表达式后按结果是否为 24 判定；表达式不合法时返回无效提示。
- 组合无解时可回答“无解”“無解”“none”“n/a”“na”“n.a.”之一。
- 判定无解且确实无解时奖励 1 花瓣；判定无解但存在解时扣除 1 花瓣并给出其中一组解；回答正确时奖励 1 花瓣。
- 花瓣增减仅在实例开启花瓣系统时生效。

对局状态按会话隔离，1 小时后过期；机器人服务重启后对局中断。
