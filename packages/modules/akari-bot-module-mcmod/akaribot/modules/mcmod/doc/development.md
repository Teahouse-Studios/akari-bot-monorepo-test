---
title: 安装与开发
---

# mcmod：安装与开发

本页说明 `mcmod` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-mcmod
```

安装后在会话中由管理员用 `module enable mcmod` 开启。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 两条命令均未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 模块声明 `support_languages=["zh_cn"]`，在非简体中文会话中启用时框架会提示语言不受支持。
- 搜索结果页由 WebRender 读取，运行前需在 core 配置中开启 `webrender.enable`。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`beautifulsoup4>=4.11.1,<5.0.0`。
- 外部服务：`search.mcmod.cn` 的搜索页，经 WebRender 抓取后用 BeautifulSoup 解析。
