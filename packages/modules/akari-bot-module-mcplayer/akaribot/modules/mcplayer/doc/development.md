---
title: 安装与开发
---

# mcplayer：安装与开发

本文将会介绍此模块的安装、配置、数据表与运行依赖。

## 安装

```bash
akaribot module add akari-bot-module-mcplayer
```

安装完成后，管理员需要在会话中执行 `module enable mcplayer` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块的命令未声明管理员或超级用户限制，普通用户可以直接执行。模块没有声明平台限制，`available_for` 取默认值 `*`。命令成功获取皮肤时会输出图片消息，因此平台需要支持发送图片。

## 数据表

<ModuleData />

披风图的缓存文件放在 core 的缓存目录下，文件名为 `<uuid>_fixed.png`。

## 依赖与外部服务

运行依赖 `akari-bot-core`、`Pillow>=13.0.0,<13.1.0` 与 `orjson>=3.10.9,<4.0.0`。外部服务为 `api.mojang.com` 与 `crafatar.com`。`api.mojang.com` 负责 UUID 查询（`user/profile`）与玩家名查询（`users/profiles/minecraft`），`crafatar.com` 提供渲染图、皮肤与披风。

结果中的 NameMC 链接指向 `namemc.com`，模块只输出链接，不请求该站。
