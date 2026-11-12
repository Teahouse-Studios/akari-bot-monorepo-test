---
title: 安装与开发
---

# convert：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-convert
```

安装后在会话中由管理员用 `module enable convert` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

无平台限制，无权限要求，不涉及网络请求。`UnitRegistry` 使用 `Decimal` 作为数值类型，避免二进制浮点误差。声明支持语言 `en_us`：启用模块时若会话语言不在该列表中，会附加不受支持语言的提示。

## 数据表

<ModuleData />

## 依赖与外部服务

仅依赖 `pint` 与 `akari-bot-core`，不使用外部服务。
