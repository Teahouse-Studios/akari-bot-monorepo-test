# mcv

查询 Minecraft：Java 版启动器的最新正式版与快照，以及基岩版在 Google Play 商店与 Microsoft Store 的最新正式版。

## 命令

### `mcv`

<CommandUsage usage="mcv" permission="public" />

查询 Java 版最新正式版与最新快照及其发布时间。读取失败时在结果中显示获取失败提示。

### `mcv mcbv`

<CommandUsage usage="mcv mcbv" permission="public" :aliases="['mcbv']" />

查询基岩版在 Google Play 与 Microsoft Store 的最新正式版。单个来源失败时该来源显示获取失败，不影响另一个来源。

`mcev` 别名指向 `mcv mcev`，对应的子命令暂未启用。
