# wolframalpha

此模块把问题或算式提交给 WolframAlpha，以结果图片或简短文本返回。接口使用公制单位。

## 命令

<ModuleAlias names="wolfram, wa" />

### `wolframalpha`

<CommandUsage usage="wolframalpha <query>" :params="['query=要检索的问题或公式']" permission="public" />

此命令把问题或算式提交给 WolframAlpha，以结果图片形式返回。查询涉及 IP、地理位置或身份等敏感内容时，命令不发起查询，直接返回彩蛋内容。接口无法理解问题时，命令提示改用英语提问。

### `wolframalpha ask`

<CommandUsage usage="wolframalpha ask <question>" :params="['question=需要以简短文本回答的问题']" permission="public" />

此命令把问题提交给 WolframAlpha，以简短文本形式返回。敏感查询与无法理解问题的处理方式与 `wolframalpha` 相同。
