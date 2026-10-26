# 字体资源

`akari-bot-assets-fonts` 分发绘制图片所需的字体文件，避免把字体路径绑死在仓库的
`assets/fonts` 布局上。源码检出与 wheel 安装下资源根不同，调用方一律经定位函数取路径。

## 内容物

| 文件 | 用途 |
| --- | --- |
| `Noto Sans CJK Bold.otf` | 中文与符号的粗体渲染 |
| `Noto Sans CJK DemiLight.otf` | 中文与符号的细体渲染 |
| `Noto Sans Symbols2 Regular.ttf` | 符号补充字形 |
| `LICENSE` | SIL Open Font License 1.1 全文与来源说明 |
| `manifest.toml` | 分发自述清单；本包不是模块或适配器 |

## 安装与定位

需要绘制中文图片的模块（如 `cytoid`、`phigros`、`maimai`、`wordle`）在依赖里声明本包，安装
模块时一并装入。也可以单独安装：

```sh
uv pip install akari-bot-assets-fonts
```

```python
from akaribot.assets.fonts import fonts_dir

bold = fonts_dir() / "Noto Sans CJK Bold.otf"
```

`fonts_dir()` 返回包内资源根，不假定内部还有子目录。

## 查找顺序

core 的 `find_font(name)` 按三级查找：

1. 本资源包；
2. 实例 `data/fonts/`，供部署者自备字体；
3. 系统字体，按已知字族候选查找。

三级都取不到时抛出 `FontNotFoundError`，消息给出安装资源包、放入实例目录或安装系统字族三条修复
路径。Docker 镜像安装 `fonts-noto-cjk` 等系统字体作为第三级兜底，因此资源包缺席时图片仍可能
渲染成功；但缺少汉字字形的字族不会进入候选，以免中文渲染成方框。

## 维护约定

- 字体按原样分发，不重新编码、不做子集化；渲染兼容性依赖原始字形表。
- 新增字体时同时更新 `find_font` 的已知字族映射（`core/utils/font.py` 的 `SYSTEM_FAMILIES`），
  否则系统字体回退不会命中。
- 文件名是调用方传入 `find_font` 的键，改名会影响使用侧。
- `LICENSE` 必须随资源一同分发。

## 许可证

字体取自 [noto-cjk](https://github.com/googlefonts/noto-cjk) 与
[source-han-sans](https://github.com/adobe-fonts/source-han-sans)，版权归 Google, Inc. 与
Adobe, Inc. 所有，以 SIL Open Font License 1.1 授权。本包以 `OFL-1.1` 分发，与本仓库主体的
AGPL-3.0 不同；`LICENSE` 中的全文与来源说明必须保留。
