# html2text

`akari-bot-html2text` 是 AkariBot 维护的 HTML 转 Markdown 文本库，独立分发，供模块离线转换网页正文时调用。它基于上游 `html2text==2020.1.16`，包内 `__version__` 同为 `(2020, 1, 16)`。

## 输入与输出

输入是 HTML 字符串，输出是 Markdown 风格的纯文本。此库只依赖标准库，不访问网络。

```python
from html2text import HTML2Text, html2text

text = html2text("<h1>标题</h1><p>正文</p>")

parser = HTML2Text(bodywidth=0)
parser.ignore_links = True
text = parser.handle("<p><a href=\"https://example.com\">链接</a></p>")
```

- `html2text(html, baseurl="", bodywidth=None, url_formatter=str)`：一次完成转换的快捷函数。
- `HTML2Text(out=None, baseurl="", bodywidth=..., url_formatter=str)`：你可以先设置 `ignore_links`、`ignore_images`、`pad_tables` 等属性，再调用 `handle()`。也可以分次调用 `feed()` 传入片段，最后调用 `finish()`。
- `url_formatter`：处理每个链接和图片 URL 的函数。默认值 `str` 表示不做加工。

对应的命令行入口：

```sh
python -m html2text page.html
python -m html2text --ignore-links --body-width 0 page.html
```

不写文件名或传入 `-` 时，命令从标准输入读取。第二个位置参数是编码，默认 `utf-8`。`--ignore-links`、`--reference-links`、`--ignore-images`、`--body-width`、`--pad-tables`、`--no-wrap-links` 等选项与上游一致。

## 与上游的差异

以下行为与上游 2020.1.16 不同，使用时须按下面的说明处理：

- **链接 title 被丢弃**：`link_url()` 不输出 `](url "标题")` 中的 title。开启链接输出时只能得到 URL 本身，不要依赖 title 生成引用或脚注。
- **`</script>` 处理**：本包把结束标签的转义写法改成了真正的 `</script>`，随后又替换成 `</ignore>`，`HTMLParser` 因此无法退出 script 的 CDATA 模式，第一个 `<script>` 之后的正文会丢失。含脚本的 HTML 应先移除 `<script>` 块，再交给此库。
- **URL 解耦**：不依赖 `akaribot.core` 的 `Url` 类型，改为通过 `url_formatter` 传入处理函数。行内链接、图片 alt、图片 URL 和引用式链接定义都会调用它。
- **`assert` 检查移除**：内部 `assert ... is not None` 已删除。输入异常时，抛出的异常可能是 `TypeError` 或 `AttributeError`，而不是 `AssertionError`。
- **类型与格式**：`OutCallback` 的方法体改为 `raise NotImplementedError`，类型注解改用内建泛型，部分辅助函数经过语义等价的改写。

本分支尚未合并上游 2024 与 2025 版本。如果需要 2025 版的行为，例如保留链接 title，就不应把本包当作上游的替代品。

## 使用边界

- 此库只负责把网页正文转成便于阅读的 Markdown，不做 HTML 清洗。输入不可信时，请先做白名单过滤。
- 页面含 `<script>`，或依赖链接 title 时，需要先预处理，或改用其他渲染器。
- 需要改写 URL 时传入 `url_formatter`，不要修改库内部方法。默认行为与上游一致。
- 测试的期望值应以实际输出文本为准，不要假定上游文档中的示例逐字成立。

## 许可证

本包是 GPL-3.0 的上游分支，与本仓库主体的 AGPL-3.0 不同。许可证文件是包根的 `LICENCE`，与上游的 `COPYING` 逐字节相同。发布的 wheel 仍须以 GPL-3.0 分发，并原样携带该文件。
