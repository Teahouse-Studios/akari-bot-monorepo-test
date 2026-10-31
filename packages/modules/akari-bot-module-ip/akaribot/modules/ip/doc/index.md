# ip

查询 IPv4 或 IPv6 地址的类型、归属地与网络属性，并尝试做反向 DNS 解析。输出包含国家、地区、城市、经纬度、邮编、组织、ASN、UTC 偏移与反向解析主机名。

## 命令

| 命令 | 说明 |
| --- | --- |
| `ip <ip_address>` | 查询 IP 地址信息 |

IPv6 使用 `::` 压缩写法时，查询前会展开为完整地址。地址不合法时返回无效提示。

地址属性按以下类别判定并展示：`global`、`private`、`reserved`、`multicast`、`link_local`、`loopback`、`unspecified`、`site_local`、`ipv4_mapped`、`sixtofour`、`teredo`，无法归类时显示未知。`ipv4_mapped` 与 `sixtofour` 会额外显示嵌入的 IPv4 地址。私有、保留、回环、链路本地、未指定地址跳过归属地查询与反向解析，只展示地址类型。
