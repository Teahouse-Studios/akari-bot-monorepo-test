# tweet

根据推文 ID 或推文链接抓取推文内容，渲染为摘要图片并附上原推文链接。

模块名 `tweet`，别名 `x`。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `tweet <tweet>` | 按推文 ID 获取摘要 | 所有用户 |

模块同时注册正则匹配，消息中出现以下形式的链接时自动触发，且不在触发时显示正在输入状态：

- `twitter.com/<用户>/status/<推文 ID>`
- `x.com/<用户>/status/<推文 ID>`
- 上述地址可带 `http://`、`https://` 与 `www.` 前缀。

处理流程：

1. 请求 `https://react-tweet.vercel.app/api/tweet/<推文 ID>` 获取推文数据；推文不存在或被限制时返回未找到提示。
2. 对推文正文、作者名称与用户名执行内容检查，命中时发送彩蛋内容而不渲染摘要。
3. 通过 WebRender 对 `https://react-tweet-next.vercel.app/light/<推文 ID>` 的 `article` 元素截图，隐藏回复框、关注入口与页脚等元素。
4. 发送截图与 `https://x.com/<用户名>/status/<推文 ID>` 链接。
