# emojimix

此模块用于将两个 Emoji 合成为一张 Emoji Kitchen 图片，也支持随机选取一对 Emoji 合成，或列出特定 Emoji 的全部组合搭档。

## 命令

### `emojimix`

<CommandUsage :usage="['emojimix', 'emojimix <emoji1> [<emoji2>]']" :params="['emoji1=参与合成的第一个 Emoji', 'emoji2=可省略，参与合成的另一个 Emoji']" permission="public" />

- 合成两个 Emoji。
- 省略参数时随机选取一对能够合成的 Emoji。仅提供一个参数时，随机选取能够与其合成的 Emoji。也可以写作 `emoji1+emoji2`。
- 参数为单个 Emoji 或多个码位组成的序列（例如带有肤色修饰的 Emoji）。
- 参数中存在非 Emoji 字符时返回无效的 Emoji 提示，提示中不列出这些字符。参数为 Emoji 但未收录在支持列表时返回不受支持的提示，并列出对应 Emoji。
- 组合存在但图片缺失时返回未找到提示。

返回结果的第一行为“左 Emoji + 右 Emoji”，下方为合成生成的图片。

<ChatExample
  :log="[
    '用户：~emojimix 😀 😍',
    '机器人：😀+😍',
    '![合成图](emojimix-example.png)',
  ]"
/>

### `emojimix list`

<CommandUsage usage="emojimix list [<emoji>]" :params="['emoji=要查询搭档的 Emoji']" permission="public" />

此命令列出全部支持的 Emoji，或指定 Emoji 的组合搭档。当结果较长时，机器人在 Discord 平台上按照每 200 个一组分批发送，在其余平台则合并为一条消息发送。

<ChatExample
  :log="[
    '用户：~emojimix list 😀',
    '机器人：支持“😀”的 Emoji 组合：😍🤣🥰😘😎🥳……',
  ]"
/>
