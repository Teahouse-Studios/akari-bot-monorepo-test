# 包文档编写指南

仓库内每个可安装包都在各自的导入包目录下包含一份 `docs/` 目录。文档引擎收集各包文档目录，合并构建为 VitePress 站点。同一条目同时供 `akaribot docs list` 与站点构建使用。

## 目录位置

`docs/` 必须位于**导入包的根目录**，包根目录、仓库根目录与测试目录下的 `docs/` 不参与收集。发现过程按 `akaribot.docs` entry point 的导入路径定位包，不导入包本身，因此 `docs/` 必须随 wheel 分发。

```text
packages/akari-bot-module-my/
├── pyproject.toml
└── akaribot/modules/my_module/
    ├── __init__.py
    └── docs/
        ├── config/
        │   ├── global/docs.global.toml
        │   └── docs.toml
        └── index.md
```

`akaribot/`、`akaribot/modules/` 是 PEP 420 命名空间目录，不得放置 `__init__.py`。`docs/` 下仅存放 Markdown、图片、`.txt`/`.pdf` 附件与 `docs/config/` 中的元数据文件，不要提交构建产物或缓存。

## `docs/config/global/docs.global.toml`

该文件是包元数据的默认层。包内可以再放置 `docs/config/docs.toml`，按同名键覆盖默认值。两个位置都接受 JSON 文件，文件名分别为 `docs.global.json` 与 `docs.json`。若缺少 `docs/config/` 则改用旧的 `docs/doc.toml`。

| 字段 | 说明 |
| --- | --- |
| `schema` | 固定为 `1`。默认按 1 处理，其他值会导致整个文件被忽略 |
| `title` | 站点标题与侧栏名。默认使用导入路径的最后一段。模块文档使用模块名，不使用描述性标题 |
| `summary` | 一句话简介。默认读取包元数据的 Summary |
| `order` | 排序权重，自小到大。默认 500，非整数按 500 处理并告警 |
| `hidden` | 为 `true` 时该包不进入目录 |
| `overview` | 为 `false` 时不生成包级概览页。导航与分组链接指向第一页，侧栏直接列出页面。默认 `true` |
| `kind` | 覆盖分组：`core`、`builtin`、`cli`、`testing`、`module`、`adapter`、`asset` 等 |
| `category` | 侧栏分类，仅接受单个字符串。默认不分类 |
| `category_order` | 分类在侧栏中的排序权重，自小到大。同一分类的文档以各自声明为准 |
| `logo` | 相对包目录的图片文件，作为站点顶栏标志的候选。多个包声明时优先采用目录顺序靠前的项 |
| `avatar` | 相对包目录的图片文件，作为命令对话示例中的机器人头像。多个包声明时优先采用目录顺序靠前的项 |
| `[locales.<标签>]` | 该语言的 `title` 与 `summary`。未列出的语言沿用默认值 |

`logo`、`avatar` 指向包目录之外或文件不存在时整项被忽略并告警。`category` 写成数组或其他类型时整项被忽略并告警。

同一分类的包在侧栏放入同一个二级分组。`category_order` 仅控制分类之间的顺序，包在分类内仍按 `order`、标题与 key 排序。

`overview = false` 适用于直接以多页面形式呈现的包。生成器不补充 `index.md`，也不将包根目录路径作为链接。

`nav`、分组页与包入口指向该包按 `order` 与路径排序后的第一页，侧栏仅列出页面。分组内仅包含一个无概览页的包时，侧栏省略重复的包标题。

不写 `kind` 时按 key 推断，其中 `core` / `builtin` / `cli` / `testing` 保持原样，`module-*` 归模块，`adapter-*` 归适配器，`assets-*` 归资源，其余归 `library`。分组控制导航与分组页。第三方模块包与适配器包分别使用 `module-`、`adapter-` 前缀，避免归入 `library` 分组。

## 模块属性卡

`docs/config/global/docs.global.toml` 支持使用 `[[meta.modules]]` 声明页首属性卡，生成器会将其渲染为 `ModuleMeta` 组件，不需要在 Markdown 里手写标签。

本仓库的模块文档不声明该表，因为模块名、别名与权限已配置在每条命令的 `CommandUsage` 上，页首无需重复展示。第三方包需要概览表时仍可使用：

```toml
[[meta.modules]]
name = "maimai"
aliases = ["mai"]
type = ["command"]
permission = "public"

[[meta.modules]]
name = "maimai-regex"
aliases = ["maimai_regex", "mai_regex"]
type = ["regex"]
permission = "public"
```

| 字段 | 说明 |
| --- | --- |
| `name` | 模块名，必填 |
| `aliases` | 模块别名 |
| `type` | 能力类型：`command`、`regex`、`rss`、`event` |
| `permission` | 模块级权限：`public`、`admin`、`superuser`、`base_superuser` |
| `platforms` | 仅可用的平台键，如 `QQBot|Group` |
| `excluded` | 排除的平台键 |
| `forced` / `hidden` | 强制启用 / 已隐藏 |
| `note` | 卡片上的补充说明 |

属性卡描述模块级信息。命令级权限写在每条命令的 `CommandUsage` 上。一个包注册多个模块时按声明顺序列出。

## 站点主题与组件

站点主题由实例 `docs.toml` 的 `[theme].source` 选择：

```toml
[theme]
source = "auto"   # auto | bundled | file:<模板路径>
```

`auto` 会在实例根目录查找 `akari-bot-docs-template`、`vendor/akari-bot-docs-template` 或 `docs-theme`。从仓库源码运行 CLI 时还会使用仓库内的 `vendor/akari-bot-docs-template` submodule。未找到时使用 CLI 内置的最小主题。

外部模板在根目录提供 `docs-theme.json`，声明主题目录、VitePress 版本、Node 要求、npm 依赖与生成配置选项。引擎仅复制主题目录，不导入主题代码。`akari-bot-docs-template` 的具体要求由其自身的 `docs-theme.json` 声明。

主题代码作为 submodule 放在 `vendor/akari-bot-docs-template`。更新主题后，在实例根目录运行 `akaribot docs sync-theme`，把该 submodule 更新至远端最新提交。该命令仅更新源码工作区。主题在构建阶段由生成器复制到实例 `cache/docs/src/.vitepress/theme`，依赖由 `akaribot docs install-deps` 单独安装。实例可以使用 `[theme].source` 指向自定义的主题目录。

`akari-bot-docs-template` 的主题内置以下组件，所有包文档都可直接使用：

| 用法 | 说明 |
| --- | --- |
| `<ModuleMeta :modules="[{ name: 'my' }]" />` | 模块属性卡。声明了 `[[meta.modules]]` 时由生成器自动注入，无需在 Markdown 中手写 |
| `<NoticeBox type="tip">提示内容</NoticeBox>` | 提示框，`type` 可选 `info`、`tip`、`warning`、`danger`、`example`、`help`、`deprecated` |
| `<ModuleAlias names="wiki_start_site,wks" />` | 模块级指令别名列表。`names` 接受逗号分隔的字符串或数组。单指令别名在 `CommandUsage` 上声明，不在此处重复 |
| `<ModuleConfig table="module_my" />` | 配置表说明。`table` 为表名，组件据此渲染配置表与 `config/<表名>.toml` 路径 |
| `<ModuleConfig table="module_my_secret" file="config/module_my.toml" />` | 模块只有密钥表时使用。`file` 覆盖配置文件路径，默认按 `config/<表名>.toml` 生成 |
| `<ModuleConfig />` | 渲染「模块没有配置项」，仅用于确实没有配置表的模块 |
| `<ModuleData tables="module_a,module_b" />` | 模块数据表列表 |
| `<ModuleData tables="module_a,module_b" :list="false" />` | 同上，正文随后用表格列出表结构时仅显示数量 |
| `<PackageDependencies package="akari-bot-module-my" />` | 运行依赖列表。构建时读取包元数据的 `Requires-Dist`，跳过 `extra` 可选依赖，按包 key 与分发名索引 |
| `<ModuleConfigFields table="module_my" />` | 配置字段表。构建时解析包内 `config.py` 与 `locales/zh_cn.json` 的 `config.comments`，渲染字段、类型、默认值与说明，正文不写字段副本。表名不存在时显示提示 |
| `<AdapterCapabilities adapter="satori" />` | 适配器能力表，省略 `adapter` 时渲染全部适配器的矩阵。数据来自包内 `features.py` |
| `<CliCommandOptions command="module add" />` | CLI 子命令的用法行与选项表，数据由命令树在构建期自省得到 |
| `<CommandUsage usage="wiki set <wikiurl>" :params="['wikiurl=站点地址，会解析为 API 地址']" permission="admin" :aliases="['wiki_start_site']" :options="[{flag: '-l', desc: '只列未完成项'}]" />` | 命令的权限、别名、用法与选项说明。`params` 逐项解释用法里的参数，渲染为支持悬浮提示的字段与参数清单，组件会自动根据括号类型判定参数是否必填（尖括号表示必填，方括号表示可选）。用法行的前缀取自实例核心配置的 `command_prefix` 首项，`prefix` 可覆盖。`type` 仅在正则、订阅等非前缀触发方式上声明。`platforms` / `excluded` 标注命令仅可用的平台与排除的平台，值可为平台键（如 `QQBot`、`QQ|Group`、`Web`）或直接填写展示文案，`excluded` 渲染为“Web 不可用” |
| `<ChatExample :log="['用户：~wiki 词条', '机器人：查询结果…']" />` | 对话示例。`log` 每行以「用户：」或「机器人：」开头，不带前缀的行续接上一条气泡，`〰〰〰` 一类分隔行渲染为分隔线 |
| `<ChatExample :messages="[{ role: 'bot', text: '**成功**', markdown: true }]" />` | 需要显式指定角色时使用，优先于 `log`。`markdown` 为真时气泡内按 Markdown 渲染 |
| `<ChatExample caption="群聊示例" bot-avatar="./avatar.png" :image-width="240" />` | 气泡上方的说明、机器人头像与示例内图片宽度。头像留空时使用站点配置的头像 |
| `<ChatExample :buttons="[{ label: '查看详情', reply: '用户：~wiki 词条' }]" />` | 消息下方的操作按钮，点击后把 `reply` 或 `messages` 追加到对话末尾。`oneShot` 为真时点击后禁用同组其余按钮 |
| `<ChatExample :card="{ title: '歌曲名', description: '歌手', url: 'https://example.com' }" />` | 机器人回复末尾的卡片消息 |

内置的 `bundled` 主题为 `ModuleMeta`、`NoticeBox`、`CommandUsage`、`ChatExample`、`PackageDependencies`、`ModuleConfigFields`、`AdapterCapabilities` 与 `CliCommandOptions` 提供同名组件。它的 `ChatExample` 把图片渲染为缩略图，点击后在新标签页打开。气泡文本按纯文本处理，不包含头像与主题色。`ModuleAlias`、`ModuleConfig`、`ModuleData` 仅在外部模板中渲染。

`CommandUsage` 的 `params` 参数清单、悬浮提示与 `platforms` / `excluded` 平台徽章同样由外部模板渲染。内置主题的命令用法组件显示用法行、权限与类型徽章、别名与选项表，补充说明由 `note` 属性提供。

外部模板的组件使用 M3E 配色变量，外观会随读者的主题色、明暗模式与对比度设置自动变化。组件仅在构建后的站点中渲染，直接在 Markdown 阅读器里会显示为标签。

属性卡由生成器注入，其他组件按需使用，正文仍以 Markdown 为主。数据去向、进程内状态这类补充说明写在卡片之后的正段落里。

## 模块页面结构

模块文档通常分为“使用方法”和“安装与开发”两部分，按读者划分内容。

内置模块不设包级概览页，每个模块各自占用一页，页面文件名取模块名，`update&restart` 写作 `update-restart.md`。导航进入第一页。侧栏直接列出命令模块与配置、工具页面，非命令钩子页面归入“钩子”子菜单。

- `index.md` 是使用说明，面向使用者。仅说明模块用途、触发方式与返回内容，以及用户可见的限制与提示，不包含安装命令、配置字段、数据表、依赖与内部实现。
- 模块有多个子命令组时使用 `##` 分组，命令仍使用 `###`，独立成节而不单独拆分为页面。
- 对话示例使用默认前缀 `~`，仅展示仓库默认配置下可直接使用的结果。需要图片结果时使用 `![说明](相对路径)` 引用包内图片，图片存放在包内 `docs/` 目录下。
- 配置与数据表两节使用 `ModuleConfig`、`ModuleData` 陈述事实，模块级别名使用 `ModuleAlias`。每项仅说明一次，不在每条命令上重复。
- `docs/config/global/docs.global.toml` 不声明 `[[meta.modules]]`，页面顶部默认不展示模块清单表。声明该表的能力仍然保留，供第三方包使用。

生成器会将同一模块目录下的页面视为同级页面。使用 `akari-bot-docs-template` 时，侧栏仅显示一个模块条目，条目名称使用模块名。

有概览页时默认打开使用方法，无概览页时默认打开第一页。`development.md` 的标签默认是「安装与开发」，可由实例 `docs.toml` 的 `[labels]` 覆盖，该页不单独出现在侧栏。

内置回退主题不提供标签栏，开发页仍作为普通页面直接列出。

## 页面与 front matter

文档目录中的每个 Markdown 文件对应一个页面，文件名小写、使用连字符分词。页面可带有 front matter：

```markdown
---
title: 命令
order: 20
description: 常用命令与参数。
submenu: 钩子
---

# 命令
```

引擎解析 `title`、`order`、`description` 与 `submenu` 四个单行键值对，分别用于标题、排序、简介与侧栏分组，不支持列表或嵌套结构。其余键原样保留，由主题读取，例如首页的 `hero`。标题默认提取正文中的第一个一级标题（跳过代码块），无一级标题时使用文件名。

包有概览页时 `index.md` 始终排在最前。无概览页的包按 `order`、路径排序。`submenu` 将同一包内取值相同的页面归入一个无链接的二级分组，分组名即字段值。未设置该字段的页面仍直接列在包下，分组排在未分组页面之后。

页面可携带的文件后缀有 `.md`、`.png`、`.jpg`、`.jpeg`、`.gif`、`.svg`、`.webp`、`.avif`、`.txt`、`.pdf`。其他后缀不进入站点。文档目录中的符号链接不得指向目录之外。

## 声明 entry point

在包的 `pyproject.toml` 声明 `akaribot.docs`，名称为 key，值为导入路径：

```toml
[project.entry-points."akaribot.docs"]
module-my-module = "akaribot.modules.my_module"
```

- key 确定 URL、生成目录名与默认分组，必须匹配 `[A-Za-z0-9][A-Za-z0-9._-]*`。
- 值仅截取 `:` 之前的导入路径。写成 `akaribot.modules.my_module:app` 也按包路径处理。
- key 重复时，排序靠后的条目会被忽略并触发告警。包已安装但 `docs/` 不存在或缺少 Markdown 页面时，系统会跳过该包并记录警告。
- entry point 仅在安装时写入包元数据。可编辑安装的包若在安装之后才声明 `akaribot.docs`，发现过程按源码 `pyproject.toml` 的声明补充收录该包并告警。重新安装即可刷新元数据，工作区实例可执行 `akaribot module update --all`。普通安装的包不按源码补充收录。

`akaribot.core` 与 `akaribot.modules.core` 分别以 `core`、`builtin` 提供文档。CLI 的 `cli` 条目由命令行工具自身合并。

## 命令与生成物

`akaribot docs` 提供 `list`、`build`、`sync-theme`、`install-deps`、`serve`、`dev`、`deploy`、`status`、`clean`：

- `list`：通过实例的 core 入口读取已安装包目录，入口无法使用时改用注册表清单。
- `build`：生成站点并调用 VitePress。
- `sync-theme`：将主题模板 submodule 同步至远端最新提交，仅更新工作区。
- `install-deps`：安装主题所需的 Node 依赖。
- `serve`：在本机预览产物。
- `dev`：监听文档与主题改动，运行 VitePress 开发服务器。
- `deploy`：发布到 Vercel 或 S3。
- `status`：读取构建与部署状态。
- `clean`：清理生成目录。

构建需要 Node.js 与 `npm`，版本要求由主题清单确定。依赖安装方式同样由主题清单的 `install_mode` 决定：`ci` 执行 `npm ci`，`install` 执行 `npm install`。内置主题使用 `ci`，`akari-bot-docs-template` 使用 `install`。生成产物位于实例根目录的 `cache/docs/src`（站点源码）、`cache/docs`（Node 工具链与 `node_modules`）与 `cache/docs/site`（默认输出，可由 `build.out_dir` 改写）。构建校验信息与部署记录保存在 `.docs/state.json`。

部署目标配置在实例根目录 `docs.toml` 的 `[deploy]` 段。登录信息仅从环境变量读取，不写入配置文件与状态文件。基础路径默认为 `/`，环境变量 `AKARIBOT_DOCS_BASE` 优先。

## 编写规则

- **简体中文**：包内文档仅使用简体中文。面向用户的固定文案仍使用 `I18NContext`。不得为文档创建或修改 `locales/` 下 `zh_cn.json` 以外的语言文件，翻译由 Weblate 自动提交。
- **仅描述当前行为**：不描述历史演进，变更历史由 git 记录。
- **段落不手动折行**：一个段落写在同一行，由渲染器自动换行。中文没有词间空格，源码中的手动换行会在页面上产生多余空格。
- **一级标题开头**：每页以 `# 标题` 开始，标题与 front matter 的 `title` 一致。
- **篇幅**：单页 40 至 120 行，仅覆盖功能概述、基本使用与接口行为。
- **链接**：同包页面使用相对路径。跨包页面按源码目录填写相对路径，生成器会转换为站点 URL，也可直接填写 `/<包 key>/<页面>`。
- **图片与附件**：放在 `docs/` 下用相对路径引用。图片、`.txt` 与 `.pdf` 都会发布到 `/<包 key>/` 路径下，组件内的相对路径同样可用。

## 最小示例

`pyproject.toml`：

```toml
[project]
name = "akari-bot-module-my"
version = "x.y.z"

[project.entry-points."akaribot.docs"]
module-my-module = "akaribot.modules.my_module"

[tool.hatch.build.targets.wheel]
packages = ["akaribot"]
```

`akaribot/modules/my_module/docs/config/global/docs.global.toml`：

```toml
schema = 1
title = "my-module"
category = "实用工具"
category_order = 400
summary = "示例模块的功能与命令。"
order = 100
```

`index.md` 以 `# my-module` 开头，说明模块用途，然后按命令分节。安装、配置、权限、数据表与依赖写入 `development.md`。新增页面后运行 `python -m akaribot.core.entrypoints.docs --json` 核对清单与告警，再构建站点。
