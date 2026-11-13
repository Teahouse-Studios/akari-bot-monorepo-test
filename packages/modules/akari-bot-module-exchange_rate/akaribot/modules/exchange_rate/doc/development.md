---
title: 安装与开发
---

# exchange-rate：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-exchange_rate
```

安装后，管理员需要在会话中执行 `module enable exchange-rate` 开启模块，并在配置中填写 API Key。

## 配置项

<ModuleConfig table="module_exchange_rate" />

`exchange_rate_api_key` 是此模块唯一的配置字段，声明为敏感项，写入同一配置文件中的 `module_exchange_rate_secret` 表。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `exchange_rate_api_key` | str | 空 | ExchangeRate-API 的 API Key |

未配置密钥时，命令会给出配置缺失提示。完整的字段清单见配置模板 `akaribot/modules/exchange_rate/config.py`。

## 权限与平台能力

此模块没有平台限制，也没有权限要求。

每次换算会请求两次接口。第一次请求获取支持的货币列表，用于校验货币代码。第二次请求获取换算结果。接口返回的结果不是 `success` 时，命令返回对应的错误提示。结果中的时间按会话时区格式化。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`。外部服务为 ExchangeRate-API（`v6.exchangerate-api.com`），提供货币列表与换算两个接口。
