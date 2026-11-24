# ncmusic

此模块用于搜索网易云音乐歌曲。按编号选择后可以查看歌曲详情，在支持的平台中也可以直接发送音乐卡片。

## 命令

### `ncmusic search`

<CommandUsage usage="ncmusic search <keyword> [--legacy]" :params="['keyword=搜索关键词']" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式。'}]" />

此命令用于搜索网易云音乐，结果取前 10 首。平台支持图片并且未指定 `--legacy` 时，结果以表格图片展示编号、歌名、歌手、专辑与 ID。图片渲染未生成结果时，展示为文本列表。

仅有一首搜索结果时，命令会询问是否查看详情。

包含多首结果时，命令等待你回复序号。序号非数字时返回无效编号提示，超出结果数量时返回编号超出范围提示。命中数量超过 10 首时附带折叠提示。

选中后返回歌曲详情。在 QQ 平台且实例启用音乐卡片时，发送音乐卡片。

### `ncmusic <sid>`

<CommandUsage usage="ncmusic <sid>" :params="['sid=网易云音乐歌曲 ID']" permission="public" platforms="QQ 群聊 / QQ 私聊" />

此命令按歌曲 ID 获取音乐，仅在 QQ 群聊与 QQ 私聊中可用。实例启用音乐卡片时，命令发送音乐卡片。未启用时输出与 `ncmusic info` 一致的歌曲详情。

### `ncmusic info <sid>`

<CommandUsage usage="ncmusic info <sid>" :params="['sid=网易云音乐歌曲 ID']" permission="public" />

此命令用于获取歌曲的封面、歌曲链接、歌名与 ID、歌手、专辑名与专辑 ID 等详细信息。歌曲不存在时返回未找到对应音乐提示。
