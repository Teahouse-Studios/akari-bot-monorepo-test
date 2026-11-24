---
title: 安装与开发
---

# dice：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-dice
```

安装完成后，管理员需要在会话中执行 `module enable dice` 启用模块。

## 配置项

<ModuleConfig table="module_dice" />

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `dice_limit` | int | 100 | 单次投掷的骰子数量上限 |
| `dice_roll_limit` | int | 10 | 一次命令的投掷次数上限 |
| `dice_count_limit` | int | 10 | 表达式中骰子项数上限 |
| `dice_output_count` | int | 50 | 单次输出的数据量上限 |
| `dice_output_len` | int | 200 | 输出最大长度 |
| `dice_output_digit` | int | 9 | 输出数位上限，超过时使用科学计数法 |
| `dice_detail_count` | int | 5 | 投掷总量达到该值时不显示详细信息 |

若任一项小于或等于 0，命令将返回配置错误提示。完整清单参见配置模板 `akaribot/modules/dice/config.py`。

## 权限与平台能力

`set` 与 `rule` 需要会话管理员权限。默认面数保存在会话数据 `dice_default_sides` 中，判定方向保存在 `dice_dc_reversed` 中。若目标平台支持 Markdown，模块会将表达式中的 `*` 转义，避免其被渲染为格式标记。

## 数据表

<ModuleData />

会话配置参数持久化存储在 `akari-bot-core` 的 Union 数据中。

## 依赖与外部服务

依赖 `numpy`（对点数排序后获取最高值或最低值）、`simpleeval`（计算表达式）、`akari-bot-core`。不使用外部网络服务。
