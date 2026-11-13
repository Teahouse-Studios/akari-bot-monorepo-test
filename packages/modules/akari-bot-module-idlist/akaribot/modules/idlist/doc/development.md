---
title: 安装与开发
---

# idlist：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-idlist
```

模块名是 `idlist`，命令的第一个词是 `idlist`，没有别名。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。此模块没有声明平台限制，所有已接入平台都可以使用。

此模块声明支持的语言为 `zh_cn`。命中总数超过 5 条时，模块会以链接形式发送完整结果页，因此平台需要支持 URL 消息元素。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`。外部服务为 ID 表服务 `https://idlist.projectxero.top/search`，查询接口与结果页都来自该站点。每次搜索都会带上 `limit=6`，用来判断是否还有更多结果。接口约定参考 caidlist 项目的 API 文档。
