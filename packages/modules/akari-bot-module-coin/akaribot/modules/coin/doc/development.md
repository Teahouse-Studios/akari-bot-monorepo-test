---
title: 安装与开发
---

# coin：安装与开发

本页说明 `coin` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-coin
```

安装后在会话中由管理员用 `module enable coin` 开启。

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
