# arcaea-rss

arcaea-rss 会定时检查 Arcaea 的官方安装包信息，发现新版本时向启用了该模块的会话推送版本号与下载地址。

## 推送

arcaea-rss 不提供聊天命令，消息由定时任务直接发出。

发现新版本时，推送版本号与下载地址。同一版本只推送一次。

## 推送示例

<ChatExample
  :log="[
    '用户：~module enable arcaea-rss',
    '机器人：成功：开启模块“arcaea-rss”。',
    '〰〰〰',
    '机器人：发现新的 Arcaea 版本：7.1.0c',
    '下载地址：https://arcaea-static.lowiro-cdn.net/yx9cMtoKHbSIS_0805gPpbsFwtCeSYQlwVHyWMPsB-l9plprHqnNVj-emkzbz4qQODR3HJu1kBFQjBQNFL9c2sk-xitdJbeEUp-O03eeOfBYH3VW7st36NJxzHGWsLOqv0OfW7O-vlCNTVA?filename=arcaea_7.1.0c.apk',
  ]"
/>
