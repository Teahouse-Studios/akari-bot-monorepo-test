# 哔哩哔哩视频

按 BV 号、AV 号或短链接查询哔哩哔哩视频，输出标题、简介、UP 主与播放、弹幕、点赞等统计数据。
消息中出现视频编号或短链接时也会自动查询。

模块名 `bilibili`，别名 `bili`；模块包含正则命令，声明支持语言 `zh_cn`。

## 安装

```bash
akaribot module add akari-bot-module-bilibili
```

安装后在会话中由管理员用 `module enable bilibili` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `bilibili <bid> [-i]` | 按 BV 号或 AV 号查询视频，`-i` 展示详细信息 | 所有用户 |
| `bilibili <bid>`（Discord 频道） | 同上的 Embed 形式，不提供 `-i` | 所有用户 |

`<bid>` 须以 `BV` 或 `AV` 开头，`AV` 号可写作 `av123456`。Discord 频道会话单独注册无选项的模板，
以 Embed 输出；其余平台输出纯文本。

## 正则触发

正则命令最多处理同一条消息中的前 5 个匹配，命中后逐条发送查询结果。

| 触发内容 | 说明 |
| --- | --- |
| `av` 加数字 | 查询 AV 号对应的视频 |
| `BV` 加 10 位字符 | 查询 BV 号对应的视频 |
| `b23.tv`、`bili22.cn`、`bili33.cn`、`bili2233.cn` 短链 | 解析跳转地址后查询，可带协议前缀 |

前两条只对纯文本消息生效；短链规则同时接受文本与富文本元素，且不显示「正在输入」状态。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 通过 WebRender 以 stealth 模式请求 `api.bilibili.com`，需开启 `webrender.enable`。
- 请求失败或视频不存在时分别返回对应提示，短链解析失败则静默跳过。
- 视频简介截断到 100 字符；多分 P 的视频在标题后标注分 P 数量。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：`httpx`（短链跳转解析）、`orjson`、`akari-bot-core`。
- 外部服务：`api.bilibili.com`（经 WebRender）、`b23.tv` 等短链服务。
