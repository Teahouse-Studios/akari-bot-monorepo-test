---
title: 安装与开发
---

# coin：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-coin
```

安装后由管理员在会话中执行 `module enable coin` 开启。

## 配置项

<ModuleConfig table="module_coin" />

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `coin_limit` | int | 10000 | 单次可抛硬币的上限 |
| `coin_faceup_weight` | int | 4997 | 正面的权重 |
| `coin_facedown_weight` | int | 4997 | 反面的权重 |
| `coin_stand_weight` | int | 6 | 立起的权重 |

三项权重不得小于 0，`coin_limit` 须大于 0，越界时命令返回配置错误提示。完整字段见配置模板 `akaribot/modules/coin/config.py`。

## 权限与平台能力

模块无平台限制与权限要求，不发起网络请求。随机数取自 core 的 `Random`，按权重区间判定结果。

## 数据表

<ModuleData />

## 依赖与外部服务

仅依赖 `akari-bot-core`，不使用外部服务。
