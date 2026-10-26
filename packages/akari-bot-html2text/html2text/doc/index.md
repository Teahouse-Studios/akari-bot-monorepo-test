# html2text

`akari-bot-html2text` 是 AkariBot 维护的 HTML 转 Markdown 文本库，独立分发给需要离线渲染网页
正文的模块使用。基线为上游 `html2text==2020.1.16`，包内 `__version__` 同为 `(2020, 1, 16)`。

## 输入与输出

输入是 HTML 字符串，输出是 Markdown 风格的纯文本。库只依赖标准库，不访问网络。

```python
from html2text import HTML2Text, html2text

text = html2text("<h1>标题</h1><p>正文</p>")

parser = HTML2Text(bodywidth=0)
parser.ignore_links = True
text = parser.handle("<p><a href=\"https://example.com\">链接</a></p>")
```

- `html2text(html, baseurl="", bodywidth=None, url_formatter=str)`：一次性转换的快捷函数。
- `HTML2Text(out=None, baseurl="", bodywidth=..., url_formatter=str)`：可先设置 `ignore_links`、
  `ignore_images`、`pad_tables` 等属性，再调用 `handle()`；也支持 `feed()` 分段输入后 `finish()`。
- `url_formatter`：对输出的每个链接与图片 URL 调用的函数，默认 `str` 表示不加工。

命令行等价入口：

```sh
python -m html2text page.html
python -m html2text --ignore-links --body-width 0 page.html
```

省略文件名或传 `-` 时从标准输入读取，第二个位置参数是编码，默认 `utf-8`。`--ignore-links`、
`--reference-links`、`--ignore-images`、`--body-width`、`--pad-tables`、`--no-wrap-links` 等选项
与上游一致。

## 与上游的差异

以下行为与上游 2020.1.16 不同，调用方须按此使用：

- **链接 title 被丢弃**：`link_url()` 不再输出 `](url "标题")` 中的 title。开启链接输出时只能
  得到 URL 本身，不要依赖 title 生成引用或脚注。
- **`</script>` 处理**：转义写法被改回真正的 `</script>`，结束标签因此变成 `</ignore>`，
  `HTMLParser` 无法退出 script 的 CDATA 模式，第一个 `<script>` 之后的正文会丢失。含脚本的
  HTML 应先移除 `<script>` 块再交给本库。
- **URL 解耦**：不再依赖 `akaribot.core` 的 `Url` 类型，改为 `url_formatter` 注入；注入点包括
  行内链接、图片 alt、图片 URL 与引用式链接定义。
- **断言移除**：内部 `assert ... is not None` 已删除，异常类型在异常输入下可能是 `TypeError`
  或 `AttributeError`，而不是 `AssertionError`。
- **类型与格式**：`OutCallback` 的方法体改为 `raise NotImplementedError`，注解使用内建泛型，
  部分辅助函数做了语义等价的改写。

本分支尚未合并上游 2024 与 2025 版本。需要 2025 版行为（例如保留链接 title）的调用方不应把
本包当作上游替代。

## 使用边界

- 只用于把网页正文转成便于阅读的 Markdown，不承担 HTML 清洗。输入不可信时先做白名单过滤。
- 含 `<script>` 或依赖链接 title 的页面需要预处理，或改用其它渲染器。
- 需要改写 URL 时传 `url_formatter`，不要修改库内部方法；默认行为与上游一致。
- 测试期望应覆盖实际输出文本，不要假定上游文档中的示例逐字成立。

## 许可证

本包是 GPL-3.0 的上游分支，与本仓库主体的 AGPL-3.0 不同。许可证文件为包根的 `LICENCE`，
与上游 `COPYING` 逐字节相同；wheel 必须继续以 GPL-3.0 分发并原样携带该文件。
