---
title: 安装与开发
---

# exchange-rate：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-exchange_rate
```

安装完成后，管理员需要在会话中执行 `module enable exchange-rate` 启用模块，并在配置中填写 API Key。

## 配置项

<ModuleConfig table="module_exchange_rate" />

`exchange_rate_api_key` 为此模块唯一的配置字段，声明为敏感配置项，写入配置文件中的 `module_exchange_rate_secret` 表。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `exchange_rate_api_key` | str | 空 | ExchangeRate-API 的 API Key |

未配置密钥时，命令将返回配置缺失提示。完整字段清单参见配置模板 `akaribot/modules/exchange_rate/config.py`。

## 权限与平台能力

此模块无平台限制，也无特殊权限要求。

每次换算均发起两次接口请求。首次请求获取受支持的货币列表以校验货币代码，第二次请求获取最终换算结果。

若接口返回的状态不为 `success`，命令将返回对应的错误提示。换算结果中的时间统一按照会话时区格式化展示。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`。外部服务为 ExchangeRate-API（`v6.exchangerate-api.com`），提供货币列表与换算两个接口。
