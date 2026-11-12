---
title: 安装与开发
---

# image：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-image
```

模块名为 `image`，命令首词为 `image`，没有别名。

## 配置项

<ModuleConfig />

## 权限与平台能力

模块声明 `required_superuser=True`，仅机器人超级用户可执行。未声明平台限制，所有已接入平台可用。平台需支持接收与发送图片：输入依赖消息中的图片元素，输出为转换后的图片。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`、`Pillow>=13.0.0,<13.1.0`。不访问外部服务。
