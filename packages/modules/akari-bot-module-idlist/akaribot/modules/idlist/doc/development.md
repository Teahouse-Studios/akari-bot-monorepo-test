---
title: 安装与开发
---

# idlist：安装与开发

本页说明 `idlist` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-idlist
```

模块名为 `idlist`，命令前缀为 `idlist`，没有别名。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 声明支持语言为 `zh_cn`。
- 结果中的完整结果页以链接形式发送，平台需支持 URL 消息元素。

## 数据表

无。查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`。
- ID 表服务：`https://idlist.projectxero.top/search`，查询接口与结果页均来自该站点。
- 接口约定参考 caidlist 项目的 API 文档。
