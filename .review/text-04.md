# 全仓可读文本审核稿 · 第 04 册 / 共 20 册

覆盖 U001495–U001851，10 个文件、357 个单元、32,997 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-cli/akaribot/cli/commands/run.py` | 6 | U001495–U001500 | 205 |
| `packages/akari-bot-cli/akaribot/cli/commands/service.py` | 5 | U001501–U001505 | 144 |
| `packages/akari-bot-cli/akaribot/cli/commands/test.py` | 4 | U001506–U001509 | 288 |
| `packages/akari-bot-cli/akaribot/cli/commands/tui.py` | 29 | U001510–U001538 | 899 |
| `packages/akari-bot-cli/akaribot/cli/commands/venv.py` | 16 | U001539–U001554 | 601 |
| `packages/akari-bot-cli/akaribot/cli/docs/commands.md` | 54 | U001555–U001608 | 7,923 |
| `packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md` | 86 | U001609–U001694 | 11,956 |
| `packages/akari-bot-cli/akaribot/cli/docs/index.md` | 27 | U001695–U001721 | 2,067 |
| `packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md` | 74 | U001722–U001795 | 3,752 |
| `packages/akari-bot-cli/akaribot/cli/docs/tui.md` | 56 | U001796–U001851 | 5,162 |

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
<<< UNIT U001495 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/run.py:31-31 >>>
# 后台启动后等待实例获取锁的秒数。获取锁前需完成 pre-init（配置、数据库），故留出余量。
<<< END U001495 >>>
<<< UNIT U001496 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/run.py:152-152 >>>
# 取到锁才算启动成功，因为进程可能在 pre-init 阶段就因配置或数据库问题退出。
<<< END U001496 >>>
<<< UNIT U001497 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/run.py:180-181 >>>
# 服务守护循环按这里的 desired 恢复上次的运行状态。无记录的实例与不可用的注册表都不该让
# 启动或停止失败，故静默跳过。
<<< END U001497 >>>
<<< UNIT U001498 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/run.py:1-1 | ctx=<module> >>>
运行机器人
<<< END U001498 >>>
<<< UNIT U001499 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/run.py:37-37 | ctx=console_log_path >>>
后台实例控制台输出的保存路径。
<<< END U001499 >>>
<<< UNIT U001500 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/run.py:60-60 | ctx=run >>>
启动、停止或查看实例。未知参数原样传递给 core。
<<< END U001500 >>>
<<< UNIT U001501 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/service.py:98-98 >>>
# 等待期间收到信号也能立即结束本轮，不必等满一个间隔。
<<< END U001501 >>>
<<< UNIT U001502 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/service.py:109-109 | ctx=install >>>
写入系统服务单元并注册服务。``--dry-run`` 只打印将写入的内容。
<<< END U001502 >>>
<<< UNIT U001503 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/service.py:127-127 | ctx=uninstall >>>
注销服务并删除单元文件。未安装时如实说明，不算失败。
<<< END U001503 >>>
<<< UNIT U001504 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/service.py:143-143 | ctx=status >>>
查看服务单元是否安装、是否已在系统中注册。
<<< END U001504 >>>
<<< UNIT U001505 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/service.py:170-170 | ctx=supervise >>>
守护本机实例，对期望运行的执行恢复或重启，期望停止的保持不动。
<<< END U001505 >>>
<<< UNIT U001506 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/test.py:25-27 >>>
# ``init`` 默认只安装 core、适配器与用户选择的模块，不安装 ``akari-bot-testing``——它是开发期依赖。
# 缺少依赖包时若直接把子进程的 ``No module named`` 抛给用户，用户无从知道该安装什么。此处给出明确的
# 下一步提示。
<<< END U001506 >>>
<<< UNIT U001507 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/test.py:57-58 >>>
# 模式必须经环境变量传递，因为 runner 在导入期读取 CI / COVERAGE，argv 里的开关生效过晚（这正是
# “--ci 仍是非 CI 模式”的原因）。argv 里也留一份，让两条入口语义一致。
<<< END U001507 >>>
<<< UNIT U001508 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/test.py:1-1 | ctx=<module> >>>
运行测试
<<< END U001508 >>>
<<< UNIT U001509 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/test.py:45-45 | ctx=test >>>
在实例环境里运行测试。未知参数原样传递给 akaribot.testing。
<<< END U001509 >>>
<<< UNIT U001510 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:26-26 >>>
# 未执行的检查不能视为通过，因此与失败项一并返回非零退出码。
<<< END U001510 >>>
<<< UNIT U001511 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:67-67 >>>
# 延迟导入 Textual，避免普通命令承担界面初始化开销。
<<< END U001511 >>>
<<< UNIT U001512 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:101-101 >>>
# 记录失败不阻止界面启动，错误由通知呈现。
<<< END U001512 >>>
<<< UNIT U001513 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:108-108 >>>
# register_existing 仅返回新增记录，已有实例的名称需从注册表读取。
<<< END U001513 >>>
<<< UNIT U001514 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:119-119 >>>
# 首屏必查控件缺失表示页面未完整装配。
<<< END U001514 >>>
<<< UNIT U001515 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:136-136 >>>
# 隐藏页采用惰性加载，因此使用独立应用实例检查模块页的数据读取。
<<< END U001515 >>>
<<< UNIT U001516 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:183-183 >>>
# noqa: BLE001 - 检查失败必须转为非零退出码
<<< END U001516 >>>
<<< UNIT U001517 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:200-200 >>>
# noqa: BLE001 - 检查失败必须转为非零退出码
<<< END U001517 >>>
<<< UNIT U001518 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:205-205 >>>
# run_worker 在下一轮消息循环中注册任务，须等待后再读取页面状态。
<<< END U001518 >>>
<<< UNIT U001519 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:240-240 >>>
# noqa: BLE001 - 未挂载与选择器不存在均按控件缺失处理
<<< END U001519 >>>
<<< UNIT U001520 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:326-326 >>>
# 安装前弹出确认框，焦点位于确认按钮上。
<<< END U001520 >>>
<<< UNIT U001521 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:337-337 >>>
# noqa: BLE001 - 诊断结果需保留异常详情
<<< END U001521 >>>
<<< UNIT U001522 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:386-386 >>>
# 侧栏包含分组标题，高亮下标须按应用的导航位置映射计算。
<<< END U001522 >>>
<<< UNIT U001523 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:400-400 >>>
# noqa: BLE001 - 诊断结果需保留异常详情
<<< END U001523 >>>
<<< UNIT U001524 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:464-464 >>>
# 已完成的 worker 会从 app.workers 移除，须提前保留句柄以读取错误状态。
<<< END U001524 >>>
<<< UNIT U001525 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:469-469 >>>
# noqa: BLE001 - 诊断结果需保留异常详情
<<< END U001525 >>>
<<< UNIT U001526 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:479-479 >>>
# 子进程错误可能包含多行输出，须合并以维持每项诊断一行的格式。
<<< END U001526 >>>
<<< UNIT U001527 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:484-484 >>>
# 单次 pause 只推进一帧，慢速平台上 worker 尚未回写，此时按读数检查会误判为失败。
<<< END U001527 >>>
<<< UNIT U001528 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:539-539 >>>
# noqa: BLE001 - 诊断结果需保留异常详情
<<< END U001528 >>>
<<< UNIT U001529 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:568-568 >>>
# noqa: BLE001 - 诊断结果需保留异常详情
<<< END U001529 >>>
<<< UNIT U001530 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:619-619 >>>
# 未安装且未启用的平台不显示在实例列表中，经安装对话框选择后安装。
<<< END U001530 >>>
<<< UNIT U001531 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:630-630 >>>
# noqa: BLE001 - 诊断结果需保留异常详情
<<< END U001531 >>>
<<< UNIT U001532 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:656-656 >>>
# compat 消息已包含检查项名称，须去除前缀以避免重复输出。
<<< END U001532 >>>
<<< UNIT U001533 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:694-694 >>>
# noqa: BLE001 - 诊断结果需保留解析异常详情
<<< END U001533 >>>
<<< UNIT U001534 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:725-725 >>>
# 缺少可读资源时无法完成检查，须记为未执行。打包产物需包含包数据。
<<< END U001534 >>>
<<< UNIT U001535 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/commands/tui.py:793-793 >>>
# noqa: BLE001 - 诊断结果需保留启动异常详情
<<< END U001535 >>>
<<< UNIT U001536 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/tui.py:1-1 | ctx=<module> >>>
启动交互界面，提供 ``--self-check`` 诊断与 ``--headless`` 无终端检查。
<<< END U001536 >>>
<<< UNIT U001537 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/tui.py:44-44 | ctx=CheckResult.render >>>
返回单行输出文本。
<<< END U001537 >>>
<<< UNIT U001538 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/tui.py:54-54 | ctx=tui >>>
启动 AkariBot 交互界面。
<<< END U001538 >>>
<<< UNIT U001539 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:30-30 >>>
# 纯仓库地址按这些主机名与 .git 后缀判定为 git 直接引用。其余 http(s) 地址按普通直接引用交给 uv。
<<< END U001539 >>>
<<< UNIT U001540 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:69-69 >>>
# 界面按这份清单管理环境，包括已安装的包、属于 AkariBot 的包以及记在实例清单里的项。
<<< END U001540 >>>
<<< UNIT U001541 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:120-120 >>>
# 依赖记录都能解析出包名。无法解析时返回空字符串，调用方据此保留它。
<<< END U001541 >>>
<<< UNIT U001542 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:125-125 >>>
# 改写清单里记录的运行库，返回改写后的列表。
<<< END U001542 >>>
<<< UNIT U001543 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:138-138 >>>
# 补全直接引用，为仓库地址加 ``git+`` 前缀，其他地址与依赖声明原样沿用。
<<< END U001543 >>>
<<< UNIT U001544 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:149-149 >>>
# 把没有版本约束的依赖声明补全为 ``名称==已安装版本``，让清单里的记录可复现。
<<< END U001544 >>>
<<< UNIT U001545 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:168-168 >>>
# 把直接引用规范成可与 ``direct_url`` 比对的形式，去掉 git+ 前缀、片段与末尾斜杠。
<<< END U001545 >>>
<<< UNIT U001546 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:176-176 >>>
# 为直接引用补全包名，安装完成后按 ``direct_url`` 反向查找对应的包。
<<< END U001546 >>>
<<< UNIT U001547 | py-comment | packages/akari-bot-cli/akaribot/cli/commands/venv.py:195-195 >>>
# 把已安装的依赖声明规范化为清单里的记录，尽可能确定包名与版本号。
<<< END U001547 >>>
<<< UNIT U001548 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/venv.py:1-1 | ctx=<module> >>>
实例 venv 托管
<<< END U001548 >>>
<<< UNIT U001549 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/venv.py:53-53 | ctx=status >>>
显示当前模式、解释器路径、环境里的包与清单里记录的运行库。
<<< END U001549 >>>
<<< UNIT U001550 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/venv.py:211-211 | ctx=add >>>
将运行库安装到实例环境。``--save`` 会同时写入实例清单，环境重建时按清单补充安装。
<<< END U001550 >>>
<<< UNIT U001551 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/venv.py:249-249 | ctx=remove >>>
从实例环境卸载运行库。``--save`` 同时删除清单里的记录。
<<< END U001551 >>>
<<< UNIT U001552 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/venv.py:294-294 | ctx=adopt >>>
切换为 CLI 托管 venv，先安装并验证通过，最后才卸载源环境的包。
<<< END U001552 >>>
<<< UNIT U001553 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/venv.py:321-321 | ctx=release >>>
放弃托管，把实例 venv 的包迁移回当前环境。
<<< END U001553 >>>
<<< UNIT U001554 | py-docstring | packages/akari-bot-cli/akaribot/cli/commands/venv.py:345-345 | ctx=recreate >>>
重建实例 venv（Python 升级后修复）。新环境安装并验证通过后才替换旧目录。
<<< END U001554 >>>
<<< UNIT U001555 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/commands.md:1-1 | ctx=命令参考 >>>
# 命令参考
<<< END U001555 >>>
<<< UNIT U001556 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:3-3 | ctx=命令参考 >>>
本文整理了各子命令的用途与选项。
<<< END U001556 >>>
<<< UNIT U001557 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:5-5 | ctx=命令参考 >>>
全局选项写在子命令前。例如：
<<< END U001557 >>>
<<< UNIT U001558 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:12-12 | ctx=命令参考 >>>
`--lang zh_cn|en_us` 只影响本次调用的界面文案，不改变实例默认语言。把它写在子命令后会被当成未知选项。
<<< END U001558 >>>
<<< UNIT U001559 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:14-14 | ctx=命令参考 >>>
需要实例的命令接受 `--instance` / `-I`，查找顺序依次为显式路径、`AKARI_INSTANCE_DIR`、从当前目录向上查找 `akaribot.toml`。找不到实例时命令报错，并提示先初始化或指定实例根目录。
<<< END U001559 >>>
<<< UNIT U001560 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:16-16 | ctx=命令参考 >>>
`--json` 让脚本读取结果。多数命令输出一行 JSON。`docs dev`、`docs serve` 这类长期运行的命令输出事件行。stdout 只输出结果或事件，进度与警告输出到 stderr。
<<< END U001560 >>>
<<< UNIT U001561 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:18-18 | ctx=命令参考 >>>
会删除内容的写操作还接受 `--yes` / `-y`，用来跳过确认。只打印操作计划的命令使用 `--dry-run`，不会写文件，也不会调用安装器。
<<< END U001561 >>>
<<< UNIT U001562 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:22-22 | ctx=init >>>
创建实例目录、写入 `akaribot.toml`、安装 core 与适配器，并生成最小配置。
<<< END U001562 >>>
<<< UNIT U001563 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:28-32 | ctx=init >>>
- `path`：实例目录，默认为当前目录。`--adapter` / `--module` 可重复，默认适配器为 `telegram`。
- `--minimal`：不安装 core extras 与表情资源包。`--extra` 追加 extra，两者互斥。
- `--no-venv`：不由 CLI 管理 venv。`--workspace-root` / `--dev`：从本地源码安装。`--python`：创建 venv 时使用的解释器。
- `--skip-config-sync`：跳过安装后的配置同步。core 的配置模块尚未就绪时使用。
- `--non-interactive` 不提问。还支持 `--offline`、`--dry-run`、`--force`、`--verbose` / `-v`。
<<< END U001563 >>>
<<< UNIT U001564 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:36-36 | ctx=run >>>
启动、停止、重启或查看实例状态。未知参数原样传给 core 的 `run` 命令。
<<< END U001564 >>>
<<< UNIT U001565 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:38-42 | ctx=run >>>
- `-a` / `--adapter`：只启动指定适配器，可重复。
- 默认在前台运行。`-d` / `--detach` 后台启动，等实例取得 `.bot.lock` 后才报告成功。
- `--stop`、`--restart`、`--status` 互斥。`--restart` 等价于停止后后台启动，`--timeout` 为停止时等待退出的秒数，默认 20。
- `--no-auto-migrate`：启动时跳过数据库结构升级。`--foreground` 显式保持前台，与 `--detach` 互斥。
- 后台控制台输出写入 `logs/RunConsole_<日期>.log`，进程号记在 `.bot.lock`。`--status --json` 输出运行状态、锁文件和控制台日志路径。
<<< END U001565 >>>
<<< UNIT U001566 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:46-46 | ctx=service >>>
将 CLI 安装为系统常驻服务，由服务按注册表里的自启与崩溃重启设置守护实例。
<<< END U001566 >>>
<<< UNIT U001567 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:48-51 | ctx=service >>>
- `install [--dry-run] [--force]`：写入并注册服务单元。macOS 写入 launchd 单元，Linux 写入 systemd 用户单元。Windows 没有受支持的后端。
- `uninstall`：注销服务并删除单元文件。
- `status [--json]`：查看是否安装、是否已注册。
- `supervise [--once] [--interval 5] [--max-restarts 5] [--backoff 2]`：守护循环本身，由服务单元调用。默认每 5 秒检查一次，单个实例最多连续重启 5 次，重启间隔从 2 秒起逐次翻倍。`--once` 只运行一轮。
<<< END U001567 >>>
<<< UNIT U001568 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:53-53 | ctx=service >>>
服务恢复实例时同时检查注册表里的自启策略和上次运行状态。只开启崩溃重启、未开启自启的实例不会在开机时被自动启动。
<<< END U001568 >>>
<<< UNIT U001569 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:57-57 | ctx=test >>>
在实例环境里运行 `akaribot.testing`，缺少测试包时提示安装 `akari-bot-testing`。
<<< END U001569 >>>
<<< UNIT U001570 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:59-62 | ctx=test >>>
- `path`：测试文件或目录，省略时运行全部默认根目录。
- `--ci`：非交互模式，跳过需要人工复核的用例，同时设置 `CI=1`。CI 里不会停在 `input()` 等待输入。
- `--coverage`：收集覆盖率。`--case`：只运行名称含该子串的用例，可重复。
- 测试框架不在实例默认依赖中，需要先安装 `akari-bot-testing`。缺少该包时命令会给出安装提示。
<<< END U001570 >>>
<<< UNIT U001571 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:64-64 | ctx=test >>>
测试由 `tester.py` 启动，和实例里的模块共用配置与临时数据目录。运行单个文件时传入包内路径，例如 `packages/akari-bot-core/tests/test_registry.py`。
<<< END U001571 >>>
<<< UNIT U001572 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:68-68 | ctx=module >>>
模块与适配器的安装、卸载、更新与全局加载。
<<< END U001572 >>>
<<< UNIT U001573 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:70-70 | ctx=module >>>
启用分三级，含义各不相同：
<<< END U001573 >>>
<<< UNIT U001574 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:72-74 | ctx=module >>>
- 安装控制代码是否安装到本实例。
- 加载控制它是否参与命令匹配。
- 场景启用控制某个群或频道能否使用，需要在机器人里执行 `~module enable`。
<<< END U001574 >>>
<<< UNIT U001575 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:76-83 | ctx=module >>>
- `list`：列出已安装的模块与适配器。`available [--kind module|adapter]`：列出 registry 里可安装的包，并标出已安装项。`status`：列出各模块的全局加载状态。
- `add <名> [-e <目录>] [--git <地址>] [--ref <引用>] [--subdir <目录>] [--dist <包名>]`：安装模块、适配器或本地源码包。
  - 还支持 `--version`、`--extra`、`--kind`、`--force`、`--offline`、`--dry-run`、`--verbose`。
  - 安装过程是：解析包 → 安装前检查 → 安装 → 补充配置 → 迁移 → 热加载 → 报告。`-e` 用可编辑模式安装本地目录，可以省略包名。
  - 安装前检查用 `uv pip install --dry-run` 生成安装计划，再检查它是否会破坏已安装的包。只调整依赖版本时给出提示并继续。会破坏已安装包或依赖无解时停止。`--force` 跳过这项检查。
- `remove <名> [--cascade] [--force] [--purge-data] [--yes]`：默认保留配置与数据。`--cascade` 连带卸载依赖它的包，先列清单再确认。`--purge-data` 同时删除该包的数据表与配置文件。
- `update [名…] [--all] [--force] [--offline] [--defer-runtime] [--json]`：更新已安装包。工作区模式下等价于按本地源码重新安装。`--defer-runtime` 把数据库迁移留到下次启动。
- `load <名>` / `unload <名>`：只改全局加载状态，不改安装状态和场景启用状态。
<<< END U001575 >>>
<<< UNIT U001576 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:85-85 | ctx=module >>>
`--json` 的 `update` 只在 stdout 输出一行结果，进度与警告输出到 stderr。字段包括 `updated`、`failed`、`skipped`、`reload_pending` 与 `restart_required`。
<<< END U001576 >>>
<<< UNIT U001577 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:89-89 | ctx=config >>>
读取、写入与编辑配置。写入由 core 以原子方式完成，值按模板声明的类型转换。
<<< END U001577 >>>
<<< UNIT U001578 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:91-95 | ctx=config >>>
- `list [--json]`：列出已有配置表。`schema --table <表> [--json]`：字段类型、默认值、注释与是否占位。
- `placeholders [--json]`：统计各表待填的占位符。它只做统计，不阻止启动。
- `get <键> --table <表>`、`set <键> <值> --table <表>`：单项读写。`set` 按模板类型转换布尔、数字与列表，密钥字段自动写入 `_secret` 表。
- `open [--table <表>]`：用 `VISUAL` / `EDITOR` 打开配置文件。`edit`：提示三种编辑方式（表单、原始文本、外部编辑器）。
- 表名以 `list` / `schema` 的输出为准。实例表可能带 `-<实例 ID>` 后缀，基础表名不能直接当作实例表名使用。
<<< END U001578 >>>
<<< UNIT U001579 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:99-99 | ctx=db >>>
浏览实例数据库并按主键写入。表名取自 `db tables` 的 `table` 列。
<<< END U001579 >>>
<<< UNIT U001580 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:101-106 | ctx=db >>>
- `tables [--json]`：列出数据表。
- `rows <表> [--limit 20] [--offset 0] [-f <条件>] [-q <搜索>][--order-by <列[:asc|desc]>] [--no-count]`：分页读取。每页最多 200 条。筛选可以重复，多个条件之间是 AND 关系。`-q` 在所有文本列上做包含匹配，不区分大小写。
- `-f` 的条件形如 `<列><运算符><值>`，支持 `=`、`!=`、`>`、`>=`、`<`、`<=`、`~`（包含）、`!~`（不包含）、`^`（前缀）、`$`（后缀）。`null` 表示空值。
- `--no-count` 不统计总条数，翻页时避免全表扫描。输出里不带总数。
- `set <表> --key <主键> --set <列>=<值>…`：在一次 UPDATE 中写入多列。
- `insert <表> --set <列>=<值>…`、`delete <表> --key <主键> [--yes]`。
<<< END U001580 >>>
<<< UNIT U001581 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:110-110 | ctx=instance >>>
管理本机注册表，不移动实例目录。
<<< END U001581 >>>
<<< UNIT U001582 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:112-117 | ctx=instance >>>
- 注册表默认在 `~/.akaribot/instances.toml`，可用 `AKARIBOT_HOME` 修改目录。
- `list [--json]`：列出本机实例、运行状态与服务设置。
- `add <目录> [--name <名>] [--locale <语言>]`：只记录位置，不创建实例、不安装包。
- `remove <名> [--yes]`：从注册表移除条目，实例目录保留。
- `use <名>`：设为默认实例。在实例目录之外运行界面或命令时，按它选择实例。
- `policy <名> [--autostart|--no-autostart] [--restart-on-crash|--no-restart-on-crash]`：设置服务策略。
<<< END U001582 >>>
<<< UNIT U001583 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:121-121 | ctx=adapter >>>
查看、添加和删除适配器实例。
<<< END U001583 >>>
<<< UNIT U001584 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:123-125 | ctx=adapter >>>
- `list [--json]`：按平台分组列出适配器实例。JSON 里的 `installed_platforms` 还会列出 core 清单中全部已安装的平台，包括还没有实例配置的平台。
- `instance add <平台> [实例 ID]`：生成 `config/bot_<平台>[-<实例 ID>].toml`，`enable` 显式设为 `false`，填写完平台要求的账号信息后再开启。
- `instance remove <平台> [实例 ID] [--dry-run]`：只删除配置文件，场景与用户数据保留。
<<< END U001584 >>>
<<< UNIT U001585 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:127-127 | ctx=adapter >>>
实例 ID 只能使用小写字母、数字和下划线，长度为 1–24 个字符。省略表示默认实例。它是 `target_id` 前缀的一部分，一旦使用不可更改。命令不提供改名。改名要迁移多张表和消息前缀。
<<< END U001585 >>>
<<< UNIT U001586 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:131-131 | ctx=venv >>>
管理实例 venv，可改为由 CLI 管理、改回自行管理或重建。
<<< END U001586 >>>
<<< UNIT U001587 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:133-137 | ctx=venv >>>
- `status`：查看当前模式、解释器路径与已安装包数量。
- `add <依赖声明> [--no-save] [--upgrade]`：安装到实例环境，默认写入实例清单。`--no-save` 只安装不记录，重建时不会自动补充安装。
- `remove <包名> [--no-save]`：卸载，默认同时删除实例清单里的记录。`--no-save` 保留记录。
- `adopt`：改为由 CLI 管理 venv，把当前环境里的包迁移到实例 venv。`release`：改回由你自己管理，把实例 venv 里的包迁移到当前环境。
- `recreate`：重建实例 venv，用于升级 Python 或修复环境。新环境安装并验证通过后才替换旧目录。
<<< END U001587 >>>
<<< UNIT U001588 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:141-141 | ctx=doctor >>>
检查多个实例之间的端口冲突、重复的登录信息，以及没有对应适配器的配置。`--json` 供 CI 读取，`--strict` 把告警按失败处理。这个命令只覆盖这三项。网络、依赖版本和文档工具链分别由运行、安装和文档命令检查。
<<< END U001588 >>>
<<< UNIT U001589 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:145-147 | ctx=new >>>
- `new module <名>`：生成模块包，支持 `--dir`、`--alias`、`--desc`、`--author`、`--license`、`--platform`、`--component`、`--command`、`--config`、`--database`、`--assets`、`--data-dir`、`--tests`、`--non-interactive`、`--add`、`--force`。
- `new adapter <名>`：生成适配器包，支持 `--platform-name`、`--feature`、`--field`、`--credential-field` 等同类选项。生成后默认执行 `akaribot module add -e .`。
- 生成目录下的包名带 `akari-bot-module-` / `akari-bot-adapter-` 前缀。`--add` 默认开启。只想生成文件时传入 `--no-add`。
<<< END U001589 >>>
<<< UNIT U001590 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:151-151 | ctx=docs >>>
收集实例中已安装包的 `docs/`，生成并构建 VitePress 站点。站点配置写在实例根目录的 `docs.toml`。Node.js 与 VitePress 版本由主题清单声明。
<<< END U001590 >>>
<<< UNIT U001591 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:153-160 | ctx=docs >>>
- `list [--query <词>] [--kind <分组>] [--json]`：列出参与构建的包、分类、页面与目录警告。
- `build [--package <key>…] [--all] [--force] [--offline] [--json]`：生成站点并调用 VitePress。不加 `--json` 时，命令实时打印各阶段进度与子进程输出。加 `--json` 时，stdout 只保留结果行，日志写入 stderr。`--package` 可重复或逗号分隔。
- `sync-theme [--repo <路径>] [--json]`：把主题模板 submodule 同步到远端最新提交。只更新工作区，不暂存父仓库 gitlink。
- `install-deps [--json]`：安装主题所需的 Node 依赖，不生成站点。
- `serve [--host 127.0.0.1] [--port 4173] [--open] [--no-build] [--json]`：构建并启动本机静态预览，直到 Ctrl+C。`--json` 先输出 ready 事件行。
- `dev [--host 127.0.0.1] [--port 5173] [--open] [--offline] [--interval 0.6] [--package <key>…] [--json]`：监听文档与主题改动，同步到 `cache/docs/dev` 并运行 VitePress 开发服务器，直到 Ctrl+C。`--json` 输出逐行事件。
- `deploy [--provider vercel|s3] [--dry-run] [--delete] [--yes] [--json]`：把构建产物部署到远端。部署用的密钥只从环境变量读取，`--delete` 只在 S3 下删除目标前缀内多余的对象。
- `status [--json]`：查看工具链、配置、包数与最近一次构建或部署。`clean [--yes]`：删除 `cache/docs`。
<<< END U001591 >>>
<<< UNIT U001592 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:162-162 | ctx=docs >>>
生成结果位于实例根目录的 `cache/docs`，开发模式使用其中的 `cache/docs/dev`，构建与部署记录在 `.docs/state.json`。主题由 `docs.toml` 的 `[theme].source` 选择，外部模板需在根目录提供 `docs-theme.json`。配置与部署字段见 [文档引擎](docs-engine.md)。
<<< END U001592 >>>
<<< UNIT U001593 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:166-166 | ctx=tui >>>
启动终端界面。`--self-check` 在无终端环境下检查资源、样式与页面交互，`--headless` 启动后完成基础读取即退出，`--no-mouse` 关闭鼠标追踪。页面与键位见 [终端界面](tui.md)。
<<< END U001593 >>>
<<< UNIT U001594 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:170-170 | ctx=logs >>>
读取实例 `logs/` 下最新的日志文件。
<<< END U001594 >>>
<<< UNIT U001595 | md-list | packages/akari-bot-cli/akaribot/cli/docs/commands.md:172-175 | ctx=logs >>>
- 日志文件在实例 `logs/` 下，文件名形如 `<进程>[_debug]_<日期>.log`。
- `--process <进程>`：限定进程前缀。`--info` / `--debug`：限定日志级别文件。
- `--lines <N>`：首次输出的末尾行数，默认 50。`--follow`：持续输出新增行，直到 Ctrl+C。
- `--path`：只打印文件路径，便于脚本自行处理。`--json`：输出单行 JSON。
<<< END U001595 >>>
<<< UNIT U001596 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:183-183 | ctx=migrate >>>
旧项目须含 `bot.py`、`core/`、`modules/` 与 `config/config.toml`。迁移只读取旧目录，不改动它，可以重复执行。报告写到新实例根目录的 `migration-report.md`。选项：`--workspace-root` / `--dev`、`--skip-install`、`--no-venv`、`--dry-run`、`--force`、`--offline`、`-v`。
<<< END U001596 >>>
<<< UNIT U001597 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/commands.md:185-185 | ctx=常见操作组合 >>>
## 常见操作组合
<<< END U001597 >>>
<<< UNIT U001598 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/commands.md:187-187 | ctx=创建并启动实例 >>>
### 创建并启动实例
<<< END U001598 >>>
<<< UNIT U001599 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:195-195 | ctx=创建并启动实例 >>>
`init` 结束时会把实例写入注册表。之后在实例目录之外，也可以直接用注册名或 `-I` 指定实例。
<<< END U001599 >>>
<<< UNIT U001600 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/commands.md:197-197 | ctx=安装模块 >>>
### 安装模块
<<< END U001600 >>>
<<< UNIT U001601 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:205-205 | ctx=安装模块 >>>
`add` 只负责安装到实例。`load` 让它参与命令匹配。要让某个群或频道使用，还要在机器人里执行 `~module enable dice`。
<<< END U001601 >>>
<<< UNIT U001602 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/commands.md:207-207 | ctx=配置与检查 >>>
### 配置与检查
<<< END U001602 >>>
<<< UNIT U001603 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:216-216 | ctx=配置与检查 >>>
`config set` 写入后是否立即生效取决于 core。需要重启的项会在命令输出里说明。`doctor` 只检查端口、重复登录信息和孤立配置，不替代完整运行检查。
<<< END U001603 >>>
<<< UNIT U001604 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/commands.md:218-218 | ctx=文档站点 >>>
### 文档站点
<<< END U001604 >>>
<<< UNIT U001605 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:226-226 | ctx=文档站点 >>>
`serve` 会先构建再启动本机预览。只修改文档时用 `docs dev`，它监听文件变化并在另一个端口启动开发服务器。
<<< END U001605 >>>
<<< UNIT U001606 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/commands.md:228-228 | ctx=环境变量 >>>
## 环境变量
<<< END U001606 >>>
<<< UNIT U001607 | md-table | packages/akari-bot-cli/akaribot/cli/docs/commands.md:230-236 | ctx=环境变量 >>>
| 变量 | 作用 |
| --- | --- |
| `AKARI_INSTANCE_DIR` | 未传入 `--instance` 时使用的实例根目录。显式参数优先。 |
| `AKARIBOT_HOME` | 实例注册表所在目录，默认 `~/.akaribot`。 |
| `AKARIBOT_PYTHON` | 非托管模式下启动实例子进程使用的解释器。 |
| `AKARIBOT_CLI_BIN` | 终端界面调用 CLI 时使用的命令。打包产物可据此指向二进制文件。 |
| `VISUAL` / `EDITOR` | `config open` 调用的外部编辑器，按这个顺序选择。 |
<<< END U001607 >>>
<<< UNIT U001608 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/commands.md:238-238 | ctx=环境变量 >>>
`AKARI_CONFIG_PATH` 由 CLI 在启动 core 子进程时注入，一般不需要手动设置。
<<< END U001608 >>>
<<< UNIT U001609 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:1-1 | ctx=文档引擎 >>>
# 文档引擎
<<< END U001609 >>>
<<< UNIT U001610 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:3-3 | ctx=文档引擎 >>>
文档引擎把已安装包的 `docs/` 目录汇总成一个 VitePress 站点，负责读取目录、生成站点源文件、调用 VitePress 构建、提供静态预览与开发预览，并记录构建与部署状态。
<<< END U001610 >>>
<<< UNIT U001611 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:5-5 | ctx=当前状态 >>>
## 当前状态
<<< END U001611 >>>
<<< UNIT U001612 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:7-7 | ctx=当前状态 >>>
引擎实现在 `akaribot/cli/docs_engine/`，包含目录收集、源文件生成、跨包链接转换、构建缓存、静态预览、开发预览与状态持久化。`akaribot docs` 已注册进 `akaribot` 主命令表。命令见下表。
<<< END U001612 >>>
<<< UNIT U001613 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:9-9 | ctx=前置条件 >>>
## 前置条件
<<< END U001613 >>>
<<< UNIT U001614 | md-list | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:11-13 | ctx=前置条件 >>>
- Node.js 与 `npm` 需要在 `PATH` 中。内置主题与外部主题的 Node.js 版本要求在各自的主题清单中声明。
- 内置主题的依赖固定在引擎模板的 `package-lock.json` 里，安装时执行 `npm ci`。外部主题的 `package.json` 由清单的 `dependencies` 生成，安装时执行 `npm install`，VitePress 版本来自清单。
- 首次构建需要联网安装依赖。离线模式要求 `<实例根目录>/cache/docs/node_modules` 已包含主题所需版本。
<<< END U001614 >>>
<<< UNIT U001615 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:15-15 | ctx=前置条件 >>>
Node.js 缺失、版本低于主题要求或 npm 不可用时，构建以工具链错误终止，不会改用其他渲染器。
<<< END U001615 >>>
<<< UNIT U001616 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:17-17 | ctx=命令 >>>
## 命令
<<< END U001616 >>>
<<< UNIT U001617 | md-table | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:19-29 | ctx=命令 >>>
| 命令 | 用途 |
| --- | --- |
| `akaribot docs list` | 列出参与构建的包、分组、标题与页面数，附目录降级警告 |
| `akaribot docs build` | 生成站点源文件并构建，支持只构建指定包、强制重建与离线构建 |
| `akaribot docs sync-theme` | 把主题模板 submodule 同步到远端最新提交，只更新工作区 |
| `akaribot docs install-deps` | 安装主题所需的 Node 依赖，不生成站点 |
| `akaribot docs serve` | 启动本机静态服务器预览构建产物 |
| `akaribot docs dev` | 监听文档与主题改动，在 `cache/docs/dev` 上运行 VitePress 开发服务器 |
| `akaribot docs deploy` | 把构建产物发布到 Vercel 或 S3 |
| `akaribot docs status` | 显示实际主题、最近一次构建的指纹、包清单、输出目录与部署记录 |
| `akaribot docs clean` | 清理生成目录，使下次构建从头开始 |
<<< END U001617 >>>
<<< UNIT U001618 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:31-31 | ctx=命令 >>>
`list` 优先经实例的 core 入口读取包清单。入口不可用时，改用注册表里的已安装包清单，并在警告中说明原因。CLI 自身的文档始终合并进目录。
<<< END U001618 >>>
<<< UNIT U001619 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:33-33 | ctx=命令 >>>
`build`、`serve` 与 `deploy` 都会触发构建。不加 `--json` 时，命令实时打印工具链、生成与 VitePress 三个阶段，并转发 npm 与 VitePress 的逐行输出。
<<< END U001619 >>>
<<< UNIT U001620 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:35-35 | ctx=命令 >>>
加 `--json` 时，stdout 只保留最终结果行，日志写入 stderr。
<<< END U001620 >>>
<<< UNIT U001621 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:37-37 | ctx=命令 >>>
TUI 的文档页在构建期间显示同一份日志，按 `l` 切换面板。`dev` 不加 `--json` 时打印阶段、同步结果与提示，加 `--json` 时输出逐行事件，子进程日志写入 stderr。
<<< END U001621 >>>
<<< UNIT U001622 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:39-39 | ctx=命令 >>>
模块文档在侧栏按 `docs/config/global/docs.global.toml` 的 `category` 分组，条目名称取模块名。
<<< END U001622 >>>
<<< UNIT U001623 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:41-41 | ctx=命令 >>>
包内的标题、简介、分类与品牌插槽写在 `docs/config/global/docs.global.toml`。同一包可以再放置 `docs/config/docs.toml`，按同名键覆盖默认值。
<<< END U001623 >>>
<<< UNIT U001624 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:43-43 | ctx=命令 >>>
两个位置都接受 JSON 文件，文件名分别为 `docs.global.json` 与 `docs.json`。没有 `docs/config/` 时回退到旧的 `docs/doc.toml`，兼容尚未迁移的包。
<<< END U001624 >>>
<<< UNIT U001625 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:46-46 | ctx=命令 >>>
同一模块目录内的页面显示为页内标签，其中 `index.md` 是“使用方法”，`development.md` 是“安装与开发”。开发页不单独出现在侧栏。其余页面按 `order` 与路径排在两者之间。
<<< END U001625 >>>
<<< UNIT U001626 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:48-48 | ctx=命令 >>>
内置 `bundled` 主题没有标签栏，开发页仍作为普通侧栏页面列出。包声明 `overview = false` 时不生成包级概览页，包入口指向第一页，侧栏直接列出页面。页面 front matter 写 `submenu` 时，同值的页面归入该名称的二级分组，普通页面仍平铺在前面。
<<< END U001626 >>>
<<< UNIT U001627 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:50-50 | ctx=命令 >>>
侧栏最前固定显示“首页”。一级分组与模块文档的分类各带一个图标。
<<< END U001627 >>>
<<< UNIT U001628 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:52-52 | ctx=命令 >>>
分组图标写在 `docs.toml` 的 `[icons]` 里，键为分组名或 `home`。
<<< END U001628 >>>
<<< UNIT U001629 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:54-54 | ctx=命令 >>>
分类图标写在 `[category_icons]` 里，键为 `docs/config/global/docs.global.toml` 的 `category`。两处的值都是主题注册的 M3E 图标名。
<<< END U001629 >>>
<<< UNIT U001630 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:56-56 | ctx=配置 >>>
## 配置
<<< END U001630 >>>
<<< UNIT U001631 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:58-58 | ctx=配置 >>>
站点标题、语言、基础路径、输出目录、界面文案、分组标题与图标名由随包分发的 `akaribot/cli/docs/defaults.toml` 提供。实例根目录下的 `docs.toml` 只读不写，按表与键逐项覆盖，未覆盖的键沿用默认值。
<<< END U001631 >>>
<<< UNIT U001632 | md-list | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:137-153 | ctx=配置 >>>
- `site.title`：站点标题，同时用作首页标题与页面描述。留空时取 `defaults.toml` 的 `[site] title`。
- `site.lang`：页面语言标签。留空时取 `defaults.toml` 的 `[site] lang`。
- `site.base`：部署基础路径。留空时取 `defaults.toml` 的 `[site] base`。环境变量 `AKARIBOT_DOCS_BASE` 优先于配置文件，值会被整理成以 `/` 开头、以 `/` 结尾的形式。
- `site.command_prefix`：命令用法行使用的前缀。留空时先读取 `config/global/config.global.toml` 或 `.json`，再由 `config/config.toml` 的 `[config] command_prefix` 覆盖，取最终列表的首项。核心配置缺失或为空时不加前缀。
- `site.locales`：站点语言清单，首项为默认语言，标签形如 `zh-CN`。留空时只有 `site.lang` 一种语言。`site.lang` 与首项不一致时按配置错误终止，未写 `site.lang` 时取首项。清单中的标签要么在 `[locales.<标签>]` 下给出配置，要么已有随包默认值。
- `locales.<标签>`：该语言的显示名称 `label`、站点标题 `title`，以及逐键覆盖界面文案的 `labels`、覆盖分组标题的 `group_titles`。未写的项沿用 `defaults.toml` 与默认语言的值。
- `site.logo` / `site.logo_dark` / `site.avatar` / `site.character` / `site.credits` / `site.favicon`：品牌插槽与站点图标。
  - 相对路径按实例根目录解析。品牌文件复制到 `public/brand-logo.<扩展名>`、`public/brand-logo-dark.<扩展名>`、`public/brand-avatar.<扩展名>`、`public/brand-character.<扩展名>` 与 `public/brand-credits.<扩展名>`，站点图标复制到 `public/site-favicon.<扩展名>`。相对路径必须位于实例根目录内，且指向的文件存在。
  - HTTP(S) URL 与 `/` 开头的站点路径原样使用。品牌插槽的站点路径不带基础路径，主题组件会用 `withBase()` 补上。
  - 品牌插槽按以下顺序取值：
    1. `docs.toml` 的 `[site]` 字段。
    2. 第一个 `brand = true` 的文档包在 `docs/config/global/docs.global.toml` 中声明的同名字段。
    3. 内置资源。
  - 没有 `brand = true` 的包时，回退到第一个声明 `logo` 或 `avatar` 的包。
  - 内置回退为 `logo.png`、`logo-night.png`、`logo.png`、`placeholder.png`。`credits` 没有内置文件时为空。品牌包缺失不会让构建失败。
  - 站点图标取 `[assets] favicon` 指向的随包文件。
- `themeConfig.akari.brand`：生成器输出的品牌插槽，供主题组件读取。
<<< END U001632 >>>
<<< UNIT U001633 | md-table | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:155-161 | ctx=配置 >>>
  | 键 | 内容 |
  | --- | --- |
  | `logo` | 日间标志 |
  | `logoDark` | 夜间标志 |
  | `avatar` | 对话示例头像 |
  | `character` | 角色立绘 |
  | `credits` | 制作人员文本 |
<<< END U001633 >>>
<<< UNIT U001634 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:163-163 | ctx=配置 >>>
  `akari.appBar.logo`、`akari.appBar.logoDark` 与 `akari.chatAvatar` 是兼容字段，分别与 `logo`、`logoDark`、`avatar` 相同。
<<< END U001634 >>>
<<< UNIT U001635 | md-list | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:164-178 | ctx=配置 >>>
- `footer`：页脚关于区块。`title` 是标题，`text` 是说明段落（字符串或字符串数组），`image` 是配图，`links` 是按钮。
  - 未写 `image` 时使用角色立绘。配图复制到 `public/footer-image.<扩展名>`。
  - `links[].icon` 写 `afdian` 或 `github` 时使用主题内置的品牌图形，其他值按品牌插槽的规则解析为图片并复制到 `public/footer-icon-<序号>.<扩展名>`。
  - `text` 与 `links` 写空数组表示不显示该部分。`enabled = false` 时页脚只保留落款。
  - 生成器把区块写入 `themeConfig.akari.footer.about`，随 CLI 分发的页脚组件据此渲染配图、标题、段落与按钮。
  - 页脚按两栏排版：左侧配图，右侧文案与按钮，两栏在文档宽度内居中靠拢，落款居中。视口窄于 840 像素时改为单栏，配图放大且文字居中。
- `labels`：界面文案。`home` 是侧栏首页条目，`overview` 是无页面时的占位标题，`usage` 与 `development` 是平行标签页的名称。`index_intro`、`footer` 与 `generated_header` 是生成内容里的固定语句。
- `group_titles`：侧栏一级分组的标题，键为包分组。
- `icons`：侧栏一级分组的图标名，键取分组（`core`、`builtin`、`cli`、`testing`、`module`、`adapter`、`asset`、`library`）或 `home`。主题只注册了有限的图标集，未注册的名称不会显示图标。
- `category_icons`：侧栏分类的图标名，键取 `docs/config/global/docs.global.toml` 的 `category`。不在表内的分类不显示图标。分类图标与一级分组的图标一样，需要在主题里注册。
- `assets`：随包素材的文件名，目前只有 `favicon`，相对 `akaribot/cli/docs/assets/`。实例可以换成同目录内的其他文件名，或改用 `site.favicon` 指向实例内的文件。
- `build.out_dir`：输出目录，相对路径以实例根目录为基准。留空时取 `defaults.toml` 的 `[site] out_dir`。
- `theme.source`：主题来源。`auto` 在实例根目录查找 `akari-bot-docs-template`、`vendor/akari-bot-docs-template` 或 `docs-theme`。从仓库源码运行 CLI 时还会查找仓库内的 `vendor/akari-bot-docs-template` submodule。找不到时使用 `bundled`。也可写 `bundled`、`file:<路径>` 或实例内的相对路径。环境变量 `AKARIBOT_DOCS_THEME` 优先于配置。
- `theme.color`：主题种子色，格式为 `#rrggbb`，留空使用主题默认值。Akari 主题把它写入 `settings.defaults.color`，访问者仍可在设置面板覆盖。内置 `bundled` 主题注入 `--vp-c-brand-*` 变量。
- `deploy`：部署目标配置，引擎不解释这些字段。
<<< END U001635 >>>
<<< UNIT U001636 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:180-180 | ctx=配置 >>>
内容按语言分目录存放，默认语言读取包文档目录，其他语言读取 `docs/<标签>/`。某个语言缺少页面时，生成器复制默认语言的同名页面，访问者不会遇到空链接。跨包链接、侧栏与导航按语言加 `/<标签>/` 前缀。
<<< END U001636 >>>
<<< UNIT U001637 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:182-182 | ctx=配置 >>>
生成器把默认语言写成 VitePress 的 `locales.root`，其余语言写成独立条目，并为每种语言生成自己的 `themeConfig`。主题的语言切换器据此展示可选语言。
<<< END U001637 >>>
<<< UNIT U001638 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:184-184 | ctx=配置 >>>
`docs.toml` 不是合法的 TOML，或其中某一段不是表时，命令以配置错误终止。
<<< END U001638 >>>
<<< UNIT U001639 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:186-186 | ctx=部署配置 >>>
### 部署配置
<<< END U001639 >>>
<<< UNIT U001640 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:208-208 | ctx=部署配置 >>>
Vercel 的令牌只从环境变量 `VERCEL_TOKEN` 读取。S3 的密钥只从 `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 与可选的 `AWS_SESSION_TOKEN` 读取。区域默认取 `AWS_REGION` 或 `AWS_DEFAULT_REGION`，都没有时使用 `us-east-1`。`provider` 默认按存在的子表推断，两者都存在时取 `vercel`。
<<< END U001640 >>>
<<< UNIT U001641 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:210-210 | ctx=生成物 >>>
## 生成物
<<< END U001641 >>>
<<< UNIT U001642 | md-table | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:212-220 | ctx=生成物 >>>
| 路径 | 内容 |
| --- | --- |
| `cache/docs/src` | 生成的 VitePress 源目录，每次构建前清空 |
| `cache/docs` | Node 工具链与 `node_modules` |
| `cache/docs/site` | 默认站点输出，可用 `build.out_dir` 改写 |
| `cache/docs/dev` | 开发模式使用的 VitePress 源目录，其中 `node_modules` 由同步保留 |
| `cache/docs/.dev-staging` | 开发模式同步用的暂存目录 |
| `cache/docs/.dev.lock` | 开发模式运行锁，记录进程、端口与基础路径 |
| `.docs/state.json` | 构建指纹、包清单与最近 50 条部署记录 |
<<< END U001642 >>>
<<< UNIT U001643 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:222-222 | ctx=生成物 >>>
生成器只接受位于 `cache/docs` 内的目标路径。包 key 必须匹配 `[A-Za-z0-9][A-Za-z0-9._-]*`，文档目录中的符号链接不得指向目录之外。文档目录可以包含 `.md`、常见图片、`.txt` 与 `.pdf`，其他后缀的文件会被忽略。
<<< END U001643 >>>
<<< UNIT U001644 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:224-224 | ctx=首页数据 >>>
### 首页数据
<<< END U001644 >>>
<<< UNIT U001645 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:226-226 | ctx=首页数据 >>>
首页的文案、按钮、统计项、角色入口、主题卡与贡献卡来自 `packages/akari-bot-cli/akaribot/cli/docs/home/home.json`。`schema` 当前为 `1`，字段如下：
<<< END U001645 >>>
<<< UNIT U001646 | md-table | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:228-236 | ctx=首页数据 >>>
| 字段 | 内容 |
| --- | --- |
| `title` / `lead` | 首页标题与说明 |
| `sections` | 界面文案，含搜索框占位、统计区标签、快速开始、主题区与参与贡献的标题 |
| `actions` | 首屏主按钮与文字链接 |
| `stats` | 统计项，`source` 取 `core_version`、`total_pages`、`module_count`、`adapter_count` |
| `roles` | 使用者与开发者入口，含说明和链接 |
| `topics` | 按主题浏览的图片卡 |
| `contribute` | 贡献与翻译卡片 |
<<< END U001646 >>>
<<< UNIT U001647 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:238-238 | ctx=首页数据 >>>
链接写成 `package` + `page`、`group` 或 `url`，生成器会按站点结构转换地址。未识别的字段会被忽略，缺少必填字段或类型不符时按配置错误终止构建。
<<< END U001647 >>>
<<< UNIT U001648 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:240-240 | ctx=构建与缓存 >>>
## 构建与缓存
<<< END U001648 >>>
<<< UNIT U001649 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:242-242 | ctx=构建与缓存 >>>
构建指纹覆盖参与包的版本与标题、每个文档文件的内容、主题清单与主题目录的文件内容、VitePress 版本、站点标题、语言与基础路径。
<<< END U001649 >>>
<<< UNIT U001650 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:244-244 | ctx=构建与缓存 >>>
主题摘要按文件内容计算，包含 `package.json` 与 `package-lock.json`。更新 submodule 或替换主题文件后，构建指纹一定变化。
<<< END U001650 >>>
<<< UNIT U001651 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:246-246 | ctx=构建与缓存 >>>
指纹未变且输出中仍有 `index.html` 时，命令直接复用上次结果。`--force` 忽略指纹，强制重建。
<<< END U001651 >>>
<<< UNIT U001652 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:248-248 | ctx=构建与缓存 >>>
`docs status` 输出实际解析的主题名称、目录与摘要。更新主题后如果构建仍然复用上次结果，先用它确认 CLI 读到的主题目录。如果解析到的是内置模板，而不是预期的位置，调整 `[theme].source`，或把主题放到实例根目录。
<<< END U001652 >>>
<<< UNIT U001653 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:250-250 | ctx=构建与缓存 >>>
构建结束后必须存在 `index.html`，否则按构建失败处理。
<<< END U001653 >>>
<<< UNIT U001654 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:252-252 | ctx=构建与缓存 >>>
站点开启 `cleanUrls`，`a.md` 对应 `/a`，`index.md` 对应 `/<包 key>/`。首页按分组汇总各包，每个分组另有汇总页。
<<< END U001654 >>>
<<< UNIT U001655 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:254-254 | ctx=构建与缓存 >>>
侧栏按包与页面清单生成，页面顺序取自 front matter 的 `order`。相同 `submenu` 的页面在包内组成二级分组。包的 `docs/config/global/docs.global.toml` 写 `overview = false` 时，不生成 `/<包 key>/` 概览页。导航与分组页改为指向第一页，侧栏不再给包标题加链接。
<<< END U001655 >>>
<<< UNIT U001656 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:256-256 | ctx=预览 >>>
## 预览
<<< END U001656 >>>
<<< UNIT U001657 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:258-258 | ctx=预览 >>>
`serve` 使用内置静态服务器，默认只绑定回环地址，端口由调用方指定或交由系统分配。
<<< END U001657 >>>
<<< UNIT U001658 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:260-260 | ctx=预览 >>>
解析规则与 `cleanUrls` 一致，`/foo` 找不到文件时改为返回 `foo.html`。目录请求改为返回 `index.html`。
<<< END U001658 >>>
<<< UNIT U001659 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:262-262 | ctx=预览 >>>
其余请求交给 `404.html`。所有响应一律带 `Cache-Control: no-store`。
<<< END U001659 >>>
<<< UNIT U001660 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:264-264 | ctx=开发模式 >>>
## 开发模式
<<< END U001660 >>>
<<< UNIT U001661 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:266-266 | ctx=开发模式 >>>
`dev` 持续监听参与构建的文档目录、主题目录与站点配置，把改动同步到实例的 `cache/docs/dev`，并在该目录上运行 VitePress 的开发服务器。浏览器端的更新由 Vite 的热更新完成，不经过 VitePress 的构建。
<<< END U001661 >>>
<<< UNIT U001662 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:268-268 | ctx=开发模式 >>>
监听范围与处理方式：
<<< END U001662 >>>
<<< UNIT U001663 | md-table | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:270-275 | ctx=开发模式 >>>
| 目标 | 变化后的处理 |
| --- | --- |
| 参与包的 `docs/` 目录 | 页面增删时重新读取包清单，其余改动只重新生成与同步 |
| 主题目录 | 重新解析主题并同步主题组件 |
| `docs.toml`、`docs-theme.json`、首页组件与站点素材 | 重新读取配置，`site.base` 变化时重启开发服务器 |
| 主题清单的 `dependencies` 或 `install_mode` | 输出提示，需停止开发模式并执行 `install-deps` |
<<< END U001663 >>>
<<< UNIT U001664 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:277-277 | ctx=开发模式 >>>
生成器先写入 `cache/docs/.dev-staging`，再按文件内容比对同步到 `cache/docs/dev`，只写入实际变化的文件。`cache/docs/dev/node_modules` 承载依赖，`.vitepress/cache` 承载 Vite 的预构建产物，两者都在同步范围之外。
<<< END U001664 >>>
<<< UNIT U001665 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:279-279 | ctx=开发模式 >>>
生成器每次清空并重写全部源文件，因此必须差分同步，否则直接改写镜像会让 Vite 在每批改动上全量失效。
<<< END U001665 >>>
<<< UNIT U001666 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:281-281 | ctx=开发模式 >>>
运行行为：
<<< END U001666 >>>
<<< UNIT U001667 | md-list | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:283-288 | ctx=开发模式 >>>
- 变更在 0.6 秒的静默窗口内合并为一批，间隔由 `--interval` 调整。
- `--package` 只监听指定包，其余包仍参与生成与跨包链接转换。
- 默认端口 5173，被占用时改用系统分配的端口。`--port 0` 直接把端口选择交给系统。
- 启动时写入 `cache/docs/.dev.lock`。同一实例上 `dev` 与 `clean`、`install-deps` 互斥，`status` 据此报告开发模式状态。
- 开发服务器与静态预览共用 `cache/docs/node_modules`，二者不能同时运行。在 TUI 中启动其一即停止另一。
- `--json` 输出逐行事件：`stage`、`ready`、`sync`、`warn`、`error`、`stopped`。工具链安装与首次生成发生在 `ready` 之前，`ready` 携带站点地址。
<<< END U001667 >>>
<<< UNIT U001668 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:290-290 | ctx=开发模式 >>>
开发模式不写 `.docs/state.json`，也不改动 `cache/docs/site`。
<<< END U001668 >>>
<<< UNIT U001669 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:292-292 | ctx=部署 >>>
## 部署
<<< END U001669 >>>
<<< UNIT U001670 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:294-294 | ctx=部署 >>>
`deploy` 的目标为 Vercel 与 S3。部署所需的密钥只从环境变量读取，不写入 `docs.toml`，也不进入 `.docs/state.json`。配置文件中只保留仓库、项目、桶与路径这类非敏感信息。
<<< END U001670 >>>
<<< UNIT U001671 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:296-296 | ctx=部署 >>>
每次部署向状态文件追加一条记录，包含目标、结果与时间。
<<< END U001671 >>>
<<< UNIT U001672 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:298-299 | ctx=部署 >>>
仓库自带的 `Builtin Tester` 工作流在 tester 通过后发布文档站，默认分支的推送与手动触发会全量构建
所有包的文档，产物交给 GitHub Pages 发布。拉取请求（PR）与其他分支不发布。
<<< END U001672 >>>
<<< UNIT U001673 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:301-302 | ctx=部署 >>>
构建在临时实例 `.ci-docs` 里进行，
基础路径取 Pages 的项目路径（`AKARIBOT_DOCS_BASE`），站内链接与资源地址因此在构建期就带上该前缀。
<<< END U001673 >>>
<<< UNIT U001674 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:304-304 | ctx=部署 >>>
仓库在 Settings → Pages 的 Source 须为 GitHub Actions。工作流在 Pages 尚未启用时会自动打开它。
<<< END U001674 >>>
<<< UNIT U001675 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:306-306 | ctx=主题 >>>
## 主题
<<< END U001675 >>>
<<< UNIT U001676 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:308-308 | ctx=主题 >>>
引擎只读取主题根目录的 `docs-theme.json`，复制清单声明的 `theme_dir`，按清单生成 VitePress 配置与依赖，不导入主题代码。清单字段：
<<< END U001676 >>>
<<< UNIT U001677 | md-table | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:310-318 | ctx=主题 >>>
| 字段 | 说明 |
| --- | --- |
| `name` / `version` | 主题标识与版本，参与构建指纹 |
| `theme_dir` | 相对主题根目录的主题目录，复制为站点 `.vitepress/theme` |
| `vitepress` | 该主题要求的 VitePress 版本 |
| `node` | Node.js 版本要求，如 `>=x.y.z` |
| `dependencies` | 安装到 `<实例根目录>/cache/docs` 的 npm 依赖 |
| `install_mode` | `ci`（复制主题的 lock）或 `install`（按依赖生成 package.json） |
| `config` | 生成配置所用声明：`appearance`、`clean_urls`、`custom_element_prefixes`、`head_module` / `head_export`、`markdown_module` / `markdown_export`、`theme_config_key`、`search` |
<<< END U001677 >>>
<<< UNIT U001678 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:320-320 | ctx=主题 >>>
页脚不在主题里实现。生成器复制主题目录后，把主题入口 `index.ts` 改名为 `theme-entry.ts`，写入自己的 `index.ts` 与 `footer/` 组件。新的入口套用模板主题，再用 `provideAkariComponents()` 覆盖 `Footer` 插槽。
<<< END U001678 >>>
<<< UNIT U001679 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:322-322 | ctx=主题 >>>
模板仓库保持原样，升级主题不会覆盖页脚改动。主题没有 `composables/useAkariConfig.ts`（即不支持插槽覆盖）时不做这层替换，站点沿用主题自带的页脚。
<<< END U001679 >>>
<<< UNIT U001680 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:324-324 | ctx=主题 >>>
`akari-bot-docs-template` 提供 `vitepress-akari-theme-docs` 主题与 `docs-theme.json`，Node.js 与 VitePress 版本由该文件声明。本仓库用 `vendor/akari-bot-docs-template` submodule 提供该模板，克隆后执行 `git submodule update --init --recursive` 即可。实例也可以把 `theme.source` 指向自己的模板目录。
<<< END U001680 >>>
<<< UNIT U001681 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:326-326 | ctx=主题 >>>
更新主题用 `akaribot docs sync-theme`。它拉取远程最新提交，只更新 submodule 工作区，父仓库的 gitlink 需要自行暂存。
<<< END U001681 >>>
<<< UNIT U001682 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:328-328 | ctx=主题 >>>
主题依赖变化后，用 `akaribot docs install-deps` 重新安装 npm 依赖。
<<< END U001682 >>>
<<< UNIT U001683 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:330-330 | ctx=主题 >>>
内置的 `bundled` 主题是同一约定的最小实现，在没有外部模板时使用它。
<<< END U001683 >>>
<<< UNIT U001684 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:332-332 | ctx=主题组件 >>>
### 主题组件
<<< END U001684 >>>
<<< UNIT U001685 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:334-334 | ctx=主题组件 >>>
外部模板的 `.vitepress/theme` 提供以下全局组件，并适配主题的 M3E 调色板：`ModuleMeta`（模块属性卡）、`ModuleConfig`（配置项）、`ModuleAlias`（模块级别名）、`ModuleData`（数据表）、`NoticeBox`（提示框）、`CommandUsage`（命令用法）、`ChatExample`（命令对话示例）与 `PackageDependencies`（运行依赖）。
<<< END U001685 >>>
<<< UNIT U001686 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:336-336 | ctx=主题组件 >>>
生成器读取包内 `docs/config/global/docs.global.toml` 的 `[[meta.modules]]`，在包首页标题后自动注入 `ModuleMeta`。本仓库的模块页不声明该表，其余组件由文档按需使用，写法见仓库根目录 `docs/package-docs.md`。
<<< END U001686 >>>
<<< UNIT U001687 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:338-338 | ctx=主题组件 >>>
依赖段落用 `<PackageDependencies package="<包 key 或包名>" />`。生成器读取已安装包元数据里的 `Requires-Dist`，过滤掉 `extra` 可选依赖，把结果写入 `themeConfig.akari.dependencies`。组件按包 key 与包名取列表，文档不写版本范围。
<<< END U001687 >>>
<<< UNIT U001688 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:340-340 | ctx=主题组件 >>>
组件只在 VitePress 构建产物中渲染，包内 Markdown 仍可直接阅读。主题目录整体复制到生成的站点，新增主题组件不需要修改生成器。
<<< END U001688 >>>
<<< UNIT U001689 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:342-342 | ctx=主题组件 >>>
内置 `bundled` 主题也提供 `ModuleMeta`、`NoticeBox`、`CommandUsage`、`ChatExample` 与 `PackageDependencies` 的同名组件。它的 `ChatExample` 把图片渲染为缩略图，点击后在新标签页打开，气泡文本按纯文本处理。
<<< END U001689 >>>
<<< UNIT U001690 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:344-344 | ctx=主题组件 >>>
外部模板的 `ChatExample` 行为如下：
<<< END U001690 >>>
<<< UNIT U001691 | md-list | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:346-353 | ctx=主题组件 >>>
- `messages` 中的消息显式设置 `markdown: true` 时按 Markdown 渲染，原始 HTML 不执行。其余消息按纯文本处理。
- 缩略图可以展开成图片预览浮层，浮层上的按钮交互可用。
- 整行只有三个以上波浪号时，渲染为时间分隔线。
- 尾部图片另起气泡，多张尾部图片共用一个气泡。
- 图片地址后的 `{natural}` 表示按原始尺寸展示，超过视口高度时等比缩小。
- `image-width` 用于固定示例内图片宽度。
- `:card` 在对话末尾渲染机器人卡片。
- 按钮项的 `buttons` 可以带二级按钮。`dismiss: true` 删除所属回复组。`:one-shot="true"` 在任一按钮点击后禁用同组按钮。
<<< END U001691 >>>
<<< UNIT U001692 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:355-355 | ctx=主题组件 >>>
`ModuleAlias`、`ModuleConfig`、`ModuleData` 以及 `CommandUsage` 的 `params` 参数清单、`platforms` / `excluded` 平台徽章只在外部模板中提供。
<<< END U001692 >>>
<<< UNIT U001693 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:357-357 | ctx=文档编写约定 >>>
## 文档编写约定
<<< END U001693 >>>
<<< UNIT U001694 | md-list | packages/akari-bot-cli/akaribot/cli/docs/docs-engine.md:359-362 | ctx=文档编写约定 >>>
- 包内文档使用简体中文。面向用户的固定文案仍使用 `I18NContext`，不要为了文档新增其他语言的 locale 文件。
- 页面以一级标题开头，文件名使用小写英文与连字符。图片放在 `docs/` 下随页面一起复制，并同步发布到 `/<包 key>/` 供组件按相对路径引用。
- 站内链接使用 `cleanUrls` 形式（`/包 key/页面`），跨包链接以包 key 开头。
- 页面正文只描述当前行为。变更历史由 git 承担。
<<< END U001694 >>>
<<< UNIT U001695 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/index.md:1-1 | ctx=CLI 与 TUI >>>
# CLI 与 TUI
<<< END U001695 >>>
<<< UNIT U001696 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:3-3 | ctx=CLI 与 TUI >>>
`akaribot` 是 AkariBot 的实例管理工具，提供命令行子命令与终端交互界面（TUI）。它安装在实例的 venv 之外，可以用系统解释器安装，也可以安装为独立工具。实例里的机器人、模块与适配器，由 CLI 通过子进程启动。
<<< END U001696 >>>
<<< UNIT U001697 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:5-5 | ctx=CLI 与 TUI >>>
自搭建实例的完整流程见 [自搭建指南](self-hosting.md)。
<<< END U001697 >>>
<<< UNIT U001698 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/index.md:7-7 | ctx=安装 >>>
## 安装
<<< END U001698 >>>
<<< UNIT U001699 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:9-9 | ctx=安装 >>>
先将 CLI 安装为独立工具，再确认版本。
<<< END U001699 >>>
<<< UNIT U001700 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:16-16 | ctx=安装 >>>
运行需要仓库 `pyproject.toml` 声明的 Python 版本。CLI 不依赖 `akaribot.core`。实例需要的 core、适配器与模块，由 `akaribot init` 安装到实例自己的 venv。
<<< END U001700 >>>
<<< UNIT U001701 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/index.md:18-18 | ctx=实例解析 >>>
## 实例解析
<<< END U001701 >>>
<<< UNIT U001702 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:20-20 | ctx=实例解析 >>>
多数子命令需要一个实例根目录（含 `akaribot.toml` 的目录）。解析顺序固定为：
<<< END U001702 >>>
<<< UNIT U001703 | md-list | packages/akari-bot-cli/akaribot/cli/docs/index.md:22-24 | ctx=实例解析 >>>
1. `--instance` / `-I` 给出的路径。
2. 环境变量 `AKARI_INSTANCE_DIR`。
3. 自当前目录向上查找 `akaribot.toml`。
<<< END U001703 >>>
<<< UNIT U001704 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:26-26 | ctx=实例解析 >>>
如果上面三种方式都找不到实例，命令会报错，并提示先初始化或指定实例根目录。
<<< END U001704 >>>
<<< UNIT U001705 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:28-28 | ctx=实例解析 >>>
直接运行 `akaribot` 或 `akaribot tui` 时例外，三种方式都找不到实例时，界面会改用注册表里的默认实例，也就是未指定实例时要操作的那一个。注册表位于 `~/.akaribot/instances.toml`，由 `akaribot instance` 子命令维护。
<<< END U001705 >>>
<<< UNIT U001706 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/index.md:30-30 | ctx=目录结构 >>>
## 目录结构
<<< END U001706 >>>
<<< UNIT U001707 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:32-32 | ctx=目录结构 >>>
实例根目录下的关键路径：
<<< END U001707 >>>
<<< UNIT U001708 | md-table | packages/akari-bot-cli/akaribot/cli/docs/index.md:34-42 | ctx=目录结构 >>>
| 路径 | 内容 |
| --- | --- |
| `akaribot.toml` | 实例元数据：名、语言、venv、解释器与来源 |
| `config/` | 扁平配置表，`<表名>.toml` |
| `data/` | 模块数据与实例私有资产 |
| `database/` | 默认 SQLite 数据库 |
| `logs/` | 进程日志，文件名形如 `<进程>[_debug]_<日期>.log` |
| `cache/` | 可丢弃的缓存，包括文档站点生成物 |
| `.bot.lock` | 运行锁，记录持锁进程与启动参数 |
<<< END U001708 >>>
<<< UNIT U001709 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/index.md:44-44 | ctx=命令总览 >>>
## 命令总览
<<< END U001709 >>>
<<< UNIT U001710 | md-table | packages/akari-bot-cli/akaribot/cli/docs/index.md:46-63 | ctx=命令总览 >>>
| 子命令 | 用途 |
| --- | --- |
| `init` | 创建实例、写入元数据、安装 core 与适配器 |
| `run` | 前台或后台启动、停止、重启、查看状态 |
| `service` | 安装常驻服务并守护本机实例 |
| `test` | 在实例环境里运行自研测试框架 |
| `module` | 模块与适配器的安装、卸载、更新与全局加载 |
| `config` | 配置表、字段、读写与外部编辑器 |
| `db` | 浏览数据库表与数据项，按主键写入 |
| `instance` | 本机实例列表、默认实例与服务策略 |
| `adapter` | 查看、添加和删除适配器实例 |
| `venv` | 管理实例 venv（接管、交还或重建） |
| `doctor` | 检查端口冲突、重复的登录信息，以及没有对应适配器的配置 |
| `docs` | 汇总已安装包的文档，构建、预览与部署 VitePress 站点 |
| `new` | 生成模块包或适配器包的脚手架 |
| `tui` | 启动交互界面，或执行界面自检 |
| `logs` | 查看、跟随与按级别筛选实例日志 |
| `migrate` | 把旧版布局的项目迁移成新实例 |
<<< END U001710 >>>
<<< UNIT U001711 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:65-65 | ctx=命令总览 >>>
每个子命令的选项见 [命令参考](commands.md)。
<<< END U001711 >>>
<<< UNIT U001712 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/index.md:67-67 | ctx=与 core 的子进程边界 >>>
## 与 core 的子进程边界
<<< END U001712 >>>
<<< UNIT U001713 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:69-69 | ctx=与 core 的子进程边界 >>>
CLI 进程不导入 core。需要 core 参与的读写，一律交给实例的解释器执行：
<<< END U001713 >>>
<<< UNIT U001714 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:75-75 | ctx=与 core 的子进程边界 >>>
CLI 向子进程传入 `AKARI_INSTANCE_DIR` 与 `AKARI_CONFIG_PATH` 两个环境变量，标准输出与退出码由命令层解析。
<<< END U001714 >>>
<<< UNIT U001715 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:77-77 | ctx=与 core 的子进程边界 >>>
读取目录、锁文件与注册表这类本机状态时，CLI 可以直接读取文件。
<<< END U001715 >>>
<<< UNIT U001716 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:79-79 | ctx=与 core 的子进程边界 >>>
涉及配置结构、模块清单、数据库或环境检查的判断，则交给子进程完成。
<<< END U001716 >>>
<<< UNIT U001717 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:81-81 | ctx=与 core 的子进程边界 >>>
用 Nuitka 打包后，`sys.executable` 指向二进制自身，CLI 因此不用它启动实例进程。非托管模式下要用的解释器由 `system_python()` 解析，可以用 `AKARIBOT_PYTHON` 覆盖。
<<< END U001717 >>>
<<< UNIT U001718 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/index.md:83-83 | ctx=界面与命令的关系 >>>
## 界面与命令的关系
<<< END U001718 >>>
<<< UNIT U001719 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:85-85 | ctx=界面与命令的关系 >>>
直接运行 `akaribot`（可交互终端）或 `akaribot tui` 进入界面。界面的写操作同样交给 `akaribot <子命令>` 子进程执行，不重复实现命令层的校验与确认逻辑。详情见 [终端界面](tui.md)。
<<< END U001719 >>>
<<< UNIT U001720 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/index.md:87-87 | ctx=本地化 >>>
## 本地化
<<< END U001720 >>>
<<< UNIT U001721 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/index.md:89-89 | ctx=本地化 >>>
界面文案由 CLI 自带的语言文件提供，`--lang zh_cn` / `--lang en_us` 指定本次调用的语言。实例的默认语言在 `akaribot init --locale` 时写入元数据，`--lang` 只影响本次调用。
<<< END U001721 >>>
<<< UNIT U001722 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:1-1 | ctx=自搭建指南 >>>
# 自搭建指南
<<< END U001722 >>>
<<< UNIT U001723 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:3-3 | ctx=自搭建指南 >>>
搭建自己的小可，需要一台能运行 Python 的机器，以及一个准备接入的平台账号。
<<< END U001723 >>>
<<< UNIT U001724 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:5-5 | ctx=自搭建指南 >>>
这份指南以终端界面（TUI）为主。安装完成后，创建实例、填写配置、安装适配器、启动与停止以及查看日志都可以在界面里完成，不需要记命令。命令行只用于安装，以及自动化、无头服务器等场景。
<<< END U001724 >>>
<<< UNIT U001725 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:7-7 | ctx=先认识几个部分 >>>
## 先认识几个部分
<<< END U001725 >>>
<<< UNIT U001726 | md-list | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:9-13 | ctx=先认识几个部分 >>>
- **命令行工具（CLI）**：`akaribot` 命令和 TUI。它安装在实例之外，负责创建、启动和检查实例。
- **实例**：一个独立目录，保存配置、数据库、日志、缓存和实例自己的 Python 环境。
- **core**：机器人的运行时。
- **适配器**：连接具体平台，例如 Telegram、QQ、Discord 或 Web。
- **模块**：提供命令和功能，例如查询、订阅、小游戏。
<<< END U001726 >>>
<<< UNIT U001727 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:15-15 | ctx=先认识几个部分 >>>
CLI 通过 core 的子进程入口读写实例。实例可以单独升级，CLI 的环境依赖与实例隔离。
<<< END U001727 >>>
<<< UNIT U001728 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:17-17 | ctx=准备环境 >>>
## 准备环境
<<< END U001728 >>>
<<< UNIT U001729 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:19-19 | ctx=准备环境 >>>
需要：
<<< END U001729 >>>
<<< UNIT U001730 | md-list | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:21-23 | ctx=准备环境 >>>
- Python。具体版本范围见仓库根目录 `pyproject.toml` 的 `requires-python`。
- [uv](https://docs.astral.sh/uv/)，用于创建实例环境并安装包。
- 只在本地构建文档站点时需要 Node.js 和 `npm`。版本要求由主题的 `docs-theme.json` 声明。
<<< END U001730 >>>
<<< UNIT U001731 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:25-25 | ctx=准备环境 >>>
默认数据库是 SQLite，连接字符串为 `sqlite://database/save.db`。需要 MySQL 时，把密钥表中的 `db_path` 换成 MySQL 连接字符串。core 默认安装的依赖已经包含 MySQL 驱动。
<<< END U001731 >>>
<<< UNIT U001732 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:27-27 | ctx=安装 CLI >>>
## 安装 CLI
<<< END U001732 >>>
<<< UNIT U001733 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:29-29 | ctx=安装 CLI >>>
把 CLI 安装为独立工具，不要安装到实例环境。
<<< END U001733 >>>
<<< UNIT U001734 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:36-36 | ctx=安装 CLI >>>
这是整份指南里唯一需要手动输入的命令。安装完成后，后面的操作都在 TUI 里完成。
<<< END U001734 >>>
<<< UNIT U001735 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:38-38 | ctx=安装 CLI >>>
如果从仓库源码使用，在仓库根目录执行：
<<< END U001735 >>>
<<< UNIT U001736 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:45-45 | ctx=安装 CLI >>>
后面的 `akaribot` 换成 `.venv/bin/akaribot` 即可。
<<< END U001736 >>>
<<< UNIT U001737 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:47-47 | ctx=打开 TUI >>>
## 打开 TUI
<<< END U001737 >>>
<<< UNIT U001738 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:53-53 | ctx=打开 TUI >>>
不带子命令运行时，只要终端支持交互，就会进入界面。也可以显式执行 `akaribot tui`。
<<< END U001738 >>>
<<< UNIT U001739 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:55-55 | ctx=打开 TUI >>>
界面打开后会进入概览页。如果当前目录没有实例，右侧实例列表是空的，按 `n` 新建一个。
<<< END U001739 >>>
<<< UNIT U001740 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:57-57 | ctx=新建实例 >>>
### 新建实例
<<< END U001740 >>>
<<< UNIT U001741 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:59-59 | ctx=新建实例 >>>
在概览页按 `n`，选择“新建实例”，填写：
<<< END U001741 >>>
<<< UNIT U001742 | md-table | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:61-64 | ctx=新建实例 >>>
| 字段 | 说明 |
| --- | --- |
| 实例目录 | 实例保存位置，例如 `/srv/akaribot`。目录不存在时由界面创建。 |
| 运行环境 | 推荐使用“由框架管理的 venv”，由实例自己管理 Python 环境。 |
<<< END U001742 >>>
<<< UNIT U001743 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:66-66 | ctx=新建实例 >>>
实例语言跟随当前界面语言。确认后，界面会调用 `akaribot init` 创建目录、建立虚拟环境、安装 core 和默认适配器，并应用数据库迁移。完成后，概览页会出现这个实例，界面也会切换到它。
<<< END U001743 >>>
<<< UNIT U001744 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:68-68 | ctx=新建实例 >>>
默认会安装 Telegram 适配器。想从创建时就安装别的适配器，见文末“高阶：命令行”。
<<< END U001744 >>>
<<< UNIT U001745 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:70-70 | ctx=填写核心配置 >>>
## 填写核心配置
<<< END U001745 >>>
<<< UNIT U001746 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:72-72 | ctx=填写核心配置 >>>
进入“配置”页，先选 `config` 表，再按 `f` 打开表单。
<<< END U001746 >>>
<<< UNIT U001747 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:74-74 | ctx=填写核心配置 >>>
需要先填的通常是：
<<< END U001747 >>>
<<< UNIT U001748 | md-list | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:76-78 | ctx=填写核心配置 >>>
- `base_superuser`：你的发送者 ID。默认值来自上游维护者，自建实例要换成自己的账号，或者清空。
- `db_path`：默认 SQLite 够用，通常无需修改。
- `proxy`、`ffmpeg_path` 等：没有对应环境时留空。
<<< END U001748 >>>
<<< UNIT U001749 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:80-80 | ctx=填写核心配置 >>>
`secret` 表存放令牌和密钥。表单会把待填项排在前面，`Enter` 进入下一项，`Ctrl+S` 保存。保存前，界面会提示还没有写入的占位符。
<<< END U001749 >>>
<<< UNIT U001750 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:82-82 | ctx=填写核心配置 >>>
不想用表单时，按 `t` 切换到原始文本，或按 `o` 用外部编辑器打开。保存后如果提示重新加载，按页面提示操作。
<<< END U001750 >>>
<<< UNIT U001751 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:84-84 | ctx=创建适配器实例 >>>
## 创建适配器实例
<<< END U001751 >>>
<<< UNIT U001752 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:86-86 | ctx=创建适配器实例 >>>
默认的 Telegram 适配器已经安装，但还没有实例。进入“适配器”页：
<<< END U001752 >>>
<<< UNIT U001753 | md-list | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:88-92 | ctx=创建适配器实例 >>>
1. 按 `n` 新建实例。
2. 选择 Telegram。
3. 填写一个实例 ID，例如 `main`。这个字段必填。
4. 在配置表单里填写 Bot Token。
5. 将 `enable` 设为开启，按 `Ctrl+S` 保存。
<<< END U001753 >>>
<<< UNIT U001754 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:94-94 | ctx=创建适配器实例 >>>
实例 ID 只能使用小写字母、数字和下划线，长度 1 到 24。实例配置写在 `config/bot_telegram-main.toml` 这样的文件里。
<<< END U001754 >>>
<<< UNIT U001755 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:96-96 | ctx=创建适配器实例 >>>
需要 Web、Discord 或别的平台时：
<<< END U001755 >>>
<<< UNIT U001756 | md-list | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:98-99 | ctx=创建适配器实例 >>>
1. 在“适配器”页按 `i`，选择要安装的平台。
2. 安装完成后按 `n`，按上面的步骤创建实例、填写配置、开启。
<<< END U001756 >>>
<<< UNIT U001757 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:101-101 | ctx=创建适配器实例 >>>
平台账号、Token 和回调地址的申请方式见各适配器的文档，入口在“适配器”页或左侧文档分类里。
<<< END U001757 >>>
<<< UNIT U001758 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:103-103 | ctx=启动机器人 >>>
## 启动机器人
<<< END U001758 >>>
<<< UNIT U001759 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:105-105 | ctx=启动机器人 >>>
进入“运行”页，按 `s` 启动当前实例。启动前会弹出确认框，确认后界面在后台启动进程，状态会自动刷新。
<<< END U001759 >>>
<<< UNIT U001760 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:107-107 | ctx=启动机器人 >>>
启动后，在群里或私聊里向机器人发送一条命令，例如：
<<< END U001760 >>>
<<< UNIT U001761 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:113-113 | ctx=启动机器人 >>>
能看到回复，说明适配器和机器人已经接通。
<<< END U001761 >>>
<<< UNIT U001762 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:115-115 | ctx=启动机器人 >>>
停止按 `x`，重启按 `Ctrl+R`。退出 TUI 后，机器人仍在后台运行。
<<< END U001762 >>>
<<< UNIT U001763 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:117-117 | ctx=安装模块 >>>
## 安装模块
<<< END U001763 >>>
<<< UNIT U001764 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:119-119 | ctx=安装模块 >>>
进入“模块”页，按 `i` 安装需要的模块，选择目标后确认。安装完成只是把代码放入实例。
<<< END U001764 >>>
<<< UNIT U001765 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:121-121 | ctx=安装模块 >>>
模块要在实例里全局加载，才会参与命令匹配。选中模块后按 `e` 切换加载状态。
<<< END U001765 >>>
<<< UNIT U001766 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:123-123 | ctx=安装模块 >>>
某个群或频道是否能用这个模块，还要单独开启。在聊天里执行：
<<< END U001766 >>>
<<< UNIT U001767 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:129-129 | ctx=安装模块 >>>
安装只把代码放入实例。全局加载后，命令才会参与匹配。场景启用后，群里才能使用。
<<< END U001767 >>>
<<< UNIT U001768 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:131-131 | ctx=设置常驻服务 >>>
## 设置常驻服务
<<< END U001768 >>>
<<< UNIT U001769 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:133-133 | ctx=设置常驻服务 >>>
确认机器人能正常启动后，回到“概览”页，按 `m` 打开服务与策略菜单：
<<< END U001769 >>>
<<< UNIT U001770 | md-list | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:135-137 | ctx=设置常驻服务 >>>
- 开启开机自启。
- 开启崩溃后自动重启。
- 安装系统服务，让实例在退出 TUI 后继续运行。
<<< END U001770 >>>
<<< UNIT U001771 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:139-139 | ctx=设置常驻服务 >>>
Windows 不支持服务安装。需要开机启动时，用任务计划程序或容器编排工具代替系统服务。
<<< END U001771 >>>
<<< UNIT U001772 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:141-141 | ctx=设置常驻服务 >>>
服务恢复实例时要同时满足开机自启已开启且实例上次处于运行状态两个条件。
<<< END U001772 >>>
<<< UNIT U001773 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:143-143 | ctx=更新与备份 >>>
## 更新与备份
<<< END U001773 >>>
<<< UNIT U001774 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:145-145 | ctx=更新 >>>
### 更新
<<< END U001774 >>>
<<< UNIT U001775 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:147-147 | ctx=更新 >>>
在“模块”页按 `r` 刷新，再按 `U` 更新已安装的包，包括 core、适配器和模块。更新后界面会尝试重新加载。需要重启才能生效的改动，到“运行”页按 `Ctrl+R`。
<<< END U001775 >>>
<<< UNIT U001776 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:149-149 | ctx=更新 >>>
更新前先备份配置、数据和数据库。更新失败时先查看“日志”页的错误，再判断是否回退。
<<< END U001776 >>>
<<< UNIT U001777 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:151-151 | ctx=备份 >>>
### 备份
<<< END U001777 >>>
<<< UNIT U001778 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:153-153 | ctx=备份 >>>
需要备份的内容：
<<< END U001778 >>>
<<< UNIT U001779 | md-table | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:155-161 | ctx=备份 >>>
| 路径 | 内容 |
| --- | --- |
| `akaribot.toml` | 实例元数据。 |
| `config/` | 配置表与密钥。 |
| `data/` | 模块数据与实例私有数据。 |
| `database/` | SQLite 数据库。 |
| `assets/private/` | 实例私有资源。 |
<<< END U001779 >>>
<<< UNIT U001780 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:163-163 | ctx=备份 >>>
`cache/`、`logs/` 和 `.venv/` 可以不备份。恢复时把上面的目录放回实例根目录，再启动实例。
<<< END U001780 >>>
<<< UNIT U001781 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:165-165 | ctx=排查问题 >>>
## 排查问题
<<< END U001781 >>>
<<< UNIT U001782 | md-list | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:167-170 | ctx=排查问题 >>>
- “诊断”页：检查端口冲突、重复的登录信息、没有对应适配器的配置。
- “日志”页：按 `m` 切换日志文件，按 `/` 过滤关键词。
- “配置”页：确认适配器的 `enable` 已开启，Token 没有多余空格。
- “运行”页：确认进程状态，必要时停止后重新启动。
<<< END U001782 >>>
<<< UNIT U001783 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:172-172 | ctx=排查问题 >>>
如果启动时提示配置表不存在，先在“适配器”或“模块”页重新安装对应包，让安装流程补充配置，再检查配置目录。
<<< END U001783 >>>
<<< UNIT U001784 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:174-174 | ctx=TUI 常用键位 >>>
## TUI 常用键位
<<< END U001784 >>>
<<< UNIT U001785 | md-table | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:176-185 | ctx=TUI 常用键位 >>>
| 键 | 作用 |
| --- | --- |
| `q` / `Ctrl+Q` | 退出界面。 |
| `?` | 查看当前页与全局键位。 |
| `Ctrl+←` / `Ctrl+→` | 上一页 / 下一页。 |
| `↑` / `↓` / `Enter` | 选择并打开。 |
| `←` / `→` | 收起 / 展开侧栏分组。 |
| `r` | 刷新当前页。 |
| `Ctrl+S` | 保存当前编辑内容。 |
| `Esc` | 返回或取消当前操作。 |
<<< END U001785 >>>
<<< UNIT U001786 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:187-187 | ctx=TUI 常用键位 >>>
各页的完整键位见 [终端界面](tui.md)。
<<< END U001786 >>>
<<< UNIT U001787 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:189-189 | ctx=高阶：命令行 >>>
## 高阶：命令行
<<< END U001787 >>>
<<< UNIT U001788 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:191-191 | ctx=高阶：命令行 >>>
TUI 覆盖日常操作。下面这些命令适合自动化、批量部署和无头服务器场景。
<<< END U001788 >>>
<<< UNIT U001789 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:193-193 | ctx=高阶：命令行 >>>
创建实例时指定适配器或模块：
<<< END U001789 >>>
<<< UNIT U001790 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:200-200 | ctx=高阶：命令行 >>>
后台运行与服务：
<<< END U001790 >>>
<<< UNIT U001791 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:208-208 | ctx=高阶：命令行 >>>
配置与模块：
<<< END U001791 >>>
<<< UNIT U001792 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:217-217 | ctx=高阶：命令行 >>>
实例与诊断：
<<< END U001792 >>>
<<< UNIT U001793 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:225-225 | ctx=高阶：命令行 >>>
在容器里运行时，实例目录挂载到容器内，用 CLI 启动。容器内没有可用的 TUI。具体参数见 [命令参考](commands.md)。
<<< END U001793 >>>
<<< UNIT U001794 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:227-227 | ctx=相关文档 >>>
## 相关文档
<<< END U001794 >>>
<<< UNIT U001795 | md-list | packages/akari-bot-cli/akaribot/cli/docs/self-hosting.md:229-233 | ctx=相关文档 >>>
- [命令参考](commands.md)：所有子命令与选项。
- [配置](../../../../akari-bot-core/akaribot/core/docs/config.md)：配置表、密钥与默认层。
- [适配器开发](../../../../akari-bot-core/akaribot/core/docs/adapter-development.md)：写一个新的平台适配器。
- [模块开发](../../../../akari-bot-core/akaribot/core/docs/module-development.md)：从第一个模块开始。
- [常见问题](../../../../akari-bot-core/akaribot/core/docs/faq.md)：启动、权限和平台相关的常见问题。
<<< END U001795 >>>
<<< UNIT U001796 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:1-1 | ctx=终端界面 >>>
# 终端界面
<<< END U001796 >>>
<<< UNIT U001797 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:3-3 | ctx=终端界面 >>>
终端界面负责实例的日常运维，涵盖启动与停止、模块与适配器、配置、数据库、日志、环境、文档和旧项目迁移。
<<< END U001797 >>>
<<< UNIT U001798 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:5-5 | ctx=终端界面 >>>
终端界面（TUI）用 Textual 实现，负责实例的日常运维：
<<< END U001798 >>>
<<< UNIT U001799 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:7-14 | ctx=终端界面 >>>
- 启动与停止
- 模块安装
- 配置编辑
- 数据库浏览
- 日志跟踪
- 环境管理
- 文档浏览与发布
- 旧项目迁移
<<< END U001799 >>>
<<< UNIT U001800 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:16-16 | ctx=终端界面 >>>
所有写操作都由 CLI 子进程完成，参数与确认只在命令层实现。对应的命令见 [命令参考](commands.md)。
<<< END U001800 >>>
<<< UNIT U001801 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:18-18 | ctx=启动 >>>
## 启动
<<< END U001801 >>>
<<< UNIT U001802 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:26-26 | ctx=启动 >>>
不带子命令运行 `akaribot` 时，只有在可交互终端下才会进入界面。管道、重定向与 CI 环境改为打印帮助，并以退出码 2 结束。没有实例时先询问是否就地初始化，初始化由 `akaribot init` 命令完成。
<<< END U001802 >>>
<<< UNIT U001803 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:28-28 | ctx=启动 >>>
启动时把当前实例写入注册表。若当前目录不属于任何实例，而目录下只有一个实例，则使用该实例并切换过去。当前目录下有多个实例时只提示，不擅自选择。标题栏显示当前管理的实例名。
<<< END U001803 >>>
<<< UNIT U001804 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:30-30 | ctx=启动 >>>
`--self-check` 在无终端环境下检查资源、样式表与页面交互。`--headless` 启动界面，完成基础读取后退出。两者都用于部署后的基本功能检查，未执行的检查按失败处理。两者只读取实例信息，不修改注册表。
<<< END U001804 >>>
<<< UNIT U001805 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:32-32 | ctx=页面 >>>
## 页面
<<< END U001805 >>>
<<< UNIT U001806 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:34-34 | ctx=页面 >>>
侧栏页面分为四组。`Ctrl+←` / `Ctrl+→` 按同一顺序翻页，折叠分组内的页面同样可达：
<<< END U001806 >>>
<<< UNIT U001807 | md-table | packages/akari-bot-cli/akaribot/cli/docs/tui.md:36-49 | ctx=页面 >>>
| 分组 | 页面 | 用途 |
| --- | --- | --- |
| 概览与运行 | 概览 | 实例与服务状态、实例清单、初始化摘要 |
| | 运行 | 前台/后台启动与停止、按适配器启动、状态轮询 |
| | 日志 | 日志文件筛选、暂停与增量跟踪 |
| | 诊断 | 端口冲突、重复的登录信息、没有对应适配器的配置 |
| 配置与平台 | 配置 | 配置表的表单与原始文本两种模式 |
| | 适配器 | 适配器实例的启动与停止、安装、添加与删除 |
| | 模块 | 模块安装、卸载、更新与全局加载 |
| 环境与数据 | 环境 | 解释器、已安装包与运行库清单 |
| | 数据库 | 表清单、分页浏览与按主键编辑 |
| 开发与迁移 | 开发 | 工作区包清单、运行测试、生成脚手架 |
| | 文档 | 已安装包的文档浏览、构建、开发预览、预览与部署 |
| | 迁移 | 旧项目迁移与试运行 |
<<< END U001807 >>>
<<< UNIT U001808 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:51-51 | ctx=页面 >>>
切换页面时焦点交给目标页，隐藏页停止轮询。页面未激活前不读取数据。
<<< END U001808 >>>
<<< UNIT U001809 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:53-53 | ctx=全局键位 >>>
## 全局键位
<<< END U001809 >>>
<<< UNIT U001810 | md-table | packages/akari-bot-cli/akaribot/cli/docs/tui.md:55-62 | ctx=全局键位 >>>
| 键 | 动作 |
| --- | --- |
| `q` / `Ctrl+Q` | 退出 |
| `?` | 当前页与全局键位帮助 |
| `Ctrl+T` | 深色/浅色主题切换 |
| `Ctrl+←` / `Ctrl+→` | 上一页 / 下一页 |
| `↑` / `↓` / `Enter` | 选择页面并打开。在分组标题上按 `Enter` 或单击切换折叠 |
| `←` / `→` | 折叠所在分组 / 展开高亮的分组 |
<<< END U001810 >>>
<<< UNIT U001811 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:64-64 | ctx=全局键位 >>>
折叠分组内的页面不显示，方向键跳过。当前页位于折叠分组内时，侧栏高亮该分组标题。折叠状态只在本次运行内保留。
<<< END U001811 >>>
<<< UNIT U001812 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:66-66 | ctx=全局键位 >>>
页脚只显示高频快捷键，低频动作放在 `?` 帮助与页内按钮中，在 80 列终端下不溢出。
<<< END U001812 >>>
<<< UNIT U001813 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:68-68 | ctx=页面键位 >>>
## 页面键位
<<< END U001813 >>>
<<< UNIT U001814 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:70-84 | ctx=页面键位 >>>
- 概览：`r` 刷新，`Enter` 切换实例，`n` 添加实例（新建或选择目录），`Ctrl+D` 从注册表移除，`m` 服务与策略（开机自启、崩溃重启、安装或卸载服务）。
- 运行：`s` 启动，`x` 停止，`Ctrl+R` 重启，`r` 刷新，`m` 更多（按适配器启动、前台运行命令）。
- 日志：`space` 暂停跟踪，`c` 清空显示缓冲，`/` 过滤，`m` 日志级别，`r` 刷新，`Esc` 清空过滤。
- 诊断：`r` 刷新，`Enter` 打开冲突详情。
- 配置：`Ctrl+S` 保存，`o` 外部编辑器，`f` 表单模式，`t` 原始文本，`r` 刷新，`Esc` 返回表清单。
- 适配器：`r` 刷新，`i` 安装适配器，`e` 启用/停用实例，`n` 新增实例，`Ctrl+D` 移除实例。
  - 列表只显示已安装或已启用的适配器。未安装的平台，要先按 `i` 打开安装对话框选择。
  - 新增实例时，在对话框中选择已安装的适配器并填写实例 ID。`↑` / `↓` 切换平台，`Enter` 创建。
  - 创建后弹出配置表单，待填写项排在最前。`Enter` 进入下一项，`Ctrl+S` 保存，`Esc` 稍后填写。
- 模块：`r` 刷新，`/` 搜索，`i` 安装（先确认目标），`u` 卸载，`U` 更新，`e` 全局加载/卸载，`space` 选择，`Shift+↑/↓` 扩展选择，`a` 全选，`c` 清除选择，`Esc` 清空搜索。
- 环境：`r` 刷新，`/` 搜索，`i` 安装运行库，`u` 卸载，`m` 解释器菜单（接管 venv、取消接管、重建 venv，只列当前模式可用的项），`Esc` 清空搜索。
- 数据库：`r` 刷新，`Ctrl+S` 保存，`n` 新建，`Ctrl+D` 删除，`/` 搜索，`f` 添加筛选，`Ctrl+F` 清空筛选，`m` 更多（排序、清空筛选），`[` / `]` 翻页，`g` / `G` 跳转首页和末页。
- 开发：`r` 刷新，`t` 运行测试，`n` 新建包对话框，`o` 聚焦输出，`Esc` 终止运行中的操作。
- 文档：`r` 刷新，`/` 搜索，`space` 选择，`b` 构建，`p` 启动或停止预览，`e` 启动或停止开发预览，`o` 打开浏览器，`m` 更多（部署、同步主题、安装依赖、任务日志），`a` 全选，`c` 清空选择。
- 迁移：`Enter` 迁移，`p` 试运行。
<<< END U001814 >>>
<<< UNIT U001815 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:86-86 | ctx=页面键位 >>>
各页按钮文字后附快捷键（如“保存 ^s”），写法与页脚一致。低频操作在 `m` 菜单中，菜单只列当前可用的项。
<<< END U001815 >>>
<<< UNIT U001816 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:88-88 | ctx=页面操作 >>>
## 页面操作
<<< END U001816 >>>
<<< UNIT U001817 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:90-90 | ctx=概览 >>>
### 概览
<<< END U001817 >>>
<<< UNIT U001818 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:92-92 | ctx=概览 >>>
概览页显示本机实例清单、当前实例的启动准备状态与服务策略。实例清单来自注册表，运行状态来自锁文件。
<<< END U001818 >>>
<<< UNIT U001819 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:94-99 | ctx=概览 >>>
- 每行显示注册名、运行状态、位置和启动策略。当前实例用 `▸` 标出。当前实例未写入注册表时也会出现在列表里。
- `Enter` 切换实例。已写入注册表的实例会同时通过 `instance use` 保存为默认实例。未写入注册表的实例只在当前会话使用。
- `n` 打开添加实例菜单。新建实例会调用 `akaribot init`，可以选择托管 venv 或使用当前环境。把已有目录加入注册表时只写入注册表。
- `Ctrl+D` 从注册表移除当前条目，实例目录保留。
- `m` 打开服务与策略菜单：开机自启、崩溃重启、安装或卸载服务。平台不支持服务时，菜单不显示安装项。
- 服务恢复实例时要求同时满足开机自启已开启且实例上次处于运行状态两个条件。
<<< END U001819 >>>
<<< UNIT U001820 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:101-101 | ctx=运行与日志 >>>
### 运行与日志
<<< END U001820 >>>
<<< UNIT U001821 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:103-103 | ctx=运行与日志 >>>
运行页的启动、停止、重启都先确认。启动指定适配器、前台运行等低频操作放在 `m` 菜单。
<<< END U001821 >>>
<<< UNIT U001822 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:105-105 | ctx=运行与日志 >>>
状态查询在后台执行，同类请求只保留最新一次。实例进程独立于界面运行。退出界面后实例继续运行。
<<< END U001822 >>>
<<< UNIT U001823 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:107-107 | ctx=运行与日志 >>>
日志页按实例 `logs/` 下的最新文件跟踪：
<<< END U001823 >>>
<<< UNIT U001824 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:109-112 | ctx=运行与日志 >>>
- `space` 暂停或恢复跟踪，`c` 清空当前显示缓冲。
- `/` 输入关键词过滤，`Esc` 清空过滤。
- `m` 选择自动跟随、INFO 文件或 debug 文件。
- 日志解析规则由 `akaribot logs` 提供，界面直接复用。
<<< END U001824 >>>
<<< UNIT U001825 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:114-114 | ctx=配置、适配器与模块 >>>
### 配置、适配器与模块
<<< END U001825 >>>
<<< UNIT U001826 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:116-116 | ctx=配置、适配器与模块 >>>
配置页有表单、原始文本和外部编辑器三种方式。表单按 `config schema` 生成，只列当前表声明的字段。保存前会标记未写入的占位符。切换表、切换模式或离开页面前，有未保存内容会先确认。
<<< END U001826 >>>
<<< UNIT U001827 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:118-118 | ctx=配置、适配器与模块 >>>
适配器页：
<<< END U001827 >>>
<<< UNIT U001828 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:120-123 | ctx=配置、适配器与模块 >>>
- 列表只显示已安装或已启用的平台。未安装的平台先按 `i` 选择安装。
- `n` 新建实例。对话框只列已安装平台，实例 ID 必填，非法字符和重名会当场提示。
- 创建后弹出配置表单，待填写项排在最前，`enable` 排在最后。这样密钥先写入，再打开实例。
- `e` 启用或停用实例。`Ctrl+D` 只删除实例配置，保留场景和用户数据。
<<< END U001828 >>>
<<< UNIT U001829 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:125-125 | ctx=配置、适配器与模块 >>>
模块页：
<<< END U001829 >>>
<<< UNIT U001830 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:127-130 | ctx=配置、适配器与模块 >>>
- `space` 选择、`Shift+↑/↓` 扩展选择、`a` 全选、`c` 清除选择。普通点击单选，`Ctrl+点击` 切换。
- `i` 安装、`u` 卸载、`U` 更新，`e` 切换全局加载。安装和卸载前会列出目标。
- 批量卸载时逐项执行，单项失败不终止其余项。结束后汇总成功与失败。清理数据的卸载要求输入确认文字或目标数量。
- 安装、加载、场景启用是三件事。安装把代码安装到实例，加载让模块参与命令匹配，场景启用控制某个群或频道能否使用。
<<< END U001830 >>>
<<< UNIT U001831 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:132-132 | ctx=环境与数据库 >>>
### 环境与数据库
<<< END U001831 >>>
<<< UNIT U001832 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:134-134 | ctx=环境与数据库 >>>
环境页管理实例解释器和运行库：
<<< END U001832 >>>
<<< UNIT U001833 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:136-139 | ctx=环境与数据库 >>>
- `i` 安装 PyPI 包、版本范围、仓库地址或 `git+` 引用，可选择是否写入实例清单。
- `u` 卸载并选择是否保留清单记录。选中包会显示反向依赖。
- `m` 打开解释器菜单：接管 venv、取消接管、重建 venv。重建前要求输入“重建”，未写入清单的额外包不会自动恢复。
- 实例运行期间可以安装或卸载运行库，但已加载的模块要重启后才更新。
<<< END U001833 >>>
<<< UNIT U001834 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:141-141 | ctx=环境与数据库 >>>
数据库页只接受 core 注册的表和列：
<<< END U001834 >>>
<<< UNIT U001835 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:143-145 | ctx=环境与数据库 >>>
- `f` 添加筛选条件，支持 `=`、`!=`、`>`、`>=`、`<`、`<=`、`~`、`!~`、`^`、`$`。多条条件按 AND 组合。
- `m` 设置排序。`[` / `]` 翻页，`g` / `G` 跳转首页和末页。每页最多 50 条。
- `Ctrl+S` 保存、`n` 新建、`Ctrl+D` 删除。同一行的多列修改合并成一次更新，任一列非法则不写入。
<<< END U001835 >>>
<<< UNIT U001836 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:147-147 | ctx=开发、文档与迁移 >>>
### 开发、文档与迁移
<<< END U001836 >>>
<<< UNIT U001837 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:149-149 | ctx=开发、文档与迁移 >>>
开发页显示工作区路径、包来源和可编辑安装状态。`t` 运行测试，`n` 新建包。输出区保留完整日志，`o` 聚焦，`Esc` 终止正在运行的操作。
<<< END U001837 >>>
<<< UNIT U001838 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:151-151 | ctx=开发、文档与迁移 >>>
文档页：
<<< END U001838 >>>
<<< UNIT U001839 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:153-155 | ctx=开发、文档与迁移 >>>
- `b` 构建，`p` 启动或停止静态预览，`e` 启动或停止开发预览，`o` 打开浏览器。
- `m` 菜单中包含部署、同步主题、安装依赖和任务日志。
- 静态预览与开发预览共用 `cache/docs/node_modules`，同时只能运行一个。离开页面时后台停止。
<<< END U001839 >>>
<<< UNIT U001840 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:157-157 | ctx=开发、文档与迁移 >>>
迁移页先选择旧项目目录，再显示参数和确认框。`p` 对最近一次源目录重新试运行。试运行只读旧目录，执行阶段才写入当前实例。
<<< END U001840 >>>
<<< UNIT U001841 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:159-159 | ctx=数据刷新与后台任务 >>>
## 数据刷新与后台任务
<<< END U001841 >>>
<<< UNIT U001842 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:161-161 | ctx=数据刷新与后台任务 >>>
页面首次显示时才读取数据，之后由 `r` 手动刷新或操作完成触发。模块清单默认缓存 30 秒，搜索、缩放和重绘不启动子进程。
<<< END U001842 >>>
<<< UNIT U001843 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:163-163 | ctx=数据刷新与后台任务 >>>
安装、更新、构建和迁移在后台执行，进度写在页内输出区。页面卸载后返回的结果会被丢弃，不会更新已经不存在的控件。
<<< END U001843 >>>
<<< UNIT U001844 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:165-165 | ctx=数据刷新与后台任务 >>>
退出界面时如果有未保存内容或后台任务，会先列出影响范围，再询问是否退出。
<<< END U001844 >>>
<<< UNIT U001845 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:167-167 | ctx=确认规则 >>>
## 确认规则
<<< END U001845 >>>
<<< UNIT U001846 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:169-169 | ctx=确认规则 >>>
删除、移除与清理数据的操作使用 `Ctrl+<字母>` 或专用字母键，卸载用 `u`。这些操作执行前一律弹出模态框，框内写明目标与影响范围：
<<< END U001846 >>>
<<< UNIT U001847 | md-list | packages/akari-bot-cli/akaribot/cli/docs/tui.md:171-175 | ctx=确认规则 >>>
- 删除数据项、移除适配器实例、移除实例记录、卸载模块都先确认。批量卸载要求输入目标数量。
- “卸载并清理数据”要求输入确认文字，框内列出将删除的配置文件与数据表。
- 重建 venv 要求输入“重建”，并说明未写入清单的额外运行库需重新安装。
- 旧项目迁移先给出试运行选项，确认框列出将传给 CLI 的参数。
- 存在未保存更改或后台任务未结束时，退出与切换实例都会先确认。
<<< END U001847 >>>
<<< UNIT U001848 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:177-177 | ctx=确认规则 >>>
确认框打开前先调用 `PendingConfirm.accept(key)` 做防抖，同一目标在防抖窗口内的连发会被忽略，避免重复弹出多层模态框。切换页面、刷新、更换表或更换选中项时，调用页面的 `reset_pending()` 作废待确认状态。
<<< END U001848 >>>
<<< UNIT U001849 | md-heading | packages/akari-bot-cli/akaribot/cli/docs/tui.md:179-179 | ctx=与 CLI 的写操作关系 >>>
## 与 CLI 的写操作关系
<<< END U001849 >>>
<<< UNIT U001850 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:181-181 | ctx=与 CLI 的写操作关系 >>>
界面的写操作统一通过 `akaribot <子命令>` 子进程执行。用 Nuitka 打包时直接调用二进制文件。参数与确认的逻辑只在命令层实现一份。需要让命令层自动确认时传入 `--yes`。子进程环境注入 `AKARI_INSTANCE_DIR` 和 `AKARI_CONFIG_PATH`，输出统一按 UTF-8 解析。
<<< END U001850 >>>
<<< UNIT U001851 | md-paragraph | packages/akari-bot-cli/akaribot/cli/docs/tui.md:183-183 | ctx=与 CLI 的写操作关系 >>>
读操作允许在进程内完成，但限于注册表、锁文件、日志文件等本机状态。日志页与 `akaribot logs` 共用 `akaribot/cli/logs.py` 的解析与增量读取规则。配置结构、模块清单、数据库与环境检查结果都通过子进程读取。
<<< END U001851 >>>
