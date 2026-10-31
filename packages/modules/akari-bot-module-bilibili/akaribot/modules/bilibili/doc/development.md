---
title: 安装与开发
---

# bilibili：安装与开发

本页说明 `bilibili` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-bilibili
```

安装后在会话中由管理员用 `module enable bilibili` 开启。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 通过 WebRender 以 stealth 模式请求 `api.bilibili.com`，需开启 `webrender.enable`。
- 请求失败或视频不存在时分别返回对应提示，短链解析失败则静默跳过。
- 视频简介截断到 100 字符；多分 P 的视频在标题后标注分 P 数量。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：`httpx`（短链跳转解析）、`orjson`、`akari-bot-core`。
- 外部服务：`api.bilibili.com`（经 WebRender）、`b23.tv` 等短链服务。
