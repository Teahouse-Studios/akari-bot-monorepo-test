# 全仓可读文本审核稿 · 第 20 册 / 共 20 册

覆盖 U013014–U013993，96 个文件、980 个单元、41,555 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md` | 130 | U013014–U013143 | 13,733 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json` | 321 | U013144–U013464 | 6,519 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/manifest.toml` | 4 | U013465–U013468 | 151 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/migrations/0002_union_id.py` | 1 | U013469–U013469 | 43 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/migrations/0003_url_rules_to_global.py` | 1 | U013470–U013470 | 31 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/migrations/__init__.py` | 1 | U013471–U013471 | 12 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/diff.py` | 1 | U013472–U013472 | 37 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/disambiguation.py` | 2 | U013473–U013474 | 59 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/forum.py` | 4 | U013475–U013478 | 103 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/magic.py` | 2 | U013479–U013480 | 94 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/mapping.py` | 1 | U013481–U013481 | 17 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/preview_render.py` | 3 | U013482–U013484 | 125 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/recommend.py` | 1 | U013485–U013485 | 45 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/screenshot_image.py` | 1 | U013486–U013486 | 43 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py` | 27 | U013487–U013513 | 1,681 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py` | 12 | U013514–U013525 | 1,067 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/weekly.py` | 4 | U013526–U013529 | 64 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wiki.py` | 4 | U013530–U013533 | 166 |
| `packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wikilog.py` | 5 | U013534–U013538 | 274 |
| `packages/modules/akari-bot-module-wiki/pyproject.toml` | 1 | U013539–U013539 | 67 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_disambiguation.py` | 1 | U013540–U013540 | 29 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_forum.py` | 1 | U013541–U013541 | 26 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_interwiki_url.py` | 2 | U013542–U013543 | 62 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_invalid_interwiki.py` | 1 | U013544–U013544 | 25 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_lifecycle.py` | 1 | U013545–U013545 | 47 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_manual_anchor.py` | 1 | U013546–U013546 | 35 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_markdown.py` | 2 | U013547–U013548 | 51 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_message_buttons.py` | 6 | U013549–U013554 | 199 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_recommend.py` | 4 | U013555–U013558 | 169 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_render_precheck.py` | 4 | U013559–U013562 | 163 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_siteinfo_cache.py` | 2 | U013563–U013564 | 44 |
| `packages/modules/akari-bot-module-wiki/tests/test_wiki_summary.py` | 2 | U013565–U013566 | 66 |
| `packages/modules/akari-bot-module-wolframalpha/README.md` | 4 | U013567–U013570 | 176 |
| `packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md` | 12 | U013571–U013582 | 522 |
| `packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/index.md` | 4 | U013583–U013586 | 218 |
| `packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/locales/zh_cn.json` | 5 | U013587–U013591 | 114 |
| `packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/manifest.toml` | 3 | U013592–U013594 | 124 |
| `packages/modules/akari-bot-module-wordle/README.md` | 4 | U013595–U013598 | 166 |
| `packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md` | 13 | U013599–U013611 | 522 |
| `packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md` | 8 | U013612–U013619 | 1,193 |
| `packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json` | 13 | U013620–U013632 | 285 |
| `packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/manifest.toml` | 2 | U013633–U013634 | 77 |
| `packages/modules/akari-bot-module-wordle/pyproject.toml` | 1 | U013635–U013635 | 56 |
| `pyproject.toml` | 5 | U013636–U013640 | 306 |
| `tester.py` | 2 | U013641–U013642 | 227 |
| `tests/build_synthetic_fixtures.py` | 10 | U013643–U013652 | 521 |
| `tests/capture_http_fixtures.py` | 4 | U013653–U013656 | 194 |
| `tests/capture_schedule_fixtures.py` | 5 | U013657–U013661 | 142 |
| `tests/capture_webrender_fixtures.py` | 1 | U013662–U013662 | 17 |
| `tests/helpers/websocket_rpc_worker.py` | 1 | U013663–U013663 | 30 |
| `tests/integration/test_core_admin.py` | 8 | U013664–U013671 | 182 |
| `tests/integration/test_core_modules.py` | 16 | U013672–U013687 | 228 |
| `tests/integration/test_external_modules.py` | 7 | U013688–U013694 | 192 |
| `tests/integration/test_external_wiki.py` | 8 | U013695–U013702 | 168 |
| `tests/integration/test_features_command.py` | 2 | U013703–U013704 | 48 |
| `tests/integration/test_game_modules.py` | 7 | U013705–U013711 | 203 |
| `tests/integration/test_scheduled_tasks.py` | 5 | U013712–U013716 | 93 |
| `tests/integration/test_url_allowlist.py` | 1 | U013717–U013717 | 18 |
| `tests/integration/test_url_blocklist.py` | 1 | U013718–U013718 | 18 |
| `tests/integration/test_utility_modules.py` | 10 | U013719–U013728 | 202 |
| `tests/integration/test_wiki_audit.py` | 1 | U013729–U013729 | 41 |
| `tests/run_one.py` | 4 | U013730–U013733 | 252 |
| `tests/unit/test_bind_channel.py` | 2 | U013734–U013735 | 121 |
| `tests/unit/test_bot_state.py` | 1 | U013736–U013736 | 14 |
| `tests/unit/test_check_test_baseline.py` | 1 | U013737–U013737 | 38 |
| `tests/unit/test_check_versions.py` | 3 | U013738–U013740 | 111 |
| `tests/unit/test_client_init.py` | 2 | U013741–U013742 | 54 |
| `tests/unit/test_daemon_logger.py` | 1 | U013743–U013743 | 17 |
| `tests/unit/test_i18n_cmd_params.py` | 8 | U013744–U013751 | 408 |
| `tests/unit/test_multi_instance.py` | 17 | U013752–U013768 | 467 |
| `tests/unit/test_permission_groups.py` | 2 | U013769–U013770 | 66 |
| `tests/unit/test_platform_management.py` | 3 | U013771–U013773 | 114 |
| `tests/unit/test_platform_member_events.py` | 2 | U013774–U013775 | 42 |
| `tests/unit/test_platform_memory.py` | 2 | U013776–U013777 | 48 |
| `tests/unit/test_platform_shutdown.py` | 2 | U013778–U013779 | 37 |
| `tests/unit/test_promote_docker.py` | 1 | U013780–U013780 | 37 |
| `tests/unit/test_publish_registry.py` | 1 | U013781–U013781 | 17 |
| `tests/unit/test_registry_release.py` | 1 | U013782–U013782 | 39 |
| `tools/build_local_index.py` | 3 | U013783–U013785 | 112 |
| `tools/build_registry.py` | 28 | U013786–U013813 | 1,104 |
| `tools/changed_packages.py` | 14 | U013814–U013827 | 455 |
| `tools/check_instance_lifecycle.py` | 2 | U013828–U013829 | 42 |
| `tools/check_test_baseline.py` | 3 | U013830–U013832 | 50 |
| `tools/check_versions.py` | 10 | U013833–U013842 | 329 |
| `tools/clean_room_check.py` | 14 | U013843–U013856 | 582 |
| `tools/codemod_core_api.py` | 5 | U013857–U013861 | 249 |
| `tools/codemod_namespace.py` | 22 | U013862–U013883 | 817 |
| `tools/codemod_private_docstrings.py` | 8 | U013884–U013891 | 234 |
| `tools/lint_boundaries.py` | 42 | U013892–U013933 | 1,921 |
| `tools/lint_comments.py` | 31 | U013934–U013964 | 1,246 |
| `tools/lint_versions.py` | 12 | U013965–U013976 | 430 |
| `tools/promote_docker.py` | 1 | U013977–U013977 | 21 |
| `tools/publish_registry.py` | 4 | U013978–U013981 | 143 |
| `tools/render_templates.py` | 6 | U013982–U013987 | 261 |
| `tools/testpypi_publish.py` | 3 | U013988–U013990 | 102 |
| `tools/verify_registry_release.py` | 3 | U013991–U013993 | 45 |

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
<<< UNIT U013014 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:12-12 | ctx=wiki >>>
此模块提供一组操作 MediaWiki 站点的命令。此模块可以查询页面与模板，按 InterWiki 前缀查询其他站点，为请求设置自定义标头与前缀。
<<< END U013014 >>>
<<< UNIT U013015 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:14-14 | ctx=wiki >>>
它还能维护 Wiki API 地址的允许与阻止列表，管理 Wiki 机器人账号，监控滥用日志与最近更改，并提供中文 Minecraft Wiki 的每周页面与茶馆周报订阅。
<<< END U013015 >>>
<<< UNIT U013016 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:16-16 | ctx=wiki >>>
`wiki`、`ab`、`rc`、`newbie` 与 `user` 的查询使用当前场景设置的默认 Wiki。`wiki-audit` 与 `wiki-bot` 不依赖默认 Wiki。
<<< END U013016 >>>
<<< UNIT U013017 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:24-24 | ctx=`wiki` >>>
省略标题时，命令查询默认 Wiki 的主页。未设置默认 Wiki 时，命令返回设置提示。
<<< END U013017 >>>
<<< UNIT U013018 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:26-26 | ctx=`wiki` >>>
填写标题时，命令查询对应页面。参数含模板或解析函数表达式时，命令先把参数当作魔术字求值，再用求值结果查询。
<<< END U013018 >>>
<<< UNIT U013019 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:28-28 | ctx=`wiki` >>>
已设置自定义前缀时，命令会在标题前面加上这个前缀。标题带已配置的 InterWiki 前缀时，命令改查对应的 Wiki。
<<< END U013019 >>>
<<< UNIT U013020 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:30-30 | ctx=`wiki` >>>
平台支持按钮时，页面预览默认使用 button 模式。回复内容是摘要与链接，并附带“渲染预览图”和“╳”两个按钮。
<<< END U013020 >>>
<<< UNIT U013021 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:32-32 | ctx=`wiki` >>>
点击“渲染预览图”后，机器人会发送页面截图。点击“╳”后，机器人会删除这条回复和已经发送的截图。
<<< END U013021 >>>
<<< UNIT U013022 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:34-34 | ctx=`wiki` >>>
平台不支持按钮时，页面预览自动使用 auto 模式。用 `wiki style card` 把场景切换为卡片样式后，页面回复改为图文卡片，不提供按钮。
<<< END U013022 >>>
<<< UNIT U013023 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:37-51 | ctx=`wiki` >>>
  caption="默认 button 模式。点击「渲染预览图」查看截图，点击「╳」删除回复与截图。"
  :log="[
    '用户：~wiki 泥土',
    '机器人：泥土（Dirt）是一种在主世界中大量生成的软质方块。',
    '`https://zh.minecraft.wiki/w/泥土`',
  ]"
  :buttons="[
    {
      label: '渲染预览图',
      loading: '正在生成预览图',
      reply: ['机器人：![泥土页面预览](wiki-preview-dirt.jpg){natural}'],
    },
    { label: '╳', dismiss: true },
  ]"
/>
<<< END U013023 >>>
<<< UNIT U013024 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:54-60 | ctx=`wiki` >>>
  caption="省略标题时查询默认 Wiki 的主页。"
  :log="[
    '用户：~wiki',
    '机器人：欢迎来到这个完全公开、可自由编辑的Wiki，中文Minecraft Wiki。这里致力于收集一切和Minecraft系列有关的信息。任何人都可以为Wiki作出贡献！',
    '`https://zh.minecraft.wiki/`',
  ]"
/>
<<< END U013024 >>>
<<< UNIT U013025 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:63-75 | ctx=`wiki` >>>
  caption="尚未设置默认 Wiki 时，查询会提示先设置，并附带推荐 Wiki 按钮。"
  :log="[
    '用户：~wiki 泥土',
    '机器人：没有设置默认 Wiki，使用“~wiki set”设置默认 Wiki。',
    '点击下方按钮，设置推荐的 Wiki。',
  ]"
  :buttons="[
    {
      label: 'Minecraft Wiki',
      reply: ['机器人：成功设置默认 Wiki：Minecraft Wiki (zh)'],
    },
  ]"
/>
<<< END U013025 >>>
<<< UNIT U013026 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:81-81 | ctx=`wiki magic` >>>
此命令查询目标 Wiki 注册的魔术字与扩展解析函数，返回短文本或查询链接。表达式支持 `#expr`、字符串处理与站点变量。
<<< END U013026 >>>
<<< UNIT U013027 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:83-83 | ctx=`wiki magic` >>>
表达式不完整、包含未支持的魔术字、缺少页面上下文或结果过长时，命令返回对应的提示。
<<< END U013027 >>>
<<< UNIT U013028 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:86-90 | ctx=`wiki magic` >>>
  :log="[
    '用户：~wiki magic #expr:6*7',
    '机器人：42',
  ]"
/>
<<< END U013028 >>>
<<< UNIT U013029 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:96-96 | ctx=`wiki id` >>>
此命令按页面 ID 查询对应页面。`<pageid>` 可以带 InterWiki 前缀，去掉前缀后必须是数字，否则命令返回提示。
<<< END U013029 >>>
<<< UNIT U013030 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:99-104 | ctx=`wiki id` >>>
  :log="[
    '用户：~wiki id 6054',
    '机器人：苦力怕（Creeper）是常见的敌对生物，它会悄无声息地接近玩家，当距离目标3格以内时就会开始爆炸。',
    '`https://zh.minecraft.wiki/w/苦力怕`',
  ]"
/>
<<< END U013030 >>>
<<< UNIT U013031 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:110-110 | ctx=`wiki random` >>>
此命令随机查询一个条目命名空间页面。
<<< END U013031 >>>
<<< UNIT U013032 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:113-118 | ctx=`wiki random` >>>
  :log="[
    '用户：~wiki random',
    '机器人：末影人（Enderman）是一种来自末地、会瞬移的高大黑色敌对生物。',
    '`https://zh.minecraft.wiki/w/末影人`',
  ]"
/>
<<< END U013032 >>>
<<< UNIT U013033 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:124-124 | ctx=`wiki search` >>>
此命令用于搜索页面，至多返回 5 条结果。回复结果前面的编号，或点击按钮，即可查询对应的页面。
<<< END U013033 >>>
<<< UNIT U013034 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:127-167 | ctx=`wiki search` >>>
  caption="点击编号查询页面。页面回复同样附带预览与删除按钮。"
  :log="[
    '用户：~wiki search 苔藓块',
    '机器人：搜索结果：',
    '点击按钮以查询对应的页面。',
  ]"
  :buttons="[
    {
      label: '1. 苔藓块',
      loading: '正在打开页面',
      reply: [
        '机器人：苔藓块（Moss Block）是一种生成于繁茂洞穴、能在骨粉的作用下快速蔓延的植物方块。',
        '`https://zh.minecraft.wiki/w/苔藓块`',
      ],
      buttons: [
        {
          label: '渲染预览图',
          loading: '正在生成预览图',
          reply: ['机器人：![苔藓块页面预览](wiki-preview-moss.jpg){natural}'],
        },
        { label: '╳', dismiss: true },
      ],
    },
    {
      label: '2. 苍白苔藓块',
      loading: '正在打开页面',
      reply: [
        '机器人：苍白苔藓块（Pale Moss Block）是一种生成于苍白之园生物群系的方块。',
        '`https://zh.minecraft.wiki/w/苍白苔藓块`',
      ],
      buttons: [
        {
          label: '渲染预览图',
          loading: '正在生成预览图',
          reply: ['机器人：![苍白苔藓块页面预览](wiki-preview-pale-moss.jpg){natural}'],
        },
        { label: '╳', dismiss: true },
      ],
    },
  ]"
/>
<<< END U013034 >>>
<<< UNIT U013035 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:173-173 | ctx=`wiki render` >>>
此命令用于切换页面渲染方式。`button` 在回复中附带预览按钮，`auto` 自动补发页面截图，`off` 关闭页面渲染。取值不在三者之内时，命令返回错误提示。
<<< END U013035 >>>
<<< UNIT U013036 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:176-192 | ctx=`wiki render` >>>
  caption="button：页面回复只显示摘要、链接和预览按钮。"
  :log="[
    '用户：~wiki render button',
    '机器人：已切换为消息展示按钮。',
    '用户：~wiki 泥土',
    '机器人：泥土（Dirt）是一种在主世界中大量生成的软质方块。',
    '`https://zh.minecraft.wiki/w/泥土`',
  ]"
  :buttons="[
    {
      label: '渲染预览图',
      loading: '正在生成预览图',
      reply: ['机器人：![泥土页面预览](wiki-preview-dirt.jpg){natural}'],
    },
    { label: '╳', dismiss: true },
  ]"
/>
<<< END U013036 >>>
<<< UNIT U013037 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:195-204 | ctx=`wiki render` >>>
  caption="auto：发送摘要与链接后自动补发页面截图，不显示预览按钮。"
  :log="[
    '用户：~wiki render auto',
    '机器人：已切换为自动渲染 Wiki 页面。',
    '用户：~wiki 泥土',
    '机器人：泥土（Dirt）是一种在主世界中大量生成的软质方块。',
    '`https://zh.minecraft.wiki/w/泥土`',
    '![泥土页面预览](wiki-preview-dirt.jpg){natural}',
  ]"
/>
<<< END U013037 >>>
<<< UNIT U013038 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:207-215 | ctx=`wiki render` >>>
  caption="off：只发送摘要与链接，不渲染页面截图。"
  :log="[
    '用户：~wiki render off',
    '机器人：已关闭 Wiki 页面渲染。',
    '用户：~wiki 泥土',
    '机器人：泥土（Dirt）是一种在主世界中大量生成的软质方块。',
    '`https://zh.minecraft.wiki/w/泥土`',
  ]"
/>
<<< END U013038 >>>
<<< UNIT U013039 | md-list | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:221-224 | ctx=`wiki style` >>>
- 此命令用于切换 Wiki 消息样式，默认为 `text`，仅在 QQ 群与 QQ 私聊注册。
- `card` 把页面回复渲染为图文卡片。标题取页面标题，摘要取页面描述，配图取页面代表图的 100 像素缩略图。
- 页面没有代表图时，卡片不带配图。查询目标带有修订号，或查询的是差异内容时，卡片同样不带配图。
- 卡片消息不支持按钮，`button` 预览模式因此改用 `auto`。
<<< END U013039 >>>
<<< UNIT U013040 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:227-232 | ctx=`wiki style` >>>
  caption="切换后页面查询改用卡片消息；卡片消息不支持按钮，button 预览模式改用 auto。"
  :log="[
    '用户：~wiki style card',
    '机器人：已切换为卡片消息样式。卡片消息不支持按钮，button 预览模式将改用 auto（自动渲染）模式。',
  ]"
/>
<<< END U013040 >>>
<<< UNIT U013041 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:235-244 | ctx=`wiki style` >>>
  caption="卡片样式：查询「石头」时返回的图文卡片。"
  :log="['用户：~wiki 石头']"
  :card="{
    title: '石头',
    description: '石头（Stone）是在主世界中大量存在的方块。',
    url: 'https://zh.minecraft.wiki/w/石头',
    image: 'wiki-card-stone.png',
    domain: 'zh.minecraft.wiki',
  }"
/>
<<< END U013041 >>>
<<< UNIT U013042 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:250-250 | ctx=`wiki set` >>>
此命令用于设置场景的默认 Wiki，参数为页面地址、站点地址或 API 地址。每个场景保存一个默认 Wiki，再次设置会覆盖原来的值。
<<< END U013042 >>>
<<< UNIT U013043 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:252-252 | ctx=`wiki set` >>>
地址无法解析时，命令返回失败详情。地址在全局阻止列表中时，命令拒绝设置。
<<< END U013043 >>>
<<< UNIT U013044 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:254-254 | ctx=`wiki set` >>>
`wiki iw` 组的子命令都可以用 `interwiki` 代替，例如 `interwiki list`。
<<< END U013044 >>>
<<< UNIT U013045 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:257-261 | ctx=`wiki set` >>>
  :log="[
    '用户：~wiki set https://zh.minecraft.wiki',
    '机器人：成功设置默认 Wiki：Minecraft Wiki (zh)',
  ]"
/>
<<< END U013045 >>>
<<< UNIT U013046 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:267-267 | ctx=`wiki iw add` >>>
此命令用于添加自定义 InterWiki。`<interwiki>` 是前缀名，`<wikiurl>` 会先解析成 API 地址再保存。前缀已存在时，命令覆盖原来的值。地址无法解析时，命令返回失败详情。
<<< END U013046 >>>
<<< UNIT U013047 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:270-275 | ctx=`wiki iw add` >>>
  :log="[
    '用户：~wiki iw add wikipedia https://zh.wikipedia.org',
    '机器人：已添加自定义 InterWiki：',
    'wikipedia -> 维基百科 (zh)',
  ]"
/>
<<< END U013047 >>>
<<< UNIT U013048 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:281-281 | ctx=`wiki iw remove` >>>
此命令用于删除自定义 InterWiki。前缀未设置时，命令同样返回成功。
<<< END U013048 >>>
<<< UNIT U013049 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:284-288 | ctx=`wiki iw remove` >>>
  :log="[
    '用户：~wiki iw remove wikipedia',
    '机器人：已删除自定义 InterWiki：wikipedia',
  ]"
/>
<<< END U013049 >>>
<<< UNIT U013050 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:294-294 | ctx=`wiki iw list` >>>
此命令列出当前设置的自定义 InterWiki，结果附带查看默认 Wiki InterWiki 的链接。平台支持图片时，命令把列表渲染成表格图片。加上 `--legacy` 后，命令改用文本列表。没有设置自定义 InterWiki 时，命令返回添加提示。
<<< END U013050 >>>
<<< UNIT U013051 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:297-303 | ctx=`wiki iw list` >>>
  :log="[
    '用户：~wiki iw list --legacy',
    '机器人：当前设置了以下 InterWiki：',
    'wikipedia: https://zh.wikipedia.org/w/api.php',
    '此处展示的是为机器人设置的自定义 InterWiki，如需查看默认 Wiki 的 InterWiki，请见：`https://zh.minecraft.wiki/w/Special:Interwiki`',
  ]"
/>
<<< END U013051 >>>
<<< UNIT U013052 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:309-309 | ctx=`wiki iw get` >>>
此命令获取 InterWiki 对应的 API 地址。前缀未配置时，命令返回未找到提示。
<<< END U013052 >>>
<<< UNIT U013053 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:312-316 | ctx=`wiki iw get` >>>
  :log="[
    '用户：~wiki iw get wikipedia',
    '机器人：`https://zh.wikipedia.org/w/api.php`',
  ]"
/>
<<< END U013053 >>>
<<< UNIT U013054 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:322-322 | ctx=`wiki headers show` >>>
此命令列出当前场景设置的自定义请求标头，结果以 JSON 对象返回。未设置时，命令返回空对象。
<<< END U013054 >>>
<<< UNIT U013055 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:325-329 | ctx=`wiki headers show` >>>
  :log="[
    '用户：~wiki headers show',
    '机器人：当前设置了以下请求标头：\n{}\n如需自定义，请使用“~wiki headers add”。\n示例：\n~wiki headers add {&quot;accept-language&quot;: &quot;zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6&quot;}',
  ]"
/>
<<< END U013055 >>>
<<< UNIT U013056 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:335-335 | ctx=`wiki headers add` >>>
此命令用于添加或覆盖请求标头。`<headers>` 是 JSON 对象，键是标头名，值是要写入的内容。参数不是 JSON 对象时，命令返回失败提示。
<<< END U013056 >>>
<<< UNIT U013057 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:338-342 | ctx=`wiki headers add` >>>
  :log="[
    '用户：~wiki headers add {&quot;accept-language&quot;:&quot;zh-CN&quot;}',
    '机器人：已更新请求时所使用的请求标头：{&quot;accept-language&quot;:&quot;zh-CN&quot;}',
  ]"
/>
<<< END U013057 >>>
<<< UNIT U013058 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:348-348 | ctx=`wiki headers remove` >>>
此命令按名称删除一个请求标头。标头不存在时，命令返回失败提示。
<<< END U013058 >>>
<<< UNIT U013059 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:351-355 | ctx=`wiki headers remove` >>>
  :log="[
    '用户：~wiki headers remove accept-language',
    '机器人：已更新请求时所使用的请求标头：{}',
  ]"
/>
<<< END U013059 >>>
<<< UNIT U013060 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:361-361 | ctx=`wiki headers reset` >>>
此命令用于清空当前场景设置的全部自定义请求标头。
<<< END U013060 >>>
<<< UNIT U013061 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:364-368 | ctx=`wiki headers reset` >>>
  :log="[
    '用户：~wiki headers reset',
    '机器人：已重置请求时所使用的请求标头。',
  ]"
/>
<<< END U013061 >>>
<<< UNIT U013062 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:374-374 | ctx=`wiki prefix set` >>>
此命令用于设置查询标题时附加的前缀。设置后，命令会把前缀拼在标题前面。这个前缀用于统一命名空间，或区分同名页面。
<<< END U013062 >>>
<<< UNIT U013063 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:377-381 | ctx=`wiki prefix set` >>>
  :log="[
    '用户：~wiki prefix set Help:',
    '机器人：已更新请求时所使用的前缀：Help:',
  ]"
/>
<<< END U013063 >>>
<<< UNIT U013064 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:387-387 | ctx=`wiki prefix reset` >>>
此命令用于清除自定义前缀，恢复按原样查询标题。
<<< END U013064 >>>
<<< UNIT U013065 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:390-394 | ctx=`wiki prefix reset` >>>
  :log="[
    '用户：~wiki prefix reset',
    '机器人：已重置请求时所使用的前缀。',
  ]"
/>
<<< END U013065 >>>
<<< UNIT U013066 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:400-400 | ctx=`wiki redlink` >>>
此命令用于切换页面不存在时是否返回编辑链接。每执行一次，命令在开启与关闭之间切换。
<<< END U013066 >>>
<<< UNIT U013067 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:403-407 | ctx=`wiki redlink` >>>
  :log="[
    '用户：~wiki redlink',
    '机器人：已开启页面不存在时返回编辑链接。',
  ]"
/>
<<< END U013067 >>>
<<< UNIT U013068 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:413-413 | ctx=wiki-inline >>>
此模块没有命令，按消息内容触发。
<<< END U013068 >>>
<<< UNIT U013069 | md-list | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:415-418 | ctx=wiki-inline >>>
- `[[标题]]`：查询页面，忽略以 `#` 开头的标题。去掉重复的标题后，至多处理 5 个页面。
- 用双层花括号包裹的模板名：解析模板调用与解析函数。
- `≺标题≻` 或 `⧼标题⧽`：查询 MediaWiki 命名空间页面。
- Wiki 页面 URL：生成 Infobox 预览或返回文件，返回哪种由渲染方式决定。
<<< END U013069 >>>
<<< UNIT U013070 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:428-428 | ctx=`wiki-audit trust` >>>
此命令从 Wiki 页面、站点或 API 地址中解析出 API 地址，再加入全局 URL 允许列表。地址无法解析，或已在阻止列表中时，命令返回失败。
<<< END U013070 >>>
<<< UNIT U013071 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:431-435 | ctx=`wiki-audit trust` >>>
  :log="[
    '用户：~wiki-audit trust https://zh.minecraft.wiki',
    '机器人：已将规则加入用户自定义 URL 允许列表：https://zh.minecraft.wiki/api.php',
  ]"
/>
<<< END U013071 >>>
<<< UNIT U013072 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:441-441 | ctx=`wiki-audit block` >>>
此命令从 Wiki 页面、站点或 API 地址中解析出 API 地址，再加入全局 URL 阻止列表。地址无法解析时，命令返回失败。
<<< END U013072 >>>
<<< UNIT U013073 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:444-448 | ctx=`wiki-audit block` >>>
  :log="[
    '用户：~wiki-audit block https://zh.wikipedia.org',
    '机器人：已将规则加入用户自定义 URL 阻止列表：https://zh.wikipedia.org/w/api.php',
  ]"
/>
<<< END U013073 >>>
<<< UNIT U013074 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:454-454 | ctx=`wiki-audit distrust` >>>
此命令从全局 URL 用户允许列表移除该 API 地址。地址不在列表中时，命令返回未找到。
<<< END U013074 >>>
<<< UNIT U013075 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:457-461 | ctx=`wiki-audit distrust` >>>
  :log="[
    '用户：~wiki-audit distrust https://zh.minecraft.wiki',
    '机器人：已从用户自定义 URL 允许列表删除规则：https://zh.minecraft.wiki/api.php',
  ]"
/>
<<< END U013075 >>>
<<< UNIT U013076 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:467-467 | ctx=`wiki-audit unblock` >>>
此命令从全局 URL 用户阻止列表移除该 API 地址。地址不在列表中时，命令返回未找到。
<<< END U013076 >>>
<<< UNIT U013077 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:470-474 | ctx=`wiki-audit unblock` >>>
  :log="[
    '用户：~wiki-audit unblock https://zh.wikipedia.org',
    '机器人：已从用户自定义 URL 阻止列表删除规则：https://zh.wikipedia.org/w/api.php',
  ]"
/>
<<< END U013077 >>>
<<< UNIT U013078 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:480-480 | ctx=`wiki-audit query` >>>
此命令解析 API 地址并查询命中的全局允许列表规则，返回规则来源。未命中时，命令返回未授权结论。
<<< END U013078 >>>
<<< UNIT U013079 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:483-488 | ctx=`wiki-audit query` >>>
  :log="[
    '用户：~wiki-audit query https://zh.minecraft.wiki',
    '机器人：https://zh.minecraft.wiki/api.php 已被以下全局规则放行：',
    '[用户规则] https://zh.minecraft.wiki/api.php',
  ]"
/>
<<< END U013079 >>>
<<< UNIT U013080 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:498-498 | ctx=`wiki-bot login` >>>
此命令用于登录 Wiki 机器人账号并保存。账号已存在时，命令提示先登出。登录失败时，命令返回失败原因。
<<< END U013080 >>>
<<< UNIT U013081 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:504-504 | ctx=`wiki-bot logout` >>>
此命令用于删除已保存的机器人账号。
<<< END U013081 >>>
<<< UNIT U013082 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:510-510 | ctx=`wiki-bot toggle` >>>
此命令用于切换当前场景是否使用机器人账号，返回开启或关闭结果。
<<< END U013082 >>>
<<< UNIT U013083 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:513-517 | ctx=`wiki-bot toggle` >>>
  :log="[
    '用户：~wiki-bot toggle',
    '机器人：已开启使用机器人账户。',
  ]"
/>
<<< END U013083 >>>
<<< UNIT U013084 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:525-525 | ctx=`ab` >>>
此命令获取默认 Wiki 的最近滥用日志。QQ 平台具备合并转发或渲染能力时，命令优先返回合并转发消息或渲染结果，否则返回普通消息。获取失败或日志受查看权限限制时，命令返回错误提示。
<<< END U013084 >>>
<<< UNIT U013085 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:528-532 | ctx=`ab` >>>
  :log="[
    '用户：~ab --legacy',
    '机器人：`https://zh.minecraft.wiki/w/Special:AbuseLog`\n•2026-11-12 21:03:11 - Example 在 草方块 执行操作“edit”时触发了过滤器。\n过滤器描述：破坏性编辑\n采取的行动：warn',
  ]"
/>
<<< END U013085 >>>
<<< UNIT U013086 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:538-538 | ctx=`rc` >>>
此命令获取默认 Wiki 的最近更改。QQ 平台具备合并转发或渲染能力时，命令优先返回合并转发消息或渲染结果，否则返回普通消息。获取失败或日志受查看权限限制时，命令返回错误提示。
<<< END U013086 >>>
<<< UNIT U013087 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:541-545 | ctx=`rc` >>>
  :log="[
    '用户：~rc --legacy',
    '机器人：`https://zh.minecraft.wiki/w/Special:RecentChanges`\n•2026-11-12 21:02:45 - 草方块 .. (+128) .. Example\n（修正笔误）',
  ]"
/>
<<< END U013087 >>>
<<< UNIT U013088 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:551-551 | ctx=`newbie` >>>
此命令获取默认 Wiki 的新用户日志。
<<< END U013088 >>>
<<< UNIT U013089 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:554-558 | ctx=`newbie` >>>
  :log="[
    '用户：~newbie',
    '机器人：`https://zh.minecraft.wiki/w/Special:Log?type=newusers`\nExampleUser\nSteve\nAlex',
  ]"
/>
<<< END U013089 >>>
<<< UNIT U013090 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:564-564 | ctx=`user` >>>
此命令用于查询 MediaWiki 用户信息。`username` 可带 InterWiki 前缀。前缀必须是已配置的 InterWiki，否则命令按原名查询。
<<< END U013090 >>>
<<< UNIT U013091 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:567-571 | ctx=`user` >>>
  :log="[
    '用户：~user Example',
    '机器人：用户：Example | 编辑数：0\n用户组：*、user\n性别：未知\n注册时间：2026 年 07 月 04 日 00:48:20 (UTC+8)',
  ]"
/>
<<< END U013091 >>>
<<< UNIT U013092 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:579-579 | ctx=`wikilog add wiki` >>>
此命令用于把一个 Wiki 加入监控列表。地址无法解析时，命令返回失败原因。Wiki 已在列表中时，命令返回操作失败。
<<< END U013092 >>>
<<< UNIT U013093 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:582-586 | ctx=`wikilog add wiki` >>>
  :log="[
    '用户：~wikilog add wiki https://zh.minecraft.wiki',
    '机器人：成功操作 Wiki：Minecraft Wiki (zh)',
  ]"
/>
<<< END U013093 >>>
<<< UNIT U013094 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:592-592 | ctx=`wikilog reset wiki` >>>
此命令将该 Wiki 的监控配置恢复为默认值。
<<< END U013094 >>>
<<< UNIT U013095 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:595-599 | ctx=`wikilog reset wiki` >>>
  :log="[
    '用户：~wikilog reset wiki https://zh.minecraft.wiki',
    '机器人：成功操作 Wiki：Minecraft Wiki (zh)',
  ]"
/>
<<< END U013095 >>>
<<< UNIT U013096 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:605-605 | ctx=`wikilog remove wiki` >>>
此命令从监控列表移除一个 Wiki。地址不在列表中时，命令返回操作失败。
<<< END U013096 >>>
<<< UNIT U013097 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:608-612 | ctx=`wikilog remove wiki` >>>
  :log="[
    '用户：~wikilog remove wiki https://zh.minecraft.wiki',
    '机器人：成功操作 Wiki：Minecraft Wiki (zh)',
  ]"
/>
<<< END U013097 >>>
<<< UNIT U013098 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:618-618 | ctx=`wikilog enable` >>>
此命令用于启用一种类型的日志监控，`logtype` 取 `ab`、`rc` 或对应的全名。取值无效或 Wiki 未加入监控列表时，命令返回失败提示。
<<< END U013098 >>>
<<< UNIT U013099 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:621-625 | ctx=`wikilog enable` >>>
  :log="[
    '用户：~wikilog enable https://zh.minecraft.wiki ab',
    '机器人：成功操作了 Minecraft Wiki (zh) AbuseLog 的监控设置。',
  ]"
/>
<<< END U013099 >>>
<<< UNIT U013100 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:631-631 | ctx=`wikilog disable` >>>
此命令用于禁用一种类型的日志监控。
<<< END U013100 >>>
<<< UNIT U013101 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:634-638 | ctx=`wikilog disable` >>>
  :log="[
    '用户：~wikilog disable https://zh.minecraft.wiki ab',
    '机器人：成功操作了 Minecraft Wiki (zh) AbuseLog 的监控设置。',
  ]"
/>
<<< END U013101 >>>
<<< UNIT U013102 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:644-644 | ctx=`wikilog filter set` >>>
此命令为某一类型的日志设置条件过滤器，`...` 处填写多条正则表达式。未给出条件时，命令提示条件为空。
<<< END U013102 >>>
<<< UNIT U013103 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:647-652 | ctx=`wikilog filter set` >>>
  :log="[
    '用户：~wikilog filter set https://zh.minecraft.wiki ab 破坏',
    '机器人：成功为 Minecraft Wiki (zh) AbuseLog 设置了以下过滤器：',
    '破坏',
  ]"
/>
<<< END U013103 >>>
<<< UNIT U013104 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:658-658 | ctx=`wikilog filter reset` >>>
此命令用于重置某一类型日志的条件过滤器。
<<< END U013104 >>>
<<< UNIT U013105 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:661-666 | ctx=`wikilog filter reset` >>>
  :log="[
    '用户：~wikilog filter reset https://zh.minecraft.wiki ab',
    '机器人：成功为 Minecraft Wiki (zh) AbuseLog 设置了以下过滤器：',
    '*',
  ]"
/>
<<< END U013105 >>>
<<< UNIT U013106 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:672-672 | ctx=`wikilog filter test` >>>
此命令用于测试条件过滤器能否匹配给定样例，返回匹配位置。表达式有误时，命令提示匹配失败。
<<< END U013106 >>>
<<< UNIT U013107 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:675-679 | ctx=`wikilog filter test` >>>
  :log="[
    '用户：~wikilog filter test ^bot bot_test',
    '机器人：成功在 0, 3 处匹配了文本：bot',
  ]"
/>
<<< END U013107 >>>
<<< UNIT U013108 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:685-685 | ctx=`wikilog filter example` >>>
此命令把数据转换为条件过滤器可识别的样例。样例不是合法 JSON 时，命令提示格式无效。
<<< END U013108 >>>
<<< UNIT U013109 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:688-692 | ctx=`wikilog filter example` >>>
  :log="[
    '用户：~wikilog filter example {&quot;user&quot;:&quot;Example&quot;}',
    '机器人：user=Example',
  ]"
/>
<<< END U013109 >>>
<<< UNIT U013110 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:698-698 | ctx=`wikilog api get` >>>
此命令获取指定 Wiki 上对应日志类型的 API 数据链接。
<<< END U013110 >>>
<<< UNIT U013111 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:701-705 | ctx=`wikilog api get` >>>
  :log="[
    '用户：~wikilog api get https://zh.minecraft.wiki ab',
    '机器人：`https://zh.minecraft.wiki/api.php?action=query&list=abuselog&aflprop=user%7Ctitle%7Caction%7Cresult%7Cfilter%7Ctimestamp&afllimit=30`',
  ]"
/>
<<< END U013111 >>>
<<< UNIT U013112 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:711-711 | ctx=`wikilog rcshow set` >>>
此命令为最近更改日志设置筛选条件，取值见下文列表。条件无效时，命令返回提示。
<<< END U013112 >>>
<<< UNIT U013113 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:714-720 | ctx=`wikilog rcshow set` >>>
  :log="[
    '用户：~wikilog rcshow set https://zh.minecraft.wiki !bot !minor',
    '机器人：成功为 Minecraft Wiki (zh) 最近更改监控设置了以下筛选条件：',
    '!bot',
    '!minor',
  ]"
/>
<<< END U013113 >>>
<<< UNIT U013114 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:726-726 | ctx=`wikilog rcshow reset` >>>
此命令用于重置最近更改日志设置的筛选条件。
<<< END U013114 >>>
<<< UNIT U013115 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:729-733 | ctx=`wikilog rcshow reset` >>>
  :log="[
    '用户：~wikilog rcshow reset https://zh.minecraft.wiki',
    '机器人：成功为 Minecraft Wiki (zh) 最近更改监控设置了以下筛选条件：',
  ]"
/>
<<< END U013115 >>>
<<< UNIT U013116 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:739-739 | ctx=`wikilog bot enable` >>>
此命令用于启用机器人获取日志。
<<< END U013116 >>>
<<< UNIT U013117 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:742-746 | ctx=`wikilog bot enable` >>>
  :log="[
    '用户：~wikilog bot enable https://zh.minecraft.wiki',
    '机器人：成功操作 Wiki：Minecraft Wiki (zh)',
  ]"
/>
<<< END U013117 >>>
<<< UNIT U013118 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:752-752 | ctx=`wikilog bot disable` >>>
此命令用于禁用机器人获取日志。
<<< END U013118 >>>
<<< UNIT U013119 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:755-759 | ctx=`wikilog bot disable` >>>
  :log="[
    '用户：~wikilog bot disable https://zh.minecraft.wiki',
    '机器人：成功操作 Wiki：Minecraft Wiki (zh)',
  ]"
/>
<<< END U013119 >>>
<<< UNIT U013120 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:765-765 | ctx=`wikilog keepalive enable` >>>
此命令用于启用机器人登录状态检查。
<<< END U013120 >>>
<<< UNIT U013121 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:768-772 | ctx=`wikilog keepalive enable` >>>
  :log="[
    '用户：~wikilog keepalive enable https://zh.minecraft.wiki',
    '机器人：成功操作 Wiki：Minecraft Wiki (zh)',
  ]"
/>
<<< END U013121 >>>
<<< UNIT U013122 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:778-778 | ctx=`wikilog keepalive disable` >>>
此命令用于禁用机器人登录状态检查。
<<< END U013122 >>>
<<< UNIT U013123 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:781-785 | ctx=`wikilog keepalive disable` >>>
  :log="[
    '用户：~wikilog keepalive disable https://zh.minecraft.wiki',
    '机器人：成功操作 Wiki：Minecraft Wiki (zh)',
  ]"
/>
<<< END U013123 >>>
<<< UNIT U013124 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:791-791 | ctx=`wikilog note set` >>>
此命令用于设置一条 Wiki 的备注，监控消息用这条备注代替 Wiki 名称。Wiki 未加入监控列表时，命令返回失败。
<<< END U013124 >>>
<<< UNIT U013125 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:794-798 | ctx=`wikilog note set` >>>
  :log="[
    '用户：~wikilog note set https://zh.minecraft.wiki 主站',
    '机器人：成功为 Minecraft Wiki (zh) 设置了备注：主站',
  ]"
/>
<<< END U013125 >>>
<<< UNIT U013126 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:804-804 | ctx=`wikilog note remove` >>>
此命令用于移除一条 Wiki 的备注。
<<< END U013126 >>>
<<< UNIT U013127 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:807-811 | ctx=`wikilog note remove` >>>
  :log="[
    '用户：~wikilog note remove https://zh.minecraft.wiki',
    '机器人：成功为 Minecraft Wiki (zh) 设置了备注：',
  ]"
/>
<<< END U013127 >>>
<<< UNIT U013128 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:817-817 | ctx=`wikilog list` >>>
此命令列出各 Wiki 的监控设置。
<<< END U013128 >>>
<<< UNIT U013129 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:819-819 | ctx=`wikilog list` >>>
上文各命令的 `logtype` 参数可以取 `ab`、`rc`、`abuselog`、`recentchanges`、`AbuseLog` 与 `RecentChanges`。最近更改的筛选条件可以取 `!anon`、`!autopatrolled`、`!bot`、`!minor`、`!patrolled`、`!redirect`、`anon`、`autopatrolled`、`bot`、`minor`、`patrolled`、`redirect` 与 `unpatrolled`。
<<< END U013129 >>>
<<< UNIT U013130 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:822-826 | ctx=`wikilog list` >>>
  :log="[
    '用户：~wikilog list',
    '机器人：https://zh.minecraft.wiki/api.php: \n滥用过滤器日志：已启用\n条件过滤器：\n&quot;破坏&quot;\n最近更改：已启用\n条件过滤器：\n&quot;!bot&quot;\n筛选条件：\n&quot;!bot&quot; &quot;!minor&quot;\n使用机器人获取信息：已禁用\n备注：主站',
  ]"
/>
<<< END U013130 >>>
<<< UNIT U013131 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:834-834 | ctx=`weekly` >>>
此命令获取中文 Minecraft Wiki 的每周页面，QQ 平台会附带图片。
<<< END U013131 >>>
<<< UNIT U013132 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:837-841 | ctx=`weekly` >>>
  :log="[
    '用户：~weekly',
    '机器人：本周页面：苔藓块（Moss Block）是一种生成于繁茂洞穴、能在骨粉的作用下快速蔓延的植物方块。……\n图片：`https://zh.minecraft.wiki/images/Moss_Block_JE1_BE1.png`\n页面链接：`https://zh.minecraft.wiki/w/苔藓块`\n每周页面：`https://zh.minecraft.wiki/w/Minecraft_Wiki:特色条目/Minecraft/2026#第46周`',
  ]"
/>
<<< END U013132 >>>
<<< UNIT U013133 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:847-847 | ctx=`weekly image` >>>
此命令获取每周页面的截图版。
<<< END U013133 >>>
<<< UNIT U013134 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:850-854 | ctx=`weekly image` >>>
  :log="[
    '用户：~weekly image',
    '机器人：![每周页面截图](weekly-image-example.webp)',
  ]"
/>
<<< END U013134 >>>
<<< UNIT U013135 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:860-860 | ctx=`weekly teahouse` >>>
此命令获取茶馆周报。
<<< END U013135 >>>
<<< UNIT U013136 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:863-867 | ctx=`weekly teahouse` >>>
  :log="[
    '用户：~weekly teahouse',
    '机器人：茶馆周报第 46 期\n\n……',
  ]"
/>
<<< END U013136 >>>
<<< UNIT U013137 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:873-873 | ctx=`weekly teahouse image` >>>
此命令获取茶馆周报的截图版。
<<< END U013137 >>>
<<< UNIT U013138 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:877-877 | ctx=RSS >>>
`weekly-rss` 与 `teahouse-weekly-rss` 没有命令，只提供 RSS 订阅。前者在每周一 9:00 推送中文 Minecraft Wiki 的每周页面，后者在每周一 9:30 推送茶馆周报。推送同时提供简体中文与繁体中文文本，QQ 平台使用图片版本。
<<< END U013138 >>>
<<< UNIT U013139 | md-heading | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:879-879 | ctx=每周页面订阅 >>>
### 每周页面订阅
<<< END U013139 >>>
<<< UNIT U013140 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:882-893 | ctx=每周页面订阅 >>>
  caption="示例内容随当周页面变化"
  :log="[
    '用户：~module enable weekly-rss',
    '机器人：成功：开启模块“weekly-rss”。',
    '〰〰〰',
    '机器人：如需获取每周页面的文字版本及链接，请使用“~weekly”。',
    '本周页面：苔藓块（Moss Block）是一种生成于繁茂洞穴、能在骨粉的作用下快速蔓延的植物方块。……',
    '图片：`https://zh.minecraft.wiki/images/Moss_Block_JE1_BE1.png`',
    '页面链接：`https://zh.minecraft.wiki/w/苔藓块`',
    '每周页面：`https://zh.minecraft.wiki/w/Minecraft_Wiki:特色条目/Minecraft/2026#第46周`',
  ]"
/>
<<< END U013140 >>>
<<< UNIT U013141 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:895-895 | ctx=每周页面订阅 >>>
QQ 平台发送整条消息的图片，其他平台发送文字与链接。
<<< END U013141 >>>
<<< UNIT U013142 | md-heading | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:897-897 | ctx=茶馆周报订阅 >>>
### 茶馆周报订阅
<<< END U013142 >>>
<<< UNIT U013143 | md-paragraph | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/docs/index.md:900-913 | ctx=茶馆周报订阅 >>>
  caption="示例内容随当周推送变化"
  :log="[
    '用户：~module enable teahouse-weekly-rss',
    '机器人：成功：开启模块“teahouse-weekly-rss”。',
    '〰〰〰',
    '机器人：如需获取每周页面的文字版本及链接，请使用“~weekly teahouse”。',
    '茶馆周报 26w46a',
    '茶馆周报更新了如下内容：',
    '  * 上周的Minecraft新闻',
    '    * Java版快照26.4-snapshot-7',
    '    * 基岩版测试版26.70.23',
    '  * ……',
  ]"
/>
<<< END U013143 >>>
<<< UNIT U013144 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:2-2 | ctx=config.comments.module_wiki.wiki_allowlist_url >>>
Wiki API 加入全局 URL 允许列表的申请网址。
<<< END U013144 >>>
<<< UNIT U013145 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:3-3 | ctx=tos.message.reason.too_many_redirects >>>
使机器人重定向页面的次数过多。
<<< END U013145 >>>
<<< UNIT U013146 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:4-4 | ctx=tos.message.reason.wiki_abuse >>>
一次性查询的页面超过 15 个。
<<< END U013146 >>>
<<< UNIT U013147 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:5-5 | ctx=wiki.help >>>
查询一个 Wiki 页面。
<<< END U013147 >>>
<<< UNIT U013148 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:6-6 | ctx=wiki.help.ab >>>
获取默认 Wiki 的最近滥用日志。
<<< END U013148 >>>
<<< UNIT U013149 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:7-7 | ctx=wiki.help.headers.add >>>
添加自定义请求标头。
<<< END U013149 >>>
<<< UNIT U013150 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:8-8 | ctx=wiki.help.headers.remove >>>
删除自定义请求标头。
<<< END U013150 >>>
<<< UNIT U013151 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:9-9 | ctx=wiki.help.headers.reset >>>
重置自定义请求标头。
<<< END U013151 >>>
<<< UNIT U013152 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:10-10 | ctx=wiki.help.headers.show >>>
列出当前设置的请求标头。
<<< END U013152 >>>
<<< UNIT U013153 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:11-11 | ctx=wiki.help.id >>>
根据页面 ID 查询一个 Wiki 页面。
<<< END U013153 >>>
<<< UNIT U013154 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:12-12 | ctx=wiki.help.iw.add >>>
添加自定义 InterWiki。
<<< END U013154 >>>
<<< UNIT U013155 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:13-13 | ctx=wiki.help.iw.get >>>
获取设置的 InterWiki 对应的 API 地址。
<<< END U013155 >>>
<<< UNIT U013156 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:14-14 | ctx=wiki.help.iw.list >>>
列出当前设置的 InterWiki。
<<< END U013156 >>>
<<< UNIT U013157 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:15-15 | ctx=wiki.help.iw.remove >>>
删除自定义 InterWiki。
<<< END U013157 >>>
<<< UNIT U013158 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:16-16 | ctx=wiki.help.newbie >>>
获取默认 Wiki 的新用户日志。
<<< END U013158 >>>
<<< UNIT U013159 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:17-17 | ctx=wiki.help.option.l >>>
查找本页面对应的语言版本，若无结果则返回当前语言。
<<< END U013159 >>>
<<< UNIT U013160 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:18-18 | ctx=wiki.help.prefix.reset >>>
重置自定义前缀。
<<< END U013160 >>>
<<< UNIT U013161 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:19-19 | ctx=wiki.help.prefix.set >>>
设置自定义前缀。
<<< END U013161 >>>
<<< UNIT U013162 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:20-20 | ctx=wiki.help.random >>>
随机一个 Wiki 页面。
<<< END U013162 >>>
<<< UNIT U013163 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:21-21 | ctx=wiki.help.render >>>
切换 Wiki 页面渲染方式（button、auto 或 off）。
<<< END U013163 >>>
<<< UNIT U013164 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:22-22 | ctx=wiki.help.style >>>
切换 Wiki 消息样式（text 或 card）。
<<< END U013164 >>>
<<< UNIT U013165 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:23-23 | ctx=wiki.help.rc >>>
获取默认 Wiki 的最近更改。
<<< END U013165 >>>
<<< UNIT U013166 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:24-24 | ctx=wiki.help.redlink >>>
切换是否在页面不存在时返回编辑链接。
<<< END U013166 >>>
<<< UNIT U013167 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:25-25 | ctx=wiki.help.search >>>
搜索一个 Wiki 页面。
<<< END U013167 >>>
<<< UNIT U013168 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:26-26 | ctx=wiki.help.set >>>
设置默认 Wiki。
<<< END U013168 >>>
<<< UNIT U013169 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:27-27 | ctx=wiki.help.user >>>
获取一个 MediaWiki 用户的信息。
<<< END U013169 >>>
<<< UNIT U013170 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:28-28 | ctx=wiki.help.wiki-audit.block >>>
从 Wiki 地址解析 API URL，并加入全局 URL 阻止列表。
<<< END U013170 >>>
<<< UNIT U013171 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:29-29 | ctx=wiki.help.wiki-audit.desc >>>
解析 Wiki API URL，并管理其全局 URL 允许与阻止列表规则。
<<< END U013171 >>>
<<< UNIT U013172 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:30-30 | ctx=wiki.help.wiki-audit.distrust >>>
从全局 URL 用户允许列表删除 Wiki 的 API URL。
<<< END U013172 >>>
<<< UNIT U013173 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:31-31 | ctx=wiki.help.wiki-audit.query >>>
解析 Wiki API URL，并查询其全局 URL 允许列表状态。
<<< END U013173 >>>
<<< UNIT U013174 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:32-32 | ctx=wiki.help.wiki-audit.trust >>>
从 Wiki 页面、站点或 API 地址解析 API URL，并加入全局 URL 允许列表。
<<< END U013174 >>>
<<< UNIT U013175 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:33-33 | ctx=wiki.help.wiki-audit.unblock >>>
从全局 URL 用户阻止列表删除 Wiki 的 API URL。
<<< END U013175 >>>
<<< UNIT U013176 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:34-34 | ctx=wiki.help.wiki-inline.desc >>>
开启后将自动解析消息中带有 [[ ]] 或 {{ }} 的字符串并自动查询 Wiki。
<<< END U013176 >>>
<<< UNIT U013177 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:35-35 | ctx=wiki.help.wiki-inline.mediawiki >>>
在 ≺ ≻ 或 ⧼ ⧽ 内输入标题以自动查询 MediaWiki 命名空间的页面。
<<< END U013177 >>>
<<< UNIT U013178 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:36-36 | ctx=wiki.help.wiki-inline.page >>>
在 [[ ]] 内输入标题以自动查询页面。
<<< END U013178 >>>
<<< UNIT U013179 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:37-37 | ctx=wiki.help.wiki-inline.template >>>
在 {{ }} 内输入名称以查询模板。
<<< END U013179 >>>
<<< UNIT U013180 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:38-38 | ctx=wiki.help.wiki-inline.url >>>
发送 Wiki 页面的 URL 时生成 Infobox 图片。
<<< END U013180 >>>
<<< UNIT U013181 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:39-39 | ctx=wiki.message.ab.qq.slice >>>
${user} 在 ${title} 执行操作“${action}”时触发了过滤器。
过滤器描述：${filter_name}
采取的行动：${result}
<<< END U013181 >>>
<<< UNIT U013182 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:40-40 | ctx=wiki.message.ab.qq.title >>>
滥用过滤器日志
<<< END U013182 >>>
<<< UNIT U013183 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:41-41 | ctx=wiki.message.ab.slice >>>
${time} - ${user} 在 ${title} 执行操作“${action}”时触发了过滤器。
过滤器描述：${filter_name}
采取的行动：${result}
<<< END U013183 >>>
<<< UNIT U013184 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:42-42 | ctx=wiki.message.error.add >>>
发生错误：无法添加此 Wiki。
<<< END U013184 >>>
<<< UNIT U013185 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:43-43 | ctx=wiki.message.error.fetch_log >>>
发生错误：无法获取日志，可能是此 Wiki 设置了日志的查看权限。
<<< END U013185 >>>
<<< UNIT U013186 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:44-44 | ctx=wiki.message.error.info >>>
详细信息：
<<< END U013186 >>>
<<< UNIT U013187 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:45-45 | ctx=wiki.message.error.query >>>
发生错误：无法查询此 Wiki。
<<< END U013187 >>>
<<< UNIT U013188 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:46-46 | ctx=wiki.message.error.render_section >>>
发生错误：章节渲染失败，请联系开发者检查原因。
<<< END U013188 >>>
<<< UNIT U013189 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:47-47 | ctx=wiki.message.error.set >>>
发生错误：无法设置此 Wiki。
<<< END U013189 >>>
<<< UNIT U013190 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:48-48 | ctx=wiki.message.api.error >>>
Wiki API 查询失败（${code}）。
<<< END U013190 >>>
<<< UNIT U013191 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:49-49 | ctx=wiki.message.api.invalid_response >>>
Wiki API 返回了无效的数据。
<<< END U013191 >>>
<<< UNIT U013192 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:50-50 | ctx=wiki.message.revision.invalid >>>
修订号必须为正整数。
<<< END U013192 >>>
<<< UNIT U013193 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:51-51 | ctx=wiki.message.revision.unavailable >>>
无法读取指定的页面修订版本。
<<< END U013193 >>>
<<< UNIT U013194 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:52-52 | ctx=wiki.message.disambiguation.table.header >>>
可能指
<<< END U013194 >>>
<<< UNIT U013195 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:53-53 | ctx=wiki.message.flies >>>
此页面包括以下文件：
<<< END U013195 >>>
<<< UNIT U013196 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:54-54 | ctx=wiki.message.forum.prompt >>>
此页面为论坛页，以下是当前活跃的帖子：
<<< END U013196 >>>
<<< UNIT U013197 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:55-55 | ctx=wiki.message.headers.add.failed >>>
更新请求标头失败，请检查输入。
<<< END U013197 >>>
<<< UNIT U013198 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:56-56 | ctx=wiki.message.headers.add.success >>>
已更新请求时所使用的请求标头：${headers}
<<< END U013198 >>>
<<< UNIT U013199 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:57-57 | ctx=wiki.message.headers.reset.success >>>
已重置请求时所使用的请求标头。
<<< END U013199 >>>
<<< UNIT U013200 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:58-58 | ctx=wiki.message.headers.show >>>
当前设置了以下请求标头：
${headers}
如需自定义，请使用“${cmd}”。
示例：
${prefix}wiki headers add {"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
<<< END U013200 >>>
<<< UNIT U013201 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:59-59 | ctx=wiki.message.id.invalid >>>
页面 ID 必须为数字。
<<< END U013201 >>>
<<< UNIT U013202 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:60-60 | ctx=wiki.message.id.not_found >>>
未找到页面 ID 为 ${id} 的页面。
<<< END U013202 >>>
<<< UNIT U013203 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:61-61 | ctx=wiki.message.invalid_namespace >>>
此 Wiki 上没有名为 ${namespace} 的命名空间，请检查输入。
<<< END U013203 >>>
<<< UNIT U013204 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:62-62 | ctx=wiki.message.invalid_section >>>
（此章节不存在）
<<< END U013204 >>>
<<< UNIT U013205 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:63-63 | ctx=wiki.message.invalid_section.prompt >>>
此章节不存在，以下是可能的章节：
<<< END U013205 >>>
<<< UNIT U013206 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:64-64 | ctx=wiki.message.invalid_section.select >>>
回复编号以选中对应的章节。
<<< END U013206 >>>
<<< UNIT U013207 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:65-65 | ctx=wiki.message.invalid_section.select.button >>>
点击按钮以选中对应的章节。
<<< END U013207 >>>
<<< UNIT U013208 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:66-66 | ctx=wiki.message.invalid_section.select.button.limit >>>
由于限制，超过 50 的章节无法显示按钮，请手动回复以选择章节。
<<< END U013208 >>>
<<< UNIT U013209 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:67-67 | ctx=wiki.message.invalid.blocked >>>
失败：该 Wiki 处于阻止列表中。
<<< END U013209 >>>
<<< UNIT U013210 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:68-68 | ctx=wiki.message.iw.add.success >>>
已添加自定义 InterWiki：
${iw} -> ${name}
<<< END U013210 >>>
<<< UNIT U013211 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:69-69 | ctx=wiki.message.iw.get.not_found >>>
未找到 InterWiki：${iw}
<<< END U013211 >>>
<<< UNIT U013212 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:70-70 | ctx=wiki.message.iw.list >>>
使用“${cmd}<InterWiki>”可以获取 InterWiki 对应的链接。
<<< END U013212 >>>
<<< UNIT U013213 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:71-71 | ctx=wiki.message.iw.list.legacy >>>
当前设置了以下 InterWiki：
<<< END U013213 >>>
<<< UNIT U013214 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:72-72 | ctx=wiki.message.iw.list.none >>>
当前没有设置任何 InterWiki，可使用“${cmd}”添加。
<<< END U013214 >>>
<<< UNIT U013215 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:73-73 | ctx=wiki.message.iw.list.prompt >>>
此处展示的是为机器人设置的自定义 InterWiki，如需查看默认 Wiki 的 InterWiki，请见：${url}
<<< END U013215 >>>
<<< UNIT U013216 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:74-74 | ctx=wiki.message.iw.remove.success >>>
已删除自定义 InterWiki：${iw}
<<< END U013216 >>>
<<< UNIT U013217 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:75-75 | ctx=wiki.message.not_found >>>
未找到 [${title}]。
<<< END U013217 >>>
<<< UNIT U013218 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:76-76 | ctx=wiki.message.not_found.autofix >>>
提示：[${title}] 不存在，你可能要找的是：[${redirected_title}]。
<<< END U013218 >>>
<<< UNIT U013219 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:77-77 | ctx=wiki.message.not_found.autofix.choice >>>
提示：[${title}] 不存在，你要找的是否是：
<<< END U013219 >>>
<<< UNIT U013220 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:78-78 | ctx=wiki.message.not_found.autofix.choice.prompt >>>
请直接发送指定编号获取对应内容，若回复“是”，则默认选择 ${number} 号内容，发送其他内容则代表取消操作。
<<< END U013220 >>>
<<< UNIT U013221 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:79-79 | ctx=wiki.message.not_found.autofix.choice.prompt.button >>>
请点击下方可能的页面来获取对应内容。
<<< END U013221 >>>
<<< UNIT U013222 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:80-80 | ctx=wiki.message.not_found.autofix.confirm >>>
提示：[${title}] 不存在，你是否要找 [${redirected_title}]？
<<< END U013222 >>>
<<< UNIT U013223 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:81-81 | ctx=wiki.message.not_set >>>
未设置默认 Wiki。
<<< END U013223 >>>
<<< UNIT U013224 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:82-82 | ctx=wiki.message.ntqq.forward.sending >>>
合并转发消息构造中，请耐心等待……
<<< END U013224 >>>
<<< UNIT U013225 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:83-83 | ctx=wiki.message.ntqq.forward.timeout >>>
若长时间未发送消息，请尝试使用“--legacy”选项重新获取。
<<< END U013225 >>>
<<< UNIT U013226 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:84-84 | ctx=wiki.message.prefix.reset.success >>>
已重置请求时所使用的前缀。
<<< END U013226 >>>
<<< UNIT U013227 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:85-85 | ctx=wiki.message.prefix.set.success >>>
已更新请求时所使用的前缀：${wiki_prefix}
<<< END U013227 >>>
<<< UNIT U013228 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:86-86 | ctx=wiki.message.rc.action.abusefilter.create >>>
${user} 建立了 ${title}
<<< END U013228 >>>
<<< UNIT U013229 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:87-87 | ctx=wiki.message.rc.action.abusefilter.modify >>>
${user} 修改了 ${title}
<<< END U013229 >>>
<<< UNIT U013230 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:88-88 | ctx=wiki.message.rc.action.actionhidden >>>
${user}（日志详情已移除）${title}
<<< END U013230 >>>
<<< UNIT U013231 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:89-89 | ctx=wiki.message.rc.action.block >>>
${user} 封禁了 ${title}
<<< END U013231 >>>
<<< UNIT U013232 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:90-90 | ctx=wiki.message.rc.action.block.reblock >>>
${user} 更改了 ${title} 的封禁设置
<<< END U013232 >>>
<<< UNIT U013233 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:91-91 | ctx=wiki.message.rc.action.block.unblock >>>
${user} 解封了 ${title}
<<< END U013233 >>>
<<< UNIT U013234 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:92-92 | ctx=wiki.message.rc.action.contentmodel.change >>>
${user} 更改了页面 ${title} 的页面模型
<<< END U013234 >>>
<<< UNIT U013235 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:93-93 | ctx=wiki.message.rc.action.contentmodel.new >>>
${user} 已使用非默认页面模型创建了页面 ${title}
<<< END U013235 >>>
<<< UNIT U013236 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:94-94 | ctx=wiki.message.rc.action.create >>>
${user} 创建了页面 ${title}
<<< END U013236 >>>
<<< UNIT U013237 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:95-95 | ctx=wiki.message.rc.action.delete >>>
${user} 删除了页面 ${title}
<<< END U013237 >>>
<<< UNIT U013238 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:96-96 | ctx=wiki.message.rc.action.delete.delete_redir >>>
${user} 通过覆盖删除了重定向 ${title}
<<< END U013238 >>>
<<< UNIT U013239 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:97-97 | ctx=wiki.message.rc.action.delete.event >>>
${user} 更改了 ${title} 日志事件的可见性
<<< END U013239 >>>
<<< UNIT U013240 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:98-98 | ctx=wiki.message.rc.action.delete.restore >>>
${user} 还原了页面 ${title}
<<< END U013240 >>>
<<< UNIT U013241 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:99-99 | ctx=wiki.message.rc.action.delete.revision >>>
${user} 更改了页面 ${title} 中修订版本的可见性
<<< END U013241 >>>
<<< UNIT U013242 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:100-100 | ctx=wiki.message.rc.action.import >>>
${user} 通过跨 Wiki 导入了 ${title}
<<< END U013242 >>>
<<< UNIT U013243 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:101-101 | ctx=wiki.message.rc.action.import.upload >>>
${user} 通过文件上传导入了 ${title}
<<< END U013243 >>>
<<< UNIT U013244 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:102-102 | ctx=wiki.message.rc.action.managetags.activate >>>
${user} 激活了标签
<<< END U013244 >>>
<<< UNIT U013245 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:103-103 | ctx=wiki.message.rc.action.managetags.create >>>
${user} 创建了标签
<<< END U013245 >>>
<<< UNIT U013246 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:104-104 | ctx=wiki.message.rc.action.managetags.deactivate >>>
${user} 停用了标签
<<< END U013246 >>>
<<< UNIT U013247 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:105-105 | ctx=wiki.message.rc.action.managetags.delete >>>
${user} 删除了标签
<<< END U013247 >>>
<<< UNIT U013248 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:106-106 | ctx=wiki.message.rc.action.merge >>>
${user} 合并了 ${title}
<<< END U013248 >>>
<<< UNIT U013249 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:107-107 | ctx=wiki.message.rc.action.move >>>
${user} 移动了页面 ${title}
<<< END U013249 >>>
<<< UNIT U013250 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:108-108 | ctx=wiki.message.rc.action.move.move_redir >>>
${user} 移动了页面 ${title} 并覆盖重定向
<<< END U013250 >>>
<<< UNIT U013251 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:109-109 | ctx=wiki.message.rc.action.newusers.autocreate >>>
自动创建了用户 ${title}
<<< END U013251 >>>
<<< UNIT U013252 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:110-110 | ctx=wiki.message.rc.action.newusers.byemail >>>
${user} 创建了用户 ${title}，并且密码已通过电子邮件发送
<<< END U013252 >>>
<<< UNIT U013253 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:111-111 | ctx=wiki.message.rc.action.newusers.create >>>
用户 ${title} 已创建
<<< END U013253 >>>
<<< UNIT U013254 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:112-112 | ctx=wiki.message.rc.action.newusers.create2 >>>
${user} 创建了用户 ${title}
<<< END U013254 >>>
<<< UNIT U013255 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:113-113 | ctx=wiki.message.rc.action.protect >>>
${user} 保护了 ${title}
<<< END U013255 >>>
<<< UNIT U013256 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:114-114 | ctx=wiki.message.rc.action.protect.modify >>>
${user} 更改了 ${title} 的保护设置
<<< END U013256 >>>
<<< UNIT U013257 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:115-115 | ctx=wiki.message.rc.action.protect.move_prot >>>
${user} 移动了 ${title} 的保护设置
<<< END U013257 >>>
<<< UNIT U013258 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:116-116 | ctx=wiki.message.rc.action.protect.unprotect >>>
${user} 移除了 ${title} 的保护
<<< END U013258 >>>
<<< UNIT U013259 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:117-117 | ctx=wiki.message.rc.action.rights >>>
${user} 更改了 ${title} 的用户组
<<< END U013259 >>>
<<< UNIT U013260 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:118-118 | ctx=wiki.message.rc.action.upload >>>
${user} 上传了 ${title}
<<< END U013260 >>>
<<< UNIT U013261 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:119-119 | ctx=wiki.message.rc.action.upload.overwrite >>>
${user} 上传了 ${title} 的新版本
<<< END U013261 >>>
<<< UNIT U013262 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:120-120 | ctx=wiki.message.rc.action.upload.revent >>>
${user} 已恢复 ${title} 至旧版本
<<< END U013262 >>>
<<< UNIT U013263 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:121-121 | ctx=wiki.message.rc.new_redirect >>>
新重定向
<<< END U013263 >>>
<<< UNIT U013264 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:122-122 | ctx=wiki.message.rc.params.duration >>>
封禁时长：
<<< END U013264 >>>
<<< UNIT U013265 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:123-123 | ctx=wiki.message.rc.params.suppress_redirect >>>
（不留重定向）
<<< END U013265 >>>
<<< UNIT U013266 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:124-124 | ctx=wiki.message.rc.params.tag >>>
标签：
<<< END U013266 >>>
<<< UNIT U013267 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:125-125 | ctx=wiki.message.rc.params.target_title >>>
目标标题：
<<< END U013267 >>>
<<< UNIT U013268 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:126-126 | ctx=wiki.message.rc.qq.link.prompt >>>
提示：将下面的任一消息复制粘贴到聊天窗口后发送，即可获取此次更改详细信息的截图。
<<< END U013268 >>>
<<< UNIT U013269 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:127-127 | ctx=wiki.message.rc.qq.title >>>
最近更改日志
<<< END U013269 >>>
<<< UNIT U013270 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:128-128 | ctx=wiki.message.redirect >>>
（重定向 [${title}] -> [${redirected_title}]）
<<< END U013270 >>>
<<< UNIT U013271 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:129-129 | ctx=wiki.message.redirect.autofix >>>
（已指定 [${title}] 更正为 [${redirected_title}]。）
<<< END U013271 >>>
<<< UNIT U013272 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:130-130 | ctx=wiki.message.redirect.template_to_page >>>
（[${title}] 尚未创建，已自动重定向至 [${redirected_title}]）
<<< END U013272 >>>
<<< UNIT U013273 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:131-131 | ctx=wiki.message.render.action.button >>>
渲染预览图
<<< END U013273 >>>
<<< UNIT U013274 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:134-134 | ctx=wiki.message.render.button >>>
已切换为消息展示按钮。
<<< END U013274 >>>
<<< UNIT U013275 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:135-135 | ctx=wiki.message.render.auto >>>
已切换为自动渲染 Wiki 页面。
<<< END U013275 >>>
<<< UNIT U013276 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:136-136 | ctx=wiki.message.render.off >>>
已关闭 Wiki 页面渲染。
<<< END U013276 >>>
<<< UNIT U013277 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:137-137 | ctx=wiki.message.render.invalid >>>
无效的渲染方式，请使用 button、auto 或 off。
<<< END U013277 >>>
<<< UNIT U013278 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:138-138 | ctx=wiki.message.style.invalid >>>
无效的消息样式，请使用 text 或 card。
<<< END U013278 >>>
<<< UNIT U013279 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:139-139 | ctx=wiki.message.style.text >>>
已切换为文字消息样式。
<<< END U013279 >>>
<<< UNIT U013280 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:140-140 | ctx=wiki.message.style.card >>>
已切换为卡片消息样式。卡片消息不支持按钮，button 预览模式将改用 auto（自动渲染）模式。
<<< END U013280 >>>
<<< UNIT U013281 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:141-141 | ctx=wiki.message.redlink.disable >>>
已关闭页面不存在时返回编辑链接。
<<< END U013281 >>>
<<< UNIT U013282 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:142-142 | ctx=wiki.message.redlink.enable >>>
已开启页面不存在时返回编辑链接。
<<< END U013282 >>>
<<< UNIT U013283 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:143-143 | ctx=wiki.message.redlink.not_found >>>
（页面不存在）
<<< END U013283 >>>
<<< UNIT U013284 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:144-144 | ctx=wiki.message.redlink.not_found.uneditable >>>
[${title}] 页面不存在。
<<< END U013284 >>>
<<< UNIT U013285 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:145-145 | ctx=wiki.message.rollback >>>
无法发送合并转发消息，已自动回退至传统样式。
<<< END U013285 >>>
<<< UNIT U013286 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:146-146 | ctx=wiki.message.search >>>
搜索结果：
<<< END U013286 >>>
<<< UNIT U013287 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:147-147 | ctx=wiki.message.search.not_found >>>
未找到结果。
<<< END U013287 >>>
<<< UNIT U013288 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:148-148 | ctx=wiki.message.search.prompt >>>
回复编号以查询对应的页面。
<<< END U013288 >>>
<<< UNIT U013289 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:149-149 | ctx=wiki.message.search.prompt.button >>>
点击按钮以查询对应的页面。
<<< END U013289 >>>
<<< UNIT U013290 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:150-150 | ctx=wiki.message.search.more >>>
更多结果：${url}
<<< END U013290 >>>
<<< UNIT U013291 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:151-151 | ctx=wiki.message.section.rendering >>>
（章节渲染中……）
<<< END U013291 >>>
<<< UNIT U013292 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:152-152 | ctx=wiki.message.set.not_set >>>
没有设置默认 Wiki，使用“${cmd}”设置默认 Wiki。
<<< END U013292 >>>
<<< UNIT U013293 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:153-153 | ctx=wiki.message.set.not_set.recommend >>>
点击下方按钮，设置推荐的 Wiki。
<<< END U013293 >>>
<<< UNIT U013294 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:154-154 | ctx=wiki.message.set.success >>>
成功设置默认 Wiki：${name}
<<< END U013294 >>>
<<< UNIT U013295 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:155-155 | ctx=wiki.message.table.header.id >>>
编号
<<< END U013295 >>>
<<< UNIT U013296 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:156-156 | ctx=wiki.message.table.header.section >>>
章节
<<< END U013296 >>>
<<< UNIT U013297 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:157-157 | ctx=wiki.message.talk_page.prompt >>>
此页面为讨论页，以下是所有的章节：
<<< END U013297 >>>
<<< UNIT U013298 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:158-158 | ctx=wiki.message.user.blocked >>>
${user} 正在被封禁中！
<<< END U013298 >>>
<<< UNIT U013299 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:159-159 | ctx=wiki.message.user.blocked.detail >>>
被 ${blocked_by} 封禁，时间从 ${blocked_time} 到 ${blocked_expires}
<<< END U013299 >>>
<<< UNIT U013300 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:160-160 | ctx=wiki.message.user.blocked.reason >>>
理由：
<<< END U013300 >>>
<<< UNIT U013301 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:161-161 | ctx=wiki.message.user.created_page_count >>>
创建数：
<<< END U013301 >>>
<<< UNIT U013302 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:162-162 | ctx=wiki.message.user.deleted_count >>>
删除数：
<<< END U013302 >>>
<<< UNIT U013303 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:163-163 | ctx=wiki.message.user.edited_count >>>
编辑数：
<<< END U013303 >>>
<<< UNIT U013304 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:164-164 | ctx=wiki.message.user.edited_wiki_count >>>
编辑过的 Wiki：
<<< END U013304 >>>
<<< UNIT U013305 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:165-165 | ctx=wiki.message.user.friends_count >>>
好友数：
<<< END U013305 >>>
<<< UNIT U013306 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:166-166 | ctx=wiki.message.user.gender >>>
性别：
<<< END U013306 >>>
<<< UNIT U013307 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:167-167 | ctx=wiki.message.user.gender.female >>>
女
<<< END U013307 >>>
<<< UNIT U013308 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:168-168 | ctx=wiki.message.user.gender.male >>>
男
<<< END U013308 >>>
<<< UNIT U013309 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:169-169 | ctx=wiki.message.user.global_edited_count >>>
全域编辑数：
<<< END U013309 >>>
<<< UNIT U013310 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:170-170 | ctx=wiki.message.user.global_home >>>
注册 Wiki：
<<< END U013310 >>>
<<< UNIT U013311 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:171-171 | ctx=wiki.message.user.global_rank >>>
全站排名：
<<< END U013311 >>>
<<< UNIT U013312 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:172-172 | ctx=wiki.message.user.global_users_groups >>>
全域用户组：
<<< END U013312 >>>
<<< UNIT U013313 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:173-173 | ctx=wiki.message.user.not_found >>>
未找到用户。
<<< END U013313 >>>
<<< UNIT U013314 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:174-174 | ctx=wiki.message.user.patrolled_count >>>
巡查数：
<<< END U013314 >>>
<<< UNIT U013315 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:175-175 | ctx=wiki.message.user.registration_time >>>
注册时间：
<<< END U013315 >>>
<<< UNIT U013316 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:176-176 | ctx=wiki.message.user.site_rank >>>
本站排名：
<<< END U013316 >>>
<<< UNIT U013317 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:177-177 | ctx=wiki.message.user.username >>>
用户：
<<< END U013317 >>>
<<< UNIT U013318 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:178-178 | ctx=wiki.message.user.users_groups >>>
用户组：
<<< END U013318 >>>
<<< UNIT U013319 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:179-179 | ctx=wiki.message.user.wiki_unavailable >>>
${wikiurl} 不可用。
<<< END U013319 >>>
<<< UNIT U013320 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:180-180 | ctx=wiki.message.utils.redacted >>>
检测到特定内容，请前往日志查看完整消息。
<<< END U013320 >>>
<<< UNIT U013321 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:181-181 | ctx=wiki.message.utils.wikilib.error.empty >>>
发生错误：API 未返回任何内容，请联系此站点管理员获取原因。
<<< END U013321 >>>
<<< UNIT U013322 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:182-182 | ctx=wiki.message.utils.wikilib.error.text_too_long >>>
发生错误：请求的页面段落文本过长，无法显示。
<<< END U013322 >>>
<<< UNIT U013323 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:183-183 | ctx=wiki.message.utils.wikilib.get_failed.api >>>
从 API 获取信息时出错：
<<< END U013323 >>>
<<< UNIT U013324 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:184-184 | ctx=wiki.message.utils.wikilib.get_failed.cloudflare >>>
CloudFlare 拦截了机器人的请求，请联系站点管理员解决此问题。
<<< END U013324 >>>
<<< UNIT U013325 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:185-185 | ctx=wiki.message.utils.wikilib.get_failed.forbidden >>>
服务器拒绝了机器人的请求。
<<< END U013325 >>>
<<< UNIT U013326 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:186-186 | ctx=wiki.message.utils.wikilib.get_failed.invalid_interwiki >>>
站点设置的 InterWiki 无效，请联系站点管理员解决此问题。
<<< END U013326 >>>
<<< UNIT U013327 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:187-187 | ctx=wiki.message.utils.wikilib.get_failed.may_not_mediawiki >>>
此站点也许不是一个有效的 MediaWiki（或自动嗅探 API 链接被网站防火墙拦截。请尝试手动设置 API 端点地址，或联系站点管理员对机器人流量特征放行）：
<<< END U013327 >>>
<<< UNIT U013328 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:188-188 | ctx=wiki.message.utils.wikilib.get_failed.moegirl >>>
萌娘百科的 API 接口不稳定，请稍后再试或直接访问站点。
<<< END U013328 >>>
<<< UNIT U013329 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:189-189 | ctx=wiki.message.utils.wikilib.get_failed.no_http_or_https_headers >>>
所给的链接没有指明协议头（链接应以“http://”或“https://”开头）。
<<< END U013329 >>>
<<< UNIT U013330 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:190-190 | ctx=wiki.message.utils.wikilib.get_failed.not_mediawiki >>>
此站点不是一个有效的 MediaWiki（或自动嗅探 API 链接被网站防火墙拦截。请尝试手动设置 API 端点地址，或联系站点管理员对机器人流量特征放行）。
<<< END U013330 >>>
<<< UNIT U013331 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:191-191 | ctx=wiki.message.utils.wikilib.get_failed.timeout >>>
建立连接超时。
<<< END U013331 >>>
<<< UNIT U013332 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:192-192 | ctx=wiki.message.utils.wikilib.get_failed.wikimedia >>>
根据维基媒体基金会政策，需要设置一个合适的 User-Agent 请求头。
<<< END U013332 >>>
<<< UNIT U013333 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:193-193 | ctx=wiki.message.utils.wikilib.invalid.empty_title >>>
请求的页面标题为空，或只包含命名空间名称。
<<< END U013333 >>>
<<< UNIT U013334 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:194-194 | ctx=wiki.message.utils.wikilib.invalid.invalid_character >>>
请求的页面标题包含无效字符：“${char}”。
<<< END U013334 >>>
<<< UNIT U013335 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:195-195 | ctx=wiki.message.utils.wikilib.no_textextracts >>>
提示：此 Wiki 没有开启 TextExtracts 扩展。摘要由机器人离线解析页面源代码生成，可能与页面实际渲染的内容存在出入，部分页面可能没有摘要。
<<< END U013335 >>>
<<< UNIT U013336 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:196-196 | ctx=wiki.message.url_policy.untrust >>>
注意：此 Wiki 的 API 端点当前没有加入机器人的全局 URL 允许列表，查询此 Wiki 时将会对返回内容进行限制。
<<< END U013336 >>>
<<< UNIT U013337 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:197-197 | ctx=wiki.message.url_policy.untrust.address >>>
如需取消限制，请在此处申请加入全局 URL 允许列表：${url}
<<< END U013337 >>>
<<< UNIT U013338 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:198-198 | ctx=wiki.message.wiki-bot.login.already >>>
登录失败：机器人账户已存在，请先登出账户。
<<< END U013338 >>>
<<< UNIT U013339 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:199-199 | ctx=wiki.message.wiki-bot.login.failed >>>
登录失败：
${detail}
<<< END U013339 >>>
<<< UNIT U013340 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:200-200 | ctx=wiki.message.wiki-bot.login.success >>>
登录成功。
<<< END U013340 >>>
<<< UNIT U013341 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:201-201 | ctx=wiki.message.wiki-bot.toggle.disable >>>
已关闭使用机器人账户。
<<< END U013341 >>>
<<< UNIT U013342 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:202-202 | ctx=wiki.message.wiki-bot.toggle.enable >>>
已开启使用机器人账户。
<<< END U013342 >>>
<<< UNIT U013343 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:203-203 | ctx=wiki.message.diff.heading >>>
版本差异
<<< END U013343 >>>
<<< UNIT U013344 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:204-204 | ctx=wiki.message.diff.revision >>>
版本 ${revision}
<<< END U013344 >>>
<<< UNIT U013345 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:205-205 | ctx=wiki.message.diff.summary >>>
${title}：版本 ${old} → ${new}
<<< END U013345 >>>
<<< UNIT U013346 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:206-206 | ctx=wiki.message.diff.empty >>>
这两个版本之间没有内容差异。
<<< END U013346 >>>
<<< UNIT U013347 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:207-207 | ctx=wiki.message.diff.invalid >>>
差异参数无效，请使用 Special:Diff/版本号、Special:Diff/旧版本号/新版本号，或 diff 与 oldid 参数。
<<< END U013347 >>>
<<< UNIT U013348 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:208-208 | ctx=wiki.message.diff.unavailable >>>
无法获取版本差异，版本可能不存在、已被隐藏，或站点不支持差异查询。
<<< END U013348 >>>
<<< UNIT U013349 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:209-209 | ctx=wiki.message.wiki-inline.flies >>>
此页面包括以下文件：
${file}
<<< END U013349 >>>
<<< UNIT U013350 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:210-210 | ctx=wiki.message.wiki-inline.detected.page >>>
检测到条目：${title}
<<< END U013350 >>>
<<< UNIT U013351 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:211-211 | ctx=wiki.message.wiki-inline.detected.section >>>
检测到段落：${title}
<<< END U013351 >>>
<<< UNIT U013352 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:212-212 | ctx=wiki.help.magic >>>
查询目标 Wiki 注册的魔术字与扩展解析函数，返回短文本或查询链接。支持 #expr、字符串处理及站点变量。
<<< END U013352 >>>
<<< UNIT U013353 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:213-213 | ctx=wiki.help.magic.option.p >>>
指定魔术字的页面上下文。含空格的标题用引号包裹。
<<< END U013353 >>>
<<< UNIT U013354 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:214-214 | ctx=wiki.message.magic.invalid >>>
请输入一个完整的魔术字表达式。
<<< END U013354 >>>
<<< UNIT U013355 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:215-215 | ctx=wiki.message.magic.unsupported >>>
此表达式包含未支持的魔术字或模板展开。
<<< END U013355 >>>
<<< UNIT U013356 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:216-216 | ctx=wiki.message.magic.input_long >>>
表达式过长或嵌套过多，请简化后查询。
<<< END U013356 >>>
<<< UNIT U013357 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:217-217 | ctx=wiki.message.magic.page_required >>>
此表达式需要页面上下文，请使用 wiki magic <表达式> -p <页面>。
<<< END U013357 >>>
<<< UNIT U013358 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:218-218 | ctx=wiki.message.magic.context_failed >>>
Wiki 无法按指定的上下文展开此表达式。
<<< END U013358 >>>
<<< UNIT U013359 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:219-219 | ctx=wiki.message.magic.output_long >>>
结果过长，请简化表达式。
<<< END U013359 >>>
<<< UNIT U013360 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:220-220 | ctx=wiki.message.magic.output_long.confirm >>>
展开内容过长，是否展示？
<<< END U013360 >>>
<<< UNIT U013361 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:221-221 | ctx=wiki.message.magic.output_long_unavailable >>>
无法生成展开结果图片，请简化表达式。
<<< END U013361 >>>
<<< UNIT U013362 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:222-222 | ctx=wiki.message.magic.evaluation_failed >>>
魔术字求值失败，请检查参数。
<<< END U013362 >>>
<<< UNIT U013363 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:223-223 | ctx=wiki.message.magic.not_plain >>>
此表达式未返回可直接显示的短结果。
<<< END U013363 >>>
<<< UNIT U013364 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:224-224 | ctx=wiki.message.magic.read_only_url >>>
仅支持生成查询页面的链接。
<<< END U013364 >>>
<<< UNIT U013365 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:225-225 | ctx=wiki.message.magic.unavailable >>>
暂时无法查询此 Wiki 的魔术字，请稍后再试。
<<< END U013365 >>>
<<< UNIT U013366 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:226-226 | ctx=wiki.message.magic.filtered >>>
此结果无法显示。
<<< END U013366 >>>
<<< UNIT U013367 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:227-227 | ctx=wiki.message.magic.empty >>>
此表达式的结果为空。
<<< END U013367 >>>
<<< UNIT U013368 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:228-228 | ctx=wiki.message.template_preview.button >>>
预览效果
<<< END U013368 >>>
<<< UNIT U013369 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:229-229 | ctx=wiki.message.template_preview.button_named >>>
预览效果 · ${title}
<<< END U013369 >>>
<<< UNIT U013370 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:230-230 | ctx=wiki.message.template_preview.heading >>>
机器人预览
<<< END U013370 >>>
<<< UNIT U013371 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:231-231 | ctx=wiki.message.template_preview.declaration >>>
机器人自动预览 · 非 Wiki 发布内容
<<< END U013371 >>>
<<< UNIT U013372 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:233-233 | ctx=wiki.message.template_preview.watermark >>>
Generated by AkariBot: ${title}${status} - 非 Wiki 内容，请注意甄别信息
<<< END U013372 >>>
<<< UNIT U013373 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:234-234 | ctx=wiki.message.template_preview.css.title >>>
样式属性
<<< END U013373 >>>
<<< UNIT U013374 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:235-235 | ctx=wiki.message.template_preview.css.element >>>
顶层元素
<<< END U013374 >>>
<<< UNIT U013375 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:236-236 | ctx=wiki.message.template_preview.css.display >>>
布局类型
<<< END U013375 >>>
<<< UNIT U013376 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:237-237 | ctx=wiki.message.template_preview.css.float >>>
浮动方式
<<< END U013376 >>>
<<< UNIT U013377 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:238-238 | ctx=wiki.message.template_preview.css.position >>>
定位方式
<<< END U013377 >>>
<<< UNIT U013378 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:239-239 | ctx=wiki.message.template_preview.css.flex_direction >>>
排列方向
<<< END U013378 >>>
<<< UNIT U013379 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:240-240 | ctx=wiki.message.template_preview.css.flex_wrap >>>
换行方式
<<< END U013379 >>>
<<< UNIT U013380 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:241-241 | ctx=wiki.message.template_preview.css.grid_columns >>>
网格列
<<< END U013380 >>>
<<< UNIT U013381 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:242-242 | ctx=wiki.message.template_preview.css.grid_rows >>>
网格行
<<< END U013381 >>>
<<< UNIT U013382 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:243-243 | ctx=wiki.message.template_preview.css.grid_auto_flow >>>
填充方向
<<< END U013382 >>>
<<< UNIT U013383 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:244-244 | ctx=wiki.message.template_preview.css.justify >>>
内容对齐
<<< END U013383 >>>
<<< UNIT U013384 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:245-245 | ctx=wiki.message.template_preview.css.align >>>
元素对齐
<<< END U013384 >>>
<<< UNIT U013385 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:246-246 | ctx=wiki.message.template_preview.css.gap >>>
元素间距
<<< END U013385 >>>
<<< UNIT U013386 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:247-247 | ctx=wiki.message.template_preview.css.background >>>
背景
<<< END U013386 >>>
<<< UNIT U013387 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:248-248 | ctx=wiki.message.template_preview.css.color >>>
文字颜色
<<< END U013387 >>>
<<< UNIT U013388 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:249-249 | ctx=wiki.message.template_preview.css.font >>>
字体
<<< END U013388 >>>
<<< UNIT U013389 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:250-250 | ctx=wiki.message.template_preview.css.size >>>
字号/行高
<<< END U013389 >>>
<<< UNIT U013390 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:251-251 | ctx=wiki.message.template_preview.css.border >>>
边框
<<< END U013390 >>>
<<< UNIT U013391 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:252-252 | ctx=wiki.message.template_preview.css.radius >>>
圆角
<<< END U013391 >>>
<<< UNIT U013392 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:253-253 | ctx=wiki.message.template_preview.css.shadow >>>
阴影
<<< END U013392 >>>
<<< UNIT U013393 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:254-254 | ctx=wiki.message.template_preview.css.spacing >>>
内外边距
<<< END U013393 >>>
<<< UNIT U013394 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:256-256 | ctx=wiki.message.template_preview.partial >>>
部分资源未加载
<<< END U013394 >>>
<<< UNIT U013395 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:257-257 | ctx=wiki.message.template_preview.invalid >>>
模板参数格式无效、过长或嵌套过多，无法生成预览。
<<< END U013395 >>>
<<< UNIT U013396 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:258-258 | ctx=wiki.message.template_preview.filtered >>>
用户输入参数未通过文本审核，无法生成预览。
<<< END U013396 >>>
<<< UNIT U013397 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:259-259 | ctx=wiki.message.template_preview.audit_unavailable >>>
参数文本审核暂不可用，无法生成预览。
<<< END U013397 >>>
<<< UNIT U013398 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:260-260 | ctx=wiki.message.template_preview.not_allowed >>>
该 Wiki 当前不在白名单内，无法生成预览。
<<< END U013398 >>>
<<< UNIT U013399 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:261-261 | ctx=wiki.message.template_preview.missing >>>
模板不存在或目标已变更，请重新查询。
<<< END U013399 >>>
<<< UNIT U013400 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:262-262 | ctx=wiki.message.template_preview.empty >>>
模板未返回可渲染内容。
<<< END U013400 >>>
<<< UNIT U013401 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:263-263 | ctx=wiki.message.template_preview.too_large >>>
模板预览内容过大，请减少参数内容后重试。
<<< END U013401 >>>
<<< UNIT U013402 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:264-264 | ctx=wiki.message.template_preview.unavailable >>>
暂时无法渲染模板效果，请稍后重新查询。
<<< END U013402 >>>
<<< UNIT U013403 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:265-265 | ctx=wiki.message.template_preview.timeout >>>
模板预览超时，请稍后重新查询。
<<< END U013403 >>>
<<< UNIT U013404 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:266-266 | ctx=wiki.message.template_preview.expired >>>
此预览按钮已过期，请重新查询。
<<< END U013404 >>>
<<< UNIT U013405 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:267-267 | ctx=wiki.message.template_preview.busy >>>
你已有一个模板预览正在生成，请等待完成。
<<< END U013405 >>>
<<< UNIT U013406 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:268-268 | ctx=wiki.message.too_many_redirects >>>
重定向的次数过多，无法解析。
<<< END U013406 >>>
<<< UNIT U013407 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:269-269 | ctx=wikilog.message.config.wiki.success >>>
成功操作 Wiki：${wiki}
<<< END U013407 >>>
<<< UNIT U013408 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:270-270 | ctx=wikilog.message.config.wiki.failed >>>
操作 Wiki 失败，请检查 URL 是否正确：${message}
<<< END U013408 >>>
<<< UNIT U013409 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:271-271 | ctx=wikilog.message.enable.log.success >>>
成功操作了 ${wiki} ${logtype} 的监控设置。
<<< END U013409 >>>
<<< UNIT U013410 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:272-272 | ctx=wikilog.message.enable.log.failed >>>
为 ${apilink} 操作 ${logtype} 失败，请检查此 Wiki 是否已添加进监控列表，以及站点状态是否正常。
<<< END U013410 >>>
<<< UNIT U013411 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:273-273 | ctx=wikilog.message.enable.log.invalid_logtype >>>
无效的 ${logtype}。
<<< END U013411 >>>
<<< UNIT U013412 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:274-274 | ctx=wikilog.message.filter.test.success >>>
成功在 ${start}, ${end} 处匹配了文本：${string}
<<< END U013412 >>>
<<< UNIT U013413 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:275-275 | ctx=wikilog.message.filter.test.failed >>>
文本匹配失败，请检查表达式是否正确。
<<< END U013413 >>>
<<< UNIT U013414 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:276-276 | ctx=wikilog.message.filter.example.invalid >>>
无效的样本，请检查样本是否符合 JSON 格式（例如括号是否闭合、结尾处不能有逗号等）。
<<< END U013414 >>>
<<< UNIT U013415 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:277-277 | ctx=wikilog.message.filter.set.success >>>
成功为 ${wiki} ${logtype} 设置了以下过滤器：
${filters}
<<< END U013415 >>>
<<< UNIT U013416 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:278-278 | ctx=wikilog.message.filter.set.failed >>>
操作失败，请检查此 Wiki 是否已被添加进列表。
<<< END U013416 >>>
<<< UNIT U013417 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:279-279 | ctx=wikilog.message.filter.set.no_filter >>>
设置的对象为空，请检查。
<<< END U013417 >>>
<<< UNIT U013418 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:280-280 | ctx=wikilog.message.rcshow.invalid >>>
无效的筛选条件，请检查：${rcshow}
<<< END U013418 >>>
<<< UNIT U013419 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:281-281 | ctx=wikilog.message.rcshow.set.success >>>
成功为 ${wiki} 最近更改监控设置了以下筛选条件：
${rcshows}
<<< END U013419 >>>
<<< UNIT U013420 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:282-282 | ctx=wikilog.message.list.abuselog >>>
滥用过滤器日志：
<<< END U013420 >>>
<<< UNIT U013421 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:283-283 | ctx=wikilog.message.enabled >>>
已启用
<<< END U013421 >>>
<<< UNIT U013422 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:284-284 | ctx=wikilog.message.disabled >>>
已禁用
<<< END U013422 >>>
<<< UNIT U013423 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:285-285 | ctx=wikilog.message.filters >>>
条件过滤器：
<<< END U013423 >>>
<<< UNIT U013424 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:286-286 | ctx=wikilog.message.recentchanges >>>
最近更改：
<<< END U013424 >>>
<<< UNIT U013425 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:287-287 | ctx=wikilog.message.rcshow >>>
筛选条件：
<<< END U013425 >>>
<<< UNIT U013426 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:288-288 | ctx=wikilog.message.usebot >>>
使用机器人获取信息：
<<< END U013426 >>>
<<< UNIT U013427 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:289-289 | ctx=wikilog.message.user >>>
用户：
<<< END U013427 >>>
<<< UNIT U013428 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:290-290 | ctx=wikilog.message.title >>>
页面标题：
<<< END U013428 >>>
<<< UNIT U013429 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:291-291 | ctx=wikilog.help.add.wiki >>>
添加一个 Wiki 到监控列表。
<<< END U013429 >>>
<<< UNIT U013430 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:292-292 | ctx=wikilog.help.reset.wiki >>>
重置一个 Wiki 的监控列表信息。
<<< END U013430 >>>
<<< UNIT U013431 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:293-293 | ctx=wikilog.help.remove.wiki >>>
从监控列表移除一个 Wiki。
<<< END U013431 >>>
<<< UNIT U013432 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:294-294 | ctx=wikilog.help.enable.logtype >>>
启用一种类型的日志监控。
<<< END U013432 >>>
<<< UNIT U013433 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:295-295 | ctx=wikilog.help.disable.logtype >>>
禁用一种类型的日志监控。
<<< END U013433 >>>
<<< UNIT U013434 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:296-296 | ctx=wikilog.help.filter.test >>>
测试条件过滤器是否能够匹配给定的样例。
<<< END U013434 >>>
<<< UNIT U013435 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:297-297 | ctx=wikilog.help.filter.example >>>
将数据转换为可以被条件过滤器识别的样例。
<<< END U013435 >>>
<<< UNIT U013436 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:298-298 | ctx=wikilog.help.filter.set >>>
为某一类型的日志设置条件过滤器。
<<< END U013436 >>>
<<< UNIT U013437 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:299-299 | ctx=wikilog.help.filter.reset >>>
重置某一类型日志的条件过滤器。
<<< END U013437 >>>
<<< UNIT U013438 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:300-300 | ctx=wikilog.help.bot.enable >>>
启用机器人获取日志
<<< END U013438 >>>
<<< UNIT U013439 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:301-301 | ctx=wikilog.help.bot.disable >>>
禁用机器人获取日志
<<< END U013439 >>>
<<< UNIT U013440 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:302-302 | ctx=wikilog.help.rcshow.set >>>
为最近更改日志设置筛选条件。
<<< END U013440 >>>
<<< UNIT U013441 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:303-303 | ctx=wikilog.help.rcshow.reset >>>
重置最近更改日志设置的筛选条件。
<<< END U013441 >>>
<<< UNIT U013442 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:304-304 | ctx=wikilog.help.list >>>
列出所有已设置的内容。
<<< END U013442 >>>
<<< UNIT U013443 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:305-305 | ctx=wikilog.help.api.get >>>
获取指定 Wiki 的指定 API 数据链接。
<<< END U013443 >>>
<<< UNIT U013444 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:306-306 | ctx=wikilog.help.keepalive.enable >>>
启用机器人登录状态检查。
<<< END U013444 >>>
<<< UNIT U013445 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:307-307 | ctx=wikilog.help.keepalive.disable >>>
禁用机器人登录状态检查。
<<< END U013445 >>>
<<< UNIT U013446 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:308-308 | ctx=wikilog.message.untrust.wiki >>>
失败：此 Wiki 当前没有加入机器人的允许列表中。
<<< END U013446 >>>
<<< UNIT U013447 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:309-309 | ctx=wikilog.message.keepalive.logged.as >>>
[Keep alive] 以 ${name} 的身份登录：${wiki}
<<< END U013447 >>>
<<< UNIT U013448 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:310-310 | ctx=wikilog.message.keepalive.failed >>>
[Keep alive] 登录状态检查失败：${link}
<<< END U013448 >>>
<<< UNIT U013449 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:311-311 | ctx=wikilog.help.note.set >>>
设置一条 Wiki 的备注，监控消息中将用备注替换 Wiki 名称。
<<< END U013449 >>>
<<< UNIT U013450 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:312-312 | ctx=wikilog.help.note.remove >>>
移除一条 Wiki 的备注。
<<< END U013450 >>>
<<< UNIT U013451 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:313-313 | ctx=wikilog.message.note.success >>>
成功为 ${wiki} 设置了备注：${note}
<<< END U013451 >>>
<<< UNIT U013452 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:314-314 | ctx=wikilog.message.note.failed >>>
操作失败，请检查此 Wiki 是否已被添加进列表。
<<< END U013452 >>>
<<< UNIT U013453 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:315-315 | ctx=wikilog.message.note >>>
备注：
<<< END U013453 >>>
<<< UNIT U013454 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:316-316 | ctx=weekly.help >>>
获取中文 Minecraft Wiki 的每周页面。
<<< END U013454 >>>
<<< UNIT U013455 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:317-317 | ctx=weekly.help.image >>>
获取中文 Minecraft Wiki 的每周页面（图片版）。
<<< END U013455 >>>
<<< UNIT U013456 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:318-318 | ctx=weekly.help.teahouse >>>
获取茶馆周报。
<<< END U013456 >>>
<<< UNIT U013457 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:319-319 | ctx=weekly.message.prompt >>>
本周页面：${text}
<<< END U013457 >>>
<<< UNIT U013458 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:320-320 | ctx=weekly.message.expired >>>
提示：本周页面已过期，请联系中文 Minecraft Wiki 更新。
<<< END U013458 >>>
<<< UNIT U013459 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:321-321 | ctx=weekly.message.image >>>
图片：${img}
<<< END U013459 >>>
<<< UNIT U013460 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:322-322 | ctx=weekly.message.link >>>

图片：${img}

页面链接：${article}
每周页面：${link}
<<< END U013460 >>>
<<< UNIT U013461 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:323-323 | ctx=weekly_rss.help.desc >>>
开启后将订阅中文 Minecraft Wiki 的每周页面（每周一 9:00 更新）。
<<< END U013461 >>>
<<< UNIT U013462 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:324-324 | ctx=weekly_rss.help.teahouse-weekly-rss.desc >>>
开启后将订阅茶馆周报的每周页面（每周一 9:30 更新）。
<<< END U013462 >>>
<<< UNIT U013463 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:325-325 | ctx=weekly_rss.message >>>
如需获取每周页面的文字版本及链接，请使用“${prefix}weekly”。
<<< END U013463 >>>
<<< UNIT U013464 | json-value | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/locales/zh_cn.json:326-326 | ctx=weekly_rss.message.teahouse-weekly-rss >>>
如需获取每周页面的文字版本及链接，请使用“${prefix}weekly teahouse”。
<<< END U013464 >>>
<<< UNIT U013465 | cfg-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/manifest.toml:1-1 >>>
# akari-bot-module-wiki 的包清单。
<<< END U013465 >>>
<<< UNIT U013466 | cfg-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/manifest.toml:6-6 >>>
# config.py 的 on_module_config("wiki") 声明的表。
<<< END U013466 >>>
<<< UNIT U013467 | cfg-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/manifest.toml:9-9 >>>
# 本包 module() 注册的全部模块名。
<<< END U013467 >>>
<<< UNIT U013468 | cfg-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/manifest.toml:24-24 >>>
# 供 --purge-data 使用。取自 database/models.py 的 Meta.table。
<<< END U013468 >>>
<<< UNIT U013469 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/migrations/0002_union_id.py:17-21 | ctx=upgrade >>>
把场景设置表的主键列改名为 union_id。

:param ctx: 迁移上下文。
<<< END U013469 >>>
<<< UNIT U013470 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/migrations/0003_url_rules_to_global.py:24-28 | ctx=upgrade >>>
迁移旧名单并删除旧表。

:param ctx: 迁移上下文。
<<< END U013470 >>>
<<< UNIT U013471 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/migrations/__init__.py:1-1 | ctx=<module> >>>
wiki 的数据库迁移。
<<< END U013471 >>>
<<< UNIT U013472 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/diff.py:76-76 >>>
# 未指定旧版本时取相对修订 prev，由网页比较当前修订与它前一个修订。
<<< END U013472 >>>
<<< UNIT U013473 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/disambiguation.py:62-62 | ctx=is_disambiguation_page >>>
判断 MediaWiki 是否把页面标记为消歧义页。
<<< END U013473 >>>
<<< UNIT U013474 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/disambiguation.py:183-183 | ctx=parse_disambiguation_html >>>
解析 MediaWiki 渲染正文，并保留同站内部链接的页面目标。
<<< END U013474 >>>
<<< UNIT U013475 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/forum.py:1-1 | ctx=<module> >>>
Wiki 讨论页列表的消息渲染工具。
<<< END U013475 >>>
<<< UNIT U013476 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/forum.py:11-11 | ctx=build_markdown_choice_table >>>
将 Wiki 选择项渲染为可点击的 Markdown 表格。
<<< END U013476 >>>
<<< UNIT U013477 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/forum.py:46-46 | ctx=build_forum_markdown_table >>>
将论坛帖子列表渲染为可点击的 Markdown 表格。
<<< END U013477 >>>
<<< UNIT U013478 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/forum.py:60-60 | ctx=build_section_markdown_table >>>
将讨论页章节列表渲染为可点击的 Markdown 表格。
<<< END U013478 >>>
<<< UNIT U013479 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/magic.py:41-41 >>>
# siteinfo 不提供 SFH_NO_HASH 标志，这些核心函数的无井号语法由 MediaWiki 定义。
<<< END U013479 >>>
<<< UNIT U013480 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/magic.py:75-75 >>>
# 扩展注册信息只有名称与别名。仅启用已确认不写入 Wiki 的解析函数。
<<< END U013480 >>>
<<< UNIT U013481 | py-inline-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/mapping.py:25-25 >>>
# 萌娘百科强制使用移动版 API
<<< END U013481 >>>
<<< UNIT U013482 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/preview_render.py:234-234 >>>
# 本地应答的虚拟 URL 为站点模块提供正确 origin，不向 Wiki 创建或请求页面。
<<< END U013482 >>>
<<< UNIT U013483 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/preview_render.py:324-324 >>>
# 远程接口不支持请求路由，所有资源须先受控下载并内联，CSP 禁止后续联网。
<<< END U013483 >>>
<<< UNIT U013484 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/preview_render.py:466-466 >>>
# 替换接口插入的 script 保持惰性。仅显式执行机器人自带的初始化代码。
<<< END U013484 >>>
<<< UNIT U013485 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/recommend.py:5-5 >>>
# 未设置默认 Wiki 时向用户推荐的 Wiki，元素为（显示名称，API 端点地址）。
<<< END U013485 >>>
<<< UNIT U013486 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/screenshot_image.py:229-229 >>>
# content 仅用于本地装配的 API HTML，属于渲染回退，需在图片上标注。
<<< END U013486 >>>
<<< UNIT U013487 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:10-11 >>>
# 引用来源、图库、代码块等标签的内容不属于正文。
# wikitextparser 的 plain_text() 不剥离标签内容，故须在其之前显式清除。
<<< END U013487 >>>
<<< UNIT U013488 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:27-27 >>>
# 章节标题行，形如 == 标题 == 或 === 子标题 ===
<<< END U013488 >>>
<<< UNIT U013489 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:30-31 >>>
# MediaWiki 行为开关，如 __TOC__、__NOTOC__、__NOEDITSECTION__。
# 它们只控制页面渲染，不属于正文，而 plain_text() 不会剥离
<<< END U013489 >>>
<<< UNIT U013490 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:34-35 >>>
# 分类链接与跨语言链接的目标前缀，如 Category:、分类：、de:、zh-hans:。
# 这两类链接不出现在渲染后的正文中，但 plain_text() 会把它们还原成链接目标文本
<<< END U013490 >>>
<<< UNIT U013491 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:42-44 >>>
# 语义属性链接 [[属性：值：]]，在页面上渲染为其值。值中可含嵌套的内外链接，故须放行一层。
# 须在解析前以文本替换处理，因为将 WikiLink 的 string 改写成非链接文本会令该对象失效，
# 其后 plain_text() 遍历到它便会抛 AttributeError
<<< END U013491 >>>
<<< UNIT U013492 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:47-48 >>>
# 未被 wikitextparser 识别的扩展标签，如 Translate 扩展的 <translate>。
# 这类标签包裹的是正文本身，只去标签、留内容
<<< END U013492 >>>
<<< UNIT U013493 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:51-52 >>>
# 正文中不应残留的 Wikitext 结构标记。构造一旦不成对或不被识别，这些标记便会原样
# 留在输出里。与其把半段源码充作摘要，不如舍去所在的行，没有正文时宁可不给摘要
<<< END U013493 >>>
<<< UNIT U013494 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:55-55 >>>
# TemplateData 扩展的标签，其内容为描述模板用法的 JSON
<<< END U013494 >>>
<<< UNIT U013495 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:58-58 >>>
# 句末标点包括中英文的句号、问号、叹号，英文标点须后随空白，以免小数点与缩写被误判
<<< END U013495 >>>
<<< UNIT U013496 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:60-60 >>>
# 首句含开括号时改用此式，取闭括号之后的句末标点，避免在括号内部截断
<<< END U013496 >>>
<<< UNIT U013497 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:64-65 >>>
# 首句短于此长度时补上第二句。“石头（Stone）是在主世界中大量存在的方块。”为 23 字符，
# 属应当补充的一档。首句本身已逾此长度的条目不再追加
<<< END U013497 >>>
<<< UNIT U013498 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:72-74 >>>
# 须在解析前自行扫描，不能交给 wikitextparser，因为构造内部若有裸露的单个花括号（如 {{#css:}}
# 所含的 CSS），括号配对会失准，该构造遂原样留在 plain_text() 输出里被当作正文。
# 只移除成对者，因为 MediaWiki 对孤立的 {{ 按字面渲染，一路吞到结尾会连正文一并丢失。
<<< END U013498 >>>
<<< UNIT U013499 | py-inline-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:87-87 >>>
# 最外层构造闭合，整段一并移除
<<< END U013499 >>>
<<< UNIT U013500 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:104-105 >>>
# 归一化章节名以供比较。
# 章节锚点中的下划线与标题中的空格等价，wikilib 传入的章节名已将空格换作下划线。
<<< END U013500 >>>
<<< UNIT U013501 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:110-110 >>>
# 取出目标章节。
<<< END U013501 >>>
<<< UNIT U013502 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:115-115 >>>
# wikitextparser 的首个章节即引言段，其 title 为 None
<<< END U013502 >>>
<<< UNIT U013503 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:125-127 >>>
# 模板文档页的说明常整个写在 <templatedata> 的 description 字段里，而其外层的
# {{TemplateData|...}} 会被当作模板剥离，正文遂无从取得。取回的说明仍是 Wikitext，
# 须由调用方再行清理。
<<< END U013503 >>>
<<< UNIT U013504 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:134-134 >>>
# 页面上的 TemplateData 未必合法，解析不了便当作没有
<<< END U013504 >>>
<<< UNIT U013505 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:143-145 >>>
# 解析 Wikitext 并取出指定章节的正文纯文本。
# 行为开关、模板类构造与语义属性链接须在解析前以文本处理，因为行为开关不构成任何
# 可识别的节点，模板类构造可能因内含未配对的花括号而不被识别，改写链接节点则会令其失效
<<< END U013505 >>>
<<< UNIT U013506 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:150-150 >>>
# 倒序清除，避免靠前的节点被置空后导致靠后节点的 span 偏移
<<< END U013506 >>>
<<< UNIT U013507 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:157-157 >>>
# 带显示文本的一定是正文中的行内链接，plain_text() 已能正确还原
<<< END U013507 >>>
<<< UNIT U013508 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:164-165 >>>
# 滤去章节标题行与仍带结构标记的残留行，前者一并覆盖目标章节自身的标题
# 与其下的子章节标题
<<< END U013508 >>>
<<< UNIT U013509 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:186-186 >>>
# TemplateData 只作补充，引言已有散文者以引言为准，指定章节时也不覆盖正文
<<< END U013509 >>>
<<< UNIT U013510 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:197-197 >>>
# 取出文本开头的一个完整句子。
<<< END U013510 >>>
<<< UNIT U013511 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:203-203 >>>
# 括号未闭合时回退到首个匹配。此处若直接取下标，空列表会抛 IndexError 并导致整段摘要缺失
<<< END U013511 >>>
<<< UNIT U013512 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:221-222 >>>
# 第二句须与首句同处一段。句末标点的匹配跨换行，不加此限制会把
# TextExtracts 输出中的章节标题、子章节正文一类的无关内容并入摘要
<<< END U013512 >>>
<<< UNIT U013513 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/summarize.py:1-1 | ctx=<module> >>>
Wikitext 离线摘要提取。
<<< END U013513 >>>
<<< UNIT U013514 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:308-308 >>>
# 萌娘百科强制使用移动版 API
<<< END U013514 >>>
<<< UNIT U013515 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:399-400 >>>
# 须带时区，因为不带时区的时间会被 Tortoise 当作 UTC 存入，缓存时间因此提前一个时区差，
# 上面的 43200 秒过期判断会多留一个时区差的缓存
<<< END U013515 >>>
<<< UNIT U013516 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:554-556 >>>
# 从查询结果中取出页面的 Wikitext。
# MediaWiki 1.32 起内容置于 slots 结构下，更低版本直接置于 revision 上，
# 两种结构都要兼容。
<<< END U013516 >>>
<<< UNIT U013517 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:986-988 >>>
# 摘要须由本地解析 Wikitext 得出。此处随主查询一并取回，无须额外请求。
# rvslots 自 MediaWiki 1.32 起提供，更低版本会忽略该参数并返回旧式结构，
# 故读取时要兼容两种结构。
<<< END U013517 >>>
<<< UNIT U013518 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:1039-1039 >>>
# 引言 extracts 不能作为重定向目标章节的摘要。
<<< END U013518 >>>
<<< UNIT U013519 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:1373-1374 >>>
# 解析不出正文时不再回退至渲染 HTML，因为那条路径取回的是信息框、
# 导航栏一类的原始文本，充作摘要没有意义，宁可只给出链接
<<< END U013519 >>>
<<< UNIT U013520 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:1441-1442 >>>
# MediaWiki 的 iwurl 会返回已经解析过全域、本地及转发规则的完整 URL。
# siteinfo.interwikimap 不一定包含扩展提供的全域前缀，因此只把缓存映射作为兼容回退。
<<< END U013520 >>>
<<< UNIT U013521 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:1460-1461 >>>
# try to query interwiki page
# 章节与查询参数随标题交给目标 wiki，由其按自身章节表校验并判定渲染目标
<<< END U013521 >>>
<<< UNIT U013522 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:1484-1484 >>>
# 参数已由目标 wiki 解析并拼入链接，此处不再重复拼接
<<< END U013522 >>>
<<< UNIT U013523 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:178-178 | ctx=WikiLib.should_check_content >>>
当前会话是否要求检查 Wiki 返回内容。
<<< END U013523 >>>
<<< UNIT U013524 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:816-829 | ctx=WikiLib.parse_page_info >>>
:param title: 页面标题，如果为 None，则使用 pageid。
:param pageid: 页面 id。
:param inline: 是否为 inline 模式。
:param lang: 所需的对应语言版本。
:param _doc: 是否为文档模式，仅用作内部递归调用判断。
:param _tried: 尝试 iw 跳转的次数，仅用作内部递归调用判断。
:param _explicit: 其中由标题显式请求的 iw 跳转次数，仅用作内部递归调用判断。
:param _prefix: iw 前缀，仅用作内部递归调用判断。
:param _iw: 是否为 iw 模式，仅用作内部递归调用判断。
:param _search: 是否为搜索模式，仅用作内部递归调用判断。
:param session: 消息会话，用于检查结果。
:param check_render: 是否使用 MediaWiki parse API 检查 WebRender 目标。
<<< END U013524 >>>
<<< UNIT U013525 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/utils/wikilib.py:1528-1531 | ctx=WikiLib.random_page >>>
获取随机页面
:return: 页面信息
<<< END U013525 >>>
<<< UNIT U013526 | py-inline-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/weekly.py:29-29 >>>
# 分段
<<< END U013526 >>>
<<< UNIT U013527 | py-inline-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/weekly.py:30-30 >>>
# 移除所有 HTML 标签
<<< END U013527 >>>
<<< UNIT U013528 | py-inline-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/weekly.py:31-31 >>>
# 移除不必要的空行
<<< END U013528 >>>
<<< UNIT U013529 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/weekly.py:99-99 | ctx=get_teahouse_rss >>>
兼容 weekly-rss 的公开入口，同时延迟加载 RSS 解析依赖。
<<< END U013529 >>>
<<< UNIT U013530 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wiki.py:485-486 >>>
# Markdown 元素后再拼接其他元素时，这个尾换行会与 MessageChain
# 的分隔换行组成空行，避免 QQ 手机端把下一行吞进引用块。
<<< END U013530 >>>
<<< UNIT U013531 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wiki.py:1346-1346 >>>
# 异常自身不是消息元素，须先取其文本再并入消息链。
<<< END U013531 >>>
<<< UNIT U013532 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wiki.py:464-464 | ctx=finish_if_wiki_blocked >>>
在发起内容查询前拒绝全局 URL 阻止列表中的 Wiki API。
<<< END U013532 >>>
<<< UNIT U013533 | py-docstring | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wiki.py:710-710 | ctx=query_pages >>>
在查询全过程中保持平台上下文，避免慢请求期间被消息清理流程释放。
<<< END U013533 >>>
<<< UNIT U013534 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wikilog.py:395-395 >>>
# 保活需逐个查询订阅的 wiki，耗时远超 hook 默认执行预算。单个 wiki 的失败在循环内就地转为会话消息。
<<< END U013534 >>>
<<< UNIT U013535 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wikilog.py:403-403 >>>
# 保活结果与目标会话无关，每个 wiki 只查一次，再交由组内推送按通道分发
<<< END U013535 >>>
<<< UNIT U013536 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wikilog.py:529-531 >>>
# 在承担推送的会话上算出并逐条发出该组的日志。
# 日志文本须按目标会话现算，因为敏感词检查取决于该会话所在平台是否要求，同组的不同平台
# 未必一致。逐条发送故在此处完成，工厂随即返回 None，不再交由外层发送。
<<< END U013536 >>>
<<< UNIT U013537 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wikilog.py:557-557 >>>
# 拉取按 union 去重，推送再按消息通道去重，同一个现实场景只收一份
<<< END U013537 >>>
<<< UNIT U013538 | py-comment | packages/modules/akari-bot-module-wiki/akaribot/modules/wiki/wikilog.py:561-561 >>>
# 单个场景组发送失败（如平台超时）不应中断其余场景组的推送
<<< END U013538 >>>
<<< UNIT U013539 | cfg-comment | packages/modules/akari-bot-module-wiki/pyproject.toml:21-21 >>>
    # aiocqhttp 是模块→平台 SDK 的现存违规依赖（T4.2 §7.6），在 core HTTP 层接管之前必须保留
<<< END U013539 >>>
<<< UNIT U013540 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_disambiguation.py:1-1 | ctx=<module> >>>
Wiki 消歧义页面识别、链接操作化与分平台长度处理测试。
<<< END U013540 >>>
<<< UNIT U013541 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_forum.py:1-1 | ctx=<module> >>>
Wiki 论坛列表 Markdown 表格布局测试。
<<< END U013541 >>>
<<< UNIT U013542 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_interwiki_url.py:1-1 | ctx=<module> >>>
Wiki 全域及多级 Interwiki URL 解析回归测试。
<<< END U013542 >>>
<<< UNIT U013543 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_interwiki_url.py:159-159 | ctx=test_wiki_interwiki_url >>>
wiki: 使用 API 解析全域及多级 Interwiki
<<< END U013543 >>>
<<< UNIT U013544 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_invalid_interwiki.py:67-67 | ctx=test_wiki_invalid_interwiki >>>
wiki: 站点 interwiki 无效时的提示
<<< END U013544 >>>
<<< UNIT U013545 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_lifecycle.py:113-113 >>>
# 模拟 query_pages 的下一轮循环覆写当前页对象。未冻结页面时闭包会读到这些新值。
<<< END U013545 >>>
<<< UNIT U013546 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_manual_anchor.py:1-1 | ctx=<module> >>>
Wiki 手动章节锚点识别、摘要抑制与 WebRender 转交测试。
<<< END U013546 >>>
<<< UNIT U013547 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_markdown.py:1-1 | ctx=<module> >>>
wiki 页面摘要 Markdown 渲染测试。
<<< END U013547 >>>
<<< UNIT U013548 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_markdown.py:75-75 | ctx=test_wiki_markdown >>>
wiki: 页面摘要按平台 Markdown 能力渲染
<<< END U013548 >>>
<<< UNIT U013549 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_message_buttons.py:40-40 >>>
# 未找到分支会读取 target_union_info.target_data，故走 assign 以贴近真实会话。
<<< END U013549 >>>
<<< UNIT U013550 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_message_buttons.py:60-60 >>>
# 运行一遍 query_pages，捕获主流程发出的消息与等待链路的提示。
<<< END U013550 >>>
<<< UNIT U013551 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_message_buttons.py:76-76 >>>
# 用户回复了无法识别的文本，等待链路按取消处理，不再发起新查询。
<<< END U013551 >>>
<<< UNIT U013552 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_message_buttons.py:129-129 >>>
# 候选项末行的关闭按钮复用渲染按钮的删除文案，按会话语言取。
<<< END U013552 >>>
<<< UNIT U013553 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_message_buttons.py:1-1 | ctx=<module> >>>
wiki 结果消息的交互与样式设置测试。
<<< END U013553 >>>
<<< UNIT U013554 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_message_buttons.py:320-320 | ctx=test_wiki_message_buttons >>>
wiki 结果消息交互与样式设置测试
<<< END U013554 >>>
<<< UNIT U013555 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_recommend.py:70-70 >>>
# 7 个按钮在上限 3 之下分作三行，余数均摊到首行
<<< END U013555 >>>
<<< UNIT U013556 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_recommend.py:79-80 >>>
# 与 bots/qqbot/bot.py 的 on_interaction_create 一致，不指定前缀，
# 故会话取到的是全局配置的前缀，而非常规消息入口所用的斜杠前缀。
<<< END U013556 >>>
<<< UNIT U013557 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_recommend.py:1-1 | ctx=<module> >>>
wiki 推荐绑定列表单元测试 - 按钮数据构造与发出门槛。
<<< END U013557 >>>
<<< UNIT U013558 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_recommend.py:135-135 | ctx=test_wiki_recommend >>>
wiki 推荐绑定列表的按钮数据与发出门槛测试
<<< END U013558 >>>
<<< UNIT U013559 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_render_precheck.py:162-162 >>>
# 主站 en: 前缀指向 minecraft.wiki，目标页面无信息框但存在目标章节。
<<< END U013559 >>>
<<< UNIT U013560 | py-comment | packages/modules/akari-bot-module-wiki/tests/test_wiki_render_precheck.py:240-240 >>>
# 主站 en 语言版本指向 minecraft.wiki，目标页面无信息框。章节按目标 wiki 的章节表校验。
<<< END U013560 >>>
<<< UNIT U013561 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_render_precheck.py:1-1 | ctx=<module> >>>
Wiki WebRender 检查在跨 wiki 跳转后的传递测试。
<<< END U013561 >>>
<<< UNIT U013562 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_render_precheck.py:309-309 | ctx=test_wiki_render_precheck >>>
wiki: 跨 wiki 跳转后仍判定目标页面可渲染性
<<< END U013562 >>>
<<< UNIT U013563 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_siteinfo_cache.py:1-1 | ctx=<module> >>>
Wiki 站点信息缓存异常响应回归测试。
<<< END U013563 >>>
<<< UNIT U013564 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_siteinfo_cache.py:158-158 | ctx=test_wiki_siteinfo_cache >>>
wiki: 无效站点信息缓存与 API 响应处理
<<< END U013564 >>>
<<< UNIT U013565 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_summary.py:1-1 | ctx=<module> >>>
wiki 摘要离线提取单元测试 - Wikitext 解析与噪音剥离。
<<< END U013565 >>>
<<< UNIT U013566 | py-docstring | packages/modules/akari-bot-module-wiki/tests/test_wiki_summary.py:296-296 | ctx=test_wiki_summary >>>
wiki 摘要离线提取的 Wikitext 解析与噪音剥离测试
<<< END U013566 >>>
<<< UNIT U013567 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/README.md:3-3 | ctx=akari-bot-module-wolframalpha >>>
向 WolframAlpha 提交问题，返回图片或简短文本答案。
<<< END U013567 >>>
<<< UNIT U013568 | md-heading | packages/modules/akari-bot-module-wolframalpha/README.md:5-5 | ctx=安装 >>>
## 安装
<<< END U013568 >>>
<<< UNIT U013569 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/README.md:7-7 | ctx=安装 >>>
Python 版本要求见包内 `pyproject.toml` 的 `requires-python`。
<<< END U013569 >>>
<<< UNIT U013570 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/README.md:13-13 | ctx=安装 >>>
模块的启用与配置参见 [项目文档](https://github.com/Teahouse-Studios/akari-bot/blob/master/README.md)。
<<< END U013570 >>>
<<< UNIT U013571 | md-heading | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:5-5 | ctx=wolframalpha：安装与开发 >>>
# wolframalpha：安装与开发
<<< END U013571 >>>
<<< UNIT U013572 | md-heading | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:7-7 | ctx=安装 >>>
## 安装
<<< END U013572 >>>
<<< UNIT U013573 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:13-13 | ctx=安装 >>>
安装后，管理员需要在会话中执行 `module enable wolframalpha` 开启模块。
<<< END U013573 >>>
<<< UNIT U013574 | md-heading | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:15-15 | ctx=配置项 >>>
## 配置项
<<< END U013574 >>>
<<< UNIT U013575 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:19-19 | ctx=配置项 >>>
唯一的配置字段是敏感项，写入同一文件的 `module_wolframalpha_secret` 表。
<<< END U013575 >>>
<<< UNIT U013576 | md-table | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:21-23 | ctx=配置项 >>>
| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `wolfram_alpha_appid` | str | 空 | WolframAlpha 的 AppID |
<<< END U013576 >>>
<<< UNIT U013577 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:25-25 | ctx=配置项 >>>
`manifest.toml` 把该字段列为需要检查重复的登录信息字段。未填写时，两个命令都会报配置缺失错误。
<<< END U013577 >>>
<<< UNIT U013578 | md-heading | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:27-27 | ctx=权限与平台能力 >>>
## 权限与平台能力
<<< END U013578 >>>
<<< UNIT U013579 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:29-29 | ctx=权限与平台能力 >>>
命令对普通用户开放，不要求管理员或超级用户权限。模块声明支持的语言为英语（`en_us`），未声明平台限制，所有已接入平台可用。`query` 的结果以图片消息发送。
<<< END U013579 >>>
<<< UNIT U013580 | md-heading | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:31-31 | ctx=数据表 >>>
## 数据表
<<< END U013580 >>>
<<< UNIT U013581 | md-heading | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:35-35 | ctx=依赖与外部服务 >>>
## 依赖与外部服务
<<< END U013581 >>>
<<< UNIT U013582 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/development.md:37-37 | ctx=依赖与外部服务 >>>
依赖 `akari-bot-core` 与 `Pillow`。外部服务为 `http://api.wolframalpha.com/v1/simple` 与 `http://api.wolframalpha.com/v1/result`。
<<< END U013582 >>>
<<< UNIT U013583 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/index.md:3-3 | ctx=wolframalpha >>>
此模块把问题或算式提交给 WolframAlpha，以结果图片或简短文本返回。接口使用公制单位。
<<< END U013583 >>>
<<< UNIT U013584 | md-heading | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/index.md:5-5 | ctx=命令 >>>
## 命令
<<< END U013584 >>>
<<< UNIT U013585 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/index.md:13-13 | ctx=`wolframalpha` >>>
此命令把问题或算式提交给 WolframAlpha，以结果图片形式返回。查询涉及 IP、地理位置或身份等敏感内容时，命令不发起查询，直接返回彩蛋内容。接口无法理解问题时，命令提示改用英语提问。
<<< END U013585 >>>
<<< UNIT U013586 | md-paragraph | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/docs/index.md:19-19 | ctx=`wolframalpha ask` >>>
此命令把问题提交给 WolframAlpha，以简短文本形式返回。敏感查询与无法理解问题的处理方式与 `wolframalpha` 相同。
<<< END U013586 >>>
<<< UNIT U013587 | json-value | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/locales/zh_cn.json:2-2 | ctx=wolframalpha.help >>>
输入问题或公式以搜索 WolframAlpha。
<<< END U013587 >>>
<<< UNIT U013588 | json-value | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/locales/zh_cn.json:3-3 | ctx=wolframalpha.help.ask >>>
通过 WolframAlpha 回答问题。
<<< END U013588 >>>
<<< UNIT U013589 | json-value | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/locales/zh_cn.json:4-4 | ctx=wolframalpha.help.desc >>>
使用 WolframAlpha。
<<< END U013589 >>>
<<< UNIT U013590 | json-value | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/locales/zh_cn.json:5-5 | ctx=wolframalpha.message.incomprehensible >>>
WolframAlpha 无法理解你的问题，请尝试使用英语提问。
<<< END U013590 >>>
<<< UNIT U013591 | json-value | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/locales/zh_cn.json:6-6 | ctx=config.comments.module_wolframalpha_secret.wolfram_alpha_appid >>>
WolframAlpha 的 AppID。
<<< END U013591 >>>
<<< UNIT U013592 | cfg-comment | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/manifest.toml:1-1 >>>
# akari-bot-module-wolframalpha 的包清单。
<<< END U013592 >>>
<<< UNIT U013593 | cfg-comment | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/manifest.toml:5-5 >>>
# config.py 的 on_module_config("wolframalpha") 声明的表。
<<< END U013593 >>>
<<< UNIT U013594 | cfg-comment | packages/modules/akari-bot-module-wolframalpha/akaribot/modules/wolframalpha/manifest.toml:9-9 >>>
# 查重用的登录信息字段，对应 WolframAlpha 应用 ID。
<<< END U013594 >>>
<<< UNIT U013595 | md-paragraph | packages/modules/akari-bot-module-wordle/README.md:3-3 | ctx=akari-bot-module-wordle >>>
猜测五个字母的英文单词，六次机会内完成挑战。
<<< END U013595 >>>
<<< UNIT U013596 | md-heading | packages/modules/akari-bot-module-wordle/README.md:5-5 | ctx=安装 >>>
## 安装
<<< END U013596 >>>
<<< UNIT U013597 | md-paragraph | packages/modules/akari-bot-module-wordle/README.md:7-7 | ctx=安装 >>>
Python 版本要求见包内 `pyproject.toml` 的 `requires-python`。
<<< END U013597 >>>
<<< UNIT U013598 | md-paragraph | packages/modules/akari-bot-module-wordle/README.md:13-13 | ctx=安装 >>>
模块的启用与配置参见 [项目文档](https://github.com/Teahouse-Studios/akari-bot/blob/master/README.md)。
<<< END U013598 >>>
<<< UNIT U013599 | md-heading | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:5-5 | ctx=wordle：安装与开发 >>>
# wordle：安装与开发
<<< END U013599 >>>
<<< UNIT U013600 | md-heading | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:7-7 | ctx=安装 >>>
## 安装
<<< END U013600 >>>
<<< UNIT U013601 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:13-13 | ctx=安装 >>>
安装后，管理员需要在会话中执行 `module enable wordle` 开启模块。
<<< END U013601 >>>
<<< UNIT U013602 | md-heading | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:15-15 | ctx=配置项 >>>
## 配置项
<<< END U013602 >>>
<<< UNIT U013603 | md-table | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:19-21 | ctx=配置项 >>>
| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `wordle_disable_image` | bool | false | 是否禁用图片并使用文本棋盘 |
<<< END U013603 >>>
<<< UNIT U013604 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:23-23 | ctx=配置项 >>>
开启 `wordle_disable_image` 后，开局与每次提交都发送文本棋盘，不发送棋盘与键盘的图片。
<<< END U013604 >>>
<<< UNIT U013605 | md-heading | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:25-25 | ctx=权限与平台能力 >>>
## 权限与平台能力
<<< END U013605 >>>
<<< UNIT U013606 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:27-27 | ctx=权限与平台能力 >>>
命令对普通用户开放，不要求管理员或超级用户权限。模块未声明平台限制，所有已接入的平台都可以使用。
<<< END U013606 >>>
<<< UNIT U013607 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:29-29 | ctx=权限与平台能力 >>>
图片模式依赖 `akari-bot-assets-fonts` 提供的字体。花瓣奖励仅在实例开启花瓣系统时生效。
<<< END U013607 >>>
<<< UNIT U013608 | md-heading | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:31-31 | ctx=数据表 >>>
## 数据表
<<< END U013608 >>>
<<< UNIT U013609 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:35-35 | ctx=数据表 >>>
对局状态与冷却都保存在进程内。
<<< END U013609 >>>
<<< UNIT U013610 | md-heading | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:37-37 | ctx=依赖与外部服务 >>>
## 依赖与外部服务
<<< END U013610 >>>
<<< UNIT U013611 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/development.md:39-39 | ctx=依赖与外部服务 >>>
依赖 `akari-bot-core`、`akari-bot-assets-fonts`、`Pillow` 与 `attrs`。模块不使用外部数据接口。答案与可提交词表随包分发，位于 `assets/answers.txt` 与 `assets/words.txt`。词典链接指向剑桥词典网站。
<<< END U013611 >>>
<<< UNIT U013612 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md:3-3 | ctx=wordle >>>
此模块是英文猜词游戏。你要猜出一个五个字母的英文单词，最多可以猜六次。每次提交后，机器人按字母与位置给出绿、黄、灰三色反馈。
<<< END U013612 >>>
<<< UNIT U013613 | md-heading | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md:5-5 | ctx=命令 >>>
## 命令
<<< END U013613 >>>
<<< UNIT U013614 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md:11-11 | ctx=`wordle` >>>
此命令用于开始新游戏，一局最多可以猜六次。`--hard` 与 `--trial` 分别开启困难模式与挑战模式，两者可以同时使用。
<<< END U013614 >>>
<<< UNIT U013615 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md:14-33 | ctx=`wordle` >>>
  caption="答案 cigar，三次猜中。图片为实际渲染结果。"
  :image-width="320"
  :log="[
    '用户：~wordle',
    '机器人：![棋盘](wordle-start-board.png)',
    '![键盘](wordle-start-keyboard.png)',
    '游戏开始，你需要猜一个由 5 个字母组成的单词，你有 6 次机会。',
    '绿色表示字母和位置都正确，黄色代表字母正确但位置不正确，灰色代表单词中没有这个字母。',
    '用户：crane',
    '机器人：![棋盘](wordle-guess1-board.png)',
    '![键盘](wordle-guess1-keyboard.png)',
    '用户：shine',
    '机器人：![棋盘](wordle-guess2-board.png)',
    '![键盘](wordle-guess2-keyboard.png)',
    '用户：cigar',
    '机器人：![棋盘](wordle-guess3-board.png)',
    '![键盘](wordle-guess3-keyboard.png)',
    '祝贺！你在 3 回合内完成了游戏。',
  ]"
/>
<<< END U013615 >>>
<<< UNIT U013616 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md:39-39 | ctx=`wordle stop` >>>
此命令用于结束当前对局并公布答案，同时附上剑桥词典链接。没有进行中的对局时，命令会返回停止失败的提示。
<<< END U013616 >>>
<<< UNIT U013617 | md-paragraph | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md:42-47 | ctx=`wordle stop` >>>
  :log="[
    '用户：~wordle stop',
    '机器人：已停止，答案为：cigar。',
    '查询词典：',
  ]"
/>
<<< END U013617 >>>
<<< UNIT U013618 | md-heading | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md:49-49 | ctx=游戏规则 >>>
## 游戏规则
<<< END U013618 >>>
<<< UNIT U013619 | md-list | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/docs/index.md:51-58 | ctx=游戏规则 >>>
- 答案从内置词表中随机抽取，猜词必须存在于可提交词表中。
- 绿色表示字母与位置都正确，黄色表示字母正确但位置错误，灰色表示该字母在当前尝试中已无剩余匹配。
- 困难模式要求后续提交保留上一回合的绿色字母位置，并保证黄色字母的出现次数达到要求。
- 默认模式下，会话内任意成员都可以提交。挑战模式只接受发起者本人的下一条消息。
- 超过六次仍未猜中时，机器人公布答案并附上剑桥词典链接。
- 挑战模式猜中后奖励花瓣。三次以内猜中奖励 2 枚，否则奖励 1 枚。同一局同时开启困难模式时，额外奖励 1 枚。
- 非超级用户两次开局间隔不少于 180 秒。对局结束或执行 `stop` 后，冷却时间重置。
- 对局状态按会话隔离，1 小时后过期。机器人服务重启后，对局会中断。
<<< END U013619 >>>
<<< UNIT U013620 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:2-2 | ctx=wordle.help >>>
开始新游戏。
<<< END U013620 >>>
<<< UNIT U013621 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:3-3 | ctx=wordle.help.desc >>>
玩 Wordle。
<<< END U013621 >>>
<<< UNIT U013622 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:4-4 | ctx=wordle.help.option.hard >>>
使用困难模式。
<<< END U013622 >>>
<<< UNIT U013623 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:5-5 | ctx=wordle.help.option.trial >>>
使用挑战模式。
<<< END U013623 >>>
<<< UNIT U013624 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:6-6 | ctx=wordle.message.occupied >>>
此{TERM:target}内有游戏正在进行。
<<< END U013624 >>>
<<< UNIT U013625 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:7-7 | ctx=wordle.message.finish >>>
游戏结束，答案为：${answer}。
查询词典：
<<< END U013625 >>>
<<< UNIT U013626 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:8-8 | ctx=wordle.message.finish.success >>>
祝贺！你在 ${attempt} 回合内完成了游戏。
<<< END U013626 >>>
<<< UNIT U013627 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:9-9 | ctx=wordle.message.hard.not_matched >>>
输入的单词不符合要求。
<<< END U013627 >>>
<<< UNIT U013628 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:10-10 | ctx=wordle.message.not_a_word >>>
这不是一个有效的单词。
<<< END U013628 >>>
<<< UNIT U013629 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:11-11 | ctx=wordle.message.start >>>
游戏开始，你需要猜一个由 5 个字母组成的单词，你有 6 次机会。
绿色表示字母和位置都正确，黄色代表字母正确但位置不正确，灰色代表单词中没有这个字母。
<<< END U013629 >>>
<<< UNIT U013630 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:12-12 | ctx=wordle.message.start.hard >>>
在上一回合中被颜色标记的字母在接下来的回合中必须出现，且必须符合对应的要求。
<<< END U013630 >>>
<<< UNIT U013631 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:13-13 | ctx=wordle.message.start.trial >>>
你正在进行挑战模式，成功完成游戏可获得花瓣。
<<< END U013631 >>>
<<< UNIT U013632 | json-value | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/locales/zh_cn.json:14-14 | ctx=wordle.message.stop >>>
已停止，答案为：${answer}。
查询词典：
<<< END U013632 >>>
<<< UNIT U013633 | cfg-comment | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/manifest.toml:1-1 >>>
# akari-bot-module-wordle 的包清单。
<<< END U013633 >>>
<<< UNIT U013634 | cfg-comment | packages/modules/akari-bot-module-wordle/akaribot/modules/wordle/manifest.toml:6-6 >>>
# config.py 的 on_module_config("wordle") 声明的表。
<<< END U013634 >>>
<<< UNIT U013635 | cfg-comment | packages/modules/akari-bot-module-wordle/pyproject.toml:18-18 >>>
    # 棋盘与键盘渲染使用资源包中的 Noto Sans CJK Bold（T3.3），缺失会导致出图失败。
<<< END U013635 >>>
<<< UNIT U013636 | cfg-comment | pyproject.toml:1-2 >>>
# monorepo 根为虚拟工作区，不发布自身。依赖按包归位于各成员的 pyproject.toml，
# 本文件只声明成员、workspace 内的版本来源，以及整个仓库的工具配置。
<<< END U013636 >>>
<<< UNIT U013637 | cfg-comment | pyproject.toml:4-4 >>>
# packages/* 会匹配到 adapters/ 与 modules/ 两个容器目录（它们不是包），故按前缀收窄范围。
<<< END U013637 >>>
<<< UNIT U013638 | cfg-comment | pyproject.toml:9-9 >>>
# 资源包不在索引上，成员对它的依赖须显式指向工作区成员，uv 才会认这条依赖。
<<< END U013638 >>>
<<< UNIT U013639 | cfg-comment | pyproject.toml:25-25 >>>
# 单元测试使用 pytest，包内测试与集成用例仍由 tester.py 运行。
<<< END U013639 >>>
<<< UNIT U013640 | cfg-comment | pyproject.toml:32-32 >>>
# 根 pyproject 无 [project]，target-version 无法由 requires-python 推出，须显式声明。
<<< END U013640 >>>
<<< UNIT U013641 | py-comment | tester.py:12-13 >>>
# 本文件位于仓库根目录，仓库根目录由调用方显式传入，runner 无须再从自身位置反推。
# 变量名须与 akaribot.testing.runner.REPO_ROOT_ENV 一致，取值必须早于该模块的导入。
<<< END U013641 >>>
<<< UNIT U013642 | py-comment | tester.py:21-22 >>>
# 使用模块别名而非逐个再导出，因为 conftest.py 与包内测试会 patch tester 模块的属性，别名让这些补丁
# 与 runner 的全局状态指向同一份对象（原 tester.py 与 runner 本就是一个模块）。
<<< END U013642 >>>
<<< UNIT U013643 | py-comment | tests/build_synthetic_fixtures.py:15-15 >>>
# minecraft_news 逐条读取 default_tile.title / sub_header 与 article_url、image.imageURL。
<<< END U013643 >>>
<<< UNIT U013644 | py-comment | tests/build_synthetic_fixtures.py:37-37 >>>
# mcv_rss 的 get_article 只从页面中取第一个 h1 作为标题，并以 "404" 判定页面不存在。
<<< END U013644 >>>
<<< UNIT U013645 | py-comment | tests/build_synthetic_fixtures.py:43-43 >>>
# minecraft_news 取到图片链接后会以 get_raw 拉取图片内容，语料按 URL 命中即可。
<<< END U013645 >>>
<<< UNIT U013646 | py-comment | tests/build_synthetic_fixtures.py:49-50 >>>
# 需要预置变更日志语料的版本号。线上版本推进后需同步更新，
# 缺失时 mcv_rss 无法取得文章标题，但不影响版本推送的检查。
<<< END U013646 >>>
<<< UNIT U013647 | py-comment | tests/build_synthetic_fixtures.py:54-56 >>>
# 稳定失败的外部端点。录制工具只保存成功响应，这些请求在测试中会改用真实网络，
# 带着重试与超时耗掉数十秒，且结果随对方服务状态波动。此处以其真实状态码固定下来，
# 使模块进入与线上一致的错误分支，同时把耗时降为零。
<<< END U013647 >>>
<<< UNIT U013648 | py-comment | tests/build_synthetic_fixtures.py:58-58 >>>
# 该推文不存在，接口稳定返回 404，模块据此提示“未找到推文”。
<<< END U013648 >>>
<<< UNIT U013649 | py-comment | tests/build_synthetic_fixtures.py:60-60 >>>
# 皮肤渲染服务源站长期不可用，Cloudflare 返回 521。
<<< END U013649 >>>
<<< UNIT U013650 | py-comment | tests/build_synthetic_fixtures.py:62-62 >>>
# 基岩版查询接口无响应，以 5xx 复现其超时后的对外表现。
<<< END U013650 >>>
<<< UNIT U013651 | py-comment | tests/build_synthetic_fixtures.py:80-80 >>>
# 变更日志的 URL 由模块自身推导，此处直接复用其实现，避免规则不一致。
<<< END U013651 >>>
<<< UNIT U013652 | py-docstring | tests/build_synthetic_fixtures.py:1-1 | ctx=<module> >>>
构造无法录制的语料。
<<< END U013652 >>>
<<< UNIT U013653 | py-comment | tests/capture_http_fixtures.py:18-18 >>>
# 以 (URL, method, 请求体摘要) 为键去重，因为同一 URL 上请求体不同的调用需各自成为一份 fixture。
<<< END U013653 >>>
<<< UNIT U013654 | py-comment | tests/capture_http_fixtures.py:25-25 >>>
# fmt="read"/"content" 的下载类请求返回二进制，无法直接写入 JSON。
<<< END U013654 >>>
<<< UNIT U013655 | py-comment | tests/capture_http_fixtures.py:67-67 >>>
# 录制阶段必须关闭 fixture 回放，否则会把上一轮的 mock 结果再录一遍。
<<< END U013655 >>>
<<< UNIT U013656 | py-docstring | tests/capture_http_fixtures.py:1-1 | ctx=<module> >>>
HTTP Fixture 捕获工具 - 运行集成测试并将真实响应录制到本地文件。
<<< END U013656 >>>
<<< UNIT U013657 | py-comment | tests/capture_schedule_fixtures.py:17-17 >>>
# 这些模块的定时任务无法在录制环境中产生有效语料，跳过以免徒劳等待。
<<< END U013657 >>>
<<< UNIT U013658 | py-comment | tests/capture_schedule_fixtures.py:19-19 >>>
# 多页抓取叠加图片渲染，单次运行耗时过长，不适合纳入测试。
<<< END U013658 >>>
<<< UNIT U013659 | py-comment | tests/capture_schedule_fixtures.py:21-21 >>>
# 依赖 Google Play 抓取，且在 ip_country 未配置时直接早退。
<<< END U013659 >>>
<<< UNIT U013660 | py-comment | tests/capture_schedule_fixtures.py:23-23 >>>
# 需要真实 wiki 机器人账号的登录信息。
<<< END U013660 >>>
<<< UNIT U013661 | py-docstring | tests/capture_schedule_fixtures.py:1-1 | ctx=<module> >>>
定时任务语料捕获工具。
<<< END U013661 >>>
<<< UNIT U013662 | py-docstring | tests/capture_webrender_fixtures.py:1-1 | ctx=<module> >>>
WebRender 语料捕获工具。
<<< END U013662 >>>
<<< UNIT U013663 | py-docstring | tests/helpers/websocket_rpc_worker.py:1-1 | ctx=<module> >>>
WebSocket JobQueue 独立进程测试工作节点。
<<< END U013663 >>>
<<< UNIT U013664 | py-comment | tests/integration/test_core_admin.py:19-19 >>>
# 把被查询的成员一律视为平台原生管理员。
<<< END U013664 >>>
<<< UNIT U013665 | py-comment | tests/integration/test_core_admin.py:60-60 >>>
# 测试进程没有平台 Peer，ID 归属校验由 mock 提供
<<< END U013665 >>>
<<< UNIT U013666 | py-docstring | tests/integration/test_core_admin.py:1-1 | ctx=<module> >>>
modules/core 管理员与模块授权命令集成测试。
<<< END U013666 >>>
<<< UNIT U013667 | py-docstring | tests/integration/test_core_admin.py:25-25 | ctx=test_admin_list >>>
admin list 命令测试
<<< END U013667 >>>
<<< UNIT U013668 | py-docstring | tests/integration/test_core_admin.py:32-32 | ctx=test_admin_add_remove >>>
admin add/remove 流程测试
<<< END U013668 >>>
<<< UNIT U013669 | py-docstring | tests/integration/test_core_admin.py:41-41 | ctx=test_admin_native_admin >>>
平台原生管理员不受机器人管理员名单管理。
<<< END U013669 >>>
<<< UNIT U013670 | py-docstring | tests/integration/test_core_admin.py:59-59 | ctx=test_auth_add_strict_confirmation >>>
auth add 的高危操作严格确认流程测试
<<< END U013670 >>>
<<< UNIT U013671 | py-docstring | tests/integration/test_core_admin.py:74-74 | ctx=test_auth_add_rejects_wrong_confirmation >>>
auth add 未完全回复确认语句时不应授权
<<< END U013671 >>>
<<< UNIT U013672 | py-docstring | tests/integration/test_core_modules.py:1-1 | ctx=<module> >>>
akaribot/modules/core 核心模块集成测试。
<<< END U013672 >>>
<<< UNIT U013673 | py-docstring | tests/integration/test_core_modules.py:18-18 | ctx=test_version >>>
version 命令测试
<<< END U013673 >>>
<<< UNIT U013674 | py-docstring | tests/integration/test_core_modules.py:26-26 | ctx=test_about >>>
about 命令测试
<<< END U013674 >>>
<<< UNIT U013675 | py-docstring | tests/integration/test_core_modules.py:34-34 | ctx=test_help >>>
help 命令测试
<<< END U013675 >>>
<<< UNIT U013676 | py-docstring | tests/integration/test_core_modules.py:65-65 | ctx=test_merged_about_bind_commands >>>
并入 about 与 bind 的信息类子命令测试
<<< END U013676 >>>
<<< UNIT U013677 | py-docstring | tests/integration/test_core_modules.py:99-99 | ctx=test_merged_setup_commands >>>
并入 setup 的前缀、语言与别名子命令测试
<<< END U013677 >>>
<<< UNIT U013678 | py-docstring | tests/integration/test_core_modules.py:131-131 | ctx=test_module_list >>>
module list 命令测试
<<< END U013678 >>>
<<< UNIT U013679 | py-docstring | tests/integration/test_core_modules.py:139-139 | ctx=test_module_enable_disable >>>
module enable/disable 命令测试
<<< END U013679 >>>
<<< UNIT U013680 | py-docstring | tests/integration/test_core_modules.py:153-153 | ctx=test_alias >>>
alias 命令测试
<<< END U013680 >>>
<<< UNIT U013681 | py-docstring | tests/integration/test_core_modules.py:164-164 | ctx=test_prefix >>>
prefix 命令测试
<<< END U013681 >>>
<<< UNIT U013682 | py-docstring | tests/integration/test_core_modules.py:176-176 | ctx=test_unknown_command >>>
未知命令测试
<<< END U013682 >>>
<<< UNIT U013683 | py-docstring | tests/integration/test_core_modules.py:184-184 | ctx=test_ping >>>
ping 命令测试
<<< END U013683 >>>
<<< UNIT U013684 | py-docstring | tests/integration/test_core_modules.py:201-201 | ctx=test_whoami >>>
whoami 命令测试
<<< END U013684 >>>
<<< UNIT U013685 | py-docstring | tests/integration/test_core_modules.py:213-213 | ctx=test_locale >>>
locale 命令测试
<<< END U013685 >>>
<<< UNIT U013686 | py-docstring | tests/integration/test_core_modules.py:223-223 | ctx=test_petal >>>
petal 命令测试
<<< END U013686 >>>
<<< UNIT U013687 | py-docstring | tests/integration/test_core_modules.py:232-232 | ctx=test_say >>>
say 命令测试
<<< END U013687 >>>
<<< UNIT U013688 | py-docstring | tests/integration/test_external_modules.py:1-1 | ctx=<module> >>>
外部模块集成测试 - wiki, mcplayer, arcaea, mcmod, oba, tweet 等。
<<< END U013688 >>>
<<< UNIT U013689 | py-docstring | tests/integration/test_external_modules.py:12-12 | ctx=test_wiki >>>
wiki 模块测试 - MediaWiki 查询
<<< END U013689 >>>
<<< UNIT U013690 | py-docstring | tests/integration/test_external_modules.py:23-23 | ctx=test_mcplayer >>>
mcplayer 模块测试 - MC 玩家查询
<<< END U013690 >>>
<<< UNIT U013691 | py-docstring | tests/integration/test_external_modules.py:33-33 | ctx=test_arcaea >>>
arcaea 模块测试 - Arcaea 查询
<<< END U013691 >>>
<<< UNIT U013692 | py-docstring | tests/integration/test_external_modules.py:40-40 | ctx=test_mcmod >>>
mcmod 模块测试 - MCMOD 模组查询
<<< END U013692 >>>
<<< UNIT U013693 | py-docstring | tests/integration/test_external_modules.py:47-47 | ctx=test_oba >>>
oba 模块测试 - OpenBMCLAPI 状态
<<< END U013693 >>>
<<< UNIT U013694 | py-docstring | tests/integration/test_external_modules.py:54-54 | ctx=test_tweet_not_found >>>
tweet 模块测试 - 不存在的推文
<<< END U013694 >>>
<<< UNIT U013695 | py-docstring | tests/integration/test_external_wiki.py:1-1 | ctx=<module> >>>
wiki 模块高级集成测试 - search、iw、headers、prefix。
<<< END U013695 >>>
<<< UNIT U013696 | py-docstring | tests/integration/test_external_wiki.py:23-23 | ctx=test_wiki_set_url_policy >>>
wiki set 应以规范 API 端点的全局 URL 策略作为唯一认证来源。
<<< END U013696 >>>
<<< UNIT U013697 | py-docstring | tests/integration/test_external_wiki.py:95-95 | ctx=test_wiki_search >>>
wiki search 搜索测试
<<< END U013697 >>>
<<< UNIT U013698 | py-docstring | tests/integration/test_external_wiki.py:103-103 | ctx=test_wiki_iw_manage >>>
wiki iw 管理测试
<<< END U013698 >>>
<<< UNIT U013699 | py-docstring | tests/integration/test_external_wiki.py:110-110 | ctx=test_wiki_headers_manage >>>
wiki headers 管理测试
<<< END U013699 >>>
<<< UNIT U013700 | py-docstring | tests/integration/test_external_wiki.py:118-118 | ctx=test_wiki_prefix_manage >>>
wiki prefix 管理测试
<<< END U013700 >>>
<<< UNIT U013701 | py-docstring | tests/integration/test_external_wiki.py:127-127 | ctx=test_wiki_not_found >>>
wiki 不存在页面测试
<<< END U013701 >>>
<<< UNIT U013702 | py-docstring | tests/integration/test_external_wiki.py:135-135 | ctx=test_wiki_start_wiki_not_set >>>
未设置默认 Wiki 提示测试
<<< END U013702 >>>
<<< UNIT U013703 | py-docstring | tests/integration/test_features_command.py:1-1 | ctx=<module> >>>
features 命令集成测试 - 当前会话与主动获取会话的特性对照。
<<< END U013703 >>>
<<< UNIT U013704 | py-docstring | tests/integration/test_features_command.py:13-13 | ctx=test_features >>>
features 命令测试
<<< END U013704 >>>
<<< UNIT U013705 | py-docstring | tests/integration/test_game_modules.py:1-1 | ctx=<module> >>>
游戏模块集成测试 - wordle, twenty_four, chemical_code 等。
<<< END U013705 >>>
<<< UNIT U013706 | py-docstring | tests/integration/test_game_modules.py:12-12 | ctx=test_wordle >>>
wordle 模块测试 - Wordle 游戏完整流程
<<< END U013706 >>>
<<< UNIT U013707 | py-docstring | tests/integration/test_game_modules.py:21-21 | ctx=test_wordle_stop >>>
wordle stop 测试 - 停止未开始的游戏
<<< END U013707 >>>
<<< UNIT U013708 | py-docstring | tests/integration/test_game_modules.py:28-28 | ctx=test_twenty_four >>>
twenty_four 模块测试 - 24 点游戏
<<< END U013708 >>>
<<< UNIT U013709 | py-docstring | tests/integration/test_game_modules.py:35-35 | ctx=test_twenty_four_no_solution >>>
twenty_four 无解测试
<<< END U013709 >>>
<<< UNIT U013710 | py-docstring | tests/integration/test_game_modules.py:42-42 | ctx=test_twenty_four_stop >>>
twenty_four stop 测试 - 停止未开始的游戏
<<< END U013710 >>>
<<< UNIT U013711 | py-docstring | tests/integration/test_game_modules.py:49-49 | ctx=test_chemical_code_stop >>>
chemical_code stop 测试 - 停止未开始的游戏
<<< END U013711 >>>
<<< UNIT U013712 | py-comment | tests/integration/test_scheduled_tasks.py:82-82 >>>
# 第二次不清空持久化列表，仅重置队列，验证去重生效。
<<< END U013712 >>>
<<< UNIT U013713 | py-comment | tests/integration/test_scheduled_tasks.py:125-125 >>>
# 目录需保留（后续写缓存依赖它存在），但其中的残留文件应被清除。
<<< END U013713 >>>
<<< UNIT U013714 | py-docstring | tests/integration/test_scheduled_tasks.py:1-1 | ctx=<module> >>>
定时任务与钩子的集成测试。
<<< END U013714 >>>
<<< UNIT U013715 | py-docstring | tests/integration/test_scheduled_tasks.py:234-234 | ctx=test_scheduled_tasks >>>
定时任务手动触发测试
<<< END U013715 >>>
<<< UNIT U013716 | py-docstring | tests/integration/test_scheduled_tasks.py:258-258 | ctx=test_module_hooks >>>
模块钩子手动触发测试
<<< END U013716 >>>
<<< UNIT U013717 | py-docstring | tests/integration/test_url_allowlist.py:1-1 | ctx=<module> >>>
全局 URL 允许列表命令集成测试。
<<< END U013717 >>>
<<< UNIT U013718 | py-docstring | tests/integration/test_url_blocklist.py:1-1 | ctx=<module> >>>
全局 URL 阻止列表命令集成测试。
<<< END U013718 >>>
<<< UNIT U013719 | py-docstring | tests/integration/test_utility_modules.py:1-1 | ctx=<module> >>>
工具模块集成测试 - dice, coin, convert, color, nbnhhsh, idlist 等。
<<< END U013719 >>>
<<< UNIT U013720 | py-docstring | tests/integration/test_utility_modules.py:13-13 | ctx=test_dice >>>
dice 模块测试
<<< END U013720 >>>
<<< UNIT U013721 | py-docstring | tests/integration/test_utility_modules.py:29-29 | ctx=test_coin >>>
coin 模块测试
<<< END U013721 >>>
<<< UNIT U013722 | py-docstring | tests/integration/test_utility_modules.py:40-40 | ctx=test_hitokoto >>>
hitokoto 模块测试
<<< END U013722 >>>
<<< UNIT U013723 | py-docstring | tests/integration/test_utility_modules.py:48-48 | ctx=test_langconv >>>
langconv 模块测试
<<< END U013723 >>>
<<< UNIT U013724 | py-docstring | tests/integration/test_utility_modules.py:56-56 | ctx=test_convert >>>
convert 模块测试 - 单位转换
<<< END U013724 >>>
<<< UNIT U013725 | py-docstring | tests/integration/test_utility_modules.py:64-64 | ctx=test_color >>>
color 模块测试 - 颜色查询
<<< END U013725 >>>
<<< UNIT U013726 | py-docstring | tests/integration/test_utility_modules.py:72-72 | ctx=test_nbnhhsh >>>
nbnhhsh 模块测试 - 缩写翻译
<<< END U013726 >>>
<<< UNIT U013727 | py-docstring | tests/integration/test_utility_modules.py:90-90 | ctx=test_idlist >>>
idlist 模块测试 - 命令 ID 查询
<<< END U013727 >>>
<<< UNIT U013728 | py-docstring | tests/integration/test_utility_modules.py:99-99 | ctx=test_emojimix >>>
emojimix 模块测试 - Emoji 混合
<<< END U013728 >>>
<<< UNIT U013729 | py-docstring | tests/integration/test_wiki_audit.py:1-1 | ctx=<module> >>>
wiki-audit 向全局 URL 允许列表添加规范 Wiki API URL。
<<< END U013729 >>>
<<< UNIT U013730 | py-comment | tests/run_one.py:10-11 >>>
# 以文件路径直接启动时，sys.path 首位是 tests/ 而非项目根目录，须先补上项目根目录。akaribot 本身
# 由已安装包解析，此处仅为与 tester.py 保持一致的导入环境。
<<< END U013730 >>>
<<< UNIT U013731 | py-comment | tests/run_one.py:14-15 >>>
# 导入 runner 即完成测试环境初始化（配置目录、合并日志目录、语言快照缓存），须早于任何
# akaribot.core.* 导入。单入口运行与全量运行因此共用同一套隔离规则。
<<< END U013731 >>>
<<< UNIT U013732 | py-comment | tests/run_one.py:79-79 >>>
# 框架加载的模块会留下未完成的后台任务，正常返回会挂起，故强制退出
<<< END U013732 >>>
<<< UNIT U013733 | py-docstring | tests/run_one.py:1-1 | ctx=<module> >>>
临时的单元测试运行脚本，仅用于开发期运行单个测试入口。
<<< END U013733 >>>
<<< UNIT U013734 | py-docstring | tests/unit/test_bind_channel.py:1-1 | ctx=<module> >>>
akaribot.modules.core.common_tools.bind 单元测试 - 消息通道的主动推送优先级（需要数据库）。
<<< END U013734 >>>
<<< UNIT U013735 | py-docstring | tests/unit/test_bind_channel.py:107-107 | ctx=test_bind_channel >>>
akaribot.modules.core.common_tools.bind: 消息通道推送优先级命令测试
<<< END U013735 >>>
<<< UNIT U013736 | py-docstring | tests/unit/test_bot_state.py:1-1 | ctx=<module> >>>
统一机器人场景状态接口测试。
<<< END U013736 >>>
<<< UNIT U013737 | py-docstring | tests/unit/test_check_test_baseline.py:133-133 | ctx=test_check_test_baseline >>>
tools.check_test_baseline: 失败的用例清单对比测试
<<< END U013737 >>>
<<< UNIT U013738 | py-comment | tests/unit/test_check_versions.py:19-19 >>>
# 整段区间被放行的提交中，正文里两次提到旧标记，但从未写过独立 trailer。
<<< END U013738 >>>
<<< UNIT U013739 | py-comment | tests/unit/test_check_versions.py:21-21 >>>
# 版本检查依赖真实历史时会被区间内的豁免声明左右，故用例自建仓库测试数据。
<<< END U013739 >>>
<<< UNIT U013740 | py-docstring | tests/unit/test_check_versions.py:173-173 | ctx=test_check_versions >>>
tools.check_versions: 版本检查豁免解析测试
<<< END U013740 >>>
<<< UNIT U013741 | py-docstring | tests/unit/test_client_init.py:1-1 | ctx=<module> >>>
客户端初始化与 Discord 启动屏障单元测试。
<<< END U013741 >>>
<<< UNIT U013742 | py-docstring | tests/unit/test_client_init.py:232-232 | ctx=test_client_init >>>
客户端初始化只执行一次，并阻止 Discord 事件抢跑。
<<< END U013742 >>>
<<< UNIT U013743 | py-docstring | tests/unit/test_daemon_logger.py:1-1 | ctx=<module> >>>
BotDaemon 日志过滤测试。
<<< END U013743 >>>
<<< UNIT U013744 | py-comment | tests/unit/test_i18n_cmd_params.py:11-13 >>>
# 以键名作为参数传入、由被调方统一补上 cmd 的调用点。
# issue_code() 接收 prompt_key 后在内部构造 ActionText，调用侧只写键名，
# 逐调用点扫描无从分辨，故列为已知例外。
<<< END U013744 >>>
<<< UNIT U013745 | py-comment | tests/unit/test_i18n_cmd_params.py:21-21 >>>
# 上述键的 cmd 实际由该文件中的 issue_code() 补上
<<< END U013745 >>>
<<< UNIT U013746 | py-comment | tests/unit/test_i18n_cmd_params.py:26-26 >>>
# 以键名字面量为锚点，向前找到本次调用的左括号，再向后按括号配平找到右括号。
<<< END U013746 >>>
<<< UNIT U013747 | py-comment | tests/unit/test_i18n_cmd_params.py:92-93 >>>
# 白名单会掩盖真实的遗漏传参，故要求其对应的参数补充代码仍在位——issue_code() 一旦不再构造 ActionText，
# 此处即失效。逐条报明缘由而不笼统忽略异常——读不到文件若被归类为检查不成立，白名单便形同虚设。
<<< END U013747 >>>
<<< UNIT U013748 | py-comment | tests/unit/test_i18n_cmd_params.py:103-103 >>>
# 白名单中的键须确实作为 prompt_key 流向该函数，而非无人问津
<<< END U013748 >>>
<<< UNIT U013749 | py-comment | tests/unit/test_i18n_cmd_params.py:113-113 >>>
# 改文案却忘了改调用点时，该键会成为孤儿，渲染出的仍是字面量。
<<< END U013749 >>>
<<< UNIT U013750 | py-docstring | tests/unit/test_i18n_cmd_params.py:1-1 | ctx=<module> >>>
i18n 文案与调用点的参数一致性测试。
<<< END U013750 >>>
<<< UNIT U013751 | py-docstring | tests/unit/test_i18n_cmd_params.py:127-127 | ctx=test_i18n_cmd_params >>>
i18n: ${cmd} 参数传递一致性测试
<<< END U013751 >>>
<<< UNIT U013752 | py-comment | tests/unit/test_multi_instance.py:33-33 >>>
# 目录名 → 平台展示名。onebot 与 milky 都为 "QQ"，因为二者是同一批账号与场景数据的两种协议接入。
<<< END U013752 >>>
<<< UNIT U013753 | py-comment | tests/unit/test_multi_instance.py:140-140 >>>
# 显式传参生成实例名，不得改动类属性
<<< END U013753 >>>
<<< UNIT U013754 | py-comment | tests/unit/test_multi_instance.py:163-163 >>>
# 前缀只差一个字符时不误替换客户端段
<<< END U013754 >>>
<<< UNIT U013755 | py-comment | tests/unit/test_multi_instance.py:166-166 >>>
# 显式给出的两段优先于推导
<<< END U013755 >>>
<<< UNIT U013756 | py-comment | tests/unit/test_multi_instance.py:172-172 >>>
# 平台进程取不到平台名（server、测试桩）时回退到 client_name
<<< END U013756 >>>
<<< UNIT U013757 | py-comment | tests/unit/test_multi_instance.py:199-199 >>>
# 实例表不存在时回退到基础表。enable 例外，不回退
<<< END U013757 >>>
<<< UNIT U013758 | py-comment | tests/unit/test_multi_instance.py:207-207 >>>
# 模块配置与全局配置不参与实例作用域
<<< END U013758 >>>
<<< UNIT U013759 | py-comment | tests/unit/test_multi_instance.py:212-212 >>>
# 已指名实例表时不再二次拼接
<<< END U013759 >>>
<<< UNIT U013760 | py-comment | tests/unit/test_multi_instance.py:216-216 >>>
# 写入与删除都只作用于实例表
<<< END U013760 >>>
<<< UNIT U013761 | py-comment | tests/unit/test_multi_instance.py:293-293 >>>
# 通配地址与具体地址争用同一端口
<<< END U013761 >>>
<<< UNIT U013762 | py-comment | tests/unit/test_multi_instance.py:298-298 >>>
# milky 的 qq_host 是远端服务地址，同端口不同主机不构成冲突
<<< END U013762 >>>
<<< UNIT U013763 | py-comment | tests/unit/test_multi_instance.py:360-360 >>>
# 适配器名含 `-` 会让 bot_<平台>-<实例> 的拆分产生歧义
<<< END U013763 >>>
<<< UNIT U013764 | py-comment | tests/unit/test_multi_instance.py:366-366 >>>
# 登录信息字段必须存在于某个配置模板类上，否则重复检查会静默失效
<<< END U013764 >>>
<<< UNIT U013765 | py-comment | tests/unit/test_multi_instance.py:386-386 >>>
# 缺少平台两段时只看前两项，平台级声明对该实例不生效，实例级声明仍然命中
<<< END U013765 >>>
<<< UNIT U013766 | py-comment | tests/unit/test_multi_instance.py:391-391 >>>
# exclude_from 的平台级声明同样覆盖实例
<<< END U013766 >>>
<<< UNIT U013767 | py-comment | tests/unit/test_multi_instance.py:434-434 >>>
# 升级前入队的旧会话没有平台两段，且 server 进程没有平台身份
<<< END U013767 >>>
<<< UNIT U013768 | py-docstring | tests/unit/test_multi_instance.py:465-465 | ctx=test_multi_instance >>>
阶段 1B: 多实例身份模型
<<< END U013768 >>>
<<< UNIT U013769 | py-comment | tests/unit/test_permission_groups.py:154-154 >>>
# OneBot 没有“管理员”以外的原生权限组，此类请求应被跳过，不发出无效调用
<<< END U013769 >>>
<<< UNIT U013770 | py-docstring | tests/unit/test_permission_groups.py:193-193 | ctx=test_permission_groups >>>
平台原生权限组能力、队列转换与 SDK 调用测试。
<<< END U013770 >>>
<<< UNIT U013771 | py-comment | tests/unit/test_platform_management.py:386-387 >>>
# Windows 不允许 TemporaryDirectory 删除仍被占用的媒体文件。
# 测试完成取样检查后主动关闭，避免清理异常掩盖实际失败结果。
<<< END U013771 >>>
<<< UNIT U013772 | py-docstring | tests/unit/test_platform_management.py:1-1 | ctx=<module> >>>
平台成员管理操作的目标身份单元测试。
<<< END U013772 >>>
<<< UNIT U013773 | py-docstring | tests/unit/test_platform_management.py:682-682 | ctx=test_platform_management >>>
平台管理操作必须作用于显式指定的成员。
<<< END U013773 >>>
<<< UNIT U013774 | py-comment | tests/unit/test_platform_member_events.py:27-27 >>>
# 只校验声明过的字段，平台后续追加事件字段时不会误报。
<<< END U013774 >>>
<<< UNIT U013775 | py-docstring | tests/unit/test_platform_member_events.py:1-1 | ctx=<module> >>>
各平台成员加入事件转换测试。
<<< END U013775 >>>
<<< UNIT U013776 | py-docstring | tests/unit/test_platform_memory.py:1-1 | ctx=<module> >>>
平台适配器的长期缓存、主动推送队列与输入状态生命周期测试。
<<< END U013776 >>>
<<< UNIT U013777 | py-docstring | tests/unit/test_platform_memory.py:358-358 | ctx=test_platform_memory >>>
平台侧长期运行内存的有界性与清理路径。
<<< END U013777 >>>
<<< UNIT U013778 | py-docstring | tests/unit/test_platform_shutdown.py:1-1 | ctx=<module> >>>
平台客户端关闭流程单元测试。
<<< END U013778 >>>
<<< UNIT U013779 | py-docstring | tests/unit/test_platform_shutdown.py:377-377 | ctx=test_platform_shutdown >>>
平台退出时必须释放核心客户端与 SDK 资源。
<<< END U013779 >>>
<<< UNIT U013780 | py-docstring | tests/unit/test_promote_docker.py:85-85 | ctx=test_promote_docker >>>
稳定 Docker 镜像晋升发布（promotion）版本与错误处理验证。
<<< END U013780 >>>
<<< UNIT U013781 | py-docstring | tests/unit/test_publish_registry.py:357-357 | ctx=test_publish_registry >>>
发布产物、增量账本与渠道隔离验证。
<<< END U013781 >>>
<<< UNIT U013782 | py-docstring | tests/unit/test_registry_release.py:100-100 | ctx=test_registry_release >>>
tools.verify_registry_release: 发布索引核对测试
<<< END U013782 >>>
<<< UNIT U013783 | py-comment | tools/build_local_index.py:29-29 >>>
# Windows 控制台默认 cp1252，中文输出会抛 UnicodeEncodeError。
<<< END U013783 >>>
<<< UNIT U013784 | py-inline-comment | tools/build_local_index.py:119-119 >>>
# noqa: A002 - 覆盖父类签名
<<< END U013784 >>>
<<< UNIT U013785 | py-comment | tools/build_local_index.py:122-122 >>>
# 服务根目录取构建时解析出的绝对路径，确保工作目录变化时不会悄悄指向另一棵目录树。
<<< END U013785 >>>
<<< UNIT U013786 | py-comment | tools/build_registry.py:53-53 >>>
# manifest 的 schema 与分发默认值，与 core.registry 的 PackageManifest、MANIFEST_SCHEMA 一致。
<<< END U013786 >>>
<<< UNIT U013787 | py-comment | tools/build_registry.py:61-61 >>>
# 模块简介的 locale 键按序取首个命中，其中 desc 是 module() 的 desc= 所指向的键，help 是模块级帮助首行。
<<< END U013787 >>>
<<< UNIT U013788 | py-comment | tools/build_registry.py:64-64 >>>
# manifest 未进入 PackageManifest 的字段若清单里写了就直接读取，没写则留空。
<<< END U013788 >>>
<<< UNIT U013789 | py-comment | tools/build_registry.py:67-67 >>>
# A.3 未列出的两个键，承载本工具新增的构建产物定位信息。
<<< END U013789 >>>
<<< UNIT U013790 | py-comment | tools/build_registry.py:85-85 >>>
# wheel 文件名按 PEP 427 把包名里的非字母数字字符替换为下划线。
<<< END U013790 >>>
<<< UNIT U013791 | py-comment | tools/build_registry.py:378-378 >>>
# import_path 末段是包名，其上各级依次是 modules 与 akaribot 命名空间根。
<<< END U013791 >>>
<<< UNIT U013792 | py-comment | tools/build_registry.py:489-489 >>>
# name 取 entry point 名，与注册名可以无关（threedsdb 包注册的是 3dsdb）。
<<< END U013792 >>>
<<< UNIT U013793 | py-comment | tools/build_registry.py:535-535 >>>
# 已安装视图的 modules 字段对适配器为命名空间名，故适配器只比对 entry point 名。
<<< END U013793 >>>
<<< UNIT U013794 | py-docstring | tools/build_registry.py:94-94 | ctx=ConfigError >>>
workspace 或包元数据不满足生成 registry 所需的结构。
<<< END U013794 >>>
<<< UNIT U013795 | py-docstring | tools/build_registry.py:124-124 | ctx=load_toml >>>
读取 TOML 文件。
<<< END U013795 >>>
<<< UNIT U013796 | py-docstring | tools/build_registry.py:130-130 | ctx=workspace_pyprojects >>>
按根 pyproject 的 members glob 展开成员清单，排除 exclude。
<<< END U013796 >>>
<<< UNIT U013797 | py-docstring | tools/build_registry.py:240-240 | ctx=provides >>>
条目声明的可安装单元，模块包取清单的 provides_modules，适配器取自身名字。
<<< END U013797 >>>
<<< UNIT U013798 | py-docstring | tools/build_registry.py:276-276 | ctx=order_summaries >>>
简介按语言代码排序，默认 locale 置首，保证同一输入产出同一字节序列。
<<< END U013798 >>>
<<< UNIT U013799 | py-docstring | tools/build_registry.py:312-312 | ctx=as_str_list >>>
把清单里的序列字段规整为字符串列表，单值按一元列表处理。
<<< END U013799 >>>
<<< UNIT U013800 | py-docstring | tools/build_registry.py:319-319 | ctx=manifest_sequences >>>
读清单里可选的序列字段，缺项为空列表。
<<< END U013800 >>>
<<< UNIT U013801 | py-docstring | tools/build_registry.py:348-348 | ctx=build_entry >>>
由包元数据构造一个 registry 条目，键序固定以便逐字节比较。
<<< END U013801 >>>
<<< UNIT U013802 | py-docstring | tools/build_registry.py:374-374 | ctx=core_api_version >>>
从 core 源码静态取 CORE_API_VERSION，作为 ``api_version`` 的唯一来源。
<<< END U013802 >>>
<<< UNIT U013803 | py-docstring | tools/build_registry.py:390-390 | ctx=resolve_generated_at >>>
取内容时间戳，按显式参数、SOURCE_DATE_EPOCH、HEAD 提交时间依次回退。
<<< END U013803 >>>
<<< UNIT U013804 | py-docstring | tools/build_registry.py:415-415 | ctx=build_registry >>>
组装完整 registry 结构。
<<< END U013804 >>>
<<< UNIT U013805 | py-docstring | tools/build_registry.py:452-452 | ctx=check_manifest_sources >>>
核对清单的 provides_modules 与源码里实际注册的模块名，防止清单不同步。
<<< END U013805 >>>
<<< UNIT U013806 | py-docstring | tools/build_registry.py:469-469 | ctx=self_check >>>
结构校验，检查顶层键与 core 段键序、条目必填字段、提供的名字非空、包名唯一。
<<< END U013806 >>>
<<< UNIT U013807 | py-docstring | tools/build_registry.py:506-506 | ctx=installed_registry >>>
在目标解释器里运行 core 的清单入口，获取已安装包视图用于交叉核对。
<<< END U013807 >>>
<<< UNIT U013808 | py-docstring | tools/build_registry.py:517-517 | ctx=check_against_installed >>>
交叉核对 registry 与已安装包视图的包名、entry point 名与提供的模块名。
<<< END U013808 >>>
<<< UNIT U013809 | py-docstring | tools/build_registry.py:546-546 | ctx=dumps >>>
序列化为稳定文本，固定缩进、不转义非 ASCII、末尾换行。
<<< END U013809 >>>
<<< UNIT U013810 | py-docstring | tools/build_registry.py:551-551 | ctx=write_output >>>
原子写文件，避免 CI 中途失败留下半份 registry.json。
<<< END U013810 >>>
<<< UNIT U013811 | py-docstring | tools/build_registry.py:594-594 | ctx=describe >>>
生成一行运行摘要，供 stderr 使用。
<<< END U013811 >>>
<<< UNIT U013812 | py-docstring | tools/build_registry.py:604-604 | ctx=build_parser >>>
命令行入口参数。
<<< END U013812 >>>
<<< UNIT U013813 | py-docstring | tools/build_registry.py:629-629 | ctx=main >>>
入口。返回进程退出码，0 表示生成的 registry 通过全部自检。
<<< END U013813 >>>
<<< UNIT U013814 | py-comment | tools/changed_packages.py:41-41 >>>
# core 是公共接口层，它的改动影响全部包，矩阵随即转为全量。
<<< END U013814 >>>
<<< UNIT U013815 | py-comment | tools/changed_packages.py:45-45 >>>
# 全局变更涵盖根目录配置、锁文件及整个仓库共用的工具，都会改变每个包的构建与测试前提。
<<< END U013815 >>>
<<< UNIT U013816 | py-comment | tools/changed_packages.py:49-49 >>>
# 文档类路径不进入任何 wheel，也不构成任何包的测试前提，故不触发构建。
<<< END U013816 >>>
<<< UNIT U013817 | py-comment | tools/changed_packages.py:54-54 >>>
# 人类可读输出里触发点的显示上限，避免一次大范围改动刷屏。
<<< END U013817 >>>
<<< UNIT U013818 | py-docstring | tools/changed_packages.py:59-59 | ctx=ConfigError >>>
根 pyproject 或成员 pyproject 不满足检查所需的结构。
<<< END U013818 >>>
<<< UNIT U013819 | py-docstring | tools/changed_packages.py:99-99 | ctx=load_toml >>>
读取 TOML 文件。
<<< END U013819 >>>
<<< UNIT U013820 | py-docstring | tools/changed_packages.py:105-105 | ctx=discover_members >>>
按根 pyproject 的 members glob 展开成员，包名取各成员自己的 [project].name。
<<< END U013820 >>>
<<< UNIT U013821 | py-docstring | tools/changed_packages.py:140-140 | ctx=resolve_commit >>>
把引用解析为提交 SHA。解析不了返回 None。
<<< END U013821 >>>
<<< UNIT U013822 | py-docstring | tools/changed_packages.py:149-149 | ctx=resolve_base >>>
取 base 与 head 的共同祖先。取不到时回退到 base 本身。
<<< END U013822 >>>
<<< UNIT U013823 | py-docstring | tools/changed_packages.py:158-158 | ctx=changed_files >>>
取 `git diff --name-only base..head` 的改动路径，仓库根目录相对 POSIX 形式。
<<< END U013823 >>>
<<< UNIT U013824 | py-docstring | tools/changed_packages.py:163-163 | ctx=package_directory >>>
从 packages/ 下的路径推断包目录，用于已不在 workspace 的包（删除、改名）。
<<< END U013824 >>>
<<< UNIT U013825 | py-docstring | tools/changed_packages.py:244-244 | ctx=print_matrix >>>
人类可读输出。
<<< END U013825 >>>
<<< UNIT U013826 | py-docstring | tools/changed_packages.py:263-263 | ctx=build_parser >>>
命令行入口参数。
<<< END U013826 >>>
<<< UNIT U013827 | py-docstring | tools/changed_packages.py:279-279 | ctx=main >>>
入口。返回进程退出码，0 表示检测完成。
<<< END U013827 >>>
<<< UNIT U013828 | py-docstring | tools/check_instance_lifecycle.py:1-1 | ctx=<module> >>>
在本机验证后台实例停止协议和进程树清理。
<<< END U013828 >>>
<<< UNIT U013829 | py-docstring | tools/check_instance_lifecycle.py:111-111 | ctx=main >>>
验证正常停止、强制停止和接管外部启动的实例。
<<< END U013829 >>>
<<< UNIT U013830 | py-docstring | tools/check_test_baseline.py:50-50 | ctx=Failure.line >>>
基准文件里的一行。
<<< END U013830 >>>
<<< UNIT U013831 | py-docstring | tools/check_test_baseline.py:140-140 | ctx=build_parser >>>
命令行入口参数。
<<< END U013831 >>>
<<< UNIT U013832 | py-docstring | tools/check_test_baseline.py:149-149 | ctx=main >>>
入口。返回进程退出码，0 表示失败的用例清单与基准按名称一一对应。
<<< END U013832 >>>
<<< UNIT U013833 | py-comment | tools/check_versions.py:41-42 >>>
# 不打入 wheel 的目录改动不要求升级版本，--strict 时该豁免失效。
# pyproject.toml 不在豁免内，因为依赖与入口点会写入 wheel 元数据，改动同样要发布新版本。
<<< END U013833 >>>
<<< UNIT U013834 | py-comment | tools/check_versions.py:45-45 >>>
# 报告里每个包的改动文件显示上限，超出只计数量。
<<< END U013834 >>>
<<< UNIT U013835 | py-docstring | tools/check_versions.py:50-50 | ctx=ConfigError >>>
根 pyproject 或成员 pyproject 不满足检查所需的结构。
<<< END U013835 >>>
<<< UNIT U013836 | py-docstring | tools/check_versions.py:90-90 | ctx=load_toml >>>
读取 TOML 文件。
<<< END U013836 >>>
<<< UNIT U013837 | py-docstring | tools/check_versions.py:96-96 | ctx=discover_members >>>
按根 pyproject 的 members glob 展开成员，读各成员自己的 [project] 名字与版本。
<<< END U013837 >>>
<<< UNIT U013838 | py-docstring | tools/check_versions.py:137-137 | ctx=resolve_commit >>>
把引用解析为提交 SHA。解析不了返回 None。
<<< END U013838 >>>
<<< UNIT U013839 | py-docstring | tools/check_versions.py:274-274 | ctx=compare_versions >>>
比较两侧版本。任一侧无法解析时返回 None。
<<< END U013839 >>>
<<< UNIT U013840 | py-docstring | tools/check_versions.py:339-339 | ctx=print_finding >>>
打印一个包的结论及其改动文件。
<<< END U013840 >>>
<<< UNIT U013841 | py-docstring | tools/check_versions.py:357-357 | ctx=build_parser >>>
命令行入口参数。
<<< END U013841 >>>
<<< UNIT U013842 | py-docstring | tools/check_versions.py:380-380 | ctx=main >>>
入口。返回进程退出码，1 表示有违规，0 表示通过或仅提示。
<<< END U013842 >>>
<<< UNIT U013843 | py-comment | tools/clean_room_check.py:41-42 >>>
# CLI 组合名只安装 CLI wheel，安装后逐条运行基本检查命令。这条对应 P1-1（wheel 干净安装后不得缺少依赖）
# 与 P1-9（--version 可用）。tui --self-check 覆盖包内资源与样式表，冻结产物最容易在这里失败。
<<< END U013843 >>>
<<< UNIT U013844 | py-comment | tools/clean_room_check.py:53-53 >>>
# 发现阶段需要读取实例配置（真实用户也先运行 akaribot init），故探针自带一份最小配置。
<<< END U013844 >>>
<<< UNIT U013845 | py-comment | tools/clean_room_check.py:66-66 >>>
# Windows 控制台默认 cp1252，中文输出会抛 UnicodeEncodeError。
<<< END U013845 >>>
<<< UNIT U013846 | py-comment | tools/clean_room_check.py:72-72 >>>
# 检查脚本在新环境里执行，输出 JSON 供本工具判定。
<<< END U013846 >>>
<<< UNIT U013847 | py-inline-comment | tools/clean_room_check.py:219-219 >>>
# noqa: BLE001 - 单个分发失败记入清单后统一判定
<<< END U013847 >>>
<<< UNIT U013848 | py-inline-comment | tools/clean_room_check.py:257-257 >>>
# noqa: BLE001 - 检查只需打印失败点
<<< END U013848 >>>
<<< UNIT U013849 | py-inline-comment | tools/clean_room_check.py:268-268 >>>
# noqa: BLE001 - 检查只需打印失败点
<<< END U013849 >>>
<<< UNIT U013850 | py-comment | tools/clean_room_check.py:275-275 >>>
# 链接带 #sha256 片段，取文件本身时要去掉，否则会被当成路径的一部分。
<<< END U013850 >>>
<<< UNIT U013851 | py-inline-comment | tools/clean_room_check.py:283-283 >>>
# noqa: BLE001 - 检查只需打印失败点
<<< END U013851 >>>
<<< UNIT U013852 | py-comment | tools/clean_room_check.py:379-379 >>>
# 内部包来自被测索引，第三方依赖仍走正式 PyPI。同名冲突时按索引优先级解析。
<<< END U013852 >>>
<<< UNIT U013853 | py-comment | tools/clean_room_check.py:464-464 >>>
# 外部依赖从索引解析，内部约束同时限定到本次 wheel，防止远端版本掩盖源码遗漏。
<<< END U013853 >>>
<<< UNIT U013854 | py-comment | tools/clean_room_check.py:664-664 >>>
# 静态索引没有本地产物集，只能运行“按索引安装”的两种组合。
<<< END U013854 >>>
<<< UNIT U013855 | py-comment | tools/clean_room_check.py:679-679 >>>
# CLI 组合只安装 CLI wheel，与发现阶段的探针无关，单独走一条检查路径。
<<< END U013855 >>>
<<< UNIT U013856 | py-inline-comment | tools/clean_room_check.py:686-686 >>>
# (包列表， extras)
<<< END U013856 >>>
<<< UNIT U013857 | py-comment | tools/codemod_core_api.py:31-31 >>>
# 适配器另有自己的公开接口，其中的符号只供适配器使用，模块包导入它会被 B3 拦截。
<<< END U013857 >>>
<<< UNIT U013858 | py-comment | tools/codemod_core_api.py:34-35 >>>
# 必须保持窄导入的文件不改写，因为公开接口导入期即展开，会把 web_render 连同 playwright 引入
# ``sys.modules``，而 Telegram 适配器专门保证“只导入 message_builder 不连带引入 web_render”。
<<< END U013858 >>>
<<< UNIT U013859 | py-inline-comment | tools/codemod_core_api.py:94-94 >>>
# noqa: BLE001 - 导入不了的模块一律不改写
<<< END U013859 >>>
<<< UNIT U013860 | py-docstring | tools/codemod_core_api.py:147-147 | ctx=plan_file.destination >>>
该符号应改用哪个公开接口。两个公开接口都没有时返回 None。
<<< END U013860 >>>
<<< UNIT U013861 | py-docstring | tools/codemod_core_api.py:205-205 | ctx=main >>>
入口。返回进程退出码。
<<< END U013861 >>>
<<< UNIT U013862 | py-comment | tools/codemod_namespace.py:24-24 >>>
# 扫描范围为物理移动后仍可能引用旧命名空间的 Python 源码。example/ 是脚手架样例，不在 packages/ 下。
<<< END U013862 >>>
<<< UNIT U013863 | py-comment | tools/codemod_namespace.py:34-34 >>>
# 旧→新前缀映射，按段匹配且长前缀优先。core.tester 已移出 core 成为独立包，是 core.* 的例外。
<<< END U013863 >>>
<<< UNIT U013864 | py-comment | tools/codemod_namespace.py:42-42 >>>
# 新→旧前缀映射，用于把 packages 下的真实模块路径反推成旧点分路径。
<<< END U013864 >>>
<<< UNIT U013865 | py-comment | tools/codemod_namespace.py:50-50 >>>
# 单段旧根包名同时充当 JSON 键、数据库字段名与文件系统目录名，无法与模块路径区分，故不入白名单。
<<< END U013865 >>>
<<< UNIT U013866 | py-comment | tools/codemod_namespace.py:55-55 >>>
# 直接 import 绑定旧根包名，改写后绑定名变为 akaribot，引用处必须一并调整，属人工事项。
<<< END U013866 >>>
<<< UNIT U013867 | py-comment | tools/codemod_namespace.py:58-58 >>>
# i18n 调用上下文中的点分字符串是文案键，即使与真实模块路径同名也不改写。
<<< END U013867 >>>
<<< UNIT U013868 | py-comment | tools/codemod_namespace.py:63-63 >>>
# patch 调用中承载点分路径的实参形式包括位置参数下标与关键字名。
<<< END U013868 >>>
<<< UNIT U013869 | py-comment | tools/codemod_namespace.py:69-69 >>>
# f-string 中出现的旧命名空间形态指字面量片段的根包名之后紧跟标识符或插值，以排除句末的散文误报。
<<< END U013869 >>>
<<< UNIT U013870 | py-comment | tools/codemod_namespace.py:125-125 >>>
# 模块路径与逐级向上的包路径都算真实路径。
<<< END U013870 >>>
<<< UNIT U013871 | py-inline-comment | tools/codemod_namespace.py:170-170 >>>
# noqa: BLE001 - 片段仅用于报告，取不到源码时回退到占位文本
<<< END U013871 >>>
<<< UNIT U013872 | py-comment | tools/codemod_namespace.py:226-226 >>>
# 位置元数据以原始节点为键，遍历产出的新节点不在其中。
<<< END U013872 >>>
<<< UNIT U013873 | py-inline-comment | tools/codemod_namespace.py:286-286 >>>
# noqa: BLE001 - 无法求值的字面量不参与改写
<<< END U013873 >>>
<<< UNIT U013874 | py-inline-comment | tools/codemod_namespace.py:359-359 >>>
# noqa: BLE001 - 单个文件异常不中断整轮改写
<<< END U013874 >>>
<<< UNIT U013875 | py-inline-comment | tools/codemod_namespace.py:366-366 >>>
# noqa: BLE001 - 单个文件异常不中断整轮改写
<<< END U013875 >>>
<<< UNIT U013876 | py-docstring | tools/codemod_namespace.py:102-102 | ctx=remap_old_to_new >>>
旧点分路径转新点分路径，不属于旧命名空间时返回 None。
<<< END U013876 >>>
<<< UNIT U013877 | py-docstring | tools/codemod_namespace.py:107-107 | ctx=remap_new_to_old >>>
新点分路径反推旧点分路径，不属于旧命名空间时返回 None。
<<< END U013877 >>>
<<< UNIT U013878 | py-docstring | tools/codemod_namespace.py:112-112 | ctx=build_known >>>
遍历 packages/**/akaribot，反推出旧点分模块路径全集。
<<< END U013878 >>>
<<< UNIT U013879 | py-docstring | tools/codemod_namespace.py:134-134 | ctx=longest_known_prefix >>>
取 text 中命中白名单的最长点分前缀，无命中返回 None。
<<< END U013879 >>>
<<< UNIT U013880 | py-docstring | tools/codemod_namespace.py:178-178 | ctx=FileOutcome >>>
单文件改写结果，字段直接进入报告与汇总。
<<< END U013880 >>>
<<< UNIT U013881 | py-docstring | tools/codemod_namespace.py:188-188 | ctx=NamespaceTransformer >>>
改写 import 语句，并按白名单改写字符串字面量。
<<< END U013881 >>>
<<< UNIT U013882 | py-docstring | tools/codemod_namespace.py:339-339 | ctx=iter_target_files >>>
枚举待扫描的 Python 文件，排除缓存目录与工具自身。
<<< END U013882 >>>
<<< UNIT U013883 | py-docstring | tools/codemod_namespace.py:354-354 | ctx=process_file >>>
改写单个文件。解析失败记入 outcome.failure 并跳过。
<<< END U013883 >>>
<<< UNIT U013884 | py-comment | tools/codemod_private_docstrings.py:30-30 >>>
# 内嵌的第三方副本保持上游原样。
<<< END U013884 >>>
<<< UNIT U013885 | py-comment | tools/codemod_private_docstrings.py:32-32 >>>
# docstring 里属于结构化字段而非散文的行。
<<< END U013885 >>>
<<< UNIT U013886 | py-comment | tools/codemod_private_docstrings.py:133-133 >>>
# 删除后紧跟的空行一并吃掉，避免函数体以空行开头。
<<< END U013886 >>>
<<< UNIT U013887 | py-comment | tools/codemod_private_docstrings.py:138-138 >>>
# 注释放在 docstring 原来的位置（函数体内），缩进取函数体而非 def 行。
<<< END U013887 >>>
<<< UNIT U013888 | py-comment | tools/codemod_private_docstrings.py:145-145 >>>
# 只剩 docstring 的定义删空后会语法错误，补 pass。缩进取函数体而非 def 行。
<<< END U013888 >>>
<<< UNIT U013889 | py-docstring | tools/codemod_private_docstrings.py:68-68 | ctx=iter_sources >>>
枚举待处理的 Python 文件。
<<< END U013889 >>>
<<< UNIT U013890 | py-docstring | tools/codemod_private_docstrings.py:84-84 | ctx=docstring_node >>>
取该定义的首条语句——若它是 docstring 则返回，否则返回 ``None``。
<<< END U013890 >>>
<<< UNIT U013891 | py-docstring | tools/codemod_private_docstrings.py:158-158 | ctx=main >>>
入口。返回进程退出码。
<<< END U013891 >>>
<<< UNIT U013892 | py-comment | tools/lint_boundaries.py:56-56 >>>
# 收录范围为 packages/ 下的全部分发源码。tests/ 与 tools/ 依赖全部层，不在约束内。
<<< END U013892 >>>
<<< UNIT U013893 | py-comment | tools/lint_boundaries.py:59-59 >>>
# 分发清单涵盖 packages/<dist>/ 与 packages/<group>/<dist>/ 两层。容器目录（adapters、modules）无 pyproject。
<<< END U013893 >>>
<<< UNIT U013894 | py-comment | tools/lint_boundaries.py:62-62 >>>
# 命名空间根标志对应位于 <dist>/akaribot/<layer>/… 的源码，据此定位分层与包路径。
<<< END U013894 >>>
<<< UNIT U013895 | py-comment | tools/lint_boundaries.py:64-64 >>>
# 分层取命名空间根之后的第一段目录名。akaribot.testing 不在受约束的三层内，规则不适用。
<<< END U013895 >>>
<<< UNIT U013896 | py-comment | tools/lint_boundaries.py:68-68 >>>
# 命名空间根与两个共享分层目录出现 __init__.py 会把命名空间包截断，故按“akaribot 之后的目录后缀”禁。
<<< END U013896 >>>
<<< UNIT U013897 | py-comment | tools/lint_boundaries.py:70-70 >>>
# 官方模块包的判定前缀，T4.6 #2 的 error 升级与 #7 都只看这一层目录。
<<< END U013897 >>>
<<< UNIT U013898 | py-comment | tools/lint_boundaries.py:76-76 >>>
# core 包自身的目录。其 bundled 模块不计入“模块包是否经过公开接口”的观察值。
<<< END U013898 >>>
<<< UNIT U013899 | py-comment | tools/lint_boundaries.py:79-79 >>>
# 模块包对外承诺的路径只有 akaribot.modules.<x>.api，包根目录与其余子路径都算内部实现。
<<< END U013899 >>>
<<< UNIT U013900 | py-comment | tools/lint_boundaries.py:81-81 >>>
# 适配器专用接口，模块导入它多半是在做本应交给适配器的事（T4.7(d)）。
<<< END U013900 >>>
<<< UNIT U013901 | py-comment | tools/lint_boundaries.py:85-85 >>>
# B8 的导出符号来源于公开接口模块、实现模块与适配器接口。
<<< END U013901 >>>
<<< UNIT U013902 | py-comment | tools/lint_boundaries.py:105-106 >>>
# B1 的基础级别为 warn，因为第三方包跨模块取内部路径可能确有需要。包归属为官方（OFFICIAL_MODULES_PREFIX）
# 时该条升级为 error，级别随命中一起记录在 Violation 上，故本表只存静态基础级别。
<<< END U013902 >>>
<<< UNIT U013903 | py-comment | tools/lint_boundaries.py:527-527 >>>
# B10 与 B1 独立，官方包连对方的 .api 也不许依赖（T4.6 #7）。
<<< END U013903 >>>
<<< UNIT U013904 | py-comment | tools/lint_boundaries.py:548-549 >>>
# 允许的位置是冻结感知的 CLI 自调用（冻结时它是二进制、非冻结时是解释器加 -m 模块名）。
# 反之把它当解释器启动实例进程，冻结后会重新调起 CLI，必须经 system_python()。
<<< END U013904 >>>
<<< UNIT U013905 | py-inline-comment | tools/lint_boundaries.py:551-551 >>>
# 各页的 cli_argv 构造
<<< END U013905 >>>
<<< UNIT U013906 | py-inline-comment | tools/lint_boundaries.py:552-552 >>>
# 脚手架末尾自调用 CLI
<<< END U013906 >>>
<<< UNIT U013907 | py-inline-comment | tools/lint_boundaries.py:553-553 >>>
# system_python() 在非冻结时就是可用解释器，冻结时才改搜索
<<< END U013907 >>>
<<< UNIT U013908 | py-comment | tools/lint_boundaries.py:555-555 >>>
# CLI 的 tests/ 不在 wheel 内（hatchling 只收 akaribot/），永远不会被冻结，本规则不适用。
<<< END U013908 >>>
<<< UNIT U013909 | py-comment | tools/lint_boundaries.py:611-612 >>>
# core 自带的 bundled 模块在路径上也属模块层，但它们随 core 同版本发布、与 core 内部同步
# 重构，不属于“模块包绑定 core 内部目录”。算进来会让观察值长期停在几百。
<<< END U013909 >>>
<<< UNIT U013910 | py-comment | tools/lint_boundaries.py:700-701 >>>
# git 的 pathspec 里不含斜杠的模式按全路径通配，如 `*.py` 能命中任意深度，
# 而字面量 `pyproject.toml` 只命中仓库根目录，故嵌套清单用 `*pyproject.toml`。
<<< END U013910 >>>
<<< UNIT U013911 | py-comment | tools/lint_boundaries.py:756-756 >>>
# 空文件（新建的 __init__.py 就是这种）也要给出第 1 行，否则 B7 在 --diff 下会漏。
<<< END U013911 >>>
<<< UNIT U013912 | py-docstring | tools/lint_boundaries.py:180-180 | ctx=Violation.key >>>
基准文件的稳定键。不含行号，代码移动后仍能命中豁免。
<<< END U013912 >>>
<<< UNIT U013913 | py-docstring | tools/lint_boundaries.py:210-210 | ctx=Workspace >>>
一次检查共用的整个仓库索引。
<<< END U013913 >>>
<<< UNIT U013914 | py-docstring | tools/lint_boundaries.py:217-217 | ctx=Workspace.dist_for >>>
取包含该文件的分发。嵌套时取最长匹配的分发目录。
<<< END U013914 >>>
<<< UNIT U013915 | py-docstring | tools/lint_boundaries.py:226-226 | ctx=iter_source_files >>>
枚举需要检查的 Python 文件，按路径排序。
<<< END U013915 >>>
<<< UNIT U013916 | py-docstring | tools/lint_boundaries.py:240-240 | ctx=iter_pyproject_files >>>
枚举 packages/ 下各分发的 pyproject.toml，按路径排序。
<<< END U013916 >>>
<<< UNIT U013917 | py-docstring | tools/lint_boundaries.py:248-248 | ctx=normalize_dist_name >>>
按 PEP 503 规范化包名，转小写并把 -、_、. 统一为 -。
<<< END U013917 >>>
<<< UNIT U013918 | py-docstring | tools/lint_boundaries.py:284-284 | ctx=load_distributions >>>
读取各分发的名字、依赖、提供的模块段与适配器 entry point 等元数据。
<<< END U013918 >>>
<<< UNIT U013919 | py-docstring | tools/lint_boundaries.py:331-331 | ctx=extract_all_names >>>
取模块级 `__all__ = [...]` 中的字符串字面量。`*_base.__all__` 这类星号元素由调用方并入。
<<< END U013919 >>>
<<< UNIT U013920 | py-docstring | tools/lint_boundaries.py:358-358 | ctx=load_core_api_names >>>
获取 akaribot.core.api 承诺的导出符号集合，通过 AST 解析 __all__ 字面量，不导入 core。
<<< END U013920 >>>
<<< UNIT U013921 | py-docstring | tools/lint_boundaries.py:384-384 | ctx=load_workspace >>>
一次性建立包索引、模块段索引与 core 公开接口导出符号集合。
<<< END U013921 >>>
<<< UNIT U013922 | py-docstring | tools/lint_boundaries.py:466-466 | ctx=under >>>
点分路径是否等于 prefix 或位于其下。
<<< END U013922 >>>
<<< UNIT U013923 | py-docstring | tools/lint_boundaries.py:471-471 | ctx=module_owner >>>
取 akaribot.modules.<x> 中的 <x>。不在该前缀下时返回 None。
<<< END U013923 >>>
<<< UNIT U013924 | py-docstring | tools/lint_boundaries.py:478-478 | ctx=b1_level >>>
B1 的级别对官方模块包升级为 error，其他（第三方在自己的仓库里复用本工具）保留 warn。
<<< END U013924 >>>
<<< UNIT U013925 | py-docstring | tools/lint_boundaries.py:485-485 | ctx=check_declared_dependency >>>
规则 B6，要求跨模块导入须在自身 pyproject 的 dependencies 中声明目标包。
<<< END U013925 >>>
<<< UNIT U013926 | py-docstring | tools/lint_boundaries.py:513-513 | ctx=check_module_import >>>
规则 B1、B2、B3、B6、B8、B10，定义模块包侧的导入限制。
<<< END U013926 >>>
<<< UNIT U013927 | py-docstring | tools/lint_boundaries.py:538-538 | ctx=check_import >>>
对单个导入语句施加全部规则。
<<< END U013927 >>>
<<< UNIT U013928 | py-docstring | tools/lint_boundaries.py:648-648 | ctx=check_adapter_entry_points >>>
规则 B9，检查适配器 entry point 名是否含 '-' 而与多实例名分隔符冲突（T1B.1）。
<<< END U013928 >>>
<<< UNIT U013929 | py-docstring | tools/lint_boundaries.py:676-676 | ctx=load_baseline >>>
读取基准豁免键。
<<< END U013929 >>>
<<< UNIT U013930 | py-docstring | tools/lint_boundaries.py:732-732 | ctx=untracked_scope >>>
未跟踪的新文件整文件计入检查范围。
<<< END U013930 >>>
<<< UNIT U013931 | py-docstring | tools/lint_boundaries.py:763-763 | ctx=level_label >>>
取规则的级别标签，为静态级别或该规则命中里实际出现过的级别（B1 两种都可能）。
<<< END U013931 >>>
<<< UNIT U013932 | py-docstring | tools/lint_boundaries.py:769-769 | ctx=generate_baseline >>>
把当前全部违规写入基准文件。
<<< END U013932 >>>
<<< UNIT U013933 | py-docstring | tools/lint_boundaries.py:788-788 | ctx=main >>>
入口。返回进程退出码，0 表示无基准外的违规。
<<< END U013933 >>>
<<< UNIT U013934 | py-comment | tools/lint_comments.py:27-28 >>>
# 收录本仓库自有 Python 源码，即 packages/ 下的分发源码与 tests/、templates/、tools/。
# 第三方内嵌库与迁移产物不在约束内。
<<< END U013934 >>>
<<< UNIT U013935 | py-comment | tools/lint_comments.py:32-32 >>>
# 内嵌的第三方副本保持上游原样，不按本仓库的书写规范改写。
<<< END U013935 >>>
<<< UNIT U013936 | py-comment | tools/lint_comments.py:35-35 >>>
# 工具指令注释不构成文档，不予检查。
<<< END U013936 >>>
<<< UNIT U013937 | py-comment | tools/lint_comments.py:42-43 >>>
# 规则 5 检查装饰性分隔注释。同一分隔字符在首尾各出现三次以上，中间允许夹带标题。
# 纯字符行与“### 标题”式 Markdown 标题不在此列。
<<< END U013937 >>>
<<< UNIT U013938 | py-comment | tools/lint_comments.py:48-48 >>>
# 规则 4 检查口语词。只收录在本仓库语境下无歧义的搭配，避免伤及正常用词（如“处理”“弄清”）。
<<< END U013938 >>>
<<< UNIT U013939 | py-comment | tools/lint_comments.py:62-63 >>>
# 规则 2 检查第一/第二人称。只收录原文明确点名的词，避免“我”在其他语境下的误判。
# “关于我们”是帮助菜单里的入口名，不是叙述人称。
<<< END U013939 >>>
<<< UNIT U013940 | py-comment | tools/lint_comments.py:67-68 >>>
# 规则 3 检查语气词与情绪标点。省略号只认中文双省略号、四个以上英文点与行尾三点，
# 以免把代码占位符（`<...>`、`[...]`）与引用文本里的标点算作情绪标点。
<<< END U013940 >>>
<<< UNIT U013941 | py-comment | tools/lint_comments.py:77-77 >>>
# 条件连词之后的省略号属于“等等”义，不视为情绪标点。
<<< END U013941 >>>
<<< UNIT U013942 | py-comment | tools/lint_comments.py:79-79 >>>
# 引号内是面向用户的原文（如“正在输入……”），其中的省略号属于该文案本身。
<<< END U013942 >>>
<<< UNIT U013943 | py-comment | tools/lint_comments.py:81-82 >>>
# 省略号被用作占位符标记（整行只有它，或它单独占一段）时不算情绪标点。列举后的“……”
# 是“等等”义（`fc`、`fs`……），同样不算。
<<< END U013943 >>>
<<< UNIT U013944 | py-comment | tools/lint_comments.py:85-85 >>>
# 规则 8 检查时间性表述。
<<< END U013944 >>>
<<< UNIT U013945 | py-comment | tools/lint_comments.py:88-89 >>>
# 规则 8 检查变更叙述。只收录无歧义地指向“已经不存在的那种写法”的词。
# “旧版本号”“旧库”“旧数据”指迁移历史数据，属规范明确保留的兼容说明，不在其中。
<<< END U013945 >>>
<<< UNIT U013946 | py-comment | tools/lint_comments.py:94-94 >>>
# 规则 9 检查中文里的半角标点。反引号包裹的代码片段与 Sphinx 字段（`:param x:`）先剔除。
<<< END U013946 >>>
<<< UNIT U013947 | py-comment | tools/lint_comments.py:97-97 >>>
# 形如 `种类:包名`、`(用例名, 类型, 消息)` 的取值格式说明属代码记号，不是中文句子里的标点。
<<< END U013947 >>>
<<< UNIT U013948 | py-comment | tools/lint_comments.py:99-99 >>>
# docstring 里的示例代码整行都不是散文，不按中文排版检查。
<<< END U013948 >>>
<<< UNIT U013949 | py-comment | tools/lint_comments.py:102-102 >>>
# 规则 10 检查中英文之间缺空格。数字与拉丁字母都算“西文”，但行内代码、URL、占位符先剔除。
<<< END U013949 >>>
<<< UNIT U013950 | py-comment | tools/lint_comments.py:104-104 >>>
# 整行不含中文时属外部引用文本（英文规范原文、英文 docstring），中文排版与长度规则都不适用。
<<< END U013950 >>>
<<< UNIT U013951 | py-comment | tools/lint_comments.py:106-106 >>>
# 双下划线方法属语言协议，不是非公开 API。
<<< END U013951 >>>
<<< UNIT U013952 | py-comment | tools/lint_comments.py:111-111 >>>
# 规则 7 检查连续行注释块。规范允许单条说明写到三行，四行起视为应当抽函数或补文档。
<<< END U013952 >>>
<<< UNIT U013953 | py-comment | tools/lint_comments.py:114-114 >>>
# 行注释长度上限，与 Ruff 的 line-length 一致。
<<< END U013953 >>>
<<< UNIT U013954 | py-comment | tools/lint_comments.py:120-120 >>>
# 规则编号与说明，输出与基准文件共用。
<<< END U013954 >>>
<<< UNIT U013955 | py-comment | tools/lint_comments.py:347-347 >>>
# docstring 里的示例代码整行按代码看。不含中文的整行是外部引用文本，都不施加散文规则。
<<< END U013955 >>>
<<< UNIT U013956 | py-docstring | tools/lint_comments.py:165-165 | ctx=Violation.key >>>
基准文件的稳定键。不含行号，代码移动后仍能命中豁免。
<<< END U013956 >>>
<<< UNIT U013957 | py-docstring | tools/lint_comments.py:173-173 | ctx=iter_source_files >>>
枚举需要检查的 Python 文件，按路径排序。
<<< END U013957 >>>
<<< UNIT U013958 | py-docstring | tools/lint_comments.py:225-225 | ctx=is_checkable >>>
工具指令、shebang 与编码声明不参与检查。
<<< END U013958 >>>
<<< UNIT U013959 | py-docstring | tools/lint_comments.py:266-266 | ctx=check_comment >>>
对单条行注释施加规则 1~5、8~10。
<<< END U013959 >>>
<<< UNIT U013960 | py-docstring | tools/lint_comments.py:367-367 | ctx=check_comment_blocks >>>
规则 7，检查连续 3 行以上、且各行均无代码的行注释块。
<<< END U013960 >>>
<<< UNIT U013961 | py-docstring | tools/lint_comments.py:382-382 | ctx=check_file >>>
检查单个文件。
<<< END U013961 >>>
<<< UNIT U013962 | py-docstring | tools/lint_comments.py:399-399 | ctx=load_baseline >>>
读取基准豁免键。
<<< END U013962 >>>
<<< UNIT U013963 | py-docstring | tools/lint_comments.py:446-446 | ctx=generate_baseline >>>
把当前全部违规写入基准文件。
<<< END U013963 >>>
<<< UNIT U013964 | py-docstring | tools/lint_comments.py:460-460 | ctx=main >>>
入口。返回进程退出码，0 表示无基准外违规。
<<< END U013964 >>>
<<< UNIT U013965 | py-comment | tools/lint_versions.py:45-45 >>>
# 第 3 条只约束对 core 的写法。名字用规范化形式比较，大小写与下划线差异不参与判断。
<<< END U013965 >>>
<<< UNIT U013966 | py-comment | tools/lint_versions.py:65-65 >>>
# 依赖字符串在 pyproject 里以字面量出现，用于反向查找行号。跨行书写时回退到 dependencies 数组行。
<<< END U013966 >>>
<<< UNIT U013967 | py-comment | tools/lint_versions.py:68-68 >>>
# 报告保留原始书写形式，因为 SpecifierSet 的 str 会按字典序重排（如 >=0.1.0,<1.0 变成 <1.0,>=0.1.0）。
<<< END U013967 >>>
<<< UNIT U013968 | py-docstring | tools/lint_versions.py:73-73 | ctx=ConfigError >>>
根 pyproject 或成员 pyproject 不满足检查所需的结构。
<<< END U013968 >>>
<<< UNIT U013969 | py-docstring | tools/lint_versions.py:108-108 | ctx=Dependency.display >>>
报告用约束文本。
<<< END U013969 >>>
<<< UNIT U013970 | py-docstring | tools/lint_versions.py:136-136 | ctx=load_toml >>>
读取 TOML 文件。
<<< END U013970 >>>
<<< UNIT U013971 | py-docstring | tools/lint_versions.py:142-142 | ctx=member_pyprojects >>>
按根 pyproject 的 members glob 展开成员清单，排除 exclude。
<<< END U013971 >>>
<<< UNIT U013972 | py-docstring | tools/lint_versions.py:159-159 | ctx=discover_members >>>
读全部成员的 [project] 名字与版本，返回规范化名到成员的映射。
<<< END U013972 >>>
<<< UNIT U013973 | py-docstring | tools/lint_versions.py:195-195 | ctx=written_specifier >>>
取条目里约束部分的书写形式，环境标记与 direct reference 不算约束。
<<< END U013973 >>>
<<< UNIT U013974 | py-docstring | tools/lint_versions.py:222-222 | ctx=suggest_constraint >>>
给出与成员实际版本相容的区间写法，下界取实际版本，上界取下一个主版本。
<<< END U013974 >>>
<<< UNIT U013975 | py-docstring | tools/lint_versions.py:363-363 | ctx=build_parser >>>
命令行入口参数。
<<< END U013975 >>>
<<< UNIT U013976 | py-docstring | tools/lint_versions.py:386-386 | ctx=main >>>
入口。返回进程退出码，0 表示无 error。
<<< END U013976 >>>
<<< UNIT U013977 | py-docstring | tools/promote_docker.py:1-1 | ctx=<module> >>>
解析已构建的最高稳定产品镜像及其确切摘要。
<<< END U013977 >>>
<<< UNIT U013978 | py-comment | tools/publish_registry.py:42-42 >>>
# 索引根地址 + 包名 + 可选版本。省略版本时取该包的最新版本。
<<< END U013978 >>>
<<< UNIT U013979 | py-comment | tools/publish_registry.py:89-89 >>>
# 优先取响应头 Retry-After，缺失时用指数退避（30s 起，上限 300s）。
<<< END U013979 >>>
<<< UNIT U013980 | py-comment | tools/publish_registry.py:147-147 >>>
# 一次构建的全部产物 → 发行清单。后续上传、下载核验与安装都对照它。
<<< END U013980 >>>
<<< UNIT U013981 | py-docstring | tools/publish_registry.py:1-1 | ctx=<module> >>>
由 PyPI 已发布产物维护发布账本和稳定、预发布索引。
<<< END U013981 >>>
<<< UNIT U013982 | py-comment | tools/render_templates.py:25-25 >>>
# 占位值。模块名取纯小写与下划线，与模板 README 所述的限制一致。
<<< END U013982 >>>
<<< UNIT U013983 | py-comment | tools/render_templates.py:34-35 >>>
# 占位符形态为 [@name@]，两处替换都要做——路径占位符在复制目录时替换，
# 文本占位符在渲染内容时替换。
<<< END U013983 >>>
<<< UNIT U013984 | py-comment | tools/render_templates.py:38-38 >>>
# 未替换占位符的识别比替换宽松，任何 [@ ... @] 都算残留，包括名字不合规的拼写错误。
<<< END U013984 >>>
<<< UNIT U013985 | py-comment | tools/render_templates.py:145-145 >>>
# 默认会移除模板末尾的换行，产物将与本项目的 ruff format 结果不符。
<<< END U013985 >>>
<<< UNIT U013986 | py-docstring | tools/render_templates.py:73-73 | ctx=template_names >>>
列出 templates/ 下的全部模板，返回相对 templates/ 的 POSIX 路径。
<<< END U013986 >>>
<<< UNIT U013987 | py-docstring | tools/render_templates.py:137-137 | ctx=main >>>
入口。返回进程退出码，0 表示全部模板的渲染产物语法正确。
<<< END U013987 >>>
<<< UNIT U013988 | py-comment | tools/testpypi_publish.py:31-31 >>>
# Windows 控制台默认 cp1252，中文输出会抛 UnicodeEncodeError。
<<< END U013988 >>>
<<< UNIT U013989 | py-inline-comment | tools/testpypi_publish.py:111-111 >>>
# noqa: S310 - 固定 https 索引地址
<<< END U013989 >>>
<<< UNIT U013990 | py-docstring | tools/testpypi_publish.py:44-44 | ctx=RateLimited >>>
索引要求等待超过本次可接受时长，留待下一窗口续传。
<<< END U013990 >>>
<<< UNIT U013991 | py-docstring | tools/verify_registry_release.py:31-31 | ctx=VerifyError >>>
索引内容与本次发布不符。
<<< END U013991 >>>
<<< UNIT U013992 | py-docstring | tools/verify_registry_release.py:95-95 | ctx=build_parser >>>
命令行入口参数。
<<< END U013992 >>>
<<< UNIT U013993 | py-docstring | tools/verify_registry_release.py:104-104 | ctx=main >>>
入口。返回进程退出码，0 表示索引与本次发布一致。
<<< END U013993 >>>
