---
title: 安装与开发
---

# wordle：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-wordle
```

安装后，管理员需要在会话中执行 `module enable wordle` 启用模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入平台均可以使用。

图片模式依赖 `akari-bot-assets-fonts` 提供的字体。会话不支持图片时，每次提交与对局结束都以文本棋盘回复。花瓣奖励仅在实例启用花瓣系统时生效。

## 数据表

<ModuleData />

对局状态与冷却都保存在进程内。

## 依赖与外部服务

依赖 `akari-bot-core`、`akari-bot-assets-fonts`、`Pillow` 与 `attrs`。模块不使用外部数据接口。答案与可提交词表随包分发，位于 `assets/answers.txt` 与 `assets/words.txt`。词典链接指向剑桥词典网站。
