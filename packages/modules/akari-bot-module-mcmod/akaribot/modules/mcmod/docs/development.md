---
title: 安装与开发
---

# mcmod：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mcmod
```

安装后，管理员需要在会话中执行 `module enable mcmod`。

## 配置项

<ModuleConfig />

## 权限与平台能力

`mcmod <mod_name>` 与 `mcmod details <content>` 都没有声明管理员或超级用户限制，普通用户可以执行。模块未声明平台限制，`available_for` 取默认值 `*`。

模块声明了 `support_languages=["zh_cn"]`。在非简体中文会话中启用该模块时，框架会提示语言不受支持。搜索结果页经 WebRender 抓取，运行前需要在 core 配置中开启 `webrender.enable`。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core` 与 `beautifulsoup4>=4.11.1,<5.0.0`。外部服务为 `search.mcmod.cn`。名称搜索使用 `https://search.mcmod.cn/s?key=`，内容搜索使用 `https://search.mcmod.cn/s?filter=3&key=`。页面经 WebRender 抓取后用 BeautifulSoup 解析。
