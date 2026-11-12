---
title: 安装与开发
---

# arcaea：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-arcaea
```

安装后在会话中由管理员用 `module enable arcaea` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

`download`、`random`、`rank` 通过 WebRender 请求官方接口，需开启 `webrender.enable`。`calc` 为纯本地计算，不依赖网络。曲绘从包内 `assets/jacket/<song_id>.jpg` 读取，文件缺失时降级为纯文本。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `orjson`、`akari-bot-core`。外部服务 `webapi.lowiro.com`（APK 信息、曲目展示、免费与付费排行），经 WebRender 读取原始响应。
