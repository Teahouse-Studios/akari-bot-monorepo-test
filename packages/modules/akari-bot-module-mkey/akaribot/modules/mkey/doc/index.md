# mkey

根据主机类型、日期与确认代码计算任天堂系列主机的监护管理万能密码。

## 命令

### `mkey`

<CommandUsage usage="mkey <device> <month> <day> <inquiry_num> [<device_id>]" :params="['device=主机类型，如 3ds 或 switch', 'month=月份，取值 1 至 12', 'day=日期，取值 1 至 31', 'inquiry_num=6、8 或 10 位确认代码', 'device_id=Switch 的 16 位主机 ID']" permission="public" />

计算监护管理万能密码。`device` 不区分大小写，可选值如下：

- `3ds`：Nintendo 3DS
- `dsi`：Nintendo DSi
- `wii`：Wii
- `wiiu`：Wii U
- `switch`：Nintendo Switch

`month` 取 1 至 12，`day` 取 1 至 31；`inquiry_num` 为 6、8 或 10 位十进制确认代码，取值越界或长度不符时返回对应错误提示。`switch` 必须提供 `device_id`，按 16 位十六进制字符串解析，缺少时单独提示。

8 位确认代码的结果为 5 位数字；10 位确认代码与 Switch 的 6 位确认代码的结果为 8 位数字。6 位确认代码只适用于 Switch。
