---
title: 安装与开发
---

# twenty-four：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-twenty_four
```

安装后，管理员需要在会话中执行 `module enable twenty-four` 启用模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入的平台都可以使用。

## 数据表

<ModuleData />

对局状态保存在进程内。

## 依赖与外部服务

依赖 `akari-bot-core` 与 `simpleeval`。模块不使用外部网络服务。
