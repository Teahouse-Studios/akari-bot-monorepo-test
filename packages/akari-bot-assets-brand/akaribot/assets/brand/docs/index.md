# 品牌资源

本文介绍品牌资源包的内容、安装方式、文档站点插槽与维护要求。

`akari-bot-assets-brand` 提供 AkariBot 的角色立绘、标志与制作人员名单。相关文件由画师提供，属于不可再生成的品牌资产，而非构建产物。

## 内容物

| 文件 | 用途 |
| --- | --- |
| `character_marked.png` | 角色立绘，用于 `~about` 等展示场景 |
| `akaribot_logo.png` | 日间标志，用于邮件报告、界面配图与文档站点 |
| `akaribot_logo_dark.png` | 夜间标志，用于深色模式的文档站点 |
| `akaribot_avatar.jpg` | 机器人头像，用于文档站点的命令对话示例 |
| `credits.txt` | 制作人员名单，包含主开发者、功能协助、画师与 Logo 设计 |
| `LICENSE` | 品牌资产许可证 |
| `manifest.toml` | 包说明清单。本包不是模块或适配器，无 registry 条目 |

## 安装与定位

```sh
uv pip install akari-bot-assets-brand
```

`akari-bot-core[full]` 已包含本包。`akaribot init` 默认安装该可选依赖组（extra）。指定 `--minimal` 时不安装本包。

包内仅导出一个函数：

```python
from akaribot.assets.brand import brand_dir

path = brand_dir() / "character_marked.png"
```

`brand_dir()` 返回本包资源的根目录。core 的 `find_brand_asset(name)` 按“资源包 → 实例 `assets/`”的顺序查找。

资源包与实例 `assets/` 均无同名文件时，`find_brand_asset()` 返回 `None`，由调用方降级处理。`~about` 缺失图片不会导致整条命令失败，SMTP 报告缺少标志时也正常发送。实例 `assets/` 中的同名文件会覆盖包内资产，便于部署者自定义立绘与标志。

## 文档站点的品牌插槽

文档引擎将品牌资源拆分为五个插槽。插槽可由品牌包提供，亦可由实例配置予以覆盖。

| 插槽 | 用途 | 未提供时 |
| --- | --- | --- |
| `logo` | 日间标志，用于顶栏、侧栏、页脚与首页 | 使用内置的日间标志 |
| `logo_dark` | 夜间标志，用于深色模式的同一组位置 | 使用内置的夜间标志 |
| `avatar` | 命令对话示例的机器人头像 | 使用内置的日间标志 |
| `character` | 角色立绘 | 使用内置的占位图 |
| `credits` | 制作人员文本 | 留空 |

### 由品牌包提供

品牌包在自己的 `docs/config/global/docs.global.toml` 中声明 `brand = true`，并声明五个字段。字段值是相对包根目录的文件路径。

```toml
brand = true

logo = "akaribot_logo.png"
logo_dark = "akaribot_logo_dark.png"
avatar = "akaribot_avatar.jpg"
character = "character_marked.png"
credits = "credits.txt"
```

文档引擎在已安装的文档包中寻找首个 `brand = true` 的提供者。路径必须位于包目录内，指向包目录之外的路径会被拒绝并发出警告。

旧包未声明 `brand` 字段时，引擎仍兼容首个声明 `logo` 或 `avatar` 的包。显式声明 `brand = true` 的包始终优先。

### 由实例覆盖

实例可在 `docs.toml` 的 `[site]` 中逐项覆盖插槽。相对路径按实例根目录解析。

```toml
[site]
logo = "assets/logo.png"
logo_dark = "assets/logo-dark.png"
avatar = "assets/avatar.jpg"
character = "assets/character.png"
credits = "assets/credits.txt"
```

覆盖顺序固定为：

1. `docs.toml` 的 `[site]` 字段
2. 品牌包声明的字段
3. 内置资源

任意一层缺失时继续向后查找。品牌包未安装，或安装后未声明特定字段，均不会导致构建失败。

### 主题接口

生成器将最终结果写入 `themeConfig.akari.brand`。自定义主题与页面组件可直接读取该对象。

```json
{
  "akari": {
    "brand": {
      "logo": "/brand-logo.png",
      "logoDark": "/brand-logo-dark.png",
      "avatar": "/brand-avatar.jpg",
      "character": "/brand-character.png",
      "credits": "/brand-credits.txt"
    }
  }
}
```

`akari.appBar.logo`、`akari.appBar.logoDark` 与 `akari.chatAvatar` 是兼容字段，值分别与 `logo`、`logoDark`、`avatar` 相同。内置顶栏、侧栏、页脚与首页通过 `useBrandAsset()` 读取插槽，外部组件读取 `themeConfig.akari.brand` 即可。

深色模式是否生效由主题的明暗状态确定。首页、顶栏、侧栏与页脚会在切换明暗时重新选择 `logo` 或 `logoDark`，主题选取颜色也会重新采样当前标志。

### 内置回退

未安装品牌包时，生成器将 CLI 自带素材复制到站点：

| 插槽 | 回退文件 |
| --- | --- |
| `logo` | `/brand-logo.png` |
| `logo_dark` | `/brand-logo-dark.png` |
| `avatar` | `/brand-avatar.png` |
| `character` | `/brand-character.png` |
| `credits` | 空字符串 |

回退不依赖 `akari-bot-assets-brand`，文档站点仍能正常显示。需要品牌立绘或完整制作人员名单时再安装品牌包。

## 许可证

立绘由 OasisAkari 提供，标志由 SAWARATSUKI 提供，二者保留全部权利，许可证保存在同目录下的 `LICENSE` 文件中。本包**不是** AGPL-3.0，与本仓库主体不同。分发时必须原样携带 `LICENSE`，不得套用仓库根目录许可证，亦不得将资产单独重新分发。

## 不得重新编码

立绘与标志必须保持画师交付的原件：

- 不得为压缩体积而重新压缩、降采样或转换格式。降采样或转调色板会导致画面明显模糊。
- 需要控制体积或显示尺寸时，调整使用方的展示宽度或缩放，而不是修改文件本身。
- 包内测试会核对资产与许可证齐全、立绘保持原件规格、标志可解码且非空。替换文件前先确认上述要求仍成立。

新增品牌资产时，将原件放入本目录，并在 `LICENSE` 或 `credits.txt` 中补充来源与授权说明。
