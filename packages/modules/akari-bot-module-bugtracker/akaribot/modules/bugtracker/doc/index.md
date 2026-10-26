# Mojira 漏洞查询

按漏洞编号查询 Mojira（Mojang 漏洞追踪器）中的记录，输出标题、类型、状态、项目、优先级、
解决状态与关联版本，并附上原文链接与页面截图。简体中文会话还会附带 spx 社区翻译。

模块名 `bugtracker`，别名 `bug`；模块包含正则命令。

## 安装

```bash
akaribot module add akari-bot-module-bugtracker
```

安装后在会话中由管理员用 `module enable bugtracker` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `bugtracker <mojiraid>` | 查询漏洞编号对应的内容 | 所有用户 |

`<mojiraid>` 须为「项目前缀-数字」的形式，例如 `MCPE-123456`。无法解析时返回格式错误提示；
项目或漏洞不存在时返回查询失败提示。

## 正则触发

消息以漏洞编号开头时自动查询，支持以下写法：

- 裸编号，如 `MCPE-123456`。
- 方括号包裹的编号，如 `[MCPE-123456]`。
- 完整链接，如 `https://bugs.mojang.com/browse/MCPE/issues/MCPE-123456`。

可识别的项目前缀为 `BDS`、`MCPE`、`MCD`、`MCL`、`MCLG`、`REALMS`、`MC`、`WEB`，大小写不敏感。
单条消息最多处理前 5 个匹配。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 页面截图依赖 WebRender 的元素截图能力，关闭时只发送文本与链接。
- `zh_cn` 会话若命中 spx 翻译表，标题后追加 `(spx: 译文)`；翻译表在进程内缓存，仅首次使用时拉取。
- 状态为 `Open` 或 `Resolved` 时与类型同行展示，其余状态单独成行。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：`orjson`、`akari-bot-core`。
- 外部服务：`bugs.mojang.com`（JQL 搜索接口）、`spxx-db.teahouse.team`（中文翻译表）、WebRender。
