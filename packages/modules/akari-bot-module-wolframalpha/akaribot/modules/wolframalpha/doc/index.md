# wolframalpha

把问题或算式提交给 WolframAlpha，分别以结果图片或简短文本返回。接口使用公制单位。

模块名 `wolframalpha`，别名 `wolfram`、`wa`。

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
