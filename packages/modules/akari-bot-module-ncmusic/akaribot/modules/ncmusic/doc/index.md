# ncmusic

搜索网易云音乐歌曲，按编号选择后查看歌曲详情，或在支持的平台上直接发送音乐卡片。

## 命令

### `ncmusic search`

<CommandUsage usage="ncmusic search <keyword> [--legacy]" :params="['keyword=搜索关键词']" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式。'}]" />

搜索网易云音乐，结果取前 10 首。平台支持图片且未指定 `--legacy` 时以表格图片展示编号、歌名、歌手、专辑与 ID，图片渲染没有产出时回退为文本列表。

只有一首结果时询问是否查看详情；多首结果时等待回复序号，序号非数字时返回无效编号提示，超出结果数时返回编号超出范围提示。命中数量超过 10 首时附折叠提示。选中后返回歌曲详情，QQ 且开启卡片时改为发送音乐卡片。

### `ncmusic <sid>`

<CommandUsage usage="ncmusic <sid>" :params="['sid=网易云音乐歌曲 ID']" permission="public" />

只在 QQ 群聊与 QQ 私聊可用。按歌曲 ID 获取音乐：实例开启音乐卡片时发送音乐卡片，未开启时输出与 `ncmusic info` 一致的歌曲详情。

### `ncmusic info <sid>`

<CommandUsage usage="ncmusic info <sid>" :params="['sid=网易云音乐歌曲 ID']" permission="public" />

获取歌曲详细信息：封面、歌曲链接、歌名与 ID、歌手、专辑名与专辑 ID。歌曲不存在时返回未找到对应的音乐提示。
