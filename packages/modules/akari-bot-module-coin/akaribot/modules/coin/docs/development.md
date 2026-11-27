---
title: 安装与开发
---

# coin：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-coin
```

安装后，管理员需要在会话中执行 `module enable coin` 以启用模块。

## 配置项

<ModuleConfig table="module_coin" />

<ModuleConfigFields table="module_coin" />

`coin_limit` 为单次抛掷硬币的数量上限，默认值为 10000。该值必须大于 0，三项权重均不能小于 0。配置值超出范围时，命令会返回配置错误提示。

## 权限与平台能力

此模块无平台限制与权限要求，也不会发起网络请求。随机数来自 `akari-bot-core` 的 `Random`，此模块按权重区间计算判定结果。

## 数据表

<ModuleData />

## 依赖与外部服务

仅依赖 `akari-bot-core`，不使用外部服务。
