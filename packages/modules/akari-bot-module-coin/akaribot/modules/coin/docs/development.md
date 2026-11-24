---
title: 安装与开发
---

# coin：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-coin
```

安装后，管理员需要在会话中执行 `module enable coin` 以启用模块。

## 配置项

<ModuleConfig table="module_coin" />

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `coin_limit` | int | 10000 | 单次可以抛掷硬币的数量上限 |
| `coin_faceup_weight` | int | 4997 | 正面的权重 |
| `coin_facedown_weight` | int | 4997 | 反面的权重 |
| `coin_stand_weight` | int | 6 | 立起的权重 |

完整配置字段参见配置模板 `akaribot/modules/coin/config.py`。

`coin_limit` 为单次抛掷硬币的数量上限，默认值为 10000。该值必须大于 0，三项权重均不能小于 0。配置值超出范围时，命令会返回配置错误提示。

## 权限与平台能力

此模块无平台限制与权限要求，也不会发起网络请求。随机数来自 `akari-bot-core` 的 `Random`，此模块按权重区间计算判定结果。

## 数据表

<ModuleData />

## 依赖与外部服务

仅依赖 `akari-bot-core`，不使用外部服务。
