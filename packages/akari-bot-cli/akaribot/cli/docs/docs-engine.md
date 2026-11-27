# 文档引擎

文档引擎将已安装包的 `docs/` 目录汇总为一个 VitePress 站点。它负责读取目录、生成站点源码、调用 VitePress 执行构建、提供静态预览与开发预览，并记录构建与部署状态。

## 当前状态

引擎实现在 `akaribot/cli/docs_engine/`，包含目录收集、源文件生成、跨包链接转换、构建缓存、静态预览、开发预览与状态持久化。`akaribot docs` 已注册至 `akaribot` 主命令表。

## 前置条件

- Node.js 与 `npm` 需要在 `PATH` 中。内置主题与外部主题的 Node.js 版本要求在各自的主题清单中声明。
- 内置主题的依赖固定在引擎模板的 `package-lock.json` 中，安装时执行 `npm ci`。外部主题的 `package.json` 根据清单的 `dependencies` 生成，安装时执行 `npm install`，VitePress 版本来自清单声明。
- 首次构建需要联网安装依赖。离线模式要求 `<实例根目录>/cache/docs/node_modules` 已包含主题所需版本。

若 Node.js 缺失、版本低于主题要求或 npm 不可用，构建将直接以工具链错误终止，不回退至其他渲染器。

## 命令

| 命令 | 用途 |
| --- | --- |
| `akaribot docs list` | 列出参与构建的包、分组、标题与页面数，附目录降级警告 |
| `akaribot docs build` | 生成站点源码并构建，支持仅构建指定包、强制重建与离线构建 |
| `akaribot docs sync-theme` | 将主题模板 submodule 同步至远端最新提交，仅更新工作区 |
| `akaribot docs install-deps` | 安装主题所需的 Node 依赖，不生成站点 |
| `akaribot docs serve` | 启动本机静态服务器预览构建产物 |
| `akaribot docs dev` | 监听文档与主题改动，在 `cache/docs/dev` 上运行 VitePress 开发服务器 |
| `akaribot docs deploy` | 将构建产物发布至 Vercel 或 S3 |
| `akaribot docs status` | 显示实际主题、最近一次构建的校验信息、包清单、输出目录与部署记录 |
| `akaribot docs clean` | 清理生成目录，使下次构建重置为空白状态 |

`list` 优先通过实例的 core 入口读取包清单。入口不可用时，改用注册表中的已安装包清单，并在警告中说明原因。CLI 自身的文档始终合并到目录中。

`build`、`serve` 与 `deploy` 均会触发构建。不加 `--json` 时，命令实时打印工具链、生成与 VitePress 三个阶段，并转发 npm 与 VitePress 的逐行输出。

加 `--json` 时，stdout 仅保留最终结果行，日志写入 stderr。

TUI 的文档页在构建期间展示同一日志流，按 `l` 切换面板。`dev` 不加 `--json` 时打印阶段、同步结果与提示，加 `--json` 时输出逐行事件，子进程日志写入 stderr。

模块文档在侧边栏按 `docs/config/global/docs.global.toml` 的 `category` 分组，条目名称使用模块名。

包内的标题、简介、分类与品牌插槽配置于 `docs/config/global/docs.global.toml` 中。同一个包支持另行提供 `docs/config/docs.toml`，按同名键覆盖默认值。

两个位置都接受 JSON 文件，文件名分别为 `docs.global.json` 与 `docs.json`。没有 `docs/config/` 时回退至旧的 `docs/doc.toml`，兼容尚未迁移的包。


同一模块目录内的页面显示为页内标签，其中 `index.md` 是“使用方法”，`development.md` 是“安装与开发”。开发页不单独出现在侧边栏。其余页面按 `order` 与路径排在两者之间。

内置 `bundled` 主题无标签栏，开发页仍作为普通侧边栏页面列出。包声明 `overview = false` 时不生成包级概览页，包入口直接指向首个页面，侧边栏直接列出对应页面。页面 front matter 配置 `submenu` 时，取值相同的页面归入该名称的二级分组，普通页面仍直接排列在前方。

侧边栏最前固定显示“首页”。一级分组与模块文档的分类各带一个图标。

分组图标配置在 `docs.toml` 的 `[icons]` 中，键为分组名或 `home`。

分类图标配置在 `[category_icons]` 中，键为 `docs/config/global/docs.global.toml` 的 `category`。两处的配置值均为主题注册的 M3E 图标名称。内置主题使用内置 M3E 字体渲染图标，外部模板亦支持映射到自身的图标集合。

## 配置

站点标题、语言、基础路径、输出目录、界面文案、分组标题与图标名由随包分发的 `akaribot/cli/docs_engine/defaults.toml` 提供。实例根目录下的 `docs.toml` 仅供读取而不写入，缺失的配置键从默认层读取。

```toml
[site]
title = "小可 · 文档"
lang = "zh-CN"
base = "/"
logo = ""
logo_dark = ""
avatar = ""  # 对话示例的机器人头像
character = ""
credits = ""
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

[footer]
title = "关于小可"
text = [
    "小可是由 Teahouse Studios 出品的多功能、跨平台、可自由扩展的聊天机器人助手，基于 AGPL-3.0 协议开源。",
    "请支持我们的工作以便持续开发与维护。",
]

[[footer.links]]
text = "爱发电"
link = "https://afdian.com/a/teahouse"
icon = "afdian"

[[footer.links]]
text = "GitHub"
link = "https://github.com/Teahouse-Studios/akari-bot"
icon = "github"

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
webp = true  # 留空时取 defaults.toml 的 [build] webp
webp_keep_original = true  # 留空时取 defaults.toml 的 [build] webp_keep_original

[theme]
source = "auto"
color = "#d69cdd"

[deploy]
# 由命令层解释，引擎原样透传
```

- `site.title`：站点标题，同时用作首页标题与页面描述。留空时使用 `defaults.toml` 的 `[site] title`。
- `site.lang`：页面语言标签。留空时使用 `defaults.toml` 的 `[site] lang`。
- `site.base`：部署基础路径。留空时使用 `defaults.toml` 的 `[site] base`。环境变量 `AKARIBOT_DOCS_BASE` 优先于配置文件，值会被整理成以 `/` 开头、以 `/` 结尾的形式。
- `site.command_prefix`：命令用法行使用的前缀。留空时先读取 `config/global/config.global.toml` 或 `.json`，再由 `config/config.toml` 的 `[config] command_prefix` 覆盖，使用最终列表的首项。核心配置缺失或为空时不加前缀。
- `site.locales`：站点语言清单，首项为默认语言，标签形如 `zh-CN`。留空时只有 `site.lang` 一种语言。`site.lang` 与首项不一致时按配置错误终止，未配置 `site.lang` 时使用首项。清单中的标签要么在 `[locales.<标签>]` 下给出配置，要么已有随包默认值。
- `locales.<标签>`：该语言的显示名称 `label`、站点标题 `title`，以及逐键覆盖界面文案的 `labels`、覆盖分组标题的 `group_titles`。未配置的项沿用 `defaults.toml` 与默认语言的值。
- `site.logo` / `site.logo_dark` / `site.avatar` / `site.character` / `site.credits` / `site.favicon`：品牌插槽与站点图标。
  - 相对路径按实例根目录解析。品牌文件复制到 `public/brand-logo.<扩展名>`、`public/brand-logo-dark.<扩展名>`、`public/brand-avatar.<扩展名>`、`public/brand-character.<扩展名>` 与 `public/brand-credits.<扩展名>`，站点图标复制到 `public/site-favicon.<扩展名>`。相对路径必须位于实例根目录内，且指向的文件存在。
  - HTTP(S) URL 与 `/` 开头的站点路径原样使用。品牌插槽的站点路径不带基础路径，主题组件会用 `withBase()` 补上。
  - 品牌插槽按以下顺序取值：
    1. `docs.toml` 的 `[site]` 字段。
    2. 第一个 `brand = true` 的文档包在 `docs/config/global/docs.global.toml` 中声明的同名字段。
    3. 内置资源。
  - 没有 `brand = true` 的包时，回退至第一个声明 `logo` 或 `avatar` 的包。
  - 内置回退为 `logo.png`、`logo-night.png`、`logo.png`、`placeholder.png`。`credits` 没有内置文件时为空。品牌包缺失不会让构建失败。
  - 站点图标使用 `[assets] favicon` 指向的随包文件。
- `themeConfig.akari.brand`：生成器输出的品牌插槽，供主题组件读取。

  | 键 | 内容 |
  | --- | --- |
  | `logo` | 日间标志 |
  | `logoDark` | 夜间标志 |
  | `avatar` | 对话示例头像 |
  | `character` | 角色立绘 |
  | `credits` | 制作人员文本 |

  `akari.appBar.logo`、`akari.appBar.logoDark` 与 `akari.chatAvatar` 是兼容字段，分别与 `logo`、`logoDark`、`avatar` 相同。
- `footer`：页脚关于区块。`title` 是标题，`text` 是说明段落（字符串或字符串数组），`image` 是配图，`links` 是按钮。
  - 未写 `image` 时使用角色立绘。配图复制到 `public/footer-image.<扩展名>`。
  - `links[].icon` 写 `afdian` 或 `github` 时使用主题内置的品牌图形，其他值按品牌插槽的规则解析为图片并复制到 `public/footer-icon-<序号>.<扩展名>`。
  - `text` 与 `links` 写空数组表示不显示该部分。`enabled = false` 时页脚仅保留落款。
  - 生成器把区块写入 `themeConfig.akari.footer.about`，随 CLI 分发的页脚组件据此渲染配图、标题、段落与按钮。
  - 页脚按两栏排版：左侧配图，右侧文案与按钮，两栏在文档宽度内居中靠拢，落款居中。视口窄于 840 像素时改为单栏，配图放大且文字居中。
- `labels`：界面文案。`home` 是侧栏首页条目，`overview` 是无页面时的占位标题，`usage` 与 `development` 是平行标签页的名称。`index_intro`、`footer` 与 `generated_header` 是生成内容里的固定语句。
- `group_titles`：侧栏一级分组的标题，键为包分组。
- `icons`：侧栏一级分组的图标名，键取分组（`core`、`builtin`、`cli`、`testing`、`module`、`adapter`、`asset`、`library`）或 `home`。主题只注册了有限的图标集，未注册的名称不会显示图标。
- `category_icons`：侧栏分类的图标名，键取 `docs/config/global/docs.global.toml` 的 `category`。不在表内的分类不显示图标。分类图标与一级分组的图标一样，需要在主题里注册。
- `assets`：随包素材的文件名，目前只有 `favicon`，相对 `akaribot/cli/docs/assets/`。实例可以换成同目录内的其他文件名，或改用 `site.favicon` 指向实例内的文件。
- `build.out_dir`：输出目录，相对路径以实例根目录为基准。留空时取 `defaults.toml` 的 `[site] out_dir`。
- `build.webp`：构建时把页面引用的位图转成 WebP，默认开启。默认值由 `defaults.toml` 的 `[build] webp` 提供。
- `build.webp_keep_original`：转换后保留原图，默认开启。默认值由 `defaults.toml` 的 `[build] webp_keep_original` 提供。保留原图时，脚本文本里写死的原图路径仍然可用。
- `theme.source`：主题来源。`auto` 在实例根目录查找 `akari-bot-docs-template`、`vendor/akari-bot-docs-template` 或 `docs-theme`。从仓库源码运行 CLI 时还会查找仓库内的 `vendor/akari-bot-docs-template` submodule。找不到时使用 `bundled`。也可写 `bundled`、`file:<路径>` 或实例内的相对路径。环境变量 `AKARIBOT_DOCS_THEME` 优先于配置。
- `theme.color`：主题种子色，格式为 `#rrggbb`，留空使用主题默认值。Akari 主题把它写入 `settings.defaults.color`，访问者仍可在设置面板覆盖。内置 `bundled` 主题注入 `--vp-c-brand-*` 变量。
- `deploy`：部署目标配置，引擎不解释这些字段。

内容按语言分目录存放，默认语言读取包文档目录，其他语言读取 `docs/<标签>/`。某个语言缺少页面时，生成器复制默认语言的同名页面，访问者不会遇到空链接。跨包链接、侧边栏与导航按语言加 `/<标签>/` 前缀。

跨包链接以对应包的 `docs/` 下相对路径书写，生成器会自动转换为站点 URL。站内绝对路径保持不变。

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

Vercel 的令牌仅从环境变量 `VERCEL_TOKEN` 读取。S3 的密钥仅从 `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 与可选的 `AWS_SESSION_TOKEN` 读取。实例根目录的 `docs.toml` 不记录登录信息。

## 生成产物

| 路径 | 内容 |
| --- | --- |
| `cache/docs/src` | 生成的 VitePress 源目录，每次构建前清空 |
| `cache/docs` | Node 工具链与 `node_modules` |
| `cache/docs/site` | 默认站点输出，可用 `build.out_dir` 改写 |
| `cache/docs/dev` | 开发模式使用的 VitePress 源目录，其中 `node_modules` 由同步保留 |
| `cache/docs/.dev-staging` | 开发模式同步用的暂存目录 |
| `cache/docs/.dev.lock` | 开发模式运行锁，记录进程、端口与基路径 |
| `.docs/state.json` | 构建指纹、包清单与最近 50 条部署记录 |

生成器仅接受位于 `cache/docs` 内的目标路径。包 key 必须匹配 `[A-Za-z0-9][A-Za-z0-9._-]*`，文件名必须匹配 `[A-Za-z0-9_.-]+.md`，包含非法字符即被拒绝。路径必须限制在包的 `docs/` 范围内，以防止目录遍历。

### 首页数据

首页的文案、按钮、统计项、角色入口、主题卡与贡献卡来自 `packages/akari-bot-cli/akaribot/cli/docs_engine/home/home.json`。`schema` 当前为 `1`，字段如下：

| 字段 | 内容 |
| --- | --- |
| `title` / `lead` | 首页标题与说明 |
| `sections` | 界面文案，包含搜索框占位、统计区标签、快速开始、主题区与参与贡献的标题 |
| `actions` | 首屏主按钮与文字链接 |
| `stats` | 统计项，`source` 可选 `core_version`、`total_pages`、`module_count`、`adapter_count` |
| `roles` | 使用者与开发者入口，包含说明和链接 |
| `topics` | 按主题浏览的图片卡 |
| `contribute` | 贡献与翻译卡片 |

链接写成 `package` + `page`、`group` 或 `url`，生成器会按站点结构转换地址。未识别的字段会被忽略，缺少必填字段或类型不符时按配置错误终止构建。

## 构建与缓存

构建校验信息覆盖参与包的版本与标题、每个文档文件的内容、主题清单与主题目录的文件内容、VitePress 版本、站点标题、语言与基础路径。

主题模板目录中的静态文件、组件与样式整体复制到构建目录。生成器不会覆盖已存在的主题同名文件。

校验信息未变化且输出中仍有 `index.html` 时，命令直接复用上次结果。`--force` 忽略校验信息，强制重建。

`docs status` 输出实际解析的主题名称、目录与摘要。更新主题后如果构建仍然复用上次结果，先通过它确认 CLI 读取到的主题目录。如果解析到的是内置模板，而不是预期的位置，调整 `[theme].source`，或把主题放到实例根目录。

部署配置保存在实例根目录的 `docs.toml` 中。未配置时仅在本地预览，不执行上传。支持的平台为 Vercel 与 S3。

站点开启 `cleanUrls`，`a.md` 对应 `/a`，`index.md` 对应 `/<包 key>/`。首页按分组汇总各包，每个分组另有汇总页。

侧边栏按包与页面清单生成，页面顺序取自 front matter 的 `order`。相同 `submenu` 的页面在包内组成二级分组。包的 `docs/config/global/docs.global.toml` 配置 `overview = false` 时，不生成 `/<包 key>/` 概览页。导航与分组页指向第一页，侧边栏不为包标题添加链接。

## 预览

`serve` 使用内置静态服务器，默认只绑定回环地址，端口由调用方指定或交由系统分配。

解析规则与 `cleanUrls` 一致，`/foo` 找不到文件时返回 `foo.html`。目录请求返回 `index.html`。

其余请求交由 `404.html` 处理。所有响应一律携带 `Cache-Control: no-store`。

## 开发模式

`dev` 持续监听参与构建的文档目录、主题目录与站点配置，把改动同步至实例的 `cache/docs/dev`，并在该目录上运行 VitePress 的开发服务器。浏览器端的更新由 Vite 的热更新完成，不经过 VitePress 的构建。

监听范围与处理方式：

| 目标 | 变化后的处理 |
| --- | --- |
| 参与包的 `docs/` 目录 | 页面增删时重新读取包清单，其余改动仅重新生成与同步 |
| 主题目录 | 重新解析主题并同步主题组件 |
| `docs.toml` | 重新读取全量配置并重新生成所有页面 |

生成器先写入 `cache/docs/.dev-staging`，再按文件内容比对同步至 `cache/docs/dev`，仅写入实际变化的文件。`cache/docs/dev/node_modules` 存放依赖，`.vitepress/cache` 存放 Vite 的预构建产物，两者都在同步范围之外。

生成器每次清空并重写全部源文件，因此必须差分同步，否则直接改写镜像会让 Vite 在每批改动上全量失效。

运行行为：

- 变更在 0.6 秒的静默窗口内合并为一批，间隔由 `--interval` 调整。
- `--package` 仅监听指定包，其余包仍参与生成与跨包链接转换。
- 默认端口 5173，被占用时改用系统分配的端口。`--port 0` 直接将端口选择交由系统处理。
- 启动时写入 `cache/docs/.dev.lock`。同一实例上 `dev` 与 `clean`、`install-deps` 互斥，`status` 据此报告开发模式状态。
- 开发服务器与静态预览共用 `cache/docs/node_modules`，二者不能同时运行。在 TUI 中启动其中一个时，会自动停止另一个。
- `--json` 输出逐行事件：`stage`、`ready`、`sync`、`warn`、`error`、`stopped`。工具链安装与首次生成发生在 `ready` 之前，`ready` 携带站点地址。

开发模式不写入 `.docs/state.json`，也不改动 `cache/docs/site`。

## 部署

`deploy` 的目标为 Vercel 与 S3。部署所需的密钥仅从环境变量读取，不写入 `docs.toml`，也不进入 `.docs/state.json`。配置文件中仅保留仓库、项目、桶与路径这类非敏感信息。

每次部署向状态文件追加一条记录，包含目标、结果与时间。

若未配置 `bucket`、`endpoint` 或 `region`，命令会在部署前输出错误提示。

仓库的 Pages 工作流在临时实例 `.ci-docs` 中执行构建，基础路径取自 Pages 的项目路径（`AKARIBOT_DOCS_BASE`）。站内链接与资源地址因此在构建阶段便包含该前缀。

仓库在 Settings → Pages 的 Source 必须为 GitHub Actions。工作流在 Pages 尚未启用时会自动打开它。

## 主题

外部主题仅通过根目录的 `docs-theme.json` 声明主题目录、依赖、VitePress/Node 要求与生成选项，引擎不导入主题代码。

| 字段 | 说明 |
| --- | --- |
| `name` / `version` | 主题标识与版本，参与构建校验信息 |
| `theme_dir` | 相对主题根目录的主题目录，复制为站点 `.vitepress/theme` |
| `vitepress` | 该主题要求的 VitePress 版本 |
| `node` | Node.js 版本要求，如 `>=x.y.z` |
| `dependencies` | 安装至 `<实例根目录>/cache/docs` 的 npm 依赖 |
| `install_mode` | `ci`（复制主题的 lock）或 `install`（按依赖生成 package.json） |
| `config` | 生成配置所用声明：`appearance`、`clean_urls`、`custom_element_prefixes`、`head_module` / `head_export`、`markdown_module` / `markdown_export`、`theme_config_key`、`search` |

页脚不在主题内部实现。生成器复制主题目录后，将主题入口 `index.ts` 重命名为 `theme-entry.ts`，写入独立的 `index.ts` 与 `footer/` 组件。新的入口应用模板主题，再通过 `provideAkariComponents()` 覆盖 `Footer` 插槽。

模板仓库保持原样，升级主题不会覆盖页脚改动。主题没有 `composables/useAkariConfig.ts`（即不支持插槽覆盖）时跳过这层替换，站点沿用主题自带的页脚。

`akari-bot-docs-template` 提供 `vitepress-akari-theme-docs` 主题与 `docs-theme.json`，Node.js 与 VitePress 版本由该文件声明。本仓库使用 `vendor/akari-bot-docs-template` submodule 提供该模板，克隆后执行 `git submodule update --init --recursive` 即可。实例亦支持将 `theme.source` 指向自定义模板目录。

更新主题使用 `akaribot docs sync-theme`。其拉取远程最新提交，仅更新 submodule 工作区，父仓库的 gitlink 需要自行暂存。

主题依赖变化后，用 `akaribot docs install-deps` 重新安装 npm 依赖。

内置的 `bundled` 主题是同一约定的最小实现，在没有外部模板时使用它。

### 主题组件

外部模板的 `.vitepress/theme` 提供以下全局组件，并适配主题的 M3E 调色板：`ModuleMeta`（模块属性卡）、`ModuleConfig`（配置项）、`ModuleAlias`（模块级别名）、`ModuleData`（数据表）、`NoticeBox`（提示框）、`CommandUsage`（命令用法）、`ChatExample`（命令对话示例）与 `PackageDependencies`（运行依赖）。

生成器读取包内 `docs/config/global/docs.global.toml` 的 `[[meta.modules]]`，在包首页标题后自动注入 `ModuleMeta`。本仓库的模块页不声明该表，其余组件由文档按需使用，写法参见仓库根目录 `docs/package-docs.md`。

依赖段落用 `<PackageDependencies package="<包 key 或包名>" />`。生成器读取已安装包元数据里的 `Requires-Dist`，过滤 `extra` 可选依赖，把结果写入 `themeConfig.akari.dependencies`。组件按包 key 与包名读取列表，文档中不填写版本范围。

组件仅在 VitePress 构建产物中渲染，包内 Markdown 仍可直接阅读。主题目录整体复制到生成的站点，新增主题组件无需修改生成器。

内置 `bundled` 主题也提供 `ModuleMeta`、`NoticeBox`、`CommandUsage`、`ChatExample` 与 `PackageDependencies` 的同名组件。它的 `ChatExample` 把图片渲染为缩略图，点击后在新标签页打开，气泡文本按纯文本处理。

外部模板的 `ChatExample` 行为如下：

- `messages` 中的消息显式设置 `markdown: true` 时按 Markdown 渲染，原始 HTML 不执行。其余消息按纯文本处理。
- 缩略图可以展开成图片预览浮层，浮层上的按钮交互可用。
- 整行只有三个以上波浪号时，渲染为时间分隔线。
- 尾部图片单独成气泡，多张尾部图片共用一个气泡。
- 图片地址后的 `{natural}` 表示按原始尺寸展示，超过视口高度时等比缩小。
- `image-width` 用于固定示例内图片宽度。
- `:card` 在对话末尾渲染机器人卡片。
- 按钮项的 `buttons` 可以带二级按钮。`dismiss: true` 删除所属回复组。`:one-shot="true"` 在任一按钮点击后禁用同组按钮。

`ModuleAlias`、`ModuleConfig`、`ModuleData` 以及 `CommandUsage` 的 `params` 参数清单、`platforms` / `excluded` 平台徽章仅在外部模板中提供。

## 文档编写约定

- 包内文档使用简体中文。面向用户的固定文案仍使用 `I18NContext`，不要为了文档新增其他语言的 locale 文件。
- 页面以一级标题开头，文件名使用小写英文与连字符。图片放在 `docs/` 下随页面一起复制，并同步发布到 `/<包 key>/` 供组件按相对路径引用。
- 站内链接使用 `cleanUrls` 形式（`/包 key/页面`），跨包链接以包 key 开头。
- 页面正文仅描述当前行为。变更历史由 git 记录。
