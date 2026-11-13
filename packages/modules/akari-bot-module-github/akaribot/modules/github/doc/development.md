---
title: 安装与开发
---

# github：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-github
```

模块名是 `github`，命令的第一个词是 `github`，别名是 `gh`。

## 配置项

<ModuleConfig table="module_github" />

| 表 | 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `module_github_secret` | `github_pat` | str | 空 | GitHub 的 Personal Access Token，用于提高 API 请求速率限制 |

`module_github_secret` 是敏感表，字段值加密存储。字段留空时按匿名请求处理，速率限制更低。

## 权限与平台能力

所有命令对普通用户开放，不要求管理员或超级用户权限。此模块没有声明平台限制，所有已接入平台都可以使用。

查询结果会经过内容安全检查。命中风险规则时，模块返回占位内容。`repo` 会发送 OpenGraph 预览图，因此平台需要支持图片消息。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`。GitHub REST API 为 `https://api.github.com`，提供仓库、用户与搜索三类接口。OpenGraph 预览图由 `https://opengraph.githubassets.com` 提供。
