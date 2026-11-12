---
title: 安装与开发
---

# whois：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-whois
```

安装后在会话中由管理员用 `module enable whois` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入平台可用。查询结果为文本，字段数量取决于注册局实际返回的数据。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `akari-bot-core` 与 `python-whois`。外部服务为由 `python-whois` 按域名后缀连接的各级 WHOIS 服务器。日期字段在应答返回列表时取第一项，按 UTC 解释后转换为会话时区。
