# 文档引擎

文档引擎把已安装包的 `doc/` 目录汇总成一个 VitePress 站点：读取目录、生成站点源文件、调用
VitePress 构建、提供本机预览，并记录构建与部署状态。

## 当前状态

引擎实现在 `akaribot/cli/docs/`，具备目录收集、源文件生成、跨包链接折算、构建缓存、静态预览与
状态持久化。`akaribot docs` 已注册进 `akaribot` 主命令表，命令面见下表。

## 前置条件

- Node.js 与 `npm` 在 `PATH` 中。内置主题要求 Node.js 18 及以上；外部主题的要求由主题清单声明，
  `akari-bot-docs-template` 当前要求 Node.js 22.12 及以上。
- 内置主题的依赖固定在引擎模板的 `package-lock.json` 里（VitePress 1.6.4），安装执行 `npm ci`；
  外部主题由清单的 `dependencies` 生成 `package.json`，安装执行 `npm install`，VitePress 版本同样
  来自清单。
- 首次构建需要联网安装依赖；离线模式要求 `<实例根>/cache/docs/node_modules` 已包含主题所需版本。

Node 缺失、版本低于主题要求或 npm 不可用时，构建以工具链错误终止，不退回其它渲染器。

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

`list` 优先经实例的 core 入口读取包清单；入口不可用时退回注册表的已装包清单，并把降级原因作为
警告展示。CLI 自身的文档始终合并进目录。

`build` 以及 `serve` / `deploy` 触发的构建在人类模式实时打印工具链、生成与 VitePress 三个阶段，
并转发 npm 与 VitePress 的逐行输出；`--json` 时 stdout 只保留最终结果行，同样的日志写入 stderr，
供 TUI 与脚本采集。TUI 的文档页在构建期间展示同一份日志，`l` 切换面板显示。

模块文档在侧栏按 `doc.toml` 的 `category` 分组，条目名称取模块名。同一模块目录内的页面作为平行
页面显示为页内标签：`index.md` 是默认的“使用方法”，`development.md` 是“安装与开发”，开发页不单独
出现在侧栏；其余页面按 `order` 与路径排在两者之间。内置回退主题没有标签栏，开发页仍作为普通侧栏
页面列出。

侧栏最前固定显示“首页”。一级分组的图标写在 `docs.toml` 的 `[icons]`，键为分组名或 `home`，值为
主题注册的 M3E 图标名；未配置的分组由主题回退为 `category`。

## 配置

实例根下的 `docs.toml` 只读不写，缺省值如下：

```toml
[site]
title = "AkariBot 文档"
lang = "zh-CN"
base = "/"
logo = ""
favicon = ""

[icons]
home = "home"
core = "dashboard"
builtin = "layers"
cli = "article"
testing = "check"
module = "widgets"
adapter = "package_2"
asset = "palette"
library = "category"

[build]
out_dir = "cache/docs/site"

[theme]
source = "auto"
color = "#d69cdd"

[deploy]
# 由命令层解释，引擎原样透传
```

- `site.title`：站点标题，同时用作首页标题与页面描述。
- `site.lang`：页面语言标签。
- `site.base`：部署基路径；环境变量 `AKARIBOT_DOCS_BASE` 优先于配置文件，值会被规范成以 `/`
  开头并结尾。
- `site.logo` / `site.favicon`：顶栏 Logo 与站点图标。相对路径按实例根解析，文件会复制到
  `public/site-logo.<扩展名>` 与 `public/site-favicon.<扩展名>` 并自动带上基路径；HTTP(S) URL 与
  `/` 开头的站点路径原样使用。相对路径必须位于实例根内且文件存在。
- `icons`：侧栏一级项的图标名，键取分组（`core`、`builtin`、`cli`、`testing`、`module`、
  `adapter`、`asset`、`library`）或 `home`。主题只注册有限图标集，未注册的名称不会显示图标。
- `build.out_dir`：输出目录，相对路径锚定实例根。
- `theme.source`：主题来源。`auto` 在实例根查找 `akari-bot-docs-template`、`vendor/akari-bot-docs-template`
  或 `docs-theme`；从仓库源码运行 CLI 时还会查找仓库内的 `vendor/akari-bot-docs-template` submodule。
  找不到时使用 `bundled`；也可写 `bundled`、`file:<路径>` 或实例内的相对路径。环境变量
  `AKARIBOT_DOCS_THEME` 优先于配置。
- `theme.color`：主题种子色，格式为 `#rrggbb`，留空使用主题默认值。Akari 主题写入
  `settings.defaults.color`，读者仍可在设置面板覆盖；内置回退主题注入 `--vp-c-brand-*` 变量。
- `deploy`：部署目标配置，引擎不解释其字段。

`docs.toml` 不是 TOML 或某一段不是表时，命令以配置错误终止。

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

Vercel 的令牌只从环境变量 `VERCEL_TOKEN` 读取。S3 的凭据只从
`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 与可选的 `AWS_SESSION_TOKEN` 读取；区域缺省取
`AWS_REGION` 或 `AWS_DEFAULT_REGION`，最后回落到 `us-east-1`。`provider` 缺省时按存在的子表推断，
两者都存在时取 `vercel`。

## 生成物

| 路径 | 内容 |
| --- | --- |
| `cache/docs/src` | 生成的 VitePress 源目录，每次构建前清空 |
| `cache/docs` | Node 工具链与 `node_modules` |
| `cache/docs/site` | 默认站点输出，可用 `build.out_dir` 改写 |
| `.docs/state.json` | 构建指纹、包清单与最近 50 条部署记录 |

生成器只接受位于 `cache/docs` 内的目标路径；包 key 必须匹配 `[A-Za-z0-9][A-Za-z0-9._-]*`，
文档目录中的符号链接不得指向目录之外。页面可携带 `.md`、常见图片、`.txt` 与 `.pdf`，其它后缀
被忽略。

## 构建与缓存

构建指纹覆盖参与包的版本与标题、每个文档文件的内容、主题清单与主题目录的文件内容、VitePress
版本、站点标题、语言与基路径。主题摘要按文件内容计算，包含 `package.json` 与
`package-lock.json`，因此更新 submodule 或替换主题文件后一定触发重建。指纹未变且输出中仍有
`index.html` 时直接复用上次结果；`--force` 忽略指纹强制重建。

`docs status` 输出实际解析的主题名称、目录与摘要。更新主题后仍显示复用时，先用它确认 CLI 读到的
主题目录；如果指向内置模板而不是预期位置，调整 `[theme].source` 或把主题放到实例根。

构建结束后必须存在 `index.html`，否则按构建失败处理。

站点开启 `cleanUrls`：`a.md` 对应 `/a`，`index.md` 对应 `/<包 key>/`。首页按分组汇总各包，
每个分组另有汇总页；侧栏按包与页面清单生成，页面顺序取自 front matter 的 `order`。

## 预览

`serve` 使用内置静态服务器，默认只绑定回环地址，端口由调用方指定或交由系统分配。解析规则与
`cleanUrls` 一致：`/foo` 找不到文件时回落到 `foo.html`，目录请求回落到 `index.html`，其余交给
`404.html`；响应一律 `Cache-Control: no-store`。

## 部署

`deploy` 的目标为 Vercel 与 S3。部署所需凭据只从环境变量读取，不写入 `docs.toml`，也不进入
`.docs/state.json`；配置文件中只放仓库、项目、桶与路径这类非敏感目标。每次部署向状态文件追加
一条记录，包含目标、结果与时间。

## 主题

主题与引擎解耦：引擎只读取主题根目录的 `docs-theme.json`，复制清单声明的 `theme_dir`，按清单生成
VitePress 配置与依赖，不导入主题代码。清单字段：

| 字段 | 说明 |
| --- | --- |
| `name` / `version` | 主题标识与版本，参与构建指纹 |
| `theme_dir` | 相对主题根的主题目录，复制为站点 `.vitepress/theme` |
| `vitepress` | 该主题要求的 VitePress 版本 |
| `node` | Node.js 版本要求，如 `>=22.12.0` |
| `dependencies` | 安装到 `<实例根>/cache/docs` 的 npm 依赖 |
| `install_mode` | `ci`（复制主题的 lock）或 `install`（按依赖生成 package.json） |
| `config` | 生成配置所用声明：`appearance`、`clean_urls`、`custom_element_prefixes`、`head_module` / `head_export`、`markdown_module` / `markdown_export`、`theme_config_key`、`search` |

`akari-bot-docs-template` 提供 `vitepress-akari-theme-docs` 主题与 `docs-theme.json`，要求 Node.js
22.12 与 VitePress 2.0.0-alpha.21。本仓库以 `vendor/akari-bot-docs-template` submodule 提供该模板，
克隆后执行 `git submodule update --init --recursive` 即可；实例也可以把 `theme.source` 指向自己的
模板 checkout。更新主题用 `akaribot docs sync-theme`：它拉取远端最新提交并只更新 submodule 工作区，
父仓库的 gitlink 需要自行暂存；`akaribot docs install-deps` 在主题依赖变化后重装 npm 依赖。内置的
`bundled` 主题是同一契约的最小实现，用于没有外部模板时的回退。

### 主题组件

外部模板的 `.vitepress/theme` 内置 `ModuleMeta`（模块属性卡）、`NoticeBox`（提示框）与
`CommandUsage`（命令用法）三个全局组件，并针对主题的 M3E 调色板适配。生成器读取包内 `doc.toml`
的 `[[meta.modules]]`，在包首页标题后自动注入 `ModuleMeta`；其余组件由文档按需使用，写法见仓库根
`docs/package-docs.md`。

组件只在 VitePress 构建产物中渲染；包内 Markdown 仍可直接阅读。主题目录整体复制到生成的站点，
新增主题组件不需要修改生成器。内置 `bundled` 主题保留同名组件作为回退。

## 文档编写约定

- 包内文档使用简体中文；面向用户的固定文案仍走 `I18NContext`，不要为了文档新增其它语言的
  locale 文件。
- 页面以一级标题开头，文件名使用小写英文与连字符；图片放在 `doc/` 下随页面一起复制。
- 站内链接使用 `cleanUrls` 形式（`/包 key/页面`），跨包链接以包 key 开头。
- 页面正文只描述当前行为；变更历史由 git 承担。
