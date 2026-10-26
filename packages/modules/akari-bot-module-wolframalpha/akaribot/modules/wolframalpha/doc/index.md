# WolframAlpha 查询

把问题或算式提交给 WolframAlpha，分别以结果图片或简短文本返回。接口使用公制单位。

模块名 `wolframalpha`，别名 `wolfram`、`wa`。

## 安装

```bash
akaribot module add akari-bot-module-wolframalpha
```

安装后在会话中由管理员用 `module enable wolframalpha` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `wolframalpha <query>` | 查询并返回 WolframAlpha 生成的结果图片 | 所有用户 |
| `wolframalpha ask <question>` | 查询并返回简短文本答案 | 所有用户 |

行为说明：

- 两个命令都先检查查询内容；命中地理位置、IP、所在地一类敏感查询时返回彩蛋内容，不访问接口。
- `query` 调用 Simple API，下载返回的图片并重新保存为 PNG 后发送。
- `ask` 调用 Short Answers API，直接发送返回的文本。
- 接口返回 501 时统一提示 WolframAlpha 无法理解问题，建议改用英语提问。
- 未配置 AppID 时命令抛出配置缺失错误。

## 配置项

manifest 声明配置表为 `module_wolframalpha`；字段为敏感项，实际写入 `module_wolframalpha_secret`（`config/module_wolframalpha_secret.toml`）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `wolfram_alpha_appid` | str | 空 | WolframAlpha 的 AppID |

`manifest.toml` 将该字段登记为重复凭据检查字段。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 模块声明支持语言为英语（`en_us`）。
- 未声明平台限制，所有已接入平台可用。
- `query` 的结果以图片消息发送。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`Pillow`。
- 外部服务：`http://api.wolframalpha.com/v1/simple` 与 `http://api.wolframalpha.com/v1/result`。
