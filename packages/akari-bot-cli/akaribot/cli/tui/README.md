# AkariBot TUI（Textual）

T5.0 的交付物之一：把 Textual 的用法收口到 `_compat.py`，并把「该用什么写法规避什么」的结论、
多环境验证进度（**已验证 / 未验证**两张表）落在本文件，供后续页面（Config / Dashboard / Logs /
Run / Adapters / Dev）遵循。

| 文件 | 职责 |
| --- | --- |
| `_compat.py` | 全部 Textual 导入与调用、终端宽度计算、包内资源与样式表加载、键位构造 |
| `cli_process.py` | 调用本 CLI 的 argv 与环境拼装（冻结感知、实例根、UTF-8），各页共用 |
| `app.py` | App 装配、侧栏与页面注册、全局键位、样式表来源、启动计时 |
| `environment.py` | 环境页：托管方式、解释器、core 版本、包清单（可搜索）与三个环境动作 |
| `database.py` | 数据库页：库表与数据项浏览、增删改查（写操作二次确认） |
| `modules.py` | 模块页：安装 / 卸载 / 更新 / 装载切换、多选批量、详情 |
| `adapters.py` | 适配器页：平台安装、启用 / 禁用、实例新增 / 移除 |
| `config.py` | 配置页：表清单、表单与原始文本两种模式 |
| `logs.py` | 日志页：进程筛选、跟随、清空、debug |
| `run.py` | 运行页：启动 / 停止 / 重启，状态轮询 |
| `dev.py` | 开发页：工作区包清单、跑测试、生成模块 / 适配器脚手架 |
| `doctor.py` | 体检页：端口冲突、凭据重复、孤立配置 |
| `misc.py` | 杂项页：不属于其它页面的一次性操作，目前是「迁移项目」（按钮 → 输入框 → 确认） |
| `dashboard.py` | 概览页：实例根目录、名称、语言、core 版本与来源、运行状态与判据、更新提示 |
| `commands/tui.py` | `akaribot tui [--self-check] [--headless] [--no-mouse]` |

**硬性约定**：`akaribot/cli/tui/` 下除 `_compat.py` 外的模块**不得**直接 `import textual` 或
`import rich`；`commands/tui.py` 在函数内延迟导入，`akaribot --help` 不付界面导入开销
（实测 `akaribot --version` 0.11–0.13 s，`akaribot tui --headless` 0.37–0.45 s）。

## 一、结论清单：该用什么写法规避什么

| 写法 | 规避的问题 |
| --- | --- |
| 宽度一律 `_compat.display_width()`（内部 `rich.cells.cell_len`），**禁止** `len()` / `str.ljust` / f-string 对齐 | 中日韩字符与 emoji 占 2 列，按码点数排版必然错位；`len("安装")==2` 而显示宽度是 4 |
| 截断用 `_compat.truncate_cells()`（内部 `rich.cells.chop_cells`），补齐用 `pad_cells()` / `fit_cells()` | `chop_cells` 不劈开宽字符；Textual 自身在奇数列裁剪时补空格（实测 `Strip.crop(0,3)` 对「名称」得 `'名 '`） |
| 详情面板两列用 `_compat.align_rows()`：先取标签列最大显示宽度再补齐 | 中英混排的标签列（「名称」「发行包」「核心 API」）列宽不同，硬编码空格数会错位 |
| 列表行的列宽在渲染时按控件实际宽度计算；放不下简介列就整列丢弃 | 80×24 与 60×20 下都不换行、不溢出；60 列时行退化为「标记 + 名称 + 版本」 |
| CSS 里对列表行用 `text-wrap: nowrap; text-overflow: ellipsis` | 属性名是 Textual 较新版本才有的（旧版用 `overflow`）；即使行宽算错也只是裁剪，不会把列表撑成多行 |
| 样式表变量（`$text-muted` 等）必须经应用实例解析：`_compat.parse_stylesheet(css, app=compat.App())` | 脱离 `App.get_css_variables()` 调用 `Stylesheet.parse()` 会报 `UnresolvedVariableError`（`--self-check` 曾因此失败，已修） |
| 样式表经 `importlib.resources` 读文本后赋给 `App.CSS`，**不用** `App.CSS_PATH` | `CSS_PATH` 依赖 App 子类所在文件的磁盘路径，Nuitka onefile 冻结后该路径不成立 |
| 键位写 `_compat.bind` / `_compat.bindings` 的三元组 | `Binding` 的参数表增删过（四元组、`id` / `system` / `group`、`priority` 语义）；`/` 的键名由 Unicode 名派生为 `solidus`，运行期实际是 `slash`，由 `KEY_ALIASES` 归一 |
| 每个动作都提供键位，鼠标只作补充；`run_app(mouse=False)` 可整体关掉鼠标追踪 | tmux 与旧 conhost 会吞掉或乱码鼠标转义序列（Textual 启动时写 `?1000/1003/1015/1006`）；不能有「只能点、不能按」的操作 |
| 文本选择开关用 `_compat.set_text_selection(widget, False)`（`ALLOW_SELECT`） | 该开关是较新版本才从 App 级拆到控件级的；列表页要的是点击选中而不是拖选文本 |
| 子进程 JSON 文本一律 `markup=False` / `_compat.plain_text()` | 模块名与简介里出现 `[` 会被 Textual 标记语法吞掉 |
| 通知用 `_compat.notify(app, msg, severity=...)`（关键字） | `App.notify` 的 `severity` 由位置参数改为关键字参数；未挂载时静默返回 |
| 列表高亮只订阅 `ListView.Highlighted` / `ListView.Selected`，下标统一读 `list_view.index` | 早期版本还有 `IndexChanged`，8.x 已移除；`highlighted_child` 与 `index` 语义有出入 |
| 无头测试经 `_compat.app_test(app, size=...)` | `run_test` 的 `headless` / `size` 均为关键字，`size` 是较新版本才加的 |
| `App[ReturnType]` 泛型、`ComposeResult`、各 widget 一律从 `_compat` 取 | 这些名字的导出位置（`textual.app` / `textual.widgets` / `textual.containers`）在版本间搬过家 |
| 数据源走注入接口，绝不在渲染路径取数 | `installed()` 是子进程（实测 90–170 ms，core 未就绪时更久）；每帧调用会直接拖垮界面 |
| **自有属性与方法名不得占用 Textual 基类名**（`_render` / `offset` / `refresh` / `display` / `styles` 等），如渲染辅助改叫 `_render_fields`、读取游标改叫 `read_offset` | 覆盖 `Widget._render()` 会让容器 visual 为 `None`，headless 下必崩（`AttributeError: 'NoneType' object has no attribute 'render_strips'`）；`Widget.offset` 是控件位置，语义完全不同 |
| 定时轮询前先判 `self.display`，隐藏页直接跳过 | 各页同挂载，隐藏页仍按周期取数会白白起子进程；实测隐藏页取数次数完全不变 |
| 切页后把焦点交给该页（各页提供 `focus_primary()`，`app.show_page()` 统一调用） | 焦点留在侧栏或上一页时，页级键位（`r`/`space`/`c`/`d`/`s`/`x`）不触发，反而被 App 级同键接管 |
| 页面只经 `_compat` 使用 Textual，页面内零 `import textual` / `import rich` | 升级 Textual 时改动面收敛到一个文件；已 grep 验证各页均无直接导入 |

## 二、中文宽字符（本项目默认中文，最关键的一条）

- 计算：`display_width("安装") == 4`、`display_width("骰子 v1.0") == 9`，而 `len()` 分别是 2 与 7。
- 截断：`truncate_cells("安装骰子模块", 7) == "安装骰…"`（宽 7）；`truncate_cells(..., 1) == "…"`，
  不会留下半个宽字符。
- 交叉验证：把 `名称      骰子 dice 混排` 交给 `Static` 渲染，`Strip.text.rstrip()` 与原文一致，
  其显示宽度 24 与 `display_width()` 的计算值相同；Textual 在奇数列裁剪时以空格补齐（`'名 '`）。
- 页面实测：80×24 下详情各列的值起始单元格同为第 10 列（「发行包」「类型」「状态」「核心 API」四行）。

## 三、数据流与缓存（Modules 页）

```
ModulesPage ──(注入)──> ModuleSource
                          ├── SubprocessModuleSource（默认，唯一生产实现）
                          │     ├── 策略 1：python -m akaribot.cli.main module list --json
                          │     ├── 策略 2：akaribot.cli.instance.Instance.installed()
                          │     ├── 可安装集合（默认并入）：… module available --json
                          │     └── 安装/卸载：… module add|remove，逐行读回输出
                          └── StaticModuleSource（自动化断言与 --self-check 用替身）
```

- CLI 进程不 import core：两条策略都是子进程，环境注入 `AKARI_INSTANCE_DIR`，实例根由
  `find_instance_root()` 定位。
- 策略 1 的 argv 在冻结产物里自动去掉 `-m`（`sys.frozen` / `__compiled__`），可用
  `AKARIBOT_CLI_BIN` 覆盖入口；子进程两侧统一 UTF-8（`PYTHONIOENCODING` + `encoding="utf-8"`）。
- 两条策略都失败时抛出汇总后的 `ModuleSourceError`，界面把原因显示在状态栏，不崩溃。
- **缓存**：`_records` + `_loaded_at`，`cache_ttl` 默认 30 s。搜索、重绘、窗口尺寸变化、
  详情更新一律只读缓存；只有挂载、`r` 键、`--force` 刷新、安装/卸载成功后（`invalidate_cache()`）
  才再取数。自动化断言用一个「第二次取数即抛错」的替身证明了这一点。
- **安装/卸载**：异步起子进程并逐行读回输出（`stream_operation`），每行显示在状态栏，完整序列
  留在 `stream_lines`；进度条按 4 个阶段推进（解析 → 子进程 → 重载列表 → 完成），失败时归零并
  把输出尾部作为详情。子进程输出可能长达数分钟，沿用阻塞式 `subprocess.run` 时界面只能空转。
- **列表范围**：默认列出全部（已装在前、未装在后），用户不必先知道名字再搜索；「只看已安装」
  开关独立成一行并水平居中，把列表收窄到已装。列表上方有与行同宽的表头（名称 / 版本 / 装载 /
  简介），列宽由 `_layout()` 统一计划：放不下简介时整列丢弃并把余量给名称列，窄屏再收窄装载列，
  收不下 4 列就整列去掉。未装项来自 `list_available()`（按分发名去重，已装项保留带
  版本与依赖的那条）；取不到时保留已装列表并把原因附在状态栏，不清空整页。
- **未安装的平台**：适配器页列出全部平台——已装的给启用／禁用，未装的给安装入口。数据来自
  `module available --kind adapter --json`，按平台名与 `adapter list` 的结果去重（已有配置的平台
  不重复补，那种记录本来就是 `installed=False`）。同一位置承载两种动作：按钮与 `i` 对未安装项是
  安装，对已装项是启用／禁用，`e` 也按同一规则分派。装完自动失效缓存并重载，随即可以启用。
- **两页分工**：模块页只列模块（`module available --kind module`），适配器只在适配器页出现，
  免得「安装模块」按到适配器上；合并时另有一道 `kind` 兜底过滤。
- **多选与批量**：选择模型对齐桌面列表——`Space`／`Ctrl+Space` 切换当前项，`Shift+↑/↓` 从锚点
  扩选一段（再移动是重算范围，不累加），`a` 全选可见项，`c` 清空；鼠标上普通点击收敛为单选、
  `Ctrl+点击` 切换、`Shift+点击` 扩选。`i`／`u` 作用于选区（没有选区时仍是当前项），选区按方向
  各筛一遍：安装只带未装项、卸载只带已装项。批量卸载先问一次，目标集合不变时再按一次才执行。
  批量执行逐条上报进度，单条失败不中断其余，收尾汇总成功与失败；成功的项随即从选区移除，
  失败的留着便于重试。`ListView` 本身不支持多选，选中位由页面自己维护并按 `_selected_key`
  复原光标。
- 安装目标：优先当前选中的未安装项，否则取搜索框里合法的模块名（`module add <名>` 语义）。

### 运行页（实例生命周期）

- 界面**不持有实例进程**：启动走 `akaribot run --detach`（实例自建会话），状态走
  `akaribot run --status --json`，停止走 `akaribot run --stop`。因此界面退出后实例继续运行，
  新开的界面也能停止由别的界面、终端或系统服务启动的实例。
- 进程号记在实例锁 `<实例根>/.bot.lock` 的内容里，锁本身仍是唯一的「是否在运行」判据；停止时
  先向主进程发温和信号，让它按自身顺序收拢适配器与 Server，超时才强杀，主进程退出后再清收它
  自建的进程组。与控制器同组的实例只按进程号发信号，避免把控制器自己一起终止。
- 状态刷新是后台任务（CLI 调用约 0.1 s），同一时刻只保留最新一次，慢响应不会堆积。

### 品牌主题

- 调色板取自品牌立绘 `packages/akari-bot-assets-brand/.../character_marked.png`：不透明部分以浅紫与
  粉色为主（`#f6d5f3` / `#fbd8ec` / `#d69cdd`），暗部是深紫褐（`#40333f` / `#2b002a`）。深色版取
  暗部作底、亮部作强调色，浅色版直接用图里的浅底与深色描边；语义色（成功 / 警告 / 失败）在图里
  没有对应，按同一色相家族调和，保证在各自底色上可读。
- 两套主题在应用构造时注册并激活深色版：样式表里的 `$primary` 等变量在首次解析时就要取到品牌色。
  `ctrl+t` 在深色与浅色之间切换。
- 调色板与主题构造都在 `_compat`（唯一允许 import textual 的模块）里，`--self-check` 的
  「品牌主题」一项核对激活的主题名与 `$primary` 的实际取值。

### 环境页（托管方式与包清单）

- 三个动作说的是同一件事的三种去向，标签直接写结果：**改用托管 venv**（把当前解释器里的包装进
  实例自己的 venv）、**改用系统解释器**（把实例 venv 的包迁回系统解释器）、**重建实例 venv**
  （Python 升级后修环境）。
- 按当前模式只显示适用的那个：托管实例给后两个，外部实例只给第一个；读不到模式时三个都不显示，
  托管方式那一行如实写「托管方式未知」而不是当成外部解释器。
- 实例运行期间一律拒绝：这些动作会换掉它正在用的解释器，先停止实例再执行（状态栏说明原因）。
- 环境归属比的是**环境根目录**（有 `pyvenv.cfg` 的那一层），不是解释器文件：uv 建的 venv 都把
  `bin/python` 指向同一个基础解释器，按 `resolve()` 后的文件比较会把两个不同的 venv 判成同一个。
- 包清单来自 `venv status --json` 的 `packages`，每行是「分发名 版本（可编辑）」，输入框按名字过滤；
  动作失败后那句结论会一直留在状态栏，直到手动刷新——否则紧接着的重读会把它冲掉。

### 数据库页

- 左栏是库表清单（`ListView` + 搜索），右上是一页数据项，右下是编辑区（每列一个输入框，主键只读）。
- 数据经 `akaribot db tables/rows` 读取，写入经 `db set/insert/delete`；表名与列名只认 core 里注册
  过的 ORM 模型，界面不拼 SQL，也不接受未注册的表名。
- **写操作一律两次确认**：`s`（保存改动）、`i`（新建）、`d`（删除）第一次只在状态栏列出将改动的列
  与新旧值，第二次按同一个键才落库；`Esc` 清空待确认状态并退出新建模式。
- **一行一次调用**：保存把整行的改动合成一次 `db set --key … --set 列=值 …`，core 侧先转换完所有
  取值再在同一次 UPDATE（显式 `in_transaction("default")`）里下发。改多列与改一列走同一条路，
  一处取值非法时整行不动，不会留下改了一半的行。
- 新建模式下主键那行换成输入框：自增主键留空由数据库生成，非自增主键（如 `module_status.module_name`、
  `stored_data.stored_key`）必须填，否则这类表根本建不了数据项。
- 写成功后重读当前表并尽量停在原主键上；失败时状态栏给出 CLI 的结论与输出尾部。

### 杂项页

- 平时只显示一个按钮：杂项操作要么一次性、要么需要额外输入，常驻输入框只会白占屏幕。
- 点击按钮弹出单行输入的模态框（`_compat.ask_text`），回车或「迁移」提交、Esc 或「取消」返回；
  拿到路径后再按一次按钮才真正执行，状态栏先列出将要发生什么。

### 界面交互约定

- **危险动作二次确认**：批量卸载、实例移除（含 `--purge-data`）、环境接管 / 解除 / 重建、旧项目
  迁移都先在状态栏问一次，再按同一个键才执行；目标或动作一变就重新询问。
- **CLI 的交互提问由界面代答**：能代答的一律用 CLI 已有的开关（`--yes`），问题由界面自己问；
  子进程不必也不该再向用户提问。
- **耗时动作逐行回显**：安装、更新、跑测试、生成脚手架都逐行读回子进程输出，状态栏给出行数与
  退出码；`Esc` 请求终止正在跑的动作。
- **只读信息就近展示**：环境状态、模块装载数、体检统计并入各自页面的字段或列表，不另设
  「命令输出」页。

## 四、已验证（本机：macOS 27.0 / arm64、Python 3.12.13、textual 8.2.8）

| 项目 | 结论与证据 |
| --- | --- |
| 版本紧钉 | `pyproject.toml` 为 `textual==8.2.8`；`--self-check` 比对运行期版本，不一致即硬失败 |
| headless 渲染自证 | `run_test()` 79 条断言全通过：启动、列表填充、排序、搜索过滤、详情随选中项更新、安装/卸载回调、键位、80×24 与 60×20 布局 |
| 真实数据端到端 | 用最小实例跑真实 `akaribot module list --json`：取到 52 条记录（含 `kind` 模块/适配器），52 行全部渲染、行宽不溢出、只取数一次；`AKARI_INSTANCE_DIR=<实例> akaribot tui --headless` 输出「80×24 下渲染 52 行模块记录」 |
| 中文宽字符 | 见第二节；与 Textual 自身渲染结果交叉验证一致，详情各列值起始列实测同为第 10 列 |
| 渲染路径不取数 | 「第二次取数即抛错」替身证明搜索/重绘/resize/缓存内刷新均未取数 |
| 子进程取数链路 | 注入 runner 校验 argv、cwd、`AKARI_INSTANCE_DIR`、`PYTHONIOENCODING`/`encoding=utf-8`、JSON 解析、失败汇总；冻结产物分支的 argv 去掉 `-m` 也被断言覆盖 |
| 非终端保护 | 无 TTY 时拒绝启动并提示改用 `--self-check` / `--headless`（退出码 2） |
| 启动耗时 | run→`on_mount` 14–19 ms，首帧 46–60 ms；`tui --headless` 进程总耗时 0.37–0.45 s（`import textual` 本身 0.06–0.07 s；真实取数子进程 0.28–0.30 s 在后台任务里，不阻塞首屏） |
| 渲染截图 | `export_screenshot()` 导出真实渲染 SVG（合成数据 80×24 / 60×20 / 100×30，真实数据 100×30），列表行与详情文本可在 SVG 里逐字核对 |
| `--self-check` | 14 项通过 / 5 项警告 / 退出码 0（警告为终端环境项，如不在 tmux、非冻结产物、`app.tcss` 尚未拆分）；含「可安装列表与安装进度」与「品牌主题」两项，后者核对 `$primary` 与立绘调色板一致 |
| 静态检查 | `ruff check` 与 `ruff format --check` 通过；`tools/lint_comments.py` 对本次新增文件 0 违规 |

## 五、未验证（需要什么环境、要观察什么、本机为什么做不了）

本机限制有两条硬事实：本会话的 bash 没有 TTY（`stdin.isatty()=False`），且**沙箱拒绝分配 pty**
（`script -q /dev/null …` 报 `openpty: Operation not permitted`，本会话不允许申请提权）。
因此下面每一项都**没有**截图或结论，表中只写「该看什么」与「复跑方式」。

| 环境 | 要观察什么 | 本机为什么做不了 |
| --- | --- | --- |
| macOS Terminal.app（基线） | 中文对齐、`q`/`/`/`i`/`u` 键位、鼠标点击安装按钮、退格与中文输入法、启动是否 > 1 s | 无 TTY 且 pty 被拒；`TERM_PROGRAM=Apple_Terminal`、`COLORTERM=truecolor` 只是从父进程继承的环境变量，不能当作实跑证据 |
| iTerm2 | 真彩渲染是否正常、鼠标（`?1006` 协议）是否被吞、文本选择与 `ALLOW_SELECT=False` 是否冲突 | 未安装 iTerm2，且同样需要真实 TTY |
| Windows Terminal | 中文对齐（ConPTY 下的宽度）、鼠标、`ctrl+q`、路径分隔符、子进程标准流编码（已强制 `PYTHONIOENCODING=utf-8` 并在父进程按 UTF-8 解码，但仍需在 GBK 代码页实测确认） | 无 Windows 主机 |
| Windows 旧 conhost | 降级是否可接受：鼠标转义序列残留、真彩退化为 16 色、`text-wrap: nowrap` 下是否错位 | 无 Windows 主机；这是**风险最高**的一项，Textual 启动即写鼠标序列 |
| Linux + tmux | tmux 是否吞掉鼠标与 `ctrl+q`（`prefix` 冲突）、`?1000/1003/1015/1006` 是否残留、SSH 下重绘是否卡顿 | 本机不在 tmux 内、无 Linux 主机 |
| SSH，窄终端 80×24 | 布局是否塌、窄屏下详情面板是否需要滚动、逐帧重绘的带宽感受 | 无 SSH 目标；80×24 的**布局**已用 headless `size=(80,24)` 与 `resize_terminal(60,20)` 覆盖，但网络重绘成本覆盖不到 |
| **Nuitka onefile 冻结产物** | `.tcss` 等包内资源能否加载、`--self-check` 在冻结产物里的退出码、首屏是否明显变慢（解包开销） | 本机未安装 Nuitka，也不应在本任务里引入构建依赖；当前样式表还是内联常量，`app.tcss` 一项在自检里为警告而非失败 |

### 复跑命令（有对应环境的人照着做）

```bash
# 通用：交互实跑与自检
export UV_CACHE_DIR="$PWD/.uvcache"
.venv/bin/akaribot tui --help
.venv/bin/akaribot tui --self-check      # 资源 / 样式表 / 中文宽度 / 80x24 启动；非零退出码表示失败
.venv/bin/akaribot tui --headless        # 无 TTY 环境下的冒烟：启动、取数一次、退出并打印耗时
.venv/bin/akaribot tui --no-mouse        # tmux 或旧 conhost 下先关鼠标对比
.venv/bin/python /tmp/verify_tui_pilot.py   # 79 条 headless 断言（脚本在 /tmp，不入库）

# 用真实实例看首屏（把 <实例根> 换成有 akaribot.toml 的目录）
AKARI_INSTANCE_DIR=<实例根> .venv/bin/akaribot tui --headless   # 期望「渲染 N 行模块记录」，且数据源调用 1 次

# tmux / SSH 下额外记录
tmux new -s akari 'akaribot tui'         # 观察鼠标点击与 ctrl+q 是否被 prefix 吞掉
printf 'q' | script -q /dev/null akaribot tui   # 需要一个能分配 pty 的环境，用于录屏与观感记录

# 冻结产物（T6.5(a)）
nuitka --onefile --assume-yes-for-downloads \
  --include-package=akaribot.cli.tui --include-package-data=akaribot.cli.tui \
  --output-filename=akaribot.bin packages/akari-bot-cli/akaribot/cli/main.py
./akaribot.bin tui --self-check ; echo "exit=$?"   # 期望 0；任一 [fail] 项即决定 --include-package-data 要列哪些包
```

## 六、已知取舍与后续

1. **样式表尚未拆成 `app.tcss`**：本次只允许改动 5 个文件，故 CSS 以内联常量放在 `app.py`，
   但加载路径已经收口在 `_compat.load_stylesheet()`：一旦新增 `tui/app.tcss`，它会自动优先使用
   包内资源，同时需要把 `akaribot.cli.tui` 加进打包数据（`--include-package-data`），
   `--self-check` 的「样式表资源 app.tcss」一项届时会从警告变为通过。
2. **对端 JSON 字段名未冻结**：`normalize_records()` 用别名表兼容
   `dist/distribution/package`、`name/module/import_name`、`summary/description` 等写法，
   也接受 `{"modules": [...]}`、顶层数组、以包名为键的映射三种形态。
   实测当前 `akaribot module list --json` 返回顶层数组，每项含
   `dist` / `name` / `kind` / `version` / `editable` / `requires_core_api` / `provides_modules`：
   **没有 `summary`、`state`、`dependents`**，故真实数据下列表不显示简介、详情里「简介」「被依赖」
   分别为「无」与缺省，全部记录按「已安装」处理。建议 T5.2 定稿时补上 `summary`（取自包 metadata）
   与 `state`，页面即可自动展示；在那之前界面按缺省值工作，不需要改代码。
3. **安装/卸载复用 CLI 子命令**：页面调 `module add` / `module remove`，真实动作与兼容性预检
   由 T5.2 提供；当前环境下这些子命令会失败，界面按「失败 + 退出码 + stderr 尾部」展示。
4. **`esc` 的两段语义**：搜索框有内容时清空搜索，已为空时把焦点交回列表；如需真正的「返回上一页」，
   等出现第二页时再引入 Screen 栈（`_compat` 已再导出 `Screen` 并提供 `push_screen` / `pop_screen` 包装）。
