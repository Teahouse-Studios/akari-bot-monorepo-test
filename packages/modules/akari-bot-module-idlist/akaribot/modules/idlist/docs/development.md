---
title: 安装与开发
---

# idlist：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-idlist
```

模块名称为 `idlist`，命令首词为 `idlist`，未设置别名。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。此模块未声明平台限制，所有已接入平台均可以正常使用。

此模块声明支持的语言为 `zh_cn`。若检索结果超过 5 条，模块将以链接形式发送完整结果页面，因此目标平台需要支持 URL 消息元素。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`。外部服务为 ID 表服务 `https://idlist.projectxero.top/search`，查询接口与结果页均来源于该站点。每次搜索均附带 `limit=6` 参数，以判断是否存在更多结果。接口约定参见 caidlist 项目的 API 文档。
