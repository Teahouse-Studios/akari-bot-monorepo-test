# tweet

根据推文 ID 或消息中的推文链接抓取推文内容，渲染为摘要图片并附上原推文链接。

## 命令

<ModuleAlias names="x" />

### `tweet`

<CommandUsage usage="tweet <tweet>" :params="['tweet=推文 ID，纯数字']" permission="public" />

按推文 ID 获取摘要图片，参数为纯数字推文 ID。推文不存在或被限制时返回未找到提示；正文、作者名称或用户名命中内容检查时改为发送彩蛋内容。

模块同时注册正则匹配，消息中出现推文链接时自动触发，触发时不显示正在输入状态。可识别的形式为 `twitter.com/<用户>/status/<推文 ID>` 与 `x.com/<用户>/status/<推文 ID>`，两种地址均可带 `http://`、`https://` 与 `www.` 前缀。自动触发的结果与命令一致：摘要图片在前，原推文链接在后。
