# AkariBot TUI（Textual）

T5.0 的交付物之一：把 Textual 的用法收口到 `_compat.py`，并把「该用什么写法规避什么」的结论、
多环境验证进度（**已验证 / 未验证**两张表）落在本文件，供后续页面（Config / Dashboard / Logs /
Run / Adapters / Dev）遵循。

| 文件 | 职责 |
| --- | --- |
| `_compat.py` | 全部 Textual 导入与调用、终端宽度计算、包内资源与样式表加载、键位构造 |
| `app.py` | App 装配、全局键位、样式表来源、启动计时 |
| `modules.py` | Modules 页：数据源接口 + 子进程实现 + 页面控件 |
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
                          │     └── 策略 2：akaribot.cli.instance.Instance.installed()
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
- **安装/卸载**：后台任务里 `asyncio.to_thread` 调子进程，进度条按 4 个阶段推进
  （解析 → 子进程 → 重载列表 → 完成）；失败时归零并显示退出码与 stderr 尾部。
- 安装目标：优先当前选中的未安装项，否则取搜索框里合法的模块名（`module add <名>` 语义），
  因为 `module list` 只返回已装包，未装包无法从列表里选。

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
| `--self-check` | 9 项通过 / 5 项警告 / 退出码 0（警告为终端环境项，如不在 tmux、非冻结产物、`app.tcss` 尚未拆分） |
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
  --output-filename=akaribot.bin packages/akari-bot-cli/src/akaribot/cli/main.py
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
