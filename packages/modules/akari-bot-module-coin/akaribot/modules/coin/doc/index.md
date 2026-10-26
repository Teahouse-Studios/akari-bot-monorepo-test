# 抛硬币

抛掷一枚或多枚硬币，结果分为正面、反面与立起三种，按配置的权重抽取。

模块名 `coin`，无别名。

## 安装

```bash
akaribot module add akari-bot-module-coin
```

安装后在会话中由管理员用 `module enable coin` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `coin [<amount>]` | 抛掷指定枚硬币，省略时抛 1 枚 | 所有用户 |

枚数为 0 时返回未抛掷的提示，为负数或超过上限时返回范围错误。单枚结果单独播报；全部同面时
汇报总数；出现多种结果时分别统计正面、反面与立起的数量。

## 配置

配置表 `module_coin`（`config/module_coin.toml`）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `coin_limit` | int | 10000 | 单次可抛硬币的上限 |
| `coin_faceup_weight` | int | 4997 | 正面的权重 |
| `coin_facedown_weight` | int | 4997 | 反面的权重 |
| `coin_stand_weight` | int | 6 | 立起的权重 |

三项权重须不小于 0，上限须大于 0，否则命令抛出配置错误提示。完整清单见配置模板
`akaribot/modules/coin/config.py`。

## 权限与平台能力

- 无平台限制，无权限要求，不涉及网络请求。
- 随机数取自 core 的 `Random`，按权重区间判定结果。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

仅依赖 `akari-bot-core`，不使用外部服务。
