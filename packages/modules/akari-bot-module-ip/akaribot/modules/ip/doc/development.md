---
title: 安装与开发
---

# ip：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-ip
```

模块名与命令首词均为 `ip`，没有别名。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入的平台都可以使用。反向解析依赖运行环境的 DNS，失败时只给出警告，不影响其余字段。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`。归属地查询使用 `https://api.ip.sb/geoip/{ip}` 接口。反向解析调用 Python 标准库的 `socket.getnameinfo`，不访问其他服务。
