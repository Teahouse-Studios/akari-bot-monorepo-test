---
title: 安装与开发
---

# ip：安装与开发

本页说明 `ip` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-ip
```

模块名为 `ip`，命令前缀为 `ip`，没有别名。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 在 KOOK、QQ、QQBot 平台上，归属地为 Hong Kong、Macao、Taiwan 时统一显示为 China；其他平台按接口原值显示。
- 反向解析依赖运行环境的 DNS，解析失败只记录警告，不影响其余字段。

## 数据表

无。查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`。
- 归属地接口：`https://api.ip.sb/geoip/{ip}`。
- 反向解析：使用系统 `socket.getnameinfo`，不访问额外服务。
