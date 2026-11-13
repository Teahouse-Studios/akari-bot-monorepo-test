# langconv

在简体中文、繁体（香港）与繁体（台湾）之间转换文本。

## 命令

<ModuleAlias names="lc" />

### `langconv`

<CommandUsage usage="langconv <language> <content>" :params="['language=目标语言，如 zh-tw', 'content=待转换文本']" permission="public" />

把文本转换为指定目标语言。`<language>` 接受 `zh-cn`、`zh-hk` 与 `zh-tw`，省略 `zh` 前缀时按 `cn`、`hk`、`tw` 处理，下划线与大小写不影响解析；目标语言不在支持范围内时返回不支持提示。`<content>` 为待转换文本，转换结果直接作为消息正文返回。

<ChatExample
  :log="[
    '用户：~langconv zh-tw 这个软件很好用',
    '机器人：這個軟體很好用',
  ]"
/>
