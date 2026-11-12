---
title: 安装与开发
---

# mcv：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mcv
```

安装后在会话中由管理员用 `module enable mcv` 开启。

## 配置项

<ModuleConfig />

是否查询 Google Play 由 core 探测的出口 IP 国家决定，不属于模块配置：国家为 `China` 时跳过 Google Play，国家尚未探测到时仍会尝试。

## 权限与平台能力

两条命令均未声明管理员或超级用户限制，普通用户可执行。模块未声明平台限制，`available_for` 取默认值 `*`。查询依赖对 Mojang、Google Play 与 `store.rg-adguard.net` 的网络访问。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`、`google-play-scraper>=1.2.2,<2.0.0` 与 `orjson>=3.10.9,<4.0.0`。外部服务为 `piston-meta.mojang.com`（Java 版版本清单）、Google Play（`com.mojang.minecraftpe`）与 `store.rg-adguard.net`（查询 Microsoft Store 商品 `9NBLGGH2JHXJ` 的 RP 环安装包版本）。
