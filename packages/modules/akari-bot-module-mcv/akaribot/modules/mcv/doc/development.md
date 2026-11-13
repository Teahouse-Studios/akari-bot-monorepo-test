---
title: 安装与开发
---

# mcv：安装与开发

本文将会介绍此模块的安装、配置、数据表与运行依赖。

## 安装

```bash
akaribot module add akari-bot-module-mcv
```

安装完成后，请让管理员在会话中执行 `module enable mcv` 开启模块。

## 配置项

<ModuleConfig />

是否查询 Google Play 取决于 core 探测到的出口 IP 所在国家，此项不属于模块配置。国家为 `China` 时跳过 Google Play，尚未探测到国家时仍会尝试。

## 权限与平台能力

`mcv` 与 `mcv mcbv` 两条命令都未声明管理员或超级用户限制，普通用户可以直接执行。模块没有声明平台限制，`available_for` 取默认值 `*`。执行查询时需要能访问 Mojang、Google Play 与 `store.rg-adguard.net`。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core`、`google-play-scraper>=1.2.2,<2.0.0` 与 `orjson>=3.10.9,<4.0.0`。外部服务为 `piston-meta.mojang.com`、Google Play 与 `store.rg-adguard.net`。

`piston-meta.mojang.com` 提供 Java 版版本清单，Google Play 提供 `com.mojang.minecraftpe` 的版本号。`store.rg-adguard.net` 用于查询 Microsoft Store 商品 `9NBLGGH2JHXJ` 的 RP 环安装包版本。
