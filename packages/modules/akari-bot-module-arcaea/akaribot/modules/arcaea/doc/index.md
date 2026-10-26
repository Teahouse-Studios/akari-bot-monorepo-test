# Arcaea 查询

查询 Arcaea 的最新安装包、随机曲目与官方游玩排行，并按分数与谱面定数计算单曲潜力值。
所有数据取自官方 Web API，经 core 的 WebRender 请求。

模块名 `arcaea`，别名 `arc`。

## 安装

```bash
akaribot module add akari-bot-module-arcaea
```

安装后在会话中由管理员用 `module enable arcaea` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `arcaea download` | 查询最新版本的游戏 APK 版本号与下载地址 | 所有用户 |
| `arcaea random` | 从官方曲目展示接口随机取一首歌，并附带本地曲绘 | 所有用户 |
| `arcaea rank free` | 查看当前免费歌曲游玩排行 | 所有用户 |
| `arcaea rank paid` | 查看当前付费歌曲游玩排行 | 所有用户 |
| `arcaea calc <score> <rating>` | 按分数与谱面定数计算单曲潜力值 | 所有用户 |

`calc` 的换算规则：分数不低于 10000000 时取定数加 2；不低于 9800000 时取定数加 1 再加
`(分数 - 9800000) / 200000`；其余情况取定数加 `(分数 - 9500000) / 300000`。结果保留两位小数，
低于 0 时按 0 输出。

`rank` 输出名次、曲名与状态；`random` 在曲绘文件存在时附带图片，否则只发送曲名。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- `download`、`random`、`rank` 通过 WebRender 请求官方接口，需开启 `webrender.enable`。
- `calc` 为纯本地计算，不依赖网络。
- 曲绘从包内 `assets/jacket/<song_id>.jpg` 读取，文件缺失时降级为纯文本。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：`orjson`、`akari-bot-core`。
- 外部服务：`webapi.lowiro.com`（APK 信息、曲目展示、免费与付费排行），经 WebRender 读取原始响应。
