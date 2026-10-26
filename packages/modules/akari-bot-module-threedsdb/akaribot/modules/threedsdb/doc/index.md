# 3DS 应用数据库

在随包分发的 3DS 应用清单中按名称或 Title ID 检索，返回应用名称、UID、Title ID、版本、体积、产品编号与发行商。

模块名 `3dsdb`，没有别名。

## 安装

```bash
akaribot module add akari-bot-module-threedsdb
```

安装后在会话中由管理员用 `module enable 3dsdb` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `3dsdb <keywords>` | 按关键词检索应用 | 所有用户 |

检索规则：

- 关键词全部为数字时按 `TitleID` 做子串匹配。
- 关键词含非数字字符时按应用名称做不区分大小写的子串匹配。
- 遍历 `assets/data` 下的日版、台版、韩版、美版与欧版清单，命中条目按字段逐行展示。
- 最多输出 10 条；达到上限时追加「结果过多，请提供更具体的关键词」提示。
- 没有任何命中时返回未找到提示。

每个条目包含 `Name`、`UID`、`TitleID`、`Version`、`Size`、`Product Code`、`Publisher` 字段，按清单原值展示。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 结果以文本消息返回，不依赖图片或网络。

## 数据表

无。manifest 未声明 `owned_tables`。应用清单以只读 JSON 随包分发，位于 `assets/data/list_JP.json`、`list_TW.json`、`list_KR.json`、`list_US.json` 与 `list_GB.json`。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`orjson`。
- 不使用外部网络服务。
