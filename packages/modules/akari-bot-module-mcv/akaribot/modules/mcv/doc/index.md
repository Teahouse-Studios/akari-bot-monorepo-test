# Minecraft 版本查询

查询 Minecraft：Java 版启动器的最新正式版与快照，以及基岩版在 Google Play 商店与 Microsoft Store
的最新正式版。模块名 `mcv`，别名为 `mcbv`（等价于 `mcv mcbv`）与 `mcev`。

## 安装

```bash
akaribot module add akari-bot-module-mcv
```

安装后在会话中由管理员用 `module enable mcv` 开启。

## 命令

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mcv` | 查询 Java 版最新正式版、最新快照及发布时间 | 所有用户 |
| `mcv mcbv` | 查询基岩版在 Google Play 与 Microsoft Store 的最新正式版 | 所有用户 |

`mcv` 读取 Mojang 的 `version_manifest.json`，读取失败时在结果中显示获取失败提示。`mcv mcbv` 分别
查询 Google Play 与 Microsoft Store；出口 IP 国家为 `China` 时跳过 Google Play，国家尚未探测到时
仍会尝试。单个来源失败时该来源显示获取失败，不影响另一个来源。

`mcev` 别名指向 `mcv mcev`，当前没有注册该子命令的处理器。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。是否查询 Google Play 由 core 探测
的出口 IP 国家决定，不属于模块配置。

## 权限与平台能力

- 两条命令均未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 查询依赖对 Mojang、Google Play 与 `store.rg-adguard.net` 的网络访问。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`google-play-scraper>=1.2.2,<2.0.0`、`orjson>=3.10.9,<4.0.0`。
- 外部服务：`piston-meta.mojang.com`（Java 版版本清单）、Google Play（`com.mojang.minecraftpe`）、
  `store.rg-adguard.net`（查询 Microsoft Store 商品 `9NBLGGH2JHXJ` 的 RP 环安装包版本）。
