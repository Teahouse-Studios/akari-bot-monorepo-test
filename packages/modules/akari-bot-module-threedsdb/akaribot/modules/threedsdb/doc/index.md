# 3dsdb

在 3DS 应用清单中按名称或 Title ID 检索，返回应用名称、UID、Title ID、版本、体积、产品编号与发行商。

## 命令

### `3dsdb`

<CommandUsage usage="3dsdb <keywords>" :params="['keywords=应用名称或 Title ID']" permission="public" />

在 3DS 应用清单中按关键词检索。检索规则：

- 关键词全部为数字时按 `TitleID` 做子串匹配。
- 关键词含非数字字符时按应用名称做不区分大小写的子串匹配。
- 清单覆盖日版、台版、韩版、美版与欧版，命中条目按字段逐行展示。
- 最多输出 10 条；达到上限时追加“结果过多，请提供更具体的关键词”提示。
- 没有任何命中时返回未找到提示。

每个条目包含 `Name`、`UID`、`TitleID`、`Version`、`Size`、`Product Code`、`Publisher` 字段，按清单原值展示。

<ChatExample
  :log="[
    '用户：~3dsdb 000400000008C400',
    '机器人：Name: Tomodachi Life™',
    'UID: 50010000021615',
    'TitleID: 000400000008C400',
  ]"
/>
