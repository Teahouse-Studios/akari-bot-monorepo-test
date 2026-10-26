# 一言

从一言 API 获取随机句子，可指定句子类型。返回内容包含句子正文、作者与出处，并附一言主页链接；繁体中文会话下正文与出处自动转换为繁体。

## 安装

```bash
akaribot module add akari-bot-module-hitokoto
```

模块名为 `hitokoto`，命令前缀为 `hitokoto`，别名为 `htkt`、`yiyan`。

## 命令

| 命令 | 说明 |
| --- | --- |
| `hitokoto` | 随机获取一条一言 |
| `hitokoto <msg_type>` | 获取指定类型的一言 |

`<msg_type>` 的取值是类型代码 `a` 至 `l`，代码含义由一言 API 定义，模块内仅校验取值范围。不在该范围内时返回无效类型提示。类型代码作为一言 API 的 `c` 参数传递。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 声明支持语言为 `zh_cn`、`zh_tw`。会话语言为 `zh_tw` 时，返回的文本字段经 langconv 转换为繁体后再发送。
- 返回内容含链接，平台需支持 URL 消息元素。

## 数据表

无。不保存查询记录。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`langconv==0.4.0`。
- 一言 API：`https://v1.hitokoto.cn/`，用于获取句子。
- 一言主页：`https://hitokoto.cn`，作为结果链接。
