---
title: CHUNITHM
order: 30
description: CHUNITHM 模块的命令、数据源与相对舞萌 DX 的差异。
---

# CHUNITHM

`chunithm` 模块（别名 `chu`）提供 CHUNITHM 的曲目、谱面与 B30 查询。下文以 `chunithm` 表示命令前缀，实际前缀由实例配置决定。除 `update` 外，命令对普通用户开放。

<NoticeBox type="info">
CHUNITHM 的曲目资料始终来自落雪咖啡屋的曲目表，缓存到实例数据目录；封面从落雪下载。成绩数据按玩家选择的数据源读取：默认落雪，未配置 <code>lxns_client_id</code> 时默认回落到水鱼。成绩绑定与水鱼、落雪账号共用，舞萌绑定的账号同样可用于 CHUNITHM。
</NoticeBox>

## 查询

| 命令 | 选项 | 说明 | 数据源 |
| --- | --- | --- | --- |
| `chunithm base <constant> [<constant_max>] [-p <page>]` | `-p <page>` | 按定数或定数范围搜索谱面 | 本地曲目库 |
| `chunithm level <level> [-p <page>]` | `-p <page>` | 按等级搜索谱面 | 本地曲目库 |
| `chunithm search <keyword> [-p <page>]` | `-p <page>` | 按歌名（可只给一部分）搜索 | 本地曲目库 |
| `chunithm chart <song>` | 无 | 查询各难度谱面；参数可为 ID、`id` 前缀或完整歌名 | 本地曲目库、曲绘 |
| `chunithm id <id>` | 无 | 按 ID 查询歌曲 | 本地曲目库、曲绘 |
| `chunithm song <song>` | 无 | 按 ID 或完整歌名查询歌曲 | 本地曲目库、曲绘 |
| `chunithm random [<diff+level>]` | 无 | 随机歌曲；不填参数时完全随机 | 本地曲目库 |

例如 `chunithm song 1086`、`chunithm chart id1086`、`chunithm random 紫14+`。

`chart`、`id`、`song` 不查询别名库：参数为纯数字或带 `id` 前缀时按 ID 解析，否则按完整歌名匹配。难度参数接受全称、三字母缩写与中文（绿、黄、红、紫、黑），大小写不敏感；CHUNITHM 的难度包含 Ultima。`random` 的 `<diff+level>` 将难度与等级连写，例如 `14+`、`紫14+`；不支持按 DX／标准类型筛选，也不支持 `*` 无条件写法。

<CommandUsage usage="chunithm random [<diff+level>]" permission="public" type="command" :aliases="['chu']" note="不填参数时从全部曲目随机；填写时按等级与可选难度筛选。" />

## B30 与账号

| 命令 | 选项 | 说明 | 数据源 |
| --- | --- | --- | --- |
| `chunithm b30 [<user>]` | 无 | 查询玩家 B30（含 N20）图片 | 所选数据源 |
| `chunithm bind df` | 无 | 绑定水鱼账号 | 水鱼 OAuth |
| `chunithm unbind df` | 无 | 解绑水鱼账号 | 水鱼 OAuth |
| `chunithm bind lx [<auth_code>]` | 无 | 绑定落雪账号；不带参数时返回授权链接 | 落雪 OAuth |
| `chunithm unbind lx` | 无 | 解绑落雪账号 | 落雪 OAuth |
| `chunithm switch` | 无 | 切换当前用户的数据源，目标数据源需已绑定 | 用户数据源设置 |
| `chunithm update [--no-cover]` | `--no-cover` | 更新曲目表与封面 | 落雪曲目表、封面 |

`b30` 不填玩家时查询绑定账号；水鱼填查分器用户名，落雪填好友码。落雪按好友码查询他人需要配置开发者令牌，未配置时只能查询绑定账号；水鱼按用户名查询使用公开端点，不需要绑定。成绩取自玩家当前选择的数据源，`switch` 在水鱼与落雪之间切换，未绑定目标账号时返回对应的绑定命令。`update` 使用 `required_superuser`，从落雪重新拉取曲目表；`switch` 与其余命令使用默认的公开权限。`--no-cover` 跳过封面下载。

<CommandUsage usage="chunithm b30 [<user>]" permission="public" type="command" :aliases="['chu']" note="水鱼填查分器用户名，落雪填好友码；留空查询绑定账号。" />

<CommandUsage usage="chunithm switch" permission="public" type="command" :aliases="['chu']" note="切换只影响当前用户；目标数据源未绑定时不会切换。" />

## 与舞萌 DX 的差异

| 方面 | CHUNITHM | 舞萌 DX |
| --- | --- | --- |
| 默认数据源 | 落雪；未配置落雪 OAuth 时回落水鱼 | 水鱼 |
| 成绩图片 | B30，附 N20 | B50 |
| 曲目资料 | 落雪曲目表 | 水鱼曲目库 |
| 别名 | 无别名命令，`chart`／`song` 按完整歌名匹配 | 支持别名查询与别名库 |
| 数据源切换权限 | 普通用户 | 超级用户 |
| 更新内容 | 曲目表与封面 | 曲目库、别名与封面 |

CHUNITHM 没有 `new`、`alias`、`grade`、`scoreline`、`calc`、`plate`、`process`、`rank`、`scorelist`、`score` 与 `b50` 命令，这些命令只在 `maimai` 模块提供。曲目资料来自落雪而非水鱼，因此舞萌的曲目更新不会改变 CHUNITHM 的曲目表。
