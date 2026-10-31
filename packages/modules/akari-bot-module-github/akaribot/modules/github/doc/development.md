---
title: 安装与开发
---

# github：安装与开发

本页说明 `github` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-github
```

模块名为 `github`，命令前缀为 `github`，别名为 `gh`。

## 配置项

配置文件为 `config/module_github.toml`。

| 表 | 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `module_github_secret` | `github_pat` | str | 空 | GitHub 的 Personal Access Token，用于提高 API 请求速率限制 |

`module_github_secret` 是敏感表，字段值加密存储。留空时按匿名请求处理，速率限制更低。

## 权限与平台能力

- 所有命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 查询结果会经过内容安全检查，命中风险规则时返回占位内容。
- `repo` 会发送 OpenGraph 预览图，平台需支持图片消息。

## 数据表

无。查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`。
- GitHub REST API：`https://api.github.com`，用于仓库、用户与仓库搜索接口。
- OpenGraph 预览图：`https://opengraph.githubassets.com`。
