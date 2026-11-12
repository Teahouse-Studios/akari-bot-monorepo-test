# arcaea

查询 Arcaea 的最新安装包、随机曲目与官方游玩排行，并按分数与谱面定数计算单曲潜力值。

## 命令

<ModuleAlias names="arc" />

### `arcaea download`

<CommandUsage usage="arcaea download" permission="public" />

查询最新版本的游戏 APK 版本号与下载地址。查询失败时显示获取失败提示。

### `arcaea random`

<CommandUsage usage="arcaea random" permission="public" />

从官方曲目列表中随机取一首歌，附上曲绘；曲绘缺失时只发送曲名。

### `arcaea rank free`

<CommandUsage usage="arcaea rank free" permission="public" />

查看当前免费歌曲的游玩排行，输出名次、曲名与状态。

### `arcaea rank paid`

<CommandUsage usage="arcaea rank paid" permission="public" />

查看当前付费歌曲的游玩排行，输出名次、曲名与状态。

### `arcaea calc`

<CommandUsage usage="arcaea calc <score> <rating>" :params="['score=游玩分数', 'rating=谱面定数']" permission="public" />

按分数与谱面定数计算单曲潜力值。分数不低于 10000000 时取定数加 2；不低于 9800000 时取定数加 1 再加 `(分数 - 9800000) / 200000`；其余情况取定数加 `(分数 - 9500000) / 300000`。结果保留两位小数，低于 0 时按 0 输出。
