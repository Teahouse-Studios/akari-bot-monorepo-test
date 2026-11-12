---
title: 安装与开发
---

# idlist：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-idlist
```

模块名为 `idlist`，命令首词为 `idlist`，没有别名。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。未声明平台限制，所有已接入平台可用。声明支持语言为 `zh_cn`。结果中的完整结果页以链接形式发送，平台需支持 URL 消息元素。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`。ID 表服务：`https://idlist.projectxero.top/search`，查询接口与结果页均来自该站点。搜索请求固定携带 `limit=6`，用于判断是否存在更多结果。接口约定参考 caidlist 项目的 API 文档。
