---
title: 安装与开发
---

# wordle：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-wordle
```

安装后在会话中由管理员用 `module enable wordle` 开启。

## 配置项

<ModuleConfig table="module_wordle" />

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `wordle_disable_image` | bool | false | 是否禁用图片并使用文本棋盘 |

启用后开局与每次提交都发送文本棋盘，不发送棋盘与键盘图片。

## 权限与平台能力

命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入平台可用。图片模式依赖 `akari-bot-assets-fonts` 提供的字体，开启 `wordle_disable_image` 时使用文本棋盘。花瓣奖励仅在实例开启花瓣系统时生效。

## 数据表

<ModuleData />

对局状态与冷却均保存在进程内。

## 依赖与外部服务

依赖 `akari-bot-core`、`akari-bot-assets-fonts`、`Pillow` 与 `attrs`。模块不使用外部数据接口；答案与可提交词表随包分发在 `assets/answers.txt` 与 `assets/words.txt`，词典链接指向剑桥词典网站。
