# Cytoid 查询

查询 Cytoid 玩家资料，生成 B30（最佳 30 首）与 R10（最近 10 首）成绩图，并按发送者保存账号绑定。

模块名 `cytoid`，别名 `ctd`。

## 安装

```bash
akaribot module add akari-bot-module-cytoid
```

安装后在会话中由管理员用 `module enable cytoid` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `cytoid profile [<username>]` | 查询用户资料，输出头像与经验、等级、Rating、评级分布 | 所有用户 |
| `cytoid b30 [<username>]` | 生成 B30 成绩图 | 所有用户 |
| `cytoid r10 [<username>]` | 生成 R10 成绩图 | 所有用户 |
| `cytoid bind <username>` | 绑定 Cytoid 用户名 | 所有用户 |
| `cytoid unbind` | 解除绑定 | 所有用户 |

省略用户名时使用发送者的绑定账号；未绑定时提示先执行 `cytoid bind`。绑定按发送者 Union 保存，
同一用户在任意会话中都可使用。用户不存在时返回未找到提示，取数失败时返回获取失败提示。

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
