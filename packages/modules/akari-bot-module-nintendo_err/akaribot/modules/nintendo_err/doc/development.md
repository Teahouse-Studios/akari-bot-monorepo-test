---
title: 安装与开发
---

# nintendo-err：安装与开发

本页说明 `nintendo-err` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-nintendo_err
```

安装后在会话中由管理员用 `module enable nintendo-err` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 结果以嵌入卡片发出，字段名与说明文本按收录数据原样展示。

## 数据表

无。manifest 未声明 `owned_tables`，报错码表随包内 Python 模块分发，查询结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`py-cord`。
- 不使用外部网络服务；报错码数据来自包内 `ctr_support.py`、`ctr_results.py`、`wiiu_support.py`、`wiiu_results.py` 与 `switch.py`。
