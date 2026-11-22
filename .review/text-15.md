# 全仓可读文本审核稿 · 第 15 册 / 共 20 册

覆盖 U010120–U010865，122 个文件、746 个单元、33,410 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-core/tests/test_http.py` | 2 | U010120–U010121 | 82 |
| `packages/akari-bot-core/tests/test_i18n.py` | 2 | U010122–U010123 | 56 |
| `packages/akari-bot-core/tests/test_jobqueue_backend.py` | 1 | U010124–U010124 | 25 |
| `packages/akari-bot-core/tests/test_jobqueue_daemon.py` | 2 | U010125–U010126 | 103 |
| `packages/akari-bot-core/tests/test_jobqueue_memory_backend.py` | 1 | U010127–U010127 | 35 |
| `packages/akari-bot-core/tests/test_jobqueue_websocket_backend.py` | 3 | U010128–U010130 | 234 |
| `packages/akari-bot-core/tests/test_loader.py` | 6 | U010131–U010136 | 379 |
| `packages/akari-bot-core/tests/test_locale_action_text.py` | 1 | U010137–U010137 | 24 |
| `packages/akari-bot-core/tests/test_locale_reload.py` | 6 | U010138–U010143 | 188 |
| `packages/akari-bot-core/tests/test_localized_time_format.py` | 2 | U010144–U010145 | 43 |
| `packages/akari-bot-core/tests/test_media_elements.py` | 3 | U010146–U010148 | 76 |
| `packages/akari-bot-core/tests/test_merge_code.py` | 4 | U010149–U010152 | 143 |
| `packages/akari-bot-core/tests/test_message.py` | 7 | U010153–U010159 | 253 |
| `packages/akari-bot-core/tests/test_module_reload.py` | 2 | U010160–U010161 | 90 |
| `packages/akari-bot-core/tests/test_module_runtime.py` | 1 | U010162–U010162 | 35 |
| `packages/akari-bot-core/tests/test_muted_policy.py` | 2 | U010163–U010164 | 40 |
| `packages/akari-bot-core/tests/test_network_proxy.py` | 3 | U010165–U010167 | 87 |
| `packages/akari-bot-core/tests/test_outgoing_hooks.py` | 1 | U010168–U010168 | 23 |
| `packages/akari-bot-core/tests/test_parser.py` | 2 | U010169–U010170 | 81 |
| `packages/akari-bot-core/tests/test_parser_hooks.py` | 19 | U010171–U010189 | 553 |
| `packages/akari-bot-core/tests/test_parser_recovery.py` | 1 | U010190–U010190 | 20 |
| `packages/akari-bot-core/tests/test_parser_routing.py` | 1 | U010191–U010191 | 55 |
| `packages/akari-bot-core/tests/test_paths.py` | 8 | U010192–U010199 | 443 |
| `packages/akari-bot-core/tests/test_petal.py` | 6 | U010200–U010205 | 187 |
| `packages/akari-bot-core/tests/test_post_message.py` | 7 | U010206–U010212 | 230 |
| `packages/akari-bot-core/tests/test_process_usage.py` | 6 | U010213–U010218 | 198 |
| `packages/akari-bot-core/tests/test_queue_lifecycle.py` | 5 | U010219–U010223 | 244 |
| `packages/akari-bot-core/tests/test_random.py` | 2 | U010224–U010225 | 70 |
| `packages/akari-bot-core/tests/test_read_all_messages.py` | 3 | U010226–U010228 | 96 |
| `packages/akari-bot-core/tests/test_regex_base_module.py` | 2 | U010229–U010230 | 106 |
| `packages/akari-bot-core/tests/test_regex_escape.py` | 1 | U010231–U010231 | 15 |
| `packages/akari-bot-core/tests/test_regex_filter_order.py` | 2 | U010232–U010233 | 89 |
| `packages/akari-bot-core/tests/test_regex_trigger_once.py` | 2 | U010234–U010235 | 85 |
| `packages/akari-bot-core/tests/test_registry.py` | 4 | U010236–U010239 | 213 |
| `packages/akari-bot-core/tests/test_report.py` | 2 | U010240–U010241 | 43 |
| `packages/akari-bot-core/tests/test_report_targets.py` | 2 | U010242–U010243 | 140 |
| `packages/akari-bot-core/tests/test_restart_prompt.py` | 6 | U010244–U010249 | 313 |
| `packages/akari-bot-core/tests/test_retired_gate.py` | 6 | U010250–U010255 | 249 |
| `packages/akari-bot-core/tests/test_retired_notice.py` | 5 | U010256–U010260 | 213 |
| `packages/akari-bot-core/tests/test_rpc_contracts.py` | 1 | U010261–U010261 | 35 |
| `packages/akari-bot-core/tests/test_runtime_lifecycle.py` | 3 | U010262–U010264 | 99 |
| `packages/akari-bot-core/tests/test_s3_async.py` | 1 | U010265–U010265 | 23 |
| `packages/akari-bot-core/tests/test_scheduler.py` | 4 | U010266–U010269 | 82 |
| `packages/akari-bot-core/tests/test_secret_filter.py` | 3 | U010270–U010272 | 53 |
| `packages/akari-bot-core/tests/test_send_direct_message.py` | 5 | U010273–U010277 | 419 |
| `packages/akari-bot-core/tests/test_session.py` | 6 | U010278–U010283 | 310 |
| `packages/akari-bot-core/tests/test_session_draft.py` | 7 | U010284–U010290 | 205 |
| `packages/akari-bot-core/tests/test_session_private.py` | 3 | U010291–U010293 | 121 |
| `packages/akari-bot-core/tests/test_setup_panel.py` | 11 | U010294–U010304 | 651 |
| `packages/akari-bot-core/tests/test_status.py` | 3 | U010305–U010307 | 98 |
| `packages/akari-bot-core/tests/test_storedata.py` | 2 | U010308–U010309 | 68 |
| `packages/akari-bot-core/tests/test_suppress_invalid_prompt.py` | 2 | U010310–U010311 | 70 |
| `packages/akari-bot-core/tests/test_term_locale.py` | 9 | U010312–U010320 | 306 |
| `packages/akari-bot-core/tests/test_timezone_offset.py` | 3 | U010321–U010323 | 116 |
| `packages/akari-bot-core/tests/test_tos.py` | 2 | U010324–U010325 | 88 |
| `packages/akari-bot-core/tests/test_typing_prompt.py` | 2 | U010326–U010327 | 55 |
| `packages/akari-bot-core/tests/test_union.py` | 13 | U010328–U010340 | 453 |
| `packages/akari-bot-core/tests/test_union_push.py` | 11 | U010341–U010351 | 387 |
| `packages/akari-bot-core/tests/test_url_guard.py` | 8 | U010352–U010359 | 504 |
| `packages/akari-bot-core/tests/test_webrender_rpc.py` | 4 | U010360–U010363 | 129 |
| `packages/akari-bot-testing/README.md` | 4 | U010364–U010367 | 168 |
| `packages/akari-bot-testing/akaribot/testing/__init__.py` | 3 | U010368–U010370 | 286 |
| `packages/akari-bot-testing/akaribot/testing/decorator.py` | 3 | U010371–U010373 | 54 |
| `packages/akari-bot-testing/akaribot/testing/docs/index.md` | 24 | U010374–U010397 | 1,470 |
| `packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md` | 28 | U010398–U010425 | 2,373 |
| `packages/akari-bot-testing/akaribot/testing/expectations.py` | 24 | U010426–U010449 | 1,122 |
| `packages/akari-bot-testing/akaribot/testing/manifest.toml` | 1 | U010450–U010450 | 61 |
| `packages/akari-bot-testing/akaribot/testing/mock/config.py` | 5 | U010451–U010455 | 204 |
| `packages/akari-bot-testing/akaribot/testing/mock/database.py` | 1 | U010456–U010456 | 22 |
| `packages/akari-bot-testing/akaribot/testing/mock/factory.py` | 2 | U010457–U010458 | 39 |
| `packages/akari-bot-testing/akaribot/testing/mock/fixtures.py` | 9 | U010459–U010467 | 506 |
| `packages/akari-bot-testing/akaribot/testing/mock/http.py` | 6 | U010468–U010473 | 100 |
| `packages/akari-bot-testing/akaribot/testing/mock/loader.py` | 3 | U010474–U010476 | 210 |
| `packages/akari-bot-testing/akaribot/testing/mock/parser.py` | 23 | U010477–U010499 | 399 |
| `packages/akari-bot-testing/akaribot/testing/mock/scheduler.py` | 2 | U010500–U010501 | 55 |
| `packages/akari-bot-testing/akaribot/testing/mock/session.py` | 5 | U010502–U010506 | 152 |
| `packages/akari-bot-testing/akaribot/testing/mock/webrender.py` | 7 | U010507–U010513 | 245 |
| `packages/akari-bot-testing/akaribot/testing/process.py` | 2 | U010514–U010515 | 148 |
| `packages/akari-bot-testing/akaribot/testing/pytest_plugin.py` | 16 | U010516–U010531 | 492 |
| `packages/akari-bot-testing/akaribot/testing/runner.py` | 39 | U010532–U010570 | 2,776 |
| `packages/akari-bot-testing/akaribot/testing/tasks.py` | 6 | U010571–U010576 | 200 |
| `packages/akari-bot-testing/akaribot/testing/tester.py` | 4 | U010577–U010580 | 339 |
| `packages/akari-bot-testing/akaribot/testing/timing.py` | 1 | U010581–U010581 | 10 |
| `packages/akari-bot-testing/tests/test_expectations.py` | 3 | U010582–U010584 | 101 |
| `packages/akari-bot-testing/tests/test_runner_options.py` | 1 | U010585–U010585 | 35 |
| `packages/akari-bot-testing/tests/test_tester_framework.py` | 5 | U010586–U010590 | 165 |
| `packages/modules/akari-bot-module-ai/README.md` | 4 | U010591–U010594 | 168 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md` | 74 | U010595–U010668 | 3,153 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/__init__.py` | 4 | U010669–U010672 | 145 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/context.py` | 4 | U010673–U010676 | 99 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md` | 17 | U010677–U010693 | 1,942 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md` | 12 | U010694–U010705 | 496 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/anthropic.py` | 5 | U010706–U010710 | 312 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/base.py` | 7 | U010711–U010717 | 292 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/completions.py` | 3 | U010718–U010720 | 123 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_generate_content.py` | 7 | U010721–U010727 | 248 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_interactions.py` | 7 | U010728–U010734 | 255 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/responses.py` | 3 | U010735–U010737 | 154 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/formatting.py` | 4 | U010738–U010741 | 33 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/hook.py` | 3 | U010742–U010744 | 125 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/llm.py` | 3 | U010745–U010747 | 151 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json` | 42 | U010748–U010789 | 890 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/manifest.toml` | 3 | U010790–U010792 | 96 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/setting.py` | 2 | U010793–U010794 | 109 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/tools/__init__.py` | 2 | U010795–U010796 | 79 |
| `packages/modules/akari-bot-module-ai/akaribot/modules/ai/tools/fetch_webpage.py` | 2 | U010797–U010798 | 93 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_anthropic_tool_choice.py` | 3 | U010799–U010801 | 127 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_billing_time_rules.py` | 3 | U010802–U010804 | 135 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_context.py` | 2 | U010805–U010806 | 81 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_fetch_webpage.py` | 2 | U010807–U010808 | 114 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_gemini_generate_content.py` | 2 | U010809–U010810 | 111 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_gemini_interactions.py` | 2 | U010811–U010812 | 105 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_hook.py` | 4 | U010813–U010816 | 139 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_image_generation.py` | 2 | U010817–U010818 | 76 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_python_images.py` | 2 | U010819–U010820 | 73 |
| `packages/modules/akari-bot-module-ai/tests/test_ai_reasoning_effort.py` | 7 | U010821–U010827 | 245 |
| `packages/modules/akari-bot-module-ai/tests/test_search_images.py` | 2 | U010828–U010829 | 59 |
| `packages/modules/akari-bot-module-arcaea/README.md` | 4 | U010830–U010833 | 159 |
| `packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md` | 9 | U010834–U010842 | 353 |
| `packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md` | 14 | U010843–U010856 | 960 |
| `packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json` | 8 | U010857–U010864 | 116 |
| `packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/manifest.toml` | 1 | U010865–U010865 | 31 |

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
<<< UNIT U010120 | py-docstring | packages/akari-bot-core/tests/test_http.py:1-1 | ctx=<module> >>>
akaribot.core.utils.http HTTP 工具单元测试（纯函数部分）。
<<< END U010120 >>>
<<< UNIT U010121 | py-docstring | packages/akari-bot-core/tests/test_http.py:191-191 | ctx=test_http >>>
akaribot.core.utils.http: HTTP 工具纯函数测试
<<< END U010121 >>>
<<< UNIT U010122 | py-docstring | packages/akari-bot-core/tests/test_i18n.py:1-1 | ctx=<module> >>>
akaribot.core.i18n 国际化系统单元测试。
<<< END U010122 >>>
<<< UNIT U010123 | py-docstring | packages/akari-bot-core/tests/test_i18n.py:47-47 | ctx=test_i18n >>>
akaribot.core.i18n: 国际化系统测试
<<< END U010123 >>>
<<< UNIT U010124 | py-docstring | packages/akari-bot-core/tests/test_jobqueue_backend.py:1-1 | ctx=<module> >>>
JobQueue 后端装配和介质无关接口约定测试。
<<< END U010124 >>>
<<< UNIT U010125 | py-comment | packages/akari-bot-core/tests/test_jobqueue_daemon.py:124-125 >>>
# 实例发现由 bot_* 配置表驱动，合成适配器没有配置表。本用例只验证守护进程的
# 编排顺序，直接给出一个已启用实例，不为它铺一份配置。
<<< END U010125 >>>
<<< UNIT U010126 | py-docstring | packages/akari-bot-core/tests/test_jobqueue_daemon.py:1-1 | ctx=<module> >>>
JobQueue WebSocket Hub 守护进程编排测试。
<<< END U010126 >>>
<<< UNIT U010127 | py-docstring | packages/akari-bot-core/tests/test_jobqueue_memory_backend.py:1-1 | ctx=<module> >>>
在不访问 JobQueue ORM 表的情况下验证共享运行时接口约定。
<<< END U010127 >>>
<<< UNIT U010128 | py-comment | packages/akari-bot-core/tests/test_jobqueue_websocket_backend.py:71-73 >>>
# wait_ready 只保证各 Peer 已注册。ready/welcome 握手仍可能在其他 Peer 的
# 处理任务或 Hub 出站队列中。测试开始前等待控制面静默，避免 queue_size=1
# 的背压用例与启动握手竞争同一个命令槽位。
<<< END U010128 >>>
<<< UNIT U010129 | py-comment | packages/akari-bot-core/tests/test_jobqueue_websocket_backend.py:292-293 >>>
# Peer ready/welcome 信号可能仍在同一 Hub 中异步收尾。这里只验证超限调用
# 自身没有遗留等待方或投递，避免把无关生命周期投递误判为泄漏。
<<< END U010129 >>>
<<< UNIT U010130 | py-docstring | packages/akari-bot-core/tests/test_jobqueue_websocket_backend.py:1-1 | ctx=<module> >>>
WebSocket JobQueue 完整后端测试。
<<< END U010130 >>>
<<< UNIT U010131 | py-comment | packages/akari-bot-core/tests/test_loader.py:51-53 >>>
# 每次热重载都会重建依赖图（遍历并解析全部模块源码，实测 0.6~0.9 秒），
# 冷文件缓存或高负载环境下会明显超过 1 秒，故等待步骤统一留出余量，
# 避免把“慢”误判为“无响应”。
<<< END U010131 >>>
<<< UNIT U010132 | py-comment | packages/akari-bot-core/tests/test_loader.py:257-258 >>>
# 用例以 `akaribot.modules.__test_loader_*` 构造独立重载场景。包身份解析改为查注册表后，
# 这些名字解析不到包，故在用例入口统一给出合成条目。真实包名仍交回注册表本身解析。
<<< END U010132 >>>
<<< UNIT U010133 | py-comment | packages/akari-bot-core/tests/test_loader.py:277-277 >>>
# 合成包不会出现在注册表中，故直接匹配前缀即可。
<<< END U010133 >>>
<<< UNIT U010134 | py-comment | packages/akari-bot-core/tests/test_loader.py:708-710 >>>
# ``return_py_module()`` 返回 ``None`` 会让热重载、locale 指纹、依赖图与模块卸载
# 四处静默失效且不报错。这条检查是“包装成 wheel 后功能未损坏”的哨兵，
# 必须常驻。
<<< END U010134 >>>
<<< UNIT U010135 | py-docstring | packages/akari-bot-core/tests/test_loader.py:1-1 | ctx=<module> >>>
core.loader 模块加载器单元测试。
<<< END U010135 >>>
<<< UNIT U010136 | py-docstring | packages/akari-bot-core/tests/test_loader.py:1276-1276 | ctx=test_loader >>>
core.loader: 模块加载器测试
<<< END U010136 >>>
<<< UNIT U010137 | py-docstring | packages/akari-bot-core/tests/test_locale_action_text.py:1-1 | ctx=<module> >>>
locale 命令的语言入口与协助翻译链接测试。
<<< END U010137 >>>
<<< UNIT U010138 | py-comment | packages/akari-bot-core/tests/test_locale_reload.py:38-38 >>>
# 内容长度和 mtime 都保持不变，确保重载依赖内容签名而非文件元数据。
<<< END U010138 >>>
<<< UNIT U010139 | py-comment | packages/akari-bot-core/tests/test_locale_reload.py:45-45 >>>
# Reader 会定期检查共享 manifest，无需恢复旧的队列广播或显式重连。
<<< END U010139 >>>
<<< UNIT U010140 | py-comment | packages/akari-bot-core/tests/test_locale_reload.py:53-53 >>>
# 临时写坏语言文件时应报告错误，但不能替换已经发布的健康快照。
<<< END U010140 >>>
<<< UNIT U010141 | py-comment | packages/akari-bot-core/tests/test_locale_reload.py:66-66 >>>
# 后续测试仍应使用测试框架在启动时发布的项目语言快照。
<<< END U010141 >>>
<<< UNIT U010142 | py-docstring | packages/akari-bot-core/tests/test_locale_reload.py:1-1 | ctx=<module> >>>
core.i18n 单元测试 - 语言快照的发布与重载。
<<< END U010142 >>>
<<< UNIT U010143 | py-docstring | packages/akari-bot-core/tests/test_locale_reload.py:72-72 | ctx=test_locale_reload >>>
core.i18n: 语言快照重载测试。
<<< END U010143 >>>
<<< UNIT U010144 | py-docstring | packages/akari-bot-core/tests/test_localized_time_format.py:1-1 | ctx=<module> >>>
本地化时间格式化的非 ASCII 字面文本测试。
<<< END U010144 >>>
<<< UNIT U010145 | py-docstring | packages/akari-bot-core/tests/test_localized_time_format.py:75-75 | ctx=test_localized_time_format >>>
本地化时间的非 ASCII 格式串测试
<<< END U010145 >>>
<<< UNIT U010146 | py-comment | packages/akari-bot-core/tests/test_media_elements.py:79-79 >>>
# get_image 带重试装饰器，最内层异常为格式校验失败
<<< END U010146 >>>
<<< UNIT U010147 | py-docstring | packages/akari-bot-core/tests/test_media_elements.py:1-1 | ctx=<module> >>>
媒体元素读写与 media 工具错误语义单元测试。
<<< END U010147 >>>
<<< UNIT U010148 | py-docstring | packages/akari-bot-core/tests/test_media_elements.py:142-142 | ctx=test_media_elements >>>
媒体元素与 media 工具的错误语义。
<<< END U010148 >>>
<<< UNIT U010149 | py-inline-comment | packages/akari-bot-core/tests/test_merge_code.py:72-72 >>>
# 归还，避免影响其他用例
<<< END U010149 >>>
<<< UNIT U010150 | py-comment | packages/akari-bot-core/tests/test_merge_code.py:83-83 >>>
# 绑定时逐个递增编号，两者此刻不同号。
<<< END U010150 >>>
<<< UNIT U010151 | py-docstring | packages/akari-bot-core/tests/test_merge_code.py:1-1 | ctx=<module> >>>
akaribot.modules.core.common_tools.merge 单元测试 - 迁移码的签发与消费。
<<< END U010151 >>>
<<< UNIT U010152 | py-docstring | packages/akari-bot-core/tests/test_merge_code.py:110-110 | ctx=test_merge_code >>>
akaribot.modules.core.common_tools.merge: 迁移码签发与消费测试
<<< END U010152 >>>
<<< UNIT U010153 | py-comment | packages/akari-bot-core/tests/test_message.py:254-254 >>>
# 逗号后的部分不应丢失
<<< END U010153 >>>
<<< UNIT U010154 | py-docstring | packages/akari-bot-core/tests/test_message.py:1-1 | ctx=<module> >>>
akaribot.core.builtins.message 消息系统单元测试。
<<< END U010154 >>>
<<< UNIT U010155 | py-docstring | packages/akari-bot-core/tests/test_message.py:287-287 | ctx=test_message_chain >>>
akaribot.core.builtins.message.chain: MessageChain 测试
<<< END U010155 >>>
<<< UNIT U010156 | py-docstring | packages/akari-bot-core/tests/test_message.py:301-301 | ctx=test_message_elements >>>
akaribot.core.builtins.message.elements: 消息元素测试
<<< END U010156 >>>
<<< UNIT U010157 | py-docstring | packages/akari-bot-core/tests/test_message.py:311-311 | ctx=test_kecode_roundtrip >>>
akaribot.core.builtins.message: KE 码转义往返测试
<<< END U010157 >>>
<<< UNIT U010158 | py-docstring | packages/akari-bot-core/tests/test_message.py:585-585 | ctx=test_message_chain_operations >>>
MessageChain: 运算符和高级操作测试
<<< END U010158 >>>
<<< UNIT U010159 | py-docstring | packages/akari-bot-core/tests/test_message.py:594-594 | ctx=test_message_elements_extended >>>
消息元素扩展测试: Image/Audio/Mention/Embed
<<< END U010159 >>>
<<< UNIT U010160 | py-docstring | packages/akari-bot-core/tests/test_module_reload.py:1-1 | ctx=<module> >>>
module reload 对基础模块的处理测试。
<<< END U010160 >>>
<<< UNIT U010161 | py-docstring | packages/akari-bot-core/tests/test_module_reload.py:102-102 | ctx=test_module_reload >>>
akaribot.modules.core.admin_tools.modules: module reload 基础模块处理测试
<<< END U010161 >>>
<<< UNIT U010162 | py-docstring | packages/akari-bot-core/tests/test_module_runtime.py:284-284 | ctx=test_module_runtime >>>
模块 runtime 状态、资源、任务与 generation 切换。
<<< END U010162 >>>
<<< UNIT U010163 | py-docstring | packages/akari-bot-core/tests/test_muted_policy.py:1-1 | ctx=<module> >>>
禁止发言策略的命令入口拦截与解除禁止发言确认测试。
<<< END U010163 >>>
<<< UNIT U010164 | py-docstring | packages/akari-bot-core/tests/test_muted_policy.py:61-61 | ctx=test_muted_policy >>>
parser 禁止发言策略测试
<<< END U010164 >>>
<<< UNIT U010165 | py-comment | packages/akari-bot-core/tests/test_network_proxy.py:35-35 >>>
# 未填写代理时取到空字符串，各 SDK 需要 None 才表示直连
<<< END U010165 >>>
<<< UNIT U010166 | py-docstring | packages/akari-bot-core/tests/test_network_proxy.py:1-1 | ctx=<module> >>>
代理与 TLS 校验设置的单元测试。
<<< END U010166 >>>
<<< UNIT U010167 | py-docstring | packages/akari-bot-core/tests/test_network_proxy.py:112-112 | ctx=test_network_proxy >>>
core.config.network: 代理与 TLS 校验设置测试
<<< END U010167 >>>
<<< UNIT U010168 | py-docstring | packages/akari-bot-core/tests/test_outgoing_hooks.py:1-1 | ctx=<module> >>>
真实发送路径的出站规范化、观察隔离与取消边界。
<<< END U010168 >>>
<<< UNIT U010169 | py-docstring | packages/akari-bot-core/tests/test_parser.py:1-1 | ctx=<module> >>>
akaribot.core.builtins.parser 命令解析单元测试。
<<< END U010169 >>>
<<< UNIT U010170 | py-docstring | packages/akari-bot-core/tests/test_parser.py:349-349 | ctx=test_parser_args >>>
akaribot.core.builtins.parser.args: 参数解析测试
<<< END U010170 >>>
<<< UNIT U010171 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:176-176 >>>
# 确保 named hook 未进入 point 索引
<<< END U010171 >>>
<<< UNIT U010172 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:275-275 >>>
# after 仍应执行，slow 的 Stop 不被采纳
<<< END U010172 >>>
<<< UNIT U010173 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:385-385 >>>
# 构造版本不一致的订阅
<<< END U010173 >>>
<<< UNIT U010174 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:439-439 >>>
# 不传入 dispatch 级 timeout，依赖订阅字段
<<< END U010174 >>>
<<< UNIT U010175 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:473-473 >>>
# 模块触发只执行带名称的 hook
<<< END U010175 >>>
<<< UNIT U010176 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:481-481 >>>
# 停用后带名称的 hook 也不执行
<<< END U010176 >>>
<<< UNIT U010177 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:594-594 >>>
# available_modules 过滤时，无 target_from 则用全部 modules
<<< END U010177 >>>
<<< UNIT U010178 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:622-622 >>>
# 非 base 且场景未启用 → 拒绝
<<< END U010178 >>>
<<< UNIT U010179 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:685-685 >>>
# 初始索引中订阅绑定旧版本
<<< END U010179 >>>
<<< UNIT U010180 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:691-692 >>>
# 模拟 reload 失败流程，先 prepare 出新 staging（新版本）→ restore 旧注册并重建索引
# （此时旧函数被标成新版本）→ abort 撤销 staging → 再次重建索引
<<< END U010180 >>>
<<< UNIT U010181 | py-inline-comment | packages/akari-bot-core/tests/test_parser_hooks.py:696-696 >>>
# restore_registrations 内的一次重建
<<< END U010181 >>>
<<< UNIT U010182 | py-inline-comment | packages/akari-bot-core/tests/test_parser_hooks.py:702-702 >>>
# 仍绑定 staging（abort 前）
<<< END U010182 >>>
<<< UNIT U010183 | py-inline-comment | packages/akari-bot-core/tests/test_parser_hooks.py:704-704 >>>
# abort 后的再次重建
<<< END U010183 >>>
<<< UNIT U010184 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:767-767 >>>
# 收尾时间超过 50ms 收尾窗口，制造“清理中父任务被取消”的窗口
<<< END U010184 >>>
<<< UNIT U010185 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:782-782 >>>
# 等 hook 超时并进入异步收尾
<<< END U010185 >>>
<<< UNIT U010186 | py-inline-comment | packages/akari-bot-core/tests/test_parser_hooks.py:788-788 >>>
# 取消被忽略，dispatch 正常返回
<<< END U010186 >>>
<<< UNIT U010187 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:804-804 >>>
# 父 hook 内嵌套同会话的 COMMAND_PREPARE 分发
<<< END U010187 >>>
<<< UNIT U010188 | py-comment | packages/akari-bot-core/tests/test_parser_hooks.py:827-827 >>>
# 嵌套分发被跳过，child 未执行，tmp 未被提交
<<< END U010188 >>>
<<< UNIT U010189 | py-docstring | packages/akari-bot-core/tests/test_parser_hooks.py:1-1 | ctx=<module> >>>
parser 入口 hook 执行器与注册索引单元测试。
<<< END U010189 >>>
<<< UNIT U010190 | py-docstring | packages/akari-bot-core/tests/test_parser_recovery.py:1-1 | ctx=<module> >>>
生产命令模板解析失败后的恢复与提示边界。
<<< END U010190 >>>
<<< UNIT U010191 | py-docstring | packages/akari-bot-core/tests/test_parser_routing.py:1-1 | ctx=<module> >>>
akaribot.modules.core.admin_tools.alias 单元测试 - 自定义别名改写。
<<< END U010191 >>>
<<< UNIT U010192 | py-comment | packages/akari-bot-core/tests/test_paths.py:14-15 >>>
# 仓库根目录从 core 包的位置向上推算（判断依据见 _repository_root），
# 既不依赖测试文件所处位置，也不取自 Paths.tests。后者正是本用例要检查的取值。
<<< END U010192 >>>
<<< UNIT U010193 | py-comment | packages/akari-bot-core/tests/test_paths.py:17-18 >>>
# 不按层数推算（源码根目录从 <dist>/src/akaribot 扁平化为 <dist>/akaribot 后层数会变），也不取
# Paths.tests。后者正是本用例要检查的取值。
<<< END U010193 >>>
<<< UNIT U010194 | py-comment | packages/akari-bot-core/tests/test_paths.py:27-27 >>>
# 子进程脚本，取出实例目录相关取值并打印，用于验证环境变量在导入期生效。
<<< END U010194 >>>
<<< UNIT U010195 | py-comment | packages/akari-bot-core/tests/test_paths.py:68-69 >>>
# config 的检查只在未设置 AKARI_CONFIG_PATH 时成立。测试框架会为该变量指向一份临时
# 配置，此处显式清空它，避免用例结论取决于外层环境。
<<< END U010195 >>>
<<< UNIT U010196 | py-comment | packages/akari-bot-core/tests/test_paths.py:151-151 >>>
# 判定须在临时目录销毁之前完成，否则退出 with 后 is_dir() 必然为假。
<<< END U010196 >>>
<<< UNIT U010197 | py-comment | packages/akari-bot-core/tests/test_paths.py:163-163 >>>
# 末级目录名取决于当前客户端（default 或 client_name 的小写）。其取值不在此检查。
<<< END U010197 >>>
<<< UNIT U010198 | py-docstring | packages/akari-bot-core/tests/test_paths.py:1-1 | ctx=<module> >>>
core.paths 实例目录单元测试。
<<< END U010198 >>>
<<< UNIT U010199 | py-docstring | packages/akari-bot-core/tests/test_paths.py:172-172 | ctx=test_paths >>>
core.paths: 实例目录测试
<<< END U010199 >>>
<<< UNIT U010200 | py-comment | packages/akari-bot-core/tests/test_petal.py:94-94 >>>
# 今日已签到返回 0，余额不再增加
<<< END U010200 >>>
<<< UNIT U010201 | py-comment | packages/akari-bot-core/tests/test_petal.py:97-97 >>>
# 把签到记录的过期时间改为过去，模拟跨过每日边界
<<< END U010201 >>>
<<< UNIT U010202 | py-comment | packages/akari-bot-core/tests/test_petal.py:124-124 >>>
# 同一用户在不同场景共用签到记录，不能因场景时区不同重复签到。
<<< END U010202 >>>
<<< UNIT U010203 | py-comment | packages/akari-bot-core/tests/test_petal.py:241-241 >>>
# 模拟停机跨过周期边界，标记停留在过去的周期时补充结算一次。
<<< END U010203 >>>
<<< UNIT U010204 | py-docstring | packages/akari-bot-core/tests/test_petal.py:1-1 | ctx=<module> >>>
akaribot.core.utils.petal 单元测试 - 花瓣系统（需要数据库/配置）。
<<< END U010204 >>>
<<< UNIT U010205 | py-docstring | packages/akari-bot-core/tests/test_petal.py:255-255 | ctx=test_petal >>>
akaribot.core.utils.petal: 花瓣系统测试
<<< END U010205 >>>
<<< UNIT U010206 | py-comment | packages/akari-bot-core/tests/test_post_message.py:20-20 >>>
# 构造一组“同一条消息通道、分属两个平台”的会话。
<<< END U010206 >>>
<<< UNIT U010207 | py-comment | packages/akari-bot-core/tests/test_post_message.py:58-58 >>>
# 取出并清空已入队的主动推送任务，返回 ``(目标会话, 下一跳列表)``。
<<< END U010207 >>>
<<< UNIT U010208 | py-comment | packages/akari-bot-core/tests/test_post_message.py:77-77 >>>
# 同一条通道对应同一个现实场景，推送两次即发出两条重复消息。
<<< END U010208 >>>
<<< UNIT U010209 | py-comment | packages/akari-bot-core/tests/test_post_message.py:92-92 >>>
# 仅第二个平台在线时，队首应换为该平台，且不再保留下一跳。
<<< END U010209 >>>
<<< UNIT U010210 | py-comment | packages/akari-bot-core/tests/test_post_message.py:125-125 >>>
# 离线目的地须当场抛出错误，不创建无人消费的请求或结果等待者。
<<< END U010210 >>>
<<< UNIT U010211 | py-docstring | packages/akari-bot-core/tests/test_post_message.py:1-1 | ctx=<module> >>>
core.builtins.bot 单元测试 - 主动推送的通道合并与掉线避让（需要数据库）。
<<< END U010211 >>>
<<< UNIT U010212 | py-docstring | packages/akari-bot-core/tests/test_post_message.py:201-201 | ctx=test_post_message >>>
core.builtins.bot: 主动推送测试
<<< END U010212 >>>
<<< UNIT U010213 | py-comment | packages/akari-bot-core/tests/test_process_usage.py:95-95 >>>
# 该取值超出 PID 上限，不对应任何进程。
<<< END U010213 >>>
<<< UNIT U010214 | py-docstring | packages/akari-bot-core/tests/test_process_usage.py:1-1 | ctx=<module> >>>
各进程内存占用汇总的单元测试 - 指标统计方式、peer 名还原与失败可见性。
<<< END U010214 >>>
<<< UNIT U010215 | py-docstring | packages/akari-bot-core/tests/test_process_usage.py:108-108 | ctx=test_process_usage_metrics >>>
core.queue.diagnostics: 内存指标统计方式测试
<<< END U010215 >>>
<<< UNIT U010216 | py-docstring | packages/akari-bot-core/tests/test_process_usage.py:118-118 | ctx=test_process_usage_summary >>>
core.queue.diagnostics: 逐实例结果汇总测试
<<< END U010216 >>>
<<< UNIT U010217 | py-docstring | packages/akari-bot-core/tests/test_process_usage.py:140-140 | ctx=test_process_usage_payload >>>
core.queue.diagnostics: 进程占用的可序列化载荷测试
<<< END U010217 >>>
<<< UNIT U010218 | py-docstring | packages/akari-bot-core/tests/test_process_usage.py:148-148 | ctx=test_process_usage_collection >>>
core.queue.diagnostics: 进程指标采集测试
<<< END U010218 >>>
<<< UNIT U010219 | py-comment | packages/akari-bot-core/tests/test_queue_lifecycle.py:142-143 >>>
# 补丁作用于进程级的 JobQueuesTable，同一事件循环中其他 Peer 的轮询器也会命中。
# 非本测试目标的调用须原样放行，否则外部轮询器会占用会合名额，使本测试的协程永久等待。
<<< END U010219 >>>
<<< UNIT U010220 | py-comment | packages/akari-bot-core/tests/test_queue_lifecycle.py:150-150 >>>
# 读取失败亦须放行对端，否则异常将表现为无进展挂起，掩盖真实原因。
<<< END U010220 >>>
<<< UNIT U010221 | py-comment | packages/akari-bot-core/tests/test_queue_lifecycle.py:161-161 >>>
# 同上，只记录本任务派发的处理协程，避免等待其他轮询器的执行中任务。
<<< END U010221 >>>
<<< UNIT U010222 | py-docstring | packages/akari-bot-core/tests/test_queue_lifecycle.py:1-1 | ctx=<module> >>>
akaribot.core.queue.base 单元测试 - 队列任务清理与取消恢复。
<<< END U010222 >>>
<<< UNIT U010223 | py-docstring | packages/akari-bot-core/tests/test_queue_lifecycle.py:220-220 | ctx=test_queue_lifecycle >>>
akaribot.core.queue.base: 队列生命周期测试。
<<< END U010223 >>>
<<< UNIT U010224 | py-docstring | packages/akari-bot-core/tests/test_random.py:1-1 | ctx=<module> >>>
core.utils.random 纯函数单元测试 - Random 类。
<<< END U010224 >>>
<<< UNIT U010225 | py-docstring | packages/akari-bot-core/tests/test_random.py:72-72 | ctx=test_random >>>
core.utils.random: Random 类全部方法测试
<<< END U010225 >>>
<<< UNIT U010226 | py-comment | packages/akari-bot-core/tests/test_read_all_messages.py:150-150 >>>
# 该用例刻意使用 QQ 官方群会话，术语随之显示为“群聊”。
<<< END U010226 >>>
<<< UNIT U010227 | py-docstring | packages/akari-bot-core/tests/test_read_all_messages.py:1-1 | ctx=<module> >>>
read_all_messages 特性与正则模块管控单元测试。
<<< END U010227 >>>
<<< UNIT U010228 | py-docstring | packages/akari-bot-core/tests/test_read_all_messages.py:246-246 | ctx=test_read_all_messages >>>
core: read_all_messages 特性与正则模块管控
<<< END U010228 >>>
<<< UNIT U010229 | py-docstring | packages/akari-bot-core/tests/test_regex_base_module.py:1-1 | ctx=<module> >>>
core.builtins.parser.message 单元测试 - base 模块的 regex 启用判定。
<<< END U010229 >>>
<<< UNIT U010230 | py-docstring | packages/akari-bot-core/tests/test_regex_base_module.py:43-43 | ctx=test_regex_base_module >>>
core.builtins.parser.message: base 模块 regex 启用判定测试
<<< END U010230 >>>
<<< UNIT U010231 | py-docstring | packages/akari-bot-core/tests/test_regex_escape.py:1-1 | ctx=<module> >>>
消息正则解析临时关闭功能测试。
<<< END U010231 >>>
<<< UNIT U010232 | py-docstring | packages/akari-bot-core/tests/test_regex_filter_order.py:1-1 | ctx=<module> >>>
core.builtins.parser.message 单元测试 - 正则平台筛选与执行锁。
<<< END U010232 >>>
<<< UNIT U010233 | py-docstring | packages/akari-bot-core/tests/test_regex_filter_order.py:210-210 | ctx=test_regex_filter_order >>>
core.builtins.parser.message: 正则平台筛选与执行锁测试
<<< END U010233 >>>
<<< UNIT U010234 | py-docstring | packages/akari-bot-core/tests/test_regex_trigger_once.py:1-1 | ctx=<module> >>>
core.builtins.parser.message 单元测试 - 正则单次触发标记。
<<< END U010234 >>>
<<< UNIT U010235 | py-docstring | packages/akari-bot-core/tests/test_regex_trigger_once.py:39-39 | ctx=test_regex_trigger_once >>>
core.builtins.parser.message: 正则单次触发标记测试
<<< END U010235 >>>
<<< UNIT U010236 | py-comment | packages/akari-bot-core/tests/test_registry.py:94-95 >>>
# 已安装包的 entry point 会先于目录回退收录，故须显式屏蔽该路径。本用例检查的是
# 目录回退本身，结论不应取决于当前环境是否安装包。
<<< END U010236 >>>
<<< UNIT U010237 | py-comment | packages/akari-bot-core/tests/test_registry.py:331-332 >>>
# 重建写的是全局索引，不还原会让同进程后续用例（如 test_rpc_contracts 依赖的
# by_import_path("…wiki")）拿到残缺注册表，报出与本次改动无关的失败。
<<< END U010237 >>>
<<< UNIT U010238 | py-docstring | packages/akari-bot-core/tests/test_registry.py:1-1 | ctx=<module> >>>
core.registry 发现层单元测试。
<<< END U010238 >>>
<<< UNIT U010239 | py-docstring | packages/akari-bot-core/tests/test_registry.py:383-383 | ctx=test_registry >>>
core.registry: 发现层测试
<<< END U010239 >>>
<<< UNIT U010240 | py-docstring | packages/akari-bot-core/tests/test_report.py:1-1 | ctx=<module> >>>
上报服务单元测试。
<<< END U010240 >>>
<<< UNIT U010241 | py-docstring | packages/akari-bot-core/tests/test_report.py:112-112 | ctx=test_report >>>
akaribot.core.smtp: SMTP 与场景上报路由测试
<<< END U010241 >>>
<<< UNIT U010242 | py-comment | packages/akari-bot-core/tests/test_report_targets.py:23-25 >>>
# 获取会话时须由拓扑缓存反向查找场景所属的客户端，未注册者无法获取会话。缓存非空时
# ``Alive.determine_client(None)`` 还会直接抛出异常，而 ``fetch_target`` 会将其吞下，
# 表现为无声地少了几个会话。
<<< END U010242 >>>
<<< UNIT U010243 | py-docstring | packages/akari-bot-core/tests/test_report_targets.py:92-92 | ctx=test_report_targets >>>
core: 上报场景按场景组展开
<<< END U010243 >>>
<<< UNIT U010244 | py-comment | packages/akari-bot-core/tests/test_restart_prompt.py:31-31 >>>
# load_prompt 会一并读取模块加载结果，该文件由 load_modules 写出，此处补齐以隔离依赖
<<< END U010244 >>>
<<< UNIT U010245 | py-comment | packages/akari-bot-core/tests/test_restart_prompt.py:100-102 >>>
# server 与各 bot 子进程一同重启，`load_prompt` 执行时本地拓扑缓存必然为空。
# 客户端须先在 Peer Registry 注册带有效租约的 ready 实例。若不等待即发送，
# RPC 的掉线检查会拒绝提示请求。
<<< END U010245 >>>
<<< UNIT U010246 | py-comment | packages/akari-bot-core/tests/test_restart_prompt.py:124-124 >>>
# 重启提示并非关键路径，客户端确已掉线时无限等待只会让 server 阻塞在初始化阶段。
<<< END U010246 >>>
<<< UNIT U010247 | py-comment | packages/akari-bot-core/tests/test_restart_prompt.py:131-131 >>>
# 超时放弃后不应残留缓存，否则下次启动会重复投递
<<< END U010247 >>>
<<< UNIT U010248 | py-docstring | packages/akari-bot-core/tests/test_restart_prompt.py:1-1 | ctx=<module> >>>
core.server.init 单元测试 - 重启提示的送达（需要数据库）。
<<< END U010248 >>>
<<< UNIT U010249 | py-docstring | packages/akari-bot-core/tests/test_restart_prompt.py:155-155 | ctx=test_restart_prompt >>>
core.server.init: 重启提示送达测试
<<< END U010249 >>>
<<< UNIT U010250 | py-comment | packages/akari-bot-core/tests/test_retired_gate.py:236-236 >>>
# 并入同一通道编号，两个平台场景自此指向同一个现实场景，等待任务随之共享
<<< END U010250 >>>
<<< UNIT U010251 | py-comment | packages/akari-bot-core/tests/test_retired_gate.py:246-246 >>>
# all_ 任务按物理场景建立稳定 bucket，check() 再按当前消息通道展开。
<<< END U010251 >>>
<<< UNIT U010252 | py-comment | packages/akari-bot-core/tests/test_retired_gate.py:249-249 >>>
# 这里只模拟平台成功持有上下文，parser 与等待任务路由仍执行真实逻辑。
<<< END U010252 >>>
<<< UNIT U010253 | py-comment | packages/akari-bot-core/tests/test_retired_gate.py:390-390 >>>
# 并入同一通道后，退役场景若不被滤除，便会以组内首位的身份排到队首
<<< END U010253 >>>
<<< UNIT U010254 | py-docstring | packages/akari-bot-core/tests/test_retired_gate.py:1-1 | ctx=<module> >>>
akaribot.core.utils.retired 单元测试 - 迁移关系解析、退役判定与介入点。
<<< END U010254 >>>
<<< UNIT U010255 | py-docstring | packages/akari-bot-core/tests/test_retired_gate.py:415-415 | ctx=test_retired_gate >>>
akaribot.core.utils.retired: 迁移关系、退役判定与介入点测试
<<< END U010255 >>>
<<< UNIT U010256 | py-comment | packages/akari-bot-core/tests/test_retired_notice.py:72-72 >>>
# 清空内存后重新加载，验证 list 与 dict 的互转无损。
<<< END U010256 >>>
<<< UNIT U010257 | py-comment | packages/akari-bot-core/tests/test_retired_notice.py:139-139 >>>
# 未串行化时，第一笔保存会在第二笔之后完成，并以只含第一个场景的旧快照覆盖数据库。
<<< END U010257 >>>
<<< UNIT U010258 | py-comment | packages/akari-bot-core/tests/test_retired_notice.py:203-203 >>>
# enqueue_notice 只负责创建后台任务，显式让出一次事件循环使模拟对象完成。
<<< END U010258 >>>
<<< UNIT U010259 | py-docstring | packages/akari-bot-core/tests/test_retired_notice.py:1-1 | ctx=<module> >>>
akaribot.core.utils.retired 单元测试 - 公告文案读取、已发记录与排队。
<<< END U010259 >>>
<<< UNIT U010260 | py-docstring | packages/akari-bot-core/tests/test_retired_notice.py:234-234 | ctx=test_retired_notice >>>
akaribot.core.utils.retired: 公告读取、已发记录与排队测试
<<< END U010260 >>>
<<< UNIT U010261 | py-comment | packages/akari-bot-core/tests/test_rpc_contracts.py:227-227 >>>
# 验证真实上报路径在 RPC 编解码和发送预处理之后仍保留诊断文本。
<<< END U010261 >>>
<<< UNIT U010262 | py-comment | packages/akari-bot-core/tests/test_runtime_lifecycle.py:359-359 >>>
# 给轮询器多次调度机会。正确实现会因 shutdown_window 持有轮询锁而无法进入。
<<< END U010262 >>>
<<< UNIT U010263 | py-docstring | packages/akari-bot-core/tests/test_runtime_lifecycle.py:1-1 | ctx=<module> >>>
Server、客户端与消息入口的后台任务生命周期测试。
<<< END U010263 >>>
<<< UNIT U010264 | py-docstring | packages/akari-bot-core/tests/test_runtime_lifecycle.py:573-573 | ctx=test_runtime_lifecycle >>>
启动、队列、后台初始化与消息任务的失败／关闭路径。
<<< END U010264 >>>
<<< UNIT U010265 | py-docstring | packages/akari-bot-core/tests/test_s3_async.py:1-1 | ctx=<module> >>>
S3 同步 SDK 的异步隔离与超时回归测试。
<<< END U010265 >>>
<<< UNIT U010266 | py-inline-comment | packages/akari-bot-core/tests/test_scheduler.py:27-27 >>>
# 没有计划任务也算通过
<<< END U010266 >>>
<<< UNIT U010267 | py-comment | packages/akari-bot-core/tests/test_scheduler.py:192-192 >>>
# 同一 Task 重入必须直接进入，不能在维护锁上自锁。
<<< END U010267 >>>
<<< UNIT U010268 | py-docstring | packages/akari-bot-core/tests/test_scheduler.py:1-1 | ctx=<module> >>>
计划任务系统单元测试 - 验证模块定时任务注册和执行。
<<< END U010268 >>>
<<< UNIT U010269 | py-docstring | packages/akari-bot-core/tests/test_scheduler.py:270-270 | ctx=test_scheduler_mock >>>
计划任务 Mock 工具测试
<<< END U010269 >>>
<<< UNIT U010270 | py-comment | packages/akari-bot-core/tests/test_secret_filter.py:113-113 >>>
# 显式关闭检查时保持原有放行语义
<<< END U010270 >>>
<<< UNIT U010271 | py-docstring | packages/akari-bot-core/tests/test_secret_filter.py:1-1 | ctx=<module> >>>
发送链路敏感信息拦截的元素覆盖与各出站路径测试。
<<< END U010271 >>>
<<< UNIT U010272 | py-docstring | packages/akari-bot-core/tests/test_secret_filter.py:223-223 | ctx=test_secret_filter >>>
发送链路敏感信息拦截测试
<<< END U010272 >>>
<<< UNIT U010273 | py-comment | packages/akari-bot-core/tests/test_send_direct_message.py:28-28 >>>
# 以给定输入参数调用 send_direct_message，返回其入队任务里的 message 字段。
<<< END U010273 >>>
<<< UNIT U010274 | py-comment | packages/akari-bot-core/tests/test_send_direct_message.py:57-59 >>>
# send_direct_message 曾把未归一化的原始输入参数直接入队。传入 bare 元素（如
# ``I18NContext(...)``）时，其序列化形态为 ``{"_type": "I18NContextElement", ...}``，
# 缺少 values 字段，客户端按 MessageChain | MessageNodes 反序列化即抛出 KeyError。
<<< END U010274 >>>
<<< UNIT U010275 | py-comment | packages/akari-bot-core/tests/test_send_direct_message.py:63-63 >>>
# 反序列化不抛出异常，即证明入队的是完整 MessageChain 而非 bare 元素。
<<< END U010275 >>>
<<< UNIT U010276 | py-docstring | packages/akari-bot-core/tests/test_send_direct_message.py:1-1 | ctx=<module> >>>
core.builtins.session.internal 单元测试 - send_direct_message 的消息归一化（需要数据库）。
<<< END U010276 >>>
<<< UNIT U010277 | py-docstring | packages/akari-bot-core/tests/test_send_direct_message.py:93-93 | ctx=test_send_direct_message >>>
core.builtins.session.internal: send_direct_message 归一化测试
<<< END U010277 >>>
<<< UNIT U010278 | py-docstring | packages/akari-bot-core/tests/test_session.py:1-1 | ctx=<module> >>>
akaribot.core.builtins.session 会话系统单元测试。
<<< END U010278 >>>
<<< UNIT U010279 | py-docstring | packages/akari-bot-core/tests/test_session.py:2988-2988 | ctx=test_features >>>
akaribot.core.builtins.session.features: Features 测试
<<< END U010279 >>>
<<< UNIT U010280 | py-docstring | packages/akari-bot-core/tests/test_session.py:3001-3001 | ctx=test_execution_lock >>>
akaribot.core.builtins.session.lock: ExecutionLockList 测试
<<< END U010280 >>>
<<< UNIT U010281 | py-docstring | packages/akari-bot-core/tests/test_session.py:3024-3024 | ctx=test_session_task >>>
akaribot.core.builtins.session.tasks: SessionTaskManager 测试
<<< END U010281 >>>
<<< UNIT U010282 | py-docstring | packages/akari-bot-core/tests/test_session.py:3083-3083 | ctx=test_message_session_lifecycle >>>
akaribot.core.builtins.session.internal: 消息发送与等待生命周期测试。
<<< END U010282 >>>
<<< UNIT U010283 | py-docstring | packages/akari-bot-core/tests/test_session.py:3110-3110 | ctx=test_strict_confirmation >>>
akaribot.core.builtins.session.internal: 严格确认测试
<<< END U010283 >>>
<<< UNIT U010284 | py-comment | packages/akari-bot-core/tests/test_session_draft.py:27-27 >>>
# 与 Locale.with_locale 一致，切换语言渲染时保留其余状态并返回新对象。
<<< END U010284 >>>
<<< UNIT U010285 | py-comment | packages/akari-bot-core/tests/test_session_draft.py:295-295 >>>
# 默认语言仍可读取为 None，修改其他字段不要求补充语言。
<<< END U010285 >>>
<<< UNIT U010286 | py-comment | packages/akari-bot-core/tests/test_session_draft.py:327-327 >>>
# 正式 payload 的节点文本未被失败 hook 改写
<<< END U010286 >>>
<<< UNIT U010287 | py-comment | packages/akari-bot-core/tests/test_session_draft.py:349-349 >>>
# h2 修改 h1 保留的草稿链，然后失败
<<< END U010287 >>>
<<< UNIT U010288 | py-comment | packages/akari-bot-core/tests/test_session_draft.py:365-365 >>>
# h1 的改写已提交，但 h2 对保留草稿的污染没有进入正式结果
<<< END U010288 >>>
<<< UNIT U010289 | py-comment | packages/akari-bot-core/tests/test_session_draft.py:385-385 >>>
# MessageChain 可以正常提交
<<< END U010289 >>>
<<< UNIT U010290 | py-docstring | packages/akari-bot-core/tests/test_session_draft.py:1-1 | ctx=<module> >>>
SessionDraft 与出站入口单元测试。
<<< END U010290 >>>
<<< UNIT U010291 | py-comment | packages/akari-bot-core/tests/test_session_private.py:10-10 >>>
# 会话由 bot 进程构造、经队列送至 server 进程，标识不随序列化丢失才有意义
<<< END U010291 >>>
<<< UNIT U010292 | py-docstring | packages/akari-bot-core/tests/test_session_private.py:1-1 | ctx=<module> >>>
core.builtins.session 单元测试 - 私聊场景标识（需要数据库）。
<<< END U010292 >>>
<<< UNIT U010293 | py-docstring | packages/akari-bot-core/tests/test_session_private.py:27-27 | ctx=test_session_private >>>
core.builtins.session.info: 私聊标识测试
<<< END U010293 >>>
<<< UNIT U010294 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:31-32 >>>
# 直接构造 SessionInfo 而非经 assign()，以免用例之间共用 union 数据。tz_offset 须显式给出，因为
# 该字段的解析发生在 assign() 中，直接构造时取默认值 None。
<<< END U010294 >>>
<<< UNIT U010295 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:129-129 >>>
# 自定义前缀做的是追加而非替换，没有可预填的单值
<<< END U010295 >>>
<<< UNIT U010296 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:147-148 >>>
# 入口若只出现在底部键盘，用户得自行把按钮与上方的设置行对应起来。全是开关的个人设置区
# 更会整段读成纯状态文字。
<<< END U010296 >>>
<<< UNIT U010297 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:165-166 >>>
# 复刻 send_msg_markdown() 的组装，将指令操作与其后紧随的文本都并入上一项，再以换行连接。该函数
# 绑在平台 SDK 上无法直接调用，而通用的 to_str() 不复现这条规则，故按同样规则建模。
<<< END U010297 >>>
<<< UNIT U010298 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:187-188 >>>
# 指令操作会使适配器把紧随其后的文本并入同一行，换行若交由适配器按元素处理，整个面板
# 会合并成一行。故此路径下的换行必须写入文本自身。
<<< END U010298 >>>
<<< UNIT U010299 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:198-198 >>>
# 两个标题各一行，其余每项设置一行
<<< END U010299 >>>
<<< UNIT U010300 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:210-211 >>>
# 该路径下指令操作已在消息链阶段并入前一个文本元素，各行本就是独立元素，再写换行
# 只会多出空行。
<<< END U010300 >>>
<<< UNIT U010301 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:306-308 >>>
# 指令操作降级为纯文本后会并入前一个文本元素，合并时既不补分隔符，也会连同命令原文
# 一起参与玩笑替换，两者缺一都会使降级平台上的命令无法复制。
# 首个纯文本元素是分组标题，它不带入口，无须留空格
<<< END U010301 >>>
<<< UNIT U010302 | py-comment | packages/akari-bot-core/tests/test_setup_panel.py:346-346 >>>
# 文案须取自按钮专设的键，因为面板标题带有分隔用的方括号，套进按钮里并不合适
<<< END U010302 >>>
<<< UNIT U010303 | py-docstring | packages/akari-bot-core/tests/test_setup_panel.py:1-1 | ctx=<module> >>>
设置面板单元测试 - 设置行的构造与渲染。
<<< END U010303 >>>
<<< UNIT U010304 | py-docstring | packages/akari-bot-core/tests/test_setup_panel.py:356-356 | ctx=test_setup_panel >>>
akaribot.modules.core.common_tools.setup: 设置面板构造测试
<<< END U010304 >>>
<<< UNIT U010305 | py-comment | packages/akari-bot-core/tests/test_status.py:40-40 >>>
# 语言键缺失时会改用键名或提示，故一律检查不含 "core.message"。
<<< END U010305 >>>
<<< UNIT U010306 | py-docstring | packages/akari-bot-core/tests/test_status.py:1-1 | ctx=<module> >>>
status 模块的 Markdown 排版与进程行测试。
<<< END U010306 >>>
<<< UNIT U010307 | py-docstring | packages/akari-bot-core/tests/test_status.py:60-60 | ctx=test_status >>>
status: Markdown 能力选择代码块或纯文本。
<<< END U010307 >>>
<<< UNIT U010308 | py-docstring | packages/akari-bot-core/tests/test_storedata.py:1-1 | ctx=<module> >>>
core.utils.storedata 单元测试 - 存储工具（需要数据库）。
<<< END U010308 >>>
<<< UNIT U010309 | py-docstring | packages/akari-bot-core/tests/test_storedata.py:36-36 | ctx=test_storedata >>>
core.utils.storedata: 存储工具测试
<<< END U010309 >>>
<<< UNIT U010310 | py-docstring | packages/akari-bot-core/tests/test_suppress_invalid_prompt.py:1-1 | ctx=<module> >>>
core.types.module 单元测试 - 模块级命令语法错误提示开关。
<<< END U010310 >>>
<<< UNIT U010311 | py-docstring | packages/akari-bot-core/tests/test_suppress_invalid_prompt.py:28-28 | ctx=test_suppress_invalid_prompt >>>
core.types.module: 命令语法错误提示开关测试
<<< END U010311 >>>
<<< UNIT U010312 | py-comment | packages/akari-bot-core/tests/test_term_locale.py:18-18 >>>
# 该键的文案为“查看当前{TERM:target}的消息通道与主动推送优先级。”
<<< END U010312 >>>
<<< UNIT U010313 | py-comment | packages/akari-bot-core/tests/test_term_locale.py:55-55 >>>
# 无会话上下文的 Locale 构造点，这些出口渲染的不是会话文案，或另有语言来源。
<<< END U010313 >>>
<<< UNIT U010314 | py-comment | packages/akari-bot-core/tests/test_term_locale.py:69-69 >>>
# 会话缺失时的默认构造，此时本就没有作用域可言。
<<< END U010314 >>>
<<< UNIT U010315 | py-comment | packages/akari-bot-core/tests/test_term_locale.py:90-90 >>>
# 前缀格式由平台侧确定，非法字符会被剔除；剔除后为空的整条链改用基础术语，流程不中断。
<<< END U010315 >>>
<<< UNIT U010316 | py-comment | packages/akari-bot-core/tests/test_term_locale.py:120-120 >>>
# 术语缺失时原样保留占位符，不抛出异常
<<< END U010316 >>>
<<< UNIT U010317 | py-comment | packages/akari-bot-core/tests/test_term_locale.py:174-174 >>>
# 术语词条只应出现在 `locales/terms/` 下。顶层残留副本会被术语目录覆盖并报审计条目。
<<< END U010317 >>>
<<< UNIT U010318 | py-comment | packages/akari-bot-core/tests/test_term_locale.py:211-211 >>>
# 按语法树而非物理行判定，避免多行调用与注释里的字样造成误报。
<<< END U010318 >>>
<<< UNIT U010319 | py-docstring | packages/akari-bot-core/tests/test_term_locale.py:1-1 | ctx=<module> >>>
术语占位符与会话术语作用域单元测试。
<<< END U010319 >>>
<<< UNIT U010320 | py-docstring | packages/akari-bot-core/tests/test_term_locale.py:235-235 | ctx=test_term_locale >>>
akaribot.core.i18n: 术语占位符与会话作用域测试
<<< END U010320 >>>
<<< UNIT U010321 | py-comment | packages/akari-bot-core/tests/test_timezone_offset.py:13-13 >>>
# 场景与用户数据中承载时区偏移的键，写入方为 modules/core/common_tools/setup.py
<<< END U010321 >>>
<<< UNIT U010322 | py-docstring | packages/akari-bot-core/tests/test_timezone_offset.py:1-1 | ctx=<module> >>>
时区偏移取值来源测试。
<<< END U010322 >>>
<<< UNIT U010323 | py-docstring | packages/akari-bot-core/tests/test_timezone_offset.py:131-131 | ctx=test_timezone_offset >>>
akaribot.core.builtins.session.info: 时区偏移取值来源测试
<<< END U010323 >>>
<<< UNIT U010324 | py-docstring | packages/akari-bot-core/tests/test_tos.py:1-1 | ctx=<module> >>>
ToS 管理系统单元测试（实现位于 modules/core/hooks/tos.py）。
<<< END U010324 >>>
<<< UNIT U010325 | py-docstring | packages/akari-bot-core/tests/test_tos.py:192-192 | ctx=test_tos >>>
akaribot.modules.core.hooks.tos: TOS 管理系统测试
<<< END U010325 >>>
<<< UNIT U010326 | py-docstring | packages/akari-bot-core/tests/test_typing_prompt.py:1-1 | ctx=<module> >>>
输入提示开关的取值来源测试。
<<< END U010326 >>>
<<< UNIT U010327 | py-docstring | packages/akari-bot-core/tests/test_typing_prompt.py:65-65 | ctx=test_typing_prompt >>>
core.builtins.session.info: 输入提示开关的取值来源测试
<<< END U010327 >>>
<<< UNIT U010328 | py-comment | packages/akari-bot-core/tests/test_union.py:29-29 >>>
# 同一 ID 应始终解析至原 union，不得重复创建。
<<< END U010328 >>>
<<< UNIT U010329 | py-comment | packages/akari-bot-core/tests/test_union.py:170-170 >>>
# 组内任一账号解析出的都是同一行，换账号绕不过封禁。
<<< END U010329 >>>
<<< UNIT U010330 | py-comment | packages/akari-bot-core/tests/test_union.py:185-185 >>>
# 合并只会把封禁传染给对方，不存在借合并洗白的方向。
<<< END U010330 >>>
<<< UNIT U010331 | py-comment | packages/akari-bot-core/tests/test_union.py:203-204 >>>
# 映射行重新关联而非重建，确保拆出的账号在任一时刻都能解析回一个已封禁的组，
# 不会因缺少映射行而被当作新账号新建干净组。
<<< END U010331 >>>
<<< UNIT U010332 | py-comment | packages/akari-bot-core/tests/test_union.py:238-238 >>>
# 不沿用任何一方的组 ID，合并方向才不存在歧义。
<<< END U010332 >>>
<<< UNIT U010333 | py-comment | packages/akari-bot-core/tests/test_union.py:271-271 >>>
# 键冲突保留发起方，不冲突的键则一并带过来。
<<< END U010333 >>>
<<< UNIT U010334 | py-comment | packages/akari-bot-core/tests/test_union.py:296-296 >>>
# 两侧的旧 ID 均须改写至新组，遗漏任何一侧都会导致管理员身份丢失。
<<< END U010334 >>>
<<< UNIT U010335 | py-comment | packages/akari-bot-core/tests/test_union.py:314-314 >>>
# union_id 为模块表主键，重新关联只能通过重建行完成，各列值须原样保留。
<<< END U010335 >>>
<<< UNIT U010336 | py-comment | packages/akari-bot-core/tests/test_union.py:381-381 >>>
# JSON 列在重建时可能被写为字符串，此处确认取回后仍为字典。
<<< END U010336 >>>
<<< UNIT U010337 | py-comment | packages/akari-bot-core/tests/test_union.py:710-710 >>>
# 两侧均自 1 起编号，直接合表会使四个互不相关的场景被归为两条通道。
<<< END U010337 >>>
<<< UNIT U010338 | py-comment | packages/akari-bot-core/tests/test_union.py:758-758 >>>
# 花瓣保留在原 union，警告次数随账号转移，避免通过解绑规避处罚。
<<< END U010338 >>>
<<< UNIT U010339 | py-docstring | packages/akari-bot-core/tests/test_union.py:1-1 | ctx=<module> >>>
core.database.models 单元测试 - union 绑定（需要数据库）。
<<< END U010339 >>>
<<< UNIT U010340 | py-docstring | packages/akari-bot-core/tests/test_union.py:1323-1323 | ctx=test_union >>>
core.database.models: union 绑定测试
<<< END U010340 >>>
<<< UNIT U010341 | py-comment | packages/akari-bot-core/tests/test_union_push.py:12-12 >>>
# 各用例使用的客户端名。保活表由测试自行提供，故不必是真实存在的平台。
<<< END U010341 >>>
<<< UNIT U010342 | py-comment | packages/akari-bot-core/tests/test_union_push.py:15-15 >>>
# 保活表的最简形态，键为客户端名，前缀用于由场景 ID 反向查找客户端。
<<< END U010342 >>>
<<< UNIT U010343 | py-comment | packages/akari-bot-core/tests/test_union_push.py:51-51 >>>
# 队首承担推送，同通道的其余会话降为发送失败时的下一跳
<<< END U010343 >>>
<<< UNIT U010344 | py-comment | packages/akari-bot-core/tests/test_union_push.py:72-72 >>>
# 先绑定的 UPUSHB 场景 ID 在字典序上更大，同分时仍应先发送。
<<< END U010344 >>>
<<< UNIT U010345 | py-comment | packages/akari-bot-core/tests/test_union_push.py:74-74 >>>
# 绑定时间由时钟写入，粗粒度时钟上两次绑定会处于同一微秒。按绑定顺序显式赋值。
<<< END U010345 >>>
<<< UNIT U010346 | py-comment | packages/akari-bot-core/tests/test_union_push.py:119-119 >>>
# 仅 UPUSHB 在线，UPUSHA 所在通道无人可送
<<< END U010346 >>>
<<< UNIT U010347 | py-comment | packages/akari-bot-core/tests/test_union_push.py:138-138 >>>
# 两个通道分别生成消息，且工厂接收实际承担推送的会话。
<<< END U010347 >>>
<<< UNIT U010348 | py-comment | packages/akari-bot-core/tests/test_union_push.py:156-156 >>>
# 仅其中一条通道有内容可发
<<< END U010348 >>>
<<< UNIT U010349 | py-comment | packages/akari-bot-core/tests/test_union_push.py:169-169 >>>
# 上报场景按平台场景 ID 配置，同一个现实场景的两个平台都被填了进来
<<< END U010349 >>>
<<< UNIT U010350 | py-docstring | packages/akari-bot-core/tests/test_union_push.py:1-1 | ctx=<module> >>>
Bot.send_direct_message_to_union_target 单元测试 - 按消息通道去重的组内推送。
<<< END U010350 >>>
<<< UNIT U010351 | py-docstring | packages/akari-bot-core/tests/test_union_push.py:193-193 | ctx=test_union_push >>>
akaribot.core.builtins.bot: 按消息通道去重的组内推送测试
<<< END U010351 >>>
<<< UNIT U010352 | py-comment | packages/akari-bot-core/tests/test_url_guard.py:21-21 >>>
# 跳板服务的域名，用以检查某条路径确实未走跳板
<<< END U010352 >>>
<<< UNIT U010353 | py-comment | packages/akari-bot-core/tests/test_url_guard.py:60-61 >>>
# wikilib 在内容审查未通过时即以 trusted=False 传入，该场景须无视会话设置。
# 此路径下 url 字段已被替换成跳板地址，须取 original_url 方能拿回原链接。
<<< END U010353 >>>
<<< UNIT U010354 | py-comment | packages/akari-bot-core/tests/test_url_guard.py:305-306 >>>
# 关闭 markdown 只应令呈现回退到跳板。若连 use_url_manager 一并关闭，未认证链接便
# 完全不再被标记，等同于取消保护。
<<< END U010354 >>>
<<< UNIT U010355 | py-comment | packages/akari-bot-core/tests/test_url_guard.py:308-309 >>>
# 平台能力集在导入时即依配置定型，故新建一份“markdown 与 URLManager 均已开启”
# 的基准并模拟该开关，使检查只考察覆盖逻辑本身，不受本地配置左右
<<< END U010355 >>>
<<< UNIT U010356 | py-comment | packages/akari-bot-core/tests/test_url_guard.py:329-330 >>>
# I18N 参数中的 MessageChain 会被转成 KE 码再解析回来（chain.py:340）。标记若在
# 这一趟丢失，已认证的链接会退化为未表态，进而被会话的 URLManager 套上跳板。
<<< END U010356 >>>
<<< UNIT U010357 | py-comment | packages/akari-bot-core/tests/test_url_guard.py:345-346 >>>
# trusted 为 False 时 url 字段已是跳板地址，故 kecode 须编码 original_url。
# 若照搬 url，还原时会在跳板地址之上再套一层跳板。
<<< END U010357 >>>
<<< UNIT U010358 | py-docstring | packages/akari-bot-core/tests/test_url_guard.py:1-1 | ctx=<module> >>>
未认证链接的呈现方式单元测试。
<<< END U010358 >>>
<<< UNIT U010359 | py-docstring | packages/akari-bot-core/tests/test_url_guard.py:374-374 | ctx=test_url_guard >>>
未认证链接的代码块呈现与回退测试
<<< END U010359 >>>
<<< UNIT U010360 | py-comment | packages/akari-bot-core/tests/test_webrender_rpc.py:22-22 >>>
# 真实返回值以 BrowserContext 对象为键，任何序列化途径都无法处理。
<<< END U010360 >>>
<<< UNIT U010361 | py-comment | packages/akari-bot-core/tests/test_webrender_rpc.py:95-95 >>>
# 被拦截的请求不得触达依赖库
<<< END U010361 >>>
<<< UNIT U010362 | py-docstring | packages/akari-bot-core/tests/test_webrender_rpc.py:1-1 | ctx=<module> >>>
core.queue.server 新增 WebUI 相关处理器的单元测试。
<<< END U010362 >>>
<<< UNIT U010363 | py-docstring | packages/akari-bot-core/tests/test_webrender_rpc.py:152-152 | ctx=test_webrender_rpc >>>
core.queue.server: 状态净化与渲染测试参数校验测试
<<< END U010363 >>>
<<< UNIT U010364 | md-paragraph | packages/akari-bot-testing/README.md:3-3 | ctx=akari-bot-testing >>>
提供 AkariBot 的测试框架与运行器。
<<< END U010364 >>>
<<< UNIT U010365 | md-heading | packages/akari-bot-testing/README.md:5-5 | ctx=安装 >>>
## 安装
<<< END U010365 >>>
<<< UNIT U010366 | md-paragraph | packages/akari-bot-testing/README.md:7-7 | ctx=安装 >>>
Python 版本要求见包内 `pyproject.toml` 的 `requires-python`。
<<< END U010366 >>>
<<< UNIT U010367 | md-paragraph | packages/akari-bot-testing/README.md:13-13 | ctx=安装 >>>
运行、配置与模块管理参见 [项目文档](https://github.com/Teahouse-Studios/akari-bot/blob/master/README.md)。
<<< END U010367 >>>
<<< UNIT U010368 | py-comment | packages/akari-bot-testing/akaribot/testing/__init__.py:40-41 >>>
# 子模块名直接返回子模块本身，避免为获取 ``runner`` 而先加载 ``tester``（后者依赖 core，
# 会把路径固定在隔离环境变量就位之前）。
<<< END U010368 >>>
<<< UNIT U010369 | py-docstring | packages/akari-bot-testing/akaribot/testing/__init__.py:30-39 | ctx=__getattr__ >>>
首次访问时解析公开名。

    子模块名直接返回子模块本身，避免为获取 ``runner`` 而先加载 ``tester``（后者依赖 core，
    会把路径固定在隔离环境变量就位之前）。

    :param name: 属性名。
    :return: 对应的对象。
    :raises AttributeError: 该名字不在任何子模块的公开接口内。
<<< END U010369 >>>
<<< UNIT U010370 | py-docstring | packages/akari-bot-testing/akaribot/testing/__init__.py:52-54 | ctx=__dir__ >>>
列出公开名，供交互式补全与文档工具使用。
<<< END U010370 >>>
<<< UNIT U010371 | py-docstring | packages/akari-bot-testing/akaribot/testing/decorator.py:9-9 | ctx=CaseEntry >>>
由 :func:`case` 注册的测试项。
<<< END U010371 >>>
<<< UNIT U010372 | py-docstring | packages/akari-bot-testing/akaribot/testing/decorator.py:29-29 | ctx=case >>>
快捷注册一个测试案例。
<<< END U010372 >>>
<<< UNIT U010373 | py-docstring | packages/akari-bot-testing/akaribot/testing/decorator.py:55-55 | ctx=func_case >>>
标记函数是否为测试函数（测试时会被调用）。
<<< END U010373 >>>
<<< UNIT U010374 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/index.md:1-1 | ctx=测试框架 >>>
# 测试框架
<<< END U010374 >>>
<<< UNIT U010375 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:3-3 | ctx=测试框架 >>>
`akaribot.testing` 是 AkariBot 的自研测试框架与运行器。用例直接调用真实模块与简化的消息解析器，不使用 pytest 的用例收集与 fixture 机制。根目录的 `conftest.py` 只是兼容适配层，行为差异以本框架为准。
<<< END U010375 >>>
<<< UNIT U010376 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/index.md:5-5 | ctx=运行入口 >>>
## 运行入口
<<< END U010376 >>>
<<< UNIT U010377 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:7-7 | ctx=运行入口 >>>
在源码仓库内：
<<< END U010377 >>>
<<< UNIT U010378 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:13-13 | ctx=运行入口 >>>
根目录的 `tester.py` 是兼容实现，转发到同一个运行器，参数与行为一致。包安装到实例后，也可以用 CLI：
<<< END U010378 >>>
<<< UNIT U010379 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:20-20 | ctx=运行入口 >>>
`akaribot test` 先确认实例环境里能导入 `akaribot.testing`，缺少该包时提示安装 `akari-bot-testing`。无法识别的参数原样交给运行器。
<<< END U010379 >>>
<<< UNIT U010380 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/index.md:22-22 | ctx=测试范围 >>>
## 测试范围
<<< END U010380 >>>
<<< UNIT U010381 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:24-24 | ctx=测试范围 >>>
运行器默认收集仓库根目录的 `tests/`，在源码仓库中还会收集 `packages/*/tests` 与 `packages/*/*/tests`。给出位置参数时只运行这些文件或目录，相对路径按仓库根目录解析。
<<< END U010381 >>>
<<< UNIT U010382 | md-list | packages/akari-bot-testing/akaribot/testing/docs/index.md:26-28 | ctx=测试范围 >>>
- `--case <子串>`：只运行名字含该子串的 `@func_case`，可重复。
- `--ci`：CI 模式，跳过需要人工复核的用例。非 CI 模式下，缺少期望值的用例可能等待输入。
- `--coverage`：收集覆盖率，入口脚本需要安装 `coverage`。
<<< END U010382 >>>
<<< UNIT U010383 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:30-30 | ctx=测试范围 >>>
测试文件放在 `tests/unit/`（纯函数）、`tests/integration/`（完整命令流程）与 `packages/*/tests/`（包内自测）。跨包共享的 HTTP 测试数据放在 `tests/fixtures/http/`。
<<< END U010383 >>>
<<< UNIT U010384 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/index.md:32-32 | ctx=CI 模式 >>>
## CI 模式
<<< END U010384 >>>
<<< UNIT U010385 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:34-34 | ctx=CI 模式 >>>
自动化运行必须设置 `CI=1` 或传 `--ci`。没有 `expected` 的用例，以及交互输入耗尽的用例，在非 CI 模式下会调用 `input()`，在非交互终端里挂起。
<<< END U010385 >>>
<<< UNIT U010386 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:36-36 | ctx=CI 模式 >>>
CI 模式跳过人工复核，交互输入不足直接判定失败。`--ci` 还会把 CI 开关写入环境变量，因为运行器在导入期就读取它。
<<< END U010386 >>>
<<< UNIT U010387 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:38-38 | ctx=CI 模式 >>>
CI 模式另设 `AKARI_TEST_TIME_SCALE=10` 放宽超时。完整运行会生成 `junit.xml`。覆盖率开启时另生成 `htmlcov/index.html` 与 `coverage.xml`。
<<< END U010387 >>>
<<< UNIT U010388 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/index.md:40-40 | ctx=单入口运行 >>>
## 单入口运行
<<< END U010388 >>>
<<< UNIT U010389 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:42-42 | ctx=单入口运行 >>>
开发期只运行一个文件或一个入口。示例：
<<< END U010389 >>>
<<< UNIT U010390 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:49-49 | ctx=单入口运行 >>>
第二个参数是入口函数名，省略时运行该文件中所有以 `test_` 开头的入口函数。脚本强制 CI 模式，收尾用 `os._exit` 退出，避免框架遗留的后台任务阻塞进程。
<<< END U010390 >>>
<<< UNIT U010391 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:51-51 | ctx=单入口运行 >>>
因此，它不适合需要 `expected=None` 人工复核的用例。`tester.py` 与模块入口没有路径或用例筛选参数。
<<< END U010391 >>>
<<< UNIT U010392 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/index.md:53-53 | ctx=环境隔离 >>>
## 环境隔离
<<< END U010392 >>>
<<< UNIT U010393 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:55-55 | ctx=环境隔离 >>>
运行器在导入期建立隔离环境，这一步必须先于任何 `akaribot.core` 导入：
<<< END U010393 >>>
<<< UNIT U010394 | md-list | packages/akari-bot-testing/akaribot/testing/docs/index.md:57-60 | ctx=环境隔离 >>>
- 配置来自临时目录，环境变量 `AKARI_CONFIG_PATH` 指向它，测试结束后删除。
- union 合并日志写入临时目录（`AKARI_UNION_MERGE_LOGS_PATH`），测试结束后删除。显式设置的值优先。
- 数据库使用内存 SQLite，每个用例入口前重建。
- HTTP 响应从 `tests/fixtures/http/` 回放，网络模块不访问真实服务。
<<< END U010394 >>>
<<< UNIT U010395 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:62-62 | ctx=环境隔离 >>>
需要留存合并日志时，把 `AKARI_UNION_MERGE_LOGS_PATH` 指向要保存的目录即可。
<<< END U010395 >>>
<<< UNIT U010396 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/index.md:64-64 | ctx=编写用例 >>>
## 编写用例
<<< END U010396 >>>
<<< UNIT U010397 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/index.md:66-66 | ctx=编写用例 >>>
用例写法、匹配器、fixture 与常见陷阱见 [编写用例](writing-tests.md)。
<<< END U010397 >>>
<<< UNIT U010398 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:1-1 | ctx=编写用例 >>>
# 编写用例
<<< END U010398 >>>
<<< UNIT U010399 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:3-3 | ctx=文件位置 >>>
## 文件位置
<<< END U010399 >>>
<<< UNIT U010400 | md-table | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:5-11 | ctx=文件位置 >>>
| 目录 | 内容 |
| --- | --- |
| `tests/unit/` | 纯函数与类型测试 |
| `tests/integration/` | 覆盖完整命令链路的集成测试 |
| `tests/fixtures/http/` | 录制的 HTTP 响应 |
| `tests/helpers/` | RPC worker 等辅助进程 |
| `packages/*/tests/` | 包自带的测试 |
<<< END U010400 >>>
<<< UNIT U010401 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:13-13 | ctx=文件位置 >>>
文件名以 `test_` 开头。不同包可以存在同名文件，运行器按仓库相对路径生成模块名。
<<< END U010401 >>>
<<< UNIT U010402 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:17-17 | ctx=`@func_case` >>>
一个被 `@func_case` 标记的 async 函数就是一个用例，参数是 `Tester`。现有用例通常在末尾 `return tester`，框架也会从传入对象收集结果。
<<< END U010402 >>>
<<< UNIT U010403 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:19-19 | ctx=`@func_case` >>>
示例：
<<< END U010403 >>>
<<< UNIT U010404 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:31-31 | ctx=`@func_case` >>>
`Tester` 只有两个用于检查的方法：
<<< END U010404 >>>
<<< UNIT U010405 | md-list | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:33-34 | ctx=`@func_case` >>>
- `await tester.integrate(input_, expected=None, note=None, timeout=None)`：发送一条命令并校验输出。`input_` 为字符串列表时表示连续多条消息，用于交互式命令。
- `await tester.test(func, note=None)`：调用纯函数或谓词，返回真值即通过，支持同步与异步。框架不提供 `tester.expect()`。
<<< END U010405 >>>
<<< UNIT U010406 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:36-36 | ctx=`@func_case` >>>
`expected` 传 `Expectation`。传 `None` 表示人工复核，只能在交互式全量运行中使用。
<<< END U010406 >>>
<<< UNIT U010407 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:40-40 | ctx=`@case` >>>
`@case` 把用例挂载在命令定义旁，模块被导入时注册。
<<< END U010407 >>>
<<< UNIT U010408 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:42-42 | ctx=`@case` >>>
示例：
<<< END U010408 >>>
<<< UNIT U010409 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:54-54 | ctx=`@case` >>>
说明：
<<< END U010409 >>>
<<< UNIT U010410 | md-list | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:56-57 | ctx=`@case` >>>
- 第一个参数是输入，第二个参数是期望，另可给 `note` 与 `timeout`。
- `@case` 用例的并发上限为 1。
<<< END U010410 >>>
<<< UNIT U010411 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:59-59 | ctx=匹配器 >>>
## 匹配器
<<< END U010411 >>>
<<< UNIT U010412 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:61-61 | ctx=匹配器 >>>
全部匹配器继承 `Expectation`，可用 `&`、`|`、`~` 组合，也可直接用 `All`、`Any`、`Not`。
<<< END U010412 >>>
<<< UNIT U010413 | md-table | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:63-75 | ctx=匹配器 >>>
| 匹配器 | 判定 |
| --- | --- |
| `Match(text)` | 渲染后的文本精确相等，默认不区分大小写 |
| `Equal(message)` | 可发送消息链完全相等 |
| `Contains` / `ContainsAll` / `ContainsAny` | 包含一个 / 全部 / 任一字符串 |
| `StartsWith` / `EndsWith` / `Regex` | 前缀、后缀、正则 |
| `InOrder` / `StructureEqual` | 元素按给定类型的顺序出现 / 数量、顺序与类型严格一致 |
| `Length` / `Count` / `OutputCount` | 元素总数 / 某类型数量 / 平台动作条目数 |
| `Exist` | 存在指定类型的元素 |
| `Empty` / `AnyOutput` | 无输出 / 有输出 |
| `Raise` / `NoException` | 期望异常 / 期望不抛出异常 |
| `ActionContains` | 平台动作包含指定内容 |
| `Predicate(func)` | 自定义判定函数 |
<<< END U010413 >>>
<<< UNIT U010414 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:77-77 | ctx=匹配器 >>>
`Contains` 同时检查纯文本与带媒体描述的完整文本。`ActionContains` 用于撤回、禁言等平台动作。
<<< END U010414 >>>
<<< UNIT U010415 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:79-79 | ctx=测试环境 >>>
## 测试环境
<<< END U010415 >>>
<<< UNIT U010416 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:81-81 | ctx=测试环境 >>>
集成测试使用 `akaribot/testing/mock/parser.py` 的简化 parser，与生产 parser 有三点差异：
<<< END U010416 >>>
<<< UNIT U010417 | md-list | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:83-85 | ctx=测试环境 >>>
1. 不按平台过滤模块。
2. 命令分发不检查模块是否已启用，无需先 `~module enable`。
3. 发送者被设为 superuser，多数权限检查直接通过。
<<< END U010417 >>>
<<< UNIT U010418 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:87-87 | ctx=测试环境 >>>
因此测试通过不代表命令在真实平台可达。涉及平台过滤、模块开关与权限的改动要另行确认。
<<< END U010418 >>>
<<< UNIT U010419 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:89-89 | ctx=测试环境 >>>
其余模拟组件：
<<< END U010419 >>>
<<< UNIT U010420 | md-list | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:91-95 | ctx=测试环境 >>>
- `mock/database.py`：内存 SQLite，运行用例前重建。
- `mock/loader.py`：加载全部已发现模块，可注入 monkey patch。
- `mock/random.py`：固定种子，随机输出可复现。
- `mock/http.py` 与 `mock/fixtures.py`：按 URL、方法、请求体摘要回放 HTTP 响应。
- `mock/session.py`：记录 `sent`、`action` 与按钮数据。
<<< END U010420 >>>
<<< UNIT U010421 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:97-97 | ctx=测试环境 >>>
需要替换 `Config` 等全局对象时用 `unittest.mock.patch`。
<<< END U010421 >>>
<<< UNIT U010422 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:101-101 | ctx=Fixture >>>
`load_modules()` 自动加载 `tests/fixtures/http/` 下的全部 JSON。新增网络模块用例时，先用 `tests/capture_http_fixtures.py` 录制真实响应，再让测试离线回放。手工构造可用 `save_fixture()`。
<<< END U010422 >>>
<<< UNIT U010423 | md-paragraph | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:103-103 | ctx=Fixture >>>
文件名是 URL、方法与请求体摘要的哈希，同一 URL 上不同请求体各自成文件。
<<< END U010423 >>>
<<< UNIT U010424 | md-heading | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:105-105 | ctx=常见陷阱 >>>
## 常见陷阱
<<< END U010424 >>>
<<< UNIT U010425 | md-list | packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md:107-113 | ctx=常见陷阱 >>>
- 自动化运行必须设置 `CI=1`。否则人工复核与交互输入会挂起。
- `tests/run_one.py` 强制 CI 模式，不适用于需要人工复核的用例。结束时调用的 `os._exit` 会跳过常规清理。
- 只检查对外行为，不要检查私有属性、调用次数、日志条数或提示文案的完整措辞。
- 比较结构化返回值时优先声明必需字段，避免新增字段让既有用例失败。
- 集成用例会启动队列轮询与后台任务。用例结束前让会话正常结束，不要留下未完成任务。
- Windows 下运行中文测试时设置 `PYTHONIOENCODING=UTF-8`。
- 不要在本地运行全量用例。全量由 CI 承担，本地只运行改动相关的文件或入口。
<<< END U010425 >>>
<<< UNIT U010426 | py-comment | packages/akari-bot-testing/akaribot/testing/expectations.py:26-26 >>>
# 失败日志与 JUnit 报告直接展示期望对象，缺少 __repr__ 时只能看到内存地址。
<<< END U010426 >>>
<<< UNIT U010427 | py-comment | packages/akari-bot-testing/akaribot/testing/expectations.py:508-508 >>>
# 检查是否包含错误信息
<<< END U010427 >>>
<<< UNIT U010428 | py-comment | packages/akari-bot-testing/akaribot/testing/expectations.py:603-603 >>>
# 检查是否有异常
<<< END U010428 >>>
<<< UNIT U010429 | py-comment | packages/akari-bot-testing/akaribot/testing/expectations.py:607-607 >>>
# 检查是否有 traceback
<<< END U010429 >>>
<<< UNIT U010430 | py-comment | packages/akari-bot-testing/akaribot/testing/expectations.py:611-611 >>>
# 检查输出是否包含错误信息
<<< END U010430 >>>
<<< UNIT U010431 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:20-20 | ctx=Expectation >>>
所有期望匹配器的基类。
<<< END U010431 >>>
<<< UNIT U010432 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:40-44 | ctx=All >>>
满足所有期望匹配器。

:param expects: 期望匹配器
<<< END U010432 >>>
<<< UNIT U010433 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:60-64 | ctx=Any >>>
满足任意期望匹配器。

:param expects: 期望匹配器
<<< END U010433 >>>
<<< UNIT U010434 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:80-84 | ctx=Not >>>
不允许满足某一期望匹配器。

:param expect: 期望匹配器
<<< END U010434 >>>
<<< UNIT U010435 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:98-98 | ctx=Empty >>>
是否无输出。
<<< END U010435 >>>
<<< UNIT U010436 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:131-136 | ctx=Match >>>
消息文本是否匹配。

:param msg_chain: 期望消息链
:param case_sensitive: 是否大小写敏感，默认 False
<<< END U010436 >>>
<<< UNIT U010437 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:161-166 | ctx=Contains >>>
消息文本中是否包含特定字符串。

:param text: 期望字符串
:param case_sensitive: 是否大小写敏感，默认 False
<<< END U010437 >>>
<<< UNIT U010438 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:186-191 | ctx=StartsWith >>>
消息文本开头是否包含特定字符串。

:param text: 期望字符串
:param case_sensitive: 是否大小写敏感，默认 False
<<< END U010438 >>>
<<< UNIT U010439 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:210-215 | ctx=EndsWith >>>
消息文本结尾是否包含特定字符串。

:param text: 期望字符串
:param case_sensitive: 是否大小写敏感，默认 False
<<< END U010439 >>>
<<< UNIT U010440 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:234-239 | ctx=Regex >>>
消息文本中是否满足正则表达式。

:param pattern: 正则表达式
:param flags: 匹配方式
<<< END U010440 >>>
<<< UNIT U010441 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:252-258 | ctx=Length >>>
消息链长度是否符合预期。

:param eq: 预期消息链精确长度
:param ge: 预期消息链最小长度
:param le: 预期消息链最大长度
<<< END U010441 >>>
<<< UNIT U010442 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:288-293 | ctx=Exist >>>
消息链中是否含有对应消息元素类型。

:param element: 消息元素类型
:param func: 自定义函数
<<< END U010442 >>>
<<< UNIT U010443 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:322-329 | ctx=Count >>>
匹配消息链中消息元素的数量。

:param element: 消息元素类型
:param eq: 预期匹配精确数量
:param ge: 预期匹配最小数量
:param le: 预期匹配最大数量
<<< END U010443 >>>
<<< UNIT U010444 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:439-445 | ctx=Raise >>>
检查抛出的异常。

:param exc: 异常类型
:param message_contain: 期望异常消息包含的字符串
:param case_sensitive: 是否大小写敏感，默认 False
<<< END U010444 >>>
<<< UNIT U010445 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:480-484 | ctx=Predicate >>>
自定义期望匹配器。

:param func: 自定义函数
<<< END U010445 >>>
<<< UNIT U010446 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:499-499 | ctx=AnyOutput >>>
是否有任意输出（非空）。
<<< END U010446 >>>
<<< UNIT U010447 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:550-555 | ctx=ContainsAll >>>
输出中包含所有指定文本。

:param texts: 需要全部包含的文本列表
:param case_sensitive: 是否大小写敏感，默认 False
<<< END U010447 >>>
<<< UNIT U010448 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:574-579 | ctx=ContainsAny >>>
输出中包含任一指定文本。

:param texts: 需要至少包含一个的文本列表
:param case_sensitive: 是否大小写敏感，默认 False
<<< END U010448 >>>
<<< UNIT U010449 | py-docstring | packages/akari-bot-testing/akaribot/testing/expectations.py:598-598 | ctx=NoException >>>
执行过程中无异常。
<<< END U010449 >>>
<<< UNIT U010450 | cfg-comment | packages/akari-bot-testing/akaribot/testing/manifest.toml:1-2 >>>
# akari-bot-testing 的包清单。
# 本包不是模块或适配器，无 registry 条目，清单仅供包说明。
<<< END U010450 >>>
<<< UNIT U010451 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/config.py:17-17 >>>
# patch 由最外层上下文持有，嵌套进入时不再重复替换，也就不会被内层退出提前还原
<<< END U010451 >>>
<<< UNIT U010452 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/config.py:26-26 >>>
# 与 CFGManager 的表名归一化保持一致，secret 与 *_secret 都指向 config 文件的密钥表
<<< END U010452 >>>
<<< UNIT U010453 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/config.py:50-50 >>>
# 未限定表名的读取要么只在 config.toml 内查找，要么按 _global 遍历全部表
<<< END U010453 >>>
<<< UNIT U010454 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/config.py:71-71 >>>
# 生成模式写入的是模板默认值，不能被测试覆盖值污染
<<< END U010454 >>>
<<< UNIT U010455 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/config.py:107-107 >>>
# 先解析全部字段，避免字段名有误时已写入的覆盖残留
<<< END U010455 >>>
<<< UNIT U010456 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/database.py:13-13 | ctx=get_last_init_error >>>
返回最近一次测试数据库初始化失败的诊断信息。
<<< END U010456 >>>
<<< UNIT U010457 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/factory.py:1-1 | ctx=<module> >>>
测试数据工厂 - 快速创建测试数据。
<<< END U010457 >>>
<<< UNIT U010458 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/factory.py:9-9 | ctx=TestDataFactory >>>
测试数据工厂，用于快速创建数据库测试数据。
<<< END U010458 >>>
<<< UNIT U010459 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:15-15 >>>
# 语料目录属源码仓库，与 Paths.tests 同源。按本文件深度推算会在包布局调整后失准。
<<< END U010459 >>>
<<< UNIT U010460 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:26-26 >>>
# 提取域名作为可读前缀
<<< END U010460 >>>
<<< UNIT U010461 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:78-79 >>>
# text 与 json_data 对 JSON 接口而言是同一份内容的两种形态，同时写入磁盘会让
# 大响应的语料体积翻倍。此时只保留 json_data，读取时再还原出 text。
<<< END U010461 >>>
<<< UNIT U010462 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:106-108 >>>
# 默认禁止回退到真实网络，因为未录制的 URL 会带着重试与超时（默认 3 次 × 20 秒）
# 拖慢用例，并让结果随外部服务状态波动。录制新语料时以环境变量放行。
# 每次调用都重置策略，使中途停用 mock 的用例不会波及后续入口。
<<< END U010462 >>>
<<< UNIT U010463 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:112-112 >>>
# 语料在同一进程内不变。重复注册只会让比对清单随入口数量膨胀。
<<< END U010463 >>>
<<< UNIT U010464 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:132-133 >>>
# 保存时省略了与 json_data 重复的 text，此处还原，
# 以便直接读取响应正文的调用方仍能取到内容。
<<< END U010464 >>>
<<< UNIT U010465 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:143-143 >>>
# 填充 json_data 以便 fmt="json" 的请求能正确返回
<<< END U010465 >>>
<<< UNIT U010466 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:150-151 >>>
# text 不是合法 JSON（或类型不匹配）时，保持 _json 未设置。
# 调用方仍可通过 text/content 使用响应内容。
<<< END U010466 >>>
<<< UNIT U010467 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/fixtures.py:1-1 | ctx=<module> >>>
HTTP Fixture 工具 - 从本地文件加载 mock 响应数据。
<<< END U010467 >>>
<<< UNIT U010468 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/http.py:1-1 | ctx=<module> >>>
HTTP Mock 工具 - 为需要网络请求的模块提供 mock 支持。
<<< END U010468 >>>
<<< UNIT U010469 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/http.py:33-33 | ctx=MockHTTPResponse >>>
模拟 HTTP 响应。
<<< END U010469 >>>
<<< UNIT U010470 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/http.py:91-91 | ctx=HTTPMock >>>
HTTP 请求 mock 管理器。
<<< END U010470 >>>
<<< UNIT U010471 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/http.py:131-131 | ctx=HTTPMock.clear >>>
清除所有 mock。
<<< END U010471 >>>
<<< UNIT U010472 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/http.py:146-146 | ctx=HTTPMock.disable >>>
禁用 HTTP mock。
<<< END U010472 >>>
<<< UNIT U010473 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/http.py:152-152 | ctx=HTTPMock.is_enabled >>>
检查 mock 是否启用。
<<< END U010473 >>>
<<< UNIT U010474 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/loader.py:13-14 >>>
# 语言包快照在同一进程内只会构建一次，因为重建要重新哈希全部语料，是每个入口固定成本的
# 主要来源。连接仍逐次重置，用例才能从干净的翻译状态开始。
<<< END U010474 >>>
<<< UNIT U010475 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/loader.py:32-32 >>>
# 测试显式配置默认 RPC peer，与生产入口一致，避免依赖模块导入顺序。
<<< END U010475 >>>
<<< UNIT U010476 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/loader.py:69-70 >>>
# 测试不检查模块是否已启用，因此直接消费发现层的清单，与生产入口同源。刻意不使用
# load_order()，因为测试不校验跨包依赖声明，按包名字典序枚举即可，测试框架不必依赖依赖图机制。
<<< END U010476 >>>
<<< UNIT U010477 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:40-40 >>>
# 检查触发命令是否在模块列表中
<<< END U010477 >>>
<<< UNIT U010478 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:43-43 >>>
# 如果使用了前缀但未命中任何模块命令，则视为不匹配（适用于单元测试）
<<< END U010478 >>>
<<< UNIT U010479 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:46-46 >>>
# 检查正则
<<< END U010479 >>>
<<< UNIT U010480 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:51-51 >>>
# 若任何正则命中则会在 _execute_regex 中调用对应函数并抛出 SessionFinished
<<< END U010480 >>>
<<< UNIT U010481 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:53-53 >>>
# 若未命中任何正则，视为不匹配（适用于单元测试）
<<< END U010481 >>>
<<< UNIT U010482 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:59-59 >>>
# 如果上游指定了命令前缀，则使用指定的命令前缀
<<< END U010482 >>>
<<< UNIT U010483 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:64-64 >>>
# 判断是否在命令前缀列表中
<<< END U010483 >>>
<<< UNIT U010484 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:69-69 >>>
# 检查消息前缀
<<< END U010484 >>>
<<< UNIT U010485 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:70-70 >>>
# 排除 ~~xxx~~ 的情况
<<< END U010485 >>>
<<< UNIT U010486 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:72-72 >>>
# 如果在命令前缀列表中，则将此命令前缀移动到列表首位
<<< END U010486 >>>
<<< UNIT U010487 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:100-100 >>>
# 判断此命令是否匹配一个实际的模块
<<< END U010487 >>>
<<< UNIT U010488 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:130-130 >>>
# 如果没有可用的命令，则展示模块简介
<<< END U010488 >>>
<<< UNIT U010489 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:148-148 >>>
# 检查模块绑定的命令是否有模板
<<< END U010489 >>>
<<< UNIT U010490 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:152-152 >>>
# 如果有，送入命令解析
<<< END U010490 >>>
<<< UNIT U010491 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:156-156 >>>
# 如果没有，直接传入下游模块
<<< END U010491 >>>
<<< UNIT U010492 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:165-165 >>>
# 将 msg 传入下游模块
<<< END U010492 >>>
<<< UNIT U010493 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:170-170 >>>
# 遍历模块
<<< END U010493 >>>
<<< UNIT U010494 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:174-174 >>>
# 遍历正则模块的表达式
<<< END U010494 >>>
<<< UNIT U010495 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:186-186 >>>
# 如果匹配成功
<<< END U010495 >>>
<<< UNIT U010496 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:190-190 >>>
# 将 msg 传入下游模块
<<< END U010496 >>>
<<< UNIT U010497 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:199-199 >>>
# 解析模块的子功能命令
<<< END U010497 >>>
<<< UNIT U010498 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:201-201 >>>
# 使用命令模板解析后的消息
<<< END U010498 >>>
<<< UNIT U010499 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/mock/parser.py:210-210 >>>
# 将 msg 传入下游模块
<<< END U010499 >>>
<<< UNIT U010500 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/scheduler.py:1-1 | ctx=<module> >>>
计划任务 Mock 工具 - 用于测试模块的定时任务注册和执行。
<<< END U010500 >>>
<<< UNIT U010501 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/scheduler.py:99-99 | ctx=strict_http >>>
在上下文内让未录制的 HTTP 请求立即失败。
<<< END U010501 >>>
<<< UNIT U010502 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/session.py:35-35 >>>
# 记录随消息下发的按钮数据，供测试检查使用。不计入 action 以免影响数量类检查。
<<< END U010502 >>>
<<< UNIT U010503 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/session.py:306-306 >>>
# 新消息共享同一个脚本列表引用，不清空原始会话的脚本
<<< END U010503 >>>
<<< UNIT U010504 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/session.py:348-348 >>>
# 新消息共享同一个脚本列表引用，不清空原始会话的脚本
<<< END U010504 >>>
<<< UNIT U010505 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/session.py:393-393 >>>
# 新消息共享同一个脚本列表引用，不清空原始会话的脚本
<<< END U010505 >>>
<<< UNIT U010506 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/session.py:183-183 | ctx=MockMessageSession.check_native_permission >>>
测试环境不提供平台成员数据，指定成员一律按无权限处理。
<<< END U010506 >>>
<<< UNIT U010507 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/webrender.py:14-14 >>>
# 语料目录属源码仓库，与 Paths.tests 同源。按本文件深度推算会在包布局调整后失准。
<<< END U010507 >>>
<<< UNIT U010508 | py-comment | packages/akari-bot-testing/akaribot/testing/mock/webrender.py:17-18 >>>
# 1x1 透明 PNG 的 base64 文本。截图类方法返回的是 base64 字符串而非二进制，
# 调用方（如 cb64imglst）会直接对其解码，故占位值必须保持同一形态。
<<< END U010508 >>>
<<< UNIT U010509 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/webrender.py:1-1 | ctx=<module> >>>
WebRender Mock 工具 - 为依赖无头浏览器的模块提供模拟对象。
<<< END U010509 >>>
<<< UNIT U010510 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/webrender.py:46-46 | ctx=WebRenderMock >>>
web_render 数据获取方法的模拟管理器。
<<< END U010510 >>>
<<< UNIT U010511 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/webrender.py:71-71 | ctx=WebRenderMock.clear >>>
清除全部已注册语料。
<<< END U010511 >>>
<<< UNIT U010512 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/webrender.py:89-89 | ctx=WebRenderMock.enable >>>
接管 web_render 的数据获取方法。
<<< END U010512 >>>
<<< UNIT U010513 | py-docstring | packages/akari-bot-testing/akaribot/testing/mock/webrender.py:126-126 | ctx=WebRenderMock.disable >>>
恢复被接管的真实方法。
<<< END U010513 >>>
<<< UNIT U010514 | py-comment | packages/akari-bot-testing/akaribot/testing/process.py:23-24 >>>
# 无进展超时监控随测试时限系数放大，但封顶 5 倍，这样慢机器上子测试可以更久，
# 真正无响应时也不能让单个用例占用整个 CI 任务太久。
<<< END U010514 >>>
<<< UNIT U010515 | py-comment | packages/akari-bot-testing/akaribot/testing/process.py:71-72 >>>
# 集成用例会启动 queue poller、waiter 或平台任务，并与后续用例共用事件循环与内存库。
# 游离任务不得越过其捕获的数据库上下文存活。
<<< END U010515 >>>
<<< UNIT U010516 | py-comment | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:113-113 >>>
# 模块注册表与 hook 订阅是进程级状态，用例可能将其改写或关闭。
<<< END U010516 >>>
<<< UNIT U010517 | py-comment | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:128-128 >>>
# 未完成取消收尾的任务会带着已关闭的数据库上下文继续运行，后续用例不再可信。
<<< END U010517 >>>
<<< UNIT U010518 | py-comment | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:158-158 >>>
# 测试自己抛出的 TimeoutError 不是测试超时，只有本上下文到期才判定。
<<< END U010518 >>>
<<< UNIT U010519 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:30-30 | ctx=get_session_loop >>>
返回整个测试会话共用的事件循环，不存在时新建并设为当前循环。
<<< END U010519 >>>
<<< UNIT U010520 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:39-39 | ctx=run_in_session_loop >>>
在会话事件循环中执行协程并返回其结果。
<<< END U010520 >>>
<<< UNIT U010521 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:44-44 | ctx=close_session_loop >>>
关闭会话事件循环，并回收残留任务。
<<< END U010521 >>>
<<< UNIT U010522 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:76-76 | ctx=resolve_timeout >>>
获取单个测试的超时秒数，标记优先于环境变量，其次为默认值。
<<< END U010522 >>>
<<< UNIT U010523 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:106-106 | ctx=prepare_runtime >>>
重建内存数据库与模块注册表，使每个测试项都有自己的初始状态。
<<< END U010523 >>>
<<< UNIT U010524 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:148-148 | ctx=TestTimeout >>>
单个测试超过时限。
<<< END U010524 >>>
<<< UNIT U010525 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:152-152 | ctx=run_with_timeout >>>
等待测试完成，超过时限时抛出 :class:`TestTimeout` 并取消测试。
<<< END U010525 >>>
<<< UNIT U010526 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:165-165 | ctx=run_test_call >>>
在会话事件循环中执行单个测试，超时判定为测试失败。
<<< END U010526 >>>
<<< UNIT U010527 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:174-174 | ctx=PytestTester >>>
在 pytest 下运行的 Tester，子测试失败直接成为 pytest 用例失败。
<<< END U010527 >>>
<<< UNIT U010528 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:177-177 | ctx=PytestTester.test >>>
运行一个纯函数子测试，返回假值或抛出异常都判定为用例失败。
<<< END U010528 >>>
<<< UNIT U010529 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:196-196 | ctx=PytestTester.integrate >>>
运行一条命令级子测试，明确不匹配时判定为用例失败。
<<< END U010529 >>>
<<< UNIT U010530 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:204-204 | ctx=FuncCaseItem >>>
一个 ``@func_case`` 入口在 pytest 中的节点。
<<< END U010530 >>>
<<< UNIT U010531 | py-docstring | packages/akari-bot-testing/akaribot/testing/pytest_plugin.py:219-219 | ctx=pytest_pycollect_makeitem >>>
把 ``@func_case`` 入口接管为框架节点，其余函数交回 pytest 默认收集。
<<< END U010531 >>>
<<< UNIT U010532 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:23-23 >>>
# ========== 测试配置引导 ==========
<<< END U010532 >>>
<<< UNIT U010533 | py-inline-comment | packages/akari-bot-testing/akaribot/testing/runner.py:24-24 >>>
# 须与 core.constants.path.CONFIG_PATH_ENV 一致
<<< END U010533 >>>
<<< UNIT U010534 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:26-28 >>>
# union 合并日志目录，须与 core.constants.path.UNION_MERGE_LOGS_PATH_ENV 一致。
# 用例会真实走到合并流程，逐次写下的快照日志只在人工回溯真实合并时才有意义，
# 留在 data/ 里只会随每次测试运行越积越多。
<<< END U010534 >>>
<<< UNIT U010535 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:31-33 >>>
# 语言快照缓存目录。用例会导入 bot，而守护进程在导入期把该变量 setdefault 到 data/i18n_cache。
# 测试进程须先把环境变量固定为自有的临时目录，否则框架启动时发布的快照与之后的读取方（包括 spawn 出的
# 子进程）会指向不同位置。
<<< END U010535 >>>
<<< UNIT U010536 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:36-37 >>>
# 测试所需的配置覆盖项，格式为 (表名, 键名, 值)。文件名不再逐项硬编码，因为现行扁平布局下
# 一个表名恰好对应一个配置文件，映射由 CFGManager 的写入路径完成（P4.4 后由 ConfigLayout 提供）。
<<< END U010536 >>>
<<< UNIT U010537 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:40-41 >>>
# 通用测试进程不启动守护进程所管理的 WebSocket Hub。数据库后端
# 作为自包含测试环境。WebSocket 的真实连接行为由专项用例显式建立 Hub 验证。
<<< END U010537 >>>
<<< UNIT U010538 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:47-49 >>>
# 注释先以 i18n 标记写入磁盘，待 i18n 快照就绪后由配置模板扫描统一翻译。版本号取当前值，因为
# core/config/update.py 的迁移在导入期执行，低于目标版本会被逐级升级。
# 本函数须在 ``AKARI_CONFIG_PATH`` 设置之后调用，其内的 core.constants 导入会固定配置目录。
<<< END U010538 >>>
<<< UNIT U010539 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:77-78 >>>
# 日志写入仍会被完整执行，产物随进程退出一并删除。需要留存时设置 ``AKARI_UNION_MERGE_LOGS_PATH``。
# 已显式设置过的运行器（如 tests/run_one.py）直接沿用，不再新建目录。
<<< END U010539 >>>
<<< UNIT U010540 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:90-90 >>>
# 快照缓存的取值只依赖环境变量，故须先于配置引导，因为后者构建语言快照时会读取它。
<<< END U010540 >>>
<<< UNIT U010541 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:102-104 >>>
# 准备好一份测试专用配置，并令其后的导入一律指向它。
# 配置不取自仓库内的配置快照，只写入最小结构，其余键由配置模板扫描补全，
# 因此仓库里不存在需要与代码同步维护的生成配置。
<<< END U010541 >>>
<<< UNIT U010542 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:107-108 >>>
# 顺序约束上，AKARI_CONFIG_PATH 与 AKARI_UNION_MERGE_LOGS_PATH 都须先于任何 core.* 导入生效。
# 二者分别固定为配置目录与合并日志目录。未设置时都会指向真实的 config/ 与 data/。
<<< END U010542 >>>
<<< UNIT U010543 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:121-121 >>>
# i18n 快照须先接上，因为模板生成的注释取自配置文件声明的语言，未接上时全部退化为 i18n 键名。
<<< END U010543 >>>
<<< UNIT U010544 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:129-130 >>>
# 覆盖项通过配置管理器的写入路径处理，使磁盘与内存副本保持一致；直接改写文件时，
# 同一文件系统时间戳精度内的改动可能绕过 watch() 的重载判定。
<<< END U010544 >>>
<<< UNIT U010545 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:156-157 >>>
# 三项引导都必须早于本模块后续的 core.* 导入。合并日志目录与语言快照缓存在前，因为它们的取值只依赖
# 环境变量，而配置引导内部会导入 core.constants 并构建语言快照，届时未设置的变量即被永久固定。
<<< END U010545 >>>
<<< UNIT U010546 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:187-187 >>>
# 源码克隆形态下的仓库根目录由根目录兼容实现 tester.py 在导入本模块前设置，取值须与它一致。
<<< END U010546 >>>
<<< UNIT U010547 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:235-236 >>>
# 完整解析留到 :func:`run`，因为本模块也会被 ``tester.py`` 等入口以各自的 argv 导入，在导入期做
# 严格解析会让那些入口因为不相干的参数直接退出。这里只做包含判断，不认识的一律忽略。
<<< END U010547 >>>
<<< UNIT U010548 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:240-240 >>>
# 本次运行的选择项。由 run() 严格解析后覆盖。main() 里的收集与筛选都在其之后读取它。
<<< END U010548 >>>
<<< UNIT U010549 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:247-249 >>>
# 不按本文件位置反推，因为本模块已在包内，反推只会指向 site-packages。优先使用 ``AKARI_REPO_ROOT``。
# 否则使用 ``Paths.tests`` 的父目录——源码克隆下 ``tests/`` 位于仓库根目录，再以 ``packages/``
# 是否存在复核，避免 ``AKARI_TESTS_PATH`` 指向别处时误判。
<<< END U010549 >>>
<<< UNIT U010550 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:259-259 >>>
# 报告输出位置与用例发现同源，源码克隆下固定在仓库根目录，安装形态下改用调用目录。
<<< END U010550 >>>
<<< UNIT U010551 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:264-266 >>>
# 各包源码存放在 ``packages[/<类>]/<包名>``（源码根目录即包根目录，不再有 ``src`` 一层），仓库根目录本身不再有可导入的 ``akaribot``。
# 判断依据只看目录是否存在，不依赖已安装包的 metadata。仓库根目录不可知时返回空列表，此时
# ``akaribot`` 由已安装包提供，无须也不应改写 ``PYTHONPATH``。
<<< END U010551 >>>
<<< UNIT U010552 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:271-271 >>>
# 源码根目录即包根目录或包根目录下的 src 两种布局都支持。
<<< END U010552 >>>
<<< UNIT U010553 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:282-282 >>>
# 空列表时不设置，因为空字符串会引入一条指向当前目录的搜索路径，与安装形态的预期相反。
<<< END U010553 >>>
<<< UNIT U010554 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:290-290 >>>
# Coverage 集成
<<< END U010554 >>>
<<< UNIT U010555 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:318-318 >>>
# 本机只运行部分集成测试时，用路径子串筛选。
<<< END U010555 >>>
<<< UNIT U010556 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:476-477 >>>
# 仓库根目录的 ``tests/`` 承载跨包用例与共享测试数据，各成员包自带的 ``tests/`` 随包分发。后者只在
# 源码克隆下可见，仓库根目录不可知时只剩 ``Paths.tests``（可由 ``AKARI_TESTS_PATH`` 指定）。
<<< END U010556 >>>
<<< UNIT U010557 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:486-487 >>>
# 按仓库根目录相对路径生成，因为不同包里可以存在同名测试文件，仅取文件名会互相覆盖。仓库根目录不可知时
# 回退到原路径，模块名的唯一性由绝对路径本身保证。
<<< END U010557 >>>
<<< UNIT U010558 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:498-500 >>>
# 目录递归收集 ``*.py``，文件按原样收集。路径按仓库根目录解析，相对路径因此与 ``tests/run_one.py``
# 的写法一致。传入错误路径时返回空列表，由调用方报“没有匹配的测试文件”——静默运行全量会让
# ``akaribot test <路径>`` 看起来生效、实际什么都没筛。
<<< END U010558 >>>
<<< UNIT U010559 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:525-526 >>>
# 给了位置参数就只运行这些路径。否则按默认根目录收集，仓库根目录的集成用例由 _iter_integration_files
# 单独列出，其目录内的辅助模块不参与收集。两种情形都按路径排序且去重。
<<< END U010559 >>>
<<< UNIT U010560 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:772-772 >>>
# 注册表用例逐条汇报，长时间运行时不必等全部用例结束才有输出。
<<< END U010560 >>>
<<< UNIT U010561 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:837-837 >>>
# 每个入口运行完毕立即报告，长时间运行时不必等全部用例结束才有输出。
<<< END U010561 >>>
<<< UNIT U010562 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:880-880 >>>
# Coverage 报告生成
<<< END U010562 >>>
<<< UNIT U010563 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:886-886 >>>
# 生成控制台报告
<<< END U010563 >>>
<<< UNIT U010564 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:891-891 >>>
# 生成 HTML 报告
<<< END U010564 >>>
<<< UNIT U010565 | py-comment | packages/akari-bot-testing/akaribot/testing/runner.py:896-896 >>>
# 生成 XML 报告（可选，用于 CI 集成）
<<< END U010565 >>>
<<< UNIT U010566 | py-docstring | packages/akari-bot-testing/akaribot/testing/runner.py:65-65 | ctx=TestEnvironment >>>
本次测试运行实际使用的输出文件路径。
<<< END U010566 >>>
<<< UNIT U010567 | py-docstring | packages/akari-bot-testing/akaribot/testing/runner.py:139-139 | ctx=cleanup_test_environment >>>
删除本次运行创建的临时目录。由环境变量显式指定的目录保留。
<<< END U010567 >>>
<<< UNIT U010568 | py-docstring | packages/akari-bot-testing/akaribot/testing/runner.py:145-145 | ctx=prepare_test_environment >>>
返回本次测试运行的输出文件路径。环境初始化已在本模块导入期完成，重复调用返回同一份路径。
<<< END U010568 >>>
<<< UNIT U010569 | py-docstring | packages/akari-bot-testing/akaribot/testing/runner.py:460-460 | ctx=FuncTestResult >>>
单个 @func_case 测试的运行结果。
<<< END U010569 >>>
<<< UNIT U010570 | py-docstring | packages/akari-bot-testing/akaribot/testing/runner.py:912-912 | ctx=run >>>
同步入口，解析参数、运行选中的用例并返回进程退出码。
<<< END U010570 >>>
<<< UNIT U010571 | py-comment | packages/akari-bot-testing/akaribot/testing/tasks.py:11-12 >>>
# 取消后的收尾保持有界，因为后台任务可能在自己的 CancelledError 处理里继续等待，
# 无限等待会让无响应的用例阻塞整个进程。
<<< END U010571 >>>
<<< UNIT U010572 | py-comment | packages/akari-bot-testing/akaribot/testing/tasks.py:15-15 >>>
# 无进展超时监控自身的等待任务，取消收尾时不能算作用例遗留的后台任务。
<<< END U010572 >>>
<<< UNIT U010573 | py-docstring | packages/akari-bot-testing/akaribot/testing/tasks.py:20-20 | ctx=consume_task_result >>>
取走任务的异常，避免未回收的异常在解释器退出时报错。
<<< END U010573 >>>
<<< UNIT U010574 | py-docstring | packages/akari-bot-testing/akaribot/testing/tasks.py:30-30 | ctx=cancel_task >>>
取消单个任务，返回它是否在时限内完成收尾。
<<< END U010574 >>>
<<< UNIT U010575 | py-docstring | packages/akari-bot-testing/akaribot/testing/tasks.py:45-45 | ctx=current_tasks >>>
当前未完成的任务集合。
<<< END U010575 >>>
<<< UNIT U010576 | py-docstring | packages/akari-bot-testing/akaribot/testing/tasks.py:50-50 | ctx=cancel_orphan_tasks >>>
取消 baseline 之外的任务，返回它们是否全部在时限内完成收尾。
<<< END U010576 >>>
<<< UNIT U010577 | py-comment | packages/akari-bot-testing/akaribot/testing/tester.py:49-49 >>>
# Predicate 等可调用对象没有 __name__，回退到其类名
<<< END U010577 >>>
<<< UNIT U010578 | py-docstring | packages/akari-bot-testing/akaribot/testing/tester.py:34-34 | ctx=Tester.mock_config >>>
返回临时覆盖配置项的上下文管理器，用法与 :class:`core.tester.mock_config` 相同。
<<< END U010578 >>>
<<< UNIT U010579 | py-docstring | packages/akari-bot-testing/akaribot/testing/tester.py:42-48 | ctx=Tester.test >>>
运行纯函数测试，不需要命令占位符。

:param func: 测试函数或 Predicate，返回 True 表示通过，False 表示失败。
:param note: 额外说明。
:returns: 测试结果字典。
<<< END U010579 >>>
<<< UNIT U010580 | py-docstring | packages/akari-bot-testing/akaribot/testing/tester.py:110-117 | ctx=Tester.integrate >>>
注册一个交互测试案例。

:param input_: 预期输入。
:param expected: 预期输出，传入期望匹配器，若为 None 则手动复核。
:param note: 额外说明。
:param timeout: 超时时间（秒），若为 None 则无超时限制。
<<< END U010580 >>>
<<< UNIT U010581 | py-docstring | packages/akari-bot-testing/akaribot/testing/timing.py:1-1 | ctx=<module> >>>
测试时限的伸缩系数。
<<< END U010581 >>>
<<< UNIT U010582 | py-comment | packages/akari-bot-testing/tests/test_expectations.py:72-72 >>>
# 两种拼写均覆盖真值表，防止恒真、恒假或只检查第一个条件。
<<< END U010582 >>>
<<< UNIT U010583 | py-docstring | packages/akari-bot-testing/tests/test_expectations.py:1-1 | ctx=<module> >>>
直接验证匹配器的正反例。命令执行由 integration 用例覆盖。
<<< END U010583 >>>
<<< UNIT U010584 | py-docstring | packages/akari-bot-testing/tests/test_expectations.py:92-92 | ctx=test_expectations >>>
Expectation 的文本、空输出、异常、自定义检查与组合条件测试。
<<< END U010584 >>>
<<< UNIT U010585 | py-docstring | packages/akari-bot-testing/tests/test_runner_options.py:128-128 | ctx=test_testing_options >>>
akaribot.testing.runner: 命令行选项与筛选测试
<<< END U010585 >>>
<<< UNIT U010586 | py-comment | packages/akari-bot-testing/tests/test_tester_framework.py:21-21 >>>
# request_url 支持以 fmt 指定返回形式，mock 响应必须覆盖代码库中实际用到的全部取值。
<<< END U010586 >>>
<<< UNIT U010587 | py-comment | packages/akari-bot-testing/tests/test_tester_framework.py:464-464 >>>
# 写入本身仍须发生，只是放在隔离目录中。若日志改为空操作，泄漏检查会假通过。
<<< END U010587 >>>
<<< UNIT U010588 | py-comment | packages/akari-bot-testing/tests/test_tester_framework.py:484-484 >>>
# 快照只构建一次，但每个入口仍要重置翻译连接的状态。
<<< END U010588 >>>
<<< UNIT U010589 | py-docstring | packages/akari-bot-testing/tests/test_tester_framework.py:1-1 | ctx=<module> >>>
测试框架自身的单元测试。
<<< END U010589 >>>
<<< UNIT U010590 | py-docstring | packages/akari-bot-testing/tests/test_tester_framework.py:648-648 | ctx=test_tester_framework >>>
akaribot.core.tester: 测试框架自身一致性测试
<<< END U010590 >>>
<<< UNIT U010591 | md-paragraph | packages/modules/akari-bot-module-ai/README.md:3-3 | ctx=akari-bot-module-ai >>>
调用大语言模型完成多轮对话、网页检索与图片生成。
<<< END U010591 >>>
<<< UNIT U010592 | md-heading | packages/modules/akari-bot-module-ai/README.md:5-5 | ctx=安装 >>>
## 安装
<<< END U010592 >>>
<<< UNIT U010593 | md-paragraph | packages/modules/akari-bot-module-ai/README.md:7-7 | ctx=安装 >>>
Python 版本要求见包内 `pyproject.toml` 的 `requires-python`。
<<< END U010593 >>>
<<< UNIT U010594 | md-paragraph | packages/modules/akari-bot-module-ai/README.md:13-13 | ctx=安装 >>>
模块的启用与配置参见 [项目文档](https://github.com/Teahouse-Studios/akari-bot/blob/master/README.md)。
<<< END U010594 >>>
<<< UNIT U010595 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:1-1 >>>
在使用本模块前，请确保在实例目录下的 `data/module/ai/` 目录中创建 `llm_api_list.yaml` 配置文件，否则模块将无法正常运行。实例目录由环境变量 `AKARI_INSTANCE_DIR` 指定，未设置时使用进程的当前工作目录。如需启用图片生成与编辑，再创建 `image_api.yaml`。
<<< END U010595 >>>
<<< UNIT U010596 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:5-5 | ctx=`llm_api_list.yaml` 文件结构 >>>
## `llm_api_list.yaml` 文件结构
<<< END U010596 >>>
<<< UNIT U010597 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:7-7 | ctx=`llm_api_list.yaml` 文件结构 >>>
该 YAML 文件应包含一个 `llm_api_list` 数组，每个元素表示一个大语言模型 API 配置。
<<< END U010597 >>>
<<< UNIT U010598 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:9-9 | ctx=基础配置示例 >>>
### 基础配置示例
<<< END U010598 >>>
<<< UNIT U010599 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:11-11 | ctx=基础配置示例 >>>
仅按 Token 数量计费的模型，价格字段直接写在模型配置的顶层。
<<< END U010599 >>>
<<< UNIT U010600 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:27-27 | ctx=计费配置示例 >>>
### 计费配置示例
<<< END U010600 >>>
<<< UNIT U010601 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:29-29 | ctx=计费配置示例 >>>
按次计费、混合计费、阶梯计费或峰谷计费的模型，价格字段写在 `billing` 中。
<<< END U010601 >>>
<<< UNIT U010602 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:67-67 | ctx=参数说明 >>>
## 参数说明
<<< END U010602 >>>
<<< UNIT U010603 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:69-69 | ctx=基础参数 >>>
### 基础参数
<<< END U010603 >>>
<<< UNIT U010604 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:71-74 | ctx=基础参数 >>>
* `api_key`：大语言模型 API 的 API Key。
* `api_url`：大语言模型 API 的 URL。
* `model_name`：大语言模型的名称。
* `endpoint`：大语言模型 API 的类型，支持以下取值：
<<< END U010604 >>>
<<< UNIT U010605 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:76-80 | ctx=基础参数 >>>
  * `openai`（默认）：OpenAI Chat Completions API。
  * `openai-response`：OpenAI Responses API。
  * `anthropic`：Anthropic Messages API。
  * `gemini`：Gemini GenerateContent API。
  * `gemini-interaction`：Gemini Interactions API。
<<< END U010605 >>>
<<< UNIT U010606 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:82-82 | ctx=可选参数 >>>
### 可选参数
<<< END U010606 >>>
<<< UNIT U010607 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:84-84 | ctx=可选参数 >>>
* `name`：向用户展示的名称。
<<< END U010607 >>>
<<< UNIT U010608 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:86-87 | ctx=可选参数 >>>
  * 如果留空，默认与 `model_name` 相同。
  * 若多个配置的 `name` 相同，则这些配置都不会被载入。
<<< END U010608 >>>
<<< UNIT U010609 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:89-89 | ctx=可选参数 >>>
* `superuser`：是否仅限超级用户使用。
<<< END U010609 >>>
<<< UNIT U010610 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:91-92 | ctx=可选参数 >>>
  * `true`：仅限超级用户使用。
  * `false` 或 `null`：无须权限。
<<< END U010610 >>>
<<< UNIT U010611 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:94-94 | ctx=生成参数 >>>
### 生成参数
<<< END U010611 >>>
<<< UNIT U010612 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:96-96 | ctx=生成参数 >>>
以下参数用于覆盖模块配置中的同名默认值，未设置时沿用模块配置：
<<< END U010612 >>>
<<< UNIT U010613 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:98-101 | ctx=生成参数 >>>
* `temperature`：模型的温度采样。
* `top_p`：模型的核采样。
* `top_logprobs`：模型返回对数概率的候选 Token 数量，范围 0 到 20。
* `reasoning_effort`：模型的思考强度，若为 `none` 则不启用思维链。
<<< END U010613 >>>
<<< UNIT U010614 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:103-103 | ctx=生成参数 >>>
`temperature`、`top_p` 与 `top_logprobs` 可显式设为 `null`，表示不向模型传入该参数，适用于不支持相应参数的模型。
<<< END U010614 >>>
<<< UNIT U010615 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:126-126 | ctx=计费配置 >>>
## 计费配置
<<< END U010615 >>>
<<< UNIT U010616 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:128-128 | ctx=计费配置 >>>
`billing` 指定模型的计费方式：
<<< END U010616 >>>
<<< UNIT U010617 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:135-135 | ctx=计费配置 >>>
`type` 支持以下三种值：
<<< END U010617 >>>
<<< UNIT U010618 | md-table | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:137-141 | ctx=计费配置 >>>
| 类型         | 说明              |
| ---------- | --------------- |
| `token`    | 按 Token 数量计费    |
| `per_call` | 按 API 调用次数计费    |
| `hybrid`   | Token 计费 + 按次计费 |
<<< END U010618 >>>
<<< UNIT U010619 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:145-145 | ctx=`token` >>>
`token` 为默认的 Token 计费模式。
<<< END U010619 >>>
<<< UNIT U010620 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:156-156 | ctx=`token` >>>
该模式按照输入 Token、缓存命中 Token 和输出 Token 分别计算费用。
<<< END U010620 >>>
<<< UNIT U010621 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:160-160 | ctx=`per_call` >>>
`per_call` 按 API 调用次数收取固定费用。
<<< END U010621 >>>
<<< UNIT U010622 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:168-168 | ctx=`per_call` >>>
每次调用扣除 `call_price` 个花瓣。
<<< END U010622 >>>
<<< UNIT U010623 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:172-172 | ctx=`hybrid` >>>
`hybrid` 同时启用按次计费和 Token 计费。
<<< END U010623 >>>
<<< UNIT U010624 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:184-184 | ctx=`hybrid` >>>
每次 API 调用的最终费用由固定调用费用和 Token 使用费用共同组成。
<<< END U010624 >>>
<<< UNIT U010625 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:188-188 | ctx=Token 价格参数 >>>
## Token 价格参数
<<< END U010625 >>>
<<< UNIT U010626 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:190-190 | ctx=Token 价格参数 >>>
以下参数的单位均为 **花瓣 / 1M token**：
<<< END U010626 >>>
<<< UNIT U010627 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:192-195 | ctx=Token 价格参数 >>>
* `price_in`：百万输入 Token 所需的花瓣数量。
* `price_cache_read`：百万输入缓存命中 Token 所需的花瓣数量。
* `price_cache_write`：百万输入缓存写入 Token 所需的花瓣数量。
* `price_out`：百万输出 Token 所需的花瓣数量。
<<< END U010627 >>>
<<< UNIT U010628 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:197-197 | ctx=Token 价格参数 >>>
`price_cache` 是 `price_cache_read` 的别名。缓存写入价格只在模型 API 返回缓存写入 Token 数量时生效。
<<< END U010628 >>>
<<< UNIT U010629 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:199-199 | ctx=Token 价格参数 >>>
如果未设置，默认值为 `0`。
<<< END U010629 >>>
<<< UNIT U010630 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:203-203 | ctx=按次计费参数 >>>
## 按次计费参数
<<< END U010630 >>>
<<< UNIT U010631 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:207-207 | ctx=`call_price` >>>
`call_price` 表示每次 API 调用固定扣除的花瓣数量。
<<< END U010631 >>>
<<< UNIT U010632 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:215-215 | ctx=`call_price` >>>
在 `hybrid` 模式下，`call_price` 与 Token 费用同时计算：
<<< END U010632 >>>
<<< UNIT U010633 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:229-229 | ctx=阶梯计费 >>>
## 阶梯计费
<<< END U010633 >>>
<<< UNIT U010634 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:231-231 | ctx=阶梯计费 >>>
`tiers` 按上下文长度设置不同的 Token 单价。
<<< END U010634 >>>
<<< UNIT U010635 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:244-244 | ctx=`context_threshold` >>>
`context_threshold` 表示上下文长度阈值，单位为 Token。
<<< END U010635 >>>
<<< UNIT U010636 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:246-246 | ctx=`context_threshold` >>>
例如：
<<< END U010636 >>>
<<< UNIT U010637 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:252-252 | ctx=`context_threshold` >>>
表示超过 128K Token 后适用该阶梯价格。
<<< END U010637 >>>
<<< UNIT U010638 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:254-254 | ctx=`context_threshold` >>>
阶梯规则中的：
<<< END U010638 >>>
<<< UNIT U010639 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:260-260 | ctx=`context_threshold` >>>
分别覆盖该阶梯对应的输入、缓存输入和输出 Token 单价。
<<< END U010639 >>>
<<< UNIT U010640 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:262-262 | ctx=`context_threshold` >>>
如果某个价格未设置，则使用基础价格。
<<< END U010640 >>>
<<< UNIT U010641 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:266-266 | ctx=峰谷/时段计费 >>>
## 峰谷/时段计费
<<< END U010641 >>>
<<< UNIT U010642 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:268-268 | ctx=峰谷/时段计费 >>>
`time_rules` 按 UTC 时间与星期设置不同的 Token 单价。
<<< END U010642 >>>
<<< UNIT U010643 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:282-282 | ctx=`time_range` >>>
`time_range` 表示适用的时间范围，使用 UTC 时间。
<<< END U010643 >>>
<<< UNIT U010644 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:284-284 | ctx=`time_range` >>>
例如：
<<< END U010644 >>>
<<< UNIT U010645 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:290-290 | ctx=`time_range` >>>
表示服务器时间 00:00 至 08:30 期间使用该价格。
<<< END U010645 >>>
<<< UNIT U010646 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:294-294 | ctx=`week` >>>
`week` 用于指定适用的星期。
<<< END U010646 >>>
<<< UNIT U010647 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:300-300 | ctx=`week` >>>
其中：
<<< END U010647 >>>
<<< UNIT U010648 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:302-308 | ctx=`week` >>>
* `1`：星期一
* `2`：星期二
* `3`：星期三
* `4`：星期四
* `5`：星期五
* `6`：星期六
* `7`：星期日
<<< END U010648 >>>
<<< UNIT U010649 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:312-312 | ctx=阶梯计费与峰谷计费的冲突规则 >>>
## 阶梯计费与峰谷计费的冲突规则
<<< END U010649 >>>
<<< UNIT U010650 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:314-314 | ctx=阶梯计费与峰谷计费的冲突规则 >>>
`tiers` 和 `time_rules` **不能同时生效**。
<<< END U010650 >>>
<<< UNIT U010651 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:316-316 | ctx=阶梯计费与峰谷计费的冲突规则 >>>
如果同一个模型同时配置了 `tiers` 和 `time_rules`，则 `tiers` 和 `time_rules` **均不生效**，不按优先级择一，也不叠加价格。
<<< END U010651 >>>
<<< UNIT U010652 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:318-318 | ctx=阶梯计费与峰谷计费的冲突规则 >>>
因此，如果需要使用阶梯计费，请不要同时配置 `time_rules`。如果需要使用峰谷计费，请不要同时配置 `tiers`。
<<< END U010652 >>>
<<< UNIT U010653 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:322-322 | ctx=顶层价格字段 >>>
## 顶层价格字段
<<< END U010653 >>>
<<< UNIT U010654 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:324-324 | ctx=顶层价格字段 >>>
价格字段也可直接写在模型配置的顶层：
<<< END U010654 >>>
<<< UNIT U010655 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:332-332 | ctx=顶层价格字段 >>>
例如：
<<< END U010655 >>>
<<< UNIT U010656 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:346-346 | ctx=顶层价格字段 >>>
该方式等价于基础的 Token 计费配置：
<<< END U010656 >>>
<<< UNIT U010657 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:357-357 | ctx=顶层价格字段 >>>
`billing` 结构支持全部计费方式与计费规则。
<<< END U010657 >>>
<<< UNIT U010658 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:361-361 | ctx=`price` 参数的计算 >>>
## `price` 参数的计算
<<< END U010658 >>>
<<< UNIT U010659 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:363-363 | ctx=`price` 参数的计算 >>>
`price` 参数按服务商实际定价换算，比例为 **1 花瓣 = ¥0.01**。
<<< END U010659 >>>
<<< UNIT U010660 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:365-365 | ctx=`price` 参数的计算 >>>
例如 `deepseek-v4-pro` 模型的价格如下：
<<< END U010660 >>>
<<< UNIT U010661 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:367-369 | ctx=`price` 参数的计算 >>>
* **输入：¥9 / 1M token**
* **缓存输入：¥0.3 / 1M token**
* **输出：¥27 / 1M token**
<<< END U010661 >>>
<<< UNIT U010662 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:371-371 | ctx=`price` 参数的计算 >>>
计算方法：
<<< END U010662 >>>
<<< UNIT U010663 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:373-375 | ctx=`price` 参数的计算 >>>
* **输入成本：** ¥9 / 1M token = 900 花瓣 / 1M token
* **缓存成本：** ¥0.3 / 1M token = 30 花瓣 / 1M token
* **输出成本：** ¥27 / 1M token = 2700 花瓣 / 1M token
<<< END U010663 >>>
<<< UNIT U010664 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:377-377 | ctx=`price` 参数的计算 >>>
据此设置：
<<< END U010664 >>>
<<< UNIT U010665 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:387-387 | ctx=`price` 参数的计算 >>>
请按实际用量与服务商定价设置 `price`，以控制成本。
<<< END U010665 >>>
<<< UNIT U010666 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:391-391 | ctx=图片生成与编辑 >>>
## 图片生成与编辑
<<< END U010666 >>>
<<< UNIT U010667 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:393-393 | ctx=图片生成与编辑 >>>
`image_api.yaml` 与 `llm_api_list.yaml` 一样放在实例目录下的 `data/module/ai/` 目录中。当配置存在且 `model_name` 非空时，模型会获得 `generate_image` 与 `edit_image` 工具。
<<< END U010667 >>>
<<< UNIT U010668 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/README.md:408-410 | ctx=图片生成与编辑 >>>
* `base_url`、`api_key` 留空时沿用当前对话模型的地址与密钥。
* `costs` 以调用费用为单位，取固定数值或按参数查找的对照表。查找顺序为 `尺寸:品质` → 品质 → 尺寸 → `default` → `auto` → 第一个数值。
* 修改配置后需重启机器人或重载 `ai` 模块。
<<< END U010668 >>>
<<< UNIT U010669 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/__init__.py:74-74 >>>
# OpenAI、Matplotlib、网页提取等依赖体积较大，仅在实际调用 AI 时加载。
<<< END U010669 >>>
<<< UNIT U010670 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/__init__.py:91-91 >>>
# 每轮建立新的快照，保留旧 ID 以支持从任意一轮分叉。
<<< END U010670 >>>
<<< UNIT U010671 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/__init__.py:181-181 >>>
# 续接上下文时沿用其原本使用的模型。该模型当前不可用时改用默认模型。
<<< END U010671 >>>
<<< UNIT U010672 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/__init__.py:196-196 >>>
# 多轮对话会跨越多次平台消息处理，保持根会话上下文直到整段对话结束。
<<< END U010672 >>>
<<< UNIT U010673 | py-inline-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/context.py:5-5 >>>
# 上下文窗口有效期（秒）
<<< END U010673 >>>
<<< UNIT U010674 | py-docstring | packages/modules/akari-bot-module-ai/akaribot/modules/ai/context.py:26-26 | ctx=create_context >>>
创建绑定场景的上下文快照，返回其 ID。
<<< END U010674 >>>
<<< UNIT U010675 | py-docstring | packages/modules/akari-bot-module-ai/akaribot/modules/ai/context.py:38-38 | ctx=get_context >>>
获取同一场景的上下文历史。不存在、跨场景或已过期返回 None。
<<< END U010675 >>>
<<< UNIT U010676 | py-docstring | packages/modules/akari-bot-module-ai/akaribot/modules/ai/context.py:47-47 | ctx=get_context_llm >>>
获取上下文快照使用的模型名称。不存在、跨场景或已过期返回 None。
<<< END U010676 >>>
<<< UNIT U010677 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:5-5 | ctx=ai：安装与开发 >>>
# ai：安装与开发
<<< END U010677 >>>
<<< UNIT U010678 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:7-7 | ctx=安装 >>>
## 安装
<<< END U010678 >>>
<<< UNIT U010679 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:13-13 | ctx=安装 >>>
安装后，管理员需要在会话中执行 `module enable ai` 开启模块。
<<< END U010679 >>>
<<< UNIT U010680 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:15-15 | ctx=配置项 >>>
## 配置项
<<< END U010680 >>>
<<< UNIT U010681 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:19-19 | ctx=配置项 >>>
`e2b_api_key` 声明为敏感项，写入同一配置文件中的 `module_ai_secret` 表。
<<< END U010681 >>>
<<< UNIT U010682 | md-table | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:21-33 | ctx=配置项 >>>
| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ai_default_llm` | str | 空 | 默认使用的大语言模型，须出现在模型清单中 |
| `llm_timeout` | float | 60 | 请求超时时间（秒） |
| `llm_max_tokens` | int | 2048 | 单次回复的最大 Token 数 |
| `llm_temperature` | float | 1.0 | 温度采样，范围 0 到 2 |
| `llm_top_p` | float | 1.0 | 核采样，范围 0 到 1 |
| `llm_frequency_penalty` | float | 0.0 | 频率惩罚，范围 -2 到 2 |
| `llm_presence_penalty` | float | 0.0 | 存在惩罚，范围 -2 到 2 |
| `llm_max_calling_iteration` | int | 5 | 工具调用的最大迭代次数 |
| `ai_cost_to_petal` | float | 1.0 | 花瓣与调用费用的比率 |
| `llm_top_logprobs` | int | -1 | 候选 Token 对数概率数量，负数不传入 |
| `e2b_api_key`（`module_ai_secret`） | str | 空 | E2B 沙箱密钥，未填写时代码执行工具不注册 |
<<< END U010682 >>>
<<< UNIT U010683 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:35-35 | ctx=配置项 >>>
完整清单见配置模板 `akaribot/modules/ai/config.py`。模型清单放在实例数据目录 `data/module/ai/` 下：
<<< END U010683 >>>
<<< UNIT U010684 | md-table | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:37-41 | ctx=配置项 >>>
| 文件 | 内容 |
| --- | --- |
| `llm_api_list.yaml` | `llm_api_list` 列表，每项含 `name`、`model_name`、`api_url`、`api_key`，可选 `endpoint`（`openai`、`openai-response`、`anthropic`、`gemini`、`gemini-interaction`）、`superuser`、`price_in`、`price_out`、`price_cache_read`、`price_cache_write`、`billing` 与采样参数 |
| `image_api.yaml` | `image_api` 段含 `model_name`、`base_url`、`api_key` 与 `costs`，缺少 `model_name` 时图像工具不注册 |
| `instructions.txt`、`persona.txt` | 覆盖包内默认的系统提示与人格提示 |
<<< END U010684 >>>
<<< UNIT U010685 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:43-43 | ctx=权限与平台能力 >>>
## 权限与平台能力
<<< END U010685 >>>
<<< UNIT U010686 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:45-45 | ctx=权限与平台能力 >>>
命令对平台没有限制。会话是否支持引用回复，决定对话是逐条等待还是连续发送。
<<< END U010686 >>>
<<< UNIT U010687 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:47-47 | ctx=权限与平台能力 >>>
网页抓取工具依赖 WebRender（`webrender.enable`），搜索工具使用 ddgs。花瓣计费仅在 core 开启花瓣系统时生效，余额不足时，调用会在发出前终止。会话级设置写入 Union 数据，包括会话默认模型 `ai_default_llm`、个人开关 `ai_enable_persona` 与 `ai_custom_instructions`。
<<< END U010687 >>>
<<< UNIT U010688 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:49-49 | ctx=数据表 >>>
## 数据表
<<< END U010688 >>>
<<< UNIT U010689 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:53-53 | ctx=数据表 >>>
会话设置保存在 core 的 Union 数据中。对话上下文是进程内缓存，服务重启即失效。
<<< END U010689 >>>
<<< UNIT U010690 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:55-55 | ctx=依赖与外部服务 >>>
## 依赖与外部服务
<<< END U010690 >>>
<<< UNIT U010691 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:57-57 | ctx=依赖与外部服务 >>>
依赖 `openai`、`anthropic`、`google-genai`、`e2b-code-interpreter`、`ddgs`、`trafilatura`、`matplotlib`、`Pillow`、`pyyaml`、`orjson`、`filetype`、`akari-bot-html2text` 与 `akari-bot-core`。
<<< END U010691 >>>
<<< UNIT U010692 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:59-59 | ctx=依赖与外部服务 >>>
外部服务包括 YAML 清单指定的模型接口、E2B 代码沙箱、ddgs 搜索与 WebRender。
<<< END U010692 >>>
<<< UNIT U010693 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/development.md:61-61 | ctx=依赖与外部服务 >>>
模块提供 Hook `ai.ask`，其他模块可以用它发起一次对话，此 Hook 没有超时限制。参数包括 `prompt`、`instructions`、`llm` 与 `use_tools`，返回 `status`、`text`、`chain`、`petal`、`llm`。
<<< END U010693 >>>
<<< UNIT U010694 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:3-3 | ctx=ai >>>
此模块可以调用大语言模型完成多轮对话、网页检索与图片生成，调用费用按模型单价折算成花瓣后扣除。可用的模型与图像服务由管理员配置，未配置模型时返回配置提示。
<<< END U010694 >>>
<<< UNIT U010695 | md-heading | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:5-5 | ctx=命令 >>>
## 命令
<<< END U010695 >>>
<<< UNIT U010696 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:11-11 | ctx=`ai` >>>
此命令用于与大语言模型聊天。省略提问时，机器人等待下一条消息作为提问。
<<< END U010696 >>>
<<< UNIT U010697 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:13-13 | ctx=`ai` >>>
说明：
<<< END U010697 >>>
<<< UNIT U010698 | md-list | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:15-16 | ctx=`ai` >>>
- 每条回复末尾附带轮次 ID 与续接命令，上下文窗口有效期为 1000 秒。
- 非超级用户两次调用间隔不少于 10 秒。超级用户不扣花瓣，也不受冷却限制。
<<< END U010698 >>>
<<< UNIT U010699 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:22-22 | ctx=`ai llm list` >>>
此命令用于查看支持的大语言模型列表。
<<< END U010699 >>>
<<< UNIT U010700 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:28-28 | ctx=`ai llm price` >>>
此命令用于查看指定大语言模型的花瓣价格。
<<< END U010700 >>>
<<< UNIT U010701 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:34-34 | ctx=`ai llm set` >>>
此命令用于设置当前场景默认的大语言模型。
<<< END U010701 >>>
<<< UNIT U010702 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:40-40 | ctx=`ai llm instruct` >>>
此命令用于设置大语言模型的自定义命令。省略参数时清除已设置的内容。
<<< END U010702 >>>
<<< UNIT U010703 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:43-49 | ctx=`ai llm instruct` >>>
  :log="[
    '用户：~ai llm instruct 用简体中文回答',
    '机器人：已设置自定义命令。',
    '用户：~ai llm instruct',
    '机器人：已清除自定义命令。',
  ]"
/>
<<< END U010703 >>>
<<< UNIT U010704 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:55-55 | ctx=`ai llm persona` >>>
此命令用于设置是否开启人格化，效果因模型而异。
<<< END U010704 >>>
<<< UNIT U010705 | md-paragraph | packages/modules/akari-bot-module-ai/akaribot/modules/ai/docs/index.md:58-62 | ctx=`ai llm persona` >>>
  :log="[
    '用户：~ai llm persona',
    '机器人：已开启人格化。',
  ]"
/>
<<< END U010705 >>>
<<< UNIT U010706 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/anthropic.py:55-55 >>>
# Anthropic 要求 user/assistant 交替。工具结果之后的图片等补充消息需并入同一轮。
<<< END U010706 >>>
<<< UNIT U010707 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/anthropic.py:63-63 >>>
# 启用思考时 Anthropic 要求原样回传上一轮的 thinking 块，否则工具续轮报错。
<<< END U010707 >>>
<<< UNIT U010708 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/anthropic.py:82-82 >>>
# anthropic 要求 user/assistant 交替，多个并行 tool_result 需合并到同一个 user 消息。
<<< END U010708 >>>
<<< UNIT U010709 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/anthropic.py:96-96 >>>
# Anthropic 仅接受 low/medium/high/xhigh/max，OpenAI 的 none/minimal 需剔除。
<<< END U010709 >>>
<<< UNIT U010710 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/anthropic.py:110-110 >>>
# anthropic 的 tool_choice 需为 {"type": "auto"/"none"/"any"/"tool"} 结构，而非字符串。
<<< END U010710 >>>
<<< UNIT U010711 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/base.py:39-39 >>>
# SDK 拒绝空密钥，不校验鉴权的自建代理会忽略该请求头。
<<< END U010711 >>>
<<< UNIT U010712 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/base.py:67-67 >>>
# 超时沿用 httpx 异常，以便落入 RETRYABLE_EXCEPTIONS。
<<< END U010712 >>>
<<< UNIT U010713 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/base.py:87-87 >>>
# 显式 null 或负数均表示不请求对数概率。
<<< END U010713 >>>
<<< UNIT U010714 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/base.py:108-108 >>>
# 只有混合思考模式的千问模型接受 enable_thinking，其他千问模型传入该参数会报错。
<<< END U010714 >>>
<<< UNIT U010715 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/base.py:129-129 >>>
# 超时 / 限流等可重试异常，统一在 llm.py 中转为 ExternalException。
<<< END U010715 >>>
<<< UNIT U010716 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/base.py:156-156 >>>
# 始终以 OpenAI Chat Completions 格式存储，用于历史上下文。
<<< END U010716 >>>
<<< UNIT U010717 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/base.py:179-179 >>>
# DeepSeek 思考模式下，工具调用轮次必须保留 reasoning_content，缺失时补空字符串。
<<< END U010717 >>>
<<< UNIT U010718 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/completions.py:11-11 >>>
# 历史消息会带有其他端点的内部键（如 _anthropic_blocks、_responses_reasoning），转发前需剔除。
<<< END U010718 >>>
<<< UNIT U010719 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/completions.py:43-43 >>>
# Chat Completions 需同时开启 logprobs 才会返回对数概率。
<<< END U010719 >>>
<<< UNIT U010720 | py-inline-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/completions.py:49-49 >>>
# 兼容 DeepSeek
<<< END U010720 >>>
<<< UNIT U010721 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_generate_content.py:59-59 >>>
# 签名由生成它的模型签发，跨模型回放会被判定为无效签名。
<<< END U010721 >>>
<<< UNIT U010722 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_generate_content.py:82-82 >>>
# generateContent 要求 user/model 交替，工具结果后的图片消息需并入同一轮。
<<< END U010722 >>>
<<< UNIT U010723 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_generate_content.py:91-91 >>>
# 模型产生的 thoughtSignature 与函数调用步骤需原样回传。
<<< END U010723 >>>
<<< UNIT U010724 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_generate_content.py:102-102 >>>
# 没有可回传的签名时无法续接函数调用，连同其结果一并舍弃。
<<< END U010724 >>>
<<< UNIT U010725 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_generate_content.py:149-149 >>>
# Gemini 3 与 2.5 Pro 无法关闭思考，省略配置以使用模型默认行为。
<<< END U010725 >>>
<<< UNIT U010726 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_generate_content.py:226-226 >>>
# 服务端判定签名失效时，改用不含签名与工具轮次的上下文重试一次。
<<< END U010726 >>>
<<< UNIT U010727 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_generate_content.py:251-251 >>>
# 思考 token 单独计入用量，按输出计费。
<<< END U010727 >>>
<<< UNIT U010728 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_interactions.py:52-52 >>>
# 签名由生成它的模型签发，跨模型回放会被判定为无效签名，此时仅保留无签名的步骤。
<<< END U010728 >>>
<<< UNIT U010729 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_interactions.py:74-74 >>>
# 工具产出的图片会作为用户消息追加，Interactions 支持直接并入工具结果。
<<< END U010729 >>>
<<< UNIT U010730 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_interactions.py:80-80 >>>
# 无状态续轮需原样回传 thought 签名与函数调用步骤。
<<< END U010730 >>>
<<< UNIT U010731 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_interactions.py:131-131 >>>
# 未识别的步骤类型需按原始载荷回传，序列化结果只有 UNKNOWN 占位。
<<< END U010731 >>>
<<< UNIT U010732 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_interactions.py:177-177 >>>
# 服务端判定签名失效时，改用不含 thought 步骤的上下文重试一次。
<<< END U010732 >>>
<<< UNIT U010733 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_interactions.py:236-236 >>>
# 无状态续轮依赖原样回传 thought 与 function_call 步骤。
<<< END U010733 >>>
<<< UNIT U010734 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/gemini_interactions.py:245-245 >>>
# 思考 token 单独计入用量，按输出计费。
<<< END U010734 >>>
<<< UNIT U010735 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/responses.py:50-50 >>>
# 手动管理上下文时，Responses API 要求回传上一轮的 reasoning 条目，否则续轮丢失思维链。
<<< END U010735 >>>
<<< UNIT U010736 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/responses.py:95-95 >>>
# Responses 需通过 include 声明才会返回对数概率。
<<< END U010736 >>>
<<< UNIT U010737 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/endpoints/responses.py:149-149 >>>
# Responses API 无状态续轮依赖原样回传 reasoning 条目（含 encrypted_content）。
<<< END U010737 >>>
<<< UNIT U010738 | py-inline-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/formatting.py:11-11 >>>
# 代码块
<<< END U010738 >>>
<<< UNIT U010739 | py-inline-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/formatting.py:12-12 >>>
# 块级 LaTeX
<<< END U010739 >>>
<<< UNIT U010740 | py-inline-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/formatting.py:13-13 >>>
# Markdown 表格
<<< END U010740 >>>
<<< UNIT U010741 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/formatting.py:14-14 >>>
# 先分块
<<< END U010741 >>>
<<< UNIT U010742 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/hook.py:90-90 >>>
# OpenAI、Matplotlib、网页提取等依赖体积较大，仅在实际调用 AI 时加载。
<<< END U010742 >>>
<<< UNIT U010743 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/hook.py:93-93 >>>
# hook 上下文只带 SessionInfo，而模型调用与出站格式化都需要消息会话。
<<< END U010743 >>>
<<< UNIT U010744 | py-docstring | packages/modules/akari-bot-module-ai/akaribot/modules/ai/hook.py:1-1 | ctx=<module> >>>
ai.ask 带名称的 hook - 供其他模块调用 AI 对话能力。
<<< END U010744 >>>
<<< UNIT U010745 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/llm.py:97-97 >>>
# 延续上下文时，历史对话（不含 system 消息）会被拼接到本次请求之前。
<<< END U010745 >>>
<<< UNIT U010746 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/llm.py:105-105 >>>
# 动态上下文放最后，节省 Token 费用
<<< END U010746 >>>
<<< UNIT U010747 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/llm.py:204-205 >>>
# 仅保留对话部分（去掉每次动态重建的 system 消息与工具迭代警告）作为新的上下文历史。
# 所有消息现均为 dict（OpenAI Chat Completions 格式）。
<<< END U010747 >>>
<<< UNIT U010748 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:2-2 | ctx=ai.help >>>
与大语言模型聊天。（需要消耗花瓣）
<<< END U010748 >>>
<<< UNIT U010749 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:3-3 | ctx=ai.help.desc >>>
有事为什么不问问小可呢？
<<< END U010749 >>>
<<< UNIT U010750 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:4-4 | ctx=ai.help.llm.instruct >>>
设置大语言模型的自定义命令。
<<< END U010750 >>>
<<< UNIT U010751 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:5-5 | ctx=ai.help.llm.list >>>
查看支持的大语言模型列表。
<<< END U010751 >>>
<<< UNIT U010752 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:6-6 | ctx=ai.help.llm.list.option.price >>>
是否显示具体价格信息。
<<< END U010752 >>>
<<< UNIT U010753 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:7-7 | ctx=ai.help.llm.persona >>>
设置是否开启人格化，效果因模型而异。
<<< END U010753 >>>
<<< UNIT U010754 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:8-8 | ctx=ai.help.llm.price >>>
查看大语言模型的花瓣价格。
<<< END U010754 >>>
<<< UNIT U010755 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:9-9 | ctx=ai.help.llm.set >>>
设置{TERM:target}内默认大语言模型。
<<< END U010755 >>>
<<< UNIT U010756 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:10-10 | ctx=ai.help.option.ctx >>>
指定要延续的对话轮次 ID。
<<< END U010756 >>>
<<< UNIT U010757 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:11-11 | ctx=ai.help.option.llm >>>
指定使用的大语言模型。
<<< END U010757 >>>
<<< UNIT U010758 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:12-12 | ctx=ai.help.option.no_tools >>>
是否禁止大语言模型调用工具。
<<< END U010758 >>>
<<< UNIT U010759 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:13-13 | ctx=ai.message.context.hint >>>
提示：在 ${expiry} 分钟内使用“${cmd}”可继续对话。
<<< END U010759 >>>
<<< UNIT U010760 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:14-14 | ctx=ai.message.context.hint.reply >>>
提示：在 ${expiry} 分钟内引用回复此消息或使用“${cmd}”可继续对话。
<<< END U010760 >>>
<<< UNIT U010761 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:15-15 | ctx=ai.message.context.id >>>
对话轮次 ID：${turn_id}
<<< END U010761 >>>
<<< UNIT U010762 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:16-16 | ctx=ai.message.context.invalid >>>
对话轮次不存在或已过期。
<<< END U010762 >>>
<<< UNIT U010763 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:17-17 | ctx=ai.message.no_prompt >>>
请发送 Prompt 消息以开始对话。
<<< END U010763 >>>
<<< UNIT U010764 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:18-18 | ctx=ai.message.llm.instruct.clear.success >>>
已清除自定义命令。
<<< END U010764 >>>
<<< UNIT U010765 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:19-19 | ctx=ai.message.llm.instruct.set.success >>>
已设置自定义命令。
<<< END U010765 >>>
<<< UNIT U010766 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:20-20 | ctx=ai.message.llm.invalid >>>
无效的大语言模型。
<<< END U010766 >>>
<<< UNIT U010767 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:21-21 | ctx=ai.message.llm.list >>>
以下为可用的大语言模型：
<<< END U010767 >>>
<<< UNIT U010768 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:22-22 | ctx=ai.message.llm.persona.enable >>>
已开启人格化。
<<< END U010768 >>>
<<< UNIT U010769 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:23-23 | ctx=ai.message.llm.persona.disable >>>
已关闭人格化。
<<< END U010769 >>>
<<< UNIT U010770 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:24-24 | ctx=ai.message.llm.price >>>
“${name}”的花瓣价格：
<<< END U010770 >>>
<<< UNIT U010771 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:25-25 | ctx=ai.message.llm.list.billing.token >>>
输入（未命中缓存）：${input_price} 花瓣/1M Token | 输出：${output_price} 花瓣/1M Token
<<< END U010771 >>>
<<< UNIT U010772 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:26-26 | ctx=ai.message.llm.list.billing.token.cache >>>
缓存创建：${cache_write_price} 花瓣/1M Token | 缓存读取：${cache_read_price} 花瓣/1M Token
<<< END U010772 >>>
<<< UNIT U010773 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:27-27 | ctx=ai.message.llm.list.billing.call >>>
调用价格：${call_price} 花瓣/次
<<< END U010773 >>>
<<< UNIT U010774 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:28-28 | ctx=ai.message.llm.list.billing.tiers.threshold >>>
超过 ${context_threshold} Token 后：
<<< END U010774 >>>
<<< UNIT U010775 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:29-29 | ctx=ai.message.llm.list.none >>>
找不到可用的大语言模型，请联系机器人拥有者添加。
<<< END U010775 >>>
<<< UNIT U010776 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:30-30 | ctx=ai.message.llm.list.prompt >>>
使用“${cmd}<模型名称>”切换模型。
<<< END U010776 >>>
<<< UNIT U010777 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:31-31 | ctx=ai.message.references.title >>>
参考资料
<<< END U010777 >>>
<<< UNIT U010778 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:32-32 | ctx=config.comments.module_ai_secret.e2b_api_key >>>
E2B 的 API key。
<<< END U010778 >>>
<<< UNIT U010779 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:33-33 | ctx=config.comments.module_ai.ai_cost_to_petal >>>
花瓣与调用费用的比率。
<<< END U010779 >>>
<<< UNIT U010780 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:34-34 | ctx=config.comments.module_ai.ai_default_llm >>>
默认使用的大语言模型。
<<< END U010780 >>>
<<< UNIT U010781 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:35-35 | ctx=config.comments.module_ai.llm_frequency_penalty >>>
大语言模型的频率惩罚，范围 -2 到 2 之间。
<<< END U010781 >>>
<<< UNIT U010782 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:36-36 | ctx=config.comments.module_ai.llm_max_calling_iteration >>>
限制大语言模型的最大工具调用迭代次数。
<<< END U010782 >>>
<<< UNIT U010783 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:37-37 | ctx=config.comments.module_ai.llm_max_tokens >>>
限制大语言模型的最大 Token 数。
<<< END U010783 >>>
<<< UNIT U010784 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:38-38 | ctx=config.comments.module_ai.llm_presence_penalty >>>
大语言模型的存在惩罚，范围 -2 到 2 之间。
<<< END U010784 >>>
<<< UNIT U010785 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:39-39 | ctx=config.comments.module_ai.llm_reasoning_effort >>>
大语言模型的思考强度，若为 none 则不启用思维链。
<<< END U010785 >>>
<<< UNIT U010786 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:40-40 | ctx=config.comments.module_ai.llm_temperature >>>
大语言模型的温度采样，范围 0 到 2 之间。不建议与 top_p 同时修改。
<<< END U010786 >>>
<<< UNIT U010787 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:41-41 | ctx=config.comments.module_ai.llm_timeout >>>
大语言模型的超时时间。
<<< END U010787 >>>
<<< UNIT U010788 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:42-42 | ctx=config.comments.module_ai.llm_top_logprobs >>>
大语言模型返回的候选 Token 对数概率数量，范围 0 到 20 之间，负数则不传入。
<<< END U010788 >>>
<<< UNIT U010789 | json-value | packages/modules/akari-bot-module-ai/akaribot/modules/ai/locales/zh_cn.json:43-43 | ctx=config.comments.module_ai.llm_top_p >>>
大语言模型的核采样，范围 0 到 1 之间。不建议与 temperature 同时修改。
<<< END U010789 >>>
<<< UNIT U010790 | cfg-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/manifest.toml:1-1 >>>
# akari-bot-module-ai 的包清单。
<<< END U010790 >>>
<<< UNIT U010791 | cfg-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/manifest.toml:6-6 >>>
# config.py 的 on_module_config("ai") 声明的表。
<<< END U010791 >>>
<<< UNIT U010792 | cfg-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/manifest.toml:10-10 >>>
# 查重用的登录信息字段，对应 E2B 沙箱服务密钥。
<<< END U010792 >>>
<<< UNIT U010793 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/setting.py:17-17 >>>
# 指令文本含 LaTeX 的 $$，标准 Template 会把它折叠成 $。该模式只识别 ${name}，其余 $ 原样保留。
<<< END U010793 >>>
<<< UNIT U010794 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/setting.py:188-188 >>>
# 配置的默认模型可能已从 llm_api_list 中移除，只有仍可用时才作为默认值。
<<< END U010794 >>>
<<< UNIT U010795 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/tools/__init__.py:41-41 >>>
# 图片以独立用户消息回传，避免把 base64 放入模型可见的工具文本。
<<< END U010795 >>>
<<< UNIT U010796 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/tools/__init__.py:134-134 >>>
# 所有工具结果之后再追加图片，避免 user 消息夹在并行的 tool 消息之间。
<<< END U010796 >>>
<<< UNIT U010797 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/tools/fetch_webpage.py:46-46 >>>
# 优先抽取正文，正文识别失败时转为无标记的纯文本，保证模型拿不到 HTML 标记。
<<< END U010797 >>>
<<< UNIT U010798 | py-comment | packages/modules/akari-bot-module-ai/akaribot/modules/ai/tools/fetch_webpage.py:72-72 >>>
# WebRender 由机器人自身发起请求，需补做内网校验，否则会绕过 get_url 的地址限制。
<<< END U010798 >>>
<<< UNIT U010799 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_anthropic_tool_choice.py:10-10 >>>
# 捕获请求参数后中断 create 流程。
<<< END U010799 >>>
<<< UNIT U010800 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_anthropic_tool_choice.py:1-1 | ctx=<module> >>>
akaribot.modules.ai Anthropic 端点 tool_choice 线格式单元测试。
<<< END U010800 >>>
<<< UNIT U010801 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_anthropic_tool_choice.py:39-39 | ctx=test_ai_anthropic_tool_choice >>>
akaribot.modules.ai: Anthropic 端点下发对象形式的 tool_choice
<<< END U010801 >>>
<<< UNIT U010802 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_billing_time_rules.py:21-21 >>>
# 23:30 UTC 在核心默认时区 +8 下是周二 07:30，命中该时段。直接按 UTC 判定则不命中。
<<< END U010802 >>>
<<< UNIT U010803 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_billing_time_rules.py:1-1 | ctx=<module> >>>
akaribot.modules.ai.setting 计费时间段单元测试。
<<< END U010803 >>>
<<< UNIT U010804 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_billing_time_rules.py:40-40 | ctx=test_ai_billing_time_rules >>>
akaribot.modules.ai.setting: LLM 计费时间段规则测试
<<< END U010804 >>>
<<< UNIT U010805 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_context.py:1-1 | ctx=<module> >>>
akaribot.modules.ai.context 上下文窗口单元测试。
<<< END U010805 >>>
<<< UNIT U010806 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_context.py:36-36 | ctx=test_ai_context >>>
akaribot.modules.ai.context: 上下文窗口隔离与快照分叉测试
<<< END U010806 >>>
<<< UNIT U010807 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_fetch_webpage.py:1-1 | ctx=<module> >>>
akaribot.modules.ai.tools.fetch_webpage 网页抓取单元测试。
<<< END U010807 >>>
<<< UNIT U010808 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_fetch_webpage.py:104-104 | ctx=test_ai_fetch_webpage >>>
akaribot.modules.ai.tools.fetch_webpage: 轻量优先、WebRender 回退与正文清洗测试
<<< END U010808 >>>
<<< UNIT U010809 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_gemini_generate_content.py:1-1 | ctx=<module> >>>
akaribot.modules.ai Gemini GenerateContent API 端点单元测试。
<<< END U010809 >>>
<<< UNIT U010810 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_gemini_generate_content.py:434-434 | ctx=test_ai_gemini_generate_content >>>
akaribot.modules.ai: Gemini GenerateContent API 端点请求与响应转换
<<< END U010810 >>>
<<< UNIT U010811 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_gemini_interactions.py:1-1 | ctx=<module> >>>
akaribot.modules.ai Gemini Interactions API 端点单元测试。
<<< END U010811 >>>
<<< UNIT U010812 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_gemini_interactions.py:303-303 | ctx=test_ai_gemini_interactions >>>
akaribot.modules.ai: Gemini Interactions API 端点请求与响应转换
<<< END U010812 >>>
<<< UNIT U010813 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_hook.py:42-42 >>>
# 调用方指定 > 场景默认 > 模块默认
<<< END U010813 >>>
<<< UNIT U010814 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_hook.py:46-46 >>>
# 显式指定的模型不可用时不替换，场景默认模型离线时改用模块默认
<<< END U010814 >>>
<<< UNIT U010815 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_hook.py:1-1 | ctx=<module> >>>
akaribot.modules.ai.hook ai.ask 带名称的 hook 单元测试。
<<< END U010815 >>>
<<< UNIT U010816 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_hook.py:99-99 | ctx=test_ai_hook >>>
akaribot.modules.ai.hook: ai.ask 调用约定测试
<<< END U010816 >>>
<<< UNIT U010817 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_image_generation.py:1-1 | ctx=<module> >>>
akaribot.modules.ai 图片生成与编辑工具单元测试。
<<< END U010817 >>>
<<< UNIT U010818 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_image_generation.py:341-341 | ctx=test_ai_image_generation >>>
akaribot.modules.ai: 图片生成与编辑工具、提示工程与成本折算测试
<<< END U010818 >>>
<<< UNIT U010819 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_python_images.py:1-1 | ctx=<module> >>>
akaribot.modules.ai Python 沙箱图片回传单元测试。
<<< END U010819 >>>
<<< UNIT U010820 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_python_images.py:153-153 | ctx=test_ai_python_images >>>
akaribot.modules.ai: 沙箱图片回传与上下文历史测试
<<< END U010820 >>>
<<< UNIT U010821 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_reasoning_effort.py:11-11 >>>
# 捕获请求参数后中断 create 流程。
<<< END U010821 >>>
<<< UNIT U010822 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_reasoning_effort.py:20-20 >>>
# 仅思考模式或非混合思考模式的千问模型不接受 enable_thinking
<<< END U010822 >>>
<<< UNIT U010823 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_reasoning_effort.py:36-36 >>>
# 显式 null 保留为空值，用于指示该参数不下发
<<< END U010823 >>>
<<< UNIT U010824 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_reasoning_effort.py:85-85 >>>
# 模块默认的 top_logprobs 为负数，表示不请求对数概率
<<< END U010824 >>>
<<< UNIT U010825 | py-comment | packages/modules/akari-bot-module-ai/tests/test_ai_reasoning_effort.py:294-294 >>>
# minimal 不映射到 output_config，但仍开启思考
<<< END U010825 >>>
<<< UNIT U010826 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_reasoning_effort.py:1-1 | ctx=<module> >>>
akaribot.modules.ai 生成参数（采样与思考强度）按模型覆盖的单元测试。
<<< END U010826 >>>
<<< UNIT U010827 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_ai_reasoning_effort.py:341-341 | ctx=test_ai_reasoning_effort >>>
akaribot.modules.ai: 采样、思考强度与对数概率支持按模型覆盖或空值省略
<<< END U010827 >>>
<<< UNIT U010828 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_search_images.py:1-1 | ctx=<module> >>>
search_images AI 工具非图片结果过滤单元测试。
<<< END U010828 >>>
<<< UNIT U010829 | py-docstring | packages/modules/akari-bot-module-ai/tests/test_search_images.py:100-100 | ctx=test_search_images >>>
search_images 仅返回可直接使用的图片结果。
<<< END U010829 >>>
<<< UNIT U010830 | md-paragraph | packages/modules/akari-bot-module-arcaea/README.md:3-3 | ctx=akari-bot-module-arcaea >>>
查询 Arcaea 相关内容。
<<< END U010830 >>>
<<< UNIT U010831 | md-heading | packages/modules/akari-bot-module-arcaea/README.md:5-5 | ctx=安装 >>>
## 安装
<<< END U010831 >>>
<<< UNIT U010832 | md-paragraph | packages/modules/akari-bot-module-arcaea/README.md:7-7 | ctx=安装 >>>
Python 版本要求见包内 `pyproject.toml` 的 `requires-python`。
<<< END U010832 >>>
<<< UNIT U010833 | md-paragraph | packages/modules/akari-bot-module-arcaea/README.md:13-13 | ctx=安装 >>>
模块的启用与配置参见 [项目文档](https://github.com/Teahouse-Studios/akari-bot/blob/master/README.md)。
<<< END U010833 >>>
<<< UNIT U010834 | md-heading | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:5-5 | ctx=arcaea：安装与开发 >>>
# arcaea：安装与开发
<<< END U010834 >>>
<<< UNIT U010835 | md-heading | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:7-7 | ctx=安装 >>>
## 安装
<<< END U010835 >>>
<<< UNIT U010836 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:13-13 | ctx=安装 >>>
安装后，管理员需要在会话中执行 `module enable arcaea` 开启模块。
<<< END U010836 >>>
<<< UNIT U010837 | md-heading | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:15-15 | ctx=配置项 >>>
## 配置项
<<< END U010837 >>>
<<< UNIT U010838 | md-heading | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:19-19 | ctx=权限与平台能力 >>>
## 权限与平台能力
<<< END U010838 >>>
<<< UNIT U010839 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:21-21 | ctx=权限与平台能力 >>>
`download`、`random`、`rank` 三个命令通过 WebRender 请求官方接口，使用前需要开启 `webrender.enable`。`calc` 是纯本地计算，不依赖网络。曲绘从包内 `assets/jacket/<song_id>.jpg` 读取，文件缺失时命令只发送文本。
<<< END U010839 >>>
<<< UNIT U010840 | md-heading | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:23-23 | ctx=数据表 >>>
## 数据表
<<< END U010840 >>>
<<< UNIT U010841 | md-heading | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:27-27 | ctx=依赖与外部服务 >>>
## 依赖与外部服务
<<< END U010841 >>>
<<< UNIT U010842 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/development.md:29-29 | ctx=依赖与外部服务 >>>
依赖 `orjson` 与 `akari-bot-core`。外部服务是 `webapi.lowiro.com`，提供 APK 信息、曲目展示、免费与付费排行。模块通过 WebRender 读取该接口返回的原始响应。
<<< END U010842 >>>
<<< UNIT U010843 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:11-11 | ctx=arcaea >>>
此模块可以查询 Arcaea 的最新版本与下载地址、官方游玩排行，随机抽取一首曲目，并按分数与谱面定数计算单曲潜力值。
<<< END U010843 >>>
<<< UNIT U010844 | md-heading | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:13-13 | ctx=命令 >>>
## 命令
<<< END U010844 >>>
<<< UNIT U010845 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:21-21 | ctx=`arcaea download` >>>
此命令用于查询游戏 APK 的最新版本号与下载地址。查询失败时返回错误提示。
<<< END U010845 >>>
<<< UNIT U010846 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:24-29 | ctx=`arcaea download` >>>
  :log="[
    '用户：~arcaea download',
    '机器人：当前最新版本：7.1.0c',
    '下载地址：`https://arcaea-static.lowiro-cdn.net/…?filename=arcaea_7.1.0c.apk`',
  ]"
/>
<<< END U010846 >>>
<<< UNIT U010847 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:35-35 | ctx=`arcaea random` >>>
此命令用于从官方曲目列表中随机抽取一首曲目，并附上曲绘。曲绘缺失时只发送曲名。
<<< END U010847 >>>
<<< UNIT U010848 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:38-42 | ctx=`arcaea random` >>>
  :log="[
    '用户：~arcaea random',
    '机器人：PUPA',
  ]"
/>
<<< END U010848 >>>
<<< UNIT U010849 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:48-48 | ctx=`arcaea rank free` >>>
此命令用于查看当前免费歌曲的游玩排行，输出名次、曲名与状态。
<<< END U010849 >>>
<<< UNIT U010850 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:51-57 | ctx=`arcaea rank free` >>>
  :log="[
    '用户：~arcaea rank free',
    '机器人：1. Kanagawa Cyber Culvert (0)',
    '2. Remind the Souls (Short Version) (0)',
    '3. Lost Civilization (0)',
  ]"
/>
<<< END U010850 >>>
<<< UNIT U010851 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:63-63 | ctx=`arcaea rank paid` >>>
此命令用于查看当前付费歌曲的游玩排行，输出名次、曲名与状态。
<<< END U010851 >>>
<<< UNIT U010852 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:66-72 | ctx=`arcaea rank paid` >>>
  :log="[
    '用户：~arcaea rank paid',
    '机器人：1. Tr!cK Ma?tEr (0)',
    '2. DEINOS PHAINEIN (0)',
    '3. Grievous Lady (3)',
  ]"
/>
<<< END U010852 >>>
<<< UNIT U010853 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:78-78 | ctx=`arcaea calc` >>>
此命令用于按分数与谱面定数计算单曲潜力值。
<<< END U010853 >>>
<<< UNIT U010854 | md-list | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:80-82 | ctx=`arcaea calc` >>>
- 分数不低于 10000000 时，按定数加 2 计算。
- 分数不低于 9800000 时，按定数加 1 计算，再加上 `(分数 - 9800000) / 200000`。
- 分数低于 9800000 时，按定数加 `(分数 - 9500000) / 300000` 计算。
<<< END U010854 >>>
<<< UNIT U010855 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:84-84 | ctx=`arcaea calc` >>>
结果保留两位小数，低于 0 时按 0 输出。
<<< END U010855 >>>
<<< UNIT U010856 | md-paragraph | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/docs/index.md:87-91 | ctx=`arcaea calc` >>>
  :log="[
    '用户：~arcaea calc 9980000 10.5',
    '机器人：11.59',
  ]"
/>
<<< END U010856 >>>
<<< UNIT U010857 | json-value | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json:2-2 | ctx=arcaea.help.calc >>>
根据分数与谱面定数计算对应的谱面潜力值。
<<< END U010857 >>>
<<< UNIT U010858 | json-value | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json:3-3 | ctx=arcaea.help.desc >>>
查询 Arcaea 相关内容。
<<< END U010858 >>>
<<< UNIT U010859 | json-value | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json:4-4 | ctx=arcaea.help.download >>>
获取最新版本的游戏 APK。
<<< END U010859 >>>
<<< UNIT U010860 | json-value | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json:5-5 | ctx=arcaea.help.random >>>
随机一首歌曲。
<<< END U010860 >>>
<<< UNIT U010861 | json-value | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json:6-6 | ctx=arcaea.help.rank.free >>>
查看当前免费歌曲游玩排行。
<<< END U010861 >>>
<<< UNIT U010862 | json-value | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json:7-7 | ctx=arcaea.help.rank.paid >>>
查看当前付费歌曲游玩排行。
<<< END U010862 >>>
<<< UNIT U010863 | json-value | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json:8-8 | ctx=arcaea.message.download >>>
当前最新版本：${version}
下载地址：${url}
<<< END U010863 >>>
<<< UNIT U010864 | json-value | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/locales/zh_cn.json:9-9 | ctx=arcaea.message.get_failed >>>
获取失败。
<<< END U010864 >>>
<<< UNIT U010865 | cfg-comment | packages/modules/akari-bot-module-arcaea/akaribot/modules/arcaea/manifest.toml:1-1 >>>
# akari-bot-module-arcaea 的包清单。
<<< END U010865 >>>
