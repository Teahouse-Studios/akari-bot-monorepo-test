# 全仓可读文本审核稿 · 第 07 册 / 共 20 册

覆盖 U004564–U005769，49 个文件、1,206 个单元、33,058 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-cli/akaribot/cli/tui/adapters.py` | 93 | U004564–U004656 | 2,694 |
| `packages/akari-bot-cli/akaribot/cli/tui/app.py` | 48 | U004657–U004704 | 1,317 |
| `packages/akari-bot-cli/akaribot/cli/tui/cli_process.py` | 2 | U004705–U004706 | 84 |
| `packages/akari-bot-cli/akaribot/cli/tui/config.py` | 138 | U004707–U004844 | 3,427 |
| `packages/akari-bot-cli/akaribot/cli/tui/context.py` | 1 | U004845–U004845 | 30 |
| `packages/akari-bot-cli/akaribot/cli/tui/dashboard.py` | 97 | U004846–U004942 | 2,558 |
| `packages/akari-bot-cli/akaribot/cli/tui/database.py` | 128 | U004943–U005070 | 3,057 |
| `packages/akari-bot-cli/akaribot/cli/tui/dev.py` | 74 | U005071–U005144 | 1,783 |
| `packages/akari-bot-cli/akaribot/cli/tui/docs.py` | 121 | U005145–U005265 | 2,874 |
| `packages/akari-bot-cli/akaribot/cli/tui/doctor.py` | 46 | U005266–U005311 | 1,079 |
| `packages/akari-bot-cli/akaribot/cli/tui/environment.py` | 64 | U005312–U005375 | 1,610 |
| `packages/akari-bot-cli/akaribot/cli/tui/logs.py` | 54 | U005376–U005429 | 1,308 |
| `packages/akari-bot-cli/akaribot/cli/tui/misc.py` | 30 | U005430–U005459 | 773 |
| `packages/akari-bot-cli/akaribot/cli/tui/modules.py` | 125 | U005460–U005584 | 3,333 |
| `packages/akari-bot-cli/akaribot/cli/tui/run.py` | 33 | U005585–U005617 | 674 |
| `packages/akari-bot-cli/akaribot/cli/venv.py` | 40 | U005618–U005657 | 1,505 |
| `packages/akari-bot-cli/akaribot/cli/windows.py` | 2 | U005658–U005659 | 33 |
| `packages/akari-bot-cli/pyproject.toml` | 6 | U005660–U005665 | 454 |
| `packages/akari-bot-cli/tests/test_adapter.py` | 4 | U005666–U005669 | 163 |
| `packages/akari-bot-cli/tests/test_command_runner_streaming.py` | 2 | U005670–U005671 | 84 |
| `packages/akari-bot-cli/tests/test_config_placeholders.py` | 12 | U005672–U005683 | 524 |
| `packages/akari-bot-cli/tests/test_db_rows.py` | 5 | U005684–U005688 | 228 |
| `packages/akari-bot-cli/tests/test_docs_builder.py` | 2 | U005689–U005690 | 82 |
| `packages/akari-bot-cli/tests/test_docs_catalog.py` | 3 | U005691–U005693 | 136 |
| `packages/akari-bot-cli/tests/test_docs_cli.py` | 1 | U005694–U005694 | 24 |
| `packages/akari-bot-cli/tests/test_docs_config.py` | 2 | U005695–U005696 | 91 |
| `packages/akari-bot-cli/tests/test_docs_deploy_cli.py` | 1 | U005697–U005697 | 43 |
| `packages/akari-bot-cli/tests/test_docs_deploy_s3.py` | 1 | U005698–U005698 | 41 |
| `packages/akari-bot-cli/tests/test_docs_deploy_vercel.py` | 1 | U005699–U005699 | 45 |
| `packages/akari-bot-cli/tests/test_docs_dev.py` | 2 | U005700–U005701 | 84 |
| `packages/akari-bot-cli/tests/test_docs_generator.py` | 2 | U005702–U005703 | 85 |
| `packages/akari-bot-cli/tests/test_docs_server.py` | 2 | U005704–U005705 | 89 |
| `packages/akari-bot-cli/tests/test_docs_sigv4.py` | 1 | U005706–U005706 | 33 |
| `packages/akari-bot-cli/tests/test_docs_theme.py` | 2 | U005707–U005708 | 85 |
| `packages/akari-bot-cli/tests/test_docs_theme_sync.py` | 2 | U005709–U005710 | 104 |
| `packages/akari-bot-cli/tests/test_docs_toolchain.py` | 2 | U005711–U005712 | 92 |
| `packages/akari-bot-cli/tests/test_docs_watch.py` | 2 | U005713–U005714 | 87 |
| `packages/akari-bot-cli/tests/test_frozen_uv.py` | 1 | U005715–U005715 | 24 |
| `packages/akari-bot-cli/tests/test_instance_cwd.py` | 1 | U005716–U005716 | 30 |
| `packages/akari-bot-cli/tests/test_instance_notify.py` | 10 | U005717–U005726 | 471 |
| `packages/akari-bot-cli/tests/test_instance_registry.py` | 7 | U005727–U005733 | 239 |
| `packages/akari-bot-cli/tests/test_logs_cli.py` | 5 | U005734–U005738 | 184 |
| `packages/akari-bot-cli/tests/test_main.py` | 13 | U005739–U005751 | 572 |
| `packages/akari-bot-cli/tests/test_migrate_plan.py` | 3 | U005752–U005754 | 155 |
| `packages/akari-bot-cli/tests/test_module_authors.py` | 3 | U005755–U005757 | 179 |
| `packages/akari-bot-cli/tests/test_module_available.py` | 3 | U005758–U005760 | 144 |
| `packages/akari-bot-cli/tests/test_module_git.py` | 2 | U005761–U005762 | 67 |
| `packages/akari-bot-cli/tests/test_module_precheck.py` | 5 | U005763–U005767 | 204 |
| `packages/akari-bot-cli/tests/test_module_purge.py` | 2 | U005768–U005769 | 76 |

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
<<< UNIT U004564 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:26-26 >>>
# 文案与列宽随当前语言计算，常量仅保存文案键。
<<< END U004564 >>>
<<< UNIT U004565 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:31-31 >>>
# 此值用于解析 CLI 输出。显示文本使用 default_id 文案键。
<<< END U004565 >>>
<<< UNIT U004566 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:516-516 >>>
# 平台显示名可能与默认实例的 client_name 相同，不能用作其他实例的状态别名。
<<< END U004566 >>>
<<< UNIT U004567 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:623-623 >>>
# 实例根目录在每次请求时解析，使子进程目录与 AKARI_INSTANCE_DIR 跟随当前实例。
<<< END U004567 >>>
<<< UNIT U004568 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:637-637 >>>
# 配置读写与配置页共用一套实现，CLI 调用规则只有一份。
<<< END U004568 >>>
<<< UNIT U004569 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1028-1028 >>>
# noqa: BLE001 - 未挂载时按无选中处理
<<< END U004569 >>>
<<< UNIT U004570 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1107-1107 >>>
# noqa: BLE001 - 数据源异常不应中断界面
<<< END U004570 >>>
<<< UNIT U004571 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1125-1125 >>>
# 可安装清单读取失败时，仍保留实例配置与启用状态。
<<< END U004571 >>>
<<< UNIT U004572 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1132-1132 >>>
# noqa: BLE001 - 数据源异常不应中断界面
<<< END U004572 >>>
<<< UNIT U004573 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1142-1142 >>>
# noqa: BLE001 - 连接状态读取失败不应中断页面
<<< END U004573 >>>
<<< UNIT U004574 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1195-1195 >>>
# 分组标题行带禁用与样式，条目只能自建。clear() 的移除是异步的，须等移除完成再落高亮。
<<< END U004574 >>>
<<< UNIT U004575 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1206-1206 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U004575 >>>
<<< UNIT U004576 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1294-1294 >>>
# 可安装平台记录不代表已配置实例，不计入实例总数。
<<< END U004576 >>>
<<< UNIT U004577 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1347-1347 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U004577 >>>
<<< UNIT U004578 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1503-1503 >>>
# 实例此时已创建，无法读取配置项时只影响填写入口，不算新增失败。
<<< END U004578 >>>
<<< UNIT U004579 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1509-1509 >>>
# noqa: BLE001 - 数据源异常只影响表单，转成状态说明
<<< END U004579 >>>
<<< UNIT U004580 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1531-1531 >>>
# 表单打开前的重绘会用旧高亮覆盖选中键，须在关闭时再指向新实例。
<<< END U004580 >>>
<<< UNIT U004581 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1541-1541 >>>
# 表单可能修改了 enable，列表须重新读取。
<<< END U004581 >>>
<<< UNIT U004582 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1548-1548 >>>
# 可安装清单依赖 registry 来源，读取失败时仍以 core 清单为准列出已安装平台。
<<< END U004582 >>>
<<< UNIT U004583 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1570-1570 >>>
# 实例 ID 参与 target_id 前缀，必须由用户指定，创建后不可更改。
<<< END U004583 >>>
<<< UNIT U004584 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1664-1664 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U004584 >>>
<<< UNIT U004585 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1699-1699 >>>
# 未安装的适配器必须先安装，才能设置启用状态。
<<< END U004585 >>>
<<< UNIT U004586 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1739-1739 >>>
# 每个平台取一条记录，可安装清单的记录带作者信息。
<<< END U004586 >>>
<<< UNIT U004587 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1776-1776 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U004587 >>>
<<< UNIT U004588 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1798-1798 >>>
# 安装耗时较长，通过实时输出提供进度反馈。
<<< END U004588 >>>
<<< UNIT U004589 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1824-1824 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U004589 >>>
<<< UNIT U004590 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:99-99 | ctx=AdapterRecord.key >>>
选中项的稳定标识，表名优先，其次为 ``client_name``。
<<< END U004590 >>>
<<< UNIT U004591 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:104-104 | ctx=AdapterRecord.display_id >>>
返回实例列文本。未配置实例的平台为空。
<<< END U004591 >>>
<<< UNIT U004592 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:111-111 | ctx=AdapterRecord.installable >>>
返回适配器包是否需要安装。
<<< END U004592 >>>
<<< UNIT U004593 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:116-116 | ctx=AdapterRecord.listed >>>
是否显示在实例列表中。未安装且未启用的平台只在安装对话框中列出。
<<< END U004593 >>>
<<< UNIT U004594 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:121-121 | ctx=AdapterRecord.enable_label >>>
返回启用状态文本。未安装的适配器显示安装状态。
<<< END U004594 >>>
<<< UNIT U004595 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:130-130 | ctx=AdapterRecord.configured >>>
是否已有配置表。由可安装清单合成的记录没有配置。
<<< END U004595 >>>
<<< UNIT U004596 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:135-135 | ctx=AdapterRecord.listen_text >>>
监听地址列的展示文本。
<<< END U004596 >>>
<<< UNIT U004597 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:140-140 | ctx=AdapterRecord.issue_text >>>
备注列的展示文本。
<<< END U004597 >>>
<<< UNIT U004598 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:163-163 | ctx=PeerStatus.label >>>
连接列的展示文本。
<<< END U004598 >>>
<<< UNIT U004599 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:191-191 | ctx=AdapterSnapshot.grouped >>>
按平台名分组，组内保持实例顺序，组间按平台名升序。
<<< END U004599 >>>
<<< UNIT U004600 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:198-198 | ctx=AdapterSnapshot.with_available >>>
补充尚无实例记录的可安装平台。
<<< END U004600 >>>
<<< UNIT U004601 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:221-221 | ctx=PeerSnapshot.status_for >>>
返回指定 ``client_name`` 的连接状态。无记录时返回未知状态与原因。
<<< END U004601 >>>
<<< UNIT U004602 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:233-233 | ctx=AdapterSourceError >>>
数据源不可用（子进程缺失、退出码非零或输出不是 JSON）。
<<< END U004602 >>>
<<< UNIT U004603 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:290-290 | ctx=StaticAdapterSource.list_instances >>>
见 :meth:`AdapterSource.list_instances`。
<<< END U004603 >>>
<<< UNIT U004604 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:295-295 | ctx=StaticAdapterSource.list_available >>>
见 :meth:`AdapterSource.list_available`。
<<< END U004604 >>>
<<< UNIT U004605 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:300-300 | ctx=StaticAdapterSource.stream_install >>>
见 :meth:`AdapterSource.stream_install`。模拟数据源直接回放固定输出。
<<< END U004605 >>>
<<< UNIT U004606 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:308-308 | ctx=StaticAdapterSource.peer_status >>>
见 :meth:`AdapterSource.peer_status`。
<<< END U004606 >>>
<<< UNIT U004607 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:313-313 | ctx=StaticAdapterSource.add_instance >>>
见 :meth:`AdapterSource.add_instance`。
<<< END U004607 >>>
<<< UNIT U004608 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:319-319 | ctx=StaticAdapterSource.remove_instance >>>
见 :meth:`AdapterSource.remove_instance`。
<<< END U004608 >>>
<<< UNIT U004609 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:325-325 | ctx=StaticAdapterSource.config_fields >>>
见 :meth:`AdapterSource.config_fields`。
<<< END U004609 >>>
<<< UNIT U004610 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:329-329 | ctx=StaticAdapterSource.set_config >>>
见 :meth:`AdapterSource.set_config`。
<<< END U004610 >>>
<<< UNIT U004611 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:336-336 | ctx=StaticAdapterSource.set_enable >>>
见 :meth:`AdapterSource.set_enable`。成功后替换缓存中的该条记录。
<<< END U004611 >>>
<<< UNIT U004612 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:349-349 | ctx=AdapterSource >>>
适配器状态与操作的数据源接口。
<<< END U004612 >>>
<<< UNIT U004613 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:352-352 | ctx=AdapterSource.list_instances >>>
返回实例清单。
<<< END U004613 >>>
<<< UNIT U004614 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:355-355 | ctx=AdapterSource.list_available >>>
返回可安装的适配器包，含尚未安装的平台。
<<< END U004614 >>>
<<< UNIT U004615 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:358-358 | ctx=AdapterSource.stream_install >>>
安装适配器包，通过 ``on_line`` 逐行返回输出。
<<< END U004615 >>>
<<< UNIT U004616 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:361-361 | ctx=AdapterSource.peer_status >>>
返回 peer 连接状态快照。不可用时以 ``available=False`` 上报原因，不抛出异常。
<<< END U004616 >>>
<<< UNIT U004617 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:364-364 | ctx=AdapterSource.set_enable >>>
通过 CLI 设置实例的 ``enable``。
<<< END U004617 >>>
<<< UNIT U004618 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:367-367 | ctx=AdapterSource.add_instance >>>
通过 CLI 为已安装的平台新建实例配置。
<<< END U004618 >>>
<<< UNIT U004619 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:370-370 | ctx=AdapterSource.remove_instance >>>
通过 CLI 移除实例配置，保留实例数据。
<<< END U004619 >>>
<<< UNIT U004620 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:373-373 | ctx=AdapterSource.config_fields >>>
返回实例配置表的全部配置项。
<<< END U004620 >>>
<<< UNIT U004621 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:376-376 | ctx=AdapterSource.set_config >>>
通过 CLI 写入一项配置。``section`` 为 ``config set --table`` 的表引用。
<<< END U004621 >>>
<<< UNIT U004622 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:643-643 | ctx=SubprocessAdapterSource.config_fields >>>
见 :meth:`AdapterSource.config_fields`。
<<< END U004622 >>>
<<< UNIT U004623 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:647-647 | ctx=SubprocessAdapterSource.set_config >>>
见 :meth:`AdapterSource.set_config`。
<<< END U004623 >>>
<<< UNIT U004624 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:652-652 | ctx=SubprocessAdapterSource.root >>>
返回实例根目录，依次采用显式路径、当前实例或自动定位结果。
<<< END U004624 >>>
<<< UNIT U004625 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:656-656 | ctx=SubprocessAdapterSource.list_instances >>>
见 :meth:`AdapterSource.list_instances`。
<<< END U004625 >>>
<<< UNIT U004626 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:672-672 | ctx=SubprocessAdapterSource.list_available >>>
见 :meth:`AdapterSource.list_available`。复用 ``module available`` 的可安装集合。
<<< END U004626 >>>
<<< UNIT U004627 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:688-688 | ctx=SubprocessAdapterSource.stream_install >>>
通过模块数据源安装适配器，并逐行返回进度。
<<< END U004627 >>>
<<< UNIT U004628 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:694-694 | ctx=SubprocessAdapterSource.peer_status >>>
返回 peer 连接状态。入口不可用时返回原因。
<<< END U004628 >>>
<<< UNIT U004629 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:720-720 | ctx=SubprocessAdapterSource.set_enable >>>
见 :meth:`AdapterSource.set_enable`。通过 ``akaribot config set`` 写入。
<<< END U004629 >>>
<<< UNIT U004630 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:738-738 | ctx=SubprocessAdapterSource.add_instance >>>
见 :meth:`AdapterSource.add_instance`。通过 ``akaribot adapter instance add`` 新建。
<<< END U004630 >>>
<<< UNIT U004631 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:754-754 | ctx=SubprocessAdapterSource.remove_instance >>>
通过 CLI 移除适配器配置，保留实例数据。
<<< END U004631 >>>
<<< UNIT U004632 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:777-777 | ctx=SubprocessAdapterSource.cli_argv >>>
构造调用本 CLI 的 argv，规则见 :mod:`akaribot.cli.tui.cli_process`。
<<< END U004632 >>>
<<< UNIT U004633 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:781-781 | ctx=SubprocessAdapterSource.peer_argv >>>
构造使用实例解释器读取 peer 快照的命令参数。
<<< END U004633 >>>
<<< UNIT U004634 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:861-861 | ctx=ColumnLayout.widths >>>
按列序返回宽度。
<<< END U004634 >>>
<<< UNIT U004635 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:994-994 | ctx=AdaptersPage.activate >>>
首次显示时读取适配器实例。
<<< END U004635 >>>
<<< UNIT U004636 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1002-1002 | ctx=AdaptersPage.records >>>
返回缓存中的全部实例，不触发子进程。
<<< END U004636 >>>
<<< UNIT U004637 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1007-1007 | ctx=AdaptersPage.snapshot >>>
返回最近一次实例清单快照。
<<< END U004637 >>>
<<< UNIT U004638 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1012-1012 | ctx=AdaptersPage.peers >>>
返回最近一次 peer 快照。
<<< END U004638 >>>
<<< UNIT U004639 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1017-1017 | ctx=AdaptersPage.peer_note >>>
返回 peer 快照不可用的原因，可用时为空字符串。
<<< END U004639 >>>
<<< UNIT U004640 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1022-1022 | ctx=AdaptersPage.selected_record >>>
返回列表当前高亮项对应的记录。停在分组标题上时为 ``None``。
<<< END U004640 >>>
<<< UNIT U004641 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1041-1041 | ctx=AdaptersPage.header_text >>>
返回列标题行当前文本。
<<< END U004641 >>>
<<< UNIT U004642 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1046-1046 | ctx=AdaptersPage.status_text >>>
返回状态栏当前文本。
<<< END U004642 >>>
<<< UNIT U004643 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1051-1051 | ctx=AdaptersPage.summary_text >>>
返回顶部摘要当前文本。
<<< END U004643 >>>
<<< UNIT U004644 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1056-1056 | ctx=AdaptersPage.detail_text >>>
返回详情栏当前文本。
<<< END U004644 >>>
<<< UNIT U004645 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1060-1060 | ctx=AdaptersPage.row_texts >>>
返回最近一次渲染出的全部行文本，包含分组标题行。
<<< END U004645 >>>
<<< UNIT U004646 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1064-1064 | ctx=AdaptersPage.group_titles >>>
返回最近一次渲染出的分组标题行文本。
<<< END U004646 >>>
<<< UNIT U004647 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1068-1068 | ctx=AdaptersPage.instance_cells >>>
返回最近一次渲染出的实例行各列取值，顺序与列表一致。
<<< END U004647 >>>
<<< UNIT U004648 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1072-1072 | ctx=AdaptersPage.cache_age >>>
返回缓存自上次读取以来的秒数。从未读取时为无穷大。
<<< END U004648 >>>
<<< UNIT U004649 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1146-1146 | ctx=AdaptersPage.invalidate_cache >>>
清除缓存有效期，使下次请求重新读取数据。
<<< END U004649 >>>
<<< UNIT U004650 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1457-1457 | ctx=AdaptersPage.request_add_instance >>>
弹出新增实例对话框，供选择已安装的平台并填写实例 ID。
<<< END U004650 >>>
<<< UNIT U004651 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1580-1580 | ctx=AdaptersPage.request_remove_instance >>>
请求确认移除实例配置，忽略防抖窗口内的重复请求。
<<< END U004651 >>>
<<< UNIT U004652 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1605-1605 | ctx=AdaptersPage.reset_pending >>>
作废待确认的移除。切换页面、刷新与更换选中项时调用。
<<< END U004652 >>>
<<< UNIT U004653 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1688-1688 | ctx=AdaptersPage.request_toggle >>>
切换所选实例的启用状态。无选中项时显示提示。
<<< END U004653 >>>
<<< UNIT U004654 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1705-1705 | ctx=AdaptersPage.request_install >>>
弹出安装对话框，列出尚未安装的适配器。当前行未安装时预选该平台。
<<< END U004654 >>>
<<< UNIT U004655 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1849-1849 | ctx=AdaptersPage.focus_primary >>>
聚焦适配器列表。列表为空时聚焦页面容器。
<<< END U004655 >>>
<<< UNIT U004656 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/adapters.py:1873-1873 | ctx=AdaptersPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U004656 >>>
<<< UNIT U004657 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:29-29 >>>
# key 同时用于控件 id（page-<key> / nav-<key>），第二项是侧栏标题的文案键。
<<< END U004657 >>>
<<< UNIT U004658 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:45-45 >>>
# 侧栏分组同时决定阅读顺序与键盘翻页顺序。
<<< END U004658 >>>
<<< UNIT U004659 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:53-53 >>>
# 页面用途说明显示在快捷键帮助中。
<<< END U004659 >>>
<<< UNIT U004660 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:69-69 >>>
# 分组标题参与侧栏索引，页面按 NAV_GROUPS 顺序排列。
<<< END U004660 >>>
<<< UNIT U004661 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:78-78 >>>
# 侧栏包含分组标题，索引需按 NAV_PLAN 计算。
<<< END U004661 >>>
<<< UNIT U004662 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:83-83 >>>
# 返回条目所属分组标题在 NAV_PLAN 中的下标，分组标题返回自身。
<<< END U004662 >>>
<<< UNIT U004663 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:97-97 >>>
# 左右键沿用树形导航习惯，在页面条目上按左键同样折叠其所属分组。
<<< END U004663 >>>
<<< UNIT U004664 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:193-193 >>>
# 文案在类创建时取值，因为 main.py 的 --lang 早于界面模块导入，改语言需重启进程。
<<< END U004664 >>>
<<< UNIT U004665 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:198-198 >>>
# 页面快捷键由各页声明，防止应用级绑定触发隐藏页面的操作。
<<< END U004665 >>>
<<< UNIT U004666 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:204-204 >>>
# 页脚空间有限，页面切换快捷键仅在帮助中显示。
<<< END U004666 >>>
<<< UNIT U004667 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:220-220 >>>
# 首次解析样式表前必须注册主题，以提供 $primary 等变量。
<<< END U004667 >>>
<<< UNIT U004668 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:223-223 >>>
# 数据源支持注入，以便在无界面测试中隔离子进程。
<<< END U004668 >>>
<<< UNIT U004669 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:234-234 >>>
# 折叠状态仅在本次会话内有效，切换实例不重建侧栏，状态随之保留。
<<< END U004669 >>>
<<< UNIT U004670 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:239-239 >>>
# 名称优先采用注册表记录，未记录时使用目录名。
<<< END U004670 >>>
<<< UNIT U004671 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:245-245 >>>
# noqa: BLE001 - 注册表不可用时回退到路径名
<<< END U004671 >>>
<<< UNIT U004672 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:252-252 >>>
# 标题栏标识当前实例，便于确认配置与数据操作的目标。
<<< END U004672 >>>
<<< UNIT U004673 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:325-325 >>>
# 分组标题可高亮，选中时折叠或展开本组，不切换页面。
<<< END U004673 >>>
<<< UNIT U004674 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:350-350 >>>
# 概览页另有实例清单与服务控制两个数据源，键为 dashboard_instances / dashboard_service。
<<< END U004674 >>>
<<< UNIT U004675 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:364-364 >>>
# 各页自行声明 __init__ 签名（不接受 classes），故样式类在此追加。
<<< END U004675 >>>
<<< UNIT U004676 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:366-366 >>>
# 统一保护渲染入口，避免异步读取在页面卸载后访问控件。
<<< END U004676 >>>
<<< UNIT U004677 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:413-413 >>>
# Textual 的默认聚焦发生在挂载后，页面焦点需在首帧之后设置。
<<< END U004677 >>>
<<< UNIT U004678 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:417-417 >>>
# 启动信息通过通知显示，以支持任意初始页面。
<<< END U004678 >>>
<<< UNIT U004679 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:423-423 >>>
# 待确认状态由实现 reset_pending() 的页面管理。
<<< END U004679 >>>
<<< UNIT U004680 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:426-426 >>>
# noqa: BLE001 - 页面尚未挂载时无需复位
<<< END U004680 >>>
<<< UNIT U004681 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:432-432 >>>
# 页面通过 dirty_note() 提供未保存更改摘要。
<<< END U004681 >>>
<<< UNIT U004682 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:438-438 >>>
# noqa: BLE001 - 未挂载页面无编辑状态
<<< END U004682 >>>
<<< UNIT U004683 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:460-460 >>>
# 切换页面会改变操作上下文，须清除待确认状态。
<<< END U004683 >>>
<<< UNIT U004684 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:462-462 >>>
# 先显示并聚焦目标页，避免隐藏旧页时 Textual 将焦点分配给隐藏容器。
<<< END U004684 >>>
<<< UNIT U004685 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:465-465 >>>
# 仅激活可见页面，避免隐藏页执行无关的读取与轮询。
<<< END U004685 >>>
<<< UNIT U004686 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:476-476 >>>
# 仅在索引变化时更新，避免侧栏事件重复触发页面同步。
<<< END U004686 >>>
<<< UNIT U004687 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:480-480 >>>
# 当前页所在分组已折叠时高亮分组标题，不擅自展开用户折叠的分组。
<<< END U004687 >>>
<<< UNIT U004688 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:501-501 >>>
# 先移走高亮再禁用条目，避免高亮停留在隐藏的页面条目上。
<<< END U004688 >>>
<<< UNIT U004689 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/app.py:504-504 >>>
# 禁用的条目会被方向键跳过，隐藏不足以阻止高亮移到其上。
<<< END U004689 >>>
<<< UNIT U004690 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:1-1 | ctx=<module> >>>
TUI 应用装配、页面注册、全局快捷键与启动入口。
<<< END U004690 >>>
<<< UNIT U004691 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:104-104 | ctx=_NavList.action_fold_group >>>
折叠高亮条目所属分组的键位动作。
<<< END U004691 >>>
<<< UNIT U004692 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:109-109 | ctx=_NavList.action_unfold_group >>>
展开高亮分组标题的键位动作。
<<< END U004692 >>>
<<< UNIT U004693 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:176-176 | ctx=stylesheet_summary >>>
返回样式表来源、长度与摘要，供 ``tui --self-check`` 打印。
<<< END U004693 >>>
<<< UNIT U004694 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:264-264 | ctx=TuiApp.action_next_page >>>
切换到下一个页面的键位动作。
<<< END U004694 >>>
<<< UNIT U004695 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:268-268 | ctx=TuiApp.action_previous_page >>>
切换到上一个页面的键位动作。
<<< END U004695 >>>
<<< UNIT U004696 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:277-277 | ctx=TuiApp.action_show_help >>>
列出当前页与全局键位的键位动作。
<<< END U004696 >>>
<<< UNIT U004697 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:304-304 | ctx=TuiApp.action_toggle_theme >>>
在品牌深色与浅色主题之间切换的键位动作。
<<< END U004697 >>>
<<< UNIT U004698 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:315-315 | ctx=TuiApp.compose >>>
装配侧栏与全部页面。
<<< END U004698 >>>
<<< UNIT U004699 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:407-407 | ctx=TuiApp.on_mount >>>
记录启动耗时、显示初始页面并设置焦点。
<<< END U004699 >>>
<<< UNIT U004700 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:449-449 | ctx=TuiApp.focus_active_page >>>
将焦点移至当前页的主控件。
<<< END U004700 >>>
<<< UNIT U004701 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:521-521 | ctx=TuiApp.page >>>
按 key 获取页面控件，供测试与键位动作使用。
<<< END U004701 >>>
<<< UNIT U004702 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:528-528 | ctx=TuiApp.modules_page >>>
返回 Modules 页控件。
<<< END U004702 >>>
<<< UNIT U004703 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:532-532 | ctx=TuiApp.action_quit >>>
退出应用。未保存更改或后台任务存在时请求确认。
<<< END U004703 >>>
<<< UNIT U004704 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/app.py:598-598 | ctx=TuiRunResult.summary >>>
返回单行文字摘要。
<<< END U004704 >>>
<<< UNIT U004705 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/cli_process.py:13-13 >>>
# 显式指定 CLI 入口，供自检与冻结产物使用。
<<< END U004705 >>>
<<< UNIT U004706 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/cli_process.py:44-44 >>>
# 子进程输出含中文与 JSON，Windows 控制台默认代码页可能是 GBK，两侧编码不一致会得到乱码或解析失败。
<<< END U004706 >>>
<<< UNIT U004707 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:42-42 >>>
# 类型标签保存文案键，按当前语言解析。
<<< END U004707 >>>
<<< UNIT U004708 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:51-51 >>>
# 类型名归一化时，由于 schema 的 type 取自运行时值的 __name__ 且会随模板写法变化，故按子串匹配。
<<< END U004708 >>>
<<< UNIT U004709 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:68-68 >>>
# 表名与配置文件一一对应，config.toml 同时承载 config 与 secret 两段。
<<< END U004709 >>>
<<< UNIT U004710 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:73-73 >>>
# region 外部编辑器
<<< END U004710 >>>
<<< UNIT U004711 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:107-107 >>>
# 标准输入必须连接终端，否则外部编辑器无法交互。
<<< END U004711 >>>
<<< UNIT U004712 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:114-114 >>>
# region 字段模型与值文本
<<< END U004712 >>>
<<< UNIT U004713 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:395-395 >>>
# region 原始文本的解析与摊平
<<< END U004713 >>>
<<< UNIT U004714 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:438-438 >>>
# tomlkit 对文件尾部的未闭合结构会报回第 1 行第 0 列，此处校正到最后一行。
<<< END U004714 >>>
<<< UNIT U004715 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:476-476 >>>
# noqa: BLE001 - 解析器的其他异常同样只用于展示，不应中断界面
<<< END U004715 >>>
<<< UNIT U004716 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:554-554 >>>
# region 数据源
<<< END U004716 >>>
<<< UNIT U004717 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:665-665 >>>
# 每次读取时解析实例根目录，确保切换实例后使用当前实例的配置。
<<< END U004717 >>>
<<< UNIT U004718 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:714-714 >>>
# noqa: BLE001 - 对端实现未知，统一转成可展示的结果
<<< END U004718 >>>
<<< UNIT U004719 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:784-784 >>>
# noqa: BLE001 - 对端实现未知，统一转成可展示的错误
<<< END U004719 >>>
<<< UNIT U004720 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:806-806 >>>
# noqa: BLE001 - 定位失败按“没有实例”处理，由调用方给出提示
<<< END U004720 >>>
<<< UNIT U004721 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:824-824 >>>
# noqa: BLE001 - 实例构造失败同样只作为降级原因上报
<<< END U004721 >>>
<<< UNIT U004722 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:923-923 >>>
# region 控件
<<< END U004722 >>>
<<< UNIT U004723 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:927-927 >>>
# 原生控件是否可用由兼容实现决定，页面通过属性检测选择实现。
<<< END U004723 >>>
<<< UNIT U004724 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:992-992 >>>
# noqa: BLE001 - 未挂载时按无按钮处理
<<< END U004724 >>>
<<< UNIT U004725 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1125-1125 >>>
# 未更改的字段保留原值，避免将表单不支持的嵌套结构提交给 ``config set``。
<<< END U004725 >>>
<<< UNIT U004726 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1227-1227 >>>
# 占位符不进入输入框，留空即未填写，既不必先删除模板文字，也不会把占位符写回配置。
<<< END U004726 >>>
<<< UNIT U004727 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1287-1287 >>>
# noqa: BLE001 - 数据源任意异常都转成行内错误
<<< END U004727 >>>
<<< UNIT U004728 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1292-1292 >>>
# 密钥项只提供概括说明，避免命令输出回显写入的值。
<<< END U004728 >>>
<<< UNIT U004729 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1408-1408 >>>
# noqa: BLE001 - 未挂载时按无 TextArea 处理
<<< END U004729 >>>
<<< UNIT U004730 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1421-1421 >>>
# region 页面
<<< END U004730 >>>
<<< UNIT U004731 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1431-1431 >>>
# 限制按钮最小宽度，确保 80 列终端能够显示全部操作。
<<< END U004731 >>>
<<< UNIT U004732 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1501-1501 >>>
# 文案在类创建时取值，因为 main.py 的 --lang 早于界面模块导入，改语言需重启进程。
<<< END U004732 >>>
<<< UNIT U004733 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1504-1504 >>>
# 低频操作由底部按钮栏提供入口，页脚为全局键位保留空间。
<<< END U004733 >>>
<<< UNIT U004734 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1506-1506 >>>
# 保存使用 ctrl+s，因为表单输入框聚焦时单字母由输入框接收，而组合键在编辑中同样生效。
<<< END U004734 >>>
<<< UNIT U004735 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1542-1542 >>>
# 终端挂起和编辑器启动允许注入模拟对象，避免自动化测试启动交互进程。
<<< END U004735 >>>
<<< UNIT U004736 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1549-1549 >>>
# 顶部只放视图切换与表概况，动作统一在底部按钮栏。
<<< END U004736 >>>
<<< UNIT U004737 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1585-1585 >>>
# region 状态读取（供测试与 App 使用）
<<< END U004737 >>>
<<< UNIT U004738 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1658-1658 >>>
# 重新挂载期间输入控件可能尚未创建，此时使用载入值。
<<< END U004738 >>>
<<< UNIT U004739 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1661-1661 >>>
# noqa: BLE001 - 未装配完成的行不构成脏值
<<< END U004739 >>>
<<< UNIT U004740 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1684-1684 >>>
# noqa: BLE001 - 没有提示控件时按空字符串处理
<<< END U004740 >>>
<<< UNIT U004741 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1686-1686 >>>
# ``Static.content`` 是 update() 传进来的原对象，文本控件收到的是 rich 的 Text。
<<< END U004741 >>>
<<< UNIT U004742 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1692-1692 >>>
# region 读取与渲染
<<< END U004742 >>>
<<< UNIT U004743 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1699-1699 >>>
# 强制刷新会重建编辑区，必须确认未保存更改的处理方式。
<<< END U004743 >>>
<<< UNIT U004744 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1718-1718 >>>
# noqa: BLE001 - 数据源任意异常都不应中断界面
<<< END U004744 >>>
<<< UNIT U004745 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1762-1762 >>>
# noqa: BLE001 - 读取数据失败只影响本页展示
<<< END U004745 >>>
<<< UNIT U004746 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1791-1791 >>>
# noqa: BLE001 - 读文件失败同样只影响展示
<<< END U004746 >>>
<<< UNIT U004747 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1875-1875 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U004747 >>>
<<< UNIT U004748 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1914-1914 >>>
# region 保存
<<< END U004748 >>>
<<< UNIT U004749 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:1986-1986 >>>
# noqa: BLE001 - 数据源任意异常都转成失败项展示
<<< END U004749 >>>
<<< UNIT U004750 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:2036-2036 >>>
# region 交互
<<< END U004750 >>>
<<< UNIT U004751 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:2090-2090 >>>
# 重建编辑区前必须确认未保存更改的处理方式。
<<< END U004751 >>>
<<< UNIT U004752 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:2100-2100 >>>
# 刷新会触发切换任务，使用独立任务组避免自我取消。
<<< END U004752 >>>
<<< UNIT U004753 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:2126-2126 >>>
# noqa: BLE001 - 行未装配完成时没有可回退的控件
<<< END U004753 >>>
<<< UNIT U004754 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:2132-2132 >>>
# 保留更改时恢复当前表的高亮，确保选中项与编辑内容一致。
<<< END U004754 >>>
<<< UNIT U004755 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/config.py:2163-2163 >>>
# noqa: BLE001 - 文件定位失败由调用方显示错误
<<< END U004755 >>>
<<< UNIT U004756 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:133-133 | ctx=kind_of_value >>>
按运行时值的 Python 类型推断归一化类型。
<<< END U004756 >>>
<<< UNIT U004757 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:188-188 | ctx=edit_text >>>
把值渲染为输入框中的文本，列表按中英文逗号分隔，其余同 :func:`write_text`。
<<< END U004757 >>>
<<< UNIT U004758 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:237-237 | ctx=ConfigField.kind_label >>>
返回类型的本地化标签。未知类型附带原始类型名。
<<< END U004758 >>>
<<< UNIT U004759 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:245-245 | ctx=ConfigField.section >>>
返回 ``config set --table`` 用的表引用，密钥段带 ``_secret`` 后缀。
<<< END U004759 >>>
<<< UNIT U004760 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:252-252 | ctx=ConfigField.edit_value >>>
返回输入控件中的初始文本。
<<< END U004760 >>>
<<< UNIT U004761 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:257-257 | ctx=ConfigField.write_value >>>
返回当前值对应的写入文本，也用于判断字段是否被更改。
<<< END U004761 >>>
<<< UNIT U004762 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:262-262 | ctx=ConfigField.help_text >>>
返回帮助文本。优先使用注释，空值时补充默认值。
<<< END U004762 >>>
<<< UNIT U004763 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:270-270 | ctx=ConfigField.marks >>>
返回表头中的本地化徽标（密钥与待填写）。
<<< END U004763 >>>
<<< UNIT U004764 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:429-429 | ctx=RawEntry.label >>>
返回“表.键=值”形式的一行说明。
<<< END U004764 >>>
<<< UNIT U004765 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:558-558 | ctx=ConfigSourceError >>>
数据源不可用（子进程缺失、退出码非零或输出不是 JSON）。
<<< END U004765 >>>
<<< UNIT U004766 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:603-603 | ctx=StaticConfigSource.list_tables >>>
见 :meth:`ConfigSource.list_tables`。
<<< END U004766 >>>
<<< UNIT U004767 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:608-608 | ctx=StaticConfigSource.schema >>>
见 :meth:`ConfigSource.schema`。
<<< END U004767 >>>
<<< UNIT U004768 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:613-613 | ctx=StaticConfigSource.read_raw >>>
见 :meth:`ConfigSource.read_raw`。
<<< END U004768 >>>
<<< UNIT U004769 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:618-618 | ctx=StaticConfigSource.set_value >>>
见 :meth:`ConfigSource.set_value`。
<<< END U004769 >>>
<<< UNIT U004770 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:624-624 | ctx=StaticConfigSource.config_file >>>
见 :meth:`ConfigSource.config_file`。
<<< END U004770 >>>
<<< UNIT U004771 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:630-630 | ctx=ConfigSource >>>
配置数据源接口。测试注入模拟对象，实际运行通过子进程访问。
<<< END U004771 >>>
<<< UNIT U004772 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:633-633 | ctx=ConfigSource.list_tables >>>
返回实例内的全部配置表名。
<<< END U004772 >>>
<<< UNIT U004773 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:636-636 | ctx=ConfigSource.schema >>>
返回一张表的全部字段。
<<< END U004773 >>>
<<< UNIT U004774 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:639-639 | ctx=ConfigSource.read_raw >>>
返回一张表的原始 TOML 文本，只供展示与编辑。
<<< END U004774 >>>
<<< UNIT U004775 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:642-642 | ctx=ConfigSource.set_value >>>
写入一项。``section`` 为 ``config set --table`` 的表引用。
<<< END U004775 >>>
<<< UNIT U004776 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:645-645 | ctx=ConfigSource.config_file >>>
返回一张表对应的配置文件路径。定位不到实例时返回 ``None``。
<<< END U004776 >>>
<<< UNIT U004777 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:676-676 | ctx=SubprocessConfigSource.root >>>
返回实例根目录路径，显式给定优先，其次为界面当前选中的实例，最后自动定位。
<<< END U004777 >>>
<<< UNIT U004778 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:680-680 | ctx=SubprocessConfigSource.list_tables >>>
见 :meth:`ConfigSource.list_tables`。
<<< END U004778 >>>
<<< UNIT U004779 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:691-691 | ctx=SubprocessConfigSource.schema >>>
见 :meth:`ConfigSource.schema`。
<<< END U004779 >>>
<<< UNIT U004780 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:696-696 | ctx=SubprocessConfigSource.read_raw >>>
见 :meth:`ConfigSource.read_raw`。
<<< END U004780 >>>
<<< UNIT U004781 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:710-710 | ctx=SubprocessConfigSource.set_value >>>
见 :meth:`ConfigSource.set_value`。
<<< END U004781 >>>
<<< UNIT U004782 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:737-737 | ctx=SubprocessConfigSource.cli_argv >>>
构造调用本 CLI 的 argv，规则见 :mod:`akaribot.cli.tui.cli_process`。
<<< END U004782 >>>
<<< UNIT U004783 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:958-958 | ctx=BoolToggle.compose >>>
装配开关按钮与状态说明。
<<< END U004783 >>>
<<< UNIT U004784 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:963-963 | ctx=BoolToggle.on_button_pressed >>>
切换开关。事件不再上传，避免被所在页面当作动作按钮处理。
<<< END U004784 >>>
<<< UNIT U004785 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:969-969 | ctx=BoolToggle.value >>>
返回当前值。
<<< END U004785 >>>
<<< UNIT U004786 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:973-973 | ctx=BoolToggle.label_text >>>
返回按钮文字，开与关以符号区分。
<<< END U004786 >>>
<<< UNIT U004787 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:977-977 | ctx=BoolToggle.set_value >>>
设置值并刷新按钮外观。
<<< END U004787 >>>
<<< UNIT U004788 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:986-986 | ctx=BoolToggle.toggle >>>
在开与关之间切换。
<<< END U004788 >>>
<<< UNIT U004789 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1042-1042 | ctx=FieldRow.compose >>>
按字段类型装配控件。密钥用密码框，占位符另起一行高亮提示。
<<< END U004789 >>>
<<< UNIT U004790 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1070-1070 | ctx=FieldRow.control >>>
返回本行的输入控件。
<<< END U004790 >>>
<<< UNIT U004791 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1075-1075 | ctx=FieldRow.text >>>
返回控件中的当前编辑文本。
<<< END U004791 >>>
<<< UNIT U004792 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1084-1084 | ctx=FieldRow.set_text >>>
设置控件文本，等价于用户键入。
<<< END U004792 >>>
<<< UNIT U004793 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1094-1094 | ctx=FieldRow.toggle >>>
切换布尔控件。非布尔行不执行操作。
<<< END U004793 >>>
<<< UNIT U004794 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1100-1100 | ctx=FieldRow.focus_control >>>
聚焦本行控件。
<<< END U004794 >>>
<<< UNIT U004795 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1106-1106 | ctx=FieldRow.show_error >>>
在行内显示校验错误。
<<< END U004795 >>>
<<< UNIT U004796 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1111-1111 | ctx=FieldRow.clear_error >>>
清空行内校验错误。
<<< END U004796 >>>
<<< UNIT U004797 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1210-1210 | ctx=ConfigFormScreen.compose >>>
装配说明、可滚动的字段区、状态行与按钮。
<<< END U004797 >>>
<<< UNIT U004798 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1233-1233 | ctx=ConfigFormScreen.on_mount >>>
聚焦首个字段。
<<< END U004798 >>>
<<< UNIT U004799 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1239-1239 | ctx=ConfigFormScreen.rows >>>
返回全部表单行。
<<< END U004799 >>>
<<< UNIT U004800 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1244-1244 | ctx=ConfigFormScreen.status_text >>>
返回状态行当前文本。
<<< END U004800 >>>
<<< UNIT U004801 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1251-1251 | ctx=ConfigFormScreen.on_input_submitted >>>
回车移到下一项。保存须明确触发，避免填到一半就写入。
<<< END U004801 >>>
<<< UNIT U004802 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1255-1255 | ctx=ConfigFormScreen.on_button_pressed >>>
保存或稍后填写。
<<< END U004802 >>>
<<< UNIT U004803 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1262-1262 | ctx=ConfigFormScreen.key_escape >>>
Esc 等同稍后填写。
<<< END U004803 >>>
<<< UNIT U004804 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1266-1266 | ctx=ConfigFormScreen.action_save >>>
校验并写入被更改的项。全部成功后关闭。
<<< END U004804 >>>
<<< UNIT U004805 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1308-1308 | ctx=ConfigFormScreen.request_close >>>
关闭对话框。有未写入的内容时先确认放弃。
<<< END U004805 >>>
<<< UNIT U004806 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1347-1347 | ctx=RawTextEditor.degraded >>>
是否处于降级实现（``_compat`` 未导出 ``TextArea``）。
<<< END U004806 >>>
<<< UNIT U004807 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1351-1351 | ctx=RawTextEditor.compose >>>
装配编辑区，使用原生 ``TextArea`` 或“操作按钮 + 逐行输入框”。
<<< END U004807 >>>
<<< UNIT U004808 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1368-1368 | ctx=RawTextEditor.text >>>
返回编辑区当前文本。
<<< END U004808 >>>
<<< UNIT U004809 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1375-1375 | ctx=RawTextEditor.load_text >>>
用新文本替换编辑区内容。
<<< END U004809 >>>
<<< UNIT U004810 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1384-1384 | ctx=RawTextEditor.append_line >>>
在末尾追加一空行。
<<< END U004810 >>>
<<< UNIT U004811 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1393-1393 | ctx=RawTextEditor.remove_last_line >>>
删除末尾一行。只剩一行时清空该行。
<<< END U004811 >>>
<<< UNIT U004812 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1548-1548 | ctx=ConfigPage.compose >>>
装配页面控件树，包含工具条、配置表列表、表单区、文本区与状态栏。
<<< END U004812 >>>
<<< UNIT U004813 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1575-1575 | ctx=ConfigPage.on_mount >>>
挂载后只装配控件。读取数据推迟到首次显示。
<<< END U004813 >>>
<<< UNIT U004814 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1579-1579 | ctx=ConfigPage.activate >>>
首次显示时读取配置表列表。
<<< END U004814 >>>
<<< UNIT U004815 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1589-1589 | ctx=ConfigPage.tables >>>
返回缓存中的配置表列表，不触发子进程。
<<< END U004815 >>>
<<< UNIT U004816 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1594-1594 | ctx=ConfigPage.selected_table >>>
返回当前表的表名。
<<< END U004816 >>>
<<< UNIT U004817 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1599-1599 | ctx=ConfigPage.fields >>>
返回当前表的字段。
<<< END U004817 >>>
<<< UNIT U004818 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1604-1604 | ctx=ConfigPage.mode >>>
返回当前模式（``form`` 或 ``raw``）。
<<< END U004818 >>>
<<< UNIT U004819 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1609-1609 | ctx=ConfigPage.status_text >>>
返回状态栏当前文本。
<<< END U004819 >>>
<<< UNIT U004820 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1614-1614 | ctx=ConfigPage.caption_text >>>
返回表头上方摘要栏当前文本。
<<< END U004820 >>>
<<< UNIT U004821 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1619-1619 | ctx=ConfigPage.saved_entries >>>
返回最近一次保存写入的“表.键=值”列表。
<<< END U004821 >>>
<<< UNIT U004822 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1624-1624 | ctx=ConfigPage.skipped_notes >>>
返回最近一次保存中跳过项的说明。
<<< END U004822 >>>
<<< UNIT U004823 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1628-1628 | ctx=ConfigPage.cache_age >>>
返回配置表列表缓存自上次读取以来的秒数。从未读取时为无穷大。
<<< END U004823 >>>
<<< UNIT U004824 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1634-1634 | ctx=ConfigPage.field_rows >>>
返回表单区中的全部字段行（按渲染顺序）。
<<< END U004824 >>>
<<< UNIT U004825 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1638-1638 | ctx=ConfigPage.row_for >>>
按键名获取字段行，未找到时返回 ``None``。
<<< END U004825 >>>
<<< UNIT U004826 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1645-1645 | ctx=ConfigPage.is_dirty >>>
判断是否存在未保存的编辑，表单行与原始文本任一与载入值不同即为真。
<<< END U004826 >>>
<<< UNIT U004827 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1652-1652 | ctx=ConfigPage.dirty_note >>>
返回未保存更改的说明。没有更改时为空字符串。
<<< END U004827 >>>
<<< UNIT U004828 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1665-1665 | ctx=ConfigPage.raw_editor >>>
返回原始文本编辑区。
<<< END U004828 >>>
<<< UNIT U004829 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1669-1669 | ctx=ConfigPage.table_row_texts >>>
返回最近一次渲染出的配置表列表行文本，供自动化检查核对宽度。
<<< END U004829 >>>
<<< UNIT U004830 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1673-1673 | ctx=ConfigPage.header_texts >>>
返回各字段行的表头文本，供自动化检查核对列对齐。
<<< END U004830 >>>
<<< UNIT U004831 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1677-1677 | ctx=ConfigPage.help_texts >>>
返回各字段行的帮助文本，即配置模板的 i18n 注释。
<<< END U004831 >>>
<<< UNIT U004832 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1681-1681 | ctx=ConfigPage.form_hint >>>
返回表单区当前显示的提示文本。正在显示字段时为空字符串。
<<< END U004832 >>>
<<< UNIT U004833 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1713-1713 | ctx=ConfigPage.reload_tables >>>
后台读取配置表列表并载入当前表，返回是否成功。
<<< END U004833 >>>
<<< UNIT U004834 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1828-1828 | ctx=ConfigPage.invalidate_cache >>>
使字段缓存失效。``table`` 为 ``None`` 时清空全部。
<<< END U004834 >>>
<<< UNIT U004835 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1838-1838 | ctx=ConfigPage.reload >>>
作废缓存并重新读取配置表列表与当前表。
<<< END U004835 >>>
<<< UNIT U004836 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:1908-1908 | ctx=ConfigPage.on_resize >>>
终端尺寸变化时按缓存重新排列配置表列表，不重新读取数据。
<<< END U004836 >>>
<<< UNIT U004837 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:2137-2137 | ctx=ConfigPage.action_save >>>
保存当前表的键位动作。
<<< END U004837 >>>
<<< UNIT U004838 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:2141-2141 | ctx=ConfigPage.action_reload >>>
作废缓存并重新加载的键位动作。
<<< END U004838 >>>
<<< UNIT U004839 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:2145-2145 | ctx=ConfigPage.action_mode_form >>>
切换到表单模式的键位动作。
<<< END U004839 >>>
<<< UNIT U004840 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:2149-2149 | ctx=ConfigPage.action_mode_raw >>>
切换到原始文本模式的键位动作。
<<< END U004840 >>>
<<< UNIT U004841 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:2213-2213 | ctx=ConfigPage.action_open_editor >>>
用外部编辑器打开当前表配置文件的键位动作。
<<< END U004841 >>>
<<< UNIT U004842 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:2217-2217 | ctx=ConfigPage.focus_primary >>>
聚焦配置表列表。列表为空时聚焦页面容器。
<<< END U004842 >>>
<<< UNIT U004843 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:2221-2221 | ctx=ConfigPage.action_focus_tables >>>
聚焦配置表列表的键位动作。
<<< END U004843 >>>
<<< UNIT U004844 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/config.py:2225-2225 | ctx=ConfigPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U004844 >>>
<<< UNIT U004845 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/context.py:16-16 | ctx=active_root >>>
返回界面当前选中的实例根目录。未选过时为 ``None``。
<<< END U004845 >>>
<<< UNIT U004846 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:32-32 >>>
# 标签须按当前语言解析，因此常量只保存文案键。
<<< END U004846 >>>
<<< UNIT U004847 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:51-51 >>>
# 切换实例会重新挂载页面，操作记录保存在应用上以供新页面读取。
<<< END U004847 >>>
<<< UNIT U004848 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:55-55 >>>
# 实例创建包含依赖解析与安装，超时须覆盖下载耗时。
<<< END U004848 >>>
<<< UNIT U004849 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:96-96 >>>
# bool 是 int 的子类，计数字段须显式排除布尔值。
<<< END U004849 >>>
<<< UNIT U004850 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:109-109 >>>
# 配置模板的占位符包含类型说明，估算时须匹配完整标记。
<<< END U004850 >>>
<<< UNIT U004851 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:420-420 >>>
# 目标目录由 init 创建，子进程须以父目录作为工作目录。
<<< END U004851 >>>
<<< UNIT U004852 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:484-484 >>>
# 当前实例可能尚未注册，清单须包含该实例。
<<< END U004852 >>>
<<< UNIT U004853 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:632-632 >>>
# 诊断发现错误时返回非零退出码，但标准输出仍包含有效统计。
<<< END U004853 >>>
<<< UNIT U004854 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:702-702 >>>
# core 统计不可用时按配置标记估算，摘要须注明估算方式。
<<< END U004854 >>>
<<< UNIT U004855 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:771-771 >>>
# noqa: BLE001 - 探测失败按未知处理，不应中断界面
<<< END U004855 >>>
<<< UNIT U004856 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:917-917 >>>
# noqa: BLE001 - 降级到本地锁探测，不中断界面
<<< END U004856 >>>
<<< UNIT U004857 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:935-935 >>>
# noqa: BLE001 - 模拟对象失败同样只降级
<<< END U004857 >>>
<<< UNIT U004858 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:947-947 >>>
# noqa: BLE001 - 实例构造失败只作为降级原因
<<< END U004858 >>>
<<< UNIT U004859 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:960-960 >>>
# noqa: BLE001 - 元数据失败不应让整页空白
<<< END U004859 >>>
<<< UNIT U004860 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:980-980 >>>
# noqa: BLE001 - 失败只写入来源说明
<<< END U004860 >>>
<<< UNIT U004861 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1008-1008 >>>
# noqa: BLE001 - 探测失败不影响其余字段
<<< END U004861 >>>
<<< UNIT U004862 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1111-1112 >>>
# 文案在类定义时解析，更改 --lang 后须重启进程。
# 低频键位通过按钮和帮助提供，避免页脚超出 80 列。
<<< END U004862 >>>
<<< UNIT U004863 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1191-1191 >>>
# CSS 不接受值为零的 line-pad，须通过样式对象设置，确保单行按钮的标签可见。
<<< END U004863 >>>
<<< UNIT U004864 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1224-1224 >>>
# noqa: BLE001 - 注册表不可用仅显示错误提示
<<< END U004864 >>>
<<< UNIT U004865 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1232-1232 >>>
# 清单变化可能使待确认目标失效，须重新确认。
<<< END U004865 >>>
<<< UNIT U004866 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1243-1243 >>>
# noqa: BLE001 - 未挂载时按无选中处理
<<< END U004866 >>>
<<< UNIT U004867 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1266-1266 >>>
# 重建列表恢复高亮时，不应使确认状态失效。
<<< END U004867 >>>
<<< UNIT U004868 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1289-1289 >>>
# 统一解析真实路径，避免将同一目录的符号链接视为不同实例。
<<< END U004868 >>>
<<< UNIT U004869 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1314-1314 >>>
# 切换确认前不得修改默认实例，以免丢失未保存的更改。
<<< END U004869 >>>
<<< UNIT U004870 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1324-1324 >>>
# CLI 读取注册表中的默认实例，切换结果须同步写入。
<<< END U004870 >>>
<<< UNIT U004871 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1331-1331 >>>
# 同一目标只启动一次注册表写入进程。
<<< END U004871 >>>
<<< UNIT U004872 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1335-1335 >>>
# 任务由应用持有，避免页面重新挂载时取消注册表写入。
<<< END U004872 >>>
<<< UNIT U004873 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1348-1348 >>>
# 页面重新挂载会清除状态栏，因此结果通过应用通知显示。
<<< END U004873 >>>
<<< UNIT U004874 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1353-1353 >>>
# 写入失败后清除请求记录，允许重试。
<<< END U004874 >>>
<<< UNIT U004875 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1413-1413 >>>
# noqa: BLE001 - 服务状态读取失败仅显示错误说明
<<< END U004875 >>>
<<< UNIT U004876 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1437-1437 >>>
# 首次激活时布局可能未完成。保留原文，渲染时按当前宽度截断。
<<< END U004876 >>>
<<< UNIT U004877 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1451-1451 >>>
# 策略与服务都依赖已注册的实例。
<<< END U004877 >>>
<<< UNIT U004878 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1538-1538 >>>
# 缓存可能过期，确认覆盖前须重新检查单元文件。
<<< END U004878 >>>
<<< UNIT U004879 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1541-1541 >>>
# noqa: BLE001 - 刷新失败按缓存状态处理，执行时不带 force
<<< END U004879 >>>
<<< UNIT U004880 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1625-1625 >>>
# 串行执行写入操作，避免多个子进程同时修改注册表。
<<< END U004880 >>>
<<< UNIT U004881 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1653-1653 >>>
# noqa: BLE001 - 执行器异常仅显示错误说明
<<< END U004881 >>>
<<< UNIT U004882 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1660-1660 >>>
# 仅由设置忙状态的操作负责清除该状态。
<<< END U004882 >>>
<<< UNIT U004883 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1702-1702 >>>
# 注册名由 CLI 生成。刷新后无法获取时使用目录名。
<<< END U004883 >>>
<<< UNIT U004884 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1765-1765 >>>
# init 负责实例注册，创建成功后刷新清单。
<<< END U004884 >>>
<<< UNIT U004885 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1867-1867 >>>
# 手动刷新使待确认目标失效，须重新确认。
<<< END U004885 >>>
<<< UNIT U004886 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1879-1879 >>>
# noqa: BLE001 - 数据源异常都不应中断界面
<<< END U004886 >>>
<<< UNIT U004887 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1904-1904 >>>
# noqa: BLE001 - 探测失败按未知展示
<<< END U004887 >>>
<<< UNIT U004888 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1937-1937 >>>
# noqa: BLE001 - 读取数据失败只降级为逐项说明
<<< END U004888 >>>
<<< UNIT U004889 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1946-1946 >>>
# 摘要限高两行，为列表与详情保留空间。原文保留完整取值，由控件按宽度截断。
<<< END U004889 >>>
<<< UNIT U004890 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2026-2026 >>>
# 运行状态和可用宽度均可能变化，须同时刷新摘要与按钮。
<<< END U004890 >>>
<<< UNIT U004891 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2033-2033 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U004891 >>>
<<< UNIT U004892 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2036-2036 >>>
# 首次激活时宽度可能为零，使用默认宽度并在 resize 时重新布局。
<<< END U004892 >>>
<<< UNIT U004893 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2069-2069 >>>
# 重建列表时 clear() 会把高亮清空，这条不是用户选择，按“不变”处理。
<<< END U004893 >>>
<<< UNIT U004894 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2071-2071 >>>
# 重建列表也会触发高亮事件，须比较目标以排除显示刷新。
<<< END U004894 >>>
<<< UNIT U004895 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2074-2074 >>>
# 重建后按钮状态可能仍是按空列表算出的，须按当前高亮刷新。
<<< END U004895 >>>
<<< UNIT U004896 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2106-2106 >>>
# 禁用状态可能改变标签宽度，须重新计算布局。
<<< END U004896 >>>
<<< UNIT U004897 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:189-189 | ctx=DashboardSnapshot.state >>>
将运行状态转换为 :data:`STATE_RUNNING` 等取值。
<<< END U004897 >>>
<<< UNIT U004898 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:196-196 | ctx=DashboardSnapshot.state_label >>>
返回运行状态的本地化标签，带状态标记。
<<< END U004898 >>>
<<< UNIT U004899 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:224-224 | ctx=InstanceRow.state_label >>>
返回运行状态的本地化标签。
<<< END U004899 >>>
<<< UNIT U004900 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:230-230 | ctx=InstanceRow.marks >>>
返回自启与崩溃重启策略标记。
<<< END U004900 >>>
<<< UNIT U004901 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:259-259 | ctx=ServiceControl >>>
读取服务状态并执行预览。安装与卸载经 :class:`CliRunner` 执行。
<<< END U004901 >>>
<<< UNIT U004902 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:262-262 | ctx=ServiceControl.service_status >>>
返回服务单元状态。
<<< END U004902 >>>
<<< UNIT U004903 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:335-335 | ctx=StaticServiceControl.set_status >>>
替换模拟对象记录的服务状态，模拟单元文件在界面之外出现或消失。
<<< END U004903 >>>
<<< UNIT U004904 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:346-346 | ctx=CliRunner >>>
写入操作的执行接口，对应一次 ``akaribot <子命令>`` 调用。
<<< END U004904 >>>
<<< UNIT U004905 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:386-386 | ctx=InitRunner >>>
新建实例的执行接口。测试注入模拟对象，生产环境经 ``akaribot init`` 子进程。
<<< END U004905 >>>
<<< UNIT U004906 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:445-445 | ctx=InstanceListSource >>>
本机实例清单的数据源接口。写入操作通过 :class:`CliRunner` 交给命令层。
<<< END U004906 >>>
<<< UNIT U004907 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:448-448 | ctx=InstanceListSource.list_instances >>>
返回注册表中的实例，附带实时运行状态。
<<< END U004907 >>>
<<< UNIT U004908 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:542-542 | ctx=SetupSummarySource >>>
首次使用摘要的数据源接口。测试注入模拟对象，生产环境经子进程与本机配置文件。
<<< END U004908 >>>
<<< UNIT U004909 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:545-545 | ctx=SetupSummarySource.summary >>>
返回摘要数据。
<<< END U004909 >>>
<<< UNIT U004910 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:567-567 | ctx=StaticSetupSummarySource.set_summary >>>
替换模拟对象记录的摘要，模拟配置或诊断结论在界面之外变化。
<<< END U004910 >>>
<<< UNIT U004911 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:776-776 | ctx=meta_core_version >>>
从 ``akaribot.toml`` 的候选位置获取 core 版本，缺失时返回空字符串。
<<< END U004911 >>>
<<< UNIT U004912 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:788-788 | ctx=DashboardSource >>>
Dashboard 数据源接口。测试注入模拟对象，运行时通过文件系统与子进程读取。
<<< END U004912 >>>
<<< UNIT U004913 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:791-791 | ctx=DashboardSource.snapshot >>>
返回完整快照，包括版本查询结果。
<<< END U004913 >>>
<<< UNIT U004914 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:794-794 | ctx=DashboardSource.probe_running >>>
只探测运行状态，代价须与读取一个锁文件相当。
<<< END U004914 >>>
<<< UNIT U004915 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:833-833 | ctx=StaticDashboardSource.set_running >>>
改写模拟对象的运行状态，模拟实例启动与停止。
<<< END U004915 >>>
<<< UNIT U004916 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:837-837 | ctx=StaticDashboardSource.set_snapshot >>>
整份替换模拟对象快照，模拟实例重建或版本变化。
<<< END U004916 >>>
<<< UNIT U004917 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1197-1197 | ctx=DashboardPage.activate >>>
首次显示时读取快照与首次使用摘要，并按周期探测锁文件。
<<< END U004917 >>>
<<< UNIT U004918 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1209-1209 | ctx=DashboardPage.focus_primary >>>
聚焦实例清单。为空时聚焦页面。
<<< END U004918 >>>
<<< UNIT U004919 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1214-1214 | ctx=DashboardPage.instance_rows >>>
返回最近一次读取到的实例清单。
<<< END U004919 >>>
<<< UNIT U004920 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1238-1238 | ctx=DashboardPage.selected_instance >>>
返回清单中当前高亮的记录。
<<< END U004920 >>>
<<< UNIT U004921 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1296-1296 | ctx=DashboardPage.switch_to_selected >>>
切换到高亮实例，并通过 CLI 设置默认实例。
<<< END U004921 >>>
<<< UNIT U004922 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1400-1400 | ctx=DashboardPage.service_row >>>
返回最近一次读到的服务状态。
<<< END U004922 >>>
<<< UNIT U004923 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1405-1405 | ctx=DashboardPage.service_preview >>>
返回最近一次服务预览的完整输出。
<<< END U004923 >>>
<<< UNIT U004924 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1409-1409 | ctx=DashboardPage.refresh_service >>>
读取并显示服务单元状态。
<<< END U004924 >>>
<<< UNIT U004925 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1455-1455 | ctx=DashboardPage.request_add_menu >>>
弹出添加实例菜单，供新建实例或注册已有目录。
<<< END U004925 >>>
<<< UNIT U004926 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1478-1478 | ctx=DashboardPage.request_service_menu >>>
弹出服务与策略菜单，只列出所选实例可用的操作。
<<< END U004926 >>>
<<< UNIT U004927 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1529-1529 | ctx=DashboardPage.request_toggle_service >>>
请求安装或卸载服务，提供执行与预览选项。
<<< END U004927 >>>
<<< UNIT U004928 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1576-1576 | ctx=DashboardPage.preview_service >>>
执行 ``akaribot service <动作> --dry-run``，在状态栏与预览区显示输出。
<<< END U004928 >>>
<<< UNIT U004929 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1666-1666 | ctx=DashboardPage.request_add_instance >>>
请求输入实例目录并注册。
<<< END U004929 >>>
<<< UNIT U004930 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1710-1710 | ctx=DashboardPage.request_new_instance >>>
请求输入新实例目录并选择环境方式。
<<< END U004930 >>>
<<< UNIT U004931 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1770-1770 | ctx=DashboardPage.request_remove_instance >>>
请求确认取消高亮实例的注册，保留实例目录。
<<< END U004931 >>>
<<< UNIT U004932 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1823-1823 | ctx=DashboardPage.snapshot >>>
返回缓存中的快照，不重新读取数据。
<<< END U004932 >>>
<<< UNIT U004933 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1828-1828 | ctx=DashboardPage.rows >>>
返回最近一次渲染使用的标签与值，供自动化检查逐字段核对。
<<< END U004933 >>>
<<< UNIT U004934 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1833-1833 | ctx=DashboardPage.fields_text >>>
返回信息面板当前渲染出的纯文本。
<<< END U004934 >>>
<<< UNIT U004935 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1838-1838 | ctx=DashboardPage.setup_summary >>>
返回缓存中的首次使用摘要，不重新读取数据。
<<< END U004935 >>>
<<< UNIT U004936 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1843-1843 | ctx=DashboardPage.setup_rows >>>
返回首次使用摘要最近一次渲染的标签与值，供自动化检查逐项核对。
<<< END U004936 >>>
<<< UNIT U004937 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1848-1848 | ctx=DashboardPage.setup_text >>>
返回首次使用行动区当前渲染出的纯文本。
<<< END U004937 >>>
<<< UNIT U004938 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1853-1853 | ctx=DashboardPage.status_text >>>
返回状态栏当前文本。
<<< END U004938 >>>
<<< UNIT U004939 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1857-1857 | ctx=DashboardPage.cache_age >>>
返回快照自上次读取以来的秒数。从未读取时为无穷大。
<<< END U004939 >>>
<<< UNIT U004940 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:1922-1922 | ctx=DashboardPage.refresh_setup >>>
读取首次使用摘要。失败时显示原因。
<<< END U004940 >>>
<<< UNIT U004941 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2057-2057 | ctx=DashboardPage.reset_pending >>>
作废本页的待确认状态。切换页面、刷新与更换选中项后须重新确认。
<<< END U004941 >>>
<<< UNIT U004942 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dashboard.py:2143-2143 | ctx=DashboardPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U004942 >>>
<<< UNIT U004943 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:24-24 >>>
# 仅加载当前页，避免一次读取大量数据。分页与总数由 core 计算。
<<< END U004943 >>>
<<< UNIT U004944 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:26-27 >>>
# 三栏并排所需的最小内容宽度为表清单 26 列、数据项 32 列（四个翻页按钮的自然宽度）与编辑区 34 列。
# 窄屏采用两行布局，为数据项和编辑区保留可读宽度。
<<< END U004944 >>>
<<< UNIT U004945 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:30-30 >>>
# 页面高度低于此值时按钮改为单行。
<<< END U004945 >>>
<<< UNIT U004946 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:33-33 >>>
# 运算符按长度降序匹配，长运算符优先，避免短运算符抢占前缀。
<<< END U004946 >>>
<<< UNIT U004947 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:35-35 >>>
# 筛选条件必须包含列名，避免将搜索词中的运算符识别为条件。
<<< END U004947 >>>
<<< UNIT U004948 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:235-235 >>>
# 模拟数据源使用与 core 一致的筛选运算符，使测试能够验证筛选后的记录。
<<< END U004948 >>>
<<< UNIT U004949 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:275-275 >>>
# 拆分 ``<列><运算符><值>``。只有列名时按“非空”处理。
<<< END U004949 >>>
<<< UNIT U004950 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:286-286 >>>
# 数值优先按数值比较，其他值按文本比较。
<<< END U004950 >>>
<<< UNIT U004951 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:493-493 >>>
# 每次读取时解析实例根目录，确保切换实例后使用当前实例的配置。
<<< END U004951 >>>
<<< UNIT U004952 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:548-548 >>>
# 分别报告执行失败和输出解析失败，便于定位错误。
<<< END U004952 >>>
<<< UNIT U004953 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:593-593 >>>
# 解析失败时保留原始输出，供调用方诊断。
<<< END U004953 >>>
<<< UNIT U004954 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:616-616 >>>
# 通过公开的 render() 读取文本，避免依赖 Textual 的内部属性。
<<< END U004954 >>>
<<< UNIT U004955 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:813-813 >>>
# 删除使用组合键。分页与筛选键位由页内控件提示，为全局键位保留页脚空间。
<<< END U004955 >>>
<<< UNIT U004956 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:816-816 >>>
# 保存使用 ctrl+s，因为编辑区输入框聚焦时单字母由输入框接收，而组合键在编辑中同样生效。
<<< END U004956 >>>
<<< UNIT U004957 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:897-897 >>>
# 字段单独放入滚动容器，字段多时只有它滚动，主键行保持可见。
<<< END U004957 >>>
<<< UNIT U004958 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:916-916 >>>
# 加载前禁用不可用的分页操作，避免首帧出现无效按钮。
<<< END U004958 >>>
<<< UNIT U004959 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:920-920 >>>
# 切换的是容器上的类，三栏的构成与控件 id 都不变。并排所需宽度见 SIDE_BY_SIDE_MIN_WIDTH。
<<< END U004959 >>>
<<< UNIT U004960 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:938-938 >>>
# 列表加载后仅在焦点仍位于页面容器时恢复列表焦点，避免中断用户输入。
<<< END U004960 >>>
<<< UNIT U004961 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:946-946 >>>
# region 状态读取（供测试与 App 使用）
<<< END U004961 >>>
<<< UNIT U004962 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:982-982 >>>
# 名称需避免覆盖 Textual 的 Widget.query()。
<<< END U004962 >>>
<<< UNIT U004963 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1059-1059 >>>
# region 读取与渲染
<<< END U004963 >>>
<<< UNIT U004964 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1083-1083 >>>
# noqa: BLE001 - 数据源任意异常都不应中断界面
<<< END U004964 >>>
<<< UNIT U004965 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1124-1124 >>>
# 筛选列属于当前表，切换表时清空条件，避免引用不存在的列。
<<< END U004965 >>>
<<< UNIT U004966 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1149-1149 >>>
# 翻页复用记录总数，避免对大表重复执行全表统计。
<<< END U004966 >>>
<<< UNIT U004967 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1161-1161 >>>
# noqa: BLE001 - 读取数据失败只影响本页展示
<<< END U004967 >>>
<<< UNIT U004968 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1171-1171 >>>
# 未重新统计时保留总数，用于页码和末页定位。
<<< END U004968 >>>
<<< UNIT U004969 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1174-1174 >>>
# 记录减少可能使偏移超出末页，修正偏移以避免空白页。
<<< END U004969 >>>
<<< UNIT U004970 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1230-1230 >>>
# 编辑区只读缓存中的数据项，渲染路径不得启动子进程。
<<< END U004970 >>>
<<< UNIT U004971 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1235-1235 >>>
# 新建时允许输入主键，以支持 module_status.module_name 等非自增主键。
<<< END U004971 >>>
<<< UNIT U004972 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1323-1323 >>>
# 在首页和末页禁用对应的翻页操作，避免进入空白页。
<<< END U004972 >>>
<<< UNIT U004973 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1327-1327 >>>
# 后台读取可能在页面卸载后完成，此时跳过控件更新。
<<< END U004973 >>>
<<< UNIT U004974 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1379-1379 >>>
# 清空筛选条件不影响排序。
<<< END U004974 >>>
<<< UNIT U004975 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1500-1500 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U004975 >>>
<<< UNIT U004976 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1521-1521 >>>
# 短屏按钮改为单行，为表格与编辑区保留高度。
<<< END U004976 >>>
<<< UNIT U004977 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1530-1530 >>>
# region 写入
<<< END U004977 >>>
<<< UNIT U004978 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1643-1643 >>>
# 写入前通过模态框展示操作范围，并防止连续触发重复确认。
<<< END U004978 >>>
<<< UNIT U004979 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1683-1683 >>>
# 原因与输出尾部是 CLI 给出的可变文本，按分隔符拼接而不是写入模板。
<<< END U004979 >>>
<<< UNIT U004980 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1707-1707 >>>
# 同一数据项的多列更改通过一次 UPDATE 写入，避免部分列更新。
<<< END U004980 >>>
<<< UNIT U004981 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1715-1715 >>>
# noqa: BLE001 - 数据源任意异常都转成失败项展示
<<< END U004981 >>>
<<< UNIT U004982 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/database.py:1733-1733 >>>
# region 交互
<<< END U004982 >>>
<<< UNIT U004983 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:71-71 | ctx=ColumnInfo.label >>>
返回字段名标签，含类型。
<<< END U004983 >>>
<<< UNIT U004984 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:96-96 | ctx=TableInfo.pk >>>
返回主键列，模型未声明时返回 ``None``。
<<< END U004984 >>>
<<< UNIT U004985 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:104-104 | ctx=TableInfo.pk_name >>>
返回主键列名，无法获取时返回空字符串。
<<< END U004985 >>>
<<< UNIT U004986 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:109-109 | ctx=TableInfo.editable_columns >>>
返回可编辑的列，主键仅作只读展示。
<<< END U004986 >>>
<<< UNIT U004987 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:127-127 | ctx=RowQuery.is_empty >>>
返回是否没有任何条件。
<<< END U004987 >>>
<<< UNIT U004988 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:131-131 | ctx=RowQuery.with_filter >>>
追加一条筛选条件。重复的条件不重复添加。
<<< END U004988 >>>
<<< UNIT U004989 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:138-138 | ctx=RowQuery.with_search >>>
设置全表搜索词。
<<< END U004989 >>>
<<< UNIT U004990 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:142-142 | ctx=RowQuery.summary >>>
返回状态栏用的一行说明。
<<< END U004990 >>>
<<< UNIT U004991 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:169-169 | ctx=RowPage.rows_total >>>
返回已知的总条数。未统计时按 0 处理。
<<< END U004991 >>>
<<< UNIT U004992 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:174-174 | ctx=RowPage.pages >>>
返回总页数，至少为 1。
<<< END U004992 >>>
<<< UNIT U004993 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:179-179 | ctx=RowPage.page_number >>>
返回当前页码，从 1 开始。
<<< END U004993 >>>
<<< UNIT U004994 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:184-184 | ctx=RowPage.last_offset >>>
返回末页的起始偏移。
<<< END U004994 >>>
<<< UNIT U004995 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:220-220 | ctx=WritePlan.summary >>>
返回状态栏用的一行说明，列出将更改的列与新旧值。
<<< END U004995 >>>
<<< UNIT U004996 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:365-365 | ctx=normalize_page >>>
把 ``db rows --json`` 的输出规范化为一页数据项。
<<< END U004996 >>>
<<< UNIT U004997 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:382-382 | ctx=DatabaseSourceError >>>
数据源不可用（子进程缺失、退出码非零或输出不是 JSON）。
<<< END U004997 >>>
<<< UNIT U004998 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:387-387 | ctx=DatabaseSource >>>
数据库数据源接口。测试注入模拟对象，实际运行通过子进程访问。
<<< END U004998 >>>
<<< UNIT U004999 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:390-390 | ctx=DatabaseSource.tables >>>
返回实例数据库中已注册模型的表。
<<< END U004999 >>>
<<< UNIT U005000 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:395-395 | ctx=DatabaseSource.rows >>>
返回一张表的一页数据项。``query`` 提供筛选条件与排序，``count`` 为假时不重新计算总条数。
<<< END U005000 >>>
<<< UNIT U005001 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:398-398 | ctx=DatabaseSource.set_values >>>
按主键更新数据项的指定列。多列更改通过一次调用提交。
<<< END U005001 >>>
<<< UNIT U005002 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:401-401 | ctx=DatabaseSource.insert_row >>>
新建一条数据项。
<<< END U005002 >>>
<<< UNIT U005003 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:404-404 | ctx=DatabaseSource.delete_row >>>
按主键删除一条数据项。
<<< END U005003 >>>
<<< UNIT U005004 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:439-439 | ctx=StaticDatabaseSource.tables >>>
见 :meth:`DatabaseSource.tables`。
<<< END U005004 >>>
<<< UNIT U005005 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:446-446 | ctx=StaticDatabaseSource.rows >>>
返回按条件筛选并分页的数据项，筛选规则与 core 一致。
<<< END U005005 >>>
<<< UNIT U005006 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:460-460 | ctx=StaticDatabaseSource.set_values >>>
见 :meth:`DatabaseSource.set_values`。
<<< END U005006 >>>
<<< UNIT U005007 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:466-466 | ctx=StaticDatabaseSource.insert_row >>>
见 :meth:`DatabaseSource.insert_row`。
<<< END U005007 >>>
<<< UNIT U005008 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:472-472 | ctx=StaticDatabaseSource.delete_row >>>
见 :meth:`DatabaseSource.delete_row`。
<<< END U005008 >>>
<<< UNIT U005009 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:501-501 | ctx=SubprocessDatabaseSource.root >>>
返回实例根目录路径，显式给定优先，其次为界面当前选中的实例，最后自动定位。
<<< END U005009 >>>
<<< UNIT U005010 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:505-505 | ctx=SubprocessDatabaseSource.tables >>>
见 :meth:`DatabaseSource.tables`。
<<< END U005010 >>>
<<< UNIT U005011 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:512-512 | ctx=SubprocessDatabaseSource.rows >>>
见 :meth:`DatabaseSource.rows`，条件、搜索与排序都交给 ``db rows``。
<<< END U005011 >>>
<<< UNIT U005012 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:527-527 | ctx=SubprocessDatabaseSource.set_values >>>
见 :meth:`DatabaseSource.set_values`，一行一次 CLI 调用，各列经重复的 ``--set`` 下发。
<<< END U005012 >>>
<<< UNIT U005013 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:535-535 | ctx=SubprocessDatabaseSource.insert_row >>>
见 :meth:`DatabaseSource.insert_row`。
<<< END U005013 >>>
<<< UNIT U005014 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:543-543 | ctx=SubprocessDatabaseSource.delete_row >>>
删除数据项，使用 ``--yes`` 传递界面的确认结果。
<<< END U005014 >>>
<<< UNIT U005015 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:633-633 | ctx=EditorField.compose >>>
装配标签与输入框。
<<< END U005015 >>>
<<< UNIT U005016 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:639-639 | ctx=EditorField.value >>>
返回输入框中的当前文本。
<<< END U005016 >>>
<<< UNIT U005017 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:643-643 | ctx=EditorField.set_value >>>
设置输入框文本，等价于用户键入。
<<< END U005017 >>>
<<< UNIT U005018 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:863-863 | ctx=DatabasePage.compose >>>
装配页面控件树，包含表清单、数据项、编辑区与状态栏。
<<< END U005018 >>>
<<< UNIT U005019 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:913-913 | ctx=DatabasePage.on_mount >>>
挂载后只装配控件。读取数据推迟到首次显示。
<<< END U005019 >>>
<<< UNIT U005020 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:927-927 | ctx=DatabasePage.activate >>>
首次显示时读取表清单。
<<< END U005020 >>>
<<< UNIT U005021 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:934-934 | ctx=DatabasePage.focus_primary >>>
聚焦表清单。列表为空时聚焦页面容器，保持页面键位可用。
<<< END U005021 >>>
<<< UNIT U005022 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:943-943 | ctx=DatabasePage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005022 >>>
<<< UNIT U005023 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:950-950 | ctx=DatabasePage.tables >>>
返回缓存中的表清单，不触发子进程。
<<< END U005023 >>>
<<< UNIT U005024 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:955-955 | ctx=DatabasePage.visible_tables >>>
返回应用当前搜索词后的表清单。
<<< END U005024 >>>
<<< UNIT U005025 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:963-963 | ctx=DatabasePage.selected_table >>>
返回当前表名。
<<< END U005025 >>>
<<< UNIT U005026 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:968-968 | ctx=DatabasePage.selected_info >>>
返回当前表的表信息。
<<< END U005026 >>>
<<< UNIT U005027 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:976-976 | ctx=DatabasePage.page >>>
返回最近一次读取的数据项，不触发子进程。
<<< END U005027 >>>
<<< UNIT U005028 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:981-981 | ctx=DatabasePage.row_query >>>
返回当前生效的筛选条件与搜索词。
<<< END U005028 >>>
<<< UNIT U005029 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:987-987 | ctx=DatabasePage.offset >>>
返回当前页的起始偏移。
<<< END U005029 >>>
<<< UNIT U005030 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:992-992 | ctx=DatabasePage.insert_mode >>>
返回是否处于新建模式。
<<< END U005030 >>>
<<< UNIT U005031 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:997-997 | ctx=DatabasePage.selected_key >>>
返回当前数据项的主键值文本。未选中时为空字符串。
<<< END U005031 >>>
<<< UNIT U005032 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1002-1002 | ctx=DatabasePage.pending >>>
返回待确认的写入计划，没有待确认时为空。
<<< END U005032 >>>
<<< UNIT U005033 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1007-1007 | ctx=DatabasePage.status_text >>>
返回状态栏当前文本。
<<< END U005033 >>>
<<< UNIT U005034 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1011-1011 | ctx=DatabasePage.table_row_texts >>>
返回最近一次渲染出的表清单行文本。
<<< END U005034 >>>
<<< UNIT U005035 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1015-1015 | ctx=DatabasePage.row_texts >>>
返回最近一次渲染出的数据项行文本。
<<< END U005035 >>>
<<< UNIT U005036 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1019-1019 | ctx=DatabasePage.editor >>>
返回编辑区中的字段控件。
<<< END U005036 >>>
<<< UNIT U005037 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1023-1023 | ctx=DatabasePage.editor_values >>>
返回编辑区各列的当前文本。
<<< END U005037 >>>
<<< UNIT U005038 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1027-1027 | ctx=DatabasePage.set_editor_value >>>
设置某一列的编辑文本，等价于用户键入。
<<< END U005038 >>>
<<< UNIT U005039 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1034-1034 | ctx=DatabasePage.set_query >>>
设置表名搜索词，等价于用户键入。
<<< END U005039 >>>
<<< UNIT U005040 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1038-1038 | ctx=DatabasePage.caption_text >>>
返回数据项列表上方的摘要文本。
<<< END U005040 >>>
<<< UNIT U005041 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1042-1042 | ctx=DatabasePage.filter_text >>>
返回条件行的当前文本。
<<< END U005041 >>>
<<< UNIT U005042 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1046-1046 | ctx=DatabasePage.pager_states >>>
返回四个翻页按钮的禁用状态，供自动化检查。
<<< END U005042 >>>
<<< UNIT U005043 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1050-1050 | ctx=DatabasePage.editor_caption >>>
返回编辑区上方的摘要文本。
<<< END U005043 >>>
<<< UNIT U005044 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1054-1054 | ctx=DatabasePage.pk_text >>>
返回主键的只读展示文本。
<<< END U005044 >>>
<<< UNIT U005045 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1074-1074 | ctx=DatabasePage.cache_age >>>
返回表清单缓存自上次读取以来的秒数。从未读取时为无穷大。
<<< END U005045 >>>
<<< UNIT U005046 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1080-1080 | ctx=DatabasePage.reload_tables >>>
后台读取表清单并载入当前表，返回是否成功。
<<< END U005046 >>>
<<< UNIT U005047 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1319-1319 | ctx=DatabasePage.sort_text >>>
返回当前排序的展示文本。
<<< END U005047 >>>
<<< UNIT U005048 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1340-1340 | ctx=DatabasePage.action_add_filter >>>
添加筛选条件或搜索词的键位动作。
<<< END U005048 >>>
<<< UNIT U005049 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1375-1375 | ctx=DatabasePage.action_clear_filters >>>
清空全部条件与搜索词的键位动作。
<<< END U005049 >>>
<<< UNIT U005050 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1385-1385 | ctx=DatabasePage.action_more >>>
打开低频操作菜单的键位动作。
<<< END U005050 >>>
<<< UNIT U005051 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1389-1389 | ctx=DatabasePage.request_more >>>
弹出低频操作菜单，提供设置排序与清空筛选条件。
<<< END U005051 >>>
<<< UNIT U005052 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1412-1412 | ctx=DatabasePage.action_set_order >>>
修改排序方式的键位动作。
<<< END U005052 >>>
<<< UNIT U005053 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1458-1458 | ctx=DatabasePage.action_next_page >>>
翻到下一页的键位动作。
<<< END U005053 >>>
<<< UNIT U005054 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1462-1462 | ctx=DatabasePage.action_previous_page >>>
翻到上一页的键位动作。
<<< END U005054 >>>
<<< UNIT U005055 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1466-1466 | ctx=DatabasePage.action_first_page >>>
跳转到第一页的键位动作。
<<< END U005055 >>>
<<< UNIT U005056 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1470-1470 | ctx=DatabasePage.action_last_page >>>
跳转到最后一页的键位动作。
<<< END U005056 >>>
<<< UNIT U005057 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1519-1519 | ctx=DatabasePage.on_resize >>>
终端尺寸变化时切换布局并按缓存重新排列，不重新读取数据。
<<< END U005057 >>>
<<< UNIT U005058 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1533-1533 | ctx=DatabasePage.action_refresh >>>
作废缓存并重新读取表与数据项的键位动作。
<<< END U005058 >>>
<<< UNIT U005059 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1538-1538 | ctx=DatabasePage.action_save >>>
保存编辑区更改的键位动作，新建模式下等价于写入新数据项。
<<< END U005059 >>>
<<< UNIT U005060 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1542-1542 | ctx=DatabasePage.action_insert >>>
进入新建模式或写入新数据项的键位动作。
<<< END U005060 >>>
<<< UNIT U005061 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1546-1546 | ctx=DatabasePage.action_delete >>>
删除当前数据项的键位动作。
<<< END U005061 >>>
<<< UNIT U005062 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1550-1550 | ctx=DatabasePage.action_cancel >>>
退出新建模式并清空待确认状态的键位动作，焦点在搜索框时先清空搜索。
<<< END U005062 >>>
<<< UNIT U005063 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1561-1561 | ctx=DatabasePage.action_focus_search >>>
聚焦搜索框的键位动作。
<<< END U005063 >>>
<<< UNIT U005064 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1565-1565 | ctx=DatabasePage.request_save >>>
通过模态框确认并保存编辑区的更改。
<<< END U005064 >>>
<<< UNIT U005065 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1585-1585 | ctx=DatabasePage.request_insert >>>
进入新建模式。已处于新建模式时打开写入确认框。
<<< END U005065 >>>
<<< UNIT U005066 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1603-1603 | ctx=DatabasePage.request_delete >>>
通过模态框确认并删除当前数据项。
<<< END U005066 >>>
<<< UNIT U005067 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1611-1611 | ctx=DatabasePage.reset_pending >>>
作废待确认的写入。切换页面、刷新、切换数据表或数据项时调用。
<<< END U005067 >>>
<<< UNIT U005068 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1616-1616 | ctx=DatabasePage.dirty_note >>>
返回未保存更改的说明。没有更改时返回空字符串。
<<< END U005068 >>>
<<< UNIT U005069 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1632-1632 | ctx=DatabasePage.cancel_edit >>>
退出新建模式、清空待确认状态并把编辑区还原为当前数据项。
<<< END U005069 >>>
<<< UNIT U005070 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/database.py:1719-1719 | ctx=DatabasePage.reload_tables_after_write >>>
写入后重新加载数据项和记录总数。编辑与删除保留当前页，新建返回第一页。
<<< END U005070 >>>
<<< UNIT U005071 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:22-22 >>>
# 文案随当前语言解析，常量仅保存文案键。
<<< END U005071 >>>
<<< UNIT U005072 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:54-54 >>>
# editable 列使用数据字段名，其余列标题按当前语言解析。
<<< END U005072 >>>
<<< UNIT U005073 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:114-114 >>>
# 页面校验名称中的空白与路径分隔符，其余命名规则由 CLI 校验。
<<< END U005073 >>>
<<< UNIT U005074 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:369-369 >>>
# uv workspace 安装不一定标记为 editable，来源判定优先采用成员索引。
<<< END U005074 >>>
<<< UNIT U005075 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:420-420 >>>
# 实例根目录在每次请求时解析，使子进程目录与 AKARI_INSTANCE_DIR 跟随当前实例。
<<< END U005075 >>>
<<< UNIT U005076 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:473-473 >>>
# 参数由界面收集，子进程标准输入使用空设备，避免读取 TUI 终端。
<<< END U005076 >>>
<<< UNIT U005077 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:539-539 >>>
# 非交互模式使表单未提供的选项采用默认值，避免子进程等待输入。
<<< END U005077 >>>
<<< UNIT U005078 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:546-546 >>>
# 显式传递开关值，使 CLI 参数与表单状态一致。
<<< END U005078 >>>
<<< UNIT U005079 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:550-550 >>>
# new adapter 仅支持 --config，不能传递模块专用参数。
<<< END U005079 >>>
<<< UNIT U005080 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:560-560 >>>
# 测试路径与新包目录相对工作区根目录解析。未配置工作区时使用实例根目录。
<<< END U005080 >>>
<<< UNIT U005081 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:567-567 >>>
# noqa: BLE001 - 模拟对象读取失败只作为错误上报
<<< END U005081 >>>
<<< UNIT U005082 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:578-578 >>>
# noqa: BLE001 - 元数据损坏不应中断页面
<<< END U005082 >>>
<<< UNIT U005083 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:600-600 >>>
# noqa: BLE001 - 工作区扫描失败只降级来源判定
<<< END U005083 >>>
<<< UNIT U005084 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:778-778 >>>
# 适配器脚手架不支持 database 与 tests 选项。
<<< END U005084 >>>
<<< UNIT U005085 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:991-991 >>>
# 后台请求可能在页面卸载后完成，访问控件前需检查挂载状态。
<<< END U005085 >>>
<<< UNIT U005086 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1094-1094 >>>
# noqa: BLE001 - 数据源异常不应中断界面
<<< END U005086 >>>
<<< UNIT U005087 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1149-1149 >>>
# 记住上次选的类型，下次打开对话框时沿用。
<<< END U005087 >>>
<<< UNIT U005088 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1193-1193 >>>
# noqa: BLE001 - 数据源异常不应中断界面
<<< END U005088 >>>
<<< UNIT U005089 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1199-1199 >>>
# 创建包后刷新清单，并保留本次操作的状态结果。
<<< END U005089 >>>
<<< UNIT U005090 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1208-1208 >>>
# 追加输出后布局尚未更新，需使用追加前的视口判断是否继续滚动跟随。
<<< END U005090 >>>
<<< UNIT U005091 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1234-1234 >>>
# noqa: BLE001 - 控件缺失时按空输入处理
<<< END U005091 >>>
<<< UNIT U005092 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1260-1260 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005092 >>>
<<< UNIT U005093 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1351-1351 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005093 >>>
<<< UNIT U005094 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1444-1444 >>>
# 布局更新后重新滚动到底部，避免将过期的滚动范围误判为用户操作。
<<< END U005094 >>>
<<< UNIT U005095 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1449-1449 >>>
# 后台请求可能在页面卸载后完成，访问控件前需检查挂载状态。
<<< END U005095 >>>
<<< UNIT U005096 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:151-151 | ctx=DevPackage.display_name >>>
包名列的展示文本。
<<< END U005096 >>>
<<< UNIT U005097 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:156-156 | ctx=DevPackage.kind_label >>>
类型列的展示文本。
<<< END U005097 >>>
<<< UNIT U005098 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:162-162 | ctx=DevPackage.editable_label >>>
editable 列的展示文本。
<<< END U005098 >>>
<<< UNIT U005099 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:167-167 | ctx=DevPackage.source_label >>>
来源列的展示文本。
<<< END U005099 >>>
<<< UNIT U005100 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:172-172 | ctx=DevPackage.path_text >>>
本地路径列的展示文本。
<<< END U005100 >>>
<<< UNIT U005101 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:177-177 | ctx=DevPackage.key >>>
选中项的稳定标识。
<<< END U005101 >>>
<<< UNIT U005102 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:208-208 | ctx=DevSnapshot.mode_label >>>
模式列的展示文本。
<<< END U005102 >>>
<<< UNIT U005103 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:214-214 | ctx=DevSnapshot.workspace_label >>>
工作区路径的展示文本。
<<< END U005103 >>>
<<< UNIT U005104 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:221-221 | ctx=DevSnapshot.source_counts >>>
按来源统计包数。
<<< END U005104 >>>
<<< UNIT U005105 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:274-274 | ctx=StaticDevSource.load_snapshot >>>
见 :meth:`DevSource.load_snapshot`。
<<< END U005105 >>>
<<< UNIT U005106 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:279-279 | ctx=StaticDevSource.stream_action >>>
见 :meth:`DevSource.stream_action`。模拟对象回放固定输出，不产生子进程。
<<< END U005106 >>>
<<< UNIT U005107 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:312-312 | ctx=StaticDevSource.cancel_action >>>
见 :meth:`DevSource.cancel_action`。模拟对象记录请求并放行被挂起的动作。
<<< END U005107 >>>
<<< UNIT U005108 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:321-321 | ctx=DevSource >>>
开发环境状态与操作的数据源接口。
<<< END U005108 >>>
<<< UNIT U005109 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:324-324 | ctx=DevSource.load_snapshot >>>
返回 workspace 配置与已安装包清单。错误记入快照而不抛出。
<<< END U005109 >>>
<<< UNIT U005110 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:337-337 | ctx=DevSource.cancel_action >>>
请求终止正在执行的动作，返回是否发出了终止请求。
<<< END U005110 >>>
<<< UNIT U005111 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:398-398 | ctx=DevSourceError >>>
数据源不可用（子进程缺失、退出码非零或输出不是 JSON）。
<<< END U005111 >>>
<<< UNIT U005112 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:432-432 | ctx=SubprocessDevSource.root >>>
返回实例根目录，依次采用显式路径、当前实例或自动定位结果。
<<< END U005112 >>>
<<< UNIT U005113 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:436-436 | ctx=SubprocessDevSource.load_snapshot >>>
见 :meth:`DevSource.load_snapshot`。
<<< END U005113 >>>
<<< UNIT U005114 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:466-466 | ctx=SubprocessDevSource.stream_action >>>
异步执行 CLI 操作，逐行返回输出并支持终止请求。
<<< END U005114 >>>
<<< UNIT U005115 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:517-517 | ctx=SubprocessDevSource.cancel_action >>>
见 :meth:`DevSource.cancel_action`。向动作子进程发送终止信号。
<<< END U005115 >>>
<<< UNIT U005116 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:623-623 | ctx=SubprocessDevSource.cli_argv >>>
构造调用本 CLI 的 argv，规则见 :mod:`akaribot.cli.tui.cli_process`。
<<< END U005116 >>>
<<< UNIT U005117 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:683-683 | ctx=PackageLayout.widths >>>
按列序返回宽度。
<<< END U005117 >>>
<<< UNIT U005118 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:749-749 | ctx=NewPackageScreen.compose >>>
装配名称、类型、目录、开关、提示与按钮。
<<< END U005118 >>>
<<< UNIT U005119 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:768-768 | ctx=NewPackageScreen.on_mount >>>
同步类型相关选项并聚焦名称输入框。
<<< END U005119 >>>
<<< UNIT U005120 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:784-784 | ctx=NewPackageScreen.on_button_pressed >>>
切换类型、提交或关闭。
<<< END U005120 >>>
<<< UNIT U005121 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:794-794 | ctx=NewPackageScreen.on_input_submitted >>>
任一输入框回车即提交。
<<< END U005121 >>>
<<< UNIT U005122 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:798-798 | ctx=NewPackageScreen.key_escape >>>
Esc 关闭对话框，放弃输入。
<<< END U005122 >>>
<<< UNIT U005123 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:802-802 | ctx=NewPackageScreen.submit >>>
校验名称。合法时关闭对话框并返回参数。
<<< END U005123 >>>
<<< UNIT U005124 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:969-969 | ctx=DevPage.activate >>>
首次显示时读取工作区快照。
<<< END U005124 >>>
<<< UNIT U005125 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:977-977 | ctx=DevPage.snapshot >>>
返回缓存快照，不启动子进程。
<<< END U005125 >>>
<<< UNIT U005126 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:982-982 | ctx=DevPage.packages >>>
返回缓存中的包记录。
<<< END U005126 >>>
<<< UNIT U005127 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:987-987 | ctx=DevPage.selected_package >>>
返回列表当前高亮项对应的包。
<<< END U005127 >>>
<<< UNIT U005128 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1002-1002 | ctx=DevPage.workspace_text >>>
返回顶部 workspace 面板当前文本。
<<< END U005128 >>>
<<< UNIT U005129 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1007-1007 | ctx=DevPage.header_text >>>
返回列标题行当前文本。
<<< END U005129 >>>
<<< UNIT U005130 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1012-1012 | ctx=DevPage.status_text >>>
返回状态栏当前文本。
<<< END U005130 >>>
<<< UNIT U005131 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1017-1017 | ctx=DevPage.detail_text >>>
返回详情栏当前文本。
<<< END U005131 >>>
<<< UNIT U005132 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1021-1021 | ctx=DevPage.row_texts >>>
返回最近一次渲染出的包行文本。
<<< END U005132 >>>
<<< UNIT U005133 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1025-1025 | ctx=DevPage.package_cells >>>
返回最近一次渲染出的包行各列取值，顺序与列表一致。
<<< END U005133 >>>
<<< UNIT U005134 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1029-1029 | ctx=DevPage.cache_age >>>
返回缓存自上次读取以来的秒数。从未读取时为无穷大。
<<< END U005134 >>>
<<< UNIT U005135 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1051-1051 | ctx=DevPage.output_title_text >>>
返回输出区标题行当前文本，含行数与跟随状态。
<<< END U005135 >>>
<<< UNIT U005136 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1056-1056 | ctx=DevPage.new_form_open >>>
返回新建包对话框是否打开。
<<< END U005136 >>>
<<< UNIT U005137 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1061-1061 | ctx=DevPage.new_hint_text >>>
返回新建包对话框的提示。对话框未打开时为空字符串。
<<< END U005137 >>>
<<< UNIT U005138 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1070-1070 | ctx=DevPage.test_args >>>
按空白拆分并返回测试输入框中的参数。
<<< END U005138 >>>
<<< UNIT U005139 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1124-1124 | ctx=DevPage.invalidate_cache >>>
清除缓存有效期，使下次请求重新读取数据。
<<< END U005139 >>>
<<< UNIT U005140 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1139-1139 | ctx=DevPage.open_new_form >>>
打开新建包对话框。操作运行期间不可用。
<<< END U005140 >>>
<<< UNIT U005141 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1157-1157 | ctx=DevPage.cancel_running_action >>>
请求终止运行中的操作。空闲时不调用数据源。
<<< END U005141 >>>
<<< UNIT U005142 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1485-1485 | ctx=DevPage.focus_primary >>>
聚焦包列表。列表为空时聚焦页面容器。
<<< END U005142 >>>
<<< UNIT U005143 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1505-1505 | ctx=DevPage.focus_output >>>
显示并聚焦输出区。无输出时显示提示。
<<< END U005143 >>>
<<< UNIT U005144 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/dev.py:1518-1518 | ctx=DevPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005144 >>>
<<< UNIT U005145 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:462-462 >>>
# 每次请求都解析当前实例，确保切换实例后子进程使用新目录。
<<< END U005145 >>>
<<< UNIT U005146 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:676-676 >>>
# 界面异常退出时事件循环可能先关闭，进程必须在解释器退出前终止。
<<< END U005146 >>>
<<< UNIT U005147 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:967-967 >>>
# 页脚只保留高频键。部署与打开浏览器等低频动作由按钮与详情提示承载。
<<< END U005147 >>>
<<< UNIT U005148 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1133-1133 >>>
# region 状态读取（供测试与 App 使用）
<<< END U005148 >>>
<<< UNIT U005149 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1161-1161 >>>
# noqa: BLE001 - 未挂载时按无选中处理
<<< END U005149 >>>
<<< UNIT U005150 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1230-1230 >>>
# region 数据读取
<<< END U005150 >>>
<<< UNIT U005151 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1237-1237 >>>
# 刷新可能改变目标集合，必须清除待确认状态。
<<< END U005151 >>>
<<< UNIT U005152 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1254-1254 >>>
# noqa: BLE001 - 数据源任意异常都不应中断界面
<<< END U005152 >>>
<<< UNIT U005153 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1269-1269 >>>
# 构建记录存在即视为已有可预览站点。本会话内的成功构建另由 _built 标记。
<<< END U005153 >>>
<<< UNIT U005154 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1284-1284 >>>
# region 渲染（只读缓存）
<<< END U005154 >>>
<<< UNIT U005155 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1289-1289 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005155 >>>
<<< UNIT U005156 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1325-1325 >>>
# noqa: BLE001 - 未挂载时跳过渲染
<<< END U005156 >>>
<<< UNIT U005157 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1338-1338 >>>
# 表头与数据行共用列宽计划，保证窄屏隐藏分组列后仍对齐。
<<< END U005157 >>>
<<< UNIT U005158 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1444-1444 >>>
# 预览按钮在启动与停止之间切换文字，键位不变。
<<< END U005158 >>>
<<< UNIT U005159 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1451-1451 >>>
# noqa: BLE001 - 尚未挂载时没有按钮可更新
<<< END U005159 >>>
<<< UNIT U005160 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1485-1485 >>>
# region 交互
<<< END U005160 >>>
<<< UNIT U005161 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1495-1495 >>>
# 待确认的部署必须与当前选择无关，换选中项时仍应复位以防误触。
<<< END U005161 >>>
<<< UNIT U005162 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1595-1595 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U005162 >>>
<<< UNIT U005163 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1620-1620 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U005163 >>>
<<< UNIT U005164 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1643-1643 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U005164 >>>
<<< UNIT U005165 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1685-1685 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U005165 >>>
<<< UNIT U005166 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1695-1695 >>>
# 启动期间页面可能已切走，此时立即停止，避免留下无人管理的服务。
<<< END U005166 >>>
<<< UNIT U005167 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1724-1724 >>>
# noqa: BLE001 - 停止失败仍需复位界面状态
<<< END U005167 >>>
<<< UNIT U005168 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1741-1741 >>>
# noqa: BLE001 - 浏览器调用失败只作为状态展示
<<< END U005168 >>>
<<< UNIT U005169 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1771-1771 >>>
# noqa: BLE001 - 数据源异常转换为状态展示
<<< END U005169 >>>
<<< UNIT U005170 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1781-1781 >>>
# 启动期间页面可能已切走，此时立即停止，避免留下无人管理的服务。
<<< END U005170 >>>
<<< UNIT U005171 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1848-1848 >>>
# noqa: BLE001 - 停止失败仍需复位界面状态
<<< END U005171 >>>
<<< UNIT U005172 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1860-1860 >>>
# noqa: BLE001 - 退出路径上不再报告停止失败
<<< END U005172 >>>
<<< UNIT U005173 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1868-1868 >>>
# 防抖窗口内忽略重复请求，避免叠加确认框。
<<< END U005173 >>>
<<< UNIT U005174 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1888-1888 >>>
# 关闭确认框后清除防抖记录，允许重新发起操作。
<<< END U005174 >>>
<<< UNIT U005175 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1907-1907 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U005175 >>>
<<< UNIT U005176 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1960-1960 >>>
# noqa: BLE001 - 退出路径上不再报告停止失败
<<< END U005176 >>>
<<< UNIT U005177 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:103-103 | ctx=DocsPageRow.display_title >>>
返回页面标题，默认使用路径。
<<< END U005177 >>>
<<< UNIT U005178 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:140-140 | ctx=DocsPackageRow.display_title >>>
返回展示标题，默认使用 key。
<<< END U005178 >>>
<<< UNIT U005179 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:144-144 | ctx=DocsPackageRow.haystack >>>
返回搜索用的匹配文本，已做大小写折叠。
<<< END U005179 >>>
<<< UNIT U005180 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:265-265 | ctx=DocsSourceError >>>
数据源不可用（子进程缺失、退出码非零或输出不是 JSON）。
<<< END U005180 >>>
<<< UNIT U005181 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:270-270 | ctx=DocsSource >>>
文档数据源接口。测试注入模拟对象，实际运行通过子进程访问。
<<< END U005181 >>>
<<< UNIT U005182 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:273-273 | ctx=DocsSource.load >>>
返回文档包、工具链与最近状态。
<<< END U005182 >>>
<<< UNIT U005183 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:276-276 | ctx=DocsSource.build >>>
构建指定包。``keys`` 为空时构建全部，输出行逐条交给 ``on_line``。
<<< END U005183 >>>
<<< UNIT U005184 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:279-279 | ctx=DocsSource.sync_theme >>>
同步主题模板 submodule，git 输出行逐条交给 ``on_line``。
<<< END U005184 >>>
<<< UNIT U005185 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:282-282 | ctx=DocsSource.install_dependencies >>>
安装主题依赖，npm 输出行逐条交给 ``on_line``。
<<< END U005185 >>>
<<< UNIT U005186 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:285-285 | ctx=DocsSource.start_server >>>
启动预览服务并返回站点 URL。
<<< END U005186 >>>
<<< UNIT U005187 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:288-288 | ctx=DocsSource.stop_server >>>
停止预览服务。
<<< END U005187 >>>
<<< UNIT U005188 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:291-291 | ctx=DocsSource.start_dev >>>
启动开发模式预览并返回站点 URL。就绪后的事件逐条交给 ``on_event``。
<<< END U005188 >>>
<<< UNIT U005189 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:294-294 | ctx=DocsSource.stop_dev >>>
停止开发模式预览。
<<< END U005189 >>>
<<< UNIT U005190 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:297-297 | ctx=DocsSource.deploy >>>
部署站点。``dry_run`` 为真时只统计将更改的文件。
<<< END U005190 >>>
<<< UNIT U005191 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:357-357 | ctx=StaticDocsSource.server_running >>>
返回预览服务是否处于运行状态。
<<< END U005191 >>>
<<< UNIT U005192 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:361-361 | ctx=StaticDocsSource.set_view >>>
替换模拟对象返回的视图。
<<< END U005192 >>>
<<< UNIT U005193 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:365-365 | ctx=StaticDocsSource.load >>>
见 :meth:`DocsSource.load`。
<<< END U005193 >>>
<<< UNIT U005194 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:370-370 | ctx=StaticDocsSource.build >>>
见 :meth:`DocsSource.build`。
<<< END U005194 >>>
<<< UNIT U005195 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:382-382 | ctx=StaticDocsSource.sync_theme >>>
见 :meth:`DocsSource.sync_theme`。
<<< END U005195 >>>
<<< UNIT U005196 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:389-389 | ctx=StaticDocsSource.install_dependencies >>>
见 :meth:`DocsSource.install_dependencies`。
<<< END U005196 >>>
<<< UNIT U005197 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:396-396 | ctx=StaticDocsSource.start_server >>>
见 :meth:`DocsSource.start_server`。
<<< END U005197 >>>
<<< UNIT U005198 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:404-404 | ctx=StaticDocsSource.stop_server >>>
见 :meth:`DocsSource.stop_server`。
<<< END U005198 >>>
<<< UNIT U005199 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:410-410 | ctx=StaticDocsSource.dev_running >>>
返回开发模式预览是否处于运行状态。
<<< END U005199 >>>
<<< UNIT U005200 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:414-414 | ctx=StaticDocsSource.start_dev >>>
见 :meth:`DocsSource.start_dev`。
<<< END U005200 >>>
<<< UNIT U005201 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:425-425 | ctx=StaticDocsSource.stop_dev >>>
见 :meth:`DocsSource.stop_dev`。
<<< END U005201 >>>
<<< UNIT U005202 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:430-430 | ctx=StaticDocsSource.deploy >>>
见 :meth:`DocsSource.deploy`。
<<< END U005202 >>>
<<< UNIT U005203 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:487-487 | ctx=SubprocessDocsSource.root >>>
返回实例根目录，依次采用显式路径、当前实例或自动定位结果。
<<< END U005203 >>>
<<< UNIT U005204 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:492-492 | ctx=SubprocessDocsSource.server_running >>>
返回预览服务子进程是否仍在运行。
<<< END U005204 >>>
<<< UNIT U005205 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:498-498 | ctx=SubprocessDocsSource.dev_running >>>
返回开发模式子进程是否仍在运行。
<<< END U005205 >>>
<<< UNIT U005206 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:503-503 | ctx=SubprocessDocsSource.load >>>
见 :meth:`DocsSource.load`。
<<< END U005206 >>>
<<< UNIT U005207 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:509-509 | ctx=SubprocessDocsSource.build >>>
见 :meth:`DocsSource.build`。``--json`` 输出构建摘要，stderr 逐行回传日志。
<<< END U005207 >>>
<<< UNIT U005208 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:517-517 | ctx=SubprocessDocsSource.deploy >>>
见 :meth:`DocsSource.deploy`。界面已确认，子进程带 ``--yes``。
<<< END U005208 >>>
<<< UNIT U005209 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:527-527 | ctx=SubprocessDocsSource.start_server >>>
启动 ``docs serve --json --no-build`` 并等待首行就绪事件。
<<< END U005209 >>>
<<< UNIT U005210 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:577-577 | ctx=SubprocessDocsSource.stop_server >>>
见 :meth:`DocsSource.stop_server`。先终止，超时后强制结束。
<<< END U005210 >>>
<<< UNIT U005211 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:586-586 | ctx=SubprocessDocsSource.start_dev >>>
启动 ``docs dev --json`` 并读取就绪事件。其余事件交给 ``on_event``。
<<< END U005211 >>>
<<< UNIT U005212 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:634-634 | ctx=SubprocessDocsSource.stop_dev >>>
见 :meth:`DocsSource.stop_dev`。先终止，超时后强制结束。
<<< END U005212 >>>
<<< UNIT U005213 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:809-809 | ctx=SubprocessDocsSource.sync_theme >>>
见 :meth:`DocsSource.sync_theme`。git 输出逐行回传。
<<< END U005213 >>>
<<< UNIT U005214 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:832-832 | ctx=SubprocessDocsSource.install_dependencies >>>
见 :meth:`DocsSource.install_dependencies`。npm 输出逐行回传。
<<< END U005214 >>>
<<< UNIT U005215 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1094-1094 | ctx=DocsPage.compose >>>
装配页面控件树。
<<< END U005215 >>>
<<< UNIT U005216 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1118-1118 | ctx=DocsPage.on_mount >>>
挂载后只装配控件。读取数据推迟到首次显示。
<<< END U005216 >>>
<<< UNIT U005217 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1123-1123 | ctx=DocsPage.activate >>>
首次显示时读取文档目录。
<<< END U005217 >>>
<<< UNIT U005218 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1130-1130 | ctx=DocsPage.focus_primary >>>
聚焦包列表。列表为空时聚焦页面容器，以保留全局键位。
<<< END U005218 >>>
<<< UNIT U005219 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1137-1137 | ctx=DocsPage.view >>>
返回最近一次读取的视图，不触发子进程。
<<< END U005219 >>>
<<< UNIT U005220 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1142-1142 | ctx=DocsPage.packages >>>
返回缓存中的全部文档包。
<<< END U005220 >>>
<<< UNIT U005221 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1147-1147 | ctx=DocsPage.visible_packages >>>
返回应用当前搜索词后的文档包。
<<< END U005221 >>>
<<< UNIT U005222 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1155-1155 | ctx=DocsPage.selected_package >>>
返回列表当前高亮项对应的文档包。
<<< END U005222 >>>
<<< UNIT U005223 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1170-1170 | ctx=DocsPage.selected_keys >>>
返回当前选中的包 key，按视图顺序排列。
<<< END U005223 >>>
<<< UNIT U005224 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1175-1175 | ctx=DocsPage.search_query >>>
返回当前搜索词。
<<< END U005224 >>>
<<< UNIT U005225 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1180-1180 | ctx=DocsPage.detail_text >>>
返回详情面板当前渲染出的纯文本。
<<< END U005225 >>>
<<< UNIT U005226 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1185-1185 | ctx=DocsPage.status_text >>>
返回状态栏当前文本。
<<< END U005226 >>>
<<< UNIT U005227 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1190-1190 | ctx=DocsPage.log_text >>>
返回日志面板当前文本。
<<< END U005227 >>>
<<< UNIT U005228 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1195-1195 | ctx=DocsPage.log_visible >>>
返回日志面板是否可见。
<<< END U005228 >>>
<<< UNIT U005229 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1200-1200 | ctx=DocsPage.preview_url >>>
返回运行中的预览地址（开发模式优先）。未运行时为空字符串。
<<< END U005229 >>>
<<< UNIT U005230 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1207-1207 | ctx=DocsPage.server_running >>>
返回静态预览服务是否处于运行状态。
<<< END U005230 >>>
<<< UNIT U005231 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1212-1212 | ctx=DocsPage.dev_running >>>
返回开发模式预览是否处于运行状态。
<<< END U005231 >>>
<<< UNIT U005232 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1217-1217 | ctx=DocsPage.dev_synced >>>
返回最近一次同步涉及的文件数。
<<< END U005232 >>>
<<< UNIT U005233 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1221-1221 | ctx=DocsPage.row_texts >>>
返回最近一次渲染出的列表行文本，供自动化检查核对宽度。
<<< END U005233 >>>
<<< UNIT U005234 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1225-1225 | ctx=DocsPage.column_text >>>
返回最近一次渲染出的表头文本。
<<< END U005234 >>>
<<< UNIT U005235 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1479-1479 | ctx=DocsPage.on_resize >>>
终端尺寸变化时按缓存重新排列，不重新读取数据。
<<< END U005235 >>>
<<< UNIT U005236 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1516-1516 | ctx=DocsPage.set_query >>>
设置搜索框内容，等价于用户键入。
<<< END U005236 >>>
<<< UNIT U005237 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1520-1520 | ctx=DocsPage.focus_search >>>
把焦点移到搜索框。
<<< END U005237 >>>
<<< UNIT U005238 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1524-1524 | ctx=DocsPage.clear_search >>>
清空搜索框。已为空时聚焦列表。
<<< END U005238 >>>
<<< UNIT U005239 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1574-1574 | ctx=DocsPage.request_build >>>
构建选区中的包。没有选区时构建全部。
<<< END U005239 >>>
<<< UNIT U005240 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1606-1606 | ctx=DocsPage.request_sync_theme >>>
同步主题模板 submodule。
<<< END U005240 >>>
<<< UNIT U005241 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1629-1629 | ctx=DocsPage.request_install_dependencies >>>
安装主题所需的 Node 依赖。
<<< END U005241 >>>
<<< UNIT U005242 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1652-1652 | ctx=DocsPage.toggle_serve >>>
启动或停止预览服务。
<<< END U005242 >>>
<<< UNIT U005243 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1709-1709 | ctx=DocsPage.stop_preview >>>
停止预览服务。未运行时只更新状态。
<<< END U005243 >>>
<<< UNIT U005244 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1734-1734 | ctx=DocsPage.open_preview >>>
在运行中的预览服务上打开浏览器。
<<< END U005244 >>>
<<< UNIT U005245 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1750-1750 | ctx=DocsPage.toggle_dev >>>
启动或停止开发模式预览。
<<< END U005245 >>>
<<< UNIT U005246 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1833-1833 | ctx=DocsPage.stop_dev >>>
停止开发模式预览。未运行时只更新状态。
<<< END U005246 >>>
<<< UNIT U005247 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1864-1864 | ctx=DocsPage.request_deploy >>>
弹出部署方式选择框。默认聚焦只读的试运行。
<<< END U005247 >>>
<<< UNIT U005248 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1925-1925 | ctx=DocsPage.reset_pending >>>
作废待确认状态。切换页面与本页状态变化时调用。
<<< END U005248 >>>
<<< UNIT U005249 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1929-1929 | ctx=DocsPage.dirty_note >>>
返回未结束的预览服务摘要，供退出与切换实例确认。
<<< END U005249 >>>
<<< UNIT U005250 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1936-1936 | ctx=DocsPage.on_hide >>>
离开页面时停止预览服务，避免后台子进程残留。
<<< END U005250 >>>
<<< UNIT U005251 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1940-1940 | ctx=DocsPage.on_unmount >>>
卸载页面时停止预览服务。
<<< END U005251 >>>
<<< UNIT U005252 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1964-1964 | ctx=DocsPage.action_refresh >>>
强制重新读取文档目录的键位动作。
<<< END U005252 >>>
<<< UNIT U005253 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1968-1968 | ctx=DocsPage.action_focus_search >>>
聚焦搜索框的键位动作。
<<< END U005253 >>>
<<< UNIT U005254 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1972-1972 | ctx=DocsPage.action_toggle_select >>>
切换当前项选中状态的键位动作。
<<< END U005254 >>>
<<< UNIT U005255 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1984-1984 | ctx=DocsPage.action_select_all >>>
选中当前可见全部文档包的键位动作。
<<< END U005255 >>>
<<< UNIT U005256 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:1993-1993 | ctx=DocsPage.action_clear_selection >>>
清空选区的键位动作。
<<< END U005256 >>>
<<< UNIT U005257 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2001-2001 | ctx=DocsPage.action_build >>>
构建选中包或全部包的键位动作。
<<< END U005257 >>>
<<< UNIT U005258 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2005-2005 | ctx=DocsPage.action_more >>>
打开低频操作菜单的键位动作。
<<< END U005258 >>>
<<< UNIT U005259 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2009-2009 | ctx=DocsPage.request_more >>>
弹出低频操作菜单，提供部署、同步主题、安装依赖与任务日志。
<<< END U005259 >>>
<<< UNIT U005260 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2042-2042 | ctx=DocsPage.toggle_log >>>
显示或隐藏任务日志面板。
<<< END U005260 >>>
<<< UNIT U005261 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2048-2048 | ctx=DocsPage.action_dev >>>
启动或停止开发模式预览的键位动作。
<<< END U005261 >>>
<<< UNIT U005262 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2052-2052 | ctx=DocsPage.action_serve >>>
启动或停止预览服务的键位动作。
<<< END U005262 >>>
<<< UNIT U005263 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2056-2056 | ctx=DocsPage.action_open >>>
在浏览器中打开预览地址的键位动作。
<<< END U005263 >>>
<<< UNIT U005264 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2060-2060 | ctx=DocsPage.action_clear_search >>>
清空搜索框的键位动作。
<<< END U005264 >>>
<<< UNIT U005265 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/docs.py:2066-2066 | ctx=DocsPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005265 >>>
<<< UNIT U005266 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:33-33 >>>
# 文案随当前语言解析，常量仅保存文案键。
<<< END U005266 >>>
<<< UNIT U005267 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:42-42 >>>
# 结论默认级别与 CLI 侧判定标准一致，端口与登录信息出现重复时报错，孤立配置只告警。
<<< END U005267 >>>
<<< UNIT U005268 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:374-374 >>>
# 实例根目录在每次请求时解析，使子进程目录与 AKARI_INSTANCE_DIR 跟随当前实例。
<<< END U005268 >>>
<<< UNIT U005269 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:397-397 >>>
# 非零退出码可能表示诊断发现问题，完整的 JSON 结果仍须展示。
<<< END U005269 >>>
<<< UNIT U005270 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:451-451 >>>
# 回车与单击均产生 Selected 消息，需单独绑定回车，才能保留单击查看详情的行为。
<<< END U005270 >>>
<<< UNIT U005271 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:592-592 >>>
# 后台请求可能在页面卸载后完成，访问控件前需检查挂载状态。
<<< END U005271 >>>
<<< UNIT U005272 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:653-653 >>>
# noqa: BLE001 - 数据源异常不应中断界面
<<< END U005272 >>>
<<< UNIT U005273 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:690-690 >>>
# 后台请求可能在页面卸载后完成，更新控件前需检查挂载状态。
<<< END U005273 >>>
<<< UNIT U005274 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:724-724 >>>
# 后台请求可能在页面卸载后完成，更新控件前需检查挂载状态。
<<< END U005274 >>>
<<< UNIT U005275 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:760-760 >>>
# 后台请求可能在页面卸载后完成，更新控件前需检查挂载状态。
<<< END U005275 >>>
<<< UNIT U005276 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:771-771 >>>
# 短屏优先显示结论与处理步骤，定位信息与详情按需滚动查看。
<<< END U005276 >>>
<<< UNIT U005277 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:798-798 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005277 >>>
<<< UNIT U005278 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:803-803 >>>
# 后台请求可能在页面卸载后完成，更新状态栏前需检查挂载状态。
<<< END U005278 >>>
<<< UNIT U005279 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:827-827 >>>
# 选项变化后，旧请求的结果无效，需取消旧请求并重新诊断。
<<< END U005279 >>>
<<< UNIT U005280 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:853-853 >>>
# 切换页面后当前状态栏不可见，使用通知显示跳转结果。
<<< END U005280 >>>
<<< UNIT U005281 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:161-161 | ctx=DoctorConflict.mark >>>
级别标记。未知级别用问号。
<<< END U005281 >>>
<<< UNIT U005282 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:166-166 | ctx=DoctorConflict.level_label >>>
级别的本地化标签。未知级别直接显示原值。
<<< END U005282 >>>
<<< UNIT U005283 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:172-172 | ctx=DoctorConflict.target_page >>>
返回处理页面键。无专用页面时按平台信息选择适配器页或概览页。
<<< END U005283 >>>
<<< UNIT U005284 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:180-180 | ctx=DoctorConflict.target_page_label >>>
处理页面的本地化名称。
<<< END U005284 >>>
<<< UNIT U005285 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:185-185 | ctx=DoctorConflict.next_step >>>
返回处理页面或 CLI 命令提示。
<<< END U005285 >>>
<<< UNIT U005286 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:210-210 | ctx=DoctorChecks.orphan_label >>>
孤立配置检查执行状态的本地化标签。
<<< END U005286 >>>
<<< UNIT U005287 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:244-244 | ctx=DoctorSnapshot.implementation_kind >>>
返回诊断结果的实现来源。
<<< END U005287 >>>
<<< UNIT U005288 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:249-249 | ctx=DoctorSnapshot.implementation_label >>>
实现来源的本地化标签。
<<< END U005288 >>>
<<< UNIT U005289 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:257-257 | ctx=DoctorSnapshot.passed >>>
返回诊断是否完成且未发现问题。
<<< END U005289 >>>
<<< UNIT U005290 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:326-326 | ctx=DoctorSourceError >>>
数据源不可用（子进程缺失、输出不是 JSON 或结构不符）。
<<< END U005290 >>>
<<< UNIT U005291 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:331-331 | ctx=DoctorSource >>>
诊断数据源接口。
<<< END U005291 >>>
<<< UNIT U005292 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:334-334 | ctx=DoctorSource.load_snapshot >>>
返回诊断结果。严格模式下警告视为失败，读取错误记录在快照的 ``errors`` 中。
<<< END U005292 >>>
<<< UNIT U005293 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:350-350 | ctx=StaticDoctorSource.load_snapshot >>>
见 :meth:`DoctorSource.load_snapshot`。
<<< END U005293 >>>
<<< UNIT U005294 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:382-382 | ctx=SubprocessDoctorSource.root >>>
返回实例根目录，依次采用显式路径、当前实例或自动定位结果。
<<< END U005294 >>>
<<< UNIT U005295 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:386-386 | ctx=SubprocessDoctorSource.load_snapshot >>>
见 :meth:`DoctorSource.load_snapshot`。
<<< END U005295 >>>
<<< UNIT U005296 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:566-566 | ctx=DoctorPage.activate >>>
首次显示时读取一次诊断结果。
<<< END U005296 >>>
<<< UNIT U005297 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:573-573 | ctx=DoctorPage.focus_primary >>>
聚焦冲突列表。列表为空时聚焦页面容器。
<<< END U005297 >>>
<<< UNIT U005298 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:578-578 | ctx=DoctorPage.snapshot >>>
返回缓存快照，不启动子进程。
<<< END U005298 >>>
<<< UNIT U005299 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:583-583 | ctx=DoctorPage.conflicts >>>
返回缓存中的结论列表。
<<< END U005299 >>>
<<< UNIT U005300 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:588-588 | ctx=DoctorPage.selected_conflict >>>
返回列表当前高亮项对应的结论。
<<< END U005300 >>>
<<< UNIT U005301 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:603-603 | ctx=DoctorPage.summary_text >>>
返回统计面板当前渲染出的文本。
<<< END U005301 >>>
<<< UNIT U005302 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:608-608 | ctx=DoctorPage.verdict_text >>>
返回结论行当前渲染出的文本。
<<< END U005302 >>>
<<< UNIT U005303 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:613-613 | ctx=DoctorPage.detail_text >>>
返回详情区当前渲染出的文本。
<<< END U005303 >>>
<<< UNIT U005304 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:618-618 | ctx=DoctorPage.status_text >>>
返回状态栏当前文本。
<<< END U005304 >>>
<<< UNIT U005305 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:623-623 | ctx=DoctorPage.status_key >>>
返回状态栏当前文案键。
<<< END U005305 >>>
<<< UNIT U005306 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:628-628 | ctx=DoctorPage.strict >>>
返回严格模式开关的当前取值。
<<< END U005306 >>>
<<< UNIT U005307 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:632-632 | ctx=DoctorPage.row_texts >>>
返回最近一次渲染出的冲突行文本。
<<< END U005307 >>>
<<< UNIT U005308 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:636-636 | ctx=DoctorPage.row_cells >>>
返回冲突行的级别标记、级别与结论，顺序与列表一致。
<<< END U005308 >>>
<<< UNIT U005309 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:640-640 | ctx=DoctorPage.refresh_report >>>
执行诊断并更新页面。读取期间禁用刷新按钮。
<<< END U005309 >>>
<<< UNIT U005310 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:846-846 | ctx=DoctorPage.open_selected_conflict >>>
打开当前结论对应的处理页面，并显示切换结果。
<<< END U005310 >>>
<<< UNIT U005311 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/doctor.py:857-857 | ctx=DoctorPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005311 >>>
<<< UNIT U005312 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:19-19 >>>
# 环境操作包含依赖解析与安装，超时上限高于状态查询。
<<< END U005312 >>>
<<< UNIT U005313 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:29-29 >>>
# save 模式同时更新实例清单，once 模式仅更改当前环境。
<<< END U005313 >>>
<<< UNIT U005314 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:31-31 >>>
# 预览记录使用独立后缀，以区分实际执行。
<<< END U005314 >>>
<<< UNIT U005315 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:335-335 >>>
# 每次请求均解析当前实例，避免切换实例后继续访问旧路径。
<<< END U005315 >>>
<<< UNIT U005316 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:442-442 >>>
# 负退出码表示终止信号，转换为信号名称显示。
<<< END U005316 >>>
<<< UNIT U005317 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:627-627 >>>
# 包管理与解释器操作分组排列，窄屏优先在组间换行。
<<< END U005317 >>>
<<< UNIT U005318 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:687-687 >>>
# noqa: BLE001 - 未挂载时按无选中处理
<<< END U005318 >>>
<<< UNIT U005319 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:748-748 >>>
# noqa: BLE001 - 数据源异常不应中断界面
<<< END U005319 >>>
<<< UNIT U005320 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:763-763 >>>
# 操作结束后的自动刷新必须保留失败原因。
<<< END U005320 >>>
<<< UNIT U005321 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:775-775 >>>
# 忙碌、运行中或托管方式未知时三项都不可用，原因相同。
<<< END U005321 >>>
<<< UNIT U005322 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:892-892 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U005322 >>>
<<< UNIT U005323 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:925-925 >>>
# 对已安装的包提供升级选项，对应 CLI 的 -U 参数。
<<< END U005323 >>>
<<< UNIT U005324 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:986-986 >>>
# 未记录在清单中的包仍会更改当前环境，卸载前必须确认。
<<< END U005324 >>>
<<< UNIT U005325 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:1016-1016 >>>
# 包操作仅更改 site-packages，允许在实例运行期间执行。
<<< END U005325 >>>
<<< UNIT U005326 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:1032-1032 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U005326 >>>
<<< UNIT U005327 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:1044-1044 >>>
# 已导入的模块保留在进程中，更改包后需要重启实例。
<<< END U005327 >>>
<<< UNIT U005328 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:1123-1123 >>>
# 窄屏优先隐藏标记列，保留包名宽度。
<<< END U005328 >>>
<<< UNIT U005329 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:1134-1134 >>>
# 重建与落高亮交给 _compat.rebuild_rows，因为 clear() 的移除是异步的，顺序错了高亮会打在旧条目上。
<<< END U005329 >>>
<<< UNIT U005330 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/environment.py:1158-1158 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005330 >>>
<<< UNIT U005331 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:73-73 | ctx=EnvironmentPackage.tag_keys >>>
按显示顺序返回标记文案键。
<<< END U005331 >>>
<<< UNIT U005332 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:89-89 | ctx=EnvironmentPackage.tags_text >>>
返回标记列的文本。
<<< END U005332 >>>
<<< UNIT U005333 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:145-145 | ctx=EnvironmentState.mode_text >>>
返回托管方式的说明。
<<< END U005333 >>>
<<< UNIT U005334 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:153-153 | ctx=EnvironmentState.package_count >>>
返回已安装的包数量。探测失败时为 ``-1``。
<<< END U005334 >>>
<<< UNIT U005335 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:157-157 | ctx=EnvironmentState.count_text >>>
返回已安装包数量的展示文本。
<<< END U005335 >>>
<<< UNIT U005336 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:165-165 | ctx=EnvironmentState.requirement_text >>>
返回清单记录的运行库说明。
<<< END U005336 >>>
<<< UNIT U005337 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:171-171 | ctx=EnvironmentState.rows >>>
返回已安装包与清单记录的并集。
<<< END U005337 >>>
<<< UNIT U005338 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:183-183 | ctx=recorded_name >>>
提取清单记录中的包名。无法解析时返回空字符串。
<<< END U005338 >>>
<<< UNIT U005339 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:192-192 | ctx=requirement_matches >>>
判断一条记录是否指向某个包。
<<< END U005339 >>>
<<< UNIT U005340 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:205-205 | ctx=EnvironmentSourceError >>>
数据源不可用（子进程缺失、输出不是 JSON 或读取超时）。
<<< END U005340 >>>
<<< UNIT U005341 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:210-210 | ctx=EnvironmentSource >>>
环境状态与操作的数据源接口。
<<< END U005341 >>>
<<< UNIT U005342 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:213-213 | ctx=EnvironmentSource.state >>>
返回环境快照。
<<< END U005342 >>>
<<< UNIT U005343 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:216-216 | ctx=EnvironmentSource.running >>>
返回实例是否在运行。探测失败时返回 ``None``。
<<< END U005343 >>>
<<< UNIT U005344 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:219-219 | ctx=EnvironmentSource.action >>>
执行 ``adopt`` / ``release`` / ``recreate``。``dry_run`` 为真时只预览。
<<< END U005344 >>>
<<< UNIT U005345 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:222-222 | ctx=EnvironmentSource.add_package >>>
安装运行库。``save`` 为真时同时写入实例清单。
<<< END U005345 >>>
<<< UNIT U005346 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:225-225 | ctx=EnvironmentSource.remove_package >>>
卸载运行库。``save`` 为真时同时删除清单记录。
<<< END U005346 >>>
<<< UNIT U005347 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:286-286 | ctx=StaticEnvironmentSource.state >>>
见 :meth:`EnvironmentSource.state`。
<<< END U005347 >>>
<<< UNIT U005348 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:291-291 | ctx=StaticEnvironmentSource.running >>>
见 :meth:`EnvironmentSource.running`。
<<< END U005348 >>>
<<< UNIT U005349 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:296-296 | ctx=StaticEnvironmentSource.action >>>
见 :meth:`EnvironmentSource.action`。
<<< END U005349 >>>
<<< UNIT U005350 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:302-302 | ctx=StaticEnvironmentSource.add_package >>>
见 :meth:`EnvironmentSource.add_package`。
<<< END U005350 >>>
<<< UNIT U005351 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:308-308 | ctx=StaticEnvironmentSource.remove_package >>>
见 :meth:`EnvironmentSource.remove_package`。
<<< END U005351 >>>
<<< UNIT U005352 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:314-314 | ctx=StaticEnvironmentSource.set_state >>>
替换模拟对象返回的快照。
<<< END U005352 >>>
<<< UNIT U005353 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:344-344 | ctx=SubprocessEnvironmentSource.root >>>
返回实例根目录，依次采用显式路径、当前实例或自动定位结果。
<<< END U005353 >>>
<<< UNIT U005354 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:348-348 | ctx=SubprocessEnvironmentSource.state >>>
见 :meth:`EnvironmentSource.state`。
<<< END U005354 >>>
<<< UNIT U005355 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:381-381 | ctx=SubprocessEnvironmentSource.running >>>
通过锁文件读取实例运行状态。
<<< END U005355 >>>
<<< UNIT U005356 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:390-390 | ctx=SubprocessEnvironmentSource.action >>>
见 :meth:`EnvironmentSource.action`。``--yes`` 由界面代答。
<<< END U005356 >>>
<<< UNIT U005357 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:399-399 | ctx=SubprocessEnvironmentSource.add_package >>>
见 :meth:`EnvironmentSource.add_package`。
<<< END U005357 >>>
<<< UNIT U005358 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:408-408 | ctx=SubprocessEnvironmentSource.remove_package >>>
见 :meth:`EnvironmentSource.remove_package`。
<<< END U005358 >>>
<<< UNIT U005359 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:609-609 | ctx=EnvironmentPage.rows >>>
返回最近一次渲染出的包列表行。
<<< END U005359 >>>
<<< UNIT U005360 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:614-614 | ctx=EnvironmentPage.column_text >>>
返回最近一次渲染出的表头行。
<<< END U005360 >>>
<<< UNIT U005361 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:642-642 | ctx=EnvironmentPage.activate >>>
首次显示时读取环境快照。
<<< END U005361 >>>
<<< UNIT U005362 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:649-649 | ctx=EnvironmentPage.focus_primary >>>
聚焦包列表。列表为空时聚焦页面容器。
<<< END U005362 >>>
<<< UNIT U005363 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:654-654 | ctx=EnvironmentPage.state >>>
返回缓存中的环境快照，不重新读取数据。
<<< END U005363 >>>
<<< UNIT U005364 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:659-659 | ctx=EnvironmentPage.status_text >>>
返回状态栏当前文本。
<<< END U005364 >>>
<<< UNIT U005365 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:664-664 | ctx=EnvironmentPage.running >>>
返回最近一次运行状态探测结果。
<<< END U005365 >>>
<<< UNIT U005366 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:669-669 | ctx=EnvironmentPage.visible_packages >>>
返回按搜索词与过滤条件筛选后的包列表。
<<< END U005366 >>>
<<< UNIT U005367 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:681-681 | ctx=EnvironmentPage.selected_package >>>
返回列表中高亮的包记录。
<<< END U005367 >>>
<<< UNIT U005368 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:717-717 | ctx=EnvironmentPage.action_clear_search >>>
清空搜索词的键位动作，已为空时聚焦包列表。
<<< END U005368 >>>
<<< UNIT U005369 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:725-725 | ctx=EnvironmentPage.set_query >>>
设置搜索词，等价于用户键入。
<<< END U005369 >>>
<<< UNIT U005370 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:729-729 | ctx=EnvironmentPage.set_recorded_only >>>
设置是否仅显示清单中的包。
<<< END U005370 >>>
<<< UNIT U005371 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:772-772 | ctx=EnvironmentPage.request_interpreter >>>
弹出解释器菜单，只列出当前托管方式可用的操作。
<<< END U005371 >>>
<<< UNIT U005372 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:869-869 | ctx=EnvironmentPage.reset_pending >>>
作废待确认的解释器动作。切换页面时由 :meth:`TuiApp.show_page` 调用。
<<< END U005372 >>>
<<< UNIT U005373 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:899-899 | ctx=EnvironmentPage.request_install >>>
请求输入运行库需求声明，并选择安装方式。
<<< END U005373 >>>
<<< UNIT U005374 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:963-963 | ctx=EnvironmentPage.request_uninstall >>>
确认并卸载选中的包，可选择是否保留清单记录。
<<< END U005374 >>>
<<< UNIT U005375 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/environment.py:1205-1205 | ctx=EnvironmentPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005375 >>>
<<< UNIT U005376 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:35-35 >>>
# 日志模式须按当前语言显示，因此常量只保存文案键。
<<< END U005376 >>>
<<< UNIT U005377 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:206-206 >>>
# 区分文件状态查询与读取失败，以识别轮转导致的文件缺失。
<<< END U005377 >>>
<<< UNIT U005378 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:280-280 >>>
# 低频操作通过按钮或输入提示提供，避免页脚超出 80 列。
<<< END U005378 >>>
<<< UNIT U005379 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:389-389 >>>
# Widget.offset 表示控件位置，不能用于日志游标。
<<< END U005379 >>>
<<< UNIT U005380 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:451-451 >>>
# noqa: BLE001 - 枚举失败只更新状态栏
<<< END U005380 >>>
<<< UNIT U005381 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:498-498 >>>
# noqa: BLE001 - 读取失败只更新状态栏
<<< END U005381 >>>
<<< UNIT U005382 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:533-533 >>>
# noqa: BLE001 - 读取失败只更新状态栏
<<< END U005382 >>>
<<< UNIT U005383 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:560-560 >>>
# 用户向上滚动时暂停跟随，保留当前阅读位置。
<<< END U005383 >>>
<<< UNIT U005384 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:638-638 >>>
# 重建列表时 clear() 会把高亮清空，这条不是用户选择，按“不变”处理。
<<< END U005384 >>>
<<< UNIT U005385 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:691-691 >>>
# 重建与落高亮交给 _compat.rebuild_rows，因为 clear() 的移除是异步的，顺序错了高亮会打在旧条目上。
<<< END U005385 >>>
<<< UNIT U005386 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:695-695 >>>
# 文件计数基于完整清单，避免其他进程的计数随过滤条件变化。
<<< END U005386 >>>
<<< UNIT U005387 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:737-737 >>>
# noqa: BLE001 - 未挂载时没有滚动容器
<<< END U005387 >>>
<<< UNIT U005388 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:758-758 >>>
# 新增内容的滚动范围在布局后更新，须再次定位末尾，避免误判为用户向上滚动。
<<< END U005388 >>>
<<< UNIT U005389 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:766-766 >>>
# 状态栏可能截断，优先显示恢复提示与过滤结果。
<<< END U005389 >>>
<<< UNIT U005390 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:793-793 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005390 >>>
<<< UNIT U005391 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/logs.py:810-810 >>>
# 视口高度改变后，跟随状态须重新定位末尾。暂停时保留阅读位置。
<<< END U005391 >>>
<<< UNIT U005392 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:50-50 | ctx=LogSourceError >>>
数据源不可用（日志目录缺失、文件不可读或读取失败）。
<<< END U005392 >>>
<<< UNIT U005393 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:55-55 | ctx=LogSource >>>
日志数据源接口。测试注入模拟对象，生产环境直接读取文件系统。
<<< END U005393 >>>
<<< UNIT U005394 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:58-58 | ctx=LogSource.list_processes >>>
返回日志目录中出现过的进程名。
<<< END U005394 >>>
<<< UNIT U005395 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:61-61 | ctx=LogSource.list_files >>>
按进程过滤返回日志文件，最新的排在前面。
<<< END U005395 >>>
<<< UNIT U005396 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:64-64 | ctx=LogSource.read_since >>>
从 ``offset`` 起增量读取，只返回新增的完整行。
<<< END U005396 >>>
<<< UNIT U005397 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:67-67 | ctx=LogSource.read_tail >>>
读取文件尾部的若干行，并把 offset 对齐到已读位置。
<<< END U005397 >>>
<<< UNIT U005398 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:90-90 | ctx=StaticLogSource.append >>>
向指定文件追加行，模拟日志继续写入。
<<< END U005398 >>>
<<< UNIT U005399 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:94-94 | ctx=StaticLogSource.truncate >>>
用新的行列表替换文件内容，模拟轮转或截断。
<<< END U005399 >>>
<<< UNIT U005400 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:160-160 | ctx=FileLogSource.logs_path >>>
返回日志目录。未显式指定时按实例根目录拼接 ``logs``。
<<< END U005400 >>>
<<< UNIT U005401 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:343-343 | ctx=LogsPage.activate >>>
首次显示时枚举日志目录，并按周期跟随。
<<< END U005401 >>>
<<< UNIT U005402 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:352-352 | ctx=LogsPage.focus_primary >>>
聚焦进程列表，供上层在页面切换时调用。
<<< END U005402 >>>
<<< UNIT U005403 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:357-357 | ctx=LogsPage.processes >>>
返回可选的进程名，不含“全部进程”。
<<< END U005403 >>>
<<< UNIT U005404 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:362-362 | ctx=LogsPage.files >>>
返回当前进程过滤下可见的文件，按最新在前排序。
<<< END U005404 >>>
<<< UNIT U005405 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:367-367 | ctx=LogsPage.visible_files >>>
返回当前过滤条件下的文件，保留完整清单用于统计。
<<< END U005405 >>>
<<< UNIT U005406 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:374-374 | ctx=LogsPage.selected_process >>>
返回当前过滤的进程。``None`` 表示不过滤。
<<< END U005406 >>>
<<< UNIT U005407 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:379-379 | ctx=LogsPage.followed_file >>>
返回当前跟随的文件。
<<< END U005407 >>>
<<< UNIT U005408 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:383-383 | ctx=LogsPage.process_labels >>>
返回最近一次渲染出的进程行文本，供自动化检查核对计数。
<<< END U005408 >>>
<<< UNIT U005409 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:388-388 | ctx=LogsPage.read_offset >>>
返回当前读取偏移。文件数据源以字节为单位。
<<< END U005409 >>>
<<< UNIT U005410 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:394-394 | ctx=LogsPage.paused >>>
返回是否处于暂停跟随状态。
<<< END U005410 >>>
<<< UNIT U005411 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:399-399 | ctx=LogsPage.debug_preference >>>
返回 debug 偏好（``auto`` / ``info`` / ``debug``）。
<<< END U005411 >>>
<<< UNIT U005412 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:404-404 | ctx=LogsPage.debug_label >>>
返回 debug 偏好的本地化标签。
<<< END U005412 >>>
<<< UNIT U005413 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:410-410 | ctx=LogsPage.last_chunk >>>
返回最近一次增量读取结果，供检查 offset 是否生效。
<<< END U005413 >>>
<<< UNIT U005414 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:415-415 | ctx=LogsPage.buffer_lines >>>
返回显示缓冲中的行。
<<< END U005414 >>>
<<< UNIT U005415 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:420-420 | ctx=LogsPage.dropped_lines >>>
返回显示缓冲丢弃的行数。
<<< END U005415 >>>
<<< UNIT U005416 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:425-425 | ctx=LogsPage.filter_keyword >>>
返回关键词过滤条件。空字符串表示不过滤。
<<< END U005416 >>>
<<< UNIT U005417 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:430-430 | ctx=LogsPage.filter_hits >>>
返回关键词在当前缓冲中的命中行数。未启用过滤时为 0。
<<< END U005417 >>>
<<< UNIT U005418 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:435-435 | ctx=LogsPage.visible_text >>>
返回日志面板当前渲染出的纯文本。
<<< END U005418 >>>
<<< UNIT U005419 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:440-440 | ctx=LogsPage.status_text >>>
返回状态栏当前文本。
<<< END U005419 >>>
<<< UNIT U005420 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:444-444 | ctx=LogsPage.refresh_files >>>
重新枚举进程与文件，必要时切换跟随目标并载入目标尾部。
<<< END U005420 >>>
<<< UNIT U005421 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:570-570 | ctx=LogsPage.pause >>>
暂停跟随。offset 保持不变，恢复后从暂停位置继续。
<<< END U005421 >>>
<<< UNIT U005422 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:576-576 | ctx=LogsPage.resume >>>
恢复跟随，补读暂停期间新增的行并返回缓冲末尾。
<<< END U005422 >>>
<<< UNIT U005423 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:584-584 | ctx=LogsPage.toggle_pause >>>
在暂停与恢复之间切换。
<<< END U005423 >>>
<<< UNIT U005424 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:591-591 | ctx=LogsPage.clear_buffer >>>
清空显示缓冲，保留读取偏移。
<<< END U005424 >>>
<<< UNIT U005425 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:598-598 | ctx=LogsPage.set_filter >>>
设置关键词过滤框内容，等价于用户键入。
<<< END U005425 >>>
<<< UNIT U005426 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:602-602 | ctx=LogsPage.focus_filter >>>
聚焦关键词过滤框。
<<< END U005426 >>>
<<< UNIT U005427 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:606-606 | ctx=LogsPage.clear_filter >>>
清空关键词过滤。已为空时聚焦进程列表。
<<< END U005427 >>>
<<< UNIT U005428 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:624-624 | ctx=LogsPage.request_debug_menu >>>
弹出日志级别菜单，列出除当前偏好以外的模式。
<<< END U005428 >>>
<<< UNIT U005429 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/logs.py:816-816 | ctx=LogsPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005429 >>>
<<< UNIT U005430 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:16-16 >>>
# 迁移计划通常较长，预览输出使用独立的截断上限。
<<< END U005430 >>>
<<< UNIT U005431 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:22-22 >>>
# 请求防抖键与项目路径分离，避免同名值覆盖防抖记录。
<<< END U005431 >>>
<<< UNIT U005432 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:79-79 >>>
# 每次请求均解析当前实例，避免切换实例后继续访问旧路径。
<<< END U005432 >>>
<<< UNIT U005433 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:94-94 >>>
# 必须显式指定 --instance，确保迁移目标为界面当前实例。
<<< END U005433 >>>
<<< UNIT U005434 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:278-278 >>>
# 防抖窗口内忽略重复请求，避免叠加确认框。
<<< END U005434 >>>
<<< UNIT U005435 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:302-302 >>>
# 输入框与确认框均响应回车，记录提交时刻以防止连续按键误确认。
<<< END U005435 >>>
<<< UNIT U005436 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:309-309 >>>
# 确认框必须列明即将传递给 CLI 的参数。
<<< END U005436 >>>
<<< UNIT U005437 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:318-318 >>>
# 默认聚焦只读预览选项，避免连续回车直接执行迁移。
<<< END U005437 >>>
<<< UNIT U005438 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:339-339 >>>
# 预览不写入数据，无需执行确认防抖检查。
<<< END U005438 >>>
<<< UNIT U005439 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:342-342 >>>
# 防抖检查避免提交路径后的连续回车直接确认迁移。
<<< END U005439 >>>
<<< UNIT U005440 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:362-362 >>>
# 在操作开始时固定参数，避免后台任务执行期间读取变化中的表单状态。
<<< END U005440 >>>
<<< UNIT U005441 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:371-371 >>>
# noqa: BLE001 - 数据源异常转换为操作结果
<<< END U005441 >>>
<<< UNIT U005442 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:382-382 >>>
# 迁移成功后清除路径，避免后续操作复用已完成的目标。
<<< END U005442 >>>
<<< UNIT U005443 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:394-394 >>>
# 试运行沿用最近一次预览或迁移的源目录。没有可用源目录时禁用。
<<< END U005443 >>>
<<< UNIT U005444 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:414-414 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005444 >>>
<<< UNIT U005445 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/misc.py:421-421 >>>
# noqa: BLE001 - 未挂载时按无控件处理
<<< END U005445 >>>
<<< UNIT U005446 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:40-40 | ctx=MiscSource >>>
项目迁移数据源接口。
<<< END U005446 >>>
<<< UNIT U005447 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:43-43 | ctx=MiscSource.migrate_legacy >>>
迁移旧版项目到当前实例。``dry_run`` 为真时仅预览，``flags`` 为附加的 CLI 参数。
<<< END U005447 >>>
<<< UNIT U005448 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:58-58 | ctx=StaticMiscSource.migrate_legacy >>>
见 :meth:`MiscSource.migrate_legacy`。
<<< END U005448 >>>
<<< UNIT U005449 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:87-87 | ctx=SubprocessMiscSource.root >>>
返回实例根目录，依次采用显式路径、当前实例与自动定位结果。
<<< END U005449 >>>
<<< UNIT U005450 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:91-91 | ctx=SubprocessMiscSource.migrate_legacy >>>
见 :meth:`MiscSource.migrate_legacy`。
<<< END U005450 >>>
<<< UNIT U005451 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:222-222 | ctx=MiscPage.activate >>>
本页没有需要预取的数据。
<<< END U005451 >>>
<<< UNIT U005452 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:225-225 | ctx=MiscPage.focus_primary >>>
聚焦按钮。
<<< END U005452 >>>
<<< UNIT U005453 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:230-230 | ctx=MiscPage.status_text >>>
返回状态栏当前文本。
<<< END U005453 >>>
<<< UNIT U005454 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:235-235 | ctx=MiscPage.pending_project >>>
返回已输入、等待确认的项目路径。
<<< END U005454 >>>
<<< UNIT U005455 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:240-240 | ctx=MiscPage.output_text >>>
返回输出区当前显示的文本。
<<< END U005455 >>>
<<< UNIT U005456 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:245-245 | ctx=MiscPage.selected_flags >>>
返回当前勾选的开关，顺序与界面一致。
<<< END U005456 >>>
<<< UNIT U005457 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:254-254 | ctx=MiscPage.reset_pending >>>
作废待确认的迁移。切换页面时由 :meth:`TuiApp.show_page` 调用。
<<< END U005457 >>>
<<< UNIT U005458 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:274-274 | ctx=MiscPage.request_migrate >>>
请求迁移。未指定路径时先请求输入，再显示确认框。
<<< END U005458 >>>
<<< UNIT U005459 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/misc.py:436-436 | ctx=MiscPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005459 >>>
<<< UNIT U005460 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:29-29 >>>
# 状态与包类型保存为文案键，以便按当前语言解析标签。
<<< END U005460 >>>
<<< UNIT U005461 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:53-53 >>>
# 界面确认后使用 ``--yes``，避免子进程等待重复的交互确认。
<<< END U005461 >>>
<<< UNIT U005462 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:55-55 >>>
# 大批量卸载要求输入目标数量，以确认操作范围。
<<< END U005462 >>>
<<< UNIT U005463 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:63-63 >>>
# 进度条按解析、执行、重载、完成分阶段推进，阶段内的细粒度进度由子进程输出行承担。
<<< END U005463 >>>
<<< UNIT U005464 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:65-65 >>>
# 实时转发时保留的末尾行数，失败时作为详情展示。
<<< END U005464 >>>
<<< UNIT U005465 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:288-288 >>>
# 安装、卸载、更新的动作名，用于批量汇总与通知标题。
<<< END U005465 >>>
<<< UNIT U005466 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:293-293 >>>
# ``module add`` 只接受名字或 git 直接引用，含协议头的输入一律按仓库地址交给 CLI 的 ``--git``。
<<< END U005466 >>>
<<< UNIT U005467 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:298-299 >>>
# 拆出地址中的 ref 与 subdirectory 片段，交给 CLI 的同名选项。末段中的 ``@`` 才是 ref
# ``git@host`` 中的 ``@`` 属于 userinfo，解析规则与引擎一致。
<<< END U005467 >>>
<<< UNIT U005468 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:449-449 >>>
# 每次读取时解析实例根目录，确保切换实例后子进程使用当前实例。
<<< END U005468 >>>
<<< UNIT U005469 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:475-475 >>>
# 适配器由独立页面管理，模块页仅查询模块。
<<< END U005469 >>>
<<< UNIT U005470 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:637-637 >>>
# noqa: BLE001 - 对端实现未知，统一转成可展示的错误
<<< END U005470 >>>
<<< UNIT U005471 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:657-657 >>>
# noqa: BLE001 - 实例构造失败同样只作为降级原因上报
<<< END U005471 >>>
<<< UNIT U005472 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:710-710 >>>
# 页面键位仅在本页生效，避免隐藏页响应操作。低频键位由详情区提示以控制页脚宽度。
<<< END U005472 >>>
<<< UNIT U005473 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:828-828 >>>
# 多选按包名记录选区，刷新后只保留仍然存在的项，_anchor 是 Shift 扩展选择的起点。
<<< END U005473 >>>
<<< UNIT U005474 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:831-831 >>>
# 确认框使用防抖，避免鼠标双击或键盘连发产生重复弹窗。
<<< END U005474 >>>
<<< UNIT U005475 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:877-877 >>>
# region 状态读取（供测试与 App 使用）
<<< END U005475 >>>
<<< UNIT U005476 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:899-899 >>>
# noqa: BLE001 - 未挂载时按无选中处理
<<< END U005476 >>>
<<< UNIT U005477 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:909-909 >>>
# 名称需避免覆盖 Textual 的 Widget.query()。
<<< END U005477 >>>
<<< UNIT U005478 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:935-935 >>>
# region 数据读取
<<< END U005478 >>>
<<< UNIT U005479 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:942-942 >>>
# 刷新可能改变目标集合，必须清除待确认状态。
<<< END U005479 >>>
<<< UNIT U005480 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:962-962 >>>
# noqa: BLE001 - 数据源任意异常都不应中断界面
<<< END U005480 >>>
<<< UNIT U005481 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:969-969 >>>
# 适配器由独立页面管理。保留类型未知的记录，避免隐藏可管理的包。
<<< END U005481 >>>
<<< UNIT U005482 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:975-975 >>>
# 清除刷新后不存在的选中项，避免批量操作包含不可见的包。
<<< END U005482 >>>
<<< UNIT U005483 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:989-989 >>>
# 列表加载后恢复列表焦点，仅在焦点仍位于页面容器时执行，避免中断搜索输入。
<<< END U005483 >>>
<<< UNIT U005484 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:995-995 >>>
# 加载状态表可能不存在，读取失败时仍展示安装列表。
<<< END U005484 >>>
<<< UNIT U005485 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:998-998 >>>
# noqa: BLE001 - 数据源任意异常都只降级
<<< END U005485 >>>
<<< UNIT U005486 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1014-1014 >>>
# 已安装记录包含本地版本与依赖信息，合并时优先保留。软件源读取失败不影响已安装列表。
<<< END U005486 >>>
<<< UNIT U005487 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1021-1021 >>>
# noqa: BLE001 - 数据源任意异常都不应中断界面
<<< END U005487 >>>
<<< UNIT U005488 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1026-1026 >>>
# 数据源返回的适配器记录不参与模块列表合并。
<<< END U005488 >>>
<<< UNIT U005489 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1037-1037 >>>
# region 渲染（只读缓存）
<<< END U005489 >>>
<<< UNIT U005490 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1061-1061 >>>
# 表头与数据行共用列宽计划，确保隐藏列后仍保持对齐。
<<< END U005490 >>>
<<< UNIT U005491 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1078-1078 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005491 >>>
<<< UNIT U005492 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1091-1091 >>>
# 仅已安装且声明模块的包具有加载状态。
<<< END U005492 >>>
<<< UNIT U005493 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1096-1096 >>>
# 空间不足时隐藏简介列，优先保证名称可读。
<<< END U005493 >>>
<<< UNIT U005494 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1104-1104 >>>
# 加载状态列宽不足 4 时隐藏该列，避免显示无法识别的截断状态。
<<< END U005494 >>>
<<< UNIT U005495 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1115-1115 >>>
# 首列是选中位，高亮条只表示光标所在，选中集合才是批量操作的操作对象。
<<< END U005495 >>>
<<< UNIT U005496 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1209-1209 >>>
# 安装按钮允许输入新的目标，不受当前选中包的安装状态限制。
<<< END U005496 >>>
<<< UNIT U005497 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1212-1212 >>>
# 更新始终可用，全量更新不依赖光标与选区。
<<< END U005497 >>>
<<< UNIT U005498 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1228-1228 >>>
# region 交互
<<< END U005498 >>>
<<< UNIT U005499 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1244-1244 >>>
# 待确认的卸载操作必须与当前高亮目标一致。
<<< END U005499 >>>
<<< UNIT U005500 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1285-1285 >>>
# 未安装的高亮项可直接作为目标。其他情况使用搜索词预填安装输入框。
<<< END U005500 >>>
<<< UNIT U005501 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1328-1328 >>>
# 安装会改动实例环境并补充配置，单字母键触发时须先确认目标。
<<< END U005501 >>>
<<< UNIT U005502 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1384-1384 >>>
# 子进程的 cwd 是实例根目录，相对路径按它解析才能与 CLI 的 -e 获取到同一个目录。
<<< END U005502 >>>
<<< UNIT U005503 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1408-1408 >>>
# Git 与可编辑安装的目标由选项指定，记录仅提供状态栏中的名称。
<<< END U005503 >>>
<<< UNIT U005504 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1415-1415 >>>
# 防抖用于避免鼠标双击或键盘连发产生重复确认框。
<<< END U005504 >>>
<<< UNIT U005505 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1440-1440 >>>
# 关闭确认框后清除防抖记录，允许重新发起操作。
<<< END U005505 >>>
<<< UNIT U005506 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1449-1449 >>>
# 全量更新的目标名仅用于展示，实际目标由 CLI 的 ``--all`` 枚举。
<<< END U005506 >>>
<<< UNIT U005507 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1511-1511 >>>
# 反向依赖由 CLI 返回。只有存在依赖时才提供级联卸载。
<<< END U005507 >>>
<<< UNIT U005508 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1596-1596 >>>
# 加载操作仅适用于已安装且声明模块的包。
<<< END U005508 >>>
<<< UNIT U005509 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1604-1604 >>>
# 批量目标按安装状态筛选，避免对同一选区执行无效操作。
<<< END U005509 >>>
<<< UNIT U005510 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1607-1607 >>>
# 更新与卸载同取已安装项
<<< END U005510 >>>
<<< UNIT U005511 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1611-1611 >>>
# 卸载与更新都只作用于已安装项。
<<< END U005511 >>>
<<< UNIT U005512 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1637-1637 >>>
# 清空选区时同步清除待确认状态。
<<< END U005512 >>>
<<< UNIT U005513 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1654-1654 >>>
# Shift 扩展选择替换上次范围，避免反向移动时保留已移出范围的记录。
<<< END U005513 >>>
<<< UNIT U005514 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1667-1667 >>>
# 重绘会按 _selected_key 恢复高亮项，需先同步当前目标。
<<< END U005514 >>>
<<< UNIT U005515 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1681-1681 >>>
# 点击事件由 ListItem 冒泡，需检查来源以排除列表外的控件。
<<< END U005515 >>>
<<< UNIT U005516 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1746-1746 >>>
# 批量操作中单项失败不影响其余目标，失败结果在全部操作结束后汇总。
<<< END U005516 >>>
<<< UNIT U005517 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1748-1748 >>>
# 单项操作保留数据源的结果说明，批量操作统一汇总。
<<< END U005517 >>>
<<< UNIT U005518 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1764-1764 >>>
# noqa: BLE001 - 数据源任意异常都转成结果展示
<<< END U005518 >>>
<<< UNIT U005519 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1778-1778 >>>
# 回调由工作线程之外的异步读取循环调用，因此只写入字段并直接刷新控件，不触发读取数据。
<<< END U005519 >>>
<<< UNIT U005520 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1794-1794 >>>
# 操作成功的目标退出选区，保留失败目标以便重试。
<<< END U005520 >>>
<<< UNIT U005521 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:104-104 | ctx=ModuleRecord.installed >>>
判断该模块是否已安装。
<<< END U005521 >>>
<<< UNIT U005522 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:109-109 | ctx=ModuleRecord.state_label >>>
返回状态的本地化标签。
<<< END U005522 >>>
<<< UNIT U005523 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:115-115 | ctx=ModuleRecord.kind_label >>>
返回该类型的本地化标签，未知时给出“未声明”。
<<< END U005523 >>>
<<< UNIT U005524 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:120-120 | ctx=ModuleRecord.haystack >>>
返回搜索用的匹配文本，已做大小写折叠。
<<< END U005524 >>>
<<< UNIT U005525 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:160-160 | ctx=ModuleSourceError >>>
数据源不可用（子进程缺失、退出码非零或输出不是 JSON）。
<<< END U005525 >>>
<<< UNIT U005526 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:201-201 | ctx=StaticModuleSource.list_modules >>>
见 :meth:`ModuleSource.list_modules`。
<<< END U005526 >>>
<<< UNIT U005527 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:206-206 | ctx=StaticModuleSource.list_available >>>
见 :meth:`ModuleSource.list_available`。
<<< END U005527 >>>
<<< UNIT U005528 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:211-211 | ctx=StaticModuleSource.load_states >>>
见 :meth:`ModuleSource.load_states`。
<<< END U005528 >>>
<<< UNIT U005529 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:216-216 | ctx=StaticModuleSource.install >>>
见 :meth:`ModuleSource.install`。
<<< END U005529 >>>
<<< UNIT U005530 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:222-222 | ctx=StaticModuleSource.uninstall >>>
见 :meth:`ModuleSource.uninstall`。
<<< END U005530 >>>
<<< UNIT U005531 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:236-236 | ctx=StaticModuleSource.stream_operation >>>
见 :meth:`ModuleSource.stream_operation`。模拟数据源直接回放固定输出。
<<< END U005531 >>>
<<< UNIT U005532 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:249-249 | ctx=ModuleSource >>>
模块数据源接口。测试注入模拟对象，实际运行通过子进程访问。
<<< END U005532 >>>
<<< UNIT U005533 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:252-252 | ctx=ModuleSource.list_modules >>>
返回全部模块记录。
<<< END U005533 >>>
<<< UNIT U005534 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:255-255 | ctx=ModuleSource.list_available >>>
返回可安装的模块记录，含尚未安装的项。
<<< END U005534 >>>
<<< UNIT U005535 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:258-258 | ctx=ModuleSource.load_states >>>
返回模块名到全局加载状态的映射。``None`` 表示尚无记录。
<<< END U005535 >>>
<<< UNIT U005536 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:261-261 | ctx=ModuleSource.install >>>
安装给定记录。
<<< END U005536 >>>
<<< UNIT U005537 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:264-264 | ctx=ModuleSource.uninstall >>>
卸载给定记录。
<<< END U005537 >>>
<<< UNIT U005538 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:323-323 | ctx=sort_key >>>
列表按已安装优先、其次按名称升序（大小写不敏感）排序。
<<< END U005538 >>>
<<< UNIT U005539 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:458-458 | ctx=SubprocessModuleSource.root >>>
返回实例根目录路径，显式给定优先，其次为界面当前选中的实例，最后自动定位。
<<< END U005539 >>>
<<< UNIT U005540 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:462-462 | ctx=SubprocessModuleSource.list_modules >>>
见 :meth:`ModuleSource.list_modules`。
<<< END U005540 >>>
<<< UNIT U005541 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:473-473 | ctx=SubprocessModuleSource.list_available >>>
返回当前实例软件源中的可安装模块及安装状态。
<<< END U005541 >>>
<<< UNIT U005542 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:490-490 | ctx=SubprocessModuleSource.install >>>
见 :meth:`ModuleSource.install`。
<<< END U005542 >>>
<<< UNIT U005543 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:496-496 | ctx=SubprocessModuleSource.uninstall >>>
见 :meth:`ModuleSource.uninstall`。
<<< END U005543 >>>
<<< UNIT U005544 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:510-510 | ctx=SubprocessModuleSource.stream_operation >>>
执行模块操作，并通过异步读取子进程输出报告进度。
<<< END U005544 >>>
<<< UNIT U005545 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:560-560 | ctx=SubprocessModuleSource.cli_argv >>>
构造调用本 CLI 的 argv，规则见 :mod:`akaribot.cli.tui.cli_process`。
<<< END U005545 >>>
<<< UNIT U005546 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:588-588 | ctx=SubprocessModuleSource.load_states >>>
通过 ``module status --json`` 读取加载状态。实例未运行时仍可读取已有记录。
<<< END U005546 >>>
<<< UNIT U005547 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:844-844 | ctx=ModulesPage.compose >>>
装配页面控件树。
<<< END U005547 >>>
<<< UNIT U005548 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:867-867 | ctx=ModulesPage.on_mount >>>
挂载后只装配控件。读取数据推迟到首次显示。
<<< END U005548 >>>
<<< UNIT U005549 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:871-871 | ctx=ModulesPage.activate >>>
首次显示时读取模块列表。
<<< END U005549 >>>
<<< UNIT U005550 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:881-881 | ctx=ModulesPage.records >>>
返回缓存中的全部记录，不触发子进程。
<<< END U005550 >>>
<<< UNIT U005551 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:886-886 | ctx=ModulesPage.visible_records >>>
返回应用当前搜索词后的记录。
<<< END U005551 >>>
<<< UNIT U005552 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:893-893 | ctx=ModulesPage.selected_record >>>
返回列表当前高亮项对应的记录。
<<< END U005552 >>>
<<< UNIT U005553 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:908-908 | ctx=ModulesPage.search_query >>>
返回当前搜索词。
<<< END U005553 >>>
<<< UNIT U005554 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:914-914 | ctx=ModulesPage.detail_text >>>
返回详情面板当前渲染出的纯文本。
<<< END U005554 >>>
<<< UNIT U005555 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:919-919 | ctx=ModulesPage.status_text >>>
返回状态栏当前文本。
<<< END U005555 >>>
<<< UNIT U005556 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:924-924 | ctx=ModulesPage.stream_lines >>>
返回最近一次模块操作的子进程输出，供故障排查与自动化验证。
<<< END U005556 >>>
<<< UNIT U005557 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:928-928 | ctx=ModulesPage.cache_age >>>
返回缓存自上次读取以来的秒数。从未读取时为无穷大。
<<< END U005557 >>>
<<< UNIT U005558 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1006-1006 | ctx=ModulesPage.load_state_text >>>
返回某条记录的加载状态文本，供列表与详情展示。
<<< END U005558 >>>
<<< UNIT U005559 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1031-1031 | ctx=ModulesPage.invalidate_cache >>>
使缓存立即失效，下一次读取必定通过数据源获取。
<<< END U005559 >>>
<<< UNIT U005560 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1053-1053 | ctx=ModulesPage.row_texts >>>
返回最近一次渲染出的列表行文本，供自动化检查核对宽度。
<<< END U005560 >>>
<<< UNIT U005561 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1057-1057 | ctx=ModulesPage.column_text >>>
返回最近一次渲染出的表头文本。
<<< END U005561 >>>
<<< UNIT U005562 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1222-1222 | ctx=ModulesPage.on_resize >>>
终端尺寸变化时按缓存重新排列，不重新读取数据。
<<< END U005562 >>>
<<< UNIT U005563 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1269-1269 | ctx=ModulesPage.set_query >>>
设置搜索框内容，等价于用户键入。
<<< END U005563 >>>
<<< UNIT U005564 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1273-1273 | ctx=ModulesPage.focus_search >>>
把焦点移到搜索框。
<<< END U005564 >>>
<<< UNIT U005565 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1277-1277 | ctx=ModulesPage.clear_search >>>
清空搜索框。已为空时聚焦列表。
<<< END U005565 >>>
<<< UNIT U005566 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1303-1303 | ctx=ModulesPage.request_install >>>
安装选区或未安装的高亮项。无可安装目标时打开安装输入框。
<<< END U005566 >>>
<<< UNIT U005567 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1413-1413 | ctx=ModulesPage.request_update >>>
发起更新，弹出选择框决定更新选中项还是全部已安装包。
<<< END U005567 >>>
<<< UNIT U005568 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1580-1580 | ctx=ModulesPage.request_toggle_load >>>
加载选中包的模块。全部已加载时取消加载。
<<< END U005568 >>>
<<< UNIT U005569 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1615-1615 | ctx=ModulesPage.action_toggle_select >>>
切换当前项选中状态的键位动作（对应 Ctrl+点击）。
<<< END U005569 >>>
<<< UNIT U005570 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1627-1627 | ctx=ModulesPage.action_select_all >>>
选中当前可见全部项的键位动作（受搜索与筛选影响）。
<<< END U005570 >>>
<<< UNIT U005571 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1636-1636 | ctx=ModulesPage.action_clear_selection >>>
清空选区的键位动作。
<<< END U005571 >>>
<<< UNIT U005572 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1646-1646 | ctx=ModulesPage.action_extend_up >>>
光标上移并扩展选区的键位动作。
<<< END U005572 >>>
<<< UNIT U005573 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1650-1650 | ctx=ModulesPage.action_extend_down >>>
光标下移并扩展选区的键位动作。
<<< END U005573 >>>
<<< UNIT U005574 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1680-1680 | ctx=ModulesPage.on_click >>>
处理列表选择，普通点击单选，Ctrl 点击切换，Shift 点击扩展选择。
<<< END U005574 >>>
<<< UNIT U005575 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1835-1835 | ctx=ModulesPage.focus_primary >>>
聚焦列表。列表为空时聚焦页面容器，加载后恢复列表焦点。
<<< END U005575 >>>
<<< UNIT U005576 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1839-1839 | ctx=ModulesPage.reset_pending >>>
作废待确认状态。切换页面与本页状态变化时调用。
<<< END U005576 >>>
<<< UNIT U005577 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1843-1843 | ctx=ModulesPage.action_refresh >>>
强制重新读取列表的键位动作。
<<< END U005577 >>>
<<< UNIT U005578 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1847-1847 | ctx=ModulesPage.action_focus_search >>>
聚焦搜索框的键位动作。
<<< END U005578 >>>
<<< UNIT U005579 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1851-1851 | ctx=ModulesPage.action_install >>>
安装当前目标的键位动作。
<<< END U005579 >>>
<<< UNIT U005580 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1855-1855 | ctx=ModulesPage.action_uninstall >>>
卸载当前目标的键位动作。
<<< END U005580 >>>
<<< UNIT U005581 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1859-1859 | ctx=ModulesPage.action_update >>>
更新选中项或全部已安装包的键位动作。
<<< END U005581 >>>
<<< UNIT U005582 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1863-1863 | ctx=ModulesPage.action_toggle_load >>>
加载或卸载选中项声明模块的快捷键操作。
<<< END U005582 >>>
<<< UNIT U005583 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1867-1867 | ctx=ModulesPage.action_clear_search >>>
清空搜索框的键位动作。
<<< END U005583 >>>
<<< UNIT U005584 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/modules.py:1873-1873 | ctx=ModulesPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005584 >>>
<<< UNIT U005585 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:26-26 >>>
# 停止超时由 CLI 处理，界面等待操作结果。
<<< END U005585 >>>
<<< UNIT U005586 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:30-30 >>>
# 状态与表头须按当前语言解析，因此常量只保存文案键。
<<< END U005586 >>>
<<< UNIT U005587 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:404-404 >>>
# 非零退出码对应的 JSON 仍包含失败详情，须先解析输出。
<<< END U005587 >>>
<<< UNIT U005588 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:460-460 >>>
# 低频操作通过按钮提供，避免页脚超出可用宽度。
<<< END U005588 >>>
<<< UNIT U005589 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:548-548 >>>
# 周期轮询不得使正在确认的操作失效。
<<< END U005589 >>>
<<< UNIT U005590 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:553-553 >>>
# noqa: BLE001 - 数据源异常都不应中断界面
<<< END U005590 >>>
<<< UNIT U005591 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:554-554 >>>
# 状态读取失败时，待确认操作失效。
<<< END U005591 >>>
<<< UNIT U005592 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:701-701 >>>
# noqa: BLE001 - 数据源异常都转成结果展示
<<< END U005592 >>>
<<< UNIT U005593 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:792-792 >>>
# noqa: BLE001 - 未挂载时按保守宽度排版
<<< END U005593 >>>
<<< UNIT U005594 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/run.py:844-844 >>>
# 实例运行时不能再启动指定适配器，菜单不列出这一项。
<<< END U005594 >>>
<<< UNIT U005595 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:72-72 | ctx=ProcessRecord.state_label >>>
返回带状态标记的本地化状态标签。
<<< END U005595 >>>
<<< UNIT U005596 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:79-79 | ctx=ProcessRecord.running >>>
该行是否表示进程正在运行。
<<< END U005596 >>>
<<< UNIT U005597 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:99-99 | ctx=RunSource >>>
运行控制数据源接口。测试注入模拟对象，运行时通过子进程执行。
<<< END U005597 >>>
<<< UNIT U005598 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:102-102 | ctx=RunSource.status >>>
返回状态表，至少一行。
<<< END U005598 >>>
<<< UNIT U005599 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:105-105 | ctx=RunSource.start >>>
启动实例。``adapter`` 非空时只启动该平台的适配器。
<<< END U005599 >>>
<<< UNIT U005600 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:108-108 | ctx=RunSource.stop >>>
停止当前实例。
<<< END U005600 >>>
<<< UNIT U005601 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:111-111 | ctx=RunSource.restart >>>
先停止再启动。
<<< END U005601 >>>
<<< UNIT U005602 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:219-219 | ctx=RunSourceError >>>
运行数据读取失败（CLI 调用失败或输出不可解析）。
<<< END U005602 >>>
<<< UNIT U005603 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:310-310 | ctx=SubprocessRunSource.probe_running >>>
探测实例是否在运行。探测失败返回 ``None``。
<<< END U005603 >>>
<<< UNIT U005604 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:508-508 | ctx=RunPage.activate >>>
首次显示时读取状态表，并按周期轮询进程与锁文件。
<<< END U005604 >>>
<<< UNIT U005605 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:517-517 | ctx=RunPage.focus_primary >>>
聚焦本页，供上层在页面切换时调用。
<<< END U005605 >>>
<<< UNIT U005606 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:522-522 | ctx=RunPage.records >>>
返回缓存中的状态表，不重新读取数据。
<<< END U005606 >>>
<<< UNIT U005607 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:527-527 | ctx=RunPage.running >>>
状态表中是否存在运行中的进程。
<<< END U005607 >>>
<<< UNIT U005608 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:532-532 | ctx=RunPage.table_text >>>
返回状态表当前渲染出的纯文本。
<<< END U005608 >>>
<<< UNIT U005609 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:537-537 | ctx=RunPage.status_text >>>
返回状态栏当前文本。
<<< END U005609 >>>
<<< UNIT U005610 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:574-574 | ctx=RunPage.reset_pending >>>
作废待确认状态。切换页面时由 App 调用。
<<< END U005610 >>>
<<< UNIT U005611 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:578-578 | ctx=RunPage.request_start >>>
请求启动当前实例。已运行时显示提示。
<<< END U005611 >>>
<<< UNIT U005612 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:590-590 | ctx=RunPage.request_stop >>>
请求停止当前实例。未运行时显示提示。
<<< END U005612 >>>
<<< UNIT U005613 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:607-607 | ctx=RunPage.request_restart >>>
发起重启。
<<< END U005613 >>>
<<< UNIT U005614 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:616-616 | ctx=RunPage.request_adapter_start >>>
请求输入平台名，确认后启动指定适配器。
<<< END U005614 >>>
<<< UNIT U005615 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:840-840 | ctx=RunPage.request_more >>>
弹出低频操作菜单，提供启动指定适配器与前台运行说明。
<<< END U005615 >>>
<<< UNIT U005616 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:864-864 | ctx=RunPage.show_foreground_hint >>>
前台运行会占用终端，界面内只给出命令。
<<< END U005616 >>>
<<< UNIT U005617 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/run.py:873-873 | ctx=RunPage.wait_for_idle >>>
等待本页发起的后台任务结束，供自动化检查与脚本使用。
<<< END U005617 >>>
<<< UNIT U005618 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:52-52 >>>
# 实时转发时保留的末尾行数，供失败时摘要使用。
<<< END U005618 >>>
<<< UNIT U005619 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:60-60 >>>
# 判定目录是否为 venv 的标志文件。
<<< END U005619 >>>
<<< UNIT U005620 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:62-63 >>>
# 清单未声明 requires_core_api 时的默认区间。与 core.registry.PackageManifest 及
# tools/build_registry.py 的 DEFAULT_REQUIRES_CORE_API 保持一致，工作区视图与 registry 视图必须一致。
<<< END U005620 >>>
<<< UNIT U005621 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:65-65 >>>
# 内置 uv 在 Windows 上必须是带 .exe 的完整文件名，因为 CreateProcess 不接受无扩展名的可执行文件。
<<< END U005621 >>>
<<< UNIT U005622 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:69-70 >>>
# 打包后本文件位于解包目录内的包层级里，资源根只在上面若干级。
# 设上限以免把无关祖先目录当成资源根。
<<< END U005622 >>>
<<< UNIT U005623 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:173-174 >>>
# 取值既可以是路径，也可以是 PATH 上的命令名（与 shell 用法一致）。不可用时返回 ``None``，
# 由调用方回退到内置资源或 PATH。
<<< END U005623 >>>
<<< UNIT U005624 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:299-299 >>>
# ref 只能跟在路径之后，路径末段里的 @ 才是 ref，userinfo 的 @（git@host）出现在更前面。
<<< END U005624 >>>
<<< UNIT U005625 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:995-995 >>>
# 兼容单个 packages 列表并逐项用 kind 字段分类的另一种写法。
<<< END U005625 >>>
<<< UNIT U005626 | py-comment | packages/akari-bot-cli/akaribot/cli/venv.py:1388-1389 >>>
# 这里比较的是环境而不是解释器文件。uv 创建的 venv 都把 bin/python 指向同一个基础解释器，
# 按 resolve() 后的文件比较会把两个不同的 venv 判定为同一个环境，导致操作全部被拒绝。
<<< END U005626 >>>
<<< UNIT U005627 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:75-75 | ctx=canonical >>>
将包名规范化为小写，并把下划线与点号统一为连字符。
<<< END U005627 >>>
<<< UNIT U005628 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:84-84 | ctx=bundled_uv_names >>>
内置 uv 的候选文件名，按尝试顺序排列。
<<< END U005628 >>>
<<< UNIT U005629 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:214-214 | ctx=create_venv_argv >>>
构造创建虚拟环境的 uv 命令，支持覆盖与可重定位模式。
<<< END U005629 >>>
<<< UNIT U005630 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:243-243 | ctx=install_argv >>>
``uv pip install --python <解释器>`` 的 argv。
<<< END U005630 >>>
<<< UNIT U005631 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:315-315 | ctx=uninstall_argv >>>
``uv pip uninstall --python <解释器>`` 的 argv。
<<< END U005631 >>>
<<< UNIT U005632 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:320-320 | ctx=dry_run_confirm_argv >>>
构造 ``--dry-run`` 用的解析检查 argv，只求解依赖而不写入磁盘。
<<< END U005632 >>>
<<< UNIT U005633 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:355-355 | ctx=CommandRunner.run >>>
执行命令并捕获文本输出。
<<< END U005633 >>>
<<< UNIT U005634 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:513-513 | ctx=InstalledDist.requirement >>>
重新安装到另一环境时使用的 uv 参数 token。
<<< END U005634 >>>
<<< UNIT U005635 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:536-536 | ctx=is_akari_dist >>>
判断一个已安装包是否属于 AkariBot（名字带前缀，或提供了模块／适配器入口点）。
<<< END U005635 >>>
<<< UNIT U005636 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:595-595 | ctx=entry_point_map >>>
把多个包的 entry points 摊平成 ``"<dist>|group|name" -> value``。
<<< END U005636 >>>
<<< UNIT U005637 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:623-623 | ctx=probe_api_version >>>
在目标解释器里读取 core 的公开 API 版本。
<<< END U005637 >>>
<<< UNIT U005638 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:749-749 | ctx=workspace_lookup >>>
在工作区索引里按包名、简称或 entry point 名查找。
<<< END U005638 >>>
<<< UNIT U005639 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:897-897 | ctx=find_workspace_root >>>
自某目录向上查找工作区根目录（含 ``packages`` 目录且其中有 pyproject 的目录）。
<<< END U005639 >>>
<<< UNIT U005640 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:941-941 | ctx=RegistryEntry >>>
registry.json 里的一条包记录（结构见 tasks 附录 A.3）。
<<< END U005640 >>>
<<< UNIT U005641 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:955-955 | ctx=RegistryEntry.from_mapping >>>
由一条 JSON 记录构造。
<<< END U005641 >>>
<<< UNIT U005642 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:972-972 | ctx=RegistryCatalog >>>
远端 registry.json 的本地视图。
<<< END U005642 >>>
<<< UNIT U005643 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:981-981 | ctx=RegistryCatalog.from_payload >>>
由 registry.json 的内容构造。
<<< END U005643 >>>
<<< UNIT U005644 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1077-1077 | ctx=RegistryCatalog.mark_cached >>>
标记为来自缓存。
<<< END U005644 >>>
<<< UNIT U005645 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1082-1082 | ctx=RegistryCatalog.find >>>
按包名、简称、provides_modules 或 legacy 名查找。
<<< END U005645 >>>
<<< UNIT U005646 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1094-1094 | ctx=RegistryCatalog.latest >>>
某包在 registry 里的最新版本。
<<< END U005646 >>>
<<< UNIT U005647 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1100-1100 | ctx=default_cache_dir >>>
返回 registry 缓存目录，``$AKARIBOT_CACHE_DIR`` 优先，否则为 ``~/.cache/akaribot``。
<<< END U005647 >>>
<<< UNIT U005648 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1122-1122 | ctx=registry_target >>>
在 registry 里解析包名，得到完整包名与版本约束。
<<< END U005648 >>>
<<< UNIT U005649 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1264-1264 | ctx=VenvStatus.package_count >>>
已安装的 akaribot 包数量。
<<< END U005649 >>>
<<< UNIT U005650 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1269-1269 | ctx=VenvStatus.installed_count >>>
环境里的全部已安装包数量。未探测时为 ``-1``。
<<< END U005650 >>>
<<< UNIT U005651 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1274-1274 | ctx=VenvStatus.core_version >>>
core 的版本。未安装时为 ``None``。
<<< END U005651 >>>
<<< UNIT U005652 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1867-1867 | ctx=installed_api_requirements >>>
列出已安装包中要求待安装包的依赖声明，供冲突说明引用。
<<< END U005652 >>>
<<< UNIT U005653 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1912-1912 | ctx=ConfigSnapshot.take >>>
抓取当前配置目录的快照。
<<< END U005653 >>>
<<< UNIT U005654 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1922-1922 | ctx=ConfigSnapshot.changed_paths >>>
列出快照之后新增或内容有变的配置文件。
<<< END U005654 >>>
<<< UNIT U005655 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1936-1936 | ctx=ConfigSnapshot.restore >>>
把配置目录恢复到快照状态，返回被动过的文件。
<<< END U005655 >>>
<<< UNIT U005656 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1960-1960 | ctx=count_placeholders >>>
统计给定配置文件里 ``<Replace me>`` 占位符的个数。
<<< END U005656 >>>
<<< UNIT U005657 | py-docstring | packages/akari-bot-cli/akaribot/cli/venv.py:1983-1983 | ctx=db_upgrade >>>
第 5 步，应用该包自己的数据库迁移。
<<< END U005657 >>>
<<< UNIT U005658 | py-docstring | packages/akari-bot-cli/akaribot/cli/windows.py:1-1 | ctx=<module> >>>
Windows 实例停止协议。
<<< END U005658 >>>
<<< UNIT U005659 | py-docstring | packages/akari-bot-cli/akaribot/cli/windows.py:10-10 | ctx=request_stop >>>
请求持有对应停止事件的实例自行退出。
<<< END U005659 >>>
<<< UNIT U005660 | cfg-comment | packages/akari-bot-cli/pyproject.toml:13-14 >>>
# 不依赖 core，全部实例操作经子进程调用 `python -m akaribot.core.entrypoints.*`，
# 使 CLI 能在实例 venv 之外运行（系统解释器、pipx 安装）。
<<< END U005660 >>>
<<< UNIT U005661 | cfg-comment | packages/akari-bot-cli/pyproject.toml:16-16 >>>
    # CLI 不依赖 core，本地化直接用发布在 PyPI 的 i18n 库
<<< END U005661 >>>
<<< UNIT U005662 | cfg-comment | packages/akari-bot-cli/pyproject.toml:19-19 >>>
    # 用于脚手架渲染（T5.5），core 也依赖它，但 CLI 不依赖 core，故自带
<<< END U005662 >>>
<<< UNIT U005663 | cfg-comment | packages/akari-bot-cli/pyproject.toml:24-24 >>>
    # 固定版本，因为 Textual 跨大版本常有 API 变动，全部调用统一经 akaribot.cli.tui._compat 转接
<<< END U005663 >>>
<<< UNIT U005664 | cfg-comment | packages/akari-bot-cli/pyproject.toml:28-28 >>>
    # 文档开发模式监听各包文档目录与主题目录，watchdog 提供跨平台原生事件源
<<< END U005664 >>>
<<< UNIT U005665 | cfg-comment | packages/akari-bot-cli/pyproject.toml:41-42 >>>
# 语言文件由 packages = ["akaribot"] 一并收录，无需 force-include（重复收录会让 hatchling 报
# "A second file is being added to the wheel archive at the same path"）。
<<< END U005665 >>>
<<< UNIT U005666 | py-comment | packages/akari-bot-cli/tests/test_adapter.py:40-40 >>>
# 涉及 core 的数据读取（registry / schema）全部由模拟对象接管，本命令仅读写配置文件。
<<< END U005666 >>>
<<< UNIT U005667 | py-comment | packages/akari-bot-cli/tests/test_adapter.py:82-82 >>>
# 说明段落由 locales 提供，这里只以选项表作为“该选项是否存在”的判断依据。
<<< END U005667 >>>
<<< UNIT U005668 | py-comment | packages/akari-bot-cli/tests/test_adapter.py:94-94 >>>
# 界面新增实例时只能从 JSON 得知尚无实例配置的已安装平台。
<<< END U005668 >>>
<<< UNIT U005669 | py-docstring | packages/akari-bot-cli/tests/test_adapter.py:117-117 | ctx=test_adapter_instance_remove >>>
cli.commands.adapter: 实例移除只删除配置测试
<<< END U005669 >>>
<<< UNIT U005670 | py-comment | packages/akari-bot-cli/tests/test_command_runner_streaming.py:99-99 >>>
# 受限环境里家目录缓存可能不可写。未显式指定 UV_CACHE_DIR 时取实例自己的缓存目录。
<<< END U005670 >>>
<<< UNIT U005671 | py-docstring | packages/akari-bot-cli/tests/test_command_runner_streaming.py:127-127 | ctx=test_command_runner_streaming >>>
cli.venv.CommandRunner: 实时转发与失败摘要测试
<<< END U005671 >>>
<<< UNIT U005672 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:39-39 >>>
# 片段里的新增键尚未并入 locales，合成一份合并后的语言目录后，检查才能取到真实渲染结果。
<<< END U005672 >>>
<<< UNIT U005673 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:53-53 >>>
# CLI 首次取文案时用包内 locales 重建快照，会覆盖合并目录。先取一次完成重建，再建合并快照。
<<< END U005673 >>>
<<< UNIT U005674 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:60-60 >>>
# 只响应 run_core_capture 的模拟对象，stdout 是 core 返回的文本，returncode 是它的退出码。
<<< END U005674 >>>
<<< UNIT U005675 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:104-104 >>>
# 表名清单取实例 config 目录下的全部 toml（含子目录），去重排序后一次下发给 core。
<<< END U005675 >>>
<<< UNIT U005676 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:118-118 >>>
# --json 原样透出 core 的结构，总数、逐表明细、已扫描与失败归集都不改写。
<<< END U005676 >>>
<<< UNIT U005677 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:128-128 >>>
# core 判定的结果里带失败表时，明细里逐条给出表名与原因。
<<< END U005677 >>>
<<< UNIT U005678 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:141-141 >>>
# 实例没有任何配置表时不传入 --tables，由 core 按自己的配置目录判定，输出如实写没有可统计的表。
<<< END U005678 >>>
<<< UNIT U005679 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:153-153 >>>
# core 退出码非零时透出它的最后一行原因，CLI 保持同一退出码。
<<< END U005679 >>>
<<< UNIT U005680 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:163-163 >>>
# 退出码为 0 但输出不是 JSON 时按格式错误报出，不把不完整的文本当统计结果。
<<< END U005680 >>>
<<< UNIT U005681 | py-comment | packages/akari-bot-cli/tests/test_config_placeholders.py:171-171 >>>
# 命令引用的键必须在片段里有定义，否则界面会把键名本身当文案显示。
<<< END U005681 >>>
<<< UNIT U005682 | py-docstring | packages/akari-bot-cli/tests/test_config_placeholders.py:72-72 | ctx=_FakeInstance.run_core_capture >>>
记录 entrypoint 与参数，返回预设输出。
<<< END U005682 >>>
<<< UNIT U005683 | py-docstring | packages/akari-bot-cli/tests/test_config_placeholders.py:180-180 | ctx=test_config_placeholders >>>
cli.config.placeholders: 占位符统计命令测试
<<< END U005683 >>>
<<< UNIT U005684 | py-comment | packages/akari-bot-cli/tests/test_db_rows.py:26-26 >>>
# 只响应 run_core_capture 的模拟对象，payload 是 core 要返回的 JSON，returncode 是它的退出码。
<<< END U005684 >>>
<<< UNIT U005685 | py-comment | packages/akari-bot-cli/tests/test_db_rows.py:126-126 >>>
# 不给条件时不下发 --filter / --search / --order-by，命令行保持最短。
<<< END U005685 >>>
<<< UNIT U005686 | py-comment | packages/akari-bot-cli/tests/test_db_rows.py:139-139 >>>
# core 把原因写入 stdout 的 JSON，退出码 2 表示用户错误。CLI 保持该退出码。
<<< END U005686 >>>
<<< UNIT U005687 | py-docstring | packages/akari-bot-cli/tests/test_db_rows.py:35-35 | ctx=_FakeInstance.run_core_capture >>>
记录 entrypoint 与参数，返回预设输出。
<<< END U005687 >>>
<<< UNIT U005688 | py-docstring | packages/akari-bot-cli/tests/test_db_rows.py:147-147 | ctx=test_db_rows >>>
cli.db.rows: 筛选、搜索、排序与分页展示测试
<<< END U005688 >>>
<<< UNIT U005689 | py-docstring | packages/akari-bot-cli/tests/test_docs_builder.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.builder`` 的构建编排、指纹复用与强制重建测试。
<<< END U005689 >>>
<<< UNIT U005690 | py-docstring | packages/akari-bot-cli/tests/test_docs_builder.py:222-222 | ctx=test_docs_builder >>>
cli.docs.builder: 构建编排与缓存复用
<<< END U005690 >>>
<<< UNIT U005691 | py-inline-comment | packages/akari-bot-cli/tests/test_docs_catalog.py:88-88 >>>
# noqa: BLE001 - 与实现一致，打包环境下没有 metadata
<<< END U005691 >>>
<<< UNIT U005692 | py-docstring | packages/akari-bot-cli/tests/test_docs_catalog.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.catalog`` 的清单解析、去重、CLI 本地合并与 registry 回退测试。
<<< END U005692 >>>
<<< UNIT U005693 | py-docstring | packages/akari-bot-cli/tests/test_docs_catalog.py:266-266 | ctx=test_docs_catalog >>>
cli.docs.catalog: 文档目录解析与回退
<<< END U005693 >>>
<<< UNIT U005694 | py-docstring | packages/akari-bot-cli/tests/test_docs_cli.py:787-787 | ctx=test_docs_cli >>>
cli.docs: 目录、构建、预览、状态与清理
<<< END U005694 >>>
<<< UNIT U005695 | py-docstring | packages/akari-bot-cli/tests/test_docs_config.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.config`` 的站点品牌、分组与分类图标、资源路径测试。
<<< END U005695 >>>
<<< UNIT U005696 | py-docstring | packages/akari-bot-cli/tests/test_docs_config.py:376-376 | ctx=test_docs_config >>>
cli.docs.config: 站点品牌、分组与分类图标、资源路径
<<< END U005696 >>>
<<< UNIT U005697 | py-docstring | packages/akari-bot-cli/tests/test_docs_deploy_cli.py:278-278 | ctx=test_docs_deploy_cli >>>
cli.docs.deploy: provider 解析、确认、结果格式约定与部署记录
<<< END U005697 >>>
<<< UNIT U005698 | py-docstring | packages/akari-bot-cli/tests/test_docs_deploy_s3.py:391-391 | ctx=test_docs_deploy_s3 >>>
cli.docs.deploy.s3: S3 兼容存储部署 provider 测试
<<< END U005698 >>>
<<< UNIT U005699 | py-docstring | packages/akari-bot-cli/tests/test_docs_deploy_vercel.py:235-235 | ctx=test_docs_deploy_vercel >>>
cli.docs.deploy.vercel: Vercel 部署 provider 测试
<<< END U005699 >>>
<<< UNIT U005700 | py-docstring | packages/akari-bot-cli/tests/test_docs_dev.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.dev`` 的镜像同步、变更归类与运行锁测试。
<<< END U005700 >>>
<<< UNIT U005701 | py-docstring | packages/akari-bot-cli/tests/test_docs_dev.py:97-97 | ctx=test_docs_dev >>>
cli.docs_engine.dev: 镜像同步、变更归类与运行锁
<<< END U005701 >>>
<<< UNIT U005702 | py-docstring | packages/akari-bot-cli/tests/test_docs_generator.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.generator`` 的站点源文件、侧栏与路径约束测试。
<<< END U005702 >>>
<<< UNIT U005703 | py-docstring | packages/akari-bot-cli/tests/test_docs_generator.py:1086-1086 | ctx=test_docs_generator >>>
cli.docs.generator: 站点生成与路径约束
<<< END U005703 >>>
<<< UNIT U005704 | py-docstring | packages/akari-bot-cli/tests/test_docs_server.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.server`` 的预览服务器 clean URL、目录索引与 404 测试。
<<< END U005704 >>>
<<< UNIT U005705 | py-docstring | packages/akari-bot-cli/tests/test_docs_server.py:89-89 | ctx=test_docs_server >>>
cli.docs.server: 本机静态预览
<<< END U005705 >>>
<<< UNIT U005706 | py-docstring | packages/akari-bot-cli/tests/test_docs_sigv4.py:140-140 | ctx=test_docs_sigv4 >>>
cli.docs.deploy.sigv4: SigV4 签名测试
<<< END U005706 >>>
<<< UNIT U005707 | py-docstring | packages/akari-bot-cli/tests/test_docs_theme.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.theme`` 的主题清单解析、外部模板与内置回退测试。
<<< END U005707 >>>
<<< UNIT U005708 | py-docstring | packages/akari-bot-cli/tests/test_docs_theme.py:149-149 | ctx=test_docs_theme >>>
cli.docs.theme: 内置回退、外部模板与来源校验
<<< END U005708 >>>
<<< UNIT U005709 | py-docstring | packages/akari-bot-cli/tests/test_docs_theme_sync.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.theme_sync`` 的主题模板 submodule 同步测试。
<<< END U005709 >>>
<<< UNIT U005710 | py-docstring | packages/akari-bot-cli/tests/test_docs_theme_sync.py:116-116 | ctx=test_docs_theme_sync >>>
cli.docs.theme_sync: submodule 同步、提交报告与失败映射
<<< END U005710 >>>
<<< UNIT U005711 | py-docstring | packages/akari-bot-cli/tests/test_docs_toolchain.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.toolchain`` 的版本探测、依赖安装与构建命令测试。
<<< END U005711 >>>
<<< UNIT U005712 | py-docstring | packages/akari-bot-cli/tests/test_docs_toolchain.py:267-267 | ctx=test_docs_toolchain >>>
cli.docs.toolchain: Node 工具链探测与命令组装
<<< END U005712 >>>
<<< UNIT U005713 | py-docstring | packages/akari-bot-cli/tests/test_docs_watch.py:1-1 | ctx=<module> >>>
``akaribot.cli.docs_engine.watch`` 的路径过滤、事件去重与批量返回测试。
<<< END U005713 >>>
<<< UNIT U005714 | py-docstring | packages/akari-bot-cli/tests/test_docs_watch.py:77-77 | ctx=test_docs_watch >>>
cli.docs_engine.watch: 文档目录监听与路径过滤
<<< END U005714 >>>
<<< UNIT U005715 | py-docstring | packages/akari-bot-cli/tests/test_frozen_uv.py:155-155 | ctx=test_frozen_uv >>>
cli.venv: 打包产物内置 uv 解析测试
<<< END U005715 >>>
<<< UNIT U005716 | py-docstring | packages/akari-bot-cli/tests/test_instance_cwd.py:76-76 | ctx=test_instance_process_cwd >>>
实例子进程一律以实例根目录为 cwd，从实例外调用也不例外。
<<< END U005716 >>>
<<< UNIT U005717 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:28-29 >>>
# 测试框架在每个用例前重新运行 ``load_modules()``，它会把当前快照连到 core 的命名空间。而 CLI 的
# ``Locale`` 按当前快照读取键，不切换回来就只会拿到键名。生产环境里 CLI 进程不加载 core，无此问题。
<<< END U005717 >>>
<<< UNIT U005718 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:85-85 >>>
# 只检查 returncode 既给不出“远端拒绝”的状态，也丢失了 core 给出的具体原因。
<<< END U005718 >>>
<<< UNIT U005719 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:152-152 >>>
# 实例确实未运行时没有可卸载的对象，卸载必须继续而不是被自己的保护条件挡住。
<<< END U005719 >>>
<<< UNIT U005720 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:192-192 >>>
# 只在这里记录一次，因为 run_streaming 是传输方式而非调用点。
<<< END U005720 >>>
<<< UNIT U005721 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:223-223 >>>
# remove() 自己解析实例，故连解析器一起替换，才能把子进程结果与运行状态都固定下来。
<<< END U005721 >>>
<<< UNIT U005722 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:262-262 >>>
# 卸载可能持续几分钟，必须使用实时转发，否则界面上看不出正在卸载还是无响应。
<<< END U005722 >>>
<<< UNIT U005723 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:353-353 >>>
# 先热卸载旧版本再热加载，否则服务端会以“包已注册”拒绝，更新永远无法生效。
<<< END U005723 >>>
<<< UNIT U005724 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:367-367 >>>
# 旧版本未卸载成功就不必再触发热加载（必定被拒绝），但要把“需要重启”如实写入结果。
<<< END U005724 >>>
<<< UNIT U005725 | py-comment | packages/akari-bot-cli/tests/test_instance_notify.py:382-382 >>>
# 适配器不支持整包热替换，沿用“安装后提示重启”的既有语义，不触发卸载。
<<< END U005725 >>>
<<< UNIT U005726 | py-docstring | packages/akari-bot-cli/tests/test_instance_notify.py:403-403 | ctx=test_cli_notify >>>
包变更通知的结果解析与卸载顺序。
<<< END U005726 >>>
<<< UNIT U005727 | py-comment | packages/akari-bot-cli/tests/test_instance_registry.py:71-71 >>>
# 同一个目录记录两次不该产生两条记录，也不该修改已有策略。
<<< END U005727 >>>
<<< UNIT U005728 | py-comment | packages/akari-bot-cli/tests/test_instance_registry.py:99-99 >>>
# 常被指向“装着实例的项目目录”，报错要直接给出可添加的子目录。
<<< END U005728 >>>
<<< UNIT U005729 | py-comment | packages/akari-bot-cli/tests/test_instance_registry.py:122-122 >>>
# 界面在实例目录里启动时自动记录，重复调用与指向非实例都要原样返回 None，不重复写入。
<<< END U005729 >>>
<<< UNIT U005730 | py-comment | packages/akari-bot-cli/tests/test_instance_registry.py:174-174 >>>
# 在任何实例之外时，默认实例就是“要管哪一个”的答案。
<<< END U005730 >>>
<<< UNIT U005731 | py-comment | packages/akari-bot-cli/tests/test_instance_registry.py:184-184 >>>
# add() 会把第一个实例设为默认，这里直接核对解析结果。
<<< END U005731 >>>
<<< UNIT U005732 | py-comment | packages/akari-bot-cli/tests/test_instance_registry.py:226-226 >>>
# 探测失败时返回 None 而不是抛出异常，清单里一格未知不应影响整页显示。
<<< END U005732 >>>
<<< UNIT U005733 | py-docstring | packages/akari-bot-cli/tests/test_instance_registry.py:237-237 | ctx=test_instance_registry >>>
cli.instances: 注册表与 instance 子命令测试
<<< END U005733 >>>
<<< UNIT U005734 | py-comment | packages/akari-bot-cli/tests/test_logs_cli.py:26-26 >>>
# 命令只读取实例根目录的 ``logs`` 子目录，模拟对象只需提供一个 root。
<<< END U005734 >>>
<<< UNIT U005735 | py-comment | packages/akari-bot-cli/tests/test_logs_cli.py:207-207 >>>
# 临时目录路径很长，rich 会在终端宽度处折行。比对时去掉全部空白，避免检查依赖路径长度。
<<< END U005735 >>>
<<< UNIT U005736 | py-comment | packages/akari-bot-cli/tests/test_logs_cli.py:246-246 >>>
# 实例空闲时当天的日志是空的，要说明一句，否则用户会以为命令没生效。
<<< END U005736 >>>
<<< UNIT U005737 | py-comment | packages/akari-bot-cli/tests/test_logs_cli.py:269-269 >>>
# 上限同时覆盖“跟随不再前进”的回归，那种情况下循环不会自己退出。
<<< END U005737 >>>
<<< UNIT U005738 | py-docstring | packages/akari-bot-cli/tests/test_logs_cli.py:299-299 | ctx=test_logs_cli >>>
cli.logs: 日志解析、增量读取与命令输出测试
<<< END U005738 >>>
<<< UNIT U005739 | py-comment | packages/akari-bot-cli/tests/test_main.py:51-51 >>>
# 框架连的是 core 的 akari-bot 命名空间，取 CLI 文案前要接上本包的快照。
<<< END U005739 >>>
<<< UNIT U005740 | py-comment | packages/akari-bot-cli/tests/test_main.py:139-139 >>>
# 可交互终端下无参数调用直接进入界面，不打印帮助。
<<< END U005740 >>>
<<< UNIT U005741 | py-comment | packages/akari-bot-cli/tests/test_main.py:154-154 >>>
# 没有实例时先询问，复用 init 本体初始化，再进入界面。
<<< END U005741 >>>
<<< UNIT U005742 | py-comment | packages/akari-bot-cli/tests/test_main.py:160-160 >>>
# 第一次找不到实例（触发引导），初始化后能找到。
<<< END U005742 >>>
<<< UNIT U005743 | py-comment | packages/akari-bot-cli/tests/test_main.py:180-180 >>>
# 拒绝初始化时不进入界面，也不调用 init。
<<< END U005743 >>>
<<< UNIT U005744 | py-comment | packages/akari-bot-cli/tests/test_main.py:196-198 >>>
# ``_ensure_instance`` 只传入路径与语言，故 init 的其余参数必须都有真实默认值。参数一旦改成必填
# （或默认值变成 typer 的 OptionInfo），无参数调用入口会在运行时失败，而 ``akaribot init`` 子命令
# 仍然正常，这项检查专门针对这一差异。
<<< END U005744 >>>
<<< UNIT U005745 | py-comment | packages/akari-bot-cli/tests/test_main.py:217-217 >>>
# 在实例目录里进入界面时自动补充记录，本机清单与自启策略随后才有对象可管理。
<<< END U005745 >>>
<<< UNIT U005746 | py-comment | packages/akari-bot-cli/tests/test_main.py:246-246 >>>
# 自动记录的结论由界面提示，否则用户看不到注册表已被改动。
<<< END U005746 >>>
<<< UNIT U005747 | py-inline-comment | packages/akari-bot-cli/tests/test_main.py:268-268 >>>
# typer.Exit 是正常收尾
<<< END U005747 >>>
<<< UNIT U005748 | py-comment | packages/akari-bot-cli/tests/test_main.py:276-276 >>>
# 在仓库根目录这类存放实例的目录下，唯一的下级实例就是当前要管理的实例，直接记录并切换过去。
<<< END U005748 >>>
<<< UNIT U005749 | py-comment | packages/akari-bot-cli/tests/test_main.py:295-295 >>>
# 再放入一个实例并更换为空注册表，下级有两个实例时不作选择，只报告候选。
<<< END U005749 >>>
<<< UNIT U005750 | py-comment | packages/akari-bot-cli/tests/test_main.py:320-321 >>>
# 实例解析会改用注册表里的默认实例，故整轮都指向一份空注册表，否则这几条用例的结果会取决于
# 运行测试的机器上记录过什么。
<<< END U005750 >>>
<<< UNIT U005751 | py-docstring | packages/akari-bot-cli/tests/test_main.py:318-318 | ctx=test_cli_main >>>
CLI 根命令的版本查询、无参数调用帮助、参数顺序与打包回退测试
<<< END U005751 >>>
<<< UNIT U005752 | py-comment | packages/akari-bot-cli/tests/test_migrate_plan.py:16-16 >>>
# 旧版 modules/ 里有 42 个官方模块目录，用户只加载过 dice 与 wiki 家族。
<<< END U005752 >>>
<<< UNIT U005753 | py-comment | packages/akari-bot-cli/tests/test_migrate_plan.py:64-65 >>>
# 未加载的模块也要在 registry 里有映射，否则“不安装”可能只是因为查不到包，用例就分不清
# “按启用状态筛选”与“碰巧映射不到”。
<<< END U005753 >>>
<<< UNIT U005754 | py-docstring | packages/akari-bot-cli/tests/test_migrate_plan.py:154-154 | ctx=test_migrate_plan >>>
cli.commands.migrate: 迁移候选与跳过诊断测试
<<< END U005754 >>>
<<< UNIT U005755 | py-comment | packages/akari-bot-cli/tests/test_module_authors.py:120-121 >>>
# ``module()`` 从调用帧取模块名再交给发现层。多退一层会取到 ``importlib._bootstrap``，
# ``_py_module_name`` 与作者一起变成空字符串，热重载、locale 指纹与依赖图同样失去依据。
<<< END U005755 >>>
<<< UNIT U005756 | py-inline-comment | packages/akari-bot-cli/tests/test_module_authors.py:122-122 >>>
# noqa: F401 - 导入即执行 module() 注册
<<< END U005756 >>>
<<< UNIT U005757 | py-docstring | packages/akari-bot-cli/tests/test_module_authors.py:133-133 | ctx=test_module_authors >>>
模块作者的 pyproject 声明与读取链路测试
<<< END U005757 >>>
<<< UNIT U005758 | py-comment | packages/akari-bot-cli/tests/test_module_available.py:59-60 >>>
# 命令经 ``rich.console.Console`` 输出，不是 stdout，故必须替换 console 本身。宽度放宽，
# 免得表格截断长包名而让检查失真。
<<< END U005758 >>>
<<< UNIT U005759 | py-comment | packages/akari-bot-cli/tests/test_module_available.py:72-72 >>>
# 表格会按终端宽度截断长名字，检查包名只能通过 JSON。
<<< END U005759 >>>
<<< UNIT U005760 | py-docstring | packages/akari-bot-cli/tests/test_module_available.py:168-168 | ctx=test_module_available >>>
cli.commands.module: 可安装包列举测试
<<< END U005760 >>>
<<< UNIT U005761 | py-inline-comment | packages/akari-bot-cli/tests/test_module_git.py:153-153 >>>
# noqa: BLE001 - fail() 抛出 typer.Exit
<<< END U005761 >>>
<<< UNIT U005762 | py-docstring | packages/akari-bot-cli/tests/test_module_git.py:211-211 | ctx=test_module_git >>>
cli.commands.module: git 直接引用安装测试
<<< END U005762 >>>
<<< UNIT U005763 | py-comment | packages/akari-bot-cli/tests/test_module_precheck.py:61-61 >>>
# 已安装包对 numpy 的要求在新版本下仍满足。只在请求 extra 时生效的依赖不参与判断。
<<< END U005763 >>>
<<< UNIT U005764 | py-comment | packages/akari-bot-cli/tests/test_module_precheck.py:80-80 >>>
# 可编辑安装的元数据停在安装那一刻。源码已放宽的约束不应再拦截依赖升级。
<<< END U005764 >>>
<<< UNIT U005765 | py-comment | packages/akari-bot-cli/tests/test_module_precheck.py:99-99 >>>
# 直接依赖与间接依赖的调整都要核对。uv 无解时同样拦截并给出原因。
<<< END U005765 >>>
<<< UNIT U005766 | py-comment | packages/akari-bot-cli/tests/test_module_precheck.py:143-143 >>>
# 兼容性检查据此判断 requires_core_api。读错位置时恒为 None，检查会被静默跳过。
<<< END U005766 >>>
<<< UNIT U005767 | py-docstring | packages/akari-bot-cli/tests/test_module_precheck.py:149-149 | ctx=test_module_precheck >>>
cli.commands.module: 安装前兼容性检查测试
<<< END U005767 >>>
<<< UNIT U005768 | py-comment | packages/akari-bot-cli/tests/test_module_purge.py:160-160 >>>
# 表这一步固定成功，本用例只针对“文件无法删除”，让结果不被真实子进程的成败左右。
<<< END U005768 >>>
<<< UNIT U005769 | py-docstring | packages/akari-bot-cli/tests/test_module_purge.py:195-195 | ctx=test_cli_module_purge >>>
cli.commands.module: 卸载清理的配置定位与顺序测试
<<< END U005769 >>>
