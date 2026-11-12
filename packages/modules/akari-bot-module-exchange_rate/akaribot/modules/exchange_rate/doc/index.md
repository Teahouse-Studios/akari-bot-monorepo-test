# exchange-rate

按当日汇率换算货币金额，输出换算结果与换算时间。命令与正则两种方式都能触发。

## 命令

<ModuleAlias names="exchange_rate, exchangerate, exchange, excr" />

### `exchange-rate`

<CommandUsage usage="exchange-rate <base> <target>" :params="['base=金额与源货币代码，金额可省略', 'target=目标货币代码']" permission="public" />

按当日汇率换算金额。`<base>` 为“金额 + 源货币代码”，`<target>` 为目标货币代码，例如 `100USD CNY`；金额省略时按 1 计算，货币代码取 `base` 末尾 3 位并转为大写。金额非数字或小于等于 0 时分别返回对应提示；源货币与目标货币不在支持列表中时一并列出。

## 正则触发

形如“金额货币兑换货币”的消息会直接触发换算，例如 `100 usd 兑换 cny`。金额可省略，兑换动词支持“兑”“换”“兌”“換”。源货币与目标货币相同时不处理。
