# 任天堂监护密码

根据主机类型、日期与确认代码计算任天堂系列主机的监护管理万能密码。模块名 `mkey`，无别名。

## 安装

```bash
akaribot module add akari-bot-module-mkey
```

安装后在会话中由管理员用 `module enable mkey` 开启。

## 命令

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mkey <device> <month> <day> <inquiry_num> [<device_id>]` | 计算万能密码 | 所有用户 |

`device` 不区分大小写，取值如下：

| 值 | 主机 | 内部代号 |
| --- | --- | --- |
| `3ds` | Nintendo 3DS | CTR |
| `dsi` | Nintendo DSi | TWL |
| `wii` | Wii | RVL |
| `wiiu` | Wii U | WUP |
| `switch` | Nintendo Switch | HAC |

`month` 取 1 至 12，`day` 取 1 至 31。`inquiry_num` 为 6、8 或 10 位十进制确认代码。`switch`
必须额外提供 `device_id`，生成器按 16 位十六进制字符串解析该参数。

3DS、DSi、Wii 与 Wii U 的结果为 5 位数字，Switch 的结果为 8 位数字。月份、日期、主机类型或确认
代码长度不合法时返回对应错误提示；Switch 缺少主机 ID 时单独提示。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 命令未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 计算完全在本地完成，不依赖网络或平台能力。

## 数据表

无。manifest 未声明 `owned_tables`，计算过程不读写数据库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`pycryptodome>=3.18.0,<4.0.0`。
- 不访问外部服务。密钥数据位于包内 `assets/data`，manifest 声明 `assets = "assets"`。
