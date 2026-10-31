---
title: 安装与开发
---

# wolframalpha：安装与开发

本页说明 `wolframalpha` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-wolframalpha
```

安装后在会话中由管理员用 `module enable wolframalpha` 开启。

## 配置项

manifest 声明配置表为 `module_wolframalpha`；字段为敏感项，实际写入 `module_wolframalpha_secret`（`config/module_wolframalpha_secret.toml`）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `wolfram_alpha_appid` | str | 空 | WolframAlpha 的 AppID |

`manifest.toml` 将该字段登记为重复凭据检查字段。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 模块声明支持语言为英语（`en_us`）。
- 未声明平台限制，所有已接入平台可用。
- `query` 的结果以图片消息发送。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`、`Pillow`。
- 外部服务：`http://api.wolframalpha.com/v1/simple` 与 `http://api.wolframalpha.com/v1/result`。
