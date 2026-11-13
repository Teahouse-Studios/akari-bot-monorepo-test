# convert

做物理量换算，支持长度、质量、面积、体积、速度、温度等常见量纲，输出原始量与换算结果。

## 命令

<ModuleAlias names="conv, unit" />

### `convert`

<CommandUsage usage="convert <from_val> <to_unit>" :params="['from_val=带单位的数值，如 100km', 'to_unit=目标单位，如 m']" permission="public" />

将带单位的数值转换为目标单位，`<from_val>` 由数值与单位连写，`<to_unit>` 只写单位，例如 `convert 100km m`。

表达式与单位名称均按单位库的规则解析，大小写敏感：`km` 与 `KM` 含义不同。无法解析的表达式、量纲不匹配或单位无法识别时统一返回转换失败提示。

<ChatExample
  :log="[
    '用户：~convert 1h min',
    '机器人：1 h = 60 min',
  ]"
/>
