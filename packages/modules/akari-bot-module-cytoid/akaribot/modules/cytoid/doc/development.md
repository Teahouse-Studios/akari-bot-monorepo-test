---
title: 安装与开发
---

# cytoid：安装与开发

本页说明 `cytoid` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-cytoid
```

安装后在会话中由管理员用 `module enable cytoid` 开启。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 绑定信息按发送者 Union 保存，不随平台或群聊变化。
- 成绩图使用包内字体与难度图标渲染，曲绘按需下载到缓存目录；简中文字使用资源包字体
  Noto Sans CJK DemiLight。
- 成绩图的曲绘目录为实例缓存目录，重复查询复用已下载文件。

## 数据表

manifest 声明的 `owned_tables`：

| 表 | 内容 |
| --- | --- |
| `module_cytoid_bind_info` | 发送者 Union ID（主键）与绑定的 Cytoid 用户名 |

版本迁移 `0002_union_id` 把绑定表的主键列由平台 ID 更名为 `union_id`，沿用原值。manifest 声明了
`migrations` 目录，升级时自动执行。

## 依赖与外部服务

- 依赖：`gql`（GraphQL 请求）、`akari-bot-html2text`、`Pillow`、`tortoise-orm`、`orjson`、
  `akari-bot-assets-fonts`、`akari-bot-core`。
- 外部服务：`services.cytoid.io` 的 REST 接口（资料、关卡信息）与 `/graphql`（成绩记录）。
