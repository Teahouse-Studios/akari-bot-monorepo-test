---
title: 安装与开发
---

# hitokoto：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-hitokoto
```

模块名称与命令首词均为 `hitokoto`，别名为 `htkt` 与 `yiyan`。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。此模块未声明平台限制，所有已接入平台均可以正常使用。

此模块声明支持 `zh_cn` 与 `zh_tw` 两种语言。会话语言为 `zh_tw` 时，返回的文本字段先使用 langconv 转换为繁体中文后再行发送。返回内容包含链接，因此平台需要支持 URL 消息元素。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core` 与 `langconv==0.4.0`。一言 API 为 `https://v1.hitokoto.cn/`，用于获取句子。类型代码作为 `c` 参数传递。结果中的链接指向一言主页 `https://hitokoto.cn`。
