# mcv

此模块可以查询 Minecraft：Java 版启动器的最新正式版与快照，以及基岩版在 Google Play 商店与 Microsoft Store 的最新正式版。

## 命令

### `mcv`

<CommandUsage usage="mcv" permission="public" />

此命令用于查询 Java 版最新正式版与最新快照，以及两者的发布时间。获取失败时，结果中会显示失败提示。

示例：

<ChatExample
  :log="[
    '用户：~mcv',
    '机器人：当前启动器内最新版本：',
    '最新版：`1.21.4`',
    '发布于：2025 年 01 月 02 日 02:00:00 (UTC+8)',
  ]"
/>

### `mcv mcbv`

<CommandUsage usage="mcv mcbv" permission="public" :aliases="['mcbv']" />

此命令用于查询基岩版在 Google Play 与 Microsoft Store 的最新正式版。某个来源失败时，该来源显示获取失败，另一个来源的结果不受影响。

示例：

<ChatExample
  :log="[
    '用户：~mcv mcbv',
    '机器人：当前 Google Play 商店内最新正式版：',
    '`1.21.51`',
  ]"
/>

`mcev` 别名指向 `mcv mcev`，但该子命令暂未启用。
