# mod-dl

此模块用于按名称同时搜索 CurseForge 与 Modrinth 上的 Mod。搜索结果以编号列表返回，选定 Mod 后再按版本给出下载链接与文件名。编号按 CurseForge 在前、Modrinth 在后的顺序合并。

## 命令

<ModuleAlias names="mod_dl, moddl" />

### `mod-dl`

<CommandUsage usage="mod-dl <mod_name> [<version>]" :params="['mod_name=Mod 名称，作为搜索关键词', 'version=游戏版本号，如 1.20.1']" permission="public" />

- 按 Mod 名称搜索并给出下载链接。
- `<version>` 符合 `x.y.z`、`x.y` 或 `xwxxa` 这类版本格式时，作为版本过滤条件。
- 不符合版本格式时，并入 Mod 名称一同搜索。
- 省略 `<version>` 时，在选定 Mod 后列出候选版本，并要求再次回复。

交互流程：

1. 两个站点各取至多 10 条结果，分别显示为“CurseForge 结果”与“Modrinth 结果”。某一站点没有结果时，该站点的结果行显示“无”。
2. 你回复编号选择 Mod，非数字或超出范围时返回对应错误。
3. 未指定版本时列出可选版本并要求再次回复。
4. 返回下载链接与文件名。Modrinth 结果另附加载器列表，CurseForge 另行返回文件支持的游戏版本。

回复中的版本号不在候选列表中时，返回“未找到指定版本”。
