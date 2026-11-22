# 全仓可读文本审核稿 · 第 10 册 / 共 20 册

覆盖 U007036–U007388，11 个文件、353 个单元、35,373 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
# 新建 union ID 的域前缀。升级与转换脚本会将旧数据的平台 ID 直接沿用为 union ID，
# 加上前缀后新生成的 ID 不会与平台 ID 混淆，并可直接区分账号组与场景组。
<<< END U007036 >>>
<<< UNIT U007037 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:36-37 >>>
# Union 的绑定、合并、删除与更新属同一 mutation 域，共用一把进程内锁。
# MySQL 路径仍在事务内锁定核心行，覆盖 Web 与 Server 分属进程的情况。
<<< END U007037 >>>
<<< UNIT U007038 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:195-196 >>>
# 删除与重建之间若中断，绑定数据将全部丢失，因此置于同一个事务内。
# 模块表可能关联在 local 连接上，事务须与表所在的连接一致，不能一律使用 default。
<<< END U007038 >>>
<<< UNIT U007039 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:222-223 >>>
# 调用方位于 Union mutation 事务中。锁定权限列表所属的 Target 行，避免 Web 与 Server
# 分属不同进程时，一边改写 Union 引用、一边添加管理员而互相覆盖整份 JSON 列表。
<<< END U007039 >>>
<<< UNIT U007040 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:263-264 >>>
# iter_union_models 已按 union_scope 过滤，此处取到的必然是同域的表，
# 不会把场景 ID 误当作用户 ID 创建记录。
<<< END U007040 >>>
<<< UNIT U007041 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:284-284 >>>
# 子类中作为主键的平台 ID 列名，供按域泛化的查询与补充创建逻辑使用
<<< END U007041 >>>
<<< UNIT U007042 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:381-381 >>>
# 所属 union 域（``sender`` / ``target``）
<<< END U007042 >>>
<<< UNIT U007043 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:383-383 >>>
# 配套的 ID 映射表
<<< END U007043 >>>
<<< UNIT U007044 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:386-387 >>>
# 由 resolve_union() 附加的映射行，非数据库字段。
# 未经解析直接查询（如 all() / filter()）得到的实例上为 None。
<<< END U007044 >>>
<<< UNIT U007045 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:391-392 >>>
# 封禁状态只此一处。union 下的全部平台 ID 共享此行，因而封禁天然对组内所有 ID 生效，
# 映射行无需重复保存标记，否则会产生组状态与单个 ID 状态不一致的问题。
<<< END U007045 >>>
<<< UNIT U007046 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:421-421 >>>
# 只有缺失或损坏的映射路径才进入 mutation 域。正常消息解析仍是无锁查询。
<<< END U007046 >>>
<<< UNIT U007047 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:425-425 >>>
# 自动兼容处理，允许存在 union_id 与平台 ID 相同、但缺少映射行的历史数据。
<<< END U007047 >>>
<<< UNIT U007048 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:451-451 >>>
# 从平台 ID 字符串或会话对象解析出 union 信息，供按会话获取记录的入口复用。
<<< END U007048 >>>
<<< UNIT U007049 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:635-636 >>>
# 创建新组、重新关联映射和继承场景限制名单必须原子完成。否则最后一步失败会留下
# 一个孤立的新 union，并使账号已经脱离原组但尚未继承全部处罚状态。
<<< END U007049 >>>
<<< UNIT U007050 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:650-651 >>>
# 先创建新组再重新关联映射行，全程不出现“账号没有映射行”的中间态。
# union_id 不是主键，可通过单条 UPDATE 重新关联。
<<< END U007050 >>>
<<< UNIT U007051 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:676-677 >>>
# 合并会同时改写核心表、平台映射、权限引用与若干模块表。任一步失败都必须整体回滚，
# 否则会留下新旧 union 并存或只有部分模块数据迁移的不可恢复状态。
<<< END U007051 >>>
<<< UNIT U007052 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:704-704 >>>
# 先按冲突取舍将两侧模块数据合并至一处，再整体重新关联到新组。新组为空，第二步不会再产生冲突。
<<< END U007052 >>>
<<< UNIT U007053 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:845-846 >>>
# Union 事务统一先锁定核心行、再锁定映射行，反序会在 MySQL 下形成循环死锁。
# 锁定核心行后必须重新读取映射并验证其未被重新关联。
<<< END U007053 >>>
<<< UNIT U007054 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:934-935 >>>
# MySQL 下锁定 union 数据行，使不同 server 进程也不能同时从相同最大通道号分配。
# SQLite 会忽略行锁语义，由外层 asyncio.Lock 保证单 server 进程内的顺序。
<<< END U007054 >>>
<<< UNIT U007055 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:967-967 >>>
# 新组、平台映射和互认记录属于同一次解绑。任一步失败均不能让数据库停在半迁移状态。
<<< END U007055 >>>
<<< UNIT U007056 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:982-982 >>>
# 封禁状态随场景一并转移，避免通过解绑规避处罚。
<<< END U007056 >>>
<<< UNIT U007057 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:989-990 >>>
# 先创建新组再重新关联映射行，全程不出现“场景没有映射行”的中间态。
# 新组仅含该场景，通道编号复位为 1。
<<< END U007057 >>>
<<< UNIT U007058 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1005-1006 >>>
# 拆出的场景与原组内的机器人不再对应同一个现实场景，互认记录须一并清除。
# 新组的 target_data 本为空，只需清理保留的一侧。调用内部版本避免重复进入全局锁。
<<< END U007058 >>>
<<< UNIT U007059 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1037-1038 >>>
# bots_id 为两级结构，随 target_data 浅合并会使 other 一侧的互认记录被整体覆盖，
# 因此单独取并集。
<<< END U007059 >>>
<<< UNIT U007060 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1059-1059 >>>
# 先按冲突取舍将两侧模块数据合并至一处，再整体重新关联到新组。新组为空，第二步不会再产生冲突。
<<< END U007060 >>>
<<< UNIT U007061 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1070-1071 >>>
# 自身一侧通道号不变，并入方整体平移，不得逐条分配新号。
# 平移须按原通道号建立映射，以保持并入方内部原本同号的场景同号。
<<< END U007061 >>>
<<< UNIT U007062 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1308-1308 >>>
# 统计命令按时间区间反复聚合，无索引时每次都是全表扫描
<<< END U007062 >>>
<<< UNIT U007063 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1529-1530 >>>
# 每个进程每 100 毫秒按这两列轮询一次，无索引时开销随表内行数线性增长
# status / timestamp 索引用于低成本回收调用方异常退出后遗留的终态记录
<<< END U007063 >>>
<<< UNIT U007064 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1577-1578 >>>
# 定时清理只删除已进入终态且超过保留期的任务。pending / processing 最长可执行两小时，
# 若沿用无条件删除，它们会在等待方和执行方自己的超时机制生效前一小时就消失。
<<< END U007064 >>>
<<< UNIT U007065 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1581-1582 >>>
# 超过全局执行上限的活动任务已不可能合法完成，无需响应的任务直接删除，
# 等待型任务先标 timeout 供轮询取得终态。终态删除须在本步之前完成。
<<< END U007065 >>>
<<< UNIT U007066 | py-comment | packages/akari-bot-core/akaribot/core/database/models.py:1601-1602 >>>
# 不附加排序，现有 (target_peer, status) 索引可在达到 limit 后停止扫描。
# JobQueue 本身不承诺严格 FIFO，避免为候选批次对全部积压记录建立临时排序表。
<<< END U007066 >>>
<<< UNIT U007067 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:43-43 | ctx=union_mutation >>>
串行执行一段 Union 状态变更。调用方不得在内部再次进入本上下文。
<<< END U007067 >>>
<<< UNIT U007068 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:49-49 | ctx=UnionDeleteBlocked >>>
Union 仍被模块记录引用，须先解除外部状态才能删除。
<<< END U007068 >>>
<<< UNIT U007069 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:71-71 | ctx=get_table_name >>>
获取模型对应的数据表名。
<<< END U007069 >>>
<<< UNIT U007070 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:77-77 | ctx=get_union_module_name >>>
获取模块表所属的模块名，用于向用户展示，无法判断时回退到表名。
<<< END U007070 >>>
<<< UNIT U007071 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:138-138 | ctx=migrate_union_references >>>
迁移显式声明协议的模块 Union 引用。
<<< END U007071 >>>
<<< UNIT U007072 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:165-171 | ctx=collect_union_conflicts >>>
列出两个 union 在模块表上互相冲突（双方都有数据）的模型。

:param from_union: 来源 union ID。
:param to_union: 目标 union ID。
:param scope: 限定 union 域。
<<< END U007072 >>>
<<< UNIT U007073 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:259-259 | ctx=backfill_union_binds >>>
为缺少映射行的 union 补充创建 ID 映射。
<<< END U007073 >>>
<<< UNIT U007074 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:295-295 | ctx=UnionBind.list_ids >>>
列出绑定到给定 union ID 的平台账号。
<<< END U007074 >>>
<<< UNIT U007075 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:300-304 | ctx=SenderUnionBind >>>
用户 ID 与 union 的映射关系。

:param sender_id: 用户 ID（平台账号）。
<<< END U007075 >>>
<<< UNIT U007076 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:315-321 | ctx=TargetUnionBind >>>
场景 ID 与 union 的映射关系。

:param target_id: 场景 ID。
:param channel_id: 所属消息通道编号，同组内同号的场景被视为同一个现实场景。
:param push_priority: 主动推送优先级，数值越大越优先。
<<< END U007076 >>>
<<< UNIT U007077 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:343-347 | ctx=TargetUnionBind.list_channels >>>
获取该 union 下“平台场景 ID → 消息通道编号”的映射。

:param union_id: 场景 union ID。
<<< END U007077 >>>
<<< UNIT U007078 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:408-408 | ctx=UnionInfo.resolve_union >>>
按平台账号查找 union 记录，缺失时按需创建。
<<< END U007078 >>>
<<< UNIT U007079 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:438-438 | ctx=UnionInfo.list_bound_ids >>>
列出该 union 记录绑定的平台账号。
<<< END U007079 >>>
<<< UNIT U007080 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:462-462 | ctx=UnionInfo.edit_attr >>>
修改 union 记录中除主键外的指定字段。
<<< END U007080 >>>
<<< UNIT U007081 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:473-473 | ctx=UnionInfo.delete_union >>>
删除 union 记录及其关联的映射和会话数据。
<<< END U007081 >>>
<<< UNIT U007082 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:527-530 | ctx=SenderUnionInfo.get_by_sender_id >>>
获取平台账号所属的 union 行，是 :meth:`UnionInfo.resolve_union` 的会话友好包装，
额外接受 MessageSession / FetchedMessageSession，从中取出 ``sender_id``。
<<< END U007082 >>>
<<< UNIT U007083 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:534-539 | ctx=SenderUnionInfo.switch_identity >>>
修改用户身份。

:param trust: 是否为白名单模式，若 False 则为黑名单模式。
:param enable: 是否要加入身份，若 False 则取消身份。
<<< END U007083 >>>
<<< UNIT U007084 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:554-558 | ctx=SenderUnionInfo.warn_user >>>
警告用户。

:param amount: 警告用户次数。
<<< END U007084 >>>
<<< UNIT U007085 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:568-572 | ctx=SenderUnionInfo.modify_petal >>>
修改用户花瓣数量。

:param amount: 要添加或减少的花瓣数量。
<<< END U007085 >>>
<<< UNIT U007086 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:582-582 | ctx=SenderUnionInfo.clear_petal >>>
清空用户花瓣数量。
<<< END U007086 >>>
<<< UNIT U007087 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:586-591 | ctx=SenderUnionInfo.edit_sender_data >>>
设置用户数据。

:param key: 键名。
:param value: 值，若留空则删除该键值对。
<<< END U007087 >>>
<<< UNIT U007088 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:611-616 | ctx=SenderUnionInfo.bind_id >>>
将一个平台账号绑定到该 union。

:param sender_id: 平台账号 ID。
:return: 是否绑定成功，若该账号已绑定至其他 union 则为 False。
<<< END U007088 >>>
<<< UNIT U007089 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:761-764 | ctx=TargetUnionInfo.get_by_target_id >>>
获取平台场景所属的 union 行，是 :meth:`UnionInfo.resolve_union` 的会话友好包装，
额外接受 MessageSession / FetchedMessageSession，从中取出 ``target_id``。
<<< END U007089 >>>
<<< UNIT U007090 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:768-772 | ctx=TargetUnionInfo.list_peer_bots >>>
获取某个平台场景视角下、同一个现实场景里其他机器人的账号。

:param target_id: 观察方的平台场景 ID。
<<< END U007090 >>>
<<< UNIT U007091 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:792-796 | ctx=TargetUnionInfo.link_peer_bots >>>
记录机器人互认关系。

:param links: ``{观察方场景 ID: {对端场景 ID: 对端机器人在观察方平台的账号}}``。
<<< END U007091 >>>
<<< UNIT U007092 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:926-931 | ctx=TargetUnionInfo.bind_id >>>
将一个平台场景绑定到该 union。

:param target_id: 平台场景 ID。
:return: 是否绑定成功，若该场景已绑定至其他 union 则为 False。
<<< END U007092 >>>
<<< UNIT U007093 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:960-965 | ctx=TargetUnionInfo.unbind_id >>>
将一个平台场景从该 union 中拆出，数据留在原 union，该场景从零开始。

:param target_id: 平台场景 ID。
:return: 拆出后该场景所属的新 union，若无法解绑则为 None。
<<< END U007093 >>>
<<< UNIT U007094 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1092-1097 | ctx=TargetUnionInfo.config_module >>>
设置场景内可用模块。

:param module_name: 指定的模块名称。
:param enable: 是否要开启模块，若 False 则关闭模块。
<<< END U007094 >>>
<<< UNIT U007095 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1118-1122 | ctx=TargetUnionInfo.switch_mute >>>
切换是否在场景中禁用机器人。

:return: 机器人是否被禁用。
<<< END U007095 >>>
<<< UNIT U007096 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1136-1141 | ctx=TargetUnionInfo.edit_target_data >>>
设置场景数据。

:param key: 键名。
:param value: 值，若留空则删除该键值对。
<<< END U007096 >>>
<<< UNIT U007097 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1161-1166 | ctx=TargetUnionInfo.config_custom_admin >>>
设置场景内管理员。

:param sender_union_id: 指定的用户 union ID。
:param enable: 是否要设置用户为场景内管理员，若 False 则移除管理员。
<<< END U007097 >>>
<<< UNIT U007098 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1193-1198 | ctx=TargetUnionInfo.config_banned_user >>>
设置场景内被限制用户。

:param sender_union_id: 指定的用户 union ID。
:param enable: 是否要设置场景内用户限制使用机器人，若 False 则取消限制。
<<< END U007098 >>>
<<< UNIT U007099 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1228-1234 | ctx=TargetUnionInfo.get_target_list_by_module >>>
获取开启此模块的所有场景列表。

:param module_name: 指定的模块名称。
:param id_prefix: 指定的 ID 前缀，按 union 下绑定的平台场景 ID 匹配。
:return: 符合要求的场景 union 列表。
<<< END U007099 >>>
<<< UNIT U007100 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1272-1277 | ctx=StoredData >>>
数据存储。

:param stored_key: 存储键。
:param value: 值。
<<< END U007100 >>>
<<< UNIT U007101 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1287-1298 | ctx=AnalyticsData >>>
统计数据。

:param module_name: 模块名称。
:param module_type: 模块类型。
:param target_id: 场景 ID。
:param sender_id: 用户 ID。
:param target_union_id: 场景所属 union ID。
:param sender_union_id: 用户所属 union ID。
:param command: 命令。
:param timestamp: 时间戳。
<<< END U007101 >>>
<<< UNIT U007102 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1316-1316 | ctx=AnalyticsData.get_data_by_times >>>
按时间范围获取统计数据。
<<< END U007102 >>>
<<< UNIT U007103 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1324-1324 | ctx=AnalyticsData.get_values_by_times >>>
按时间范围获取数值。
<<< END U007103 >>>
<<< UNIT U007104 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1332-1332 | ctx=AnalyticsData.get_count_by_times >>>
按时间范围统计数量。
<<< END U007104 >>>
<<< UNIT U007105 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1340-1340 | ctx=AnalyticsData.get_modules_count >>>
返回按模块统计的数量。
<<< END U007105 >>>
<<< UNIT U007106 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1363-1368 | ctx=ModuleStatus >>>
模块状态。

:param module_name: 模块名称。
:param load: 是否已加载。
<<< END U007106 >>>
<<< UNIT U007107 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1378-1378 | ctx=ModuleStatus.init_modules >>>
初始化模块状态记录。
<<< END U007107 >>>
<<< UNIT U007108 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1401-1401 | ctx=ModuleStatus.set_module_loaded >>>
设置模块的加载状态。
<<< END U007108 >>>
<<< UNIT U007109 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1411-1411 | ctx=ModuleStatus.get_all_modules >>>
返回全部模块状态。
<<< END U007109 >>>
<<< UNIT U007110 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1416-1416 | ctx=ModuleStatus.get_loaded_modules >>>
返回已加载的模块。
<<< END U007110 >>>
<<< UNIT U007111 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1421-1421 | ctx=ModuleStatus.get_unloaded_modules >>>
返回未加载的模块。
<<< END U007111 >>>
<<< UNIT U007112 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1426-1430 | ctx=DBVersion >>>
数据库版本。

:param version: 数据库版本号。
<<< END U007112 >>>
<<< UNIT U007113 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1439-1449 | ctx=UnfriendlyActionRecords >>>
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
任务队列表。

:param task_id: 任务 ID。
:param target_peer: 目标进程实例或 service。
:param expects_response: 调用方是否等待终态结果。
:param action: 动作。
:param args: 参数。
:param status: 任务状态。
:param result: 任务结果。
:param timestamp: 时间戳。
<<< END U007114 >>>
<<< UNIT U007115 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1535-1535 | ctx=JobQueuesTable.add_task >>>
加入任务。
<<< END U007115 >>>
<<< UNIT U007116 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1541-1541 | ctx=JobQueuesTable.set_val >>>
设置任务值。
<<< END U007116 >>>
<<< UNIT U007117 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1548-1548 | ctx=JobQueuesTable.set_status >>>
设置任务状态。
<<< END U007117 >>>
<<< UNIT U007118 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1554-1554 | ctx=JobQueuesTable.claim >>>
原子地将 pending 任务认领为 processing。
<<< END U007118 >>>
<<< UNIT U007119 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1568-1568 | ctx=JobQueuesTable.clear_task >>>
删除任务。
<<< END U007119 >>>
<<< UNIT U007120 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1591-1591 | ctx=JobQueuesTable.get_first >>>
返回第一个任务。
<<< END U007120 >>>
<<< UNIT U007121 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1598-1598 | ctx=JobQueuesTable.get_all >>>
返回全部任务。
<<< END U007121 >>>
<<< UNIT U007122 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1610-1610 | ctx=JobQueuePeersTable >>>
JobQueue 进程注册表。租约是在线状态的唯一事实来源。
<<< END U007122 >>>
<<< UNIT U007123 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1633-1640 | ctx=MaliciousLoginRecords >>>
恶意登录行为记录。

:param id: 记录 ID。
:param ip_address: IP 地址。
:param blocked_until: 被封禁的截止时间。
:param created_date: 创建日期。
<<< END U007123 >>>
<<< UNIT U007124 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1652-1652 | ctx=MaliciousLoginRecords.check_blocked >>>
检查登录来源是否被阻止。
<<< END U007124 >>>
<<< UNIT U007125 | py-docstring | packages/akari-bot-core/akaribot/core/database/models.py:1657-1668 | ctx=SchemaMigration >>>
已应用的数据库迁移记录。

每个包的每条 revision 在此各记一行，取代全局唯一的数据库版本号。MySQL 的 DDL 会自动
提交，无法把“执行 DDL”与“写入版本记录”放入同一事务，因此判断某条 revision 是否已应用
只看本表，迁移必须自行保证可重复执行。

:param package: 包名，``core`` 或其他包名。
:param revision: revision 标识符。
:param applied_at: 应用时间。
:param checksum: 迁移文件源码的 sha256，用于发现已应用的迁移被改写。
<<< END U007125 >>>
<<< UNIT U007126 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:1-1 | ctx=适配器开发 >>>
# 适配器开发
<<< END U007126 >>>
<<< UNIT U007127 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:3-3 | ctx=适配器开发 >>>
本文介绍适配器的包结构、能力声明与平台入口。
<<< END U007127 >>>
<<< UNIT U007128 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:5-5 | ctx=适配器开发 >>>
适配器连接平台与 core。它接收平台消息，转换成 core 的会话对象后交给 Server 处理。适配器还会把 core 发出的消息和操作交给平台 SDK 执行。
<<< END U007128 >>>
<<< UNIT U007129 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:7-7 | ctx=适配器开发 >>>
适配器在 `pyproject.toml` 的 `akaribot.adapters` 分组中写入平台键与包路径的对应关系。目录名使用平台键。
<<< END U007129 >>>
<<< UNIT U007130 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:9-9 | ctx=包结构 >>>
## 包结构
<<< END U007130 >>>
<<< UNIT U007131 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:28-28 | ctx=包结构 >>>
`manifest.toml` 用 `config_table = "bot_telegram"` 指向 `config.py` 中的配置表。`credential_fields = ["telegram_token"]` 列出登录字段。启动实例前，守护进程会读取这两个字段，再检查同一平台的多个实例是否使用了相同的账号或令牌。
<<< END U007131 >>>
<<< UNIT U007132 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:45-45 | ctx=info.py >>>
`platform_name` 是平台展示名，`client_name` 由它生成，多实例时带实例后缀（如 `Telegram-alt`）。两个前缀列表传给 `client_init()`，由它校验会话 ID 并建立平台路由。
<<< END U007132 >>>
<<< UNIT U007133 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:47-47 | ctx=info.py >>>
守护进程会在导入适配器之前设置 `instance_id`。`bot_<平台>.toml` 中 `enable` 的值为 `true` 时，守护进程启动该实例。
<<< END U007133 >>>
<<< UNIT U007134 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:49-49 | ctx=多实例 >>>
## 多实例
<<< END U007134 >>>
<<< UNIT U007135 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:51-51 | ctx=多实例 >>>
同一适配器可以启动多个实例。实例 ID 匹配 `[a-z0-9_]{1,24}`，配置表名为 `bot_<平台>-<实例ID>`，例如 `bot_telegram-alt`。
<<< END U007135 >>>
<<< UNIT U007136 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:53-53 | ctx=多实例 >>>
有实例 ID 时，`Info.resolve_client_name(platform_name)` 返回 `平台-实例ID`（例如 `Telegram-alt`）。`platform_name` 本身不变。
<<< END U007136 >>>
<<< UNIT U007137 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:55-55 | ctx=多实例 >>>
实例表控制实例是否启用，平台基础表保存该平台的默认配置。
<<< END U007137 >>>
<<< UNIT U007138 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:57-57 | ctx=多实例 >>>
启动实例前，守护进程会读取 `manifest.toml` 的 `credential_fields`，并检查同一平台其他实例的登录信息和监听端口。
<<< END U007138 >>>
<<< UNIT U007139 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:59-59 | ctx=多实例 >>>
如果同一平台已有相同的登录信息或监听端口，守护进程会提示冲突，并拒绝启动该实例。
<<< END U007139 >>>
<<< UNIT U007140 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:61-61 | ctx=能力声明 >>>
## 能力声明
<<< END U007140 >>>
<<< UNIT U007141 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:63-63 | ctx=能力声明 >>>
在 `features.py` 中创建 `Features` 实例，`ContextManager` 用类属性引用它：
<<< END U007141 >>>
<<< UNIT U007142 | md-table | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:71-76 | ctx=能力声明 >>>
| 分组 | 字段 |
| --- | --- |
| 媒体与格式 | `support_image`、`support_audio`、`support_video`、`support_markdown`、`support_markdown_extension`、`support_embed` |
| 交互 | `support_mention`、`support_reaction`、`support_quote`、`support_typing`、`support_wait`、`support_action_text`、`support_button` |
| 管理 | `support_delete`、`support_manage`、`support_permission_group` |
| 消息范围与开关 | `read_all_messages`、`support_rss`、`support_handle_message_nodes`、`require_enable_modules`、`require_check_dirty_words` |
<<< END U007142 >>>
<<< UNIT U007143 | md-list | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:78-83 | ctx=能力声明 >>>
- `client_init()` 注册节点时，把这些能力标志写入 `capabilities`。
- `Module.unsupported_reason()` 根据 `read_all_messages` 和 `support_rss`，判断正则、事件、RSS 模块在当前会话中是否可用。
- `check_bot_state()` 返回 `BotState`。
- `can_*` 字段记录机器人能否执行对应操作，`permissions` 保存平台返回的权限。
- 检查结果写入 `SessionInfo`。
- `Module.unsupported_bot_permissions()` 读取这份结果，检查模块要求的权限。机器人缺少模块要求的权限时，这个模块不会启用。
<<< END U007143 >>>
<<< UNIT U007144 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:85-85 | ctx=平台入口 >>>
## 平台入口
<<< END U007144 >>>
<<< UNIT U007145 | md-list | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:104-106 | ctx=平台入口 >>>
- `Bot.register_bot()` 设置 `PrivateData` 目录与 `Info.client_name`。`register_context_manager()` 返回 `ctx_slot`，构造 `SessionInfo` 时要把 `ctx_slot` 一并填入。`fetch_session=True` 的管理器用于主动抓取会话。
- 收到消息时构造 `SessionInfo`（场景、发送者、`message_id`、`reply_id`、`messages`、`ctx_slot`、`bot_id`），再调用 `Bot.process_message(session, ctx)`。平台事件用 `EventInfo.assign(...)` 与 `Bot.process_event()` 投递。
- `client_init()` 初始化数据库连接（可选 `load_module_db=True`）、连接语言快照并注册节点。`client_cleanup()` 取消轮询、释放上下文并关闭连接。
<<< END U007145 >>>
<<< UNIT U007146 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:110-110 | ctx=ContextManager >>>
`ContextManager` 以类属性保存 `session_id` 到平台上下文的映射：
<<< END U007146 >>>
<<< UNIT U007147 | md-list | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:112-114 | ctx=ContextManager >>>
- `add_context()`、`del_context()` 添加与移除上下文。
- `activate_context()`、`deactivate_context()` 标记入站消息的处理区间，在这个区间内不删除上下文。
- `hold_context()`、`release_context()` 跨消息保持上下文，支持嵌套。
<<< END U007147 >>>
<<< UNIT U007148 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:116-116 | ctx=ContextManager >>>
须实现的抽象方法：
<<< END U007148 >>>
<<< UNIT U007149 | md-table | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:118-124 | ctx=ContextManager >>>
| 方法 | 用途 |
| --- | --- |
| `check_native_permission()`、`check_bot_state()` | 平台原生管理员与机器人权限快照 |
| `send_message()`、`send_private_msg()`、`derive_private_session()` | 发送、私聊与创建私聊会话 |
| `delete_message()`、`restrict_member()`、`unrestrict_member()`、`kick_member()` | 删除、禁言、解除与移除 |
| `ban_member()`、`unban_member()`、`grant_permission_group()`、`revoke_permission_group()` | 封禁与权限组 |
| `add_reaction()`、`remove_reaction()`、`error_signal()`、`start_typing()`、`end_typing()` | 表情、错误提示与输入状态 |
<<< END U007149 >>>
<<< UNIT U007150 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:126-126 | ctx=ContextManager >>>
这些方法由 `PlatformAPI` 的 `context_method()` 自动绑定。Server 跨进程调用时，会按 `SessionInfo` 选择上下文管理器。平台扩展接口由 `PlatformAPI` 声明，再由适配器绑定实现。
<<< END U007150 >>>
<<< UNIT U007151 | md-heading | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:128-128 | ctx=配置与本地化 >>>
## 配置与本地化
<<< END U007151 >>>
<<< UNIT U007152 | md-list | packages/akari-bot-core/akaribot/core/docs/adapter-development.md:130-133 | ctx=配置与本地化 >>>
- 适配器配置用 `@on_bot_config("<平台>")` 声明，表名是 `bot_<平台>`。
- 密钥写入 `[bot_<平台>_secret]`。
- 字段注释写成 `config.comments.bot_<平台>.<字段名>`。密钥表的配置注释要带 `_secret` 后缀。
- 面向用户的文案只在适配器包的 `locales/zh_cn.json` 中创建，具体见[配置](config.md)与[本地化](i18n.md)。
<<< END U007152 >>>
<<< UNIT U007153 | md-heading | packages/akari-bot-core/akaribot/core/docs/api-reference.md:8-8 | ctx=API 导出索引 >>>
# API 导出索引
<<< END U007153 >>>
<<< UNIT U007154 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/api-reference.md:10-10 | ctx=API 导出索引 >>>
本页按模块列出 `akaribot.core.api` 与 `akaribot.core.api.adapters` 的全部公开导出。类的方法、函数签名、参数类型、默认值和说明由构建过程读取源码生成，不在页面里手写。
<<< END U007154 >>>
<<< UNIT U007155 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/api-reference.md:12-12 | ctx=API 导出索引 >>>
如果某个参数在 docstring 里没有写明用途，清单只显示名称和类型。
<<< END U007155 >>>
<<< UNIT U007156 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:1-1 | ctx=架构 >>>
# 架构
<<< END U007156 >>>
<<< UNIT U007157 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:3-3 | ctx=架构 >>>
本文介绍 AkariBot 实例的内部结构。
<<< END U007157 >>>
<<< UNIT U007158 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:5-5 | ctx=介绍 >>>
## 介绍
<<< END U007158 >>>
<<< UNIT U007159 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:7-7 | ctx=介绍 >>>
AkariBot 的代码按包拆分。core 提供运行时和公共设施。内置模块、外部模块、平台适配器分别打包。
<<< END U007159 >>>
<<< UNIT U007160 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:9-9 | ctx=介绍 >>>
实例启动时，守护进程负责启动并监控子进程。这些子进程分别负责配置初始化、平台连接、消息处理与计划任务。
<<< END U007160 >>>
<<< UNIT U007161 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:11-11 | ctx=代码结构 >>>
## 代码结构
<<< END U007161 >>>
<<< UNIT U007162 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:24-24 | ctx=代码结构 >>>
补充说明：
<<< END U007162 >>>
<<< UNIT U007163 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:26-28 | ctx=代码结构 >>>
- `akaribot`、`akaribot.modules`、`akaribot.adapters`、`akaribot.assets` 是 PEP 420 命名空间目录，不带 `__init__.py`。查找包时以 `pyproject.toml` 中声明的入口为准，只有入口缺失时才扫描目录。
- 执行 `akaribot <子命令>` 时，命令行工具（CLI）通过子进程调用 `python -m akaribot.core.entrypoints.{run,registry,config,db,peers,modules,rpc}`。
- 仓库根目录保留旧导入入口。`bot.py`、`tester.py` 通过 `sys.modules` 把旧模块名映射到新实现。`core/database/update.py` 只负责把旧版本留下的升级操作交给当前实现处理。
<<< END U007163 >>>
<<< UNIT U007164 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:30-30 | ctx=进程拓扑 >>>
## 进程拓扑
<<< END U007164 >>>
<<< UNIT U007165 | md-table | packages/akari-bot-core/akaribot/core/docs/architecture.md:32-38 | ctx=进程拓扑 >>>
| 进程 | 启动方式 | 职责 |
| --- | --- | --- |
| BotDaemon | `python -m akaribot.core.entrypoints.run` | 检查同一实例是否已经启动，执行 pre-init，启动并监控子进程 |
| pre-init | 守护进程以 `spawn`（Windows、macOS）或 `forkserver` 启动 | 补充缺失的配置项，创建数据表，执行数据库迁移 |
| 平台进程 | 每个适配器实例对应一个进程，进程名为 `client_name` | 维护平台 SDK 连接，保存消息上下文和按钮状态 |
| Server | 进程名 `server` | 解析消息，执行模块，运行计划任务 |
| jobqueue-hub | 进程名 `jobqueue-hub`，仅内置 WebSocket 后端 | 维护节点连接，选择接收任务的节点，传递控制信号 |
<<< END U007165 >>>
<<< UNIT U007166 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:40-40 | ctx=进程拓扑 >>>
任何子进程启动前，守护进程都会设置 `AKARI_CONFIG_READONLY=1`。此后所有子进程只能读取配置。只有 pre-init 进程可以写入配置，它会清除这个标记。
<<< END U007166 >>>
<<< UNIT U007167 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:42-42 | ctx=进程拓扑 >>>
`<实例根目录>/.bot.lock` 用来防止同一实例重复启动。同一实例第二次启动时，新进程会以退出码 1 结束。
<<< END U007167 >>>
<<< UNIT U007168 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:44-44 | ctx=启动顺序 >>>
## 启动顺序
<<< END U007168 >>>
<<< UNIT U007169 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:46-50 | ctx=启动顺序 >>>
1. 守护进程先选择语言，并生成初始 `config.toml`。这个文件只在首次运行时生成，只包含 `default_locale` 和 `config_version`。
2. pre-init 子进程加载配置模板，补充缺失项，调用 `init_db(generate_schemas=True)` 创建数据表并执行迁移。
3. 守护进程读取适配器实例。它会先检查同一平台是否有重复的登录信息或端口配置，再逐个启动平台进程。
4. 如果 JobQueue 使用 `websocket` 后端，且模式为 `embedded`，守护进程会先启动 Hub，等待它进入就绪状态，最多等待 10 秒。
5. 启动 Server 进程。之后，守护进程每秒检查一次各子进程的状态。
<<< END U007169 >>>
<<< UNIT U007170 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:52-52 | ctx=退出码与重启 >>>
## 退出码与重启
<<< END U007170 >>>
<<< UNIT U007171 | md-table | packages/akari-bot-core/akaribot/core/docs/architecture.md:54-59 | ctx=退出码与重启 >>>
| 退出码 | 含义 | 守护进程动作 |
| --- | --- | --- |
| `0` | 正常退出 | Server 退出时整体退出，平台进程退出时不重启 |
| `33` | 请求重启 | 清理导入缓存，重启全部子进程 |
| `78` | 配置错误，无法恢复 | 移除该进程，不再重启 |
| 其他 | 异常退出 | 平台进程会重启，同一实例在 60 秒内连续失败三次后不再重启 |
<<< END U007171 >>>
<<< UNIT U007172 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:61-61 | ctx=退出码与重启 >>>
`~restart` 先把发起重启的会话写入 `data/private/<client>/.cache_restart_author`，再调用 `core.server.terminate.restart()`。这个函数清理全部资源，然后调用 `os._exit(33)`。
<<< END U007172 >>>
<<< UNIT U007173 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:63-63 | ctx=退出码与重启 >>>
新的 Server 启动后，会等待目标平台进程以新的 `peer_id` 注册为 `ready`，最多等待 60 秒，然后发送重启提示。模块加载失败的信息记录在 `.cache_loader` 中。
<<< END U007173 >>>
<<< UNIT U007174 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:65-65 | ctx=Server 初始化 >>>
## Server 初始化
<<< END U007174 >>>
<<< UNIT U007175 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:67-67 | ctx=Server 初始化 >>>
`core.server.run.main()` 依次完成：
<<< END U007175 >>>
<<< UNIT U007176 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:78-78 | ctx=Server 初始化 >>>
`init_async` 还会注册 `hourly-background` 核心任务。这个任务每小时执行一次会话后台检查，清理过期的队列记录和临时字典。
<<< END U007176 >>>
<<< UNIT U007177 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:80-80 | ctx=Server 初始化 >>>
主循环每秒检查一次队列轮询任务是否仍在运行。轮询器异常退出被视为致命错误，进程会立即退出，由守护进程处理。
<<< END U007177 >>>
<<< UNIT U007178 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:82-82 | ctx=消息收发 >>>
## 消息收发
<<< END U007178 >>>
<<< UNIT U007179 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:84-84 | ctx=消息收发 >>>
消息分为入站和出站两条链路。平台进程负责与平台 SDK 交互，Server 负责解析消息并执行模块。
<<< END U007179 >>>
<<< UNIT U007180 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:86-86 | ctx=入站 >>>
### 入站
<<< END U007180 >>>
<<< UNIT U007181 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:88-92 | ctx=入站 >>>
1. 平台进程构造 `SessionInfo`，其中包含平台、场景、发送者、消息链和 `ctx_slot`，然后调用 `Bot.process_message()`。
2. `Bot.process_message()` 在后台保存上下文并设置存活标记，再通过 `ServerAPI.receive_message` 把消息投递给 Server。处理结束后，平台 SDK 的上下文会被释放。
3. Server 端的 `parser()` 刷新会话信息，依次执行 `SESSION_READY`、`SESSION_BEFORE_WAIT` 等 Hook，检查是否有等待这条消息的任务，再判断命令前缀。
4. 命令路径先解析别名，按最长匹配选中模块并获取执行锁，再由模块的命令模板完成匹配。正则路径在 `REGEX_ROUTE` Hook 之后遍历候选模块。
5. 模块函数通过 `MessageSession` 读取 `session_info`、`parsed_msg` 和 `trigger_msg`。
<<< END U007181 >>>
<<< UNIT U007182 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:94-94 | ctx=出站 >>>
### 出站
<<< END U007182 >>>
<<< UNIT U007183 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:96-98 | ctx=出站 >>>
1. `MessageSession.send_message()` 先整理消息链，再执行关键词过滤、媒体压缩和敏感内容检查。之后经过 `OUTGOING_BEFORE_SEND` Hook，再调用 `PlatformAPI.send_message`。
2. Server 根据 `owner_peer_id` 把调用交给接收原消息的平台进程。平台进程的 `ContextManager` 完成实际发送，并返回消息 ID。
3. 主动推送由 `Bot.post_message` 发起。它按场景组和消息通道选出候选会话。每个通道先由队首会话发送，其余会话留作备用。发送失败时，平台进程把备用会话列表交回 Server。Server 再依次尝试下一个会话。
<<< END U007183 >>>
<<< UNIT U007184 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:100-100 | ctx=计划任务 >>>
## 计划任务
<<< END U007184 >>>
<<< UNIT U007185 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:102-102 | ctx=计划任务 >>>
`SchedulerLifecycle` 管理模块任务和核心任务：
<<< END U007185 >>>
<<< UNIT U007186 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:104-108 | ctx=计划任务 >>>
- 模块任务 ID 为 `module:<模块>:<序号>`，核心任务 ID 为 `core:<名称>`。
- `CronTrigger` 和 `DateTrigger` 直接使用，`IntervalTrigger` 按 `schedule_interval_multiplier` 调整间隔。
- 每个任务最多同时运行一个实例（`max_instances=1`）。错过触发后最多延迟 30 秒执行。
- 卸载、重载和关闭前会进入维护时段。这期间调度器会先停止接受新任务，等待正在启动的任务进入运行状态，再取消并收集正在运行的任务。
- 维护期间提交、但还没开始执行的任务，会在启动前被拒绝。
<<< END U007186 >>>
<<< UNIT U007187 | md-heading | packages/akari-bot-core/akaribot/core/docs/architecture.md:110-110 | ctx=关闭顺序 >>>
## 关闭顺序
<<< END U007187 >>>
<<< UNIT U007188 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:112-112 | ctx=关闭顺序 >>>
`cleanup_sessions()` 按以下顺序执行：
<<< END U007188 >>>
<<< UNIT U007189 | md-list | packages/akari-bot-core/akaribot/core/docs/architecture.md:114-120 | ctx=关闭顺序 >>>
1. 停止接收新任务。
2. 等待正在处理的队列任务完成。
3. 取消消息处理器。
4. 关闭调度器。
5. 停止后台初始化。
6. 关闭模块运行环境。
7. 运行预先安排的后台清理任务。
<<< END U007189 >>>
<<< UNIT U007190 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:122-122 | ctx=关闭顺序 >>>
最后，它停止轮询，再关闭队列、WebRender 与数据库连接。
<<< END U007190 >>>
<<< UNIT U007191 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/architecture.md:124-124 | ctx=关闭顺序 >>>
守护进程按平台进程、Server、Hub 的顺序终止子进程。Hub 最后退出，以便传递关闭信号并返回结果。
<<< END U007191 >>>
<<< UNIT U007192 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:1-1 | ctx=配置 >>>
# 配置
<<< END U007192 >>>
<<< UNIT U007193 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:3-3 | ctx=配置 >>>
本文介绍配置文件与表的布局、模板声明、读写接口与只读限制。
<<< END U007193 >>>
<<< UNIT U007194 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:5-5 | ctx=配置 >>>
`core.config.CFGManager` 负责读写配置。配置模板类在导入时确定每个字段的读取方式。
<<< END U007194 >>>
<<< UNIT U007195 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:7-7 | ctx=配置 >>>
用户配置放在 `config/` 根目录，全局默认值放在 `config/global/`。`CFGManager.load()` 会同时读取这两个位置。全局文件提供默认值，用户文件中的同名配置覆盖这些默认值。
<<< END U007195 >>>
<<< UNIT U007196 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:9-9 | ctx=文件与表布局 >>>
## 文件与表布局
<<< END U007196 >>>
<<< UNIT U007197 | md-table | packages/akari-bot-core/akaribot/core/docs/config.md:11-19 | ctx=文件与表布局 >>>
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
密钥始终与公开配置同文件，以 `_secret` 后缀区分。
<<< END U007198 >>>
<<< UNIT U007199 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:23-23 | ctx=全局默认层 >>>
## 全局默认层
<<< END U007199 >>>
<<< UNIT U007200 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:25-25 | ctx=全局默认层 >>>
`config/global/` 存放只读的默认配置，文件名与用户配置对应：
<<< END U007200 >>>
<<< UNIT U007201 | md-table | packages/akari-bot-core/akaribot/core/docs/config.md:27-30 | ctx=全局默认层 >>>
| 文件 | 用途 |
| --- | --- |
| `<表名>.global.toml` | TOML 格式的全局默认值 |
| `<表名>.global.json` | JSON 格式的全局默认值 |
<<< END U007201 >>>
<<< UNIT U007202 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:32-32 | ctx=全局默认层 >>>
加载时，`CFGManager` 先读取全局文件，再读取 `config/<表名>.toml`。
<<< END U007202 >>>
<<< UNIT U007203 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:34-34 | ctx=全局默认层 >>>
两层配置会递归合并。用户配置覆盖同名的标量、列表和子表。用户文件只需填写需要修改的字段即可，其余字段继续使用全局值。
<<< END U007203 >>>
<<< UNIT U007204 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:36-36 | ctx=全局默认层 >>>
写入、删除与配置注释修复只修改用户文件，不修改 `config/global/`。
<<< END U007204 >>>
<<< UNIT U007205 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:38-38 | ctx=全局默认层 >>>
删除用户文件里的某个键后，这个键会回到全局默认值。
<<< END U007205 >>>
<<< UNIT U007206 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:40-40 | ctx=全局默认层 >>>
删除整个用户文件后，这个表只使用全局文件。全局文件缺失时，启动不受影响。
<<< END U007206 >>>
<<< UNIT U007207 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:52-52 | ctx=全局默认层 >>>
多实例部署下，适配器表名带实例后缀，例如 `bot_telegram-alt`。如果实例表不存在，读取时会改用该平台的基础表。写入只落到实例表。
<<< END U007207 >>>
<<< UNIT U007208 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:54-54 | ctx=模板声明 >>>
## 模板声明
<<< END U007208 >>>
<<< UNIT U007209 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:56-56 | ctx=模板声明 >>>
模板类在所属包内声明，装饰器用来指定表名：
<<< END U007209 >>>
<<< UNIT U007210 | md-table | packages/akari-bot-core/akaribot/core/docs/config.md:58-64 | ctx=模板声明 >>>
| 装饰器 | 表名 | 使用方 |
| --- | --- | --- |
| `@on_base_config()` | 表外顶层键 | `config.toml` 的 `default_locale`、`config_version` |
| `@on_config("config")` | `[config]` | 核心公开配置 |
| `@on_config("config", secret=True)` | `[secret]` | 核心密钥 |
| `@on_bot_config("telegram")` | `bot_telegram` | 适配器 |
| `@on_module_config("dice")` | `module_dice` | 模块 |
<<< END U007210 >>>
<<< UNIT U007211 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:66-66 | ctx=模板声明 >>>
生成的内容取决于字段的类型标注与默认值：
<<< END U007211 >>>
<<< UNIT U007212 | md-list | packages/akari-bot-core/akaribot/core/docs/config.md:68-71 | ctx=模板声明 >>>
- 支持的类型为 `bool`、`datetime`、`date`、`float`、`int`、`list`、`str`。列表默认值写成 `[]`。
- 无默认值的必填项生成 `<Replace me with <type> value>` 占位符，读取时返回 `None`。
- 联合类型中含不受支持的成员时（如 `str | None`），生成通用占位符 `<Replace me>`。
- 键名会先转成小写，再读写。
<<< END U007212 >>>
<<< UNIT U007213 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:73-73 | ctx=读取与写入 >>>
## 读取与写入
<<< END U007213 >>>
<<< UNIT U007214 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:75-75 | ctx=读取与写入 >>>
模板类通过元类按属性名取值，未声明的字段直接抛出 `AttributeError`：
<<< END U007214 >>>
<<< UNIT U007215 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:84-84 | ctx=读取与写入 >>>
底层接口：
<<< END U007215 >>>
<<< UNIT U007216 | md-table | packages/akari-bot-core/akaribot/core/docs/config.md:86-92 | ctx=读取与写入 >>>
| 方法 | 说明 |
| --- | --- |
| `CFGManager.get(q, default=None, cfg_type=None, secret=False, table_name=None)` | 读取配置值，缺失时按默认值写入 |
| `CFGManager.has(q, secret=False, table_name=None)` | 判断键是否存在 |
| `CFGManager.write(...)` | 写入，受只读限制 |
| `CFGManager.edit_write(...)`、`edit_delete(...)` | 交互式编辑写入，需明确授权 |
| `CFGManager.save()` | 仅重写内容有变化的文件 |
<<< END U007216 >>>
<<< UNIT U007217 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:94-94 | ctx=读取与写入 >>>
读取到的值是模板写入的占位符（如 `<Replace me with <type> value>` 或 `<Replace me>`）时，返回 `None`。值类型与模板不符时，给出警告并返回原值。
<<< END U007217 >>>
<<< UNIT U007218 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:96-96 | ctx=字段注释 >>>
## 字段注释
<<< END U007218 >>>
<<< UNIT U007219 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:98-98 | ctx=字段注释 >>>
字段在模板类中声明后，须在所属包的 `locales/zh_cn.json` 中为它编写一条配置注释：
<<< END U007219 >>>
<<< UNIT U007220 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:104-104 | ctx=字段注释 >>>
表名取值：
<<< END U007220 >>>
<<< UNIT U007221 | md-list | packages/akari-bot-core/akaribot/core/docs/config.md:106-108 | ctx=字段注释 >>>
- 核心公开表为 `config`，核心密钥表为 `secret`。
- 适配器表为 `bot_<平台>`，适配器密钥表为 `bot_<平台>_secret`。
- 模块表为 `module_<模块>`，模块密钥表为 `module_<模块>_secret`。
<<< END U007221 >>>
<<< UNIT U007222 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:110-110 | ctx=字段注释 >>>
配置注释用于说明这个字段的作用。生成配置时，注释和字段一起写入。切换 `default_locale` 后，`CFGManager.repair_i18n_comments()` 会按新语言重写注释。
<<< END U007222 >>>
<<< UNIT U007223 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:112-112 | ctx=只读限制 >>>
## 只读限制
<<< END U007223 >>>
<<< UNIT U007224 | md-list | packages/akari-bot-core/akaribot/core/docs/config.md:114-119 | ctx=只读限制 >>>
- 守护进程在启动子进程前把 `AKARI_CONFIG_READONLY` 设为 `1`，平台进程与 Server 均只读。
- 只读进程中调用 `write()` 或 `save()` 会抛出 `ConfigOperationError`。`edit_write()`、`edit_delete()` 只能在明确授权的范围内使用。`~config` 命令和启动阶段补充缺失的配置与密钥时会调用这两个方法。
- 缺失项只在启动前的准备阶段写入。
- 写入时会先获取 `config/.config.lock` 的锁。重新加载、修改与保存都在持有锁的期间完成，同一时间只有一个进程可以执行。最多等待 10 秒。锁文件超过 60 秒没有更新时，视为过期锁。
- 写入使用临时文件加 `os.replace` 原子替换。
- 文件 mtime 变化后，最多延迟 1 秒重新加载。磁盘文件被清空而内存仍有内容时，保留内存中的值。
<<< END U007224 >>>
<<< UNIT U007225 | md-heading | packages/akari-bot-core/akaribot/core/docs/config.md:121-121 | ctx=配置版本 >>>
## 配置版本
<<< END U007225 >>>
<<< UNIT U007226 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:123-123 | ctx=配置版本 >>>
`config.toml` 的 `config_version` 当前为 6，由 `core.config.update` 执行升级。
<<< END U007226 >>>
<<< UNIT U007227 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:125-125 | ctx=配置版本 >>>
其他配置文件的版本由所属包维护。迁移脚本放在包的 `config_migrations/` 下，文件名以四位编号开头。迁移执行后，迁移编号会写回该配置文件的 `config_version`。
<<< END U007227 >>>
<<< UNIT U007228 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/config.md:127-127 | ctx=配置版本 >>>
新生成的配置文件会把 `manifest.toml` 的 `config_schema_version` 写入自身的 `config_version`。第一次迁移的编号必须是 `config_schema_version` 的值加 1，后续每次迁移的编号依次递增。
<<< END U007228 >>>
<<< UNIT U007229 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:1-1 | ctx=数据库 >>>
# 数据库
<<< END U007229 >>>
<<< UNIT U007230 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:3-3 | ctx=数据库 >>>
本文介绍数据库的 `default` 与 `local` 两个连接、union 数据、迁移执行与热重载。
<<< END U007230 >>>
<<< UNIT U007231 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:5-5 | ctx=数据库 >>>
数据库层基于 Tortoise ORM。它负责连接管理、模型注册、启动迁移与热重载。
<<< END U007231 >>>
<<< UNIT U007232 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:7-7 | ctx=数据库 >>>
业务模型继承 `akaribot.core.api.DBModel`，通过 `get_by_target_id()`、`get_by_sender_id()` 关联到会话或 union。
<<< END U007232 >>>
<<< UNIT U007233 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:9-9 | ctx=双连接 >>>
## 双连接
<<< END U007233 >>>
<<< UNIT U007234 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:11-11 | ctx=双连接 >>>
`init_db()` 注册两个连接与两个应用：
<<< END U007234 >>>
<<< UNIT U007235 | md-table | packages/akari-bot-core/akaribot/core/docs/database.md:13-16 | ctx=双连接 >>>
| 连接 | 默认连接字符串 | 应用 | 内容 |
| --- | --- | --- | --- |
| `default` | `sqlite://database/save.db` | `models` | 核心模型与各包的模型 |
| `local` | `sqlite://database/local.db` | `local_models` | 本机缓存表 |
<<< END U007235 >>>
<<< UNIT U007236 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:18-18 | ctx=双连接 >>>
`default` 的连接字符串由 `CoreSecretConfig.db_path` 提供。SQLite 的相对路径以实例根目录为基准解析，进程可以从任意目录启动。
<<< END U007236 >>>
<<< UNIT U007237 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:20-20 | ctx=双连接 >>>
连接参数先设置 `busy_timeout=30000`，然后启用 WAL。并发启动时，等待写锁的时间也受这个超时约束。
<<< END U007237 >>>
<<< UNIT U007238 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:22-22 | ctx=双连接 >>>
`local` 存放可随时重建的本机数据，例如关键词检测缓存和外部平台活动记录。这些数据存放在单独的数据库文件里。
<<< END U007238 >>>
<<< UNIT U007239 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:38-38 | ctx=双连接 >>>
框架从各包的发现信息里收集模型文件。`PackageRegistry.db_model_paths()` 给出导入路径。
<<< END U007239 >>>
<<< UNIT U007240 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:40-40 | ctx=双连接 >>>
`init_db()` 把这些模型路径加入 `models` 应用。`get_model_names()` 与 `get_model_fields()` 供 `~database` 命令列出数据表与字段。
<<< END U007240 >>>
<<< UNIT U007241 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:42-42 | ctx=union 数据 >>>
## union 数据
<<< END U007241 >>>
<<< UNIT U007242 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:44-44 | ctx=union 数据 >>>
平台账号与场景的 ID 会变化，业务数据都关联到 union：
<<< END U007242 >>>
<<< UNIT U007243 | md-table | packages/akari-bot-core/akaribot/core/docs/database.md:46-51 | ctx=union 数据 >>>
| 表 | 关键列 | 说明 |
| --- | --- | --- |
| `sender_union_info` | `union_id` | 用户数据：`blocked`、`trusted`、`superuser`、`warns`、`petal`、`sender_data` |
| `sender_union_bind` | `sender_id` → `union_id` | 平台账号到用户 union 的映射 |
| `target_union_info` | `union_id` | 场景数据：`muted`、`locale`、`modules`、`custom_admins`、`banned_users`、`target_data` |
| `target_union_bind` | `target_id` → `union_id`，`channel_id` | 平台场景到场景 union 的映射与消息通道编号 |
<<< END U007243 >>>
<<< UNIT U007244 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:53-53 | ctx=union 数据 >>>
`resolve_union(id, create)` 返回记录所属的 union。`create` 为真且记录不存在时，它会新建。
<<< END U007244 >>>
<<< UNIT U007245 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:55-55 | ctx=union 数据 >>>
`TargetUnionInfo.config_module()`、`switch_mute()`、`edit_target_data()` 和 `SenderUnionInfo.edit_sender_data()` 都在事务中运行。它们通过 `select_for_update()` 改写 JSON 列。
<<< END U007245 >>>
<<< UNIT U007246 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:57-57 | ctx=union 数据 >>>
同一 union 下 `channel_id` 相同的场景被视为同一条消息通道。主动推送按通道只发送一次。
<<< END U007246 >>>
<<< UNIT U007247 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:59-59 | ctx=union 数据 >>>
`delete_union()` 先校验引用，再清理该 union 所在域的全部表。
<<< END U007247 >>>
<<< UNIT U007248 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:61-61 | ctx=union 数据 >>>
跨表写入同一 union 时，先调用 `union_mutation()`，再在 `default` 事务中对该 union 的行加锁：
<<< END U007248 >>>
<<< UNIT U007249 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:88-88 | ctx=union 数据 >>>
查询与写入必须共用同一个 `connection`，否则 `select_for_update()` 的行锁不覆盖后续写入。
<<< END U007249 >>>
<<< UNIT U007250 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:90-90 | ctx=union 数据 >>>
核心包在 `manifest.toml` 的 `owned_tables` 中声明自己拥有的表，数据清理时据此判断数据表属于哪个包。各包的模型与表由自己的 `manifest.toml` 声明。
<<< END U007250 >>>
<<< UNIT U007251 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:92-92 | ctx=迁移 >>>
## 迁移
<<< END U007251 >>>
<<< UNIT U007252 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:94-94 | ctx=迁移 >>>
每个包把 revision 放在 `migrations/`（或 `manifest.migrations` 声明的目录）：
<<< END U007252 >>>
<<< UNIT U007253 | md-list | packages/akari-bot-core/akaribot/core/docs/database.md:105-109 | ctx=迁移 >>>
- `REVISION` 非空，`DEPENDS_ON` 只能指向同包 revision。`DEPENDS_ON` 未声明时，按 revision 字典序执行。
- 执行顺序固定为 core 的全部待应用 revision，再按包名执行各包。
- 已应用记录写入 `schema_migrations`（`package`、`revision`、`applied_at`、`checksum`），以 `(package, revision)` 唯一。revision 文件改动后 checksum 随之变化，可以据此发现文件已被修改。
- 每条 revision 必须可重复执行，因为 MySQL 的 DDL 自动提交，无法与版本记录写入同一事务，因此每一步先探测再执行。SQLite 支持事务性 DDL，Runner 把单条 revision 与版本记录包进同一事务。
- `MigrationContext` 提供 `execute()`、`execute_script()`、`fetch_all()`、`has_table()`、`has_column()`、`rename_table()`、`rename_column()`，按方言生成 SQL。
<<< END U007253 >>>
<<< UNIT U007254 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:111-111 | ctx=迁移 >>>
迁移只在创建数据表的写入进程中执行。pre-init 以 `generate_schemas=True` 调用 `init_db()`，随后运行 `run_startup_migrations()`。平台进程与 Server 只读写已有的数据，数据表与表结构的创建和修改都在写入进程中进行。
<<< END U007254 >>>
<<< UNIT U007255 | md-heading | packages/akari-bot-core/akaribot/core/docs/database.md:113-113 | ctx=热重载 >>>
## 热重载
<<< END U007255 >>>
<<< UNIT U007256 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:115-115 | ctx=热重载 >>>
模块安装、卸载或数据库维护会重建连接：
<<< END U007256 >>>
<<< UNIT U007257 | md-list | packages/akari-bot-core/akaribot/core/docs/database.md:117-120 | ctx=热重载 >>>
1. `prepare_db_reload()` 在旧 context 仍可用时初始化新 context。
2. 激活前先等待 JobQueue 处理完队列中的任务，并让 Scheduler 进入维护窗口，停止接收新任务，取消正在运行的计划任务。
3. `activate_db_reload()` 原子替换全局 context，随后关闭旧 context。
4. 失败时 `close_prepared_db_reload()` 丢弃未激活的 context，旧连接保持可用。
<<< END U007257 >>>
<<< UNIT U007258 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/database.md:122-122 | ctx=热重载 >>>
`close_db()` 关闭连接并清除 Tortoise 的全局与任务级 context，使下一次初始化从空状态开始。
<<< END U007258 >>>
<<< UNIT U007259 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:1-1 | ctx=开发流程 >>>
# 开发流程
<<< END U007259 >>>
<<< UNIT U007260 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:3-3 | ctx=开发流程 >>>
本文介绍克隆仓库后的环境准备、日常检查、测试命令与提交约定。包结构、API 与测试的细节分别见 [模块开发](module-development.md)、[公共 API](public-api.md) 与测试框架的[运行入口](../../../../akari-bot-testing/akaribot/testing/docs/index.md)。
<<< END U007260 >>>
<<< UNIT U007261 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:5-5 | ctx=环境准备 >>>
## 环境准备
<<< END U007261 >>>
<<< UNIT U007262 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:7-7 | ctx=环境准备 >>>
仓库是 uv workspace，仓库根目录的 `pyproject.toml` 只声明工作区中的包与工具配置，没有 `[project]` 表。
<<< END U007262 >>>
<<< UNIT U007263 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:14-14 | ctx=环境准备 >>>
缓存与 `.venv` 都放在工作区内。新增依赖时按包添加：
<<< END U007263 >>>
<<< UNIT U007264 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:20-20 | ctx=环境准备 >>>
`uv add` 要把依赖写入 `[project]` 表，而仓库根目录的 `pyproject.toml` 没有这个表。因此新增依赖时，要按上面的命令用 `--package` 指定包。
<<< END U007264 >>>
<<< UNIT U007265 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:22-22 | ctx=环境准备 >>>
依赖版本以 `uv.lock` 为准。`pre-commit` 的 `uv-export` 从这个文件导出依赖清单，结果不包含 hash。
<<< END U007265 >>>
<<< UNIT U007266 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:24-24 | ctx=环境准备 >>>
CI 使用 `--locked --all-extras --dev` 安装。`uv.lock` 与声明的依赖不一致时，安装失败。
<<< END U007266 >>>
<<< UNIT U007267 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:26-26 | ctx=日常命令 >>>
## 日常命令
<<< END U007267 >>>
<<< UNIT U007268 | md-table | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:28-35 | ctx=日常命令 >>>
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
全量测试运行完成后，失败的用例清单必须与 `tools/test_baseline.txt` 中列出的用例按名称一一对应。运行结束后，用 `tools/check_test_baseline.py --junit junit.xml --baseline tools/test_baseline.txt` 检查两者是否一致。
<<< END U007269 >>>
<<< UNIT U007270 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:39-39 | ctx=日常命令 >>>
只读测试使用另一份清单 `tools/test_baseline_readonly.txt`。这份清单由 `tools/check_test_baseline.py` 的 `--update` 参数重新生成。
<<< END U007270 >>>
<<< UNIT U007271 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:41-41 | ctx=提交前检查 >>>
## 提交前检查
<<< END U007271 >>>
<<< UNIT U007272 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:43-43 | ctx=提交前检查 >>>
提交前要执行下列检查，每一项都覆盖整个仓库：
<<< END U007272 >>>
<<< UNIT U007273 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:51-51 | ctx=提交前检查 >>>
`pre-commit install` 安装的钩子与上面的检查项不同，`comment-lint` 与 `boundary-lint` 带 `--diff HEAD`，只检查改动行，这样仓库中已有的违规不会阻止提交。推送前仍要执行全部检查。其余钩子为 `uv-export`、`ruff-check --fix` 与 `ruff-format`。
<<< END U007273 >>>
<<< UNIT U007274 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:53-53 | ctx=代码风格 >>>
## 代码风格
<<< END U007274 >>>
<<< UNIT U007275 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:55-55 | ctx=代码风格 >>>
Ruff 行宽 120、双引号、目标版本 `py312`，忽略 `E402`、`F405`、`F403`、`E741`、`E721`。导入按标准库、第三方、项目内部分组。
<<< END U007275 >>>
<<< UNIT U007276 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:57-57 | ctx=代码风格 >>>
模块与适配器只从 `akaribot.core.api` 获取公开接口，核心内部出现循环依赖时，改用 `akaribot.core.exports` 注册，需要时按名称取回。
<<< END U007276 >>>
<<< UNIT U007277 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:59-59 | ctx=代码风格 >>>
注释说明这段代码为何这样编写，单条一般不超过三行。含义清楚的代码不加注释，非公开 API 不加 docstring。
<<< END U007277 >>>
<<< UNIT U007278 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:61-61 | ctx=代码风格 >>>
注释、文档与配置说明一律用正式书面语。中文与拉丁字母之间加空格，使用全角标点与弯引号。面向用户的文案称呼对方为“你”，机器人自称“机器人”。
<<< END U007278 >>>
<<< UNIT U007279 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:63-63 | ctx=代码风格 >>>
文档、注释与配置说明只描述当前状态。设计取舍说明当前为何如此，变更过程交给 git 历史。为迁移历史数据保留的兼容逻辑注明适用范围。
<<< END U007279 >>>
<<< UNIT U007280 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:65-65 | ctx=分支与提交 >>>
## 分支与提交
<<< END U007280 >>>
<<< UNIT U007281 | md-list | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:67-71 | ctx=分支与提交 >>>
- 新功能用 `dev/` 前缀，修复用 `fix/` 前缀，分支名使用英文。
- 未经授权不执行 `git commit`、`git add`、`git push`、`git reset` 或 `git checkout -- <文件>`。授权只对当次请求有效。
- 提交信息用英文书面语，正文写清实际运行输出、失败用例的对比与检查结果等证据。
- 移动文件用 `git mv`，保留文件的修改历史。根目录保留同名兼容文件时 git 不记为 rename，按“先纯移动、再改内容”两段提交。
- 包内有源码改动时，要提升该包的 `version`。不升级版本时，在提交信息的最后一段单独写一行 `Skip-Version: true`，跳过全部包。只想跳过部分包时，写 `Skip-Version: <包名>[, <包名>]`，列出要跳过的包。`tools/check_versions.py` 负责检查这项约定，由 CI 在 PR 阶段以目标分支为基准运行，日常检查不包含它。
<<< END U007281 >>>
<<< UNIT U007282 | md-heading | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:73-73 | ctx=文档 >>>
## 文档
<<< END U007282 >>>
<<< UNIT U007283 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:75-75 | ctx=文档 >>>
每个包的导入包目录下都有 `docs/`。目录中的 `docs/config/global/docs.global.toml` 声明文档的标题、简介与排序。包在 `pyproject.toml` 的 `[project.entry-points."akaribot.docs"]` 中声明文档所在的导入路径，站点按这条声明收录该包的文档。
<<< END U007283 >>>
<<< UNIT U007284 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/development-workflow.md:77-77 | ctx=文档 >>>
文档站的命令为 `akaribot docs list|build|serve|deploy|status|clean`。站点配置写在实例根目录的 `docs.toml`，生成的文件放在实例的 `cache/docs/` 目录。包文档需要哪些字段、目录如何组织，见仓库根目录的 `docs/package-docs.md`。
<<< END U007284 >>>
<<< UNIT U007285 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:1-1 | ctx=常见问题 >>>
# 常见问题
<<< END U007285 >>>
<<< UNIT U007286 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:3-3 | ctx=常见问题 >>>
本文列出常见问题的排查与操作办法。命令与默认值以当前源码为准，权限模型、模块启用与部署细节分别见[权限](permissions.md)、[模块开发](module-development.md)与 [CLI 文档](../../../../akari-bot-cli/akaribot/cli/docs/index.md)。
<<< END U007286 >>>
<<< UNIT U007287 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:5-5 | ctx=查看帮助与文档 >>>
## 查看帮助与文档
<<< END U007287 >>>
<<< UNIT U007288 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:7-7 | ctx=查看帮助与文档 >>>
在聊天中发送 `~help` 查看模块列表与入口，发送 `~help <module>` 查看指定模块的命令、参数与权限。
<<< END U007288 >>>
<<< UNIT U007289 | md-list | packages/akari-bot-core/akaribot/core/docs/faq.md:9-11 | ctx=查看帮助与文档 >>>
- `--legacy`：强制输出文字或表格版本。
- `--img`：强制输出图片版本。
- 平台不支持图片时，命令改用文字版本。
<<< END U007289 >>>
<<< UNIT U007290 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:13-13 | ctx=查看帮助与文档 >>>
文档站点由已安装包内的 `docs/` 汇总生成，常用命令：
<<< END U007290 >>>
<<< UNIT U007291 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:21-21 | ctx=查看帮助与文档 >>>
构建需要 Node.js 与 npm，版本以主题清单为准。生成物写在实例的 `cache/docs/`。`~help` 底部的在线文档入口来自 `config.toml` 的 `help_url` 与 `help_page_url`。
<<< END U007291 >>>
<<< UNIT U007292 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:23-23 | ctx=模块没有反应或未启用 >>>
## 模块没有反应或未启用
<<< END U007292 >>>
<<< UNIT U007293 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:25-25 | ctx=模块没有反应或未启用 >>>
先确认模块是否安装、是否全局加载、是否在当前场景启用，这是三个独立状态：
<<< END U007293 >>>
<<< UNIT U007294 | md-table | packages/akari-bot-core/akaribot/core/docs/faq.md:27-31 | ctx=模块没有反应或未启用 >>>
| 状态 | 检查方式 | 修改方式 |
| --- | --- | --- |
| 已安装 | `akaribot module list` | `akaribot module add <名>` |
| 全局加载 | `akaribot module status` | `akaribot module load <名>` |
| 场景启用 | `~module list` | `~module enable <名>` |
<<< END U007294 >>>
<<< UNIT U007295 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:33-33 | ctx=模块没有反应或未启用 >>>
`base=True` 的基础模块始终启用。普通模块需要场景管理员执行 `~module enable` 启用。
<<< END U007295 >>>
<<< UNIT U007296 | md-list | packages/akari-bot-core/akaribot/core/docs/faq.md:35-36 | ctx=模块没有反应或未启用 >>>
- 未启用时，机器人会提示启用命令。
- 声明了 `required_superuser` 的模块只有超级用户能启用。`~module enable all` 会跳过这些模块。
<<< END U007296 >>>
<<< UNIT U007297 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:38-38 | ctx=模块没有反应或未启用 >>>
模块已启用但仍不响应时，先检查平台能力与机器人权限：
<<< END U007297 >>>
<<< UNIT U007298 | md-list | packages/akari-bot-core/akaribot/core/docs/faq.md:40-42 | ctx=模块没有反应或未启用 >>>
- `rss` 模块要求平台支持推送。
- `regex` 与 `event` 模块要求平台可读取全部消息。
- `required_bot_permissions` 中的权限缺失时，`~module enable` 会列出缺少项。
<<< END U007298 >>>
<<< UNIT U007299 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:44-44 | ctx=模块没有反应或未启用 >>>
机器人被禁止发言或用户被封禁时，模块不响应。
<<< END U007299 >>>
<<< UNIT U007300 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:46-46 | ctx=提示权限不足 >>>
## 提示权限不足
<<< END U007300 >>>
<<< UNIT U007301 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:48-48 | ctx=提示权限不足 >>>
权限分为普通用户、场景管理员、超级用户与基础超级用户，判定与授予方式见[权限](permissions.md)。常见处理：
<<< END U007301 >>>
<<< UNIT U007302 | md-list | packages/akari-bot-core/akaribot/core/docs/faq.md:50-53 | ctx=提示权限不足 >>>
- 场景管理命令被拒绝：请场景管理员执行 `~admin add <用户 ID>`，或由平台原生管理员操作。
- 超级用户命令被拒绝：请现有超级用户执行 `~superuser add <用户 ID>`。
- 仅某个模块被拒绝：请超级用户执行 `~auth add <用户 ID> <模块>`，该授权只对声明 `required_superuser` 的模块有效。
- 模块开启被拒绝：可能是模块级权限、机器人权限或平台能力不足，按提示处理。
<<< END U007302 >>>
<<< UNIT U007303 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:55-55 | ctx=提示权限不足 >>>
`base_superuser` 只能通过 `config.toml` 维护。
<<< END U007303 >>>
<<< UNIT U007304 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:57-57 | ctx=报告问题与贡献 >>>
## 报告问题与贡献
<<< END U007304 >>>
<<< UNIT U007305 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:59-59 | ctx=报告问题与贡献 >>>
提交 Issue 前先搜索是否已有相同问题。错误报告应包含简要描述、复现步骤、预期结果、实际结果与日志。功能建议应说明用途与可能的实现方式。仓库地址见 [CONTRIBUTING.md](https://github.com/Teahouse-Studios/akari-bot/blob/master/CONTRIBUTING.md)。Issue 模板见该文件。
<<< END U007305 >>>
<<< UNIT U007306 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:61-61 | ctx=报告问题与贡献 >>>
贡献代码的流程为先 Fork 仓库，再创建分支、修改并提交 PR。分支名使用英文，新功能用 `dev/`，修复用 `fix/`。提交前运行 Ruff、注释检查、边界检查与版本检查，具体命令见贡献指南。
<<< END U007306 >>>
<<< UNIT U007307 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:63-63 | ctx=报告问题与贡献 >>>
翻译经 Weblate 提交。简体中文以外的翻译问题，不建议在 Issue 里讨论。
<<< END U007307 >>>
<<< UNIT U007308 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:67-67 | ctx=报告问题与贡献 >>>
涉及敏感信息的安全问题不要提交到 Issue 或其他公开渠道，应按 `SECURITY.md` 的方式私下联系维护者。
<<< END U007308 >>>
<<< UNIT U007309 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:71-71 | ctx=许可证 >>>
## 许可证
<<< END U007309 >>>
<<< UNIT U007310 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:73-73 | ctx=许可证 >>>
core、官方模块与适配器使用 AGPL-3.0-only。字体资源使用 OFL-1.1，品牌资产使用专有许可，`akari-bot-html2text` 使用 GPL-3.0。每个包具体适用哪个许可证，以该包的 `pyproject.toml` 与包内 LICENSE 中写明的为准。
<<< END U007310 >>>
<<< UNIT U007311 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:75-75 | ctx=许可证 >>>
修改并分发本项目时，要遵守对应的许可证。AGPL-3.0 还要求向网络用户提供对应的源码。
<<< END U007311 >>>
<<< UNIT U007312 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:77-77 | ctx=更新实例 >>>
## 更新实例
<<< END U007312 >>>
<<< UNIT U007313 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:79-79 | ctx=更新实例 >>>
实例内的 core、模块与适配器由 CLI 更新：
<<< END U007313 >>>
<<< UNIT U007314 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:85-85 | ctx=更新实例 >>>
机器人执行 `~update` 时，会调用 CLI 的 `module update --defer-runtime`。安装完成后，按提示执行 `~restart`。加上 `--defer-runtime` 时，这一步只安装包并同步配置，数据库迁移与代码切换要等下一次启动才执行。
<<< END U007314 >>>
<<< UNIT U007315 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:87-87 | ctx=更新实例 >>>
直接在宿主机上更新时，迁移立即执行，新代码也立即生效。升级涉及数据结构变化时，先停止实例，再备份数据库与配置。CLI 本身按 `uv tool` 的安装方式升级。
<<< END U007315 >>>
<<< UNIT U007316 | md-heading | packages/akari-bot-core/akaribot/core/docs/faq.md:89-89 | ctx=自建实例 >>>
## 自建实例
<<< END U007316 >>>
<<< UNIT U007317 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:91-91 | ctx=自建实例 >>>
需要仓库 `pyproject.toml` 中声明的 Python 版本和 [uv](https://docs.astral.sh/uv/)。基本流程：
<<< END U007317 >>>
<<< UNIT U007318 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:102-102 | ctx=自建实例 >>>
按 `config schema` 列出的字段填写适配器的登录信息，然后启动实例。用 `akaribot config set <字段> <值> --table <表名>` 写入的值，会按模板声明的类型转换。
<<< END U007318 >>>
<<< UNIT U007319 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/faq.md:104-104 | ctx=自建实例 >>>
`akaribot init` 默认安装品牌资产、表情与常规可选依赖。加上 `--minimal` 时只安装核心所需的最小依赖。模块用 `akaribot module add <名>` 安装。旧部署的备份、试运行与迁移见 [命令参考中的 migrate](../../../../akari-bot-cli/akaribot/cli/docs/commands.md#migrate)。
<<< END U007319 >>>
<<< UNIT U007320 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:1-1 | ctx=本地化 >>>
# 本地化
<<< END U007320 >>>
<<< UNIT U007321 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:3-3 | ctx=本地化 >>>
本文介绍文案的声明方式、键的组织方式、插值规则与语言文件维护。
<<< END U007321 >>>
<<< UNIT U007322 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:5-5 | ctx=本地化 >>>
面向用户的固定文案统一用 `I18NContext` 声明，翻译数据存放在各包的 `locales/`，运行时由 `akari-bot-i18n` 的 `Locale` 解析。默认语言是 `zh_cn`。支持的语言从 `lang_list` 生成，构建时写入页面：
<<< END U007322 >>>
<<< UNIT U007323 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:17-17 | ctx=I18NContext >>>
`I18NContext` 是消息元素，保存键名与参数，发送时才按会话语言翻译。可选参数：
<<< END U007323 >>>
<<< UNIT U007324 | md-table | packages/akari-bot-core/akaribot/core/docs/i18n.md:19-23 | ctx=I18NContext >>>
| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `fallback` | `True` | 键缺失时回退到默认语言 |
| `locale_failed_prompt` | `True` | 翻译失败时附加提示 |
| `disable_joke` | `False` | 禁用文案中的玩笑替换 |
<<< END U007324 >>>
<<< UNIT U007325 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:25-25 | ctx=I18NContext >>>
参数值可以是字符串、数字或其他消息元素。消息元素作为参数时，会先转成字符串。
<<< END U007325 >>>
<<< UNIT U007326 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:27-27 | ctx=键与来源 >>>
## 键与来源
<<< END U007326 >>>
<<< UNIT U007327 | md-list | packages/akari-bot-core/akaribot/core/docs/i18n.md:29-36 | ctx=键与来源 >>>
- 每个包用 `manifest.toml` 的 `locales` 字段指定文案目录。
- 省略这个字段时，使用 `locales`。
- 目录里的文件名是语言代码。
- 文案以简体中文 `locales/zh_cn.json` 为准，人工只维护这个文件。新增的 key 只写在这里。
- 运行时快照由 `build_locale_snapshot(lang_list, collect_locale_paths(), "akari-bot")` 构建，`collect_locale_paths()` 取自发现层，core 的目录排在最前。
- 配置字段注释使用 `config.comments.<表名>.<字段名>` 形式的键，与普通文案同文件。
- 命令模板中的帮助文案写作 `I18N:key` 并用双层花括号包裹，由帮助系统解析。
- 术语占位符 `{TERM:...}` 由 `locales/terms/<语言>.json` 提供平台相关措辞（如“场景”“群组”）。
<<< END U007327 >>>
<<< UNIT U007328 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:38-38 | ctx=插值与占位符 >>>
## 插值与占位符
<<< END U007328 >>>
<<< UNIT U007329 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/i18n.md:40-40 | ctx=插值与占位符 >>>
模板使用 `${name}` 插值：
<<< END U007329 >>>
<<< UNIT U007330 | md-list | packages/akari-bot-core/akaribot/core/docs/i18n.md:48-50 | ctx=插值与占位符 >>>
- 占位符名按含义选取英文名，与调用处关键字一一对应。
- 占位符名不得与 `t()` 的形参（`key`、`fallback`、`locale_failed_prompt`、`disable_joke`）同名。同名会在渲染时触发 `TypeError`，例如 `${key}` 配 `key=...`。
- 修改键名或占位符后，须同时核对调用点的关键字参数。
<<< END U007330 >>>
<<< UNIT U007331 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:52-52 | ctx=语言文件维护 >>>
## 语言文件维护
<<< END U007331 >>>
<<< UNIT U007332 | md-list | packages/akari-bot-core/akaribot/core/docs/i18n.md:54-56 | ctx=语言文件维护 >>>
- 只编辑 `locales/zh_cn.json`。其他语言文件由 Weblate 自动提交，请不要自行创建、修改或补齐。
- `assets/config_store/<语言>/` 由配置模板生成，非 `zh_cn` 版本同样由自动化流程产出。
- 文案面向用户，保持书面语，不写口语或语气词。
<<< END U007332 >>>
<<< UNIT U007333 | md-heading | packages/akari-bot-core/akaribot/core/docs/i18n.md:58-58 | ctx=会话语言 >>>
## 会话语言
<<< END U007333 >>>
<<< UNIT U007334 | md-list | packages/akari-bot-core/akaribot/core/docs/i18n.md:60-63 | ctx=会话语言 >>>
- `BaseConfig.default_locale` 是全局默认语言，实例内可用 `~setup locale <lang>` 修改场景语言。
- 会话语言保存在 `TargetUnionInfo.locale`，`msg.t` 与 `I18NContext` 都按该值解析。
- 语言文件缺失或键不存在时按 `fallback` 设置回退，并在回复中给出提示。
- `Locale.t_str(text)` 用于对已拼接的文本再执行一次 key 替换，未命中的内容原样保留。
<<< END U007334 >>>
<<< UNIT U007335 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:1-1 | ctx=核心运行时 >>>
# 核心运行时
<<< END U007335 >>>
<<< UNIT U007336 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:3-3 | ctx=核心运行时 >>>
本文介绍核心运行时的定位、依赖与进程模型，并列出其余文档页。
<<< END U007336 >>>
<<< UNIT U007337 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:5-5 | ctx=核心运行时 >>>
`akaribot.core` 是 AkariBot 的核心运行时，提供公共接口和基础功能，由 `akari-bot-core` 包提供。`akari-bot-core` 同时提供内置模块 `akaribot.modules.core`，文档见[内置模块](../../modules/core/docs/index.md)。
<<< END U007337 >>>
<<< UNIT U007338 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:7-7 | ctx=定位 >>>
## 定位
<<< END U007338 >>>
<<< UNIT U007339 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:9-9 | ctx=定位 >>>
`akaribot.core` 提供守护进程入口、Server 进程、消息解析和会话模型，也定义平台进程与 Server 共用的接口。包发现、配置、数据库、计划任务、JobQueue 和本地化数据由它负责。
<<< END U007339 >>>
<<< UNIT U007340 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:11-11 | ctx=定位 >>>
模块和适配器都通过公共 API 使用 core。模块导入 `akaribot.core.api`，适配器再导入 `akaribot.core.api.adapters`。内置模块也使用这套 API。
<<< END U007340 >>>
<<< UNIT U007341 | md-list | packages/akari-bot-core/akaribot/core/docs/index.md:13-16 | ctx=定位 >>>
- `akaribot`、`akaribot.modules`、`akaribot.adapters` 使用 [PEP 420](https://peps.python.org/pep-0420/) 命名空间目录，没有 `__init__.py`。
- `akaribot.core` 是常规包。
- `CORE_API_VERSION` 定义公共 API 的版本号，运行时通过 `__api_version__` 暴露这个值。
- 模块包在 `manifest.toml` 的 `requires_core_api` 中声明支持的版本范围。
<<< END U007341 >>>
<<< UNIT U007342 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:18-18 | ctx=依赖关系 >>>
## 依赖关系
<<< END U007342 >>>
<<< UNIT U007343 | md-table | packages/akari-bot-core/akaribot/core/docs/index.md:20-27 | ctx=依赖关系 >>>
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
可选依赖以 extra 提供：
<<< END U007344 >>>
<<< UNIT U007345 | md-table | packages/akari-bot-core/akaribot/core/docs/index.md:31-36 | ctx=依赖关系 >>>
| extra | 内容 |
| --- | --- |
| `s3` | `boto3`，对象存储 |
| `mysql` | `asyncmy` 驱动 |
| `image`、`chart` | `matplotlib`，统计图表 |
| `full` | 上述三项加品牌与表情资源包 |
<<< END U007345 >>>
<<< UNIT U007346 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:38-38 | ctx=进程模型概览 >>>
## 进程模型概览
<<< END U007346 >>>
<<< UNIT U007347 | md-table | packages/akari-bot-core/akaribot/core/docs/index.md:40-46 | ctx=进程模型概览 >>>
| 进程 | 职责 |
| --- | --- |
| BotDaemon | 获取防止实例重复启动的锁文件，执行 pre-init，启动并监控子进程 |
| pre-init | 唯一可写配置的进程，补充缺失的配置项、创建数据表、执行迁移 |
| 平台进程 | 每个适配器实例一个，持有平台 SDK 与上下文 |
| Server | 解析消息、执行模块、运行计划任务 |
| jobqueue-hub | WebSocket 后端的内置 Hub，可选 |
<<< END U007347 >>>
<<< UNIT U007348 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/index.md:48-48 | ctx=进程模型概览 >>>
实例根目录由 `AKARI_INSTANCE_DIR` 指定，未设置时使用进程的当前目录。配置目录可以用 `AKARI_CONFIG_PATH` 单独指定。详情见[架构](architecture.md)。
<<< END U007348 >>>
<<< UNIT U007349 | md-heading | packages/akari-bot-core/akaribot/core/docs/index.md:50-50 | ctx=文档导航 >>>
## 文档导航
<<< END U007349 >>>
<<< UNIT U007350 | md-table | packages/akari-bot-core/akaribot/core/docs/index.md:52-67 | ctx=文档导航 >>>
| 页面 | 内容 |
| --- | --- |
| [架构](architecture.md) | 代码结构、进程拓扑、启动与重启、消息收发链路、计划任务 |
| [开发流程](development-workflow.md) | 环境、日常命令、检查项、代码风格、分支与提交、文档工具链 |
| [JobQueue](queue.md) | 后端选择、节点注册、RPC 与信号、超时与关闭 |
| [配置](config.md) | 配置模板、表布局、字段注释、只读限制 |
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
# 消息 API 参考
<<< END U007351 >>>
<<< UNIT U007352 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:3-3 | ctx=消息 API 参考 >>>
本文列出模块处理函数可用的消息接口、消息链与消息元素。接口与参数均从 `akaribot.core.api` 导入，模块声明与命令模板的写法见[模块开发](module-development.md)。
<<< END U007352 >>>
<<< UNIT U007353 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:5-5 | ctx=会话对象 >>>
## 会话对象
<<< END U007353 >>>
<<< UNIT U007354 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:7-7 | ctx=会话对象 >>>
模块函数接收 `Bot.MessageSession`。对象本身只保存会话快照与本次解析状态，场景字段都通过 `session_info` 读取，例如 `msg.session_info.bot_name` 用于获取机器人名称。
<<< END U007354 >>>
<<< UNIT U007355 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:9-14 | ctx=会话对象 >>>
| 字段或属性 | 说明 |
| --- | --- |
| `session_info` | `SessionInfo` 快照。目标、发送者、平台能力、语言与权限都记在这份快照里 |
| `sent` / `trigger_msg` | 已发送消息链列表（默认空）。parser 处理后的触发文本 |
| `matched_msg` / `parsed_msg` | 正则或事件的匹配结果。命令参数解析结果，无模板模块可能为 `None` |
| `target` / `t` / `t_str` | `target` 已弃用，等价于 `session_info`。`t`、`t_str` 按会话语言翻译键或文本 |
<<< END U007355 >>>
<<< UNIT U007356 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:16-16 | ctx=会话对象 >>>
场景字段通过 `msg.session_info` 访问：
<<< END U007356 >>>
<<< UNIT U007357 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:18-26 | ctx=会话对象 >>>
| 字段 | 说明 |
| --- | --- |
| `target_id`、`target_from`、`client_name` | 场景 ID、场景来源与客户端名 |
| `sender_id`、`sender_from`、`sender_name` | 发送者信息。主动会话可能为空 |
| `message_id`、`reply_id`、`messages`、`session_id`、`timestamp` | 触发消息、回复目标、原始消息链、会话 UUID 与时间戳 |
| `prefixes`、`muted`、`custom_admins`、`enabled_modules` | 可用命令前缀、禁止发言状态、自定义管理员 union ID 与已启用模块 |
| `locale`、`timezone_offset`、`display_timezone_offset`、`tmp` | `Locale` 对象（语言代码通过 `locale.locale` 获取）、场景与个人显示时区偏移（`timedelta`，未设置为 `None`）与临时字典 |
| `tz`、`display_tz`、`tz_label`、`display_tz_label` | 场景时区与展示时区（`tzinfo`）及其规范偏移字符串。展示时区未设置时跟随场景时区 |
| `bot_name`、`bot_id`、`is_private`、`fetch`、`support_*` | 本地化机器人名称与 ID。私聊、主动会话与平台能力标志 |
<<< END U007357 >>>
<<< UNIT U007358 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:28-28 | ctx=发送消息 >>>
## 发送消息
<<< END U007358 >>>
<<< UNIT U007359 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:30-35 | ctx=发送消息 >>>
| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `send_message()` | `message_chain`、`quote=True`、`disable_secret_check=False`、`callback=None`、`callback_id=None`、`callback_timeout=1800`、`callback_once=False` | 发送并返回 `FinishedSession` |
| `finish()` | 参数同 `send_message()`，`message_chain` 可省略 | 发送后抛出 `SessionFinished`。不传入消息链时只结束会话 |
| `send_direct_message()` | `message_chain`、`disable_secret_check=False` | 提交后立即返回 `None`。消息 ID 由其他接口提供 |
| `send_private_message()` | `message_chain`、`user_id=None`、`disable_secret_check=False` | 私聊发送，返回消息 ID 列表。空列表表示失败 |
<<< END U007359 >>>
<<< UNIT U007360 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:37-37 | ctx=发送消息 >>>
`send_message()` 的 `callback` 在用户引用或点击这条消息后执行，输入参数是回复的 `MessageSession`。
<<< END U007360 >>>
<<< UNIT U007361 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:39-39 | ctx=发送消息 >>>
`callback_id` 是按钮回调使用的虚拟回复 ID。取值规则如下：
<<< END U007361 >>>
<<< UNIT U007362 | md-list | packages/akari-bot-core/akaribot/core/docs/message-api.md:41-42 | ctx=发送消息 >>>
- 省略 `callback_id` 时，框架会为缺少 `reply_id` 的按钮生成一个。
- 消息里没有按钮时，框架按实际消息 ID 绑定。
<<< END U007362 >>>
<<< UNIT U007363 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:44-44 | ctx=发送消息 >>>
`callback_timeout` 默认 1800 秒。传 `None` 表示不设置超时。`callback_once=True` 表示首次触发后失效。
<<< END U007363 >>>
<<< UNIT U007364 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:46-46 | ctx=发送消息 >>>
返回的 `FinishedSession` 提供 `message_id`。`delete()` 是异步方法，用于删除已发送的消息。平台没有返回 ID 时，`message_id` 可能是空列表。
<<< END U007364 >>>
<<< UNIT U007365 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:59-59 | ctx=发送消息 >>>
发送路径默认会执行 `MessageChain.is_safe` 的敏感信息扫描。检查不通过时，整条消息链会被替换成 `error.message.chain.unsafe`。只有确认内容安全时，才可以传 `disable_secret_check=True` 跳过检查。
<<< END U007365 >>>
<<< UNIT U007366 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:63-63 | ctx=等待用户输入 >>>
## 等待用户输入
<<< END U007366 >>>
<<< UNIT U007367 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:65-70 | ctx=等待用户输入 >>>
| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `wait_confirm()` | `message_chain=None`、`quote=True`、`delete=True`、`timeout=120`、`append_instruction=True`、`no_confirm_action=True`、`release_execution_lock=True`、`consume_any_message=False`、`confirm_token=None` | 等待确认，返回 `bool` |
| `wait_next_message()` | `message_chain=None`、`quote=True`、`delete=False`、`timeout=120`、`append_instruction=True` | 等待同一发送者的下一条消息 |
| `wait_reply()` | `message_chain`、`quote=True`、`delete=False`、`timeout=120`、`all_=False`、`append_instruction=True` | 等待对该消息的引用回复 |
| `wait_anyone()` | `message_chain=None`、`quote=False`、`delete=False`、`timeout=120` | 等待场景内任意成员的消息 |
<<< END U007367 >>>
<<< UNIT U007368 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:72-72 | ctx=等待用户输入 >>>
等待消息的方法返回新的 `MessageSession`，`wait_confirm()` 例外，只返回 `bool`。
<<< END U007368 >>>
<<< UNIT U007369 | md-list | packages/akari-bot-core/akaribot/core/docs/message-api.md:74-81 | ctx=等待用户输入 >>>
- 默认超时 120 秒。传 `None` 关闭超时。
- 超时、取消或无法取得结果时抛出 `WaitCancelException`。
- 等待期间默认释放执行锁。方法返回前重新获取该锁，获取失败按取消处理。
- `wait_confirm()` 在 `confirm_token` 非 `None` 时进入严格确认模式，必须原样回复这个口令，才算确认。普通模式接受 `confirm_command` 中的确认词。发送 `no` 返回 `False`。
- `consume_any_message=True` 时，任意消息都会结束等待，返回值仍按是否为确认词判断。
- 全局 `no_confirm` 开启时，直接返回 `no_confirm_action`。
- 平台不支持引用回复时，`wait_reply()` 改用 `wait_next_message()` 或 `wait_anyone()`，并以 `quote=False` 发送提示。`all_=True` 时接受任意成员的回复。
- `wait_next_message()` 与 `wait_anyone()` 命中的消息仍交常规 parser 处理。`wait_confirm()` 与 `wait_reply()` 会取走命中的消息，不再交给常规 parser。
<<< END U007369 >>>
<<< UNIT U007370 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:95-95 | ctx=等待用户输入 >>>
`WaitCancelException` 与 `SessionFinished` 都继承 `BaseException`，`except Exception` 捕获不到。
<<< END U007370 >>>
<<< UNIT U007371 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:99-99 | ctx=权限 >>>
## 权限
<<< END U007371 >>>
<<< UNIT U007372 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:101-105 | ctx=权限 >>>
| 方法 | 参数 | 说明 |
| --- | --- | --- |
| `check_super_user()` | 无，同步 | 发送者是否为超级用户 |
| `check_permission()` | 无，异步 | 自定义管理员或超级用户返回 `True`，否则检查平台原生权限 |
| `check_native_permission()` | `user_id=None`，异步 | 指定成员或发送者的平台原生管理员权限 |
<<< END U007372 >>>
<<< UNIT U007373 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:114-114 | ctx=其他操作 >>>
## 其他操作
<<< END U007373 >>>
<<< UNIT U007374 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:116-124 | ctx=其他操作 >>>
| 方法 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `as_display()` | `text_only=False`、`element_filter=None`、`connector="\n"` | 把触发消息转为字符串。`text_only=True` 只保留 `PlainElement` 文本，非文本元素按 KE 码、AT 码等字符串表示 |
| `delete()` | `reason=None` | 删除触发消息 |
| `sleep()` / `hold()` / `release()` / `start_typing()` / `end_typing()` | `s` / 无 | 暂停并释放执行锁（恢复失败时抛出 `WaitCancelException`）。保持或释放平台上下文。开始或结束输入状态 |
| `format_time()` / `format_num()` | `timestamp`、`date=True`、`simple=False`、`time=True`、`seconds=True`、`timezone=True` / `number`、`precision=0` | 按会话时区与语言格式化时间 / 按语言缩放数字（万、亿、兆或 k、M、G） |
| `call_onebot_api()` / `call_api()` | `api_name`、`**kwargs` | 转发到 OneBot 扩展接口。`call_api()` 已弃用。平台不支持时返回 `{"success": False, "error": ...}` |
| `restrict_member()` / `unrestrict_member()` | `user_id`、`duration=None`、`reason=None`、`wait=False` / `user_id`、`wait=False` | 禁言与解除禁言，`duration=None` 表示永久 |
| `kick_member()` / `ban_member()` / `unban_member()` | `user_id`、`reason=None`（`unban` 无 reason） | 移除、封禁、解封成员 |
<<< END U007374 >>>
<<< UNIT U007375 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:126-126 | ctx=其他操作 >>>
`now()` 与 `today()` 按场景时区返回当前时间与日期，业务代码需要时间时用这两个方法。
<<< END U007375 >>>
<<< UNIT U007376 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:128-128 | ctx=其他操作 >>>
主动会话（`FetchedMessageSession`）没有 `session_info.messages`。调用 `as_display()` 前，先检查它是否为空。
<<< END U007376 >>>
<<< UNIT U007377 | md-list | packages/akari-bot-core/akaribot/core/docs/message-api.md:130-133 | ctx=其他操作 >>>
- `as_display()` 的 `text_only` 默认是 `False`，`MessageChain.to_str()` 则为 `True`。
- `add_reaction()`、`remove_reaction()` 作用于触发消息。
- `grant_permission_group()`、`revoke_permission_group()` 管理平台权限组。
- `handle_error_signal()` 提交错误信号。
<<< END U007377 >>>
<<< UNIT U007378 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:143-143 | ctx=消息链 >>>
## 消息链
<<< END U007378 >>>
<<< UNIT U007379 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:145-153 | ctx=消息链 >>>
| 方法或属性 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `MessageChain.assign()` / `create()` / `from_list()` | `elements=None` / 无 / `lst` | 由字符串、元素、元素列表或元组构造。创建空链。从 `to_list()` 结果还原 |
| `as_sendable()` | `session_info=None`、`parse_message=True`、`enable_markdown=True` | 解析多语言与 KE 码，并按平台能力降级 |
| `to_str()` / `to_list()` / `to_kecode()` | `text_only=True`、`element_filter=None`、`connector="\n"` | 转为字符串、字典列表或 KE 码 |
| `is_safe` | 属性 | 是否不含敏感信息 |
| `append()` / `insert()` / `remove()` | `element`（`insert` 另有 `index`） | 追加与插入会把字符串转成 `PlainElement`。`remove()` 按元素删除 |
| `extend()` / `copy()` | 另一条链或元素列表 / 无 | 原地拼接或复制 |
| `contains()` / `only()` | 元素类型或类型元组 | 是否含某类元素、是否只含某类元素 |
<<< END U007379 >>>
<<< UNIT U007380 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:155-155 | ctx=消息链 >>>
`+` 返回新的消息链并深拷贝元素，`+=` 原地修改。两者的参数可以是 `MessageChain`、元素列表或单个元素，不能是单独的字符串。`in` 只判断元素类型，例如 `PlainElement in chain`，传入实例会抛出 `TypeError`。`MessageChain.assign()` 传入已有链时原样返回，不复制。需要独立副本时用 `copy()`。
<<< END U007380 >>>
<<< UNIT U007381 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:164-164 | ctx=消息链 >>>
`PlatformMessageChain.assign()` 按 `session_info.target_from` 选择对应的链。该键缺失时改用 `default`。`I18NMessageChain.assign()` 按 `session_info.locale.locale` 选择。这类链必须包含 `default` 键，否则抛出 `ValueError`。这两类链都由发送路径自动解析。
<<< END U007381 >>>
<<< UNIT U007382 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:166-166 | ctx=消息元素 >>>
## 消息元素
<<< END U007382 >>>
<<< UNIT U007383 | md-table | packages/akari-bot-core/akaribot/core/docs/message-api.md:168-178 | ctx=消息元素 >>>
| 构造器 | 关键参数（默认值） | 说明 |
| --- | --- | --- |
| `Plain()` / `Markdown()` | `*texts`、`disable_joke=False`、`allow_parse=True` | 纯文本与 Markdown 文本。`allow_parse=False` 时不解析 KE 码与多语言标记 |
| `Image()` / `Audio()` / `Video()` | `path`、`headers=None`、`max_h=None`、`allow_split=True` / `path` | 本地路径、URL、Base64 或 PIL 图片。音频与视频 |
| `Embed()` / `EmbedField()` | `title=None`、`description=None`、`url=None`、`timestamp`（默认取导入时时间）、`color=0x0091FF`、`image=None`、`thumbnail=None`、`author=None`、`footer=None`、`fields=None` / `name`、`value`、`inline=False` | 富文本卡片与字段 |
| `I18NContext()` | `key`、`fallback=True`、`locale_failed_prompt=True`、`disable_joke=False`、`**kwargs` | 按会话语言解析的文案 |
| `Mention()` | `user_id` | 提及用户，格式为平台前缀加用户 ID |
| `Url()` | `url`、`trusted=None`、`md_format=False`、`md_format_name=None` | 链接元素，受 URL 策略限制 |
| `FormattedTime()` | `timestamp`、`date=True`、`simple=False`、`time=True`、`seconds=True`、`timezone=True` | 按会话时区格式化的时间 |
| `ActionText()` | `text`、`show=None`、`reference=False`、`show_on_fallback=True`、`quote_on_fallback=False` | 可点击的命令文本 |
| `Button()` / `ButtonFrame()` | `show`、`value`、`reply_id=None`、`permission=OWNER`、`click_limit=1` / `rows` | 按钮与按钮区域 |
<<< END U007383 >>>
<<< UNIT U007384 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:191-191 | ctx=消息元素 >>>
`Plain`、`Image`、`Embed` 等名字绑定的是对应元素的 `assign` 类方法。类型判断使用 `PlainElement`、`ImageElement`、`EmbedElement` 等真实类。
<<< END U007384 >>>
<<< UNIT U007385 | md-heading | packages/akari-bot-core/akaribot/core/docs/message-api.md:195-195 | ctx=消息节点与渲染 >>>
## 消息节点与渲染
<<< END U007385 >>>
<<< UNIT U007386 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:197-197 | ctx=消息节点与渲染 >>>
`MessageNodes.assign(values, name=None)` 把多条 `MessageChain` 组成转发节点列表。`name` 省略时自动生成。`send_message()` 支持 `MessageNodes`。平台未声明 `support_handle_message_nodes` 时，框架会把消息节点渲染为图片再发送。
<<< END U007386 >>>
<<< UNIT U007387 | md-paragraph | packages/akari-bot-core/akaribot/core/docs/message-api.md:208-208 | ctx=消息节点与渲染 >>>
发送路径会处理以下情况：
<<< END U007387 >>>
<<< UNIT U007388 | md-list | packages/akari-bot-core/akaribot/core/docs/message-api.md:210-212 | ctx=消息节点与渲染 >>>
- `I18NContext` 按会话语言解析。`Markdown` 在平台不支持 `support_markdown` 时转为纯文本。
- `Embed` 在平台不支持 `support_embed` 时转为文本与图片。`ActionText` 在平台不支持 `support_action_text` 时转为纯文本。`Button` 与 `ButtonFrame` 在平台不支持 `support_button` 时丢弃。
- 空链会被替换为 `error.message.chain.empty`。未通过 `is_safe` 的整条消息链会被替换为 `error.message.chain.unsafe`，除非发送时传入 `disable_secret_check=True`。
<<< END U007388 >>>
