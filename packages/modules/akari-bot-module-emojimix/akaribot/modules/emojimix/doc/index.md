# Emoji 合成

把两个 Emoji 合成为一张 Emoji Kitchen 图片，也可以随机取一对，或列出某个 Emoji 支持的全部搭档。

模块名 `emojimix`，无别名。

## 安装

```bash
akaribot module add akari-bot-module-emojimix
```

安装后在会话中由管理员用 `module enable emojimix` 开启。

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

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 合成图直接从 Emoji Kitchen 的静态资源地址引用，不经过本地缓存。
- `list` 在 Discord 平台按每 200 个一批分条发送，其余平台合并为一条消息。
- 支持列表随包分发在 `assets/emoji_data.json`，包含受支持 Emoji、组合与对应资源目录日期。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：`emoji`、`orjson`、`akari-bot-core`。
- 外部服务：`www.gstatic.com` 的 Emoji Kitchen 静态图片。
