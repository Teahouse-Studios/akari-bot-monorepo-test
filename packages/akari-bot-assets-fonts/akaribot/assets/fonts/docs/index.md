# 字体资源

`akari-bot-assets-fonts` 提供绘制图片所需的字体文件，避免调用方依赖仓库里 `assets/fonts` 的固定路径。克隆仓库与 wheel 安装时，字体所在目录不同，调用方一律使用 `fonts_dir()` 获取路径。

## 内容物

| 文件 | 用途 |
| --- | --- |
| `Noto Sans CJK Bold.otf` | 中文与符号的粗体渲染 |
| `Noto Sans CJK DemiLight.otf` | 中文与符号的细体渲染 |
| `Noto Sans Symbols2 Regular.ttf` | 符号补充字形 |
| `LICENSE` | SIL Open Font License 1.1 全文与来源说明 |
| `manifest.toml` | 包说明清单。本包不是模块或适配器 |

## 安装与定位

需要绘制中文图片的模块（如 `cytoid`、`phigros`、`maimai`、`wordle`）在依赖中声明本包，安装模块时一并安装。亦可单独安装：

```sh
uv pip install akari-bot-assets-fonts
```

```python
from akaribot.assets.fonts import fonts_dir

bold = fonts_dir() / "Noto Sans CJK Bold.otf"
```

`fonts_dir()` 返回本包资源的根目录，调用方不得假定其中包含子目录。

## 查找顺序

core 的 `find_font(name)` 按三级查找：

1. 本资源包。
2. 实例 `data/fonts/`，供部署者自备字体。
3. 系统字体，按已知字族候选查找。

三级均未找到时，`find_font` 抛出 `FontNotFoundError`。异常消息中列出安装资源包、将字体放入实例目录、安装系统字族三种解决方案。

Docker 镜像已安装 `fonts-noto-cjk` 等系统字体，第三级可命中。因此即使未安装资源包，图片仍可能渲染成功。缺少汉字字形的字族不会进入候选，以避免中文被渲染为方框。

## 维护约定

- 字体按原样分发，不重新编码，也不子集化。渲染兼容性依赖原始字形表。
- 新增字体时同时更新 `find_font` 的已知字族映射（`core/utils/font.py` 的 `SYSTEM_FAMILIES`）。否则系统字体该层级无法查询到。
- `find_font` 按文件名查找字体，重命名会影响所有调用方。
- `LICENSE` 必须随资源一同分发。

## 许可证

字体取自 [noto-cjk](https://github.com/googlefonts/noto-cjk) 与 [source-han-sans](https://github.com/adobe-fonts/source-han-sans)，版权归 Google, Inc. 与 Adobe, Inc. 所有，按 SIL Open Font License 1.1 授权。本包的许可证是 `OFL-1.1`，与本仓库主体的 AGPL-3.0 不同。`LICENSE` 中的全文与来源说明必须保留。
