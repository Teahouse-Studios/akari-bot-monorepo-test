---
title: 安装与开发
---

# wolframalpha：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-wolframalpha
```

安装后在会话中由管理员用 `module enable wolframalpha` 开启。

## 配置项

<ModuleConfig table="module_wolframalpha" />

唯一字段声明为敏感项，写入同一文件的 `module_wolframalpha_secret` 表。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `wolfram_alpha_appid` | str | 空 | WolframAlpha 的 AppID |

`manifest.toml` 将该字段登记为重复凭据检查字段。未填写时两个命令均抛出配置缺失错误。

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块声明支持语言为英语（`en_us`），未声明平台限制，所有已接入平台可用。`query` 的结果以图片消息发送。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `akari-bot-core` 与 `Pillow`。外部服务为 `http://api.wolframalpha.com/v1/simple` 与 `http://api.wolframalpha.com/v1/result`。
