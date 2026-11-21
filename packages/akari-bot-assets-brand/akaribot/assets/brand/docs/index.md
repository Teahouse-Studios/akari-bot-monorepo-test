# 品牌资源

本文介绍品牌资源包的内容、安装方式、文档站点插槽与维护要求。

`akari-bot-assets-brand` 提供 AkariBot 的角色立绘、标志与制作人员名单。这些文件由画师提供，属于不可再生成的品牌资产，不是构建产物。

## 内容物

| 文件 | 用途 |
| --- | --- |
| `character_marked.png` | 角色立绘，用于 `~about` 等展示场景 |
| `akaribot_logo.png` | 日间标志，用于邮件报告、界面配图与文档站点 |
| `akaribot_logo_dark.png` | 夜间标志，用于深色模式的文档站点 |
| `akaribot_avatar.jpg` | 机器人头像，用于文档站点的命令对话示例 |
| `credits.txt` | 制作人员名单，含主开发者、功能协助、画师与 Logo 设计 |
| `LICENSE` | 品牌资产许可证 |
| `manifest.toml` | 分发自述清单。本包不是模块或适配器，没有 registry 条目 |

## 安装与定位

```sh
uv pip install akari-bot-assets-brand
```

`akari-bot-core[full]` 已包含本包。`akaribot init` 默认会安装这个 extra。使用 `--minimal` 时不安装本包。

包内只暴露一个函数：

```python
from akaribot.assets.brand import brand_dir

path = brand_dir() / "character_marked.png"
```

`brand_dir()` 返回本包资源的根目录。core 的 `find_brand_asset(name)` 按“资源包 → 实例 `assets/`”的顺序查找。

资源包与实例 `assets/` 都没有同名文件时，`find_brand_asset()` 返回 `None`，由调用方降级处理。`~about` 少一张图不会让整条命令失败，SMTP 报告缺少标志时也照常发送。实例 `assets/` 中的同名文件会覆盖包内资产，供部署者替换标志。

## 文档站点的品牌插槽

文档引擎把品牌资源拆成五个插槽。插槽可以来自品牌包，也可以由实例配置覆盖。

| 插槽 | 用途 | 未提供时 |
| --- | --- | --- |
| `logo` | 日间标志，用于顶栏、侧栏、页脚与首页 | 使用内置的日间标志 |
| `logo_dark` | 夜间标志，用于深色模式的同一组位置 | 使用内置的夜间标志 |
| `avatar` | 命令对话示例的机器人头像 | 使用内置的日间标志 |
| `character` | 角色立绘 | 使用内置的占位图 |
| `credits` | 制作人员文本 | 留空 |

### 由品牌包提供

品牌包在自己的 `docs/config/global/docs.global.toml` 中声明 `brand = true`，并给出五个字段。字段值是相对包根目录的文件路径。

```toml
brand = true

logo = "akaribot_logo.png"
logo_dark = "akaribot_logo_dark.png"
avatar = "akaribot_avatar.jpg"
character = "character_marked.png"
credits = "credits.txt"
```

文档引擎在已安装的文档包中寻找第一个 `brand = true` 的提供者。路径必须留在包目录内，指向包目录之外的路径会被拒绝并给出警告。

旧包没有 `brand` 字段时，引擎仍兼容第一个声明 `logo` 或 `avatar` 的包。显式声明 `brand = true` 的包始终优先。

### 由实例覆盖

实例可以在 `docs.toml` 的 `[site]` 中逐项覆盖插槽。相对路径按实例根解析。

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

任意一层缺失时继续向后查找。品牌包没有安装，或者安装后没有声明某个字段，都不会让构建失败。

### 主题接口

生成器把最终结果写入 `themeConfig.akari.brand`。自定义主题与页面组件可以直接读取这个对象。

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

`akari.appBar.logo`、`akari.appBar.logoDark` 与 `akari.chatAvatar` 是兼容字段，值分别与 `logo`、`logoDark`、`avatar` 相同。内置顶栏、侧栏、页脚与首页通过 `useBrandAsset()` 读取插槽，外部组件读 `themeConfig.akari.brand` 即可。

深色模式是否生效由主题的明暗状态决定。首页、顶栏、侧栏与页脚会在切换明暗时重新选择 `logo` 或 `logoDark`，主题取色也会重新采样当前标志。

### 内置回退

没有品牌包时，生成器把 CLI 自带素材复制到站点：

| 插槽 | 回退文件 |
| --- | --- |
| `logo` | `/brand-logo.png` |
| `logo_dark` | `/brand-logo-dark.png` |
| `avatar` | `/brand-avatar.png` |
| `character` | `/brand-character.png` |
| `credits` | 空字符串 |

回退不依赖 `akari-bot-assets-brand`，文档站点仍能正常显示。需要品牌立绘或完整制作人员名单时再安装品牌包。

## 许可证

立绘由 OasisAkari 提供，标志由 SAWARATSUKI 提供，二者保留全部权利，许可证写在同目录的 `LICENSE` 中。本包**不是** AGPL-3.0，与本仓库主体不同。分发包必须原样携带 `LICENSE`，不得套用仓库根许可证，也不得把资产单独再分发。

## 不得重新编码

立绘与标志必须保持画师交付的原件：

- 不得为压缩体积而重新压缩、降采样或转换格式。降采样或转调色板会让画面明显变糊。
- 需要控制体积或显示尺寸时，调整使用侧的展示宽度或缩放，而不是改文件本身。
- 包内测试会核对资产与许可证齐全、立绘保持原件规格、标志可解码且非空。替换文件前先确认这些要求仍成立。

新增品牌资产时，把原件放入本目录，并在 `LICENSE` 或 `credits.txt` 中补齐来源与授权说明。
