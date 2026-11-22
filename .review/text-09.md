# 全仓可读文本审核稿 · 第 09 册 / 共 20 册

覆盖 U006498–U007035，45 个文件、538 个单元、31,936 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md` | 30 | U006498–U006527 | 3,655 |
| `packages/akari-bot-core/akaribot/core/builtins/parser/hooks/__init__.py` | 1 | U006528–U006528 | 24 |
| `packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py` | 10 | U006529–U006538 | 317 |
| `packages/akari-bot-core/akaribot/core/builtins/parser/hooks/dispatch.py` | 6 | U006539–U006544 | 170 |
| `packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py` | 8 | U006545–U006552 | 289 |
| `packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py` | 8 | U006553–U006560 | 273 |
| `packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py` | 23 | U006561–U006583 | 564 |
| `packages/akari-bot-core/akaribot/core/builtins/parser/hooks/results.py` | 7 | U006584–U006590 | 168 |
| `packages/akari-bot-core/akaribot/core/builtins/parser/message.py` | 87 | U006591–U006677 | 3,796 |
| `packages/akari-bot-core/akaribot/core/builtins/session/context.py` | 22 | U006678–U006699 | 1,772 |
| `packages/akari-bot-core/akaribot/core/builtins/session/features.py` | 5 | U006700–U006704 | 138 |
| `packages/akari-bot-core/akaribot/core/builtins/session/info.py` | 37 | U006705–U006741 | 1,741 |
| `packages/akari-bot-core/akaribot/core/builtins/session/internal.py` | 60 | U006742–U006801 | 3,014 |
| `packages/akari-bot-core/akaribot/core/builtins/session/lock.py` | 23 | U006802–U006824 | 1,223 |
| `packages/akari-bot-core/akaribot/core/builtins/session/tasks.py` | 32 | U006825–U006856 | 1,750 |
| `packages/akari-bot-core/akaribot/core/builtins/session/terms.py` | 3 | U006857–U006859 | 100 |
| `packages/akari-bot-core/akaribot/core/builtins/temp/__init__.py` | 3 | U006860–U006862 | 178 |
| `packages/akari-bot-core/akaribot/core/builtins/types/__init__.py` | 3 | U006863–U006865 | 74 |
| `packages/akari-bot-core/akaribot/core/builtins/utils/__init__.py` | 5 | U006866–U006870 | 154 |
| `packages/akari-bot-core/akaribot/core/client/init.py` | 5 | U006871–U006875 | 211 |
| `packages/akari-bot-core/akaribot/core/component.py` | 6 | U006876–U006881 | 2,102 |
| `packages/akari-bot-core/akaribot/core/config/__init__.py` | 1 | U006882–U006882 | 40 |
| `packages/akari-bot-core/akaribot/core/config/base.py` | 4 | U006883–U006886 | 157 |
| `packages/akari-bot-core/akaribot/core/config/core.py` | 12 | U006887–U006898 | 183 |
| `packages/akari-bot-core/akaribot/core/config/jobqueue.py` | 3 | U006899–U006901 | 89 |
| `packages/akari-bot-core/akaribot/core/config/migration.py` | 6 | U006902–U006907 | 427 |
| `packages/akari-bot-core/akaribot/core/config/network.py` | 2 | U006908–U006909 | 62 |
| `packages/akari-bot-core/akaribot/core/config/s3.py` | 1 | U006910–U006910 | 14 |
| `packages/akari-bot-core/akaribot/core/config/webrender.py` | 1 | U006911–U006911 | 15 |
| `packages/akari-bot-core/akaribot/core/constants/__init__.py` | 1 | U006912–U006912 | 37 |
| `packages/akari-bot-core/akaribot/core/constants/exceptions.py` | 1 | U006913–U006913 | 19 |
| `packages/akari-bot-core/akaribot/core/constants/info.py` | 12 | U006914–U006925 | 990 |
| `packages/akari-bot-core/akaribot/core/constants/path.py` | 11 | U006926–U006936 | 839 |
| `packages/akari-bot-core/akaribot/core/database/__init__.py` | 11 | U006937–U006947 | 767 |
| `packages/akari-bot-core/akaribot/core/database/base.py` | 2 | U006948–U006949 | 212 |
| `packages/akari-bot-core/akaribot/core/database/compat.py` | 3 | U006950–U006952 | 89 |
| `packages/akari-bot-core/akaribot/core/database/legacy.py` | 22 | U006953–U006974 | 1,906 |
| `packages/akari-bot-core/akaribot/core/database/link.py` | 5 | U006975–U006979 | 479 |
| `packages/akari-bot-core/akaribot/core/database/migration.py` | 36 | U006980–U007015 | 2,909 |
| `packages/akari-bot-core/akaribot/core/database/migrations/0001_initial.py` | 1 | U007016–U007016 | 31 |
| `packages/akari-bot-core/akaribot/core/database/migrations/0002_banned_users_and_nullable_sender.py` | 4 | U007017–U007020 | 116 |
| `packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py` | 12 | U007021–U007032 | 641 |
| `packages/akari-bot-core/akaribot/core/database/migrations/0005_rebuild_job_queues.py` | 1 | U007033–U007033 | 88 |
| `packages/akari-bot-core/akaribot/core/database/migrations/0006_push_priority.py` | 1 | U007034–U007034 | 99 |
| `packages/akari-bot-core/akaribot/core/database/migrations/__init__.py` | 1 | U007035–U007035 | 14 |

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
<<< UNIT U006498 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:1-1 | ctx=Parser 入口 Hook API >>>
# Parser 入口 Hook API
<<< END U006498 >>>
<<< UNIT U006499 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:3-3 | ctx=Parser 入口 Hook API >>>
模块通过 `@module.hook(point=...)` 订阅 parser 阶段。带名称的能力（`.hook("name")`）也由同一套订阅执行机制负责。
<<< END U006499 >>>
<<< UNIT U006500 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:5-5 | ctx=具名 Module Hook >>>
## 带名称的 Module Hook
<<< END U006500 >>>
<<< UNIT U006501 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:7-8 | ctx=具名 Module Hook >>>
带名称的 hook 通过 `Bot.Hook.trigger("module.name", session_info=..., args=...)` 调用。
它与 parser hook 共享模块启用状态、平台过滤、runtime generation、超时和取消收尾：
<<< END U006501 >>>
<<< UNIT U006502 | md-list | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:10-13 | ctx=具名 Module Hook >>>
- `module.name`：执行指定能力，返回最后一个成功回调的返回值。异常直接传播给调用方。
- `module`：按优先级执行该模块全部未指定 `point` 的带名称 hook。单个回调失败会记录并继续，返回值不向广播调用方汇总。
- 带名称的 hook 默认执行预算为 5 秒，可在 `@module.hook(..., timeout=...)` 覆盖。传 `timeout<=0` 表示不限时。
- 带名称的 hook 的 `available_for` / `exclude_from` 会基于传入的 `session_info` 检查。没有会话时只执行全平台订阅。
<<< END U006502 >>>
<<< UNIT U006503 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:15-15 | ctx=具名 Module Hook >>>
测试和计划任务 mock 也调用同一分发入口，不应直接获取 `ModulesManager.modules_hooks` 并调用函数。
<<< END U006503 >>>
<<< UNIT U006504 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:17-17 | ctx=快速开始 >>>
## 快速开始
<<< END U006504 >>>
<<< UNIT U006505 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:39-39 | ctx=入口一览 >>>
## 入口一览
<<< END U006505 >>>
<<< UNIT U006506 | md-table | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:41-61 | ctx=入口一览 >>>
| HookPoint | 时机 | 典型用途 |
| --- | --- | --- |
| `SESSION_READY` | 会话刷新后、等待任务前 | 入站过滤、补充 tmp，可写入 SessionDraft |
| `SESSION_BEFORE_WAIT` | 入站策略后、等待任务投递前 | 调整等待任务路由 |
| `MESSAGE_NORMALIZED` | 消息文本规范化后、前缀判断前 | 自定义别名等触发文本改写 |
| `COMMAND_PREPARE` | 命令候选后、模块权限前 | 冷却、ToS 临封，可写入 SessionDraft |
| `COMMAND_BEFORE_PARSE` | 模块策略后、模板解析前 | ToS 计数，可写入 SessionDraft |
| `COMMAND_BEFORE_EXECUTE` | 模板解析后、命令函数调用前 | 命令权限与平台策略 |
| `COMMAND_ROUTE` | 命令解析后、通道认领前 | 命令路由与迁移策略 |
| `COMMAND_UNMATCHED` | 未找到模块/模板 | 纠错建议，可写入 SessionDraft |
| `REGEX_ROUTE` | 消息规范化后、正则候选遍历前 | 正则禁用前缀、禁止发言与运行中提醒 |
| `REGEX_CANDIDATE` | 每个正则模块匹配前 | 模块级正则路由 |
| `CHANNEL_CLAIM` | 候选策略通过后、通道认领前 | 通道避让策略 |
| `REGEX_PREPARE` | 正则匹配并完成循环去重后 | regex 临封与权限 |
| `REGEX_BEFORE_EXECUTE` | regex 冷却后、获取锁前 | regex 计数 |
| `EXECUTION_FINISHED` | 命令/正则函数执行结束 | 统计观察 |
| `EXECUTION_ERROR` | 可分类异常 | AbuseWarning 处理 |
| `FINISHED` | parser finally 清理后 | 消息级计数 |
| `OUTGOING_BEFORE_SEND` | 安全检查后、平台发送前 | 消息转换、机器人被禁止发言时拦截主动发言，可修改 `ctx.outgoing.chain` |
| `OUTGOING_SENT` | 平台返回成功 | 观察 |
| `OUTGOING_FAILED` | 平台发送失败 | 观察 |
<<< END U006506 >>>
<<< UNIT U006507 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:63-63 | ctx=结果类型 >>>
## 结果类型
<<< END U006507 >>>
<<< UNIT U006508 | md-list | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:65-69 | ctx=结果类型 >>>
- `Continue()`（或 `None`）：继续
- `RewriteTrigger(trigger_msg)`：提交新的触发文本并继续同入口的后续 hook
- `Stop(message=..., scope=CANDIDATE|MESSAGE)`：业务拒绝。出站入口表示取消发送
- `RecoveryProposal(trigger_msg, command_first_word, display)`：恢复建议
- `Handled()`：错误入口已处理（观察入口禁止）
<<< END U006508 >>>
<<< UNIT U006509 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:71-71 | ctx=结果类型 >>>
非法返回值按失败隔离，不会中断后续 hook。
<<< END U006509 >>>
<<< UNIT U006510 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:75-75 | ctx=SessionDraft >>>
`SESSION_DRAFT_POINTS` 上每个 hook 获得独立草稿。成功才 `commit()`，失败或超时执行 `revoke()`。
<<< END U006510 >>>
<<< UNIT U006511 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:77-77 | ctx=SessionDraft >>>
可写字段包括 `tmp` / `prefixes` / `messages` / `bot_name` / `muted` / `locale_lang`。
<<< END U006511 >>>
<<< UNIT U006512 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:79-81 | ctx=SessionDraft >>>
`locale_lang` 写入时必须是非空、非空白字符串。`None`、空字符串等无效值会抛出 `SessionDraftError`，
不会标记字段变更。未修改语言且原会话未设定语言时，读取仍可返回 `None`。
`ctx.session_info` 的容器返回独立副本，Union ORM 及关联对象只允许读取属性，禁止调用其方法。
<<< END U006512 >>>
<<< UNIT U006513 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:90-90 | ctx=SessionDraft >>>
身份、权限、ORM、执行锁不在草稿内。
<<< END U006513 >>>
<<< UNIT U006514 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:92-92 | ctx=出站 >>>
## 出站
<<< END U006514 >>>
<<< UNIT U006515 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:94-94 | ctx=出站 >>>
`before_send` 通过 `ctx.outgoing` 改写 `chain` / `quote`。递归 send 跳过嵌套改写。`sent`/`failed` 只观察，不改写原结果。
<<< END U006515 >>>
<<< UNIT U006516 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:96-96 | ctx=出站 >>>
结果观察中的 `chain` 是改写后经过滤、平台转换与安全检查的实际发送内容，`message_ids` 来自平台返回值。
<<< END U006516 >>>
<<< UNIT U006517 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:98-98 | ctx=出站 >>>
构建快照或运行观察者失败只记录日志，不影响已发送消息的返回结果，也不遮蔽原始发送异常。外部取消与进程退出仍传播。
<<< END U006517 >>>
<<< UNIT U006518 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:100-100 | ctx=出站 >>>
`send_direct_message()` 的 `submit` 成功仅表示队列接受投递，因此不发布 `OUTGOING_SENT`。投递本身失败时发布 `OUTGOING_FAILED`。
<<< END U006518 >>>
<<< UNIT U006519 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:102-102 | ctx=执行契约 >>>
## 执行规则
<<< END U006519 >>>
<<< UNIT U006520 | md-list | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:104-111 | ctx=执行契约 >>>
- 串行。优先级升序 → 模块名 → 订阅 ID
- 单 hook 异常 / 超时 / SessionFinished 等协议异常：丢弃并继续
- 外部 `CancelledError` / `SystemExit` / `KeyboardInterrupt` 传播
- 模块 `_db_load` / `load` 为假时不执行
- 订阅绑定到构建时的 module generation。热重载后旧版本回调跳过
- `timeout` 默认 5s，可按订阅覆盖。`<=0` 不限时
- `available_for` / `exclude_from` 语义同 command
- 无订阅时 parser 不扫描模块
<<< END U006520 >>>
<<< UNIT U006521 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:113-113 | ctx=故障边界 >>>
## 故障边界
<<< END U006521 >>>
<<< UNIT U006522 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:115-115 | ctx=故障边界 >>>
hook 不得：
<<< END U006522 >>>
<<< UNIT U006523 | md-list | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:117-119 | ctx=故障边界 >>>
- 使用 `msg.finish()` 或抛出 `SessionFinished` 表达业务拒绝（请用 `Stop`）
- 在观察入口忽略原异常或改写执行结果
- 依赖对 SessionInfo 身份字段的写入（可写字段必须经 `SessionDraft` 提交）
<<< END U006523 >>>
<<< UNIT U006524 | md-heading | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:121-121 | ctx=内置订阅方 >>>
## 内置订阅方
<<< END U006524 >>>
<<< UNIT U006525 | md-list | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:123-128 | ctx=内置订阅方 >>>
- `akaribot/modules/core/hooks/policies.py`：入站、冷却、权限、正则路由、机器人被禁止发言时拦截出站消息、默认命令反馈
- `akaribot/modules/core/hooks/errors.py`：异常反馈与错误详情格式化
- `akaribot/modules/core/hooks/retired.py`：退役客户端路由和通道避让
- `akaribot/modules/core/admin_tools/alias.py`：自定义别名改写
- `akaribot/modules/core/hooks/routing.py`：同通道消息认领
- `akaribot/modules/core/hooks/tos.py`：临封、令牌桶、上报。四个强制检查不限时，检查故障时按消息级 `Stop` 处理，
<<< END U006525 >>>
<<< UNIT U006526 | md-paragraph | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:129-129 | ctx=内置订阅方 >>>
  避免失败放行。带名称的能力 `tos.check_temp_ban` / `tos.remove_temp_ban` / `tos.report`
<<< END U006526 >>>
<<< UNIT U006527 | md-list | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/README.md:130-131 | ctx=内置订阅方 >>>
- `akaribot/modules/core/hooks/telemetry.py`：AnalyticsData 与 Info 计数
- `akaribot/modules/core/hooks/typo.py`：纠错 RecoveryProposal
<<< END U006527 >>>
<<< UNIT U006528 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/__init__.py:1-1 | ctx=<module> >>>
Parser / 出站入口 hook 公共导出。
<<< END U006528 >>>
<<< UNIT U006529 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:51-51 >>>
# 这些值对象允许在独立副本上使用翻译/消息 API。复制失败必须拒绝读取，不能回退到源引用。
<<< END U006529 >>>
<<< UNIT U006530 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:119-119 >>>
# 其他带 copy 的元素级对象按自身语义复制。失败则拒绝快照，避免共享引用
<<< END U006530 >>>
<<< UNIT U006531 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:129-129 >>>
# 提交时再断开一次引用，防止成功 hook 继续持有草稿链后，之后的就地修改污染正式结果
<<< END U006531 >>>
<<< UNIT U006532 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:140-140 >>>
# 结果类型作为上下文能力暴露，内置模块无需为简单控制流重复导入。
<<< END U006532 >>>
<<< UNIT U006533 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:173-173 >>>
# 深拷贝解析结果，防止 hook 对嵌套列表/字典的就地修改写回原解析结果
<<< END U006533 >>>
<<< UNIT U006534 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:1-1 | ctx=<module> >>>
Parser / 出站入口 hook 的上下文对象。
<<< END U006534 >>>
<<< UNIT U006535 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:72-72 | ctx=SessionInfoView >>>
SessionInfo 的只读视图，阻止就地写入身份与可变容器。
<<< END U006535 >>>
<<< UNIT U006536 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:99-99 | ctx=OutgoingPayload >>>
出站 before_send 的可变载荷。
<<< END U006536 >>>
<<< UNIT U006537 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:138-138 | ctx=ParserHookContext >>>
入口订阅执行时的受控上下文。
<<< END U006537 >>>
<<< UNIT U006538 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/context.py:159-159 | ctx=ParserHookContext.session_info >>>
只读视图。可写字段请用 ``draft``。
<<< END U006538 >>>
<<< UNIT U006539 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/dispatch.py:22-22 >>>
# 出站递归防护，在 before_send 内再 send 时跳过嵌套 before_send 改写
<<< END U006539 >>>
<<< UNIT U006540 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/dispatch.py:24-24 >>>
# 结果观察递归防护
<<< END U006540 >>>
<<< UNIT U006541 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/dispatch.py:1-1 | ctx=<module> >>>
parser / 出站内部使用的入口分发便捷函数。
<<< END U006541 >>>
<<< UNIT U006542 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/dispatch.py:63-63 | ctx=dispatch_outgoing_before_send >>>
出站改写。返回 Stop 表示取消本次发送。
<<< END U006542 >>>
<<< UNIT U006543 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/dispatch.py:86-86 | ctx=dispatch_outgoing_result >>>
隔离快照与观察失败，保留实际发送结果。取消与进程退出仍向外传播。
<<< END U006543 >>>
<<< UNIT U006544 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/dispatch.py:106-106 | ctx=reset_parser_hook_executor >>>
供测试使用，丢弃单例以便替换 ModulesManager。
<<< END U006544 >>>
<<< UNIT U006545 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py:56-56 >>>
# Locale 实际字段是 locale（不是 lang）
<<< END U006545 >>>
<<< UNIT U006546 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py:87-87 >>>
# ---- 可写容器，就地修改在 commit 时统一快照 ----
<<< END U006546 >>>
<<< UNIT U006547 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py:215-216 >>>
# Locale 对象也先构造，与字段校验同属“准备”阶段。构造失败则整次提交不发布，
# 避免其余字段已写回而 locale 静默降级造成的部分提交。
<<< END U006547 >>>
<<< UNIT U006548 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py:219-219 >>>
# 通过生成接口以保留术语作用域。新建 Locale 会让本会话之后的渲染回退到基础术语。
<<< END U006548 >>>
<<< UNIT U006549 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py:1-1 | ctx=<module> >>>
SessionInfo 会话草稿，允许入口 hook 修改有限字段，成功才提交。
<<< END U006549 >>>
<<< UNIT U006550 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py:15-15 | ctx=SessionDraftError >>>
草稿使用错误（重复提交、已撤销、非法字段）。
<<< END U006550 >>>
<<< UNIT U006551 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py:33-33 | ctx=SessionDraft >>>
从已提交 SessionInfo 构建的独立草稿。
<<< END U006551 >>>
<<< UNIT U006552 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/draft.py:64-64 | ctx=SessionDraft.session_info >>>
只读视图。正式对象请勿经此写入。
<<< END U006552 >>>
<<< UNIT U006553 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py:44-44 >>>
# 同一会话发生嵌套分发且父 hook 仍在执行时，子 dispatch 直接跳过，避免子事务提交后父失败无法撤销
<<< END U006553 >>>
<<< UNIT U006554 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py:47-47 >>>
# 观察入口禁止控制结果中断后续执行
<<< END U006554 >>>
<<< UNIT U006555 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py:57-57 >>>
# 每入口允许的结果类型。未列出的入口允许全部
<<< END U006555 >>>
<<< UNIT U006556 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py:164-164 >>>
# 父 hook 尚未结束时拒绝同会话的嵌套分发，因为子事务的提交无法随父失败撤销。
<<< END U006556 >>>
<<< UNIT U006557 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py:180-180 >>>
# 前序 hook 等待期间可能停用或重载后续订阅方。调用前必须按最新状态复核。
<<< END U006557 >>>
<<< UNIT U006558 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py:190-190 >>>
# 快照构建也在 hook 边界内，克隆失败按当前 hook 失败处理，不得中断后续 hook
<<< END U006558 >>>
<<< UNIT U006559 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py:250-250 >>>
# 观察入口将控制结果视为失败，不中断后续执行
<<< END U006559 >>>
<<< UNIT U006560 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/executor.py:1-1 | ctx=<module> >>>
Parser / 出站入口 hook 执行器。
<<< END U006560 >>>
<<< UNIT U006561 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:9-9 >>>
# 会话信息刷新后、等待任务投递前。过滤消息或补充临时元数据
<<< END U006561 >>>
<<< UNIT U006562 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:11-11 >>>
# 会话入口策略完成后、投递等待任务前。确定是否交给等待任务取走
<<< END U006562 >>>
<<< UNIT U006563 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:13-13 >>>
# 消息文本规范化后、前缀判断前。允许重写触发文本
<<< END U006563 >>>
<<< UNIT U006564 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:15-15 >>>
# 命令候选选定后、模块处理前。冷却、临封和模块策略
<<< END U006564 >>>
<<< UNIT U006565 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:17-17 >>>
# 模块权限处理后、模板解析前。ToS 令牌桶计数
<<< END U006565 >>>
<<< UNIT U006566 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:19-19 >>>
# 模板解析后、命令函数调用前。命令级权限与平台策略
<<< END U006566 >>>
<<< UNIT U006567 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:21-21 >>>
# 命令候选通过前缀/别名解析后、通道认领前。路由策略
<<< END U006567 >>>
<<< UNIT U006568 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:23-23 >>>
# 命令未匹配模块或模板时。纠错建议
<<< END U006568 >>>
<<< UNIT U006569 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:25-25 >>>
# 消息完成基础规范化后、开始遍历正则候选前。正则路由策略
<<< END U006569 >>>
<<< UNIT U006570 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:27-27 >>>
# 每个正则模块候选匹配前。模块级路由策略
<<< END U006570 >>>
<<< UNIT U006571 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:29-29 >>>
# 命令或正则候选通过策略后、通道认领前。通道避让策略
<<< END U006571 >>>
<<< UNIT U006572 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:31-31 >>>
# 正则匹配并完成候选去重后。regex 侧策略
<<< END U006572 >>>
<<< UNIT U006573 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:33-33 >>>
# regex 场景冷却之后、获取执行锁之前。regex 侧 ToS 计数
<<< END U006573 >>>
<<< UNIT U006574 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:35-35 >>>
# 命令/正则真实调用结束。统计观察
<<< END U006574 >>>
<<< UNIT U006575 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:37-37 >>>
# 命令/正则抛出可分类异常时。ToS 业务拒绝等
<<< END U006575 >>>
<<< UNIT U006576 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:39-39 >>>
# parser 主流程 finally 清理之后。消息级计数
<<< END U006576 >>>
<<< UNIT U006577 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:41-41 >>>
# 公共出站协调层，位于安全检查之后、发往平台之前，可改写 chain
<<< END U006577 >>>
<<< UNIT U006578 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:43-43 >>>
# 平台实际返回后观察
<<< END U006578 >>>
<<< UNIT U006579 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:45-45 >>>
# 平台发送失败后观察
<<< END U006579 >>>
<<< UNIT U006580 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:49-49 >>>
# 允许构建 SessionDraft 并在成功后提交的入口
<<< END U006580 >>>
<<< UNIT U006581 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:59-59 >>>
# 分发时按此顺序校验，未知入口拒绝注册
<<< END U006581 >>>
<<< UNIT U006582 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:1-1 | ctx=<module> >>>
Parser / 出站生命周期入口点。
<<< END U006582 >>>
<<< UNIT U006583 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/points.py:7-7 | ctx=HookPoint >>>
parser 与出站生命周期入口。
<<< END U006583 >>>
<<< UNIT U006584 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/results.py:1-1 | ctx=<module> >>>
Parser 入口 hook 的类型化结果。
<<< END U006584 >>>
<<< UNIT U006585 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/results.py:13-13 | ctx=HookResult >>>
入口 hook 返回值的基类。
<<< END U006585 >>>
<<< UNIT U006586 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/results.py:18-18 | ctx=Continue >>>
继续后续 hook 与默认流程。
<<< END U006586 >>>
<<< UNIT U006587 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/results.py:25-25 | ctx=RewriteTrigger >>>
提交新的触发文本并继续当前入口的后续 hook。
<<< END U006587 >>>
<<< UNIT U006588 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/results.py:31-31 | ctx=StopScope >>>
``Stop`` 的作用域。
<<< END U006588 >>>
<<< UNIT U006589 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/results.py:72-72 | ctx=Handled >>>
错误/恢复入口专用结果，表示该 hook 已处理，不再使用默认错误提示。
<<< END U006589 >>>
<<< UNIT U006590 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/hooks/results.py:78-78 | ctx=normalize_result >>>
把 hook 返回值归一化为类型化结果，``None`` 视为 Continue。
<<< END U006590 >>>
<<< UNIT U006591 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:46-46 >>>
# 匹配哈希缓存 - 缓存消息与模块的匹配结果，加速处理
<<< END U006591 >>>
<<< UNIT U006592 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:51-52 >>>
# 标记为单次触发的正则，其“模块名 + 正则序号 + 场景 ID”在此记录，记录后不再参与匹配。
# 仅存于进程内存，重启即清空。条目数上限为“触发过的场景数 × 单次触发正则条数”，有界。
<<< END U006592 >>>
<<< UNIT U006593 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:64-64 >>>
# 无订阅时直接跳过，避免每条消息空执行 executor。
<<< END U006593 >>>
<<< UNIT U006594 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:118-118 >>>
# 有命令模板但当前客户端解析不出可用命令，视为过期建议。无模板模块允许直接通过
<<< END U006594 >>>
<<< UNIT U006595 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:121-121 >>>
# 检查场景启用状态，非 base 且要求启用时，若确认期间被禁用则放弃
<<< END U006595 >>>
<<< UNIT U006596 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:143-143 >>>
# 扩展已处理，不再发送默认提示
<<< END U006596 >>>
<<< UNIT U006597 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:146-146 >>>
# message 已由 _dispatch_stage 发送
<<< END U006597 >>>
<<< UNIT U006598 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:160-160 >>>
# 确认期间可能发生热重载或权限变化，从最新注册表获取模块并重新校验
<<< END U006598 >>>
<<< UNIT U006599 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:164-165 >>>
# 等待期间模块状态可能已变，刷新 Union 生成状态，
# 同时保留本次消息已生效的前缀与 hook 草稿修改。
<<< END U006599 >>>
<<< UNIT U006600 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:181-181 >>>
# 用户拒绝后不再追加无效提示
<<< END U006600 >>>
<<< UNIT U006601 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:185-185 >>>
# 默认语法提示由 parser_policies 的 COMMAND_UNMATCHED 订阅负责。
<<< END U006601 >>>
<<< UNIT U006602 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:187-187 >>>
# 默认模块不存在提示同样由策略订阅负责。
<<< END U006602 >>>
<<< UNIT U006603 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:196-196 >>>
# 刷新会话信息（从数据库重新加载最新数据）
<<< END U006603 >>>
<<< UNIT U006604 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:199-199 >>>
# 创建标识字符串用于日志记录
<<< END U006604 >>>
<<< UNIT U006605 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:202-202 >>>
# 入站策略（忽略发送者、互认机器人、封禁/阻断身份）在等待任务投递前统一处理。
<<< END U006605 >>>
<<< UNIT U006606 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:207-208 >>>
# 检查是否有等待此消息的任务（如等待用户回复）。入口策略可以明确让出等待路由，
# 但仍允许消息继续进入普通命令/正则流程。
<<< END U006606 >>>
<<< UNIT U006607 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:216-217 >>>
# 独占等待任务或 callback 会消费消息。允许并行路由的等待任务则在完成等待后
# 继续进入命令/正则路由。
<<< END U006607 >>>
<<< UNIT U006608 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:221-221 >>>
# 获取该平台和客户端的所有可用模块
<<< END U006608 >>>
<<< UNIT U006609 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:224-224 >>>
# 将消息转换为易读的显示格式
<<< END U006609 >>>
<<< UNIT U006610 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:231-231 >>>
# 如果消息为空，直接返回
<<< END U006610 >>>
<<< UNIT U006611 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:235-237 >>>
# 如果消息中有需要过滤的词，直接返回
# if contain_badwords(msg.trigger_msg):
#     return
<<< END U006611 >>>
<<< UNIT U006612 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:239-239 >>>
# 检查消息是否以命令前缀开头
<<< END U006612 >>>
<<< UNIT U006613 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:242-242 >>>
# 检查消息前缀，注意此时 log 的 msg.trigger_msg 是带前缀的
<<< END U006613 >>>
<<< UNIT U006614 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:291-291 >>>
# 检查触发命令是否在模块列表中
<<< END U006614 >>>
<<< UNIT U006615 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:292-292 >>>
# 检查模块是否已加载
<<< END U006615 >>>
<<< UNIT U006616 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:305-305 >>>
# 正则路由策略（禁用前缀、禁止发言、运行中提醒）由 core policy hook 确定。
<<< END U006616 >>>
<<< UNIT U006617 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:316-316 >>>
# 出现于等待被取消的情况
<<< END U006617 >>>
<<< UNIT U006618 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:325-326 >>>
# wait_* 的回复会话共享根命令的 ExecutionState，但无最终清理所有权。
# 最终 lease 只能由原始 parser 释放。
<<< END U006618 >>>
<<< UNIT U006619 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:356-356 >>>
# 如果上游指定了命令前缀，使用指定的命令前缀
<<< END U006619 >>>
<<< UNIT U006620 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:358-358 >>>
# 如果前缀列表中包含空字符串，表示禁用前缀检查
<<< END U006620 >>>
<<< UNIT U006621 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:372-372 >>>
# 排除消息太短或属于删除线格式（~~xxx~~）的特殊情况
<<< END U006621 >>>
<<< UNIT U006622 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:376-376 >>>
# 如果匹配到前缀，将其移到列表首位
<<< END U006622 >>>
<<< UNIT U006623 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:385-385 >>>
# ========== 步骤 1: 移除命令前缀 ==========
<<< END U006623 >>>
<<< UNIT U006624 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:387-387 >>>
# 禁用前缀模式，使用完整消息作为命令
<<< END U006624 >>>
<<< UNIT U006625 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:390-390 >>>
# 移除前缀，提取实际命令
<<< END U006625 >>>
<<< UNIT U006626 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:394-394 >>>
# 任意空白都算词间分隔，保留每个词在原文中的位置以便还原换行
<<< END U006626 >>>
<<< UNIT U006627 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:399-399 >>>
# 别名改写会抹去用户实际输入的首词，退役策略的白名单依赖它
<<< END U006627 >>>
<<< UNIT U006628 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:406-406 >>>
# 找到了匹配的模块，标记为非别名
<<< END U006628 >>>
<<< UNIT U006629 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:417-417 >>>
# 如果第一个词不是模块名，检查所有别名
<<< END U006629 >>>
<<< UNIT U006630 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:421-421 >>>
# 如果第一个词是模块名，只检查该模块下的别名
<<< END U006630 >>>
<<< UNIT U006631 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:428-428 >>>
# 选择最长的别名（避免短别名误匹配）
<<< END U006631 >>>
<<< UNIT U006632 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:430-430 >>>
# 获取别名对应的实际模块名
<<< END U006632 >>>
<<< UNIT U006633 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:433-433 >>>
# 只替换别名词，其后的原始文字（含换行）原样保留
<<< END U006633 >>>
<<< UNIT U006634 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:438-438 >>>
# 更新消息的触发命令
<<< END U006634 >>>
<<< UNIT U006635 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:441-441 >>>
# 返回命令的第一个词（模块名）
<<< END U006635 >>>
<<< UNIT U006636 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:454-454 >>>
# 标记是否正在显示“正在输入……”状态
<<< END U006636 >>>
<<< UNIT U006637 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:478-478 >>>
# 标记模块是否缺少命令模板
<<< END U006637 >>>
<<< UNIT U006638 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:479-479 >>>
# 模块是否按模板路由与查看者的权限无关，受限命令同样算作模板命令
<<< END U006638 >>>
<<< UNIT U006639 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:491-491 >>>
# 有命令模板，进行命令解析
<<< END U006639 >>>
<<< UNIT U006640 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:494-495 >>>
# ``None`` 表示命令已被入口策略处理（例如权限拒绝或参数错误），
# 不应伪装成成功执行。正常命令会在 helper 内抛出 SessionFinished。
<<< END U006640 >>>
<<< UNIT U006641 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:497-497 >>>
# 仅模板匹配失败进入恢复。参数转换或已开始执行的命令报错不能重试。
<<< END U006641 >>>
<<< UNIT U006642 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:501-501 >>>
# 模块没有命令模板，直接将消息传给模块处理
<<< END U006642 >>>
<<< UNIT U006643 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:505-505 >>>
# 显示“正在输入……”状态（如果用户启用）
<<< END U006643 >>>
<<< UNIT U006644 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:509-509 >>>
# 执行模块函数
<<< END U006644 >>>
<<< UNIT U006645 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:527-527 >>>
# 会话正常结束
<<< END U006645 >>>
<<< UNIT U006646 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:550-550 >>>
# 其他未预期的异常
<<< END U006646 >>>
<<< UNIT U006647 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:560-560 >>>
# 清理工作
<<< END U006647 >>>
<<< UNIT U006648 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:562-562 >>>
# 结束“正在输入……”状态
<<< END U006648 >>>
<<< UNIT U006649 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:564-564 >>>
# 释放执行锁
<<< END U006649 >>>
<<< UNIT U006650 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:711-712 >>>
# 同一条消息会被所有模块的正则轮流匹配，而渲染结果只取决于这两个参数，
# 按参数缓存一次，避免每条正则都把消息链重新处理一遍
<<< END U006650 >>>
<<< UNIT U006651 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:722-722 >>>
# 跳过未加载的模块
<<< END U006651 >>>
<<< UNIT U006652 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:735-735 >>>
# ========== 步骤 2: 检查模块可用性和平台限制 ==========
<<< END U006652 >>>
<<< UNIT U006653 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:736-736 >>>
# 模块未加载
<<< END U006653 >>>
<<< UNIT U006654 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:738-738 >>>
# 平台/客户端未被排除且在允许列表内
<<< END U006654 >>>
<<< UNIT U006655 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:755-756 >>>
# 正则级的平台声明，与命令级的 available_for / exclude_from 对称。
# 步骤 3 校验的是模块级声明，两者互不覆盖。
<<< END U006655 >>>
<<< UNIT U006656 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:760-761 >>>
# 单次触发的正则在该场景触发过之后不再参与匹配，避免每条消息都付出
# 通道认领的数据库查询与统计插入。
<<< END U006656 >>>
<<< UNIT U006657 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:766-766 >>>
# 标记是否匹配成功
<<< END U006657 >>>
<<< UNIT U006658 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:767-767 >>>
# 标记是否显示“正在输入……”
<<< END U006658 >>>
<<< UNIT U006659 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:769-769 >>>
# 用于检测重复匹配
<<< END U006659 >>>
<<< UNIT U006660 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:771-771 >>>
# 获取要匹配的消息文本（可能只包含纯文本或过滤特定元素）
<<< END U006660 >>>
<<< UNIT U006661 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:808-808 >>>
# 策略通过后再认领通道，未授权正则不会阻塞其他场景。
<<< END U006661 >>>
<<< UNIT U006662 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:830-831 >>>
# 正则由消息内容隐式触发，锁被占用时静默跳过。
# 此处若发出提示并 return，还会连带中断后续模块的正则遍历。
<<< END U006662 >>>
<<< UNIT U006663 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:835-836 >>>
# 标记须在处理函数执行前落下，否则同场景下条消息会重复触发。
# 抛出异常时同样保留标记。
<<< END U006663 >>>
<<< UNIT U006664 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:844-844 >>>
# 将 msg 传入下游模块
<<< END U006664 >>>
<<< UNIT U006665 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:848-848 >>>
# 将 msg 传入下游模块
<<< END U006665 >>>
<<< UNIT U006666 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:897-898 >>>
# 可选参数标注为 ``int | None`` 时仍应按 ``int`` 做类型转换，
# 否则值会以原始字符串形式传入命令函数。
<<< END U006666 >>>
<<< UNIT U006667 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:907-909 >>>
# 带子参数的选项（如 ``[--foo <bar>]``）在 ``msg.parsed_msg`` 中会被解析为字典
# （形如 ``{"<bar>": "value"}``）。恰好只有一个子参数时解包为该子参数的值，
# 使函数参数可以直接拿到 ``"value"``。其余情况原样返回。
<<< END U006667 >>>
<<< UNIT U006668 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:936-937 >>>
# 标注为 ``Param`` 的参数按 ``Param.name`` 取值，因为 ``-i``、``<address:port>`` 这类模板元素
# 无法作为函数参数名。选项未提供时，非 ``bool`` 参数回退到默认值，``bool`` 参数传入 ``False``。
<<< END U006668 >>>
<<< UNIT U006669 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:958-958 >>>
# 已声明默认值（如可选选项缺失）时无需提示，避免每次执行都告警
<<< END U006669 >>>
<<< UNIT U006670 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:970-970 >>>
# 选项/标志未提供时解析结果为 False，非 bool 参数应回退到默认值
<<< END U006670 >>>
<<< UNIT U006671 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:1011-1012 >>>
# 受限命令保留在模板集合中，由 COMMAND_BEFORE_EXECUTE 策略给出权限提示，
# 否则无权使用时会误报语法错误
<<< END U006671 >>>
<<< UNIT U006672 | py-comment | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:1044-1044 >>>
# 模板已匹配后发生的转换错误只进入 hook，不能重新执行命令。
<<< END U006672 >>>
<<< UNIT U006673 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:1-1 | ctx=<module> >>>
消息解析模块 - 处理消息的完整解析流程。
<<< END U006673 >>>
<<< UNIT U006674 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:569-576 | ctx=regex_once_triggered >>>
判断一条标记为单次触发的正则是否已在该场景中触发过。

:param module_name: 所属模块名称。
:param index: 该正则在模块 ``regex_list`` 中的序号。
:param target_id: 场景 ID。
:return: 是否已触发过。
<<< END U006674 >>>
<<< UNIT U006675 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:581-587 | ctx=mark_regex_once >>>
记录一条单次触发的正则已在该场景中触发过。

:param module_name: 所属模块名称。
:param index: 该正则在模块 ``regex_list`` 中的序号。
:param target_id: 场景 ID。
<<< END U006675 >>>
<<< UNIT U006676 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:594-608 | ctx=regex_module_enabled >>>
判断一个模块的正则处理函数是否应当参与匹配。

base 模块无须在场景中启用即可生效，与命令路径 :func:`_execute_module` 的判定保持一致，
base 模块注册的正则据此也能触发。

权限判定置于启用判定之前，因为模块可能在权限开启期间被启用，其后权限又被关闭，此时
``enabled_modules`` 中仍留有该模块，只拦截启用入口并不足够。

:param module: 待判定的模块。
:param module_name: 模块名称。
:param enabled_modules: 当前场景已启用的模块列表。
:param read_all_messages: 机器人在该场景是否有权限读取全部消息。
:return: 是否参与匹配。
<<< END U006676 >>>
<<< UNIT U006677 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/parser/message.py:634-650 | ctx=regex_func_available >>>
判断一条正则处理函数在当前平台上是否可用。

判定规则与 :meth:`RegexMatches.get` 一致，按 target_from / client_name / platform_from /
platform_name 的四元组匹配，使 ``available_for="Telegram"`` 对全部 Telegram 实例有效。
只校验模块级的 ``available_for`` 会让注册时写下的 ``@module.regex(available_for=...)``
形同虚设，故正则级的平台声明同样参与匹配。

:param rfunc: 正则处理函数的元数据。
:param target_from: 当前场景的前缀。
:param client_name: 当前客户端名称。
:param platform_from: 平台场景前缀。
:param platform_name: 平台展示名。
:param scope: 已取得的平台判定条件。调用方持有会话对象时经 :func:`scope_of` 传入，
    以免逐字段读取会话——会话可能是只提供所需字段的模拟对象。
:return: 是否可用。
<<< END U006677 >>>
<<< UNIT U006678 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/context.py:32-32 >>>
# 会话上下文存储 - 键为 session_id，值为上下文对象（如对应平台框架下的消息实例）
<<< END U006678 >>>
<<< UNIT U006679 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/context.py:41-43 >>>
# 入站消息处理期间不得删除上下文。平台侧在消息处理结束后才撤销记录，而
# Server 侧的 hold／send 是跨进程调用，抵达顺序无法由固定等待秒数保证。
# 这里以内联计数记录“仍在处理中的入站消息”的存活区间，避免删除早于调用。
<<< END U006679 >>>
<<< UNIT U006680 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/context.py:125-126 >>>
# 平台关闭流程可能已先清空上下文字典。release 仍须移除 hold 计数，
# 不能因重复清理抛出 KeyError 而让后台任务以未取回异常结束。
<<< END U006680 >>>
<<< UNIT U006681 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/context.py:128-129 >>>
# 平台侧可能已撤销本次消息的上下文。此时不能把同 session_id 重建的
# 入站上下文一并删除。
<<< END U006681 >>>
<<< UNIT U006682 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:1-1 | ctx=<module> >>>
会话上下文管理模块 - 管理消息会话的生命周期和通信接口。
<<< END U006682 >>>
<<< UNIT U006683 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:19-30 | ctx=ContextManager >>>
上下文管理器抽象基类。

定义了会话上下文的管理接口、消息发送接口、权限管理接口等，
用于与各种通讯平台的集成。

属性说明：
    context: 存储会话上下文的字典，键为 session_id，值为上下文对象
    features: 会话支持的功能特性对象
    typing_flags: 输入状态标志的事件对象字典
    context_marks_hold: 记录上下文被保持的次数（支持嵌套保持）
<<< END U006683 >>>
<<< UNIT U006684 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:48-53 | ctx=ContextManager.add_context >>>
为会话添加上下文。

:param session_info: 会话信息对象
:param context: 要存储的上下文对象（通常是对应平台框架下的消息实例）
<<< END U006684 >>>
<<< UNIT U006685 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:137-143 | ctx=ContextManager.check_native_permission >>>
检查权限。

:param session_info: 会话信息
:param user_id: 指定成员的平台 ID，留空则检查发送者本人
:return: 是否具备权限，指定成员时，不含场景成员的上下文一律返回 False
<<< END U006685 >>>
<<< UNIT U006686 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:162-169 | ctx=ContextManager.send_message >>>
向会话所在的场景发送消息。

:param session_info: 会话信息
:param message: 消息内容，可以是 MessageChain 或字符串
:param quote: 是否引用消息
:return: 消息 ID 列表
<<< END U006686 >>>
<<< UNIT U006687 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:217-223 | ctx=ContextManager.delete_message >>>
删除指定场景中的消息，可能需要该场景的管理员权限。

:param session_info: 会话信息
:param message_id: 消息 ID 列表（为最大兼容，请将元素转换为 str，若实现需要传入其他类型再在下方另行实现）
:param reason: 原因（可选）
<<< END U006687 >>>
<<< UNIT U006688 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:239-246 | ctx=ContextManager.restrict_member >>>
禁言指定场景中的成员，可能需要该场景的管理员权限。

:param session_info: 会话信息
:param user_id: 用户 ID
:param duration: 禁言时长
:param reason: 原因（可选）
<<< END U006688 >>>
<<< UNIT U006689 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:260-265 | ctx=ContextManager.unrestrict_member >>>
解除禁言指定场景中的成员，可能需要该场景的管理员权限。

:param session_info: 会话信息
:param user_id: 用户 ID
<<< END U006689 >>>
<<< UNIT U006690 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:279-285 | ctx=ContextManager.kick_member >>>
踢出指定场景中的成员，可能需要该场景的管理员权限。

:param session_info: 会话信息
:param user_id: 用户 ID
:param reason: 原因（可选）
<<< END U006690 >>>
<<< UNIT U006691 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:299-305 | ctx=ContextManager.ban_member >>>
封禁指定场景中的成员，可能需要该场景的管理员权限。

:param session_info: 会话信息
:param user_id: 用户 ID
:param reason: 原因（可选）
<<< END U006691 >>>
<<< UNIT U006692 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:319-324 | ctx=ContextManager.unban_member >>>
解除封禁指定场景中的成员，可能需要该场景的管理员权限。

:param session_info: 会话信息
:param user_id: 用户 ID
<<< END U006692 >>>
<<< UNIT U006693 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:344-344 | ctx=ContextManager.grant_permission_group >>>
为场景成员授予平台原生权限组或角色。
<<< END U006693 >>>
<<< UNIT U006694 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:356-356 | ctx=ContextManager.revoke_permission_group >>>
移除场景成员的平台原生权限组或角色。
<<< END U006694 >>>
<<< UNIT U006695 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:362-368 | ctx=ContextManager.add_reaction >>>
为指定消息添加反应。

:param session_info: 会话信息
:param message_id: 消息 ID
:param emoji: 反应内容（如表情符号）
<<< END U006695 >>>
<<< UNIT U006696 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:381-387 | ctx=ContextManager.remove_reaction >>>
为指定消息删除反应。

:param session_info: 会话信息
:param message_id: 消息 ID
:param emoji: 反应内容（如表情符号）
<<< END U006696 >>>
<<< UNIT U006697 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:400-404 | ctx=ContextManager.start_typing >>>
开始输入状态。

:param session_info: 会话信息
<<< END U006697 >>>
<<< UNIT U006698 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:419-423 | ctx=ContextManager.end_typing >>>
结束输入状态。

:param session_info: 会话信息
<<< END U006698 >>>
<<< UNIT U006699 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/context.py:434-438 | ctx=ContextManager.error_signal >>>
发送错误信号。

:param session_info: 会话信息
<<< END U006699 >>>
<<< UNIT U006700 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/features.py:30-30 >>>
# Markdown 扩展支持 - 会话是否支持渲染表格、代码块、LaTeX 等
<<< END U006700 >>>
<<< UNIT U006701 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/features.py:43-43 >>>
# 处理消息节点支持 - 会话是否有独立处理消息节点的能力
<<< END U006701 >>>
<<< UNIT U006702 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/features.py:1-1 | ctx=<module> >>>
会话功能特性模块 - 定义消息会话支持的各种功能。
<<< END U006702 >>>
<<< UNIT U006703 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/features.py:8-8 | ctx=Features >>>
会话功能特性类。
<<< END U006703 >>>
<<< UNIT U006704 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/features.py:68-68 | ctx=Features.override >>>
创建一个新的 Features 实例，并根据提供的关键字参数覆盖默认值。
<<< END U006704 >>>
<<< UNIT U006705 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:32-32 >>>
# 并发解析时用于占位的空协程，使 gather 的两路返回值位置保持固定。
<<< END U006705 >>>
<<< UNIT U006706 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:77-77 >>>
# 多实例的平台两段，语义同 SessionInfo。默认实例下分别等于 client_name 与 target_from。
<<< END U006706 >>>
<<< UNIT U006707 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:167-168 >>>
# 多实例的平台两段（纯字符串以便跨进程序列化），默认实例下分别等于 client_name 与
# target_from，四元组条件回退为两段。缺失时按同一规则补齐。
<<< END U006707 >>>
<<< UNIT U006708 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:171-172 >>>
# 与平台 SDK 上下文绑定的入站会话必须回到原始 Client 实例。
# 主动会话留空以使用服务组 anycast。
<<< END U006708 >>>
<<< UNIT U006709 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:204-205 >>>
# 场景 union 由 assign() 解析，无法解析时即抛出异常，故此后必定有值。
# 用户 union 则不同，没有 sender_id 的会话（如主动推送）本就没有它。
<<< END U006709 >>>
<<< UNIT U006710 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:210-210 >>>
# 本场景在其场景组内的消息通道编号，同组同号即现实中的同一个场景，详见 channel_key
<<< END U006710 >>>
<<< UNIT U006711 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:214-215 >>>
# 会话一律经 assign() 建立，其中必定按场景语言赋值。此处的默认值仅用于
# 反序列化等未赋值情形，故声明为非可选，免去各调用点无谓的空值检查。
<<< END U006711 >>>
<<< UNIT U006712 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:223-223 >>>
# 平台按当前场景返回的权限快照。由 MessageSession.check_bot_state() 写入。
<<< END U006712 >>>
<<< UNIT U006713 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:229-230 >>>
# 平台消息入口额外声明的前缀（如 Discord Slash、QQ 官方的 ``/``）。
# refresh_info() 会刷新数据库中的自定义前缀，但必须保留这一组入口能力。
<<< END U006713 >>>
<<< UNIT U006714 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:232-232 >>>
# 主动推送的备用场景 ID 列表，本次发送失败时由客户端回调服务端改用列表中的下一个场景重发
<<< END U006714 >>>
<<< UNIT U006715 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:236-237 >>>
# 是否为私聊场景。由平台适配器在构造会话时判定，各平台对“私聊”的表达互不相同
# （QQ 为 Private、Discord 为 DM 频道、QQ 官方分 C2C 与频道私信等），核心不作推断。
<<< END U006715 >>>
<<< UNIT U006716 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:245-245 >>>
# 单次处理内的临时数据，assign() 必定赋值，且会被就地写入，故须逐实例新建
<<< END U006716 >>>
<<< UNIT U006717 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:281-282 >>>
# 场景与用户的 union 解析互不依赖，并发发出可省去一半的往返等待。
# 主数据库在远端时这一项按每次往返的网络延迟计。
<<< END U006717 >>>
<<< UNIT U006718 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:378-379 >>>
# 主动会话在 server 进程构造，本进程的 Info.platform_name 是 "Server"。
# 平台名只能取自被路由到的客户端元数据，否则平台级声明落不到这个会话上。
<<< END U006718 >>>
<<< UNIT U006719 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:395-396 >>>
# 跨进程反序列化的会话（含升级前入队的旧消息）可能缺少平台两段。此处按当前已知的
# client_name / target_from 补齐，缺少字段时回退为改造前的两段判定条件，不会误判为别的实例。
<<< END U006719 >>>
<<< UNIT U006720 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:400-401 >>>
# SessionInfo 是入队时快照，其间权限、禁止发言、语言与前缀可能已被改动。
# 只替换 ORM 对象而保留生成字段，会让 parser 按入队时的旧状态执行。
<<< END U006720 >>>
<<< UNIT U006721 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/info.py:406-408 >>>
# assign() 已在平台进程为入站消息建立两侧映射。消息排队期间若管理员删除了
# 对应 Union，刷新时绝不能再创建一套默认状态继续执行，否则会复活已删除身份，
# 并可能绕过原 Union 上的封禁、禁止发言或模块配置。
<<< END U006721 >>>
<<< UNIT U006722 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:1-1 | ctx=<module> >>>
会话信息模块 - 定义和管理消息会话的信息和上下文。
<<< END U006722 >>>
<<< UNIT U006723 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:70-70 | ctx=EventInfo >>>
可跨进程序列化的平台事件上下文。
<<< END U006723 >>>
<<< UNIT U006724 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:102-102 | ctx=EventInfo.assign >>>
把上下文字段复制到当前对象。
<<< END U006724 >>>
<<< UNIT U006725 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:145-145 | ctx=EventInfo.refresh_info >>>
反序列化后从数据库恢复 union 对象及场景前缀。
<<< END U006725 >>>
<<< UNIT U006726 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:162-162 | ctx=SessionInfo >>>
可跨进程序列化的会话快照，包含平台身份、消息元数据、能力、权限及 Union 状态。
<<< END U006726 >>>
<<< UNIT U006727 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:272-278 | ctx=SessionInfo.assign >>>
用于将参数传入 SessionInfo 对象中。

:param platform_name: 平台展示名，未提供时取当前进程的 Info.platform_name（平台进程内可用）。
:param platform_from: 平台场景前缀，未提供时由 target_from 的客户端段替换而来。
:return: SessionInfo 对象。
<<< END U006727 >>>
<<< UNIT U006728 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:394-394 | ctx=SessionInfo.refresh_info >>>
从数据库同步会影响当前消息解析的 Union 状态。
<<< END U006728 >>>
<<< UNIT U006729 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:447-447 | ctx=SessionInfo.get_common_target_id >>>
获取场景的常用 ID。
<<< END U006729 >>>
<<< UNIT U006730 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:451-451 | ctx=SessionInfo.get_common_sender_id >>>
获取用户的常用 ID。
<<< END U006730 >>>
<<< UNIT U006731 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:484-484 | ctx=SessionInfo.emote_enabled >>>
本会话是否使用表情资源。
<<< END U006731 >>>
<<< UNIT U006732 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:500-500 | ctx=SessionInfo.target_offset >>>
模块业务使用的场景偏移量。
<<< END U006732 >>>
<<< UNIT U006733 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:511-511 | ctx=SessionInfo.display_offset >>>
向用户展示时间使用的偏移量。
<<< END U006733 >>>
<<< UNIT U006734 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:522-522 | ctx=SessionInfo.tz >>>
模块业务使用的时区。
<<< END U006734 >>>
<<< UNIT U006735 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:527-527 | ctx=SessionInfo.display_tz >>>
向用户展示时间使用的时区。
<<< END U006735 >>>
<<< UNIT U006736 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:532-532 | ctx=SessionInfo.tz_label >>>
场景偏移量的规范字符串。
<<< END U006736 >>>
<<< UNIT U006737 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:537-537 | ctx=SessionInfo.display_tz_label >>>
展示偏移量的规范字符串。
<<< END U006737 >>>
<<< UNIT U006738 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:541-541 | ctx=SessionInfo.now >>>
获取场景时区的当前时间。
<<< END U006738 >>>
<<< UNIT U006739 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:545-545 | ctx=SessionInfo.today >>>
获取场景时区的当前日期。
<<< END U006739 >>>
<<< UNIT U006740 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:551-551 | ctx=FetchedSessionInfo >>>
主动获取的消息会话信息。
<<< END U006740 >>>
<<< UNIT U006741 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/info.py:556-556 | ctx=ModuleHookContext >>>
模块任务上下文。主要用于传递模块任务的参数。
<<< END U006741 >>>
<<< UNIT U006742 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:37-37 >>>
# 会话相关配置在导入期获取一次快照，避免每次获取文案都读取配置
<<< END U006742 >>>
<<< UNIT U006743 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:48-48 >>>
# 平台进程可能只返回 ValueError 文本，此时按消息内容回退。
<<< END U006743 >>>
<<< UNIT U006744 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:134-134 >>>
# 会话信息 - 存储会话的所有基本信息
<<< END U006744 >>>
<<< UNIT U006745 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:145-146 >>>
# 别名改写前用户实际输入的命令首词。模块别名可能把白名单命令并入其他模块
# （如 merge 现为 bind 的别名），退役策略解析后仍需据此判断放行与否。
<<< END U006745 >>>
<<< UNIT U006746 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:149-150 >>>
# 仅存在于 Server 进程的命令执行状态。wait_* 取得的回复会话共享同一对象，
# 嵌套等待据此释放／重获同一 lease，并由原始 parser 统一释放平台 context。
<<< END U006746 >>>
<<< UNIT U006747 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:173-174 >>>
# release_context 是跨进程动作。一次瞬时 Queue／平台异常不应把已经
# hold 的 context 永久遗留。成功项只释放一次，失败项让出一拍后重试。
<<< END U006747 >>>
<<< UNIT U006748 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:265-265 >>>
# 在 callback 注册之前，避免取消时遗留 pending 注册
<<< END U006748 >>>
<<< UNIT U006749 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:280-280 >>>
# 改写后的最终消息必须重新过完整发送规范化（含 MessageNodes 节点校验与平台转换）
<<< END U006749 >>>
<<< UNIT U006750 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:288-288 >>>
# 在平台发送前为每次 callback 建立独立注册。
<<< END U006750 >>>
<<< UNIT U006751 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:314-315 >>>
# 会话上下文已不可用时，让调用方按可恢复的会话失效处理，而不是把
# 跨进程错误原样漏到模块层。
<<< END U006751 >>>
<<< UNIT U006752 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:332-333 >>>
# callback 可能已在发送响应前被主动撤销、过期或作为一次性
# callback 消费。此时 extend 返回 None，不能重新注册。
<<< END U006752 >>>
<<< UNIT U006753 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:349-349 >>>
# 空 ID 表示平台发送失败，不能只凭 bot_id 为不存在的消息留下 callback。
<<< END U006753 >>>
<<< UNIT U006754 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:352-352 >>>
# 观察快照带真实消息 ID 与最终发送内容。慢观察者不会延长 callback 未绑定窗口
<<< END U006754 >>>
<<< UNIT U006755 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:416-416 >>>
# ========== 步骤 1.5: 出站 before_send ==========
<<< END U006755 >>>
<<< UNIT U006756 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:441-441 >>>
# submit 仅代表接受投递，不能据此发布 sent
<<< END U006756 >>>
<<< UNIT U006757 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:460-460 >>>
# 平台不支持私信时无需经过队列，直接判定失败
<<< END U006757 >>>
<<< UNIT U006758 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:493-493 >>>
# 私信接口没有引用参数，观察内容始终反映实际的不引用发送。
<<< END U006758 >>>
<<< UNIT U006759 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:507-507 >>>
# 观察入口获取快照，不能改写正式返回值
<<< END U006759 >>>
<<< UNIT U006760 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:677-677 >>>
# 恢复时须沿用最初展示提示的会话。等待取得的回复会话没有对应的平台提示。
<<< END U006760 >>>
<<< UNIT U006761 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:691-692 >>>
# 添加确认反应的内部方法。
# 自动为不同平台选择合适的确认反应（勾选和叉号）。
<<< END U006761 >>>
<<< UNIT U006762 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:739-739 >>>
# 合并转发消息无从追加提示行，此时略过
<<< END U006762 >>>
<<< UNIT U006763 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:769-770 >>>
# 等待任务须在跨进程发送提示前就位。平台可能已展示消息并收到用户操作，
# 而发送 action 的结果尚未回到 Server。
<<< END U006763 >>>
<<< UNIT U006764 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:785-785 >>>
# 严格确认的匹配器已限定为完全等于口令，命中即通过
<<< END U006764 >>>
<<< UNIT U006765 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:820-820 >>>
# 合并转发消息无从追加提示行，此时略过
<<< END U006765 >>>
<<< UNIT U006766 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1065-1065 >>>
# 中日韩文字数单位，万（10^4）、亿（10^8）、兆（10^12）
<<< END U006766 >>>
<<< UNIT U006767 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1075-1075 >>>
# 英文单位，k（10^3）、M（10^6）、G（10^9）
<<< END U006767 >>>
<<< UNIT U006768 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1118-1119 >>>
# 比较两个消息会话对象是否相等。
# 两个会话仅当会话 ID 相同时才认为相等。
<<< END U006768 >>>
<<< UNIT U006769 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1-1 | ctx=<module> >>>
消息会话内部模块 - 提供消息会话的核心实现和方法。
<<< END U006769 >>>
<<< UNIT U006770 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:55-55 | ctx=normalize_confirm_token >>>
将严格确认的口令归一化为待比对文本，I18N 模板按会话语言解析其占位符。
<<< END U006770 >>>
<<< UNIT U006771 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:101-101 | ctx=normalize_outgoing_chain >>>
对 hook 改写后的最终出站链完整执行发送规范化。
<<< END U006771 >>>
<<< UNIT U006772 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:120-132 | ctx=MessageSession >>>
消息会话类 - 处理与用户的交互。

该类提供了一套完整的消息交互接口，包括发送消息、接收回复、等待用户输入等功能。
每个消息会话对应一个用户在某个平台的一条消息。

属性说明：
    session_info: 会话信息对象，包含会话的所有基本信息
    sent: 已发送消息链列表，用于跟踪消息历史
    trigger_msg: 触发本会话的原始消息文本
    matched_msg: 正则表达式或其他匹配的结果
    parsed_msg: 已解析的消息内容（如命令参数）
<<< END U006772 >>>
<<< UNIT U006773 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:163-163 | ctx=MessageSession.release_execution_resources >>>
由原始 parser 在命令结束时释放全部等待结果 context。
<<< END U006773 >>>
<<< UNIT U006774 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:201-206 | ctx=MessageSession.from_session_info >>>
从会话信息创建消息会话实例。

:param session: 会话信息对象
:return: 消息会话实例
<<< END U006774 >>>
<<< UNIT U006775 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:211-211 | ctx=MessageSession.t >>>
返回当前会话的翻译函数。
<<< END U006775 >>>
<<< UNIT U006776 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:219-219 | ctx=MessageSession.t_str >>>
返回当前会话的字符串翻译函数。
<<< END U006776 >>>
<<< UNIT U006777 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:514-521 | ctx=MessageSession.as_display >>>
用于将消息转换为一般文本格式。

:param text_only: 是否只保留纯文本。（默认为 False）
:param element_filter: 元素过滤器，用于过滤消息链中的元素。（默认为 None）
:param connector: 元素之间的连接符。（默认为换行）
:return: 转换后的字符串。
<<< END U006777 >>>
<<< UNIT U006778 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:525-529 | ctx=MessageSession.delete >>>
用于删除这条消息。

:param reason: 删除原因（可选）
<<< END U006778 >>>
<<< UNIT U006779 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:549-553 | ctx=MessageSession.unrestrict_member >>>
用于解除成员的禁言，可能需要该场景的管理员权限。

:param user_id: 用户 ID 或 ID 列表
<<< END U006779 >>>
<<< UNIT U006780 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:558-563 | ctx=MessageSession.kick_member >>>
用于踢出成员，可能需要该场景的管理员权限。

:param user_id: 用户 ID 或 ID 列表
:param reason: 踢出原因（可选）
<<< END U006780 >>>
<<< UNIT U006781 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:567-572 | ctx=MessageSession.ban_member >>>
用于封禁成员，可能需要该场景的管理员权限。

:param user_id: 用户 ID 或 ID 列表
:param reason: 封禁原因（可选）
<<< END U006781 >>>
<<< UNIT U006782 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:576-580 | ctx=MessageSession.unban_member >>>
用于解除成员的封禁，可能需要该场景的管理员权限。

:param user_id: 用户 ID 或 ID 列表
<<< END U006782 >>>
<<< UNIT U006783 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:590-590 | ctx=MessageSession.grant_permission_group >>>
为场景成员授予平台原生权限组或角色。
<<< END U006783 >>>
<<< UNIT U006784 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:606-606 | ctx=MessageSession.revoke_permission_group >>>
移除场景成员的平台原生权限组或角色。
<<< END U006784 >>>
<<< UNIT U006785 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:624-629 | ctx=MessageSession.remove_reaction >>>
用于给这条消息删除反应。

:param emoji: 反应内容（如表情符号、Unicode 字符等）
:return: 平台返回的删除结果
<<< END U006785 >>>
<<< UNIT U006786 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:647-647 | ctx=MessageSession.handle_error_signal >>>
用于处理错误信号。
<<< END U006786 >>>
<<< UNIT U006787 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:651-651 | ctx=MessageSession.hold >>>
用于持久化会话上下文，手动控制会话的生命周期，避免会话结束后资源被释放。
<<< END U006787 >>>
<<< UNIT U006788 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:660-660 | ctx=MessageSession.release >>>
用于手动释放持久化的会话。
<<< END U006788 >>>
<<< UNIT U006789 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:664-664 | ctx=MessageSession.start_typing >>>
用于在会话中开始输入状态。
<<< END U006789 >>>
<<< UNIT U006790 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:669-669 | ctx=MessageSession.end_typing >>>
用于结束会话中的输入状态。
<<< END U006790 >>>
<<< UNIT U006791 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:951-955 | ctx=MessageSession.sleep >>>
用于暂停执行指定的秒数。

:param s: 暂停时长（秒）
<<< END U006791 >>>
<<< UNIT U006792 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:962-966 | ctx=MessageSession.check_super_user >>>
用于检查消息用户是否为超级用户。

:return: 如果用户是超级用户返回 True，否则返回 False
<<< END U006792 >>>
<<< UNIT U006793 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:992-992 | ctx=MessageSession.call_api >>>
调用平台 API。
<<< END U006793 >>>
<<< UNIT U006794 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1047-1062 | ctx=MessageSession.format_num >>>
格式化数字为本地化的表示。

根据地区设置进行本地化处理，包括数字分隔符和单位符号的翻译。
支持自动缩放大数字（如 100 万 -> 1 百万 或 1M）。

:param number: 要格式化的数字
:param precision: 保留小数点位数（默认为 0）
:return: 本地化格式的数字字符串

示例：
```
    > session.format_num(1000000, precision=1)  # 中文： '100.0 万'
    > session.format_num(1000000, precision=1)  # 英文： '1.0M'
```
<<< END U006794 >>>
<<< UNIT U006795 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1110-1117 | ctx=MessageSession.__eq__ >>>
比较两个消息会话对象是否相等。

        两个会话仅当会话 ID 相同时才认为相等。

        :param other: 另一个对象
        :return: 如果相等返回 True，否则返回 False
<<< END U006795 >>>
<<< UNIT U006796 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1127-1127 | ctx=FinishedSession >>>
结束会话类 - 表示已完成的消息发送会话。
<<< END U006796 >>>
<<< UNIT U006797 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1134-1140 | ctx=FinishedSession.assign >>>
创建 FinishedSession 实例。

:param session: 消息会话信息
:param message_id: 消息 ID，如果是单个值会被转换为列表
:return: FinishedSession 实例
<<< END U006797 >>>
<<< UNIT U006798 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1146-1146 | ctx=FinishedSession.delete >>>
用于删除这条消息。
<<< END U006798 >>>
<<< UNIT U006799 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1150-1152 | ctx=FinishedSession.__str__ >>>
返回字符串表示
<<< END U006799 >>>
<<< UNIT U006800 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1158-1158 | ctx=FetchedMessageSession >>>
主动获取的消息会话。
<<< END U006800 >>>
<<< UNIT U006801 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/internal.py:1162-1167 | ctx=FetchedMessageSession.from_session_info >>>
从会话信息创建主动获取的消息会话实例。

:param session: 会话信息对象（可以是普通 SessionInfo 或 FetchedSessionInfo）
:return: FetchedMessageSession 实例
<<< END U006801 >>>
<<< UNIT U006802 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:20-21 >>>
# parser 的根 asyncio.Task 是 lease 的最终生命周期边界。
# 未覆盖的退出路径由任务完成回调回收遗留 lease。
<<< END U006802 >>>
<<< UNIT U006803 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:24-25 >>>
# wait_anyone／wait_reply(all_=True) 的结果可能来自另一名用户，
# 执行锁仍须按最初发起命令的用户计算。
<<< END U006803 >>>
<<< UNIT U006804 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:27-28 >>>
# 输入提示按会话消息 ID 展示，恢复时须沿用最初发起提示的会话。
# wait_* 取得的回复会话不能用自己的 ID 重新开启。
<<< END U006804 >>>
<<< UNIT U006805 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:35-36 >>>
# token -> 该 lease 覆盖的 Union／物理账号键。保留 ``_list`` 名称以兼容
# 运行时调试和旧测试中的 clear()。
<<< END U006805 >>>
<<< UNIT U006806 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:38-39 >>>
# 正在扩展身份域的 merge reservation。单独记录 token，才能区分“必须等待
# 结束的普通命令”和“另一个也在等待扩域的合并命令”，避免后者互相等待。
<<< END U006806 >>>
<<< UNIT U006807 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:76-77 >>>
# SessionInfo 是入队时快照，等待期间 merge／unbind 可能使其 union 行失效，
# 必须按物理 ID 重新解析，以免漏掉新组成员或误锁已分离账号。
<<< END U006807 >>>
<<< UNIT U006808 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:109-110 >>>
# wait_* 的内部辅助 Task 可能共享根执行状态。lease 生命周期仍应由
# 最初取得它的 parser Task 管理，不能被短命辅助 Task 提前回收。
<<< END U006808 >>>
<<< UNIT U006809 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:148-149 >>>
# 服务器重载或测试可能清空 lease 表却留下执行域 token。
# 它已不代表所有权，必须丢弃后重新获取。
<<< END U006809 >>>
<<< UNIT U006810 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:154-156 >>>
# _current_keys() 的数据库查询会让出执行权。其间同一执行域的另一协程
# （被等待任务消费的回复会话）可能已把 token 写入。必须在判定冲突前
# 重新确认所有权，否则根命令会等待自己持有的 lease 永久自锁。
<<< END U006810 >>>
<<< UNIT U006811 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:162-162 >>>
# _conflicts() 与 _install() 之间没有 await，在同一事件循环中是原子的。
<<< END U006811 >>>
<<< UNIT U006812 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:189-190 >>>
# 两个合并命令的扩展域只要相交，后进入 reservation 的命令必须让出。
# 只检查“完整覆盖”挡不住 A+B 与 B+C 这类部分重叠，双方将相互等待。
<<< END U006812 >>>
<<< UNIT U006813 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:1-1 | ctx=<module> >>>
执行锁模块 - 用于管理消息执行锁，防止同一用户的多个命令并发执行。
<<< END U006813 >>>
<<< UNIT U006814 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:14-14 | ctx=ExecutionState >>>
仅存在于 Server 进程中的一次命令执行状态。
<<< END U006814 >>>
<<< UNIT U006815 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:33-33 | ctx=ExecutionLockList >>>
执行锁列表 - 管理正在执行的消息会话。
<<< END U006815 >>>
<<< UNIT U006816 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:45-45 | ctx=ExecutionLockList.state >>>
取得会话的 server-only 执行状态，并兼容未调用父类构造器的测试替身。
<<< END U006816 >>>
<<< UNIT U006817 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:173-173 | ctx=ExecutionLockList.is_locked >>>
按当前 Union 绑定集检查会话是否与现有 lease 冲突。
<<< END U006817 >>>
<<< UNIT U006818 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:180-180 | ctx=ExecutionLockList.reserve >>>
扩展当前 lease 并等待与扩展身份域冲突的其他命令结束。
<<< END U006818 >>>
<<< UNIT U006819 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:208-208 | ctx=ExecutionLockList.refresh >>>
按数据库中的最新 Union 绑定集刷新当前 lease 覆盖范围。
<<< END U006819 >>>
<<< UNIT U006820 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:222-222 | ctx=ExecutionLockList.add >>>
兼容无 I/O 的旧调用点，仅使用会话已有的 Union 和物理 ID。
<<< END U006820 >>>
<<< UNIT U006821 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:232-232 | ctx=ExecutionLockList.remove >>>
只释放当前会话自己持有的 lease。
<<< END U006821 >>>
<<< UNIT U006822 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:246-246 | ctx=ExecutionLockList.check >>>
无 I/O 的兼容检查，生产 parser 应使用 :meth:`is_locked`。
<<< END U006822 >>>
<<< UNIT U006823 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:253-253 | ctx=ExecutionLockList.get >>>
返回所有活跃 lease 覆盖的身份键，用于调试和管理命令。
<<< END U006823 >>>
<<< UNIT U006824 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/lock.py:258-258 | ctx=ExecutionLockList.count >>>
返回活跃命令 lease 数，可排除调用命令自身。
<<< END U006824 >>>
<<< UNIT U006825 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:19-20 >>>
# 索引只使用记录时不可变的物理场景／账号 ID，因为 union ID 与 channel_id 会在等待期间因合并、
# 解绑或重新分配通道而变化，拿快照作永久索引会让原物理用户失去 waiter，甚至被旧组成员接管。
<<< END U006825 >>>
<<< UNIT U006826 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:24-25 >>>
# 存储待执行回调的字典。key 用独立注册 token，不用消息 ID 别名，因为
# message_id 只在单会话内唯一，channel_key 又会合并多个平台入口。
<<< END U006826 >>>
<<< UNIT U006827 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:58-58 >>>
# 使用物理 ID 建立稳定索引。Union／channel 都允许在等待期间变化。
<<< END U006827 >>>
<<< UNIT U006828 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:70-70 >>>
# 使用字符串元组保存回复 ID。平台 ID 自身可能包含逗号，不能依赖分隔符拼接。
<<< END U006828 >>>
<<< UNIT U006829 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:76-76 >>>
# 存储任务信息
<<< END U006829 >>>
<<< UNIT U006830 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:83-83 >>>
# 平台发送完成后才能确定的物理消息 ID
<<< END U006830 >>>
<<< UNIT U006831 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:86-86 >>>
# 跨用户专属／all 索引的稳定记录顺序
<<< END U006831 >>>
<<< UNIT U006832 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:87-88 >>>
# reply 的物理 message_id 只在发送它的客户端／平台场景中有意义。
# 即使两个入口属于同一现实通道，也不能跨平台用碰巧相同的 ID 命中。
<<< END U006832 >>>
<<< UNIT U006833 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:141-142 >>>
# 将同一次发送的全部消息 ID／虚拟按钮 ID／fallback ID 合并为一组。元组
# 不会像逗号拼接字符串那样在平台 ID 自身含逗号时产生歧义。
<<< END U006833 >>>
<<< UNIT U006834 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:153-153 >>>
# 存储回调信息
<<< END U006834 >>>
<<< UNIT U006835 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:161-162 >>>
# 可重复 callback 必须串行执行，避免同一消息的快速连续操作并发
# 修改模块状态。一次性 callback 仍会在 await 用户代码前原子删除。
<<< END U006835 >>>
<<< UNIT U006836 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:292-293 >>>
# 绑定与通道变更是低频管理操作。读取候选 bucket 时与它们共用 mutation
# 域，避免先读旧 Union、再读新 channel 而组合出数据库中从未存在过的范围。
<<< END U006836 >>>
<<< UNIT U006837 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:347-348 >>>
# hold_context 会跨进程让出执行权。其间等待命令可能已超时或被取消。
# 此时不能把结果发布给失效任务，也不能遗留刚取得的 context hold。
<<< END U006837 >>>
<<< UNIT U006838 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:370-371 >>>
# 先找已 ready 的精确引用目标。没有则同时等待所有 pending 任务中的任意一个，
# 避免记录早但发送阻塞的任务阻塞后续 ready 任务。
<<< END U006838 >>>
<<< UNIT U006839 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:422-422 >>>
# 已完成的独占等待任务优先消费消息。允许 fallthrough 的 wait_next 任务除外。
<<< END U006839 >>>
<<< UNIT U006840 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:426-427 >>>
# 没有引用目标时不能命中回调。直接做 str(None) 会得到字面量 "None"，
# 一旦某个平台或测试注册了同名消息 ID，普通消息也会错误消费该回调。
<<< END U006840 >>>
<<< UNIT U006841 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:431-432 >>>
# 先按真实／虚拟消息 ID 精确匹配。bot_id fallback 仅在当前作用域与发送者下唯一时可用，
# 否则不能按注册顺序猜测用户引用的是哪一次发送。
<<< END U006841 >>>
<<< UNIT U006842 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:436-437 >>>
# bg_check() 仅用于周期清理，不能作为授权边界。callback 必须在
# 尝试命中时按自身 timeout 立即判定是否失效。
<<< END U006842 >>>
<<< UNIT U006843 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:457-458 >>>
# 真实／虚拟主 ID 比 bot_id fallback 强。但同等级有多个候选时无法
# 确定用户操作的是哪次发送，必须保留全部注册而不是按字典顺序猜测。
<<< END U006843 >>>
<<< UNIT U006844 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:469-469 >>>
# 一次性 callback 在 await 用户代码前原子删除，避免并发回复重复执行。
<<< END U006844 >>>
<<< UNIT U006845 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:475-476 >>>
# callback 使用 msg.finish() 正常结束当前交互，这是控制流信号，不能
# 逸出到 JobQueue action 令任务停在 processing 直到两小时超时。
<<< END U006845 >>>
<<< UNIT U006846 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:481-482 >>>
# 匹配和取得执行锁之间 callback 可能已被发送失败清理、主动撤销
# 或过期任务删除。执行前重新确认注册身份和有效期，不能让旧引用复活。
<<< END U006846 >>>
<<< UNIT U006847 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:1-1 | ctx=<module> >>>
会话任务管理模块 - 管理等待用户回复和执行回调的任务。
<<< END U006847 >>>
<<< UNIT U006848 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:17-17 | ctx=SessionTaskManager >>>
管理等待任务与消息回调。任务以稳定的物理 ID 索引，命中时再按当前 Union 拓扑展开。回调使用独立注册 token，并在发送完成后绑定物理消息 ID。
<<< END U006848 >>>
<<< UNIT U006849 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:105-105 | ctx=SessionTaskManager.set_task_reply >>>
为发送前记录的 reply 等待任务补全物理消息 ID。
<<< END U006849 >>>
<<< UNIT U006850 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:176-176 | ctx=SessionTaskManager.extend_callback >>>
为尚未消费的 callback 补充发送后才取得的物理消息 ID。
<<< END U006850 >>>
<<< UNIT U006851 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:189-189 | ctx=SessionTaskManager.remove_callback >>>
撤销一组仍在有效期内的 callback 别名。
<<< END U006851 >>>
<<< UNIT U006852 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:211-216 | ctx=SessionTaskManager.get_result >>>
获取指定任务的执行结果。

:param msg: 消息会话对象
:return: 任务完成后的结果（通常是一个 MessageSession 对象），如果没有结果则返回 None
<<< END U006852 >>>
<<< UNIT U006853 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:224-224 | ctx=SessionTaskManager.remove_task >>>
移除等待任务并清理已经为空的父级索引。
<<< END U006853 >>>
<<< UNIT U006854 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:246-250 | ctx=SessionTaskManager.get >>>
获取整个任务列表。

:return: 任务列表字典
<<< END U006854 >>>
<<< UNIT U006855 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:255-255 | ctx=SessionTaskManager.active_count >>>
返回仍处于等待状态的任务数量。
<<< END U006855 >>>
<<< UNIT U006856 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/tasks.py:266-266 | ctx=SessionTaskManager.bg_check >>>
后台检查任务超时。
<<< END U006856 >>>
<<< UNIT U006857 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/terms.py:9-9 >>>
# 场景前缀来自各适配器，格式由平台侧确定。不能进入键名或占位符语法的字符一律剔除。
<<< END U006857 >>>
<<< UNIT U006858 | py-comment | packages/akari-bot-core/akaribot/core/builtins/session/terms.py:32-32 >>>
# 前缀由平台侧声明，仓库外的适配器可能给出不合规的格式。此时回退到基础术语而非中断消息处理。
<<< END U006858 >>>
<<< UNIT U006859 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/session/terms.py:1-1 | ctx=<module> >>>
会话术语作用域的构造。
<<< END U006859 >>>
<<< UNIT U006860 | py-comment | packages/akari-bot-core/akaribot/core/builtins/temp/__init__.py:18-18 >>>
# 存储临时数据的字典，键值对形式存储临时信息
<<< END U006860 >>>
<<< UNIT U006861 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/temp/__init__.py:1-1 | ctx=<module> >>>
临时存储模块 - 用于在会话生命周期内存储临时数据。
<<< END U006861 >>>
<<< UNIT U006862 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/temp/__init__.py:5-16 | ctx=Temp >>>
临时存储类。

提供一个全局的临时数据存储字典，用于在会话或消息处理期间
存储临时数据。数据在程序重启后将丢失。

示例：
```
    Temp.data['key'] = 'value'
    value = Temp.data['key']
```
<<< END U006862 >>>
<<< UNIT U006863 | py-comment | packages/akari-bot-core/akaribot/core/builtins/types/__init__.py:24-24 >>>
# 多媒体元素类型联合体 - 包含纯文本、图片、语音、原始格式消息
<<< END U006863 >>>
<<< UNIT U006864 | py-comment | packages/akari-bot-core/akaribot/core/builtins/types/__init__.py:27-27 >>>
# 完整的消息元素类型联合体 - 包含所有支持的消息元素类型
<<< END U006864 >>>
<<< UNIT U006865 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/types/__init__.py:1-1 | ctx=<module> >>>
消息元素类型定义模块。
<<< END U006865 >>>
<<< UNIT U006866 | py-comment | packages/akari-bot-core/akaribot/core/builtins/utils/__init__.py:11-12 >>>
# 确认命令列表 - 用户确认操作时可使用的关键词，加上默认的圆形符号表情
# 从配置中加载，去重处理，并默认添加 ⭕ 符号作为万能确认符
<<< END U006866 >>>
<<< UNIT U006867 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/utils/__init__.py:15-15 >>>
# 确认词
<<< END U006867 >>>
<<< UNIT U006868 | py-comment | packages/akari-bot-core/akaribot/core/builtins/utils/__init__.py:17-18 >>>
# 命令前缀列表 - 触发命令的前缀符号，如 "/" 或 "~"
# 从配置中加载，进行去重处理
<<< END U006868 >>>
<<< UNIT U006869 | py-inline-comment | packages/akari-bot-core/akaribot/core/builtins/utils/__init__.py:19-19 >>>
# 命令前缀
<<< END U006869 >>>
<<< UNIT U006870 | py-docstring | packages/akari-bot-core/akaribot/core/builtins/utils/__init__.py:1-1 | ctx=<module> >>>
内置工具模块 - 提供命令前缀和确认词等系统级配置。
<<< END U006870 >>>
<<< UNIT U006871 | py-comment | packages/akari-bot-core/akaribot/core/client/init.py:75-76 >>>
# 多实例下 client_name 带实例后缀，平台展示名只能由客户端在此声明，因为
# server 侧构造主动会话时本进程没有平台身份，须经被路由到的 peer 元数据取回。
<<< END U006871 >>>
<<< UNIT U006872 | py-comment | packages/akari-bot-core/akaribot/core/client/init.py:88-89 >>>
# 初始化应当具备事务性，后半段失败时撤销本轮刚启动的任务并关闭连接，
# 使下一次重试从干净状态开始，而不是叠加一组半初始化资源。
<<< END U006872 >>>
<<< UNIT U006873 | py-docstring | packages/akari-bot-core/akaribot/core/client/init.py:21-21 | ctx=check_queue >>>
监控客户端队列轮询。瞬时异常后退避并重新启动。
<<< END U006873 >>>
<<< UNIT U006874 | py-docstring | packages/akari-bot-core/akaribot/core/client/init.py:116-116 | ctx=client_init >>>
初始化平台客户端。
<<< END U006874 >>>
<<< UNIT U006875 | py-docstring | packages/akari-bot-core/akaribot/core/client/init.py:138-138 | ctx=client_cleanup >>>
取消客户端初始化和队列任务，并关闭数据库连接。
<<< END U006875 >>>
<<< UNIT U006876 | py-comment | packages/akari-bot-core/akaribot/core/component.py:132-132 >>>
# 注册期归一化，匹配时不必对每条正则再 upper() 一次
<<< END U006876 >>>
<<< UNIT U006877 | py-comment | packages/akari-bot-core/akaribot/core/component.py:422-422 >>>
# 调用方就是定义模块本身，再往外一层是 importlib，取到的是 "importlib._bootstrap"。
<<< END U006877 >>>
<<< UNIT U006878 | py-comment | packages/akari-bot-core/akaribot/core/component.py:426-427 >>>
# 包名由发现层解析，因为按调用方文件路径推导时，目录布局变化
# 会静默得到空字符串，连带使热重载、locale 指纹、依赖图与模块卸载失去依据。
<<< END U006878 >>>
<<< UNIT U006879 | py-docstring | packages/akari-bot-core/akaribot/core/component.py:22-22 | ctx=Bind >>>
平台消息元素与绑定键的映射表。
<<< END U006879 >>>
<<< UNIT U006880 | py-docstring | packages/akari-bot-core/akaribot/core/component.py:41-72 | ctx=Bind.Module.command >>>
绑定模块命令。

命令模板语法参见 :func:`core.builtins.parser.args.parse_template`。
模板中的参数与选项可直接映射为被装饰函数的参数：

- ``<name>``：位置参数，对应同名函数参数。未提供时使用默认值或 ``None``。
- ``[flag]``：标志选项，对应同名函数参数，标注为 ``bool`` 时直接得到选项是否传入。
- ``[-b]`` / ``[--foo <bar>]``：以连字符开头的选项，对应同名函数参数，参数名中的
  下划线按连字符匹配（如参数 ``no_cover`` 对应 ``--no-cover``）。
  带子参数且仅有一个子参数时，直接将该子参数的值传入。
- 也可直接使用选项的子参数名，如 ``[-p <page>]`` 对应函数参数 ``page``。
- ``-i``、``<address:port>`` 等无法作为函数参数名的模板元素，可用 ``Param``
  标注指定对应的模板元素，如 ``data: Param("-i", bool) = False``。

示例：:

    @module.command("test [-b] [--foo <bar>]")
    async def _(msg: Bot.MessageSession, b: bool = False, foo: str | None = None):
        ...

:param command_template: 命令模板，可传入多个模板作为同一命令的多个变体。
:param command_templates: 额外的命令模板。
:param options_desc: 选项描述，用于生成帮助文档。
:param required_admin: 此命令是否需要场景管理员权限。
:param required_superuser: 此命令是否仅超级用户可执行。
:param required_base_superuser: 此命令是否仅基础超级用户可执行。
:param available_for: 此命令支持的平台列表。
:param exclude_from: 此命令排除的平台列表。
:param load: 是否加载此命令。
:param priority: 匹配优先级，数值越大优先级越高。
<<< END U006880 >>>
<<< UNIT U006881 | py-docstring | packages/akari-bot-core/akaribot/core/component.py:396-420 | ctx=module >>>
绑定一个模块。

:param module_name: 绑定的命令前缀。
:param alias: 此命令的别名。
同时用于命令解析。此项不为空时会尝试解析其中的语法，并将结果存入 MessageSession.parsed_msg。
:param desc: 此命令的简介。
:param recommend_modules: 推荐打开的其他模块。
:param required_admin: 此命令是否需要场景管理员权限。
:param base: 将此命令设为基础命令。设为基础命令后此命令将被强制开启。（默认为 False）
:param doc: 此命令是否存在线上说明文件。（默认为 False）
:param hidden: 将此命令设为隐藏命令。设为隐藏命令后此命令在帮助列表中不可见。（默认为 False）
:param load: 设置此命令是否加载。（默认为 True）
:param rss: 将此命令设为 RSS 命令。（默认为 False）
:param regex: 将此命令设为正则命令。（默认为 False）
:param event: 将此命令设为事件模块。事件模块要求平台可读取全部消息。（默认为 False）
:param required_superuser: 将此命令设为仅机器人的超级用户可执行。（默认为 False）
:param required_base_superuser: 将此命令设为仅机器人的基础超级用户可执行。（默认为 False）
:param required_bot_permissions: 开启模块前要求机器人具备的平台权限字段。
:param suppress_invalid_prompt: 命令未能匹配任何模板时是否抑制语法错误提示。
适用于命令按平台分流、匹配不上属于预期结果的模块。（默认为 False）
:param available_for: 此命令支持的平台列表。（默认为 `*`）
:param exclude_from: 此命令排除的平台列表。
:param support_languages: 此命令支持的语言列表。
<<< END U006881 >>>
<<< UNIT U006882 | py-comment | packages/akari-bot-core/akaribot/core/config/__init__.py:23-23 >>>
# 模板在类创建时注册字段并补充缺失键，因此加载与迁移须先于此处的模板导入完成。
<<< END U006882 >>>
<<< UNIT U006883 | py-comment | packages/akari-bot-core/akaribot/core/config/base.py:8-9 >>>
# 以下是位于 config.toml 中任何表之外的顶层键值对。它们在首次运行时由 bot.py 写出结构，
# 并由 akaribot/core/config/update.py 的版本迁移维护，声明在此仅为提供一个带类型的读取入口。
<<< END U006883 >>>
<<< UNIT U006884 | py-comment | packages/akari-bot-core/akaribot/core/config/base.py:18-18 >>>
# 保留既有导入路径
<<< END U006884 >>>
<<< UNIT U006885 | py-docstring | packages/akari-bot-core/akaribot/core/config/base.py:1-1 | ctx=<module> >>>
表外顶层基础配置及历史导入路径兼容实现。
<<< END U006885 >>>
<<< UNIT U006886 | py-docstring | packages/akari-bot-core/akaribot/core/config/base.py:12-12 | ctx=BaseConfig >>>
配置模板的基类。
<<< END U006886 >>>
<<< UNIT U006887 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:24-24 >>>
# 调试与运行
<<< END U006887 >>>
<<< UNIT U006888 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:38-38 >>>
# 身份与权限
<<< END U006888 >>>
<<< UNIT U006889 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:44-44 >>>
# 命令交互
<<< END U006889 >>>
<<< UNIT U006890 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:52-52 >>>
# 通用功能
<<< END U006890 >>>
<<< UNIT U006891 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:61-61 >>>
# 拼写检查
<<< END U006891 >>>
<<< UNIT U006892 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:74-74 >>>
# 花瓣
<<< END U006892 >>>
<<< UNIT U006893 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:85-85 >>>
# 玩笑
<<< END U006893 >>>
<<< UNIT U006894 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:91-91 >>>
# 外部链接
<<< END U006894 >>>
<<< UNIT U006895 | py-comment | packages/akari-bot-core/akaribot/core/config/core.py:102-103 >>>
# 密钥项写在 config.toml 的 [secret] 表内，故表名为 config、以 secret 标志区分。
# 不可写作 on_config("secret")，否则会去查找并不存在的 secret.toml。
<<< END U006895 >>>
<<< UNIT U006896 | py-docstring | packages/akari-bot-core/akaribot/core/config/core.py:1-1 | ctx=<module> >>>
通用核心配置模板。
<<< END U006896 >>>
<<< UNIT U006897 | py-docstring | packages/akari-bot-core/akaribot/core/config/core.py:25-25 | ctx=CoreConfig >>>
核心配置模板。
<<< END U006897 >>>
<<< UNIT U006898 | py-docstring | packages/akari-bot-core/akaribot/core/config/core.py:106-106 | ctx=CoreSecretConfig >>>
核心机密配置模板。
<<< END U006898 >>>
<<< UNIT U006899 | py-comment | packages/akari-bot-core/akaribot/core/config/jobqueue.py:47-47 >>>
# 延迟导入以避免配置模板初始化期间经 core.config.base 形成循环导入。
<<< END U006899 >>>
<<< UNIT U006900 | py-docstring | packages/akari-bot-core/akaribot/core/config/jobqueue.py:1-1 | ctx=<module> >>>
JobQueue 配置模板。
<<< END U006900 >>>
<<< UNIT U006901 | py-docstring | packages/akari-bot-core/akaribot/core/config/jobqueue.py:40-40 | ctx=bootstrap_jobqueue_config >>>
在子进程启动前生成并持久化缺失的 JobQueue 共享配置。
<<< END U006901 >>>
<<< UNIT U006902 | py-comment | packages/akari-bot-core/akaribot/core/config/migration.py:58-58 >>>
# 配置管理器已加载时以它为准，因为测试与脚本可能已切换过配置路径。
<<< END U006902 >>>
<<< UNIT U006903 | py-comment | packages/akari-bot-core/akaribot/core/config/migration.py:66-67 >>>
# 现行扁平布局下非核心表一名一文件。ConfigLayout 启用后改由
# ConfigLayout.file_for() 提供同一映射。
<<< END U006903 >>>
<<< UNIT U006904 | py-comment | packages/akari-bot-core/akaribot/core/config/migration.py:72-73 >>>
# 清单未声明 ``config_table`` 时按装饰器的命名规则推导，适配器为 ``bot_<名>``，
# 模块为 ``module_<名>``。
<<< END U006904 >>>
<<< UNIT U006905 | py-comment | packages/akari-bot-core/akaribot/core/config/migration.py:154-155 >>>
# 这类文件生成于本机制启用之前，其内容等价于该包首个迁移之前的状态。包尚无迁移脚本时，
# 直接采用清单声明的表结构版本。
<<< END U006905 >>>
<<< UNIT U006906 | py-comment | packages/akari-bot-core/akaribot/core/config/migration.py:167-168 >>>
# 不经 ``importlib.import_module`` 加载，因为以迁移编号开头的模块名不是合法标识符，且重复加载会在
# ``sys.modules`` 留下同名残留。脚本声明的 ``REVISION`` 与文件名不一致时立即报错。
<<< END U006906 >>>
<<< UNIT U006907 | py-comment | packages/akari-bot-core/akaribot/core/config/migration.py:185-186 >>>
# 调用方可能是同步的启动流程，也可能处在事件循环内。后者不能再执行 ``asyncio.run``，
# 故另起线程驱动。
<<< END U006907 >>>
<<< UNIT U006908 | py-comment | packages/akari-bot-core/akaribot/core/config/network.py:5-5 >>>
# 各 SDK 的代理参数均以 None 表示直连，配置未填写时取到的是空字符串
<<< END U006908 >>>
<<< UNIT U006909 | py-docstring | packages/akari-bot-core/akaribot/core/config/network.py:1-1 | ctx=<module> >>>
出站网络请求使用的代理与 TLS 校验设置。
<<< END U006909 >>>
<<< UNIT U006910 | py-docstring | packages/akari-bot-core/akaribot/core/config/s3.py:1-1 | ctx=<module> >>>
S3 兼容对象存储配置模板。
<<< END U006910 >>>
<<< UNIT U006911 | py-docstring | packages/akari-bot-core/akaribot/core/config/webrender.py:1-1 | ctx=<module> >>>
WebRender 配置模板。
<<< END U006911 >>>
<<< UNIT U006912 | py-comment | packages/akari-bot-core/akaribot/core/constants/__init__.py:1-1 >>>
# 为避免循环导入而硬编码的常量，供各模块导入。此处不要引入不必要的依赖。
<<< END U006912 >>>
<<< UNIT U006913 | py-docstring | packages/akari-bot-core/akaribot/core/constants/exceptions.py:53-53 | ctx=SessionContextUnavailable >>>
平台进程中对应的消息上下文已经不可用。
<<< END U006913 >>>
<<< UNIT U006914 | py-comment | packages/akari-bot-core/akaribot/core/constants/info.py:36-36 >>>
# union 返回新集合、并不就地修改，此处必须用 update 才能记录批量密钥
<<< END U006914 >>>
<<< UNIT U006915 | py-comment | packages/akari-bot-core/akaribot/core/constants/info.py:68-68 >>>
# 空字符串表示默认实例。非空时须匹配 INSTANCE_ID_PATTERN。
<<< END U006915 >>>
<<< UNIT U006916 | py-comment | packages/akari-bot-core/akaribot/core/constants/info.py:71-71 >>>
# JobQueue 运行实例 ID 每次进程启动都不同。client_name 仍表示可竞争消费的服务组。
<<< END U006916 >>>
<<< UNIT U006917 | py-comment | packages/akari-bot-core/akaribot/core/constants/info.py:74-74 >>>
# 守护进程与内置 Hub 非 JobQueue 节点，其 PID 须由守护进程在启动时显式传入。
<<< END U006917 >>>
<<< UNIT U006918 | py-comment | packages/akari-bot-core/akaribot/core/constants/info.py:82-83 >>>
# 启用后，mock 未命中的请求直接失败，不改用真实网络。
# 改用真实网络会带上重试与超时（默认 3 次 × 20 秒），足以让单个未录制的 URL 拖慢测试逾一分钟。
<<< END U006918 >>>
<<< UNIT U006919 | py-comment | packages/akari-bot-core/akaribot/core/constants/info.py:86-86 >>>
# 实例 ID 的合法形式。限制字符集是为了让它能安全地拼进 target_id 前缀与配置文件名。
<<< END U006919 >>>
<<< UNIT U006920 | py-docstring | packages/akari-bot-core/akaribot/core/constants/info.py:6-6 | ctx=Secret >>>
敏感配置值。
<<< END U006920 >>>
<<< UNIT U006921 | py-docstring | packages/akari-bot-core/akaribot/core/constants/info.py:14-14 | ctx=Secret.add >>>
加入敏感值。
<<< END U006921 >>>
<<< UNIT U006922 | py-docstring | packages/akari-bot-core/akaribot/core/constants/info.py:20-20 | ctx=Secret.check >>>
检查敏感值是否存在。
<<< END U006922 >>>
<<< UNIT U006923 | py-docstring | packages/akari-bot-core/akaribot/core/constants/info.py:28-28 | ctx=Secret.remove >>>
删除敏感值。
<<< END U006923 >>>
<<< UNIT U006924 | py-docstring | packages/akari-bot-core/akaribot/core/constants/info.py:34-34 | ctx=Secret.update >>>
替换敏感值。
<<< END U006924 >>>
<<< UNIT U006925 | py-docstring | packages/akari-bot-core/akaribot/core/constants/info.py:41-60 | ctx=Info >>>
机器人信息。

:param version: 机器人版本。
:param subprocess: 是否为子进程。
:param binary_mode: 是否为二进制模式。
:param command_parsed: 已处理命令数量。
:param message_parsed: 已处理消息数量。
:param platform_name: 平台展示名，如 ``Telegram``，同一平台的全部实例共用。
:param instance_id: 实例 ID，空字符串表示默认实例。
:param client_name: 客户端名称，由平台展示名与实例 ID 生成。
:param peer_id: 当前 JobQueue 进程实例 ID。
:param peer_role: 当前 JobQueue 进程角色。
:param daemon_pid: 守护进程 PID，由守护进程显式传入，独立运行时为 None。
:param hub_pid: 内置 JobQueue Hub 子进程 PID，未启用内置 Hub 时为 None。
:param dirty_word_check: 是否启用文本过滤。
:param web_render_status: WebRender 状态。
:param use_url_manager: 是否启用 URLManager。
:param use_url_md_format: 是否启用 URL Markdown 格式。
<<< END U006925 >>>
<<< UNIT U006926 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:17-18 >>>
# 配置只读模式的环境变量名，由守护进程在创建子进程前设置，pre-init 进程清除。
# 该常量须位于不依赖 core.config 的模块，以免提前触发导入期版本迁移。
<<< END U006926 >>>
<<< UNIT U006927 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:21-22 >>>
# union 合并日志目录的环境变量名，测试引导据此写入临时目录。
# 取值发生在导入期，引导代码须以字面量重复该名称。
<<< END U006927 >>>
<<< UNIT U006928 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:25-25 >>>
# 基本路径
<<< END U006928 >>>
<<< UNIT U006929 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:37-38 >>>
# assets 只放随仓库分发的只读内容，运行时与部署者产生的内容一律写入 data。此处不创建
# 目录，否则只读取版本号的调用也会在当前目录留下副作用。使用方经 Paths.ensure() 创建。
<<< END U006929 >>>
<<< UNIT U006930 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:40-40 >>>
# assets 子路径（只读）
<<< END U006930 >>>
<<< UNIT U006931 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:42-43 >>>
# 模板随 core wheel 分发（akaribot/core/assets/templates）。实例的 assets/templates 存在时优先，
# 便于部署者覆盖。打包形态下 __file__ 与包内资源都可用，故直接由包位置推导。
<<< END U006931 >>>
<<< UNIT U006932 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:47-47 >>>
# data 子路径（可写）
<<< END U006932 >>>
<<< UNIT U006933 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:53-54 >>>
# 字体文件路径的三个常量已弃用，字体随 akari-bot-assets-fonts 分发，路径不再固定，取值一律改用
# akaribot.core.api.find_font()。下面的映射只为兼容既有导入保留，取用时才查找，找不到时即抛出异常。
<<< END U006933 >>>
<<< UNIT U006934 | py-comment | packages/akari-bot-core/akaribot/core/constants/path.py:73-74 >>>
# 惰性导入避免导入期多拉一层依赖，因为字体查找要用 importlib.resources 与 matplotlib，而本模块
# 在引导阶段就被读入。
<<< END U006934 >>>
<<< UNIT U006935 | py-docstring | packages/akari-bot-core/akaribot/core/constants/path.py:63-72 | ctx=__getattr__ >>>
已弃用字体常量的取用口，替代品为 ``akaribot.core.api.find_font``。

    惰性导入避免导入期多拉一层依赖，因为字体查找要用 importlib.resources 与 matplotlib，而本模块
    在引导阶段就被读入。

    :param name: 常量名。
    :return: 字体文件路径。
    :raises AttributeError: 名字不在已弃用清单内。
<<< END U006935 >>>
<<< UNIT U006936 | py-docstring | packages/akari-bot-core/akaribot/core/constants/path.py:95-95 | ctx=PrivateData.ensure >>>
创建私有目录并返回其路径。
<<< END U006936 >>>
<<< UNIT U006937 | py-comment | packages/akari-bot-core/akaribot/core/database/__init__.py:109-109 >>>
# 迁移只在创建数据表的写入进程中执行，读进程不创建数据表，也不该改动库结构。
<<< END U006937 >>>
<<< UNIT U006938 | py-comment | packages/akari-bot-core/akaribot/core/database/__init__.py:115-116 >>>
# 初始化可能在部分连接建立后被取消。清理完成后保留取消语义，
# 让上层生命周期控制能够正常停止。
<<< END U006938 >>>
<<< UNIT U006939 | py-comment | packages/akari-bot-core/akaribot/core/database/__init__.py:124-126 >>>
# Tortoise.init() 可能在部分连接已经建立后才失败。若把半初始化的
# 全局状态留给调用方，随后重试会复用或覆盖一套不完整的连接注册表。
# init_db() 对外以 False 表示失败，因此也应在返回前完成自身回滚。
<<< END U006939 >>>
<<< UNIT U006940 | py-comment | packages/akari-bot-core/akaribot/core/database/__init__.py:133-135 >>>
# Tortoise.init() 在无当前 context 时会把初始化 context 写入当前任务。
# 该 context 会被复制给 Queue poller 等后续任务，reload 替换全局 context 后它们
# 仍会持有旧对象。初始化完成后恢复为“仅使用 global fallback”。
<<< END U006940 >>>
<<< UNIT U006941 | py-comment | packages/akari-bot-core/akaribot/core/database/__init__.py:198-199 >>>
# Tortoise 只提供 set_global_context，但缺少可替换现有 global 的公共 API。
# 在切换前新 context 已完全初始化，故这里是有意的原子替换点。
<<< END U006941 >>>
<<< UNIT U006942 | py-comment | packages/akari-bot-core/akaribot/core/database/__init__.py:202-203 >>>
# 不把新 context 固定到当前任务，否则后续子任务会继续继承任务级对象，
# 下一次 reload 替换全局 context 时重现旧 context 泄漏。
<<< END U006942 >>>
<<< UNIT U006943 | py-comment | packages/akari-bot-core/akaribot/core/database/__init__.py:236-237 >>>
# 先让 Queue handler 处理完队列中的任务，再停止新 Job 并取消运行中的 Job。新 context
# 的构建不触碰旧连接，准备完成后才激活新 context 并关闭旧 context。
<<< END U006943 >>>
<<< UNIT U006944 | py-comment | packages/akari-bot-core/akaribot/core/database/__init__.py:261-262 >>>
# close_connections 只关闭连接，不会移除 Tortoise 的 global fallback。
# 清理任务级与全局 context，允许后续 init_db() 真正重新初始化。
<<< END U006944 >>>
<<< UNIT U006945 | py-docstring | packages/akari-bot-core/akaribot/core/database/__init__.py:34-34 | ctx=fetch_module_db >>>
获取模块数据库。
<<< END U006945 >>>
<<< UNIT U006946 | py-docstring | packages/akari-bot-core/akaribot/core/database/__init__.py:44-44 | ctx=get_model_names >>>
返回模型名。
<<< END U006946 >>>
<<< UNIT U006947 | py-docstring | packages/akari-bot-core/akaribot/core/database/__init__.py:58-58 | ctx=get_model_fields >>>
返回模型字段。
<<< END U006947 >>>
<<< UNIT U006948 | py-comment | packages/akari-bot-core/akaribot/core/database/base.py:68-69 >>>
# resolve_union 返回后到模块行创建前，另一个进程可能删除整个 Union。
# 在 mutation 域内重新锁定核心行，确保“核心行存在”与“模块行创建”同属一个事务。
<<< END U006948 >>>
<<< UNIT U006949 | py-docstring | packages/akari-bot-core/akaribot/core/database/base.py:13-18 | ctx=extract_session_id >>>
从字符串或会话对象中取出平台 ID。

:param value: ID 字符串或 MessageSession / FetchedMessageSession 实例。
:param attr: 要读取的 SessionInfo 属性名。
<<< END U006949 >>>
<<< UNIT U006950 | py-inline-comment | packages/akari-bot-core/akaribot/core/database/compat.py:14-14 >>>
# pragma: no cover - 未安装 MySQL 驱动时跳过 MySQL 补丁
<<< END U006950 >>>
<<< UNIT U006951 | py-docstring | packages/akari-bot-core/akaribot/core/database/compat.py:1-1 | ctx=<module> >>>
Tortoise ORM 兼容补丁。
<<< END U006951 >>>
<<< UNIT U006952 | py-docstring | packages/akari-bot-core/akaribot/core/database/compat.py:147-147 | ctx=install_tortoise_transaction_compat >>>
安装各后端事务与批量写入的取消安全补丁，可重复调用。
<<< END U006952 >>>
<<< UNIT U006953 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:26-26 >>>
# 旧版本号的终点。到达该版本后旧数据库不再需要逐级升级，只需记录 revision。
<<< END U006953 >>>
<<< UNIT U006954 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:29-30 >>>
# 旧版本号到 ``(包名, revision)`` 的对照表。使用包名，与 PackageRegistry.migration_dirs()
# 的键一致。旧数据库升到某版本后，该版本及其之前的全部 revision 都视为已应用，不再重放。
<<< END U006954 >>>
<<< UNIT U006955 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:46-47 >>>
# v3 中，原本以平台 ID 为主键的两张核心表改为关联 union，表名与模型名一致，
# 以免“target_info”这类旧名继续读作“平台场景信息”。
<<< END U006955 >>>
<<< UNIT U006956 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:53-53 >>>
# v3 中，原本以平台 ID 为主键的表改为关联 union，旧数据的 union ID 直接沿用原 ID，因此只需重命名主键列。
<<< END U006956 >>>
<<< UNIT U006957 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:69-69 >>>
# v3 中，统计与审计表保留原始 ID，另增 union 列用于聚合。
<<< END U006957 >>>
<<< UNIT U006958 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:72-72 >>>
# v4 中，Wiki API 独立名单并入全局 URL 规则文件，迁移成功后移除旧表。
<<< END U006958 >>>
<<< UNIT U006959 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:78-78 >>>
# v6 中，绑定表补充 OAuth 授权所需的列，水鱼、落雪两侧的数据获取方式都改由 OAuth 令牌确定。
<<< END U006959 >>>
<<< UNIT U006960 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:85-86 >>>
# v6 中绑定方式换代后不再读写的历史列。落雪好友码曾用于免授权的查分接口，现已改为上传 OAuth 令牌，
# 模型也不再声明该列。留着它只会让库结构与模型长期不一致（旧列带 NOT NULL 且无默认值，新写入会直接失败）。
<<< END U006960 >>>
<<< UNIT U006961 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:150-151 >>>
# 核心表改名。调用方已先执行过 generate_schemas()，按新模型创建的目标表此刻为空表，
# 须先移除再改名，否则改名会与之冲突。目标表若已有数据，说明改名早已完成，跳过即可。
<<< END U006961 >>>
<<< UNIT U006962 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:162-162 >>>
# 主键列改名。表由 generate_schemas() 新建时已是 union_id，此时旧列不存在，跳过即可。
<<< END U006962 >>>
<<< UNIT U006963 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:172-172 >>>
# CHANGE COLUMN 兼容 MySQL 8.0 以下版本。
<<< END U006963 >>>
<<< UNIT U006964 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:177-178 >>>
# 补充创建映射行。旧数据的 union ID 与原 ID 相同，直接按原值一一对应即可。
# 账号级封禁保持关闭，原有的封禁状态已记在 union 上。
<<< END U006964 >>>
<<< UNIT U006965 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:181-181 >>>
# 消息通道编号。target_union_bind 由 generate_schemas() 新建时已包含该列，正常升级路径不会执行此段。
<<< END U006965 >>>
<<< UNIT U006966 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:188-189 >>>
# 通道号须在组内逐个顺延。若一律保留默认值 1，同一组下的全部场景会被判定为同一条消息通道，
# 命令与推送将相互去重，导致场景不再有消息送达。
<<< END U006966 >>>
<<< UNIT U006967 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:196-197 >>>
# 旧版 connect 将机器人互认记录存为扁平列表，无法反向查询某条记录属于哪个场景，解绑时也就无从删除。
# 该结构已改为两级字典，旧值直接清除，重新执行一次 bind auto 即可。
<<< END U006967 >>>
<<< UNIT U006968 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:203-203 >>>
# 统计与审计表增列并回填，历史记录的原始 ID 保持不动。
<<< END U006968 >>>
<<< UNIT U006969 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:220-221 >>>
# 轮询与区间统计所需的索引，因为 job_queues 每 100 毫秒被轮询，analytics_data 要按区间反复聚合，
# 两者都随行数增长退化为全表扫描。开发期已升到 v3 的库需把版本号退回 2 重新执行以补上索引。
<<< END U006969 >>>
<<< UNIT U006970 | py-comment | packages/akari-bot-core/akaribot/core/database/legacy.py:285-285 >>>
# 未启用该模块时这张表可能根本不存在，此时无需迁移。
<<< END U006970 >>>
<<< UNIT U006971 | py-docstring | packages/akari-bot-core/akaribot/core/database/legacy.py:145-149 | ctx=update_database_to_v3 >>>
将数据库升级至 v3，使平台 ID 与数据解耦，数据改为关联 union。

:param conn: 数据库连接。
<<< END U006971 >>>
<<< UNIT U006972 | py-docstring | packages/akari-bot-core/akaribot/core/database/legacy.py:301-309 | ctx=drop_indexes_on_missing_columns >>>
删除指向不存在列的索引。

``generate_schemas(safe=True)`` 会为已存在的旧表补建按当前模型声明的索引，而旧表可能尚未改
列名，于是出现指向不存在列的索引。SQLite 改动任何表结构时都会重新解析整个库结构，这类索引会
让升级的第一条 ALTER 失败。删除的索引随后由 ``generate_schemas`` 依模型重建。

:param conn: 数据库连接。
<<< END U006972 >>>
<<< UNIT U006973 | py-docstring | packages/akari-bot-core/akaribot/core/database/legacy.py:334-342 | ctx=legacy_upgrade_to_v6 >>>
按旧版本号把既有库逐级升级到 v6，返回升级前的版本号。

调用方须已完成数据库初始化。本函数不建立也不关闭连接，以便在 ``init_db()`` 的连接上直接
执行。每一步都先探测再执行，中途失败后重新执行不会重复施加变更。

:param conn: 数据库连接，省略时使用默认连接。
:return: 升级前的版本号，无版本记录时为 ``None``。
<<< END U006973 >>>
<<< UNIT U006974 | py-docstring | packages/akari-bot-core/akaribot/core/database/legacy.py:459-467 | ctx=convert_legacy_version >>>
把旧版本号转换为 ``schema_migrations`` 记录。

只在 ``schema_migrations`` 为空且 ``database_version`` 有记录时执行一次，前者为空说明该
库尚未记录过 revision，后者有记录说明库来自旧版本。版本低于 v6 时先按旧逻辑升级到 v6，
再把不超过该版本的 revision 全部记录为已应用，避免重放已验证的升级步骤。

:return: 转换前的旧版本号，无需转换时为 ``None``。
<<< END U006974 >>>
<<< UNIT U006975 | py-comment | packages/akari-bot-core/akaribot/core/database/link.py:9-10 >>>
# Tortoise 按参数顺序执行 PRAGMA。先延长锁等待时间，再尝试切换 WAL，
# 避免多个进程并发启动时 journal_mode 尚未受到 30 秒等待策略保护。
<<< END U006975 >>>
<<< UNIT U006976 | py-comment | packages/akari-bot-core/akaribot/core/database/link.py:17-18 >>>
# 路径可能直接复制自 Windows 配置，``Path`` 在其他平台上无法识别盘符与反斜杠开头的写法，
# 故按字面补充判断，免得把绝对路径误判为相对实例根目录。
<<< END U006976 >>>
<<< UNIT U006977 | py-comment | packages/akari-bot-core/akaribot/core/database/link.py:25-27 >>>
# 默认链接是 ``sqlite://database/save.db`` 这样的相对路径，驱动按进程 cwd 解析它，
# 从实例外启动的入口因此会把数据库创建到调用目录。实例内的相对路径一律以
# :class:`akaribot.core.paths.Paths` 记录的实例根目录为基准，与 ``AKARI_INSTANCE_DIR`` 一致。
<<< END U006977 >>>
<<< UNIT U006978 | py-comment | packages/akari-bot-core/akaribot/core/database/link.py:56-56 >>>
# 内存数据库没有文件可建，故不预先创建目录。其余后端先创建好目录，驱动不会代建。
<<< END U006978 >>>
<<< UNIT U006979 | py-comment | packages/akari-bot-core/akaribot/core/database/link.py:73-74 >>>
# busy_timeout 必须在可能取得写锁的 PRAGMA（尤其 journal_mode）之前生效。
# 即使调用方显式提供了参数并采用其他排列，也统一提前执行等待策略。
<<< END U006979 >>>
<<< UNIT U006980 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:31-31 >>>
# 包内迁移目录的约定名。包若在 manifest 中声明了 migrations，则以声明为准。
<<< END U006980 >>>
<<< UNIT U006981 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:34-34 >>>
# 支持事务性 DDL 的方言。其余方言只按先探测再执行的方式保证可重复执行。
<<< END U006981 >>>
<<< UNIT U006982 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:45-47 >>>
# 获取连接的方言名。
# 以连接自身的能力为准而不是模块级配置，因为测试与转换脚本会在同一进程内使用与配置不同的
# 连接，按配置判断会生成错误的 DDL。
<<< END U006982 >>>
<<< UNIT U006983 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:95-95 >>>
# SQLite executescript 会隐式提交。完整语句逐条执行以保留 revision 的事务边界。
<<< END U006983 >>>
<<< UNIT U006984 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:377-377 >>>
# 跨包依赖无法表达，Runner 已固定 core 先于各包执行。
<<< END U006984 >>>
<<< UNIT U006985 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:422-422 >>>
# 获取已记录的 revision。
<<< END U006985 >>>
<<< UNIT U006986 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:444-446 >>>
# 提示已应用的迁移文件被改写。
# 只警告不阻断，因为开发期改动迁移文件是常态，阻断会制造无谓摩擦，但生产环境的静默改动
# 值得一条告警。
<<< END U006986 >>>
<<< UNIT U006987 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:458-460 >>>
# 获取包的执行顺序。
# core 的全部 revision 先执行完，再按包名依次执行各模块包，因为模块侧的绑定回填以 core 的
# 改名与回填已完成为前提，且各包的 revision 无法互相声明依赖。
<<< END U006987 >>>
<<< UNIT U006988 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:549-549 >>>
# 执行并记录一条迁移。
<<< END U006988 >>>
<<< UNIT U006989 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:555-555 >>>
# 在方言允许时以事务执行迁移入口。
<<< END U006989 >>>
<<< UNIT U006990 | py-comment | packages/akari-bot-core/akaribot/core/database/migration.py:561-561 >>>
# 事务内取到的连接由事务上下文持有，模型查询与裸 SQL 都会走同一连接。
<<< END U006990 >>>
<<< UNIT U006991 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:41-41 | ctx=MigrationError >>>
迁移定义或执行不符合接口约定。
<<< END U006991 >>>
<<< UNIT U006992 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:53-60 | ctx=MigrationContext >>>
单条 revision 的执行上下文。

探测与 DDL 均按当前方言生成，revision 只描述要达成什么，不必自行分支 SQLite 与 MySQL。

:param conn: 数据库连接。
:param db_type: 方言名，省略时由连接推断。
<<< END U006992 >>>
<<< UNIT U006993 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:67-72 | ctx=MigrationContext.quote >>>
按方言给标识符加引号。

:param ident: 表名或列名。
:return: 加引号后的标识符。
<<< END U006993 >>>
<<< UNIT U006994 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:76-81 | ctx=MigrationContext.execute >>>
执行一条语句。

:param sql: SQL 语句。
:param params: 位置参数。
<<< END U006994 >>>
<<< UNIT U006995 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:106-112 | ctx=MigrationContext.fetch_all >>>
执行查询并取回全部行。

:param sql: SQL 查询。
:param params: 位置参数。
:return: 行字典列表。
<<< END U006995 >>>
<<< UNIT U006996 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:118-123 | ctx=MigrationContext.has_table >>>
判断表是否存在。

:param table: 表名。
:return: 是否存在。
<<< END U006996 >>>
<<< UNIT U006997 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:136-142 | ctx=MigrationContext.has_column >>>
判断列是否存在，表不存在时同样返回 False。

:param table: 表名。
:param column: 列名。
:return: 是否存在。
<<< END U006997 >>>
<<< UNIT U006998 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:154-162 | ctx=MigrationContext.column_is_nullable >>>
判断列是否可为空。

用于“收紧或放宽约束”这类无法靠列名判断是否已完成的步骤。

:param table: 表名。
:param column: 列名。
:return: 列可空或不存在时为 True。
<<< END U006998 >>>
<<< UNIT U006999 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:177-186 | ctx=MigrationContext.has_index >>>
判断指定列上是否已有索引，该列是任一索引的首列即算。

按列而非按索引名判断，因为新建的库由 ``generate_schemas`` 依模型声明创建索引，索引名由 ORM
生成，与迁移里显式指定的名字不同。按名字判断会为已有索引的库重复创建一份。

:param table: 表名。
:param column: 列名。
:return: 是否存在。
<<< END U006999 >>>
<<< UNIT U007000 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:204-212 | ctx=MigrationContext.add_column >>>
新增列。

:param table: 表名。
:param column: 列名。
:param ddl_type: 列类型，如 ``VARCHAR(1024)``。
:param null: 是否允许为空。
:param default: 默认值表达式，省略时不写 ``DEFAULT``。
<<< END U007000 >>>
<<< UNIT U007001 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:220-225 | ctx=MigrationContext.drop_column >>>
删除列。

:param table: 表名。
:param column: 列名。
<<< END U007001 >>>
<<< UNIT U007002 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:229-238 | ctx=MigrationContext.rename_column >>>
修改列名。

MySQL 的 ``CHANGE COLUMN`` 必须重复列类型，且向下兼容到 8.0 以下版本，故统一使用它。

:param table: 表名。
:param old: 旧列名。
:param new: 新列名。
:param ddl_type: 新列在 MySQL 上的完整类型，如 ``VARCHAR(512) NOT NULL``。
<<< END U007002 >>>
<<< UNIT U007003 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:247-252 | ctx=MigrationContext.rename_table >>>
修改表名。

:param old: 旧表名。
:param new: 新表名。
<<< END U007003 >>>
<<< UNIT U007004 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:256-264 | ctx=MigrationContext.create_index >>>
创建索引。

调用方须先以 :meth:`has_index` 探测，因为 MySQL 不支持 ``CREATE INDEX IF NOT EXISTS``。

:param table: 表名。
:param columns: 参与索引的列。
:param name: 索引名。
<<< END U007004 >>>
<<< UNIT U007005 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:269-269 | ctx=MigrationContext.generate_schemas >>>
生成迁移用的表结构。
<<< END U007005 >>>
<<< UNIT U007006 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:280-290 | ctx=MigrationModule >>>
一条已加载的迁移。

:param package: 所属包名。
:param revision: revision 标识符。
:param path: 迁移文件路径。
:param checksum: 文件源码的 sha256。
:param depends_on: 同包内须先执行的 revision。
:param upgrade: 升级函数。
:param downgrade: 回退函数，未声明时为 ``None``。
<<< END U007006 >>>
<<< UNIT U007007 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:306-315 | ctx=load_migration >>>
加载一个迁移文件。

按文件路径加载而非按包名导入，因为包名与目录布局在拆包前后不同，路径是唯一稳定的标识。

:param package: 所属包名。
:param path: 迁移文件路径。
:return: 迁移对象。
:raises MigrationError: 文件缺少可调用入口或元数据不合法。
<<< END U007007 >>>
<<< UNIT U007008 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:353-360 | ctx=order_migrations >>>
按 ``DEPENDS_ON`` 拓扑排序，未声明依赖时按 revision 字典序。

:param package: 包名。
:param modules: 该包的迁移。
:return: 可依次执行的顺序。
:raises MigrationError: revision 重名、依赖缺失或成环。
<<< END U007008 >>>
<<< UNIT U007009 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:393-393 | ctx=MigrationRunner >>>
迁移的发现、注册与执行。
<<< END U007009 >>>
<<< UNIT U007010 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:397-403 | ctx=MigrationRunner.discover >>>
发现 core 与各模块包的迁移。

模块包不存在时其迁移目录不存在，对应的 revision 不会被发现，其表也不会被触碰。

:return: 包名到有序迁移列表的映射。
<<< END U007010 >>>
<<< UNIT U007011 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:428-432 | ctx=MigrationRunner.pending >>>
获取尚未应用的 revision。

:return: 包名到待应用 revision 的映射，无待应用项时为空字典。
<<< END U007011 >>>
<<< UNIT U007012 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:470-475 | ctx=MigrationRunner.upgrade >>>
执行待应用的 revision。

:param package: 只执行该包，省略时执行全部包。
:return: 已应用的 ``(包名, revision)`` 列表。
<<< END U007012 >>>
<<< UNIT U007013 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:491-498 | ctx=MigrationRunner.downgrade >>>
回退该包已应用的 revision。

:param package: 包名。
:param to: 回退到该 revision 为止（保留它），省略时全部回退。
:return: 已回退的 ``(包名, revision)`` 列表。
:raises MigrationError: revision 未声明 ``downgrade``，或 ``to`` 不存在。
<<< END U007013 >>>
<<< UNIT U007014 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:522-530 | ctx=MigrationRunner.stamp >>>
标记 revision 为已应用而不执行。

供旧数据库版本号转换与显式跳过使用。包不存在时其 revision 不会被发现，此处仍正常写入记录，
以便日后安装该包时不再重放这些历史步骤。

:param package: 包名。
:param revisions: revision 列表。
<<< END U007014 >>>
<<< UNIT U007015 | py-docstring | packages/akari-bot-core/akaribot/core/database/migration.py:579-579 | ctx=run_startup_migrations >>>
启动期迁移入口，先转换旧版本号，再执行各包的待应用 revision。
<<< END U007015 >>>
<<< UNIT U007016 | py-docstring | packages/akari-bot-core/akaribot/core/database/migrations/0001_initial.py:16-20 | ctx=upgrade >>>
基准迁移，无实际变更。

:param ctx: 迁移上下文。
<<< END U007016 >>>
<<< UNIT U007017 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0002_banned_users_and_nullable_sender.py:14-14 >>>
# 旧数据库此时仍是 target_info。若表已改名为 target_union_info，说明数据库已越过本步骤。
<<< END U007017 >>>
<<< UNIT U007018 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0002_banned_users_and_nullable_sender.py:88-88 >>>
# 为场景表增设封禁用户列。
<<< END U007018 >>>
<<< UNIT U007019 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0002_banned_users_and_nullable_sender.py:100-100 >>>
# 放宽统计表的发送者列。
<<< END U007019 >>>
<<< UNIT U007020 | py-docstring | packages/akari-bot-core/akaribot/core/database/migrations/0002_banned_users_and_nullable_sender.py:78-82 | ctx=upgrade >>>
执行 v2 变更。

:param ctx: 迁移上下文。
<<< END U007020 >>>
<<< UNIT U007021 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:16-16 >>>
# 旧名到新名。表若已由 generate_schemas 按新模型创建，须先移除这张空表再改名。
<<< END U007021 >>>
<<< UNIT U007022 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:22-22 >>>
# 主键列改为 union_id。旧数据的 union ID 沿用原平台 ID，故只需改名。
<<< END U007022 >>>
<<< UNIT U007023 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:28-28 >>>
# 统计与审计表保留原始 ID，另增 union 列用于聚合。
<<< END U007023 >>>
<<< UNIT U007024 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:31-32 >>>
# 轮询与区间统计所需的索引，因为 job_queues 每 100 毫秒被轮询，analytics_data 要按区间反复聚合，
# 两者都会随行数增长退化为全表扫描。v5 已重建 job_queues，故创建索引前须确认目标列仍在。
<<< END U007024 >>>
<<< UNIT U007025 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:57-57 >>>
# 核心表改用 union 命名。
<<< END U007025 >>>
<<< UNIT U007026 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:70-70 >>>
# 把核心表的主键列改名为 union_id。
<<< END U007026 >>>
<<< UNIT U007027 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:79-81 >>>
# 为绑定行补上消息通道编号并按组顺延。
# 通道编号须在组内逐个顺延，若一律保留默认值，同一 union 下的全部场景会被判定为同一条消息
# 通道，命令与推送将相互去重，导致场景不再有消息送达。
<<< END U007027 >>>
<<< UNIT U007028 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:88-88 >>>
# 后续 revision 追加的列此时尚不存在，整行保存会因缺少列被判定为 partial。
<<< END U007028 >>>
<<< UNIT U007029 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:93-94 >>>
# 旧版 connect 把互认记录存为扁平列表，无法反向查询某条记录属于哪个场景，解绑时也就无从删除。
# 该结构已改为两级字典，旧值直接清除，重新执行一次 ``bind auto`` 即可。
<<< END U007029 >>>
<<< UNIT U007030 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:102-102 >>>
# 为统计与审计表增设 union 列并回填。
<<< END U007030 >>>
<<< UNIT U007031 | py-comment | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:115-115 >>>
# 为轮询与区间统计补充创建索引。
<<< END U007031 >>>
<<< UNIT U007032 | py-docstring | packages/akari-bot-core/akaribot/core/database/migrations/0003_union_core.py:40-46 | ctx=upgrade >>>
执行 v3 的核心变更。

模块表的列改名由各模块包自己的 revision 完成，core 不记录模块表名。

:param ctx: 迁移上下文。
<<< END U007032 >>>
<<< UNIT U007033 | py-docstring | packages/akari-bot-core/akaribot/core/database/migrations/0005_rebuild_job_queues.py:17-23 | ctx=upgrade >>>
丢弃旧任务队列表并重建。

``DROP TABLE IF EXISTS`` 与以 safe 模式创建数据表都可重复执行，无需额外探测。

:param ctx: 迁移上下文。
<<< END U007033 >>>
<<< UNIT U007034 | py-docstring | packages/akari-bot-core/akaribot/core/database/migrations/0006_push_priority.py:19-25 | ctx=upgrade >>>
补充推送优先级列。

``ALTER TABLE ... ADD COLUMN`` 在不同方言下均不支持 ``IF NOT EXISTS``，故先探测再执行。

:param ctx: 迁移上下文。
<<< END U007034 >>>
<<< UNIT U007035 | py-docstring | packages/akari-bot-core/akaribot/core/database/migrations/__init__.py:1-1 | ctx=<module> >>>
core 自身的数据库迁移。
<<< END U007035 >>>
