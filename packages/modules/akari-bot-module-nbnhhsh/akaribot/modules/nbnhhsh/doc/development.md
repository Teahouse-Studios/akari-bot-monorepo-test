---
title: 安装与开发
---

# nbnhhsh：安装与开发

本页说明 `nbnhhsh` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-nbnhhsh
```

安装后在会话中由管理员用 `module enable nbnhhsh` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 模块声明支持语言为简体中文。
- 未声明平台限制，所有已接入平台可用。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`orjson`。
- 外部服务：`https://lab.magiconch.com/api/nbnhhsh/guess`，以 JSON 请求体提交待查询文本。
