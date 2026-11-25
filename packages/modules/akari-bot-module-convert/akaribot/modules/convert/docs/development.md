---
title: 安装与开发
---

# convert：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-convert
```

安装后，管理员需要在会话中执行 `module enable convert` 启用模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块无平台限制与权限要求，不发起网络请求。`UnitRegistry` 使用 `Decimal` 作为数值类型，避免二进制浮点运算的误差。

模块声明支持的语言为 `en_us`。启用模块时，若会话语言未包含在支持列表中，回复中会附带提示，说明当前语言不受支持。

## 数据表

<ModuleData />

## 依赖与外部服务

仅依赖 `pint` 与 `akari-bot-core`，不使用外部服务。
