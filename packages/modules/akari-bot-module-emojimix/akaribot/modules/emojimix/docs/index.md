# emojimix

此模块用于把两个 Emoji 合成为一张 Emoji Kitchen 图片，也支持随机取一对 Emoji 合成，或列出某个 Emoji 的全部搭档。

## 命令

### `emojimix`

<CommandUsage :usage="['emojimix', 'emojimix <emoji1> [<emoji2>]']" :params="['emoji1=参与合成的第一个 Emoji', 'emoji2=可省略，参与合成的另一个 Emoji']" permission="public" />

- 合成两个 Emoji。
- 省略参数时随机取一对可合成的 Emoji。只给一个时，随机取一个能与它合成的 Emoji。也可以写作 `emoji1+emoji2`。
- 参数为单个 Emoji 或多个码位组成的序列（如带肤色修饰的 Emoji）。
- 参数中只要有一个不是 Emoji，或有一个不在支持列表中，就返回不支持提示，并列出这些 Emoji。
- 组合存在但图片缺失时返回未找到提示。

返回的第一行是“左 Emoji + 右 Emoji”，其下是合成图。

<ChatExample
  :log="[
    '用户：~emojimix 😀 😍',
    '机器人：😀+😍',
    '![合成图](emojimix-example.png)',
  ]"
/>

### `emojimix list`

<CommandUsage usage="emojimix list [<emoji>]" :params="['emoji=要查询搭档的 Emoji']" permission="public" />

此命令列出全部支持的 Emoji，或指定 Emoji 的搭档。结果较长时，机器人在 Discord 上按每 200 个一批分条发送，其余平台合并为一条消息。

<ChatExample
  :log="[
    '用户：~emojimix list 😀',
    '机器人：支持“😀”的 Emoji 组合：😍🤣🥰😘😎🥳……',
  ]"
/>
