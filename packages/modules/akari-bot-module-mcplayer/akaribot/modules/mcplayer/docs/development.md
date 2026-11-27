---
title: 安装与开发
---

# mcplayer：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-mcplayer
```

安装完成后，管理员需要在会话中执行 `module enable mcplayer` 命令以启用该模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块的命令未声明管理员或超级用户限制，普通用户可以直接执行。模块未声明平台限制，`available_for` 采用默认值 `*`。命令成功获取皮肤时将输出图片消息，因此目标平台需要支持发送图片。

## 数据表

<ModuleData />

披风图的缓存文件保存在 core 的缓存目录下，文件名为 `<uuid>_fixed.png`。

## 依赖与外部服务

运行依赖 <PackageDependencies package="akari-bot-module-mcplayer" />。外部服务为 `api.mojang.com` 与 `crafatar.com`。`api.mojang.com` 用于 UUID 查询（`user/profile`）与玩家名查询（`users/profiles/minecraft`），`crafatar.com` 提供渲染图、皮肤与披风资源。

结果中的 NameMC 链接指向 `namemc.com`，模块仅输出链接，不向该站点发送网络请求。
