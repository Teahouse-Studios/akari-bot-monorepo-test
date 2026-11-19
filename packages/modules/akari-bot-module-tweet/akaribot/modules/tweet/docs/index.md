# tweet

此模块可以根据推文 ID 或消息中的推文链接抓取推文内容，渲染为摘要图片并附上原推文链接。

## 命令

<ModuleAlias names="x" />

### `tweet`

<CommandUsage usage="tweet <tweet>" :params="['tweet=推文 ID，纯数字']" permission="public" />

此命令按推文 ID 获取摘要图片，ID 为纯数字。推文不存在或被限制时返回未找到提示。正文、作者名称或用户名含不合规内容时，改为发送彩蛋内容。

此模块还注册了正则匹配，消息中出现推文链接时会自动触发。触发时不显示“正在输入”提示。

可识别的形式为 `twitter.com/<用户>/status/<推文 ID>` 与 `x.com/<用户>/status/<推文 ID>`，两种地址均可带 `http://`、`https://` 与 `www.` 前缀。自动触发时的输出与命令相同：摘要图片在前，原推文链接在后。

<ChatExample
  :log="[
    '用户：~tweet 20',
    '机器人：![推文截图](tweet-example.png)',
    'https://x.com/jack/status/20',
  ]"
/>
