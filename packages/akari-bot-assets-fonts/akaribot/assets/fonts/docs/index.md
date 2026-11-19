# 字体资源

本文将会介绍字体资源包的内容、查找顺序与维护约定。

`akari-bot-assets-fonts` 提供绘制图片所需的字体文件，避免调用方依赖仓库里 `assets/fonts` 的固定路径。源码检出与 wheel 安装时，字体所在目录不同，调用方一律用 `fonts_dir()` 取路径。

## 内容物

| 文件 | 用途 |
| --- | --- |
| `Noto Sans CJK Bold.otf` | 中文与符号的粗体渲染 |
| `Noto Sans CJK DemiLight.otf` | 中文与符号的细体渲染 |
| `Noto Sans Symbols2 Regular.ttf` | 符号补充字形 |
| `LICENSE` | SIL Open Font License 1.1 全文与来源说明 |
| `manifest.toml` | 分发自述清单。本包不是模块或适配器 |

## 安装与定位

需要绘制中文图片的模块（如 `cytoid`、`phigros`、`maimai`、`wordle`）在依赖里声明本包，安装模块时一并装入。也可以单独安装：

```sh
uv pip install akari-bot-assets-fonts
```

```python
from akaribot.assets.fonts import fonts_dir

bold = fonts_dir() / "Noto Sans CJK Bold.otf"
```

`fonts_dir()` 返回本包资源的根目录，调用方不要假定其中还有子目录。

## 查找顺序

core 的 `find_font(name)` 按三级查找：

1. 本资源包。
2. 实例 `data/fonts/`，供部署者自备字体。
3. 系统字体，按已知字族候选查找。

三级都取不到时，`find_font` 抛出 `FontNotFoundError`。异常消息里给出三种修复方式：安装资源包、把字体放进实例目录、安装系统字族。

Docker 镜像已安装 `fonts-noto-cjk` 等系统字体，第三级可以命中。因此即使没有安装资源包，图片仍可能渲染成功。缺少汉字字形的字族不会进入候选，以免中文渲染成方框。

## 维护约定

- 字体按原样分发，不重新编码，也不做子集化。渲染兼容性依赖原始字形表。
- 新增字体时同时更新 `find_font` 的已知字族映射（`core/utils/font.py` 的 `SYSTEM_FAMILIES`）。否则系统字体这一级查不到。
- `find_font` 按文件名查找字体，改名会影响所有调用方。
- `LICENSE` 必须随资源一同分发。

## 许可证

字体取自 [noto-cjk](https://github.com/googlefonts/noto-cjk) 与 [source-han-sans](https://github.com/adobe-fonts/source-han-sans)，版权归 Google, Inc. 与 Adobe, Inc. 所有，按 SIL Open Font License 1.1 授权。本包的许可证是 `OFL-1.1`，与本仓库主体的 AGPL-3.0 不同。`LICENSE` 中的全文与来源说明必须保留。
