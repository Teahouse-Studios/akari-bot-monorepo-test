# mcv

查询 Minecraft：Java 版启动器的最新正式版与快照，以及基岩版在 Google Play 商店与 Microsoft Store
的最新正式版。模块名 `mcv`，别名为 `mcbv`（等价于 `mcv mcbv`）与 `mcev`。

## 命令

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mcv` | 查询 Java 版最新正式版、最新快照及发布时间 | 所有用户 |
| `mcv mcbv` | 查询基岩版在 Google Play 与 Microsoft Store 的最新正式版 | 所有用户 |

`mcv` 读取 Mojang 的 `version_manifest.json`，读取失败时在结果中显示获取失败提示。`mcv mcbv` 分别
查询 Google Play 与 Microsoft Store；出口 IP 国家为 `China` 时跳过 Google Play，国家尚未探测到时
仍会尝试。单个来源失败时该来源显示获取失败，不影响另一个来源。

`mcev` 别名指向 `mcv mcev`，当前没有注册该子命令的处理器。
