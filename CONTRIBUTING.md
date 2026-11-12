# 贡献指南

感谢你对小可及其衍生项目的关注。

本项目接受各种形式的贡献，各类参与方式与处理流程见下方[目录](#目录)。参与前请阅读对应章节，以减少维护者的沟通成本。

> [!NOTE]
> 不打算贡献代码时，也可以通过以下方式支持本项目：
> - 为本仓库点 Star
> - 在自己项目的 README 中引用本项目
> - 将机器人加入群聊或服务器
> - 向他人推荐本项目

## 目录

- [提出问题](#提出问题)
- [做出贡献](#做出贡献)
  - [报告错误](#报告错误)
  - [提出建议](#提出建议)
  - [本地化](#本地化)
- [提交代码更改](#提交代码更改)
  - [快速开始](#快速开始)
  - [开发环境](#开发环境)
    - [依赖冲突与联合求解](#依赖冲突与联合求解)
  - [分支命名](#分支命名)
  - [提交规范](#提交规范)
  - [PR 描述](#pr-描述)
  - [代码风格](#代码风格)
  - [新增模块包](#新增模块包)
- [文字排版](#文字排版)

## 提出问题

> [!NOTE]
> 建议先阅读[《提问的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)。
>
> 本指南不提供本项目的实际支持服务。

提问前请先搜索是否已有同类 [Issue](https://github.com/Teahouse-Studios/akari-bot/issues)。能在搜索引擎中找到答案的问题，不建议提交 Issue。

需要联系开发者时，可通过以下渠道：

- 在 Issue 中[创建新问题](https://github.com/Teahouse-Studios/akari-bot/issues/new)
- 加入 QQ 平台的[小可公共实例测试群（738829671）](https://qm.qq.com/q/Rmuo5ORYgq)或[茶馆工作室聊天群（979982065）](https://qm.qq.com/q/sjwFNX1NVC)

无论通过哪种渠道，都请**尽可能详细地描述**问题。

## 做出贡献

### 报告错误

> [!WARNING]
> **绝对不要**在 Issue 或其他任何公开渠道报告或复现包含敏感信息的安全问题或漏洞。
> 
> 涉及敏感内容的问题必须通过电子邮件或私聊联系开发者，详见 [`SECURITY.md`](/SECURITY.md)。
>
> 违反本条规则的内容将被删除，由此产生的后果由发布者承担。

提交前请确认是否已有同类 [Issue](https://github.com/Teahouse-Studios/akari-bot/issues)。

若没有，请使用[错误报告模板](https://github.com/Teahouse-Studios/akari-bot/issues/new?template=report_bug.yaml)创建新的 Issue，并提供以下信息：
- 错误的简要描述
- 复现步骤
- 预期结果和实际结果
- 错误信息（若有）

报告应包含上述信息，避免维护者反复追问细节。

### 提出建议

提交前请确认是否已有同类 [Issue](https://github.com/Teahouse-Studios/akari-bot/issues)。

若没有，请使用[功能建议模板](https://github.com/Teahouse-Studios/akari-bot/issues/new?template=feature_request.yaml)创建新的 Issue，并提供：
- 建议的简要描述
- 可能的实现方案（若有）
- 建议对项目有益的理由（推荐）

已完成开发的改动同样建议先提交 Issue 讨论，再创建 PR。

### 本地化

多语言内容由 Weblate 托管，翻译改进请前往 [Weblate](https://hosted.weblate.org/engage/akaribot)。

除简体中文外，翻译问题请在 Weblate 讨论，不提交到 Issue。

没有 Weblate 账号时可联系开发者代为提交。

## 提交代码更改

本节面向准备提交代码的贡献者。本项目对代码改动的限制较少，但下列约定须遵守。

### 快速开始

1. Fork 本仓库
2. 克隆 Fork 到本地
3. 创建新分支
4. 完成改动
5. 向本项目提交 PR

提交规范见视频[《🐧你为啥直接 commit 到我的 master 分支啊》](https://bilibili.com/video/BV1pwC6BxEeb)。

### 开发环境

本项目使用 Python，最低版本要求见 [README](/README.md)。推荐使用 [PyCharm](https://www.jetbrains.com/pycharm) 或
[VS Code](https://code.visualstudio.com)。

本项目使用 [uv](https://docs.astral.sh/uv) 管理依赖，安装依赖：

```sh
uv sync
```

新增依赖：

```sh
uv add <包名>
```

新增依赖须放入 `pyproject.toml` 中对应的注释分组，并按字母顺序排列。

改动依赖后更新锁文件：

```sh
uv lock
```

### 依赖冲突与联合求解

本项目已拆分为 uv workspace，全部官方包共用根目录下的单一 `uv.lock`。该文件对全部成员包做一次**联合求解**，因而各包声明的第三方依赖若互相排斥，`uv lock` 会立即失败，例如两个包对 `packaging` 的可接受区间没有交集：

```sh
  × No solution found when resolving dependencies:
  ╰─▶ Because pkg-a depends on packaging>=24,<25 and pkg-b depends
      on packaging>=25,<26, we can conclude that pkg-a and pkg-b are
      incompatible.
      And because your workspace requires pkg-a and pkg-b, we can conclude
      that your workspace's requirements are unsatisfiable.
```

CI 在 PR 阶段执行 `uv sync --locked`（见 [`.github/workflows/run-builtin-tester.yml`](/.github/workflows/run-builtin-tester.yml)），该命令会重新求解并在解不出或 lockfile 过期时失败。因此第三方依赖互斥会在 PR 阶段直接暴露，而不必等到用户安装时；多仓库布局下不存在任何一处会做这样的联合求解，这是 monorepo 布局的主要收益。

该防线有两处边界：仅覆盖 workspace 内成员包之间的**第三方**依赖互斥，不覆盖**内部**版本约束漂移（例如某包声明 `akari-bot-core>=2.0,<3.0`，而 core 实际为 `0.1.0`，此时 `uv lock` 仍然通过，约束却会原样写进发布出的 wheel），后者由 `uv run python tools/lint_versions.py` 负责；也不覆盖第三方模块，它们不在 workspace 内，依赖互斥只能靠净室验证与 `akaribot module add` 的安装前预检拦截。

`uv lock` 失败时应调整 `pyproject.toml` 中的约束，使冲突双方的区间重新相容并说明原因。不得以 `--no-verify` 绕过检查、手工编辑 `uv.lock` 或放宽约束来通过检查，这些做法只会把冲突推迟到用户安装现场。

仓库已配置 pre-commit 钩子，安装方式：

```sh
pre-commit install
```

提交时自动执行格式化、静态分析与依赖导出。

### 分支命名

新功能与改动分支使用 `dev/` 前缀，缺陷修复分支使用 `fix/` 前缀。分支名必须使用英文，建议使用简短描述或
Issue 编号。

### 提交规范

提交信息使用英文或简体中文。遵循 Conventional Commits 规范更佳。

### PR 描述

PR 标题参考[提交规范](#提交规范)，正文按 PR 模板填写。描述中可用 `#<编号>` [关联
Issue](#提出建议)。

PR 须通过全部 CI 检查，并获得至少 1 名开发者的 LGTM 方可合并。重大更改须提交 PR 审查，不得直接
push 到 `master`。

### 代码风格

本项目使用 [Ruff](https://docs.astral.sh/ruff) 格式化与静态分析。提交前运行：

```sh
ruff format .
ruff check .
```

VS Code 用户可安装 Ruff 扩展。

### 新增模块包

仓库已按包拆分，官方模块各占一个 workspace 成员（`packages/modules/akari-bot-module-<名>/`）。
新增模块用脚手架生成后按需修改：

```sh
akaribot new module <名>          # 交互问卷；也可用 --non-interactive 配合逐项参数
akaribot module add -e .          # 在生成的包目录内执行；脚手架 --add 默认已代跑
```

脚手架产出 `<--dir>/akari-bot-module-<名>/`，与 `packages/modules/akari-bot-module-<名>/` 同构：
`pyproject.toml`、`manifest.toml`、`README.md`、`akaribot/modules/<名>/`（含 `config.py`、
`database/models.py`、`migrations/`、`locales/zh_cn.json`、`assets/`）与 `tests/test_<名>.py`。
`--add` 默认开启，生成后会在该目录内执行 `akaribot module add -e .`；若要手工执行，先进入包目录。

`manifest.toml` 放在导入包目录内，字段与 `akaribot/core/registry.py` 的 `PackageManifest` 一一对应，
未启用的能力整行省略：

| 字段 | 用途 |
| --- | --- |
| `schema` | 清单版本，当前为 `1` |
| `requires_core_api` | 兼容的 core 公共 API 区间，当前写 `">=1,<2"` |
| `locales` / `assets` / `migrations` / `config_migrations` | 各目录相对包根的路径，没有的能力省略 |
| `config_table` / `config_schema_version` | `config.py` 中 `on_module_config("<名>")` 登记的表名与配置版本 |
| `provides_modules` | 本包 `module()` 注册的全部模块名 |
| `owned_tables` | 本包拥有的数据库表，供 `akaribot module remove --purge-data` 使用 |

清单里**不写版本号与依赖清单**：两者的真源是 distribution metadata。生成后请核对几条硬性约定：

- 代码一律 `from akaribot.core.api import ...`，不要写 `akaribot.core.builtins.*` 这类深路径。
- `locales/zh_cn.json` **只提交 zh_cn**，其余语言交给 Weblate；键名前缀须与模块名一致。
- 对 core 的约束写 `akari-bot-core>=0.1.0,<1.0`：全部 first-party 包的这一串必须**字面一致**，
  `python tools/lint_versions.py` 会检查。
- 模块之间不要互相依赖：官方模块包之间**不得存在任何依赖**（`tools/lint_boundaries.py` 的 B10）。
- 若模块要建表，迁移文件放在 `migrations/`，并保证可重复执行（判断某条 revision 是否已应用只看
  `schema_migrations` 表）。
- 包内不要出现 `akaribot/__init__.py`：`akaribot` 是命名空间包（B7）。

提交前运行全部门禁：

```sh
uv run ruff check . && uv run ruff format --check .
uv run python tools/lint_comments.py      # 注释书面语与块长
uv run python tools/lint_boundaries.py    # 分层、命名空间、依赖声明
uv run python tools/lint_versions.py      # 内部版本约束一致性
```

## 文字排版

> “有研究显示，打字的时候不喜欢在中文和英文之间加空格的人，感情路都走得很辛苦，有七成的比例会在 34 岁的时候跟自己不爱的人结婚，而其余三成的人最后只能把遗产留给自己的猫。毕竟爱情跟书写都需要适时地留白。
>
> 与大家共勉之。”
>
> ——[vinta/paranoid-auto-spacing](https://github.com/vinta/pangu.js)

本项目的所有中文文字排版（包括本文）参考[中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines/blob/master/README.zh-Hans.md)。

规则包括：
- 中英文之间需要增加空格
- 使用全角中文标点
- 专有名词使用正确的大小写

以下情况例外：
- 简体中文使用弯引号
- 链接之间不额外增加空格

补充约定：
- 称呼用户须使用“你”，而不是“您”
- 机器人自称时避免使用“我”，统一使用“机器人”
- 尽可能避免使用第一人称描述
- 机器人的第三人称统一为“它”

---

# Contributing Guide

Thank you for your interest in AkariBot (and its derivative projects)!

We welcome contributions of all kinds. For detailed information on different ways to participate and the corresponding workflows, please refer to the [table of contents](#table-of-contents) below.

Before starting to contribute, please make sure to read the relevant sections. This will significantly reduce the burden on maintainers and lead to a smoother collaboration experience for everyone.

> [!NOTE]
> If you like this project but are not planning to contribute code at the moment, that's completely fine. You can still support us in the following ways:
> - Star this repository
> - Mention / link to this project in your own project's README
> - Add the bot to your group chat / server
> - Share or recommend the project / bot to others

## Table of Contents

- [Asking Questions](#asking-questions)
- [Making Contributions](#making-contributions)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Localization](#localization)
- [Submitting Code Changes](#submitting-code-changes)
  - [Quick Start](#quick-start)
  - [Development Environment](#development-environment)
  - [Branch Naming](#branch-naming)
  - [Commit Message Convention](#commit-message-convention)
  - [Pull Request Description](#pull-request-description)
  - [Code Style](#code-style)
  - [Adding a Module Package](#adding-a-module-package)
- [Text Typography (for Chinese)](#text-typography-for-chinese)

## Asking Questions

> [!NOTE]
> We strongly recommend reading [*How To Ask Questions The Smart Way*](http://www.catb.org/~esr/faqs/smart-questions.html) first — it helps avoid unnecessary back-and-forth.
>
> Notice: This guide is not a help desk for this project!

Before asking, please search whether a similar [issue](https://github.com/Teahouse-Studios/akari-bot/issues) already exists. For very obvious questions, we recommend trying a search engine first.

If you still need to reach the developers, you can use these channels:

- Create a new [issue](https://github.com/Teahouse-Studios/akari-bot/issues/new)
- Join the QQ group for [public instance testing (738829671)](https://qm.qq.com/q/Rmuo5ORYgq) or the [Teahouse Studios chat group (979982065)](https://qm.qq.com/q/sjwFNX1NVC)
- We are not online on Discord frequently, so there is no Discord server at present.

No matter which method you choose, please **describe your problem in as much detail as possible**.

## Making Contributions

### Reporting Bugs

> [!WARNING]
> **Never** report or reproduce security issues / vulnerabilities that involve sensitive information in Issues or any public channels.
>
> Such issues must be reported privately via email or direct message to the developers. See [`SECURITY.md`](/SECURITY.md).
>
> Content that violates this rule will be removed. Persistent violation may have consequences.

Before submitting a bug report, please check if a similar [issue](https://github.com/Teahouse-Studios/akari-bot/issues) already exists.

If not, create a new Issue using the [Bug Report template](https://github.com/Teahouse-Studios/akari-bot/issues/new?template=report_bug.yaml) and include:

- A short description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Error messages / logs (if any)

A good bug report should not require others to keep asking for more details. Please provide as much complete information as possible.

### Suggesting Features

Before suggesting a feature, please check if a similar [issue](https://github.com/Teahouse-Studios/akari-bot/issues) already exists.

If not, create a new issue using the [Feature Request template](https://github.com/Teahouse-Studios/akari-bot/issues/new?template=feature_request.yaml) and include:

- A short description of the suggestion
- Possible implementation ideas (optional but welcome)
- Why this would benefit the project (recommended)

Even if you have already implemented the feature, we still recommend opening an Issue for discussion first before submitting a pull request — it helps ensure alignment.

### Localization

Internationalization content for this project is hosted on Weblate. You can participate in translation and improvement [here](https://hosted.weblate.org/engage/akaribot).

To avoid unnecessary issues clutter, we prefer that translation-related discussions (except for Simplified Chinese) happen on Weblate rather than in issues.

If you do not have a Weblate account, feel free to contact the developers and we can submit the translations on your behalf.

## Submitting Code Changes

This section covers code contributions. The project does not impose many restrictions on code changes, but the
conventions below are required.

### Quick Start

1. Fork the repository
2. Clone your fork locally
3. Create a new branch
4. Make your changes
5. Open a pull request to this repository

Never commit directly to another repository's `master` / `main` branch.

### Development Environment

The project is based on Python. Make sure you meet the minimum Python version requirement (see [README](/README.md)).

Recommended IDEs: [PyCharm](https://www.jetbrains.com/pycharm) or [VS Code](https://code.visualstudio.com).

This project uses [uv](https://docs.astral.sh/uv) to manage dependencies. After installing uv, run:

```bash
uv sync
```

To add a new dependency:

```bash
uv add <package-name>
```

Please move the new dependency to the appropriate commented group in `pyproject.toml` and sort dependencies alphabetically.

Finally, remember to lock the dependencies:

```bash
uv lock
```

Pre-commit hooks are already configured. Install them with:

```bash
pre-commit install
```

They will automatically run formatting, linting, dependency export, etc. on commit.

### Branch Naming

Branches for new features or changes use the `dev/` prefix; bugfix branches use the `fix/` prefix.

Branch names must be in English. Short descriptive names or Issue numbers (e.g. `dev/add-xxx-command`, `fix/123`) are recommended.

### Commit Message Convention

Commit messages should be written in English or Simplified Chinese. No other strict requirements.

Following [Conventional Commits](https://www.conventionalcommits.org/) is appreciated but not mandatory.

### Pull Request Description

Pull request titles refer to the [commit message](#commit-message-convention). The body text according to the template.

It is recommended to [reference related issues](#suggesting-features) in the description by writing `#<number>`.

A pull request must pass all CI checks and receive at least 1 developer's LGTM (Looks Good To Me) before it can be merged.

Major changes should not be pushed directly to `master` — please open a pull request for review.

### Code Style

This project uses [Ruff](https://docs.astral.sh/ruff) for formatting and static analysis. Before submitting code, please run:

```bash
ruff format .
ruff check .
```

If you're using VS Code, installing the Ruff extension is recommended.

### Adding a Module Package

The repository is split into packages, and every official module is its own workspace member
(`packages/modules/akari-bot-module-<name>/`). Generate a new module with the scaffold, then adapt it:

```bash
akaribot new module <name>        # interactive questionnaire; --non-interactive plus per-item options for scripts
akaribot module add -e .          # run inside the generated package; the scaffold's --add already does this
```

The scaffold writes `<--dir>/akari-bot-module-<name>/`, mirroring `packages/modules/akari-bot-module-<name>/`:
`pyproject.toml`, `manifest.toml`, `README.md`, `akaribot/modules/<name>/` (with `config.py`,
`database/models.py`, `migrations/`, `locales/zh_cn.json`, `assets/`) and `tests/test_<name>.py`.

`manifest.toml` lives inside the import package. Its fields map one-to-one to `PackageManifest` in
`akaribot/core/registry.py`, and capabilities that are not used are omitted entirely:

| Field | Purpose |
| --- | --- |
| `schema` | Manifest version, currently `1` |
| `requires_core_api` | Compatible core public API range, currently `">=1,<2"` |
| `locales` / `assets` / `migrations` / `config_migrations` | Directory paths relative to the package root; omitted when absent |
| `config_table` / `config_schema_version` | Table registered by `on_module_config("<name>")` in `config.py`, and its config version |
| `provides_modules` | Every module name registered by `module()` in this package |
| `owned_tables` | Database tables owned by this package, used by `akaribot module remove --purge-data` |

The manifest deliberately carries **no version and no dependency list**: distribution metadata is the single
source of truth for both. After generating, check the hard requirements:

- Import from the facade only: `from akaribot.core.api import ...`, never deep paths such as `akaribot.core.builtins.*`.
- Only `locales/zh_cn.json` is committed; other languages come from Weblate. Locale keys are prefixed with the module name.
- Declare the core constraint as `akari-bot-core>=0.1.0,<1.0`. This string must be **byte-for-byte identical**
  across all first-party packages; `python tools/lint_versions.py` checks it.
- Official module packages must not depend on each other (`tools/lint_boundaries.py`, rule B10).
- Database migrations live in `migrations/` and must be repeatable; whether a revision has been applied is
  decided solely by the `schema_migrations` table.
- Never add `akaribot/__init__.py`: `akaribot` is a namespace package (rule B7).

Run all gates before committing:

```bash
uv run ruff check . && uv run ruff format --check .
uv run python tools/lint_comments.py      # comment style and block length
uv run python tools/lint_boundaries.py    # layering, namespaces, dependency declarations
uv run python tools/lint_versions.py      # internal version constraint consistency
```

## Text Typography (for Chinese)

> “Research shows that, people adding no space between Chinese and English suffer from pathetic relationships. 70% of them are married by the age of 34, with someone they don't love; 30% of them left everything for their cats and died. Blank spaces are essential to both romance and writing.”
>
> —— [vinta/paranoid-auto-spacing](https://github.com/vinta/pangu.js)

All Chinese text in this project (including this document) follows the guidelines from [*Chinese Copywriting Guidelines*](https://github.com/sparanoid/chinese-copywriting-guidelines/blob/master/README.en.md).

Includes (but is not limited to):

- Place one space before/after English words
- Use punctuation in fullwidth form
- Avoid jargons

Exceptions:

- Use curly quotation marks instead of  corner brackets for Chinese Simplified
- No extra spaces before/after links

Additional project-specific conventions:

- Address users with “你” (informal/casual “you”), not “您” (polite/formal)
- When the bot refers to itself, avoid “我” (I / me); use “机器人” (the Bot / this Bot) instead
- Avoid first-person descriptions whenever possible
- The bot's third-person pronoun is uniformly “它” (it / it)
