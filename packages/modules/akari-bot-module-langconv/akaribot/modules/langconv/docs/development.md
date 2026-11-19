---
title: 安装与开发
---

# langconv：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-langconv
```

模块名为 `langconv`，命令首词为 `langconv`，别名为 `lc`。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块没有声明平台限制，所有已接入的平台都可以使用。

模块没有声明支持的语言，转换目标由命令参数决定，与会话语言无关。三个转换器在首次使用时加载，之后在进程内复用。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core` 与 `langconv==0.4.0`。转换在进程内完成，不访问外部服务。
