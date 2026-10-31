---
title: 安装与开发
---

# exchange-rate：安装与开发

本页说明 `exchange-rate` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-exchange_rate
```

安装后在会话中由管理员用 `module enable exchange-rate` 开启，并在配置中填写 API Key。

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
