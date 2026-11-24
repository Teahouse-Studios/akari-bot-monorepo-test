# exchange-rate

此模块可以按照当日汇率换算货币金额，返回换算结果与换算时间。命令与正则表达式均支持触发换算。

## 命令

<ModuleAlias names="exchange_rate, exchangerate, exchange, excr" />

### `exchange-rate`

<CommandUsage usage="exchange-rate <base> <target>" :params="['base=金额与源货币代码，金额可省略', 'target=目标货币代码']" permission="public" />

此命令用于按照当日汇率换算货币金额。

说明：

- `<base>` 为“金额 + 源货币代码”，`<target>` 为目标货币代码，例如 `100USD CNY`。
- 金额省略时按照 1 计算。货币代码截取 `base` 末尾 3 位并转换为大写。
- 若金额非数字或小于或等于 0，分别返回对应的错误提示。
- 若源货币或目标货币不受支持，提示信息中将列出对应的货币代码。

## 正则触发

直接发送“金额 货币 兑换 货币”格式的文本即可触发换算，例如 `100 usd 兑换 cny`。金额参数支持省略。兑换动词支持“兑”“换”“兌”“換”。若源货币与目标货币相同则不予处理。
