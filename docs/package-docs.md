# 包文档编写指南

仓库内每个可安装包都在自己的导入包目录下带一份 `doc/`。文档引擎收集这些目录，合并成 VitePress
站点；同一条目同时供 `akaribot docs list` 与站点构建使用。

## 目录位置
`doc/` 必须位于**导入包的根目录**，不是分发包根、仓库根的 `docs/` 或测试目录。发现过程按
`akaribot.docs` entry point 的导入路径定位包，不导入包本身，因此 `doc/` 必须随 wheel 分发。

```
packages/akari-bot-module-my/
├── pyproject.toml
└── akaribot/modules/my_module/
    ├── __init__.py
    └── doc/{doc.toml, index.md, commands.md}
```

`akaribot/`、`akaribot/modules/` 是 PEP 420 命名空间目录，不得放 `__init__.py`；`doc/` 下只放
Markdown、图片、`.txt`/`.pdf` 附件与 `doc.toml`，不要提交构建产物或缓存。

## `doc.toml`
| 字段 | 说明 |
| --- | --- |
| `schema` | 固定为 `1`；缺省按 1 处理，其他值使整个文件被忽略 |
| `title` | 站点标题与侧栏名；缺省取导入路径最后一段 |
| `summary` | 一句话简介；缺省取分发元数据的 Summary |
| `order` | 排序权重，自小到大；缺省 500，非整数按 500 处理并告警 |
| `hidden` | 为 `true` 时该包不进入目录 |
| `kind` | 覆盖分组：`core`、`builtin`、`cli`、`testing`、`module`、`adapter`、`asset` 等 |

不写 `kind` 时按 key 推断：`core` / `builtin` / `cli` / `testing` 原样；`module-*` 归模块，
`adapter-*` 归适配器，`assets-*` 归资源，其余归 `library`。分组决定导航与分组页。第三方模块包与
适配器包分别使用 `module-`、`adapter-` 前缀，避免落进 `library` 分组。

## 模块属性卡
模块包可在 `doc.toml` 用 `[[meta.modules]]` 声明页首属性卡，生成器会把它渲染成 `ModuleMeta`
组件，不需要在 Markdown 里手写标签：

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

属性卡描述模块级信息；命令级权限仍写在命令表里。一个包注册多个模块时按声明顺序列出。

## 站点组件
CLI 的 VitePress 主题内置以下组件，所有包文档都可直接使用：

| 组件 | 用途 |
| --- | --- |
| `<ModuleMeta :modules="..." />` | 模块属性卡；由 `doc.toml` 自动注入，通常不手写 |
| `<NoticeBox type="warning" title="...">…</NoticeBox>` | 提示框，类型取 `info`、`tip`、`warning`、`danger`、`example`、`help` |
| `<CommandUsage usage="..." permission="..." :options="[...]" />` | 命令用法与选项表 |

组件只在构建后的站点中渲染；直接在 Markdown 阅读器里会显示为标签。属性卡由生成器注入，其它
组件按需使用，正文仍以 Markdown 为主。

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

只识别 `title`、`order`、`description` 三个单行标量键，不支持列表或嵌套结构。标题缺省取正文
第一个一级标题（跳过代码块），再缺省取文件名。`index.md` 始终排在该包最前，其余页面按
`order`、路径排序。

页面可携带 `.md`、`.png`、`.jpg`、`.jpeg`、`.gif`、`.svg`、`.webp`、`.avif`、`.txt`、`.pdf`；
其他后缀不进入站点。文档目录中的符号链接不得指向目录之外。

## 声明 entry point
在包的 `pyproject.toml` 声明 `akaribot.docs`，名称为 key，值为导入路径：

```toml
[project.entry-points."akaribot.docs"]
module-my-module = "akaribot.modules.my_module"
```

- key 决定 URL、生成目录名与默认分组，必须匹配 `[A-Za-z0-9][A-Za-z0-9._-]*`。
- 值只取 `:` 之前的导入路径；写成 `akaribot.modules.my_module:app` 也按包路径处理。
- key 重复时排序靠后的条目被忽略并告警；包已安装但 `doc/` 不存在或没有 Markdown 页面时，
  该包被跳过并记入警告。

`akaribot.core` 与 `akaribot.modules.core` 分别以 `core`、`builtin` 提供文档；CLI 的 `cli`
条目由命令行工具自身合并。

## 命令与生成物
`akaribot docs` 提供 `list`、`build`、`serve`、`deploy`、`status`、`clean`：
`list` 经实例的 core 入口读取已装包目录，入口不可用时退回注册表清单；`build` 生成站点并调用
VitePress；`serve` 在本机预览产物；`deploy` 发布到 Vercel 或 S3；`status` 读取构建与部署状态；
`clean` 清理生成目录。

构建需要 Node.js >= 18 与 `npm`，VitePress 固定为 1.6.4，依赖由 `npm ci` 安装。生成物位于
实例根的 `cache/docs/src`（站点源）、`cache/docs`（Node 工具链与 `node_modules`）与 `cache/docs/site`
（默认输出，可由 `build.out_dir` 改写）；构建指纹与部署记录在 `.docs/state.json`。

部署目标写在实例根 `docs.toml` 的 `[deploy]` 段，凭据只从环境变量读取，不写入配置文件与状态
文件。基路径默认 `/`，环境变量 `AKARIBOT_DOCS_BASE` 优先。

## 编写规则
- **简体中文**：包内文档只写简体中文。面向用户的固定文案仍用 `I18NContext`；不得为文档创建或
  修改 `locales/` 下 `zh_cn.json` 以外的语言文件，翻译由 Weblate 自动提交。
- **只写当前行为**：不写「原来如何、现在改为如何」，变更历史由 git 承担。
- **一级标题开头**：每页以 `# 标题` 开始，标题与 front matter 的 `title` 一致。
- **篇幅**：单页 40 至 120 行，只覆盖功能概述、基本使用与接口行为。
- **链接与图片**：同包页面使用相对路径；跨包页面按源码目录写相对路径，生成器会折算成站点 URL，
  也可以直接写 `/<包 key>/<页面>`。图片与附件放在 `doc/` 下用相对路径引用；`.txt` 与 `.pdf` 会
  发布到 `/<包 key>/` 路径下。

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
title = "我的模块"
summary = "示例模块的功能与命令。"
order = 100
```

`index.md` 以 `# 我的模块` 开头，说明安装、配置与命令入口即可。新增页面后运行
`python -m akaribot.core.entrypoints.docs --json` 核对清单与告警，再构建站点。
