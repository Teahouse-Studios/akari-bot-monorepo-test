# emojimix

把两个 Emoji 合成为一张 Emoji Kitchen 图片，也支持随机取一对或列出某个 Emoji 的全部搭档。

## 命令

### `emojimix`

<CommandUsage :usage="['emojimix', 'emojimix <emoji1> [<emoji2>]']" :params="['emoji1=参与合成的第一个 Emoji', 'emoji2=可省略，参与合成的另一个 Emoji']" permission="public" />

合成两个 Emoji；省略参数时随机取一对可合成的 Emoji，只给一个时随机搭配另一半，也可写作 `emoji1+emoji2`。参数为单个 Emoji 或多个码位组成的序列（如带肤色修饰的 Emoji）。任一参数不是 Emoji，或不在支持列表中时，返回不支持提示并列出具体的 Emoji；组合存在但图片缺失时返回未找到提示。

### `emojimix list`

<CommandUsage usage="emojimix list [<emoji>]" :params="['emoji=要查询搭档的 Emoji']" permission="public" />

列出全部受支持的 Emoji，或指定 Emoji 的搭档。列表较长时在 Discord 按每 200 个一批分条发送，其余平台合并为一条消息。

输出首行为“左 Emoji + 右 Emoji”，随后是合成图。
