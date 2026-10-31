# phigros

绑定 Phigros 云存档后查询 B30、单曲成绩、解锁进度、游戏设置与曲目资料。曲目信息与曲绘按小时检查更新，存放于实例数据目录。

模块名 `phigros`，别名 `pgr`、`phi`。

## 命令

下表省略命令前缀，前缀由实例配置决定。`refresh`、`b30`、`info`、`unlock`、`settings`、`score` 要求当前用户已绑定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `phigros bind <sessiontoken> [-i]` | 使用云存档 SessionToken 绑定；`-i` 表示国际服账号 | 所有用户 |
| `phigros login` | 通过 TapTap 扫码登录并绑定国服账号 | 所有用户，仅限私聊 |
| `phigros unbind` | 解除当前用户的绑定 | 所有用户 |
| `phigros refresh` | 刷新 SessionToken，原令牌立即失效 | 已绑定用户 |
| `phigros b30` | 查询 B30 列表并生成图片 | 已绑定用户 |
| `phigros info` | 查询账号概览 | 已绑定用户 |
| `phigros unlock` | 查询解锁进度 | 已绑定用户 |
| `phigros settings` | 查询游戏设置 | 已绑定用户 |
| `phigros score <song_name>` | 查询指定歌曲各难度的成绩 | 已绑定用户 |
| `phigros song <song_name>` | 查询歌曲资料与谱面信息 | 所有用户 |
| `phigros random` | 随机展示一首歌曲 | 所有用户 |
| `phigros update [--no-illus]` | 更新曲目信息与曲绘；`--no-illus` 跳过曲绘 | 超级用户 |

行为说明：

- `bind` 在公开场景执行时先发送令牌泄露警告并撤回命令消息。SessionToken 格式不合法时直接拒绝。
- `login` 只允许私聊，依次展示 TapTap 授权二维码或链接、轮询授权结果、换取 SessionToken 并绑定国服账号；二维码过期、授权取消与登录失败分别返回对应提示。
- `refresh` 成功后自动写回新令牌，不在消息中回显。
- 依赖曲目信息的命令在文件缺失或结构过旧时提示先执行 `phigros update`。
- `b30` 以图片形式返回排名结果；`song` 与 `random` 在曲绘存在时附带曲绘。
- 令牌失效时提示重新绑定，云存档读取失败时返回统一的获取失败提示。
- 曲目资源每小时自动检查一次版本；自动更新失败只记录警告，等待下一轮重试。
