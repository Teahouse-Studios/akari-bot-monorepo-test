# 全仓可读文本审核稿 · 第 13 册 / 共 20 册

覆盖 U008594–U009156，68 个文件、563 个单元、33,600 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-core/akaribot/core/server/run.py` | 5 | U008594–U008598 | 314 |
| `packages/akari-bot-core/akaribot/core/server/terminate.py` | 8 | U008599–U008606 | 530 |
| `packages/akari-bot-core/akaribot/core/smtp.py` | 7 | U008607–U008613 | 134 |
| `packages/akari-bot-core/akaribot/core/types/command/__init__.py` | 1 | U008614–U008614 | 7 |
| `packages/akari-bot-core/akaribot/core/types/module/__init__.py` | 3 | U008615–U008617 | 23 |
| `packages/akari-bot-core/akaribot/core/types/module/component_meta.py` | 8 | U008618–U008625 | 223 |
| `packages/akari-bot-core/akaribot/core/utils/bash.py` | 1 | U008626–U008626 | 40 |
| `packages/akari-bot-core/akaribot/core/utils/button.py` | 13 | U008627–U008639 | 666 |
| `packages/akari-bot-core/akaribot/core/utils/button_runtime.py` | 8 | U008640–U008647 | 105 |
| `packages/akari-bot-core/akaribot/core/utils/cache.py` | 1 | U008648–U008648 | 21 |
| `packages/akari-bot-core/akaribot/core/utils/container.py` | 25 | U008649–U008673 | 318 |
| `packages/akari-bot-core/akaribot/core/utils/cooldown.py` | 8 | U008674–U008681 | 527 |
| `packages/akari-bot-core/akaribot/core/utils/dirty_check.py` | 7 | U008682–U008688 | 202 |
| `packages/akari-bot-core/akaribot/core/utils/font.py` | 6 | U008689–U008694 | 326 |
| `packages/akari-bot-core/akaribot/core/utils/func.py` | 15 | U008695–U008709 | 274 |
| `packages/akari-bot-core/akaribot/core/utils/game.py` | 10 | U008710–U008719 | 285 |
| `packages/akari-bot-core/akaribot/core/utils/http.py` | 1 | U008720–U008720 | 33 |
| `packages/akari-bot-core/akaribot/core/utils/image.py` | 3 | U008721–U008723 | 163 |
| `packages/akari-bot-core/akaribot/core/utils/image_split.py` | 2 | U008724–U008725 | 62 |
| `packages/akari-bot-core/akaribot/core/utils/image_table.py` | 2 | U008726–U008727 | 184 |
| `packages/akari-bot-core/akaribot/core/utils/media.py` | 4 | U008728–U008731 | 43 |
| `packages/akari-bot-core/akaribot/core/utils/petal.py` | 11 | U008732–U008742 | 439 |
| `packages/akari-bot-core/akaribot/core/utils/process_control.py` | 1 | U008743–U008743 | 23 |
| `packages/akari-bot-core/akaribot/core/utils/random.py` | 14 | U008744–U008757 | 790 |
| `packages/akari-bot-core/akaribot/core/utils/retired.py` | 27 | U008758–U008784 | 1,854 |
| `packages/akari-bot-core/akaribot/core/utils/s3.py` | 8 | U008785–U008792 | 400 |
| `packages/akari-bot-core/akaribot/core/utils/session.py` | 1 | U008793–U008793 | 50 |
| `packages/akari-bot-core/akaribot/core/utils/storedata.py` | 2 | U008794–U008795 | 16 |
| `packages/akari-bot-core/akaribot/core/utils/table.py` | 5 | U008796–U008800 | 295 |
| `packages/akari-bot-core/akaribot/core/utils/timezone.py` | 7 | U008801–U008807 | 96 |
| `packages/akari-bot-core/akaribot/core/utils/url_audit.py` | 19 | U008808–U008826 | 392 |
| `packages/akari-bot-core/akaribot/core/utils/web_render.py` | 4 | U008827–U008830 | 136 |
| `packages/akari-bot-core/akaribot/modules/core/admin_tools/__init__.py` | 1 | U008831–U008831 | 11 |
| `packages/akari-bot-core/akaribot/modules/core/admin_tools/admin.py` | 2 | U008832–U008833 | 105 |
| `packages/akari-bot-core/akaribot/modules/core/admin_tools/alias.py` | 2 | U008834–U008835 | 28 |
| `packages/akari-bot-core/akaribot/modules/core/admin_tools/locale.py` | 3 | U008836–U008838 | 48 |
| `packages/akari-bot-core/akaribot/modules/core/admin_tools/modules.py` | 4 | U008839–U008842 | 177 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/__init__.py` | 1 | U008843–U008843 | 20 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py` | 8 | U008844–U008851 | 197 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py` | 20 | U008852–U008871 | 1,675 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/about.py` | 3 | U008872–U008874 | 80 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py` | 36 | U008875–U008910 | 2,115 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/help.py` | 17 | U008911–U008927 | 1,912 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py` | 16 | U008928–U008943 | 1,226 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/petal.py` | 1 | U008944–U008944 | 14 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/ping.py` | 1 | U008945–U008945 | 36 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py` | 11 | U008946–U008956 | 1,330 |
| `packages/akari-bot-core/akaribot/modules/core/common_tools/version.py` | 1 | U008957–U008957 | 26 |
| `packages/akari-bot-core/akaribot/modules/core/docs/about.md` | 13 | U008958–U008970 | 1,167 |
| `packages/akari-bot-core/akaribot/modules/core/docs/abuse.md` | 23 | U008971–U008993 | 1,507 |
| `packages/akari-bot-core/akaribot/modules/core/docs/admin.md` | 15 | U008994–U009008 | 1,107 |
| `packages/akari-bot-core/akaribot/modules/core/docs/analytics.md` | 10 | U009009–U009018 | 693 |
| `packages/akari-bot-core/akaribot/modules/core/docs/auth.md` | 7 | U009019–U009025 | 580 |
| `packages/akari-bot-core/akaribot/modules/core/docs/bind.md` | 27 | U009026–U009052 | 2,485 |
| `packages/akari-bot-core/akaribot/modules/core/docs/config.md` | 9 | U009053–U009061 | 666 |
| `packages/akari-bot-core/akaribot/modules/core/docs/database.md` | 6 | U009062–U009067 | 241 |
| `packages/akari-bot-core/akaribot/modules/core/docs/echo.md` | 3 | U009068–U009070 | 175 |
| `packages/akari-bot-core/akaribot/modules/core/docs/eval.md` | 2 | U009071–U009072 | 143 |
| `packages/akari-bot-core/akaribot/modules/core/docs/features.md` | 3 | U009073–U009075 | 296 |
| `packages/akari-bot-core/akaribot/modules/core/docs/help.md` | 18 | U009076–U009093 | 1,596 |
| `packages/akari-bot-core/akaribot/modules/core/docs/jobqueue.md` | 3 | U009094–U009096 | 108 |
| `packages/akari-bot-core/akaribot/modules/core/docs/merge.md` | 5 | U009097–U009101 | 309 |
| `packages/akari-bot-core/akaribot/modules/core/docs/module.md` | 19 | U009102–U009120 | 1,392 |
| `packages/akari-bot-core/akaribot/modules/core/docs/mute.md` | 3 | U009121–U009123 | 192 |
| `packages/akari-bot-core/akaribot/modules/core/docs/parser_errors.md` | 5 | U009124–U009128 | 449 |
| `packages/akari-bot-core/akaribot/modules/core/docs/parser_policies.md` | 3 | U009129–U009131 | 648 |
| `packages/akari-bot-core/akaribot/modules/core/docs/parser_routing.md` | 2 | U009132–U009133 | 202 |
| `packages/akari-bot-core/akaribot/modules/core/docs/petal.md` | 23 | U009134–U009156 | 1,673 |

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
<<< UNIT U008594 | py-comment | packages/akari-bot-core/akaribot/core/server/run.py:43-44 >>>
# 重启提示须等待发起者所在客户端完成节点注册，且投递自身依赖队列结果泵，
# 故置于当前 Server 注册 ready 并开始轮询之后。
<<< END U008594 >>>
<<< UNIT U008595 | py-comment | packages/akari-bot-core/akaribot/core/server/run.py:47-48 >>>
# 队列轮询是 Server 的生命线。它若因数据库或代码异常退出而主循环仍继续，
# 进程会表现为在线却不再收发任何消息，守护进程也无法察觉并重启。
<<< END U008595 >>>
<<< UNIT U008596 | py-comment | packages/akari-bot-core/akaribot/core/server/run.py:59-60 >>>
# cleanup_sessions 会在释放依赖 Queue 的后台 context 后停止 poller。初始化在
# poller 建立前失败时，仍需在此取消已创建的局部任务。
<<< END U008596 >>>
<<< UNIT U008597 | py-docstring | packages/akari-bot-core/akaribot/core/server/run.py:1-8 | ctx=<module> >>>
服务器主运行模块。

该模块是服务器的入口点，负责：
- 设置信号处理器（捕获 Ctrl+C）
- 启动服务器主循环
- 初始化队列处理
<<< END U008597 >>>
<<< UNIT U008598 | py-docstring | packages/akari-bot-core/akaribot/core/server/run.py:33-33 | ctx=main >>>
服务器主函数。
<<< END U008598 >>>
<<< UNIT U008599 | py-comment | packages/akari-bot-core/akaribot/core/server/terminate.py:23-24 >>>
# 先关闭新 action 入口并与已经开始认领的一轮轮询建立屏障。轮询器仍继续回收
# 执行中 RPC 的远端结果，供下面取消任务时释放平台 context。
<<< END U008599 >>>
<<< UNIT U008600 | py-comment | packages/akari-bot-core/akaribot/core/server/terminate.py:26-27 >>>
# Queue handler 可能持有 Scheduler 维护锁，也可能在退出路径创建 detached task。
# 先取消并等待它们，再关闭 Scheduler，最后统一清理所有已注册后台任务。
<<< END U008600 >>>
<<< UNIT U008601 | py-comment | packages/akari-bot-core/akaribot/core/server/terminate.py:38-39 >>>
# 注册项可能持有 MessageSession context，须在停止 poller 之前取消。
# 只有实际导入过的组件会注册，关闭阶段不为清理额外导入模块。
<<< END U008601 >>>
<<< UNIT U008602 | py-comment | packages/akari-bot-core/akaribot/core/server/terminate.py:41-43 >>>
# restart() 可能由 Queue action 自身触发，此时主循环的轮询器仍在运行。关闭窗口
# 必须先阻止它继续认领任务，再取消其他 handler，并在独占轮询锁时关闭资源。
# 不能清空全局队列表，因为同一 service 的其他 Server 实例仍可能依赖其中的任务。
<<< END U008602 >>>
<<< UNIT U008603 | py-comment | packages/akari-bot-core/akaribot/core/server/terminate.py:45-46 >>>
# detached task 的 context 已经释放，此后不再需要轮询远端结果。先停止轮询器，
# 再在持有 _poll_lock 的情况下关闭依赖，避免窗口退出后轮询已关闭的数据库。
<<< END U008603 >>>
<<< UNIT U008604 | py-docstring | packages/akari-bot-core/akaribot/core/server/terminate.py:1-1 | ctx=<module> >>>
服务器清理和重启模块。
<<< END U008604 >>>
<<< UNIT U008605 | py-docstring | packages/akari-bot-core/akaribot/core/server/terminate.py:19-19 | ctx=cleanup_sessions >>>
清理服务器资源。
<<< END U008605 >>>
<<< UNIT U008606 | py-docstring | packages/akari-bot-core/akaribot/core/server/terminate.py:61-61 | ctx=restart >>>
重启服务器。
<<< END U008606 >>>
<<< UNIT U008607 | py-comment | packages/akari-bot-core/akaribot/core/smtp.py:17-17 >>>
# 品牌资产包优先，实例 assets/ 可覆盖。两处都没有时为 None，此时不内嵌标志。
<<< END U008607 >>>
<<< UNIT U008608 | py-comment | packages/akari-bot-core/akaribot/core/smtp.py:68-68 >>>
# 纯文本版本
<<< END U008608 >>>
<<< UNIT U008609 | py-comment | packages/akari-bot-core/akaribot/core/smtp.py:71-71 >>>
# HTML 版本
<<< END U008609 >>>
<<< UNIT U008610 | py-comment | packages/akari-bot-core/akaribot/core/smtp.py:74-74 >>>
# 内嵌 Logo。品牌资产缺失时跳过，邮件正文本身正常发出。
<<< END U008610 >>>
<<< UNIT U008611 | py-docstring | packages/akari-bot-core/akaribot/core/smtp.py:25-25 | ctx=email_report_enabled >>>
检查邮件报告是否启用。
<<< END U008611 >>>
<<< UNIT U008612 | py-docstring | packages/akari-bot-core/akaribot/core/smtp.py:56-56 | ctx=send_email >>>
发送邮件报告。
<<< END U008612 >>>
<<< UNIT U008613 | py-docstring | packages/akari-bot-core/akaribot/core/smtp.py:107-107 | ctx=send_report >>>
将上报发送到 SMTP 邮件或配置的上报场景。
<<< END U008613 >>>
<<< UNIT U008614 | py-docstring | packages/akari-bot-core/akaribot/core/types/command/__init__.py:5-5 | ctx=Param >>>
命令参数定义。
<<< END U008614 >>>
<<< UNIT U008615 | py-docstring | packages/akari-bot-core/akaribot/core/types/module/__init__.py:23-23 | ctx=Module >>>
已加载模块的信息。
<<< END U008615 >>>
<<< UNIT U008616 | py-docstring | packages/akari-bot-core/akaribot/core/types/module/__init__.py:55-55 | ctx=Module.assign >>>
复制模块字段。
<<< END U008616 >>>
<<< UNIT U008617 | py-docstring | packages/akari-bot-core/akaribot/core/types/module/__init__.py:62-62 | ctx=Module.to_dict >>>
返回模块字典。
<<< END U008617 >>>
<<< UNIT U008618 | py-comment | packages/akari-bot-core/akaribot/core/types/module/component_meta.py:22-22 >>>
# 注册组件时必定传入处理函数，默认值仅为满足 attrs 的字段顺序要求
<<< END U008618 >>>
<<< UNIT U008619 | py-comment | packages/akari-bot-core/akaribot/core/types/module/component_meta.py:56-56 >>>
# 注册阶段编译好的模式，避免每条消息都去 re 模块的全局缓存里查一次
<<< END U008619 >>>
<<< UNIT U008620 | py-comment | packages/akari-bot-core/akaribot/core/types/module/component_meta.py:62-62 >>>
# 已编译的模式无法再附加 flags，附加会在此后的每次匹配中抛出异常
<<< END U008620 >>>
<<< UNIT U008621 | py-comment | packages/akari-bot-core/akaribot/core/types/module/component_meta.py:81-81 >>>
# 入口订阅字段。带名称的 hook 保持默认即可
<<< END U008621 >>>
<<< UNIT U008622 | py-comment | packages/akari-bot-core/akaribot/core/types/module/component_meta.py:87-87 >>>
# 单次执行预算（秒）。<=0 表示不限时
<<< END U008622 >>>
<<< UNIT U008623 | py-comment | packages/akari-bot-core/akaribot/core/types/module/component_meta.py:89-89 >>>
# server 作用域免受场景 enabled_modules 约束，但仍受全局停用状态与平台范围限制
<<< END U008623 >>>
<<< UNIT U008624 | py-docstring | packages/akari-bot-core/akaribot/core/types/module/component_meta.py:23-23 | ctx=CommandMeta >>>
命令的元数据。
<<< END U008624 >>>
<<< UNIT U008625 | py-docstring | packages/akari-bot-core/akaribot/core/types/module/component_meta.py:77-77 | ctx=HookMeta >>>
模块 hook 元数据。
<<< END U008625 >>>
<<< UNIT U008626 | py-comment | packages/akari-bot-core/akaribot/core/utils/bash.py:18-18 >>>
# communicate() 返回后进程已结束。默认值仅用于满足返回类型约定。
<<< END U008626 >>>
<<< UNIT U008627 | py-comment | packages/akari-bot-core/akaribot/core/utils/button.py:15-15 >>>
# 平台单行按钮数量的硬上限
<<< END U008627 >>>
<<< UNIT U008628 | py-comment | packages/akari-bot-core/akaribot/core/utils/button.py:18-18 >>>
# 平台按钮行数的硬上限
<<< END U008628 >>>
<<< UNIT U008629 | py-comment | packages/akari-bot-core/akaribot/core/utils/button.py:21-21 >>>
# 可读性上限，即默认的每行按钮数量
<<< END U008629 >>>
<<< UNIT U008630 | py-comment | packages/akari-bot-core/akaribot/core/utils/button.py:24-24 >>>
# MessageChain 自动排布单个 Button 时，每行的按钮数量
<<< END U008630 >>>
<<< UNIT U008631 | py-comment | packages/akari-bot-core/akaribot/core/utils/button.py:27-27 >>>
# MessageChain 自动排布单个 Button 时，允许生成的最大行数
<<< END U008631 >>>
<<< UNIT U008632 | py-comment | packages/akari-bot-core/akaribot/core/utils/button.py:66-66 >>>
# 余数均摊到靠前的几行，使各行数量至多相差一个
<<< END U008632 >>>
<<< UNIT U008633 | py-comment | packages/akari-bot-core/akaribot/core/utils/button.py:105-105 >>>
# 将旧版内嵌编码立即规范化，之后各平台只读取语义字段。
<<< END U008633 >>>
<<< UNIT U008634 | py-comment | packages/akari-bot-core/akaribot/core/utils/button.py:124-124 >>>
# 兼容显式 callback_id 但消息内没有按钮的既有调用。
<<< END U008634 >>>
<<< UNIT U008635 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button.py:1-1 | ctx=<module> >>>
按钮排布工具 - 将扁平的按钮序列整理为消息底部键盘所需的按行结构。
<<< END U008635 >>>
<<< UNIT U008636 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button.py:37-48 | ctx=arrange_buttons >>>
将（展示文本，点击数据）序列整理为 ``ButtonFrame`` 所需的按钮行。

行数由 ``per_row`` 计算后即固定，再把按钮均分到各行，使各行的数量至多相差一个——
直接按 ``per_row`` 切片会得到 ``[3, 3, 3, 1]`` 这样参差的末行。行数超出平台上限时
压回上限，此时每行的数量将突破 ``per_row``，至多到 ``MAX_BUTTONS_PER_ROW``。

:param buttons: （标签，命令）序列。标签为按钮上展示的文本，命令为点击后发出的内容。
:param per_row: 每行按钮数量的可读性上限。
:param small: 是否使用紧凑按钮样式。
:return: 按钮行列表。输入为空时返回空列表。
<<< END U008636 >>>
<<< UNIT U008637 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button.py:75-75 | ctx=build_button_rows >>>
把旧式的按行映射转换为类型化按钮行。
<<< END U008637 >>>
<<< UNIT U008638 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button.py:100-100 | ctx=bind_callback_reply_ids >>>
为消息中的按钮绑定 callback 使用的虚拟 ``reply_id``。
<<< END U008638 >>>
<<< UNIT U008639 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button.py:131-131 | ctx=public_button_reply_ids >>>
返回消息中允许所有人点击的按钮 callback ID。
<<< END U008639 >>>
<<< UNIT U008640 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button_runtime.py:1-1 | ctx=<module> >>>
跨平台按钮 token 的注册与消费。
<<< END U008640 >>>
<<< UNIT U008641 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button_runtime.py:18-18 | ctx=ButtonState >>>
按钮的当前状态。
<<< END U008641 >>>
<<< UNIT U008642 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button_runtime.py:30-30 | ctx=RegisteredButton >>>
已注册的按钮。
<<< END U008642 >>>
<<< UNIT U008643 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button_runtime.py:38-38 | ctx=ButtonConsumeStatus >>>
按钮回调处理结果。
<<< END U008643 >>>
<<< UNIT U008644 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button_runtime.py:49-49 | ctx=ButtonConsumeResult >>>
按钮回调的处理结果。
<<< END U008644 >>>
<<< UNIT U008645 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button_runtime.py:68-68 | ctx=register_button_rows >>>
注册按钮行并返回平台可用的短 token。
<<< END U008645 >>>
<<< UNIT U008646 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button_runtime.py:97-97 | ctx=consume_button >>>
校验并核销一个按钮 token。
<<< END U008646 >>>
<<< UNIT U008647 | py-docstring | packages/akari-bot-core/akaribot/core/utils/button_runtime.py:121-121 | ctx=normalize_button_payload >>>
将平台确认按钮转换为现有确认文本。
<<< END U008647 >>>
<<< UNIT U008648 | py-docstring | packages/akari-bot-core/akaribot/core/utils/cache.py:8-10 | ctx=random_cache_path >>>
提供带有随机 UUID 文件名的缓存路径。
<<< END U008648 >>>
<<< UNIT U008649 | py-comment | packages/akari-bot-core/akaribot/core/utils/container.py:59-60 >>>
# 这里仅存弱引用，因为记录表只为定期清理服务。若持强引用，任何已记录的容器都永远无法被回收，
# 冷却、绑定码这类按“场景 × 键”不断新建的容器会让它无上限增长。
<<< END U008649 >>>
<<< UNIT U008650 | py-comment | packages/akari-bot-core/akaribot/core/utils/container.py:147-147 >>>
# 同时移除失效的弱引用，避免记录表持续增长。
<<< END U008650 >>>
<<< UNIT U008651 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:9-9 | ctx=TokenBucket >>>
令牌桶限流器。
<<< END U008651 >>>
<<< UNIT U008652 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:23-23 | ctx=TokenBucket.consume >>>
消耗令牌。
<<< END U008652 >>>
<<< UNIT U008653 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:31-31 | ctx=TokenBucket.peek >>>
查看当前令牌数。
<<< END U008653 >>>
<<< UNIT U008654 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:36-36 | ctx=TokenBucket.wait_time >>>
返回等待下一个令牌的秒数。
<<< END U008654 >>>
<<< UNIT U008655 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:43-43 | ctx=TokenBucket.refill >>>
补充令牌。
<<< END U008655 >>>
<<< UNIT U008656 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:55-55 | ctx=ExpiringTempDict >>>
带过期时间的字典。
<<< END U008656 >>>
<<< UNIT U008657 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:110-110 | ctx=ExpiringTempDict.is_expired >>>
判断键是否过期。
<<< END U008657 >>>
<<< UNIT U008658 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:115-115 | ctx=ExpiringTempDict.refresh >>>
刷新键的过期时间。
<<< END U008658 >>>
<<< UNIT U008659 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:120-123 | ctx=ExpiringTempDict.clear_expired >>>
清除内部过期数据。
返回 True 表示自身可被外层删除。
<<< END U008659 >>>
<<< UNIT U008660 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:142-142 | ctx=ExpiringTempDict.clear_all >>>
删除所有键并清空过期时间。
<<< END U008660 >>>
<<< UNIT U008661 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:162-162 | ctx=ExpiringTempDict.to_dict >>>
返回普通字典。
<<< END U008661 >>>
<<< UNIT U008662 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:176-176 | ctx=ExpiringTempDict.from_dict >>>
从字典构造实例。
<<< END U008662 >>>
<<< UNIT U008663 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:188-188 | ctx=ExpiringTempDict.clear >>>
删除所有键。
<<< END U008663 >>>
<<< UNIT U008664 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:193-193 | ctx=ExpiringTempDict.copy >>>
返回浅拷贝。
<<< END U008664 >>>
<<< UNIT U008665 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:201-201 | ctx=ExpiringTempDict.fromkeys >>>
按给定键创建实例。
<<< END U008665 >>>
<<< UNIT U008666 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:209-209 | ctx=ExpiringTempDict.get >>>
按键读取值。
<<< END U008666 >>>
<<< UNIT U008667 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:224-224 | ctx=ExpiringTempDict.keys >>>
返回键视图。
<<< END U008667 >>>
<<< UNIT U008668 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:228-228 | ctx=ExpiringTempDict.values >>>
返回值视图。
<<< END U008668 >>>
<<< UNIT U008669 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:232-232 | ctx=ExpiringTempDict.items >>>
返回键值对视图。
<<< END U008669 >>>
<<< UNIT U008670 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:236-236 | ctx=ExpiringTempDict.pop >>>
按键删除并返回值。
<<< END U008670 >>>
<<< UNIT U008671 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:241-241 | ctx=ExpiringTempDict.popitem >>>
删除并返回最后一个键值对。
<<< END U008671 >>>
<<< UNIT U008672 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:246-246 | ctx=ExpiringTempDict.setdefault >>>
读取键，不存在时写入默认值。
<<< END U008672 >>>
<<< UNIT U008673 | py-docstring | packages/akari-bot-core/akaribot/core/utils/container.py:251-251 | ctx=ExpiringTempDict.update >>>
批量写入键值对。
<<< END U008673 >>>
<<< UNIT U008674 | py-comment | packages/akari-bot-core/akaribot/core/utils/cooldown.py:23-24 >>>
# 场景维度按消息通道划分，因为仅共享 union 而通道编号不同的场景属于不同的现实场景，
# 不应共用一份冷却。用户维度只按 union，同一个人换平台账号仍受同一份冷却约束。
<<< END U008674 >>>
<<< UNIT U008675 | py-comment | packages/akari-bot-core/akaribot/core/utils/cooldown.py:29-31 >>>
# 获取或创建冷却事件字典。
# 对于单个用户，返回 sender_union_id -> key 的结构。
# 对于 whole_target，返回 channel_key -> key 的结构。
<<< END U008675 >>>
<<< UNIT U008676 | py-comment | packages/akari-bot-core/akaribot/core/utils/cooldown.py:34-34 >>>
# 这些容器嵌在 _cd_dict 之下，清理由根容器递归下来，不必各自记录为根项
<<< END U008676 >>>
<<< UNIT U008677 | py-comment | packages/akari-bot-core/akaribot/core/utils/cooldown.py:46-47 >>>
# 与 :meth:`_get_cd_dict` 不同，这里不创建缺失的层级，故能区分“从未使用过”与“冷却已结束”。
# 容器在过期后经代理方法取值会先清理再刷新时间戳，等于把冷却续上，故直接读底层字典。
<<< END U008677 >>>
<<< UNIT U008678 | py-comment | packages/akari-bot-core/akaribot/core/utils/cooldown.py:72-72 >>>
# 记录只在 reset() 时创建，其 exp 即冷却时长、ts 即上次重置时刻。
<<< END U008678 >>>
<<< UNIT U008679 | py-docstring | packages/akari-bot-core/akaribot/core/utils/cooldown.py:10-16 | ctx=CoolDown >>>
冷却事件构造器。
:param key: 冷却事件名称
:param msg: 消息会话
:param delay: 冷却时间（秒）
:param whole_target: 是否应用至整个场景（默认为 False）
<<< END U008679 >>>
<<< UNIT U008680 | py-docstring | packages/akari-bot-core/akaribot/core/utils/cooldown.py:65-68 | ctx=CoolDown.check >>>
检查冷却事件剩余时间。
:return: 剩余冷却时间（秒），0 表示已可用
<<< END U008680 >>>
<<< UNIT U008681 | py-docstring | packages/akari-bot-core/akaribot/core/utils/cooldown.py:77-77 | ctx=CoolDown.reset >>>
重置冷却事件。
<<< END U008681 >>>
<<< UNIT U008682 | py-comment | packages/akari-bot-core/akaribot/core/utils/dirty_check.py:55-55 >>>
# 向后最多回退 50 字符找一个自然断点
<<< END U008682 >>>
<<< UNIT U008683 | py-comment | packages/akari-bot-core/akaribot/core/utils/dirty_check.py:126-126 >>>
# 命中 AT / KE / I18N 结构部分时跳过，或与已替换区间重叠时跳过
<<< END U008683 >>>
<<< UNIT U008684 | py-comment | packages/akari-bot-core/akaribot/core/utils/dirty_check.py:167-167 >>>
# 未记录分片长度的历史缓存按定长切片还原。
<<< END U008684 >>>
<<< UNIT U008685 | py-comment | packages/akari-bot-core/akaribot/core/utils/dirty_check.py:205-205 >>>
# 未分片的历史缓存保存的是整条文本的检测结果。
<<< END U008685 >>>
<<< UNIT U008686 | py-comment | packages/akari-bot-core/akaribot/core/utils/dirty_check.py:226-226 >>>
# 单条 task 最多检测 10000 字符，超出会被接口拒绝。
<<< END U008686 >>>
<<< UNIT U008687 | py-docstring | packages/akari-bot-core/akaribot/core/utils/dirty_check.py:1-1 | ctx=<module> >>>
检查字符串是否合规，支持阿里云内容安全与自定义关键词过滤。
<<< END U008687 >>>
<<< UNIT U008688 | py-docstring | packages/akari-bot-core/akaribot/core/utils/dirty_check.py:43-43 | ctx=split_text >>>
把文本按 size 切块，尽量在标点/换行处断开，避免切断关键词。
<<< END U008688 >>>
<<< UNIT U008689 | py-comment | packages/akari-bot-core/akaribot/core/utils/font.py:16-16 >>>
# 字体资源包与用户自备字体的目录名。资源包通过 ``fonts_dir()`` 声明资源根目录，此处不假定其内部布局。
<<< END U008689 >>>
<<< UNIT U008690 | py-comment | packages/akari-bot-core/akaribot/core/utils/font.py:20-20 >>>
# CJK 字族候选按序取首个命中，Docker 镜像装的 fonts-noto-cjk 在最前，其后是各平台自带字面。
<<< END U008690 >>>
<<< UNIT U008691 | py-comment | packages/akari-bot-core/akaribot/core/utils/font.py:36-36 >>>
# 符号字族候选只收同类字族，避免回退到缺少汉字字形的默认字族时把中文渲染成方框。
<<< END U008691 >>>
<<< UNIT U008692 | py-comment | packages/akari-bot-core/akaribot/core/utils/font.py:39-39 >>>
# 已知字体名到系统字族候选的映射。未收录的名字只在资源包与实例 data 两级查找。
<<< END U008692 >>>
<<< UNIT U008693 | py-comment | packages/akari-bot-core/akaribot/core/utils/font.py:56-56 >>>
# 资源包是可选依赖，故按名称按需导入，出现 ImportError 即视该级不可用，core 的依赖清单不变。
<<< END U008693 >>>
<<< UNIT U008694 | py-comment | packages/akari-bot-core/akaribot/core/utils/font.py:80-80 >>>
# fallback_to_default=False 让未命中时抛出 ValueError，而不是静默回退到 DejaVu Sans。
<<< END U008694 >>>
<<< UNIT U008695 | py-comment | packages/akari-bot-core/akaribot/core/utils/func.py:21-21 >>>
# 取数值真假而非字符串真假，因为字符串 "0" 非空，bool() 会将其判定为 True
<<< END U008695 >>>
<<< UNIT U008696 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:10-10 | ctx=convert_bool >>>
将常见真值/假值转为布尔值，无法识别时返回默认值。
<<< END U008696 >>>
<<< UNIT U008697 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:31-31 | ctx=convert_list >>>
将其他类型转为列表。
<<< END U008697 >>>
<<< UNIT U008698 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:42-42 | ctx=is_iterable >>>
判断对象是否是字符串以外的可迭代对象。
<<< END U008698 >>>
<<< UNIT U008699 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:47-47 | ctx=is_json_serializable >>>
检查对象是否可以被 JSON 序列化。
<<< END U008699 >>>
<<< UNIT U008700 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:56-56 | ctx=chunk_list >>>
将可迭代对象分块，返回生成器。
<<< END U008700 >>>
<<< UNIT U008701 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:76-76 | ctx=unique_list >>>
在不破坏顺序下去重可迭代对象。
<<< END U008701 >>>
<<< UNIT U008702 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:93-93 | ctx=flatten_list >>>
将嵌套可迭代对象扁平化。
<<< END U008702 >>>
<<< UNIT U008703 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:107-107 | ctx=flatten_dict >>>
将嵌套字典扁平化。
<<< END U008703 >>>
<<< UNIT U008704 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:119-119 | ctx=unflatten_dict >>>
将扁平化字典还原。
<<< END U008704 >>>
<<< UNIT U008705 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:133-133 | ctx=is_float >>>
检查对象是否符合 `float` 类型。
<<< END U008705 >>>
<<< UNIT U008706 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:142-142 | ctx=is_int >>>
检查对象是否符合 `int` 类型。
<<< END U008706 >>>
<<< UNIT U008707 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:153-153 | ctx=camel_to_snake >>>
驼峰命名转蛇形命名。
<<< END U008707 >>>
<<< UNIT U008708 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:201-201 | ctx=parse_offset >>>
解析 UTC 偏移量。
<<< END U008708 >>>
<<< UNIT U008709 | py-docstring | packages/akari-bot-core/akaribot/core/utils/func.py:241-241 | ctx=format_offset >>>
将 UTC 偏移量格式化为 ``+8``、``+5:30`` 或 ``-3``。
<<< END U008709 >>>
<<< UNIT U008710 | py-inline-comment | packages/akari-bot-core/akaribot/core/utils/game.py:9-9 >>>
# 游戏事件过期时间（秒）
<<< END U008710 >>>
<<< UNIT U008711 | py-comment | packages/akari-bot-core/akaribot/core/utils/game.py:25-26 >>>
# 按消息通道而非 union 构造键，因为同一 union 下通道编号不同的场景属于不同的现实场景，
# 各自的对局互不相干，合并为一处会让一边开局把另一边也带进游戏中。
<<< END U008711 >>>
<<< UNIT U008712 | py-comment | packages/akari-bot-core/akaribot/core/utils/game.py:32-32 >>>
# 获取场景的游戏事件字典，如果不存在则自动创建。
<<< END U008712 >>>
<<< UNIT U008713 | py-docstring | packages/akari-bot-core/akaribot/core/utils/game.py:15-20 | ctx=PlayState >>>
游戏事件构造器。

:param game: 游戏事件名称。
:param msg: 消息会话。
<<< END U008713 >>>
<<< UNIT U008714 | py-docstring | packages/akari-bot-core/akaribot/core/utils/game.py:37-37 | ctx=PlayState.enable >>>
开启游戏事件。
<<< END U008714 >>>
<<< UNIT U008715 | py-docstring | packages/akari-bot-core/akaribot/core/utils/game.py:46-46 | ctx=PlayState.disable >>>
关闭游戏事件。
<<< END U008715 >>>
<<< UNIT U008716 | py-docstring | packages/akari-bot-core/akaribot/core/utils/game.py:57-57 | ctx=PlayState.running >>>
在当前调用存活期间维护游戏状态，并只清理它开启的这一局。
<<< END U008716 >>>
<<< UNIT U008717 | py-docstring | packages/akari-bot-core/akaribot/core/utils/game.py:67-67 | ctx=PlayState.update >>>
更新游戏事件中需要的值。
<<< END U008717 >>>
<<< UNIT U008718 | py-docstring | packages/akari-bot-core/akaribot/core/utils/game.py:74-74 | ctx=PlayState.check >>>
检查游戏事件状态。
<<< END U008718 >>>
<<< UNIT U008719 | py-docstring | packages/akari-bot-core/akaribot/core/utils/game.py:79-84 | ctx=PlayState.get >>>
获取游戏事件中需要的值。

:param key: 键名。
:param default: 默认值。
<<< END U008719 >>>
<<< UNIT U008720 | py-docstring | packages/akari-bot-core/akaribot/core/utils/http.py:1-1 | ctx=<module> >>>
基于 `httpx` 的互联网请求工具，用于让机器人请求外部网站。
<<< END U008720 >>>
<<< UNIT U008721 | py-comment | packages/akari-bot-core/akaribot/core/utils/image.py:87-88 >>>
# MessageSession 本身不持有 locale，需先取出其 session_info。
# SessionInfo 没有该属性，原样返回
<<< END U008721 >>>
<<< UNIT U008722 | py-comment | packages/akari-bot-core/akaribot/core/utils/image.py:91-92 >>>
# 图片是纯文本载体，无从承载可点击的行内元素，故按不支持 markdown 转换，
# 指令操作等元素会就地降级为纯文本，否则模板认不出它们，其内容会静默丢失
<<< END U008722 >>>
<<< UNIT U008723 | py-docstring | packages/akari-bot-core/akaribot/core/utils/image.py:29-29 | ctx=get_fontsize >>>
计算图片文字字号。
<<< END U008723 >>>
<<< UNIT U008724 | py-docstring | packages/akari-bot-core/akaribot/core/utils/image_split.py:1-1 | ctx=<module> >>>
轻量图片切分工具，避免平台适配器加载完整 WebRender 链路。
<<< END U008724 >>>
<<< UNIT U008725 | py-docstring | packages/akari-bot-core/akaribot/core/utils/image_split.py:9-9 | ctx=image_split >>>
按最大高度切分图片，并及时释放 Pillow 图像资源。
<<< END U008725 >>>
<<< UNIT U008726 | py-docstring | packages/akari-bot-core/akaribot/core/utils/image_table.py:17-22 | ctx=ImageTable >>>
图片表格。

:param data: 表格内容，每行的列数需与表头数量相符。
:param headers: 表格表头。
<<< END U008726 >>>
<<< UNIT U008727 | py-docstring | packages/akari-bot-core/akaribot/core/utils/image_table.py:60-67 | ctx=image_table_render >>>
使用 WebRender 渲染图片表格。

:param table: 要渲染的表格。
:param save_source: 是否保存源文件。
:param dark_mode: 是否使用深色模式渲染。
:return: 图片的 PIL 对象。
<<< END U008727 >>>
<<< UNIT U008728 | py-comment | packages/akari-bot-core/akaribot/core/utils/media.py:184-184 >>>
# 小于等于阈值，无需压缩，直接保留
<<< END U008728 >>>
<<< UNIT U008729 | py-docstring | packages/akari-bot-core/akaribot/core/utils/media.py:64-64 | ctx=compress_image >>>
压缩图片文件。
<<< END U008729 >>>
<<< UNIT U008730 | py-docstring | packages/akari-bot-core/akaribot/core/utils/media.py:102-102 | ctx=compress_audio_video >>>
压缩音视频文件。
<<< END U008730 >>>
<<< UNIT U008731 | py-docstring | packages/akari-bot-core/akaribot/core/utils/media.py:160-160 | ctx=compress_media_chain >>>
压缩消息链中的媒体。
<<< END U008731 >>>
<<< UNIT U008732 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:17-19 >>>
# 花瓣余额关联在 union 上，日额度也须随之跨平台共享，因此存储不按客户端分桶。
# 桶内亦按 union 而非平台账号索引，否则一个人绑几个平台就能领到数倍的每日额度。
# 每日周期按触发场景的时区计算，记录内保存周期偏移，跨场景共用同一条记录。
<<< END U008732 >>>
<<< UNIT U008733 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:34-34 >>>
# 场景时区变更后的首个周期按 24 小时滚动，避免修改时区提前刷新。
<<< END U008733 >>>
<<< UNIT U008734 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:56-56 >>>
# 无用户 union 的会话不持有花瓣，且 union_id 为空会污染存储桶的键
<<< END U008734 >>>
<<< UNIT U008735 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:110-110 >>>
# 与 gained_petal 同理，缺少用户 union 时无从记账
<<< END U008735 >>>
<<< UNIT U008736 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:205-205 >>>
# 签到记录同样关联在 union 上，避免多平台绑定后重复签到。
<<< END U008736 >>>
<<< UNIT U008737 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:215-215 >>>
# 今日已签到，返回 0 由上层提示“明日再试”。
<<< END U008737 >>>
<<< UNIT U008738 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:238-238 >>>
# 分批写入，避免用户量大时单条 UPDATE 超出数据库的语句长度上限。
<<< END U008738 >>>
<<< UNIT U008739 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:264-264 >>>
# 取严格晚于当前时刻的下一次触发时间，确保当前时刻恰好等于触发点时也不会重复结算。
<<< END U008739 >>>
<<< UNIT U008740 | py-comment | packages/akari-bot-core/akaribot/core/utils/petal.py:290-290 >>>
# 周期结算属于后台维护，失败只记录并在下个检查点重试，不中断同批次的其他维护工作。
<<< END U008740 >>>
<<< UNIT U008741 | py-docstring | packages/akari-bot-core/akaribot/core/utils/petal.py:183-183 | ctx=sign_get_petal >>>
执行签到并返回花瓣。
<<< END U008741 >>>
<<< UNIT U008742 | py-docstring | packages/akari-bot-core/akaribot/core/utils/petal.py:255-255 | ctx=reset_petals_if_due >>>
检查并重置到期的花瓣。
<<< END U008742 >>>
<<< UNIT U008743 | py-docstring | packages/akari-bot-core/akaribot/core/utils/process_control.py:11-11 | ctx=listen_for_windows_stop >>>
监听实例停止事件，使主线程执行正常的退出清理。
<<< END U008743 >>>
<<< UNIT U008744 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:136-136 | ctx=Random >>>
随机生成工具。
<<< END U008744 >>>
<<< UNIT U008745 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:143-147 | ctx=Random.random >>>
返回 0 到 1 之间的随机浮点数。

:return: 随机浮点数。
<<< END U008745 >>>
<<< UNIT U008746 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:152-158 | ctx=Random.randint >>>
返回 [a, b] 范围内的随机整数。

:param a: 下界。
:param b: 上界。
:return: 符合条件的随机整数。
<<< END U008746 >>>
<<< UNIT U008747 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:163-169 | ctx=Random.uniform >>>
返回 [a, b] 范围内的随机浮点数。

:param a: 下界。
:param b: 上界。
:return: 符合条件的随机浮点数。
<<< END U008747 >>>
<<< UNIT U008748 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:174-181 | ctx=Random.randrange >>>
返回范围内的随机整数，类似于 `range`。

:param start: 开始值。
:param stop: 结束值，不包含在范围内。
:param step: 步长。
:return: 符合条件的随机整数。
<<< END U008748 >>>
<<< UNIT U008749 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:186-191 | ctx=Random.randbits >>>
返回 k 字节长度的随机整数。

:param k: 字节长度。
:return: 符合条件的随机整数。
<<< END U008749 >>>
<<< UNIT U008750 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:196-201 | ctx=Random.randbytes >>>
生成 n 个随机字节。

:param n: 字节数量。
:return: 符合条件的随机字节。
<<< END U008750 >>>
<<< UNIT U008751 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:206-211 | ctx=Random.choice >>>
从序列中随机选择一个元素。

:param seq: 给定序列。
:return: 序列内的随机元素。
<<< END U008751 >>>
<<< UNIT U008752 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:216-222 | ctx=Random.choices >>>
从总体中选择 k 个元素，允许重复。

:param population: 给定序列。
:param k: 选择的元素个数。
:return: 序列内符合条件的随机元素列表。
<<< END U008752 >>>
<<< UNIT U008753 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:227-233 | ctx=Random.sample >>>
从总体中选择 k 个不重复元素。

:param population: 给定序列。
:param k: 选择的元素个数。
:return: 序列内符合条件的随机元素列表。
<<< END U008753 >>>
<<< UNIT U008754 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:238-243 | ctx=Random.shuffle >>>
随机打乱序列。

:param seq: 给定序列。
:return: 重新打乱后的序列。
<<< END U008754 >>>
<<< UNIT U008755 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:248-254 | ctx=Random.randstr >>>
生成指定长度的随机字符串。

:param length: 字符串长度。
:param chars: 可选的字符集，默认为大小写字母和数字。
:return: 随机生成的字符串。
<<< END U008755 >>>
<<< UNIT U008756 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:259-259 | ctx=Random.token_urlsafe >>>
生成适合用于 URL 的随机文本 token。
<<< END U008756 >>>
<<< UNIT U008757 | py-docstring | packages/akari-bot-core/akaribot/core/utils/random.py:264-264 | ctx=SecureRandom >>>
始终使用 ``secrets`` 后端的安全随机工具。
<<< END U008757 >>>
<<< UNIT U008758 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:14-14 >>>
# 公告文案的基础语言。当前语言缺失时优先回退至此。
<<< END U008758 >>>
<<< UNIT U008759 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:17-17 >>>
# 已发送公告的场景记录，以单个键存放，避免为每个场景创建记录行而污染存储表。
<<< END U008759 >>>
<<< UNIT U008760 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:20-21 >>>
# 公告延迟推送的区间（秒）。随机取值以错峰，因为多个场景常在同一时段活跃，
# 固定延迟会让公告集中在同一瞬间涌出，触发平台频率限制。
<<< END U008760 >>>
<<< UNIT U008761 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:25-26 >>>
# 已排入延时队列、尚未推送的场景。防止用户在等待期间连续发送消息导致重复排队。
# 仅存于进程内存，重启即清空。因已发送记录只在推送成功后写入数据库，重启后会自然重新排队。
<<< END U008761 >>>
<<< UNIT U008762 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:30-31 >>>
# ``enqueue_notice`` 的判断与 set 占位之间含 await，须以互斥覆盖。
# 锁只覆盖判断与占位，真正的延时投递不在临界区内。
<<< END U008762 >>>
<<< UNIT U008763 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:34-35 >>>
# 内存态是唯一来源，判断与写入均以内存为准，写入数据库时全量覆盖。
# 若改为逐次读取数据库、追加再写回，两个场景并发触发时先写入的记录会被覆盖，对应场景将重复收到公告。
<<< END U008763 >>>
<<< UNIT U008764 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:38-39 >>>
# 公告投递任务可能并发完成。每次持久化都从共享内存字典生成一份快照，若两个 save
# 写入顺序交错时，较早生成的旧快照可能最后写入数据库，使后完成的场景在重启后再次收到公告。
<<< END U008764 >>>
<<< UNIT U008765 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:43-43 >>>
# 迁移关系的分隔符，配置形如 "QQ -> QQBot"。
<<< END U008765 >>>
<<< UNIT U008766 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:46-47 >>>
# 退役实例上仍可执行的模块，命令路径与正则路径共用这一套判断规则。
# 白名单按用户输入的首词匹配。解析出的模块名不在白名单时回退到改写前的首词。
<<< END U008766 >>>
<<< UNIT U008767 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:98-98 >>>
# 就地改写而非重新赋值，因为装饰器可能已持有这两个列表对象的引用。
<<< END U008767 >>>
<<< UNIT U008768 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:184-184 >>>
# 加载已发送公告的场景记录，首次调用时从存储读入并转为字典。
<<< END U008768 >>>
<<< UNIT U008769 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:190-190 >>>
# 等锁期间可能已由另一协程完成加载，获取锁后须重新确认。
<<< END U008769 >>>
<<< UNIT U008770 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:234-235 >>>
# 内存态是后续排队判断的数据来源。持久化失败时若不回滚，本进程会误以为已经投递，
# 后续消息将永远无法重试，直到下一次进程重启。
<<< END U008770 >>>
<<< UNIT U008771 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:308-310 >>>
# 等待指定时长后向场景推送退役公告。
# 推送成功才记录已发送，因为失败多半意味着场景已永久失效（群解散、机器人被移出），
# 此时不重试，留待进程重启后由该场景的下条消息重新排队。
<<< END U008771 >>>
<<< UNIT U008772 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:321-321 >>>
# 传入单元素会话列表，使按通道合并只分出一组，公告不会被转投至同通道的其他平台。
<<< END U008772 >>>
<<< UNIT U008773 | py-comment | packages/akari-bot-core/akaribot/core/utils/retired.py:380-380 >>>
# 占位成功但任务未能创建时必须释放，否则该场景在本进程余下生命周期内都不会再排队。
<<< END U008773 >>>
<<< UNIT U008774 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:52-64 | ctx=parse_retired_routes >>>
把 ``"源 -> 目标"`` 形式的配置解析为映射。

两侧均按 ``client_name`` 解释，即针对具体实例而非整个平台种类，例如 ``"Telegram -> QQBot"``
只退役默认实例 ``Telegram``，多实例下的 ``Telegram-alt`` 不受影响。要退役某个实例就写
``"Telegram-alt -> QQBot"``。现有单实例部署下 ``client_name`` 即平台名，行为与改造前一致。

只填写源客户端时目标为 None，表示该客户端退役但不提供迁移目标。格式错误的项一律跳过并记录警告，
不使解析失败，因为退役属于运营配置，一处笔误不应阻断整个实例的启动。

:param entries: 配置中的原始条目。
:return: ``源客户端 → 目标客户端`` 的映射，目标可能为 None。
<<< END U008774 >>>
<<< UNIT U008775 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:95-95 | ctx=reload_retired_routes >>>
重新解析迁移关系配置。
<<< END U008775 >>>
<<< UNIT U008776 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:107-112 | ctx=is_retired_client >>>
判断一个客户端是否已退役。

:param client_name: 客户端名称，如 ``QQ``。
:return: 是否已退役。未配置迁移关系时恒为 False。
<<< END U008776 >>>
<<< UNIT U008777 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:130-135 | ctx=is_module_allowed_when_retired >>>
判断一个模块在已退役的客户端上是否仍可执行。

:param module_name: 模块名称。
:return: 是否在白名单内。
<<< END U008777 >>>
<<< UNIT U008778 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:203-203 | ctx=reset_notified_cache >>>
清空已发送公告的内存记录，使下次判断重新从存储加载。仅供测试使用。
<<< END U008778 >>>
<<< UNIT U008779 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:209-214 | ctx=has_notified >>>
判断某个场景是否已收到过退役公告。

:param target_id: 场景 ID。
:return: 是否已发送过。
<<< END U008779 >>>
<<< UNIT U008780 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:219-223 | ctx=mark_notified >>>
记录某个场景已收到退役公告，并将内存记录全量写回存储。

:param target_id: 场景 ID。
<<< END U008780 >>>
<<< UNIT U008781 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:273-273 | ctx=reset_pending_cache >>>
清空待推送队列的内存记录。仅供测试使用。
<<< END U008781 >>>
<<< UNIT U008782 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:278-282 | ctx=pick_notice_delay >>>
获取一个公告推送的随机延迟秒数。

:return: 位于 :data:`RETIRED_NOTIFY_DELAY_MIN` 与 :data:`RETIRED_NOTIFY_DELAY_MAX` 之间的秒数。
<<< END U008782 >>>
<<< UNIT U008783 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:287-292 | ctx=should_enqueue_notice >>>
判断某个场景此刻是否应当排入公告队列。

:param target_id: 场景 ID。
:return: 已发送过或已在队列中时为 False。
<<< END U008783 >>>
<<< UNIT U008784 | py-docstring | packages/akari-bot-core/akaribot/core/utils/retired.py:364-369 | ctx=enqueue_notice >>>
为一个场景排入退役公告的延时推送。

:param session_info: 触发排队的会话信息。
:return: 是否新排入队列。
<<< END U008784 >>>
<<< UNIT U008785 | py-comment | packages/akari-bot-core/akaribot/core/utils/s3.py:20-20 >>>
# botocore 属可选依赖（extra ``s3``），只在类型标注中引用。
<<< END U008785 >>>
<<< UNIT U008786 | py-comment | packages/akari-bot-core/akaribot/core/utils/s3.py:30-30 >>>
# 可选依赖缺失时的修复指引。boto3 与 botocore 同属 extra ``s3``，未安装时只在构造处抛出。
<<< END U008786 >>>
<<< UNIT U008787 | py-comment | packages/akari-bot-core/akaribot/core/utils/s3.py:38-38 >>>
# 默认可不安装 boto3（extra ``s3``），故导入阶段不引入。只有真正创建客户端时才需要。
<<< END U008787 >>>
<<< UNIT U008788 | py-comment | packages/akari-bot-core/akaribot/core/utils/s3.py:49-49 >>>
# 只在异常冒泡到处理分支时求值，那时客户端已创建完成，botocore 必然可以导入。
<<< END U008788 >>>
<<< UNIT U008789 | py-comment | packages/akari-bot-core/akaribot/core/utils/s3.py:77-77 >>>
# 先解析 SDK，确保依赖缺失时在分配线程池之前抛出带指引的异常。
<<< END U008789 >>>
<<< UNIT U008790 | py-comment | packages/akari-bot-core/akaribot/core/utils/s3.py:215-215 >>>
# updater 可为同步或异步函数。返回新列表时写入新列表，返回 None 时保留原地修改后的列表。
<<< END U008790 >>>
<<< UNIT U008791 | py-comment | packages/akari-bot-core/akaribot/core/utils/s3.py:348-348 >>>
# 例： ("persist", "/tmp/data.txt", None, "a1b2c3") → "persist/data_a1b2c3.txt"
<<< END U008791 >>>
<<< UNIT U008792 | py-docstring | packages/akari-bot-core/akaribot/core/utils/s3.py:54-54 | ctx=S3StorageAPI >>>
S3 兼容对象存储客户端，提供持久文件和临时文件的上传、列出、删除及预签名链接生成。
<<< END U008792 >>>
<<< UNIT U008793 | py-comment | packages/akari-bot-core/akaribot/core/utils/session.py:10-10 >>>
# 就地注入后返回原对象，故须保留调用方传入的具体子类型（如 FetchedSessionInfo）
<<< END U008793 >>>
<<< UNIT U008794 | py-docstring | packages/akari-bot-core/akaribot/core/utils/storedata.py:13-13 | ctx=get_stored_list >>>
读取持久化列表。
<<< END U008794 >>>
<<< UNIT U008795 | py-docstring | packages/akari-bot-core/akaribot/core/utils/storedata.py:26-26 | ctx=update_stored_list >>>
更新持久化列表。
<<< END U008795 >>>
<<< UNIT U008796 | py-comment | packages/akari-bot-core/akaribot/core/utils/table.py:6-6 >>>
# 表格的高度上限。条目增多时通过增加列数分摊，使表格高度不超过该上限。
<<< END U008796 >>>
<<< UNIT U008797 | py-comment | packages/akari-bot-core/akaribot/core/utils/table.py:9-10 >>>
# 表格的最少列数。条目寥寥时若仍按高度上限反算列数会得到一两列的竖长条，
# 该下限只会让表更矮更宽，不会反过来拉高。
<<< END U008797 >>>
<<< UNIT U008798 | py-docstring | packages/akari-bot-core/akaribot/core/utils/table.py:1-1 | ctx=<module> >>>
Markdown 表格工具 - 单元格转义与“高度封顶、宽度按需”的列数求解。
<<< END U008798 >>>
<<< UNIT U008799 | py-docstring | packages/akari-bot-core/akaribot/core/utils/table.py:15-20 | ctx=escape_table_cell >>>
把文本整理成可以放入 markdown 表格单元格的形态。

:param text: 原始文本。
:return: 可安全放入单元格的文本。
<<< END U008799 >>>
<<< UNIT U008800 | py-docstring | packages/akari-bot-core/akaribot/core/utils/table.py:25-30 | ctx=format_table_code >>>
把文本包成 markdown 行内代码，使其中的格式标记不被解析。

:param text: 原始文本。
:return: 可安全放入单元格的行内代码。文本为空时返回空字符串。
<<< END U008800 >>>
<<< UNIT U008801 | py-docstring | packages/akari-bot-core/akaribot/core/utils/timezone.py:1-1 | ctx=<module> >>>
机器人的时间工具。
<<< END U008801 >>>
<<< UNIT U008802 | py-docstring | packages/akari-bot-core/akaribot/core/utils/timezone.py:11-11 | ctx=core_offset >>>
获取核心默认偏移量。
<<< END U008802 >>>
<<< UNIT U008803 | py-docstring | packages/akari-bot-core/akaribot/core/utils/timezone.py:21-21 | ctx=core_tz >>>
获取核心默认时区。
<<< END U008803 >>>
<<< UNIT U008804 | py-docstring | packages/akari-bot-core/akaribot/core/utils/timezone.py:26-26 | ctx=core_offset_text >>>
获取规范化的核心默认偏移量字符串。
<<< END U008804 >>>
<<< UNIT U008805 | py-docstring | packages/akari-bot-core/akaribot/core/utils/timezone.py:31-31 | ctx=core_now >>>
获取核心时区（或指定时区）的当前时间。
<<< END U008805 >>>
<<< UNIT U008806 | py-docstring | packages/akari-bot-core/akaribot/core/utils/timezone.py:36-36 | ctx=core_today >>>
获取核心时区（或指定时区）的当前日期。
<<< END U008806 >>>
<<< UNIT U008807 | py-docstring | packages/akari-bot-core/akaribot/core/utils/timezone.py:41-41 | ctx=core_midnight >>>
获取核心时区（或指定时区）的今日零点。
<<< END U008807 >>>
<<< UNIT U008808 | py-comment | packages/akari-bot-core/akaribot/core/utils/url_audit.py:148-149 >>>
# 主仓规则 global.txt 随仓库分发，位于 data/url_audit/<名单>。
# 部署者规则 user.txt 与之同目录但被 Git 忽略。测试可整体替换这几个路径。
<<< END U008808 >>>
<<< UNIT U008809 | py-comment | packages/akari-bot-core/akaribot/core/utils/url_audit.py:300-300 >>>
# 全局规则与用户规则合计适用同一份上限，重复项按加载时的去重结果计数。
<<< END U008809 >>>
<<< UNIT U008810 | py-comment | packages/akari-bot-core/akaribot/core/utils/url_audit.py:320-320 >>>
# 临时文件与目标同目录，确保 os.replace 只在同一文件系统内进行。
<<< END U008810 >>>
<<< UNIT U008811 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:46-46 | ctx=URLRule.serialized >>>
返回规则的序列化文本。
<<< END U008811 >>>
<<< UNIT U008812 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:160-160 | ctx=_GlobalURLRuleList.clear_cache >>>
清空当前名单的内存缓存。
<<< END U008812 >>>
<<< UNIT U008813 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:227-227 | ctx=_GlobalURLRuleList.matching_rules >>>
返回匹配该 URL 的规则列表。
<<< END U008813 >>>
<<< UNIT U008814 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:249-249 | ctx=_GlobalURLRuleList.contains >>>
检查 URL 是否命中当前名单。
<<< END U008814 >>>
<<< UNIT U008815 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:274-274 | ctx=_GlobalURLRuleList.rules >>>
返回名单中的全部规则。
<<< END U008815 >>>
<<< UNIT U008816 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:279-279 | ctx=_GlobalURLRuleList.user_rules >>>
返回本地用户规则。
<<< END U008816 >>>
<<< UNIT U008817 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:284-284 | ctx=_GlobalURLRuleList.file_signature >>>
返回文件路径、修改时间和大小组成的签名。
<<< END U008817 >>>
<<< UNIT U008818 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:289-289 | ctx=_GlobalURLRuleList.replace_user_rules >>>
用给定规则整体替换本地用户规则。
<<< END U008818 >>>
<<< UNIT U008819 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:337-337 | ctx=_GlobalURLRuleList.add_user_rule >>>
添加一条本地用户规则。
<<< END U008819 >>>
<<< UNIT U008820 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:361-361 | ctx=_GlobalURLRuleList.import_user_rules >>>
批量导入规则，返回新增条数。
<<< END U008820 >>>
<<< UNIT U008821 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:371-371 | ctx=_GlobalURLRuleList.remove_user_rule >>>
删除一条本地用户规则。
<<< END U008821 >>>
<<< UNIT U008822 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:398-398 | ctx=GlobalURLAllowlist >>>
全局 URL 允许名单。
<<< END U008822 >>>
<<< UNIT U008823 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:411-411 | ctx=GlobalURLAllowlist.is_allowed >>>
判断 URL 是否允许。
<<< END U008823 >>>
<<< UNIT U008824 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:416-416 | ctx=GlobalURLBlocklist >>>
全局 URL 阻止名单。
<<< END U008824 >>>
<<< UNIT U008825 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:429-429 | ctx=GlobalURLBlocklist.is_blocked >>>
判断 URL 是否阻止。
<<< END U008825 >>>
<<< UNIT U008826 | py-docstring | packages/akari-bot-core/akaribot/core/utils/url_audit.py:434-434 | ctx=evaluate_url_policy >>>
统一判定 URL 的全局允许与阻止状态，阻止列表始终优先。
<<< END U008826 >>>
<<< UNIT U008827 | py-comment | packages/akari-bot-core/akaribot/core/utils/web_render.py:42-43 >>>
# remote_only 的所有操作（包括 status）均由依赖库转发至远端。此时启动本地
# Playwright 不仅违背配置，还会让无浏览器环境中的可用远端服务被误判为不可用。
<<< END U008827 >>>
<<< UNIT U008828 | py-docstring | packages/akari-bot-core/akaribot/core/utils/web_render.py:37-37 | ctx=init_web_render >>>
初始化网页渲染器。
<<< END U008828 >>>
<<< UNIT U008829 | py-docstring | packages/akari-bot-core/akaribot/core/utils/web_render.py:55-55 | ctx=check_web_render_status >>>
检查当前配置所选 WebRender 后端是否可用。
<<< END U008829 >>>
<<< UNIT U008830 | py-docstring | packages/akari-bot-core/akaribot/core/utils/web_render.py:63-63 | ctx=close_web_render >>>
关闭网页渲染器。
<<< END U008830 >>>
<<< UNIT U008831 | py-docstring | packages/akari-bot-core/akaribot/modules/core/admin_tools/__init__.py:1-1 | ctx=<module> >>>
场景与管理员配置命令。
<<< END U008831 >>>
<<< UNIT U008832 | py-comment | packages/akari-bot-core/akaribot/modules/core/admin_tools/admin.py:23-23 >>>
# 将权限列表中的 union ID 展开为其下绑定的平台账号 ID 用于展示，一行对应一个 union。
<<< END U008832 >>>
<<< UNIT U008833 | py-comment | packages/akari-bot-core/akaribot/modules/core/admin_tools/admin.py:33-33 >>>
# 将平台账号 ID 解析为写入权限列表的 union ID，未绑定任何 union 时回退到原 ID。
<<< END U008833 >>>
<<< UNIT U008834 | py-comment | packages/akari-bot-core/akaribot/modules/core/admin_tools/alias.py:70-70 >>>
# 处理下划线与空格的情况
<<< END U008834 >>>
<<< UNIT U008835 | py-docstring | packages/akari-bot-core/akaribot/modules/core/admin_tools/alias.py:13-13 | ctx=transform_alias >>>
按场景自定义规则改写命令文本。
<<< END U008835 >>>
<<< UNIT U008836 | py-comment | packages/akari-bot-core/akaribot/modules/core/admin_tools/locale.py:61-61 >>>
# 缓存损坏时移除，避免后续反复命中坏文件。
<<< END U008836 >>>
<<< UNIT U008837 | py-docstring | packages/akari-bot-core/akaribot/modules/core/admin_tools/locale.py:20-20 | ctx=build_locale_list >>>
构造逐行显示的可用语言列表。
<<< END U008837 >>>
<<< UNIT U008838 | py-docstring | packages/akari-bot-core/akaribot/modules/core/admin_tools/locale.py:34-34 | ctx=build_locale_overview >>>
构造语言命令的概览消息。
<<< END U008838 >>>
<<< UNIT U008839 | py-comment | packages/akari-bot-core/akaribot/modules/core/admin_tools/modules.py:14-14 >>>
# 模块受限成因到提示文案的映射，键取自 Module.unsupported_reason() 的返回值。
<<< END U008839 >>>
<<< UNIT U008840 | py-comment | packages/akari-bot-core/akaribot/modules/core/admin_tools/modules.py:21-21 >>>
# 机器人平台权限到中文名称的映射。未记录的权限直接回退为字段名，避免误报为其他能力。
<<< END U008840 >>>
<<< UNIT U008841 | py-comment | packages/akari-bot-core/akaribot/modules/core/admin_tools/modules.py:121-122 >>>
# RPC 与网络故障不能视为机器人无权限。
# 只有平台明确返回 False 才阻止开启，查询失败按能力声明处理。
<<< END U008841 >>>
<<< UNIT U008842 | py-docstring | packages/akari-bot-core/akaribot/modules/core/admin_tools/modules.py:34-34 | ctx=format_bot_permissions >>>
将机器人权限字段渲染为管理员可读的名称列表。
<<< END U008842 >>>
<<< UNIT U008843 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/__init__.py:1-1 | ctx=<module> >>>
面向普通用户的公共查询、绑定与场景工具。
<<< END U008843 >>>
<<< UNIT U008844 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py:11-11 >>>
# 花苞与花瓣一样关联在 union 上、跨平台共享，存储桶复用花瓣的 Union 作用域。
<<< END U008844 >>>
<<< UNIT U008845 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py:14-14 >>>
# 花苞有效期（秒）。过期后不可领取，未领取的花瓣退回发送者并清理。
<<< END U008845 >>>
<<< UNIT U008846 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py:1-1 | ctx=<module> >>>
花苞（拼手气红包）工具。
<<< END U008846 >>>
<<< UNIT U008847 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py:46-46 | ctx=generate_bud_id >>>
生成一个不与已有花苞冲突的短 ID。
<<< END U008847 >>>
<<< UNIT U008848 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py:78-78 | ctx=create_bud >>>
创建花苞并写入存储，口令冲突时返回 ``None``。
<<< END U008848 >>>
<<< UNIT U008849 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py:101-101 | ctx=find_bud >>>
按花苞 ID 查找花苞。
<<< END U008849 >>>
<<< UNIT U008850 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py:109-109 | ctx=release_buds >>>
释放所有空花苞和过期花苞，并返回释放数量。
<<< END U008850 >>>
<<< UNIT U008851 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_bud.py:122-122 | ctx=claim_bud >>>
领取花苞，返回 ``(状态, 花苞, 领取数量)``。
<<< END U008851 >>>
<<< UNIT U008852 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:24-25 >>>
# 下面几个名字没有纳入 core.api。表名工具是否成为第三方公开接口待 P5 复核。日志路径常量只是兼容入口，
# 计划在阶段 4 删除，纳入公开接口会把待删除的名字写入稳定接口清单。
<<< END U008852 >>>
<<< UNIT U008853 | py-inline-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:29-29 >>>
# 绑定码有效期（秒）
<<< END U008853 >>>
<<< UNIT U008854 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:110-112 >>>
# 标签仍须显示实际命令，操作提示仅作为附注。
# 该提示离开可点击的平台便无意义，故不随降级带往其他平台。引号同理，
# 可点击的标签自带视觉边界，仅降级后的命令原文才需要它
<<< END U008854 >>>
<<< UNIT U008855 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:120-120 >>>
# 平台仅在消息实际投递成功时返回消息 ID，未获取即表示该条私信未送达。
<<< END U008855 >>>
<<< UNIT U008856 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:156-156 >>>
# 文件内容自带这几项，日志文件即便被重命名或移走仍可辨认。
<<< END U008856 >>>
<<< UNIT U008857 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:164-165 >>>
# 时间置于文件名开头，目录按名称排序即为时间顺序。微秒一并带上，同一秒内的两次合并不会重名。
# union ID 中的 "|" 须换成 "-"，因为 Windows 不接受该字符出现在文件名中。
<<< END U008857 >>>
<<< UNIT U008858 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:167-168 >>>
# 先写入临时文件再原子替换，避免直接写入磁盘在中途被强制结束时留下不完整的日志，
# 导致读取时才发现损坏。经此一步，该文件要么完整要么不存在。
<<< END U008858 >>>
<<< UNIT U008859 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:258-259 >>>
# 旧 Union 行可能在等待其他活跃命令期间被第三方合并并删除。以双方稳定的
# 物理 ID 为锚点重新解析，不能对旧 ORM 对象直接 refresh_from_db()。
<<< END U008859 >>>
<<< UNIT U008860 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:286-287 >>>
# 等待期间一侧可能又与第三组发生合并。把新增成员继续纳入 barrier，
# 直到重新解析出的完整身份域已被当前 reservation 覆盖。
<<< END U008860 >>>
<<< UNIT U008861 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:467-467 >>>
# 缺少绑定行的场景理论上不会出现。该分支用于保证展示流程连续。
<<< END U008861 >>>
<<< UNIT U008862 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:35-43 | ctx=generate_code >>>
为发起方生成一枚绑定码，同一组同时只保留最新的一枚。

:param store: 绑定码存储。
:param union_id: 发起方所属的组 ID。
:param holder_id: 发起方的平台 ID，用于向对方展示绑定来源。
:param extra: 随绑定码一并留存的附加信息。
:return: 绑定码。
<<< END U008862 >>>
<<< UNIT U008863 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:128-128 | ctx=id_lines >>>
将 ID 列表逐行展示，ID 不参与文本替换。
<<< END U008863 >>>
<<< UNIT U008864 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:186-191 | ctx=choose_conflicts >>>
逐个询问模块数据冲突时保留哪一份。

:param conflicts: 双方都有数据的模块表模型。
:return: 需要保留发起方数据的表名集合。
<<< END U008864 >>>
<<< UNIT U008865 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:254-254 | ctx=reserve_sender_merge >>>
为账号组合并建立双方身份域 barrier，并重新生成最新计划。
<<< END U008865 >>>
<<< UNIT U008866 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:296-302 | ctx=apply_sender_merge >>>
按计划执行账号组合并并记录快照。

:param plan: :func:`plan_sender_merge` 生成的合并计划。
:param keep_other_tables: 需要保留发起方数据的表名集合。
:return: 合并后的新账号组。
<<< END U008866 >>>
<<< UNIT U008867 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:353-361 | ctx=plan_target_merge >>>
收集一次场景组合并所需的双方 ID、冲突模块与待确认文案。

:param initiator: 发起方（生成绑定码或发起通道握手的一方）。
:param current: 另一方。
:param inherit_key: 继承说明的 i18n 键。绑定码流程仅合并场景组，消息通道保持独立。
                    ``bind auto`` 会同时将双方并入同一条消息通道，两者的说明需分开。
:return: 合并计划。
<<< END U008867 >>>
<<< UNIT U008868 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:387-393 | ctx=apply_target_merge >>>
按计划执行场景组合并并记录快照。

:param plan: :func:`plan_target_merge` 生成的合并计划。
:param keep_other_tables: 需要保留发起方数据的表名集合。
:return: 合并后的新场景组。
<<< END U008868 >>>
<<< UNIT U008869 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:428-435 | ctx=merge_target_unions >>>
按“展示继承关系 → 确认 → 逐个处理冲突 → 记录快照 → 合并”的流程完成一次场景组合并。

:param initiator: 发起方（生成绑定码或发起通道握手的一方）。
:param current: 另一方。
:param inherit_key: 继承说明的 i18n 键。
:return: 合并后的新场景组，用户取消时为 None。
<<< END U008869 >>>
<<< UNIT U008870 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:443-443 | ctx=channel_hint_lines >>>
消息通道含义的说明，末尾附合并通道的途径。
<<< END U008870 >>>
<<< UNIT U008871 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/_union_merge.py:456-461 | ctx=target_lines >>>
将场景 ID 逐行展示，每行标注所在的消息通道，末尾附通道含义说明。

:param union_id: 这些场景所属的组 ID。
:param ids: 组内的平台场景 ID。
<<< END U008871 >>>
<<< UNIT U008872 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/about.py:76-76 >>>
# 品牌资产包缺失（或部署者删除了配图）时跳过配图，少一张图不应让整条 `~about` 失败。
<<< END U008872 >>>
<<< UNIT U008873 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/about.py:60-60 | ctx=build_credits_message >>>
构造制作人员名单消息。
<<< END U008873 >>>
<<< UNIT U008874 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/about.py:72-72 | ctx=build_about_message >>>
根据平台能力构造 `~about` 菜单。
<<< END U008874 >>>
<<< UNIT U008875 | py-inline-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:34-34 >>>
# 通道握手超时（秒）
<<< END U008875 >>>
<<< UNIT U008876 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:40-41 >>>
# 自动配对是为多个机器人共处同一场景的情形预留的，默认关闭。命令是否注册在导入时即已确定，
# 因此取一份快照，改动配置须重启机器人才能生效。
<<< END U008876 >>>
<<< UNIT U008877 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:44-45 >>>
# 绑定码与握手状态仅保存在 server 进程内存中，重启即失效。
# 各平台的 bot 子进程共用同一个 server 进程，因此跨平台握手无需写入数据库。
<<< END U008877 >>>
<<< UNIT U008878 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:58-59 >>>
# 握手分待认领的 probe 与待闭合的 confirm 两段记录。口令一经发出即出现在场景中，
# 任何人都能原样复制，故两段各自的口令都只能使用一次。
<<< END U008878 >>>
<<< UNIT U008879 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:62-63 >>>
# 握手闭合串行执行。若避让机制未生效（如某一平台的 probe 投递延迟），
# 两轮并发执行至“是否同组”判定时会同时读到合并前的数据，各自新建一个组，合并即告失败。
<<< END U008879 >>>
<<< UNIT U008880 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:105-105 >>>
# 取出并核销一枚由 ``bind`` 签发的绑定码。
<<< END U008880 >>>
<<< UNIT U008881 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:113-113 >>>
# 当前场景的消息通道信息，含同通道的其他场景。
<<< END U008881 >>>
<<< UNIT U008882 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:187-188 >>>
# 私聊中的用户身份与私聊场景属于同一数据边界，应一并绑定，
# 否则换到另一个平台私聊机器人时数据仍是两份。
<<< END U008882 >>>
<<< UNIT U008883 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:197-197 >>>
# 场景组绑定会改动整个场景的数据，需要管理员权限。私聊没有这个顾虑，校验放在此处执行。
<<< END U008883 >>>
<<< UNIT U008884 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:256-258 >>>
# 完成一次私聊绑定，将账号组与场景组一并合并。
# 私聊里“这个账号”与“这段私聊”指的是同一件事。只合并其一会让另一半的数据留在原处。
# 两者共用一次确认，确认后一起执行，避免用户在第二次确认时取消而停在只绑定一半的状态。
<<< END U008884 >>>
<<< UNIT U008885 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:263-263 >>>
# 生成绑定码的一方为发起方，冲突数据默认以发起方为准。
<<< END U008885 >>>
<<< UNIT U008886 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:269-269 >>>
# 一侧已同组时只合并另一侧。两侧都已同组说明这枚码来自本方，无需绑定。
<<< END U008886 >>>
<<< UNIT U008887 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:290-291 >>>
# 场景选择须在建立 sender barrier 前完成。普通 wait_confirm 会释放执行
# lease。sender barrier 建立后，冲突选择保持 lease，直到合并写入结束。
<<< END U008887 >>>
<<< UNIT U008888 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:328-329 >>>
# 绑定码的生成与使用须处于同类场景。私聊码带着发起方的场景组，若在群里兑换，
# 会把一个群的数据合并到对方的私聊，群码在私聊里兑换同理。
<<< END U008888 >>>
<<< UNIT U008889 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:336-336 >>>
# 场景组绑定会改动整个场景的数据，与 bind start 一样需要管理员权限。
<<< END U008889 >>>
<<< UNIT U008890 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:418-419 >>>
# 此处不作二次确认。双方尚未关联，通道去重与互认记录均未生效，同一场景内的每个机器人都会
# 各自解析该命令，确认提示会被重复发出。需要确认的是握手闭合后的合并提示。
<<< END U008890 >>>
<<< UNIT U008891 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:427-427 >>>
# 该命令仅供同一场景内的其他机器人识别，对用户不具备可读语义。
<<< END U008891 >>>
<<< UNIT U008892 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:438-438 >>>
# 口令过期后收回本轮握手的全部记录。
<<< END U008892 >>>
<<< UNIT U008893 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:441-441 >>>
# 本轮已避让或已闭合，上下文在各自的路径中释放，此处不再重复处理。
<<< END U008893 >>>
<<< UNIT U008894 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:444-444 >>>
# probe 口令既已过期，由它换来的 confirm 口令不应继续有效。
<<< END U008894 >>>
<<< UNIT U008895 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:458-459 >>>
# 口令在场景中以明文出现，任何人都能原样复制，故认领是一次性的，一经认领即作废。其后携带
# 同一串口令的消息一律丢弃，否则复制该命令的用户会被视为对端机器人，其发言将被忽略。
<<< END U008895 >>>
<<< UNIT U008896 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:464-464 >>>
# 部分平台会将机器人自身发出的消息回送，遇到自身发起的握手直接忽略。
<<< END U008896 >>>
<<< UNIT U008897 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:468-470 >>>
# 同一场景内的每个机器人都会收到同一条 ~bind auto 并各自发起一轮握手，两轮交叉配对
# 会使同一对场景被合并两次。此处按 probe 口令排序作确定性避让，仅保留口令最小的一轮。
# 各方均先写入记录再发出 probe，因此收到对方 probe 时自身记录必然已存在，判定不会遗漏。
<<< END U008897 >>>
<<< UNIT U008898 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:481-481 >>>
# 自身这一轮口令更小，由对方响应本轮即可，不再应答对方。
<<< END U008898 >>>
<<< UNIT U008899 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:484-484 >>>
# 自身这一轮已被对方认领并等待闭合，无须再发起新一轮。
<<< END U008899 >>>
<<< UNIT U008900 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:490-490 >>>
# 避让过程中已交出控制权，其间该口令可能已被另一个机器人认领，认领前须再确认一次。
<<< END U008900 >>>
<<< UNIT U008901 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:500-500 >>>
# 持有上下文期间 probe 可能已经超时。此时不再生成一个无人负责清理的 confirm。
<<< END U008901 >>>
<<< UNIT U008902 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:506-507 >>>
# confirm 口令至此才生成，因而每一次配对各持一枚，且只有本次的响应方知晓——
# 发起方广播出去的那一枚 probe 口令不足以推出它，旁观者无从抢先应答。
<<< END U008902 >>>
<<< UNIT U008903 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:526-528 >>>
# 闭合一轮握手。
# confirm 口令同样只能使用一次，且只在发起场景中生效。响应方发出的口令必然出现在双方共处的
# 那个场景里，出现在别处即说明它是被转贴过去的，据此可拒绝跨场景的冒用。
<<< END U008903 >>>
<<< UNIT U008904 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:557-559 >>>
# 握手闭合后把两个场景合成同一条消息通道。
# 此时已确认两个场景对应同一个现实场景，随后依次合并场景组（数据共享）、
# 统一消息通道编号（命令与推送去重），并互相记录对方的机器人账号（屏蔽对方发出的消息）。
<<< END U008904 >>>
<<< UNIT U008905 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:563-563 >>>
# 获取锁之后再读取组信息，因为若先读取再加锁，读到的仍是并发方修改前的数据，加锁将失去意义。
<<< END U008905 >>>
<<< UNIT U008906 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:578-578 >>>
# 另一轮握手已完成同样的处理，无需重复向管理员确认，也无需重复写入数据库。
<<< END U008906 >>>
<<< UNIT U008907 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:587-587 >>>
# 合并场景组、统一通道编号、互记机器人账号。调用方需持有 :data:`_handshake_lock`。
<<< END U008907 >>>
<<< UNIT U008908 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:593-593 >>>
# 合并确认在发起方进行，因为执行该命令的管理员位于发起方。
<<< END U008908 >>>
<<< UNIT U008909 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:601-602 >>>
# 将对方所在的完整通道并入本场景通道。若只修改响应方这一行，它原通道中的第三个平台入口
# 会被错误拆开。通道等价关系具有传递性，必须整体移动。
<<< END U008909 >>>
<<< UNIT U008910 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/bind.py:611-612 >>>
# 记录双方的机器人账号，避免将对方发出的消息当作用户输入解析。
# 账号按观察方所在平台的命名空间记录，其中发起方观察到的对端账号取自 confirm，对端观察到的发起方账号取自 probe。
<<< END U008910 >>>
<<< UNIT U008911 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:249-250 >>>
# 表头与分隔线开头，随后各行的收尾、下一组的区隔行都合并到同一个纯文本，
# 以免相邻纯文本之间被适配器补上换行
<<< END U008911 >>>
<<< UNIT U008912 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:340-342 >>>
# 每节为 (区隔行文案, [(种类, 首列, 次列), ...])。命令一节不带区隔行。
# 种类控制首列在单元格中的呈现方式，其中 command 渲染为指令操作，code 已是成型的行内代码，
# text 则正常转义。
<<< END U008912 >>>
<<< UNIT U008913 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:350-350 >>>
# 正则包含大量格式标记字符，使用行内代码原样呈现，不再逐字符转义。
<<< END U008913 >>>
<<< UNIT U008914 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:370-370 >>>
# 末行补空的成对单元格，markdown 要求各行的列数一致
<<< END U008914 >>>
<<< UNIT U008915 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:380-380 >>>
# code 已由 format_table_code() 处理妥当，再转义会把围栏内的反斜杠显示出来
<<< END U008915 >>>
<<< UNIT U008916 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:384-384 >>>
# 末尾保留换行，理由同 build_module_table()，表格靠空行终结
<<< END U008916 >>>
<<< UNIT U008917 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:472-472 >>>
# 表格版另需成对的（正则，说明），与拼接成一行的 mdocs 并行收集
<<< END U008917 >>>
<<< UNIT U008918 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:481-481 >>>
# 会话缺少推送能力时订阅扩展模块无法启用，展示其帮助会误导用户
<<< END U008918 >>>
<<< UNIT U008919 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:484-484 >>>
# 仅在模块确实含有管理员条目时才查询平台权限，普通模块的帮助不额外付出一次接口调用
<<< END U008919 >>>
<<< UNIT U008920 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:532-533 >>>
# 表格版把正则包进行内代码，不需要也不能要这层反斜杠转义，
# 故在转义前先留一份原样的
<<< END U008920 >>>
<<< UNIT U008921 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:575-575 >>>
# 表格版优先于图片版，因为命令可点击填入，且与模块列表的排法一致
<<< END U008921 >>>
<<< UNIT U008922 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:742-742 >>>
# 各类模块同处一张表，以一行区隔行分开。表格以纯文本收尾，无须 end_inline_run()
<<< END U008922 >>>
<<< UNIT U008923 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:821-821 >>>
# 与 ~help 同理，表格不可用时优先保留图片，图片生成失败后再降级到文字版
<<< END U008923 >>>
<<< UNIT U008924 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:879-879 >>>
# 与 ~help 同款表格，收尾同样是纯文本
<<< END U008924 >>>
<<< UNIT U008925 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:119-119 | ctx=get_module_type_display >>>
返回适合 Markdown 详情页展示的模块类型标记。
<<< END U008925 >>>
<<< UNIT U008926 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:166-181 | ctx=end_inline_run >>>
终止行内连排，使其后追加的元素能各自成行。

可点击的模块列表以指令操作收尾，而适配器会把紧随指令操作之后的文本并入同一行
（见 ``akaribot/adapters/qqbot/context.py`` 中 send_msg_markdown() 的 ``inline_pending``）。
该规则本是为“文字 + 标签 + 收尾文字”这类同出一句话的场合而设，跨消息元素时却会
把调用方随后追加的提示语紧贴在最后一个模块名之后。补一个纯文本片段即可断开连排。

片段取一个空格而非空字符串，因为消息链会把空文本换成错误提示（见
``akaribot/core/builtins/message/chain.py`` 对空文本的处理）。换行同样不可取——适配器随后
仍会按元素补一次换行，两者叠加会多出一个空行。

本函数只在具备指令操作能力的平台上有意义，调用点均已由 ``use_clickable`` 控制。

:param chain: 待收尾的消息链，就地修改。
<<< END U008926 >>>
<<< UNIT U008927 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/help.py:191-213 | ctx=build_module_table >>>
把若干组模块名排成一张 markdown 表。

各组同处一张表，组与组之间以一行只填组名的区隔行分开。首组的组名即表头。表格至多
:data:`~akaribot.core.utils.table.TABLE_MAX_ROWS` 行、至少 :data:`~akaribot.core.utils.table.TABLE_MIN_COLUMNS` 列，
模块数增多时通过增加列数分摊。末行不足处补空单元格 —— markdown 要求各行的列数一致。

``include_help_header`` 开启时，机器人名、当前语言、版本与用户权限会成为同一张表的首行。
此时表格至少使用四列，列数更多时在首行末尾补空单元格，所有行始终保持相同列数。

模块名渲染为指令操作，点击即把 ``<前缀>help <模块名>`` 填入输入框。标签之所以能置于单元格
中间，依赖的正是适配器把指令操作及其后的文本一并并入上一项的行为（见
``akaribot/adapters/qqbot/context.py`` 的 ``inline_pending``），整张表因此累积成一个文本块，
竖线与换行均由此处显式写出。也正因如此，本函数生成的元素中**不得出现相邻的两个纯文本**
—— 适配器只在指令操作之后才会合并，两个纯文本之间会被补上换行，表格随即被拆成两半。
区隔行因此与上一组的收尾同处一个元素。

:param msg: 消息会话。
:param groups: (组名多语言键, 模块名列表) 的序列，模块名为空的组会被跳过。
:param include_help_header: 是否在模块表格内加入 help 顶栏。
:param permission: 顶栏权限类型，可选 ``user``、``admin`` 或 ``superuser``。
:return: 消息元素列表。所有组都为空时返回空片段，空状态文案由调用方负责。
<<< END U008927 >>>
<<< UNIT U008928 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:32-33 >>>
# 迁移码与 bind 的绑定码分开存放，两者不可混用，因为
# 迁移码用于把退役实例上的数据迁移到新实例，与常规的跨平台绑定不是同一件事。
<<< END U008928 >>>
<<< UNIT U008929 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:37-38 >>>
# ``merge`` 是 ``bind`` 的别名，此处保留同名隐藏模块，仅承载退役公告触发器，因为
# 退役策略的白名单按模块名放行，公告正则须挂载在白名单模块上才能在退役场景继续匹配。
<<< END U008929 >>>
<<< UNIT U008930 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:43-43 >>>
# 取出并核销一枚由 ``merge`` 签发的迁移码。
<<< END U008930 >>>
<<< UNIT U008931 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:51-53 >>>
# 两个场景并入同一条通道，使命令执行与消息推送只由其中一方承担。若两个机器人回到共作状态，
# 不同通道会让两个机器人各自通过通道认领的快路径，同一条命令被响应两次，统一通道是这类回退场景的保险。
# 通道编号取发起方的现有编号。两个场景原本所在的完整通道都保留等价关系，避免拆开第三个入口。
<<< END U008931 >>>
<<< UNIT U008932 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:63-64 >>>
# 两行都存在却无法统一，说明迁移后的 Target Union 拓扑与调用约定不符。
# 此时不能把其中一侧静默移到其他通道，避免掩盖未完成的 Union 合并。
<<< END U008932 >>>
<<< UNIT U008933 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:76-77 >>>
# 迁移码须记录签发方的客户端与场景，前者用于兑换时校验迁移目标，
# 后者用于迁移完成后统一两侧的消息通道编号。
<<< END U008933 >>>
<<< UNIT U008934 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:81-82 >>>
# 私聊中的用户身份与私聊场景属于同一数据边界，应一并迁移，
# 否则用户的个人数据仍留在退役实例上。
<<< END U008934 >>>
<<< UNIT U008935 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:97-97 >>>
# 场景迁移会改动整个场景的数据，需要管理员权限。私聊没有这个顾虑，校验放在此处执行。
<<< END U008935 >>>
<<< UNIT U008936 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:113-115 >>>
# 完成一次私聊迁移，将账号数据与私聊场景数据一并合并。
# 私聊里“这个账号”与“这段私聊”指的是同一件事。只合并其一会让另一半的数据留在退役实例上。
# 两者共用一次确认后一起执行，避免用户在第二次确认时取消而停在只迁移一半的状态。
<<< END U008936 >>>
<<< UNIT U008937 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:120-120 >>>
# 签发迁移码的一方为发起方，冲突数据默认以发起方为准。
<<< END U008937 >>>
<<< UNIT U008938 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:152-153 >>>
# 场景选择须在建立 sender barrier 前完成。普通 wait_confirm 会释放执行
# lease。sender barrier 建立后，其冲突选择则保持 lease，直到合并写入结束。
<<< END U008938 >>>
<<< UNIT U008939 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:185-186 >>>
# 命令字面量按“位置无关的标志”匹配，因为沿用 merge token 作命令路径会被 bind token 抢先匹配
# （``<code>`` 匹配并消耗 "merge"），源平台便不再避让。用户端命令不变，通过别名映射到这里。
<<< END U008939 >>>
<<< UNIT U008940 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:199-200 >>>
# 迁移码只能在其所属迁移关系的目标平台兑换。命令级 available_for 只能表明本平台是
# 某条关系的目标，配置多条关系时挡不住用甲关系的码在乙关系的目标上兑换。
<<< END U008940 >>>
<<< UNIT U008941 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:204-205 >>>
# 迁移码的签发与使用须处于同类场景。私聊码带着发起方的场景组，若在群里兑换，
# 会把一段私聊的数据合并到群场景，群码在私聊里兑换同理。
<<< END U008941 >>>
<<< UNIT U008942 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:212-212 >>>
# 场景迁移会改动整个场景的数据，与签发迁移码时一样需要管理员权限。
<<< END U008942 >>>
<<< UNIT U008943 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/merge.py:255-256 >>>
# 只做排队，不向场景发送内容，公告由延时任务在数分钟后推送。若挂载在命令拦截上，退役后用户
# 不再发送命令，该场景便永远收不到公告。单次触发使每个场景只执行一次，避免每条消息都查询数据库。
<<< END U008943 >>>
<<< UNIT U008944 | py-inline-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/petal.py:42-42 >>>
# 客户端级隔离，避免刷花瓣
<<< END U008944 >>>
<<< UNIT U008945 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/ping.py:21-21 >>>
# 平台名与 jobqueue-hub 为专有名词，仅占位标签需本地化。
<<< END U008945 >>>
<<< UNIT U008946 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:81-83 >>>
# 不加 available_for，因为框架只能按平台名过滤命令，无法按会话特性过滤。若改用平台名，
# 将来其他平台声明了 support_markdown_toggle，面板会出现“有此行、命令却不可用”的无效行。
# 以能力标志作为唯一判断依据可避免该情形，代价是其他平台的帮助列表中仍会列出这条命令。
<<< END U008946 >>>
<<< UNIT U008947 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:164-164 >>>
# 构造一个开关型设置行，其取值与入口文案按当前状态选定。
<<< END U008947 >>>
<<< UNIT U008948 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:169-169 >>>
# 入口文案与当前状态相反，已开启时能做的是关闭
<<< END U008948 >>>
<<< UNIT U008949 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:305-306 >>>
# 判断元素列表是否以行内入口收尾。
# 适配器会把紧随行内入口之后的文本并入同一行，故其后的元素须自带换行。
<<< END U008949 >>>
<<< UNIT U008950 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:350-350 >>>
# 首行紧随标题，标题不是行内入口，不会被并入。其后各行才需要自带换行
<<< END U008950 >>>
<<< UNIT U008951 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:352-353 >>>
# 保留行尾空格，因为指令操作无论以元素形态并入还是降级为纯文本，都不会自行补分隔符。
# disable_joke 也不可省略，降级后的命令原文会并入本元素，被替换后就无法直接复制了。
<<< END U008951 >>>
<<< UNIT U008952 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:387-387 >>>
# 不指定域时两域同列，一条命令即可看全
<<< END U008952 >>>
<<< UNIT U008953 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:391-391 >>>
# 只读展示对所有人开放，能否修改才看权限
<<< END U008953 >>>
<<< UNIT U008954 | py-comment | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:398-398 >>>
# 场景组末尾若留有行内入口，个人组的标题会被适配器并入那一行
<<< END U008954 >>>
<<< UNIT U008955 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:144-155 | ctx=SettingRow >>>
面板中的一行设置。

各字段均为已翻译的字符串。模块运行于服务端进程，会话语言在此已经确定，就地翻译
可使渲染阶段只关心排版。取值若留作消息元素，还会在充当 :class:`I18NContext` 的
参数时被强制转为字符串字面量（见 ``akaribot/core/builtins/message/chain.py`` 的参数翻译一段）。

:param label: 设置名。
:param value: 当前取值。
:param action: 交互入口上展示的文案。
:param command: 不含前缀的完整命令，尽可能带上当前取值，前缀由渲染阶段补上。
<<< END U008955 >>>
<<< UNIT U008956 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/setup.py:317-337 | ctx=render_rows >>>
将设置行渲染为消息元素。

每一行都在行尾附加指令操作，点击即把命令连同当前取值填入输入框。开关不另设底部按钮，
因为按钮虽能一键切换，却与所属的设置行相隔一段距离，需要用户自行对应。把入口一律放在各自
那一行，整个面板的读法才是一致的。不支持指令操作的平台由消息链自动降级为纯文本，
模块方无须再分支。

换行的写法随平台而分。指令操作在支持它的平台上会作为独立元素留给适配器，而适配器会把
紧随其后的文本一并并入上一行（见 ``akaribot/adapters/qqbot/context.py`` 的 ``inline_pending``），
换行若交由适配器按元素处理，整个面板会合并成一行，故此路径下须把换行写入文本自身。
降级平台上指令操作已在消息链阶段并入前一个文本元素，各行本就是独立元素，再写换行反倒
会多出空行。标题同样以纯文本构造而非 :class:`I18NContext`，正是为了能在其前补上换行。

:param msg: 消息会话。
:param title_key: 分组标题的多语言键。
:param rows: 设置行列表。
:param can_edit: 当前用户是否可以修改这一组设置。
:param after_inline: 本组之前是否紧跟着一个行内入口，为 True 时标题须自带换行。
:return: 消息元素列表。
<<< END U008956 >>>
<<< UNIT U008957 | py-docstring | packages/akari-bot-core/akaribot/modules/core/common_tools/version.py:10-10 | ctx=get_version_display >>>
返回面向用户展示的版本号。未知版本时返回 None。
<<< END U008957 >>>
<<< UNIT U008958 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:7-7 | ctx=about >>>
此模块输出机器人的简介、版本、制作人员、权限配置链接与运行状态。别名 `version`、`ping`、`status` 指向对应子命令。
<<< END U008958 >>>
<<< UNIT U008959 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:13-13 | ctx=`about` >>>
此命令输出机器人简介、仓库与反馈链接，以及制作人员入口。配图取自品牌资产，链接取自 `repo_url`、`issue_url`、`donate_url` 配置。平台支持按钮时，这些入口显示为按钮。
<<< END U008959 >>>
<<< UNIT U008960 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:16-22 | ctx=`about` >>>
  :log="[
    '用户：~about',
    '机器人：小可是由 Teahouse Studios 出品的多功能、跨平台、可自由扩展的聊天机器人助手，基于 AGPL-3.0 协议开源。',
    '请支持我们的工作以便持续开发与维护。',
    '开源存储库地址：https://github.com/Teahouse-Studios/akari-bot',
  ]"
/>
<<< END U008960 >>>
<<< UNIT U008961 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:28-28 | ctx=`about version` >>>
此命令输出机器人版本。从源码运行时附带对应的提交链接，发行版附带发行标签链接。版本号未知时给出提示。链接是否附带由 `enable_commit_url` 控制。
<<< END U008961 >>>
<<< UNIT U008962 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:31-36 | ctx=`about version` >>>
  :log="[
    '用户：~about version',
    '机器人：当前机器人版本号：`1a2b3c4`',
    'https://github.com/Teahouse-Studios/akari-bot/commit/1a2b3c4',
  ]"
/>
<<< END U008962 >>>
<<< UNIT U008963 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:42-42 | ctx=`about credits` >>>
此命令输出制作人员名单。品牌资产中缺少名单文件，或名单内容为空时，机器人提示不可用。
<<< END U008963 >>>
<<< UNIT U008964 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:45-51 | ctx=`about credits` >>>
  :log="[
    '用户：~about credits',
    '机器人：```开发人员名单',
    '……',
    '```',
  ]"
/>
<<< END U008964 >>>
<<< UNIT U008965 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:57-57 | ctx=`about permissions` >>>
此命令仅在 QQBot 平台可用，用于生成群聊的权限配置链接。省略群号时返回带占位提示的命令补全入口。群号不是数字时返回提示。
<<< END U008965 >>>
<<< UNIT U008966 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:60-64 | ctx=`about permissions` >>>
  :log="[
    '用户：~about permissions 123456789',
    '机器人：使用 Android 手机点击以下按钮可快速设置权限：',
  ]"
/>
<<< END U008966 >>>
<<< UNIT U008967 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:70-70 | ctx=`about ping` >>>
此命令返回 Pong，以及运行时长、CPU、内存与磁盘占用。
<<< END U008967 >>>
<<< UNIT U008968 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:73-79 | ctx=`about ping` >>>
  :log="[
    '用户：~about ping',
    '机器人：Pong!',
    '机器人已运行：03:12:45',
    '处理器使用率：7.4%',
  ]"
/>
<<< END U008968 >>>
<<< UNIT U008969 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:85-85 | ctx=`about status` >>>
此命令输出系统与运行时详情，包含进程占用与 WebRender 状态。
<<< END U008969 >>>
<<< UNIT U008970 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/about.md:88-94 | ctx=`about status` >>>
  :log="[
    '用户：~about status',
    '机器人：系统启动时间：2026-11-01 08:03:11 (UTC+8)',
    '机器人已运行：03:12:45',
    'Python 版本：3.12.7',
  ]"
/>
<<< END U008970 >>>
<<< UNIT U008971 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:9-9 | ctx=abuse >>>
此模块用于管理用户的警告次数、临时封禁与黑白名单，也可以屏蔽指定的场景。模块级权限为超级用户。
<<< END U008971 >>>
<<< UNIT U008972 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:15-15 | ctx=`abuse check` >>>
此命令查看用户的警告次数、临时封禁与黑白名单状态。用户还没有 union 记录时，机器人先要求确认，再创建记录。
<<< END U008972 >>>
<<< UNIT U008973 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:18-23 | ctx=`abuse check` >>>
  :log="[
    '用户：~abuse check QQ|123456',
    '机器人：用户 QQ|123456 已被警告 2 次。',
    '（此用户已处于黑名单）',
  ]"
/>
<<< END U008973 >>>
<<< UNIT U008974 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:29-29 | ctx=`abuse warn` >>>
此命令增加警告次数，`<count>` 默认为 1。累计警告次数超过 `tos_warning_counts`，且用户不在白名单时，机器人将其转入黑名单。临时封禁的时长取自 `tos_temp_ban_time`，封禁动作由 `tos` 钩子执行，见 [tos](tos.md)。
<<< END U008974 >>>
<<< UNIT U008975 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:32-36 | ctx=`abuse warn` >>>
  :log="[
    '用户：~abuse warn QQ|123456',
    '机器人：成功警告用户 QQ|123456 1 次。此用户已被警告 3 次。',
  ]"
/>
<<< END U008975 >>>
<<< UNIT U008976 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:42-42 | ctx=`abuse revoke` >>>
此命令减少警告次数，`<count>` 默认为 1。
<<< END U008976 >>>
<<< UNIT U008977 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:45-49 | ctx=`abuse revoke` >>>
  :log="[
    '用户：~abuse revoke QQ|123456',
    '机器人：成功移除用户 QQ|123456 的 1 次警告。此用户已被警告 2 次。',
  ]"
/>
<<< END U008977 >>>
<<< UNIT U008978 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:55-55 | ctx=`abuse clear` >>>
此命令将用户的警告次数清零。
<<< END U008978 >>>
<<< UNIT U008979 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:58-62 | ctx=`abuse clear` >>>
  :log="[
    '用户：~abuse clear QQ|123456',
    '机器人：成功清除用户 QQ|123456 的警告。',
  ]"
/>
<<< END U008979 >>>
<<< UNIT U008980 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:68-68 | ctx=`abuse untempban` >>>
此命令解除临时封禁，具体处理交给 `tos.remove_temp_ban` 钩子。
<<< END U008980 >>>
<<< UNIT U008981 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:71-75 | ctx=`abuse untempban` >>>
  :log="[
    '用户：~abuse untempban QQ|123456',
    '机器人：成功解除用户 QQ|123456 的临时封禁。',
  ]"
/>
<<< END U008981 >>>
<<< UNIT U008982 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:81-81 | ctx=`abuse ban` >>>
此命令将用户加入黑名单，同时移出白名单。
<<< END U008982 >>>
<<< UNIT U008983 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:84-88 | ctx=`abuse ban` >>>
  :log="[
    '用户：~abuse ban QQ|123456',
    '机器人：成功将用户 QQ|123456 加入黑名单。',
  ]"
/>
<<< END U008983 >>>
<<< UNIT U008984 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:94-94 | ctx=`abuse unban` >>>
此命令将用户移出黑名单。
<<< END U008984 >>>
<<< UNIT U008985 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:97-101 | ctx=`abuse unban` >>>
  :log="[
    '用户：~abuse unban QQ|123456',
    '机器人：成功将用户 QQ|123456 移除黑名单。',
  ]"
/>
<<< END U008985 >>>
<<< UNIT U008986 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:107-107 | ctx=`abuse trust` >>>
此命令将用户加入白名单，同时移出黑名单。白名单中的用户不会因警告被封禁。
<<< END U008986 >>>
<<< UNIT U008987 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:110-114 | ctx=`abuse trust` >>>
  :log="[
    '用户：~abuse trust QQ|123456',
    '机器人：成功将用户 QQ|123456 加入白名单。',
  ]"
/>
<<< END U008987 >>>
<<< UNIT U008988 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:120-120 | ctx=`abuse distrust` >>>
此命令将用户移出白名单。
<<< END U008988 >>>
<<< UNIT U008989 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:123-127 | ctx=`abuse distrust` >>>
  :log="[
    '用户：~abuse distrust QQ|123456',
    '机器人：成功将用户 QQ|123456 移除白名单。',
  ]"
/>
<<< END U008989 >>>
<<< UNIT U008990 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:133-133 | ctx=`abuse block` >>>
此命令仅在 QQ 可用，用于屏蔽指定场景。`<target>` 须为带 `QQ|Group|` 前缀的完整 ID，且不能是当前场景。
<<< END U008990 >>>
<<< UNIT U008991 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:136-140 | ctx=`abuse block` >>>
  :log="[
    '用户：~abuse block QQ|Group|987654321',
    '机器人：成功将群聊 QQ|Group|987654321 加入黑名单。',
  ]"
/>
<<< END U008991 >>>
<<< UNIT U008992 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:146-146 | ctx=`abuse unblock` >>>
此命令仅在 QQ 可用，用于解除对指定场景的屏蔽。
<<< END U008992 >>>
<<< UNIT U008993 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/abuse.md:149-153 | ctx=`abuse unblock` >>>
  :log="[
    '用户：~abuse unblock QQ|Group|987654321',
    '机器人：成功将群聊 QQ|Group|987654321 移除黑名单。',
  ]"
/>
<<< END U008993 >>>
<<< UNIT U008994 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:7-7 | ctx=admin >>>
此模块用于管理本场景的管理员名单与封禁名单，也可以让机器人退出群聊。模块级权限为场景管理员。别名 `ban`、`unban`、`ban list`、`leave`、`dismiss` 分别指向对应的子命令，可以直接调用。
<<< END U008994 >>>
<<< UNIT U008995 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:13-13 | ctx=`admin add` >>>
此命令把用户加入本场景的机器人管理员名单。`<user>` 须为带平台前缀的完整 ID（如 `QQ|123456`），缺少前缀时，机器人会提示先用 `bind whoami` 查询。平台原生管理员与已在名单中的用户无需执行此命令。
<<< END U008995 >>>
<<< UNIT U008996 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:16-20 | ctx=`admin add` >>>
  :log="[
    '用户：~admin add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为机器人管理员。',
  ]"
/>
<<< END U008996 >>>
<<< UNIT U008997 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:26-26 | ctx=`admin remove` >>>
此命令把用户移出本场景的机器人管理员名单。移除自己时，机器人会要求输入确认内容，确认后才执行。平台原生管理员无法通过此命令移除。
<<< END U008997 >>>
<<< UNIT U008998 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:29-33 | ctx=`admin remove` >>>
  :log="[
    '用户：~admin remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出机器人管理员。',
  ]"
/>
<<< END U008998 >>>
<<< UNIT U008999 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:39-39 | ctx=`admin list` >>>
此命令列出本场景的管理员。名单按用户记录，展示时展开为该用户绑定的平台账号，一行对应一个用户。
<<< END U008999 >>>
<<< UNIT U009000 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:42-47 | ctx=`admin list` >>>
  :log="[
    '用户：~admin list',
    '机器人：当前被手动设置的机器人管理员：',
    'QQ|123456',
  ]"
/>
<<< END U009000 >>>
<<< UNIT U009001 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:53-53 | ctx=`admin ban` >>>
此命令禁止用户在本场景使用机器人，不能封禁自己。封禁记录按用户保存，同一用户绑定的其他平台账号一并受限。
<<< END U009001 >>>
<<< UNIT U009002 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:56-60 | ctx=`admin ban` >>>
  :log="[
    '用户：~admin ban QQ|123456',
    '机器人：成功限制用户 QQ|123456 使用机器人。',
  ]"
/>
<<< END U009002 >>>
<<< UNIT U009003 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:66-66 | ctx=`admin unban` >>>
此命令解除对用户的封禁。
<<< END U009003 >>>
<<< UNIT U009004 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:69-73 | ctx=`admin unban` >>>
  :log="[
    '用户：~admin unban QQ|123456',
    '机器人：成功取消限制用户 QQ|123456 使用机器人。',
  ]"
/>
<<< END U009004 >>>
<<< UNIT U009005 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:79-79 | ctx=`admin ban list` >>>
此命令列出本场景被禁止的用户。名单按用户记录，展示时展开为该用户绑定的平台账号。
<<< END U009005 >>>
<<< UNIT U009006 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:82-87 | ctx=`admin ban list` >>>
  :log="[
    '用户：~admin ban list',
    '机器人：当前被设置限制使用机器人的成员：',
    'QQ|123456',
  ]"
/>
<<< END U009006 >>>
<<< UNIT U009007 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:93-93 | ctx=`admin leave` >>>
此命令仅在 QQ 群聊可用，用于让机器人退出当前群聊，执行前需要你确认。命令只注册于 `QQ|Group` 场景。
<<< END U009007 >>>
<<< UNIT U009008 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/admin.md:96-102 | ctx=`admin leave` >>>
  :log="[
    '用户：~admin leave',
    '机器人：你确定吗？此操作不可逆。',
    '用户：是',
    '机器人：已执行，再见。',
  ]"
/>
<<< END U009008 >>>
<<< UNIT U009009 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:9-9 | ctx=analytics >>>
此模块用于统计命令的调用次数与分布。模块级权限为超级用户。
<<< END U009009 >>>
<<< UNIT U009010 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:15-15 | ctx=`analytics` >>>
此命令输出命令总数、今日命令数与首条记录的时间。
<<< END U009010 >>>
<<< UNIT U009011 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:18-23 | ctx=`analytics` >>>
  :log="[
    '用户：~analytics',
    '机器人：机器人已执行命令次数（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：12486',
    '今日已执行命令次数：98',
  ]"
/>
<<< END U009011 >>>
<<< UNIT U009012 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:29-29 | ctx=`analytics days` >>>
此命令输出近 30 天的命令数折线图，可按模块过滤。
<<< END U009012 >>>
<<< UNIT U009013 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:32-36 | ctx=`analytics days` >>>
  :log="[
    '用户：~analytics days',
    '机器人：最近 30 天的所有命令调用次数统计（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：',
  ]"
/>
<<< END U009013 >>>
<<< UNIT U009014 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:42-42 | ctx=`analytics year` >>>
此命令输出近 12 个月的命令数折线图，可按模块过滤。
<<< END U009014 >>>
<<< UNIT U009015 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:45-49 | ctx=`analytics year` >>>
  :log="[
    '用户：~analytics year petal',
    '机器人：最近一年的“petal”命令调用次数统计（自 2026-11-01 00:00:00 (UTC+8) 开始统计）：',
  ]"
/>
<<< END U009015 >>>
<<< UNIT U009016 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:55-55 | ctx=`analytics modules` >>>
此命令以横向条形图输出模块命令调用排行。`<rank>` 默认为 30。
<<< END U009016 >>>
<<< UNIT U009017 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:58-62 | ctx=`analytics modules` >>>
  :log="[
    '用户：~analytics modules 5',
    '机器人：（横向条形图：模块命令调用次数排行，取前 5 个模块）',
  ]"
/>
<<< END U009017 >>>
<<< UNIT U009018 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/analytics.md:64-64 | ctx=`analytics modules` >>>
统计功能关闭时，机器人提示该功能已停用。缺少 `matplotlib` 时，机器人提示安装 `image` extra，不生成图表。统计数据由 `telemetry` 写入，见 [telemetry](telemetry.md)。
<<< END U009018 >>>
<<< UNIT U009019 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/auth.md:7-7 | ctx=auth >>>
此模块让超级用户把某个模块的超级用户权限授予其他用户。使用此模块的命令需要超级用户权限。授权只对声明了 `required_superuser` 的模块生效。
<<< END U009019 >>>
<<< UNIT U009020 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/auth.md:13-13 | ctx=`auth add` >>>
此命令把指定模块的超级用户权限授予目标用户。执行前需要按提示确认，授权记录中会同时记录授权者。目标模块未声明 `required_superuser` 时，此命令会被拒绝。
<<< END U009020 >>>
<<< UNIT U009021 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/auth.md:16-22 | ctx=`auth add` >>>
  :log="[
    '用户：~auth add QQ|123456 update',
    '机器人：你确定吗？',
    '（此为危险操作，完全发送“我授权用户 QQ|123456 使用模块 update。”来确认）',
    '用户：我授权用户 QQ|123456 使用模块 update。',
  ]"
/>
<<< END U009021 >>>
<<< UNIT U009022 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/auth.md:28-28 | ctx=`auth remove` >>>
此命令撤销授权，只删除自己授予的条目。授权者失去超级用户身份后，对应的授权不再生效。
<<< END U009022 >>>
<<< UNIT U009023 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/auth.md:31-35 | ctx=`auth remove` >>>
  :log="[
    '用户：~auth remove QQ|123456 update',
    '机器人：已取消 QQ|123456 使用模块 update 的授权。',
  ]"
/>
<<< END U009023 >>>
<<< UNIT U009024 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/auth.md:41-41 | ctx=`auth list` >>>
此命令列出用户获得的模块授权。
<<< END U009024 >>>
<<< UNIT U009025 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/auth.md:44-48 | ctx=`auth list` >>>
  :log="[
    '用户：~auth list QQ|123456',
    '机器人：QQ|123456 被 QQ|654321 授权使用模块 update',
  ]"
/>
<<< END U009025 >>>
<<< UNIT U009026 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:7-7 | ctx=bind >>>
此模块把不同平台上的同一用户、同一现实场景归入同一个 union（用户组或场景组）。别名 `whoami`、`merge`、`merge token` 指向对应子命令。
<<< END U009026 >>>
<<< UNIT U009027 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:13-13 | ctx=`bind` >>>
此命令查看当前用户与当前场景各自所属的 union，以及其中已绑定的平台账号。
<<< END U009027 >>>
<<< UNIT U009028 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:16-22 | ctx=`bind` >>>
  :log="[
    '用户：~bind',
    '机器人：当前用户所属的用户组：`USID|7C4F0B2E9A1D4E6B8C3A5F7D1E9B2C4A`',
    '已绑定 1 个用户：',
    '`QQ|Group|123456789`',
  ]"
/>
<<< END U009028 >>>
<<< UNIT U009029 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:28-28 | ctx=`bind whoami` >>>
此命令显示发送者的平台 ID、union ID 与权限身份，同时列出当前场景的平台 ID 与 union ID。场景管理员、平台原生管理员与超级用户身份分别标注。
<<< END U009029 >>>
<<< UNIT U009030 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:31-37 | ctx=`bind whoami` >>>
  :log="[
    '用户：~bind whoami',
    '机器人：你的 ID：`QQ|Group|123456789`',
    '本群聊的 ID：`QQ|Group|123456789`',
    '当前用户所属的用户组：`USID|7C4F0B2E9A1D4E6B8C3A5F7D1E9B2C4A`',
  ]"
/>
<<< END U009030 >>>
<<< UNIT U009031 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:43-43 | ctx=`bind self` >>>
此命令列出当前用户绑定的全部账号。
<<< END U009031 >>>
<<< UNIT U009032 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:46-52 | ctx=`bind self` >>>
  :log="[
    '用户：~bind self',
    '机器人：当前用户所属的用户组：`USID|7C4F0B2E9A1D4E6B8C3A5F7D1E9B2C4A`',
    '已绑定 1 个用户：',
    '`QQ|Group|123456789`',
  ]"
/>
<<< END U009032 >>>
<<< UNIT U009033 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:58-58 | ctx=`bind start` >>>
此命令生成绑定码。在群内执行需要场景管理员权限。私聊中生成的绑定码同时包含发送者与私聊场景，使用后两者一起绑定。在群内生成的绑定码只合并场景组。
<<< END U009033 >>>
<<< UNIT U009034 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:61-65 | ctx=`bind start` >>>
  :log="[
    '用户：~bind start',
    '机器人：绑定码已通过私信发送，请注意查收。（请注意给新的机器人开启必要的权限，如获取全部消息和主动消息权限）',
  ]"
/>
<<< END U009034 >>>
<<< UNIT U009035 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:71-71 | ctx=`bind token` >>>
此命令用绑定码完成绑定。在群内执行需要场景管理员权限。绑定码只能在同类场景中使用，跨类型使用会被拒绝。绑定码失效时会返回提示。
<<< END U009035 >>>
<<< UNIT U009036 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:74-80 | ctx=`bind token` >>>
  :log="[
    '用户：~bind token 7K3M9Q',
    '机器人：绑定成功，新的场景组：`UTID|3E8C1A5F7B9D2E4C6A8B0D2F4E6C8A1B`',
    '已绑定 2 个群聊：',
    '`QQ|Group|123456789`[消息通道 1]',
  ]"
/>
<<< END U009036 >>>
<<< UNIT U009037 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:86-86 | ctx=`bind self remove` >>>
此命令解绑当前用户的某个账号，执行前须确认。最后一个账号不可解绑。
<<< END U009037 >>>
<<< UNIT U009038 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:89-95 | ctx=`bind self remove` >>>
  :log="[
    '用户：~bind self remove QQ|Group|123456789',
    '机器人：即将把 `QQ|Group|123456789` 移出当前用户组，该用户将不再共享组内数据且无法自动恢复，是否继续？',
    '用户：是',
    '机器人：已将 `QQ|Group|123456789` 移出当前用户组。',
  ]"
/>
<<< END U009038 >>>
<<< UNIT U009039 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:101-101 | ctx=`bind target` >>>
此命令查看当前场景绑定的平台入口。
<<< END U009039 >>>
<<< UNIT U009040 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:104-110 | ctx=`bind target` >>>
  :log="[
    '用户：~bind target',
    '机器人：当前群聊所属的场景组：`UTID|3E8C1A5F7B9D2E4C6A8B0D2F4E6C8A1B`',
    '已绑定 2 个群聊：',
    '`QQ|Group|123456789`[消息通道 1]',
  ]"
/>
<<< END U009040 >>>
<<< UNIT U009041 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:116-116 | ctx=`bind target remove` >>>
此命令解绑当前场景的某个平台入口，执行前须确认。最后一个入口不可解绑。
<<< END U009041 >>>
<<< UNIT U009042 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:119-125 | ctx=`bind target remove` >>>
  :log="[
    '用户：~bind target remove QQ|Group|987654321',
    '机器人：即将把 `QQ|Group|987654321` 移出当前场景组，该群聊将不再共享组内数据且无法自动恢复，是否继续？',
    '用户：是',
    '机器人：已将 `QQ|Group|987654321` 移出当前场景组。',
  ]"
/>
<<< END U009042 >>>
<<< UNIT U009043 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:131-131 | ctx=`bind channel` >>>
此命令查看当前场景的消息通道编号，以及共用该通道的其他场景的数量与编号。
<<< END U009043 >>>
<<< UNIT U009044 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:134-140 | ctx=`bind channel` >>>
  :log="[
    '用户：~bind channel',
    '机器人：当前群聊的消息通道：1 号',
    '同通道的群聊共 1 个：',
    '`QQ|Group|123456789`',
  ]"
/>
<<< END U009044 >>>
<<< UNIT U009045 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:146-146 | ctx=`bind channel set` >>>
此命令设置当前场景的消息通道编号。通道编号相同的场景在命令执行与消息推送时会去重。
<<< END U009045 >>>
<<< UNIT U009046 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:149-153 | ctx=`bind channel set` >>>
  :log="[
    '用户：~bind channel set 2',
    '机器人：已将当前群聊的消息通道设为 2 号。同一号的群聊会被视为现实中的同一个群聊（例如一个群聊里同时有两个机器人），命令只由其中一个机器人执行，推送只发送一次。',
  ]"
/>
<<< END U009046 >>>
<<< UNIT U009047 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:159-159 | ctx=`bind channel reset` >>>
此命令把当前场景的消息通道编号重置为默认值。
<<< END U009047 >>>
<<< UNIT U009048 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:162-166 | ctx=`bind channel reset` >>>
  :log="[
    '用户：~bind channel reset',
    '机器人：已让当前群聊脱离原有通道，现单独占用 3 号通道。',
  ]"
/>
<<< END U009048 >>>
<<< UNIT U009049 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:172-172 | ctx=`bind auto` >>>
仅当 `enable_bind_auto` 开启时才注册此命令。此命令与同一场景内的其他机器人实例自动配对。配对完成后，两个实例合并场景组、统一消息通道编号，并互相记录对方的账号，用来屏蔽对方的消息。
<<< END U009049 >>>
<<< UNIT U009050 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:178-178 | ctx=`bind channel probe` >>>
这是内部命令，不需要手动执行。它由 `bind auto` 自动发出，用于响应握手请求。口令只能使用一次，使用后失效。
<<< END U009050 >>>
<<< UNIT U009051 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:184-184 | ctx=`bind channel confirm` >>>
这是内部命令，不需要手动执行。它由 `bind auto` 自动发出，用于结束握手。双方确认处于同一场景后，机器人把两个场景合并到同一条消息通道。
<<< END U009051 >>>
<<< UNIT U009052 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/bind.md:186-186 | ctx=`bind channel confirm` >>>
绑定码为 6 位大写字母与数字，有效期 300 秒，只保存在 Server 进程的内存中，重启即失效。场景数据中的 `command_prefix` 与 `command_alias` 随场景 union 一起迁移，绑定后以合并结果为准。
<<< END U009052 >>>
<<< UNIT U009053 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:9-9 | ctx=config >>>
此模块可以读取、写入和删除配置项。模块级权限为超级用户。
<<< END U009053 >>>
<<< UNIT U009054 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:15-15 | ctx=`config get` >>>
读取配置项的值。省略表名时，命令在 `config.toml` 的主表内查找。
<<< END U009054 >>>
<<< UNIT U009055 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:18-22 | ctx=`config get` >>>
  :log="[
    '用户：~config get auto_purge_crontab',
    '机器人：0 0 * * *',
  ]"
/>
<<< END U009055 >>>
<<< UNIT U009056 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:28-28 | ctx=`config write` >>>
写入配置项。配置值按类型解析，`true` 和 `false` 转为布尔值，整数与浮点数转为对应数值。以 `[...]` 写出的值按 JSON 解析为列表，其余内容按字符串写入。`-s` 表示按密钥项处理，核心配置写入 `[secret]`，平台和模块配置写入对应的 `_secret` 表。
<<< END U009056 >>>
<<< UNIT U009057 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:30-30 | ctx=`config write` >>>
写入尚不存在的键会改变配置文件的结构，此时命令会在执行前要求确认。
<<< END U009057 >>>
<<< UNIT U009058 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:33-37 | ctx=`config write` >>>
  :log="[
    '用户：~config write enable_joke false',
    '机器人：成功。',
  ]"
/>
<<< END U009058 >>>
<<< UNIT U009059 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:43-43 | ctx=`config delete` >>>
删除配置项。执行时调用 `CFGManager.edit_delete()`，返回成功或失败。
<<< END U009059 >>>
<<< UNIT U009060 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:45-45 | ctx=`config delete` >>>
表名形如 `bot_<平台>`、`module_<模块>`。配置只读时，进程不能直接修改配置文件，写入改用 `CFGManager.edit_write()`，删除改用 `edit_delete()`。字段布局、只读限制和版本机制见[配置](../../../core/docs/config.md)。
<<< END U009060 >>>
<<< UNIT U009061 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/config.md:48-52 | ctx=`config delete` >>>
  :log="[
    '用户：~config delete enable_joke',
    '机器人：成功。',
  ]"
/>
<<< END U009061 >>>
<<< UNIT U009062 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/database.md:9-9 | ctx=database >>>
此模块用于调试和排查故障，可以直接操作数据库，只在开发模式下加载。模块级权限为超级用户。
<<< END U009062 >>>
<<< UNIT U009063 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/database.md:15-15 | ctx=`database model` >>>
列出核心和各模块注册的数据表名。
<<< END U009063 >>>
<<< UNIT U009064 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/database.md:21-21 | ctx=`database field` >>>
列出每个字段的名称、类型以及是否可以为空。
<<< END U009064 >>>
<<< UNIT U009065 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/database.md:23-23 | ctx=`database field` >>>
默认渲染为图片表格。平台不支持图片或指定 `--legacy` 时，改用文本表格。表名不存在时返回无结果提示。
<<< END U009065 >>>
<<< UNIT U009066 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/database.md:29-29 | ctx=`database exec` >>>
执行 SQL 语句。`SELECT` 查询按每页 10 行展示，页码超出范围时改用最接近的有效页。其他语句直接执行，返回影响的行数。
<<< END U009066 >>>
<<< UNIT U009067 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/database.md:31-31 | ctx=`database exec` >>>
默认渲染为图片表格。平台不支持图片或指定 `--legacy` 时，改用文本表格。
<<< END U009067 >>>
<<< UNIT U009068 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/echo.md:7-7 | ctx=echo >>>
此模块可以原文复述消息内容。模块级权限为超级用户。
<<< END U009068 >>>
<<< UNIT U009069 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/echo.md:13-13 | ctx=`echo` >>>
此命令会原文复述给定的内容，不解析消息元素。省略参数时，命令会等待你发送下一条消息，再复述这条消息的显示文本。
<<< END U009069 >>>
<<< UNIT U009070 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/echo.md:16-22 | ctx=`echo` >>>
  :log="[
    '用户：~echo',
    '机器人：请发送想要重复的消息。',
    '用户：今天的布丁很好吃',
    '机器人：今天的布丁很好吃',
  ]"
/>
<<< END U009070 >>>
<<< UNIT U009071 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/eval.md:7-7 | ctx=eval >>>
此模块仅在开发模式下加载，可以执行 Python 表达式。模块级权限为超级用户。
<<< END U009071 >>>
<<< UNIT U009072 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/eval.md:13-13 | ctx=`eval` >>>
此命令在包含 `msg` 和 `Bot` 的命名空间中执行表达式。结果以纯文本返回，不经过敏感内容检查。表达式抛出异常时，异常会被包装成 `NoReportException` 后回显，不进入错误上报流程。
<<< END U009072 >>>
<<< UNIT U009073 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/features.md:7-7 | ctx=features >>>
此模块可以查看当前会话的能力标志。模块级权限为超级用户。
<<< END U009073 >>>
<<< UNIT U009074 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/features.md:13-13 | ctx=`features` >>>
此命令逐项列出当前会话的能力标志，并主动获取同一场景的会话作为对照，有差异的项用 `*` 标出。主动获取失败时，主动会话一列显示未知。字段来自 `Features`，见[适配器开发](../../../core/docs/adapter-development.md)。
<<< END U009074 >>>
<<< UNIT U009075 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/features.md:16-22 | ctx=`features` >>>
  :log="[
    '用户：~features',
    '机器人：QQ|Group 的特性标志（当前会话 / 主动会话）：',
    'support_image: 是 / 是',
    'support_audio: 否 / 否',
  ]"
/>
<<< END U009075 >>>
<<< UNIT U009076 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:7-7 | ctx=help >>>
此模块输出模块清单和命令帮助。
<<< END U009076 >>>
<<< UNIT U009077 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:13-13 | ctx=`help` >>>
说明：
<<< END U009077 >>>
<<< UNIT U009078 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/help.md:15-19 | ctx=`help` >>>
- 省略模块名时，按当前场景列出可用模块的清单和启用状态。
- 清单带锁定和订阅标记，并提供启用、停用按钮。
- `hidden=True` 的模块不出现在清单中。平台不支持的模块以删除线标注。
- 给出模块名时，展示这个模块的简介和命令模板。
- 超级用户命令对非超级用户隐藏，管理员命令对普通成员隐藏。
<<< END U009078 >>>
<<< UNIT U009079 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:22-28 | ctx=`help` >>>
  :log="[
    '用户：~help bind',
    '机器人：管理用户组、场景组与消息通道，同一组内的用户或群聊共享同一份数据。',
    '`~bind self remove <user>` - 将指定用户移出当前用户组。',
    '`~bind token <code>` - 填入另一处生成的绑定码以完成绑定。',
  ]"
/>
<<< END U009079 >>>
<<< UNIT U009080 | md-heading | packages/akari-bot-core/akaribot/modules/core/docs/help.md:31-31 | ctx=输出样式 >>>
## 输出样式
<<< END U009080 >>>
<<< UNIT U009081 | md-heading | packages/akari-bot-core/akaribot/modules/core/docs/help.md:33-33 | ctx=Markdown 表格（QQBot） >>>
### Markdown 表格（QQBot）
<<< END U009081 >>>
<<< UNIT U009082 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:35-35 | ctx=Markdown 表格（QQBot） >>>
平台支持 Markdown 扩展时，模块清单排成一张表，QQBot 使用这种样式。点击模块名会填入对应的 `help` 命令。
<<< END U009082 >>>
<<< UNIT U009083 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:38-46 | ctx=Markdown 表格（QQBot） >>>
  :messages="[
    { role: 'user', text: '~help' },
    {
      role: 'bot',
      markdown: true,
      text: '| AkariBot | 简体中文 | 版本：v0.1.1 | 权限：管理员 |\n| --- | --- | --- | --- |\n| 基础模块 | | | |\n| 🔓 help | 🔓 module | 🔓 admin | 🔓 bind |\n| 扩展模块 | 🔓 = 已开启 | 🔐 = 已关闭 | |\n| 🔓 wiki | 🔓 maimai | 🔓 ncmusic | 🔓 rss |\n| 订阅扩展模块 | 🔔 = 已开启 | 🔕 = 已关闭 | |\n| 🔔 rss | 🔔 bilibili | 🔔 minecraft_news | |\n\n向右滑动以查看所有模块，点击可自动填入对应帮助命令。',
    },
  ]"
/>
<<< END U009083 >>>
<<< UNIT U009084 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:48-48 | ctx=Markdown 表格（QQBot） >>>
示例中的表格是静态的。实际消息里，语言、版本和模块名是可点击的动作文本，点击后填入对应的命令。
<<< END U009084 >>>
<<< UNIT U009085 | md-heading | packages/akari-bot-core/akaribot/modules/core/docs/help.md:50-50 | ctx=图片模块列表 >>>
### 图片模块列表
<<< END U009085 >>>
<<< UNIT U009086 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:52-52 | ctx=图片模块列表 >>>
当 Markdown 表格不可用、平台支持图片且未强制文本模式时，模块清单渲染为一张图片。模块按基础、扩展、订阅分组，未启用的模块单独着色。
<<< END U009086 >>>
<<< UNIT U009087 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:55-60 | ctx=图片模块列表 >>>
  :image-width="720"
  :messages="[
    { role: 'user', text: '~help' },
    { role: 'bot', text: '![模块列表（示例数据）](help-modules.png)' },
  ]"
/>
<<< END U009087 >>>
<<< UNIT U009088 | md-heading | packages/akari-bot-core/akaribot/modules/core/docs/help.md:62-62 | ctx=文本模式 >>>
### 文本模式
<<< END U009088 >>>
<<< UNIT U009089 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:64-64 | ctx=文本模式 >>>
Markdown 表格不可用、图片渲染失败或指定 `--legacy` 时，模块清单按分组输出为纯文本，模块之间用 `|` 分隔。
<<< END U009089 >>>
<<< UNIT U009090 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:67-75 | ctx=文本模式 >>>
  :log="[
    '用户：~help --legacy',
    '机器人：基础模块：',
    '🔓 help | 🔓 module | 🔓 admin | 🔓 bind',
    '扩展模块：',
    '🔓 wiki | 🔓 maimai | 🔓 ncmusic | 🔓 rss',
    '使用“~help <模块名称>”查看详细信息。',
  ]"
/>
<<< END U009090 >>>
<<< UNIT U009091 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:77-77 | ctx=文本模式 >>>
`--img` 优先渲染图片，渲染不可用时改用文本。`--legacy` 强制文本模式。
<<< END U009091 >>>
<<< UNIT U009092 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:79-79 | ctx=文本模式 >>>
模块顺序和启用状态取自场景的 `modules` 列，基础模块始终显示为已启用。未启用的模块可以通过清单按钮或 `module enable <module>` 启用。
<<< END U009092 >>>
<<< UNIT U009093 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/help.md:81-81 | ctx=文本模式 >>>
模块的帮助文案来自命令模板末尾的 `I18N:key`，简介来自 `module(desc=...)`。
<<< END U009093 >>>
<<< UNIT U009094 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/jobqueue.md:7-7 | ctx=jobqueue >>>
此模块可以清空计划任务队列。模块级权限为超级用户。
<<< END U009094 >>>
<<< UNIT U009095 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/jobqueue.md:13-13 | ctx=`jobqueue clear` >>>
此命令清空计划任务队列，正在执行的任务也一并删除。
<<< END U009095 >>>
<<< UNIT U009096 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/jobqueue.md:16-20 | ctx=`jobqueue clear` >>>
  :log="[
    '用户：~jobqueue clear',
    '机器人：成功。',
  ]"
/>
<<< END U009096 >>>
<<< UNIT U009097 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/merge.md:7-7 | ctx=merge >>>
此模块属于隐藏模块，仅在 `retired_clients` 非空时加载。命令注册在 `bind` 上，模块本身只保留退役公告的正则触发器。
<<< END U009097 >>>
<<< UNIT U009098 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/merge.md:13-13 | ctx=`bind merge` >>>
此命令只在已退役的源客户端上注册，并在该客户端生成迁移码。在私聊中执行时，发送者和私聊场景的数据一并迁移。在群内执行时要求场景管理员权限。
<<< END U009098 >>>
<<< UNIT U009099 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/merge.md:19-19 | ctx=`bind merge-token` >>>
此命令仅在目标客户端注册，用迁移码合并用户和场景数据。迁移码和绑定码分开存放，使用其中一种不会消耗另一种。
<<< END U009099 >>>
<<< UNIT U009100 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/merge.md:21-21 | ctx=`bind merge-token` >>>
迁移会改写模块表中以平台 ID 为主键的数据，并同步场景管理员、封禁列表和消息通道。
<<< END U009100 >>>
<<< UNIT U009101 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/merge.md:23-23 | ctx=`bind merge-token` >>>
`retired_clients` 的格式为 `<源客户端> -> <目标客户端>`。只填写源客户端表示不提供迁移，此时不注册迁移命令，只保留退役公告。
<<< END U009101 >>>
<<< UNIT U009102 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:7-7 | ctx=module >>>
此模块可以查看模块清单，也可以启用、停用、加载、重载和卸载模块。命令级权限按子命令区分。`list` 对所有人开放，`enable` 和 `disable` 要求场景管理员，`load`、`reload`、`unload` 要求超级用户。
<<< END U009102 >>>
<<< UNIT U009103 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:9-9 | ctx=module >>>
别名 `enable`、`disable`、`load`、`reload`、`unload` 可以省略 `module` 直接使用，例如 `~enable`。
<<< END U009103 >>>
<<< UNIT U009104 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:15-15 | ctx=`module list` >>>
此命令列出当前平台可用的模块及其启用状态。默认以图片表格呈现，指定 `--legacy` 时改用文本表格。
<<< END U009104 >>>
<<< UNIT U009105 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:18-24 | ctx=`module list` >>>
  :log="[
    '用户：~module list --legacy',
    '机器人：当前可用的模块有：',
    '🔐 arcaea | 🔐 cytoid | 🔐 dice | 🔐 hitokoto',
    '使用“`~help <模块名称>`”查看详细信息。',
  ]"
/>
<<< END U009105 >>>
<<< UNIT U009106 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:30-30 | ctx=`module enable` >>>
此命令在当前场景内启用指定模块，一次可以给出多个模块名。
<<< END U009106 >>>
<<< UNIT U009107 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:32-32 | ctx=`module enable` >>>
启用前，命令检查平台能力（正则、事件、RSS）和机器人权限。平台能力或机器人权限缺失时，命令给出具体原因。模块声明了推荐模块时，命令随后询问是否一并启用。
<<< END U009107 >>>
<<< UNIT U009108 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:35-39 | ctx=`module enable` >>>
  :log="[
    '用户：~module enable dice',
    '机器人：成功：开启模块“dice”。',
  ]"
/>
<<< END U009108 >>>
<<< UNIT U009109 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:45-45 | ctx=`module enable all` >>>
此命令启用全部可启用的模块。基础模块、隐藏模块、仅超级用户授权使用的模块，以及当前平台不支持或缺少机器人权限的模块会被跳过。
<<< END U009109 >>>
<<< UNIT U009110 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:48-54 | ctx=`module enable all` >>>
  :log="[
    '用户：~module enable all',
    '机器人：成功：开启模块“arcaea”。',
    '成功：开启模块“dice”。',
    '成功：开启模块“hitokoto”。',
  ]"
/>
<<< END U009110 >>>
<<< UNIT U009111 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:60-60 | ctx=`module disable` >>>
此命令在当前场景内停用指定模块。基础模块不能停用。指定基础模块时，命令返回提示，不改动场景配置。
<<< END U009111 >>>
<<< UNIT U009112 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:63-67 | ctx=`module disable` >>>
  :log="[
    '用户：~module disable dice',
    '机器人：成功：关闭模块“dice”。',
  ]"
/>
<<< END U009112 >>>
<<< UNIT U009113 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:73-73 | ctx=`module disable all` >>>
此命令停用全部可停用的模块。基础模块、隐藏模块和仅超级用户授权使用的模块会被跳过。
<<< END U009113 >>>
<<< UNIT U009114 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:76-82 | ctx=`module disable all` >>>
  :log="[
    '用户：~module disable all',
    '机器人：成功：关闭模块“arcaea”。',
    '成功：关闭模块“dice”。',
    '成功：关闭模块“hitokoto”。',
  ]"
/>
<<< END U009114 >>>
<<< UNIT U009115 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:88-88 | ctx=`module load` >>>
此命令加载已卸载的模块，对所有场景生效。
<<< END U009115 >>>
<<< UNIT U009116 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:91-95 | ctx=`module load` >>>
  :log="[
    '用户：~module load dice',
    '机器人：成功加载模块：dice',
  ]"
/>
<<< END U009116 >>>
<<< UNIT U009117 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:101-101 | ctx=`module reload` >>>
此命令重新加载指定模块。依赖该模块的其他模块会一并重载。重载范围超出给定模块时，命令在执行前列出范围并要求确认。
<<< END U009117 >>>
<<< UNIT U009118 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:104-110 | ctx=`module reload` >>>
  :log="[
    '用户：~module reload dice',
    '机器人：成功重载模块：',
    'dice',
    '未发现已加载的其余文件。',
  ]"
/>
<<< END U009118 >>>
<<< UNIT U009119 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:116-116 | ctx=`module unload` >>>
此命令卸载已加载的模块，对所有场景生效。基础模块不能卸载。
<<< END U009119 >>>
<<< UNIT U009120 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/module.md:119-123 | ctx=`module unload` >>>
  :log="[
    '用户：~module unload dice',
    '机器人：成功卸载模块：dice',
  ]"
/>
<<< END U009120 >>>
<<< UNIT U009121 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/mute.md:7-7 | ctx=mute >>>
此模块用于切换当前场景的禁止发言状态。模块级权限为场景管理员。
<<< END U009121 >>>
<<< UNIT U009122 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/mute.md:13-13 | ctx=`mute` >>>
此命令切换当前场景的禁止发言状态。禁止发言期间，除 `mute` 外的命令和正则都不执行，发往该场景的主动推送也会被阻止。再次执行同一命令即可恢复。
<<< END U009122 >>>
<<< UNIT U009123 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/mute.md:16-22 | ctx=`mute` >>>
  :log="[
    '用户：~mute',
    '机器人：已禁止发言。',
    '用户：~mute',
    '机器人：已解除禁止发言。',
  ]"
/>
<<< END U009123 >>>
<<< UNIT U009124 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/parser_errors.md:8-8 | ctx=parser_errors >>>
此模块用于统一处理命令与正则表达式抛出的异常。各类异常对应的反馈如下：
<<< END U009124 >>>
<<< UNIT U009125 | md-table | packages/akari-bot-core/akaribot/modules/core/docs/parser_errors.md:10-16 | ctx=parser_errors >>>
| 异常 | 反馈 |
| --- | --- |
| `NoReportException` | 回显异常文本，不进入上报流程 |
| `ExternalException` | 回显异常文本与外部错误说明 |
| `AbuseWarning` | 回显提示与拒绝原因，不进入上报流程 |
| `SendMessageFailed` | 触发平台错误提示与限流文案 |
| 其他异常 | 回显错误详情、上报场景与问题反馈地址，并发送错误报告 |
<<< END U009125 >>>
<<< UNIT U009126 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/parser_errors.md:18-18 | ctx=parser_errors >>>
错误详情按平台能力渲染。支持 Markdown 时使用 Markdown 代码块，否则按纯文本解析。启用表情且平台支持图片时，还会附带随机表情。
<<< END U009126 >>>
<<< UNIT U009127 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/parser_errors.md:20-20 | ctx=parser_errors >>>
上报通过 `send_report()` 发送到 `report_targets`，同时写入 SMTP 报告（若启用）。
<<< END U009127 >>>
<<< UNIT U009128 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/parser_errors.md:22-22 | ctx=parser_errors >>>
模块还提供一个带名称的 Hook `format_error_detail`，RPC 的错误报告复用同一套格式化逻辑。
<<< END U009128 >>>
<<< UNIT U009129 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/parser_policies.md:8-8 | ctx=parser_policies >>>
以下为消息入口的内置策略，按入口顺序执行。同一入口内先执行优先级数值小的策略。
<<< END U009129 >>>
<<< UNIT U009130 | md-table | packages/akari-bot-core/akaribot/modules/core/docs/parser_policies.md:10-21 | ctx=parser_policies >>>
| 入口 | 优先级 | 行为 |
| --- | --- | --- |
| `SESSION_READY` | 10 | 丢弃 `ignored_sender`、同场景其他机器人、黑名单用户与被本场景限制用户的消息 |
| `COMMAND_PREPARE` | 5 | 场景冷却，非管理员在 `cooldown_time` 内只收到一次提示 |
| `COMMAND_PREPARE` | 30 | 模块路由，检查权限、平台能力、场景启用状态与自动启用确认 |
| `COMMAND_ROUTE` | 20 | 禁止发言场景只放行 `mute` |
| `COMMAND_BEFORE_EXECUTE` | 10 | 命令级权限校验 |
| `COMMAND_BEFORE_EXECUTE` | 100 | 执行锁被占用时提示“正在运行” |
| `REGEX_ROUTE` | 10 | 跳过正则禁用前缀、禁止发言场景与运行中提醒 |
| `REGEX_PREPARE` | 5 / 15 | 正则权限与冷却 |
| `COMMAND_UNMATCHED` | 100 | 未匹配时提示语法错误或未加载提示 |
| `OUTGOING_BEFORE_SEND` | 10 | 阻止发往禁止发言场景的主动推送 |
<<< END U009130 >>>
<<< UNIT U009131 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/parser_policies.md:23-23 | ctx=parser_policies >>>
场景冷却状态保存在模块的 runtime 中。同版本热重载后，这些状态仍然保留。管理员不受冷却限制。
<<< END U009131 >>>
<<< UNIT U009132 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/parser_routing.md:8-8 | ctx=parser_routing >>>
同一现实场景可能对应多条消息通道。同一条消息经多条通道到达时，此策略只允许一个平台场景认领它。
<<< END U009132 >>>
<<< UNIT U009133 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/parser_routing.md:10-12 | ctx=parser_routing >>>
- `CHANNEL_CLAIM` 上优先级为 1 的 Hook 读取场景的 `channel_id` 映射。
- 优先级为 100 的 Hook 按“union + 通道 + 命令摘要”判定。10 秒内只允许一个平台场景认领，其余通道收到的同一条消息会被丢弃。
- 认领记录 30 秒后过期，进程重启后清空。
<<< END U009133 >>>
<<< UNIT U009134 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:7-7 | ctx=petal >>>
花瓣是跨平台的积分。此模块只在 `enable_petal` 为 `true` 时加载。别名 `petals`、`sign` 分别指向 `petal` 与 `petal sign`。
<<< END U009134 >>>
<<< UNIT U009135 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:13-13 | ctx=`petal` >>>
此命令用于查询花瓣数量。不指定用户时，查询发送者本人。指定用户时要求超级用户权限。目标用户尚未初始化时，先确认再创建。
<<< END U009135 >>>
<<< UNIT U009136 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:16-20 | ctx=`petal` >>>
  :log="[
    '用户：~petal',
    '机器人：当前花瓣数为 42。',
  ]"
/>
<<< END U009136 >>>
<<< UNIT U009137 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:26-26 | ctx=`petal sign` >>>
此命令用于每日签到，签到后获得花瓣。场景可以通过 `setup sign` 关闭签到。签到关闭时返回停用提示，当日已签到则返回已领取提示。
<<< END U009137 >>>
<<< UNIT U009138 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:29-34 | ctx=`petal sign` >>>
  :log="[
    '用户：~petal sign',
    '机器人：签到成功！',
    '获得了 7 片花瓣。',
  ]"
/>
<<< END U009138 >>>
<<< UNIT U009139 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:40-40 | ctx=`petal give` >>>
此命令用于向同一平台的用户转账花瓣，执行前要求确认。目标必须是带平台前缀的完整 ID，不能是发送者本人。花瓣数量小于或等于 0 时返回提示。
<<< END U009139 >>>
<<< UNIT U009140 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:43-49 | ctx=`petal give` >>>
  :log="[
    '用户：~petal give 5 QQ|Group|987654321',
    '机器人：此操作将会将 5 花瓣给予用户 QQ|Group|987654321 ，是否继续？',
    '用户：是',
    '机器人：已将 5 花瓣给予用户 QQ|Group|987654321 ，当前花瓣数为：42。',
  ]"
/>
<<< END U009140 >>>
<<< UNIT U009141 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:55-55 | ctx=`petal modify` >>>
此命令用于增减指定用户的花瓣，负数表示扣除。不指定用户时，修改发送者本人。目标用户尚未初始化时，先确认再创建。
<<< END U009141 >>>
<<< UNIT U009142 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:58-62 | ctx=`petal modify` >>>
  :log="[
    '用户：~petal modify -10',
    '机器人：已修改 -10 花瓣，当前花瓣数为：32。',
  ]"
/>
<<< END U009142 >>>
<<< UNIT U009143 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:68-68 | ctx=`petal clear` >>>
此命令用于把花瓣清零。不指定用户时，处理发送者本人。
<<< END U009143 >>>
<<< UNIT U009144 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:71-75 | ctx=`petal clear` >>>
  :log="[
    '用户：~petal clear',
    '机器人：已清除所有花瓣。',
  ]"
/>
<<< END U009144 >>>
<<< UNIT U009145 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:81-81 | ctx=`petal bud send` >>>
此命令用于发放花瓣红包，执行前要求确认。
<<< END U009145 >>>
<<< UNIT U009146 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:83-85 | ctx=`petal bud send` >>>
- `<petal>` 为总额。
- `<count>` 为份数。
- `<passcode>` 为领取口令。
<<< END U009146 >>>
<<< UNIT U009147 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:87-87 | ctx=`petal bud send` >>>
总额不能小于份数。口令重复时退回已扣除的花瓣。成功时返回红包 ID。
<<< END U009147 >>>
<<< UNIT U009148 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:90-96 | ctx=`petal bud send` >>>
  :log="[
    '用户：~petal bud send 30 3 布丁',
    '机器人：此操作将花费 30 片花瓣，发出可领取 3 次的花苞（口令：布丁）。是否继续？',
    '用户：是',
    '机器人：花苞已发送！共 30 片花瓣，可领取 3 次。',
  ]"
/>
<<< END U009148 >>>
<<< UNIT U009149 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:102-102 | ctx=`petal bud` >>>
此命令用于凭口令领取红包，返回领取结果与获得的花瓣数。
<<< END U009149 >>>
<<< UNIT U009150 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:105-110 | ctx=`petal bud` >>>
  :log="[
    '用户：~petal bud 布丁',
    '机器人：领取成功！',
    '获得了 10 片花瓣。',
  ]"
/>
<<< END U009150 >>>
<<< UNIT U009151 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:116-116 | ctx=`petal bud info` >>>
此命令用于查看红包的发送者、口令、总额、份数与领取记录。
<<< END U009151 >>>
<<< UNIT U009152 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:119-125 | ctx=`petal bud info` >>>
  :log="[
    '用户：~petal bud info K7QX2M9F',
    '机器人：发送者：QQ|Group|123456789',
    '口令：布丁',
    '总量：30 片｜已领取：2/3 次',
  ]"
/>
<<< END U009152 >>>
<<< UNIT U009153 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:131-131 | ctx=`petal bud release` >>>
此命令用于强制释放所有过期花苞，返回释放数量。没有可释放的花苞时返回提示。
<<< END U009153 >>>
<<< UNIT U009154 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:134-138 | ctx=`petal bud release` >>>
  :log="[
    '用户：~petal bud release',
    '机器人：已释放 2 个过期花苞。',
  ]"
/>
<<< END U009154 >>>
<<< UNIT U009155 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:140-140 | ctx=`petal bud release` >>>
配置项包括 `enable_get_petal`、`petal_gained_limit`、`petal_lost_limit`、`petal_sign_min`、`petal_sign_max`、`petal_sign_rate`、`petal_rebate_rate`、`petal_reset_crontab`。
<<< END U009155 >>>
<<< UNIT U009156 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/petal.md:142-142 | ctx=`petal bud release` >>>
定时任务按 `petal_reset_crontab` 结算花瓣，默认值为每月 1 日的 `0 0 1 * *`。转账与红包要求目标用户属于同一平台，避免跨平台刷取。
<<< END U009156 >>>
