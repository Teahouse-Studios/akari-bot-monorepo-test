# bilibili

此模块可以按 BV 号、AV 号或短链接查询哔哩哔哩视频，输出标题、简介、UP 主，以及播放、弹幕、点赞等统计数据。消息中出现视频编号或短链接时也会自动查询。

## 命令

<ModuleAlias names="bili" />

### `bilibili`

<CommandUsage :usage="['bilibili <bid> [-i]', 'bilibili <bid>']" :params="['bid=视频 BV 号或 AV 号']" permission="public" :options="[{flag: '-i', desc: '获取详细信息。'}]" />

此命令用于按 BV 号或 AV 号查询单个视频。

说明：

- `<bid>` 必须以 `BV` 或 `AV` 开头。`AV` 号可写作 `av123456`。
- 视频简介截断到 100 字符。
- 多分 P 的视频在标题后标注分 P 数量。
- 视频不存在或请求被风控拦截时，分别返回对应提示。
- Discord 频道会话不支持 `-i`，改用 Embed 卡片输出。其余平台输出纯文本。

<ChatExample
  :log="[
    '用户：~bilibili BV1aTWm6jEL8',
    '机器人：标题：《原神》过场动画-「岩与契约」',
    'UP 主：原神',
  ]"
/>

## 正则触发

正则命令最多处理同一条消息中的前 5 个匹配，命中后逐条发送查询结果。

- `av` 加数字：查询 AV 号对应的视频。
- `BV` 加 10 位字符：查询 BV 号对应的视频。
- `b23.tv`、`bili22.cn`、`bili33.cn`、`bili2233.cn` 短链：解析跳转地址后查询，可带协议前缀。

前两条规则只对纯文本消息生效。短链规则对图文消息同样生效，不显示“正在输入”状态，解析失败时静默跳过。
