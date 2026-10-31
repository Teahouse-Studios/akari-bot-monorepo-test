---
title: 安装与开发
---

# mkey：安装与开发

本页说明 `mkey` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-mkey
```

安装后在会话中由管理员用 `module enable mkey` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 命令未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 计算完全在本地完成，不依赖网络或平台能力。

## 数据表

无。manifest 未声明 `owned_tables`，计算过程不读写数据库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`pycryptodome>=3.18.0,<5.0.0`。
- 不访问外部服务。密钥数据位于包内 `assets/data`，manifest 声明 `assets = "assets"`。
