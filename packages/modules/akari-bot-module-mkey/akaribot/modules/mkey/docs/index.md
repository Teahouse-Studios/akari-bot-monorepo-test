# mkey

此模块用于计算任天堂系列主机的监护管理万能密码。密码通过主机类型、日期与确认代码计算得出。

## 命令

### `mkey`

<CommandUsage usage="mkey <device> <month> <day> <inquiry_num> [<device_id>]" :params="['device=主机类型，如 3ds 或 switch', 'month=月份，取值 1 至 12', 'day=日期，取值 1 至 31', 'inquiry_num=6、8 或 10 位确认代码', 'device_id=Switch 的 16 位主机 ID']" permission="public" />

此命令用于计算监护管理万能密码。`device` 不区分大小写，可选值包含：

- `3ds`：Nintendo 3DS
- `dsi`：Nintendo DSi
- `wii`：Wii
- `wiiu`：Wii U
- `switch`：Nintendo Switch

- `month` 取值范围为 1 到 12，`day` 取值范围为 1 到 31，取值越界时返回对应的错误提示。
- `inquiry_num` 为 6、8 或 10 位十进制确认代码，长度不符时返回错误提示。
- `switch` 必须提供 `device_id`，该参数按 16 位十六进制字符串解析。缺少 `device_id` 时单独提示。

8 位确认代码计算得出 5 位密码，10 位确认代码计算得出 8 位密码。6 位确认代码仅适用于 Switch，同样计算得出 8 位密码。

<ChatExample
  :log="[
    '用户：~mkey 3ds 1 1 12345678',
    '机器人：你的万能密码是：64838。',
  ]"
/>
