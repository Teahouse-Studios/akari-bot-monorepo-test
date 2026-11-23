# 全仓可读文本审核稿 · 第 10 册 / 共 20 册

覆盖 U007036–U007388，11 个文件、353 个单元、35,373 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

改动只写在 `<<< UNIT … >>>` 与 `<<< END … >>>` 之间。UNIT 行含编号与位置，回填按编号对位，这一行不要动。

每个单元正文前有一行 `审阅次数：0`，用来记录这一格被看过几遍，回填时忽略这一行。

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
| `packages/akari-bot-core/akaribot/core/database/models.py` | 90 | U007036–U007125 | 5,404 |
| `packages/akari-bot-core/akaribot/core/docs/adapter-development.md` | 27 | U007126–U007152 | 3,302 |
| `packages/akari-bot-core/akaribot/core/docs/api-reference.md` | 3 | U007153–U007155 | 155 |
| `packages/akari-bot-core/akaribot/core/docs/architecture.md` | 36 | U007156–U007191 | 3,462 |
| `packages/akari-bot-core/akaribot/core/docs/config.md` | 37 | U007192–U007228 | 3,223 |
| `packages/akari-bot-core/akaribot/core/docs/database.md` | 30 | U007229–U007258 | 2,843 |
| `packages/akari-bot-core/akaribot/core/docs/development-workflow.md` | 26 | U007259–U007284 | 2,614 |
| `packages/akari-bot-core/akaribot/core/docs/faq.md` | 35 | U007285–U007319 | 2,573 |
| `packages/akari-bot-core/akaribot/core/docs/i18n.md` | 15 | U007320–U007334 | 1,476 |
| `packages/akari-bot-core/akaribot/core/docs/index.md` | 16 | U007335–U007350 | 2,214 |
| `packages/akari-bot-core/akaribot/core/docs/message-api.md` | 38 | U007351–U007388 | 8,107 |

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
<<< UNIT U007036 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:29-30 >>>
审阅次数：11
# 新建 union ID 的域前缀。升级与转换脚本会将历史数据的平台 ID 直接沿用为 union ID，
# 附加前缀后，新生成的 ID 不会与平台原生 ID 混淆，且可明确区分账号组与场景组。
<<< END U007036 >>>
<<< UNIT U007037 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:36-37 >>>
审阅次数：11
# Union 的绑定、合并、删除与更新属于同一 mutation 域，共用单一进程内互斥锁。
# MySQL 路径仍将在事务内锁定核心行，兼顾 Web 与 Server 分属不同进程的场景。
<<< END U007037 >>>
<<< UNIT U007038 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:195-196 >>>
审阅次数：11
# 删除与重建之间若中断，绑定数据将全部丢失，因此必须纳入同一个事务执行。
# 模块表可能关联在 local 连接上，事务必须与表所在的连接一致，不可直接使用 default 连接。
<<< END U007038 >>>
<<< UNIT U007039 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:222-223 >>>
审阅次数：11
# 调用方位于 Union mutation 事务中。锁定权限列表所属的 Target 行，避免 Web 与 Server
# 分属不同进程时，因并发修改 Union 引用与追加管理员而相互覆盖完整的 JSON 列表。
<<< END U007039 >>>
<<< UNIT U007040 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:263-264 >>>
审阅次数：11
# iter_union_models 已按 union_scope 过滤，此处获取的数据表必定属于相同作用域，
# 避免将场景 ID 误作为用户 ID 创建记录。
<<< END U007040 >>>
<<< UNIT U007041 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:284-284 >>>
审阅次数：11
# 子类中作为主键的平台 ID 列名称，供按域泛化的查询与补充创建逻辑使用。
<<< END U007041 >>>
<<< UNIT U007042 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:381-381 >>>
审阅次数：11
# 所属 union 作用域（``sender`` / ``target``）。
<<< END U007042 >>>
<<< UNIT U007043 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:383-383 >>>
审阅次数：11
# 配套的 ID 映射表。
<<< END U007043 >>>
<<< UNIT U007044 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:386-387 >>>
审阅次数：11
# 由 resolve_union() 附加的映射行，并非数据库持久化字段。
# 若未通过解析直接执行查询（如 all() / filter()），获取的实例中该字段值为 None。
<<< END U007044 >>>
<<< UNIT U007045 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:391-392 >>>
审阅次数：11
# 封禁状态仅记录于此处。union 下的全部平台 ID 共享此行，因而封禁设置直接对组内所有平台 ID 生效，
# 映射行无需重复保存标记，避免产生组状态与单个 ID 状态不一致的问题。
<<< END U007045 >>>
<<< UNIT U007046 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:421-421 >>>
审阅次数：11
# 仅当映射路径缺失或损坏时才进入 mutation 域。常规消息解析仍保持无锁查询。
<<< END U007046 >>>
<<< UNIT U007047 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:425-425 >>>
审阅次数：11
# 自动兼容处理，允许存在 union_id 与平台 ID 相同但缺少映射行的历史数据。
<<< END U007047 >>>
<<< UNIT U007048 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:451-451 >>>
审阅次数：11
# 从平台 ID 字符串或会话对象解析 union 信息，供按会话获取记录的入口复用。
<<< END U007048 >>>
<<< UNIT U007049 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:635-636 >>>
审阅次数：11
# 创建新组、重新关联映射和继承场景限制名单必须以原子操作完成。否则最后一步执行失败会导致残留
# 孤立的新 union，并使账号脱离原组后未能继承全部限制状态。
<<< END U007049 >>>
<<< UNIT U007050 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:650-651 >>>
审阅次数：11
# 首先创建新组，随后重新关联映射行，全程避免出现“账号缺少映射行”的中间状态。
# union_id 并非主键，可通过单条 UPDATE 语句完成重新关联。
<<< END U007050 >>>
<<< UNIT U007051 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:676-677 >>>
审阅次数：11
# 合并操作同时涉及核心表、平台映射、权限引用与若干模块表的改写。任何步骤失败均必须整体回滚，
# 避免出现新旧 union 并存或仅部分模块数据完成迁移的不可恢复状态。
<<< END U007051 >>>
<<< UNIT U007052 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:704-704 >>>
审阅次数：11
# 首先依据冲突解决策略将两侧模块数据合并至一处，随后整体重新关联至新组。新组初始为空，第二阶段不再产生冲突。
<<< END U007052 >>>
<<< UNIT U007053 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:845-846 >>>
审阅次数：11
# Union 事务统一先锁定核心行，再锁定映射行。逆序加锁将在 MySQL 环境下导致循环死锁。
# 锁定核心行后必须重新读取映射并验证其未被重新关联。
<<< END U007053 >>>
<<< UNIT U007054 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:934-935 >>>
审阅次数：11
# MySQL 环境下锁定 union 数据行，使不同 Server 进程无法同时依据相同最大通道号分配通道编号。
# SQLite 会忽略行锁语义，由外层 asyncio.Lock 保证单 Server 进程内的顺序。
<<< END U007054 >>>
<<< UNIT U007055 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:967-967 >>>
审阅次数：11
# 新组创建、平台映射重新关联与互认记录迁移属于同一次解绑事务。任何步骤失败均必须完整回滚，严禁数据库处于部分迁移状态。
<<< END U007055 >>>
<<< UNIT U007056 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:982-982 >>>
审阅次数：11
# 封禁状态随场景一并转移，避免通过解绑规避限制。
<<< END U007056 >>>
<<< UNIT U007057 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:989-990 >>>
审阅次数：11
# 首先创建新组，随后重新关联映射行，全程避免出现“场景缺少映射行”的中间状态。
# 新组初始仅包含该场景，其消息通道编号重置为 1。
<<< END U007057 >>>
<<< UNIT U007058 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1005-1006 >>>
审阅次数：11
# 拆分出的场景与原组内的机器人不再对应同一现实场景，互认记录必须一并清除。
# 新组的 target_data 初始为空，仅需清理保留的一侧。调用内部方法避免重复获取全局锁。
<<< END U007058 >>>
<<< UNIT U007059 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1037-1038 >>>
审阅次数：11
# bots_id 为二级嵌套结构，若随 target_data 执行浅合并，将导致 other 一侧的互认记录被整体覆盖，
# 因此必须单独计算并集。
<<< END U007059 >>>
<<< UNIT U007060 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1059-1059 >>>
审阅次数：11
# 首先依据冲突解决策略将两侧模块数据合并至一处，随后整体重新关联至新组。新组初始为空，第二阶段不再产生冲突。
<<< END U007060 >>>
<<< UNIT U007061 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1070-1071 >>>
审阅次数：11
# 自身一侧通道编号保持不变，并入方执行整体平移，严禁逐条分配新编号。
# 通道平移必须依据原通道编号建立映射，确保并入方内部处于同一通道的场景在平移后继续归属于同一通道。
<<< END U007061 >>>
<<< UNIT U007062 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1308-1308 >>>
审阅次数：11
# 统计命令按时间区间频繁聚合，缺少索引时每次均会执行全表扫描。
<<< END U007062 >>>
<<< UNIT U007063 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1529-1530 >>>
审阅次数：11
# 每个进程每 100 毫秒依据该两列轮询一次，缺少索引时开销将随表内行数线性增长。
# status / timestamp 索引用于低成本回收调用方异常退出后遗留的终态记录。
<<< END U007063 >>>
<<< UNIT U007064 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1577-1578 >>>
审阅次数：11
# 定时清理仅删除已进入终态且超过保留期的任务。pending 与 processing 状态最长可执行两小时，
# 若沿用无条件删除，对应任务将在等待方与执行方超时机制生效前提前被清理。
<<< END U007064 >>>
<<< UNIT U007065 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1581-1582 >>>
审阅次数：11
# 超过全局执行上限的活跃任务已无法正常完成，无需响应的任务直接删除。
# 等待型任务先标记为 timeout 供轮询机制获取终态。终态删除必须在本步骤之前完成。
<<< END U007065 >>>
<<< UNIT U007066 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1601-1602 >>>
审阅次数：11
# 此处不附加 ORDER BY 排序，复用既有 (target_peer, status) 索引可在匹配至 limit 阈值后提前终止扫描。
# JobQueue 本身不承诺严格 FIFO 语义，以此避免在获取候选批次时对全量积压记录生成临时排序表。
<<< END U007066 >>>
<<< UNIT U007067 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:43-43 | ctx=union_mutation >>>
审阅次数：11
串行执行一段 Union 状态变更。调用方不得在内部再次进入本上下文。
<<< END U007067 >>>
<<< UNIT U007068 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:49-49 | ctx=UnionDeleteBlocked >>>
审阅次数：11
Union 仍被模块记录引用，必须先解除外部状态才能删除。
<<< END U007068 >>>
<<< UNIT U007069 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:71-71 | ctx=get_table_name >>>
审阅次数：11
获取模型对应的数据表名称。
<<< END U007069 >>>
<<< UNIT U007070 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:77-77 | ctx=get_union_module_name >>>
审阅次数：11
获取模块表所属的模块名称，供面向用户的提示使用。无法识别时回退为数据表名称。
<<< END U007070 >>>
<<< UNIT U007071 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:138-138 | ctx=migrate_union_references >>>
审阅次数：11
迁移显式声明协议的模块 Union 引用。
<<< END U007071 >>>
<<< UNIT U007072 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:165-171 | ctx=collect_union_conflicts >>>
审阅次数：11
:param from_union: 来源 union ID。
:param to_union: 目标 union ID。
:param scope: 限定 union 作用域。

列出两个 union 在模块表上相互冲突（双方均存在数据）的模型。
<<< END U007072 >>>
<<< UNIT U007073 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:259-259 | ctx=backfill_union_binds >>>
审阅次数：11
为缺少映射行的 union 补充创建 ID 映射。
<<< END U007073 >>>
<<< UNIT U007074 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:295-295 | ctx=UnionBind.list_ids >>>
审阅次数：11
列出绑定至给定 union ID 的平台账号。
<<< END U007074 >>>
<<< UNIT U007075 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:300-304 | ctx=SenderUnionBind >>>
审阅次数：11
用户 ID 与 union 的映射关系。

:param sender_id: 用户 ID（平台账号）。
<<< END U007075 >>>
<<< UNIT U007076 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:315-321 | ctx=TargetUnionBind >>>
审阅次数：11
场景 ID 与 union 的映射关系。

:param target_id: 场景 ID。
:param channel_id: 所属消息通道编号，同组内相同通道号的场景被视为同一现实场景。
:param push_priority: 主动推送优先级，数值越大越优先。
<<< END U007076 >>>
<<< UNIT U007077 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:343-347 | ctx=TargetUnionBind.list_channels >>>
审阅次数：11
获取该 union 下“平台场景 ID → 消息通道编号”的映射。

:param union_id: 场景 union ID。
<<< END U007077 >>>
<<< UNIT U007078 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:408-408 | ctx=UnionInfo.resolve_union >>>
审阅次数：11
按平台账号查找 union 记录，不存在时按需创建。
<<< END U007078 >>>
<<< UNIT U007079 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:438-438 | ctx=UnionInfo.list_bound_ids >>>
审阅次数：11
列出该 union 记录绑定的平台账号。
<<< END U007079 >>>
<<< UNIT U007080 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:462-462 | ctx=UnionInfo.edit_attr >>>
审阅次数：11
修改 union 记录中除主键外的指定字段值。
<<< END U007080 >>>
<<< UNIT U007081 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:473-473 | ctx=UnionInfo.delete_union >>>
审阅次数：11
删除 union 记录及其关联的映射和会话数据。
<<< END U007081 >>>
<<< UNIT U007082 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:527-530 | ctx=SenderUnionInfo.get_by_sender_id >>>
审阅次数：11
获取平台账号所属的 union 记录行，为 :meth:`UnionInfo.resolve_union` 的会话便捷封装。方法支持传入 MessageSession 或 FetchedMessageSession 并自动提取 ``sender_id``。
<<< END U007082 >>>
<<< UNIT U007083 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:534-539 | ctx=SenderUnionInfo.switch_identity >>>
审阅次数：11
修改用户身份。

:param trust: 是否为白名单模式，若 False 则为黑名单模式。
:param enable: 是否授予身份。若为 False 则撤销身份。
<<< END U007083 >>>
<<< UNIT U007084 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:554-558 | ctx=SenderUnionInfo.warn_user >>>
审阅次数：11
警告用户。

:param amount: 警告增加次数。
<<< END U007084 >>>
<<< UNIT U007085 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:568-572 | ctx=SenderUnionInfo.modify_petal >>>
审阅次数：11
修改用户花瓣数量。

:param amount: 增加或扣除的花瓣数量。
<<< END U007085 >>>
<<< UNIT U007086 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:582-582 | ctx=SenderUnionInfo.clear_petal >>>
审阅次数：11
清空用户的花瓣余额。
<<< END U007086 >>>
<<< UNIT U007087 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:586-591 | ctx=SenderUnionInfo.edit_sender_data >>>
审阅次数：11
设置用户数据。

:param key: 键名称。
:param value: 值，若留空则删除该键值对。
<<< END U007087 >>>
<<< UNIT U007088 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:611-616 | ctx=SenderUnionInfo.bind_id >>>
审阅次数：11
将平台账号绑定至该 union。

:param sender_id: 平台账号 ID。
:return: 是否绑定成功，若该账号已绑定至其他 union 则返回 False。
<<< END U007088 >>>
<<< UNIT U007089 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:761-764 | ctx=TargetUnionInfo.get_by_target_id >>>
审阅次数：11
获取平台场景所属的 union 记录行，为 :meth:`UnionInfo.resolve_union` 的会话便捷封装。方法支持传入 MessageSession 或 FetchedMessageSession 并自动提取 ``target_id``。
<<< END U007089 >>>
<<< UNIT U007090 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:768-772 | ctx=TargetUnionInfo.list_peer_bots >>>
审阅次数：11
获取指定平台场景视角下、同一现实场景中其他机器人的账号。

:param target_id: 观察方的平台场景 ID。
<<< END U007090 >>>
<<< UNIT U007091 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:792-796 | ctx=TargetUnionInfo.link_peer_bots >>>
审阅次数：11
记录机器人互认关系。

:param links: ``{观察方场景 ID: {对端场景 ID: 对端机器人在观察方平台的账号}}``。
<<< END U007091 >>>
<<< UNIT U007092 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:926-931 | ctx=TargetUnionInfo.bind_id >>>
审阅次数：11
将平台场景绑定至该 union。

:param target_id: 平台场景 ID。
:return: 是否绑定成功，若该场景已绑定至其他 union 则返回 False。
<<< END U007092 >>>
<<< UNIT U007093 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:960-965 | ctx=TargetUnionInfo.unbind_id >>>
审阅次数：11
将指定平台场景自该 union 中拆分，历史数据保留于原 union，该场景重置为空白状态。

:param target_id: 平台场景 ID。
:return: 拆分后该场景所属的新 union，若无法解绑则为 None。
<<< END U007093 >>>
<<< UNIT U007094 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1092-1097 | ctx=TargetUnionInfo.config_module >>>
审阅次数：11
设置场景内可用模块。

:param module_name: 指定的模块名称。
:param enable: 是否启用该模块。若为 False 则禁用。
<<< END U007094 >>>
<<< UNIT U007095 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1118-1122 | ctx=TargetUnionInfo.switch_mute >>>
审阅次数：11
切换场景内机器人禁止发言与禁用状态。

:return: 机器人是否被禁用。
<<< END U007095 >>>
<<< UNIT U007096 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1136-1141 | ctx=TargetUnionInfo.edit_target_data >>>
审阅次数：11
设置场景数据。

:param key: 键名称。
:param value: 值，若留空则删除该键值对。
<<< END U007096 >>>
<<< UNIT U007097 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1161-1166 | ctx=TargetUnionInfo.config_custom_admin >>>
审阅次数：11
设置场景内管理员。

:param sender_union_id: 指定的用户 union ID。
:param enable: 是否授予场景管理员权限。若为 False 则撤销权限。
<<< END U007097 >>>
<<< UNIT U007098 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1193-1198 | ctx=TargetUnionInfo.config_banned_user >>>
审阅次数：11
设置场景内被限制用户。

:param sender_union_id: 指定的用户 union ID。
:param enable: 是否限制该用户在场景内使用机器人。若为 False 则解除限制。
<<< END U007098 >>>
<<< UNIT U007099 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1228-1234 | ctx=TargetUnionInfo.get_target_list_by_module >>>
审阅次数：11
获取已启用该模块的全部场景列表。

:param module_name: 指定的模块名称。
:param id_prefix: 指定的 ID 前缀，按 union 下绑定的平台场景 ID 匹配。
:return: 符合要求的场景 union 列表。
<<< END U007099 >>>
<<< UNIT U007100 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1272-1277 | ctx=StoredData >>>
审阅次数：11
持久化数据存储。

:param stored_key: 存储键名称。
:param value: 存储值。
<<< END U007100 >>>
<<< UNIT U007101 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1287-1298 | ctx=AnalyticsData >>>
审阅次数：11
统计数据。

:param module_name: 模块名称。
:param module_type: 模块类型。
:param target_id: 场景 ID。
:param sender_id: 用户 ID。
:param target_union_id: 场景所属 union ID。
:param sender_union_id: 用户所属 union ID。
:param command: 命令名称。
:param timestamp: 时间戳。
<<< END U007101 >>>
<<< UNIT U007102 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1316-1316 | ctx=AnalyticsData.get_data_by_times >>>
审阅次数：11
按时间范围获取统计数据。
<<< END U007102 >>>
<<< UNIT U007103 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1324-1324 | ctx=AnalyticsData.get_values_by_times >>>
审阅次数：11
按时间范围获取数值。
<<< END U007103 >>>
<<< UNIT U007104 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1332-1332 | ctx=AnalyticsData.get_count_by_times >>>
审阅次数：11
按时间范围统计数量。
<<< END U007104 >>>
<<< UNIT U007105 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1340-1340 | ctx=AnalyticsData.get_modules_count >>>
审阅次数：11
获取按模块统计的数量。
<<< END U007105 >>>
<<< UNIT U007106 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1363-1368 | ctx=ModuleStatus >>>
审阅次数：11
模块状态。

:param module_name: 模块名称。
:param load: 是否已加载。
<<< END U007106 >>>
<<< UNIT U007107 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1378-1378 | ctx=ModuleStatus.init_modules >>>
审阅次数：11
初始化模块状态记录。
<<< END U007107 >>>
<<< UNIT U007108 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1401-1401 | ctx=ModuleStatus.set_module_loaded >>>
审阅次数：11
设置模块的加载状态。
<<< END U007108 >>>
<<< UNIT U007109 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1411-1411 | ctx=ModuleStatus.get_all_modules >>>
审阅次数：11
获取全部模块状态。
<<< END U007109 >>>
<<< UNIT U007110 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1416-1416 | ctx=ModuleStatus.get_loaded_modules >>>
审阅次数：11
获取已加载的模块列表。
<<< END U007110 >>>
<<< UNIT U007111 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1421-1421 | ctx=ModuleStatus.get_unloaded_modules >>>
审阅次数：11
获取未加载的模块列表。
<<< END U007111 >>>
<<< UNIT U007112 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1426-1430 | ctx=DBVersion >>>
审阅次数：11
数据库版本。

:param version: 数据库版本号。
<<< END U007112 >>>
<<< UNIT U007113 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1439-1449 | ctx=UnfriendlyActionRecords >>>
审阅次数：11
不友好行为记录。

:param target_id: 场景 ID。
:param sender_id: 用户 ID。
:param target_union_id: 场景所属 union ID。
:param sender_union_id: 用户所属 union ID。
:param action: 行为类型。
:param detail: 行为详情。
:param timestamp: 时间戳。
<<< END U007113 >>>
<<< UNIT U007114 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1499-1510 | ctx=JobQueuesTable >>>
审阅次数：11
任务队列表。

:param task_id: 任务 ID。
:param target_peer: 目标节点进程实例或服务。
:param expects_response: 调用方是否等待终态结果。
:param action: 操作类型。
:param args: 参数。
:param status: 任务状态。
:param result: 任务结果。
:param timestamp: 时间戳。
<<< END U007114 >>>
<<< UNIT U007115 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1535-1535 | ctx=JobQueuesTable.add_task >>>
审阅次数：11
向任务队列表添加任务。
<<< END U007115 >>>
<<< UNIT U007116 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1541-1541 | ctx=JobQueuesTable.set_val >>>
审阅次数：11
更新任务的执行结果与关联属性。
<<< END U007116 >>>
<<< UNIT U007117 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1548-1548 | ctx=JobQueuesTable.set_status >>>
审阅次数：11
设置任务状态。
<<< END U007117 >>>
<<< UNIT U007118 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1554-1554 | ctx=JobQueuesTable.claim >>>
审阅次数：11
以原子操作将 pending 状态的任务认领为 processing 状态。
<<< END U007118 >>>
<<< UNIT U007119 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1568-1568 | ctx=JobQueuesTable.clear_task >>>
审阅次数：11
清理或删除任务记录。
<<< END U007119 >>>
<<< UNIT U007120 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1591-1591 | ctx=JobQueuesTable.get_first >>>
审阅次数：11
获取队列表中的首个任务。
<<< END U007120 >>>
<<< UNIT U007121 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1598-1598 | ctx=JobQueuesTable.get_all >>>
审阅次数：11
获取全部任务记录。
<<< END U007121 >>>
<<< UNIT U007122 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1610-1610 | ctx=JobQueuePeersTable >>>
审阅次数：11
JobQueue 进程注册表。租约是在线状态的唯一来源。
<<< END U007122 >>>
<<< UNIT U007123 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1633-1640 | ctx=MaliciousLoginRecords >>>
审阅次数：11
恶意登录行为记录。

:param id: 记录 ID。
:param ip_address: IP 地址。
:param blocked_until: 封禁截止时间。
:param created_date: 创建日期。
<<< END U007123 >>>
<<< UNIT U007124 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1652-1652 | ctx=MaliciousLoginRecords.check_blocked >>>
审阅次数：11
检查登录来源是否已被封禁拦截。
<<< END U007124 >>>
<<< UNIT U007125 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1657-1668 | ctx=SchemaMigration >>>
审阅次数：11
已应用的数据库迁移记录。

每个成员包的每条 revision 在此各记录一行，取代全局唯一的数据库版本号。MySQL 的 DDL 会自动
提交，无法将“执行 DDL”与“写入版本记录”纳入同一事务，因此判断某条 revision 是否已应用
仅查询本表，迁移必须自行保证可重复执行。

:param package: 包名称，``core`` 或其他包名称。
:param revision: revision 标识符。
:param applied_at: 应用时间。
:param checksum: 迁移文件源码的 SHA-256 哈希值，用于发现已应用的迁移被改写。
<<< END U007125 >>>
<<< UNIT U007126 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:1-1 | ctx=适配器开发 >>>
审阅次数：11
# 适配器开发
<<< END U007126 >>>
<<< UNIT U007127 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:3-3 | ctx=适配器开发 >>>
审阅次数：11
本文介绍适配器的包结构、能力声明与平台入口。
<<< END U007127 >>>
<<< UNIT U007128 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:5-5 | ctx=适配器开发 >>>
审阅次数：11
适配器负责连接第三方平台与 core。它接收平台消息，将其转换为 core 的会话对象后提交 Server 处理，同时将 core 发出的消息和操作交由平台 SDK 执行。
<<< END U007128 >>>
<<< UNIT U007129 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:7-7 | ctx=适配器开发 >>>
审阅次数：11
适配器在 `pyproject.toml` 的 `akaribot.adapters` 入口点中声明平台键与包路径的对应关系，目录名称采用平台键命名。
<<< END U007129 >>>
<<< UNIT U007130 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:9-9 | ctx=包结构 >>>
审阅次数：11
## 包结构
<<< END U007130 >>>
<<< UNIT U007131 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:28-28 | ctx=包结构 >>>
审阅次数：11
`manifest.toml` 通过 `config_table = "bot_telegram"` 指向 `config.py` 中的配置表。`credential_fields = ["telegram_token"]` 列出登录字段。启动实例前，守护进程会读取该两项配置，并检查同一平台的多个实例是否使用了相同的账号或令牌。
<<< END U007131 >>>
<<< UNIT U007132 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:45-45 | ctx=info.py >>>
审阅次数：11
`platform_name` 是平台展示名称，`client_name` 由它生成，多实例部署时附带实例后缀（如 `Telegram-alt`）。两个前缀列表传入 `client_init()`，用于校验会话 ID 并建立平台路由映射。
<<< END U007132 >>>
<<< UNIT U007133 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:47-47 | ctx=info.py >>>
审阅次数：11
守护进程在导入适配器之前设置 `instance_id`。当 `bot_<平台>.toml` 中的 `enable` 为 `true` 时，守护进程启动该实例。
<<< END U007133 >>>
<<< UNIT U007134 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:49-49 | ctx=多实例 >>>
审阅次数：11
## 多实例
<<< END U007134 >>>
<<< UNIT U007135 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:51-51 | ctx=多实例 >>>
审阅次数：11
同一适配器可以启动多个实例。实例 ID 匹配 `[a-z0-9_]{1,24}`，配置表名称为 `bot_<平台>-<实例ID>`，例如 `bot_telegram-alt`。
<<< END U007135 >>>
<<< UNIT U007136 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:53-53 | ctx=多实例 >>>
审阅次数：11
当指定了实例 ID 时，`Info.resolve_client_name(platform_name)` 返回 `平台-实例ID`（例如 `Telegram-alt`）。`platform_name` 本身保持不变。
<<< END U007136 >>>
<<< UNIT U007137 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:55-55 | ctx=多实例 >>>
审阅次数：11
实例配置表控制对应实例的启用状态，平台基础配置表保存该平台的默认配置项。
<<< END U007137 >>>
<<< UNIT U007138 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:57-57 | ctx=多实例 >>>
审阅次数：11
启动实例前，守护进程会读取 `manifest.toml` 的 `credential_fields`，并检查同一平台其他实例的登录信息和监听端口。
<<< END U007138 >>>
<<< UNIT U007139 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:59-59 | ctx=多实例 >>>
审阅次数：11
若同一平台已存在相同的登录信息或监听端口，守护进程将输出冲突提示并拒绝启动该实例。
<<< END U007139 >>>
<<< UNIT U007140 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:61-61 | ctx=能力声明 >>>
审阅次数：11
## 能力声明
<<< END U007140 >>>
<<< UNIT U007141 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:63-63 | ctx=能力声明 >>>
审阅次数：11
在 `features.py` 中创建 `Features` 实例，`ContextManager` 通过类属性引用该实例：
<<< END U007141 >>>
<<< UNIT U007142 | md-table | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:71-76 | ctx=能力声明 >>>
审阅次数：11
| 分组 | 字段 |
| --- | --- |
| 媒体与格式 | `support_image`、`support_audio`、`support_video`、`support_markdown`、`support_markdown_extension`、`support_embed` |
| 交互 | `support_mention`、`support_reaction`、`support_quote`、`support_typing`、`support_wait`、`support_action_text`、`support_button` |
| 管理 | `support_delete`、`support_manage`、`support_permission_group` |
| 消息范围与开关 | `read_all_messages`、`support_rss`、`support_handle_message_nodes`、`require_enable_modules`、`require_check_dirty_words` |
<<< END U007142 >>>
<<< UNIT U007143 | md-list | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:78-83 | ctx=能力声明 >>>
审阅次数：11
- `client_init()` 注册节点时，将上述能力标志写入 `capabilities`。
- `Module.unsupported_reason()` 依据 `read_all_messages` 和 `support_rss` 标志，判断正则、事件与 RSS 模块在当前会话中是否可用。
- `check_bot_state()` 返回 `BotState`。
- `can_*` 字段记录机器人是否具备执行对应操作的能力，`permissions` 保存平台返回的原生权限。
- 检查结果写入 `SessionInfo`。
- `Module.unsupported_bot_permissions()` 读取该检查结果，验证模块所需的权限。若机器人缺少模块所需权限，该模块将不会启用。
<<< END U007143 >>>
<<< UNIT U007144 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:85-85 | ctx=平台入口 >>>
审阅次数：11
## 平台入口
<<< END U007144 >>>
<<< UNIT U007145 | md-list | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:104-106 | ctx=平台入口 >>>
审阅次数：11
- `Bot.register_bot()` 设置 `PrivateData` 目录与 `Info.client_name`。`register_context_manager()` 返回 `ctx_slot`，构造 `SessionInfo` 时必须将 `ctx_slot` 一并传入。指定 `fetch_session=True` 的管理器用于主动获取会话。
- 接收到消息时构造 `SessionInfo`（包含场景、发送者、`message_id`、`reply_id`、`messages`、`ctx_slot`、`bot_id`），随后调用 `Bot.process_message(session, ctx)`。平台事件通过 `EventInfo.assign(...)` 与 `Bot.process_event()` 投递。
- `client_init()` 初始化数据库连接（可选 `load_module_db=True`）、连接语言快照并注册节点。`client_cleanup()` 取消轮询、释放上下文并关闭连接。
<<< END U007145 >>>
<<< UNIT U007146 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:110-110 | ctx=ContextManager >>>
审阅次数：11
`ContextManager` 以类属性保存 `session_id` 到平台上下文的映射：
<<< END U007146 >>>
<<< UNIT U007147 | md-list | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:112-114 | ctx=ContextManager >>>
审阅次数：11
- `add_context()` 与 `del_context()` 用于添加和移除上下文。
- `activate_context()` 与 `deactivate_context()` 标记入站消息的处理区间，在该区间内不释放上下文。
- `hold_context()` 与 `release_context()` 用于跨消息保持上下文，支持多层嵌套。
<<< END U007147 >>>
<<< UNIT U007148 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:116-116 | ctx=ContextManager >>>
审阅次数：11
必须实现的抽象方法：
<<< END U007148 >>>
<<< UNIT U007149 | md-table | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:118-124 | ctx=ContextManager >>>
审阅次数：11
| 方法 | 用途 |
| --- | --- |
| `check_native_permission()`、`check_bot_state()` | 平台原生管理员与机器人权限快照 |
| `send_message()`、`send_private_msg()`、`derive_private_session()` | 发送、私聊与创建私聊会话 |
| `delete_message()`、`restrict_member()`、`unrestrict_member()`、`kick_member()` | 删除、禁言、解除与移除 |
| `ban_member()`、`unban_member()`、`grant_permission_group()`、`revoke_permission_group()` | 封禁与权限组 |
| `add_reaction()`、`remove_reaction()`、`error_signal()`、`start_typing()`、`end_typing()` | 表情、错误提示与输入状态 |
<<< END U007149 >>>
<<< UNIT U007150 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:126-126 | ctx=ContextManager >>>
审阅次数：11
上述方法由 `PlatformAPI` 的 `context_method()` 自动绑定。Server 执行跨进程调用时，依据 `SessionInfo` 选择对应的上下文管理器。平台扩展接口由 `PlatformAPI` 声明，并由具体适配器绑定实现。
<<< END U007150 >>>
<<< UNIT U007151 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:128-128 | ctx=配置与本地化 >>>
审阅次数：11
## 配置与本地化
<<< END U007151 >>>
<<< UNIT U007152 | md-list | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:130-133 | ctx=配置与本地化 >>>
审阅次数：11
- 适配器配置通过 `@on_bot_config("<平台>")` 声明，表名称为 `bot_<平台>`。
- 密钥写入 `[bot_<平台>_secret]`。
- 字段配置注释键名称为 `config.comments.bot_<平台>.<字段名>`。密钥表的配置注释需附带 `_secret` 后缀。
- 面向用户的文案仅在适配器包的 `locales/zh_cn.json` 中创建，具体参见[配置](config.md)与[本地化](i18n.md)。
<<< END U007152 >>>
<<< UNIT U007153 | md-heading | packages/akari-bot-core/akaribot/core/docs/api-reference.md:8-8 | ctx=API 导出索引 >>>
审阅次数：11
# API 导出索引
<<< END U007153 >>>
<<< UNIT U007154 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/api-reference.md:10-10 | ctx=API 导出索引 >>>
审阅次数：11
本页按模块列出 `akaribot.core.api` 与 `akaribot.core.api.adapters` 的全部公开导出。类的方法、函数签名、参数类型、默认值和说明由构建过程读取源码生成，不在此页面中手动编写。
<<< END U007154 >>>
<<< UNIT U007155 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/api-reference.md:12-12 | ctx=API 导出索引 >>>
审阅次数：11
若某个参数在 docstring 中未写明用途，清单仅显示其名称与类型。
<<< END U007155 >>>
<<< UNIT U007156 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:1-1 | ctx=架构 >>>
审阅次数：11
# 架构
<<< END U007156 >>>
<<< UNIT U007157 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:3-3 | ctx=架构 >>>
审阅次数：11
本文介绍 AkariBot 实例的内部结构。
<<< END U007157 >>>
<<< UNIT U007158 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:5-5 | ctx=介绍 >>>
审阅次数：11
## 介绍
<<< END U007158 >>>
<<< UNIT U007159 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:7-7 | ctx=介绍 >>>
审阅次数：11
AkariBot 采用模块化多包架构。core 提供运行时环境与基础公共设施，内置模块、外部模块及平台适配器均作为独立成员包维护。
<<< END U007159 >>>
<<< UNIT U007160 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:9-9 | ctx=介绍 >>>
审阅次数：11
实例启动时，守护进程负责启动并监控子进程。各子进程分别承担配置初始化、平台连接、消息处理与计划任务调度。
<<< END U007160 >>>
<<< UNIT U007161 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:11-11 | ctx=代码结构 >>>
审阅次数：11
## 代码结构
<<< END U007161 >>>
<<< UNIT U007162 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:24-24 | ctx=代码结构 >>>
审阅次数：11
补充说明：
<<< END U007162 >>>
<<< UNIT U007163 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:26-28 | ctx=代码结构 >>>
审阅次数：11
- `akaribot`、`akaribot.modules`、`akaribot.adapters`、`akaribot.assets` 是 PEP 420 命名空间目录，不带 `__init__.py`。查找包时以 `pyproject.toml` 中声明的入口为准，仅在入口缺失时才扫描目录。
- 执行 `akaribot <子命令>` 时，命令行工具（CLI）通过子进程调用 `python -m akaribot.core.entrypoints.{run,registry,config,db,peers,modules,rpc}`。
- 仓库根目录保留兼容导入入口。`bot.py`、`tester.py` 通过 `sys.modules` 把原有模块名称映射至新实现。`core/database/update.py` 仅负责将历史版本遗留的升级操作交给当前实现处理。
<<< END U007163 >>>
<<< UNIT U007164 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:30-30 | ctx=进程拓扑 >>>
审阅次数：11
## 进程拓扑
<<< END U007164 >>>
<<< UNIT U007165 | md-table | packages/akari-bot-core/akaribot/core/docs/architecture.md:32-38 | ctx=进程拓扑 >>>
审阅次数：11
| 进程 | 启动方式 | 职责 |
| --- | --- | --- |
| BotDaemon | `python -m akaribot.core.entrypoints.run` | 检查同一实例是否已经启动，执行 pre-init，启动并监控子进程 |
| pre-init | 守护进程以 `spawn`（Windows、macOS）或 `forkserver` 启动 | 补充缺失的配置项，创建数据表，执行数据库迁移 |
| 平台进程 | 每个适配器实例对应一个进程，进程名称为 `client_name` | 维护平台 SDK 连接，保存消息上下文和按钮状态 |
| Server | 进程名称为 `server` | 解析消息，执行模块，运行计划任务 |
| jobqueue-hub | 进程名称为 `jobqueue-hub`，仅用于内置 WebSocket 后端 | 维护节点连接，选择接收任务的节点，传递控制信号 |
<<< END U007165 >>>
<<< UNIT U007166 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:40-40 | ctx=进程拓扑 >>>
审阅次数：11
在启动任何子进程前，守护进程均会设置环境变量 `AKARI_CONFIG_READONLY=1`。此后所有子进程仅能读取配置。仅 pre-init 进程具备配置写入权限，并在执行写入前清除该标记。
<<< END U007166 >>>
<<< UNIT U007167 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:42-42 | ctx=进程拓扑 >>>
审阅次数：11
`<实例根目录>/.bot.lock` 用于防止同一实例重复启动。若尝试再次启动同一实例，新进程将以退出码 1 退出。
<<< END U007167 >>>
<<< UNIT U007168 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:44-44 | ctx=启动顺序 >>>
审阅次数：11
## 启动顺序
<<< END U007168 >>>
<<< UNIT U007169 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:46-50 | ctx=启动顺序 >>>
审阅次数：11
1. 守护进程先选择语言，并生成初始 `config.toml`。该文件仅在首次运行时生成，仅包含 `default_locale` 和 `config_version`。
2. pre-init 子进程加载配置模板，补充缺失项，调用 `init_db(generate_schemas=True)` 创建数据表并执行迁移。
3. 守护进程读取适配器实例。它会先检查同一平台是否有重复的登录信息或端口配置，再逐个启动平台进程。
4. 若 JobQueue 使用 `websocket` 后端且模式为 `embedded`，守护进程会先启动 Hub 并等待其进入就绪状态，最多等待 10 秒。
5. 启动 Server 进程。随后守护进程每秒检查一次各子进程的运行状态。
<<< END U007169 >>>
<<< UNIT U007170 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:52-52 | ctx=退出码与重启 >>>
审阅次数：11
## 退出码与重启
<<< END U007170 >>>
<<< UNIT U007171 | md-table | packages/akari-bot-core/akaribot/core/docs/architecture.md:54-59 | ctx=退出码与重启 >>>
审阅次数：11
| 退出码 | 含义 | 守护进程操作 |
| --- | --- | --- |
| `0` | 正常退出 | Server 退出时整体退出，平台进程退出时不重启 |
| `33` | 请求重启 | 清理导入缓存，重启全部子进程 |
| `78` | 配置错误，无法恢复 | 移除该进程，不再重启 |
| 其他 | 异常退出 | 平台进程会重启，同一实例在 60 秒内连续失败三次后不再重启 |
<<< END U007171 >>>
<<< UNIT U007172 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:61-61 | ctx=退出码与重启 >>>
审阅次数：11
`~restart` 首先将发起重启的会话记录保存至 `data/private/<client>/.cache_restart_author`，随后调用 `core.server.terminate.restart()`。该函数负责释放全部运行时资源，并以退出码 33 终止进程（`os._exit(33)`）。
<<< END U007172 >>>
<<< UNIT U007173 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:63-63 | ctx=退出码与重启 >>>
审阅次数：11
新启动的 Server 进程将等待目标平台进程以新的 `peer_id` 注册为 `ready` 状态（超时上限为 60 秒），随后发送重启完成提示。模块加载失败的详细信息记录于 `.cache_loader` 中。
<<< END U007173 >>>
<<< UNIT U007174 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:65-65 | ctx=Server 初始化 >>>
审阅次数：11
## Server 初始化
<<< END U007174 >>>
<<< UNIT U007175 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:67-67 | ctx=Server 初始化 >>>
审阅次数：11
`core.server.run.main()` 依次完成：
<<< END U007175 >>>
<<< UNIT U007176 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:78-78 | ctx=Server 初始化 >>>
审阅次数：11
`init_async` 还会注册 `hourly-background` 核心任务。该任务每小时执行一次会话后台检查，清理过期的队列记录与临时缓存映射。
<<< END U007176 >>>
<<< UNIT U007177 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:80-80 | ctx=Server 初始化 >>>
审阅次数：11
主循环每秒检查一次队列轮询任务的运行状态。轮询器异常退出将被判定为严重故障，Server 进程立即退出并交由守护进程处理。
<<< END U007177 >>>
<<< UNIT U007178 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:82-82 | ctx=消息收发 >>>
审阅次数：11
## 消息收发
<<< END U007178 >>>
<<< UNIT U007179 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:84-84 | ctx=消息收发 >>>
审阅次数：11
消息分为入站和出站两条链路。平台进程负责与平台 SDK 交互，Server 负责解析消息并执行模块。
<<< END U007179 >>>
<<< UNIT U007180 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:86-86 | ctx=入站 >>>
审阅次数：11
### 入站
<<< END U007180 >>>
<<< UNIT U007181 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:88-92 | ctx=入站 >>>
审阅次数：11
1. 平台进程构造 `SessionInfo`，其中包含平台、场景、发送者、消息链和 `ctx_slot`，随后调用 `Bot.process_message()`。
2. `Bot.process_message()` 在后台保存上下文并设置保活标记，通过 `ServerAPI.receive_message` 将消息投递至 Server。处理流程结束后，平台 SDK 的上下文将被释放。
3. Server 端的 `parser()` 刷新会话信息，依次执行 `SESSION_READY` 与 `SESSION_BEFORE_WAIT` 等 Hook，检查是否存在等待该消息的挂起任务，随后解析命令前缀。
4. 命令路径首先解析别名，依据最长前缀匹配选定模块并获取执行锁，随后由模块的命令模板执行参数解析。正则匹配路径则在 `REGEX_ROUTE` Hook 执行后遍历候选模块。
5. 模块函数通过 `MessageSession` 读取 `session_info`、`parsed_msg` 和 `trigger_msg`。
<<< END U007181 >>>
<<< UNIT U007182 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:94-94 | ctx=出站 >>>
审阅次数：11
### 出站
<<< END U007182 >>>
<<< UNIT U007183 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:96-98 | ctx=出站 >>>
审阅次数：11
1. `MessageSession.send_message()` 首先整理消息链，执行敏感词过滤、媒体压缩与合规检查。通过 `OUTGOING_BEFORE_SEND` Hook 处理后，调用 `PlatformAPI.send_message`。
2. Server 依据 `owner_peer_id` 将调用分发至接收原始消息的平台进程。平台进程的 `ContextManager` 执行实际发送，并返回消息 ID。
3. 主动推送由 `Bot.post_message` 发起。该流程依据场景组与消息通道筛选候选会话，各通道优先由队首会话执行投递，其余会话作为备用会话。发送失败时，平台进程将备用会话列表返回至 Server，由 Server 依次尝试后续会话。
<<< END U007183 >>>
<<< UNIT U007184 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:100-100 | ctx=计划任务 >>>
审阅次数：11
## 计划任务
<<< END U007184 >>>
<<< UNIT U007185 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:102-102 | ctx=计划任务 >>>
审阅次数：11
`SchedulerLifecycle` 统一管理模块任务和核心任务：
<<< END U007185 >>>
<<< UNIT U007186 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:104-108 | ctx=计划任务 >>>
审阅次数：11
- 模块任务 ID 为 `module:<模块>:<序号>`，核心任务 ID 为 `core:<名称>`。
- `CronTrigger` 与 `DateTrigger` 直接生效，`IntervalTrigger` 依据 `schedule_interval_multiplier` 按倍数调整触发间隔。
- 每个任务最多同时并发运行单一实例（`max_instances=1`），错过触发时限后最多允许延迟 30 秒执行。
- 卸载、重载和关闭前会进入维护时段。在此期间调度器将停止接收新任务，等待正在启动的任务进入运行状态，随后终止正在运行的任务。
- 维护期间提交但尚未开始执行的任务，将在启动前被直接拒绝。
<<< END U007186 >>>
<<< UNIT U007187 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:110-110 | ctx=关闭顺序 >>>
审阅次数：11
## 关闭顺序
<<< END U007187 >>>
<<< UNIT U007188 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:112-112 | ctx=关闭顺序 >>>
审阅次数：11
`cleanup_sessions()` 按以下顺序执行：
<<< END U007188 >>>
<<< UNIT U007189 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:114-120 | ctx=关闭顺序 >>>
审阅次数：11
1. 停止接收新任务。
2. 等待正在处理的队列任务完成。
3. 取消消息处理器。
4. 关闭调度器。
5. 停止后台初始化。
6. 关闭模块运行环境。
7. 运行预先安排的后台清理任务。
<<< END U007189 >>>
<<< UNIT U007190 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:122-122 | ctx=关闭顺序 >>>
审阅次数：11
最后停止轮询器，并关闭队列、WebRender 与数据库连接。
<<< END U007190 >>>
<<< UNIT U007191 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:124-124 | ctx=关闭顺序 >>>
审阅次数：11
守护进程按平台进程、Server、Hub 的顺序终止子进程。Hub 最后退出，以便传递关闭信号并返回结果。
<<< END U007191 >>>
<<< UNIT U007192 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:1-1 | ctx=配置 >>>
审阅次数：11
# 配置
<<< END U007192 >>>
<<< UNIT U007193 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:3-3 | ctx=配置 >>>
审阅次数：11
本文介绍配置文件与表的布局、模板声明、读写接口与只读限制。
<<< END U007193 >>>
<<< UNIT U007194 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:5-5 | ctx=配置 >>>
审阅次数：11
`core.config.CFGManager` 负责配置的读取与持久化。配置模板类在模块导入阶段确定各字段的解析规则与转换方式。
<<< END U007194 >>>
<<< UNIT U007195 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:7-7 | ctx=配置 >>>
审阅次数：11
用户配置文件位于 `config/` 目录，全局默认配置位于 `config/global/`。`CFGManager.load()` 会同时读取两个路径，由全局配置提供备用默认值，用户配置文件中的同名项优先覆盖默认值。
<<< END U007195 >>>
<<< UNIT U007196 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:9-9 | ctx=文件与表布局 >>>
审阅次数：11
## 文件与表布局
<<< END U007196 >>>
<<< UNIT U007197 | md-table | packages/akari-bot-core/akaribot/core/docs/config.md:11-19 | ctx=文件与表布局 >>>
审阅次数：11
| 文件 | 表 | 用途 |
| --- | --- | --- |
| `config.toml` | `[config]`、`[secret]`，另有顶层 `default_locale`、`config_version` | 核心配置与核心密钥 |
| `jobqueue.toml` | `[jobqueue]`、`[jobqueue_secret]` | 通信后端与 Hub 令牌 |
| `s3.toml` | `[s3]`、`[s3_secret]` | 对象存储 |
| `smtp.toml` | `[smtp]`、`[smtp_secret]` | 邮件上报 |
| `webrender.toml` | `[webrender]` | 网页渲染 |
| `bot_<平台>.toml` | `[bot_<平台>]`、`[bot_<平台>_secret]` | 适配器配置 |
| `module_<模块>.toml` | `[module_<模块>]`、`[module_<模块>_secret]` | 模块配置 |
<<< END U007197 >>>
<<< UNIT U007198 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:21-21 | ctx=文件与表布局 >>>
审阅次数：11
密钥配置与公开配置保存在同一文件内，通过 `_secret` 配置表名称后缀予以区分。
<<< END U007198 >>>
<<< UNIT U007199 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:23-23 | ctx=全局默认层 >>>
审阅次数：11
## 全局默认层
<<< END U007199 >>>
<<< UNIT U007200 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:25-25 | ctx=全局默认层 >>>
审阅次数：11
`config/global/` 存放只读的默认配置，文件名称与用户配置对应：
<<< END U007200 >>>
<<< UNIT U007201 | md-table | packages/akari-bot-core/akaribot/core/docs/config.md:27-30 | ctx=全局默认层 >>>
审阅次数：11
| 文件 | 用途 |
| --- | --- |
| `<表名称>.global.toml` | TOML 格式的全局默认值 |
| `<表名称>.global.json` | JSON 格式的全局默认值 |
<<< END U007201 >>>
<<< UNIT U007202 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:32-32 | ctx=全局默认层 >>>
审阅次数：11
加载时，`CFGManager` 首先读取全局配置，随后加载 `config/<表名称>.toml`。
<<< END U007202 >>>
<<< UNIT U007203 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:34-34 | ctx=全局默认层 >>>
审阅次数：11
两层配置执行递归合并。用户配置优先覆盖同名的标量、列表及子表。用户文件仅需声明需要调整的项，未声明项自动继承全局配置值。
<<< END U007203 >>>
<<< UNIT U007204 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:36-36 | ctx=全局默认层 >>>
审阅次数：11
写入、删除与配置注释修复仅修改用户文件，不改动 `config/global/`。
<<< END U007204 >>>
<<< UNIT U007205 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:38-38 | ctx=全局默认层 >>>
审阅次数：11
删除用户配置文件中的某个键后，该配置键将回退至全局默认值。
<<< END U007205 >>>
<<< UNIT U007206 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:40-40 | ctx=全局默认层 >>>
审阅次数：11
若删除整个用户配置文件，该配置表仅使用全局文件。当全局文件缺失时，实例启动不受影响。
<<< END U007206 >>>
<<< UNIT U007207 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:52-52 | ctx=全局默认层 >>>
审阅次数：11
在多实例部署下，适配器配置表名称带有实例后缀（如 `bot_telegram-alt`）。若实例表不存在，读取操作将回退至该平台的基础配置表。写入操作则仅作用于对应的实例表。
<<< END U007207 >>>
<<< UNIT U007208 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:54-54 | ctx=模板声明 >>>
审阅次数：11
## 模板声明
<<< END U007208 >>>
<<< UNIT U007209 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:56-56 | ctx=模板声明 >>>
审阅次数：11
模板类在所属成员包内声明，装饰器用于指定表名称：
<<< END U007209 >>>
<<< UNIT U007210 | md-table | packages/akari-bot-core/akaribot/core/docs/config.md:58-64 | ctx=模板声明 >>>
审阅次数：11
| 装饰器 | 表名称 | 使用方 |
| --- | --- | --- |
| `@on_base_config()` | 配置表之外的顶层键 | `config.toml` 的 `default_locale`、`config_version` |
| `@on_config("config")` | `[config]` | 核心公开配置 |
| `@on_config("config", secret=True)` | `[secret]` | 核心密钥 |
| `@on_bot_config("telegram")` | `bot_telegram` | 适配器 |
| `@on_module_config("dice")` | `module_dice` | 模块 |
<<< END U007210 >>>
<<< UNIT U007211 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:66-66 | ctx=模板声明 >>>
审阅次数：11
生成的内容取决于字段的类型标注与默认值：
<<< END U007211 >>>
<<< UNIT U007212 | md-list | packages/akari-bot-core/akaribot/core/docs/config.md:68-71 | ctx=模板声明 >>>
审阅次数：11
- 支持的类型为 `bool`、`datetime`、`date`、`float`、`int`、`list`、`str`。列表默认值写成 `[]`。
- 无默认值的必填项生成 `<Replace me with <type> value>` 占位符，读取时返回 `None`。
- 联合类型中包含不受支持的成员时（如 `str | None`），生成通用占位符 `<Replace me>`。
- 键名称统一转换为小写后执行读写操作。
<<< END U007212 >>>
<<< UNIT U007213 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:73-73 | ctx=读取与写入 >>>
审阅次数：11
## 读取与写入
<<< END U007213 >>>
<<< UNIT U007214 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:75-75 | ctx=读取与写入 >>>
审阅次数：11
模板类通过元类机制依据属性名解析配置值，访问未声明的字段将直接抛出 `AttributeError`：
<<< END U007214 >>>
<<< UNIT U007215 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:84-84 | ctx=读取与写入 >>>
审阅次数：11
底层接口：
<<< END U007215 >>>
<<< UNIT U007216 | md-table | packages/akari-bot-core/akaribot/core/docs/config.md:86-92 | ctx=读取与写入 >>>
审阅次数：11
| 方法 | 说明 |
| --- | --- |
| `CFGManager.get(q, default=None, cfg_type=None, secret=False, table_name=None)` | 读取配置项数值，缺失时写入默认值 |
| `CFGManager.has(q, secret=False, table_name=None)` | 检查配置键是否存在 |
| `CFGManager.write(...)` | 执行配置写入（受只读约束） |
| `CFGManager.edit_write(...)`、`edit_delete(...)` | 交互式编辑写入与删除（必须获得明确授权） |
| `CFGManager.save()` | 仅持久化内容发生变动的配置文件 |
<<< END U007216 >>>
<<< UNIT U007217 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:94-94 | ctx=读取与写入 >>>
审阅次数：11
若读取到的值为模板写入的占位符（如 `<Replace me with <type> value>` 或 `<Replace me>`），返回 `None`。若配置值类型与模板不符，系统给出警告并返回原值。
<<< END U007217 >>>
<<< UNIT U007218 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:96-96 | ctx=字段注释 >>>
审阅次数：11
## 字段注释
<<< END U007218 >>>
<<< UNIT U007219 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:98-98 | ctx=字段注释 >>>
审阅次数：11
在模板类中声明字段后，必须在所属成员包的 `locales/zh_cn.json` 中为其补充对应的配置注释项：
<<< END U007219 >>>
<<< UNIT U007220 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:104-104 | ctx=字段注释 >>>
审阅次数：11
表名称取值：
<<< END U007220 >>>
<<< UNIT U007221 | md-list | packages/akari-bot-core/akaribot/core/docs/config.md:106-108 | ctx=字段注释 >>>
审阅次数：11
- 核心公开表为 `config`，核心密钥表为 `secret`。
- 适配器表为 `bot_<平台>`，适配器密钥表为 `bot_<平台>_secret`。
- 模块表为 `module_<模块>`，模块密钥表为 `module_<模块>_secret`。
<<< END U007221 >>>
<<< UNIT U007222 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:110-110 | ctx=字段注释 >>>
审阅次数：11
配置注释用于说明对应字段的用途。生成配置文件时，注释与字段一并写入。切换 `default_locale` 后，`CFGManager.repair_i18n_comments()` 会按新语言重写注释。
<<< END U007222 >>>
<<< UNIT U007223 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:112-112 | ctx=只读限制 >>>
审阅次数：11
## 只读约束
<<< END U007223 >>>
<<< UNIT U007224 | md-list | packages/akari-bot-core/akaribot/core/docs/config.md:114-119 | ctx=只读限制 >>>
审阅次数：11
- 守护进程在启动子进程前将 `AKARI_CONFIG_READONLY` 设置为 `1`，平台进程与 Server 均设为只读模式。
- 在只读进程中调用 `write()` 或 `save()` 会抛出 `ConfigOperationError`。`edit_write()`、`edit_delete()` 仅能在明确授权的范围内使用。`~config` 命令和启动阶段补充缺失的配置与密钥时会调用这两个方法。
- 缺失项仅在启动前的准备阶段写入。
- 配置写入前必须获取文件锁 `config/.config.lock`。重新加载、内存修改与文件保存均在持有该锁期间执行，同一时间仅允许单一进程执行写入操作（获取锁的最长等待时间为 10 秒。若锁文件超过 60 秒未更新，则判定为过期失效）。
- 写入过程采用临时文件加 `os.replace` 执行原子替换。
- 当文件 mtime 发生变更后，系统最多延迟 1 秒触发重新加载。若磁盘文件被清空但内存缓存有效，则继续保留内存中的当前配置值。
<<< END U007224 >>>
<<< UNIT U007225 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:121-121 | ctx=配置版本 >>>
审阅次数：11
## 配置版本
<<< END U007225 >>>
<<< UNIT U007226 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:123-123 | ctx=配置版本 >>>
审阅次数：11
`config.toml` 的 `config_version` 由 `core.config.update` 执行升级。
<<< END U007226 >>>
<<< UNIT U007227 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:125-125 | ctx=配置版本 >>>
审阅次数：11
其余配置文件的版本由所属成员包维护。配置迁移脚本存放于包内 `config_migrations/` 目录，文件名称以四位数字编号开头。迁移执行完成后，当前迁移编号将写回该配置文件的 `config_version` 字段。
<<< END U007227 >>>
<<< UNIT U007228 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:127-127 | ctx=配置版本 >>>
审阅次数：11
新生成的配置文件将 `manifest.toml` 中的 `config_schema_version` 作为初始 `config_version`。首个迁移脚本的编号必须为 `config_schema_version` 数值加 1，后续迁移编号依次单调递增。
<<< END U007228 >>>
<<< UNIT U007229 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:1-1 | ctx=数据库 >>>
审阅次数：11
# 数据库
<<< END U007229 >>>
<<< UNIT U007230 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:3-3 | ctx=数据库 >>>
审阅次数：11
本文介绍 `default` 与 `local` 双数据库连接、union 数据模型、数据迁移机制及热重载流程。
<<< END U007230 >>>
<<< UNIT U007231 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:5-5 | ctx=数据库 >>>
审阅次数：11
数据库层基于 Tortoise ORM，负责连接管理、模型注册、启动迁移与热重载。
<<< END U007231 >>>
<<< UNIT U007232 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:7-7 | ctx=数据库 >>>
审阅次数：11
业务模型继承 `akaribot.core.api.DBModel`，通过 `get_by_target_id()`、`get_by_sender_id()` 关联到会话或 union。
<<< END U007232 >>>
<<< UNIT U007233 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:9-9 | ctx=双连接 >>>
审阅次数：11
## 双连接
<<< END U007233 >>>
<<< UNIT U007234 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:11-11 | ctx=双连接 >>>
审阅次数：11
`init_db()` 注册两个连接与两个应用：
<<< END U007234 >>>
<<< UNIT U007235 | md-table | packages/akari-bot-core/akaribot/core/docs/database.md:13-16 | ctx=双连接 >>>
审阅次数：11
| 连接 | 默认连接字符串 | 应用 | 内容 |
| --- | --- | --- | --- |
| `default` | `sqlite://database/save.db` | `models` | 核心模型与各成员包的模型 |
| `local` | `sqlite://database/local.db` | `local_models` | 本机缓存表 |
<<< END U007235 >>>
<<< UNIT U007236 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:18-18 | ctx=双连接 >>>
审阅次数：11
`default` 的连接字符串由 `CoreSecretConfig.db_path` 提供。SQLite 的相对路径以实例根目录为基准解析，进程可以从任意目录启动。
<<< END U007236 >>>
<<< UNIT U007237 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:20-20 | ctx=双连接 >>>
审阅次数：11
连接参数首先配置 `busy_timeout=30000`，随后启用 WAL 模式。并发启动期间，等待写入锁的时间同样受该超时阈值约束。
<<< END U007237 >>>
<<< UNIT U007238 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:22-22 | ctx=双连接 >>>
审阅次数：11
`local` 连接用于存储可随时重建的本机数据（如敏感词检测缓存与外部平台活动记录），相关数据独立保存于专用数据库文件中。
<<< END U007238 >>>
<<< UNIT U007239 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:38-38 | ctx=双连接 >>>
审阅次数：11
框架通过各成员包的发现元数据收集模型文件，由 `PackageRegistry.db_model_paths()` 提供对应的导入路径。
<<< END U007239 >>>
<<< UNIT U007240 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:40-40 | ctx=双连接 >>>
审阅次数：11
`init_db()` 将上述模型路径注册至 `models` 应用。`get_model_names()` 与 `get_model_fields()` 供 `~database` 命令列出数据表及其字段定义。
<<< END U007240 >>>
<<< UNIT U007241 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:42-42 | ctx=union 数据 >>>
审阅次数：11
## union 数据
<<< END U007241 >>>
<<< UNIT U007242 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:44-44 | ctx=union 数据 >>>
审阅次数：11
鉴于平台原生账号与场景 ID 存在变更可能，所有业务数据统一关联至持久化的 union 实体：
<<< END U007242 >>>
<<< UNIT U007243 | md-table | packages/akari-bot-core/akaribot/core/docs/database.md:46-51 | ctx=union 数据 >>>
审阅次数：11
| 表 | 关键列 | 说明 |
| --- | --- | --- |
| `sender_union_info` | `union_id` | 用户数据：`blocked`、`trusted`、`superuser`、`warns`、`petal`、`sender_data` |
| `sender_union_bind` | `sender_id` → `union_id` | 平台账号到用户 union 的映射 |
| `target_union_info` | `union_id` | 场景数据：`muted`、`locale`、`modules`、`custom_admins`、`banned_users`、`target_data` |
| `target_union_bind` | `target_id` → `union_id`，`channel_id` | 平台场景到场景 union 的映射与消息通道编号 |
<<< END U007243 >>>
<<< UNIT U007244 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:53-53 | ctx=union 数据 >>>
审阅次数：11
`resolve_union(id, create)` 解析并返回记录所属的 union。若 `create` 为 `True` 且对应记录不存在，则自动创建新记录。
<<< END U007244 >>>
<<< UNIT U007245 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:55-55 | ctx=union 数据 >>>
审阅次数：11
`TargetUnionInfo.config_module()`、`switch_mute()`、`edit_target_data()` 与 `SenderUnionInfo.edit_sender_data()` 均在数据库事务中执行，通过 `select_for_update()` 实现 JSON 列的安全更新。
<<< END U007245 >>>
<<< UNIT U007246 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:57-57 | ctx=union 数据 >>>
审阅次数：11
同一 union 实体下具有相同 `channel_id` 的场景归属于同一消息通道，主动推送按通道维度仅执行一次投递。
<<< END U007246 >>>
<<< UNIT U007247 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:59-59 | ctx=union 数据 >>>
审阅次数：11
`delete_union()` 首先校验外部引用约束，随后清理该 union 作用域内的全部关联数据表记录。
<<< END U007247 >>>
<<< UNIT U007248 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:61-61 | ctx=union 数据 >>>
审阅次数：11
跨表写入同一 union 时，首先调用 `union_mutation()`，随后在 `default` 事务中对该 union 所在的数据行加锁：
<<< END U007248 >>>
<<< UNIT U007249 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:88-88 | ctx=union 数据 >>>
审阅次数：11
查询与写入操作必须共用同一 `connection`，否则 `select_for_update()` 获取的行级锁无法覆盖后续写入操作。
<<< END U007249 >>>
<<< UNIT U007250 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:90-90 | ctx=union 数据 >>>
审阅次数：11
核心包在 `manifest.toml` 的 `owned_tables` 中声明自身拥有的数据表，数据清理时据此识别数据表所属的包。各成员包的模型与数据表均由各自的 `manifest.toml` 声明。
<<< END U007250 >>>
<<< UNIT U007251 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:92-92 | ctx=迁移 >>>
审阅次数：11
## 迁移
<<< END U007251 >>>
<<< UNIT U007252 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:94-94 | ctx=迁移 >>>
审阅次数：11
各成员包将迁移脚本（revision）存放于 `migrations/` 目录（或由 `manifest.migrations` 显式声明的路径）：
<<< END U007252 >>>
<<< UNIT U007253 | md-list | packages/akari-bot-core/akaribot/core/docs/database.md:105-109 | ctx=迁移 >>>
审阅次数：11
- `REVISION` 非空，`DEPENDS_ON` 仅能指向同包 revision。`DEPENDS_ON` 未声明时，按 revision 字典序执行。
- 执行顺序固定为首先应用 core 的全部待执行 revision，随后按成员包名称字典序依次执行各成员包的迁移。
- 已应用的迁移记录保存于 `schema_migrations`（包含 `package`、`revision`、`applied_at`、`checksum` 字段），以 `(package, revision)` 复合键保持唯一。迁移文件内容发生变动时 checksum 随之变化，系统据此检测已应用迁移文件的异常篡改。
- 每条 revision 必须保持幂等与可重复执行。鉴于 MySQL 的 DDL 操作会自动提交事务，无法与版本记录纳入同一原子事务，因而每个执行步骤均遵循“先探测后执行”原则。SQLite 支持事务性 DDL，Runner 会将单条 revision 与对应版本记录纳入同一原子事务。
- `MigrationContext` 提供 `execute()`、`execute_script()`、`fetch_all()`、`has_table()`、`has_column()`、`rename_table()`、`rename_column()`，按方言生成 SQL。
<<< END U007253 >>>
<<< UNIT U007254 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:111-111 | ctx=迁移 >>>
审阅次数：11
数据库迁移仅在具备写入权限的初始化进程中执行。pre-init 以 `generate_schemas=True` 参数调用 `init_db()`，随后触发 `run_startup_migrations()`。平台进程与 Server 仅对既有数据执行读写，数据表及表结构的创建与变更均由独立初始化进程完成。
<<< END U007254 >>>
<<< UNIT U007255 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:113-113 | ctx=热重载 >>>
审阅次数：11
## 热重载
<<< END U007255 >>>
<<< UNIT U007256 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:115-115 | ctx=热重载 >>>
审阅次数：11
模块安装、卸载或执行数据库维护操作时将触发连接重建：
<<< END U007256 >>>
<<< UNIT U007257 | md-list | packages/akari-bot-core/akaribot/core/docs/database.md:117-120 | ctx=热重载 >>>
审阅次数：11
1. `prepare_db_reload()` 在原有 context 仍可用时初始化新 context。
2. 激活新 context 前，系统会等待 JobQueue 处理完毕队列中的存量任务，并使 Scheduler 进入维护时段以停止接收新任务，同时取消当前运行中的计划任务。
3. `activate_db_reload()` 原子替换全局 context，随后关闭旧 context。
4. 若执行失败，`close_prepared_db_reload()` 会丢弃未激活的 context，原有连接继续保持可用。
<<< END U007257 >>>
<<< UNIT U007258 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:122-122 | ctx=热重载 >>>
审阅次数：11
`close_db()` 负责释放连接并清理 Tortoise 的全局及任务级 context，确保下一次初始化从干净的初始状态开始。
<<< END U007258 >>>
<<< UNIT U007259 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:1-1 | ctx=开发流程 >>>
审阅次数：11
# 开发流程
<<< END U007259 >>>
<<< UNIT U007260 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:3-3 | ctx=开发流程 >>>
审阅次数：11
本文介绍开发环境搭建、日常质量检查、测试执行命令及代码提交约定。包结构、API 与测试框架的详细说明分别参见[模块开发](module-development.md)、[公共 API](public-api.md)及[测试框架运行入口](../../../../akari-bot-testing/akaribot/testing/docs/index.md)。
<<< END U007260 >>>
<<< UNIT U007261 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:5-5 | ctx=环境准备 >>>
审阅次数：11
## 环境准备
<<< END U007261 >>>
<<< UNIT U007262 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:7-7 | ctx=环境准备 >>>
审阅次数：11
仓库采用 uv workspace 结构，仓库根目录的 `pyproject.toml` 仅声明工作区中的包与工具配置，未包含 `[project]` 表。
<<< END U007262 >>>
<<< UNIT U007263 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:14-14 | ctx=环境准备 >>>
审阅次数：11
工具缓存与虚拟环境 `.venv` 均置于工作区内部。新增依赖项时必须按成员包维度添加：
<<< END U007263 >>>
<<< UNIT U007264 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:20-20 | ctx=环境准备 >>>
审阅次数：11
`uv add` 默认将依赖写入 `[project]` 表，而仓库根目录的 `pyproject.toml` 仅声明工作区且未包含该表。因此新增依赖时，必须通过 `--package` 参数指定具体目标包。
<<< END U007264 >>>
<<< UNIT U007265 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:22-22 | ctx=环境准备 >>>
审阅次数：11
依赖版本以 `uv.lock` 为准。`pre-commit` 的 `uv-export` 从该文件导出依赖清单，输出结果不包含哈希值。
<<< END U007265 >>>
<<< UNIT U007266 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:24-24 | ctx=环境准备 >>>
审阅次数：11
CI 环境使用 `--locked --all-extras --dev` 执行安装。若 `uv.lock` 与声明的依赖不一致，安装流程将直接失败。
<<< END U007266 >>>
<<< UNIT U007267 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:26-26 | ctx=日常命令 >>>
审阅次数：11
## 日常命令
<<< END U007267 >>>
<<< UNIT U007268 | md-table | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:28-35 | ctx=日常命令 >>>
审阅次数：11
| 用途 | 命令 |
| --- | --- |
| 全量测试 | `CI=1 MPLCONFIGDIR=/tmp/mplconfig PYTHONIOENCODING=UTF-8 .venv/bin/python -m akaribot.testing` |
| 单个文件 | `.venv/bin/python tests/run_one.py packages/akari-bot-core/tests/test_registry.py` |
| 静态检查 | `.venv/bin/ruff check .` 与 `.venv/bin/ruff format --check .` |
| 注释与排版 | `.venv/bin/python tools/lint_comments.py` |
| 分层与依赖 | `.venv/bin/python tools/lint_boundaries.py` |
| 内部版本要求 | `.venv/bin/python tools/lint_versions.py` |
<<< END U007268 >>>
<<< UNIT U007269 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:37-37 | ctx=日常命令 >>>
审阅次数：11
全量测试运行完成后，失败用例清单必须与 `tools/test_baseline.txt` 中的基准用例按名称完全保持一一对应。测试执行完毕后，调用 `tools/check_test_baseline.py --junit junit.xml --baseline tools/test_baseline.txt` 验证两者的一致性。
<<< END U007269 >>>
<<< UNIT U007270 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:39-39 | ctx=日常命令 >>>
审阅次数：11
只读测试使用另一份清单 `tools/test_baseline_readonly.txt`。该清单由 `tools/check_test_baseline.py` 的 `--update` 参数重新生成。
<<< END U007270 >>>
<<< UNIT U007271 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:41-41 | ctx=提交前检查 >>>
审阅次数：11
## 提交前检查
<<< END U007271 >>>
<<< UNIT U007272 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:43-43 | ctx=提交前检查 >>>
审阅次数：11
提交前需要执行下列检查，每一项均覆盖整个仓库：
<<< END U007272 >>>
<<< UNIT U007273 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:51-51 | ctx=提交前检查 >>>
审阅次数：11
`pre-commit install` 安装的钩子与上述检查项不同，`comment-lint` 与 `boundary-lint` 带有 `--diff HEAD` 参数，仅检查改动行，避免仓库中已有的存量违规阻止提交。推送前仍需要执行全部检查。其余钩子为 `uv-export`、`ruff-check --fix` 与 `ruff-format`。
<<< END U007273 >>>
<<< UNIT U007274 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:53-53 | ctx=代码风格 >>>
审阅次数：11
## 代码风格
<<< END U007274 >>>
<<< UNIT U007275 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:55-55 | ctx=代码风格 >>>
审阅次数：11
Ruff 行宽 120、双引号、目标版本 `py312`，忽略 `E402`、`F405`、`F403`、`E741`、`E721`。导入按标准库、第三方、项目内部分组。
<<< END U007275 >>>
<<< UNIT U007276 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:57-57 | ctx=代码风格 >>>
审阅次数：11
模块与适配器仅从 `akaribot.core.api` 获取公开接口。核心内部出现循环依赖时，改用 `akaribot.core.exports` 注册，需要时按名称取回。
<<< END U007276 >>>
<<< UNIT U007277 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:59-59 | ctx=代码风格 >>>
审阅次数：11
注释旨在阐释代码背后的设计意图与边界约束，单条长度通常不超过三行。逻辑清晰且含义明确的代码无需添加注释，非公开 API 严禁添加 docstring。
<<< END U007277 >>>
<<< UNIT U007278 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:61-61 | ctx=代码风格 >>>
审阅次数：11
注释、文档及配置说明一律采用严谨的书面中文。中文与西文字符之间必须保留空格，标点统一采用全角符号。面向用户的交互文案称呼对方为“你”，机器人自称为“机器人”。
<<< END U007278 >>>
<<< UNIT U007279 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:63-63 | ctx=代码风格 >>>
审阅次数：11
文档、注释与配置说明仅描述当前状态。阐释设计取舍时直接陈述当前逻辑与约束，历史演进交由 git 记录。为迁移历史数据保留的兼容逻辑需注明适用范围。
<<< END U007279 >>>
<<< UNIT U007280 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:65-65 | ctx=分支与提交 >>>
审阅次数：11
## 分支与提交
<<< END U007280 >>>
<<< UNIT U007281 | md-list | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:67-71 | ctx=分支与提交 >>>
审阅次数：11
- 新功能分支使用 `dev/` 前缀，修复分支使用 `fix/` 前缀，分支名称使用英文。
- 未获得明确授权不可执行 `git commit`、`git add`、`git push`、`git reset` 或 `git checkout -- <文件>`。授权仅对当次请求有效。
- 提交信息使用英文书面语，正文写明实际运行输出、失败用例的对比与检查结果等证据。
- 移动文件必须使用 `git mv` 以保留历史追溯记录。当根目录保留同名兼容文件时，git 无法自动判定为重命名，必须拆分为“先纯移动文件、后修改内容”两次独立提交。
- 当成员包内存在源码修改时，必须递增该包 `pyproject.toml` 中的 `version`。若无需升级版本，必须在提交信息的最后一段单独声明 `Skip-Version: true`（豁免全部成员包），或填写 `Skip-Version: <包名称>[, <包名称>]`（列出特定豁免包）。版本检查脚本 `tools/check_versions.py` 负责验证该约束，由 CI 在拉取请求（PR）阶段以目标分支为基准执行检查。
<<< END U007281 >>>
<<< UNIT U007282 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:73-73 | ctx=文档 >>>
审阅次数：11
## 文档
<<< END U007282 >>>
<<< UNIT U007283 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:75-75 | ctx=文档 >>>
审阅次数：11
每个成员包的导入包根目录下均包含 `docs/` 目录，通过 `docs/config/global/docs.global.toml` 声明文档标题、简介及排序权重。在 `pyproject.toml` 的 `[project.entry-points."akaribot.docs"]` 中声明文档导入路径，文档构建引擎据此收录该包的文档页面。
<<< END U007283 >>>
<<< UNIT U007284 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:77-77 | ctx=文档 >>>
审阅次数：11
文档站点管理命令涵盖 `akaribot docs list|build|serve|deploy|status|clean`。站点配置定义于实例根目录的 `docs.toml`，构建产物输出至 `cache/docs/` 目录。关于包文档所需的元数据字段及目录结构规范，详见 `docs/package-docs.md`。
<<< END U007284 >>>
<<< UNIT U007285 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:1-1 | ctx=常见问题 >>>
审阅次数：11
# 常见问题
<<< END U007285 >>>
<<< UNIT U007286 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:3-3 | ctx=常见问题 >>>
审阅次数：11
本文汇总常见问题的排查与解决方案。相关命令与默认配置均以当前源码实现为准。权限模型、模块启用及部署细节分别参见[权限](permissions.md)、[模块开发](module-development.md)与 [CLI 文档](../../../../akari-bot-cli/akaribot/cli/docs/index.md)。
<<< END U007286 >>>
<<< UNIT U007287 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:5-5 | ctx=查看帮助与文档 >>>
审阅次数：11
## 查看帮助与文档
<<< END U007287 >>>
<<< UNIT U007288 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:7-7 | ctx=查看帮助与文档 >>>
审阅次数：11
在会话中发送 `~help` 可查看可用模块列表与命令入口。发送 `~help <module>` 可获取指定模块的详细命令语法、参数定义及权限要求。
<<< END U007288 >>>
<<< UNIT U007289 | md-list | packages/akari-bot-core/akaribot/core/docs/faq.md:9-11 | ctx=查看帮助与文档 >>>
审阅次数：11
- `--legacy`：显式输出纯文本或表格版本。
- `--img`：显式输出图片渲染版本。
- 若当前平台未声明图片支持能力，帮助命令将自动降级输出文本版本。
<<< END U007289 >>>
<<< UNIT U007290 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:13-13 | ctx=查看帮助与文档 >>>
审阅次数：11
文档站点由已安装成员包内的 `docs/` 资源聚合构建生成，常用运维命令如下：
<<< END U007290 >>>
<<< UNIT U007291 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:21-21 | ctx=查看帮助与文档 >>>
审阅次数：11
文档构建依赖 Node.js 与 npm 环境，具体版本要求以主题清单声明为准。站点生成产物存放于实例目录 `cache/docs/`。`~help` 面板底部的在线文档链接读取自 `config.toml` 中的 `help_url` 与 `help_page_url` 配置项。
<<< END U007291 >>>
<<< UNIT U007292 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:23-23 | ctx=模块没有反应或未启用 >>>
审阅次数：11
## 模块没有反应或未启用
<<< END U007292 >>>
<<< UNIT U007293 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:25-25 | ctx=模块没有反应或未启用 >>>
审阅次数：11
首先确认目标模块是否已安装、是否已全局加载以及是否在当前场景中启用，三者属于相互独立的状态维度：
<<< END U007293 >>>
<<< UNIT U007294 | md-table | packages/akari-bot-core/akaribot/core/docs/faq.md:27-31 | ctx=模块没有反应或未启用 >>>
审阅次数：11
| 状态 | 检查方式 | 修改方式 |
| --- | --- | --- |
| 已安装 | `akaribot module list` | `akaribot module add <名>` |
| 全局加载 | `akaribot module status` | `akaribot module load <名>` |
| 场景启用 | `~module list` | `~module enable <名>` |
<<< END U007294 >>>
<<< UNIT U007295 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:33-33 | ctx=模块没有反应或未启用 >>>
审阅次数：11
声明 `base=True` 的核心基础模块始终处于启用状态。普通功能模块需要由场景管理员执行 `~module enable` 手动启用。
<<< END U007295 >>>
<<< UNIT U007296 | md-list | packages/akari-bot-core/akaribot/core/docs/faq.md:35-36 | ctx=模块没有反应或未启用 >>>
审阅次数：11
- 未启用时，机器人会提示启用命令。
- 声明了 `required_superuser` 的模块仅超级用户可以启用。`~module enable all` 会跳过此类模块。
<<< END U007296 >>>
<<< UNIT U007297 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:38-38 | ctx=模块没有反应或未启用 >>>
审阅次数：11
若模块处于启用状态但仍未响应指令，请排查平台能力支持与机器人权限：
<<< END U007297 >>>
<<< UNIT U007298 | md-list | packages/akari-bot-core/akaribot/core/docs/faq.md:40-42 | ctx=模块没有反应或未启用 >>>
审阅次数：11
- `rss` 模块要求平台具备主动推送能力（`support_rss`）。
- `regex` 与 `event` 模块要求平台具备全部消息接收权限（`read_all_messages`）。
- 当机器人缺失 `required_bot_permissions` 声明的必要权限时，`~module enable` 将列出缺失的权限项。
<<< END U007298 >>>
<<< UNIT U007299 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:44-44 | ctx=模块没有反应或未启用 >>>
审阅次数：11
当机器人被限制发言或发送者处于封禁状态时，各模块将静默拒绝响应。
<<< END U007299 >>>
<<< UNIT U007300 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:46-46 | ctx=提示权限不足 >>>
审阅次数：11
## 提示权限不足
<<< END U007300 >>>
<<< UNIT U007301 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:48-48 | ctx=提示权限不足 >>>
审阅次数：11
权限层级划分为普通用户、场景管理员、超级用户与基础超级用户，鉴权逻辑与授权机制参见[权限说明](permissions.md)。常见处理方案如下：
<<< END U007301 >>>
<<< UNIT U007302 | md-list | packages/akari-bot-core/akaribot/core/docs/faq.md:50-53 | ctx=提示权限不足 >>>
审阅次数：11
- 若场景管理命令被拒绝，可由场景管理员执行 `~admin add <用户 ID>`，或由平台原生管理员操作。
- 若超级用户命令被拒绝，可由现有超级用户执行 `~superuser add <用户 ID>`。
- 若仅特定模块被拒绝，可由超级用户执行 `~auth add <用户 ID> <模块>`，该授权仅对声明 `required_superuser` 的模块生效。
- 若模块开启被拒绝，通常因模块级权限门槛、机器人权限缺失或平台能力不满足所致，请依循返回提示排查。
<<< END U007302 >>>
<<< UNIT U007303 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:55-55 | ctx=提示权限不足 >>>
审阅次数：11
`base_superuser` 仅能通过 `config.toml` 维护。
<<< END U007303 >>>
<<< UNIT U007304 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:57-57 | ctx=报告问题与贡献 >>>
审阅次数：11
## 报告问题与贡献
<<< END U007304 >>>
<<< UNIT U007305 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:59-59 | ctx=报告问题与贡献 >>>
审阅次数：11
提交 Issue 前必须检索是否已存在同类问题。缺陷报告应当包含简要描述、复现步骤、预期结果、实际表现与相关日志。新功能建议应当阐明应用场景与设计思路。仓库地址与 Issue 模板参见 [CONTRIBUTING.md](https://github.com/Teahouse-Studios/akari-bot/blob/master/CONTRIBUTING.md)。
<<< END U007305 >>>
<<< UNIT U007306 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:61-61 | ctx=报告问题与贡献 >>>
审阅次数：11
代码贡献流程包括 Fork 仓库后创建特性分支，完成改动后发起拉取请求（PR）。分支命名必须采用英文，新功能分支以 `dev/` 为前缀，缺陷修复分支以 `fix/` 为前缀。发起提交前必须执行 Ruff、注释检查、边界检查与版本一致性检查，对应命令参见贡献指南。
<<< END U007306 >>>
<<< UNIT U007307 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:63-63 | ctx=报告问题与贡献 >>>
审阅次数：11
多语言翻译统一通过 Weblate 平台协同提交。简体中文以外的翻译词句讨论，请勿在 GitHub Issue 中提出。
<<< END U007307 >>>
<<< UNIT U007308 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:67-67 | ctx=报告问题与贡献 >>>
审阅次数：11
凡涉及安全漏洞与敏感信息的缺陷，严禁提交至公开 Issue 或公开讨论区，请依循 `SECURITY.md` 中指引的私密沟通渠道联系维护团队。
<<< END U007308 >>>
<<< UNIT U007309 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:71-71 | ctx=许可证 >>>
审阅次数：11
## 许可证
<<< END U007309 >>>
<<< UNIT U007310 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:73-73 | ctx=许可证 >>>
审阅次数：11
core、官方内置模块及平台适配器采用 AGPL-3.0-only 开源许可证。字体资产采用 OFL-1.1 协议，品牌视觉资产采用专有商业授权，`akari-bot-html2text` 采用 GPL-3.0 协议。各成员包所适用的具体许可协议，以该包内 `pyproject.toml` 及 LICENSE 文件中的明确声明为准。
<<< END U007310 >>>
<<< UNIT U007311 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:75-75 | ctx=许可证 >>>
审阅次数：11
修改并分发本项目衍生版本时，必须严格遵守对应的开源许可协议约束。AGPL-3.0 许可证额外要求通过网络向服务终端用户公开对应的完整源代码。
<<< END U007311 >>>
<<< UNIT U007312 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:77-77 | ctx=更新实例 >>>
审阅次数：11
## 更新实例
<<< END U007312 >>>
<<< UNIT U007313 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:79-79 | ctx=更新实例 >>>
审阅次数：11
实例环境中的 core、功能模块及适配器均通过 CLI 统一更新：
<<< END U007313 >>>
<<< UNIT U007314 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:85-85 | ctx=更新实例 >>>
审阅次数：11
在线执行 `~update` 时，系统将调用 CLI 的 `module update --defer-runtime` 命令。软件包安装完成后，按提示执行 `~restart`。指定 `--defer-runtime` 参数时，该阶段仅下载安装软件包并同步配置，数据库迁移与代码生效将推迟至下一次启动流程中执行。
<<< END U007314 >>>
<<< UNIT U007315 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:87-87 | ctx=更新实例 >>>
审阅次数：11
在宿主机环境直接执行升级时，数据库迁移与新版代码将立即生效。若升级涉及底层数据结构变更，必须首先停止实例进程，并完整备份数据库文件与配置目录。CLI 工具自身请依循 `uv tool` 的标准更新方式升级。
<<< END U007315 >>>
<<< UNIT U007316 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:89-89 | ctx=自建实例 >>>
审阅次数：11
## 自建实例
<<< END U007316 >>>
<<< UNIT U007317 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:91-91 | ctx=自建实例 >>>
审阅次数：11
运行环境需要满足仓库 `pyproject.toml` 中声明的 Python 版本及 [uv](https://docs.astral.sh/uv/) 包管理器要求。基础搭建流程如下：
<<< END U007317 >>>
<<< UNIT U007318 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:102-102 | ctx=自建实例 >>>
审阅次数：11
依据 `config schema` 输出的字段定义配置适配器的登录信息，随后启动机器人实例。使用 `akaribot config set <字段> <值> --table <表名称>` 命令写入的配置值，将依据对应配置模板所声明的类型执行自动转换。
<<< END U007318 >>>
<<< UNIT U007319 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:104-104 | ctx=自建实例 >>>
审阅次数：11
`akaribot init` 默认安装品牌资产、表情与常规可选依赖。指定 `--minimal` 时仅安装核心所需的最小依赖。模块通过 `akaribot module add <名>` 安装。历史部署的备份、试运行与迁移参见 [命令参考中的 migrate](../../../../akari-bot-cli/akaribot/cli/docs/commands.md#migrate)。
<<< END U007319 >>>
<<< UNIT U007320 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:1-1 | ctx=本地化 >>>
审阅次数：11
# 本地化
<<< END U007320 >>>
<<< UNIT U007321 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:3-3 | ctx=本地化 >>>
审阅次数：11
本文介绍文案定义规范、国际化键名称结构、动态插值规则及语言资源文件的维护流程。
<<< END U007321 >>>
<<< UNIT U007322 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:5-5 | ctx=本地化 >>>
审阅次数：11
面向用户的固定文案统一采用 `I18NContext` 构造声明，翻译资源持久化于各成员包的 `locales/` 目录，运行时由 `akari-bot-i18n` 的 `Locale` 组件执行解析。默认语言环境为 `zh_cn`。支持的语言列表依据 `lang_list` 动态生成并在文档构建时注入页面：
<<< END U007322 >>>
<<< UNIT U007323 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:17-17 | ctx=I18NContext >>>
审阅次数：11
`I18NContext` 作为特殊消息元素封装了文案键名称与插值参数，在消息投递时依据会话语言环境动态翻译。支持的可选参数如下：
<<< END U007323 >>>
<<< UNIT U007324 | md-table | packages/akari-bot-core/akaribot/core/docs/i18n.md:19-23 | ctx=I18NContext >>>
审阅次数：11
| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `fallback` | `True` | 键缺失时回退到默认语言 |
| `locale_failed_prompt` | `True` | 翻译失败时附加提示 |
| `disable_joke` | `False` | 禁用文案中的玩笑替换 |
<<< END U007324 >>>
<<< UNIT U007325 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:25-25 | ctx=I18NContext >>>
审阅次数：11
插值参数可以为字符串、数值或嵌套的消息元素。当消息元素作为参数传入时，系统将在渲染前将其转换为文本字符串。
<<< END U007325 >>>
<<< UNIT U007326 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:27-27 | ctx=键与来源 >>>
审阅次数：11
## 键与来源
<<< END U007326 >>>
<<< UNIT U007327 | md-list | packages/akari-bot-core/akaribot/core/docs/i18n.md:29-36 | ctx=键与来源 >>>
审阅次数：11
- 各成员包通过 `manifest.toml` 的 `locales` 字段声明文案资源目录。
- 省略该字段时，默认使用 `locales`。
- 目录中的文件名称为语言代码。
- 文案以简体中文 `locales/zh_cn.json` 为基准源文件，开发者仅需维护该文件，所有新增键名称均仅在该文件中定义。
- 运行时快照由 `build_locale_snapshot(lang_list, collect_locale_paths(), "akari-bot")` 构建，`collect_locale_paths()` 来自发现层，core 的目录排在最前。
- 配置字段注释使用 `config.comments.<表名称>.<字段名>` 形式的键，与普通文案保存在同一文件。
- 命令模板中的帮助文案写作 `I18N:key` 并用双层花括号包裹，由帮助系统解析。
- 术语占位符 `{TERM:...}` 由 `locales/terms/<语言>.json` 提供平台相关措辞（如“场景”“群组”）。
<<< END U007327 >>>
<<< UNIT U007328 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:38-38 | ctx=插值与占位符 >>>
审阅次数：11
## 插值与占位符
<<< END U007328 >>>
<<< UNIT U007329 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:40-40 | ctx=插值与占位符 >>>
审阅次数：11
文案模板采用 `${name}` 执行插值：
<<< END U007329 >>>
<<< UNIT U007330 | md-list | packages/akari-bot-core/akaribot/core/docs/i18n.md:48-50 | ctx=插值与占位符 >>>
审阅次数：11
- 占位符名称按含义选取英文名称，与调用处关键字一一对应。
- 占位符名称严禁与 `t()` 的内部形参（`key`、`fallback`、`locale_failed_prompt`、`disable_joke`）发生冲突。形参同名将在渲染时抛出 `TypeError`（例如使用占位符 `${key}` 同时传递 `key=...` 关键字实参）。
- 修改键名称或占位符后，必须同时核对调用点的关键字参数。
<<< END U007330 >>>
<<< UNIT U007331 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:52-52 | ctx=语言文件维护 >>>
审阅次数：11
## 语言文件维护
<<< END U007331 >>>
<<< UNIT U007332 | md-list | packages/akari-bot-core/akaribot/core/docs/i18n.md:54-56 | ctx=语言文件维护 >>>
审阅次数：11
- 仅编辑 `locales/zh_cn.json`。其他语言文件由 Weblate 自动同步提交，请勿自行创建、修改或补齐。
- `assets/config_store/<语言>/` 由配置模板生成，非 `zh_cn` 版本同样由自动化流程生成。
- 文案面向用户，保持书面语，不写口语或语气词。
<<< END U007332 >>>
<<< UNIT U007333 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:58-58 | ctx=会话语言 >>>
审阅次数：11
## 会话语言
<<< END U007333 >>>
<<< UNIT U007334 | md-list | packages/akari-bot-core/akaribot/core/docs/i18n.md:60-63 | ctx=会话语言 >>>
审阅次数：11
- `BaseConfig.default_locale` 是全局默认语言，实例内可用 `~setup locale <lang>` 修改场景语言。
- 会话语言保存在 `TargetUnionInfo.locale`，`msg.t` 与 `I18NContext` 均依据该值解析。
- 语言文件缺失或键不存在时按 `fallback` 设置回退，并在回复中给出提示。
- `Locale.t_str(text)` 用于对已拼接的文本再次执行 key 替换，未匹配的内容原样保留。
<<< END U007334 >>>
<<< UNIT U007335 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:1-1 | ctx=核心运行时 >>>
审阅次数：11
# 核心运行时
<<< END U007335 >>>
<<< UNIT U007336 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:3-3 | ctx=核心运行时 >>>
审阅次数：11
本文阐明核心运行时的架构定位、运行时依赖与多进程拓扑模型，并提供相关文档导航。
<<< END U007336 >>>
<<< UNIT U007337 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:5-5 | ctx=核心运行时 >>>
审阅次数：11
`akaribot.core` 为 AkariBot 的核心运行时框架，负责提供公共 API 与底层基础设施，由 `akari-bot-core` 包提供。该包同时包含内置功能模块 `akaribot.modules.core`，相关说明参见[内置模块](../../modules/core/docs/index.md)。
<<< END U007337 >>>
<<< UNIT U007338 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:7-7 | ctx=定位 >>>
审阅次数：11
## 定位
<<< END U007338 >>>
<<< UNIT U007339 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:9-9 | ctx=定位 >>>
审阅次数：11
`akaribot.core` 提供守护进程入口、Server 进程、消息解析和会话模型，同时定义平台进程与 Server 共用的接口。包发现、配置、数据库、计划任务、JobQueue 和本地化数据均由该核心包管理。
<<< END U007339 >>>
<<< UNIT U007340 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:11-11 | ctx=定位 >>>
审阅次数：11
外部功能模块与平台适配器均通过标准公共 API 接入 core。模块导入 `akaribot.core.api`，适配器额外导入 `akaribot.core.api.adapters`。内置核心模块同样严格遵循该分层调用规范。
<<< END U007340 >>>
<<< UNIT U007341 | md-list | packages/akari-bot-core/akaribot/core/docs/index.md:13-16 | ctx=定位 >>>
审阅次数：11
- `akaribot`、`akaribot.modules`、`akaribot.adapters` 属于 [PEP 420](https://peps.python.org/pep-0420/) 命名空间目录，不包含 `__init__.py`。
- `akaribot.core` 是常规包。
- `CORE_API_VERSION` 定义公共 API 的版本号，运行时通过 `__api_version__` 导出该版本号。
- 模块包在 `manifest.toml` 的 `requires_core_api` 中声明支持的版本范围。
<<< END U007341 >>>
<<< UNIT U007342 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:18-18 | ctx=依赖关系 >>>
审阅次数：11
## 依赖关系
<<< END U007342 >>>
<<< UNIT U007343 | md-table | packages/akari-bot-core/akaribot/core/docs/index.md:20-27 | ctx=依赖关系 >>>
审阅次数：11
| 依赖 | 用途 |
| --- | --- |
| `akari-bot-i18n` | `Locale`、文案快照与术语校验 |
| `akari-bot-webrender` | 网页与元素截图渲染 |
| `tortoise-orm` | ORM、连接管理与迁移执行 |
| `APScheduler` | 模块与核心计划任务 |
| `fastapi`、`uvicorn` | 内置 WebSocket Hub 与 HTTP 服务 |
| `httpx`、`httpx-ws` | 出站请求与 WebSocket 客户端 |
<<< END U007343 >>>
<<< UNIT U007344 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:29-29 | ctx=依赖关系 >>>
审阅次数：11
可选依赖以 extra 提供：
<<< END U007344 >>>
<<< UNIT U007345 | md-table | packages/akari-bot-core/akaribot/core/docs/index.md:31-36 | ctx=依赖关系 >>>
审阅次数：11
| extra | 内容 |
| --- | --- |
| `s3` | `boto3`，对象存储 |
| `mysql` | `asyncmy` 驱动 |
| `image`、`chart` | `matplotlib`，统计图表 |
| `full` | 上述三项以及品牌与表情资源包 |
<<< END U007345 >>>
<<< UNIT U007346 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:38-38 | ctx=进程模型概览 >>>
审阅次数：11
## 进程模型概览
<<< END U007346 >>>
<<< UNIT U007347 | md-table | packages/akari-bot-core/akaribot/core/docs/index.md:40-46 | ctx=进程模型概览 >>>
审阅次数：11
| 进程 | 职责 |
| --- | --- |
| BotDaemon | 获取防止实例重复启动的锁文件，执行 pre-init，启动并监控子进程 |
| pre-init | 唯一可写入配置的进程，补充缺失的配置项、创建数据表、执行迁移 |
| 平台进程 | 对应每个适配器实例，持有平台 SDK 与上下文 |
| Server | 解析消息、执行模块、运行计划任务 |
| jobqueue-hub | WebSocket 后端的内置 Hub，可选 |
<<< END U007347 >>>
<<< UNIT U007348 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:48-48 | ctx=进程模型概览 >>>
审阅次数：11
实例根目录由 `AKARI_INSTANCE_DIR` 指定，未设置时使用进程的当前目录。配置目录可以通过 `AKARI_CONFIG_PATH` 单独指定。详情参见[架构](architecture.md)。
<<< END U007348 >>>
<<< UNIT U007349 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:50-50 | ctx=文档导航 >>>
审阅次数：11
## 文档导航
<<< END U007349 >>>
<<< UNIT U007350 | md-table | packages/akari-bot-core/akaribot/core/docs/index.md:52-67 | ctx=文档导航 >>>
审阅次数：11
| 页面 | 内容 |
| --- | --- |
| [架构](architecture.md) | 代码结构、进程拓扑、启动与重启、消息收发链路、计划任务 |
| [开发流程](development-workflow.md) | 环境、日常命令、检查项、代码风格、分支与提交、文档工具链 |
| [JobQueue](queue.md) | 后端选择、节点注册、RPC 与信号、超时与关闭 |
| [配置](config.md) | 配置模板、表布局、字段注释、只读约束 |
| [数据库](database.md) | 双连接、模型、union 数据、迁移 |
| [WebRender](webrender.md) | 渲染服务配置、运行模式、启动与降级 |
| [模块开发](module-development.md) | 模块、命令、权限、配置、hook、i18n |
| [消息 API](message-api.md) | `MessageSession`、等待接口、消息链与消息元素 |
| [权限](permissions.md) | 角色、模块与命令级权限、模块授权、机器人权限 |
| [适配器开发](adapter-development.md) | 适配器入口、特性声明、上下文管理器 |
| [公共 API](public-api.md) | 模块与适配器可依赖的公开 API 与版本要求 |
| [本地化](i18n.md) | `I18NContext`、语言文件与占位符规则 |
| [占位符](placeholders.md) | KE 码、I18N 标记、AT 码的语法与转义 |
| [常见问题](faq.md) | 帮助、模块启用、权限、更新、贡献与许可 |
<<< END U007350 >>>
<<< UNIT U007351 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:1-1 | ctx=消息 API 参考 >>>
审阅次数：11
# 消息 API 参考
<<< END U007351 >>>
<<< UNIT U007352 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:3-3 | ctx=消息 API 参考 >>>
审阅次数：11
本文列出模块处理函数可用的消息接口、消息链与消息元素。接口与参数均从 `akaribot.core.api` 导入，模块声明与命令模板的编写规范参见[模块开发](module-development.md)。
<<< END U007352 >>>
<<< UNIT U007353 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:5-5 | ctx=会话对象 >>>
审阅次数：11
## 会话对象
<<< END U007353 >>>
<<< UNIT U007354 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:7-7 | ctx=会话对象 >>>
审阅次数：11
模块处理函数接收 `Bot.MessageSession` 实例。该对象本身仅保存会话快照与当前解析状态，场景及用户相关字段均通过 `session_info` 读取（例如通过 `msg.session_info.bot_name` 获取机器人的本地化展示名称）。
<<< END U007354 >>>
<<< UNIT U007355 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:9-14 | ctx=会话对象 >>>
审阅次数：11
| 字段或属性 | 说明 |
| --- | --- |
| `session_info` | `SessionInfo` 快照。目标、发送者、平台能力、语言与权限均记录于该快照中 |
| `sent` / `trigger_msg` | 已发送消息链列表（默认空）。parser 处理后的触发文本 |
| `matched_msg` / `parsed_msg` | 正则或事件的匹配结果。命令参数解析结果，无模板模块可能为 `None` |
| `target` / `t` / `t_str` | `target` 已弃用，等价于 `session_info`。`t`、`t_str` 按会话语言翻译键或文本 |
<<< END U007355 >>>
<<< UNIT U007356 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:16-16 | ctx=会话对象 >>>
审阅次数：11
场景字段通过 `msg.session_info` 访问：
<<< END U007356 >>>
<<< UNIT U007357 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:18-26 | ctx=会话对象 >>>
审阅次数：11
| 字段 | 说明 |
| --- | --- |
| `target_id`、`target_from`、`client_name` | 场景 ID、场景来源与客户端名称 |
| `sender_id`、`sender_from`、`sender_name` | 发送者元数据（主动推送会话中可能为空） |
| `message_id`、`reply_id`、`messages`、`session_id`、`timestamp` | 触发消息、回复目标、原始消息链、会话 UUID 与时间戳 |
| `prefixes`、`muted`、`custom_admins`、`enabled_modules` | 可用命令前缀、禁止发言状态、自定义管理员 union ID 与已启用模块 |
| `locale`、`timezone_offset`、`display_timezone_offset`、`tmp` | `Locale` 对象（语言代码通过 `locale.locale` 获取）、场景与个人显示时区偏移（`timedelta`，未设置为 `None`）与临时字典 |
| `tz`、`display_tz`、`tz_label`、`display_tz_label` | 场景时区与展示时区（`tzinfo`）及其规范偏移字符串。展示时区未设置时跟随场景时区 |
| `bot_name`、`bot_id`、`is_private`、`fetch`、`support_*` | 本地化机器人名称与平台账号 ID，包含私聊标识、主动会话标识及各项平台能力标志 |
<<< END U007357 >>>
<<< UNIT U007358 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:28-28 | ctx=发送消息 >>>
审阅次数：11
## 发送消息
<<< END U007358 >>>
<<< UNIT U007359 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:30-35 | ctx=发送消息 >>>
审阅次数：11
| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `send_message()` | `message_chain`、`quote=True`、`disable_secret_check=False`、`callback=None`、`callback_id=None`、`callback_timeout=1800`、`callback_once=False` | 发送并返回 `FinishedSession` |
| `finish()` | 参数同 `send_message()`，`message_chain` 可省略 | 发送后抛出 `SessionFinished`。不传入消息链时仅结束会话 |
| `send_direct_message()` | `message_chain`、`disable_secret_check=False` | 提交后立即返回 `None`。消息 ID 由其他接口提供 |
| `send_private_message()` | `message_chain`、`user_id=None`、`disable_secret_check=False` | 私聊发送，返回消息 ID 列表。空列表表示失败 |
<<< END U007359 >>>
<<< UNIT U007360 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:37-37 | ctx=发送消息 >>>
审阅次数：11
`send_message()` 的 `callback` 回调函数在用户引用回复或点击交互按钮后触发执行，传入的回调参数为对应响应的 `MessageSession` 实例。
<<< END U007360 >>>
<<< UNIT U007361 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:39-39 | ctx=发送消息 >>>
审阅次数：11
`callback_id` 为按钮回调机制所使用的虚拟回复 ID，其生成与校验规则如下：
<<< END U007361 >>>
<<< UNIT U007362 | md-list | packages/akari-bot-core/akaribot/core/docs/message-api.md:41-42 | ctx=发送消息 >>>
审阅次数：11
- 省略 `callback_id` 时，框架会为缺少 `reply_id` 的按钮生成虚拟 ID。
- 消息中未包含交互按钮时，框架按实际消息 ID 绑定。
<<< END U007362 >>>
<<< UNIT U007363 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:44-44 | ctx=发送消息 >>>
审阅次数：11
`callback_timeout` 默认取值为 1800 秒。传入 `None` 表示不设置超时。`callback_once=True` 表示首次触发后失效。
<<< END U007363 >>>
<<< UNIT U007364 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:46-46 | ctx=发送消息 >>>
审阅次数：11
调用返回的 `FinishedSession` 对象包含已发送消息的 `message_id`。`delete()` 为异步方法，用于撤回或删除已投递的消息。当第三方平台未返回消息唯一标识时，`message_id` 将为空列表。
<<< END U007364 >>>
<<< UNIT U007365 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:59-59 | ctx=发送消息 >>>
审阅次数：11
发送路径默认执行 `MessageChain.is_safe` 的敏感信息扫描。检查未通过时，整条消息链将被替换为 `error.message.chain.unsafe`。仅在确认内容安全时，才允许传入 `disable_secret_check=True` 跳过检查。
<<< END U007365 >>>
<<< UNIT U007366 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:63-63 | ctx=等待用户输入 >>>
审阅次数：11
## 等待用户输入
<<< END U007366 >>>
<<< UNIT U007367 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:65-70 | ctx=等待用户输入 >>>
审阅次数：11
| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `wait_confirm()` | `message_chain=None`、`quote=True`、`delete=True`、`timeout=120`、`append_instruction=True`、`no_confirm_action=True`、`release_execution_lock=True`、`consume_any_message=False`、`confirm_token=None` | 等待确认，返回 `bool` |
| `wait_next_message()` | `message_chain=None`、`quote=True`、`delete=False`、`timeout=120`、`append_instruction=True` | 等待同一发送者的下一条消息 |
| `wait_reply()` | `message_chain`、`quote=True`、`delete=False`、`timeout=120`、`all_=False`、`append_instruction=True` | 等待对该消息的引用回复 |
| `wait_anyone()` | `message_chain=None`、`quote=False`、`delete=False`、`timeout=120` | 等待场景内任意成员的消息 |
<<< END U007367 >>>
<<< UNIT U007368 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:72-72 | ctx=等待用户输入 >>>
审阅次数：11
等待消息的方法均返回新的 `MessageSession` 实例，`wait_confirm()` 例外，仅返回 `bool`。
<<< END U007368 >>>
<<< UNIT U007369 | md-list | packages/akari-bot-core/akaribot/core/docs/message-api.md:74-81 | ctx=等待用户输入 >>>
审阅次数：11
- 默认超时 120 秒。传入 `None` 关闭超时。
- 超时、取消或无法获取结果时抛出 `WaitCancelException`。
- 等待期间默认释放执行锁。方法返回前重新获取该锁，获取失败按取消处理。
- `wait_confirm()` 在 `confirm_token` 非 `None` 时进入严格确认模式，必须原样回复该口令，才视为确认。普通模式接受 `confirm_command` 中的确认词。发送 `no` 返回 `False`。
- `consume_any_message=True` 时，任意消息都会结束等待，返回值仍按是否为确认词判断。
- 全局 `no_confirm` 开启时，直接返回 `no_confirm_action`。
- 平台不支持引用回复时，`wait_reply()` 改用 `wait_next_message()` 或 `wait_anyone()`，并以 `quote=False` 发送提示。`all_=True` 时接受任意成员的回复。
- `wait_next_message()` 与 `wait_anyone()` 匹配到的消息仍交给常规解析器（parser）处理。`wait_confirm()` 与 `wait_reply()` 会取走匹配到的消息，不再交给常规解析器（parser）处理。
<<< END U007369 >>>
<<< UNIT U007370 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:95-95 | ctx=等待用户输入 >>>
审阅次数：11
`WaitCancelException` 与 `SessionFinished` 均继承自 `BaseException`，无法通过 `except Exception` 捕获。
<<< END U007370 >>>
<<< UNIT U007371 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:99-99 | ctx=权限 >>>
审阅次数：11
## 权限
<<< END U007371 >>>
<<< UNIT U007372 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:101-105 | ctx=权限 >>>
审阅次数：11
| 方法 | 参数 | 说明 |
| --- | --- | --- |
| `check_super_user()` | 无，同步 | 发送者是否为超级用户 |
| `check_permission()` | 无，异步 | 自定义管理员或超级用户返回 `True`，否则检查平台原生权限 |
| `check_native_permission()` | `user_id=None`，异步 | 指定成员或发送者的平台原生管理员权限 |
<<< END U007372 >>>
<<< UNIT U007373 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:114-114 | ctx=其他操作 >>>
审阅次数：11
## 其他操作
<<< END U007373 >>>
<<< UNIT U007374 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:116-124 | ctx=其他操作 >>>
审阅次数：11
| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `as_display()` | `text_only=False`、`element_filter=None`、`connector="\n"` | 将触发消息序列化为文本字符串。`text_only=True` 仅保留 `PlainElement` 文本，非文本元素按 KE 码、AT 码等字符串表示 |
| `delete()` | `reason=None` | 删除触发消息 |
| `sleep()` / `hold()` / `release()` / `start_typing()` / `end_typing()` | `s` / 无 | 暂停并释放执行锁（恢复失败时抛出 `WaitCancelException`）。保持或释放平台上下文。开始或结束输入状态 |
| `format_time()` / `format_num()` | `timestamp`、`date=True`、`simple=False`、`time=True`、`seconds=True`、`timezone=True` / `number`、`precision=0` | 依据会话时区与语言环境格式化时间戳 / 依据语言规则缩放格式化数值（支持万、亿、兆或 k、M、G 计数制） |
| `call_onebot_api()` / `call_api()` | `api_name`、`**kwargs` | 将调用转发至 OneBot 扩展接口（`call_api()` 为已废弃接口）。若平台不支持该调用，将返回 `{"success": False, "error": ...}` |
| `restrict_member()` / `unrestrict_member()` | `user_id`、`duration=None`、`reason=None`、`wait=False` / `user_id`、`wait=False` | 执行禁言或解除禁言限制，当 `duration=None` 时代表永久禁言 |
| `kick_member()` / `ban_member()` / `unban_member()` | `user_id`、`reason=None`（`unban` 无 reason） | 移除、封禁或解除封禁群组成员 |
<<< END U007374 >>>
<<< UNIT U007375 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:126-126 | ctx=其他操作 >>>
审阅次数：11
`now()` 与 `today()` 按场景时区返回当前时间与日期，业务代码获取当前时间时应调用这两个方法。
<<< END U007375 >>>
<<< UNIT U007376 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:128-128 | ctx=其他操作 >>>
审阅次数：11
主动会话（`FetchedMessageSession`）不包含 `session_info.messages`。调用 `as_display()` 前，请先检查其是否为空。
<<< END U007376 >>>
<<< UNIT U007377 | md-list | packages/akari-bot-core/akaribot/core/docs/message-api.md:130-133 | ctx=其他操作 >>>
审阅次数：11
- `as_display()` 的 `text_only` 默认值为 `False`，`MessageChain.to_str()` 默认值为 `True`。
- `add_reaction()`、`remove_reaction()` 作用于触发消息。
- `grant_permission_group()`、`revoke_permission_group()` 管理平台权限组。
- `handle_error_signal()` 提交错误信号。
<<< END U007377 >>>
<<< UNIT U007378 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:143-143 | ctx=消息链 >>>
审阅次数：11
## 消息链
<<< END U007378 >>>
<<< UNIT U007379 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:145-153 | ctx=消息链 >>>
审阅次数：11
| 方法或属性 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `append()` / `insert()` / `remove()` | 元素或纯文本（`insert` 另有 `index`） | 追加与插入会将纯字符串转换为 `PlainElement`。`remove()` 按元素删除 |
| `extend()` / `copy()` | 另一条链或元素列表 / 无 | 原地拼接或复制 |
| `contains()` / `only()` | 元素类型或类型元组 | 是否包含某类元素、是否仅包含某类元素 |
<<< END U007379 >>>
<<< UNIT U007380 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:155-155 | ctx=消息链 >>>
审阅次数：11
`+` 运算符返回深拷贝元素后的全新消息链，`+=` 运算符执行原地追加修改。两者的右值操作数支持 `MessageChain`、元素列表或单一消息元素，不支持纯字符串。`in` 运算符仅用于匹配元素类型（例如 `PlainElement in chain`），若传入元素实例将抛出 `TypeError`。`MessageChain.assign()` 接收已有消息链时直接原样返回而不执行复制。若需要独立副本，请显式调用 `copy()`。
<<< END U007380 >>>
<<< UNIT U007381 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:164-164 | ctx=消息链 >>>
审阅次数：11
`PlatformMessageChain.assign()` 依据 `session_info.target_from` 选择平台对应的专属消息链，若缺少匹配键则回退至 `default` 项。`I18NMessageChain.assign()` 依据 `session_info.locale.locale` 语言标识选择对应的消息链，此类型消息链必须包含 `default` 回退项，否则抛出 `ValueError`。两类多态链均在发送管线中自动完成解析分发。
<<< END U007381 >>>
<<< UNIT U007382 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:166-166 | ctx=消息元素 >>>
审阅次数：11
## 消息元素
<<< END U007382 >>>
<<< UNIT U007383 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:168-178 | ctx=消息元素 >>>
审阅次数：11
| 构造器 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `Plain()` / `Markdown()` | `*texts`、`disable_joke=False`、`allow_parse=True` | 纯文本与 Markdown 文本。`allow_parse=False` 时不解析 KE 码与多语言标记 |
| `Image()` / `Audio()` / `Video()` | `path`、`headers=None`、`max_h=None`、`allow_split=True` / `path` | 本地路径、URL、Base64 或 PIL 图片。音频与视频 |
| `Embed()` / `EmbedField()` | `title=None`、`description=None`、`url=None`、`timestamp`（默认采用导入时时间）、`color=0x0091FF`、`image=None`、`thumbnail=None`、`author=None`、`footer=None`、`fields=None` / `name`、`value`、`inline=False` | 富文本卡片与字段 |
| `I18NContext()` | `key`、`fallback=True`、`locale_failed_prompt=True`、`disable_joke=False`、`**kwargs` | 按会话语言解析的文案 |
| `Mention()` | `user_id` | 提及用户，格式为平台前缀加用户 ID |
| `Url()` | `url`、`trusted=None`、`md_format=False`、`md_format_name=None` | 链接元素，受 URL 策略限制 |
| `FormattedTime()` | `timestamp`、`date=True`、`simple=False`、`time=True`、`seconds=True`、`timezone=True` | 按会话时区格式化的时间 |
| `ActionText()` | `text`、`show=None`、`reference=False`、`show_on_fallback=True`、`quote_on_fallback=False` | 可点击的命令文本 |
| `Button()` / `ButtonFrame()` | `show`、`value`、`reply_id=None`、`permission=OWNER`、`click_limit=1` / `rows` | 按钮与按钮区域 |
<<< END U007383 >>>
<<< UNIT U007384 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:191-191 | ctx=消息元素 >>>
审阅次数：11
`Plain`、`Image`、`Embed` 等名称绑定的是对应元素的 `assign` 类方法。类型判断使用 `PlainElement`、`ImageElement`、`EmbedElement` 等真实类。
<<< END U007384 >>>
<<< UNIT U007385 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:195-195 | ctx=消息节点与渲染 >>>
审阅次数：11
## 消息节点与渲染
<<< END U007385 >>>
<<< UNIT U007386 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:197-197 | ctx=消息节点与渲染 >>>
审阅次数：11
`MessageNodes.assign(values, name=None)` 将多条 `MessageChain` 组合封装为转发消息节点列表，省略 `name` 参数时将自动生成默认节点名称。`send_message()` 原生支持 `MessageNodes`。若当前平台未声明具备 `support_handle_message_nodes` 能力，框架将自动把消息节点合成渲染为图片后执行发送。
<<< END U007386 >>>
<<< UNIT U007387 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:208-208 | ctx=消息节点与渲染 >>>
审阅次数：11
发送路径会处理以下情况：
<<< END U007387 >>>
<<< UNIT U007388 | md-list | packages/akari-bot-core/akaribot/core/docs/message-api.md:210-212 | ctx=消息节点与渲染 >>>
审阅次数：11
- `I18NContext` 按会话语言解析。`Markdown` 在平台不支持 `support_markdown` 时转为纯文本。
- 若目标平台未声明 `support_embed` 能力，`Embed` 富文本卡片将降级为图文混排输出。若未声明 `support_action_text`，`ActionText` 将转换为常规纯文本。若未声明 `support_button`，`Button` 与 `ButtonFrame` 将被安全过滤丢弃。
- 空消息链将被替换为 `error.message.chain.empty`。未通过 `is_safe` 检查的整条消息链将被替换为 `error.message.chain.unsafe`，发送时传入 `disable_secret_check=True` 的情况除外。
<<< END U007388 >>>
