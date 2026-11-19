---
title: 安装与开发
---

# coin：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-coin
```

安装后，管理员需要在会话中执行 `module enable coin`。

## 配置项

<ModuleConfig table="module_coin" />

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `coin_limit` | int | 10000 | 单次可抛硬币的上限 |
| `coin_faceup_weight` | int | 4997 | 正面的权重 |
| `coin_facedown_weight` | int | 4997 | 反面的权重 |
| `coin_stand_weight` | int | 6 | 立起的权重 |

完整字段见配置模板 `akaribot/modules/coin/config.py`。

`coin_limit` 是单次抛硬币的数量上限，默认 10000。该值必须大于 0，三项权重都不能小于 0。配置值超出范围时，命令会返回配置错误提示。

## 权限与平台能力

模块没有平台限制和权限要求，也不会发起网络请求。随机数来自 `akari-bot-core` 的 `Random`，模块按权重区间判断结果。

## 数据表

<ModuleData />

## 依赖与外部服务

只依赖 `akari-bot-core`，不使用外部服务。
