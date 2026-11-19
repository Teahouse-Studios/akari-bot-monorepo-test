# twenty-four

此模块是二十四点游戏。机器人随机给出四个 1 到 13 的整数，你需要用加、减、乘、除与括号使结果为 24。机器人也能判断一组数字是否无解，或列出全部解。

## 命令

<ModuleAlias names="twenty_four, twentyfour, 24" />

### `twenty-four`

<CommandUsage usage="twenty-four" permission="public" />

此命令用于开始新游戏，机器人会随机给出四个 1 到 13 的整数。当前会话存在进行中的对局时，命令会提示已有对局尚未结束。

<ChatExample
  :log="[
    '用户：~twenty-four',
    '机器人：给出的数字组合：(3, 8, 3, 1)',
    '用户：3*(8+1)-3',
    '机器人：回答正确。',
  ]"
/>

### `twenty-four stop`

<CommandUsage usage="twenty-four stop" permission="public" />

此命令用于结束当前对局。没有进行中的对局时，命令会返回停止失败的提示。

<ChatExample
  :log="[
    '用户：~twenty-four stop',
    '机器人：已停止。',
  ]"
/>

### `twenty-four solve`

<CommandUsage usage="twenty-four solve <num1> <num2> <num3> <num4>" :params="['num1=第一个数，取值 1 到 13', 'num2=第二个数，取值 1 到 13', 'num3=第三个数，取值 1 到 13', 'num4=第四个数，取值 1 到 13']" permission="public" />

此命令用于列出四个数字的全部解。四个数字都必须在 1 到 13 之间。当前会话存在进行中的对局时，命令拒绝执行。

非超级用户执行时需要支付 4 花瓣。实例未开启花瓣系统时，不扣除花瓣。余额不足时，命令终止执行。存在解时，命令逐条列出。不存在解时，命令返回无解的提示。

<ChatExample
  :log="[
    '用户：~twenty-four solve 1 5 5 5',
    '机器人：数字组合 (1, 5, 5, 5) 的所有解为：',
    '5*(5-1/5)',
  ]"
/>

## 游戏规则

- 四个数字都必须且只能使用一次，只允许四则运算与括号。
- 提交表达式后，按结果是否为 24 判定。表达式不合法时返回无效的提示。
- 组合无解时可回答“无解”“無解”“none”“n/a”“na”“n.a.”之一。
- 回答无解且组合确实无解时，奖励 1 花瓣。回答无解但组合存在解时，扣除 1 花瓣，并给出其中一组解。回答正确时奖励 1 花瓣。
- 花瓣的增减仅在实例开启花瓣系统时生效。

对局状态按会话隔离，1 小时后过期。机器人服务重启后，对局会中断。
