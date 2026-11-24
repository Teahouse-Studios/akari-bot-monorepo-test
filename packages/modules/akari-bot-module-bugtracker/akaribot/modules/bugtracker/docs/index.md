# bugtracker

此模块可以按漏洞编号查询 Mojira（Mojang 漏洞追踪器）中的记录。查询结果包含标题、类型、状态、项目、优先级、解决状态与关联版本，并提供原文链接与页面截图。简体中文会话还会附带 spx 社区翻译。

## 命令

<ModuleAlias names="bug" />

### `bugtracker`

<CommandUsage usage="bugtracker <mojiraid>" :params="['mojiraid=Mojira 漏洞编号，含项目前缀']" permission="public" />

此命令用于查询漏洞编号对应的记录。`<mojiraid>` 格式必须为“项目前缀-数字”，例如 `MCPE-123456`。

编号无法解析时返回编号无效的提示。若项目或漏洞不存在，则返回查询失败提示。

<ChatExample
  :log="[
    '用户：~bugtracker MCPE-123456',
    '机器人：[MCPE-123456] Large Mouse Input Lag.',
    'Type: Bug | Status: Resolved',
    'Resolution: Duplicate',
    '![漏洞页面截图](bugtracker-example.webp)',
  ]"
/>

## 正则触发

消息以漏洞编号开头时，机器人会自动执行查询，支持以下输入形式：

- 纯编号，如 `MCPE-123456`。
- 方括号包裹的编号，如 `[MCPE-123456]`。
- 完整链接，如 `https://bugs.mojang.com/browse/MCPE/issues/MCPE-123456`。

支持识别的项目前缀为 `BDS`、`MCPE`、`MCD`、`MCL`、`MCLG`、`REALMS`、`MC`、`WEB`，不区分大小写。单条消息最多处理前 5 个匹配项。
