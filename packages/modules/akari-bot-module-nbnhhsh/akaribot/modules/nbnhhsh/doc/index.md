# nbnhhsh

查询一句含有拼音首字母缩写的话，返回站点收录的候选含义。适用于“yyds”、“xswl”一类网络缩写。

## 命令

### `nbnhhsh`

<CommandUsage usage="nbnhhsh <term>" :params="['term=含有拼音首字母缩写的文本']" permission="public" />

- 查询文本中的拼音首字母缩写含义。
- 回复以输入文本的小写形式开头，随后列出匹配结果。
- 站点提供确定释义时，以顿号分隔各条释义。
- 只提供候选输入时，以“有可能是：”开头列出候选；没有匹配结果时返回未找到提示。
- 释义发送前经过内容审核，不合规部分替换为 `[REDACTED:原因]`。

<ChatExample
  :log="[
    '用户：~nbnhhsh u1s1',
    '机器人：u1s1',
    '有一说一',
  ]"
/>
