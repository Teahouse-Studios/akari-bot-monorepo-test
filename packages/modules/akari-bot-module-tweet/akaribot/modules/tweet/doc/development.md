---
title: 安装与开发
---

# tweet：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-tweet
```

安装后在会话中由管理员用 `module enable tweet` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令与正则匹配对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入平台可用。摘要图依赖实例启用 WebRender，未启用时无法生成截图；图片发送能力由平台决定，不支持图片的平台无法展示摘要图。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `akari-bot-core` 与 `orjson`。外部服务为 `react-tweet.vercel.app` 数据接口、`react-tweet-next.vercel.app` 渲染页面与 WebRender 截图服务。
