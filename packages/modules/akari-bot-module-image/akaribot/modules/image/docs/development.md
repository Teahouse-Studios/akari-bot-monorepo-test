---
title: 安装与开发
---

# image：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-image
```

模块名为 `image`，命令首词也是 `image`，没有别名。

## 配置项

<ModuleConfig />

## 权限与平台能力

模块声明 `required_superuser=True`，只有机器人的超级用户可以使用这些命令。模块没有声明平台限制，已接入的平台都能运行，但平台需要支持接收与发送图片。输入来自消息里的图片元素，输出是转换后的图片。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core` 与 `Pillow>=13.0.0,<13.1.0`。此模块不访问外部服务。
