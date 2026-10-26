# 占位符

消息文本中的 `[KE:...]`、`{I18N:...}` 与 `<AT:...>` 是三种文本占位符，分别在构造消息链、本地化
与平台发送阶段解析。模块应优先使用消息元素类构造内容，只在需要由文本触发元素或跨进程传递时写
占位符。

<NoticeBox type="warning" title="解析顺序与嵌套">
纯文本先由 `Locale.t_str()` 替换 I18N 标记，再由 `match_kecode()` 解析 KE 码；AT 码不参与这两步，
由平台适配器在发送时渲染。KE 与 I18N 可以互相嵌套；参数值中的结构字符须按本节规则转义。
</NoticeBox>

## KE 码

KE 码用于在文本中插入图片、语音、按钮等消息元素，语法为：

```text
[KE:元素类型,参数1=值1,参数2=值2]
```

元素类型不区分大小写，参数之间用逗号分隔。`plain`、`markdown`、`url`、`action_text` 与按钮的
文本参数会做 URL 解码；所有参数值在解析前先做 HTML 实体反转义。KE 元素作为独立消息元素插入，
通常与相邻文本分行；行内提及应使用 AT 码。

| 类型 | 参数 |
| --- | --- |
| `plain` | `text` 必填；可选 `disable_joke=1`、`allow_parse=0` |
| `markdown` | 与 `plain` 相同，按 Markdown 渲染，平台不支持时降级为纯文本 |
| `image` | `path` 必填，支持 URL、`file://` 路径、`base64://` 与 data URI；可选 `headers`（Base64 编码的 JSON）、`max_h`、`allow_split=0` |
| `audio` | `path` 必填，本地文件路径 |
| `video` | `path` 必填，本地文件路径 |
| `i18n` | `i18nkey` 必填；其余键作为翻译参数；可选 `fallback=0`、`locale_failed_prompt=0`、`disable_joke=1` |
| `mention` | `userid` 必填，格式为 `客户端\|用户 ID` |
| `url` | `text` 必填；可选 `trusted=1` 或 `trusted=0` |
| `action_text` | `text` 必填，点击后插入输入框；可选 `show`、`reference=1`、`show_on_fallback=0`、`quote_on_fallback=1` |
| `button` | `show`、`value` 必填；可选 `reply_id`、`permission=all`、`click_limit` |
| `button_frame` | `data` 必填，按钮行数组的 URL 编码 JSON |

```text
[KE:plain,text=hello]
[KE:image,path=https://example.com/a.png]
[KE:mention,userid=QQ|123456]
[KE:button,show=确定,value=confirm,permission=all]
```

`button` 的 `permission=all` 允许场景内其他人点击，缺省仅发送者可用；`click_limit` 为 `0` 表示
不限次数。`button_frame` 的 `data` 由 `ButtonFrameElement.kecode()` 生成，手写时应保持 JSON 结构。

## I18N 标记

I18N 标记用于在文本中行内插入翻译结果，语法为：

```text
{I18N:键名,参数1=值1,参数2=值2}
```

键名不能包含空白、逗号或花括号；参数可选，名称须匹配 `\w+`，值不能包含逗号。参数值支持 HTML
实体，例如 `&#44;` 表示逗号。标记由 `Locale.t_str()` 递归解析，最多 10 层；翻译结果中的新标记会
继续展开。

```text
{I18N:core.message.brackets,msg=test}
```

需要构造消息元素而非纯文本时使用 `I18NContext`：

```python
from akaribot.core.api import I18NContext

await msg.finish(I18NContext("core.message.brackets", msg="test"))
```

`[KE:i18n]` 与 `{I18N:...}` 的区别在于前者产生独立的 `I18NContextElement`，后者在字符串内联替换。

## AT 码

AT 码用于行内提及用户，语法为 `<AT:客户端|用户 ID>`，也接受 `<@:客户端|用户 ID>`：

```text
<AT:QQ|123456>
<@:Discord|123456>
```

中间可以带额外的子平台字段，解析时取最后一个字段作为用户 ID：

```text
<AT:QQ|guild|123456>
```

客户端与当前平台不一致的 AT 码会原样保留；用户 ID 不是纯数字时按全体提及处理。同一段文本中
相邻的 AT 码会按惰性匹配合并为一次提及并取最后一个 ID，需要分别提及时应在两者之间插入其他文本。

用户 ID 的结构为 `客户端|子平台（可选）|平台 ID`，例如 `QQ|Group|123456`。`MentionElement`
取第一个字段作为客户端、最后一个字段作为 ID；可用 `~bind whoami` 查看当前账号的完整 ID。

## 转义

参数值中的结构字符须写成 HTML 实体，避免被解析器当作分隔符：

| 字符 | 实体 |
| --- | --- |
| `&` | `&amp;` |
| `,` | `&#44;` |
| `[` / `]` | `&#91;` / `&#93;` |
| `{` / `}` | `&#123;` / `&#125;` |
| `<` / `>` | `&lt;` / `&gt;` |

```text
[KE:plain,text=&#91;示例&#93;&#44;含逗号]
{I18N:core.message.brackets,msg=a&#44;b}
```

拼接用户输入时应对结构字符做实体转义。AT 码没有转义语法，ID 中不能出现 `|` 或 `>`；跨平台 ID
不匹配时保持原文。KE 参数值中不要直接出现 `[KE:`，否则块扫描会在此处截断。
