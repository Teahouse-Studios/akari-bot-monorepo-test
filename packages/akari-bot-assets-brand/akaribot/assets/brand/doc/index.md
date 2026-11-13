# 品牌资源

本文将会介绍品牌资源包的内容、安装方式与维护要求。

`akari-bot-assets-brand` 提供 AkariBot 的角色立绘、标志与制作人员名单。这些文件由画师提供，属于不可再生成的品牌资产，不是构建产物。

## 内容物

| 文件 | 用途 |
| --- | --- |
| `character_marked.png` | 角色立绘，用于 `~about` 等展示场景 |
| `akaribot_logo.png` | 标志，用于邮件报告、界面配图与文档站点顶栏 |
| `akaribot_avatar.jpg` | 机器人头像，用于文档站点的命令对话示例 |
| `credits.txt` | 制作人员名单，含主开发者、功能协助、画师与 Logo 设计 |
| `LICENSE` | 品牌资产许可证 |
| `manifest.toml` | 分发自述清单。本包不是模块或适配器，没有 registry 条目 |

## 安装与定位

```sh
uv pip install akari-bot-assets-brand
```

`akari-bot-core[full]` 已包含本包。`akaribot init` 默认会安装这个 extra。使用 `--minimal` 时不安装本包。

包内只暴露一个定位函数：

```python
from akaribot.assets.brand import brand_dir

path = brand_dir() / "character_marked.png"
```

`doc/doc.toml` 的 `logo` 指向 `akaribot_logo.png`，`avatar` 指向 `akaribot_avatar.jpg`，文档引擎据此把标志与对话头像设为站点素材。实例在 `docs.toml` 里配置 `site.logo` 或 `site.avatar` 时，以实例配置为准。

`brand_dir()` 返回本包资源的根目录。core 的 `find_brand_asset(name)` 按“资源包 → 实例 `assets/`”的顺序查找。

资源包与实例 `assets/` 都没有同名文件时，`find_brand_asset()` 返回 `None`，由调用方降级处理。`~about` 少一张图不会让整条命令失败，SMTP 报告缺少标志时也照常发送。实例 `assets/` 中的同名文件会覆盖包内资产，供部署者替换标志。

## 许可证

立绘由 OasisAkari 提供，标志由 SAWARATSUKI 提供，二者保留全部权利，许可证写在同目录的 `LICENSE` 中。本包**不是** AGPL-3.0，与本仓库主体不同。分发包必须原样携带 `LICENSE`，不得套用仓库根许可证，也不得把资产单独再分发。

## 不得重新编码

立绘与标志必须保持画师交付的原件：

- 不得为压缩体积而重新压缩、降采样或转换格式。降采样或转调色板会让画面明显变糊。
- 需要控制体积或显示尺寸时，调整使用侧的展示宽度或缩放，而不是改文件本身。
- 包内测试会核对三份资产与许可证齐全、立绘保持原件规格、标志可解码且非空。替换文件前先确认这些要求仍成立。

新增品牌资产时，把原件放入本目录，并在 `LICENSE` 或 `credits.txt` 中补齐来源与授权说明。
