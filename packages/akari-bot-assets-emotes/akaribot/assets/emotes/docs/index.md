# 表情资源

本文将会介绍表情资源包的内容、调用方与维护约定。

`akari-bot-assets-emotes` 分发 AkariBot 使用的表情 GIF，按场景分为三组。`akari-bot-core[full]` 默认安装本包。`akaribot init --minimal` 不安装本包，相关功能按默认行为降级。

## 内容物

| 目录 | 数量 | 用途 |
| --- | --- | --- |
| `common/` | 24 个 GIF | 对发送速率不敏感的场景，可保持较大体积 |
| `captcha_held/` | 25 个 GIF | 按钮验证码的表情模式，手持物作为答案依据 |
| `typing/` | 30 个 GIF | QQBot 群聊输入状态提示 |

表情素材由 [EmoteLab](https://emotelab.app/) 制作。`typing/` 为加快发送速度，缩小了尺寸并减少了帧数，单图上限约 500 KB。`common/` 没有这一限制。

## 安装与定位

```sh
uv pip install akari-bot-assets-emotes
```

```python
from akaribot.assets.emotes import emotes_dir

captcha = emotes_dir() / "captcha_held"
```

`emotes_dir()` 返回本包资源的根目录，`common`、`captcha_held`、`typing` 都在其下。

主要调用方：

- core 的错误钩子用 `common/` 为错误提示配图。
- `akari-bot-module-captcha` 用 `captcha_held/` 生成按钮验证码。
- `akari-bot-adapter-qqbot` 用 `typing/` 发送输入状态。

资源包缺失时，调用方跳过配图或输入状态，不阻断命令本身。

## 维护约定

- 新增或替换 GIF 时，请保持各目录的用途不变。验证码素材必须能通过手持物区分答案，输入状态素材必须控制单图体积与帧数。
- 文件名是调用方拼接的资源名，改名会影响调用方。调整前请先搜索 `emotes_dir()` 的调用位置。
- 表情是二进制资源，不通过代码生成。仓库不会为了压缩体积统一转码，各目录按自身的发送速率要求处理。

## 许可证

本包以 AGPL-3.0 分发，许可证文件为包根的 `LICENSE`。表情制作来源见包内 `README.md`。再分发或修改素材时保留该说明。
