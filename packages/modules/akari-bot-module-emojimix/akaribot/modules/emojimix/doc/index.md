# emojimix

把两个 Emoji 合成为一张 Emoji Kitchen 图片，也可以随机取一对，或列出某个 Emoji 支持的全部搭档。

模块名 `emojimix`，无别名。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `emojimix` | 随机取一对可合成的 Emoji 并返回合成图 | 所有用户 |
| `emojimix <emoji1> [<emoji2>]` | 合成指定的两个 Emoji；也可写成 `emoji1+emoji2`；只给一个时随机搭配 | 所有用户 |
| `emojimix list [<emoji>]` | 列出全部受支持的 Emoji，或指定 Emoji 的搭档 | 所有用户 |

参数可以是单个 Emoji，也可以是由多个码位组成的序列（如带肤色修饰的 Emoji），解析交给 `emoji`
库完成。任一参数不是 Emoji、或不在支持列表中时，返回不支持提示并列出具体的 Emoji；组合存在但
图片缺失时返回未找到提示。输出首行为「左 Emoji + 右 Emoji」，随后是合成图。
