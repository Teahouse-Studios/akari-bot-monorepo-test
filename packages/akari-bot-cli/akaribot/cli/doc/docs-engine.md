# 文档引擎

文档引擎把已安装包的 `doc/` 目录汇总成一个 VitePress 站点：读取目录、生成站点源文件、调用
VitePress 构建、提供本机预览，并记录构建与部署状态。

## 当前状态

引擎实现在 `akaribot/cli/docs/`，具备目录收集、源文件生成、跨包链接折算、构建缓存、静态预览与
状态持久化。`akaribot docs` 已注册进 `akaribot` 主命令表，命令面见下表。

## 前置条件

- Node.js 主版本不低于 18，且 `npm` 在 `PATH` 中。
- 依赖固定在引擎模板的 `package-lock.json` 里，VitePress 版本为 1.6.4；安装只执行 `npm ci`。
- 首次构建需要联网安装依赖；离线模式要求 `<实例根>/cache/docs/node_modules` 已存在。

Node 缺失、版本过低或 npm 不可用时，构建以工具链错误终止，不退回其它渲染器。

## 命令

| 命令 | 用途 |
| --- | --- |
| `akaribot docs list` | 列出参与构建的包、分组、标题与页面数，附目录降级警告 |
| `akaribot docs build` | 生成站点源文件并构建，支持只构建指定包、强制重建与离线构建 |
| `akaribot docs serve` | 启动本机静态服务器预览构建产物 |
| `akaribot docs deploy` | 把构建产物发布到 Vercel 或 S3 |
| `akaribot docs status` | 显示最近一次构建的指纹、包清单、输出目录与部署记录 |
| `akaribot docs clean` | 清理生成目录，使下次构建从头开始 |

`list` 优先经实例的 core 入口读取包清单；入口不可用时退回注册表的已装包清单，并把降级原因作为
警告展示。CLI 自身的文档始终合并进目录。

## 配置

实例根下的 `docs.toml` 只读不写，缺省值如下：

```toml
[site]
title = "AkariBot 文档"
lang = "zh-CN"
base = "/"

[build]
out_dir = "cache/docs/site"

[deploy]
# 由命令层解释，引擎原样透传
```

- `site.title`：站点标题，同时用作首页标题与页面描述。
- `site.lang`：页面语言标签。
- `site.base`：部署基路径；环境变量 `AKARIBOT_DOCS_BASE` 优先于配置文件，值会被规范成以 `/`
  开头并结尾。
- `build.out_dir`：输出目录，相对路径锚定实例根。
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

构建指纹覆盖参与包的版本与标题、每个文档文件的内容、模板版本、VitePress 版本、站点标题、语言
与基路径。指纹未变且输出中仍有 `index.html` 时直接复用上次结果；强制重建忽略指纹。构建结束后
必须存在 `index.html`，否则按构建失败处理。

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

## 主题组件

模板的 `.vitepress/theme` 随 CLI 分发，内置三个全局组件：`ModuleMeta`（模块属性卡）、
`NoticeBox`（提示框）与 `CommandUsage`（命令用法）。生成器读取包内 `doc.toml` 的
`[[meta.modules]]`，在包首页标题后自动注入 `ModuleMeta`；其余组件由文档按需使用，写法见仓库根
`docs/package-docs.md`。

组件只在 VitePress 构建产物中渲染；包内 Markdown 仍可直接阅读，不要在组件标签里放必须显示的
正文。主题目录整体复制到生成的站点，新增组件不需要修改生成器。

## 文档编写约定

- 包内文档使用简体中文；面向用户的固定文案仍走 `I18NContext`，不要为了文档新增其它语言的
  locale 文件。
- 页面以一级标题开头，文件名使用小写英文与连字符；图片放在 `doc/` 下随页面一起复制。
- 站内链接使用 `cleanUrls` 形式（`/包 key/页面`），跨包链接以包 key 开头。
- 页面正文只描述当前行为；变更历史由 git 承担。
