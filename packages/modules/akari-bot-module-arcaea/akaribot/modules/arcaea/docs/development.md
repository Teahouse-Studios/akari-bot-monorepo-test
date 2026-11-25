---
title: 安装与开发
---

# arcaea：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-arcaea
```

安装后，管理员需要在会话中执行 `module enable arcaea` 启用模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

`download`、`random`、`rank` 三项命令通过 WebRender 请求官方接口，使用前需要启用 `webrender.enable`。`calc` 为纯本地计算，不依赖网络。曲绘从包内 `assets/jacket/<song_id>.jpg` 读取，文件缺失时命令仅发送文本。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `orjson` 与 `akari-bot-core`。外部服务为 `webapi.lowiro.com`，提供 APK 信息、曲目展示、免费与付费排行榜。模块通过 WebRender 读取该接口返回的原始响应。
