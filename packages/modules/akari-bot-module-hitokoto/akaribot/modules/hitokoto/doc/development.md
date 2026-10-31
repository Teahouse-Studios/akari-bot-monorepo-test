---
title: 安装与开发
---

# hitokoto：安装与开发

本页说明 `hitokoto` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-hitokoto
```

模块名为 `hitokoto`，命令前缀为 `hitokoto`，别名为 `htkt`、`yiyan`。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 也未声明配置表。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 声明支持语言为 `zh_cn`、`zh_tw`。会话语言为 `zh_tw` 时，返回的文本字段经 langconv 转换为繁体后再发送。
- 返回内容含链接，平台需支持 URL 消息元素。

## 数据表

无。不保存查询记录。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`langconv==0.4.0`。
- 一言 API：`https://v1.hitokoto.cn/`，用于获取句子。
- 一言主页：`https://hitokoto.cn`，作为结果链接。
