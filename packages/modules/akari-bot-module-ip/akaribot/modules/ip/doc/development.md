---
title: 安装与开发
---

# ip：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-ip
```

模块名为 `ip`，命令首词为 `ip`，没有别名。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。未声明平台限制，所有已接入平台可用。反向解析依赖运行环境的 DNS，解析失败只记录警告，不影响其余字段。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`。归属地接口：`https://api.ip.sb/geoip/{ip}`。反向解析：使用系统 `socket.getnameinfo`，不访问额外服务。
