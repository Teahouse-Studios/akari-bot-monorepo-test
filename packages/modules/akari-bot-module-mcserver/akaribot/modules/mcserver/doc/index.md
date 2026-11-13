# mcserver

查询 Minecraft：Java 版与基岩版服务器的 MOTD、在线人数、版本与游戏模式。

## 命令

<ModuleAlias names="server" />

### `mcserver`

<CommandUsage usage="mcserver <address:port> [-r] [-p]" :params="['address:port=服务器地址，可带端口']" permission="public" :options="[{flag: '-r', desc: '保留原始格式，返回内容不去除 § 颜色代码。'}, {flag: '-p', desc: '在 Java 版结果中附加在线玩家名单；基岩版查询不返回名单。'}]" />

查询指定服务器的 MOTD、在线人数、版本与游戏模式。`<address:port>` 为服务器地址，可带端口；省略端口时 Java 版使用 25565，基岩版使用 19132。

命令并行查询 Java 版与基岩版，任一版本有响应就发送该版本结果；两个版本都没有响应时返回未找到。

`localhost`、`192.168.*`、`172.16.*` 至 `172.31.*`、`10.*`、`127.*` 与 `0.0.0.0` 被视为本地地址并直接拒绝。

<ChatExample
  :log="[
    '用户：~mcserver mc.hypixel.net',
    '机器人：[JE]',
    'Hypixel Network [1.8/26.3]',
    '在线玩家：19399 / 200000',
  ]"
/>
