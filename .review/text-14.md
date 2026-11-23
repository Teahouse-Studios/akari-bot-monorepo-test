# 全仓可读文本审核稿 · 第 14 册 / 共 20 册

覆盖 U009157–U010119，74 个文件、963 个单元、33,804 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-core/akaribot/modules/core/docs/post-whitelist.md` | 4 | U009157–U009160 | 261 |
| `packages/akari-bot-core/akaribot/modules/core/docs/post.md` | 5 | U009161–U009165 | 392 |
| `packages/akari-bot-core/akaribot/modules/core/docs/purge.md` | 4 | U009166–U009169 | 199 |
| `packages/akari-bot-core/akaribot/modules/core/docs/raise.md` | 3 | U009170–U009172 | 166 |
| `packages/akari-bot-core/akaribot/modules/core/docs/restart.md` | 3 | U009173–U009175 | 281 |
| `packages/akari-bot-core/akaribot/modules/core/docs/retired_policy.md` | 3 | U009176–U009178 | 274 |
| `packages/akari-bot-core/akaribot/modules/core/docs/say.md` | 5 | U009179–U009183 | 287 |
| `packages/akari-bot-core/akaribot/modules/core/docs/set.md` | 19 | U009184–U009202 | 1,398 |
| `packages/akari-bot-core/akaribot/modules/core/docs/setup.md` | 48 | U009203–U009250 | 3,117 |
| `packages/akari-bot-core/akaribot/modules/core/docs/superuser.md` | 5 | U009251–U009255 | 349 |
| `packages/akari-bot-core/akaribot/modules/core/docs/telemetry.md` | 4 | U009256–U009259 | 276 |
| `packages/akari-bot-core/akaribot/modules/core/docs/tos.md` | 3 | U009260–U009262 | 456 |
| `packages/akari-bot-core/akaribot/modules/core/docs/typo.md` | 3 | U009263–U009265 | 305 |
| `packages/akari-bot-core/akaribot/modules/core/docs/update-restart.md` | 4 | U009266–U009269 | 288 |
| `packages/akari-bot-core/akaribot/modules/core/docs/update.md` | 3 | U009270–U009272 | 481 |
| `packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md` | 25 | U009273–U009297 | 2,242 |
| `packages/akari-bot-core/akaribot/modules/core/docs/webrender.md` | 7 | U009298–U009304 | 353 |
| `packages/akari-bot-core/akaribot/modules/core/hooks/__init__.py` | 1 | U009305–U009305 | 22 |
| `packages/akari-bot-core/akaribot/modules/core/hooks/errors.py` | 3 | U009306–U009308 | 170 |
| `packages/akari-bot-core/akaribot/modules/core/hooks/policies.py` | 4 | U009309–U009312 | 251 |
| `packages/akari-bot-core/akaribot/modules/core/hooks/retired.py` | 2 | U009313–U009314 | 98 |
| `packages/akari-bot-core/akaribot/modules/core/hooks/routing.py` | 2 | U009315–U009316 | 47 |
| `packages/akari-bot-core/akaribot/modules/core/hooks/telemetry.py` | 2 | U009317–U009318 | 60 |
| `packages/akari-bot-core/akaribot/modules/core/hooks/tos.py` | 13 | U009319–U009331 | 570 |
| `packages/akari-bot-core/akaribot/modules/core/hooks/typo.py` | 2 | U009332–U009333 | 85 |
| `packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json` | 559 | U009334–U009892 | 11,994 |
| `packages/akari-bot-core/akaribot/modules/core/manifest.toml` | 3 | U009893–U009895 | 162 |
| `packages/akari-bot-core/akaribot/modules/core/su_tools/__init__.py` | 1 | U009896–U009896 | 12 |
| `packages/akari-bot-core/akaribot/modules/core/su_tools/analytics.py` | 6 | U009897–U009902 | 448 |
| `packages/akari-bot-core/akaribot/modules/core/su_tools/config.py` | 1 | U009903–U009903 | 31 |
| `packages/akari-bot-core/akaribot/modules/core/su_tools/features.py` | 2 | U009904–U009905 | 42 |
| `packages/akari-bot-core/akaribot/modules/core/su_tools/update.py` | 8 | U009906–U009913 | 415 |
| `packages/akari-bot-core/pyproject.toml` | 4 | U009914–U009917 | 455 |
| `packages/akari-bot-core/tests/test_about.py` | 2 | U009918–U009919 | 114 |
| `packages/akari-bot-core/tests/test_action_text.py` | 14 | U009920–U009933 | 510 |
| `packages/akari-bot-core/tests/test_analytics_plot.py` | 8 | U009934–U009941 | 319 |
| `packages/akari-bot-core/tests/test_analytics_window.py` | 4 | U009942–U009945 | 186 |
| `packages/akari-bot-core/tests/test_atcode.py` | 3 | U009946–U009948 | 112 |
| `packages/akari-bot-core/tests/test_bind_auto.py` | 17 | U009949–U009965 | 730 |
| `packages/akari-bot-core/tests/test_bind_start.py` | 7 | U009966–U009972 | 279 |
| `packages/akari-bot-core/tests/test_brand_lookup.py` | 2 | U009973–U009974 | 52 |
| `packages/akari-bot-core/tests/test_bud.py` | 5 | U009975–U009979 | 135 |
| `packages/akari-bot-core/tests/test_button_arrange.py` | 2 | U009980–U009981 | 38 |
| `packages/akari-bot-core/tests/test_button_runtime.py` | 2 | U009982–U009983 | 43 |
| `packages/akari-bot-core/tests/test_cache.py` | 2 | U009984–U009985 | 56 |
| `packages/akari-bot-core/tests/test_chain_normalize.py` | 2 | U009986–U009987 | 162 |
| `packages/akari-bot-core/tests/test_channel_dedup.py` | 7 | U009988–U009994 | 264 |
| `packages/akari-bot-core/tests/test_channel_scope.py` | 6 | U009995–U010000 | 226 |
| `packages/akari-bot-core/tests/test_component.py` | 2 | U010001–U010002 | 68 |
| `packages/akari-bot-core/tests/test_config.py` | 3 | U010003–U010005 | 102 |
| `packages/akari-bot-core/tests/test_config_global.py` | 2 | U010006–U010007 | 45 |
| `packages/akari-bot-core/tests/test_config_migration.py` | 2 | U010008–U010009 | 142 |
| `packages/akari-bot-core/tests/test_config_readonly.py` | 3 | U010010–U010012 | 68 |
| `packages/akari-bot-core/tests/test_config_scan.py` | 9 | U010013–U010021 | 373 |
| `packages/akari-bot-core/tests/test_confirm_prompt.py` | 1 | U010022–U010022 | 15 |
| `packages/akari-bot-core/tests/test_container.py` | 4 | U010023–U010026 | 154 |
| `packages/akari-bot-core/tests/test_cooldown.py` | 6 | U010027–U010032 | 254 |
| `packages/akari-bot-core/tests/test_data_entrypoint.py` | 13 | U010033–U010045 | 569 |
| `packages/akari-bot-core/tests/test_database_init.py` | 3 | U010046–U010048 | 126 |
| `packages/akari-bot-core/tests/test_database_link_anchor.py` | 1 | U010049–U010049 | 49 |
| `packages/akari-bot-core/tests/test_database_migration.py` | 4 | U010050–U010053 | 160 |
| `packages/akari-bot-core/tests/test_database_transaction_cancel.py` | 3 | U010054–U010056 | 96 |
| `packages/akari-bot-core/tests/test_database_update.py` | 7 | U010057–U010063 | 237 |
| `packages/akari-bot-core/tests/test_dependency_graph.py` | 3 | U010064–U010066 | 114 |
| `packages/akari-bot-core/tests/test_dirty_check.py` | 4 | U010067–U010070 | 213 |
| `packages/akari-bot-core/tests/test_dirty_check_features.py` | 3 | U010071–U010073 | 160 |
| `packages/akari-bot-core/tests/test_docs_entrypoint.py` | 2 | U010074–U010075 | 87 |
| `packages/akari-bot-core/tests/test_entrypoint_config.py` | 9 | U010076–U010084 | 438 |
| `packages/akari-bot-core/tests/test_entrypoint_db_purge.py` | 1 | U010085–U010085 | 29 |
| `packages/akari-bot-core/tests/test_entrypoint_rpc.py` | 7 | U010086–U010092 | 394 |
| `packages/akari-bot-core/tests/test_error_reporting.py` | 2 | U010093–U010094 | 45 |
| `packages/akari-bot-core/tests/test_event.py` | 2 | U010095–U010096 | 54 |
| `packages/akari-bot-core/tests/test_func_utils.py` | 2 | U010097–U010098 | 49 |
| `packages/akari-bot-core/tests/test_help_action_text.py` | 21 | U010099–U010119 | 550 |

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
<<< UNIT U009157 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post-whitelist.md:9-9 | ctx=post-whitelist >>>
审阅次数：10
模块级所需权限为超级用户。
<<< END U009157 >>>
<<< UNIT U009158 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post-whitelist.md:15-15 | ctx=`post-whitelist` >>>
审阅次数：10
此命令切换目标群的主动推送优先级，仅 QQ 平台可用。参数必须是以 `QQ|Group|` 开头的完整 ID。若目标群尚未包含场景记录，机器人需要先请求确认，确认通过后再执行创建。
<<< END U009158 >>>
<<< UNIT U009159 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post-whitelist.md:17-17 | ctx=`post-whitelist` >>>
审阅次数：10
此开关的值写入场景数据的 `in_post_whitelist`。适配器在主动推送时根据此设置将场景排入高优先级队列。
<<< END U009159 >>>
<<< UNIT U009160 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post-whitelist.md:20-24 | ctx=`post-whitelist` >>>
审阅次数：10
  :log="[
    '用户：~post-whitelist QQ|Group|123456789',
    '机器人：成功为群聊设置了以下参数：in_post_whitelist -> True',
  ]"
/>
<<< END U009160 >>>
<<< UNIT U009161 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post.md:7-7 | ctx=post >>>
审阅次数：10
模块级所需权限为超级用户。
<<< END U009161 >>>
<<< UNIT U009162 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post.md:13-13 | ctx=`post` >>>
审阅次数：10
此命令向指定场景推送主动消息，执行前需要确认。目标场景 ID 必须包含平台前缀。若缺少前缀，机器人会提示当前场景所使用的前缀。`post_msg` 支持 KE 码。
<<< END U009162 >>>
<<< UNIT U009163 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post.md:16-22 | ctx=`post` >>>
审阅次数：10
  :log="[
    '用户：~post QQ|Group|987654321 今晚 23:00 例行维护。',
    '机器人：此操作将会为群聊 QQ|Group|987654321 推送以下消息，是否继续？',
    '用户：是',
    '机器人：推送消息完成。',
  ]"
/>
<<< END U009163 >>>
<<< UNIT U009164 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post.md:28-28 | ctx=`post global` >>>
审阅次数：10
此命令向全部已启用的场景广播主动消息，执行前需要确认。
<<< END U009164 >>>
<<< UNIT U009165 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/post.md:31-37 | ctx=`post global` >>>
审阅次数：10
  :log="[
    '用户：~post global 全部群聊将于今晚 23:00 重启。',
    '机器人：警告：此操作将会为所有群聊推送以下消息，是否继续？',
    '用户：是',
    '机器人：推送消息完成。',
  ]"
/>
<<< END U009165 >>>
<<< UNIT U009166 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/purge.md:7-7 | ctx=purge >>>
审阅次数：10
此模块提供缓存清理命令与定时清理任务，模块级所需权限为超级用户。
<<< END U009166 >>>
<<< UNIT U009167 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/purge.md:13-13 | ctx=`purge` >>>
审阅次数：10
此命令清空实例的 `cache/` 目录。若目录为空，机器人会输出提示信息。
<<< END U009167 >>>
<<< UNIT U009168 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/purge.md:15-15 | ctx=`purge` >>>
审阅次数：10
此模块同时注册了定时清理任务，按照 `auto_purge_crontab` 执行，默认值为 `0 0 * * *`。命令与定时任务均不会修改 `data/` 目录以及数据库。
<<< END U009168 >>>
<<< UNIT U009169 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/purge.md:18-22 | ctx=`purge` >>>
审阅次数：10
  :log="[
    '用户：~purge',
    '机器人：成功清除缓存。',
  ]"
/>
<<< END U009169 >>>
<<< UNIT U009170 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/raise.md:7-7 | ctx=raise >>>
审阅次数：10
模块级所需权限为超级用户。
<<< END U009170 >>>
<<< UNIT U009171 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/raise.md:13-13 | ctx=`raise` >>>
审阅次数：10
此命令抛出 `TestException` 异常，用于验证错误上报链路。传入的参数作为异常信息，省略参数时使用内置文案。
<<< END U009171 >>>
<<< UNIT U009172 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/raise.md:16-22 | ctx=`raise` >>>
审阅次数：10
  :log="[
    '用户：~raise 测试错误上报',
    '机器人：执行命令时发生错误：',
    '测试错误上报',
    '请将此信息报告给机器人所有者。',
  ]"
/>
<<< END U009172 >>>
<<< UNIT U009173 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/restart.md:7-7 | ctx=restart >>>
审阅次数：10
模块级所需权限为超级用户。
<<< END U009173 >>>
<<< UNIT U009174 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/restart.md:13-18 | ctx=`restart` >>>
审阅次数：10
- Web 平台不注册此命令，仅在子进程模式下可用。
- 重启全部子进程。
- 默认等待正在执行的命令结束，并请求确认。若 60 秒内仍有命令处于执行状态，机器人会输出提示信息。
- `--force` 跳过确认与等待。
- 执行前将发起会话写入 `data/private/<client>/.cache_restart_author`。
- 进程以退出码 33 结束，通过守护进程重启全部子进程。重启完成后，机器人会在原场景发送提示信息。
<<< END U009174 >>>
<<< UNIT U009175 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/restart.md:21-25 | ctx=`restart` >>>
审阅次数：10
  :log="[
    '用户：~restart --force',
    '机器人：重启中……',
  ]"
/>
<<< END U009175 >>>
<<< UNIT U009176 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/retired_policy.md:8-8 | ctx=retired_policy >>>
审阅次数：10
此策略配合 `config.toml` 中的 `retired_clients` 配置项处理退役客户端：
<<< END U009176 >>>
<<< UNIT U009177 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/retired_policy.md:10-12 | ctx=retired_policy >>>
审阅次数：10
- 退役客户端的消息仅放行 `merge` 白名单中的命令。模块别名改写前，用户实际输入的首词同样参与判定。
- 同一消息通道存在未退役场景时，退役场景处于非活动状态，不等待任务，亦不参与命令认领。相关命令交由未退役场景处理。
- `retired_clients` 为空时策略不生效。非空时，`merge` 模块按照此配置加载，参见 [merge](merge.md)。
<<< END U009177 >>>
<<< UNIT U009178 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/retired_policy.md:14-14 | ctx=retired_policy >>>
审阅次数：10
配置格式为 `<源客户端> -> <目标客户端>`。若仅填写源客户端，表示此客户端已处于退役状态，但未指定迁移目标。
<<< END U009178 >>>
<<< UNIT U009179 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/say.md:7-7 | ctx=say >>>
审阅次数：10
模块级所需权限为超级用户。
<<< END U009179 >>>
<<< UNIT U009180 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/say.md:13-13 | ctx=`say` >>>
审阅次数：10
此命令将给定内容按照消息链格式解析后发送，不引用原消息。文本中包含发送者平台前缀的用户 ID 会被转换为 AT 码，发送后渲染为对该用户的提及。
<<< END U009180 >>>
<<< UNIT U009181 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/say.md:16-20 | ctx=`say` >>>
审阅次数：10
  :log="[
    '用户：~say 今晚 23:00 例行维护，请提前保存。',
    '机器人：今晚 23:00 例行维护，请提前保存。',
  ]"
/>
<<< END U009181 >>>
<<< UNIT U009182 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/say.md:26-26 | ctx=`say md` >>>
审阅次数：10
此命令按照 Markdown 格式复述指定内容，并附加按钮示例。
<<< END U009182 >>>
<<< UNIT U009183 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/say.md:29-33 | ctx=`say md` >>>
审阅次数：10
  :log="[
    '用户：~say md **维护通知**：今晚 23:00 重启。',
    '机器人：**维护通知**：今晚 23:00 重启。',
  ]"
/>
<<< END U009183 >>>
<<< UNIT U009184 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:7-7 | ctx=set >>>
审阅次数：10
此模块可以直接修改目标场景或用户的数据。模块级权限为超级用户。参数中的 ID 必须包含平台前缀。若目标场景不存在，机器人会先请求确认，确认通过后再执行创建。
<<< END U009184 >>>
<<< UNIT U009185 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:13-13 | ctx=`set target module enable` >>>
审阅次数：10
此命令在目标场景启用模块。未包含在当前平台可用列表中的模块名称将被忽略。若指定的模块名称均无效，命令会返回失败提示信息。
<<< END U009185 >>>
<<< UNIT U009186 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:16-20 | ctx=`set target module enable` >>>
审阅次数：10
  :log="[
    '用户：~set target module enable QQ|Group|123456789 wiki',
    '机器人：成功为群聊开启以下模块：wiki',
  ]"
/>
<<< END U009186 >>>
<<< UNIT U009187 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:26-26 | ctx=`set target module disable` >>>
审阅次数：10
此命令在目标场景停用模块，仅处理该场景已启用的模块。
<<< END U009187 >>>
<<< UNIT U009188 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:29-33 | ctx=`set target module disable` >>>
审阅次数：10
  :log="[
    '用户：~set target module disable QQ|Group|123456789 wiki',
    '机器人：成功为群聊关闭以下模块：wiki',
  ]"
/>
<<< END U009188 >>>
<<< UNIT U009189 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:39-39 | ctx=`set target module list` >>>
审阅次数：10
此命令列出目标场景已启用的模块，并按照名称排序。
<<< END U009189 >>>
<<< UNIT U009190 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:42-47 | ctx=`set target module list` >>>
审阅次数：10
  :log="[
    '用户：~set target module list QQ|Group|123456789',
    '机器人：此群聊已开启的模块：',
    'dice | wiki',
  ]"
/>
<<< END U009190 >>>
<<< UNIT U009191 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:53-53 | ctx=`set target data get` >>>
审阅次数：10
此命令读取场景数据。省略键名称时列出全部键值对，指定键名称时仅返回对应键的值。常见的场景数据键包括 `command_prefix` 与 `cooldown_time`。
<<< END U009191 >>>
<<< UNIT U009192 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:56-60 | ctx=`set target data get` >>>
审阅次数：10
  :log="[
    '用户：~set target data get QQ|Group|123456789 cooldown_time',
    '机器人：5',
  ]"
/>
<<< END U009192 >>>
<<< UNIT U009193 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:66-66 | ctx=`set target data edit` >>>
审阅次数：10
此命令写入场景数据。传入值 `<v>` 为 `[...]` 或 `{...}` 时按照 JSON 解析。若值为 `true` 或 `false` 则存储为布尔值，其余情况均作为字符串写入。
<<< END U009193 >>>
<<< UNIT U009194 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:69-73 | ctx=`set target data edit` >>>
审阅次数：10
  :log="[
    '用户：~set target data edit QQ|Group|123456789 cooldown_time 5',
    '机器人：成功为群聊设置了以下参数：cooldown_time -> 5',
  ]"
/>
<<< END U009194 >>>
<<< UNIT U009195 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:79-79 | ctx=`set target data delete` >>>
审阅次数：10
此命令删除指定的场景数据键。
<<< END U009195 >>>
<<< UNIT U009196 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:82-86 | ctx=`set target data delete` >>>
审阅次数：10
  :log="[
    '用户：~set target data delete QQ|Group|123456789 cooldown_time',
    '机器人：成功。',
  ]"
/>
<<< END U009196 >>>
<<< UNIT U009197 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:92-92 | ctx=`set sender data get` >>>
审阅次数：10
此命令读取用户数据。省略键名称时列出全部键值对，指定键名称时仅返回对应键的值。常见的用户数据键包括 `typing_prompt` 与 `module_auth`。
<<< END U009197 >>>
<<< UNIT U009198 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:95-99 | ctx=`set sender data get` >>>
审阅次数：10
  :log="[
    '用户：~set sender data get QQ|123456 dark_mode',
    '机器人：True',
  ]"
/>
<<< END U009198 >>>
<<< UNIT U009199 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:105-105 | ctx=`set sender data edit` >>>
审阅次数：10
此命令写入用户数据，值的解析规则与 `set target data edit` 保持一致。
<<< END U009199 >>>
<<< UNIT U009200 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:108-112 | ctx=`set sender data edit` >>>
审阅次数：10
  :log="[
    '用户：~set sender data edit QQ|123456 dark_mode true',
    '机器人：成功为群聊设置了以下参数：dark_mode -> True',
  ]"
/>
<<< END U009200 >>>
<<< UNIT U009201 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:118-118 | ctx=`set sender data delete` >>>
审阅次数：10
此命令删除指定的用户数据键。
<<< END U009201 >>>
<<< UNIT U009202 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/set.md:121-125 | ctx=`set sender data delete` >>>
审阅次数：10
  :log="[
    '用户：~set sender data delete QQ|123456 dark_mode',
    '机器人：成功。',
  ]"
/>
<<< END U009202 >>>
<<< UNIT U009203 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:7-7 | ctx=setup >>>
审阅次数：10
此模块用于查看与修改机器人的设置。别名 `toggle`、`prefix`、`locale`、`lang` 与 `alias` 各自指向一条子命令。
<<< END U009203 >>>
<<< UNIT U009204 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:9-9 | ctx=setup >>>
审阅次数：10
这些命令分别作用于场景域与个人域。
`setup list` 展示全部设置项。
<<< END U009204 >>>
<<< UNIT U009205 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:15-15 | ctx=`setup typing` >>>
审阅次数：10
切换“正在输入”状态提示。此开关默认处于开启状态，设置保存在个人域。
<<< END U009205 >>>
<<< UNIT U009206 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:18-22 | ctx=`setup typing` >>>
审阅次数：10
  :log="[
    '用户：~setup typing',
    '机器人：已关闭输入提示。',
  ]"
/>
<<< END U009206 >>>
<<< UNIT U009207 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:28-28 | ctx=`setup check` >>>
审阅次数：10
切换命令拼写检查。此开关默认处于开启状态，设置保存在个人域。
<<< END U009207 >>>
<<< UNIT U009208 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:31-35 | ctx=`setup check` >>>
审阅次数：10
  :log="[
    '用户：~setup check',
    '机器人：已关闭命令语法检查提示。',
  ]"
/>
<<< END U009208 >>>
<<< UNIT U009209 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:41-41 | ctx=`setup markdown` >>>
审阅次数：10
切换 Markdown 渲染开关，设置保存在个人域。若平台不支持 Markdown，机器人会返回提示信息，原设置保持不变。
<<< END U009209 >>>
<<< UNIT U009210 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:44-48 | ctx=`setup markdown` >>>
审阅次数：10
  :log="[
    '用户：~setup markdown',
    '机器人：此平台不支持 Markdown 消息。',
  ]"
/>
<<< END U009210 >>>
<<< UNIT U009211 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:54-54 | ctx=`setup dark` >>>
审阅次数：10
切换深色模式开关，设置保存在个人域。
<<< END U009211 >>>
<<< UNIT U009212 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:57-61 | ctx=`setup dark` >>>
审阅次数：10
  :log="[
    '用户：~setup dark',
    '机器人：已开启深色模式。',
  ]"
/>
<<< END U009212 >>>
<<< UNIT U009213 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:67-67 | ctx=`setup list` >>>
审阅次数：10
展示设置面板。若省略域参数，面板会同时列出场景域与个人域。场景域的修改入口仅向场景管理员显示，个人域向所有用户开放。
<<< END U009213 >>>
<<< UNIT U009214 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:70-76 | ctx=`setup list` >>>
审阅次数：10
  :log="[
    '用户：~setup list',
    '机器人：【群聊设置】',
    '语言：简体中文 修改（`~setup locale zh_cn`）',
    '禁止发言：已关闭 开启（`~mute`）',
  ]"
/>
<<< END U009214 >>>
<<< UNIT U009215 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:82-82 | ctx=`setup prefix list` >>>
审阅次数：10
列出默认命令前缀与当前场景的自定义前缀。
<<< END U009215 >>>
<<< UNIT U009216 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:85-90 | ctx=`setup prefix list` >>>
审阅次数：10
  :log="[
    '用户：~setup prefix list',
    '机器人：默认命令前缀：~, ～',
    '自定义命令前缀为空。',
  ]"
/>
<<< END U009216 >>>
<<< UNIT U009217 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:96-96 | ctx=`setup prefix add` >>>
审阅次数：10
为当前场景添加命令前缀。若前缀已经存在，机器人会返回重复提示信息。
<<< END U009217 >>>
<<< UNIT U009218 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:99-103 | ctx=`setup prefix add` >>>
审阅次数：10
  :log="[
    '用户：~setup prefix add !',
    '机器人：已添加自定义命令前缀：!',
  ]"
/>
<<< END U009218 >>>
<<< UNIT U009219 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:109-109 | ctx=`setup prefix remove` >>>
审阅次数：10
移除当前场景的命令前缀。若前缀不存在，机器人会返回未找到提示信息。
<<< END U009219 >>>
<<< UNIT U009220 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:112-116 | ctx=`setup prefix remove` >>>
审阅次数：10
  :log="[
    '用户：~setup prefix remove !',
    '机器人：已移除自定义命令前缀：!',
  ]"
/>
<<< END U009220 >>>
<<< UNIT U009221 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:122-122 | ctx=`setup prefix reset` >>>
审阅次数：10
清空当前场景的自定义命令前缀列表。
<<< END U009221 >>>
<<< UNIT U009222 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:125-129 | ctx=`setup prefix reset` >>>
审阅次数：10
  :log="[
    '用户：~setup prefix reset',
    '机器人：已重置自定义命令前缀列表。',
  ]"
/>
<<< END U009222 >>>
<<< UNIT U009223 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:135-135 | ctx=`setup locale` >>>
审阅次数：10
若省略语言代码，则列出可用语言及其各自的翻译进度。若指定语言代码，命令会设置场景的语言，该操作需要场景管理员权限。若语言代码未包含在可用列表中，机器人会返回提示信息并列出可选值。
<<< END U009223 >>>
<<< UNIT U009224 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:138-144 | ctx=`setup locale` >>>
审阅次数：10
  :log="[
    '用户：~setup locale',
    '机器人：当前使用的语言：简体中文',
    '使用“`~setup locale <语言代码>`”设置语言。',
    '支持的语言列表：\n简体中文\n繁體中文\nEnglish\n日本語\n한국어',
  ]"
/>
<<< END U009224 >>>
<<< UNIT U009225 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:150-150 | ctx=`setup locale reload` >>>
审阅次数：10
重新加载语言文件。加载失败时返回提示，并列出出错的文件。
<<< END U009225 >>>
<<< UNIT U009226 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:153-157 | ctx=`setup locale reload` >>>
审阅次数：10
  :log="[
    '用户：~setup locale reload',
    '机器人：成功。',
  ]"
/>
<<< END U009226 >>>
<<< UNIT U009227 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:163-163 | ctx=`setup alias list` >>>
审阅次数：10
列出场景自定义命令别名。结果默认渲染为图片表格，加 `--legacy` 时改用文本表格。
<<< END U009227 >>>
<<< UNIT U009228 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:166-171 | ctx=`setup alias list` >>>
审阅次数：10
  :log="[
    '用户：~setup alias list --legacy',
    '机器人：自定义命令别名列表：',
    'wk -> ~wiki',
  ]"
/>
<<< END U009228 >>>
<<< UNIT U009229 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:177-177 | ctx=`setup alias add` >>>
审阅次数：10
为当前场景添加命令别名。替换文本必须以命令前缀开头。
<<< END U009229 >>>
<<< UNIT U009230 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:179-179 | ctx=`setup alias add` >>>
审阅次数：10
别名与替换文本均不能仅由占位符构成，且必须包含占位符之外的正文字符，占位符写作 `${名称}`。若不满足上述条件，机器人会返回对应提示信息。若别名重复，则返回已存在提示信息。
<<< END U009230 >>>
<<< UNIT U009231 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:182-186 | ctx=`setup alias add` >>>
审阅次数：10
  :log="[
    '用户：~setup alias add wk ~wiki',
    '机器人：已添加自定义命令别名：wk -> ~wiki',
  ]"
/>
<<< END U009231 >>>
<<< UNIT U009232 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:192-192 | ctx=`setup alias remove` >>>
审阅次数：10
移除当前场景的自定义命令别名。
<<< END U009232 >>>
<<< UNIT U009233 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:195-199 | ctx=`setup alias remove` >>>
审阅次数：10
  :log="[
    '用户：~setup alias remove wk',
    '机器人：已移除自定义命令别名：wk',
  ]"
/>
<<< END U009233 >>>
<<< UNIT U009234 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:205-205 | ctx=`setup alias reset` >>>
审阅次数：10
清空当前场景的自定义命令别名列表。
<<< END U009234 >>>
<<< UNIT U009235 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:208-212 | ctx=`setup alias reset` >>>
审阅次数：10
  :log="[
    '用户：~setup alias reset',
    '机器人：已重置自定义命令别名列表。',
  ]"
/>
<<< END U009235 >>>
<<< UNIT U009236 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:218-218 | ctx=`setup timeoffset` >>>
审阅次数：10
设置场景的时区偏移，支持的格式为 `8`、`-5:30`。若小时数值超过 12 或分钟数值达到 60，机器人会返回格式错误提示。写入时统一规范为 `+8`、`-5:30` 的形式。传入参数为 `reset` 时将清除场景偏移，恢复为未设置状态。
<<< END U009236 >>>
<<< UNIT U009237 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:221-225 | ctx=`setup timeoffset` >>>
审阅次数：10
  :log="[
    '用户：~setup timeoffset 8',
    '机器人：已将群聊时区设置为 UTC+8。',
  ]"
/>
<<< END U009237 >>>
<<< UNIT U009238 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:228-232 | ctx=`setup timeoffset` >>>
审阅次数：10
  :log="[
    '用户：~setup timeoffset reset',
    '机器人：已将群聊时区恢复为默认值。',
  ]"
/>
<<< END U009238 >>>
<<< UNIT U009239 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:238-238 | ctx=`setup timezone` >>>
审阅次数：10
设置个人显示时区偏移，该设置会覆盖场景时区，格式与 `setup timeoffset` 保持一致。传入参数为 `reset` 时将清除个人偏移，恢复为跟随场景时区。
<<< END U009239 >>>
<<< UNIT U009240 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:241-245 | ctx=`setup timezone` >>>
审阅次数：10
  :log="[
    '用户：~setup timezone +3',
    '机器人：已将用户显示时区设置为 UTC+3。',
  ]"
/>
<<< END U009240 >>>
<<< UNIT U009241 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:248-252 | ctx=`setup timezone` >>>
审阅次数：10
  :log="[
    '用户：~setup timezone reset',
    '机器人：已恢复跟随群聊时区。',
  ]"
/>
<<< END U009241 >>>
<<< UNIT U009242 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:258-258 | ctx=`setup cooldown` >>>
审阅次数：10
设置场景的命令冷却秒数。负数值均按 0 处理。
<<< END U009242 >>>
<<< UNIT U009243 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:261-265 | ctx=`setup cooldown` >>>
审阅次数：10
  :log="[
    '用户：~setup cooldown 5',
    '机器人：已将命令冷却时间设置为 5 秒。',
  ]"
/>
<<< END U009243 >>>
<<< UNIT U009244 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:271-271 | ctx=`setup invalid-module-prompt` >>>
审阅次数：10
切换未知模块提示信息的开关。
<<< END U009244 >>>
<<< UNIT U009245 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:274-278 | ctx=`setup invalid-module-prompt` >>>
审阅次数：10
  :log="[
    '用户：~setup invalid-module-prompt',
    '机器人：已关闭“模块不存在”提示。',
  ]"
/>
<<< END U009245 >>>
<<< UNIT U009246 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:284-284 | ctx=`setup sign` >>>
审阅次数：10
此命令仅在 `enable_petal` 为 `true` 时注册，用于切换场景的签到开关。该开关默认处于开启状态，`petal` 模块的签到命令会读取此设置。
<<< END U009246 >>>
<<< UNIT U009247 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:290-290 | ctx=`setup emote` >>>
审阅次数：10
此命令仅在 `use_emote` 为 `true` 时注册，用于切换场景的表情开关。
<<< END U009247 >>>
<<< UNIT U009248 | md-heading | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:292-292 | ctx=数据键 >>>
审阅次数：10
## 数据键
<<< END U009248 >>>
<<< UNIT U009249 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:294-294 | ctx=数据键 >>>
审阅次数：10
`setup` 与 `set` 写入的键存储在 union 的 JSON 列中：
<<< END U009249 >>>
<<< UNIT U009250 | md-table | packages/akari-bot-core/akaribot/modules/core/docs/setup.md:296-309 | ctx=数据键 >>>
审阅次数：10
| 域 | 键 | 用途 |
| --- | --- | --- |
| 场景 | `command_prefix` | 自定义命令前缀 |
| 场景 | `command_alias` | 自定义命令别名 |
| 场景 | `cooldown_time` | 命令冷却秒数 |
| 场景 | `timezone_offset` | 时区偏移 |
| 场景 | `invalid_module_prompt` | 未知模块提示开关 |
| 场景 | `use_emote` | 表情开关 |
| 场景 | `petal_sign` | 签到开关 |
| 个人 | `typing_prompt` | 输入状态提示 |
| 个人 | `typo_check` | 拼写检查 |
| 个人 | `use_markdown` | Markdown 渲染 |
| 个人 | `dark_mode` | 深色模式 |
| 个人 | `timezone_offset` | 显示时区偏移 |
<<< END U009250 >>>
<<< UNIT U009251 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/superuser.md:9-9 | ctx=superuser >>>
审阅次数：10
此模块用于维护超级用户名单。模块内全部命令均需要超级用户权限。
<<< END U009251 >>>
<<< UNIT U009252 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/superuser.md:15-15 | ctx=`superuser add` >>>
审阅次数：10
此命令将用户设置为超级用户。若该用户尚未包含 union 记录，机器人会先请求确认，确认通过后再创建记录。
<<< END U009252 >>>
<<< UNIT U009253 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/superuser.md:18-22 | ctx=`superuser add` >>>
审阅次数：10
  :log="[
    '用户：~superuser add QQ|123456',
    '机器人：成功将用户 QQ|123456 设置为超级用户。',
  ]"
/>
<<< END U009253 >>>
<<< UNIT U009254 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/superuser.md:28-28 | ctx=`superuser remove` >>>
审阅次数：10
此命令撤销用户的超级用户身份。移除当前操作者时，机器人会要求输入确认内容。`config.toml` 中的 `base_superuser` 是基础超级用户名单，启动时写入数据库，仅可通过配置文件维护。
<<< END U009254 >>>
<<< UNIT U009255 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/superuser.md:31-35 | ctx=`superuser remove` >>>
审阅次数：10
  :log="[
    '用户：~superuser remove QQ|123456',
    '机器人：成功将用户 QQ|123456 移出超级用户。',
  ]"
/>
<<< END U009255 >>>
<<< UNIT U009256 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/telemetry.md:8-8 | ctx=telemetry >>>
审阅次数：10
此 Hook 挂载在 `EXECUTION_FINISHED` 与 `FINISHED` 两个位置，用于统计命令执行与消息解析的次数。
<<< END U009256 >>>
<<< UNIT U009257 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/telemetry.md:10-10 | ctx=telemetry >>>
审阅次数：10
说明：
<<< END U009257 >>>
<<< UNIT U009258 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/telemetry.md:12-15 | ctx=telemetry >>>
审阅次数：10
- 每次执行命令或匹配正则表达式时，`Info.command_parsed` 加一。
- 每条消息解析结束时，`Info.message_parsed` 加一。
- 若 `enable_analytics` 处于开启状态，同时写入 `analytics_data`，记录场景、发送者、命令、模块和模块类型。
- 若写入失败，仅记录日志，命令仍然正常结束。
<<< END U009258 >>>
<<< UNIT U009259 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/telemetry.md:17-17 | ctx=telemetry >>>
审阅次数：10
若 `enable_analytics` 处于关闭状态，不再向数据表写入记录，进程内计数则继续累加。
<<< END U009259 >>>
<<< UNIT U009260 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/tos.md:8-8 | ctx=tos >>>
审阅次数：10
此 Hook 基于令牌桶算法限制命令与正则表达式的调用频率。超出限制后，机器人将临时限制该发送者。
<<< END U009260 >>>
<<< UNIT U009261 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/tos.md:10-10 | ctx=tos >>>
审阅次数：10
说明：
<<< END U009261 >>>
<<< UNIT U009262 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/tos.md:12-15 | ctx=tos >>>
审阅次数：10
- 配置项包括 `enable_tos`、`tos_warning_counts`、`tos_temp_ban_time` 与 `report_targets`。
- 机器人在 `COMMAND_BEFORE_PARSE` 与 `REGEX_BEFORE_EXECUTE` 阶段计数，在 `COMMAND_PREPARE` 与 `REGEX_PREPARE` 阶段检查发送者是否处于临时限制状态。
- `EXECUTION_ERROR` 捕获 `AbuseWarning`。警告次数超过 `tos_warning_counts` 后，机器人将临时限制该发送者，限制时长通过 `tos_temp_ban_time` 控制，默认 300 秒。
- 模块提供命名 Hook（`check_temp_ban`、`remove_temp_ban`、`report` 与 `warning_counts`），供 `abuse` 等模块调用。
<<< END U009262 >>>
<<< UNIT U009263 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/typo.md:8-8 | ctx=typo >>>
审阅次数：10
此 Hook 在命令未匹配到任何模块时提供拼写纠错建议。
<<< END U009263 >>>
<<< UNIT U009264 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/typo.md:10-10 | ctx=typo >>>
审阅次数：10
说明：
<<< END U009264 >>>
<<< UNIT U009265 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/typo.md:12-15 | ctx=typo >>>
审阅次数：10
- 仅在 `unmatched_kind == "module"` 且用户未关闭 `typo_check` 时触发。
- 相似度阈值取自 `typo_check_module_score`、`typo_check_command_score`、`typo_check_args_score` 与 `typo_check_options_score`。
- 长度差异比例通过 `typo_check_module_diff_ratio` 控制。
- Hook 将修复建议封装在 `RecoveryProposal` 中返回。是否重试纠正后的命令，通过解析器确定。
<<< END U009265 >>>
<<< UNIT U009266 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/update-restart.md:9-9 | ctx=update&restart >>>
审阅次数：10
此模块用于更新机器人并重启进程。模块内的命令均需要超级用户权限。
<<< END U009266 >>>
<<< UNIT U009267 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/update-restart.md:15-15 | ctx=`update&restart` >>>
审阅次数：10
此命令不注册至 Web 平台，仅在子进程模式下可用。执行时首先执行更新，随后进入重启流程。
<<< END U009267 >>>
<<< UNIT U009268 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/update-restart.md:17-17 | ctx=`update&restart` >>>
审阅次数：10
指定 `--force` 选项时跳过确认与等待。未指定该选项时，需要先完成确认，确认通过后等待其他正在执行的命令结束。更新报告发送后，进程按照 `restart` 的流程退出，通过守护进程重新启动全部子进程。
<<< END U009268 >>>
<<< UNIT U009269 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/update-restart.md:20-25 | ctx=`update&restart` >>>
审阅次数：10
  :log="[
    '用户：~update&restart --force',
    '机器人：重启中……',
    '更新成功：3 个包（CLI：/usr/local/bin/akaribot，退出码 0）。',
  ]"
/>
<<< END U009269 >>>
<<< UNIT U009270 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/update.md:7-7 | ctx=update >>>
审阅次数：10
此模块用于更新机器人及其依赖项。模块内命令均需要超级用户权限。
<<< END U009270 >>>
<<< UNIT U009271 | md-list | packages/akari-bot-core/akaribot/modules/core/docs/update.md:13-17 | ctx=`update` >>>
审阅次数：10
- 更新通过 `akaribot module update --all --non-interactive --defer-runtime --json` 执行。
- 更新在 CLI 子进程中执行。机器人与 Server 进程仅读取配置，不直接写入磁盘，亦不迁移数据库。
- 二进制封装模式下，命令会拒绝执行，并提示手动下载新版本完成替换。
- 执行报告列出成功、失败与跳过的包。
- 若存在尚未热加载的包，机器人会提示执行 `restart`。若全部包均已热加载，报告则说明已全部完成热加载。
<<< END U009271 >>>
<<< UNIT U009272 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/update.md:20-26 | ctx=`update` >>>
审阅次数：10
  :log="[
    '用户：~update',
    '机器人：更新成功：3 个包（CLI：/usr/local/bin/akaribot，退出码 0）。',
    '成功：akari-bot-core、akari-bot-module-dice、akari-bot-module-petal',
    '以下包尚未热装载：akari-bot-core；请执行 `~restart` 让新版本生效。',
  ]"
/>
<<< END U009272 >>>
<<< UNIT U009273 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:7-7 | ctx=url-audit >>>
审阅次数：10
此模块用于维护全局 URL 允许规则与阻止规则。模块内命令要求超级用户权限。规则存储在实例的 `data/url_audit/` 目录中，是否启用通过 `enable_urlmanager` 配置项控制。
<<< END U009273 >>>
<<< UNIT U009274 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:13-13 | ctx=`url-audit allowlist add` >>>
审阅次数：10
向用户自定义的全局允许列表添加一条精确 URL 规则。若规则已经存在，则返回提示信息。
<<< END U009274 >>>
<<< UNIT U009275 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:16-20 | ctx=`url-audit allowlist add` >>>
审阅次数：10
  :log="[
    '用户：~url-audit allowlist add https://example.com/news/1',
    '机器人：已将规则加入用户自定义 URL 允许列表：https://example.com/news/1',
  ]"
/>
<<< END U009275 >>>
<<< UNIT U009276 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:26-26 | ctx=`url-audit allowlist add-regex` >>>
审阅次数：10
向允许列表添加正则表达式规则。正则表达式必须能够完整匹配目标 URL。若规则不合法，机器人会返回具体原因。
<<< END U009276 >>>
<<< UNIT U009277 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:29-33 | ctx=`url-audit allowlist add-regex` >>>
审阅次数：10
  :log="[
    '用户：~url-audit allowlist add-regex https://example.com/(news|blog)/.*',
    '机器人：已将规则加入用户自定义 URL 允许列表：regex:https://example.com/(news|blog)/.*',
  ]"
/>
<<< END U009277 >>>
<<< UNIT U009278 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:39-39 | ctx=`url-audit allowlist remove` >>>
审阅次数：10
从允许列表移除精确 URL 规则。若规则不存在，则返回提示信息。
<<< END U009278 >>>
<<< UNIT U009279 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:42-46 | ctx=`url-audit allowlist remove` >>>
审阅次数：10
  :log="[
    '用户：~url-audit allowlist remove https://example.com/news/1',
    '机器人：已从用户自定义 URL 允许列表删除规则：https://example.com/news/1',
  ]"
/>
<<< END U009279 >>>
<<< UNIT U009280 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:52-52 | ctx=`url-audit allowlist remove-regex` >>>
审阅次数：10
从全局允许列表中移除正则表达式规则。
<<< END U009280 >>>
<<< UNIT U009281 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:55-59 | ctx=`url-audit allowlist remove-regex` >>>
审阅次数：10
  :log="[
    '用户：~url-audit allowlist remove-regex https://example.com/(news|blog)/.*',
    '机器人：已从用户自定义 URL 允许列表删除规则：regex:https://example.com/(news|blog)/.*',
  ]"
/>
<<< END U009281 >>>
<<< UNIT U009282 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:65-65 | ctx=`url-audit allowlist query` >>>
审阅次数：10
查询 URL 匹配的允许规则，逐条列出规则来源与内容。若未匹配到规则，则提示该 URL 未被允许。
<<< END U009282 >>>
<<< UNIT U009283 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:68-73 | ctx=`url-audit allowlist query` >>>
审阅次数：10
  :log="[
    '用户：~url-audit allowlist query https://example.com/news/1',
    '机器人：https://example.com/news/1 已被以下全局规则放行：',
    '[用户规则] regex:https://example.com/(news|blog)/.*',
  ]"
/>
<<< END U009283 >>>
<<< UNIT U009284 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:79-79 | ctx=`url-audit allowlist list` >>>
审阅次数：10
列出全部允许规则，以图片表格展示来源、类型与规则内容。若列表为空，则返回提示信息。
<<< END U009284 >>>
<<< UNIT U009285 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:82-87 | ctx=`url-audit allowlist list` >>>
审阅次数：10
  :log="[
    '用户：~url-audit allowlist list',
    '机器人：全局 URL 允许列表规则：',
    '（图片表格：来源 / 类型 / 规则）',
  ]"
/>
<<< END U009285 >>>
<<< UNIT U009286 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:93-93 | ctx=`url-audit blocklist add` >>>
审阅次数：10
向用户自定义的全局阻止列表添加一条精确 URL 规则。若规则已经存在，则返回提示信息。
<<< END U009286 >>>
<<< UNIT U009287 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:96-100 | ctx=`url-audit blocklist add` >>>
审阅次数：10
  :log="[
    '用户：~url-audit blocklist add https://example.com/ads/1',
    '机器人：已将规则加入用户自定义 URL 阻止列表：https://example.com/ads/1',
  ]"
/>
<<< END U009287 >>>
<<< UNIT U009288 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:106-106 | ctx=`url-audit blocklist add-regex` >>>
审阅次数：10
向阻止列表添加正则表达式规则。正则表达式必须能够完整匹配目标 URL。若规则不合法，机器人会返回具体原因。
<<< END U009288 >>>
<<< UNIT U009289 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:109-113 | ctx=`url-audit blocklist add-regex` >>>
审阅次数：10
  :log="[
    '用户：~url-audit blocklist add-regex https://example.com/ads/.*',
    '机器人：已将规则加入用户自定义 URL 阻止列表：regex:https://example.com/ads/.*',
  ]"
/>
<<< END U009289 >>>
<<< UNIT U009290 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:119-119 | ctx=`url-audit blocklist remove` >>>
审阅次数：10
从阻止列表移除精确 URL 规则。若规则不存在，则返回提示信息。
<<< END U009290 >>>
<<< UNIT U009291 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:122-126 | ctx=`url-audit blocklist remove` >>>
审阅次数：10
  :log="[
    '用户：~url-audit blocklist remove https://example.com/ads/1',
    '机器人：已从用户自定义 URL 阻止列表删除规则：https://example.com/ads/1',
  ]"
/>
<<< END U009291 >>>
<<< UNIT U009292 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:132-132 | ctx=`url-audit blocklist remove-regex` >>>
审阅次数：10
从全局阻止列表中移除正则表达式规则。
<<< END U009292 >>>
<<< UNIT U009293 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:135-139 | ctx=`url-audit blocklist remove-regex` >>>
审阅次数：10
  :log="[
    '用户：~url-audit blocklist remove-regex https://example.com/ads/.*',
    '机器人：已从用户自定义 URL 阻止列表删除规则：regex:https://example.com/ads/.*',
  ]"
/>
<<< END U009293 >>>
<<< UNIT U009294 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:145-145 | ctx=`url-audit blocklist query` >>>
审阅次数：10
查询 URL 匹配的阻止规则。若未匹配到任何规则，则提示该 URL 未被阻止。
<<< END U009294 >>>
<<< UNIT U009295 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:148-153 | ctx=`url-audit blocklist query` >>>
审阅次数：10
  :log="[
    '用户：~url-audit blocklist query https://example.com/ads/1',
    '机器人：https://example.com/ads/1 已被以下全局规则拦截：',
    '[用户规则] https://example.com/ads/1',
  ]"
/>
<<< END U009295 >>>
<<< UNIT U009296 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:159-159 | ctx=`url-audit blocklist list` >>>
审阅次数：10
列出全部阻止规则，以图片表格展示来源、类型与规则内容。若列表为空，则返回提示信息。
<<< END U009296 >>>
<<< UNIT U009297 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/url-audit.md:162-167 | ctx=`url-audit blocklist list` >>>
审阅次数：10
  :log="[
    '用户：~url-audit blocklist list',
    '机器人：全局 URL 阻止列表规则：',
    '（图片表格：来源 / 类型 / 规则）',
  ]"
/>
<<< END U009297 >>>
<<< UNIT U009298 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/webrender.md:7-7 | ctx=webrender >>>
审阅次数：10
此模块用于控制网页渲染服务。模块内全部命令均需要超级用户权限。
<<< END U009298 >>>
<<< UNIT U009299 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/webrender.md:13-13 | ctx=`webrender status` >>>
审阅次数：10
输出网页渲染服务的当前状态。
<<< END U009299 >>>
<<< UNIT U009300 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/webrender.md:19-19 | ctx=`webrender start` >>>
审阅次数：10
启动本地渲染服务。启动成功后重新检查渲染状态，并将结果写入运行时记录。
<<< END U009300 >>>
<<< UNIT U009301 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/webrender.md:25-25 | ctx=`webrender stop` >>>
审阅次数：10
停止渲染服务，随后重新检查渲染状态，并将结果写入运行时记录。
<<< END U009301 >>>
<<< UNIT U009302 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/webrender.md:28-32 | ctx=`webrender stop` >>>
审阅次数：10
  :log="[
    '用户：~webrender stop',
    '机器人：成功。',
  ]"
/>
<<< END U009302 >>>
<<< UNIT U009303 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/webrender.md:38-38 | ctx=`webrender reload` >>>
审阅次数：10
先停止再启动渲染服务，用于重新加载配置。
<<< END U009303 >>>
<<< UNIT U009304 | md-paragraph | packages/akari-bot-core/akaribot/modules/core/docs/webrender.md:40-40 | ctx=`webrender reload` >>>
审阅次数：10
服务参数位于 `config/webrender.toml`，包括 `enable`、`browser_type`、`browser_executable_path`、`headless`、`remote_only` 与 `remote_web_render_url`。当渲染服务不可用时，依赖截图的命令会自行处理失败结果，例如回退为文字，或直接终止且不发送图片。
<<< END U009304 >>>
<<< UNIT U009305 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/__init__.py:1-1 | ctx=<module> >>>
审阅次数：10
Parser 生命周期策略与观察 Hook。
<<< END U009305 >>>
<<< UNIT U009306 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/errors.py:137-138 >>>
审阅次数：10
# SendMessageFailed 继承 BaseException，是消息会话控制流的一部分，不可使用
# ``Exception`` 作为入口过滤，否则发送失败会被解析器误判定为未处理异常。
<<< END U009306 >>>
<<< UNIT U009307 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/errors.py:1-1 | ctx=<module> >>>
审阅次数：10
parser 执行异常的默认用户反馈与报告策略。
<<< END U009307 >>>
<<< UNIT U009308 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/errors.py:65-65 | ctx=format_error_detail >>>
审阅次数：10
按目标平台能力格式化错误详情。支持 Markdown 时使用 Markdown 代码块。
<<< END U009308 >>>
<<< UNIT U009309 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/policies.py:27-27 >>>
审阅次数：10
# 场景冷却属于策略状态。通过模块 runtime 管理，在同版本热重载时予以保留。
<<< END U009309 >>>
<<< UNIT U009310 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/policies.py:101-102 >>>
审阅次数：10
# 必须在候选模块匹配阶段拦截，因为未匹配的模块会进入纠错与默认提示流程，相关路径不会
# 经过 :attr:`HookPoint.COMMAND_PREPARE`，若置于模板解析之前则无法实现完整拦截。
<<< END U009310 >>>
<<< UNIT U009311 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/policies.py:110-111 >>>
审阅次数：10
# 被动回复已由 :func:`_command_muted` / :func:`_regex_route` 控制，此处仅拦截
# 主动获取的会话（``fetch``），避免将 `mute` 命令本身的确认流程一并取消。
<<< END U009311 >>>
<<< UNIT U009312 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/policies.py:1-1 | ctx=<module> >>>
审阅次数：10
消息入口的内置策略。
<<< END U009312 >>>
<<< UNIT U009313 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/retired.py:28-29 >>>
审阅次数：10
# 模块别名可以将白名单命令并入其他模块（merge 解析为 bind），此时模块名不在
# 白名单内，回退至用户别名改写前实际输入的首词继续判定。其他首词依然统一予以拦截。
<<< END U009313 >>>
<<< UNIT U009314 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/retired.py:1-1 | ctx=<module> >>>
审阅次数：10
退役客户端的消息路由策略。
<<< END U009314 >>>
<<< UNIT U009315 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/routing.py:58-58 >>>
审阅次数：10
# 查询与写入操作之间不得使用 await。此处依赖单线程事件循环维持抢占原子性。
<<< END U009315 >>>
<<< UNIT U009316 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/routing.py:1-1 | ctx=<module> >>>
审阅次数：10
同通道消息认领策略。
<<< END U009316 >>>
<<< UNIT U009317 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/telemetry.py:42-42 >>>
审阅次数：10
# 采集失败不得影响命令收尾与正则表达式遍历。
<<< END U009317 >>>
<<< UNIT U009318 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/telemetry.py:1-1 | ctx=<module> >>>
审阅次数：10
通过 parser 观察入口写入 AnalyticsData 与 Info 计数。
<<< END U009318 >>>
<<< UNIT U009319 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:67-67 >>>
审阅次数：10
# 同版本 reload 保留限流与临时封禁状态。版本变化时重建。
<<< END U009319 >>>
<<< UNIT U009320 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:80-80 >>>
审阅次数：10
# 临时限制计数在同版本热重载时予以保留，版本发生变化时重新构建。
<<< END U009320 >>>
<<< UNIT U009321 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:118-118 >>>
审阅次数：10
# 上报场景按场景组配置，展开后同一现实场景的多个平台入口仅应由其中一个入口接收回传消息。
<<< END U009321 >>>
<<< UNIT U009322 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:130-130 >>>
审阅次数：10
# 没有用户 union 的会话（如主动推送）不存在可警告的对象，直接跳过。
<<< END U009322 >>>
<<< UNIT U009323 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:197-197 >>>
审阅次数：10
# 升级限制时拒绝决定已经生成，通知失败不得将其误判定为“放行”。
<<< END U009323 >>>
<<< UNIT U009324 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:227-228 >>>
审阅次数：10
# 超限属于已确定的业务拒绝，需要先固定 Stop 再尽力完成通知流程，
# 上报与提示发送失败不得将已确认超限的命令予以放行。
<<< END U009324 >>>
<<< UNIT U009325 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:245-245 >>>
审阅次数：10
# 与“检查本身失败时降级”不同，此处业务拒绝已经形成，丢失通知不能连带丢失拒绝决定。
<<< END U009325 >>>
<<< UNIT U009326 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:249-250 >>>
审阅次数：10
# 发送失败等框架控制流继承 BaseException。拒绝决定已经生成，不可由 executor
# 将通知失败视作检查失败后予以放行。外部取消与进程退出仍然必须向外传播。
<<< END U009326 >>>
<<< UNIT U009327 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:265-265 >>>
审阅次数：10
# 强制检查不设置超时（``timeout=0``）。外部取消仍然向外传播，不可因 Hook 超时而降级放行。
<<< END U009327 >>>
<<< UNIT U009328 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:314-314 >>>
审阅次数：10
# 供管理命令与 Client RPC（OneBot 等）使用的命名功能。
<<< END U009328 >>>
<<< UNIT U009329 | py-comment | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:335-336 >>>
审阅次数：10
# 客户端通过 ``ServerAPI.trigger_hook("tos.report", ...)`` 调用，
# 上报（SMTP 邮件或上报场景）与场景组展开在 Server 进程完成。
<<< END U009329 >>>
<<< UNIT U009330 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:1-1 | ctx=<module> >>>
审阅次数：10
ToS 限流、临时封禁与滥用上报。
<<< END U009330 >>>
<<< UNIT U009331 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/tos.py:107-107 | ctx=tos_report >>>
审阅次数：10
上报滥用行为。
<<< END U009331 >>>
<<< UNIT U009332 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/typo.py:1-1 | ctx=<module> >>>
审阅次数：10
通过 ``parser.command.unmatched`` 返回命令纠错建议（RecoveryProposal）。
<<< END U009332 >>>
<<< UNIT U009333 | py-docstring | packages/akari-bot-core/akaribot/modules/core/hooks/typo.py:43-43 | ctx=suggest_correction >>>
审阅次数：10
计算纠错建议。若无建议则返回 None，且不请求用户确认。
<<< END U009333 >>>
<<< UNIT U009334 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:2-2 | ctx=core.help.about >>>
审阅次数：10
查看关于机器人与开发人员的信息。
<<< END U009334 >>>
<<< UNIT U009335 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:3-3 | ctx=core.help.about.credits >>>
审阅次数：10
查看开发人员名单。
<<< END U009335 >>>
<<< UNIT U009336 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:4-4 | ctx=core.help.about.permissions >>>
审阅次数：10
查看 QQ 官方机器人所需的群聊权限。
<<< END U009336 >>>
<<< UNIT U009337 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:5-5 | ctx=core.help.about.ping >>>
审阅次数：10
查看机器人的运行状态。
<<< END U009337 >>>
<<< UNIT U009338 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:6-6 | ctx=core.help.about.status >>>
审阅次数：10
查看机器人的详细运行状态。
<<< END U009338 >>>
<<< UNIT U009339 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:7-7 | ctx=core.help.about.version >>>
审阅次数：10
查看机器人的版本号。
<<< END U009339 >>>
<<< UNIT U009340 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:8-8 | ctx=core.help.abuse.ban >>>
审阅次数：10
将指定用户加入黑名单。
<<< END U009340 >>>
<<< UNIT U009341 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:9-9 | ctx=core.help.abuse.block >>>
审阅次数：10
将指定{TERM:target}加入黑名单。
<<< END U009341 >>>
<<< UNIT U009342 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:10-10 | ctx=core.help.abuse.check >>>
审阅次数：10
查看用户的警告与封禁状态。
<<< END U009342 >>>
<<< UNIT U009343 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:11-11 | ctx=core.help.abuse.clear >>>
审阅次数：10
清除用户的警告记录。
<<< END U009343 >>>
<<< UNIT U009344 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:12-12 | ctx=core.help.abuse.distrust >>>
审阅次数：10
将指定用户移出白名单。
<<< END U009344 >>>
<<< UNIT U009345 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:13-13 | ctx=core.help.abuse.revoke >>>
审阅次数：10
撤销用户的警告。
<<< END U009345 >>>
<<< UNIT U009346 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:14-14 | ctx=core.help.abuse.trust >>>
审阅次数：10
将指定用户加入白名单。
<<< END U009346 >>>
<<< UNIT U009347 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:15-15 | ctx=core.help.abuse.unban >>>
审阅次数：10
将指定用户移出黑名单。
<<< END U009347 >>>
<<< UNIT U009348 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:16-16 | ctx=core.help.abuse.unblock >>>
审阅次数：10
将指定{TERM:target}移出黑名单。
<<< END U009348 >>>
<<< UNIT U009349 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:17-17 | ctx=core.help.abuse.untempban >>>
审阅次数：10
解除指定用户的临时限制状态。
<<< END U009349 >>>
<<< UNIT U009350 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:18-18 | ctx=core.help.abuse.warn >>>
审阅次数：10
向指定用户发出警告。
<<< END U009350 >>>
<<< UNIT U009351 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:19-19 | ctx=core.help.admin.add >>>
审阅次数：10
将成员设置为机器人管理员。若已属于{TERM:target}管理员则无需重复设置。
<<< END U009351 >>>
<<< UNIT U009352 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:20-20 | ctx=core.help.admin.ban >>>
审阅次数：10
限制指定成员使用机器人。
<<< END U009352 >>>
<<< UNIT U009353 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:21-21 | ctx=core.help.admin.ban.list >>>
审阅次数：10
查看全部被限制使用机器人的成员。
<<< END U009353 >>>
<<< UNIT U009354 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:22-22 | ctx=core.help.admin.desc >>>
审阅次数：10
机器人管理员专用的管理命令。
<<< END U009354 >>>
<<< UNIT U009355 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:23-23 | ctx=core.help.admin.leave >>>
审阅次数：10
使机器人离开群聊。
<<< END U009355 >>>
<<< UNIT U009356 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:24-24 | ctx=core.help.admin.list >>>
审阅次数：10
查看全部机器人管理员。
<<< END U009356 >>>
<<< UNIT U009357 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:25-25 | ctx=core.help.admin.remove >>>
审阅次数：10
移除指定成员的机器人管理员权限。
<<< END U009357 >>>
<<< UNIT U009358 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:26-26 | ctx=core.help.admin.unban >>>
审阅次数：10
解除指定成员使用机器人的限制。
<<< END U009358 >>>
<<< UNIT U009359 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:27-27 | ctx=core.help.alias.add >>>
审阅次数：10
添加自定义命令别名。
<<< END U009359 >>>
<<< UNIT U009360 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:28-28 | ctx=core.help.alias.list >>>
审阅次数：10
查看自定义命令别名列表。
<<< END U009360 >>>
<<< UNIT U009361 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:29-29 | ctx=core.help.alias.remove >>>
审阅次数：10
移除自定义命令别名。
<<< END U009361 >>>
<<< UNIT U009362 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:30-30 | ctx=core.help.alias.reset >>>
审阅次数：10
重置自定义命令别名。
<<< END U009362 >>>
<<< UNIT U009363 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:31-31 | ctx=core.help.analytics >>>
审阅次数：10
查看机器人命令执行统计数据。
<<< END U009363 >>>
<<< UNIT U009364 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:32-32 | ctx=core.help.analytics.days >>>
审阅次数：10
查看最近 30 天的命令执行统计数据。
<<< END U009364 >>>
<<< UNIT U009365 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:33-33 | ctx=core.help.analytics.modules >>>
审阅次数：10
查看各模块命令调用量排行。
<<< END U009365 >>>
<<< UNIT U009366 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:34-34 | ctx=core.help.analytics.year >>>
审阅次数：10
查看最近一年的命令执行统计数据。
<<< END U009366 >>>
<<< UNIT U009367 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:35-35 | ctx=core.help.auth.add >>>
审阅次数：10
授权指定用户使用超级用户模块。
<<< END U009367 >>>
<<< UNIT U009368 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:36-36 | ctx=core.help.auth.list >>>
审阅次数：10
查看指定用户获得的模块授权清单。
<<< END U009368 >>>
<<< UNIT U009369 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:37-37 | ctx=core.help.auth.remove >>>
审阅次数：10
撤销指定用户的模块授权。
<<< END U009369 >>>
<<< UNIT U009370 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:38-38 | ctx=core.help.bind >>>
审阅次数：10
查看当前用户与当前{TERM:target}各自所属的分组。
<<< END U009370 >>>
<<< UNIT U009371 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:39-39 | ctx=core.help.bind.auto >>>
审阅次数：10
自动检索同一{TERM:target}内的其他机器人并合并消息通道。
<<< END U009371 >>>
<<< UNIT U009372 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:40-40 | ctx=core.help.bind.channel >>>
审阅次数：10
查看当前{TERM:target}的消息通道编号与主动推送优先级。
<<< END U009372 >>>
<<< UNIT U009373 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:41-41 | ctx=core.help.bind.channel.internal >>>
审阅次数：10
（内部命令）机器人之间用于确认彼此处于同一{TERM:target}的命令，请勿手动执行。
<<< END U009373 >>>
<<< UNIT U009374 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:42-42 | ctx=core.help.bind.channel.priority.reset >>>
审阅次数：10
将当前{TERM:target}的主动推送优先级恢复为 0。
<<< END U009374 >>>
<<< UNIT U009375 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:43-43 | ctx=core.help.bind.channel.priority.set >>>
审阅次数：10
设置当前{TERM:target}的主动推送优先级（取值范围 0 到 100，数值越大优先级越高）。
<<< END U009375 >>>
<<< UNIT U009376 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:44-44 | ctx=core.help.bind.channel.reset >>>
审阅次数：10
使当前{TERM:target}脱离所在的消息通道，并分配独立的新通道。
<<< END U009376 >>>
<<< UNIT U009377 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:45-45 | ctx=core.help.bind.channel.set >>>
审阅次数：10
手动设置当前{TERM:target}的消息通道编号。
<<< END U009377 >>>
<<< UNIT U009378 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:46-46 | ctx=core.help.bind.desc >>>
审阅次数：10
管理用户组、场景组与消息通道，同一组内的用户或{TERM:target}共享同一份数据。
<<< END U009378 >>>
<<< UNIT U009379 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:47-47 | ctx=core.help.bind.merge >>>
审阅次数：10
机器人将通过私聊发送一枚迁移码。在私聊中执行将同时迁移用户数据与私聊数据，在频道中执行则迁移当前{TERM:target}的数据。
<<< END U009379 >>>
<<< UNIT U009380 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:48-48 | ctx=core.help.bind.merge.desc >>>
审阅次数：10
将当前机器人上的数据迁移至新的机器人。
<<< END U009380 >>>
<<< UNIT U009381 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:49-49 | ctx=core.help.bind.merge.token >>>
审阅次数：10
在新的机器人中输入迁移码以完成数据迁移。
<<< END U009381 >>>
<<< UNIT U009382 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:50-50 | ctx=core.help.bind.self >>>
审阅次数：10
查看当前用户所属的用户组。
<<< END U009382 >>>
<<< UNIT U009383 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:51-51 | ctx=core.help.bind.self.remove >>>
审阅次数：10
将指定用户移出当前所属用户组。
<<< END U009383 >>>
<<< UNIT U009384 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:52-52 | ctx=core.help.bind.start >>>
审阅次数：10
开始绑定流程，机器人将通过私聊发送一枚绑定码。在私聊中执行将同时绑定用户组与场景组，在频道中执行则绑定场景组。
<<< END U009384 >>>
<<< UNIT U009385 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:53-53 | ctx=core.help.bind.target >>>
审阅次数：10
查看当前{TERM:target}所属的场景组与消息通道编号。
<<< END U009385 >>>
<<< UNIT U009386 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:54-54 | ctx=core.help.bind.target.remove >>>
审阅次数：10
将指定{TERM:target}移出当前所属场景组。
<<< END U009386 >>>
<<< UNIT U009387 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:55-55 | ctx=core.help.bind.token >>>
审阅次数：10
输入另一处生成的绑定码以完成绑定。
<<< END U009387 >>>
<<< UNIT U009388 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:56-56 | ctx=core.help.bind.whoami >>>
审阅次数：10
查看当前命令发送者在机器人内部的唯一标识。
<<< END U009388 >>>
<<< UNIT U009389 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:57-57 | ctx=core.help.config.delete >>>
审阅次数：10
删除指定配置项。
<<< END U009389 >>>
<<< UNIT U009390 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:58-58 | ctx=core.help.config.get >>>
审阅次数：10
读取指定配置项的值。
<<< END U009390 >>>
<<< UNIT U009391 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:59-59 | ctx=core.help.config.write >>>
审阅次数：10
修改或新增指定配置项。
<<< END U009391 >>>
<<< UNIT U009392 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:60-60 | ctx=core.help.config.write.option.s >>>
审阅次数：10
指定是否为密钥配置项。
<<< END U009392 >>>
<<< UNIT U009393 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:61-61 | ctx=core.help.database.exec >>>
审阅次数：10
执行 SQL 查询。
<<< END U009393 >>>
<<< UNIT U009394 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:62-62 | ctx=core.help.database.field >>>
审阅次数：10
查看指定数据库模型的字段定义。
<<< END U009394 >>>
<<< UNIT U009395 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:63-63 | ctx=core.help.database.model >>>
审阅次数：10
查看数据库模型列表。
<<< END U009395 >>>
<<< UNIT U009396 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:64-64 | ctx=core.help.echo >>>
审阅次数：10
复述指定的消息内容。
<<< END U009396 >>>
<<< UNIT U009397 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:65-65 | ctx=core.help.eval >>>
审阅次数：10
执行 Python 表达式。
<<< END U009397 >>>
<<< UNIT U009398 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:66-66 | ctx=core.help.features >>>
审阅次数：10
查看当前{TERM:target}的特性标志。
<<< END U009398 >>>
<<< UNIT U009399 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:67-67 | ctx=core.help.help >>>
审阅次数：10
查看帮助信息列表。
<<< END U009399 >>>
<<< UNIT U009400 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:68-68 | ctx=core.help.help.detail >>>
审阅次数：10
查看指定模块的详细帮助信息。
<<< END U009400 >>>
<<< UNIT U009401 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:69-69 | ctx=core.help.jobqueue.clear >>>
审阅次数：10
清空计划任务队列中的待执行任务。
<<< END U009401 >>>
<<< UNIT U009402 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:70-70 | ctx=core.help.module.disable >>>
审阅次数：10
停用指定的一个或多个模块。
<<< END U009402 >>>
<<< UNIT U009403 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:71-71 | ctx=core.help.module.disable_all >>>
审阅次数：10
停用全部模块。
<<< END U009403 >>>
<<< UNIT U009404 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:72-72 | ctx=core.help.module.enable >>>
审阅次数：10
启用指定的一个或多个模块。
<<< END U009404 >>>
<<< UNIT U009405 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:73-73 | ctx=core.help.module.enable_all >>>
审阅次数：10
启用全部模块。
<<< END U009405 >>>
<<< UNIT U009406 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:74-74 | ctx=core.help.module.list >>>
审阅次数：10
查看全部可用模块。
<<< END U009406 >>>
<<< UNIT U009407 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:75-75 | ctx=core.help.module.load >>>
审阅次数：10
动态加载指定模块。
<<< END U009407 >>>
<<< UNIT U009408 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:76-76 | ctx=core.help.module.reload >>>
审阅次数：10
重载指定模块。
<<< END U009408 >>>
<<< UNIT U009409 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:77-77 | ctx=core.help.module.unload >>>
审阅次数：10
动态卸载指定模块。
<<< END U009409 >>>
<<< UNIT U009410 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:78-78 | ctx=core.help.mute >>>
审阅次数：10
设置机器人禁止在当前场景发言。
<<< END U009410 >>>
<<< UNIT U009411 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:79-79 | ctx=core.help.petal >>>
审阅次数：10
查看当前的花瓣余额。
<<< END U009411 >>>
<<< UNIT U009412 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:80-80 | ctx=core.help.petal.admin >>>
审阅次数：10
查看指定用户的花瓣余额。
<<< END U009412 >>>
<<< UNIT U009413 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:81-81 | ctx=core.help.petal.bud >>>
审阅次数：10
领取指定口令对应的花苞。
<<< END U009413 >>>
<<< UNIT U009414 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:82-82 | ctx=core.help.petal.bud.info >>>
审阅次数：10
查看指定花苞的详细领取信息。
<<< END U009414 >>>
<<< UNIT U009415 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:83-83 | ctx=core.help.petal.bud.release >>>
审阅次数：10
强制释放全部已过期的花苞。
<<< END U009415 >>>
<<< UNIT U009416 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:84-84 | ctx=core.help.petal.bud.send >>>
审阅次数：10
创建并发送花苞。
<<< END U009416 >>>
<<< UNIT U009417 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:85-85 | ctx=core.help.petal.clear >>>
审阅次数：10
清空指定用户的花瓣余额。
<<< END U009417 >>>
<<< UNIT U009418 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:86-86 | ctx=core.help.petal.give >>>
审阅次数：10
将花瓣赠予其他用户。
<<< END U009418 >>>
<<< UNIT U009419 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:87-87 | ctx=core.help.petal.modify >>>
审阅次数：10
调整指定用户的花瓣余额。
<<< END U009419 >>>
<<< UNIT U009420 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:88-88 | ctx=core.help.petal.sign >>>
审阅次数：10
执行每日签到以获取花瓣奖励。
<<< END U009420 >>>
<<< UNIT U009421 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:89-89 | ctx=core.help.post >>>
审阅次数：10
向指定{TERM:target}推送主动消息。
<<< END U009421 >>>
<<< UNIT U009422 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:90-90 | ctx=core.help.post-whitelist >>>
审阅次数：10
切换指定 QQ 群的主动推送消息白名单状态。
<<< END U009422 >>>
<<< UNIT U009423 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:91-91 | ctx=core.help.post.global >>>
审阅次数：10
向全部{TERM:target}推送主动消息。
<<< END U009423 >>>
<<< UNIT U009424 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:92-92 | ctx=core.help.purge >>>
审阅次数：10
清空机器人实例的缓存数据。
<<< END U009424 >>>
<<< UNIT U009425 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:93-93 | ctx=core.help.raise >>>
审阅次数：10
抛出 TestException 测试异常以验证上报链路。
<<< END U009425 >>>
<<< UNIT U009426 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:94-94 | ctx=core.help.restart >>>
审阅次数：10
重启机器人。
<<< END U009426 >>>
<<< UNIT U009427 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:95-95 | ctx=core.help.restart.option.force >>>
审阅次数：10
跳过确认与等待，强制重启。
<<< END U009427 >>>
<<< UNIT U009428 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:96-96 | ctx=core.help.resume >>>
审阅次数：10
继续处理处于暂停状态的广播消息。
<<< END U009428 >>>
<<< UNIT U009429 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:97-97 | ctx=core.help.resume.clear >>>
审阅次数：10
清空处于等待发送状态的广播消息。
<<< END U009429 >>>
<<< UNIT U009430 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:98-98 | ctx=core.help.resume.continue >>>
审阅次数：10
跳过当前条目并继续执行广播发送。
<<< END U009430 >>>
<<< UNIT U009431 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:99-99 | ctx=core.help.say >>>
审阅次数：10
复述指定消息内容。
<<< END U009431 >>>
<<< UNIT U009432 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:100-100 | ctx=core.help.say.md >>>
审阅次数：10
以 Markdown 格式复述指定消息内容。
<<< END U009432 >>>
<<< UNIT U009433 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:101-101 | ctx=core.help.set.sender.data.delete >>>
审阅次数：10
删除指定用户数据键。
<<< END U009433 >>>
<<< UNIT U009434 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:102-102 | ctx=core.help.set.sender.data.edit >>>
审阅次数：10
修改指定用户数据键的值。
<<< END U009434 >>>
<<< UNIT U009435 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:103-103 | ctx=core.help.set.sender.data.get >>>
审阅次数：10
读取指定用户数据键的值。
<<< END U009435 >>>
<<< UNIT U009436 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:104-104 | ctx=core.help.set.target.data.delete >>>
审阅次数：10
删除指定{TERM:target}数据键。
<<< END U009436 >>>
<<< UNIT U009437 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:105-105 | ctx=core.help.set.target.data.edit >>>
审阅次数：10
修改指定{TERM:target}数据键的值。
<<< END U009437 >>>
<<< UNIT U009438 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:106-106 | ctx=core.help.set.target.data.get >>>
审阅次数：10
读取指定{TERM:target}数据键的值。
<<< END U009438 >>>
<<< UNIT U009439 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:107-107 | ctx=core.help.set.target.module.disable >>>
审阅次数：10
停用{TERM:target}中的模块。
<<< END U009439 >>>
<<< UNIT U009440 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:108-108 | ctx=core.help.set.target.module.enable >>>
审阅次数：10
启用{TERM:target}中的模块。
<<< END U009440 >>>
<<< UNIT U009441 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:109-109 | ctx=core.help.set.target.module.list >>>
审阅次数：10
查看{TERM:target}中已启用的模块。
<<< END U009441 >>>
<<< UNIT U009442 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:110-110 | ctx=core.help.setup.check >>>
审阅次数：10
切换命令语法与拼写检查开关。
<<< END U009442 >>>
<<< UNIT U009443 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:111-111 | ctx=core.help.setup.cooldown >>>
审阅次数：10
设置{TERM:target}内的命令冷却秒数。
<<< END U009443 >>>
<<< UNIT U009444 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:112-112 | ctx=core.help.setup.desc >>>
审阅次数：10
配置机器人的运行行为与偏好。
<<< END U009444 >>>
<<< UNIT U009445 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:113-113 | ctx=core.help.setup.emote >>>
审阅次数：10
切换{TERM:target}内的表情展示开关。
<<< END U009445 >>>
<<< UNIT U009446 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:114-114 | ctx=core.help.setup.invalid-module-prompt >>>
审阅次数：10
切换“模块不存在”提示开关。
<<< END U009446 >>>
<<< UNIT U009447 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:115-115 | ctx=core.help.setup.list >>>
审阅次数：10
列出当前{TERM:target}与用户的设置状态。
<<< END U009447 >>>
<<< UNIT U009448 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:116-116 | ctx=core.help.setup.list.sender >>>
审阅次数：10
列出用户的设置状态。
<<< END U009448 >>>
<<< UNIT U009449 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:117-117 | ctx=core.help.setup.list.target >>>
审阅次数：10
列出当前{TERM:target}的设置状态。
<<< END U009449 >>>
<<< UNIT U009450 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:118-118 | ctx=core.help.setup.locale.desc >>>
审阅次数：10
配置机器人的运行语言。
<<< END U009450 >>>
<<< UNIT U009451 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:119-119 | ctx=core.help.setup.locale.reload >>>
审阅次数：10
重载语言文件。
<<< END U009451 >>>
<<< UNIT U009452 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:120-120 | ctx=core.help.setup.locale.set >>>
审阅次数：10
设置机器人的运行语言代码。
<<< END U009452 >>>
<<< UNIT U009453 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:121-121 | ctx=core.help.setup.markdown >>>
审阅次数：10
切换 Markdown 消息渲染开关。
<<< END U009453 >>>
<<< UNIT U009454 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:122-122 | ctx=core.help.setup.prefix.add >>>
审阅次数：10
添加自定义命令前缀。
<<< END U009454 >>>
<<< UNIT U009455 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:123-123 | ctx=core.help.setup.prefix.list >>>
审阅次数：10
查看自定义命令前缀列表。
<<< END U009455 >>>
<<< UNIT U009456 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:124-124 | ctx=core.help.setup.prefix.remove >>>
审阅次数：10
移除自定义命令前缀。
<<< END U009456 >>>
<<< UNIT U009457 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:125-125 | ctx=core.help.setup.prefix.reset >>>
审阅次数：10
重置自定义命令前缀。
<<< END U009457 >>>
<<< UNIT U009458 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:126-126 | ctx=core.help.setup.sign >>>
审阅次数：10
切换{TERM:target}内的签到功能开关。
<<< END U009458 >>>
<<< UNIT U009459 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:127-127 | ctx=core.help.setup.dark >>>
审阅次数：10
切换深色模式开关。
<<< END U009459 >>>
<<< UNIT U009460 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:128-128 | ctx=core.help.setup.timeoffset >>>
审阅次数：10
设置{TERM:target}时区偏移量，传入 reset 则恢复默认值。
<<< END U009460 >>>
<<< UNIT U009461 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:129-129 | ctx=core.help.setup.timezone >>>
审阅次数：10
设置用户显示时区偏移量，传入 reset 则恢复跟随{TERM:target}时区。
<<< END U009461 >>>
<<< UNIT U009462 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:130-130 | ctx=core.help.setup.typing >>>
审阅次数：10
切换输入状态提示开关。
<<< END U009462 >>>
<<< UNIT U009463 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:131-131 | ctx=core.help.superuser.add >>>
审阅次数：10
将指定用户设置为超级用户。
<<< END U009463 >>>
<<< UNIT U009464 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:132-132 | ctx=core.help.superuser.remove >>>
审阅次数：10
撤销指定用户的超级用户权限。
<<< END U009464 >>>
<<< UNIT U009465 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:133-133 | ctx=core.help.update >>>
审阅次数：10
更新机器人及其依赖。
<<< END U009465 >>>
<<< UNIT U009466 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:134-134 | ctx=core.help.update.option.force >>>
审阅次数：10
强制重置与更新源代码。
<<< END U009466 >>>
<<< UNIT U009467 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:135-135 | ctx=core.help.update&restart >>>
审阅次数：10
更新并重启机器人。
<<< END U009467 >>>
<<< UNIT U009468 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:136-136 | ctx=core.help.update&restart.option.force >>>
审阅次数：10
跳过确认，强制重置与更新源代码并强制重启。
<<< END U009468 >>>
<<< UNIT U009469 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:137-137 | ctx=core.help.url-audit.allowlist.add >>>
审阅次数：10
向用户自定义的全局 URL 允许列表中添加精确 URL 规则。
<<< END U009469 >>>
<<< UNIT U009470 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:138-138 | ctx=core.help.url-audit.allowlist.add_regex >>>
审阅次数：10
向用户自定义的全局 URL 允许列表中添加受约束的完整正则表达式规则。
<<< END U009470 >>>
<<< UNIT U009471 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:139-139 | ctx=core.help.url-audit.allowlist.list >>>
审阅次数：10
列出预设全局与用户自定义的 URL 允许列表规则。
<<< END U009471 >>>
<<< UNIT U009472 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:140-140 | ctx=core.help.url-audit.allowlist.query >>>
审阅次数：10
查询 URL 匹配的全局允许列表规则。
<<< END U009472 >>>
<<< UNIT U009473 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:141-141 | ctx=core.help.url-audit.allowlist.remove >>>
审阅次数：10
从用户自定义的全局 URL 允许列表中删除精确 URL 规则。
<<< END U009473 >>>
<<< UNIT U009474 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:142-142 | ctx=core.help.url-audit.allowlist.remove_regex >>>
审阅次数：10
从用户自定义的全局 URL 允许列表中删除正则表达式规则。
<<< END U009474 >>>
<<< UNIT U009475 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:143-143 | ctx=core.help.url-audit.blocklist.add >>>
审阅次数：10
向用户自定义的全局 URL 阻止列表中添加精确 URL 规则。
<<< END U009475 >>>
<<< UNIT U009476 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:144-144 | ctx=core.help.url-audit.blocklist.add_regex >>>
审阅次数：10
向用户自定义的全局 URL 阻止列表中添加受约束的完整正则表达式规则。
<<< END U009476 >>>
<<< UNIT U009477 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:145-145 | ctx=core.help.url-audit.blocklist.list >>>
审阅次数：10
列出预设全局与用户自定义的 URL 阻止列表规则。
<<< END U009477 >>>
<<< UNIT U009478 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:146-146 | ctx=core.help.url-audit.blocklist.query >>>
审阅次数：10
查询 URL 匹配的全局阻止列表规则。
<<< END U009478 >>>
<<< UNIT U009479 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:147-147 | ctx=core.help.url-audit.blocklist.remove >>>
审阅次数：10
从用户自定义的全局 URL 阻止列表中删除精确 URL 规则。
<<< END U009479 >>>
<<< UNIT U009480 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:148-148 | ctx=core.help.url-audit.blocklist.remove_regex >>>
审阅次数：10
从用户自定义的全局 URL 阻止列表中删除正则表达式规则。
<<< END U009480 >>>
<<< UNIT U009481 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:149-149 | ctx=core.help.webrender.reload >>>
审阅次数：10
重载 WebRender 网页渲染服务。
<<< END U009481 >>>
<<< UNIT U009482 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:150-150 | ctx=core.help.webrender.start >>>
审阅次数：10
启动 WebRender 网页渲染服务。
<<< END U009482 >>>
<<< UNIT U009483 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:151-151 | ctx=core.help.webrender.status >>>
审阅次数：10
查看 WebRender 网页渲染服务的运行状态。
<<< END U009483 >>>
<<< UNIT U009484 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:152-152 | ctx=core.help.webrender.stop >>>
审阅次数：10
停止 WebRender 网页渲染服务。
<<< END U009484 >>>
<<< UNIT U009485 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:153-153 | ctx=core.message.about.button.donate >>>
审阅次数：10
💵 赞助项目
<<< END U009485 >>>
<<< UNIT U009486 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:154-154 | ctx=core.message.about.button.issue >>>
审阅次数：10
问题反馈与功能建议提交入口
<<< END U009486 >>>
<<< UNIT U009487 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:155-155 | ctx=core.message.about.button.qq_group >>>
审阅次数：10
QQ 测试群与快速反馈
<<< END U009487 >>>
<<< UNIT U009488 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:156-156 | ctx=core.message.about.button.repository >>>
审阅次数：10
开源仓库地址
<<< END U009488 >>>
<<< UNIT U009489 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:157-157 | ctx=core.message.about.credits >>>
审阅次数：10
开发人员名单
<<< END U009489 >>>
<<< UNIT U009490 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:158-158 | ctx=core.message.about.credits.unavailable >>>
审阅次数：10
无法读取开发人员名单。
<<< END U009490 >>>
<<< UNIT U009491 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:159-159 | ctx=core.message.about.introduction >>>
审阅次数：10
小可是由 Teahouse Studios 出品的多功能、跨平台、可自由扩展的聊天机器人助手，基于 AGPL-3.0 协议开源。
请支持开发团队以便持续推进开发与维护。
<<< END U009491 >>>
<<< UNIT U009492 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:160-160 | ctx=core.message.about.permissions >>>
审阅次数：10
请让群主在最新版手机 QQ 中打开群聊设置，进入“群机器人”并选择当前机器人，随后开启“获取群内全部消息”与“机器人主动在群聊内发言”权限。开启后，订阅扩展模块与正则表达式模块方可正常工作。

Android 手机可以输入“${cmd}[<QQ 群号>]”快速完成权限设置。
<<< END U009492 >>>
<<< UNIT U009493 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:161-161 | ctx=core.message.about.permissions.action >>>
审阅次数：10
查看权限开启方法
<<< END U009493 >>>
<<< UNIT U009494 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:162-162 | ctx=core.message.about.permissions.invalid >>>
审阅次数：10
QQ 群号格式无效。
<<< END U009494 >>>
<<< UNIT U009495 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:163-163 | ctx=core.message.about.permissions.prompt >>>
审阅次数：10
带有删除线的模块需要额外权限。${cmd}
<<< END U009495 >>>
<<< UNIT U009496 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:164-164 | ctx=core.message.about.permissions.quick_config >>>
审阅次数：10
使用 Android 手机点击以下按钮可快速设置权限：
<<< END U009496 >>>
<<< UNIT U009497 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:165-165 | ctx=core.message.about.permissions.quick_config.button >>>
审阅次数：10
点击设置权限
<<< END U009497 >>>
<<< UNIT U009498 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:166-166 | ctx=core.message.about.ping >>>
审阅次数：10
机器人已运行：${bot_running_time}
处理器使用率：${cpu_percent}%
内存使用率：${ram_percent}%
磁盘使用率：${disk_percent}%
<<< END U009498 >>>
<<< UNIT U009499 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:167-167 | ctx=core.message.about.status.detail >>>
审阅次数：10
系统启动时间：${system_boot_time}
机器人已运行：${bot_running_time}
Python 版本：${python_version}
WebRender 状态：${web_render_status}
JobQueue 后端类型：${jobqueue_backend}
客户端名称：${client_name}
自启动以来已处理命令：${command_parsed}
自启动以来已处理消息：${parsed}
处理器型号：${cpu_brand}
处理器使用率：${cpu_percent}%
物理内存：${ram}M 使用率：${ram_percent}%
Swap 内存：${swap}M 使用率：${swap_percent}%
磁盘容量：${disk_space}G/${disk_space_total}G
<<< END U009499 >>>
<<< UNIT U009500 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:169-169 | ctx=core.message.about.status.process.daemon >>>
审阅次数：10
守护进程
<<< END U009500 >>>
<<< UNIT U009501 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:170-170 | ctx=core.message.about.status.process.list >>>
审阅次数：10
各进程内存占用：
<<< END U009501 >>>
<<< UNIT U009502 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:171-171 | ctx=core.message.about.status.process.peers >>>
审阅次数：10
各平台与服务端进程
<<< END U009502 >>>
<<< UNIT U009503 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:172-172 | ctx=core.message.about.status.process.unavailable >>>
审阅次数：10
${name}：不可用（${reason}）
<<< END U009503 >>>
<<< UNIT U009504 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:173-173 | ctx=core.message.about.version >>>
审阅次数：10
当前机器人版本号：${version}
<<< END U009504 >>>
<<< UNIT U009505 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:174-174 | ctx=core.message.about.version.unknown >>>
审阅次数：10
无法获取版本号。当前机器人可能未通过 Git 方式部署。
<<< END U009505 >>>
<<< UNIT U009506 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:175-175 | ctx=core.message.abuse.ban.success >>>
审阅次数：10
成功将用户 ${sender} 加入黑名单。
<<< END U009506 >>>
<<< UNIT U009507 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:176-176 | ctx=core.message.abuse.block.self >>>
审阅次数：10
无法在此{TERM:target}内执行此操作。
<<< END U009507 >>>
<<< UNIT U009508 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:177-177 | ctx=core.message.abuse.block.success >>>
审阅次数：10
成功将{TERM:target} ${target} 加入黑名单。
<<< END U009508 >>>
<<< UNIT U009509 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:178-178 | ctx=core.message.abuse.check.banned >>>
审阅次数：10
（此用户已处于黑名单状态）
<<< END U009509 >>>
<<< UNIT U009510 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:179-179 | ctx=core.message.abuse.check.tempbanned >>>
审阅次数：10
（此用户已被临时限制，距离解封尚余 ${ban_time} 秒）
<<< END U009510 >>>
<<< UNIT U009511 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:180-180 | ctx=core.message.abuse.check.trusted >>>
审阅次数：10
（此用户已处于白名单状态）
<<< END U009511 >>>
<<< UNIT U009512 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:181-181 | ctx=core.message.abuse.check.warns >>>
审阅次数：10
用户 ${sender} 已被警告 ${warns} 次。
<<< END U009512 >>>
<<< UNIT U009513 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:182-182 | ctx=core.message.abuse.clear.success >>>
审阅次数：10
成功清除用户 ${sender} 的警告。
<<< END U009513 >>>
<<< UNIT U009514 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:183-183 | ctx=core.message.abuse.distrust.success >>>
审阅次数：10
成功将用户 ${sender} 移出白名单。
<<< END U009514 >>>
<<< UNIT U009515 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:184-184 | ctx=core.message.abuse.revoke.success >>>
审阅次数：10
成功移除用户 ${sender} 的 ${count} 次警告。此用户已被警告 ${warn_count} 次。
<<< END U009515 >>>
<<< UNIT U009516 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:185-185 | ctx=core.message.abuse.trust.success >>>
审阅次数：10
成功将用户 ${sender} 加入白名单。
<<< END U009516 >>>
<<< UNIT U009517 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:186-186 | ctx=core.message.abuse.unban.success >>>
审阅次数：10
成功将用户 ${sender} 移出黑名单。
<<< END U009517 >>>
<<< UNIT U009518 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:187-187 | ctx=core.message.abuse.unblock.success >>>
审阅次数：10
成功将{TERM:target} ${target} 移出黑名单。
<<< END U009518 >>>
<<< UNIT U009519 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:188-188 | ctx=core.message.abuse.untempban.success >>>
审阅次数：10
成功解除用户 ${sender} 的临时封禁。
<<< END U009519 >>>
<<< UNIT U009520 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:189-189 | ctx=core.message.abuse.warn.success >>>
审阅次数：10
成功警告用户 ${sender} ${count} 次。此用户已被警告 ${warn_count} 次。
<<< END U009520 >>>
<<< UNIT U009521 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:190-190 | ctx=core.message.admin.add.already >>>
审阅次数：10
此成员已属于机器人管理员。
<<< END U009521 >>>
<<< UNIT U009522 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:191-191 | ctx=core.message.admin.add.native >>>
审阅次数：10
此成员已属于{TERM:target}管理员，无需重复授予机器人管理员权限。
<<< END U009522 >>>
<<< UNIT U009523 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:192-192 | ctx=core.message.admin.add.success >>>
审阅次数：10
成功将用户 ${sender} 设置为机器人管理员。
<<< END U009523 >>>
<<< UNIT U009524 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:193-193 | ctx=core.message.admin.ban.already >>>
审阅次数：10
此成员已被限制使用机器人。
<<< END U009524 >>>
<<< UNIT U009525 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:194-194 | ctx=core.message.admin.ban.list >>>
审阅次数：10
当前被设置限制使用机器人的成员：
<<< END U009525 >>>
<<< UNIT U009526 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:195-195 | ctx=core.message.admin.ban.list.none >>>
审阅次数：10
当前无被限制使用机器人的成员。
<<< END U009526 >>>
<<< UNIT U009527 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:196-196 | ctx=core.message.admin.ban.self >>>
审阅次数：10
无法对自己设置限制。
<<< END U009527 >>>
<<< UNIT U009528 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:197-197 | ctx=core.message.admin.ban.success >>>
审阅次数：10
成功限制用户 ${sender} 使用机器人。
<<< END U009528 >>>
<<< UNIT U009529 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:198-198 | ctx=core.message.admin.invalid >>>
审阅次数：10
ID 格式错误，格式应为“${sender}|<用户 ID>”，请使用“${cmd}”查看用户 ID。
<<< END U009529 >>>
<<< UNIT U009530 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:199-199 | ctx=core.message.admin.leave.confirm >>>
审阅次数：10
此操作不可逆，请确认是否继续。
<<< END U009530 >>>
<<< UNIT U009531 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:200-200 | ctx=core.message.admin.leave.success >>>
审阅次数：10
已执行，再见。
<<< END U009531 >>>
<<< UNIT U009532 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:201-201 | ctx=core.message.admin.list >>>
审阅次数：10
当前手动配置的机器人管理员列表：
<<< END U009532 >>>
<<< UNIT U009533 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:202-202 | ctx=core.message.admin.list.none >>>
审阅次数：10
当前无手动配置的机器人管理员。
<<< END U009533 >>>
<<< UNIT U009534 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:203-203 | ctx=core.message.admin.remove.confirm >>>
审阅次数：10
即将移除自身的机器人管理员权限，请确认是否继续。
<<< END U009534 >>>
<<< UNIT U009535 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:204-204 | ctx=core.message.admin.remove.confirm.token >>>
审阅次数：10
我确定移除我自己的机器人管理员权限。
<<< END U009535 >>>
<<< UNIT U009536 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:205-205 | ctx=core.message.admin.remove.native >>>
审阅次数：10
此成员已属于{TERM:target}管理员，无法通过机器人撤销其管理员权限。
<<< END U009536 >>>
<<< UNIT U009537 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:206-206 | ctx=core.message.admin.remove.success >>>
审阅次数：10
成功将用户 ${sender} 移出机器人管理员名单。
<<< END U009537 >>>
<<< UNIT U009538 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:207-207 | ctx=core.message.admin.unban.success >>>
审阅次数：10
成功取消限制用户 ${sender} 使用机器人。
<<< END U009538 >>>
<<< UNIT U009539 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:208-208 | ctx=core.message.alias.add.already >>>
审阅次数：10
别名“${alias}”已存在于自定义别名列表。
<<< END U009539 >>>
<<< UNIT U009540 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:209-209 | ctx=core.message.alias.add.invalid_placeholder >>>
审阅次数：10
所添加的别名中包含无效的占位符。
<<< END U009540 >>>
<<< UNIT U009541 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:210-210 | ctx=core.message.alias.add.invalid_prefix >>>
审阅次数：10
所添加的别名对应命令必须以命令前缀开头，请检查输入。
<<< END U009541 >>>
<<< UNIT U009542 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:211-211 | ctx=core.message.alias.add.success >>>
审阅次数：10
已添加自定义命令别名：${alias} -> ${command}
<<< END U009542 >>>
<<< UNIT U009543 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:212-212 | ctx=core.message.alias.list >>>
审阅次数：10
自定义命令别名列表：
<<< END U009543 >>>
<<< UNIT U009544 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:213-213 | ctx=core.message.alias.list.none >>>
审阅次数：10
自定义命令别名列表当前为空。
<<< END U009544 >>>
<<< UNIT U009545 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:214-214 | ctx=core.message.alias.list.table.header.alias >>>
审阅次数：10
别名
<<< END U009545 >>>
<<< UNIT U009546 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:215-215 | ctx=core.message.alias.list.table.header.command >>>
审阅次数：10
命令
<<< END U009546 >>>
<<< UNIT U009547 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:216-216 | ctx=core.message.alias.not_found >>>
审阅次数：10
别名“${alias}”不存在于自定义别名列表中。
<<< END U009547 >>>
<<< UNIT U009548 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:217-217 | ctx=core.message.alias.remove.success >>>
审阅次数：10
已移除自定义命令别名：${alias}
<<< END U009548 >>>
<<< UNIT U009549 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:218-218 | ctx=core.message.alias.reset.success >>>
审阅次数：10
已重置自定义命令别名列表。
<<< END U009549 >>>
<<< UNIT U009550 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:219-219 | ctx=core.message.analytics.counts >>>
审阅次数：10
机器人已执行命令次数（自 ${first_record} 开始统计）：${counts}
今日已执行命令次数：${counts_today}
<<< END U009550 >>>
<<< UNIT U009551 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:220-220 | ctx=core.message.analytics.days >>>
审阅次数：10
最近 30 天的“${module}”命令调用次数统计（自 ${first_record} 开始统计）：
<<< END U009551 >>>
<<< UNIT U009552 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:221-221 | ctx=core.message.analytics.days.total >>>
审阅次数：10
最近 30 天的全部命令调用次数统计（自 ${first_record} 开始统计）：
<<< END U009552 >>>
<<< UNIT U009553 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:222-222 | ctx=core.message.analytics.disabled >>>
审阅次数：10
当前未启用命令统计功能。
<<< END U009553 >>>
<<< UNIT U009554 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:223-223 | ctx=core.message.analytics.missing_matplotlib >>>
审阅次数：10
未安装绘图依赖 matplotlib，在安装 core 的 image extra 依赖项后方可使用。
<<< END U009554 >>>
<<< UNIT U009555 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:224-224 | ctx=core.message.analytics.none >>>
审阅次数：10
机器人数据库当前为空，正在执行初始化……
<<< END U009555 >>>
<<< UNIT U009556 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:225-225 | ctx=core.message.analytics.year >>>
审阅次数：10
最近一年的“${module}”命令调用次数统计（自 ${first_record} 开始统计）：
<<< END U009556 >>>
<<< UNIT U009557 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:226-226 | ctx=core.message.analytics.year.total >>>
审阅次数：10
最近一年的全部命令调用次数统计（自 ${first_record} 开始统计）：
<<< END U009557 >>>
<<< UNIT U009558 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:227-227 | ctx=core.message.auth.add.already >>>
审阅次数：10
${user} 已被授权使用模块 ${module}。
<<< END U009558 >>>
<<< UNIT U009559 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:228-228 | ctx=core.message.auth.add.confirm.token >>>
审阅次数：10
我授权用户 ${user} 使用模块 ${module}。
<<< END U009559 >>>
<<< UNIT U009560 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:229-229 | ctx=core.message.auth.add.success >>>
审阅次数：10
成功授权 ${user} 使用模块 ${module}。
<<< END U009560 >>>
<<< UNIT U009561 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:230-230 | ctx=core.message.auth.list.empty >>>
审阅次数：10
当前无任何授权记录。
<<< END U009561 >>>
<<< UNIT U009562 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:231-231 | ctx=core.message.auth.list.entry >>>
审阅次数：10
${user} 被 ${authorized_by} 授权使用模块 ${module}
<<< END U009562 >>>
<<< UNIT U009563 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:232-232 | ctx=core.message.auth.module_not_found >>>
审阅次数：10
模块“${module}”不存在。
<<< END U009563 >>>
<<< UNIT U009564 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:233-233 | ctx=core.message.auth.module_not_required_superuser >>>
审阅次数：10
模块“${module}”无需超级用户权限。
<<< END U009564 >>>
<<< UNIT U009565 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:234-234 | ctx=core.message.auth.remove.not_found >>>
审阅次数：10
未找到由你向 ${user} 授予的 ${module} 授权记录。
<<< END U009565 >>>
<<< UNIT U009566 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:235-235 | ctx=core.message.auth.remove.success >>>
审阅次数：10
已取消 ${user} 使用模块 ${module} 的授权。
<<< END U009566 >>>
<<< UNIT U009567 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:236-236 | ctx=core.message.bind.auto.cancelled >>>
审阅次数：10
已取消，未执行任何修改。
<<< END U009567 >>>
<<< UNIT U009568 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:237-237 | ctx=core.message.bind.auto.confirm.inherit >>>
审阅次数：10
继承数据时，语言沿用发起方。模块开关、管理员名单、限制名单取两侧并集。{TERM:target}设置逐项合并，同名项以发起方为准。模块数据仅一侧存在则直接迁移，两侧均存在则逐个询问保留哪一份。两个{TERM:target}还会被标记为同一条消息通道，同一消息通道的一条命令仅由此{TERM:target}内的某一个机器人执行，消息推送也仅发送一次。合并后无法撤销。
<<< END U009568 >>>
<<< UNIT U009569 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:238-238 | ctx=core.message.bind.auto.success >>>
审阅次数：10
已与当前{TERM:target}内的其他机器人合并（场景组 ${id}，消息通道 ${channel} 号）。此后同一条命令仅由其中一个机器人执行，推送仅发送一次。
<<< END U009569 >>>
<<< UNIT U009570 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:239-239 | ctx=core.message.bind.auto.timeout >>>
审阅次数：10
等待超时，未在当前{TERM:target}内找到其他机器人。
<<< END U009570 >>>
<<< UNIT U009571 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:240-240 | ctx=core.message.bind.channel.hint >>>
审阅次数：10
标注为同一消息通道的{TERM:target}会被视作现实中的同一{TERM:target}（例如同一个{TERM:target}内存在两个机器人时，为防止命令被两个机器人同时执行，可以将消息通道设置为同一个通道），同一消息通道的一条命令仅由此{TERM:target}内的某一个机器人执行，消息推送也仅发送一次。
<<< END U009571 >>>
<<< UNIT U009572 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:241-241 | ctx=core.message.bind.channel.hint.auto >>>
审阅次数：10
如需合并消息通道，请使用“${prefix}bind auto”执行自动配对，或使用“${prefix}bind channel set”手动指定同一个通道编号。
<<< END U009572 >>>
<<< UNIT U009573 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:242-242 | ctx=core.message.bind.channel.hint.manual >>>
审阅次数：10
如需合并消息通道，请使用“${prefix}bind channel set”手动指定同一个通道编号。
<<< END U009573 >>>
<<< UNIT U009574 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:243-243 | ctx=core.message.bind.channel.info >>>
审阅次数：10
当前{TERM:target}的消息通道：${channel} 号
<<< END U009574 >>>
<<< UNIT U009575 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:244-244 | ctx=core.message.bind.channel.info.entry >>>
审阅次数：10
${id}（推送优先级 ${priority}）
<<< END U009575 >>>
<<< UNIT U009576 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:245-245 | ctx=core.message.bind.channel.info.shared >>>
审阅次数：10
同通道的{TERM:target}共 ${count} 个，按主动推送顺序排列：
<<< END U009576 >>>
<<< UNIT U009577 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:246-246 | ctx=core.message.bind.channel.priority.invalid >>>
审阅次数：10
推送优先级的取值范围为 0 到 100 的整数。
<<< END U009577 >>>
<<< UNIT U009578 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:247-247 | ctx=core.message.bind.channel.priority.reset.success >>>
审阅次数：10
已将当前{TERM:target}的推送优先级重置为 0。
<<< END U009578 >>>
<<< UNIT U009579 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:248-248 | ctx=core.message.bind.channel.priority.set.success >>>
审阅次数：10
已将当前{TERM:target}的推送优先级设为 ${priority}。
<<< END U009579 >>>
<<< UNIT U009580 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:249-249 | ctx=core.message.bind.channel.reset.success >>>
审阅次数：10
已使当前{TERM:target}脱离原有通道，已分配为 ${channel} 号独立通道。
<<< END U009580 >>>
<<< UNIT U009581 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:250-250 | ctx=core.message.bind.channel.set.success >>>
审阅次数：10
已将当前{TERM:target}的消息通道设置为 ${channel} 号。具有相同编号的{TERM:target}会被视作现实中的同一个{TERM:target}（例如一个{TERM:target}内同时存在两个机器人），命令仅由其中一个机器人执行，推送仅发送一次。
<<< END U009581 >>>
<<< UNIT U009582 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:251-251 | ctx=core.message.bind.channel.unknown >>>
审阅次数：10
当前{TERM:target}尚未创建绑定记录，无法查看消息通道信息。
<<< END U009582 >>>
<<< UNIT U009583 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:252-252 | ctx=core.message.bind.code >>>
审阅次数：10
绑定码：${code}
<<< END U009583 >>>
<<< UNIT U009584 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:253-253 | ctx=core.message.bind.code.context.mismatch >>>
审阅次数：10
绑定失败，绑定码的生成与使用必须处于同类{TERM:target}。绑定流程已中止。
<<< END U009584 >>>
<<< UNIT U009585 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:254-254 | ctx=core.message.bind.code.invalid >>>
审阅次数：10
绑定码格式无效或已超过有效期。
<<< END U009585 >>>
<<< UNIT U009586 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:255-255 | ctx=core.message.bind.code.private.failed >>>
审阅次数：10
绑定码私聊发送失败，绑定流程已中止。可能是因为机器人未被添加为好友、对方关闭了私聊，或平台限制了主动私聊。请先与机器人建立私聊会话后重试。
<<< END U009586 >>>
<<< UNIT U009587 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:256-256 | ctx=core.message.bind.code.private.sent >>>
审阅次数：10
绑定码已通过私聊发送，请查收。（请为新的机器人开启必要权限，例如获取全部消息与主动消息权限）
<<< END U009587 >>>
<<< UNIT U009588 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:257-257 | ctx=core.message.bind.code.private.unsupported >>>
审阅次数：10
当前平台不支持私聊，无法安全地发送绑定码。绑定流程已中止。
<<< END U009588 >>>
<<< UNIT U009589 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:258-258 | ctx=core.message.bind.conflict >>>
审阅次数：10
以下模块在两侧均保存有数据，需要逐个选择保留哪一份数据：${modules}
<<< END U009589 >>>
<<< UNIT U009590 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:259-259 | ctx=core.message.bind.conflict.choose >>>
审阅次数：10
模块“${module}”在两侧均保存有数据。如需保留发起方的数据请确认，如需保留当前侧的数据请取消。
<<< END U009590 >>>
<<< UNIT U009591 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:260-260 | ctx=core.message.bind.merge.channel.unified >>>
审阅次数：10
两侧{TERM:target}已并入消息通道 ${channel}，此后命令与推送仅由其中一方承担。
<<< END U009591 >>>
<<< UNIT U009592 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:261-261 | ctx=core.message.bind.merge.code >>>
审阅次数：10
迁移码：${code}
<<< END U009592 >>>
<<< UNIT U009593 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:262-262 | ctx=core.message.bind.merge.code.invalid >>>
审阅次数：10
迁移码格式无效或已超过有效期，请重新执行“${cmd}”获取。
<<< END U009593 >>>
<<< UNIT U009594 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:263-263 | ctx=core.message.bind.merge.context.mismatch >>>
审阅次数：10
迁移码的使用场景类型不匹配。
<<< END U009594 >>>
<<< UNIT U009595 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:264-264 | ctx=core.message.bind.merge.private.confirm >>>
审阅次数：10
即将将你在原机器人上的用户数据与私聊数据迁移至此处，请确认以下内容：
<<< END U009595 >>>
<<< UNIT U009596 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:265-265 | ctx=core.message.bind.merge.private.failed >>>
审阅次数：10
迁移失败，请稍后重试。若问题持续，请联系机器人所有者。
<<< END U009596 >>>
<<< UNIT U009597 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:266-266 | ctx=core.message.bind.merge.route.mismatch >>>
审阅次数：10
此迁移码与平台不匹配。请确认你是在指定的平台上执行数据迁移。
<<< END U009597 >>>
<<< UNIT U009598 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:267-267 | ctx=core.message.bind.merge.same >>>
审阅次数：10
两侧数据原已属于同一分组，无需执行迁移。
<<< END U009598 >>>
<<< UNIT U009599 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:268-268 | ctx=core.message.bind.merge.self.success >>>
审阅次数：10
用户数据已迁移完成，当前用户组：${id}
<<< END U009599 >>>
<<< UNIT U009600 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:269-269 | ctx=core.message.bind.merge.start.private.prompt >>>
审阅次数：10
请在 ${minute} 分钟内，于新机器人的私聊中发送“${cmd}”以完成迁移。
<<< END U009600 >>>
<<< UNIT U009601 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:270-270 | ctx=core.message.bind.merge.start.prompt >>>
审阅次数：10
请在 ${minute} 分钟内，于新机器人所在的同一个{TERM:target}中发送“${cmd}”以完成迁移。
<<< END U009601 >>>
<<< UNIT U009602 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:271-271 | ctx=core.message.bind.merge.target.confirm.inherit >>>
审阅次数：10
迁移后，原机器人上此{TERM:target}的数据将并入此处，双方共享同一份数据。
<<< END U009602 >>>
<<< UNIT U009603 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:272-272 | ctx=core.message.bind.merge.target.success >>>
审阅次数：10
{TERM:target}数据已迁移完成，当前场景组：${id}
<<< END U009603 >>>
<<< UNIT U009604 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:273-273 | ctx=core.message.bind.self.confirm >>>
审阅次数：10
即将将以下两个用户组合并为新的用户组，原有的两个组 ID 均将失效：
<<< END U009604 >>>
<<< UNIT U009605 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:274-274 | ctx=core.message.bind.self.confirm.current >>>
审阅次数：10
当前用户组（${count} 个用户）：
<<< END U009605 >>>
<<< UNIT U009606 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:275-275 | ctx=core.message.bind.self.confirm.inherit >>>
审阅次数：10
继承数据时，偏好设置逐项合并，同名项以发起方为准。模块数据仅一侧存在则直接迁移，两侧均存在则逐个询问保留哪一份。合并后无法撤销。
<<< END U009606 >>>
<<< UNIT U009607 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:276-276 | ctx=core.message.bind.self.confirm.initiator >>>
审阅次数：10
发起方用户组（${count} 个用户）：
<<< END U009607 >>>
<<< UNIT U009608 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:277-277 | ctx=core.message.bind.self.confirm.petal >>>
审阅次数：10
花瓣：${initiator} + ${current} = ${total}
<<< END U009608 >>>
<<< UNIT U009609 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:278-278 | ctx=core.message.bind.self.info >>>
审阅次数：10
当前用户所属的用户组：${id}
<<< END U009609 >>>
<<< UNIT U009610 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:279-279 | ctx=core.message.bind.self.info.bound >>>
审阅次数：10
已绑定 ${count} 个用户：
<<< END U009610 >>>
<<< UNIT U009611 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:280-280 | ctx=core.message.bind.self.remove.confirm >>>
审阅次数：10
即将将 ${id} 移出当前用户组，此用户将无法继续共享组内数据且无法自动恢复，是否继续？
<<< END U009611 >>>
<<< UNIT U009612 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:281-281 | ctx=core.message.bind.self.remove.failed >>>
审阅次数：10
解绑失败。
<<< END U009612 >>>
<<< UNIT U009613 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:282-282 | ctx=core.message.bind.self.remove.last >>>
审阅次数：10
当前用户组内仅包含此用户，无需执行解绑。
<<< END U009613 >>>
<<< UNIT U009614 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:283-283 | ctx=core.message.bind.self.remove.not_bound >>>
审阅次数：10
此用户未包含在当前用户组中。
<<< END U009614 >>>
<<< UNIT U009615 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:284-284 | ctx=core.message.bind.self.remove.success >>>
审阅次数：10
已将 ${id} 移出当前用户组。
<<< END U009615 >>>
<<< UNIT U009616 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:285-285 | ctx=core.message.bind.self.same >>>
审阅次数：10
此绑定码由当前用户组生成，无需执行绑定。
<<< END U009616 >>>
<<< UNIT U009617 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:286-286 | ctx=core.message.bind.self.success >>>
审阅次数：10
绑定成功，新的用户组：${id}
<<< END U009617 >>>
<<< UNIT U009618 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:287-287 | ctx=core.message.bind.start.private.confirm >>>
审阅次数：10
私聊中的绑定会同时处理用户组与场景组，以下变更将一并生效：
<<< END U009618 >>>
<<< UNIT U009619 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:288-288 | ctx=core.message.bind.start.private.failed >>>
审阅次数：10
绑定失败，请稍后重试。
<<< END U009619 >>>
<<< UNIT U009620 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:289-289 | ctx=core.message.bind.start.private.prompt >>>
审阅次数：10
请在 ${minute} 分钟内于另一个平台的私聊中发送“${cmd}”以完成绑定。绑定后，你的用户数据与{TERM:target}数据都将被合并，且无法撤销。请勿将绑定码告知他人。
<<< END U009620 >>>
<<< UNIT U009621 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:290-290 | ctx=core.message.bind.target.code.prompt >>>
审阅次数：10
请在 ${minute} 分钟内于另一个{TERM:target}中发送“${cmd}”以完成绑定。绑定后双方数据将被合并且无法撤销，请勿将绑定码告知他人。
<<< END U009621 >>>
<<< UNIT U009622 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:291-291 | ctx=core.message.bind.target.confirm >>>
审阅次数：10
即将将以下两个场景组合并为新的场景组，原有的两个组 ID 均将失效：
<<< END U009622 >>>
<<< UNIT U009623 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:292-292 | ctx=core.message.bind.target.confirm.current >>>
审阅次数：10
当前场景组（${count} 个{TERM:target}）：
<<< END U009623 >>>
<<< UNIT U009624 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:293-293 | ctx=core.message.bind.target.confirm.inherit >>>
审阅次数：10
继承数据时，语言沿用发起方。模块开关、管理员名单、限制名单取两侧并集。{TERM:target}设置逐项合并，同名项以发起方为准。模块数据仅一侧存在则直接迁移，两侧均存在则逐个询问保留哪一份。消息通道不会自动合并，并入的{TERM:target}会另行编号，如需合并请在绑定后使用“${prefix}bind channel set”。合并后无法撤销。
<<< END U009624 >>>
<<< UNIT U009625 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:294-294 | ctx=core.message.bind.target.confirm.initiator >>>
审阅次数：10
发起方场景组（${count} 个{TERM:target}）：
<<< END U009625 >>>
<<< UNIT U009626 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:295-295 | ctx=core.message.bind.target.info >>>
审阅次数：10
当前{TERM:target}所属的场景组：${id}
<<< END U009626 >>>
<<< UNIT U009627 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:296-296 | ctx=core.message.bind.target.info.bound >>>
审阅次数：10
已绑定 ${count} 个{TERM:target}：
<<< END U009627 >>>
<<< UNIT U009628 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:297-297 | ctx=core.message.bind.target.info.entry >>>
审阅次数：10
${id}[消息通道 ${channel}]
<<< END U009628 >>>
<<< UNIT U009629 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:298-298 | ctx=core.message.bind.target.remove.confirm >>>
审阅次数：10
即将将 ${id} 移出当前场景组，此{TERM:target}将无法继续共享组内数据且无法自动恢复，是否继续？
<<< END U009629 >>>
<<< UNIT U009630 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:299-299 | ctx=core.message.bind.target.remove.failed >>>
审阅次数：10
解绑失败。
<<< END U009630 >>>
<<< UNIT U009631 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:300-300 | ctx=core.message.bind.target.remove.last >>>
审阅次数：10
当前场景组内仅包含此{TERM:target}，无需执行解绑。
<<< END U009631 >>>
<<< UNIT U009632 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:301-301 | ctx=core.message.bind.target.remove.not_bound >>>
审阅次数：10
此{TERM:target}未包含在当前场景组中。
<<< END U009632 >>>
<<< UNIT U009633 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:302-302 | ctx=core.message.bind.target.remove.success >>>
审阅次数：10
已将 ${id} 移出当前场景组。
<<< END U009633 >>>
<<< UNIT U009634 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:303-303 | ctx=core.message.bind.target.same >>>
审阅次数：10
此绑定码由当前场景组生成，无需执行绑定。绑定流程已中止。
<<< END U009634 >>>
<<< UNIT U009635 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:304-304 | ctx=core.message.bind.target.success >>>
审阅次数：10
绑定成功，新的场景组：${id}
<<< END U009635 >>>
<<< UNIT U009636 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:305-305 | ctx=core.message.bind.whoami.admin >>>
审阅次数：10
（你拥有当前{TERM:target}的管理员权限）
<<< END U009636 >>>
<<< UNIT U009637 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:306-306 | ctx=core.message.bind.whoami.botadmin >>>
审阅次数：10
（你拥有当前{TERM:target}的机器人管理员权限）
<<< END U009637 >>>
<<< UNIT U009638 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:307-307 | ctx=core.message.bind.whoami.sender >>>
审阅次数：10
你的 ID：
${id}
<<< END U009638 >>>
<<< UNIT U009639 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:308-308 | ctx=core.message.bind.whoami.sender.union >>>
审阅次数：10
当前用户所属的用户组：
${id}
<<< END U009639 >>>
<<< UNIT U009640 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:309-309 | ctx=core.message.bind.whoami.sender.union.bound >>>
审阅次数：10
已绑定 ${count} 个用户：

<<< END U009640 >>>
<<< UNIT U009641 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:310-310 | ctx=core.message.bind.whoami.superuser >>>
审阅次数：10
（你拥有当前机器人的超级用户权限）
<<< END U009641 >>>
<<< UNIT U009642 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:311-311 | ctx=core.message.bind.whoami.target >>>
审阅次数：10
当前{TERM:target}的 ID：
${id}
<<< END U009642 >>>
<<< UNIT U009643 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:312-312 | ctx=core.message.bind.whoami.target.union >>>
审阅次数：10
当前{TERM:target}所属的场景组：
${id}
<<< END U009643 >>>
<<< UNIT U009644 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:313-313 | ctx=core.message.bind.whoami.target.union.bound >>>
审阅次数：10
已绑定 ${count} 个{TERM:target}：

<<< END U009644 >>>
<<< UNIT U009645 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:314-314 | ctx=core.message.config.write.create.confirm >>>
审阅次数：10
配置项 ${k}（${table}）尚不存在，本次写入将会新建该配置项。是否继续？
<<< END U009645 >>>
<<< UNIT U009646 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:315-315 | ctx=core.message.database.list >>>
审阅次数：10
数据库中全部支持操作的模型：
<<< END U009646 >>>
<<< UNIT U009647 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:316-316 | ctx=core.message.database.no_result >>>
审阅次数：10
查询无结果。
<<< END U009647 >>>
<<< UNIT U009648 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:317-317 | ctx=core.message.database.pages >>>
审阅次数：10
（第 ${page} 页，共 ${total_pages} 页，共 ${data_count} 条）
<<< END U009648 >>>
<<< UNIT U009649 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:318-318 | ctx=core.message.database.success >>>
审阅次数：10
成功修改 ${rows} 条数据。
<<< END U009649 >>>
<<< UNIT U009650 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:319-319 | ctx=core.message.echo.prompt >>>
审阅次数：10
请发送需要复述的消息内容。
<<< END U009650 >>>
<<< UNIT U009651 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:320-320 | ctx=core.message.features.diff >>>
审阅次数：10
其中 ${count} 项两侧不一致，已使用星号标记。
<<< END U009651 >>>
<<< UNIT U009652 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:321-321 | ctx=core.message.features.fetch.failed >>>
审阅次数：10
无法主动获取当前{TERM:target}的会话，右侧一列显示为未知。
<<< END U009652 >>>
<<< UNIT U009653 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:322-322 | ctx=core.message.features.prompt >>>
审阅次数：10
${target} 的特性标志（当前会话 / 主动会话）：
<<< END U009653 >>>
<<< UNIT U009654 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:323-323 | ctx=core.message.help.all_modules >>>
审阅次数：10
使用“${cmd}”查看全部可用模块。
<<< END U009654 >>>
<<< UNIT U009655 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:324-324 | ctx=core.message.help.button.about >>>
审阅次数：10
ℹ️ 关于机器人
<<< END U009655 >>>
<<< UNIT U009656 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:325-325 | ctx=core.message.help.button.document >>>
审阅次数：10
📃 在线文档
<<< END U009656 >>>
<<< UNIT U009657 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:326-326 | ctx=core.message.help.button.modules >>>
审阅次数：10
🧩 模块列表
<<< END U009657 >>>
<<< UNIT U009658 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:327-327 | ctx=core.message.help.command_count >>>
审阅次数：10
${count} 条命令
<<< END U009658 >>>
<<< UNIT U009659 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:328-328 | ctx=core.message.help.detail >>>
审阅次数：10
使用“${cmd}<模块名称>”查看详细信息。
<<< END U009659 >>>
<<< UNIT U009660 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:329-329 | ctx=core.message.help.document >>>
审阅次数：10
你也可以通过查阅在线文档获取帮助信息：${url}
<<< END U009660 >>>
<<< UNIT U009661 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:330-330 | ctx=core.message.help.donate >>>
审阅次数：10
若你愿意支持项目发展，欢迎赞助开发工作：${url}
<<< END U009661 >>>
<<< UNIT U009662 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:331-331 | ctx=core.message.help.header.locale >>>
审阅次数：10
语言：${language}
<<< END U009662 >>>
<<< UNIT U009663 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:332-332 | ctx=core.message.help.header.permission.admin >>>
审阅次数：10
权限：{TERM:target}管理员
<<< END U009663 >>>
<<< UNIT U009664 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:333-333 | ctx=core.message.help.header.permission.superuser >>>
审阅次数：10
权限：超级用户
<<< END U009664 >>>
<<< UNIT U009665 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:334-334 | ctx=core.message.help.header.permission.user >>>
审阅次数：10
权限：普通用户
<<< END U009665 >>>
<<< UNIT U009666 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:335-335 | ctx=core.message.help.header.version >>>
审阅次数：10
版本：${version}
<<< END U009666 >>>
<<< UNIT U009667 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:336-336 | ctx=core.message.help.header.version.unknown >>>
审阅次数：10
版本：未知
<<< END U009667 >>>
<<< UNIT U009668 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:337-337 | ctx=core.message.help.helpdoc.address >>>
审阅次数：10
在线模块文档：${url}
<<< END U009668 >>>
<<< UNIT U009669 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:338-338 | ctx=core.message.help.legacy.availables >>>
审阅次数：10
当前可用模块列表：
<<< END U009669 >>>
<<< UNIT U009670 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:339-339 | ctx=core.message.help.legacy.availables.none >>>
审阅次数：10
当前无可用模块。
<<< END U009670 >>>
<<< UNIT U009671 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:340-340 | ctx=core.message.help.legacy.base >>>
审阅次数：10
基础模块：
<<< END U009671 >>>
<<< UNIT U009672 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:341-341 | ctx=core.message.help.legacy.external >>>
审阅次数：10
扩展模块：
<<< END U009672 >>>
<<< UNIT U009673 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:342-342 | ctx=core.message.help.legacy.subscription >>>
审阅次数：10
订阅扩展模块：
<<< END U009673 >>>
<<< UNIT U009674 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:343-343 | ctx=core.message.help.mdtable >>>
审阅次数：10
向右滑动以查看全部模块，点击可自动填入对应帮助命令。
<<< END U009674 >>>
<<< UNIT U009675 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:344-344 | ctx=core.message.help.not_found >>>
审阅次数：10
目标模块可能不存在，请检查输入是否正确。
<<< END U009675 >>>
<<< UNIT U009676 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:345-345 | ctx=core.message.help.prompt >>>
审阅次数：10
标为斜体的模块仅限此{TERM:target}的管理员使用。
<<< END U009676 >>>
<<< UNIT U009677 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:346-346 | ctx=core.message.help.qqbot.limited >>>
审阅次数：10
当前群聊的机器人功能受限，仅可使用部分功能。如需使用主动推送模块与正则表达式类模块，请联系群主为机器人开启“获取群内全部消息”与“机器人主动在群聊内发言”权限。
（需要最新版本手机 QQ，且仅群主可开启）
<<< END U009677 >>>
<<< UNIT U009678 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:347-347 | ctx=core.message.help.regex_count >>>
审阅次数：10
${count} 条表达式
<<< END U009678 >>>
<<< UNIT U009679 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:348-348 | ctx=core.message.help.table.alias >>>
审阅次数：10
别名
<<< END U009679 >>>
<<< UNIT U009680 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:349-349 | ctx=core.message.help.table.base >>>
审阅次数：10
基础模块
<<< END U009680 >>>
<<< UNIT U009681 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:350-350 | ctx=core.message.help.table.command >>>
审阅次数：10
命令
<<< END U009681 >>>
<<< UNIT U009682 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:351-351 | ctx=core.message.help.table.desc >>>
审阅次数：10
描述
<<< END U009682 >>>
<<< UNIT U009683 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:352-352 | ctx=core.message.help.table.disabled >>>
审阅次数：10
未启用模块
<<< END U009683 >>>
<<< UNIT U009684 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:353-353 | ctx=core.message.help.table.external >>>
审阅次数：10
扩展模块
<<< END U009684 >>>
<<< UNIT U009685 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:354-354 | ctx=core.message.help.table.legend.external.disabled >>>
审阅次数：10
🔐 = 已停用
<<< END U009685 >>>
<<< UNIT U009686 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:355-355 | ctx=core.message.help.table.legend.external.enabled >>>
审阅次数：10
🔓 = 已启用
<<< END U009686 >>>
<<< UNIT U009687 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:356-356 | ctx=core.message.help.table.legend.subscription.disabled >>>
审阅次数：10
🔕 = 已停用
<<< END U009687 >>>
<<< UNIT U009688 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:357-357 | ctx=core.message.help.table.legend.subscription.enabled >>>
审阅次数：10
🔔 = 已启用
<<< END U009688 >>>
<<< UNIT U009689 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:358-358 | ctx=core.message.help.table.options >>>
审阅次数：10
选项
<<< END U009689 >>>
<<< UNIT U009690 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:359-359 | ctx=core.message.help.table.regex >>>
审阅次数：10
正则表达式
<<< END U009690 >>>
<<< UNIT U009691 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:360-360 | ctx=core.message.help.table.subscription >>>
审阅次数：10
订阅扩展模块
<<< END U009691 >>>
<<< UNIT U009692 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:361-361 | ctx=core.message.help.table.title >>>
审阅次数：10
可用模块
<<< END U009692 >>>
<<< UNIT U009693 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:362-362 | ctx=core.message.module.bot_permission.manage_members >>>
审阅次数：10
管理成员
<<< END U009693 >>>
<<< UNIT U009694 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:363-363 | ctx=core.message.module.bot_permission.manage_messages >>>
审阅次数：10
管理消息
<<< END U009694 >>>
<<< UNIT U009695 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:364-364 | ctx=core.message.module.bot_permission.react >>>
审阅次数：10
添加消息回应
<<< END U009695 >>>
<<< UNIT U009696 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:365-365 | ctx=core.message.module.bot_permission.read_all_messages >>>
审阅次数：10
读取全部消息
<<< END U009696 >>>
<<< UNIT U009697 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:366-366 | ctx=core.message.module.bot_permission.restrict_members >>>
审阅次数：10
限制成员
<<< END U009697 >>>
<<< UNIT U009698 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:367-367 | ctx=core.message.module.bot_permission.send_messages >>>
审阅次数：10
发送消息
<<< END U009698 >>>
<<< UNIT U009699 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:368-368 | ctx=core.message.module.bot_permission.send_proactive_messages >>>
审阅次数：10
主动发送消息
<<< END U009699 >>>
<<< UNIT U009700 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:369-369 | ctx=core.message.module.bot_permission.unknown >>>
审阅次数：10
平台权限（${permission}）
<<< END U009700 >>>
<<< UNIT U009701 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:370-370 | ctx=core.message.module.disable.already >>>
审阅次数：10
失败：模块“${module}”已处于停用状态。
<<< END U009701 >>>
<<< UNIT U009702 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:371-371 | ctx=core.message.module.disable.base >>>
审阅次数：10
失败：“${module}”为基础模块，无法停用。
<<< END U009702 >>>
<<< UNIT U009703 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:372-372 | ctx=core.message.module.disable.failed >>>
审阅次数：10
失败：无法停用模块“${module}”。
<<< END U009703 >>>
<<< UNIT U009704 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:373-373 | ctx=core.message.module.disable.not_found >>>
审阅次数：10
失败：模块“${module}”不存在。
<<< END U009704 >>>
<<< UNIT U009705 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:374-374 | ctx=core.message.module.disable.success >>>
审阅次数：10
成功：已停用模块“${module}”。
<<< END U009705 >>>
<<< UNIT U009706 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:375-375 | ctx=core.message.module.enable.already >>>
审阅次数：10
失败：模块“${module}”已处于启用状态。
<<< END U009706 >>>
<<< UNIT U009707 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:376-376 | ctx=core.message.module.enable.event_permissions >>>
审阅次数：10
提示：事件模块依赖平台事件订阅、读取全部消息以及相应的{TERM:target}管理权限，请确认机器人已获得对应权限。
<<< END U009707 >>>
<<< UNIT U009708 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:377-377 | ctx=core.message.module.enable.not_found >>>
审阅次数：10
失败：模块“${module}”不存在。
<<< END U009708 >>>
<<< UNIT U009709 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:378-378 | ctx=core.message.module.enable.success >>>
审阅次数：10
成功：已启用模块“${module}”。
<<< END U009709 >>>
<<< UNIT U009710 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:379-379 | ctx=core.message.module.enable.unsupported_bot_permissions >>>
审阅次数：10
失败：机器人缺少启用模块所需的平台权限：${permissions}。请先授予对应权限后重试。
<<< END U009710 >>>
<<< UNIT U009711 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:380-380 | ctx=core.message.module.enable.unsupported_event >>>
审阅次数：10
失败：此{TERM:target}无法读取全部消息，不能启用事件模块，请先授予机器人对应权限。
<<< END U009711 >>>
<<< UNIT U009712 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:381-381 | ctx=core.message.module.enable.unsupported_regex >>>
审阅次数：10
失败：此{TERM:target}不支持正则表达式模块，请检查是否已开启对应权限。
<<< END U009712 >>>
<<< UNIT U009713 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:382-382 | ctx=core.message.module.enable.unsupported_rss >>>
审阅次数：10
失败：此{TERM:target}不支持主动推送模块，请检查是否已开启对应权限。
<<< END U009713 >>>
<<< UNIT U009714 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:383-383 | ctx=core.message.module.list.header >>>
审阅次数：10
模块列表
<<< END U009714 >>>
<<< UNIT U009715 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:384-384 | ctx=core.message.module.load.failed >>>
审阅次数：10
模块加载失败。
<<< END U009715 >>>
<<< UNIT U009716 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:385-385 | ctx=core.message.module.load.not_found >>>
审阅次数：10
失败：此模块已加载或不存在。
<<< END U009716 >>>
<<< UNIT U009717 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:386-386 | ctx=core.message.module.load.success >>>
审阅次数：10
成功加载模块：${module}
<<< END U009717 >>>
<<< UNIT U009718 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:387-387 | ctx=core.message.module.recommends >>>
审阅次数：10
建议同时启用以下模块：
${modules}
是否一并启用？
<<< END U009718 >>>
<<< UNIT U009719 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:388-388 | ctx=core.message.module.recommends.help >>>
审阅次数：10
模块“${module}”的帮助信息：
<<< END U009719 >>>
<<< UNIT U009720 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:389-389 | ctx=core.message.module.reload.confirm >>>
审阅次数：10
此操作将额外重载以下模块：
${modules}
是否继续？
<<< END U009720 >>>
<<< UNIT U009721 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:390-390 | ctx=core.message.module.reload.failed >>>
审阅次数：10
模块重载失败。
<<< END U009721 >>>
<<< UNIT U009722 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:391-391 | ctx=core.message.module.reload.no_more >>>
审阅次数：10
未检测到已加载的其他文件。
<<< END U009722 >>>
<<< UNIT U009723 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:392-392 | ctx=core.message.module.reload.not_found >>>
审阅次数：10
失败：模块“${module}”不存在。
<<< END U009723 >>>
<<< UNIT U009724 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:393-393 | ctx=core.message.module.reload.success >>>
审阅次数：10
成功重载模块：
${module}
<<< END U009724 >>>
<<< UNIT U009725 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:394-394 | ctx=core.message.module.reload.with >>>
审阅次数：10
以及此模块下的 ${reload_count} 个文件。
<<< END U009725 >>>
<<< UNIT U009726 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:395-395 | ctx=core.message.module.unload.base >>>
审阅次数：10
失败：模块“${module}”为基础模块，无法卸载。
<<< END U009726 >>>
<<< UNIT U009727 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:396-396 | ctx=core.message.module.unload.not_found >>>
审阅次数：10
失败：此模块不存在。
<<< END U009727 >>>
<<< UNIT U009728 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:397-397 | ctx=core.message.module.unload.success >>>
审阅次数：10
成功卸载模块：${module}
<<< END U009728 >>>
<<< UNIT U009729 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:398-398 | ctx=core.message.module.unload.unavailable.confirm >>>
审阅次数：10
此模块因发生错误而无法加载，此操作将在下一次重启后彻底禁用此模块，是否继续？
<<< END U009729 >>>
<<< UNIT U009730 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:399-399 | ctx=core.message.module.unsupported_language >>>
审阅次数：10
提示：模块“${module}”未支持当前语言，可能无法正常展示当前语言的内容。
<<< END U009730 >>>
<<< UNIT U009731 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:400-400 | ctx=core.message.mute.disable >>>
审阅次数：10
已解除禁止发言。
<<< END U009731 >>>
<<< UNIT U009732 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:401-401 | ctx=core.message.mute.enable >>>
审阅次数：10
已禁止发言。
<<< END U009732 >>>
<<< UNIT U009733 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:402-402 | ctx=core.message.petal >>>
审阅次数：10
当前用户 ${sender} 的花瓣数为 ${petal}。
<<< END U009733 >>>
<<< UNIT U009734 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:403-403 | ctx=core.message.petal.bud.code.exists >>>
审阅次数：10
此口令已被占用。
<<< END U009734 >>>
<<< UNIT U009735 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:404-404 | ctx=core.message.petal.bud.count.invalid >>>
审阅次数：10
无效的次数，必须为正整数且不超过花瓣数量。
<<< END U009735 >>>
<<< UNIT U009736 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:405-405 | ctx=core.message.petal.bud.info >>>
审阅次数：10
发送者：${sender}
口令：${code}
总量：${total} 片｜已领取：${claimed}/${count} 次
领取记录：
<<< END U009736 >>>
<<< UNIT U009737 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:406-406 | ctx=core.message.petal.bud.info.not_found >>>
审阅次数：10
未找到此花苞。
<<< END U009737 >>>
<<< UNIT U009738 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:407-407 | ctx=core.message.petal.bud.info.record >>>
审阅次数：10
${sender}：${amount} 片
<<< END U009738 >>>
<<< UNIT U009739 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:408-408 | ctx=core.message.petal.bud.receive.already >>>
审阅次数：10
已领取过此花苞。
<<< END U009739 >>>
<<< UNIT U009740 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:409-409 | ctx=core.message.petal.bud.receive.empty >>>
审阅次数：10
此花苞已全部领取完毕。
<<< END U009740 >>>
<<< UNIT U009741 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:410-410 | ctx=core.message.petal.bud.receive.not_found >>>
审阅次数：10
未找到匹配的花苞，请检查口令是否正确。
<<< END U009741 >>>
<<< UNIT U009742 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:411-411 | ctx=core.message.petal.bud.receive.success >>>
审阅次数：10
领取成功。
<<< END U009742 >>>
<<< UNIT U009743 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:412-412 | ctx=core.message.petal.bud.release >>>
审阅次数：10
已释放 ${count} 个过期花苞。
<<< END U009743 >>>
<<< UNIT U009744 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:413-413 | ctx=core.message.petal.bud.release.none >>>
审阅次数：10
没有需要释放的过期花苞。
<<< END U009744 >>>
<<< UNIT U009745 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:414-414 | ctx=core.message.petal.bud.send.confirm >>>
审阅次数：10
此操作将花费 ${total} 片花瓣，发出可领取 ${count} 次的花苞（口令：${code}）。是否继续？
<<< END U009745 >>>
<<< UNIT U009746 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:415-415 | ctx=core.message.petal.bud.send.success >>>
审阅次数：10
花苞已成功发送。共 ${total} 片花瓣，可领取 ${count} 次。
ID：${id}
使用“${cmd}”可领取此花苞。
<<< END U009746 >>>
<<< UNIT U009747 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:416-416 | ctx=core.message.petal.clear >>>
审阅次数：10
已清空用户 ${sender} 的全部花瓣。
<<< END U009747 >>>
<<< UNIT U009748 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:417-417 | ctx=core.message.petal.clear.self >>>
审阅次数：10
已清空全部花瓣。
<<< END U009748 >>>
<<< UNIT U009749 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:418-418 | ctx=core.message.petal.give.confirm >>>
审阅次数：10
此操作会将 ${give_petal} 片花瓣赠予用户 ${sender}，是否继续？
<<< END U009749 >>>
<<< UNIT U009750 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:419-419 | ctx=core.message.petal.give.self >>>
审阅次数：10
无法将花瓣赠予自己。
<<< END U009750 >>>
<<< UNIT U009751 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:420-420 | ctx=core.message.petal.give.success >>>
审阅次数：10
已将 ${give_petal} 片花瓣赠予用户 ${sender}，当前花瓣数为 ${petal}。
<<< END U009751 >>>
<<< UNIT U009752 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:421-421 | ctx=core.message.petal.modify >>>
审阅次数：10
已为用户 ${sender} 调整 ${add_petal} 片花瓣，当前花瓣数为 ${petal}。
<<< END U009752 >>>
<<< UNIT U009753 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:422-422 | ctx=core.message.petal.modify.self >>>
审阅次数：10
已调整 ${add_petal} 片花瓣，当前花瓣数为 ${petal}。
<<< END U009753 >>>
<<< UNIT U009754 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:423-423 | ctx=core.message.petal.self >>>
审阅次数：10
当前花瓣数为 ${petal}。
<<< END U009754 >>>
<<< UNIT U009755 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:424-424 | ctx=core.message.petal.sign.already >>>
审阅次数：10
今日已完成签到，请明日再试。
<<< END U009755 >>>
<<< UNIT U009756 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:425-425 | ctx=core.message.petal.sign.disabled >>>
审阅次数：10
此{TERM:target}已停用签到功能。
<<< END U009756 >>>
<<< UNIT U009757 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:426-426 | ctx=core.message.petal.sign.success >>>
审阅次数：10
签到成功。
<<< END U009757 >>>
<<< UNIT U009758 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:427-427 | ctx=core.message.post.confirm >>>
审阅次数：10
此操作将会为{TERM:target} ${target} 推送以下消息，是否继续？
<<< END U009758 >>>
<<< UNIT U009759 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:428-428 | ctx=core.message.post.global.confirm >>>
审阅次数：10
警告：此操作将会为全部{TERM:target}推送以下消息，是否继续？
<<< END U009759 >>>
<<< UNIT U009760 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:429-429 | ctx=core.message.post.prefix >>>
审阅次数：10
[推送消息]
<<< END U009760 >>>
<<< UNIT U009761 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:430-430 | ctx=core.message.post.success >>>
审阅次数：10
推送消息完成。
<<< END U009761 >>>
<<< UNIT U009762 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:431-431 | ctx=core.message.purge.empty >>>
审阅次数：10
当前缓存目录为空。
<<< END U009762 >>>
<<< UNIT U009763 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:432-432 | ctx=core.message.purge.success >>>
审阅次数：10
成功清除缓存。
<<< END U009763 >>>
<<< UNIT U009764 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:433-433 | ctx=core.message.raise >>>
审阅次数：10
异常测试
<<< END U009764 >>>
<<< UNIT U009765 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:434-434 | ctx=core.message.restart.prompt >>>
审阅次数：10
由于机器人正在执行重启，当前命令的后续流程已被终止。
请等待重启完成后重新执行。
<<< END U009765 >>>
<<< UNIT U009766 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:435-435 | ctx=core.message.restart.restarting >>>
审阅次数：10
重启中……
<<< END U009766 >>>
<<< UNIT U009767 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:436-436 | ctx=core.message.restart.timeout >>>
审阅次数：10
等待已超时，强制重启中……
<<< END U009767 >>>
<<< UNIT U009768 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:437-437 | ctx=core.message.restart.wait >>>
审阅次数：10
有 ${count} 个命令正在执行中，将于执行完毕后重启。
<<< END U009768 >>>
<<< UNIT U009769 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:438-438 | ctx=core.message.resume.clear >>>
审阅次数：10
已清理全部消息。
<<< END U009769 >>>
<<< UNIT U009770 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:439-439 | ctx=core.message.resume.done >>>
审阅次数：10
重发完成。
<<< END U009770 >>>
<<< UNIT U009771 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:440-440 | ctx=core.message.resume.nothing >>>
审阅次数：10
没有需要重发的消息。
<<< END U009771 >>>
<<< UNIT U009772 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:441-441 | ctx=core.message.resume.processing >>>
审阅次数：10
正在重发 ${counts} 条消息……
<<< END U009772 >>>
<<< UNIT U009773 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:442-442 | ctx=core.message.resume.skip >>>
审阅次数：10
跳过一条消息，正在重发 ${counts} 条消息……
<<< END U009773 >>>
<<< UNIT U009774 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:443-443 | ctx=core.message.set.module.disable.failed >>>
审阅次数：10
未执行任何修改，模块可能处于未启用状态或不存在。
<<< END U009774 >>>
<<< UNIT U009775 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:444-444 | ctx=core.message.set.module.disable.success >>>
审阅次数：10
成功为{TERM:target}停用以下模块：${modules}
<<< END U009775 >>>
<<< UNIT U009776 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:445-445 | ctx=core.message.set.module.enable.failed >>>
审阅次数：10
未执行任何修改，模块可能不存在。
<<< END U009776 >>>
<<< UNIT U009777 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:446-446 | ctx=core.message.set.module.enable.success >>>
审阅次数：10
成功为{TERM:target}启用以下模块：${modules}
<<< END U009777 >>>
<<< UNIT U009778 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:447-447 | ctx=core.message.set.module.list >>>
审阅次数：10
此{TERM:target}已启用的模块：
<<< END U009778 >>>
<<< UNIT U009779 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:448-448 | ctx=core.message.set.module.list.none >>>
审阅次数：10
此{TERM:target}未启用任何模块。
<<< END U009779 >>>
<<< UNIT U009780 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:449-449 | ctx=core.message.set.option.edit.success >>>
审阅次数：10
成功为{TERM:target}设置了以下参数：${k} -> ${v}
<<< END U009780 >>>
<<< UNIT U009781 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:450-450 | ctx=core.message.setup.check.disable >>>
审阅次数：10
已停用命令语法检查提示。
<<< END U009781 >>>
<<< UNIT U009782 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:451-451 | ctx=core.message.setup.check.enable >>>
审阅次数：10
已启用命令语法检查提示。
<<< END U009782 >>>
<<< UNIT U009783 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:452-452 | ctx=core.message.setup.cooldown.success >>>
审阅次数：10
已将命令冷却时间设置为 ${time} 秒。
<<< END U009783 >>>
<<< UNIT U009784 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:453-453 | ctx=core.message.setup.emote.disable >>>
审阅次数：10
已停用在{TERM:target}内发送表情。
<<< END U009784 >>>
<<< UNIT U009785 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:454-454 | ctx=core.message.setup.emote.enable >>>
审阅次数：10
已启用在{TERM:target}内发送表情。
<<< END U009785 >>>
<<< UNIT U009786 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:455-455 | ctx=core.message.setup.invalid-module-prompt.disable >>>
审阅次数：10
已停用“模块不存在”提示。
<<< END U009786 >>>
<<< UNIT U009787 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:456-456 | ctx=core.message.setup.invalid-module-prompt.enable >>>
审阅次数：10
已启用“模块不存在”提示。
<<< END U009787 >>>
<<< UNIT U009788 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:457-457 | ctx=core.message.setup.list.action.add >>>
审阅次数：10
添加
<<< END U009788 >>>
<<< UNIT U009789 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:458-458 | ctx=core.message.setup.list.action.modify >>>
审阅次数：10
修改
<<< END U009789 >>>
<<< UNIT U009790 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:459-459 | ctx=core.message.setup.list.action.off >>>
审阅次数：10
停用
<<< END U009790 >>>
<<< UNIT U009791 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:460-460 | ctx=core.message.setup.list.action.on >>>
审阅次数：10
启用
<<< END U009791 >>>
<<< UNIT U009792 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:461-461 | ctx=core.message.setup.list.button.sender >>>
审阅次数：10
💬 用户设置
<<< END U009792 >>>
<<< UNIT U009793 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:462-462 | ctx=core.message.setup.list.button.target >>>
审阅次数：10
👥 {TERM:target}设置
<<< END U009793 >>>
<<< UNIT U009794 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:463-463 | ctx=core.message.setup.list.item.check >>>
审阅次数：10
拼写检查
<<< END U009794 >>>
<<< UNIT U009795 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:464-464 | ctx=core.message.setup.list.item.cooldown >>>
审阅次数：10
命令冷却
<<< END U009795 >>>
<<< UNIT U009796 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:465-465 | ctx=core.message.setup.list.item.emote >>>
审阅次数：10
使用表情
<<< END U009796 >>>
<<< UNIT U009797 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:466-466 | ctx=core.message.setup.list.item.invalid-module-prompt >>>
审阅次数：10
“模块不存在”提示
<<< END U009797 >>>
<<< UNIT U009798 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:467-467 | ctx=core.message.setup.list.item.locale >>>
审阅次数：10
语言
<<< END U009798 >>>
<<< UNIT U009799 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:468-468 | ctx=core.message.setup.list.item.markdown >>>
审阅次数：10
Markdown 消息
<<< END U009799 >>>
<<< UNIT U009800 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:469-469 | ctx=core.message.setup.list.item.mute >>>
审阅次数：10
禁止发言
<<< END U009800 >>>
<<< UNIT U009801 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:470-470 | ctx=core.message.setup.list.item.prefix >>>
审阅次数：10
自定义前缀
<<< END U009801 >>>
<<< UNIT U009802 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:471-471 | ctx=core.message.setup.list.item.sign >>>
审阅次数：10
签到
<<< END U009802 >>>
<<< UNIT U009803 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:472-472 | ctx=core.message.setup.list.item.theme >>>
审阅次数：10
深色模式
<<< END U009803 >>>
<<< UNIT U009804 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:473-473 | ctx=core.message.setup.list.item.timeoffset >>>
审阅次数：10
时间偏移
<<< END U009804 >>>
<<< UNIT U009805 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:474-474 | ctx=core.message.setup.list.item.timezone >>>
审阅次数：10
显示时区
<<< END U009805 >>>
<<< UNIT U009806 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:475-475 | ctx=core.message.setup.list.item.typing >>>
审阅次数：10
输入提示
<<< END U009806 >>>
<<< UNIT U009807 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:476-476 | ctx=core.message.setup.list.readonly >>>
审阅次数：10
修改以下设置需要管理员权限。
<<< END U009807 >>>
<<< UNIT U009808 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:478-478 | ctx=core.message.setup.list.sender >>>
审阅次数：10
【用户设置】
<<< END U009808 >>>
<<< UNIT U009809 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:479-479 | ctx=core.message.setup.list.target >>>
审阅次数：10
【{TERM:target}设置】
<<< END U009809 >>>
<<< UNIT U009810 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:480-480 | ctx=core.message.setup.list.value.cooldown >>>
审阅次数：10
${time} 秒
<<< END U009810 >>>
<<< UNIT U009811 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:481-481 | ctx=core.message.setup.list.value.off >>>
审阅次数：10
已停用
<<< END U009811 >>>
<<< UNIT U009812 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:482-482 | ctx=core.message.setup.list.value.on >>>
审阅次数：10
已启用
<<< END U009812 >>>
<<< UNIT U009813 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:484-484 | ctx=core.message.setup.locale.contribute >>>
审阅次数：10
欢迎前往协助翻译：${url}
<<< END U009813 >>>
<<< UNIT U009814 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:485-485 | ctx=core.message.setup.locale.langlist >>>
审阅次数：10
支持的语言列表：
${langlist}
<<< END U009814 >>>
<<< UNIT U009815 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:486-486 | ctx=core.message.setup.locale.prompt >>>
审阅次数：10
当前使用的语言：${lang}
<<< END U009815 >>>
<<< UNIT U009816 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:487-487 | ctx=core.message.setup.locale.reload.failed >>>
审阅次数：10
以下字符串重载失败：
<<< END U009816 >>>
<<< UNIT U009817 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:488-488 | ctx=core.message.setup.locale.set.invalid >>>
审阅次数：10
语言代码格式无效。
<<< END U009817 >>>
<<< UNIT U009818 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:489-489 | ctx=core.message.setup.locale.set.prompt >>>
审阅次数：10
请使用“${cmd}<语言代码>”设置语言。
<<< END U009818 >>>
<<< UNIT U009819 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:490-490 | ctx=core.message.setup.locale.translation_progress >>>
审阅次数：10
${name}的进度为 ${percent}%，欢迎前往 Weblate 参与翻译：
<<< END U009819 >>>
<<< UNIT U009820 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:491-491 | ctx=core.message.setup.markdown.disable >>>
审阅次数：10
已停用 Markdown 消息。
<<< END U009820 >>>
<<< UNIT U009821 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:492-492 | ctx=core.message.setup.markdown.enable >>>
审阅次数：10
已启用 Markdown 消息。
<<< END U009821 >>>
<<< UNIT U009822 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:493-493 | ctx=core.message.setup.markdown.unsupported >>>
审阅次数：10
此平台不支持 Markdown 消息。
<<< END U009822 >>>
<<< UNIT U009823 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:494-494 | ctx=core.message.setup.prefix.add.already >>>
审阅次数：10
此命令前缀已存在于自定义前缀列表中。
<<< END U009823 >>>
<<< UNIT U009824 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:495-495 | ctx=core.message.setup.prefix.add.success >>>
审阅次数：10
已添加自定义命令前缀：${prefix}
<<< END U009824 >>>
<<< UNIT U009825 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:496-496 | ctx=core.message.setup.prefix.list.custom >>>
审阅次数：10
自定义命令前缀：${prefixes}
<<< END U009825 >>>
<<< UNIT U009826 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:497-497 | ctx=core.message.setup.prefix.list.custom.none >>>
审阅次数：10
自定义命令前缀列表当前为空。
<<< END U009826 >>>
<<< UNIT U009827 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:498-498 | ctx=core.message.setup.prefix.list.default >>>
审阅次数：10
默认命令前缀：${prefixes}
<<< END U009827 >>>
<<< UNIT U009828 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:499-499 | ctx=core.message.setup.prefix.remove.not_found >>>
审阅次数：10
此命令前缀不存在于自定义前缀列表中。
<<< END U009828 >>>
<<< UNIT U009829 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:500-500 | ctx=core.message.setup.prefix.remove.success >>>
审阅次数：10
已移除自定义命令前缀：${prefix}
<<< END U009829 >>>
<<< UNIT U009830 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:501-501 | ctx=core.message.setup.prefix.reset >>>
审阅次数：10
已重置自定义命令前缀列表。
<<< END U009830 >>>
<<< UNIT U009831 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:502-502 | ctx=core.message.setup.sign.disable >>>
审阅次数：10
已停用签到。
<<< END U009831 >>>
<<< UNIT U009832 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:503-503 | ctx=core.message.setup.sign.enable >>>
审阅次数：10
已启用签到。
<<< END U009832 >>>
<<< UNIT U009833 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:504-504 | ctx=core.message.setup.dark.disable >>>
审阅次数：10
已停用深色模式。
<<< END U009833 >>>
<<< UNIT U009834 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:505-505 | ctx=core.message.setup.dark.enable >>>
审阅次数：10
已启用深色模式。
<<< END U009834 >>>
<<< UNIT U009835 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:506-506 | ctx=core.message.setup.timeoffset.invalid >>>
审阅次数：10
时间偏移量格式无效。
<<< END U009835 >>>
<<< UNIT U009836 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:507-507 | ctx=core.message.setup.timeoffset.reset >>>
审阅次数：10
已将{TERM:target}时区恢复为默认值。
<<< END U009836 >>>
<<< UNIT U009837 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:508-508 | ctx=core.message.setup.timeoffset.success >>>
审阅次数：10
已将{TERM:target}时区设置为 UTC${offset}。
<<< END U009837 >>>
<<< UNIT U009838 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:509-509 | ctx=core.message.setup.timezone.invalid >>>
审阅次数：10
时区偏移量格式无效。
<<< END U009838 >>>
<<< UNIT U009839 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:510-510 | ctx=core.message.setup.timezone.reset >>>
审阅次数：10
已恢复跟随{TERM:target}时区。
<<< END U009839 >>>
<<< UNIT U009840 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:511-511 | ctx=core.message.setup.timezone.success >>>
审阅次数：10
已将用户显示时区设置为 UTC${offset}。
<<< END U009840 >>>
<<< UNIT U009841 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:512-512 | ctx=core.message.setup.typing.disable >>>
审阅次数：10
已停用输入提示。
<<< END U009841 >>>
<<< UNIT U009842 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:513-513 | ctx=core.message.setup.typing.enable >>>
审阅次数：10
已启用输入提示。
<<< END U009842 >>>
<<< UNIT U009843 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:514-514 | ctx=core.message.superuser.add.success >>>
审阅次数：10
成功将用户 ${sender} 设置为超级用户。
<<< END U009843 >>>
<<< UNIT U009844 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:515-515 | ctx=core.message.superuser.already >>>
审阅次数：10
此用户已属于超级用户。
<<< END U009844 >>>
<<< UNIT U009845 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:516-516 | ctx=core.message.superuser.remove.confirm >>>
审阅次数：10
即将移除自身的超级用户权限，请确认是否继续。
<<< END U009845 >>>
<<< UNIT U009846 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:517-517 | ctx=core.message.superuser.remove.confirm.token >>>
审阅次数：10
我确定移除我自己的超级用户权限。
<<< END U009846 >>>
<<< UNIT U009847 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:518-518 | ctx=core.message.superuser.remove.success >>>
审阅次数：10
成功将用户 ${sender} 移出超级用户。
<<< END U009847 >>>
<<< UNIT U009848 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:519-519 | ctx=core.message.update.binary_mode >>>
审阅次数：10
机器人处于二进制部署模式，无法执行更新。请手动下载最新版本的二进制文件并完成替换。
<<< END U009848 >>>
<<< UNIT U009849 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:520-520 | ctx=core.message.update.failed >>>
审阅次数：10
从 GitHub 获取更新失败。
<<< END U009849 >>>
<<< UNIT U009850 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:521-521 | ctx=core.message.url-audit.allowlist.add.exists >>>
审阅次数：10
规则已存在于全局 URL 允许列表中：${rule}
<<< END U009850 >>>
<<< UNIT U009851 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:522-522 | ctx=core.message.url-audit.allowlist.add.success >>>
审阅次数：10
已将规则加入用户自定义 URL 允许列表：${rule}
<<< END U009851 >>>
<<< UNIT U009852 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:523-523 | ctx=core.message.url-audit.allowlist.error.invalid >>>
审阅次数：10
URL 允许列表规则格式无效：${reason}
<<< END U009852 >>>
<<< UNIT U009853 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:524-524 | ctx=core.message.url-audit.allowlist.error.reason.broad_regex >>>
审阅次数：10
正则表达式的匹配范围过宽
<<< END U009853 >>>
<<< UNIT U009854 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:525-525 | ctx=core.message.url-audit.allowlist.error.reason.file_too_large >>>
审阅次数：10
用户自定义允许列表文件超过大小限制
<<< END U009854 >>>
<<< UNIT U009855 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:526-526 | ctx=core.message.url-audit.allowlist.error.reason.invalid_regex >>>
审阅次数：10
正则表达式格式不正确或长度超限
<<< END U009855 >>>
<<< UNIT U009856 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:527-527 | ctx=core.message.url-audit.allowlist.error.reason.invalid_url >>>
审阅次数：10
仅支持不包含登录信息的有效 HTTP(S) URL
<<< END U009856 >>>
<<< UNIT U009857 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:528-528 | ctx=core.message.url-audit.allowlist.error.reason.too_many_regex >>>
审阅次数：10
正则表达式规则数量已达到上限
<<< END U009857 >>>
<<< UNIT U009858 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:529-529 | ctx=core.message.url-audit.allowlist.error.reason.too_many_rules >>>
审阅次数：10
允许列表规则总数已达到上限
<<< END U009858 >>>
<<< UNIT U009859 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:530-530 | ctx=core.message.url-audit.allowlist.error.reason.unsafe_regex >>>
审阅次数：10
正则表达式包含不安全的高级构造或执行超时
<<< END U009859 >>>
<<< UNIT U009860 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:531-531 | ctx=core.message.url-audit.allowlist.list.empty >>>
审阅次数：10
全局 URL 允许列表当前不存在规则。
<<< END U009860 >>>
<<< UNIT U009861 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:532-532 | ctx=core.message.url-audit.allowlist.list.result >>>
审阅次数：10
全局 URL 允许列表规则：
${rules}
<<< END U009861 >>>
<<< UNIT U009862 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:533-533 | ctx=core.message.url-audit.allowlist.list.title >>>
审阅次数：10
全局 URL 允许列表规则：
<<< END U009862 >>>
<<< UNIT U009863 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:534-534 | ctx=core.message.url-audit.allowlist.query.allowed >>>
审阅次数：10
${url} 已被以下全局规则放行：
${rules}
<<< END U009863 >>>
<<< UNIT U009864 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:535-535 | ctx=core.message.url-audit.allowlist.query.denied >>>
审阅次数：10
${url} 未被全局 URL 允许列表放行。
<<< END U009864 >>>
<<< UNIT U009865 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:536-536 | ctx=core.message.url-audit.allowlist.remove.missing >>>
审阅次数：10
用户自定义允许列表中不存在此规则：${rule}
<<< END U009865 >>>
<<< UNIT U009866 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:537-537 | ctx=core.message.url-audit.allowlist.remove.success >>>
审阅次数：10
已从用户自定义 URL 允许列表删除规则：${rule}
<<< END U009866 >>>
<<< UNIT U009867 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:538-538 | ctx=core.message.url-audit.allowlist.source.global >>>
审阅次数：10
全局规则
<<< END U009867 >>>
<<< UNIT U009868 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:539-539 | ctx=core.message.url-audit.allowlist.source.user >>>
审阅次数：10
用户规则
<<< END U009868 >>>
<<< UNIT U009869 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:540-540 | ctx=core.message.url-audit.blocklist.add.exists >>>
审阅次数：10
规则已存在于全局 URL 阻止列表中：${rule}
<<< END U009869 >>>
<<< UNIT U009870 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:541-541 | ctx=core.message.url-audit.blocklist.add.success >>>
审阅次数：10
已将规则加入用户自定义 URL 阻止列表：${rule}
<<< END U009870 >>>
<<< UNIT U009871 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:542-542 | ctx=core.message.url-audit.blocklist.error.invalid >>>
审阅次数：10
URL 阻止列表规则格式无效：${reason}
<<< END U009871 >>>
<<< UNIT U009872 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:543-543 | ctx=core.message.url-audit.blocklist.error.reason.broad_regex >>>
审阅次数：10
正则表达式的匹配范围过宽
<<< END U009872 >>>
<<< UNIT U009873 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:544-544 | ctx=core.message.url-audit.blocklist.error.reason.file_too_large >>>
审阅次数：10
用户自定义阻止列表文件超过大小限制
<<< END U009873 >>>
<<< UNIT U009874 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:545-545 | ctx=core.message.url-audit.blocklist.error.reason.invalid_regex >>>
审阅次数：10
正则表达式格式不正确或长度超限
<<< END U009874 >>>
<<< UNIT U009875 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:546-546 | ctx=core.message.url-audit.blocklist.error.reason.invalid_url >>>
审阅次数：10
仅支持不包含登录信息的有效 HTTP(S) URL
<<< END U009875 >>>
<<< UNIT U009876 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:547-547 | ctx=core.message.url-audit.blocklist.error.reason.too_many_regex >>>
审阅次数：10
正则表达式规则数量已达到上限
<<< END U009876 >>>
<<< UNIT U009877 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:548-548 | ctx=core.message.url-audit.blocklist.error.reason.too_many_rules >>>
审阅次数：10
阻止列表规则总数已达到上限
<<< END U009877 >>>
<<< UNIT U009878 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:549-549 | ctx=core.message.url-audit.blocklist.error.reason.unsafe_regex >>>
审阅次数：10
正则表达式包含不安全的高级构造或执行超时
<<< END U009878 >>>
<<< UNIT U009879 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:550-550 | ctx=core.message.url-audit.blocklist.list.empty >>>
审阅次数：10
全局 URL 阻止列表当前不存在规则。
<<< END U009879 >>>
<<< UNIT U009880 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:551-551 | ctx=core.message.url-audit.blocklist.list.result >>>
审阅次数：10
全局 URL 阻止列表规则：
${rules}
<<< END U009880 >>>
<<< UNIT U009881 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:552-552 | ctx=core.message.url-audit.blocklist.list.title >>>
审阅次数：10
全局 URL 阻止列表规则：
<<< END U009881 >>>
<<< UNIT U009882 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:553-553 | ctx=core.message.url-audit.blocklist.query.allowed >>>
审阅次数：10
${url} 未被全局 URL 阻止列表拦截。
<<< END U009882 >>>
<<< UNIT U009883 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:554-554 | ctx=core.message.url-audit.blocklist.query.blocked >>>
审阅次数：10
${url} 已被以下全局规则拦截：
${rules}
<<< END U009883 >>>
<<< UNIT U009884 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:555-555 | ctx=core.message.url-audit.blocklist.remove.missing >>>
审阅次数：10
用户自定义阻止列表中不存在此规则：${rule}
<<< END U009884 >>>
<<< UNIT U009885 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:556-556 | ctx=core.message.url-audit.blocklist.remove.success >>>
审阅次数：10
已从用户自定义 URL 阻止列表删除规则：${rule}
<<< END U009885 >>>
<<< UNIT U009886 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:557-557 | ctx=core.message.url-audit.blocklist.source.global >>>
审阅次数：10
全局规则
<<< END U009886 >>>
<<< UNIT U009887 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:558-558 | ctx=core.message.url-audit.blocklist.source.user >>>
审阅次数：10
用户规则
<<< END U009887 >>>
<<< UNIT U009888 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:559-559 | ctx=core.message.url-audit.list.table.header.rule >>>
审阅次数：10
规则
<<< END U009888 >>>
<<< UNIT U009889 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:560-560 | ctx=core.message.url-audit.list.table.header.source >>>
审阅次数：10
来源
<<< END U009889 >>>
<<< UNIT U009890 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:561-561 | ctx=core.message.url-audit.list.table.header.type >>>
审阅次数：10
类型
<<< END U009890 >>>
<<< UNIT U009891 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:562-562 | ctx=core.message.url-audit.list.table.type.exact >>>
审阅次数：10
精确 URL
<<< END U009891 >>>
<<< UNIT U009892 | json-value | packages/akari-bot-core/akaribot/modules/core/locales/zh_cn.json:563-563 | ctx=core.message.url-audit.list.table.type.regex >>>
审阅次数：10
正则表达式
<<< END U009892 >>>
<<< UNIT U009893 | cfg-comment | packages/akari-bot-core/akaribot/modules/core/manifest.toml:1-1 >>>
审阅次数：10
# akari-bot-core 的包清单。
<<< END U009893 >>>
<<< UNIT U009894 | cfg-comment | packages/akari-bot-core/akaribot/modules/core/manifest.toml:5-5 >>>
审阅次数：10
# 随 core 一并分发的模块注册名称，提取自包内全部 module() 调用。
<<< END U009894 >>>
<<< UNIT U009895 | cfg-comment | packages/akari-bot-core/akaribot/modules/core/manifest.toml:45-46 >>>
审阅次数：10
# 核心包拥有的数据表，取自 akaribot/core/database/models.py 的 Meta.table。
# 随 core 分发的模块目录内没有 database/models.py。
<<< END U009895 >>>
<<< UNIT U009896 | py-docstring | packages/akari-bot-core/akaribot/modules/core/su_tools/__init__.py:1-1 | ctx=<module> >>>
审阅次数：10
超级用户与系统运维命令。
<<< END U009896 >>>
<<< UNIT U009897 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/analytics.py:30-30 >>>
审阅次数：10
# matplotlib 是 core 体积最大的可选依赖（extra ``image``），默认安装不引入，绘图命令据此执行降级处理。
<<< END U009897 >>>
<<< UNIT U009898 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/analytics.py:58-58 >>>
审阅次数：10
# 标注相对其数据点向上占用的像素高度，额外预留 4 磅间距避免标注紧贴顶部边框。
<<< END U009898 >>>
<<< UNIT U009899 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/analytics.py:70-70 >>>
审阅次数：10
# 将最高点放置于“坐标区顶端向下 headroom 像素”处。取较大者以确保仅抬高而不压缩。
<<< END U009899 >>>
<<< UNIT U009900 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/analytics.py:120-120 >>>
审阅次数：10
# 零点在循环外部获取一次，避免逐次取值在跨越零点时将前后两天的边界混合。
<<< END U009900 >>>
<<< UNIT U009901 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/analytics.py:167-167 >>>
审阅次数：10
# 本月一日在循环外部获取一次，避免逐次取值在跨越零点时将前后两个月的边界混合。
<<< END U009901 >>>
<<< UNIT U009902 | py-docstring | packages/akari-bot-core/akaribot/modules/core/su_tools/analytics.py:39-49 | ctx=annotate_points >>>
审阅次数：10
在折线的各数据点上方标注数值，并按需抬高 y 轴上限。

标注按相对数据点的像素偏移放置，此类标注不参与坐标轴自动缩放，默认 5% 的上边距
无法容纳最高点的标注，标注会超出坐标区。因此在绘制后测算标注实际向上占用的像素高度，
随后据此推算 y 轴上限的调整目标，该计算逻辑与数据量级及图幅大小均无关。

:param plt: ``matplotlib.pyplot`` 模块。
:param data_x: 横轴刻度。
:param data_y: 纵轴数值。
<<< END U009902 >>>
<<< UNIT U009903 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/config.py:49-49 >>>
审阅次数：10
# 新建配置项会改变配置文件结构，与修改已有值不同，需要执行额外确认。
<<< END U009903 >>>
<<< UNIT U009904 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/features.py:31-31 >>>
审阅次数：10
# 差异项附加星号标记，聊天窗口中不支持颜色显示。
<<< END U009904 >>>
<<< UNIT U009905 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/features.py:37-37 >>>
审阅次数：10
# 特性名是代码标识符，不能参与文本替换。
<<< END U009905 >>>
<<< UNIT U009906 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/update.py:26-26 >>>
审阅次数：10
# CLI 可执行文件的定位途径（T7.2）依次为 CLI 注入的环境变量、解释器同目录，最后查 PATH。
<<< END U009906 >>>
<<< UNIT U009907 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/update.py:30-30 >>>
审阅次数：10
# 只读标记与实例根目录的环境变量名。两者均不属于 core 公开接口，因此按照引导代码的方式定义为字面量。
<<< END U009907 >>>
<<< UNIT U009908 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/update.py:34-34 >>>
审阅次数：10
# 传递给 CLI 的参数固定且不接受用户输入拼接，其中 --all 覆盖全部已安装包，--json 确保输出结果可解析。
<<< END U009908 >>>
<<< UNIT U009909 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/update.py:37-37 >>>
审阅次数：10
# 更新流程由子进程执行 uv 下载、补全配置与数据库迁移，等待上限按分钟计。
<<< END U009909 >>>
<<< UNIT U009910 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/update.py:40-40 >>>
审阅次数：10
# 返回结果附带的错误输出行数上限，避免将 CLI 的完整日志输出至会话中。
<<< END U009910 >>>
<<< UNIT U009911 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/update.py:112-112 >>>
审阅次数：10
# 只读标记仅约束 Server 自身，由于更新过程需要写入配置，需要使子进程按照宿主机 CLI 的权限执行。
<<< END U009911 >>>
<<< UNIT U009912 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/update.py:219-220 >>>
审阅次数：10
# 新版 CLI 直接回传 ``reload_pending``。历史版本仅回传 ``notified`` 明细，据此推导。
# 两者均缺失时，保守地将全部已更新的包视为待重载。
<<< END U009912 >>>
<<< UNIT U009913 | py-comment | packages/akari-bot-core/akaribot/modules/core/su_tools/update.py:277-277 >>>
审阅次数：10
# 缺少 reload_pending 字段说明 CLI 版本较旧，此时保守地提示重启，而非假定已完成热加载。
<<< END U009913 >>>
<<< UNIT U009914 | cfg-comment | packages/akari-bot-core/pyproject.toml:31-31 >>>
审阅次数：10
    # bundled modules/core 的 ~ping 顶层导入，按 T4.2 §3 裁决 1 留在必需依赖。
<<< END U009914 >>>
<<< UNIT U009915 | cfg-comment | packages/akari-bot-core/pyproject.toml:33-33 >>>
审阅次数：10
    # bundled modules/core 的 analytics.py 顶层导入，根 pyproject 未声明（T4.2 §7.12）。
<<< END U009915 >>>
<<< UNIT U009916 | cfg-comment | packages/akari-bot-core/pyproject.toml:58-58 >>>
审阅次数：10
# matplotlib 体积大且 ~analytics 支持降级，按照 T4.2 §3 裁决 2 归入 extra。chart 是 plan:591 的历史名称，保留为别名。
<<< END U009916 >>>
<<< UNIT U009917 | cfg-comment | packages/akari-bot-core/pyproject.toml:61-63 >>>
审阅次数：10
# CLI 的默认安装集合（T3.3）包含 s3 / mysql / image 三个常规 extra 加上 emotes 与 brand 两个资源包，与
# Dockerfile 的 --all-extras 开箱依赖一致，chart 与 image 同义，不重复列出。`akaribot init --minimal` 仅安装最小
# core，跳过完整套件；此时 ~about 不携带配图、SMTP 报告不携带标志，其余功能正常（参见 core/utils/brand.py）。
<<< END U009917 >>>
<<< UNIT U009918 | py-comment | packages/akari-bot-core/tests/test_about.py:25-25 >>>
审阅次数：10
# 立绘通过 akari-bot-assets-brand 资源包分发。实例 assets/ 可覆盖，因此按照同一入口获取期望路径。
<<< END U009918 >>>
<<< UNIT U009919 | py-docstring | packages/akari-bot-core/tests/test_about.py:178-178 | ctx=test_about >>>
审阅次数：10
akaribot.modules.core.common_tools.about 的 ~about 菜单测试。
<<< END U009919 >>>
<<< UNIT U009920 | py-comment | packages/akari-bot-core/tests/test_action_text.py:70-70 >>>
审阅次数：10
# 无会话时回退到半角括号。
<<< END U009920 >>>
<<< UNIT U009921 | py-comment | packages/akari-bot-core/tests/test_action_text.py:133-133 >>>
审阅次数：10
# 内层已解析为纯文本元素。
<<< END U009921 >>>
<<< UNIT U009922 | py-comment | packages/akari-bot-core/tests/test_action_text.py:202-202 >>>
审阅次数：10
# message.brackets 的值为“（${msg}）”，借此构造一个前后均包含文本的测试语句。
<<< END U009922 >>>
<<< UNIT U009923 | py-comment | packages/akari-bot-core/tests/test_action_text.py:207-207 >>>
审阅次数：10
# 元素前后的括号应作为纯文本保留。
<<< END U009923 >>>
<<< UNIT U009924 | py-comment | packages/akari-bot-core/tests/test_action_text.py:343-343 >>>
审阅次数：10
# 默认值不写入 KE 码，还原后仍然为 True。
<<< END U009924 >>>
<<< UNIT U009925 | py-comment | packages/akari-bot-core/tests/test_action_text.py:384-384 >>>
审阅次数：10
# 无会话时回退到半角引号。
<<< END U009925 >>>
<<< UNIT U009926 | py-comment | packages/akari-bot-core/tests/test_action_text.py:387-387 >>>
审阅次数：10
# 默认值不写入 KE 码。
<<< END U009926 >>>
<<< UNIT U009927 | py-comment | packages/akari-bot-core/tests/test_action_text.py:414-414 >>>
审阅次数：10
# 支持的平台上元素得以保留，引号不参与其中。
<<< END U009927 >>>
<<< UNIT U009928 | py-docstring | packages/akari-bot-core/tests/test_action_text.py:1-1 | ctx=<module> >>>
审阅次数：10
ActionText 消息元素构造、内层解析与纯文本降级单元测试。
<<< END U009928 >>>
<<< UNIT U009929 | py-docstring | packages/akari-bot-core/tests/test_action_text.py:429-429 | ctx=test_action_text_element >>>
审阅次数：10
akaribot.core.builtins.message.elements 的 ActionTextElement 构造与降级测试
<<< END U009929 >>>
<<< UNIT U009930 | py-docstring | packages/akari-bot-core/tests/test_action_text.py:439-439 | ctx=test_action_text_kecode >>>
审阅次数：10
akaribot.core.builtins.message 的 ActionTextElement KE 码往返测试
<<< END U009930 >>>
<<< UNIT U009931 | py-docstring | packages/akari-bot-core/tests/test_action_text.py:451-451 | ctx=test_action_text_fallback >>>
审阅次数：10
akaribot.core.builtins.message.chain 的 ActionTextElement 降级与保留测试
<<< END U009931 >>>
<<< UNIT U009932 | py-docstring | packages/akari-bot-core/tests/test_action_text.py:465-465 | ctx=test_action_text_inline >>>
审阅次数：10
akaribot.core.builtins.message.chain 的 ActionTextElement 行内嵌入测试
<<< END U009932 >>>
<<< UNIT U009933 | py-docstring | packages/akari-bot-core/tests/test_action_text.py:476-476 | ctx=test_action_text_serialize >>>
审阅次数：10
akaribot.core.builtins.converter 的 ActionTextElement 跨进程序列化测试
<<< END U009933 >>>
<<< UNIT U009934 | py-inline-comment | packages/akari-bot-core/tests/test_analytics_plot.py:19-19 >>>
审阅次数：10
# 峰值出现在末尾。
<<< END U009934 >>>
<<< UNIT U009935 | py-inline-comment | packages/akari-bot-core/tests/test_analytics_plot.py:20-20 >>>
审阅次数：10
# 全零，此时不应反过来压缩坐标区。
<<< END U009935 >>>
<<< UNIT U009936 | py-inline-comment | packages/akari-bot-core/tests/test_analytics_plot.py:21-21 >>>
审阅次数：10
# year 分支的 12 个点。
<<< END U009936 >>>
<<< UNIT U009937 | py-comment | packages/akari-bot-core/tests/test_analytics_plot.py:26-26 >>>
审阅次数：10
# 按照 analytics 折线图的绘制逻辑生成图表，返回标注顶端超出坐标区上沿的最大像素数。
<<< END U009937 >>>
<<< UNIT U009938 | py-comment | packages/akari-bot-core/tests/test_analytics_plot.py:45-45 >>>
审阅次数：10
# 标注按像素偏移放置，不参与坐标轴自动缩放，因此要覆盖不同数据量级与图幅。
<<< END U009938 >>>
<<< UNIT U009939 | py-comment | packages/akari-bot-core/tests/test_analytics_plot.py:53-54 >>>
审阅次数：10
# 在子进程中将 matplotlib 模拟为缺失状态，验证核心包不会因可选依赖缺失而在导入阶段失败，
# 避免整个 bundled 模块随之一并消失。
<<< END U009939 >>>
<<< UNIT U009940 | py-docstring | packages/akari-bot-core/tests/test_analytics_plot.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.modules.core.su_tools.analytics 折线图数值标注排版与缺失依赖降级单元测试。
<<< END U009940 >>>
<<< UNIT U009941 | py-docstring | packages/akari-bot-core/tests/test_analytics_plot.py:74-74 | ctx=test_analytics_plot >>>
审阅次数：10
akaribot.modules.core.su_tools.analytics 折线图标注排版与缺失依赖降级测试
<<< END U009941 >>>
<<< UNIT U009942 | py-comment | packages/akari-bot-core/tests/test_analytics_window.py:17-17 >>>
审阅次数：10
# 未携带时区信息的时间会被 Tortoise 视作 UTC，除了产生告警日志，还会导致统计窗口整体偏移一个时区差。
<<< END U009942 >>>
<<< UNIT U009943 | py-comment | packages/akari-bot-core/tests/test_analytics_window.py:37-37 >>>
审阅次数：10
# 昨天与明天各一条，都不应被今日窗口计入。
<<< END U009943 >>>
<<< UNIT U009944 | py-docstring | packages/akari-bot-core/tests/test_analytics_window.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.modules.core.su_tools.analytics 统计时间窗口时区处理单元测试（需要数据库）。
<<< END U009944 >>>
<<< UNIT U009945 | py-docstring | packages/akari-bot-core/tests/test_analytics_window.py:55-55 | ctx=test_analytics_window >>>
审阅次数：10
akaribot.modules.core.su_tools.analytics 统计时间窗口测试
<<< END U009945 >>>
<<< UNIT U009946 | py-comment | packages/akari-bot-core/tests/test_atcode.py:63-63 >>>
审阅次数：10
# 此行为由各适配器共用的正则表达式确定，通过测试约束以确保输出格式保持稳定。
<<< END U009946 >>>
<<< UNIT U009947 | py-docstring | packages/akari-bot-core/tests/test_atcode.py:1-1 | ctx=<module> >>>
审阅次数：10
core.builtins.message.mention 行内 AT 码解析与渲染单元测试。
<<< END U009947 >>>
<<< UNIT U009948 | py-docstring | packages/akari-bot-core/tests/test_atcode.py:174-174 | ctx=test_atcode >>>
审阅次数：10
行内 AT 码的解析、渲染与用户 ID 包装测试
<<< END U009948 >>>
<<< UNIT U009949 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:43-43 >>>
审阅次数：10
# 实际确认需要等待用户回复，过程中必然释放控制权。此处同样释放一次控制权，以便并发用例交错执行。
<<< END U009949 >>>
<<< UNIT U009950 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:76-76 >>>
审阅次数：10
# 两轮 probe 交叉送达。避让机制应使其中一轮退出，仅剩一轮进入 confirm。
<<< END U009950 >>>
<<< UNIT U009951 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:81-81 >>>
审阅次数：10
# confirm 由发起方一侧接收，另一侧为其发出方。
<<< END U009951 >>>
<<< UNIT U009952 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:100-100 >>>
审阅次数：10
# 若不避让，双方都会应答对方，产生两个 confirm，同一对场景将被合并两次。
<<< END U009952 >>>
<<< UNIT U009953 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:116-116 >>>
审阅次数：10
# 绕过避让机制直接构造两轮交互，模拟避让未生效的最坏情况（例如某一平台的 probe 投递延迟）。
<<< END U009953 >>>
<<< UNIT U009954 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:133-133 >>>
审阅次数：10
# 若各自新建一个新组，后创建的分组不会包含任何指向它的场景记录。
<<< END U009954 >>>
<<< UNIT U009955 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:136-136 >>>
审阅次数：10
# 互认记录必须写入实际生效的场景组，写入未引用的孤儿组等同于未写入。
<<< END U009955 >>>
<<< UNIT U009956 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:152-153 >>>
审阅次数：10
# 解析器即依据此名单屏蔽对端机器人。保留的一侧若仍然记录对方，
# 重新配对所用的 probe / confirm 会被直接丢弃，握手流程无法闭合，双方因而无法重新建立关联。
<<< END U009956 >>>
<<< UNIT U009957 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:188-188 >>>
审阅次数：10
# 账号按照观察方所在平台的命名空间记录，若混合在扁平列表中将无法区分所属平台。
<<< END U009957 >>>
<<< UNIT U009958 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:216-216 >>>
审阅次数：10
# 对端机器人正常认领，返回一枚 confirm 确认口令。
<<< END U009958 >>>
<<< UNIT U009959 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:218-218 >>>
审阅次数：10
# 用户直接复制场景中出现的同一条命令并发送。口令若仍然被受理，该用户将被误记录为对端机器人。
<<< END U009959 >>>
<<< UNIT U009960 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:232-232 >>>
审阅次数：10
# 口令被转发至另一场景。响应方发送的口令仅会出现在双方共存的场景中，出现在其他位置均不生效。
<<< END U009960 >>>
<<< UNIT U009961 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:237-237 >>>
审阅次数：10
# 同一枚口令由发起场景接收时仍然应当正常闭合握手。
<<< END U009961 >>>
<<< UNIT U009962 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:252-252 >>>
审阅次数：10
# 两条口令命令均以明文形式出现在场景中，用户直接原样复制并发送。
<<< END U009962 >>>
<<< UNIT U009963 | py-comment | packages/akari-bot-core/tests/test_bind_auto.py:256-256 >>>
审阅次数：10
# 互认名单属于解析器的屏蔽依据，发送口令的用户一旦混入，其后续发言将被全部忽略。
<<< END U009963 >>>
<<< UNIT U009964 | py-docstring | packages/akari-bot-core/tests/test_bind_auto.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.modules.core.common_tools.bind 的 bind auto 握手并发正确性与口令防重放单元测试（需要数据库）。
<<< END U009964 >>>
<<< UNIT U009965 | py-docstring | packages/akari-bot-core/tests/test_bind_auto.py:362-362 | ctx=test_bind_auto >>>
审阅次数：10
akaribot.modules.core.common_tools.bind 的 bind auto 握手测试
<<< END U009965 >>>
<<< UNIT U009966 | py-comment | packages/akari-bot-core/tests/test_bind_start.py:29-29 >>>
审阅次数：10
# 以私聊身份生成一枚绑定码并立即提取，返回绑定码所携带的会话信息。
<<< END U009966 >>>
<<< UNIT U009967 | py-comment | packages/akari-bot-core/tests/test_bind_start.py:40-40 >>>
审阅次数：10
# 将 wait_confirm 固定为指定答复，避免触发交互流程。
<<< END U009967 >>>
<<< UNIT U009968 | py-comment | packages/akari-bot-core/tests/test_bind_start.py:50-50 >>>
审阅次数：10
# 当前用例验证真实数据库合并逻辑。模拟平台接收最终的成功提示信息。
<<< END U009968 >>>
<<< UNIT U009969 | py-comment | packages/akari-bot-core/tests/test_bind_start.py:56-56 >>>
审阅次数：10
# 私聊中的用户身份与私聊场景应当同时合并，否则部分数据仍然会残留在原有分组中。
<<< END U009969 >>>
<<< UNIT U009970 | py-comment | packages/akari-bot-core/tests/test_bind_start.py:88-88 >>>
审阅次数：10
# 两次合并共用一次确认，取消后不应处于仅完成部分绑定的中间状态。
<<< END U009970 >>>
<<< UNIT U009971 | py-docstring | packages/akari-bot-core/tests/test_bind_start.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.modules.core.common_tools.bind 的 bind start 私聊与群聊分支单元测试（需要数据库）。
<<< END U009971 >>>
<<< UNIT U009972 | py-docstring | packages/akari-bot-core/tests/test_bind_start.py:103-103 | ctx=test_bind_start >>>
审阅次数：10
akaribot.modules.core.common_tools.bind 的 bind start 测试
<<< END U009972 >>>
<<< UNIT U009973 | py-inline-comment | packages/akari-bot-core/tests/test_brand_lookup.py:84-84 >>>
审阅次数：10
# noqa: BLE001 - 任何异常均视作测试失败。
<<< END U009973 >>>
<<< UNIT U009974 | py-docstring | packages/akari-bot-core/tests/test_brand_lookup.py:101-101 | ctx=test_brand_lookup >>>
审阅次数：10
core.utils.brand 品牌资产回退链测试
<<< END U009974 >>>
<<< UNIT U009975 | py-comment | packages/akari-bot-core/tests/test_bud.py:99-99 >>>
审阅次数：10
# 将花苞创建时间前移 25 小时，使其达到过期状态。
<<< END U009975 >>>
<<< UNIT U009976 | py-comment | packages/akari-bot-core/tests/test_bud.py:106-106 >>>
审阅次数：10
# 触发清理与退款流程。
<<< END U009976 >>>
<<< UNIT U009977 | py-comment | packages/akari-bot-core/tests/test_bud.py:110-110 >>>
审阅次数：10
# 发送者未领取的剩余额度（100 - amount）应当退回。
<<< END U009977 >>>
<<< UNIT U009978 | py-docstring | packages/akari-bot-core/tests/test_bud.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.core.utils.bud 花苞系统单元测试。
<<< END U009978 >>>
<<< UNIT U009979 | py-docstring | packages/akari-bot-core/tests/test_bud.py:146-146 | ctx=test_bud >>>
审阅次数：10
akaribot.core.utils.bud 花苞系统测试
<<< END U009979 >>>
<<< UNIT U009980 | py-docstring | packages/akari-bot-core/tests/test_button_arrange.py:1-1 | ctx=<module> >>>
审阅次数：10
按钮排布工具单元测试。
<<< END U009980 >>>
<<< UNIT U009981 | py-docstring | packages/akari-bot-core/tests/test_button_arrange.py:73-73 | ctx=test_button_arrange >>>
审阅次数：10
core.utils.button 按钮排布工具测试
<<< END U009981 >>>
<<< UNIT U009982 | py-docstring | packages/akari-bot-core/tests/test_button_runtime.py:1-1 | ctx=<module> >>>
审阅次数：10
按钮运行时单元测试。
<<< END U009982 >>>
<<< UNIT U009983 | py-docstring | packages/akari-bot-core/tests/test_button_runtime.py:143-143 | ctx=test_button_runtime >>>
审阅次数：10
core.utils.button_runtime 按钮运行时测试。
<<< END U009983 >>>
<<< UNIT U009984 | py-docstring | packages/akari-bot-core/tests/test_cache.py:1-1 | ctx=<module> >>>
审阅次数：10
core.utils.cache 缓存工具纯函数单元测试。
<<< END U009984 >>>
<<< UNIT U009985 | py-docstring | packages/akari-bot-core/tests/test_cache.py:21-21 | ctx=test_cache >>>
审阅次数：10
core.utils.cache 缓存工具测试
<<< END U009985 >>>
<<< UNIT U009986 | py-comment | packages/akari-bot-core/tests/test_chain_normalize.py:34-36 >>>
审阅次数：10
# 此用例复现线上异常场景。finish() 若接收到 MessageChain，get_message_chain()
# 则直接原样返回并跳过 assign 规范化，导致字符串类型透传至 cattrs 并引发异常：
# TypeError: 'str' object is not a mapping。
<<< END U009986 >>>
<<< UNIT U009987 | py-docstring | packages/akari-bot-core/tests/test_chain_normalize.py:71-71 | ctx=test_chain_normalize >>>
审阅次数：10
消息链原地修改的规范化测试
<<< END U009987 >>>
<<< UNIT U009988 | py-comment | packages/akari-bot-core/tests/test_channel_dedup.py:13-13 >>>
审阅次数：10
# 构造满足通道认领 Hook 运行所需的最小会话对象。
<<< END U009988 >>>
<<< UNIT U009989 | py-comment | packages/akari-bot-core/tests/test_channel_dedup.py:35-35 >>>
审阅次数：10
# 连续两次调用均不应判定为重复，避免单一场景丢弃自身的消息。
<<< END U009989 >>>
<<< UNIT U009990 | py-comment | packages/akari-bot-core/tests/test_channel_dedup.py:66-66 >>>
审阅次数：10
# 认领键仅由通道与内容构成，不包含发起方，重发的消息会匹配到自身上一条残留的认领记录。
<<< END U009990 >>>
<<< UNIT U009991 | py-comment | packages/akari-bot-core/tests/test_channel_dedup.py:69-69 >>>
审阅次数：10
# 重发之后相同通道的其他场景仍然应当避让，避免同一条消息被重复响应两次。
<<< END U009991 >>>
<<< UNIT U009992 | py-comment | packages/akari-bot-core/tests/test_channel_dedup.py:88-88 >>>
审阅次数：10
# 将认领时间调整至时间窗口之外，模拟较长间隔后重新发送相同消息的场景。
<<< END U009992 >>>
<<< UNIT U009993 | py-docstring | packages/akari-bot-core/tests/test_channel_dedup.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.modules.core.hooks.routing 消息通道去重单元测试（需要数据库）。
<<< END U009993 >>>
<<< UNIT U009994 | py-docstring | packages/akari-bot-core/tests/test_channel_dedup.py:107-107 | ctx=test_channel_dedup >>>
审阅次数：10
akaribot.modules.core.hooks.routing 消息通道去重测试
<<< END U009994 >>>
<<< UNIT U009995 | py-comment | packages/akari-bot-core/tests/test_channel_scope.py:29-29 >>>
审阅次数：10
# 判断同一 union 下的两个平台场景是否共享冷却、运行状态与等待任务。
<<< END U009995 >>>
<<< UNIT U009996 | py-comment | packages/akari-bot-core/tests/test_channel_scope.py:36-36 >>>
审阅次数：10
# check() 仅根据底层字典是否包含内容判断，无法用于观测所属范围，因此直接比对冷却桶本身。
<<< END U009996 >>>
<<< UNIT U009997 | py-comment | packages/akari-bot-core/tests/test_channel_scope.py:57-57 >>>
审阅次数：10
# 绑定后各场景默认采用独立通道并仅共享配置，不代表属于同一现实场景。
<<< END U009997 >>>
<<< UNIT U009998 | py-comment | packages/akari-bot-core/tests/test_channel_scope.py:116-116 >>>
审阅次数：10
# 花瓣余额关联于 union，日额度若仍然按平台账号记账，绑定多个平台即可重复领取多倍额度。
<<< END U009998 >>>
<<< UNIT U009999 | py-docstring | packages/akari-bot-core/tests/test_channel_scope.py:1-1 | ctx=<module> >>>
审阅次数：10
union 与消息通道作用域单元测试（内存状态按通道、花瓣额度按 union 划分，需要数据库）。
<<< END U009999 >>>
<<< UNIT U010000 | py-docstring | packages/akari-bot-core/tests/test_channel_scope.py:171-171 | ctx=test_channel_scope >>>
审阅次数：10
core 的 union 与消息通道作用域测试
<<< END U010000 >>>
<<< UNIT U010001 | py-docstring | packages/akari-bot-core/tests/test_component.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.core.component 组件注册系统单元测试。
<<< END U010001 >>>
<<< UNIT U010002 | py-docstring | packages/akari-bot-core/tests/test_component.py:75-75 | ctx=test_component >>>
审阅次数：10
akaribot.core.component 组件注册系统测试
<<< END U010002 >>>
<<< UNIT U010003 | py-docstring | packages/akari-bot-core/tests/test_config.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.core.config 配置系统单元测试。
<<< END U010003 >>>
<<< UNIT U010004 | py-docstring | packages/akari-bot-core/tests/test_config.py:108-108 | ctx=test_config >>>
审阅次数：10
akaribot.core.config 的 Config 函数测试
<<< END U010004 >>>
<<< UNIT U010005 | py-docstring | packages/akari-bot-core/tests/test_config.py:119-119 | ctx=test_mock_config >>>
审阅次数：10
akaribot.testing.mock.config 配置项模拟对象测试
<<< END U010005 >>>
<<< UNIT U010006 | py-docstring | packages/akari-bot-core/tests/test_config_global.py:1-1 | ctx=<module> >>>
审阅次数：10
全局默认配置与用户配置覆盖的单元测试。
<<< END U010006 >>>
<<< UNIT U010007 | py-docstring | packages/akari-bot-core/tests/test_config_global.py:71-71 | ctx=test_config_global >>>
审阅次数：10
core.config 全局默认配置与用户覆盖测试
<<< END U010007 >>>
<<< UNIT U010008 | py-comment | packages/akari-bot-core/tests/test_config_migration.py:61-62 >>>
审阅次数：10
# ``PackageRegistry.modules()`` 的键为包名称（非 ``种类:包名``），由于迁移运行器按照 ``entry.name``
# 获取对应的 revision，键名错误会导致整条链路静默且无法查询到迁移记录。
<<< END U010008 >>>
<<< UNIT U010009 | py-docstring | packages/akari-bot-core/tests/test_config_migration.py:177-177 | ctx=test_config_migration >>>
审阅次数：10
core.config.migration 配置迁移端到端测试
<<< END U010009 >>>
<<< UNIT U010010 | py-comment | packages/akari-bot-core/tests/test_config_readonly.py:12-12 >>>
审阅次数：10
# 最小可用的配置文件内容，包含配置表之外的顶层键，以及常规配置表与密钥表各一项。
<<< END U010010 >>>
<<< UNIT U010011 | py-docstring | packages/akari-bot-core/tests/test_config_readonly.py:1-1 | ctx=<module> >>>
审阅次数：10
配置只读语义与授权写入的单元测试。
<<< END U010011 >>>
<<< UNIT U010012 | py-docstring | packages/akari-bot-core/tests/test_config_readonly.py:139-139 | ctx=test_config_readonly >>>
审阅次数：10
core.config 配置只读语义测试
<<< END U010012 >>>
<<< UNIT U010013 | py-comment | packages/akari-bot-core/tests/test_config_scan.py:132-132 >>>
审阅次数：10
# core 内置的语言文件按照包位置定位；由于当前用例随包发布，按测试文件上溯会在安装布局下失准。
<<< END U010013 >>>
<<< UNIT U010014 | py-comment | packages/akari-bot-core/tests/test_config_scan.py:169-169 >>>
审阅次数：10
# 命名空间包横跨多个 distribution，__path__ 的每一项均需遍历，若仅检查首项会导致遗漏成员包。
<<< END U010014 >>>
<<< UNIT U010015 | py-comment | packages/akari-bot-core/tests/test_config_scan.py:174-174 >>>
审阅次数：10
# 按包枚举的代码依赖 __init__.py，缺少该文件的包会被跳过，其配置随之缺失（如 akaribot.adapters.milky）。
<<< END U010015 >>>
<<< UNIT U010016 | py-comment | packages/akari-bot-core/tests/test_config_scan.py:199-199 >>>
审阅次数：10
# 与守护进程启动的平台进程一致，模板导入完成后一律设置为只读状态。
<<< END U010016 >>>
<<< UNIT U010017 | py-comment | packages/akari-bot-core/tests/test_config_scan.py:263-263 >>>
审阅次数：10
# 已由 tester 导入的配置模板不会再次执行 process_config_class，因此通过此处声明的模板验证补充行为。
<<< END U010017 >>>
<<< UNIT U010018 | py-comment | packages/akari-bot-core/tests/test_config_scan.py:362-362 >>>
审阅次数：10
# 迁移后的 3 秒提示停顿不属于持久化行为。仅在隔离进程中跳过。
<<< END U010018 >>>
<<< UNIT U010019 | py-comment | packages/akari-bot-core/tests/test_config_scan.py:402-402 >>>
审阅次数：10
# 迁移后的 3 秒提示停顿不属于持久化行为。仅在隔离进程中跳过。
<<< END U010019 >>>
<<< UNIT U010020 | py-docstring | packages/akari-bot-core/tests/test_config_scan.py:1-1 | ctx=<module> >>>
审阅次数：10
配置模板扫描的单元测试。
<<< END U010020 >>>
<<< UNIT U010021 | py-docstring | packages/akari-bot-core/tests/test_config_scan.py:428-428 | ctx=test_config_scan >>>
审阅次数：10
akaribot.core.config.scan 配置模板扫描测试
<<< END U010021 >>>
<<< UNIT U010022 | py-docstring | packages/akari-bot-core/tests/test_confirm_prompt.py:74-74 | ctx=test_confirm_prompt >>>
审阅次数：10
core 确认提示文案选择逻辑测试。
<<< END U010022 >>>
<<< UNIT U010023 | py-comment | packages/akari-bot-core/tests/test_container.py:155-155 >>>
审阅次数：10
# TokenBucket 测试。
<<< END U010023 >>>
<<< UNIT U010024 | py-comment | packages/akari-bot-core/tests/test_container.py:161-161 >>>
审阅次数：10
# ExpiringTempDict 测试。
<<< END U010024 >>>
<<< UNIT U010025 | py-docstring | packages/akari-bot-core/tests/test_container.py:1-1 | ctx=<module> >>>
审阅次数：10
core.utils.container 的 TokenBucket 与 ExpiringTempDict 纯函数单元测试。
<<< END U010025 >>>
<<< UNIT U010026 | py-docstring | packages/akari-bot-core/tests/test_container.py:154-154 | ctx=test_container >>>
审阅次数：10
core.utils.container 的 TokenBucket 与 ExpiringTempDict 测试
<<< END U010026 >>>
<<< UNIT U010027 | py-comment | packages/akari-bot-core/tests/test_cooldown.py:15-16 >>>
审阅次数：10
# 场景维度按消息通道、用户维度按 union，确保切换平台账号仍然受同一份冷却约束，
# 但仅共享 union 而通道编号不同的场景不应互相牵连。
<<< END U010027 >>>
<<< UNIT U010028 | py-comment | packages/akari-bot-core/tests/test_cooldown.py:49-49 >>>
审阅次数：10
# 模块每次执行命令均会创建新的 CoolDown 实例，冷却限制必须跨实例生效。
<<< END U010028 >>>
<<< UNIT U010029 | py-comment | packages/akari-bot-core/tests/test_cooldown.py:51-51 >>>
审阅次数：10
# 重置后应恰好保留完整冷却时长，模块正是通过此非 0 值实现对重复调用的拦截。
<<< END U010029 >>>
<<< UNIT U010030 | py-comment | packages/akari-bot-core/tests/test_cooldown.py:63-63 >>>
审阅次数：10
# 将记录的时间戳调整至冷却时长之前，模拟冷却已经结束。
<<< END U010030 >>>
<<< UNIT U010031 | py-docstring | packages/akari-bot-core/tests/test_cooldown.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.core.utils.cooldown 冷却系统单元测试。
<<< END U010031 >>>
<<< UNIT U010032 | py-docstring | packages/akari-bot-core/tests/test_cooldown.py:84-84 | ctx=test_cooldown >>>
审阅次数：10
akaribot.core.utils.cooldown 的 CoolDown 冷却系统测试
<<< END U010032 >>>
<<< UNIT U010033 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:25-25 >>>
审阅次数：10
# 多列修改的测试用例需要包含两列以上常规数据列的数据表。
<<< END U010033 >>>
<<< UNIT U010034 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:32-32 >>>
审阅次数：10
# 数据库连接在 init_db() 调用时读取模块级变量，因此将两个连接均指向临时目录，确保用例绝不访问仓库实例的数据库。
<<< END U010034 >>>
<<< UNIT U010035 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:52-52 >>>
审阅次数：10
# 入口内部使用 asyncio.run()，而用例运行在事件循环中，因此交由无事件循环的线程执行。
<<< END U010035 >>>
<<< UNIT U010036 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:123-123 >>>
审阅次数：10
# 一行多列测试，单次 set 操作修改整行的若干列，重新读取后各列均已生效。
<<< END U010036 >>>
<<< UNIT U010037 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:150-150 >>>
审阅次数：10
# 多列中若存在非法取值则整行保持不变，仅当类型转换全部通过后才提交 UPDATE，避免残留处于部分修改状态的记录行。
<<< END U010037 >>>
<<< UNIT U010038 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:207-207 >>>
审阅次数：10
# 分页与筛选功能需要可控的测试数据，因此直接创建测试数据行，避免逐次发起子进程调用。
<<< END U010038 >>>
<<< UNIT U010039 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:217-217 >>>
审阅次数：10
# 条件与分页均在 core 中统一处理，界面仅传递条件，条数按筛选后计算，offset 仅影响当前页。
<<< END U010039 >>>
<<< UNIT U010040 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:243-243 >>>
审阅次数：10
# 大表上 COUNT 会触发全表扫描，因此翻页可以仅获取当前页，total 返回 null，通过调用方沿用上一次的条数。
<<< END U010040 >>>
<<< UNIT U010041 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:280-280 >>>
审阅次数：10
# 构造测试数据时 load 等于“名称以 0 结尾”，因此 load=true 且名称包含 mod-01 的仅包含 mod-010。
<<< END U010041 >>>
<<< UNIT U010042 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:293-293 >>>
审阅次数：10
# 被搜索的三行 load 均为 false，因此与 load=false 取交集的条数保持不变。
<<< END U010042 >>>
<<< UNIT U010043 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:305-305 >>>
审阅次数：10
# 空白搜索词按照“未提供”处理，界面清空搜索框后无需区分空字符串与默认值。
<<< END U010043 >>>
<<< UNIT U010044 | py-comment | packages/akari-bot-core/tests/test_data_entrypoint.py:321-321 >>>
审阅次数：10
# 尚未创建数据表时同样返回清单。条数返回未知状态，清单则正常返回。
<<< END U010044 >>>
<<< UNIT U010045 | py-docstring | packages/akari-bot-core/tests/test_data_entrypoint.py:381-381 | ctx=test_data_entrypoint >>>
审阅次数：10
core.entrypoints.data 数据浏览与写入入口测试
<<< END U010045 >>>
<<< UNIT U010046 | py-comment | packages/akari-bot-core/tests/test_database_init.py:449-450 >>>
审阅次数：10
# 清单为空仅表示该包未声明数据库模型。包内缺失依赖导致的失败通过 ``init_db()`` 在实际导入
# 模型时抛出（参见下一条用例），发现阶段不作处理。
<<< END U010046 >>>
<<< UNIT U010047 | py-docstring | packages/akari-bot-core/tests/test_database_init.py:1-1 | ctx=<module> >>>
审阅次数：10
数据库连接参数与初始化职责单元测试。
<<< END U010047 >>>
<<< UNIT U010048 | py-docstring | packages/akari-bot-core/tests/test_database_init.py:509-509 | ctx=test_database_init >>>
审阅次数：10
SQLite 参数自动补全，且仅 pre-init 模式创建数据表。
<<< END U010048 >>>
<<< UNIT U010049 | py-docstring | packages/akari-bot-core/tests/test_database_link_anchor.py:100-100 | ctx=test_database_link_anchoring >>>
审阅次数：10
相对 SQLite 链接以实例根目录为基准，绝对路径、内存数据库与非 SQLite 链接不受影响。
<<< END U010049 >>>
<<< UNIT U010050 | py-comment | packages/akari-bot-core/tests/test_database_migration.py:29-29 >>>
审阅次数：10
# 样本数据库随 core 包分发，与当前用例属于同一成员包，按照测试文件位置定位即可。
<<< END U010050 >>>
<<< UNIT U010051 | py-comment | packages/akari-bot-core/tests/test_database_migration.py:38-38 >>>
审阅次数：10
# 样本数据库与测试进程内置数据库不可共用连接，由于版本升级会修改表结构，连接必须指向独立的文件副本。
<<< END U010051 >>>
<<< UNIT U010052 | py-comment | packages/akari-bot-core/tests/test_database_migration.py:85-85 >>>
审阅次数：10
# 历史版本号仅记录至 LATEST_LEGACY_VERSION，后续追加的 revision 通过常规升级流程执行，因此按包含关系检查。
<<< END U010052 >>>
<<< UNIT U010053 | py-docstring | packages/akari-bot-core/tests/test_database_migration.py:1-1 | ctx=<module> >>>
审阅次数：10
数据库迁移框架测试。
<<< END U010053 >>>
<<< UNIT U010054 | py-inline-comment | packages/akari-bot-core/tests/test_database_transaction_cancel.py:16-16 >>>
审阅次数：10
# pragma: no cover - 未安装 MySQL 驱动时跳过对应测试用例。
<<< END U010054 >>>
<<< UNIT U010055 | py-docstring | packages/akari-bot-core/tests/test_database_transaction_cancel.py:1-1 | ctx=<module> >>>
审阅次数：10
数据库事务在进入、退出或批量写入阶段被取消时，不得产生残留连接锁、未提交事务或未释放的连接池连接。
<<< END U010055 >>>
<<< UNIT U010056 | py-docstring | packages/akari-bot-core/tests/test_database_transaction_cancel.py:247-247 | ctx=test_database_transaction_cancel >>>
审阅次数：10
事务取消后数据库与连接池仍然保持可用状态。
<<< END U010056 >>>
<<< UNIT U010057 | py-comment | packages/akari-bot-core/tests/test_database_update.py:171-171 >>>
审阅次数：10
# 先还原为升级前的表结构，仅保留原有列，且携带一行历史数据。
<<< END U010057 >>>
<<< UNIT U010058 | py-comment | packages/akari-bot-core/tests/test_database_update.py:191-191 >>>
审阅次数：10
# 原有记录行不包含 refresh token，需要由用户重新完成一次绑定。
<<< END U010058 >>>
<<< UNIT U010059 | py-comment | packages/akari-bot-core/tests/test_database_update.py:200-200 >>>
审阅次数：10
# 落雪的令牌不需要额外保存用户标识，因此此处仅补齐 refresh token 单列，不涉及 `subject`。
<<< END U010059 >>>
<<< UNIT U010060 | py-comment | packages/akari-bot-core/tests/test_database_update.py:203-203 >>>
审阅次数：10
# 先还原为升级前的表结构，仅保留历史好友码列，且携带一行历史数据。
<<< END U010060 >>>
<<< UNIT U010061 | py-comment | packages/akari-bot-core/tests/test_database_update.py:225-225 >>>
审阅次数：10
# 原有记录行虽然保留但缺少 refresh token，需要由用户重新完成一次绑定。
<<< END U010061 >>>
<<< UNIT U010062 | py-comment | packages/akari-bot-core/tests/test_database_update.py:236-236 >>>
审阅次数：10
# 先还原为升级前的表结构，不包含推送优先级列，且携带一行历史数据。
<<< END U010062 >>>
<<< UNIT U010063 | py-docstring | packages/akari-bot-core/tests/test_database_update.py:1-1 | ctx=<module> >>>
审阅次数：10
数据库版本升级测试。
<<< END U010063 >>>
<<< UNIT U010064 | py-comment | packages/akari-bot-core/tests/test_dependency_graph.py:282-282 >>>
审阅次数：10
# 条目顺序特意使依赖方先行出现，使初始判定时被依赖方尚未被标记为拒绝，仅能通过级联机制实现拦截。
<<< END U010064 >>>
<<< UNIT U010065 | py-comment | packages/akari-bot-core/tests/test_dependency_graph.py:351-351 >>>
审阅次数：10
# optional 本身已完成安装，但其所属的 dev extra 缺失 ruff，仍然视作未安装状态。
<<< END U010065 >>>
<<< UNIT U010066 | py-docstring | packages/akari-bot-core/tests/test_dependency_graph.py:389-389 | ctx=test_dependency_graph >>>
审阅次数：10
core.registry 模块依赖图测试
<<< END U010066 >>>
<<< UNIT U010067 | py-comment | packages/akari-bot-core/tests/test_dirty_check.py:27-28 >>>
审阅次数：10
# AT 码的合法形式是 <AT:client|id>（参见 core/builtins/message/mention.py），
# 中间的额外字段为展示名，与 client、id 一并予以豁免。
<<< END U010067 >>>
<<< UNIT U010068 | py-comment | packages/akari-bot-core/tests/test_dirty_check.py:37-37 >>>
审阅次数：10
# 豁免不得扩大成整条消息不过滤，AT 码之外的同一个词仍应被替换。
<<< END U010068 >>>
<<< UNIT U010069 | py-docstring | packages/akari-bot-core/tests/test_dirty_check.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot.core.utils.dirty_check 内容审核系统单元测试。
<<< END U010069 >>>
<<< UNIT U010070 | py-docstring | packages/akari-bot-core/tests/test_dirty_check.py:283-283 | ctx=test_dirty_check >>>
审阅次数：10
akaribot.core.utils.dirty_check 内容审核系统测试
<<< END U010070 >>>
<<< UNIT U010071 | py-comment | packages/akari-bot-core/tests/test_dirty_check_features.py:20-21 >>>
审阅次数：10
# 主动推送的会话没有触发消息，能力标志仅能从进程注册元数据中传入，
# wikilog 等模块的 check() 正是据此判断是否过滤。
<<< END U010071 >>>
<<< UNIT U010072 | py-docstring | packages/akari-bot-core/tests/test_dirty_check_features.py:1-1 | ctx=<module> >>>
审阅次数：10
akaribot/adapters/*/features 平台能力开关传递单元测试（需要数据库）。
<<< END U010072 >>>
<<< UNIT U010073 | py-docstring | packages/akari-bot-core/tests/test_dirty_check_features.py:91-91 | ctx=test_dirty_check_features >>>
审阅次数：10
akaribot.adapters.features 平台能力开关测试
<<< END U010073 >>>
<<< UNIT U010074 | py-comment | packages/akari-bot-core/tests/test_docs_entrypoint.py:520-520 >>>
审阅次数：10
# 可编辑安装模式的元数据若缺失源码中的 akaribot.docs 声明，则按源码补充并发出告警；常规安装不按源码补充。
<<< END U010074 >>>
<<< UNIT U010075 | py-docstring | packages/akari-bot-core/tests/test_docs_entrypoint.py:624-624 | ctx=test_docs_entrypoint >>>
审阅次数：10
core.entrypoints.docs 包文档清单入口测试
<<< END U010075 >>>
<<< UNIT U010076 | py-comment | packages/akari-bot-core/tests/test_entrypoint_config.py:59-59 >>>
审阅次数：10
# 引导代码可能为整个测试进程设置过配置目录，子进程必须仅使用本次的实例根目录。
<<< END U010076 >>>
<<< UNIT U010077 | py-comment | packages/akari-bot-core/tests/test_entrypoint_config.py:76-76 >>>
审阅次数：10
# 注释中的示例文本与字符串值中内嵌的同形文本均不构成占位项，仅当完整值等于标记时才计入统计。
<<< END U010077 >>>
<<< UNIT U010078 | py-comment | packages/akari-bot-core/tests/test_entrypoint_config.py:90-90 >>>
审阅次数：10
# 占位标记格式按照 core 的正则表达式判定，无后缀标记与带后缀、带类型说明的写法均计入统计，同一表内逐项累计。
<<< END U010078 >>>
<<< UNIT U010079 | py-comment | packages/akari-bot-core/tests/test_entrypoint_config.py:98-98 >>>
审阅次数：10
# 单张表解析失败或编码非 UTF-8 时，仅将该表记入 failed，其余表正常执行统计，命令仍然以退出码 0 结束。
<<< END U010079 >>>
<<< UNIT U010080 | py-comment | packages/akari-bot-core/tests/test_entrypoint_config.py:115-115 >>>
审阅次数：10
# 缺少文件与包含路径分隔符的表名各保留一条原因说明，由于表名称仅用于拼接配置目录下的文件名。
<<< END U010080 >>>
<<< UNIT U010081 | py-comment | packages/akari-bot-core/tests/test_entrypoint_config.py:129-129 >>>
审阅次数：10
# 未传入 --tables 参数时遍历配置目录下的全部数据表，逐表输出占位项与总项数，并汇总总数量。
<<< END U010081 >>>
<<< UNIT U010082 | py-comment | packages/akari-bot-core/tests/test_entrypoint_config.py:147-147 >>>
审阅次数：10
# 实例配置文件的注释提取自 schema，缺少专属注释时采用各适配器共用的 enable 注释，不输出 {I18N:...} 标记。
<<< END U010082 >>>
<<< UNIT U010083 | py-comment | packages/akari-bot-core/tests/test_entrypoint_config.py:169-170 >>>
审阅次数：10
# 适配器配置模板在导入阶段写入磁盘。入口必须在读取 schema 前重新加载配置，
# 避免首次安装阶段配置表尚不存在而导致配置补全流程失败。
<<< END U010083 >>>
<<< UNIT U010084 | py-docstring | packages/akari-bot-core/tests/test_entrypoint_config.py:209-209 | ctx=test_entrypoint_config >>>
审阅次数：10
core.entrypoints.config 占位符统计入口测试
<<< END U010084 >>>
<<< UNIT U010085 | py-docstring | packages/akari-bot-core/tests/test_entrypoint_db_purge.py:146-146 | ctx=test_entrypoint_db_purge >>>
审阅次数：10
core.entrypoints.db 卸载清理入口测试
<<< END U010085 >>>
<<< UNIT U010086 | py-comment | packages/akari-bot-core/tests/test_entrypoint_rpc.py:41-42 >>>
审阅次数：10
# 入口按照实例配置选择后端。测试环境采用共享内存后端，并使“是否需要连接数据库”分支进入非 database
# 路径，避免访问测试进程已初始化的内存数据库。
<<< END U010086 >>>
<<< UNIT U010087 | py-comment | packages/akari-bot-core/tests/test_entrypoint_rpc.py:98-98 >>>
审阅次数：10
# 白名单若失效，main 会在运行中的事件循环中调用 asyncio.run 而抛出异常，当前用例随之判定为失败。
<<< END U010087 >>>
<<< UNIT U010088 | py-comment | packages/akari-bot-core/tests/test_entrypoint_rpc.py:175-175 >>>
审阅次数：10
# 检查处理器接收到的是调用方传入的包对象，确保 dist 元数据不会在中途丢失。
<<< END U010088 >>>
<<< UNIT U010089 | py-comment | packages/akari-bot-core/tests/test_entrypoint_rpc.py:222-223 >>>
审阅次数：10
# 优先选用 arcaea_rss，因为它声明了一个计划任务，能一并验证 Scheduler 的注册与拆除。缺失时回退至任意
# 声明了 ``provides_modules`` 的模块包，用例对包名保持无关。
<<< END U010089 >>>
<<< UNIT U010090 | py-comment | packages/akari-bot-core/tests/test_entrypoint_rpc.py:299-299 >>>
审阅次数：10
# 环境缺少已安装模块包或仓库实例配置时无法搭建隔离实例，输出明确告警，不视作测试通过。
<<< END U010090 >>>
<<< UNIT U010091 | py-comment | packages/akari-bot-core/tests/test_entrypoint_rpc.py:320-320 >>>
审阅次数：10
# 安装后注册表、sys.modules、Scheduler 与 module_status 必须与包声明保持一致。卸载后必须全部复原。
<<< END U010091 >>>
<<< UNIT U010092 | py-docstring | packages/akari-bot-core/tests/test_entrypoint_rpc.py:344-344 | ctx=test_entrypoint_rpc >>>
审阅次数：10
包变更 RPC 入口的白名单、真实投递与失败分类。
<<< END U010092 >>>
<<< UNIT U010093 | py-docstring | packages/akari-bot-core/tests/test_error_reporting.py:1-1 | ctx=<module> >>>
审阅次数：10
parser 异常上报的消息格式测试。
<<< END U010093 >>>
<<< UNIT U010094 | py-docstring | packages/akari-bot-core/tests/test_error_reporting.py:61-61 | ctx=test_error_reporting >>>
审阅次数：10
错误上报按目标平台能力渲染 traceback 测试
<<< END U010094 >>>
<<< UNIT U010095 | py-docstring | packages/akari-bot-core/tests/test_event.py:1-1 | ctx=<module> >>>
审阅次数：10
模块事件注册、事件上下文及跨进程分发单元测试。
<<< END U010095 >>>
<<< UNIT U010096 | py-docstring | packages/akari-bot-core/tests/test_event.py:227-227 | ctx=test_event >>>
审阅次数：10
模块事件的注册、EventInfo、队列转换与服务器分发测试。
<<< END U010096 >>>
<<< UNIT U010097 | py-docstring | packages/akari-bot-core/tests/test_func_utils.py:1-1 | ctx=<module> >>>
审阅次数：10
core.utils.func 纯函数单元测试。
<<< END U010097 >>>
<<< UNIT U010098 | py-docstring | packages/akari-bot-core/tests/test_func_utils.py:164-164 | ctx=test_func_utils >>>
审阅次数：10
core.utils.func 所有工具函数测试
<<< END U010098 >>>
<<< UNIT U010099 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:36-36 >>>
审阅次数：10
# 表格测试所用的表头键，此处不校验其内容，仅用于完成渲染流程。
<<< END U010099 >>>
<<< UNIT U010100 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:53-53 >>>
审阅次数：10
# show 为选填项，默认由平台读取 text 并展示。
<<< END U010100 >>>
<<< UNIT U010101 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:91-91 >>>
审阅次数：10
# 选项已通过解析器转换为函数参数并注入，此处仅保持属性存在。
<<< END U010101 >>>
<<< UNIT U010102 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:200-200 >>>
审阅次数：10
# 关键字必须与命令模板 [--img] 解析所得的参数名称保持一致，参见 core/builtins/parser/message.py。
<<< END U010102 >>>
<<< UNIT U010103 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:850-850 >>>
审阅次数：10
# 渲染结果应为四行内容，包括两个标题各占一行、两组列表各占一行。
<<< END U010103 >>>
<<< UNIT U010104 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:879-879 >>>
审阅次数：10
# 包括两个标题各占一行、两组列表各占一行、两条提示各占一行。
<<< END U010104 >>>
<<< UNIT U010105 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:883-883 >>>
审阅次数：10
# 模块列表所在行不得混入提示文案。
<<< END U010105 >>>
<<< UNIT U010106 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:897-897 >>>
审阅次数：10
# 模块数量对应（列数，行数）。列数取根据高度上限反推计算所得的列数与最少列数中的较大者。
<<< END U010106 >>>
<<< UNIT U010107 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:918-918 >>>
审阅次数：10
# 首行作为表头、次行作为分隔行，其余行均作为数据行。
<<< END U010107 >>>
<<< UNIT U010108 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:957-957 >>>
审阅次数：10
# 模拟 ~help <模块> 的组装逻辑，包含简介、表格与作者信息。
<<< END U010108 >>>
<<< UNIT U010109 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:990-990 >>>
审阅次数：10
# 未携带参数的条目原样返回，点击后可直接发送。
<<< END U010109 >>>
<<< UNIT U010110 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:992-992 >>>
审阅次数：10
# 携带参数的条目保留一个末尾空格，以便光标停留在参数位置。
<<< END U010110 >>>
<<< UNIT U010111 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:997-997 >>>
审阅次数：10
# 嵌套场景，选项自身携带参数。
<<< END U010111 >>>
<<< UNIT U010112 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:1000-1000 >>>
审阅次数：10
# 可变长度参数同样不应残留。
<<< END U010112 >>>
<<< UNIT U010113 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:1071-1071 >>>
审阅次数：10
# 竖线仍然需要转义，因为表格先按竖线切分单元格，代码块无法拦截。
<<< END U010113 >>>
<<< UNIT U010114 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:1073-1073 >>>
审阅次数：10
# 代码块围栏必须比内容中最长的连续反引号更长，避免在中途被提前闭合。
<<< END U010114 >>>
<<< UNIT U010115 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:1076-1076 >>>
审阅次数：10
# 内容以反引号起止时两侧补充空格，否则会被并入围栏。
<<< END U010115 >>>
<<< UNIT U010116 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:1078-1078 >>>
审阅次数：10
# 换行在代码块内无法直接表达，折叠转换为空格。
<<< END U010116 >>>
<<< UNIT U010117 | py-comment | packages/akari-bot-core/tests/test_help_action_text.py:1080-1080 >>>
审阅次数：10
# 针对空文本不生成空代码块围栏。
<<< END U010117 >>>
<<< UNIT U010118 | py-docstring | packages/akari-bot-core/tests/test_help_action_text.py:1-1 | ctx=<module> >>>
审阅次数：10
帮助页布局与可点击模块列表的单元测试。
<<< END U010118 >>>
<<< UNIT U010119 | py-docstring | packages/akari-bot-core/tests/test_help_action_text.py:1114-1114 | ctx=test_clickable_modules >>>
审阅次数：10
akaribot.modules.core.common_tools.help 可点击模块列表测试
<<< END U010119 >>>
