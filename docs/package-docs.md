# 包文档编写指南

仓库内每个可安装包都在自己的导入包目录下带一份 `doc/`。文档引擎收集这些目录，合并成 VitePress 站点；同一条目同时供 `akaribot docs list` 与站点构建使用。

## 目录位置

`doc/` 必须位于**导入包的根目录**，不是分发包根、仓库根的 `docs/` 或测试目录。发现过程按 `akaribot.docs` entry point 的导入路径定位包，不导入包本身，因此 `doc/` 必须随 wheel 分发。

```text
packages/akari-bot-module-my/
├── pyproject.toml
└── akaribot/modules/my_module/
    ├── __init__.py
    └── doc/{doc.toml, index.md, development.md}
```

`akaribot/`、`akaribot/modules/` 是 PEP 420 命名空间目录，不得放 `__init__.py`；`doc/` 下只放 Markdown、图片、`.txt`/`.pdf` 附件与 `doc.toml`，不要提交构建产物或缓存。

## `doc.toml`

| 字段 | 说明 |
| --- | --- |
| `schema` | 固定为 `1`；缺省按 1 处理，其他值使整个文件被忽略 |
| `title` | 站点标题与侧栏名；缺省取导入路径最后一段。模块文档使用模块名，不使用描述性标题 |
| `summary` | 一句话简介；缺省取分发元数据的 Summary |
| `order` | 排序权重，自小到大；缺省 500，非整数按 500 处理并告警 |
| `hidden` | 为 `true` 时该包不进入目录 |
| `kind` | 覆盖分组：`core`、`builtin`、`cli`、`testing`、`module`、`adapter`、`asset` 等 |
| `category` | 侧栏分类，只接受一个字符串；缺省不分类 |
| `category_order` | 分类在侧栏中的排序权重，自小到大；同一分类的文档取各自声明 |
| `logo` | 相对包目录的图片文件，作为站点顶栏标志的候选；多个包声明时取目录顺序靠前者 |
| `avatar` | 相对包目录的图片文件，作为命令对话示例中的机器人头像；多个包声明时取目录顺序靠前者 |
| `[locales.<标签>]` | 该语言的 `title` 与 `summary`；未列出的语言沿用默认值 |

`logo`、`avatar` 指向包目录之外或文件不存在时整项被忽略并告警。`category` 写成数组或其他类型时整项被忽略并告警。

同一分类的包在侧栏放入同一个二级分组；`category_order` 只决定分类之间的先后，包在分类内仍按 `order`、标题与 key 排序。

不写 `kind` 时按 key 推断：`core` / `builtin` / `cli` / `testing` 原样；`module-*` 归模块，`adapter-*` 归适配器，`assets-*` 归资源，其余归 `library`。分组决定导航与分组页。第三方模块包与适配器包分别使用 `module-`、`adapter-` 前缀，避免落进 `library` 分组。

## 模块属性卡

`doc.toml` 支持用 `[[meta.modules]]` 声明页首属性卡，生成器会把它渲染成 `ModuleMeta` 组件，不需要在 Markdown 里手写标签。本仓库的模块文档不声明该表：模块名、别名与权限写在每条命令的 `CommandUsage` 上，页首不再重复。第三方包需要一览表时仍可使用：

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
| `forced` / `hidden` | 强制开启 / 已隐藏 |
| `note` | 卡片上的补充说明 |

属性卡描述模块级信息；命令级权限写在每条命令的 `CommandUsage` 上。一个包注册多个模块时按声明顺序列出。

## 站点主题与组件

站点主题由实例 `docs.toml` 的 `[theme].source` 选择：

```toml
[theme]
source = "auto"   # auto | bundled | file:<模板路径>
```

`auto` 会在实例根查找 `akari-bot-docs-template`、`vendor/akari-bot-docs-template` 或 `docs-theme`；从仓库源码运行 CLI 时还会使用仓库内的 `vendor/akari-bot-docs-template` submodule。找不到时使用 CLI 内置的最小主题。外部模板在根目录提供 `docs-theme.json`，声明主题目录、VitePress 版本、Node 要求、npm 依赖与生成配置选项；引擎只复制主题目录，不导入主题代码。`akari-bot-docs-template` 当前要求 Node.js 22.12 与 VitePress 2.0.0-alpha.21。

从源码检出运行 CLI 时，`akaribot docs sync-theme` 把 submodule 更新到远端最新提交，`akaribot docs install-deps` 安装或刷新主题依赖。实例可用 `[theme].color = "#rrggbb"` 设置站点主题色；留空使用主题默认值。

`akari-bot-docs-template` 的主题内置以下组件，所有包文档都可直接使用：

| 组件 | 用途 |
| --- | --- |
| `<ModuleMeta :modules="..." />` | 模块属性卡；由 `doc.toml` 自动注入，本仓库不使用 |
| `<ModuleConfig />` | 模块没有配置项时使用 |
| `<ModuleConfig table="module_coin" />` | 模块有配置表时给出表名与配置文件路径 |
| `<ModuleData />` | 模块不保存数据时使用 |
| `<ModuleData tables="module_a,module_b" />` | 模块拥有数据表时给出表名与表结构位置 |
| `<ModuleData tables="module_a,module_b" :list="false" />` | 同上，正文随后用表格罗列表结构时只报数量 |
| `<ModuleAlias names="wiki_bot, wbot" />` | 模块级别名，写在章节标题下，对该节所有命令生效 |
| `<NoticeBox type="warning" title="...">…</NoticeBox>` | 提示框，类型取 `info`、`tip`、`help`、`example`、`warning`、`danger`、`deprecated` |
| `<ChatExample :log="['用户：~whois example.com', '机器人：域名：example.com']" />` | 命令对话示例：`用户：` 与 `机器人：` 前缀区分角色，无前缀的行续接上一条；反引号内按行内代码渲染；`![说明](地址)` 在气泡内渲染为缩略图，点击后从缩略图位置展开可缩放、旋转的查看叠层，关闭时收回原位；在地址后加 `{natural}` 表示按原始尺寸展示，适合缩放后宽度过小的竖长图；`image-width` 固定示例内所有图片的宽度，适合同一气泡内多张图需要对齐的场景；`botAvatar` 可覆盖机器人头像；只含三个以上波浪号的行（如 `〰〰〰`）渲染为时间分隔线 |
| `<ChatExample :log="[...]" :buttons="[{ label: '苔藓块', reply: ['机器人：…', '![苔藓块](moss.png)'] }]" />` | 在最后一条机器人初始消息下渲染按钮；`reply` 使用与 `log` 相同的写法，点击后先显示加载动画并预加载其中的图片，再把回复淡入追加到按钮下方；`loading` 可覆盖加载文案，`messages` 可直接给结构化消息；按钮项再写 `buttons` 时，回复会带上二级按钮，可用来模拟「查询页面 → 预览/关闭」；`dismiss: true` 表示关闭按钮，点击后删除该按钮所属的整组回复（含后续二级回复），基础消息上的关闭按钮会连同初始回复一起隐藏；尾部图片单独成气泡，多张尾部图片合并到同一气泡；右上角的重置图标清空追加内容与按钮禁用状态 |
| `<CommandUsage usage="wiki set <wikiurl>" :params="['wikiurl=站点地址，会解析为 API 地址']" permission="admin" :aliases="['wiki_start_site']" :options="[{flag: '-l', desc: '只列未完成项'}]" />` | 命令的权限、别名、用法与选项说明；`params` 逐项解释用法里的参数，渲染为可悬浮的字段与参数清单，尖括号必填、方括号可选由组件自动判定；用法行的前缀取自实例核心配置的 `command_prefix` 首项，`prefix` 可覆盖；`type` 只在正则、订阅等非前缀触发方式上声明；`platforms` / `excluded` 标注命令仅可用的平台与排除的平台，值可为平台键（如 `QQBot`、`QQ|Group`、`Web`）或直接写展示文案，`excluded` 渲染为“Web 不可用” |

内置的 `bundled` 主题为 `ModuleMeta`、`NoticeBox`、`CommandUsage` 与 `ChatExample` 保留同名组件（`ChatExample` 将图片渲染为缩略图、点击在新标签页打开，不含头像与主题色），`ModuleAlias`、`ModuleConfig`、`ModuleData` 只在外部模板中渲染；`CommandUsage` 的 `params` 参数清单、悬浮提示与 `platforms` / `excluded` 平台徽章同样由外部模板渲染，内置主题只显示用法行。外部模板的组件使用 M3E 颜色令牌，外观随读者的种子色、明暗模式与对比度设置变化。组件只在构建后的站点中渲染；直接在 Markdown 阅读器里会显示为标签。属性卡由生成器注入，其它组件按需使用，正文仍以 Markdown 为主。数据去向、进程内状态这类补充说明写在卡片之后的正段落里。

## 模块页面结构

模块文档分为“使用方法”和“安装与开发”两部分，按读者划分内容：

- `index.md` 是使用方法，面向使用者。只写模块做什么、怎么触发、会得到什么，以及用户可见的限制与提示；不写安装命令、配置字段、数据表、依赖与内部实现。每条命令一个 `###` 章节：标题写命令名，下面接一行 `CommandUsage` 交代权限与别名，再写一至三句说明参数与行为；需要展示实际往返时，在说明后接一个 `ChatExample`。模块有多个子命令组时用 `##` 分组，命令仍写 `###`；命令不再单独成页。
- 命令不用表格罗列。用法行由 `CommandUsage` 按实例配置的命令前缀渲染，未配置前缀时不加；用法里的参数用 `params` 逐项说明，格式为 `['名字=说明', …]`，名字不带尖括号，占位名是中文时照写；选项写在 `options` 上，渲染为列表；字段说明这类小表改成列表，长对照表（颜色名、谱面定数等）保留表格。对话示例使用默认前缀 `~`，只展示仓库默认配置下可直接使用的结果；需要图片结果时用 `![说明](相对路径)` 引用包内图片，图片放在包内 `doc/` 目录下；图片位于消息尾部时另起气泡，多张尾部图片共用一个气泡；竖长图缩到 200px 高后宽度过小时在地址后加 `{natural}`，按原始尺寸展示；同一气泡内的多张图需要等宽时，在 `ChatExample` 上写 `:image-width="320"`。订阅类模块的示例按「开启成功 → 时间分隔线 → 实际推送」组织，分隔线写 `〰〰〰`。需要模拟消息按钮时，在 `ChatExample` 上写 `buttons`，每项用 `label` 与 `reply` 描述按钮和点击后的回复；回复需要继续挂按钮时在按钮项上再写 `buttons`，关闭类按钮写 `dismiss: true`；图片会在点击后才开始加载。
- `development.md` 是安装与开发，面向部署者与维护者。放安装步骤、配置字段、权限与平台能力、数据表与依赖；不写玩法规则与命令用法。配置与数据表两节用 `ModuleConfig`、`ModuleData` 说明事实，模块级别名用 `ModuleAlias`；每项只写一次，不在每条命令上重复。
- `doc.toml` 不声明 `[[meta.modules]]`，页面顶部不再出现模块清单表。声明该表的能力仍然保留，供第三方包使用。
- 其余页面作为补充用法，与上述两页一起出现。
- 译文放在 `doc/<语言标签>/` 下，文件名与默认语言一致；某个语言缺少页面时生成器复制默认语言的同名页面，不产生空链接。`doc.toml` 用 `[locales.<标签>]` 覆盖该语言的标题与简介。

生成器把同一模块目录下的页面作为平行页面：使用 `akari-bot-docs-template` 时，侧栏只显示一个模块条目，条目名称取模块名；默认打开使用方法，`development.md` 的标签固定为“安装与开发”，不单独出现在侧栏。内置回退主题没有标签栏，开发页仍作为普通侧栏页面列出。页面顺序由 `order` 与文件名决定，`index.md` 始终在最前，`development.md` 始终在最后。

## 页面与 front matter

每个 `.md` 是一个页面，文件名小写、用连字符分词。页面可带简单 front matter：

```markdown
---
title: 命令
order: 20
description: 常用命令与参数。
---

# 命令
```

只识别 `title`、`order`、`description` 三个单行标量键，不支持列表或嵌套结构。标题缺省取正文第一个一级标题（跳过代码块），再缺省取文件名。`index.md` 始终排在该包最前，其余页面按 `order`、路径排序。

页面可携带 `.md`、`.png`、`.jpg`、`.jpeg`、`.gif`、`.svg`、`.webp`、`.avif`、`.txt`、`.pdf`；其他后缀不进入站点。文档目录中的符号链接不得指向目录之外。

## 声明 entry point

在包的 `pyproject.toml` 声明 `akaribot.docs`，名称为 key，值为导入路径：

```toml
[project.entry-points."akaribot.docs"]
module-my-module = "akaribot.modules.my_module"
```

- key 决定 URL、生成目录名与默认分组，必须匹配 `[A-Za-z0-9][A-Za-z0-9._-]*`。
- 值只取 `:` 之前的导入路径；写成 `akaribot.modules.my_module:app` 也按包路径处理。
- key 重复时排序靠后的条目被忽略并告警；包已安装但 `doc/` 不存在或没有 Markdown 页面时，该包被跳过并记入警告。
- entry point 只在安装时写入包元数据。可编辑安装的包若在安装之后才声明 `akaribot.docs`，发现过程按源码 `pyproject.toml` 的声明补入该包并告警；重新安装即可刷新元数据，工作区实例可执行 `akaribot module update --all`。普通安装的包不按源码补入。

`akaribot.core` 与 `akaribot.modules.core` 分别以 `core`、`builtin` 提供文档；CLI 的 `cli` 条目由命令行工具自身合并。

## 命令与生成物

`akaribot docs` 提供 `list`、`build`、`serve`、`deploy`、`status`、`clean`：`list` 经实例的 core 入口读取已装包目录，入口不可用时退回注册表清单；`build` 生成站点并调用 VitePress；`serve` 在本机预览产物；`deploy` 发布到 Vercel 或 S3；`status` 读取构建与部署状态；`clean` 清理生成目录。

构建需要 Node.js >= 18 与 `npm`，VitePress 固定为 1.6.4，依赖由 `npm ci` 安装。生成物位于实例根的 `cache/docs/src`（站点源）、`cache/docs`（Node 工具链与 `node_modules`）与 `cache/docs/site`（默认输出，可由 `build.out_dir` 改写）；构建指纹与部署记录在 `.docs/state.json`。

部署目标写在实例根 `docs.toml` 的 `[deploy]` 段，凭据只从环境变量读取，不写入配置文件与状态文件。基路径默认 `/`，环境变量 `AKARIBOT_DOCS_BASE` 优先。

## 编写规则

- **简体中文**：包内文档只写简体中文。面向用户的固定文案仍用 `I18NContext`；不得为文档创建或修改 `locales/` 下 `zh_cn.json` 以外的语言文件，翻译由 Weblate 自动提交。
- **只写当前行为**：不写“原来如何、现在改为如何”，变更历史由 git 承担。
- **段落不按列硬换行**：一个段落写在同一行，由渲染器换行；中文没有词间空格，源码里的软换行会在页面上留下空格。
- **一级标题开头**：每页以 `# 标题` 开始，标题与 front matter 的 `title` 一致。
- **篇幅**：单页 40 至 120 行，只覆盖功能概述、基本使用与接口行为。
- **链接与图片**：同包页面使用相对路径；跨包页面按源码目录写相对路径，生成器会折算成站点 URL，也可直接写 `/<包 key>/<页面>`。图片与附件放在 `doc/` 下用相对路径引用；图片、`.txt` 与 `.pdf` 都会发布到 `/<包 key>/` 路径下，组件内的相对路径同样可用。

## 最小示例

`pyproject.toml`：

```toml
[project]
name = "akari-bot-module-my"
version = "0.1.0"

[project.entry-points."akaribot.docs"]
module-my-module = "akaribot.modules.my_module"

[tool.hatch.build.targets.wheel]
packages = ["akaribot"]
```

`akaribot/modules/my_module/doc/doc.toml`：

```toml
schema = 1
title = "my-module"
category = "实用工具"
category_order = 400
summary = "示例模块的功能与命令。"
order = 100
```

`index.md` 以 `# my-module` 开头，说明模块用途，然后按命令分节；安装、配置、权限、数据表与依赖写入 `development.md`。新增页面后运行 `python -m akaribot.core.entrypoints.docs --json` 核对清单与告警，再构建站点。
