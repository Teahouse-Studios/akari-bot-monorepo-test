---
title: 安装与开发
---

# cytoid：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-cytoid
```

安装后，管理员需要在会话中执行 `module enable cytoid` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

绑定信息按发送者的 Union ID 保存，不随平台或群聊变化。成绩图使用包内字体与难度图标渲染，曲绘按需下载到实例缓存目录，重复查询时复用已下载的文件。成绩图中的简体中文使用资源包中的 Noto Sans CJK DemiLight 字体。

## 数据表

<ModuleData tables="module_cytoid_bind_info" :list="false" />

| 表 | 内容 |
| --- | --- |
| `module_cytoid_bind_info` | 发送者 Union ID（主键）与绑定的 Cytoid 用户名 |

版本迁移 `0002_union_id` 把绑定表的主键列改名为 `union_id`，沿用原平台 ID 的值。manifest 声明了 `migrations` 目录，升级时自动执行其中的迁移。

## 依赖与外部服务

依赖 `gql`（GraphQL 请求）、`akari-bot-html2text`、`Pillow`、`tortoise-orm`、`orjson`、`akari-bot-assets-fonts`、`akari-bot-core`。外部服务为 `services.cytoid.io` 的 REST 接口（资料、关卡信息）与 `/graphql`（成绩记录）。
