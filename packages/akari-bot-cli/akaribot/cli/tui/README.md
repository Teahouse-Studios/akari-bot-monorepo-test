# AkariBot TUI（Textual）

T5.0 的交付物之一：把 Textual 的用法收口到 `_compat.py`，并把「该用什么写法规避什么」的结论、
多环境验证进度（**已验证 / 未验证**两张表）落在本文件，供后续页面（Config / Dashboard / Logs /
Run / Adapters / Dev）遵循。

| 文件 | 职责 |
| --- | --- |
| `_compat.py` | 全部 Textual 导入与调用、终端宽度计算、包内资源与样式表加载、键位构造 |
| `cli_process.py` | 调用本 CLI 的 argv 与环境拼装（冻结感知、实例根、UTF-8），各页共用 |
| `context.py` | 界面当前操作的实例：各页数据源在取数时经它解析实例根，切换实例后自动改指 |
| `app.py` | App 装配、侧栏与页面注册、全局键位、样式表来源、启动计时 |
| `environment.py` | 环境页：环境清单（全部已装包 + 清单记录）、装 / 卸运行库、托管方式与解释器动作 |
| `database.py` | 数据库页：库表与数据项浏览、条件筛选与分页、增删改查（写入前弹确认框并列出改动摘要）；窄屏自动改成上下堆叠 |
| `modules.py` | 模块页：安装 / 卸载 / 更新（`U` 弹范围选择，可只更新选中项或全部 `--all`）/ 装载切换、多选批量、详情 |
| `adapters.py` | 适配器页：平台安装、启用 / 禁用、实例新增 / 移除（弹框确认；只删配置文件，场景与用户数据保留） |
| `config.py` | 配置页：表清单、表单与原始文本两种模式；`o` 把终端交给外部编辑器打开该表文件 |
| `logs.py` | 日志页：进程筛选、贴底跟随（上滚即暂停）、关键词过滤、清空、debug；解析规则在 `akaribot/cli/logs.py` |
| `run.py` | 运行页：启动 / 停止 / 重启（均弹框确认，可只启动指定适配器），状态轮询 |
| `dev.py` | 开发页：工作区包清单、跑测试、生成模块 / 适配器脚手架（类型二态切换，config / database / tests 开关）；动作输出全量保留在可滚动区，状态栏只放结论 |
| `doctor.py` | 体检页：端口冲突、凭据重复、孤立配置；回车跳到对应页面处理 |
| `misc.py` | 迁移页：迁移旧项目（按钮 → 输入框 → 模态确认，可先预演） |
| `dashboard.py` | 概览页：本机实例清单、服务状态与装卸、当前实例的字段；实例操作都在页底两行按钮上 |
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
  各筛一遍：安装只带未装项、卸载只带已装项。批量卸载先弹确认框（选项给处置方式），超过 10 个
  还要输入目标数量。
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

### 概览页：多实例与服务

- 顶部是首次使用的行动区：四项摘要（未配置适配器数、待填写占位符数、实例运行状态、最近一次体检
  结论）与三个跳转按钮（去配置 / 启动实例 / 运行体检），前提不满足的按钮置灰并说明原因。摘要首次
  显示时取一次，`r` 可重取；取数失败逐项降级为「未取到（原因）」，不影响页面其余部分。
  未配置适配器数与体检结论来自 `akaribot doctor --json`，运行状态来自锁文件探测，占位符数来自
  `akaribot config placeholders --json`（core 入口 `placeholders` 一次遍历全部表，本机实测 0.27 s；
  逐表 `config schema` 需 13 s 级）。该命令失败时退化为按配置文本标记估算，标签改成「疑似待填写
  （估算）」并在原因里写明走了估算——估算值不作精确值展示。

- 顶部是**本机实例清单**（注册表 `~/.akaribot/instances.toml`，`AKARIBOT_HOME` 可改）：每行给
  注册名、运行状态、位置与策略标记，当前管理的那个带 `▸`；站在未登记的实例里启动界面时，它也会
  作为「（未登记）」出现在清单里。
- 界面启动时会把**当前所在的实例**自动登记进注册表，随后以通知报出结论；已在注册表里的原样跳过。
  站在实例之外（例如源码仓库根）而下级目录里恰好有一个实例时，登记并切换过去；下级有多个实例时
  不猜，只把候选报出来。这一步在命令行入口（`akaribot tui`、裸调用 `akaribot`）完成，界面只读
  注册表；`--self-check` 与 `--headless` 不走这条路，不会写用户的注册表。
- `Enter`（或 `s`）切换实例：`context.set_active_root()` 记下新根，应用重挂载全部页面，各页随后的
  取数都指向新实例。数据源因此**在取数时**解析实例根（`context.resolve_root()`），不在构造时定死。
- `a` / `c` 翻转开机自启与崩溃重启（写回注册表）；`n` 弹出输入框登记实例目录，输入框预填当前实例
  根因而回车即登记；`d` 连按两次移除登记（实例目录本身不动）。自启是逐实例的开关：服务启动时只
  恢复**开了自启**且上次在跑的实例，「上次在跑」本身不构成拉起的理由。
- **页底按钮区是主要入口**，键位（`n` / `ctrl+n` / `ctrl+d` / `a` / `c` / `i` / `r` / 回车）作为
  快捷方式保留，`?` 键位一览里能查全。按钮按语义分两组：对选中实例（切换实例 / 新建实例 /
  登记目录 / 移除登记）与对当前实例（开机自启：开|关 / 崩溃重启：开|关 / 安装服务|卸载服务 /
  刷新）。按钮区见 `_compat.ButtonFlow`：宽终端下一行放完，放不下才在分组处折行，列宽按最宽的
  标签对齐。按钮的标签与禁用状态跟着清单、策略与服务状态走——没选中、未登记或平台没有服务
  后端时直接置灰，不让用户点下去才被拒绝。
- 清单上方的说明行不再逐条罗列键位，改成指向页底按钮。
- `n` 登记已有目录，`ctrl+n` 新建实例（弹输入框收目录 → 选「建托管 venv」或「用当前环境」→
  经 `akaribot init <目录> --non-interactive` 执行并把输出逐行回显）；`ctrl+d` 二次确认移除登记。
- 切换实例（`Enter`）成功后会把缺省实例写回注册表（`instance use` 的效果），退出界面后 CLI 读到的
  也是它；未登记的实例只切本次会话并如实说明。切换前若别的页面有未保存改动，先在模态里问一次。
- 服务行展示常驻服务状态；`i` 弹出选择框（执行 / 先预演 / 取消），单元文件已存在时确认文案明确
  写「将覆盖现有单元文件」。
- 缺省实例的写回在子进程里异步进行，结论用通知给出——切换后页面会重挂载，状态栏随旧页消失。单元文件由 CLI 侧 `service` 模块生成，界面不
  自己拼；单元里记下安装时的注册表位置（`AKARIBOT_HOME`），因为系统服务管理器不继承登录 shell
  的环境，服务进程据此读到的注册表与 `service status` 读到的必须是同一份。

### 环境页（环境清单与运行库装卸）

这一页是 uv 的薄封装，管的是**环境里装了什么**，与模块页的定位不同：模块页管 AkariBot 模块的
安装与装载，这里管任意运行库（含 httpx 这类传递依赖）。

- 清单是「环境里的全部分发」与「实例清单记录的运行库」的并集：每行给标记、名称、版本与标签。
  标记 `●` 表示这条记在实例清单里（`akaribot.toml` 的 `runtime.requirements`），`○` 表示只存在于
  当前环境；标签写性质——`模块` / `适配器`（提供了对应入口点）、`AkariBot`（名字带前缀）、
  `可编辑`、`未安装`（清单里有记录但环境里没有，重建时会补装）。输入框按名字与来源地址过滤，
  勾选「只看清单里的」只看记录项；表头与行共用同一份列宽计划，放不下时先丢标签列。
- `i` 安装运行库：先弹输入框要需求串（PyPI 名字、版本区间、仓库地址或 `git+` 直引用），选中后
  再问去处——**写进实例清单并安装**（`venv add --save`，环境重建时按它补装）或**仅装进当前环境**
  （`--no-save`，重建后不保留）。`u` 卸载：记在清单里的包同样先问去处（**移除记录并卸载** /
  **仅从环境卸载，保留记录**），没记录的包连按两次确认即可。
- 装卸只动 site-packages，实例运行期间允许；此时状态栏会补一句「重启后才会生效」，因为已经
  import 的模块不会因为环境变了就换版本。选中项的摘要写在「选中」那一行，并列出依赖它的
  AkariBot 包，便于判断卸掉会不会影响运行。
- 装卸与环境动作合成一个按钮区（`_compat.ButtonFlow`）：宽终端下一行，窄终端下在两组之间折行；
  三个解释器动作按一次键就弹选择框（执行 / 先预演 / 取消），标签直接写结果：**改用托管 venv**（把当前解释器里的
  包装进实例自己的 venv）、**改用系统解释器**（把实例 venv 的包迁回系统解释器）、**重建实例
  venv**（Python 升级后修环境）。按当前模式只显示适用的那个：托管实例给后两个，外部实例只给
  第一个；读不到模式时三个都不显示，托管方式那一行如实写「托管方式未知」而不是当成外部解释器。
  实例运行期间一律拒绝——这些动作会换掉它正在用的解释器，先停止实例再执行（状态栏说明原因）。
- 环境归属比的是**环境根目录**（有 `pyvenv.cfg` 的那一层），不是解释器文件：uv 建的 venv 都把
  `bin/python` 指向同一个基础解释器，按 `resolve()` 后的文件比较会把两个不同的 venv 判成同一个。
- 底部按钮分两行：上行是包装卸（安装运行库 / 卸载 / 刷新），下行是解释器动作；动作失败后那句
  结论会一直留在状态栏，直到手动刷新——否则紧接着的重读会把它冲掉。

### 数据库页

- 左栏是库表清单（`ListView` + 搜索），右上是一页数据项（条件行 + 列表 + 翻页按钮），右下是编辑区
  （每列一个输入框，主键只读）。
- 数据经 `akaribot db tables/rows` 读取，写入经 `db set/insert/delete`；表名与列名只认 core 里注册
  过的 ORM 模型，界面不拼 SQL，也不接受未注册的表名。
- **筛选与搜索都下推到 core**：`f` 弹出输入框，写成 `<列><运算符><值>` 就是筛选条件（`=`、`!=`、
  `>`、`>=`、`<`、`<=`、`~` 包含、`!~` 不包含、`^` 前缀、`$` 后缀，值写 `null` 判空），其余写法
  一律按**全表搜索**处理（在所有文本列里找这个词）；多条条件之间是 AND，`ctrl+f` 清空。判定条件
  只看「列名开头 + 运算符」，所以搜索词里带 `~`、`=` 也不会被误当成条件。大表上搜索会全表扫描，
  条件则按列过滤——想知道有哪些列可筛，输入框的提示里直接列出当前表的列名。
- **排序也下推**：`o` 弹出输入框，写列名按升序、写 `列名:desc` 按降序、留空回到缺省（主键倒序）；
  当前排序始终显示在条件行末尾。`ctrl+f` 只清条件与搜索词，排序留着。
- **一页最多 50 条**：`n` / `p` 翻页，`g` / `G` 跳首末页，底部四个翻页按钮同步禁用；页码、总条数与
  本页条数都按 core 回传的 `total` 计算，筛选或改排序后立即重算并回到第一页。纯翻页带 `--no-count`，
  不重复数总数（大表上一次 COUNT 就是一次全表扫描），条数沿用上一页的值。界面上限固定为 50，CLI 的
  `--limit` 可另给（core 侧上限 200）。
- 条件与排序只对当前表成立，换表即清空；写入或筛选后偏移落到末页之外时夹回末页，不会停在空白页。
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
  拿到路径后弹确认框（先预演 / 开始迁移 / 取消），框里列出将下发的选项。

### 侧栏与页面说明

- 侧栏按四组排列：概览与运行（概览 / 运行 / 日志 / 体检）、配置与平台（配置 / 适配器 / 模块）、
  环境与数据（环境 / 数据库）、开发与迁移（开发 / 迁移）。分组标题是禁用条目，方向键会跳过，
  鼠标点到它时高亮还给当前页。
- 每个页面条目第二行是该页用途（如「旧项目迁入」），`?` 浮层顶部也会写「本页用途」并附一行固定
  导航说明（`↑/↓` 选页、`Enter` 打开、`Esc` 取消或返回等）。
- 侧栏次序与翻页次序不同：页面创建、`ctrl+←/→` 翻页与逐页遍历只读 `PAGES`，侧栏下标由
  `TuiApp._nav_position(key)` 折算。80×24 下侧栏需要滚动才能看全 15 条。

### 长输出

动作输出（跑测试、装包、迁移失败等）不再截断：数据源的 `detail` 保留全部行，页面里放进
`VerticalScroll`，长行换行后完整可读。`o` 或「查看输出」按钮把焦点交给输出区，`Home`/`End`/
`PgUp`/`PgDn`/`↑`/`↓` 都可用；运行中只在已经贴底时自动跟随，上滚即暂停并在标题行提示按 `End`
回到末尾。状态栏只留结论与下一步（例如「动作失败，退出码 7，按 o 查看完整输出」），行数写在输出
区标题里。

### 渲染守卫

后台取数与定时轮询可能在页面卸载（切实例重挂载、退出界面）之后才落地，此时 Textual 已经卸掉子
控件，按 id 取控件会抛 `NoMatches` 并把异常抛给 worker。页面构造时由 `_compat.guard_renders()`
统一把 `_render*` / `_sync*` / `_set_*` / `_paint*` 这些只写控件的入口包一层：

- 进入时页面不可用（应用已请求退出，或页面挂载过又被卸下）→ 直接返回，并记一次跳过诊断；
- 进入时页面可用、抛错时已被卸下 → 属卸载竞态，按不可用处理；
- **页面可用时抛出的 `NoMatches` 原样抛出**——活动页面里的选择器错误必须让 worker、自检与用例
  看到，不能被统一守卫吞掉。`tests/test_tui_render_guard.py` 固化这三条契约。

`mounted()` 的判据分三种情形：应用已请求退出（`App._exit`）→ 不可用；页面挂载过又被卸下 →
不可用；页面还没走完首次 `on_mount`（此时 `is_mounted` 尚为假，但子控件已建好、首次渲染正依赖
这一点）→ 可用。只判 `is_mounted` 会跳过页面自己的首次渲染，界面会停在未初始化的样子。

### 与 CLI 的分工

- **写操作一律经 `akaribot <子命令>` 子进程**（`cli_process.cli_argv` + `cli_env`，界面用已有的
  `--yes` 代答确认）：CLI 是唯一写入口，参数校验与确认只有一份。概览页的实例登记 / 移除 / 缺省项 /
  策略与服务装卸、各页的安装与迁移都走这条。
- **读操作允许进程内直读**，但限于不含业务判断的本机状态：注册表、锁文件、日志文件、
  `akaribot.toml`。概览页 2 秒一次轮询、日志页 1 秒一次跟随，起子进程会明显拖慢。需要 core 参与
  判断的读取（配置 schema、数据项、模块清单、体检）一律经子进程。
- **界面不得拥有 CLI 没有的能力**：新增界面功能前先问「对应的命令是什么」，没有就先补命令。
  日志的解析规则因此在 `akaribot/cli/logs.py`，由 `akaribot logs` 与日志页共用。

### 界面交互约定

- **破坏性动作一律弹模态确认**：一次触发就弹出选择框，框里写清后果与可选项（改写哪些列、
  保留数据还是连数据一起清、执行还是先预演）。状态栏里「再按一次 X 确认」的写法已经不用了——
  它既容易被鼠标双击与键盘连发穿透，也让人看不清到底将改动什么。
- **闸门只挡连发**：`_compat.PendingConfirm.accept(key)` 在 0.4 秒的防抖窗口内拒绝同一个目标，
  避免双击或按住不放叠出两层模态；`reset()` 在切页（`TuiApp.show_page()` → 页面 `reset_pending()`）、
  刷新、换选中项时清掉记录。周期性轮询不作废，否则 2 秒一次的轮询会让确认框反复出现。
- **不可逆动作要打字确认**：全选后的批量卸载超过 10 个要求输入目标数量。做错一步也回得来。
- **先预演再执行**：`module` / `venv` / `service` / `adapter instance remove` / `migrate legacy`
  这些命令都有 `--dry-run`，界面在确认框里给「先预演」选项，输出显示在状态栏或详情区
  （概览页的服务预演全文留在 `service_preview`）。
- **破坏性动作不用单字母键**：删除 / 移除类走 `ctrl+d` 或专用键（卸载用 `u`），并必须弹确认框。
- **未保存改动不静默丢失**：配置页与数据库页实现 `dirty_note()`，换表 / 换行 / 重载 / 切模式 /
  切实例前先问「放弃改动」；`TuiApp.switch_instance()` 会逐页收集后再问一次。
- **退出前看后台任务**：有 worker 在跑时按 `q` 先确认，免得把装了一半的子进程丢在后台。
- **当前实例写在标题栏**：`sub_title` 是「实例管理｜<注册名>」，切换实例后立即更新——界面同时
  管多个实例，看不出在改哪一个最危险。
- **换页不用鼠标**：`ctrl+←` / `ctrl+→` 逐页走（越界折返），`?` 打开本页键位一览（低频键位不在
  页脚显示，浮层里能查全）。
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
| 真实数据端到端 | `akaribot tui --headless` 跑两段真实冒烟：默认首屏（断言 `active_page == dashboard`、`#setup` / `#instance-list` / `#fields` 已挂载、焦点非空）与模块页（显式 `initial_page="modules"`、真实 `module list` 子进程、要求数据源取数 ≥1 次并打印真实行数）。用最小实例实测：模块页渲染 44 行、`list` 调用 1 次 |
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
.venv/bin/akaribot tui --headless        # 无 TTY 冒烟：真实默认首屏（概览页控件与焦点）+ 模块页真实取数，任一段失败即非零退出
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
