# Mod 下载

按名称同时搜索 CurseForge 与 Modrinth，以编号列表返回候选 Mod，选定后再按版本输出下载链接与文件名。
结果按 CurseForge 在前、Modrinth 在后的顺序合并编号。

模块名 `mod-dl`，别名 `mod_dl`、`moddl`。

## 安装

```bash
akaribot module add akari-bot-module-mod_dl
```

安装后在会话中由管理员用 `module enable mod-dl` 开启。模块建议与 `mcmod` 模块搭配使用。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mod-dl <mod_name> [<version>]` | 搜索 Mod，回复编号后选择版本并获取下载链接 | 所有用户 |

参数 `<version>` 符合 `x.y.z`、`x.y` 或 `xwxxa` 一类版本格式时作为版本过滤条件，否则并入 Mod 名称一同搜索。

交互流程：

1. 两个站点各取至多 10 条结果，分别显示为「CurseForge 结果」「Modrinth 结果」；某一站点无结果时显示「无」。
2. 用户回复编号选择 Mod，非数字或超出范围时返回对应错误。
3. 未指定版本时列出可选版本并要求再次回复；Modrinth 的候选版本来自项目的版本列表，CurseForge 的候选版本来自 `latestFilesIndexes` 中的游戏版本。
4. 返回加载器列表（Modrinth）、下载链接与文件名，CurseForge 另行返回文件支持的游戏版本。

回复的版本不在候选列表中时返回「未找到指定版本」。

## 配置项

manifest 声明配置表为 `module_mod_dl`；本模块的唯一字段是敏感项，实际写入 `module_mod_dl_secret`（`config/module_mod_dl_secret.toml`）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `curseforge_api_key` | str | 空 | CurseForge API 密钥 |

未填写密钥时，CurseForge 请求改走 `https://mcim.z0z0r4.top` 镜像；填写后直连官方接口并携带 `x-api-key`。`manifest.toml` 将该字段登记为重复凭据检查字段。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 搜索与版本选择依赖会话内的连续回复。

## 数据表

无。manifest 未声明 `owned_tables`，搜索结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`。
- 搜索与文件信息：`https://api.modrinth.com/v2`、`https://api.curseforge.com/v1`，未配置密钥时使用 `https://mcim.z0z0r4.top` 镜像。
- 推荐模块：`mcmod`，仅作为搭配建议，不构成依赖。
