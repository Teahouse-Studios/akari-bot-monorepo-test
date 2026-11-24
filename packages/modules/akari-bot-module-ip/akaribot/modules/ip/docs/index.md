# ip

此模块用于查询 IPv4 或 IPv6 地址的类型、归属地与网络属性，并尝试执行反向 DNS 解析。返回结果包含国家、地区、城市、经纬度、邮编、组织、ASN、UTC 偏移与反向解析主机名。

## 命令

### `ip`

<CommandUsage usage="ip <ip_address>" :params="['ip_address=IPv4 或 IPv6 地址']" permission="public" />

此命令查询地址的归属地、网络属性与反向解析主机名。IPv6 地址使用 `::` 压缩写法也可以直接查询。若地址不合法，将返回无效提示。

地址属性按照 `global`、`private`、`reserved`、`multicast`、`link_local`、`loopback`、`unspecified`、`site_local`、`ipv4_mapped`、`sixtofour`、`teredo` 等类别判定并展示。若无法归入任何类别，则显示为未知。`ipv4_mapped` 与 `sixtofour` 会额外展示内嵌的 IPv4 地址。

私有、保留、回环、链路本地与未指定地址将跳过归属地查询与反向解析，仅展示地址类型。在 KOOK、QQ 与 QQBot 平台上，归属地若为 Hong Kong、Macao 或 Taiwan，统一显示为 China。在其他平台上按照查询结果原样展示。

<ChatExample
  :log="[
    '用户：~ip 8.8.8.8',
    '机器人：8.8.8.8',
    '类型：IPv4全局地址',
    '位置：Mountain View, California, United States (97.822°W, 37.751°N)',
  ]"
/>
