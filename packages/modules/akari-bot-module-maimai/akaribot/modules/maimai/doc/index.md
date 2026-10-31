# maimai

查询舞萌 DX 与 CHUNITHM 的曲目资料、谱面成绩、B50/B30、名牌板、段位与评级进度，并支持绑定水鱼查分器与落雪咖啡屋账号。包内注册三个模块：`maimai`、`chunithm` 与 `maimai-regex`。

## 命令

下表列出常用命令。

| 命令 | 说明 |
| --- | --- |
| `maimai b50 [<user>]` | 查询玩家 B50 |
| `maimai score <id_or_alias>` | 查询歌曲成绩 |
| `maimai bind df` / `maimai bind lx` | 绑定水鱼 / 落雪账号 |
| `maimai switch` | 切换成绩数据源（超级用户） |
| `chunithm b30 [<user>]` | 查询玩家 B30 |
| `maimai <ID>是什么歌` | 正则：按 ID 或别名查询歌曲 |

每条命令的完整参数、选项、权限与输出见[完整命令](commands.md)；CHUNITHM 的差异见
[CHUNITHM](chunithm.md)，正则句式见[正则句式](regex.md)。
