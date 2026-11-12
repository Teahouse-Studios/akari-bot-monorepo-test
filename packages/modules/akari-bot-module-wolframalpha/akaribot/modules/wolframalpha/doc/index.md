# wolframalpha

把问题或算式提交给 WolframAlpha，分别以结果图片或简短文本返回。接口使用公制单位。

## 命令

<ModuleAlias names="wolfram, wa" />

### `wolframalpha`

<CommandUsage usage="wolframalpha <query>" :params="['query=要检索的问题或公式']" permission="public" />

把问题或算式提交给 WolframAlpha，以结果图片形式返回。查询命中 IP、地理位置或身份类敏感检查时返回彩蛋内容，不发起查询；接口无法理解问题时提示改用英语提问。

### `wolframalpha ask`

<CommandUsage usage="wolframalpha ask <question>" :params="['question=需要以简短文本回答的问题']" permission="public" />

把问题提交给 WolframAlpha，以简短文本形式返回。敏感查询与无法理解问题的处理与 `wolframalpha` 一致。
