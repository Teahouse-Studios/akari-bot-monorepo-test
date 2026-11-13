---
title: 安装与开发
---

# nintendo-err：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-nintendo_err
```

安装后，管理员在会话中执行 `module enable nintendo-err` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此命令对普通用户开放，不要求管理员或超级用户权限。模块没有声明平台限制，所有已接入的平台均可使用。结果以嵌入卡片返回，字段名与说明文本按收录数据原样展示。

## 数据表

<ModuleData />

报错码表随包内的 Python 模块分发。

## 依赖与外部服务

依赖 `akari-bot-core` 与 `py-cord`，不使用外部网络服务。报错码数据来自包内的 `ctr_support.py`、`ctr_results.py`、`wiiu_support.py`、`wiiu_results.py` 与 `switch.py`。
