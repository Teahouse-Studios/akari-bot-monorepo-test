# phigros

绑定 Phigros 云存档后查询 B30、单曲成绩、解锁进度、游戏设置与曲目资料。曲目信息与曲绘每小时自动检查更新。

## 命令

<ModuleAlias names="pgr, phi" />

### `phigros bind`

<CommandUsage usage="phigros bind <sessiontoken> [-i]" :params="['sessiontoken=云存档 SessionToken']" permission="public" :options="[{flag: '-i', desc: '表示国际服账号。'}]" />

使用云存档 SessionToken 绑定账号。SessionToken 格式不合法时直接拒绝；在公开场景执行时先发送令牌泄露警告并撤回命令消息。

### `phigros login`

<CommandUsage usage="phigros login" permission="public" />

仅限私聊。通过 TapTap 扫码登录并绑定国服账号。命令依次展示授权二维码或链接、轮询授权结果、换取 SessionToken 并完成绑定；二维码过期、授权取消与登录失败分别返回对应提示。

### `phigros unbind`

<CommandUsage usage="phigros unbind" permission="public" />

解除当前用户的绑定。

<ChatExample
  :log="[
    '用户：~phigros unbind',
    '机器人：解绑成功。',
  ]"
/>

### `phigros refresh`

<CommandUsage usage="phigros refresh" permission="public" />

刷新当前账号的 SessionToken，原令牌立即失效。刷新后自动写回新令牌，不在消息中回显。需先绑定账号。

### `phigros b30`

<CommandUsage usage="phigros b30" permission="public" />

查询 B30 列表，以图片形式返回排名结果。需先绑定账号。

### `phigros info`

<CommandUsage usage="phigros info" permission="public" />

查询账号概览。需先绑定账号。

### `phigros unlock`

<CommandUsage usage="phigros unlock" permission="public" />

查询解锁进度。需先绑定账号。

### `phigros settings`

<CommandUsage usage="phigros settings" permission="public" />

查询游戏设置。需先绑定账号。

### `phigros score`

<CommandUsage usage="phigros score <song_name>" :params="['song_name=曲名，匹配时忽略标点与大小写']" permission="public" />

查询指定歌曲各难度的成绩，曲绘存在时附带曲绘。需先绑定账号。

### `phigros song`

<CommandUsage usage="phigros song <song_name>" :params="['song_name=曲名，匹配时忽略标点与大小写']" permission="public" />

查询歌曲资料与谱面信息，曲绘存在时附带曲绘。

<ChatExample
  :log="[
    '用户：~phigros song Dlyrotz',
    '机器人：Dlyrotz － Likey',
    '画师：DoublePian',
    'EZ 4.0｜谱师：Su1fuR',
    'HD 9.1｜谱师：Su1fuR',
    'IN 13.7｜谱师：XMT小咩兔 vs. Barbarianerman',
  ]"
/>

### `phigros random`

<CommandUsage usage="phigros random" permission="public" />

随机展示一首歌曲，曲绘存在时附带曲绘。

<ChatExample
  :log="[
    '用户：~phigros random',
    '机器人：Cthugha － USAO',
    '画师：谷地（青鸟 modified）',
    'EZ 6.0｜谱师：Barbarianerman',
    'HD 10.4｜谱师：Barbarianerman',
    'IN 16.0｜谱师：Gausbon',
    'AT 16.1｜谱师：百九十八 feat. NerSAN',
  ]"
/>

### `phigros update`

<CommandUsage usage="phigros update [--no-illus]" permission="superuser" :options="[{flag: '--no-illus', desc: '跳过曲绘下载。'}]" />

更新曲目信息与曲绘。资源由模块每小时自动检查一次，也可用此命令手动更新。

<ChatExample
  :log="[
    '用户：~phigros update',
    '机器人：成功。',
  ]"
/>

依赖曲目信息的命令在文件缺失或结构过旧时提示先执行 `phigros update`。令牌失效时提示重新绑定，云存档读取失败时返回统一的获取失败提示。
