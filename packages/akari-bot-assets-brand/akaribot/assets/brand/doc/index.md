# 品牌资源

`akari-bot-assets-brand` 分发 AkariBot 的角色立绘、标志与制作人员名单。这些文件由画师提供，
属于不可再生成的品牌资产，不属于构建产物。

## 内容物

| 文件 | 用途 |
| --- | --- |
| `character_marked.png` | 角色立绘，用于 `~about` 等展示场景 |
| `akaribot_logo.png` | 标志，用于邮件报告与界面配图 |
| `credits.txt` | 制作人员名单，含主开发者、功能协助、画师与 Logo 设计 |
| `LICENSE` | 品牌资产许可证 |
| `manifest.toml` | 分发自述清单；本包不是模块或适配器，没有 registry 条目 |

## 安装与定位

```sh
uv pip install akari-bot-assets-brand
```

`akari-bot-core[full]` 已包含本包，`akaribot init` 默认安装该 extra；`--minimal` 不安装。

包内只暴露一个定位函数：

```python
from akaribot.assets.brand import brand_dir

path = brand_dir() / "character_marked.png"
```

`brand_dir()` 返回包内资源根。core 的 `find_brand_asset(name)` 按「资源包 → 实例 `assets/`」的
顺序查找，两处都没有时返回 `None`，由调用方降级：`~about` 少一张图不会让整条命令失败，SMTP
报告没有标志也照常发送。实例 `assets/` 中的同名文件可以覆盖包内资产，供部署者替换标志。

## 许可证

立绘由 OasisAkari 提供，标志由 SAWARATSUKI 提供，二者保留全部权利，许可证写在同目录的
`LICENSE` 中。本包**不是** AGPL-3.0，与本仓库主体不同；分发包必须原样携带 `LICENSE`，不得套用
仓库根许可证，也不得把资产单独再分发。

## 不得重新编码

立绘与标志必须保持画师交付的原件：

- 不得为压体积重新压缩、降采样或转换格式；降采样或转调色板会让画面明显变糊。
- 需要控制体积或显示尺寸时，调整使用侧的展示宽度或缩放，而不是改文件本身。
- 包内测试会核对三份资产与许可证齐全、立绘保持原件规格、标志可解码且非空；替换文件前先确认
  这些约束仍成立。

新增品牌资产时，把原件放入本目录并在 `LICENSE` 或 `credits.txt` 中补齐来源与授权说明。
