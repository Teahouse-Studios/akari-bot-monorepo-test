# 颜色信息

解析颜色代码，返回十六进制、RGB、HSL 三种表示，以及最接近的 CSS 与 Material Design 颜色名称，
并附一张包含全部信息的色卡图片。

模块名 `color`，别名 `colour`。

## 安装

```bash
akaribot module add akari-bot-module-color
```

安装后在会话中由管理员用 `module enable color` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `color [<color>]` | 解析颜色并返回色值；省略参数时随机取色 | 所有用户 |

支持的输入形式（完整名称表见[颜色名称表](colors.md)）：

- CSS 颜色名，如 `rebeccapurple`、`cornflowerblue`。
- Material Design 颜色名，如 `red-500`、`bluegrey-200`。
- 十六进制，3 位或 6 位，可省略 `#`，如 `#f00`、`336699`。
- `rgb(255, 0, 0)` 与百分比形式 `rgb(100%, 0%, 0%)`。
- `hsl(0, 100%, 50%)` 与带角度单位的形式 `hsl(0deg, 100%, 50%)`。

无法识别的格式返回格式错误提示。颜色名与 Material Design 名称需要精确命中，十六进制中的字母
不区分大小写。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 输出为 Embed，含 HEX、RGB、HSL 三个字段与两个颜色名字段；仅在颜色名与色值完全一致时使用
  「颜色名称」，否则标注为「最相似的」名称。
- 色卡文字使用资源包字体 Noto Sans CJK DemiLight，文字颜色按背景亮度在黑与白之间切换。
- Material Design 名称表随包分发在 `assets/material_colors.json`。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

- 依赖：`Pillow`、`numpy`、`webcolors`、`orjson`、`akari-bot-assets-fonts`、`akari-bot-core`。
- 不使用外部网络服务，颜色名称表全部随包或随依赖分发。
