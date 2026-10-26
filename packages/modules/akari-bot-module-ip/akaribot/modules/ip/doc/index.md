# IP 查询

查询 IPv4 或 IPv6 地址的类型、归属地与网络属性，并尝试做反向 DNS 解析。输出包含国家、地区、城市、经纬度、邮编、组织、ASN、UTC 偏移与反向解析主机名。

## 安装

```bash
akaribot module add akari-bot-module-ip
```

模块名为 `ip`，命令前缀为 `ip`，没有别名。

## 命令

| 命令 | 说明 |
| --- | --- |
| `ip <ip_address>` | 查询 IP 地址信息 |

IPv6 使用 `::` 压缩写法时，查询前会展开为完整地址。地址不合法时返回无效提示。

地址属性按以下类别判定并展示：`global`、`private`、`reserved`、`multicast`、`link_local`、`loopback`、`unspecified`、`site_local`、`ipv4_mapped`、`sixtofour`、`teredo`，无法归类时显示未知。`ipv4_mapped` 与 `sixtofour` 会额外显示嵌入的 IPv4 地址。私有、保留、回环、链路本地、未指定地址跳过归属地查询与反向解析，只展示地址类型。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 在 KOOK、QQ、QQBot 平台上，归属地为 Hong Kong、Macao、Taiwan 时统一显示为 China；其他平台按接口原值显示。
- 反向解析依赖运行环境的 DNS，解析失败只记录警告，不影响其余字段。

## 数据表

无。查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`。
- 归属地接口：`https://api.ip.sb/geoip/{ip}`。
- 反向解析：使用系统 `socket.getnameinfo`，不访问额外服务。
