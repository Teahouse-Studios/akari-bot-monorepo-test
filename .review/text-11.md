# 全仓可读文本审核稿 · 第 11 册 / 共 20 册

覆盖 U007389–U007870，14 个文件、482 个单元、31,865 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

改动只写在 `<<< UNIT … >>>` 与 `<<< END … >>>` 之间。UNIT 行含编号与位置，回填按编号对位，这一行不要动。

## 分册索引

| 册 | 覆盖单元 | 单元数 | 文件数 | 字符数 |
| --- | --- | --- | --- | --- |
| [01](text-01.md) | U000001–U000392 | 392 | 17 | 35,782 |
| [02](text-02.md) | U000393–U000868 | 476 | 55 | 33,076 |
| [03](text-03.md) | U000869–U001494 | 626 | 102 | 33,069 |
| [04](text-04.md) | U001495–U001851 | 357 | 10 | 32,997 |
| [05](text-05.md) | U001852–U003218 | 1,367 | 20 | 32,840 |
| [06](text-06.md) | U003219–U004563 | 1,345 | 12 | 33,868 |
| [07](text-07.md) | U004564–U005769 | 1,206 | 49 | 33,058 |
| [08](text-08.md) | U005770–U006497 | 728 | 50 | 33,300 |
| [09](text-09.md) | U006498–U007035 | 538 | 45 | 31,936 |
| [10](text-10.md) | U007036–U007388 | 353 | 11 | 35,373 |
| [11](text-11.md) | U007389–U007870 | 482 | 14 | 31,865 |
| [12](text-12.md) | U007871–U008593 | 723 | 27 | 33,699 |
| [13](text-13.md) | U008594–U009156 | 563 | 68 | 33,600 |
| [14](text-14.md) | U009157–U010119 | 963 | 74 | 33,804 |
| [15](text-15.md) | U010120–U010865 | 746 | 122 | 33,410 |
| [16](text-16.md) | U010866–U011178 | 313 | 41 | 33,480 |
| [17](text-17.md) | U011179–U011214 | 36 | 7 | 37,679 |
| [18](text-18.md) | U011215–U012141 | 927 | 98 | 37,650 |
| [19](text-19.md) | U012142–U013013 | 872 | 116 | 37,801 |
| [20](text-20.md) | U013014–U013993 | 980 | 96 | 41,555 |

## 本册文件

| 文件 | 单元数 | 单元范围 | 字符数 |
| --- | --- | --- | --- |
| `packages/akari-bot-core/akaribot/core/docs/module-development.md` | 129 | U007389–U007517 | 9,593 |
| `packages/akari-bot-core/akaribot/core/docs/permissions.md` | 38 | U007518–U007555 | 2,877 |
| `packages/akari-bot-core/akaribot/core/docs/placeholders.md` | 29 | U007556–U007584 | 2,227 |
| `packages/akari-bot-core/akaribot/core/docs/public-api.md` | 135 | U007585–U007719 | 8,172 |
| `packages/akari-bot-core/akaribot/core/docs/queue.md` | 26 | U007720–U007745 | 2,193 |
| `packages/akari-bot-core/akaribot/core/docs/webrender.md` | 26 | U007746–U007771 | 2,355 |
| `packages/akari-bot-core/akaribot/core/entrypoints/config.py` | 16 | U007772–U007787 | 825 |
| `packages/akari-bot-core/akaribot/core/entrypoints/data.py` | 21 | U007788–U007808 | 947 |
| `packages/akari-bot-core/akaribot/core/entrypoints/db.py` | 9 | U007809–U007817 | 616 |
| `packages/akari-bot-core/akaribot/core/entrypoints/docs.py` | 15 | U007818–U007832 | 480 |
| `packages/akari-bot-core/akaribot/core/entrypoints/modules.py` | 17 | U007833–U007849 | 714 |
| `packages/akari-bot-core/akaribot/core/entrypoints/peers.py` | 5 | U007850–U007854 | 172 |
| `packages/akari-bot-core/akaribot/core/entrypoints/registry.py` | 3 | U007855–U007857 | 172 |
| `packages/akari-bot-core/akaribot/core/entrypoints/rpc.py` | 13 | U007858–U007870 | 522 |

## 单元类型

| 类型 | 含义 |
| --- | --- |
| `md-paragraph` | Markdown 正文段落 |
| `md-heading` | Markdown 标题 |
| `md-list` | Markdown 列表项 |
| `md-table` | Markdown 表格行 |
| `py-comment` | Python 整行注释 |
| `py-inline-comment` | Python 行尾注释 |
| `py-docstring` | Python docstring |
| `json-value` | 语言文件的字符串值 |
| `cfg-comment` | 配置文件的中文注释 |

## 正文
<<< UNIT U007389 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:1-1 | ctx=模块开发 >>>
# 模块开发
<<< END U007389 >>>
<<< UNIT U007390 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:3-3 | ctx=模块开发 >>>
本文从生成、安装到运行，说明第一个模块的完整流程。后面介绍模块的包结构、命令、Hook、配置和运行时资源。阅读前，你需要了解 Python 异步编程，并熟悉本仓库的包管理方式。
<<< END U007390 >>>
<<< UNIT U007391 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:5-5 | ctx=准备工作 >>>
## 准备工作
<<< END U007391 >>>
<<< UNIT U007392 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:7-7 | ctx=准备工作 >>>
先打开一个终端，进入实例目录，执行：
<<< END U007392 >>>
<<< UNIT U007393 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:13-13 | ctx=准备工作 >>>
左侧是页面列表，右侧是当前页面。用 ↑/↓ 选中“开发”，按 Enter 打开。页脚会列出当前页可用的按键。
<<< END U007393 >>>
<<< UNIT U007394 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:15-15 | ctx=准备工作 >>>
开发页列出当前实例与工作区的包。按 `n` 打开“新建包”对话框。
<<< END U007394 >>>
<<< UNIT U007395 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:19-19 | ctx=生成第一个模块 >>>
## 生成第一个模块
<<< END U007395 >>>
<<< UNIT U007396 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:21-21 | ctx=生成第一个模块 >>>
在“新建包”对话框中填写以下内容：
<<< END U007396 >>>
<<< UNIT U007397 | md-table | packages/akari-bot-core/akaribot/core/docs/module-development.md:23-30 | ctx=生成第一个模块 >>>
| 字段 | 本次填写 | 说明 |
| --- | --- | --- |
| 名称 | `greet` | 模块名，建议使用小写字母、数字和下划线，不能包含空格或斜杠 |
| 类型 | 模块 | 默认值。按钮可以在模块与适配器之间切换，本教程保持模块 |
| 目标目录 | `akari-modules` | 相对当前工作区根目录，未配置工作区时相对实例根目录。包会放在该目录下的 `akari-bot-module-greet/` |
| 生成配置 | 不勾选 | 先不生成配置模板 |
| 生成数据库 | 不勾选 | 先不生成数据库与迁移 |
| 生成测试 | 勾选 | 默认已勾选，保留一条集成测试 |
<<< END U007397 >>>
<<< UNIT U007398 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:32-32 | ctx=生成第一个模块 >>>
用 Tab 在名称、类型、目标目录和三个复选项之间移动。空格切换复选项状态。最后把焦点移到“生成包”，按 Enter。
<<< END U007398 >>>
<<< UNIT U007399 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:34-34 | ctx=生成第一个模块 >>>
按 Esc 或选择“关闭”会放弃本次填写。
<<< END U007399 >>>
<<< UNIT U007400 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:36-36 | ctx=生成第一个模块 >>>
生成过程中的输出会显示在输出区。完成后状态栏提示生成成功，按 `o` 查看完整输出。新包会出现在开发页的包列表中。
<<< END U007400 >>>
<<< UNIT U007401 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:38-38 | ctx=生成第一个模块 >>>
生成的目录结构如下。其中 `akari-modules` 是上一步填写的目标目录。
<<< END U007401 >>>
<<< UNIT U007402 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:51-51 | ctx=生成第一个模块 >>>
生成配置和生成数据库两项未勾选。需要时再添加对应的 `config.py` 与 `database/`。
<<< END U007402 >>>
<<< UNIT U007403 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:53-53 | ctx=生成的文件 >>>
### 生成的文件
<<< END U007403 >>>
<<< UNIT U007404 | md-table | packages/akari-bot-core/akaribot/core/docs/module-development.md:55-63 | ctx=生成的文件 >>>
| 文件 | 用途 |
| --- | --- |
| `pyproject.toml` | 包名、依赖与 `akaribot.modules` 入口 |
| `manifest.toml` | 包清单，声明语言目录与提供的模块名 |
| `akaribot/modules/greet/__init__.py` | 模块声明与命令实现 |
| `locales/zh_cn.json` | 帮助文本与回复文案 |
| `tests/test_greet.py` | 一条集成测试，核对命令回复 |
| `README.md` | 包的安装、命令与结构说明 |
| `.github/workflows/publish.yml` | 推送版本标签后上传到 PyPI 的工作流 |
<<< END U007404 >>>
<<< UNIT U007405 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:65-65 | ctx=先看生成的代码 >>>
### 先看生成的代码
<<< END U007405 >>>
<<< UNIT U007406 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:67-67 | ctx=先看生成的代码 >>>
打开 `akaribot/modules/greet/__init__.py`，会看到下面这段代码。
<<< END U007406 >>>
<<< UNIT U007407 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:90-90 | ctx=先看生成的代码 >>>
`@mod.command()` 未提供模板时，注册的是模块的默认命令。它的调用形式是 `~greet default`。
<<< END U007407 >>>
<<< UNIT U007408 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:92-92 | ctx=先看生成的代码 >>>
`module()` 的 `desc` 指向模块说明。处理函数调用 `msg.finish()`，把 `I18NContext` 对应的文案发送到当前会话。
<<< END U007408 >>>
<<< UNIT U007409 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:94-94 | ctx=先看生成的代码 >>>
文案在 `locales/zh_cn.json`：
<<< END U007409 >>>
<<< UNIT U007410 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:104-104 | ctx=先看生成的代码 >>>
`greet.help.desc` 是模块说明，`greet.help` 是默认命令的帮助文本。回复文案目前还是 `Hello World!`，下一节修改它。
<<< END U007410 >>>
<<< UNIT U007411 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:106-106 | ctx=修改第一条回复 >>>
## 修改第一条回复
<<< END U007411 >>>
<<< UNIT U007412 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:108-108 | ctx=修改第一条回复 >>>
打开 `locales/zh_cn.json`，把 `greet.message.hello` 改成：
<<< END U007412 >>>
<<< UNIT U007413 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:114-114 | ctx=修改第一条回复 >>>
如果生成时保留了测试，`tests/test_greet.py` 里的预期文案也要同步修改：
<<< END U007413 >>>
<<< UNIT U007414 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:128-128 | ctx=修改第一条回复 >>>
测试里的预期文案和实际文案不一致时，测试会失败。改完文案后，把 `zh_cn.json` 和测试里的预期文案一起检查。
<<< END U007414 >>>
<<< UNIT U007415 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:130-130 | ctx=安装并启用 >>>
## 安装并启用
<<< END U007415 >>>
<<< UNIT U007416 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:132-132 | ctx=安装并启用 >>>
生成的文件留在目标目录。切换到侧栏的“模块”页，先按 `c` 清除选择，再按 `i` 打开安装对话框。
<<< END U007416 >>>
<<< UNIT U007417 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:134-134 | ctx=安装并启用 >>>
在输入框里填入刚才生成的包目录，路径用输出区显示的完整路径。按“下一步”。终端界面（TUI）识别到目录后，安装方式里会出现“可编辑安装本地目录”。选中它，安装就开始。
<<< END U007417 >>>
<<< UNIT U007418 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:136-136 | ctx=安装并启用 >>>
可编辑安装直接使用这份源码。安装完成后，模块页会刷新列表，`greet` 出现在列表里。
<<< END U007418 >>>
<<< UNIT U007419 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:138-138 | ctx=安装并启用 >>>
如果实例正在运行，新模块会直接加载。实例未运行时，模块会在下次启动时加载。
<<< END U007419 >>>
<<< UNIT U007420 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:140-140 | ctx=安装并启用 >>>
安装只负责让实例能加载这个模块。普通模块还需要在场景内启用。场景管理员在会话中执行：
<<< END U007420 >>>
<<< UNIT U007421 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:146-146 | ctx=安装并启用 >>>
基础模块始终开启。`greet` 是普通模块，要先启用。修改代码后，重启实例，或者由超级用户在会话中执行：
<<< END U007421 >>>
<<< UNIT U007422 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:152-152 | ctx=对话示例 >>>
## 对话示例
<<< END U007422 >>>
<<< UNIT U007423 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:154-154 | ctx=对话示例 >>>
下面的对话假设模块已经安装，并且当前场景已启用 `greet`。
<<< END U007423 >>>
<<< UNIT U007424 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:157-163 | ctx=对话示例 >>>
  :log="[
    '用户：~module enable greet',
    '机器人：成功：开启模块“greet”。',
    '用户：~greet default',
    '机器人：你好，世界！',
  ]"
/>
<<< END U007424 >>>
<<< UNIT U007425 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:165-165 | ctx=对话示例 >>>
`~module enable greet` 只需要执行一次。之后的 `~greet default` 会命中 `@mod.command()` 注册的默认命令，返回你在 `zh_cn.json` 中编写的文案。
<<< END U007425 >>>
<<< UNIT U007426 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:167-167 | ctx=对话示例 >>>
如果机器人没有响应，先检查三件事：
<<< END U007426 >>>
<<< UNIT U007427 | md-list | packages/akari-bot-core/akaribot/core/docs/module-development.md:169-171 | ctx=对话示例 >>>
- 模块是否安装成功。回到“模块”页，看 `greet` 是否在列表里，状态是否为已安装。
- 当前场景是否启用模块。在会话中执行 `~module list`。
- 修改文案后是否重载。执行 `~module reload greet`，或重启实例。
<<< END U007427 >>>
<<< UNIT U007428 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:173-173 | ctx=继续开发 >>>
## 继续开发
<<< END U007428 >>>
<<< UNIT U007429 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:175-175 | ctx=继续开发 >>>
生成模板只提供最小可运行结构。别名、平台范围、权限、配置、数据库与 Hook 按需补充。
<<< END U007429 >>>
<<< UNIT U007430 | md-list | packages/akari-bot-core/akaribot/core/docs/module-development.md:177-181 | ctx=继续开发 >>>
- 修改 `module()` 的参数，可以声明别名、支持平台和模块级权限。参数见下文“声明模块”。
- 想给默认命令换一个名字，把 `@mod.command()` 改成 `@mod.command("hello {{I18N:greet.help.hello}}")`，并同步修改 `greet.help.hello` 与测试中的 `~greet hello`。
- 修改 `@mod.command()` 的模板，可以增加位置参数、标志选项和帮助文本。规则见下文“命令”。
- 需要定时执行或监听消息时，使用 `@mod.schedule()`、`@mod.hook()` 或 `@mod.event()`。
- 需要保存配置或数据时，在 `config.py` 和 `database/models.py` 中声明，并同步修改 `manifest.toml`。
<<< END U007430 >>>
<<< UNIT U007431 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:183-183 | ctx=包结构与清单 >>>
## 包结构与清单
<<< END U007431 >>>
<<< UNIT U007432 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:196-196 | ctx=包结构与清单 >>>
`pyproject.toml` 声明依赖和入口，`manifest.toml` 声明清单字段。
<<< END U007432 >>>
<<< UNIT U007433 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:212-212 | ctx=包结构与清单 >>>
示例只列出包名。实际的版本范围从包目录下的 `pyproject.toml` 的 `dependencies` 读取，文档不重复具体约束。
<<< END U007433 >>>
<<< UNIT U007434 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:214-214 | ctx=包结构与清单 >>>
清单字段如下：
<<< END U007434 >>>
<<< UNIT U007435 | md-table | packages/akari-bot-core/akaribot/core/docs/module-development.md:216-225 | ctx=包结构与清单 >>>
| 字段 | 说明 |
| --- | --- |
| `schema` | 清单结构版本，当前为 `1` |
| `requires_core_api` | 核心 API 兼容区间，默认 `>=1,<2` |
| `locales`、`assets` | 语言文件与资源目录，默认 `locales`，相对导入包目录解析 |
| `migrations`、`config_migrations` | 数据库迁移与配置迁移目录 |
| `config_table`、`config_schema_version` | 配置表名，新生成配置写入的结构版本，默认 `1` |
| `provides_modules` | 包提供的模块名 |
| `owned_tables` | 数据清理时归属本包的表 |
| `credential_fields` | 启动前用于多实例查重的登录信息字段 |
<<< END U007435 >>>
<<< UNIT U007436 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:227-227 | ctx=包结构与清单 >>>
未识别的键只会记录警告，不影响加载。
<<< END U007436 >>>
<<< UNIT U007437 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:229-229 | ctx=发现与加载 >>>
## 发现与加载
<<< END U007437 >>>
<<< UNIT U007438 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:231-231 | ctx=发现与加载 >>>
`PackageRegistry` 读取已安装包声明的模块入口，`load_order()` 按依赖关系确定加载顺序。模块只依赖 `akaribot.core.api` 的公开接口。包缺少模块声明时，框架才用目录扫描发现模块。
<<< END U007438 >>>
<<< UNIT U007439 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:233-233 | ctx=发现与加载 >>>
JobQueue 处理完现有任务、Scheduler 进入维护状态后，框架才执行安装、卸载和重载。框架会替换原有的注册项，新注册项在正在运行的任务退出后生效。
<<< END U007439 >>>
<<< UNIT U007440 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:235-235 | ctx=发现与加载 >>>
模块加载失败或不兼容时，失败原因写入 `.cache_loader`，启动提示会读取这个文件。`ModulesManager.reload_module()` 返回 `(状态, 重载次数)`。命令 `~module reload` 失败时会给出提示。
<<< END U007440 >>>
<<< UNIT U007441 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:237-237 | ctx=声明模块 >>>
## 声明模块
<<< END U007441 >>>
<<< UNIT U007442 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:245-245 | ctx=声明模块 >>>
`module()` 的参数如下：
<<< END U007442 >>>
<<< UNIT U007443 | md-table | packages/akari-bot-core/akaribot/core/docs/module-development.md:247-256 | ctx=声明模块 >>>
| 参数 | 说明 |
| --- | --- |
| `module_name` | 命令首词，同时作为模块标识 |
| `alias` | 别名，可传字符串、列表或 `{别名: 完整命令}` 映射 |
| `desc` / `doc` / `hidden` | 帮助简介、线上说明与隐藏开关 |
| `recommend_modules` / `base` / `load` | 推荐模块、强制开启与加载开关 |
| `rss` / `regex` / `event` | 声明所需平台能力，影响模块能否在该场景启用 |
| `required_admin` / `required_superuser` / `required_base_superuser` | 模块级权限 |
| `required_bot_permissions` | 开启前要求机器人具备的平台权限 |
| `suppress_invalid_prompt` / `available_for` / `exclude_from` | 提示开关与平台范围 |
<<< END U007443 >>>
<<< UNIT U007444 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:258-258 | ctx=命令 >>>
## 命令
<<< END U007444 >>>
<<< UNIT U007445 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:266-266 | ctx=命令 >>>
模板元素分四类：
<<< END U007445 >>>
<<< UNIT U007446 | md-list | packages/akari-bot-core/akaribot/core/docs/module-development.md:268-271 | ctx=命令 >>>
- `<name>` 是位置参数，对应同名函数参数。没有提供参数时，使用默认值或 `None`。
- `[flag]` 是标志选项。标注为 `bool` 的函数参数会直接得到布尔值。
- `[-b]`、`[--foo <bar>]` 是以连字符开头的选项。选项名中的下划线按连字符匹配。选项只有一个子参数时，直接把子参数的值传给同名函数参数。`[-p <page>]` 也可以直接使用子参数名 `page`。无法作为参数名的元素用 `Param` 标注。
- 模板末尾用双层花括号包裹的 `I18N:key` 是帮助文案，不参与解析。
<<< END U007446 >>>
<<< UNIT U007447 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:273-273 | ctx=命令 >>>
`int`、`float`、`bool` 参数按类型标注转换。一个命令可以注册多个模板，命中任意一个即可。`priority` 越大，越先匹配。
<<< END U007447 >>>
<<< UNIT U007448 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:275-275 | ctx=命令 >>>
解析结果写入 `parsed_msg`。位置参数以模板中的参数名为键。
<<< END U007448 >>>
<<< UNIT U007449 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:277-277 | ctx=命令 >>>
以连字符开头的选项会以选项名作为键。`-l` 和 `--l` 按同一个选项处理，选项名中的下划线会映射为连字符。
<<< END U007449 >>>
<<< UNIT U007450 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:279-279 | ctx=命令 >>>
函数中标注为 `Bot.MessageSession` 的参数由框架注入，其余参数按名称从 `parsed_msg` 读取。转换失败时抛出 `InvalidCommandFormatError`。
<<< END U007450 >>>
<<< UNIT U007451 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:281-281 | ctx=等待用户交互 >>>
## 等待用户交互
<<< END U007451 >>>
<<< UNIT U007452 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:283-283 | ctx=等待用户交互 >>>
命令执行到一半需要用户回答时，用 `MessageSession` 的等待方法。这些方法会暂停当前命令，收到消息后再继续。
<<< END U007452 >>>
<<< UNIT U007453 | md-table | packages/akari-bot-core/akaribot/core/docs/module-development.md:285-290 | ctx=等待用户交互 >>>
| 方法 | 适合的场景 | 返回 |
| --- | --- | --- |
| `wait_confirm()` | 只需要用户回答是或否 | `bool` |
| `wait_next_message()` | 收集同一用户的下一条消息 | `MessageSession` |
| `wait_reply()` | 要求用户引用某条提示再回复 | `MessageSession` |
| `wait_anyone()` | 让场景内任意成员回答 | `MessageSession` |
<<< END U007453 >>>
<<< UNIT U007454 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:292-292 | ctx=等待用户交互 >>>
这些方法默认等待 120 秒。等待期间默认释放执行锁，返回前重新获取。超时、用户取消或重新获取失败都会抛出 `WaitCancelException`。
<<< END U007454 >>>
<<< UNIT U007455 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:294-294 | ctx=等待用户交互 >>>
下面的例子在 `greet` 模块上继续添加命令。文案键要写入 `locales/zh_cn.json`。
<<< END U007455 >>>
<<< UNIT U007456 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:300-300 | ctx=等待确认 >>>
### 等待确认
<<< END U007456 >>>
<<< UNIT U007457 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:319-319 | ctx=等待确认 >>>
`wait_confirm()` 默认引用原消息，并在收到回答后删除机器人发出的提示。它只把确认词当作回答，用户发送其他内容时会继续等待。
<<< END U007457 >>>
<<< UNIT U007458 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:321-321 | ctx=等待确认 >>>
删除数据、解绑账号这类不可逆操作，可以传 `confirm_token`，要求用户完整输入口令。
<<< END U007458 >>>
<<< UNIT U007459 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:323-323 | ctx=收集下一条消息 >>>
### 收集下一条消息
<<< END U007459 >>>
<<< UNIT U007460 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:344-344 | ctx=收集下一条消息 >>>
`wait_next_message()` 等待下一条消息。这条消息必须来自触发命令的用户。这条消息仍会进入常规解析流程。如果用户发的是一条命令，那条命令也可能被执行。`delete=True` 会在等待结束后删除机器人发出的提示。
<<< END U007460 >>>
<<< UNIT U007461 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:346-346 | ctx=等待引用回复 >>>
### 等待引用回复
<<< END U007461 >>>
<<< UNIT U007462 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:363-363 | ctx=等待引用回复 >>>
`wait_reply()` 等待用户引用机器人发出的那条提示再回复。用户需要引用这条提示。平台不支持引用时，它会改为等待下一条消息。传 `all_=True` 时改为等待场景内任意成员。
<<< END U007462 >>>
<<< UNIT U007463 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:365-365 | ctx=等待任何人回答 >>>
### 等待任何人回答
<<< END U007463 >>>
<<< UNIT U007464 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:382-382 | ctx=等待任何人回答 >>>
`wait_anyone()` 等待场景内第一个回答的成员。成员可以直接回答，也可以引用提示。适合抢答、投票和多人协作。它的提示需要在 `greet.message.quiz.prompt` 里写清楚怎么回答。
<<< END U007464 >>>
<<< UNIT U007465 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:384-384 | ctx=等待任何人回答 >>>
只需要暂停几秒时，用 `await msg.sleep(3)`。它和等待方法一样，会在暂停期间释放执行锁。
<<< END U007465 >>>
<<< UNIT U007466 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:388-388 | ctx=等待任何人回答 >>>
`WaitCancelException` 和 `SessionFinished` 继承 `BaseException`，`except Exception` 捕获不到。等待超时、用户取消、会话结束要分别处理。
<<< END U007466 >>>
<<< UNIT U007467 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:392-392 | ctx=正则匹配 >>>
## 正则匹配
<<< END U007467 >>>
<<< UNIT U007468 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:394-394 | ctx=正则匹配 >>>
命令必须先输入命令前缀才能触发。只要消息里出现符合正则的文本，对应的处理函数就会执行。正则适合识别链接、编号和固定格式的句子。
<<< END U007468 >>>
<<< UNIT U007469 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:396-396 | ctx=正则匹配 >>>
下面用 bilibili 模块识别 av 号。`bili` 是它的模块实例，换成自己的模块变量即可：
<<< END U007469 >>>
<<< UNIT U007470 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:416-416 | ctx=正则匹配 >>>
`mode="A"` 使用 `findall` 找出消息里的全部匹配。匹配结果会去重。`msg.matched_msg` 是匹配文本组成的元组。示例只保留前 5 个，避免一条消息触发太多次回复。这里的回复文本只是演示，实际模块应换成查询到的视频信息。
<<< END U007470 >>>
<<< UNIT U007471 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:418-418 | ctx=正则匹配 >>>
`mode="M"` 使用 `re.match`，只从文本开头匹配。命中后 `msg.matched_msg` 是正则的 Match 对象，可以用 `group()` 获取分组：
<<< END U007471 >>>
<<< UNIT U007472 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:429-429 | ctx=正则匹配 >>>
常用选项：
<<< END U007472 >>>
<<< UNIT U007473 | md-list | packages/akari-bot-core/akaribot/core/docs/module-development.md:431-436 | ctx=正则匹配 >>>
- `flags` 传 `re.I` 等正则选项。
- `desc` 是帮助里的说明。
- `logging=False` 不记录每次命中，`show_typing=False` 不显示正在输入。
- `trigger_once_startup=True` 让每个场景只在启动后命中一次，适合发送迁移提示或一次性公告。
- `skip_long_message_confirm=True` 跳过超长消息确认。只在对匹配结果有把握时使用。
- `element_filter=(PlainElement,)` 只匹配纯文本，避免把图片说明或提及当成正文。
<<< END U007473 >>>
<<< UNIT U007474 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:438-438 | ctx=正则匹配 >>>
正则处理函数会在每条消息上运行，应保持轻量。网络请求和大量遍历放到后台任务里。
<<< END U007474 >>>
<<< UNIT U007475 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:440-440 | ctx=定时任务 >>>
## 定时任务
<<< END U007475 >>>
<<< UNIT U007476 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:442-442 | ctx=定时任务 >>>
`@greet.schedule()` 注册后台任务。任务函数不接收 `msg`，也没有会话上下文。需要主动发送消息时，用 `Bot.post_message()`。
<<< END U007476 >>>
<<< UNIT U007477 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:444-444 | ctx=定时任务 >>>
每天凌晨 4 点清理模块缓存：
<<< END U007477 >>>
<<< UNIT U007478 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:455-455 | ctx=定时任务 >>>
`CronTrigger.from_crontab()` 接收五段 crontab 表达式，依次是分钟、小时、日期、月份、星期。它按实例时区计算下一次执行时间。
<<< END U007478 >>>
<<< UNIT U007479 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:457-457 | ctx=定时任务 >>>
每 30 分钟检查一次更新：
<<< END U007479 >>>
<<< UNIT U007480 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:467-467 | ctx=定时任务 >>>
`IntervalTrigger` 的间隔会按 `schedule_interval_multiplier` 调整。测试或调试时可以用这个配置把周期缩短。
<<< END U007480 >>>
<<< UNIT U007481 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:469-469 | ctx=定时任务 >>>
定时任务也可以主动推送消息。下面这个任务每周一早上 9 点向启用了 `greet` 的场景推送提醒：
<<< END U007481 >>>
<<< UNIT U007482 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:477-477 | ctx=定时任务 >>>
`Bot.post_message()` 只发送到启用了 `greet` 的场景。
<<< END U007482 >>>
<<< UNIT U007483 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:479-479 | ctx=定时任务 >>>
定时任务还接受 `DateTrigger`，也可以用 `AndTrigger`、`OrTrigger` 组合多个触发器。同一个函数可以叠加多个 `@schedule`，每个装饰器注册一个任务。
<<< END U007483 >>>
<<< UNIT U007484 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:481-481 | ctx=定时任务 >>>
模块未加载时，它的命令、正则和定时任务都不会执行。场景没有启用某个非基础模块时，该模块的命令和正则会在 `parser_policies` 的模块匹配阶段被拦截。
<<< END U007484 >>>
<<< UNIT U007485 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:483-483 | ctx=Hook 与事件 >>>
## Hook 与事件
<<< END U007485 >>>
<<< UNIT U007486 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:485-485 | ctx=Hook 与事件 >>>
Hook 挂载在消息处理链的固定位置，用来观察或改变处理结果。它不替代命令，适合做统计、拦截、错误提示和平台事件响应。
<<< END U007486 >>>
<<< UNIT U007487 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:487-487 | ctx=命令执行后统计 >>>
### 命令执行后统计
<<< END U007487 >>>
<<< UNIT U007488 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:499-499 | ctx=命令执行后统计 >>>
在 `EXECUTION_FINISHED` 阶段，Hook 的返回值会被忽略。`priority` 越小越先执行，默认 100。`timeout` 默认 5 秒，`<=0` 表示不限时。
<<< END U007488 >>>
<<< UNIT U007489 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:501-501 | ctx=命令执行后统计 >>>
`server_scope=True` 的 Hook 不受场景内模块开关限制，但全局停用状态与平台范围仍会拦截它。
<<< END U007489 >>>
<<< UNIT U007490 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:503-503 | ctx=拦截出站消息 >>>
### 拦截出站消息
<<< END U007490 >>>
<<< UNIT U007491 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:512-512 | ctx=拦截出站消息 >>>
`OUTGOING_BEFORE_SEND` 在平台发送前执行。返回 `ctx.Stop()` 可以取消这次发送，也可以修改 `ctx.outgoing.chain` 改写内容。它同时作用于命令回复和 `Bot.post_message()` 的主动推送，适合在机器人被禁止发言的场景里拦截出站消息。
<<< END U007491 >>>
<<< UNIT U007492 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:514-514 | ctx=处理执行错误 >>>
### 处理执行错误
<<< END U007492 >>>
<<< UNIT U007493 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:529-529 | ctx=处理执行错误 >>>
`EXECUTION_ERROR` 的 `ctx.data` 里有 `error`、`module_type`，部分错误还有 `error_kind`。返回 `ctx.Handled()` 表示已经处理，框架不再记录未处理错误。只处理你认识的异常，其余交给默认处理。
<<< END U007493 >>>
<<< UNIT U007494 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:531-531 | ctx=响应平台事件 >>>
### 响应平台事件
<<< END U007494 >>>
<<< UNIT U007495 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:541-541 | ctx=响应平台事件 >>>
`@greet.event("事件名")` 订阅适配器上报的事件，不经过命令解析，也没有 `msg`。`available_for` 限定平台与场景类型。例如 QQBot 群聊会上报 `member_joined` 和 `member_left`。
<<< END U007495 >>>
<<< UNIT U007496 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:543-543 | ctx=响应平台事件 >>>
事件字段由适配器提供，常用 `target_id`、`sender_id` 和 `data`。需要发送欢迎语时，先把事件目标转成会话，再调用发送方法。
<<< END U007496 >>>
<<< UNIT U007497 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:545-545 | ctx=响应平台事件 >>>
`HookPoint` 有以下阶段：
<<< END U007497 >>>
<<< UNIT U007498 | md-list | packages/akari-bot-core/akaribot/core/docs/module-development.md:547-551 | ctx=响应平台事件 >>>
- 会话与消息：`SESSION_READY`、`SESSION_BEFORE_WAIT`、`MESSAGE_NORMALIZED`。
- 命令处理：`COMMAND_PREPARE`、`COMMAND_BEFORE_PARSE`、`COMMAND_BEFORE_EXECUTE`、`COMMAND_ROUTE`、`COMMAND_UNMATCHED`。
- 正则匹配：`REGEX_ROUTE`、`REGEX_CANDIDATE`、`CHANNEL_CLAIM`、`REGEX_PREPARE`、`REGEX_BEFORE_EXECUTE`。
- 执行：`EXECUTION_FINISHED`、`EXECUTION_ERROR`、`FINISHED`。
- 出站：`OUTGOING_BEFORE_SEND`、`OUTGOING_SENT`、`OUTGOING_FAILED`。
<<< END U007498 >>>
<<< UNIT U007499 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:553-553 | ctx=响应平台事件 >>>
在路由或候选阶段，Hook 返回 `Stop` 会终止后续处理。
<<< END U007499 >>>
<<< UNIT U007500 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:555-555 | ctx=响应平台事件 >>>
带名称的 Hook 按 `模块名.钩子名` 注册。`Bot.Hook.trigger("模块.钩子")` 只调用这个模块的回调。名称中没有点时，调用会广播给同名 Hook。某个回调失败时，框架记录错误后继续执行其他回调。
<<< END U007500 >>>
<<< UNIT U007501 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:557-557 | ctx=权限 >>>
## 权限
<<< END U007501 >>>
<<< UNIT U007502 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:559-559 | ctx=权限 >>>
模块级 `required_*` 对所有命令生效。命令上配置的权限只能比模块级更严格。
<<< END U007502 >>>
<<< UNIT U007503 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:561-561 | ctx=权限 >>>
运行时可以调用 `await msg.check_permission()` 判断当前用户是否为场景管理员，调用 `msg.check_super_user()` 判断是否为超级用户。
<<< END U007503 >>>
<<< UNIT U007504 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:563-563 | ctx=权限 >>>
基础模块始终开启，普通模块要先在场景内执行 `~module enable` 才能使用。`~auth` 可以给单个用户授予模块级超级用户权限。
<<< END U007504 >>>
<<< UNIT U007505 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:565-565 | ctx=配置、数据库与本地化 >>>
## 配置、数据库与本地化
<<< END U007505 >>>
<<< UNIT U007506 | md-list | packages/akari-bot-core/akaribot/core/docs/module-development.md:567-569 | ctx=配置、数据库与本地化 >>>
- 配置在 `config.py` 中用 `@on_module_config("<模块>")` 声明，表名为 `module_<模块>`。配置注释保存在 `config.comments.module_<模块>.<字段名>` 下。详见[配置](config.md)。
- 模型放在 `database/models.py`，继承 `DBModel`，表名在 `Meta.table` 声明。新增表要写入 `owned_tables`。结构变更用 `migrations/` 下的脚本完成。详见[数据库](database.md)。
- 文案一律用 `I18NContext("key", **参数)`，并且只在包内 `locales/zh_cn.json` 中创建对应条目。详见[本地化](i18n.md)。
<<< END U007506 >>>
<<< UNIT U007507 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:571-571 | ctx=常用工具 >>>
## 常用工具
<<< END U007507 >>>
<<< UNIT U007508 | md-list | packages/akari-bot-core/akaribot/core/docs/module-development.md:573-575 | ctx=常用工具 >>>
- `CoolDown(key, msg, delay, whole_target=False)`：按用户或整个场景记录冷却时间，`check()` 返回剩余秒数。
- `gained_petal()`、`lost_petal()`、`cost_petal()`、`sign_get_petal()`、`reset_petals_if_due()`：读写花瓣余额，并在消息中提示。
- `PlayState(game, msg)`：按会话保存小游戏状态。默认在 3600 秒（`GAME_EXPIRED`）后过期。`running()` 作为上下文管理器标记进行中状态。
<<< END U007508 >>>
<<< UNIT U007509 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:577-577 | ctx=运行期资源 >>>
## 运行时资源
<<< END U007509 >>>
<<< UNIT U007510 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:579-579 | ctx=运行期资源 >>>
`Bind.Module` 提供由框架管理的资源接口：
<<< END U007510 >>>
<<< UNIT U007511 | md-list | packages/akari-bot-core/akaribot/core/docs/module-development.md:581-586 | ctx=运行期资源 >>>
- `state()` 跨重载保留进程内状态。
- `cache()` 在版本变化时失效。
- `resource()` 首次使用时加载，并在关闭时释放。
- `cache_path()` 返回框架管理的缓存目录。
- `cleanup()` 注册退出清理。
- `spawn()` 创建由框架跟踪的后台任务。
<<< END U007511 >>>
<<< UNIT U007512 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:588-588 | ctx=运行期资源 >>>
重载会替换原有注册项，并等待正在运行的任务退出。
<<< END U007512 >>>
<<< UNIT U007513 | md-heading | packages/akari-bot-core/akaribot/core/docs/module-development.md:590-590 | ctx=会话接口 >>>
## 会话接口
<<< END U007513 >>>
<<< UNIT U007514 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:592-592 | ctx=会话接口 >>>
`send_message()` 发送消息，返回 `FinishedSession`。`finish()` 发送消息后结束当前处理，并抛出 `SessionFinished`。
<<< END U007514 >>>
<<< UNIT U007515 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:594-594 | ctx=会话接口 >>>
`wait_confirm()`、`wait_next_message()`、`wait_reply()`、`wait_anyone()` 的用法见上文“等待用户交互”。`sleep()` 在暂停期间释放执行锁。
<<< END U007515 >>>
<<< UNIT U007516 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:596-596 | ctx=会话接口 >>>
`delete()` 删除触发消息。`hold()`、`release()` 保持和释放平台上下文。
<<< END U007516 >>>
<<< UNIT U007517 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/module-development.md:598-598 | ctx=会话接口 >>>
同一个用户已有命令正在执行时，新命令会被拒绝。机器人回复“当前有命令正在执行，请稍后再试。”
<<< END U007517 >>>
<<< UNIT U007518 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:1-1 | ctx=权限 >>>
# 权限
<<< END U007518 >>>
<<< UNIT U007519 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:3-3 | ctx=权限 >>>
本文介绍 AkariBot 的权限分层与检查方式。
<<< END U007519 >>>
<<< UNIT U007520 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:5-5 | ctx=权限 >>>
权限分为普通用户、场景管理员、超级用户与基础超级用户四层。模块和命令通过装饰器声明所需层级，parser 在匹配模块和执行命令前检查。`~auth` 可以把单个模块的超级用户权限授予某个用户。
<<< END U007520 >>>
<<< UNIT U007521 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:7-7 | ctx=角色 >>>
## 角色
<<< END U007521 >>>
<<< UNIT U007522 | md-table | packages/akari-bot-core/akaribot/core/docs/permissions.md:9-14 | ctx=角色 >>>
| 角色 | 获得方式 | 判定接口 |
| --- | --- | --- |
| 普通用户 | 默认角色，无需授予 | 无 |
| 场景管理员 | 平台原生管理员、场景自定义管理员，或超级用户 | `msg.check_permission()` |
| 超级用户 | 数据库中的 `SenderUnionInfo.superuser` 标志 | `msg.check_super_user()` |
| 基础超级用户 | `config.toml` 的 `[config].base_superuser` 名单 | `sender_id` 与名单精确匹配 |
<<< END U007522 >>>
<<< UNIT U007523 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:16-16 | ctx=角色 >>>
`check_permission()` 依次判断场景自定义管理员与超级用户，最后调用平台的 `check_native_permission()`。
<<< END U007523 >>>
<<< UNIT U007524 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:18-18 | ctx=场景管理员 >>>
### 场景管理员
<<< END U007524 >>>
<<< UNIT U007525 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:20-20 | ctx=场景管理员 >>>
场景自定义管理员存放在 `TargetUnionInfo.custom_admins`，记录的是 union ID。因此同一用户绑定的多个平台账号共享权限。管理命令由 `admin` 模块提供：
<<< END U007525 >>>
<<< UNIT U007526 | md-table | packages/akari-bot-core/akaribot/core/docs/permissions.md:22-26 | ctx=场景管理员 >>>
| 命令 | 说明 |
| --- | --- |
| `~admin add <user>` | 添加场景管理员。目标须与发送者同平台，已是平台原生管理员时拒绝 |
| `~admin remove <user>` | 移除场景管理员。移除自己时要求确认 |
| `~admin list` | 列出场景自定义管理员 |
<<< END U007526 >>>
<<< UNIT U007527 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:28-28 | ctx=场景管理员 >>>
`admin` 模块整体声明 `required_admin=True`。自定义名单只记录非原生管理员。`add` 与 `remove` 只处理这类管理员，目标已是平台原生管理员时返回提示。
<<< END U007527 >>>
<<< UNIT U007528 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:30-30 | ctx=超级用户 >>>
### 超级用户
<<< END U007528 >>>
<<< UNIT U007529 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:32-32 | ctx=超级用户 >>>
超级用户控制机器人本身的行为，权限高于场景管理员。授予与撤销命令由 `superuser` 模块（别名 `su`）提供：
<<< END U007529 >>>
<<< UNIT U007530 | md-table | packages/akari-bot-core/akaribot/core/docs/permissions.md:34-37 | ctx=超级用户 >>>
| 命令 | 说明 |
| --- | --- |
| `~superuser add <user>` | 将用户写入数据库，并标记为 `superuser` |
| `~superuser remove <user>` | 清除标志。移除自己时要求确认 |
<<< END U007530 >>>
<<< UNIT U007531 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:39-39 | ctx=超级用户 >>>
`<user>` 必须是形如 `QQ|123456` 的完整用户 ID。用户尚未建立记录时，机器人先要求确认，再初始化 union。
<<< END U007531 >>>
<<< UNIT U007532 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:43-43 | ctx=超级用户 >>>
超级用户可以执行 `~config`、`~eval`、`~restart`、`~module unload` 等高危命令，也能通过 `~auth` 转授模块权限。此权限只应授予能够合法访问机器人后端与配置的人。
<<< END U007532 >>>
<<< UNIT U007533 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:47-47 | ctx=基础超级用户 >>>
### 基础超级用户
<<< END U007533 >>>
<<< UNIT U007534 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:49-49 | ctx=基础超级用户 >>>
`base_superuser` 是 `[config]` 表下的用户 ID 列表，也可以写单个字符串。在 pre-init 阶段，名单中的用户会被解析为 union 写入数据库，同时标记为超级用户。`required_base_superuser` 直接比较 `session_info.sender_id` 与配置名单，这份名单只能通过配置文件维护。
<<< END U007534 >>>
<<< UNIT U007535 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:51-51 | ctx=模块级权限 >>>
## 模块级权限
<<< END U007535 >>>
<<< UNIT U007536 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:53-53 | ctx=模块级权限 >>>
`module()` 接受以下三个布尔参数，对模块内的全部命令生效：
<<< END U007536 >>>
<<< UNIT U007537 | md-table | packages/akari-bot-core/akaribot/core/docs/permissions.md:60-64 | ctx=模块级权限 >>>
| 参数 | 默认 | 作用 |
| --- | --- | --- |
| `required_admin` | `False` | 要求场景管理员。拒绝时提示该场景的管理员 |
| `required_superuser` | `False` | 要求超级用户，或持有该模块 `~auth` 授权的用户 |
| `required_base_superuser` | `False` | 要求发送者在 `base_superuser` 名单中 |
<<< END U007537 >>>
<<< UNIT U007538 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:66-66 | ctx=模块级权限 >>>
框架按 `required_base_superuser`、`required_superuser`、`required_admin` 的顺序检查，任一项不通过就拒绝。命令级权限只能比模块级更严格。非基础模块还需要在场景内启用，声明了 `required_superuser` 的模块只有超级用户能启用。
<<< END U007538 >>>
<<< UNIT U007539 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:68-68 | ctx=命令级权限 >>>
## 命令级权限
<<< END U007539 >>>
<<< UNIT U007540 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:70-70 | ctx=命令级权限 >>>
`@module.command()`、`@module.regex()` 接受同名的三个参数，用于给单个命令或正则追加更严格的要求：
<<< END U007540 >>>
<<< UNIT U007541 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:77-77 | ctx=命令级权限 >>>
框架先解析命令模板，再执行命令级检查，最后调用处理函数。单个命令可以提高权限要求，不能放宽模块级的限制。
<<< END U007541 >>>
<<< UNIT U007542 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:79-79 | ctx=命令级权限 >>>
例如模块已经声明 `required_superuser`，某个命令再声明 `required_admin`，最终仍按模块级要求判断。`~auth` 的授权作用于整个模块，模块内的命令共用同一条授权记录。
<<< END U007542 >>>
<<< UNIT U007543 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:81-81 | ctx=模块授权 >>>
## 模块授权
<<< END U007543 >>>
<<< UNIT U007544 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:83-83 | ctx=模块授权 >>>
`auth` 模块让超级用户把单个模块的超级用户权限授予普通用户：
<<< END U007544 >>>
<<< UNIT U007545 | md-table | packages/akari-bot-core/akaribot/core/docs/permissions.md:85-89 | ctx=模块授权 >>>
| 命令 | 说明 |
| --- | --- |
| `~auth add <user> <module>` | 授权。要求确认口令，同一授权者重复授权会提示已存在 |
| `~auth remove <user> <module>` | 撤销当前发送者给出的授权 |
| `~auth list <user>` | 列出该用户持有的模块授权 |
<<< END U007545 >>>
<<< UNIT U007546 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:91-91 | ctx=模块授权 >>>
授权记录保存在 `SenderUnionInfo.sender_data["module_auth"]` 中，每项包含模块名与授权者 ID。授权只对声明了 `required_superuser` 的模块有效，`auth add` 会拒绝其他模块。授权时可以用模块别名代替模块名。
<<< END U007546 >>>
<<< UNIT U007547 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:93-93 | ctx=模块授权 >>>
授权者不再是超级用户时，其给出的授权自动失效。
<<< END U007547 >>>
<<< UNIT U007548 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:95-95 | ctx=机器人权限 >>>
## 机器人权限
<<< END U007548 >>>
<<< UNIT U007549 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:97-97 | ctx=机器人权限 >>>
`required_bot_permissions` 检查机器人在场景中必须具备的平台权限。检查在 `~module enable` 时进行：
<<< END U007549 >>>
<<< UNIT U007550 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:103-103 | ctx=机器人权限 >>>
字段名对应 `BotState` 的属性名：
<<< END U007550 >>>
<<< UNIT U007551 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:113-113 | ctx=机器人权限 >>>
平台自定义权限写成 `permissions.<名称>`。
<<< END U007551 >>>
<<< UNIT U007552 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:115-115 | ctx=机器人权限 >>>
`event` 与 `regex` 模块会自动加入 `can_read_all_messages`。`rss` 模块会自动加入 `can_send_proactive_messages`。
<<< END U007552 >>>
<<< UNIT U007553 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:117-117 | ctx=机器人权限 >>>
检查只把平台明确返回的 `False` 视为缺少对应权限。`None` 与状态查询失败按未知处理，继续启用。`~module enable all` 会跳过缺少机器人权限的模块。
<<< END U007553 >>>
<<< UNIT U007554 | md-heading | packages/akari-bot-core/akaribot/core/docs/permissions.md:119-119 | ctx=相关文档 >>>
## 相关文档
<<< END U007554 >>>
<<< UNIT U007555 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/permissions.md:121-121 | ctx=相关文档 >>>
模块声明与命令模板见[模块开发](module-development.md)。平台权限查询与能力声明见 [适配器开发](adapter-development.md)。内置管理模块见[内置模块](../../modules/core/docs/index.md)。
<<< END U007555 >>>
<<< UNIT U007556 | md-heading | packages/akari-bot-core/akaribot/core/docs/placeholders.md:1-1 | ctx=占位符 >>>
# 占位符
<<< END U007556 >>>
<<< UNIT U007557 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:3-3 | ctx=占位符 >>>
本文列出消息文本中的三种占位符，以及它们的转义规则。
<<< END U007557 >>>
<<< UNIT U007558 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:5-5 | ctx=占位符 >>>
`[KE:...]`、`{I18N:...}` 与 `<AT:...>` 分别在构造消息链、本地化与平台发送阶段解析。模块应优先用消息元素类构造内容。只有在文本里需要触发元素，或者内容要跨进程传递时，才使用占位符。
<<< END U007558 >>>
<<< UNIT U007559 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:9-9 | ctx=占位符 >>>
纯文本先由 `Locale.t_str()` 替换 I18N 标记，再由 `match_kecode()` 解析 KE 码。AT 码不参与这两步，由平台适配器在发送时渲染。KE 与 I18N 可以互相嵌套，参数值中的结构字符须按本页的转义规则处理。
<<< END U007559 >>>
<<< UNIT U007560 | md-heading | packages/akari-bot-core/akaribot/core/docs/placeholders.md:13-13 | ctx=KE 码 >>>
## KE 码
<<< END U007560 >>>
<<< UNIT U007561 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:15-15 | ctx=KE 码 >>>
KE 码用于在文本中插入图片、语音与按钮等消息元素。语法为：
<<< END U007561 >>>
<<< UNIT U007562 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:21-21 | ctx=KE 码 >>>
元素类型不区分大小写，参数之间用逗号分隔。
<<< END U007562 >>>
<<< UNIT U007563 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:23-23 | ctx=KE 码 >>>
`plain`、`markdown`、`url`、`action_text` 与按钮的文本参数会做 URL 解码。所有参数值在解析前都会做 HTML 实体反转义。
<<< END U007563 >>>
<<< UNIT U007564 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:25-25 | ctx=KE 码 >>>
KE 元素会作为独立的消息元素插入，通常与相邻文本分行。
<<< END U007564 >>>
<<< UNIT U007565 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:27-27 | ctx=KE 码 >>>
需要行内提及时应使用 AT 码。
<<< END U007565 >>>
<<< UNIT U007566 | md-table | packages/akari-bot-core/akaribot/core/docs/placeholders.md:29-41 | ctx=KE 码 >>>
| 类型 | 参数 |
| --- | --- |
| `plain` | `text` 必填。可选 `disable_joke=1`、`allow_parse=0` |
| `markdown` | 与 `plain` 相同，按 Markdown 渲染，平台不支持时降级为纯文本 |
| `image` | `path` 必填，支持 URL、`file://` 路径、`base64://` 与 data URI。可选 `headers`（Base64 编码的 JSON）、`max_h`、`allow_split=0` |
| `audio` | `path` 必填，本地文件路径 |
| `video` | `path` 必填，本地文件路径 |
| `i18n` | `i18nkey` 必填。其余键作为翻译参数。可选 `fallback=0`、`locale_failed_prompt=0`、`disable_joke=1` |
| `mention` | `userid` 必填，格式为 `客户端\|用户 ID` |
| `url` | `text` 必填。可选 `trusted=1` 或 `trusted=0` |
| `action_text` | `text` 必填，点击后插入输入框。可选 `show`、`reference=1`、`show_on_fallback=0`、`quote_on_fallback=1` |
| `button` | `show`、`value` 必填。可选 `reply_id`、`permission=all`、`click_limit` |
| `button_frame` | `data` 必填，按钮行数组的 URL 编码 JSON |
<<< END U007566 >>>
<<< UNIT U007567 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:50-50 | ctx=KE 码 >>>
`button` 的 `permission=all` 允许场景内的其他人点击，默认只有发送者可用。`click_limit` 为 `0` 表示不限次数。`button_frame` 的 `data` 由 `ButtonFrameElement.kecode()` 生成，手写时应保持 JSON 结构。
<<< END U007567 >>>
<<< UNIT U007568 | md-heading | packages/akari-bot-core/akaribot/core/docs/placeholders.md:52-52 | ctx=I18N 标记 >>>
## I18N 标记
<<< END U007568 >>>
<<< UNIT U007569 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:54-54 | ctx=I18N 标记 >>>
I18N 标记用于在文本中行内插入翻译结果。语法为：
<<< END U007569 >>>
<<< UNIT U007570 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:60-60 | ctx=I18N 标记 >>>
键名不能包含空白、逗号或花括号。参数可选，名称须匹配 `\w+`，值不能包含逗号。参数值支持 HTML 实体，例如 `&#44;` 表示逗号。
<<< END U007570 >>>
<<< UNIT U007571 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:62-62 | ctx=I18N 标记 >>>
标记由 `Locale.t_str()` 递归解析，最多 10 层，翻译结果中的新标记会继续展开。
<<< END U007571 >>>
<<< UNIT U007572 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:68-68 | ctx=I18N 标记 >>>
需要构造消息元素而非纯文本时使用 `I18NContext`：
<<< END U007572 >>>
<<< UNIT U007573 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:76-76 | ctx=I18N 标记 >>>
`[KE:i18n]` 与 `{I18N:...}` 的区别在于，前者产生独立的 `I18NContextElement`，后者在字符串内做内联替换。
<<< END U007573 >>>
<<< UNIT U007574 | md-heading | packages/akari-bot-core/akaribot/core/docs/placeholders.md:78-78 | ctx=AT 码 >>>
## AT 码
<<< END U007574 >>>
<<< UNIT U007575 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:80-80 | ctx=AT 码 >>>
AT 码用于行内提及用户。语法为 `<AT:客户端|用户 ID>`，也接受 `<@:客户端|用户 ID>`：
<<< END U007575 >>>
<<< UNIT U007576 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:87-87 | ctx=AT 码 >>>
中间可以带额外的子平台字段，解析时取最后一个字段作为用户 ID。例如：
<<< END U007576 >>>
<<< UNIT U007577 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:93-93 | ctx=AT 码 >>>
客户端与当前平台不一致的 AT 码会原样保留。用户 ID 不是纯数字时，按全体提及处理。
<<< END U007577 >>>
<<< UNIT U007578 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:95-95 | ctx=AT 码 >>>
同一段文本中相邻的 AT 码会合并成一次提及，并取最后一个 ID。需要分别提及时，应在两者之间插入其他文本。
<<< END U007578 >>>
<<< UNIT U007579 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:97-97 | ctx=AT 码 >>>
用户 ID 的结构为 `客户端|子平台（可选）|平台 ID`，例如 `QQ|Group|123456`。`MentionElement` 把第一个字段作为客户端，最后一个字段作为 ID。可以用 `~bind whoami` 查看当前账号的完整 ID。
<<< END U007579 >>>
<<< UNIT U007580 | md-heading | packages/akari-bot-core/akaribot/core/docs/placeholders.md:99-99 | ctx=转义 >>>
## 转义
<<< END U007580 >>>
<<< UNIT U007581 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:101-101 | ctx=转义 >>>
参数值中的结构字符须写成 HTML 实体，避免被解析器当作分隔符：
<<< END U007581 >>>
<<< UNIT U007582 | md-table | packages/akari-bot-core/akaribot/core/docs/placeholders.md:103-109 | ctx=转义 >>>
| 字符 | 实体 |
| --- | --- |
| `&` | `&amp;` |
| `,` | `&#44;` |
| `[` / `]` | `&#91;` / `&#93;` |
| `{` / `}` | `&#123;` / `&#125;` |
| `<` / `>` | `&lt;` / `&gt;` |
<<< END U007582 >>>
<<< UNIT U007583 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:116-116 | ctx=转义 >>>
拼接用户输入时，应对结构字符做实体转义。AT 码没有转义语法，ID 中应避开 `|` 与 `>`。
<<< END U007583 >>>
<<< UNIT U007584 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/placeholders.md:118-118 | ctx=转义 >>>
跨平台 ID 不匹配时保持原文。KE 参数值中避免直接出现 `[KE:`，否则扫描消息块时会在此处截断。
<<< END U007584 >>>
<<< UNIT U007585 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:1-1 | ctx=公共 API >>>
# 公共 API
<<< END U007585 >>>
<<< UNIT U007586 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:3-3 | ctx=公共 API >>>
本文按类列出 `akaribot.core.api` 导出的主要名字与用途。
<<< END U007586 >>>
<<< UNIT U007587 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:5-5 | ctx=公共 API >>>
平台适配器另有 `akaribot.core.api.adapters`，收录只有适配器使用的设施。
<<< END U007587 >>>
<<< UNIT U007588 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:11-11 | ctx=公共 API >>>
`__all__` 列出了公开接口的全部名字。新增导出时，须同时更新 `__all__` 与来源映射。
<<< END U007588 >>>
<<< UNIT U007589 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:13-13 | ctx=版本与兼容 >>>
## 版本与兼容
<<< END U007589 >>>
<<< UNIT U007590 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:15-15 | ctx=版本与兼容 >>>
`akaribot.core.api.__api_version__` 读取 `core.registry.CORE_API_VERSION`。各包在 `manifest.toml` 的 `requires_core_api` 中声明兼容范围，官方包写 `">=1,<2"`。
<<< END U007590 >>>
<<< UNIT U007591 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:17-17 | ctx=版本与兼容 >>>
框架在注册包之前检查这个范围。版本不满足要求时，框架拒绝注册这个包并记录原因。这个包因此不会出现在模块或适配器清单里。
<<< END U007591 >>>
<<< UNIT U007592 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:19-19 | ctx=版本与兼容 >>>
公开接口只读取静态声明。配置缺失时未能绑定的名字，会在首次访问时重新解析，因此 CLI 与框架可以在配置就绪之前读取 `__api_version__`。模块与适配器的声明方式分别见[模块开发](module-development.md)与[适配器开发](adapter-development.md)。
<<< END U007592 >>>
<<< UNIT U007593 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:23-23 | ctx=`Bot` >>>
`Bot` 是运行时入口，保存全局状态，并提供跨场景推送与会话获取。
<<< END U007593 >>>
<<< UNIT U007594 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:27-27 | ctx=`Bot.MessageSession` >>>
命令处理函数的输入参数类型。实际对象是当前会话的 `MessageSession`。
<<< END U007594 >>>
<<< UNIT U007595 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:31-31 | ctx=`post_message()` >>>
`Bot.post_message(module_name, message, session_list=None, **kwargs)` 向启用了模块的场景推送消息。`session_list` 为空时，按模块启用状态自动获取目标。
<<< END U007595 >>>
<<< UNIT U007596 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:33-33 | ctx=`post_message()` >>>
同一条消息通道只推送一次，其余会话留作发送失败时的后备。
<<< END U007596 >>>
<<< UNIT U007597 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:37-37 | ctx=`fetch_target()` >>>
`Bot.fetch_target(...)` 按目标信息读取场景快照，返回 `FetchedSessionInfo`。需要向指定场景主动发送消息时，先用 `FetchedMessageSession.from_session_info()` 把它转成会话。
<<< END U007597 >>>
<<< UNIT U007598 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:41-41 | ctx=`get_enabled_this_module()` >>>
`Bot.get_enabled_this_module(module_name)` 返回启用了指定模块的场景列表。计划任务没有消息上下文时，通常先用它获取目标，再调用 `post_message()`。
<<< END U007598 >>>
<<< UNIT U007599 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:45-45 | ctx=`Hook.trigger()` >>>
`Bot.Hook.trigger(name, ...)` 调用带名称的 Hook。名称在 `@module.hook(name=...)` 中声明。
<<< END U007599 >>>
<<< UNIT U007600 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:49-49 | ctx=`MessageSession` >>>
`MessageSession` 代表当前会话。发送、等待、删除、权限检查与执行锁都从这里开始。
<<< END U007600 >>>
<<< UNIT U007601 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:53-53 | ctx=`send_message()` >>>
发送一条消息，返回 `FinishedSession`。字符串会自动包装成只含 `PlainElement` 的消息链。
<<< END U007601 >>>
<<< UNIT U007602 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:55-55 | ctx=`send_message()` >>>
默认会引用触发消息，并执行敏感信息检查。参数与失败处理见[消息 API](message-api.md)。
<<< END U007602 >>>
<<< UNIT U007603 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:59-59 | ctx=`finish()` >>>
发送最终回复并结束当前处理。调用后模块代码不会继续执行，框架会抛出 `SessionFinished`。
<<< END U007603 >>>
<<< UNIT U007604 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:63-63 | ctx=`delete()` >>>
删除触发当前会话的消息。平台不支持删除时，按平台能力返回或报错。
<<< END U007604 >>>
<<< UNIT U007605 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:67-67 | ctx=`check_bot_state()` >>>
读取机器人在当前场景的权限快照，返回 `BotState`。结果会写入 `SessionInfo.bot_state`，供 `Module.unsupported_bot_permissions()` 检查模块权限。
<<< END U007605 >>>
<<< UNIT U007606 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:71-71 | ctx=`wait_confirm()` >>>
等待用户确认。普通模式按确认词判断，用户回复 `no` 时返回 `False`。`confirm_token` 不为 `None` 时，必须原样回复口令。超时或取消抛出 `WaitCancelException`。
<<< END U007606 >>>
<<< UNIT U007607 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:75-75 | ctx=`wait_next_message()` >>>
等待当前会话的下一条消息，返回新的 `MessageSession`。命中的消息仍会进入常规 parser。
<<< END U007607 >>>
<<< UNIT U007608 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:79-79 | ctx=`wait_reply()` >>>
等待引用当前消息的回复。平台不支持引用时，改用 `wait_next_message()` 或 `wait_anyone()`，并以 `quote=False` 发送提示。`all_=True` 时接受任意成员的回复。
<<< END U007608 >>>
<<< UNIT U007609 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:83-83 | ctx=`wait_anyone()` >>>
等待场景内任意成员发送消息，返回新的 `MessageSession`。
<<< END U007609 >>>
<<< UNIT U007610 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:85-85 | ctx=`wait_anyone()` >>>
等待方法默认释放执行锁，返回前重新获取。超时、取消或重新获取失败都抛出 `WaitCancelException`。
<<< END U007610 >>>
<<< UNIT U007611 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:89-89 | ctx=`SessionInfo` >>>
`SessionInfo` 是可跨进程传输的会话快照，不含活动连接。
<<< END U007611 >>>
<<< UNIT U007612 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:91-91 | ctx=`SessionInfo` >>>
主要属性：
<<< END U007612 >>>
<<< UNIT U007613 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:93-98 | ctx=`SessionInfo` >>>
- `target_id`、`target_from`：场景标识与平台名。
- `sender_id`、`sender_name`：发送者。
- `client_name`、`bot_id`、`bot_name`：平台客户端与机器人身份。
- `locale`：当前语言。
- `support_*`：平台能力标志。
- `bot_state`：最近一次 `check_bot_state()` 的结果。
<<< END U007613 >>>
<<< UNIT U007614 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:100-100 | ctx=`SessionInfo` >>>
字段的具体含义见[消息 API](message-api.md)与[适配器开发](adapter-development.md)。
<<< END U007614 >>>
<<< UNIT U007615 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:104-104 | ctx=`FetchedMessageSession` >>>
主动获取的会话。用 `FetchedMessageSession.from_session_info()` 创建。`Bot.fetch_target()` 返回的快照可以直接传入。
<<< END U007615 >>>
<<< UNIT U007616 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:106-106 | ctx=`FetchedMessageSession` >>>
它继承 `MessageSession` 的发送与等待方法，但没有 `session_info.messages`。调用 `as_display()` 前要先检查消息列表是否为空。
<<< END U007616 >>>
<<< UNIT U007617 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:110-110 | ctx=`FinishedSession` >>>
已发送消息的封装对象。`send_message()` 返回这个对象。
<<< END U007617 >>>
<<< UNIT U007618 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:114-114 | ctx=`assign()` >>>
`FinishedSession.assign(session, message_id)` 创建这个对象。单个消息 ID 会转成列表。
<<< END U007618 >>>
<<< UNIT U007619 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:118-118 | ctx=`delete()` >>>
删除这条已发送的消息。实际删除动作交给 `PlatformAPI.delete_message`。
<<< END U007619 >>>
<<< UNIT U007620 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:122-122 | ctx=`MessageChain` >>>
`MessageChain` 是多个消息元素组成的消息链，支持拼接、序列化与安全检查。
<<< END U007620 >>>
<<< UNIT U007621 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:126-126 | ctx=`create()` >>>
创建空消息链。
<<< END U007621 >>>
<<< UNIT U007622 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:130-130 | ctx=`assign()` >>>
`MessageChain.assign(elements)` 从字符串、元素、元素列表或另一条消息链创建消息链，并做深拷贝。
<<< END U007622 >>>
<<< UNIT U007623 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:134-134 | ctx=`is_safe` >>>
属性。遍历消息元素，检查是否包含敏感信息。发送前默认使用这个结果。
<<< END U007623 >>>
<<< UNIT U007624 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:138-138 | ctx=`to_str()` >>>
把消息链转成字符串。`text_only=True` 时只拼纯文本，`element_filter` 可限定转换的元素类型，`connector` 指定连接符。
<<< END U007624 >>>
<<< UNIT U007625 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:142-142 | ctx=`I18NMessageChain` >>>
按语言选择消息链。`I18NMessageChain.assign(values)` 的 `values` 以语言代码为键，必须包含 `default`。
<<< END U007625 >>>
<<< UNIT U007626 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:144-144 | ctx=`I18NMessageChain` >>>
发送时按会话语言选一条。没有匹配语言时使用 `default`。
<<< END U007626 >>>
<<< UNIT U007627 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:148-148 | ctx=`PlatformMessageChain` >>>
按平台选择消息链。`PlatformMessageChain.assign(values)` 的 `values` 以平台名为键，必须包含 `default`。
<<< END U007627 >>>
<<< UNIT U007628 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:150-150 | ctx=`PlatformMessageChain` >>>
选择顺序是 `PlatformMessageChain` > `I18NMessageChain` > `MessageChain`。
<<< END U007628 >>>
<<< UNIT U007629 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:154-154 | ctx=`MessageNodes` >>>
合并转发消息的节点列表。`MessageNodes.assign(values, name=None)` 把多条 `MessageChain` 组成节点列表，`name` 省略时自动生成。
<<< END U007629 >>>
<<< UNIT U007630 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:156-156 | ctx=`MessageNodes` >>>
`is_safe` 检查所有节点。平台未声明 `support_handle_message_nodes` 时，框架会把节点渲染成图片再发送。
<<< END U007630 >>>
<<< UNIT U007631 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:158-158 | ctx=消息元素 >>>
## 消息元素
<<< END U007631 >>>
<<< UNIT U007632 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:160-160 | ctx=消息元素 >>>
`Plain`、`Image`、`Audio`、`Video`、`Markdown`、`Embed`、`EmbedField`、`Url`、`Mention`、`ActionText`、`Button`、`ButtonFrame`、`FormattedTime`、`I18NContext` 与 `Raw` 是构造消息的便捷类。对应的 `*Element` 类是可序列化的元素模型，`BaseElement` 是元素基类。
<<< END U007632 >>>
<<< UNIT U007633 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:162-162 | ctx=消息元素 >>>
`I18NContext` 的参数值支持字符串、数字与消息元素。按钮的排布用 `ButtonPermission`、`ButtonRows`、`arrange_buttons()` 与 `build_button_rows()`。
<<< END U007633 >>>
<<< UNIT U007634 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:166-166 | ctx=`get_message_chain()` >>>
把平台消息链或多语言消息链转换为当前会话可用的 `MessageChain`。
<<< END U007634 >>>
<<< UNIT U007635 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:170-170 | ctx=`match_kecode()`、`escape_special_char()` >>>
前者解析 KE 码，后者转义 KE 的结构字符。元素类型与参数规则见[占位符](placeholders.md)。
<<< END U007635 >>>
<<< UNIT U007636 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:174-174 | ctx=`module()` >>>
`module(name, ...)` 声明模块，返回 `Bind.Module`。后续的命令、正则、计划任务、Hook 与事件都挂载在这个对象上。
<<< END U007636 >>>
<<< UNIT U007637 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:180-180 | ctx=`command()` >>>
`command(template, ...)` 绑定命令。模板里的参数会映射到处理函数的同名参数。
<<< END U007637 >>>
<<< UNIT U007638 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:184-184 | ctx=`regex()` >>>
`regex(pattern, mode="M", ...)` 绑定正则。`mode="M"` 从消息开头匹配，`mode="A"` 在消息内查找。
<<< END U007638 >>>
<<< UNIT U007639 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:188-188 | ctx=`schedule()` >>>
`schedule(trigger)` 绑定计划任务。触发器可用 `CronTrigger`、`IntervalTrigger`、`DateTrigger`、`AndTrigger` 或 `OrTrigger`。
<<< END U007639 >>>
<<< UNIT U007640 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:192-192 | ctx=`hook()` >>>
`hook(point=..., priority=..., name=...)` 绑定 Hook。`priority` 数值小的先执行。带名称的 Hook 由 `Bot.Hook.trigger()` 调用。
<<< END U007640 >>>
<<< UNIT U007641 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:196-196 | ctx=`event()` >>>
`event(event_name, ...)` 绑定平台事件。事件回调的参数是 `EventInfo`。
<<< END U007641 >>>
<<< UNIT U007642 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:200-200 | ctx=`CommandParser` >>>
`CommandParser` 按模块的命令模板解析输入，并生成帮助文档。
<<< END U007642 >>>
<<< UNIT U007643 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:202-202 | ctx=`CommandParser` >>>
主要入口是 `return_formatted_help_doc(locale=None)`。它按当前权限过滤命令，返回可直接发送的帮助文本。
<<< END U007643 >>>
<<< UNIT U007644 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:206-206 | ctx=`ModulesManager` >>>
`ModulesManager` 维护模块注册、别名、Hook、事件与依赖关系。
<<< END U007644 >>>
<<< UNIT U007645 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:208-210 | ctx=`ModulesManager` >>>
- `load_module(module_name)`：加载一个模块，注册它的命令、正则、计划任务与 Hook。
- `reload_module(module_name)`：重新加载模块，并刷新命令、Hook 与配置字段。
- `get_module_and_alias_first_words(module_or_alias)`：返回模块名与别名对应的首词。
<<< END U007645 >>>
<<< UNIT U007646 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:214-214 | ctx=`ModuleRuntimeManager` >>>
`ModuleRuntimeManager` 管理运行时状态。
<<< END U007646 >>>
<<< UNIT U007647 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:216-218 | ctx=`ModuleRuntimeManager` >>>
- `get_or_create(module_name)`：获取模块的 `ModuleRuntime`，没有时创建。
- `ModuleRuntime.get()`：读取模块实例。
- `ModuleRuntime.get_state()`：读取运行状态。
<<< END U007647 >>>
<<< UNIT U007648 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:220-220 | ctx=`ModuleRuntimeManager` >>>
`ModuleStatus` 是模块加载状态的枚举。
<<< END U007648 >>>
<<< UNIT U007649 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:222-222 | ctx=`HookPoint` 与返回值 >>>
## `HookPoint` 与返回值
<<< END U007649 >>>
<<< UNIT U007650 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:224-224 | ctx=`HookPoint` 与返回值 >>>
`HookPoint` 列出命令、正则、会话与执行生命周期的 Hook 位置。
<<< END U007650 >>>
<<< UNIT U007651 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:226-226 | ctx=`HookPoint` 与返回值 >>>
Hook 可以返回：
<<< END U007651 >>>
<<< UNIT U007652 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:228-231 | ctx=`HookPoint` 与返回值 >>>
- `Handled`：表示本次 hook 已处理。
- `Stop`：终止后续处理，可附带消息与作用范围。
- `StopScope`：`Stop` 的作用范围。
- `RecoveryProposal`：向调用方提出恢复建议。
<<< END U007652 >>>
<<< UNIT U007653 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:233-233 | ctx=`HookPoint` 与返回值 >>>
具体触发点与执行顺序见[模块开发](module-development.md)。
<<< END U007653 >>>
<<< UNIT U007654 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:237-237 | ctx=`CFGManager` >>>
`CFGManager` 负责配置读写。模板类在导入时确定每个字段的读取方式，用户配置放在 `config/`，默认层放在 `config/global/`。
<<< END U007654 >>>
<<< UNIT U007655 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:241-241 | ctx=`load()` >>>
读取全局层与用户层，合并成当前配置。
<<< END U007655 >>>
<<< UNIT U007656 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:245-245 | ctx=`save()` >>>
只把有变化的用户配置写回用户层，不修改全局层。
<<< END U007656 >>>
<<< UNIT U007657 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:249-249 | ctx=`get()` >>>
按字段名读取值。值类型不符合模板时给出警告，并返回原值。
<<< END U007657 >>>
<<< UNIT U007658 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:253-253 | ctx=`delete()` >>>
删除用户层里的键。删除后，该键回退到全局默认值。
<<< END U007658 >>>
<<< UNIT U007659 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:257-257 | ctx=`edit_write()`、`edit_delete()` >>>
交互式编辑写入与删除。只在明确授权的范围内使用，供 `~config` 与启动阶段密钥初始化调用。
<<< END U007659 >>>
<<< UNIT U007660 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:259-259 | ctx=`edit_write()`、`edit_delete()` >>>
`CoreConfig`、`BaseConfig` 与 `CoreSecretConfig` 是配置模板类。`on_module_config()` 与 `on_bot_config()` 用来声明模块配置与适配器配置。
<<< END U007660 >>>
<<< UNIT U007661 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:263-263 | ctx=`DBModel` >>>
`DBModel` 是业务模型的基类。
<<< END U007661 >>>
<<< UNIT U007662 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:265-266 | ctx=`DBModel` >>>
- `get_by_target_id()`：按场景 ID 读取记录，可指定是否创建。
- `get_by_sender_id()`：按发送者 ID 读取记录，可指定是否创建。
<<< END U007662 >>>
<<< UNIT U007663 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:268-268 | ctx=`DBModel` >>>
模块自有模型继承 `DBModel`，迁移用 `MigrationContext` 与 `fetch_module_db()`。
<<< END U007663 >>>
<<< UNIT U007664 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:270-270 | ctx=`SenderUnionInfo`、`TargetUnionInfo` 与绑定表 >>>
## `SenderUnionInfo`、`TargetUnionInfo` 与绑定表
<<< END U007664 >>>
<<< UNIT U007665 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:272-272 | ctx=`SenderUnionInfo`、`TargetUnionInfo` 与绑定表 >>>
`SenderUnionInfo` 保存发送者 union 数据，`TargetUnionInfo` 保存场景 union 数据。`SenderUnionBind` 与 `TargetUnionBind` 保存平台 ID 到 union 的映射。
<<< END U007665 >>>
<<< UNIT U007666 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:274-274 | ctx=`SenderUnionInfo`、`TargetUnionInfo` 与绑定表 >>>
场景数据包括 `muted`、`locale`、`modules`、`custom_admins`、`banned_users` 与 `target_data`。
<<< END U007666 >>>
<<< UNIT U007667 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:276-276 | ctx=`SenderUnionInfo`、`TargetUnionInfo` 与绑定表 >>>
`StoredData`、`ModuleStatus`、`AnalyticsData`、`JobQueuesTable` 是 core 自带的数据模型。
<<< END U007667 >>>
<<< UNIT U007668 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:280-280 | ctx=`UNION_SCOPE_SENDER`、`UNION_SCOPE_TARGET` >>>
指定 union 的作用域。
<<< END U007668 >>>
<<< UNIT U007669 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:284-284 | ctx=`union_mutation()` >>>
跨表写入同一 union 时，先调用它，再在 `default` 事务里给 union 行加锁。
<<< END U007669 >>>
<<< UNIT U007670 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:288-288 | ctx=`get_model_names()`、`get_model_fields()` >>>
枚举当前数据库的表与字段。`~database` 命令用它们生成帮助。详见[数据库](database.md)。
<<< END U007670 >>>
<<< UNIT U007671 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:292-292 | ctx=`ServerAPI` >>>
`ServerAPI` 是模块与 Server 进程之间的 RPC 接口约定。
<<< END U007671 >>>
<<< UNIT U007672 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:294-294 | ctx=`ServerAPI` >>>
常见方法：
<<< END U007672 >>>
<<< UNIT U007673 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:296-300 | ctx=`ServerAPI` >>>
- `receive_message()`、`receive_event()`：把消息或平台事件交给 Server 处理。
- `trigger_hook()`：触发带名称的 Hook。
- `direct_message()`：直接向会话发送消息。
- `report_error()`：上报错误。
- `get_bot_version()`、`get_web_render_status()`、`get_runtime_stats()`：读取运行状态。
<<< END U007673 >>>
<<< UNIT U007674 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:302-302 | ctx=`ServerAPI` >>>
直接 `await` 会等待远程结果，`.submit()` 只等到后端接收任务。
<<< END U007674 >>>
<<< UNIT U007675 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:306-306 | ctx=`PlatformAPI` >>>
`PlatformAPI` 是 Server 与平台进程之间的 RPC 接口约定。
<<< END U007675 >>>
<<< UNIT U007676 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:308-308 | ctx=`PlatformAPI` >>>
发送与消息操作：
<<< END U007676 >>>
<<< UNIT U007677 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:313-313 | ctx=`PlatformAPI` >>>
查询与权限：
<<< END U007677 >>>
<<< UNIT U007678 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:318-318 | ctx=`PlatformAPI` >>>
交互与扩展：
<<< END U007678 >>>
<<< UNIT U007679 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:320-322 | ctx=`PlatformAPI` >>>
- `add_reaction()`、`remove_reaction()`、`start_typing()`、`end_typing()`、`error_signal()`。
- `hold_context()`、`release_context()`。
- `call_onebot_api()`：调用平台明确支持的 OneBot 扩展。
<<< END U007679 >>>
<<< UNIT U007680 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:326-326 | ctx=`RpcError` >>>
RPC 失败的基类。具体子类区分不可达、超时、取消、方法不存在与协议错误。
<<< END U007680 >>>
<<< UNIT U007681 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:330-330 | ctx=`web_render` >>>
`web_render` 是渲染服务单例。
<<< END U007681 >>>
<<< UNIT U007682 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:332-334 | ctx=`web_render` >>>
- `init_web_render()`：启动服务。
- `check_web_render_status()`：检查服务状态。
- `close_web_render()`：关闭服务。
<<< END U007682 >>>
<<< UNIT U007683 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:336-336 | ctx=截图参数 >>>
## 截图参数
<<< END U007683 >>>
<<< UNIT U007684 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:338-338 | ctx=截图参数 >>>
截图参数用以下类描述：
<<< END U007684 >>>
<<< UNIT U007685 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:340-346 | ctx=截图参数 >>>
- `PageScreenshotOptions`：整页截图。
- `ElementScreenshotOptions`：元素截图。
- `SectionScreenshotOptions`：区域截图。
- `SourceOptions`：渲染 HTML 源。
- `RawOptions`：直接传原始内容。
- `LegacyScreenshotOptions`：旧版截图参数。
- `ReplaceElementScreenshotOptions`：替换页面元素。
<<< END U007685 >>>
<<< UNIT U007686 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:348-348 | ctx=图像辅助 >>>
## 图像辅助
<<< END U007686 >>>
<<< UNIT U007687 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:350-353 | ctx=图像辅助 >>>
- `ImageTable`：图片表格的数据。
- `image_table_render()`：把表格渲染成图片。
- `msgchain2image()`：把消息链渲染成图片。
- `svg_render()`：把 SVG 渲染成图片元素。
<<< END U007687 >>>
<<< UNIT U007688 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:355-355 | ctx=图像辅助 >>>
服务配置与降级见 [WebRender](webrender.md)。
<<< END U007688 >>>
<<< UNIT U007689 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:359-359 | ctx=`Logger` >>>
`Logger` 提供分级日志。业务代码通过它输出调试、信息、警告与错误级别的日志，模块不需要自己配置日志器。
<<< END U007689 >>>
<<< UNIT U007690 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:363-363 | ctx=`Locale` >>>
`Locale` 负责当前语言的文案。`Locale.t()` 用于获取文案，`Locale.t_str()` 处理已经是文案的字符串。`lang_list` 是可用语言表。
<<< END U007690 >>>
<<< UNIT U007691 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:367-367 | ctx=`Info` >>>
`Info` 提供实例与平台信息。
<<< END U007691 >>>
<<< UNIT U007692 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:369-370 | ctx=`Info` >>>
- `Info.resolve_client_name(platform_name)`：有实例 ID 时返回 `平台-实例ID`。
- `Info.instance_id`：当前实例 ID。
<<< END U007692 >>>
<<< UNIT U007693 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:374-374 | ctx=`Secret` >>>
`Secret` 标记配置字段为密钥。带这个标记的字段写入密钥表，不进入普通配置。
<<< END U007693 >>>
<<< UNIT U007694 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:378-378 | ctx=`Random`、`SecureRandom` >>>
`Random` 提供可复现的随机数。`SecureRandom` 使用安全随机源，适合生成令牌、验证码一类的值。
<<< END U007694 >>>
<<< UNIT U007695 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:382-382 | ctx=`CoolDown`、`TokenBucket` >>>
`CoolDown` 控制同一键的触发间隔。`TokenBucket` 按容量与速率限制调用次数。
<<< END U007695 >>>
<<< UNIT U007696 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:386-386 | ctx=`ExpiringTempDict` >>>
带过期时间的临时字典。写入时指定有效期，读取时自动清理过期项。
<<< END U007696 >>>
<<< UNIT U007697 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:388-388 | ctx=HTTP 与文本工具 >>>
## HTTP 与文本工具
<<< END U007697 >>>
<<< UNIT U007698 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:392-393 | ctx=HTTP 与文本工具 >>>
- `get_url()`、`post_url()`、`request_url()`：发送请求。
- `download()`：下载文件。
<<< END U007698 >>>
<<< UNIT U007699 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:395-395 | ctx=HTTP 与文本工具 >>>
文本与数据：
<<< END U007699 >>>
<<< UNIT U007700 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:397-400 | ctx=HTTP 与文本工具 >>>
- `chunk_list()`：按长度切分列表。
- `truncate_text()`：截断文本。
- `parse_time_string()`：解析时间字符串。
- `converter`：结构化数据转换。
<<< END U007700 >>>
<<< UNIT U007701 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:402-402 | ctx=URL 审计 >>>
## URL 审计
<<< END U007701 >>>
<<< UNIT U007702 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:404-406 | ctx=URL 审计 >>>
- `GlobalURLAllowlist`、`GlobalURLBlocklist`：全局 URL 允许与阻止名单。
- `URLRule`：单条 URL 规则。
- `evaluate_url_policy()`：按规则判断 URL 是否放行。
<<< END U007702 >>>
<<< UNIT U007703 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:408-408 | ctx=运维 >>>
## 运维
<<< END U007703 >>>
<<< UNIT U007704 | md-list | packages/akari-bot-core/akaribot/core/docs/public-api.md:410-412 | ctx=运维 >>>
- `run_sys_command()`：执行系统命令。
- `restart`：重启入口。
- `send_email()`：发送邮件。
<<< END U007704 >>>
<<< UNIT U007705 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:414-414 | ctx=适配器面 >>>
## 适配器接口
<<< END U007705 >>>
<<< UNIT U007706 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:416-416 | ctx=适配器面 >>>
`akaribot.core.api.adapters` 提供适配器专用的名字。
<<< END U007706 >>>
<<< UNIT U007707 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:420-420 | ctx=`ContextManager` >>>
平台上下文管理器。它实现发送、删除、禁言、权限组、表情与输入状态等平台动作。
<<< END U007707 >>>
<<< UNIT U007708 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:424-424 | ctx=`PlatformAPI` >>>
适配器端的 RPC 接口。`context_method()` 把 `ContextManager` 的方法绑定成可远程调用的动作。
<<< END U007708 >>>
<<< UNIT U007709 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:428-428 | ctx=`Features` >>>
声明平台能力。`client_init()` 注册节点时，把这些标志写入 `capabilities`。
<<< END U007709 >>>
<<< UNIT U007710 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:432-432 | ctx=`BotState` >>>
机器人在当前场景的权限快照。`can_*` 字段表示能否执行对应操作，`permissions` 保存平台返回的权限。
<<< END U007710 >>>
<<< UNIT U007711 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:436-436 | ctx=`client_init()`、`client_cleanup()` >>>
`client_init()` 初始化平台客户端并注册能力。`client_cleanup()` 清理连接与临时资源。
<<< END U007711 >>>
<<< UNIT U007712 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:440-440 | ctx=`check_queue()` >>>
检查平台进程的队列状态，供启动与健康检查使用。
<<< END U007712 >>>
<<< UNIT U007713 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:444-444 | ctx=`Temp`、`S3Storage`、`S3StorageAPI` >>>
`Temp` 提供临时文件目录。`S3Storage` 与 `S3StorageAPI` 提供对象存储读写。
<<< END U007713 >>>
<<< UNIT U007714 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:446-446 | ctx=按钮与媒体辅助 >>>
### 按钮与媒体辅助
<<< END U007714 >>>
<<< UNIT U007715 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:448-448 | ctx=按钮与媒体辅助 >>>
按钮：
<<< END U007715 >>>
<<< UNIT U007716 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:453-453 | ctx=按钮与媒体辅助 >>>
媒体：
<<< END U007716 >>>
<<< UNIT U007717 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:458-458 | ctx=按钮与媒体辅助 >>>
两个公开接口共有的名字（`Bot`、`SessionInfo` 与消息元素等）只在 `akaribot.core.api` 导出。适配器同时依赖这两个接口。适配器入口、能力声明与上下文管理器的实现要求见[适配器开发](adapter-development.md)。
<<< END U007717 >>>
<<< UNIT U007718 | md-heading | packages/akari-bot-core/akaribot/core/docs/public-api.md:460-460 | ctx=完整导出清单 >>>
## 完整导出清单
<<< END U007718 >>>
<<< UNIT U007719 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/public-api.md:462-462 | ctx=完整导出清单 >>>
类、函数、常量、方法签名与参数的完整列表见[完整 API 导出清单](api-reference.md)。本页只保留分类说明和常用接口。
<<< END U007719 >>>
<<< UNIT U007720 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:3-3 | ctx=JobQueue >>>
本文介绍 JobQueue 的后端、节点定位、RPC、信号与关闭流程。
<<< END U007720 >>>
<<< UNIT U007721 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:5-5 | ctx=JobQueue >>>
JobQueue 是平台进程与 Server 之间的跨进程通信层，同时提供节点注册表与消息传输。业务代码通过 `PlatformAPI`、`ServerAPI` 与信号声明使用它。
<<< END U007721 >>>
<<< UNIT U007722 | md-heading | packages/akari-bot-core/akaribot/core/docs/queue.md:7-7 | ctx=后端 >>>
## 后端
<<< END U007722 >>>
<<< UNIT U007723 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:9-9 | ctx=后端 >>>
配置在 `config/jobqueue.toml`，`[jobqueue].jobqueue_backend` 可选 `database` 或 `websocket`。两种后端互斥。同一逻辑集群的进程必须使用相同的值，切换后端需要重启进程。
<<< END U007723 >>>
<<< UNIT U007724 | md-table | packages/akari-bot-core/akaribot/core/docs/queue.md:11-16 | ctx=后端 >>>
| 比较项 | `database` | `websocket` |
| --- | --- | --- |
| 传输 | 轮询 `job_queues` 表 | Hub 内实时路由 |
| 离线任务 | 保留待认领记录 | 不保留，目标离线即不可用 |
| 额外组件 | 无 | Hub 进程或外部 Hub |
| 适用场景 | 支持并发写入的共享数据库 | 默认选项，SQLite 与高频 RPC |
<<< END U007724 >>>
<<< UNIT U007725 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:18-18 | ctx=后端 >>>
`jobqueue_websocket_mode` 区分 `embedded` 与 `external`。内置模式从 `jobqueue_websocket_url` 解析监听地址，仅接受回环地址上的 `ws`。连接外部 Hub 须使用 `wss`，并配置共享令牌。
<<< END U007725 >>>
<<< UNIT U007726 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:20-20 | ctx=后端 >>>
`jobqueue_node_id` 是节点标签，为空时 pre-init 会生成 UUID 并写回配置。
<<< END U007726 >>>
<<< UNIT U007727 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:22-22 | ctx=后端 >>>
`jobqueue_websocket_token` 为空时，启动前会生成令牌并写回配置。
<<< END U007727 >>>
<<< UNIT U007728 | md-heading | packages/akari-bot-core/akaribot/core/docs/queue.md:24-24 | ctx=节点身份与定位 >>>
## 节点身份与定位
<<< END U007728 >>>
<<< UNIT U007729 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:26-26 | ctx=节点身份与定位 >>>
每个进程有两个身份：
<<< END U007729 >>>
<<< UNIT U007730 | md-list | packages/akari-bot-core/akaribot/core/docs/queue.md:28-29 | ctx=节点身份与定位 >>>
- `peer_id`：进程启动时生成，用于把请求直接发给该进程。
- `service`：按名称固定的服务组标识（如 `Server`、`QQ`）。同组成员竞争认领普通 RPC 请求，每个请求由一个节点接收。
<<< END U007730 >>>
<<< UNIT U007731 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:31-31 | ctx=节点身份与定位 >>>
进程状态依次为 `starting`、`ready`、`maintenance`、`draining`、`stopped`。`check_job_queue()` 注册实例并切换为 `ready`。
<<< END U007731 >>>
<<< UNIT U007732 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:33-33 | ctx=节点身份与定位 >>>
节点每 15 秒更新一次注册信息，每 10 秒与注册表核对一次。超过 45 秒没有更新，节点就被判定为离线。关闭时，节点先广播 `draining`。处理完正在执行的任务后，节点再广播 `stopped`。
<<< END U007732 >>>
<<< UNIT U007733 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:35-35 | ctx=节点身份与定位 >>>
`core.alive.Alive` 是进程内的同步路由缓存。该缓存只复用已由注册表确认的记录。若要让同一个业务键固定路由到同一个实例，请用 `ServiceRoute` 描述 service、角色与路由键。运行时按 Rendezvous Hash 从 `ready` 实例中选出目标。
<<< END U007733 >>>
<<< UNIT U007734 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:39-39 | ctx=RPC >>>
共享接口约定声明在 `akaribot/core/queue/contracts.py`：
<<< END U007734 >>>
<<< UNIT U007735 | md-list | packages/akari-bot-core/akaribot/core/docs/queue.md:49-53 | ctx=RPC >>>
- 直接 `await` 会等待远程结果。`.submit()` 只等待后端接受任务。
- `ContextManager` 上的平台方法通过 `context_method()` 自动绑定，参数签名取自方法本身。
- 默认超时：普通调用 120 秒，信号 30 秒，消息处理与发送最长 7200 秒。每个请求有独立的截止时间。
- 失败时抛出 `RpcError` 的子类：`RpcUnavailableError`（目标不可达）、`RpcTimeoutError`、`RpcCancelledError`、`RpcMethodNotFoundError`、`RpcProtocolError`，远程异常会包装为 `RpcRemoteError`，并保留 traceback。
- 一个请求至少会被投递一次，也可能重复投递。发送、禁言等有外部副作用的调用在超时后，由调用方判断是否重试。
<<< END U007735 >>>
<<< UNIT U007736 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:55-55 | ctx=RPC >>>
`PlatformAPI.post_message` 在目标通道发送失败时，把 `SessionInfo.next_hops` 交回 Server，由 Server 继续尝试下一跳。整条通道都不可用时，此方法返回空列表。
<<< END U007736 >>>
<<< UNIT U007737 | md-heading | packages/akari-bot-core/akaribot/core/docs/queue.md:57-57 | ctx=信号 >>>
## 信号
<<< END U007737 >>>
<<< UNIT U007738 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:59-59 | ctx=信号 >>>
信号按发送时刻的在线实例逐条发送，各目标独立确认：
<<< END U007738 >>>
<<< UNIT U007739 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:78-78 | ctx=信号 >>>
`.emit()` 只发送，`.gather()` 逐个实例等待确认。信号处理函数必须可以重复执行，同一个信号收到多次时，结果与收到一次相同。带版本号的数据以持久化状态为准。
<<< END U007739 >>>
<<< UNIT U007740 | md-heading | packages/akari-bot-core/akaribot/core/docs/queue.md:80-80 | ctx=数据表 >>>
## 数据表
<<< END U007740 >>>
<<< UNIT U007741 | md-table | packages/akari-bot-core/akaribot/core/docs/queue.md:82-85 | ctx=数据表 >>>
| 表 | 内容 |
| --- | --- |
| `job_queues` | 任务记录（目标、来源、动作、参数、状态、认领者与结果） |
| `job_queue_peers` | 节点注册表（角色、service、状态、能力、元数据与注册有效期） |
<<< END U007741 >>>
<<< UNIT U007742 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:87-87 | ctx=数据表 >>>
`database` 后端以 `pending` 为条件原子认领任务，每轮候选上限 100 条。已经结束的任务，其记录在调用方读取后删除。遗漏的记录由每小时运行的后台任务清理。`websocket` 后端不保存任务记录和结束状态。
<<< END U007742 >>>
<<< UNIT U007743 | md-heading | packages/akari-bot-core/akaribot/core/docs/queue.md:89-89 | ctx=关闭与维护 >>>
## 关闭与维护
<<< END U007743 >>>
<<< UNIT U007744 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:91-91 | ctx=关闭与维护 >>>
进入维护窗口后，节点先停止认领新任务，再等待已经开始的处理完成。数据库热重载在维护窗口内进行，期间独占数据库连接。
<<< END U007744 >>>
<<< UNIT U007745 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/queue.md:93-93 | ctx=关闭与维护 >>>
关闭期间，结果接收器继续运行。会话与后台任务清理完毕后，它才停止。轮询器异常退出时，实例会撤销注册，并释放本地等待方。
<<< END U007745 >>>
<<< UNIT U007746 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:3-3 | ctx=WebRender >>>
本文介绍 WebRender 的配置、运行模式与降级行为。
<<< END U007746 >>>
<<< UNIT U007747 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:5-5 | ctx=WebRender >>>
WebRender 把 HTML、网页或页面元素渲染为图片，供帮助菜单、Wiki infobox、图片表格与其他截图功能使用。
<<< END U007747 >>>
<<< UNIT U007748 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:7-7 | ctx=WebRender >>>
core 通过 `akari-bot-webrender` 客户端调用本地 Playwright 浏览器，或把请求转发到远程渲染服务。渲染不可用时，相关命令改用其他输出方式，例如帮助菜单改用文字或表格。
<<< END U007748 >>>
<<< UNIT U007749 | md-heading | packages/akari-bot-core/akaribot/core/docs/webrender.md:9-9 | ctx=配置 >>>
## 配置
<<< END U007749 >>>
<<< UNIT U007750 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:11-11 | ctx=配置 >>>
配置文件为 `config/webrender.toml`，表名 `[webrender]`。字段在 `akaribot/core/config/webrender.py` 中声明：
<<< END U007750 >>>
<<< UNIT U007751 | md-table | packages/akari-bot-core/akaribot/core/docs/webrender.md:13-20 | ctx=配置 >>>
| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | `bool` | `false` | 是否开启 WebRender |
| `browser_type` | `str` | `"chrome"` | 浏览器类型，支持 `chrome` 与 `firefox` |
| `browser_executable_path` | `str` | `""` | 浏览器可执行文件路径。为空时使用 Playwright 安装的浏览器 |
| `headless` | `bool` | `true` | 是否以无头模式运行浏览器 |
| `remote_only` | `bool` | `false` | 是否仅使用远程服务，跳过本地浏览器 |
| `remote_web_render_url` | `str` | `""` | 远程服务地址。本地渲染失败时尝试，`remote_only` 时必需 |
<<< END U007751 >>>
<<< UNIT U007752 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:28-28 | ctx=配置 >>>
修改后须重启实例才能生效。`~webrender reload` 只重启浏览器，不重新读取配置文件。
<<< END U007752 >>>
<<< UNIT U007753 | md-heading | packages/akari-bot-core/akaribot/core/docs/webrender.md:30-30 | ctx=运行模式 >>>
## 运行模式
<<< END U007753 >>>
<<< UNIT U007754 | md-table | packages/akari-bot-core/akaribot/core/docs/webrender.md:32-38 | ctx=运行模式 >>>
| 配置 | 行为 |
| --- | --- |
| `enable=false` | 不初始化浏览器，状态检查返回不可用 |
| `enable=true`、`remote_only=false`、URL 为空 | 使用本地 Playwright 浏览器 |
| `enable=true`、`remote_only=false`、URL 非空 | 优先本地。浏览器未初始化或渲染失败时转发到远程 |
| `enable=true`、`remote_only=true`、URL 非空 | 不启动本地浏览器，所有请求（含状态查询）均发往远程服务 |
| `enable=true`、`remote_only=true`、URL 为空 | 远程未配置，渲染不可用 |
<<< END U007754 >>>
<<< UNIT U007755 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:40-40 | ctx=运行模式 >>>
远程地址必须是 HTTP 或 HTTPS URL，不能带查询参数或片段标识。
<<< END U007755 >>>
<<< UNIT U007756 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:42-42 | ctx=运行模式 >>>
远程服务由独立的 [`akari-bot-webrender`](https://github.com/Teahouse-Studios/akari-bot-webrender) 项目提供。浏览器与运行依赖的安装方法见该项目文档。机器人侧只需填写地址，并选择是否启用 `remote_only`。
<<< END U007756 >>>
<<< UNIT U007757 | md-heading | packages/akari-bot-core/akaribot/core/docs/webrender.md:44-44 | ctx=启动与状态 >>>
## 启动与状态
<<< END U007757 >>>
<<< UNIT U007758 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:46-46 | ctx=启动与状态 >>>
Server 启动时在后台任务中调用 `init_web_render()`，随后把 `check_web_render_status()` 的结果写入 `Bot.Info.web_render_status`。初始化失败时只记录日志，并把状态设为不可用。
<<< END U007758 >>>
<<< UNIT U007759 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:48-48 | ctx=启动与状态 >>>
`close_web_render()` 在进程退出时关闭本地浏览器。`remote_only` 模式只使用远程服务。
<<< END U007759 >>>
<<< UNIT U007760 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:50-50 | ctx=启动与状态 >>>
`webrender` 是基础模块，命令要求超级用户：
<<< END U007760 >>>
<<< UNIT U007761 | md-table | packages/akari-bot-core/akaribot/core/docs/webrender.md:52-57 | ctx=启动与状态 >>>
| 命令 | 说明 |
| --- | --- |
| `~webrender status` | 输出渲染服务状态 |
| `~webrender start` | 按当前配置初始化。`remote_only` 时只检查远程服务 |
| `~webrender stop` | 关闭本地浏览器。`remote_only` 时只更新状态 |
| `~webrender reload` | 先关闭再重新初始化 |
<<< END U007761 >>>
<<< UNIT U007762 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:59-59 | ctx=启动与状态 >>>
命令清单与权限见[内置工具](../../modules/core/docs/tools.md)。
<<< END U007762 >>>
<<< UNIT U007763 | md-heading | packages/akari-bot-core/akaribot/core/docs/webrender.md:61-61 | ctx=降级 >>>
## 降级
<<< END U007763 >>>
<<< UNIT U007764 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:63-63 | ctx=降级 >>>
`check_web_render_status()` 返回 `false` 时，调用方无需继续请求截图。帮助菜单在生成图片前检查 `Bot.Info.web_render_status`，状态为不可用时改用文字或表格。
<<< END U007764 >>>
<<< UNIT U007765 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:65-65 | ctx=降级 >>>
其他模块通常先检查状态。没有先检查的模块会在调用失败后改用纯文本。异常由渲染服务内部处理，本地与远程都失败时返回 `None`。
<<< END U007765 >>>
<<< UNIT U007766 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:69-69 | ctx=降级 >>>
设置 `remote_web_render_url` 后，本地渲染失败时会改用远程服务，本地浏览器未初始化、渲染结果为空与一般异常都算失败。远程服务也失败时，客户端返回空结果。`remote_only=true` 时只用远程服务，此时远程地址必须可用。
<<< END U007766 >>>
<<< UNIT U007767 | md-heading | packages/akari-bot-core/akaribot/core/docs/webrender.md:73-73 | ctx=程序接口 >>>
## 程序接口
<<< END U007767 >>>
<<< UNIT U007768 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:75-75 | ctx=程序接口 >>>
模块通过公共 API 使用渲染能力：
<<< END U007768 >>>
<<< UNIT U007769 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:90-90 | ctx=程序接口 >>>
`web_render` 还提供以下方法：
<<< END U007769 >>>
<<< UNIT U007770 | md-list | packages/akari-bot-core/akaribot/core/docs/webrender.md:92-95 | ctx=程序接口 >>>
- 页面截图
- 区域截图
- 页面源码
- 原始请求
<<< END U007770 >>>
<<< UNIT U007771 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/webrender.md:97-97 | ctx=程序接口 >>>
这些方法的参数分别由 `PageScreenshotOptions`、`SectionScreenshotOptions`、`SourceOptions` 与 `RawOptions` 描述。`init_web_render()`、`close_web_render()` 与相关选项类都从 `akaribot.core.api` 导出，完整清单见[公共 API](public-api.md)。
<<< END U007771 >>>
<<< UNIT U007772 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:20-20 >>>
# 标记 i18n 快照是否已接上，子进程只在需要注释时接一次。
<<< END U007772 >>>
<<< UNIT U007773 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:23-23 >>>
# 配置注释的键前缀，与配置模板写入期使用的 i18n 键一致（core/config/__init__.py 的注释生成路径）。
<<< END U007773 >>>
<<< UNIT U007774 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:35-35 >>>
# 入口以子进程运行，builtins 包本身不自动初始化，读取任何配置表之前先加载（含版本迁移），重复调用无副作用。
<<< END U007774 >>>
<<< UNIT U007775 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:83-83 >>>
# 各适配器的 enable 共用一条注释，与配置写入路径的键查找规则一致。
<<< END U007775 >>>
<<< UNIT U007776 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:88-88 >>>
# 缺失的键可能回退为键名，也可能回退为 ``{I18N:键名}`` 标记。
<<< END U007776 >>>
<<< UNIT U007777 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:95-96 >>>
# 子进程没有 bot 启动阶段的快照，不接上时 ``Locale.t`` 一律回退为键名（注释会显示成
# ``{I18N:...}`` 标记）。只做一次。
<<< END U007777 >>>
<<< UNIT U007778 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:109-110 >>>
# 键清单以配置文件为准（模板在生成期已把声明字段全部写入磁盘）。占位判定是 schema 与
# placeholders 共用的判定标准，只在这里出现一次。
<<< END U007778 >>>
<<< UNIT U007779 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:131-131 >>>
# 类型与默认值优先使用模板声明，未声明的项使用配置文件中的类型。
<<< END U007779 >>>
<<< UNIT U007780 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:153-153 >>>
# 任一文件损坏都会让 ``CFGManager.load()`` 整体失败，故按表读取文件，未能读取的表单独归集。
<<< END U007780 >>>
<<< UNIT U007781 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:175-175 >>>
# 表名只用于拼接配置目录下的文件名。含分隔符的名字一律拒绝，无法读取目录之外。
<<< END U007781 >>>
<<< UNIT U007782 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:184-184 >>>
# noqa: BLE001 - 解析错误类型取决于 tomlkit，逐表归集后继续
<<< END U007782 >>>
<<< UNIT U007783 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:241-242 >>>
# 不做转换会把 `enable` 之类的布尔项写成字符串 ``"true"``，导致文件里类型不对，重新读取虽是 ``true``
# 但任何按布尔取用的代码都会拿到真值字符串。
<<< END U007783 >>>
<<< UNIT U007784 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:337-337 >>>
# placeholders 只按文件统计，配置加载失败时仍要能报告损坏的表。其余命令都经配置管理器。
<<< END U007784 >>>
<<< UNIT U007785 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:408-408 >>>
# 配置模板在导入时写入磁盘。当前进程启动时还没有这张表，必须重新加载后再读取 schema。
<<< END U007785 >>>
<<< UNIT U007786 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:413-413 >>>
# 包没有模块配置模板（core 内置模块即如此，其配置由首次运行扫描生成），不是失败。
<<< END U007786 >>>
<<< UNIT U007787 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/config.py:449-449 >>>
# noqa: BLE001 - 入口层捕获全部异常，错误信息给操作者看
<<< END U007787 >>>
<<< UNIT U007788 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:25-25 >>>
# 文本列才能做包含与前后缀匹配。其余类型只支持等值与大小比较。
<<< END U007788 >>>
<<< UNIT U007789 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:28-29 >>>
# 运算符按“先长后短”排列，确保双字符运算符先命中，否则不等号与取反包含符会被当成单字符运算符拆开，
# 导致列名与取值错位。
<<< END U007789 >>>
<<< UNIT U007790 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:79-79 >>>
# noqa: BLE001 - 清单读取失败只让 package 一栏留空，不应阻断浏览
<<< END U007790 >>>
<<< UNIT U007791 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:108-108 >>>
# 可调用默认值（uuid4、list 等）的结果要到运行时才能确定，用 null 表示由模型自行确定。
<<< END U007791 >>>
<<< UNIT U007792 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:163-163 >>>
# 把 ``<列><运算符><值>`` 拆成三段。运算符与值都可以省略（省略时按等值处理）。
<<< END U007792 >>>
<<< UNIT U007793 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:175-175 >>>
# 只有列名时按“该列非空”理解，比默默当成等值空字符串更符合预期。
<<< END U007793 >>>
<<< UNIT U007794 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:191-191 >>>
# Tortoise 的等值筛选不支持 ``__exact`` 后缀，直接写列名。
<<< END U007794 >>>
<<< UNIT U007795 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:198-198 >>>
# 在所有文本列上做不区分大小写的包含匹配。表里没有文本列时拒绝。
<<< END U007795 >>>
<<< UNIT U007796 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:227-227 >>>
# 主键作次级排序键，确保分页时同值行之间有稳定顺序，翻页不会重复或漏行。
<<< END U007796 >>>
<<< UNIT U007797 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:236-236 >>>
# 唯一约束、外键约束这类拒绝由数据库给出，属调用方传入了错误的值，按用户错误上报。
<<< END U007797 >>>
<<< UNIT U007798 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:246-246 >>>
# 包已安装但实例尚未创建该表时无法读取条数。此时保留表并如实返回“未知”，不让一张表导致整份清单异常。
<<< END U007798 >>>
<<< UNIT U007799 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:249-249 >>>
# noqa: BLE001 - 不同后端的缺表报错类型不同，统一按未知处理
<<< END U007799 >>>
<<< UNIT U007800 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:291-291 >>>
# 用户错误先校验完成再访问数据库，未知列与非法取值不该先触发数据库报错。
<<< END U007800 >>>
<<< UNIT U007801 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:297-297 >>>
# 大表上 COUNT 是一次全表扫描，故翻页可以只获取本页。不统计总数时 total 返回 null，由调用方沿用上次的值。
<<< END U007801 >>>
<<< UNIT U007802 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:304-304 >>>
# 回显分页与筛选状态，方便调用方据此显示“第几页 / 共几条 / 当前条件”，不必自己记。
<<< END U007802 >>>
<<< UNIT U007803 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:315-315 >>>
# 一行多列更新时，所有取值先转换完再下发，且在同一次 UPDATE 里写入，不会出现“改了一半”的行。
<<< END U007803 >>>
<<< UNIT U007804 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:333-333 >>>
# 连接名必须显式给出，因为实例同时挂着 default 与 local 两个库，省略会被 Tortoise 拒绝。
<<< END U007804 >>>
<<< UNIT U007805 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:403-403 >>>
# 输出恒为 JSON，``--json`` 只为与其他入口的命令行形态保持一致。
<<< END U007805 >>>
<<< UNIT U007806 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:459-459 >>>
# 失败原因同时写入 stdout 的 JSON，因为调用方（CLI 与界面）只解析 stdout，只写入 stderr 则无法获取结构化原因。
<<< END U007806 >>>
<<< UNIT U007807 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/data.py:477-477 >>>
# noqa: BLE001 - 入口层捕获全部异常，错误信息给操作者看
<<< END U007807 >>>
<<< UNIT U007808 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/data.py:36-36 | ctx=DataError >>>
用户错误（未知表或列、缺少必填字段、主键不存在、值无法按列类型转换）。
<<< END U007808 >>>
<<< UNIT U007809 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/db.py:31-32 >>>
# 表名只从 manifest 读取，**绝不接受调用方传入**，因为 purge 是破坏性操作，谁拥有哪张表只能由包自己
# 声明。CLI 即使被改坏或被人手工调用，也无法借这个入口删除未声明的表。
<<< END U007809 >>>
<<< UNIT U007810 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/db.py:87-88 >>>
# 迁移记录表由创建数据表负责。写进程同样先执行 generate_schemas 再迁移，
# 否则全新实例上第一条迁移会因 schema_migrations 不存在而失败。
<<< END U007810 >>>
<<< UNIT U007811 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/db.py:94-94 >>>
# 迁移按包名记录，core 的迁移记录为 "core"，而 CLI 传的是包名 akari-bot-core。
<<< END U007811 >>>
<<< UNIT U007812 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/db.py:98-98 >>>
# 没有迁移目录是合法状态，本仓库 39 个模块包不创建数据表。只有包未安装时才算用户错误。
<<< END U007812 >>>
<<< UNIT U007813 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/db.py:104-104 >>>
# 旧版本号转换与逐包 revision 一并执行，旧数据库升到某版本后其 revision 视为已应用。
<<< END U007813 >>>
<<< UNIT U007814 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/db.py:113-115 >>>
# 表已不存在时按幂等成功处理，因为本命令的预期目标是“这些表不再存在”，重新运行或手工删除后再次运行
# 都满足该预期，报成失败只会让卸载流程停滞在已经达成的目标上。缺失的表名如实返回，操作者
# 据此判断清单是否不同步。
<<< END U007814 >>>
<<< UNIT U007815 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/db.py:204-205 >>>
# --json 时把原因也写入 stdout，因为调用方（CLI 的 db_purge）解析的是 stdout，
# 只写入 stderr 则无法获取结构化原因，只能退回“退出码 1”这种无用信息。
<<< END U007815 >>>
<<< UNIT U007816 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/db.py:213-213 >>>
# noqa: BLE001 - 入口层统一捕获，错误信息给操作者看
<<< END U007816 >>>
<<< UNIT U007817 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/db.py:16-16 | ctx=PurgeError >>>
卸载清理不满足前提（包不在发现结果里，或没有可删除的表）。
<<< END U007817 >>>
<<< UNIT U007818 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:84-84 >>>
# 内置模块与核心运行时同属一个包，不按模块包命名。
<<< END U007818 >>>
<<< UNIT U007819 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:106-106 >>>
# noqa: BLE001 - 元数据残缺时按导入路径推导
<<< END U007819 >>>
<<< UNIT U007820 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:118-118 >>>
# noqa: BLE001 - 元数据残缺时按源码克隆处理
<<< END U007820 >>>
<<< UNIT U007821 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:126-126 >>>
# noqa: BLE001 - Summary 缺失不影响清单
<<< END U007821 >>>
<<< UNIT U007822 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:133-133 >>>
# 按项目声明顺序显示依赖，跳过 extra 的可选依赖。
<<< END U007822 >>>
<<< UNIT U007823 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:159-159 >>>
# 读取运行依赖，跳过 extra 的可选依赖。
<<< END U007823 >>>
<<< UNIT U007824 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:164-164 >>>
# noqa: BLE001 - 元数据残缺时按无依赖处理
<<< END U007824 >>>
<<< UNIT U007825 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:187-187 >>>
# noqa: BLE001 - 无法读取安装记录时按普通安装处理
<<< END U007825 >>>
<<< UNIT U007826 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:212-212 >>>
# 依次返回全局、用户覆盖与迁移兼容的文档元数据文件。
<<< END U007826 >>>
<<< UNIT U007827 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:490-490 >>>
# noqa: BLE001 - 单个类不可内省时仍保留类说明
<<< END U007827 >>>
<<< UNIT U007828 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:544-544 >>>
# noqa: B007 - 只遍历公开承诺
<<< END U007828 >>>
<<< UNIT U007829 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:686-686 >>>
# noqa: BLE001 - 安装记录缺失或损坏时视为非可编辑安装
<<< END U007829 >>>
<<< UNIT U007830 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:695-695 >>>
# 可编辑安装的入口只在安装时写入元数据，源码 pyproject 之后新增的 akaribot.docs 声明要重新安装才生效。
<<< END U007830 >>>
<<< UNIT U007831 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:700-700 >>>
# noqa: BLE001 - 元数据残缺的包不参与补入
<<< END U007831 >>>
<<< UNIT U007832 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/docs.py:739-739 >>>
# noqa: BLE001 - 元数据损坏时回退到目录扫描，仍给出可用结果
<<< END U007832 >>>
<<< UNIT U007833 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:16-16 >>>
# 等 Server 确认的秒数上限。热加载要处理完队列任务并让出调度器窗口，故高于普通查询。
<<< END U007833 >>>
<<< UNIT U007834 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:19-19 >>>
# peer 注册与就绪的秒数上限。超时说明实例的 JobQueue 不可达。
<<< END U007834 >>>
<<< UNIT U007835 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:22-22 >>>
# 实例未运行时的统一提示，与 CLI 文案一致，避免两处说法不一致。
<<< END U007835 >>>
<<< UNIT U007836 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:31-31 >>>
# 表不存在表示实例尚未完成过一次启动，与状态为空对操作者是同一件事，故一并返回空映射。
<<< END U007836 >>>
<<< UNIT U007837 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:39-39 >>>
# noqa: BLE001 - 状态表不可读时降级为“无记录”，原因如实输出
<<< END U007837 >>>
<<< UNIT U007838 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:47-48 >>>
# 清单里的 ``provides_modules`` 覆盖内置模块与已安装模块包。它声明为空的包只有运行时才
# 知道注册名，这类包不产生条目，其模块名由状态表补上，包名留空。
<<< END U007838 >>>
<<< UNIT U007839 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:70-70 >>>
# 下划线开头的是框架内部注册（解析器策略、错误处理等），不是用户可加载的模块，列出只会成为噪声。
<<< END U007839 >>>
<<< UNIT U007840 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:89-89 >>>
# 本进程只做一次 RPC，注册为临时 peer 以便接收结果，不修改任何模块索引，也不写入状态表。
<<< END U007840 >>>
<<< UNIT U007841 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:102-102 >>>
# 后端与 peer 的装配失败与“连不上”对操作者是同一件事，都意味着实例的 JobQueue 用不了。
<<< END U007841 >>>
<<< UNIT U007842 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:106-106 >>>
# noqa: BLE001 - 配置未生成或后端不可用，实例同样不可达
<<< END U007842 >>>
<<< UNIT U007843 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:112-112 >>>
# noqa: BLE001 - 连不上 JobQueue 与实例未运行对操作者是同一件事
<<< END U007843 >>>
<<< UNIT U007844 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:132-132 >>>
# 与 list 规则一致，下划线开头是框架内部注册，不接受用户加载。
<<< END U007844 >>>
<<< UNIT U007845 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:136-136 >>>
# noqa: BLE001 - 校验只是提前拦截笔误，无法读取状态表时不应阻断操作
<<< END U007845 >>>
<<< UNIT U007846 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:166-166 >>>
# noqa: BLE001 - 入口层统一捕获，错误信息给操作者看
<<< END U007846 >>>
<<< UNIT U007847 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:204-204 >>>
# noqa: BLE001 - 入口层统一捕获，错误信息给操作者看
<<< END U007847 >>>
<<< UNIT U007848 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:27-27 | ctx=InstanceUnreachable >>>
运行中的 Server 实例不可达。
<<< END U007848 >>>
<<< UNIT U007849 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/modules.py:96-96 | ctx=_notify_server.CliPeer >>>
一次性 RPC 调用方。只发送一次请求，不绑定任何远端处理器。
<<< END U007849 >>>
<<< UNIT U007850 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/peers.py:18-18 >>>
# 导入本身就可能在实例配置缺失时抛出异常（core 的配置在导入阶段加载），故一并纳入降级路径。
<<< END U007850 >>>
<<< UNIT U007851 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/peers.py:24-24 >>>
# noqa: BLE001 - 数据库不可用属可降级状态
<<< END U007851 >>>
<<< UNIT U007852 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/peers.py:29-29 >>>
# noqa: BLE001 - 表不存在时同样降级
<<< END U007852 >>>
<<< UNIT U007853 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/peers.py:38-38 >>>
# 租约是唯一事实来源，已过期的记录仍在表里，但不算在线。
<<< END U007853 >>>
<<< UNIT U007854 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/peers.py:64-64 >>>
# 默认即 JSON，--json 显式写法与 TUI 数据源的调用一致，必须接受。
<<< END U007854 >>>
<<< UNIT U007855 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/registry.py:23-23 >>>
# noqa: BLE001 - 元数据缺失不该让清单输出失败
<<< END U007855 >>>
<<< UNIT U007856 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/registry.py:46-46 >>>
# 供兼容性诊断使用，缺了它消费方只能显示“未声明”，与 manifest 实际内容不符。
<<< END U007856 >>>
<<< UNIT U007857 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/registry.py:48-49 >>>
# 供卸载清理使用，表名确定要删除的表，config_table 确定要删除的扁平配置文件。
# 缺这两项时 CLI 只能靠 provides_modules 猜文件名，而现行布局是扁平路径。
<<< END U007857 >>>
<<< UNIT U007858 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:21-22 >>>
# 等 Server 确认的秒数上限。接口约定为 7200 秒（热加载要导入依赖并重挂数据库 context），但
# Server 掉线而租约未过期时无人认领消息，按约定等下去会让 CLI 阻塞两小时，故在此缩短。
<<< END U007858 >>>
<<< UNIT U007859 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:25-25 >>>
# peer 注册与就绪的秒数上限。超时说明实例的 JobQueue 不可达。
<<< END U007859 >>>
<<< UNIT U007860 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:28-28 >>>
# 白名单记录 remote 到固定接口的对应关系。新增包变更动作时必须在此记录，不得由调用方拼方法名。
<<< END U007860 >>>
<<< UNIT U007861 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:125-125 >>>
# 后端与 peer 的装配失败与“连不上”对操作者是同一件事，都意味着实例的 JobQueue 用不了。
<<< END U007861 >>>
<<< UNIT U007862 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:129-129 >>>
# noqa: BLE001 - 配置未生成或后端不可用，实例同样不可达
<<< END U007862 >>>
<<< UNIT U007863 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:135-135 >>>
# noqa: BLE001 - 连不上 JobQueue 与实例未运行对操作者是同一件事
<<< END U007863 >>>
<<< UNIT U007864 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:161-161 >>>
# 超时表示“结果未知”，远端可能已经修改了状态，调用方不得当作未发生。
<<< END U007864 >>>
<<< UNIT U007865 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:165-165 >>>
# noqa: BLE001 - 入口层捕获全部异常，错误信息给操作者看
<<< END U007865 >>>
<<< UNIT U007866 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:194-194 >>>
# 白名单在导入 core 之前判断，既避免为一次误用启动整套运行时，也不给拼接方法名留入口。
<<< END U007866 >>>
<<< UNIT U007867 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:59-59 | ctx=InstanceUnreachable >>>
运行中的 Server 实例不可达。
<<< END U007867 >>>
<<< UNIT U007868 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:81-81 | ctx=Outcome.exit_code >>>
本结果对应的进程退出码。
<<< END U007868 >>>
<<< UNIT U007869 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:85-85 | ctx=Outcome.payload >>>
结果 JSON 载荷。
<<< END U007869 >>>
<<< UNIT U007870 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/rpc.py:119-119 | ctx=_deliver.CliPeer >>>
一次性 RPC 调用方。只发送一次请求，不绑定任何远端处理器。
<<< END U007870 >>>
