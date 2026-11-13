# nintendo-err

解析任天堂系列主机的报错码，返回对应的模块、摘要与说明，并附上官方支持页面链接（若有收录）。

## 命令

<ModuleAlias names="nintendo_err, err" />

### `nintendo-err`

<CommandUsage usage="nintendo-err <err_code>" :params="['err_code=报错码或结果码']" permission="public" />

解析任天堂系列主机的报错码或结果码，返回对应的模块、摘要与说明。`<err_code>` 接受 3DS 与 2DS 支持码、Wii U 支持码与结果码、Switch 错误码与 `2-BBBBB-CCCC` 应用错误码。

支持的输入形式：

- 3DS 与 2DS 的支持码，形如 `002-0102`。
- Wii U 的支持码与结果码。
- Switch 的错误码，形如 `2002-4153`，也接受 `0x` 开头的十六进制值与省略 `0x` 的十六进制值。
- Switch 的 `2-BBBBB-CCCC` 应用错误码，仅识别模块与说明，不做十六进制换算。

输入会先截断到 16 个字符。十六进制输入若省略 `0x`，会在可解析时补全为十六进制形式。`0xdeadbeef`、`0xdeadbabe` 与 `0x8badf00d` 三个彩蛋码返回固定文案，不进入解析流程。

解析成功时以嵌入卡片返回标题、补充说明与若干字段；无法识别或不属于受支持主机时返回无效提示。

<ChatExample
  :log="[
    '用户：~nintendo-err 011-3021',
    '机器人：011-3021 (Nintendo 2DS/3DS)',
    '分类：eshop (website?)',
    '描述：无法在eShop找到这个应用（错误的区域或者这个东西就根本不存在）',
  ]"
/>
