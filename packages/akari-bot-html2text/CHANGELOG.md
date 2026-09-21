# 变更记录

本包是 `html2text` 的 AkariBot 维护分支，基线为上游 `html2text==2020.1.16`（副本 `__version__ = (2020, 1, 16)`）。
以下按类别记录相对该基线的全部本地改动，条目取自 `generated_docs/html2text_fork_baseline.md` 的逐文件实测。

## 0.1.0

首个独立分发版本。上游自 2020.1.16 后仍有 2024.2.25、2024.2.26、2025.4.15 三个版本，
本分支尚未合并它们，后续如需 rebase 请以本节记录为分支基线。

### 行为改动（与上游不同，第三方使用者须留意）

- **丢弃链接 title**：`link_url()` 不再输出 `](url "标题")` 中的 title 部分，签名由
  `link_url(self, link, title="")` 变为 `link_url(self, link)`，调用点计算的 `title = escape_md(...)` 遂成死代码。
  上游 2020.1.16 与 2025.4.15 均保留 title；实测影响面为 `ignore_links=False` 下的页面（wiki 模块因
  `ignore_links=True` 不经过该路径）。
- **改写 `</script>`**：`feed()` 把上游的字面量 `"</' + 'script>"`（上游永不命中，系自动化改写事故的残留）
  改为真正的 `"</script>"`。替换后 `HTMLParser` 收到的结束标签变为 `</ignore>`，无法退出 script 的 CDATA 模式，
  第一个 `<script>` 之后的正文会被丢弃。修复方向本身存疑，回退与否待上游 issue 结论。

### 解耦改动（相对内嵌时期）

- 解除 `Url` 耦合：`HTML2Text.__init__` 与模块级 `html2text()` 新增
  `url_formatter: Callable[[str], str] = str`，原四处 `str(Url(...))` 调用改为 `self.url_formatter(...)`。
  默认 `str` 即上游语义「不做额外处理」，包内不再 import 任何 `akaribot` 代码。
  注入点共四处：行内链接、`<img>` 的 alt 文本、`<img>` 的 URL、引用式链接定义；调用次数取决于选项组合。

### 断言与类型

- 删除 `__init__.py` 的 6 处与 `utils.py` 的 3 处 `assert ... is not None`。正常输入下无差异；
  断言本会触发时，异常类型由 `AssertionError` 变为 `TypeError`/`AttributeError`。
- `typing.py` 的 `OutCallback.__call__` 函数体由 `...` 改为 `raise NotImplementedError`，仅涉类型标注，运行时不会实例化。
- `utils.py` 的 `"courier new" == font_family or "consolas" == font_family` 改写为
  `font_family in ("courier new", "consolas")`，语义等价。

### 格式与现代化（不改变正常路径输出）

- `config.py` 的 `RE_MD_BACKSLASH_MATCHER` 由 `%` 格式化改写为 rf-string，并把模式串内的注释移出，
  经逐段核对语义等价（`re.VERBOSE` 与字符集内容不变）。
- `cli.py` 有 1 处 help 文本内的 3 对单引号改为双引号（字符串内容变化，CLI 不被 bot 调用），另有折行重排。
- `elements.py` 删除 `typing` 导入，注解改用内建泛型；其余文件为注解现代化与 ruff format 重排。
- `__main__.py` 与 `py.typed` 与上游逐字节相同。

### 许可证

- `LICENCE` 与上游 `COPYING` 逐字节相同，为 **GPL-3.0**（非本仓库主体包的 AGPL-3.0），
  wheel 必须继续以 GPL-3.0 分发并原样携带该文件。
