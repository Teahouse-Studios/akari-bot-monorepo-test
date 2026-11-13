# 文档引擎

本文将会介绍文档引擎的目录收集、站点生成、构建缓存、预览与部署。

文档引擎把已安装包的 `doc/` 目录汇总成一个 VitePress 站点：读取目录、生成站点源文件、调用 VitePress 构建、提供本机预览，并记录构建与部署状态。

## 当前状态

引擎实现在 `akaribot/cli/docs/`，包含目录收集、源文件生成、跨包链接折算、构建缓存、静态预览与状态持久化。`akaribot docs` 已注册进 `akaribot` 主命令表。命令见下表。

## 前置条件

- Node.js 与 `npm` 需要在 `PATH` 中。内置主题要求 Node.js 18 及以上。外部主题的要求由主题清单声明，`akari-bot-docs-template` 当前要求 Node.js 22.12 及以上。
- 内置主题的依赖固定在引擎模板的 `package-lock.json` 里（VitePress 1.6.4），安装执行 `npm ci`。外部主题的 `package.json` 由清单的 `dependencies` 生成，安装执行 `npm install`，VitePress 版本同样来自清单。
- 首次构建需要联网安装依赖。离线模式要求 `<实例根>/cache/docs/node_modules` 已包含主题所需版本。

Node.js 缺失、版本低于主题要求或 npm 不可用时，构建以工具链错误终止，不会改用其它渲染器。

## 命令

| 命令 | 用途 |
| --- | --- |
| `akaribot docs list` | 列出参与构建的包、分组、标题与页面数，附目录降级警告 |
| `akaribot docs build` | 生成站点源文件并构建，支持只构建指定包、强制重建与离线构建 |
| `akaribot docs sync-theme` | 把主题模板 submodule 同步到远端最新提交，只更新工作区 |
| `akaribot docs install-deps` | 安装主题所需的 Node 依赖，不生成站点 |
| `akaribot docs serve` | 启动本机静态服务器预览构建产物 |
| `akaribot docs deploy` | 把构建产物发布到 Vercel 或 S3 |
| `akaribot docs status` | 显示实际主题、最近一次构建的指纹、包清单、输出目录与部署记录 |
| `akaribot docs clean` | 清理生成目录，使下次构建从头开始 |

`list` 优先经实例的 core 入口读取包清单。入口不可用时，改用注册表里的已装包清单，并在警告中说明原因。CLI 自身的文档始终合并进目录。

`build`、`serve` 与 `deploy` 都会触发构建。不加 `--json` 时，命令实时打印工具链、生成与 VitePress 三个阶段，并转发 npm 与 VitePress 的逐行输出。加 `--json` 时，stdout 只保留最终结果行，日志写入 stderr。TUI 的文档页在构建期间显示同一份日志，按 `l` 切换面板。

模块文档在侧栏按 `doc.toml` 的 `category` 分组，条目名称取模块名。

同一模块目录内的页面显示为页内标签：`index.md` 是“使用方法”，`development.md` 是“安装与开发”。开发页不单独出现在侧栏。其余页面按 `order` 与路径排在两者之间。

内置 `bundled` 主题没有标签栏，开发页仍作为普通侧栏页面列出。包声明 `overview = false` 时不生成包级概览页，包入口指向第一页，侧栏直接列出页面。页面 front matter 写 `submenu` 时，同值的页面收进该名称的二级分组，普通页面仍平铺在前面。

侧栏最前固定显示“首页”。一级分组与模块文档的分类各带一个图标。分组图标写在 `docs.toml` 的 `[icons]` 里，键为分组名或 `home`。分类图标写在 `[category_icons]` 里，键为 `doc.toml` 的 `category`。两处的值都是主题注册的 M3E 图标名。

## 配置

站点标题、语言、基路径、输出目录、界面文案、分组标题与图标名由随包分发的 `akaribot/cli/docs/defaults.toml` 提供。实例根下的 `docs.toml` 只读不写，按表与键逐项覆盖，未覆盖的键沿用默认值。

```toml
[site]
title = "小可 · 文档"
lang = "zh-CN"
base = "/"
logo = ""
avatar = ""  # 对话示例的机器人头像，留空时取包声明的 avatar
favicon = ""
command_prefix = ""  # 留空时取实例核心配置的首个命令前缀
locales = ["zh-CN"]  # 首项为默认语言；只列一项时等同于单语言站点

[locales.zh-CN]
label = "简体中文"

# [locales.en-US]
# label = "English"
# title = "AkariBot Docs"
#
# [locales.en-US.labels]
# home = "Home"
#
# [locales.en-US.group_titles]
# module = "Modules"

[labels]
home = "首页"
overview = "概览"
usage = "使用方法"
development = "安装与开发"

[group_titles]
# 键为包分组，未列出的分组直接显示分组名
core = "核心"
module = "模块"

[icons]
home = "home"
module = "widgets"

[category_icons]
"音游查询" = "music_note"

[assets]
# 随包素材的文件名，相对 akaribot/cli/docs/assets/
favicon = "favicon.ico"

[build]
out_dir = "cache/docs/site"  # 留空时取 defaults.toml 的 [site] out_dir

[theme]
source = "auto"
color = "#d69cdd"

[deploy]
# 由命令层解释，引擎原样透传
```

- `site.title`：站点标题，同时用作首页标题与页面描述。留空时取 `defaults.toml` 的 `[site] title`。
- `site.lang`：页面语言标签。留空时取 `defaults.toml` 的 `[site] lang`。
- `site.base`：部署基路径。留空时取 `defaults.toml` 的 `[site] base`。环境变量 `AKARIBOT_DOCS_BASE` 优先于配置文件，值会被整理成以 `/` 开头、以 `/` 结尾的形式。
- `site.command_prefix`：命令用法行使用的前缀。留空时取 `config/config.toml` 中 `[config]` 的 `command_prefix` 首项。核心配置缺失或为空时不加前缀。
- `site.locales`：站点语言清单，首项为默认语言，标签形如 `zh-CN`。留空时只有 `site.lang` 一种语言。`site.lang` 与首项不一致时按配置错误终止，未写 `site.lang` 时取首项。清单中的标签要么在 `[locales.<标签>]` 下给出配置，要么已有随包默认值。
- `locales.<标签>`：该语言的显示名称 `label`、站点标题 `title`，以及逐键覆盖界面文案的 `labels`、覆盖分组标题的 `group_titles`。未写的项沿用 `defaults.toml` 与默认语言的值。
- `site.logo` / `site.avatar` / `site.favicon`：顶栏标志、对话示例头像与站点图标。
  - 相对路径按实例根解析，文件会复制到 `public/site-logo.<扩展名>`、`public/site-avatar.<扩展名>` 与 `public/site-favicon.<扩展名>`，并自动带上基路径。相对路径必须位于实例根内，且指向的文件存在。
  - HTTP(S) URL 与 `/` 开头的站点路径原样使用。
  - 三项留空时取默认值：
    - 顶栏标志取第一个声明了 `logo` 的包提供的图片，没有这样的包时沿用站点图标。
    - 对话头像取第一个声明了 `avatar` 的包提供的图片，没有这样的包时沿用站点图标。
    - 站点图标取 `[assets] favicon` 指向的随包文件。
- `labels`：界面文案。`home` 是侧栏首页条目，`overview` 是无页面时的占位标题，`usage` 与 `development` 是平行标签页的名称。`index_intro`、`footer` 与 `generated_header` 是生成内容里的固定语句。
- `group_titles`：侧栏一级分组的标题，键为包分组。
- `icons`：侧栏一级分组的图标名，键取分组（`core`、`builtin`、`cli`、`testing`、`module`、`adapter`、`asset`、`library`）或 `home`。主题只注册了有限的图标集，未注册的名称不会显示图标。
- `category_icons`：侧栏分类的图标名，键取 `doc.toml` 的 `category`。不在表内的分类不显示图标。分类图标与一级分组的图标一样，需要在主题里注册。
- `assets`：随包素材的文件名，目前只有 `favicon`，相对 `akaribot/cli/docs/assets/`。实例可以换成同目录内的其它文件名，或改用 `site.favicon` 指向实例内的文件。
- `build.out_dir`：输出目录，相对路径锚定实例根。留空时取 `defaults.toml` 的 `[site] out_dir`。
- `theme.source`：主题来源。`auto` 在实例根查找 `akari-bot-docs-template`、`vendor/akari-bot-docs-template` 或 `docs-theme`。从仓库源码运行 CLI 时还会查找仓库内的 `vendor/akari-bot-docs-template` submodule。找不到时使用 `bundled`。也可写 `bundled`、`file:<路径>` 或实例内的相对路径。环境变量 `AKARIBOT_DOCS_THEME` 优先于配置。
- `theme.color`：主题种子色，格式为 `#rrggbb`，留空使用主题默认值。Akari 主题写入 `settings.defaults.color`，访问者仍可在设置面板覆盖。内置 `bundled` 主题注入 `--vp-c-brand-*` 变量。
- `deploy`：部署目标配置，引擎不解释这些字段。

内容按语言分目录：默认语言读取包文档目录，其他语言读取 `doc/<标签>/`。某个语言缺少页面时，生成器复制默认语言的同名页面，访问者不会遇到空链接。跨包链接、侧栏与导航按语言加 `/<标签>/` 前缀。

生成器把默认语言写成 VitePress 的 `locales.root`，其余语言写成独立条目，并为每种语言生成自己的 `themeConfig`。主题的语言切换器据此展示可选语言。

`docs.toml` 不是合法的 TOML，或其中某一段不是表时，命令以配置错误终止。

### 部署配置

```toml
[deploy]
provider = "s3"

[deploy.vercel]
project_id = "prj_xxx"   # 与 org_id 同时给出时直接部署
org_id = "team_xxx"
project = "akaribot-docs" # 只有项目名时先执行 vercel link
scope = "team-slug"

[deploy.s3]
endpoint = "https://<account>.r2.cloudflarestorage.com"
bucket = "akaribot-docs"
region = "auto"
prefix = "docs/"
public_url = "https://docs.example.com"
addressing = "auto"       # auto / path / virtual
cache_control = ""        # 留空时 HTML 用 no-cache，assets/ 用 immutable
```

Vercel 的令牌只从环境变量 `VERCEL_TOKEN` 读取。S3 的密钥只从 `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 与可选的 `AWS_SESSION_TOKEN` 读取。区域默认取 `AWS_REGION` 或 `AWS_DEFAULT_REGION`，都没有时使用 `us-east-1`。`provider` 默认按存在的子表推断，两者都存在时取 `vercel`。

## 生成物

| 路径 | 内容 |
| --- | --- |
| `cache/docs/src` | 生成的 VitePress 源目录，每次构建前清空 |
| `cache/docs` | Node 工具链与 `node_modules` |
| `cache/docs/site` | 默认站点输出，可用 `build.out_dir` 改写 |
| `.docs/state.json` | 构建指纹、包清单与最近 50 条部署记录 |

生成器只接受位于 `cache/docs` 内的目标路径。包 key 必须匹配 `[A-Za-z0-9][A-Za-z0-9._-]*`，文档目录中的符号链接不得指向目录之外。文档目录可以包含 `.md`、常见图片、`.txt` 与 `.pdf`，其它后缀的文件会被忽略。

## 构建与缓存

构建指纹覆盖参与包的版本与标题、每个文档文件的内容、主题清单与主题目录的文件内容、VitePress 版本、站点标题、语言与基路径。

主题摘要按文件内容计算，包含 `package.json` 与 `package-lock.json`。更新 submodule 或替换主题文件后，构建指纹一定变化。

指纹未变且输出中仍有 `index.html` 时，命令直接复用上次结果。`--force` 忽略指纹，强制重建。

`docs status` 输出实际解析的主题名称、目录与摘要。更新主题后如果构建仍然复用上次结果，先用它确认 CLI 读到的主题目录。如果解析到的是内置模板，而不是预期的位置，调整 `[theme].source`，或把主题放到实例根。

构建结束后必须存在 `index.html`，否则按构建失败处理。

站点开启 `cleanUrls`：`a.md` 对应 `/a`，`index.md` 对应 `/<包 key>/`。首页按分组汇总各包，每个分组另有汇总页。

侧栏按包与页面清单生成，页面顺序取自 front matter 的 `order`。相同 `submenu` 的页面在包内组成二级分组。包的 `doc.toml` 写 `overview = false` 时，不生成 `/<包 key>/` 概览页。导航与分组页改为指向第一页，侧栏不再给包标题加链接。

## 预览

`serve` 使用内置静态服务器，默认只绑定回环地址，端口由调用方指定或交由系统分配。解析规则与 `cleanUrls` 一致：`/foo` 找不到文件时改为返回 `foo.html`。目录请求改为返回 `index.html`。其余请求交给 `404.html`。所有响应一律带 `Cache-Control: no-store`。

## 部署

`deploy` 的目标为 Vercel 与 S3。部署所需的密钥只从环境变量读取，不写入 `docs.toml`，也不进入 `.docs/state.json`。配置文件中只放仓库、项目、桶与路径这类非敏感信息。

每次部署向状态文件追加一条记录，包含目标、结果与时间。

## 主题

主题与引擎解耦：引擎只读取主题根目录的 `docs-theme.json`，复制清单声明的 `theme_dir`，按清单生成 VitePress 配置与依赖，不导入主题代码。清单字段：

| 字段 | 说明 |
| --- | --- |
| `name` / `version` | 主题标识与版本，参与构建指纹 |
| `theme_dir` | 相对主题根的主题目录，复制为站点 `.vitepress/theme` |
| `vitepress` | 该主题要求的 VitePress 版本 |
| `node` | Node.js 版本要求，如 `>=22.12.0` |
| `dependencies` | 安装到 `<实例根>/cache/docs` 的 npm 依赖 |
| `install_mode` | `ci`（复制主题的 lock）或 `install`（按依赖生成 package.json） |
| `config` | 生成配置所用声明：`appearance`、`clean_urls`、`custom_element_prefixes`、`head_module` / `head_export`、`markdown_module` / `markdown_export`、`theme_config_key`、`search` |

`akari-bot-docs-template` 提供 `vitepress-akari-theme-docs` 主题与 `docs-theme.json`，要求 Node.js 22.12 与 VitePress 2.0.0-alpha.21。本仓库用 `vendor/akari-bot-docs-template` submodule 提供该模板，克隆后执行 `git submodule update --init --recursive` 即可。实例也可以把 `theme.source` 指向自己的模板目录。

更新主题用 `akaribot docs sync-theme`。它拉取远程最新提交，只更新 submodule 工作区，父仓库的 gitlink 需要自行暂存。主题依赖变化后，用 `akaribot docs install-deps` 重装 npm 依赖。内置的 `bundled` 主题是同一约定的最小实现，在没有外部模板时使用它。

### 主题组件

外部模板的 `.vitepress/theme` 内置七个全局组件，并适配主题的 M3E 调色板：`ModuleMeta`（模块属性卡）、`ModuleConfig`（配置项）、`ModuleAlias`（模块级别名）、`ModuleData`（数据表）、`NoticeBox`（提示框）、`CommandUsage`（命令用法）与 `ChatExample`（命令对话示例）。

生成器读取包内 `doc.toml` 的 `[[meta.modules]]`，在包首页标题后自动注入 `ModuleMeta`。本仓库的模块页不声明该表，其余组件由文档按需使用，写法见仓库根 `docs/package-docs.md`。

组件只在 VitePress 构建产物中渲染，包内 Markdown 仍可直接阅读。主题目录整体复制到生成的站点，新增主题组件不需要修改生成器。

内置 `bundled` 主题也提供 `ModuleMeta`、`NoticeBox`、`CommandUsage` 与 `ChatExample` 的同名组件。它的 `ChatExample` 把图片渲染为缩略图，点击后在新标签页打开，气泡文本按纯文本处理。

外部模板的 `ChatExample` 行为如下：

- `messages` 中的消息显式设置 `markdown: true` 时按 Markdown 渲染，原始 HTML 不执行。其余消息按纯文本处理。
- 缩略图可以展开成图片预览浮层，浮层上的按钮交互可用。
- 整行只有三个以上波浪号时，渲染为时间分隔线。
- 尾部图片另起气泡，多张尾部图片共用一个气泡。
- 图片地址后的 `{natural}` 表示按原始尺寸展示，超过视口高度时等比缩小。
- `image-width` 用于固定示例内图片宽度。
- `:card` 在对话末尾渲染机器人卡片。
- 按钮项的 `buttons` 可以带二级按钮。`dismiss: true` 删除所属回复组。`:one-shot="true"` 在任一按钮点击后禁用同组按钮。

`ModuleAlias`、`ModuleConfig`、`ModuleData` 以及 `CommandUsage` 的 `params` 参数清单、`platforms` / `excluded` 平台徽章只在外部模板中提供。

## 文档编写约定

- 包内文档使用简体中文。面向用户的固定文案仍走 `I18NContext`，不要为了文档新增其它语言的 locale 文件。
- 页面以一级标题开头，文件名使用小写英文与连字符。图片放在 `doc/` 下随页面一起复制，并同步发布到 `/<包 key>/` 供组件按相对路径引用。
- 站内链接使用 `cleanUrls` 形式（`/包 key/页面`），跨包链接以包 key 开头。
- 页面正文只描述当前行为。变更历史由 git 承担。
