# 任天堂报错码

解析任天堂系列主机的报错码，返回对应的模块、摘要与说明，并附上官方支持页面链接（若有收录）。

模块名 `nintendo-err`，别名 `nintendo_err`、`err`。

## 安装

```bash
akaribot module add akari-bot-module-nintendo_err
```

安装后在会话中由管理员用 `module enable nintendo-err` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `nintendo-err <err_code>` | 解析报错码或结果码 | 所有用户 |

支持的输入形式：

- 3DS 与 2DS 的支持码，形如 `002-0102`。
- Wii U 的支持码与结果码。
- Switch 的错误码，形如 `2002-4153`，也接受 `0x` 开头的十六进制值与省略 `0x` 的十六进制值。
- Switch 的 `2-BBBBB-CCCC` 应用错误码，仅能识别模块与说明，不进行十六进制换算。

输入会先截断到 16 个字符。十六进制输入若省略 `0x`，会在可解析时补全为十六进制形式。`0xdeadbeef`、`0xdeadbabe` 与 `0x8badf00d` 三个彩蛋码返回固定文案，不进入解析流程。

解析成功时以嵌入卡片返回标题、补充说明与若干字段；无法识别或不属于受支持主机时返回无效提示。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 结果以嵌入卡片发出，字段名与说明文本按收录数据原样展示。

## 数据表

无。manifest 未声明 `owned_tables`，报错码表随包内 Python 模块分发，查询结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`py-cord`。
- 不使用外部网络服务；报错码数据来自包内 `ctr_support.py`、`ctr_results.py`、`wiiu_support.py`、`wiiu_results.py` 与 `switch.py`。
