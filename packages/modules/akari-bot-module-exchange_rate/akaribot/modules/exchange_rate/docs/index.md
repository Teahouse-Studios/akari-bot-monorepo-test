# exchange-rate

此模块可以按当日汇率换算货币金额，返回换算结果与换算时间。命令和正则都能触发换算。

## 命令

<ModuleAlias names="exchange_rate, exchangerate, exchange, excr" />

### `exchange-rate`

<CommandUsage usage="exchange-rate <base> <target>" :params="['base=金额与源货币代码，金额可省略', 'target=目标货币代码']" permission="public" />

此命令用于按当日汇率换算金额。

说明：

- `<base>` 为“金额 + 源货币代码”，`<target>` 为目标货币代码，例如 `100USD CNY`。
- 金额省略时按 1 计算。货币代码取 `base` 末尾 3 位，并转为大写。
- 金额非数字或小于等于 0 时，分别返回对应提示。
- 源货币或目标货币不受支持时，提示中会列出这些货币代码。

## 正则触发

直接发送“金额 货币 兑换 货币”形式的文本即可触发换算，例如 `100 usd 兑换 cny`。金额可以省略。兑换动词支持“兑”“换”“兌”“換”。源货币与目标货币相同时不处理。
