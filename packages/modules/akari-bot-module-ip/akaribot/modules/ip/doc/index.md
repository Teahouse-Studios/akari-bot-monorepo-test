# ip

查询 IPv4 或 IPv6 地址的类型、归属地与网络属性，并尝试做反向 DNS 解析。输出包含国家、地区、城市、经纬度、邮编、组织、ASN、UTC 偏移与反向解析主机名。

## 命令

### `ip`

<CommandUsage usage="ip <ip_address>" :params="['ip_address=IPv4 或 IPv6 地址']" permission="public" />

查询 IPv4 或 IPv6 地址的归属地、网络属性与反向解析主机名。IPv6 使用 `::` 压缩写法也可直接查询；地址不合法时返回无效提示。

地址属性按以下类别判定并展示：`global`、`private`、`reserved`、`multicast`、`link_local`、`loopback`、`unspecified`、`site_local`、`ipv4_mapped`、`sixtofour`、`teredo`，无法归类时显示未知。`ipv4_mapped` 与 `sixtofour` 会额外显示嵌入的 IPv4 地址。私有、保留、回环、链路本地、未指定地址跳过归属地查询与反向解析，只展示地址类型。在 KOOK、QQ、QQBot 平台上，归属地为 Hong Kong、Macao、Taiwan 时统一显示为 China；其他平台按查询结果原值显示。

<ChatExample
  :log="[
    '用户：~ip 8.8.8.8',
    '机器人：8.8.8.8',
    '类型：IPv4全局地址',
    '位置：Mountain View, California, United States (97.822°W, 37.751°N)',
  ]"
/>
