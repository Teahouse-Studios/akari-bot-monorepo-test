# wolframalpha

此模块将问题或算式提交至 WolframAlpha，以结果图片或简短文本返回解答。接口使用公制单位。

## 命令

<ModuleAlias names="wolfram, wa" />

### `wolframalpha`

<CommandUsage usage="wolframalpha <query>" :params="['query=要检索的问题或公式']" permission="public" />

此命令将问题或算式提交至 WolframAlpha，以结果图片形式返回。若查询涉及 IP、地理位置或身份等敏感内容，此命令不会发起查询，而是直接返回彩蛋内容。若接口无法理解问题，此命令将提示改用英语提问。

### `wolframalpha ask`

<CommandUsage usage="wolframalpha ask <question>" :params="['question=需要以简短文本回答的问题']" permission="public" />

此命令将问题提交至 WolframAlpha，以简短文本形式返回解答。敏感查询与无法理解问题的处理逻辑与 `wolframalpha` 相同。
