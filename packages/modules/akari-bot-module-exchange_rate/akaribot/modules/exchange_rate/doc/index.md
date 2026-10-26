# 汇率转换

调用 ExchangeRate-API 换算货币金额，输出换算结果与换算时间。命令与正则两种方式都能触发。

模块名 `exchange-rate`，别名 `exchange_rate`、`exchangerate`、`exchange`、`excr`；模块包含正则命令。

## 安装

```bash
akaribot module add akari-bot-module-exchange_rate
```

安装后在会话中由管理员用 `module enable exchange-rate` 开启，并在配置中填写 API Key。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `exchange-rate <base> <target>` | 按当日汇率换算金额 | 所有用户 |

`<base>` 为「金额 + 源货币代码」，`<target>` 为目标货币代码，例如 `100USD CNY`。金额省略时按 1
计算，货币代码取 `base` 末尾 3 位并转为大写。金额非数字或小于等于 0 时分别返回对应提示；源货币
与目标货币不在支持列表中时一并列出。

## 正则触发

形如「金额 货币 兑换 货币」的消息会直接触发换算，例如 `100 usd 兑换 cny`。金额可省略，兑换
动词支持「兑」「换」「兌」「換」。源货币与目标货币相同时不处理。

## 配置

密钥表 `module_exchange_rate_secret`（`config/module_exchange_rate.toml`）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `exchange_rate_api_key` | str | 空 | ExchangeRate-API 的 API Key |

未配置密钥时命令抛出配置缺失提示。完整清单见配置模板 `akaribot/modules/exchange_rate/config.py`。

## 权限与平台能力

- 无平台限制，无权限要求。
- 每次换算请求两次接口：先取支持货币列表校验代码，再取换算结果；接口返回非 `success` 时
  返回对应错误提示。
- 结果中的时间按会话时区格式化。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：仅 `akari-bot-core`。
- 外部服务：ExchangeRate-API（`v6.exchangerate-api.com`）的货币列表与换算接口。
