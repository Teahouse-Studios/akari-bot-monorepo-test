# 推文摘要

根据推文 ID 或推文链接抓取推文内容，渲染为摘要图片并附上原推文链接。

模块名 `tweet`，别名 `x`。

## 安装

```bash
akaribot module add akari-bot-module-tweet
```

安装后在会话中由管理员用 `module enable tweet` 开启。

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

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令与正则匹配对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 摘要图依赖实例启用 WebRender；未启用时无法生成截图。
- 图片发送能力由平台决定，不支持图片的平台无法展示摘要图。

## 数据表

无。manifest 未声明 `owned_tables`，推文数据不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`orjson`。
- 外部服务：`react-tweet.vercel.app` 数据接口、`react-tweet-next.vercel.app` 渲染页面与 WebRender 截图服务。
