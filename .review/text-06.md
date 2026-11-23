# 全仓可读文本审核稿 · 第 06 册 / 共 20 册

覆盖 U003219–U004563，12 个文件、1,345 个单元、33,868 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json`（续） | 1036 | U003219–U004254 | 16,565 |
| `packages/akari-bot-cli/akaribot/cli/logs.py` | 6 | U004255–U004260 | 84 |
| `packages/akari-bot-cli/akaribot/cli/main.py` | 9 | U004261–U004269 | 761 |
| `packages/akari-bot-cli/akaribot/cli/process.py` | 21 | U004270–U004290 | 610 |
| `packages/akari-bot-cli/akaribot/cli/service.py` | 23 | U004291–U004313 | 779 |
| `packages/akari-bot-cli/akaribot/cli/templates/README.md` | 30 | U004314–U004343 | 2,517 |
| `packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md` | 9 | U004344–U004352 | 1,013 |
| `packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py` | 8 | U004353–U004360 | 188 |
| `packages/akari-bot-cli/akaribot/cli/templates/module/.github/workflows/publish.yml` | 1 | U004361–U004361 | 140 |
| `packages/akari-bot-cli/akaribot/cli/tui/README.md` | 116 | U004362–U004477 | 9,364 |
| `packages/akari-bot-cli/akaribot/cli/tui/__init__.py` | 1 | U004478–U004478 | 11 |
| `packages/akari-bot-cli/akaribot/cli/tui/_compat.py` | 85 | U004479–U004563 | 1,836 |

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
<<< UNIT U003219 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1229-1229 | ctx=cli.tui.dashboard.service_menu_hint >>>
审阅次数：2
当前：${autostart}，${crash}。${service}
<<< END U003219 >>>
<<< UNIT U003220 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1230-1230 | ctx=cli.tui.dashboard.service_menu_title >>>
审阅次数：2
服务与策略：${name}
<<< END U003220 >>>
<<< UNIT U003221 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1231-1231 | ctx=cli.tui.dashboard.service_menu_unavailable >>>
审阅次数：2
请先选择已添加的实例。未添加的实例没有服务与启动策略
<<< END U003221 >>>
<<< UNIT U003222 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1232-1232 | ctx=cli.tui.dashboard.service_missing >>>
审阅次数：2
服务：未安装（按 m 安装）
<<< END U003222 >>>
<<< UNIT U003223 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1233-1233 | ctx=cli.tui.dashboard.service_preview_done >>>
审阅次数：2
预览输出：${output}
<<< END U003223 >>>
<<< UNIT U003224 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1234-1234 | ctx=cli.tui.dashboard.service_preview_failed >>>
审阅次数：2
预览失败：${error}
<<< END U003224 >>>
<<< UNIT U003225 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1235-1235 | ctx=cli.tui.dashboard.service_preview_label_install >>>
审阅次数：2
预览服务安装
<<< END U003225 >>>
<<< UNIT U003226 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1236-1236 | ctx=cli.tui.dashboard.service_preview_label_uninstall >>>
审阅次数：2
预览服务卸载
<<< END U003226 >>>
<<< UNIT U003227 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1237-1237 | ctx=cli.tui.dashboard.service_preview_stub_ok >>>
审阅次数：2
模拟预览成功
<<< END U003227 >>>
<<< UNIT U003228 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1238-1238 | ctx=cli.tui.dashboard.service_registered_unknown >>>
审阅次数：2
注册状态未知
<<< END U003228 >>>
<<< UNIT U003229 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1239-1239 | ctx=cli.tui.dashboard.service_removed >>>
审阅次数：2
服务已卸载：${path}
<<< END U003229 >>>
<<< UNIT U003230 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1240-1240 | ctx=cli.tui.dashboard.service_unsupported >>>
审阅次数：2
服务：当前平台不受支持（${detail}）
<<< END U003230 >>>
<<< UNIT U003231 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1241-1241 | ctx=cli.tui.dashboard.setup_adapters_label >>>
审阅次数：2
未配置适配器
<<< END U003231 >>>
<<< UNIT U003232 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1242-1242 | ctx=cli.tui.dashboard.setup_adapters_value >>>
审阅次数：2
${count} 个
<<< END U003232 >>>
<<< UNIT U003233 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1243-1243 | ctx=cli.tui.dashboard.setup_block_no_instance >>>
审阅次数：2
无可用实例
<<< END U003233 >>>
<<< UNIT U003234 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1244-1244 | ctx=cli.tui.dashboard.setup_block_running >>>
审阅次数：2
实例运行中
<<< END U003234 >>>
<<< UNIT U003235 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1245-1245 | ctx=cli.tui.dashboard.setup_blocked_status >>>
审阅次数：2
${action}不可用：${reason}
<<< END U003235 >>>
<<< UNIT U003236 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1246-1246 | ctx=cli.tui.dashboard.setup_button_config >>>
审阅次数：2
打开配置
<<< END U003236 >>>
<<< UNIT U003237 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1247-1247 | ctx=cli.tui.dashboard.setup_button_config_blocked >>>
审阅次数：2
打开配置（无实例）
<<< END U003237 >>>
<<< UNIT U003238 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1248-1248 | ctx=cli.tui.dashboard.setup_button_doctor >>>
审阅次数：2
运行诊断
<<< END U003238 >>>
<<< UNIT U003239 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1249-1249 | ctx=cli.tui.dashboard.setup_button_doctor_blocked >>>
审阅次数：2
运行诊断（无实例）
<<< END U003239 >>>
<<< UNIT U003240 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1250-1250 | ctx=cli.tui.dashboard.setup_button_run >>>
审阅次数：2
启动实例
<<< END U003240 >>>
<<< UNIT U003241 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1251-1251 | ctx=cli.tui.dashboard.setup_button_run_blocked >>>
审阅次数：2
启动实例（无实例）
<<< END U003241 >>>
<<< UNIT U003242 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1252-1252 | ctx=cli.tui.dashboard.setup_button_run_running >>>
审阅次数：2
启动实例（运行中）
<<< END U003242 >>>
<<< UNIT U003243 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1253-1253 | ctx=cli.tui.dashboard.setup_checks_unreadable >>>
审阅次数：2
诊断统计缺少必要字段
<<< END U003243 >>>
<<< UNIT U003244 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1254-1254 | ctx=cli.tui.dashboard.setup_cli_timeout >>>
审阅次数：2
诊断命令超时（${seconds} 秒）
<<< END U003244 >>>
<<< UNIT U003245 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1255-1255 | ctx=cli.tui.dashboard.setup_doctor_label >>>
审阅次数：2
最近诊断
<<< END U003245 >>>
<<< UNIT U003246 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1256-1256 | ctx=cli.tui.dashboard.setup_doctor_unreadable >>>
审阅次数：2
诊断输出无法解析（退出码 ${code}）
<<< END U003246 >>>
<<< UNIT U003247 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1257-1257 | ctx=cli.tui.dashboard.setup_doctor_value >>>
审阅次数：2
${errors} 项错误，${warnings} 项警告
<<< END U003247 >>>
<<< UNIT U003248 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1258-1258 | ctx=cli.tui.dashboard.setup_instance_label >>>
审阅次数：2
实例运行状态
<<< END U003248 >>>
<<< UNIT U003249 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1259-1259 | ctx=cli.tui.dashboard.setup_placeholders_estimate_unavailable >>>
审阅次数：2
core 统计不可用（${detail}），配置目录读取失败（${error}）
<<< END U003249 >>>
<<< UNIT U003250 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1260-1260 | ctx=cli.tui.dashboard.setup_placeholders_estimated_reason >>>
审阅次数：2
core 统计不可用（${detail}），按配置标记估算
<<< END U003250 >>>
<<< UNIT U003251 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1261-1261 | ctx=cli.tui.dashboard.setup_placeholders_failed >>>
审阅次数：2
配置统计命令失败（退出码 ${code}）
<<< END U003251 >>>
<<< UNIT U003252 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1262-1262 | ctx=cli.tui.dashboard.setup_placeholders_label >>>
审阅次数：2
待填写占位符
<<< END U003252 >>>
<<< UNIT U003253 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1263-1263 | ctx=cli.tui.dashboard.setup_placeholders_label_estimated >>>
审阅次数：2
待填写占位符（估算）
<<< END U003253 >>>
<<< UNIT U003254 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1264-1264 | ctx=cli.tui.dashboard.setup_placeholders_partial_reason >>>
审阅次数：2
${count} 张表未纳入统计：${tables}
<<< END U003254 >>>
<<< UNIT U003255 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1265-1265 | ctx=cli.tui.dashboard.setup_placeholders_timeout >>>
审阅次数：2
配置统计命令超时（${seconds} 秒）
<<< END U003255 >>>
<<< UNIT U003256 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1266-1266 | ctx=cli.tui.dashboard.setup_placeholders_unreadable >>>
审阅次数：2
配置统计输出无法解析（退出码 ${code}）
<<< END U003256 >>>
<<< UNIT U003257 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1267-1267 | ctx=cli.tui.dashboard.setup_placeholders_value >>>
审阅次数：2
${count} 项
<<< END U003257 >>>
<<< UNIT U003258 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1268-1268 | ctx=cli.tui.dashboard.setup_placeholders_value_note >>>
审阅次数：2
${count} 项（${reason}）
<<< END U003258 >>>
<<< UNIT U003259 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1269-1269 | ctx=cli.tui.dashboard.setup_src_no_instance >>>
审阅次数：2
未找到实例，无法读取统计
<<< END U003259 >>>
<<< UNIT U003260 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1270-1270 | ctx=cli.tui.dashboard.setup_value_missing >>>
审阅次数：2
未获取
<<< END U003260 >>>
<<< UNIT U003261 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1271-1271 | ctx=cli.tui.dashboard.setup_value_missing_reason >>>
审阅次数：2
未获取（${reason}）
<<< END U003261 >>>
<<< UNIT U003262 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1272-1272 | ctx=cli.tui.dashboard.src_instance_failed >>>
审阅次数：2
实例初始化失败：${kind}：${error}
<<< END U003262 >>>
<<< UNIT U003263 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1273-1273 | ctx=cli.tui.dashboard.src_instance_unavailable >>>
审阅次数：2
akaribot.cli.instance 不可用：${error}
<<< END U003263 >>>
<<< UNIT U003264 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1274-1274 | ctx=cli.tui.dashboard.src_list_failed >>>
审阅次数：2
module list --json 读取失败：${kind}：${error}
<<< END U003264 >>>
<<< UNIT U003265 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1275-1275 | ctx=cli.tui.dashboard.src_meta_read_failed >>>
审阅次数：2
${file} 读取失败：${kind}：${error}
<<< END U003265 >>>
<<< UNIT U003266 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1276-1276 | ctx=cli.tui.dashboard.src_modules_unavailable >>>
审阅次数：2
akaribot.cli.tui.modules 不可用
<<< END U003266 >>>
<<< UNIT U003267 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1277-1277 | ctx=cli.tui.dashboard.src_no_core_record >>>
审阅次数：2
module list --json 中无 core 记录
<<< END U003267 >>>
<<< UNIT U003268 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1278-1278 | ctx=cli.tui.dashboard.src_no_instance >>>
审阅次数：2
未找到实例：${path} 及其父目录下没有 ${meta}
<<< END U003268 >>>
<<< UNIT U003269 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1279-1279 | ctx=cli.tui.dashboard.src_probe_callback_failed >>>
审阅次数：2
更新检查失败：${kind}：${error}
<<< END U003269 >>>
<<< UNIT U003270 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1280-1280 | ctx=cli.tui.dashboard.src_probe_failed >>>
审阅次数：2
Instance.is_running() 失败：${kind}：${error}
<<< END U003270 >>>
<<< UNIT U003271 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1281-1281 | ctx=cli.tui.dashboard.src_root_unknown >>>
审阅次数：2
实例根目录未知，无法定位锁文件
<<< END U003271 >>>
<<< UNIT U003272 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1282-1282 | ctx=cli.tui.dashboard.src_stub_failed >>>
审阅次数：2
模拟实例失败：${kind}：${error}
<<< END U003272 >>>
<<< UNIT U003273 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1283-1283 | ctx=cli.tui.dashboard.state_running >>>
审阅次数：2
运行中
<<< END U003273 >>>
<<< UNIT U003274 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1284-1284 | ctx=cli.tui.dashboard.state_stopped >>>
审阅次数：2
已停止
<<< END U003274 >>>
<<< UNIT U003275 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1285-1285 | ctx=cli.tui.dashboard.state_unknown >>>
审阅次数：2
状态未知
<<< END U003275 >>>
<<< UNIT U003276 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1286-1286 | ctx=cli.tui.dashboard.status_cached >>>
审阅次数：2
使用 ${age} 秒前的快照
<<< END U003276 >>>
<<< UNIT U003277 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1287-1287 | ctx=cli.tui.dashboard.status_load_failed >>>
审阅次数：2
读取失败：${error}
<<< END U003277 >>>
<<< UNIT U003278 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1288-1288 | ctx=cli.tui.dashboard.status_loading >>>
审阅次数：2
正在读取实例信息…
<<< END U003278 >>>
<<< UNIT U003279 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1289-1289 | ctx=cli.tui.dashboard.status_partial_failed >>>
审阅次数：2
部分字段读取失败：${error}
<<< END U003279 >>>
<<< UNIT U003280 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1290-1290 | ctx=cli.tui.dashboard.status_probe_failed >>>
审阅次数：2
运行状态探测失败：${error}
<<< END U003280 >>>
<<< UNIT U003281 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1291-1291 | ctx=cli.tui.dashboard.status_running >>>
审阅次数：2
运行状态：${state}（${detail}）
<<< END U003281 >>>
<<< UNIT U003282 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1292-1292 | ctx=cli.tui.dashboard.status_updated >>>
审阅次数：2
快照更新于 ${time}
<<< END U003282 >>>
<<< UNIT U003283 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1293-1293 | ctx=cli.tui.dashboard.switch_default_done >>>
审阅次数：2
已设为默认实例
<<< END U003283 >>>
<<< UNIT U003284 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1294-1294 | ctx=cli.tui.dashboard.switch_default_failed >>>
审阅次数：2
默认实例写入失败：${error}
<<< END U003284 >>>
<<< UNIT U003285 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1295-1295 | ctx=cli.tui.dashboard.switch_default_skipped >>>
审阅次数：2
实例未添加，默认实例未更改
<<< END U003285 >>>
<<< UNIT U003286 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1296-1296 | ctx=cli.tui.dashboard.switch_deferred >>>
审阅次数：2
存在未保存的更改，等待切换确认
<<< END U003286 >>>
<<< UNIT U003287 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1297-1297 | ctx=cli.tui.dashboard.switch_done >>>
审阅次数：2
已切换到 ${name}
<<< END U003287 >>>
<<< UNIT U003288 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1298-1298 | ctx=cli.tui.dashboard.switch_missing >>>
审阅次数：2
${root} 中无 akaribot.toml，无法切换
<<< END U003288 >>>
<<< UNIT U003289 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1299-1299 | ctx=cli.tui.dashboard.switch_no_selection >>>
审阅次数：2
请先选择实例
<<< END U003289 >>>
<<< UNIT U003290 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1300-1300 | ctx=cli.tui.dashboard.switch_unsupported >>>
审阅次数：2
当前应用不支持切换实例
<<< END U003290 >>>
<<< UNIT U003291 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1301-1301 | ctx=cli.tui.dashboard.update_source_line >>>
审阅次数：2
更新提示来源：${source}
<<< END U003291 >>>
<<< UNIT U003292 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1302-1302 | ctx=cli.tui.dashboard.update_source_pending >>>
审阅次数：2
未配置更新检查
<<< END U003292 >>>
<<< UNIT U003293 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1303-1303 | ctx=cli.tui.dashboard.update_source_probe >>>
审阅次数：2
更新检查回调
<<< END U003293 >>>
<<< UNIT U003294 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1304-1304 | ctx=cli.tui.dashboard.update_source_probe_no_hint >>>
审阅次数：2
更新检查未返回信息（${source}）
<<< END U003294 >>>
<<< UNIT U003295 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1305-1305 | ctx=cli.tui.dashboard.use_calling >>>
审阅次数：2
正在将 ${name} 设为默认实例…
<<< END U003295 >>>
<<< UNIT U003296 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1306-1306 | ctx=cli.tui.dashboard.use_label >>>
审阅次数：2
将 ${name} 设为默认实例
<<< END U003296 >>>
<<< UNIT U003297 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1307-1307 | ctx=cli.tui.dashboard.value_no_hint >>>
审阅次数：2
（无）
<<< END U003297 >>>
<<< UNIT U003298 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1308-1308 | ctx=cli.tui.dashboard.value_version_missing >>>
审阅次数：2
未获取
<<< END U003298 >>>
<<< UNIT U003299 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1309-1309 | ctx=cli.tui.dashboard.warning_line >>>
审阅次数：2
读取警告：${error}
<<< END U003299 >>>
<<< UNIT U003300 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1310-1310 | ctx=cli.tui.database.bind_cancel >>>
审阅次数：2
取消编辑
<<< END U003300 >>>
<<< UNIT U003301 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1311-1311 | ctx=cli.tui.database.bind_clear_filters >>>
审阅次数：2
清空筛选条件
<<< END U003301 >>>
<<< UNIT U003302 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1312-1312 | ctx=cli.tui.database.bind_delete >>>
审阅次数：2
删除数据项
<<< END U003302 >>>
<<< UNIT U003303 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1313-1313 | ctx=cli.tui.database.bind_filter >>>
审阅次数：2
添加筛选条件或搜索词
<<< END U003303 >>>
<<< UNIT U003304 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1314-1314 | ctx=cli.tui.database.bind_first_page >>>
审阅次数：2
第一页
<<< END U003304 >>>
<<< UNIT U003305 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1315-1315 | ctx=cli.tui.database.bind_insert >>>
审阅次数：2
新建数据项
<<< END U003305 >>>
<<< UNIT U003306 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1316-1316 | ctx=cli.tui.database.bind_last_page >>>
审阅次数：2
最后一页
<<< END U003306 >>>
<<< UNIT U003307 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1317-1317 | ctx=cli.tui.database.bind_next_page >>>
审阅次数：2
下一页
<<< END U003307 >>>
<<< UNIT U003308 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1318-1318 | ctx=cli.tui.database.bind_order >>>
审阅次数：2
设置排序
<<< END U003308 >>>
<<< UNIT U003309 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1319-1319 | ctx=cli.tui.database.bind_previous_page >>>
审阅次数：2
上一页
<<< END U003309 >>>
<<< UNIT U003310 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1320-1320 | ctx=cli.tui.database.bind_refresh >>>
审阅次数：2
刷新
<<< END U003310 >>>
<<< UNIT U003311 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1321-1321 | ctx=cli.tui.database.bind_save >>>
审阅次数：2
保存更改
<<< END U003311 >>>
<<< UNIT U003312 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1322-1322 | ctx=cli.tui.database.bind_search >>>
审阅次数：2
搜索表名
<<< END U003312 >>>
<<< UNIT U003313 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1323-1323 | ctx=cli.tui.database.button_delete >>>
审阅次数：2
删除
<<< END U003313 >>>
<<< UNIT U003314 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1324-1324 | ctx=cli.tui.database.button_filter >>>
审阅次数：2
筛选
<<< END U003314 >>>
<<< UNIT U003315 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1325-1325 | ctx=cli.tui.database.button_first_page >>>
审阅次数：2
首页
<<< END U003315 >>>
<<< UNIT U003316 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1326-1326 | ctx=cli.tui.database.button_insert >>>
审阅次数：2
新建
<<< END U003316 >>>
<<< UNIT U003317 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1327-1327 | ctx=cli.tui.database.button_last_page >>>
审阅次数：2
末页
<<< END U003317 >>>
<<< UNIT U003318 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1328-1328 | ctx=cli.tui.database.button_more >>>
审阅次数：2
更多…
<<< END U003318 >>>
<<< UNIT U003319 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1329-1329 | ctx=cli.tui.database.button_next_page >>>
审阅次数：2
下一页
<<< END U003319 >>>
<<< UNIT U003320 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1330-1330 | ctx=cli.tui.database.button_previous_page >>>
审阅次数：2
上一页
<<< END U003320 >>>
<<< UNIT U003321 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1331-1331 | ctx=cli.tui.database.button_refresh >>>
审阅次数：2
刷新
<<< END U003321 >>>
<<< UNIT U003322 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1332-1332 | ctx=cli.tui.database.button_save >>>
审阅次数：2
保存
<<< END U003322 >>>
<<< UNIT U003323 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1333-1333 | ctx=cli.tui.database.cancel >>>
审阅次数：2
取消
<<< END U003323 >>>
<<< UNIT U003324 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1335-1335 | ctx=cli.tui.database.confirm_delete >>>
审阅次数：2
将删除 ${table} 的数据项 ${pk}，删除后无法恢复。
<<< END U003324 >>>
<<< UNIT U003325 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1336-1336 | ctx=cli.tui.database.confirm_insert >>>
审阅次数：2
将在 ${table} 中新建数据项：${values}
<<< END U003325 >>>
<<< UNIT U003326 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1337-1337 | ctx=cli.tui.database.confirm_set >>>
审阅次数：2
将更新 ${table} 的数据项 ${pk}：${changes}
<<< END U003326 >>>
<<< UNIT U003327 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1338-1338 | ctx=cli.tui.database.dirty_edit >>>
审阅次数：2
数据库页：${pk} 有 ${count} 个字段未保存
<<< END U003327 >>>
<<< UNIT U003328 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1339-1339 | ctx=cli.tui.database.dirty_insert >>>
审阅次数：2
数据库页：新建数据项有 ${count} 个字段未写入
<<< END U003328 >>>
<<< UNIT U003329 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1340-1340 | ctx=cli.tui.database.editor_caption_edit >>>
审阅次数：2
编辑 ${table} 的 ${pk} = ${value}
<<< END U003329 >>>
<<< UNIT U003330 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1341-1341 | ctx=cli.tui.database.editor_caption_empty >>>
审阅次数：2
选择数据项后编辑字段
<<< END U003330 >>>
<<< UNIT U003331 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1342-1342 | ctx=cli.tui.database.editor_caption_insert >>>
审阅次数：2
在 ${table} 中新建数据项
<<< END U003331 >>>
<<< UNIT U003332 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1343-1343 | ctx=cli.tui.database.editor_caption_no_row >>>
审阅次数：2
表 ${table}：请选择数据项
<<< END U003332 >>>
<<< UNIT U003333 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1344-1344 | ctx=cli.tui.database.editor_no_fields >>>
审阅次数：2
该表没有主键以外的可编辑列
<<< END U003333 >>>
<<< UNIT U003334 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1345-1345 | ctx=cli.tui.database.editor_pk_edit >>>
审阅次数：2
主键 ${column} = ${pk}（只读）
<<< END U003334 >>>
<<< UNIT U003335 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1346-1346 | ctx=cli.tui.database.editor_pk_empty >>>
审阅次数：2
主键：无
<<< END U003335 >>>
<<< UNIT U003336 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1347-1347 | ctx=cli.tui.database.editor_pk_placeholder >>>
审阅次数：2
主键值，自增主键留空
<<< END U003336 >>>
<<< UNIT U003337 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1348-1348 | ctx=cli.tui.database.err_bad_json >>>
审阅次数：2
db 子进程的输出不是有效的 JSON（${cmd}）
<<< END U003337 >>>
<<< UNIT U003338 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1349-1349 | ctx=cli.tui.database.err_bad_payload >>>
审阅次数：2
db 子进程返回的 JSON 不是对象
<<< END U003338 >>>
<<< UNIT U003339 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1350-1350 | ctx=cli.tui.database.err_exec >>>
审阅次数：2
无法执行 ${cmd}：${error}
<<< END U003339 >>>
<<< UNIT U003340 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1351-1351 | ctx=cli.tui.database.err_exit >>>
审阅次数：2
db 子进程执行失败（${cmd}，退出码 ${code}）
<<< END U003340 >>>
<<< UNIT U003341 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1352-1352 | ctx=cli.tui.database.err_timeout >>>
审阅次数：2
${cmd} 执行超时（${seconds} 秒）
<<< END U003341 >>>
<<< UNIT U003342 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1354-1354 | ctx=cli.tui.database.filter_cancelled >>>
审阅次数：2
已取消添加筛选条件
<<< END U003342 >>>
<<< UNIT U003343 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1355-1355 | ctx=cli.tui.database.filter_confirm >>>
审阅次数：2
添加
<<< END U003343 >>>
<<< UNIT U003344 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1356-1356 | ctx=cli.tui.database.filter_hint >>>
审阅次数：2
筛选格式：<列><运算符><值>。运算符：=、!=、>、>=、<、<=、~（包含）、!~（不包含）、^（前缀）、$（后缀）。null 表示空值。多条条件使用 AND 连接。其他输入用于搜索所有文本列。可筛选列：${columns}
<<< END U003344 >>>
<<< UNIT U003345 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1357-1357 | ctx=cli.tui.database.filter_line >>>
审阅次数：2
筛选：${conditions}（按 f 添加，Ctrl+f 清空）
<<< END U003345 >>>
<<< UNIT U003346 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1358-1358 | ctx=cli.tui.database.filter_none >>>
审阅次数：2
筛选：无（按 f 添加条件或搜索词，[ / ] 翻页）
<<< END U003346 >>>
<<< UNIT U003347 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1359-1359 | ctx=cli.tui.database.filter_placeholder >>>
审阅次数：2
load=false 或 module_name~wik 或 wik
<<< END U003347 >>>
<<< UNIT U003348 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1360-1360 | ctx=cli.tui.database.filter_title >>>
审阅次数：2
筛选表 ${table} 的数据项
<<< END U003348 >>>
<<< UNIT U003349 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1361-1361 | ctx=cli.tui.database.filter_with_order >>>
审阅次数：2
${line} ｜ 排序：${order}（按 m 设置）
<<< END U003349 >>>
<<< UNIT U003350 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1363-1363 | ctx=cli.tui.database.more_hint >>>
审阅次数：2
设置排序会询问排序列与方向。清空筛选条件同时清空搜索词，保留当前排序。
<<< END U003350 >>>
<<< UNIT U003351 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1364-1364 | ctx=cli.tui.database.more_title >>>
审阅次数：2
更多数据操作
<<< END U003351 >>>
<<< UNIT U003352 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1365-1365 | ctx=cli.tui.database.order_cancelled >>>
审阅次数：2
已取消设置排序
<<< END U003352 >>>
<<< UNIT U003353 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1366-1366 | ctx=cli.tui.database.order_confirm >>>
审阅次数：2
应用排序
<<< END U003353 >>>
<<< UNIT U003354 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1367-1367 | ctx=cli.tui.database.order_default >>>
审阅次数：2
${column}（默认）
<<< END U003354 >>>
<<< UNIT U003355 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1368-1368 | ctx=cli.tui.database.order_hint >>>
审阅次数：2
输入列名按升序排列，列名:desc 按降序排列。留空恢复默认排序。可排序列：${columns}
<<< END U003355 >>>
<<< UNIT U003356 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1370-1370 | ctx=cli.tui.database.order_title >>>
审阅次数：2
设置表 ${table} 的排序
<<< END U003356 >>>
<<< UNIT U003357 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1371-1371 | ctx=cli.tui.database.rows_caption >>>
审阅次数：2
表 ${table}：共 ${total} 条，第 ${page}/${pages} 页，本页 ${count} 条
<<< END U003357 >>>
<<< UNIT U003358 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1372-1372 | ctx=cli.tui.database.rows_caption_empty >>>
审阅次数：2
尚未选中表
<<< END U003358 >>>
<<< UNIT U003359 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1373-1373 | ctx=cli.tui.database.rows_load_failed >>>
审阅次数：2
读取数据项失败：${error}
<<< END U003359 >>>
<<< UNIT U003360 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1374-1374 | ctx=cli.tui.database.rows_no_table >>>
审阅次数：2
请选择表以查看数据项
<<< END U003360 >>>
<<< UNIT U003361 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1375-1375 | ctx=cli.tui.database.search_placeholder >>>
审阅次数：2
搜索表名
<<< END U003361 >>>
<<< UNIT U003362 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1376-1376 | ctx=cli.tui.database.search_term >>>
审阅次数：2
搜索 ${keyword}
<<< END U003362 >>>
<<< UNIT U003363 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1377-1377 | ctx=cli.tui.database.status_cached >>>
审阅次数：2
使用缓存中的 ${count} 张表
<<< END U003363 >>>
<<< UNIT U003364 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1378-1378 | ctx=cli.tui.database.status_cancelled >>>
审阅次数：2
已取消编辑
<<< END U003364 >>>
<<< UNIT U003365 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1379-1379 | ctx=cli.tui.database.status_filter_added >>>
审阅次数：2
已添加筛选条件：${condition}
<<< END U003365 >>>
<<< UNIT U003366 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1380-1380 | ctx=cli.tui.database.status_filters_cleared >>>
审阅次数：2
已清空筛选条件与搜索词
<<< END U003366 >>>
<<< UNIT U003367 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1381-1381 | ctx=cli.tui.database.status_insert_mode >>>
审阅次数：2
正在 ${table} 中新建数据项。填写后按 n 或 Ctrl+S 确认写入
<<< END U003367 >>>
<<< UNIT U003368 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1382-1382 | ctx=cli.tui.database.status_load_failed >>>
审阅次数：2
读取表清单失败
<<< END U003368 >>>
<<< UNIT U003369 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1383-1383 | ctx=cli.tui.database.status_loaded >>>
审阅次数：2
已读取 ${count} 张表
<<< END U003369 >>>
<<< UNIT U003370 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1384-1384 | ctx=cli.tui.database.status_loading >>>
审阅次数：2
正在读取表清单
<<< END U003370 >>>
<<< UNIT U003371 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1385-1385 | ctx=cli.tui.database.status_no_changes >>>
审阅次数：2
${table} 的 ${pk} 没有更改
<<< END U003371 >>>
<<< UNIT U003372 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1386-1386 | ctx=cli.tui.database.status_no_row >>>
审阅次数：2
尚未选中数据项
<<< END U003372 >>>
<<< UNIT U003373 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1387-1387 | ctx=cli.tui.database.status_no_table >>>
审阅次数：2
尚未选中表
<<< END U003373 >>>
<<< UNIT U003374 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1388-1388 | ctx=cli.tui.database.status_no_tables >>>
审阅次数：2
实例数据库中没有已注册的表
<<< END U003374 >>>
<<< UNIT U003375 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1389-1389 | ctx=cli.tui.database.status_order_reset >>>
审阅次数：2
已恢复默认排序（主键降序）
<<< END U003375 >>>
<<< UNIT U003376 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1390-1390 | ctx=cli.tui.database.status_order_set >>>
审阅次数：2
已设置排序：${order}
<<< END U003376 >>>
<<< UNIT U003377 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1391-1391 | ctx=cli.tui.database.status_page_loaded >>>
审阅次数：2
已切换到第 ${page}/${pages} 页
<<< END U003377 >>>
<<< UNIT U003378 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1392-1392 | ctx=cli.tui.database.status_page_loading >>>
审阅次数：2
正在加载页面…
<<< END U003378 >>>
<<< UNIT U003379 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1393-1393 | ctx=cli.tui.database.status_page_same >>>
审阅次数：2
已在第 ${page}/${pages} 页
<<< END U003379 >>>
<<< UNIT U003380 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1394-1394 | ctx=cli.tui.database.status_ready >>>
审阅次数：2
就绪
<<< END U003380 >>>
<<< UNIT U003381 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1395-1395 | ctx=cli.tui.database.status_rows_failed >>>
审阅次数：2
读取表 ${table} 失败
<<< END U003381 >>>
<<< UNIT U003382 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1396-1396 | ctx=cli.tui.database.status_search_set >>>
审阅次数：2
已搜索文本列：${keyword}
<<< END U003382 >>>
<<< UNIT U003383 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1397-1397 | ctx=cli.tui.database.status_table_loaded >>>
审阅次数：2
已加载 ${table}，共 ${rows} 条
<<< END U003383 >>>
<<< UNIT U003384 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1398-1398 | ctx=cli.tui.database.status_unknown_table >>>
审阅次数：2
未注册的表 ${table}
<<< END U003384 >>>
<<< UNIT U003385 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1399-1399 | ctx=cli.tui.database.status_write_failed >>>
审阅次数：2
表 ${table} 写入失败
<<< END U003385 >>>
<<< UNIT U003386 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1400-1400 | ctx=cli.tui.database.status_writing >>>
审阅次数：2
正在写入 ${table}
<<< END U003386 >>>
<<< UNIT U003387 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1401-1401 | ctx=cli.tui.database.status_written >>>
审阅次数：2
${table} 的 ${action} 完成，共 ${count} 项
<<< END U003387 >>>
<<< UNIT U003388 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1402-1402 | ctx=cli.tui.database.stub_delete_ok >>>
审阅次数：2
模拟数据源：删除成功
<<< END U003388 >>>
<<< UNIT U003389 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1403-1403 | ctx=cli.tui.database.stub_insert_ok >>>
审阅次数：2
模拟数据源：新建成功
<<< END U003389 >>>
<<< UNIT U003390 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1404-1404 | ctx=cli.tui.database.stub_write_ok >>>
审阅次数：2
模拟数据源：单列更新成功
<<< END U003390 >>>
<<< UNIT U003391 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1406-1406 | ctx=cli.tui.database.write_cancelled >>>
审阅次数：2
已取消写入
<<< END U003391 >>>
<<< UNIT U003392 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1407-1407 | ctx=cli.tui.database.write_confirm >>>
审阅次数：2
写入
<<< END U003392 >>>
<<< UNIT U003393 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1408-1408 | ctx=cli.tui.database.write_ok >>>
审阅次数：2
${table} 写入完成
<<< END U003393 >>>
<<< UNIT U003394 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1409-1409 | ctx=cli.tui.database.write_title >>>
审阅次数：2
确认写入 ${table}
<<< END U003394 >>>
<<< UNIT U003395 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1410-1410 | ctx=cli.tui.dev.action_cancel >>>
审阅次数：2
终止操作
<<< END U003395 >>>
<<< UNIT U003396 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1411-1411 | ctx=cli.tui.dev.action_cancelled >>>
审阅次数：2
已终止${label}
<<< END U003396 >>>
<<< UNIT U003397 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1412-1412 | ctx=cli.tui.dev.action_focus_output >>>
审阅次数：2
查看输出
<<< END U003397 >>>
<<< UNIT U003398 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1413-1413 | ctx=cli.tui.dev.action_label_new >>>
审阅次数：2
生成脚手架
<<< END U003398 >>>
<<< UNIT U003399 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1414-1414 | ctx=cli.tui.dev.action_label_test >>>
审阅次数：2
测试
<<< END U003399 >>>
<<< UNIT U003400 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1415-1415 | ctx=cli.tui.dev.action_new_failed >>>
审阅次数：2
生成脚手架失败，退出码 ${code}
<<< END U003400 >>>
<<< UNIT U003401 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1416-1416 | ctx=cli.tui.dev.action_new_ok >>>
审阅次数：2
脚手架已生成，退出码 ${code}
<<< END U003401 >>>
<<< UNIT U003402 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1417-1417 | ctx=cli.tui.dev.action_new_package >>>
审阅次数：2
新建包…
<<< END U003402 >>>
<<< UNIT U003403 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1418-1418 | ctx=cli.tui.dev.action_refresh >>>
审阅次数：2
刷新
<<< END U003403 >>>
<<< UNIT U003404 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1419-1419 | ctx=cli.tui.dev.action_run_tests >>>
审阅次数：2
运行测试
<<< END U003404 >>>
<<< UNIT U003405 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1420-1420 | ctx=cli.tui.dev.action_test_failed >>>
审阅次数：2
测试失败，退出码 ${code}
<<< END U003405 >>>
<<< UNIT U003406 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1421-1421 | ctx=cli.tui.dev.action_test_ok >>>
审阅次数：2
测试通过，退出码 ${code}
<<< END U003406 >>>
<<< UNIT U003407 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1422-1422 | ctx=cli.tui.dev.col_kind >>>
审阅次数：2
类型
<<< END U003407 >>>
<<< UNIT U003408 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1423-1423 | ctx=cli.tui.dev.col_package >>>
审阅次数：2
包
<<< END U003408 >>>
<<< UNIT U003409 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1424-1424 | ctx=cli.tui.dev.col_path >>>
审阅次数：2
本地路径
<<< END U003409 >>>
<<< UNIT U003410 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1425-1425 | ctx=cli.tui.dev.col_source >>>
审阅次数：2
来源
<<< END U003410 >>>
<<< UNIT U003411 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1426-1426 | ctx=cli.tui.dev.col_version >>>
审阅次数：2
版本
<<< END U003411 >>>
<<< UNIT U003412 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1427-1427 | ctx=cli.tui.dev.detail_empty >>>
审阅次数：2
暂无已安装包记录
<<< END U003412 >>>
<<< UNIT U003413 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1428-1428 | ctx=cli.tui.dev.detail_first >>>
审阅次数：2
包名：${dist}  来源：${source}  ${path}
<<< END U003413 >>>
<<< UNIT U003414 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1429-1429 | ctx=cli.tui.dev.detail_hint_select >>>
审阅次数：2
选择包查看来源详情
<<< END U003414 >>>
<<< UNIT U003415 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1430-1430 | ctx=cli.tui.dev.detail_placeholder >>>
审阅次数：2
选择包查看来源详情
<<< END U003415 >>>
<<< UNIT U003416 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1431-1431 | ctx=cli.tui.dev.detail_second >>>
审阅次数：2
版本：${version}，editable：${editable}，requires_core_api：${core_api}，提供：${provides}
<<< END U003416 >>>
<<< UNIT U003417 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1432-1432 | ctx=cli.tui.dev.instance_line >>>
审阅次数：2
实例：${root}（mode=${mode}）
<<< END U003417 >>>
<<< UNIT U003418 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1433-1433 | ctx=cli.tui.dev.kind_adapter >>>
审阅次数：2
适配器
<<< END U003418 >>>
<<< UNIT U003419 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1434-1434 | ctx=cli.tui.dev.kind_core >>>
审阅次数：2
核心
<<< END U003419 >>>
<<< UNIT U003420 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1435-1435 | ctx=cli.tui.dev.kind_module >>>
审阅次数：2
模块
<<< END U003420 >>>
<<< UNIT U003421 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1436-1436 | ctx=cli.tui.dev.kind_testing >>>
审阅次数：2
测试
<<< END U003421 >>>
<<< UNIT U003422 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1437-1437 | ctx=cli.tui.dev.meta_module_missing >>>
审阅次数：2
akaribot.cli.instance 不可用：${error}
<<< END U003422 >>>
<<< UNIT U003423 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1438-1438 | ctx=cli.tui.dev.meta_parse_failed >>>
审阅次数：2
读取 akaribot.toml 失败：${kind}：${error}
<<< END U003423 >>>
<<< UNIT U003424 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1439-1439 | ctx=cli.tui.dev.meta_read_failed >>>
审阅次数：2
读取实例元数据失败：${kind}：${error}
<<< END U003424 >>>
<<< UNIT U003425 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1440-1440 | ctx=cli.tui.dev.mode_installed >>>
审阅次数：2
installed（发行版）
<<< END U003425 >>>
<<< UNIT U003426 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1441-1441 | ctx=cli.tui.dev.mode_unknown >>>
审阅次数：2
未读取到 akaribot.toml
<<< END U003426 >>>
<<< UNIT U003427 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1442-1442 | ctx=cli.tui.dev.mode_workspace >>>
审阅次数：2
workspace（本地源码）
<<< END U003427 >>>
<<< UNIT U003428 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1443-1443 | ctx=cli.tui.dev.new_close >>>
审阅次数：2
关闭
<<< END U003428 >>>
<<< UNIT U003429 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1444-1444 | ctx=cli.tui.dev.new_config >>>
审阅次数：2
生成配置
<<< END U003429 >>>
<<< UNIT U003430 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1445-1445 | ctx=cli.tui.dev.new_confirm >>>
审阅次数：2
生成包
<<< END U003430 >>>
<<< UNIT U003431 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1446-1446 | ctx=cli.tui.dev.new_database >>>
审阅次数：2
生成数据库
<<< END U003431 >>>
<<< UNIT U003432 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1447-1447 | ctx=cli.tui.dev.new_dir_placeholder >>>
审阅次数：2
目标目录，留空使用默认路径
<<< END U003432 >>>
<<< UNIT U003433 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1448-1448 | ctx=cli.tui.dev.new_kind_adapter >>>
审阅次数：2
适配器
<<< END U003433 >>>
<<< UNIT U003434 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1449-1449 | ctx=cli.tui.dev.new_kind_module >>>
审阅次数：2
模块
<<< END U003434 >>>
<<< UNIT U003435 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1450-1450 | ctx=cli.tui.dev.new_kind_toggle >>>
审阅次数：2
类型：${kind}
<<< END U003435 >>>
<<< UNIT U003436 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1451-1451 | ctx=cli.tui.dev.new_name_invalid >>>
审阅次数：2
名称不得包含空格或斜杠
<<< END U003436 >>>
<<< UNIT U003437 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1452-1452 | ctx=cli.tui.dev.new_name_placeholder >>>
审阅次数：2
名称，如 dice
<<< END U003437 >>>
<<< UNIT U003438 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1453-1453 | ctx=cli.tui.dev.new_name_required >>>
审阅次数：2
请输入名称
<<< END U003438 >>>
<<< UNIT U003439 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1454-1454 | ctx=cli.tui.dev.new_skeleton_hint >>>
审阅次数：2
生成包结构。其他选项可通过 akaribot new 指定。
<<< END U003439 >>>
<<< UNIT U003440 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1455-1455 | ctx=cli.tui.dev.new_tests >>>
审阅次数：2
生成测试
<<< END U003440 >>>
<<< UNIT U003441 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1456-1456 | ctx=cli.tui.dev.new_title >>>
审阅次数：2
新建包
<<< END U003441 >>>
<<< UNIT U003442 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1457-1457 | ctx=cli.tui.dev.no >>>
审阅次数：2
否
<<< END U003442 >>>
<<< UNIT U003443 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1458-1458 | ctx=cli.tui.dev.not_instance >>>
审阅次数：2
${root} 不是 AkariBot 实例（未找到 akaribot.toml）
<<< END U003443 >>>
<<< UNIT U003444 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1459-1459 | ctx=cli.tui.dev.note_no_workspace >>>
审阅次数：2
[dev] workspace_root 未配置，安装使用远端注册表
<<< END U003444 >>>
<<< UNIT U003445 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1460-1460 | ctx=cli.tui.dev.notes_line >>>
审阅次数：2
说明：${notes}
<<< END U003445 >>>
<<< UNIT U003446 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1461-1461 | ctx=cli.tui.dev.output_empty >>>
审阅次数：2
暂无输出
<<< END U003446 >>>
<<< UNIT U003447 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1462-1462 | ctx=cli.tui.dev.output_paused >>>
审阅次数：2
已暂停自动滚动，按 End 返回末尾
<<< END U003447 >>>
<<< UNIT U003448 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1463-1463 | ctx=cli.tui.dev.output_title >>>
审阅次数：2
操作输出（${count} 行）
<<< END U003448 >>>
<<< UNIT U003449 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1464-1464 | ctx=cli.tui.dev.packages_installed >>>
审阅次数：2
已安装 ${total} 个包
<<< END U003449 >>>
<<< UNIT U003450 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1465-1465 | ctx=cli.tui.dev.path_outside_workspace >>>
审阅次数：2
（非工作区路径）
<<< END U003450 >>>
<<< UNIT U003451 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1466-1466 | ctx=cli.tui.dev.scan_failed >>>
审阅次数：2
扫描工作区成员失败：${kind}：${error}
<<< END U003451 >>>
<<< UNIT U003452 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1467-1467 | ctx=cli.tui.dev.source_count >>>
审阅次数：2
${label} ${count} 个
<<< END U003452 >>>
<<< UNIT U003453 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1468-1468 | ctx=cli.tui.dev.source_editable >>>
审阅次数：2
本地可编辑安装
<<< END U003453 >>>
<<< UNIT U003454 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1469-1469 | ctx=cli.tui.dev.source_registry >>>
审阅次数：2
远端注册表
<<< END U003454 >>>
<<< UNIT U003455 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1470-1470 | ctx=cli.tui.dev.source_unknown >>>
审阅次数：2
来源未知
<<< END U003455 >>>
<<< UNIT U003456 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1471-1471 | ctx=cli.tui.dev.source_workspace >>>
审阅次数：2
本地工作区
<<< END U003456 >>>
<<< UNIT U003457 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1472-1472 | ctx=cli.tui.dev.sources_line >>>
审阅次数：2
远端源：${sources}
<<< END U003457 >>>
<<< UNIT U003458 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1473-1473 | ctx=cli.tui.dev.sources_unset >>>
审阅次数：2
未配置
<<< END U003458 >>>
<<< UNIT U003459 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1474-1474 | ctx=cli.tui.dev.src_bad_json >>>
审阅次数：2
`${label}` 输出无法解析为 JSON：${error}
<<< END U003459 >>>
<<< UNIT U003460 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1475-1475 | ctx=cli.tui.dev.src_empty_output >>>
审阅次数：2
`${label}` 未返回内容
<<< END U003460 >>>
<<< UNIT U003461 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1476-1476 | ctx=cli.tui.dev.src_exe_missing >>>
审阅次数：2
未找到可执行文件：${path}（${error}）
<<< END U003461 >>>
<<< UNIT U003462 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1477-1477 | ctx=cli.tui.dev.src_exit_code >>>
审阅次数：2
`${cmd}` 退出码 ${code}：${tail}
<<< END U003462 >>>
<<< UNIT U003463 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1478-1478 | ctx=cli.tui.dev.src_oserror >>>
审阅次数：2
`${cmd}` 执行失败：${error}
<<< END U003463 >>>
<<< UNIT U003464 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1479-1479 | ctx=cli.tui.dev.src_timeout >>>
审阅次数：2
`${cmd}` 执行超时（${seconds} 秒）
<<< END U003464 >>>
<<< UNIT U003465 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1480-1480 | ctx=cli.tui.dev.status_action_busy >>>
审阅次数：2
已有操作运行中，请等待完成或按 Esc 终止
<<< END U003465 >>>
<<< UNIT U003466 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1481-1481 | ctx=cli.tui.dev.status_action_done >>>
审阅次数：2
操作完成，退出码 ${code}
<<< END U003466 >>>
<<< UNIT U003467 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1482-1482 | ctx=cli.tui.dev.status_action_error >>>
审阅次数：2
操作失败：${error}
<<< END U003467 >>>
<<< UNIT U003468 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1483-1483 | ctx=cli.tui.dev.status_action_failed >>>
审阅次数：2
操作失败，退出码 ${code}
<<< END U003468 >>>
<<< UNIT U003469 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1484-1484 | ctx=cli.tui.dev.status_action_unsupported >>>
审阅次数：2
当前数据源不支持此操作
<<< END U003469 >>>
<<< UNIT U003470 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1485-1485 | ctx=cli.tui.dev.status_cached >>>
审阅次数：2
使用 ${age} 秒前的缓存，共 ${total} 个包
<<< END U003470 >>>
<<< UNIT U003471 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1486-1486 | ctx=cli.tui.dev.status_cancel_none >>>
审阅次数：2
无运行中的操作
<<< END U003471 >>>
<<< UNIT U003472 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1487-1487 | ctx=cli.tui.dev.status_cancel_requested >>>
审阅次数：2
已请求终止${label}
<<< END U003472 >>>
<<< UNIT U003473 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1488-1488 | ctx=cli.tui.dev.status_cancel_unsupported >>>
审阅次数：2
当前数据源不支持终止操作
<<< END U003473 >>>
<<< UNIT U003474 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1489-1489 | ctx=cli.tui.dev.status_load_failed >>>
审阅次数：2
读取失败：${error}
<<< END U003474 >>>
<<< UNIT U003475 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1490-1490 | ctx=cli.tui.dev.status_loaded >>>
审阅次数：2
已读取 ${total} 个包
<<< END U003475 >>>
<<< UNIT U003476 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1491-1491 | ctx=cli.tui.dev.status_loaded_detail >>>
审阅次数：2
已读取 ${total} 个包（${detail}）
<<< END U003476 >>>
<<< UNIT U003477 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1492-1492 | ctx=cli.tui.dev.status_loading >>>
审阅次数：2
正在读取工作区配置与包清单…
<<< END U003477 >>>
<<< UNIT U003478 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1493-1493 | ctx=cli.tui.dev.status_new_running >>>
审阅次数：2
正在生成脚手架…（已输出 ${count} 行）
<<< END U003478 >>>
<<< UNIT U003479 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1494-1494 | ctx=cli.tui.dev.status_next_step >>>
审阅次数：2
按 o 查看完整输出
<<< END U003479 >>>
<<< UNIT U003480 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1496-1496 | ctx=cli.tui.dev.status_test_running >>>
审阅次数：2
正在运行测试…（已输出 ${count} 行）
<<< END U003480 >>>
<<< UNIT U003481 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1497-1497 | ctx=cli.tui.dev.test_path_placeholder >>>
审阅次数：2
用例路径或过滤词，可留空
<<< END U003481 >>>
<<< UNIT U003482 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1498-1498 | ctx=cli.tui.dev.unnamed >>>
审阅次数：2
未命名
<<< END U003482 >>>
<<< UNIT U003483 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1499-1499 | ctx=cli.tui.dev.venv_module_missing >>>
审阅次数：2
akaribot.cli.venv 不可用，无法扫描工作区成员：${error}
<<< END U003483 >>>
<<< UNIT U003484 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1500-1500 | ctx=cli.tui.dev.workspace_dir_missing >>>
审阅次数：2
[dev] workspace_root 指向的目录不存在：${path}
<<< END U003484 >>>
<<< UNIT U003485 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1501-1501 | ctx=cli.tui.dev.workspace_exists >>>
审阅次数：2
${path}（存在）
<<< END U003485 >>>
<<< UNIT U003486 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1502-1502 | ctx=cli.tui.dev.workspace_line >>>
审阅次数：2
工作区：[dev] workspace_root = ${workspace}
<<< END U003486 >>>
<<< UNIT U003487 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1503-1503 | ctx=cli.tui.dev.workspace_missing >>>
审阅次数：2
${path}（目录不存在）
<<< END U003487 >>>
<<< UNIT U003488 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1504-1504 | ctx=cli.tui.dev.workspace_pending >>>
审阅次数：2
尚未读取工作区配置
<<< END U003488 >>>
<<< UNIT U003489 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1505-1505 | ctx=cli.tui.dev.workspace_unset >>>
审阅次数：2
未配置（[dev] workspace_root 为空）
<<< END U003489 >>>
<<< UNIT U003490 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1506-1506 | ctx=cli.tui.dev.yes >>>
审阅次数：2
是
<<< END U003490 >>>
<<< UNIT U003491 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1507-1507 | ctx=cli.tui.docs.action_build >>>
审阅次数：2
构建
<<< END U003491 >>>
<<< UNIT U003492 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1508-1508 | ctx=cli.tui.docs.action_deploy >>>
审阅次数：2
部署
<<< END U003492 >>>
<<< UNIT U003493 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1509-1509 | ctx=cli.tui.docs.action_dev >>>
审阅次数：2
开发预览
<<< END U003493 >>>
<<< UNIT U003494 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1510-1510 | ctx=cli.tui.docs.action_dev_stop >>>
审阅次数：2
停止开发预览
<<< END U003494 >>>
<<< UNIT U003495 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1511-1511 | ctx=cli.tui.docs.action_install_deps >>>
审阅次数：2
安装依赖
<<< END U003495 >>>
<<< UNIT U003496 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1512-1512 | ctx=cli.tui.docs.action_open >>>
审阅次数：2
打开浏览器
<<< END U003496 >>>
<<< UNIT U003497 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1513-1513 | ctx=cli.tui.docs.action_refresh >>>
审阅次数：2
刷新
<<< END U003497 >>>
<<< UNIT U003498 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1514-1514 | ctx=cli.tui.docs.action_serve >>>
审阅次数：2
预览
<<< END U003498 >>>
<<< UNIT U003499 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1515-1515 | ctx=cli.tui.docs.action_stop >>>
审阅次数：2
停止预览
<<< END U003499 >>>
<<< UNIT U003500 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1516-1516 | ctx=cli.tui.docs.action_sync_theme >>>
审阅次数：2
同步主题
<<< END U003500 >>>
<<< UNIT U003501 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1517-1517 | ctx=cli.tui.docs.all_packages >>>
审阅次数：2
全部文档包
<<< END U003501 >>>
<<< UNIT U003502 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1518-1518 | ctx=cli.tui.docs.bind_clear >>>
审阅次数：2
清空选择
<<< END U003502 >>>
<<< UNIT U003503 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1519-1519 | ctx=cli.tui.docs.bind_clear_search >>>
审阅次数：2
清空搜索
<<< END U003503 >>>
<<< UNIT U003504 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1520-1520 | ctx=cli.tui.docs.bind_search >>>
审阅次数：2
搜索
<<< END U003504 >>>
<<< UNIT U003505 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1521-1521 | ctx=cli.tui.docs.bind_select_all >>>
审阅次数：2
全选
<<< END U003505 >>>
<<< UNIT U003506 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1522-1522 | ctx=cli.tui.docs.bind_toggle >>>
审阅次数：2
选择
<<< END U003506 >>>
<<< UNIT U003507 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1523-1523 | ctx=cli.tui.docs.build_done >>>
审阅次数：2
构建完成：${count} 个包（${duration} 毫秒）
<<< END U003507 >>>
<<< UNIT U003508 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1524-1524 | ctx=cli.tui.docs.build_failed >>>
审阅次数：2
构建失败：${detail}
<<< END U003508 >>>
<<< UNIT U003509 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1525-1525 | ctx=cli.tui.docs.build_reused >>>
审阅次数：2
已复用上次构建：${count} 个包（${duration} 毫秒）
<<< END U003509 >>>
<<< UNIT U003510 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1526-1526 | ctx=cli.tui.docs.build_started >>>
审阅次数：2
正在构建 ${label}…
<<< END U003510 >>>
<<< UNIT U003511 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1527-1527 | ctx=cli.tui.docs.build_state >>>
审阅次数：2
最近构建
<<< END U003511 >>>
<<< UNIT U003512 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1528-1528 | ctx=cli.tui.docs.build_value >>>
审阅次数：2
${at}（${count} 个包）
<<< END U003512 >>>
<<< UNIT U003513 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1529-1529 | ctx=cli.tui.docs.button_more >>>
审阅次数：2
更多…
<<< END U003513 >>>
<<< UNIT U003514 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1530-1530 | ctx=cli.tui.docs.cancel >>>
审阅次数：2
取消
<<< END U003514 >>>
<<< UNIT U003515 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1531-1531 | ctx=cli.tui.docs.cancelled >>>
审阅次数：2
已取消
<<< END U003515 >>>
<<< UNIT U003516 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1532-1532 | ctx=cli.tui.docs.category >>>
审阅次数：2
分类
<<< END U003516 >>>
<<< UNIT U003517 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1533-1533 | ctx=cli.tui.docs.column_group >>>
审阅次数：2
分组
<<< END U003517 >>>
<<< UNIT U003518 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1534-1534 | ctx=cli.tui.docs.column_key >>>
审阅次数：2
包
<<< END U003518 >>>
<<< UNIT U003519 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1535-1535 | ctx=cli.tui.docs.column_pages >>>
审阅次数：2
页
<<< END U003519 >>>
<<< UNIT U003520 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1536-1536 | ctx=cli.tui.docs.column_title >>>
审阅次数：2
标题
<<< END U003520 >>>
<<< UNIT U003521 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1537-1537 | ctx=cli.tui.docs.column_version >>>
审阅次数：2
版本
<<< END U003521 >>>
<<< UNIT U003522 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1538-1538 | ctx=cli.tui.docs.count >>>
审阅次数：2
显示 ${shown}/${total}
<<< END U003522 >>>
<<< UNIT U003523 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1539-1539 | ctx=cli.tui.docs.deploy_done >>>
审阅次数：2
部署完成：${detail}
<<< END U003523 >>>
<<< UNIT U003524 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1540-1540 | ctx=cli.tui.docs.deploy_dry_run >>>
审阅次数：2
试运行
<<< END U003524 >>>
<<< UNIT U003525 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1541-1541 | ctx=cli.tui.docs.deploy_failed >>>
审阅次数：2
部署失败：${detail}
<<< END U003525 >>>
<<< UNIT U003526 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1542-1542 | ctx=cli.tui.docs.deploy_hint >>>
审阅次数：2
试运行只统计将上传与删除的文件。部署会把构建产物发布到配置的远端。
<<< END U003526 >>>
<<< UNIT U003527 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1543-1543 | ctx=cli.tui.docs.deploy_real >>>
审阅次数：2
部署
<<< END U003527 >>>
<<< UNIT U003528 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1544-1544 | ctx=cli.tui.docs.deploy_started >>>
审阅次数：2
正在${label}…
<<< END U003528 >>>
<<< UNIT U003529 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1545-1545 | ctx=cli.tui.docs.deploy_state >>>
审阅次数：2
最近部署
<<< END U003529 >>>
<<< UNIT U003530 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1546-1546 | ctx=cli.tui.docs.deploy_title >>>
审阅次数：2
部署文档站点
<<< END U003530 >>>
<<< UNIT U003531 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1548-1548 | ctx=cli.tui.docs.deps_failed >>>
审阅次数：2
依赖安装失败：${detail}
<<< END U003531 >>>
<<< UNIT U003532 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1549-1549 | ctx=cli.tui.docs.deps_ready >>>
审阅次数：2
Node 依赖已就绪：VitePress ${version}
<<< END U003532 >>>
<<< UNIT U003533 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1550-1550 | ctx=cli.tui.docs.deps_started >>>
审阅次数：2
正在安装 Node 依赖…
<<< END U003533 >>>
<<< UNIT U003534 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1551-1551 | ctx=cli.tui.docs.detail_placeholder >>>
审阅次数：2
选择文档包查看详情
<<< END U003534 >>>
<<< UNIT U003535 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1552-1552 | ctx=cli.tui.docs.dev_event_log >>>
审阅次数：2
开发预览
<<< END U003535 >>>
<<< UNIT U003536 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1553-1553 | ctx=cli.tui.docs.dev_failed >>>
审阅次数：2
开发预览失败：${detail}
<<< END U003536 >>>
<<< UNIT U003537 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1554-1554 | ctx=cli.tui.docs.dev_ready >>>
审阅次数：2
开发预览已就绪：${url}
<<< END U003537 >>>
<<< UNIT U003538 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1555-1555 | ctx=cli.tui.docs.dev_started >>>
审阅次数：2
正在启动开发预览…
<<< END U003538 >>>
<<< UNIT U003539 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1556-1556 | ctx=cli.tui.docs.dev_stopped >>>
审阅次数：2
开发预览已停止。
<<< END U003539 >>>
<<< UNIT U003540 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1557-1557 | ctx=cli.tui.docs.dev_synced >>>
审阅次数：2
已同步 ${count} 个文件
<<< END U003540 >>>
<<< UNIT U003541 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1558-1558 | ctx=cli.tui.docs.dirty_note >>>
审阅次数：2
文档预览服务仍在运行：${url}。退出界面将停止该服务。
<<< END U003541 >>>
<<< UNIT U003542 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1559-1559 | ctx=cli.tui.docs.doc_path >>>
审阅次数：2
文档目录
<<< END U003542 >>>
<<< UNIT U003543 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1560-1560 | ctx=cli.tui.docs.editable >>>
审阅次数：2
可编辑
<<< END U003543 >>>
<<< UNIT U003544 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1561-1561 | ctx=cli.tui.docs.empty >>>
审阅次数：2
没有可用的文档包
<<< END U003544 >>>
<<< UNIT U003545 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1562-1562 | ctx=cli.tui.docs.field_dist >>>
审阅次数：2
发行包
<<< END U003545 >>>
<<< UNIT U003546 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1563-1563 | ctx=cli.tui.docs.field_summary >>>
审阅次数：2
简介
<<< END U003546 >>>
<<< UNIT U003547 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1564-1564 | ctx=cli.tui.docs.field_title >>>
审阅次数：2
标题
<<< END U003547 >>>
<<< UNIT U003548 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1565-1565 | ctx=cli.tui.docs.group >>>
审阅次数：2
分组
<<< END U003548 >>>
<<< UNIT U003549 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1566-1566 | ctx=cli.tui.docs.log_title >>>
审阅次数：2
任务日志
<<< END U003549 >>>
<<< UNIT U003550 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1567-1567 | ctx=cli.tui.docs.more_hint >>>
审阅次数：2
部署会先确认目标。同步主题与安装依赖只影响本机的主题目录与 Node 依赖。
<<< END U003550 >>>
<<< UNIT U003551 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1568-1568 | ctx=cli.tui.docs.more_log_hide >>>
审阅次数：2
隐藏任务日志
<<< END U003551 >>>
<<< UNIT U003552 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1569-1569 | ctx=cli.tui.docs.more_log_show >>>
审阅次数：2
显示任务日志
<<< END U003552 >>>
<<< UNIT U003553 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1570-1570 | ctx=cli.tui.docs.more_title >>>
审阅次数：2
更多文档操作
<<< END U003553 >>>
<<< UNIT U003554 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1571-1571 | ctx=cli.tui.docs.need_build >>>
审阅次数：2
站点尚未构建，先按 b 构建
<<< END U003554 >>>
<<< UNIT U003555 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1572-1572 | ctx=cli.tui.docs.need_serve >>>
审阅次数：2
预览服务未运行，先按 p 启动
<<< END U003555 >>>
<<< UNIT U003556 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1573-1573 | ctx=cli.tui.docs.no >>>
审阅次数：2
否
<<< END U003556 >>>
<<< UNIT U003557 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1574-1574 | ctx=cli.tui.docs.no_match >>>
审阅次数：2
没有匹配的文档包，按 Esc 清空搜索
<<< END U003557 >>>
<<< UNIT U003558 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1575-1575 | ctx=cli.tui.docs.no_pages >>>
审阅次数：2
该包未提供页面
<<< END U003558 >>>
<<< UNIT U003559 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1576-1576 | ctx=cli.tui.docs.open_failed >>>
审阅次数：2
无法打开浏览器：${detail}
<<< END U003559 >>>
<<< UNIT U003560 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1577-1577 | ctx=cli.tui.docs.page_count >>>
审阅次数：2
${count} 个
<<< END U003560 >>>
<<< UNIT U003561 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1579-1579 | ctx=cli.tui.docs.pages >>>
审阅次数：2
页面
<<< END U003561 >>>
<<< UNIT U003562 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1580-1580 | ctx=cli.tui.docs.pages_list >>>
审阅次数：2
页面（${count}）
<<< END U003562 >>>
<<< UNIT U003563 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1581-1581 | ctx=cli.tui.docs.search_placeholder >>>
审阅次数：2
搜索包名、标题或简介
<<< END U003563 >>>
<<< UNIT U003564 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1582-1582 | ctx=cli.tui.docs.selected >>>
审阅次数：2
已选 ${count} 项
<<< END U003564 >>>
<<< UNIT U003565 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1583-1583 | ctx=cli.tui.docs.serve_failed >>>
审阅次数：2
预览服务启动失败：${detail}
<<< END U003565 >>>
<<< UNIT U003566 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1584-1584 | ctx=cli.tui.docs.serve_ready >>>
审阅次数：2
预览服务已启动：${url}
<<< END U003566 >>>
<<< UNIT U003567 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1585-1585 | ctx=cli.tui.docs.serve_starting >>>
审阅次数：2
正在启动预览服务…
<<< END U003567 >>>
<<< UNIT U003568 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1586-1586 | ctx=cli.tui.docs.server_running >>>
审阅次数：2
预览服务运行中：${url}
<<< END U003568 >>>
<<< UNIT U003569 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1587-1587 | ctx=cli.tui.docs.server_stopped >>>
审阅次数：2
预览服务已停止
<<< END U003569 >>>
<<< UNIT U003570 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1588-1588 | ctx=cli.tui.docs.src_bad_json >>>
审阅次数：2
`${label}` 输出无法解析为 JSON：${error}
<<< END U003570 >>>
<<< UNIT U003571 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1589-1589 | ctx=cli.tui.docs.src_empty_output >>>
审阅次数：2
`${label}` 未返回内容
<<< END U003571 >>>
<<< UNIT U003572 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1590-1590 | ctx=cli.tui.docs.src_dev_exit >>>
审阅次数：2
开发预览进程已退出（退出码 ${code}）
<<< END U003572 >>>
<<< UNIT U003573 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1591-1591 | ctx=cli.tui.docs.src_exe_missing >>>
审阅次数：2
未找到可执行文件：${path}（${error}）
<<< END U003573 >>>
<<< UNIT U003574 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1592-1592 | ctx=cli.tui.docs.src_exit_code >>>
审阅次数：2
`${cmd}` 退出码 ${code}：${tail}
<<< END U003574 >>>
<<< UNIT U003575 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1593-1593 | ctx=cli.tui.docs.src_oserror >>>
审阅次数：2
`${cmd}` 执行失败：${error}
<<< END U003575 >>>
<<< UNIT U003576 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1594-1594 | ctx=cli.tui.docs.src_serve_exit >>>
审阅次数：2
预览服务提前退出（退出码 ${code}）：${detail}
<<< END U003576 >>>
<<< UNIT U003577 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1595-1595 | ctx=cli.tui.docs.src_serve_timeout >>>
审阅次数：2
预览服务未在 ${seconds} 秒内就绪
<<< END U003577 >>>
<<< UNIT U003578 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1596-1596 | ctx=cli.tui.docs.src_timeout >>>
审阅次数：2
`${cmd}` 执行超时（${seconds} 秒）
<<< END U003578 >>>
<<< UNIT U003579 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1597-1597 | ctx=cli.tui.docs.status_cached >>>
审阅次数：2
缓存于 ${age} 秒前
<<< END U003579 >>>
<<< UNIT U003580 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1598-1598 | ctx=cli.tui.docs.status_load_failed >>>
审阅次数：2
读取文档目录失败：${error}
<<< END U003580 >>>
<<< UNIT U003581 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1599-1599 | ctx=cli.tui.docs.status_dev >>>
审阅次数：2
开发预览：${detail}
<<< END U003581 >>>
<<< UNIT U003582 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1600-1600 | ctx=cli.tui.docs.status_loaded >>>
审阅次数：2
已读取 ${count} 个文档包
<<< END U003582 >>>
<<< UNIT U003583 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1601-1601 | ctx=cli.tui.docs.status_loading >>>
审阅次数：2
正在读取文档目录…
<<< END U003583 >>>
<<< UNIT U003584 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1602-1602 | ctx=cli.tui.docs.status_ready >>>
审阅次数：2
就绪
<<< END U003584 >>>
<<< UNIT U003585 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1603-1603 | ctx=cli.tui.docs.theme_current >>>
审阅次数：2
主题已是最新：${after}
<<< END U003585 >>>
<<< UNIT U003586 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1604-1604 | ctx=cli.tui.docs.theme_sync_failed >>>
审阅次数：2
主题同步失败：${detail}
<<< END U003586 >>>
<<< UNIT U003587 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1605-1605 | ctx=cli.tui.docs.theme_sync_started >>>
审阅次数：2
正在同步主题模板…
<<< END U003587 >>>
<<< UNIT U003588 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1606-1606 | ctx=cli.tui.docs.theme_synced >>>
审阅次数：2
主题已更新：${before} → ${after}
<<< END U003588 >>>
<<< UNIT U003589 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1607-1607 | ctx=cli.tui.docs.title >>>
审阅次数：2
文档
<<< END U003589 >>>
<<< UNIT U003590 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1608-1608 | ctx=cli.tui.docs.toolchain >>>
审阅次数：2
Node.js 工具链
<<< END U003590 >>>
<<< UNIT U003591 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1609-1609 | ctx=cli.tui.docs.toolchain_missing >>>
审阅次数：2
Node.js 工具链不可用：${detail}
<<< END U003591 >>>
<<< UNIT U003592 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1611-1611 | ctx=cli.tui.docs.version >>>
审阅次数：2
版本
<<< END U003592 >>>
<<< UNIT U003593 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1612-1612 | ctx=cli.tui.docs.warning >>>
审阅次数：2
警告：${message}
<<< END U003593 >>>
<<< UNIT U003594 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1613-1613 | ctx=cli.tui.docs.yes >>>
审阅次数：2
是
<<< END U003594 >>>
<<< UNIT U003595 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1614-1614 | ctx=cli.tui.doctor.action_open >>>
审阅次数：2
打开对应页面
<<< END U003595 >>>
<<< UNIT U003596 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1615-1615 | ctx=cli.tui.doctor.action_refresh >>>
审阅次数：2
刷新
<<< END U003596 >>>
<<< UNIT U003597 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1616-1616 | ctx=cli.tui.doctor.bind_open >>>
审阅次数：2
打开对应页面
<<< END U003597 >>>
<<< UNIT U003598 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1617-1617 | ctx=cli.tui.doctor.bind_refresh >>>
审阅次数：2
刷新
<<< END U003598 >>>
<<< UNIT U003599 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1618-1618 | ctx=cli.tui.doctor.checks_degraded >>>
审阅次数：2
孤立配置检查：${orphan}，登录信息范围：${scope}，适配器清单不可用：${note}
<<< END U003599 >>>
<<< UNIT U003600 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1619-1619 | ctx=cli.tui.doctor.checks_line >>>
审阅次数：2
孤立配置检查：${orphan}，登录信息范围：${scope}
<<< END U003600 >>>
<<< UNIT U003601 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1620-1620 | ctx=cli.tui.doctor.detail_failed >>>
审阅次数：2
诊断未完成，请检查数据读取错误。
<<< END U003601 >>>
<<< UNIT U003602 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1621-1621 | ctx=cli.tui.doctor.detail_hint_select >>>
审阅次数：2
按上下键选择结论并查看详情。
<<< END U003602 >>>
<<< UNIT U003603 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1622-1622 | ctx=cli.tui.doctor.detail_passed >>>
审阅次数：2
未发现冲突，无需处理。
<<< END U003603 >>>
<<< UNIT U003604 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1623-1623 | ctx=cli.tui.doctor.detail_placeholder >>>
审阅次数：2
正在读取诊断结果…
<<< END U003604 >>>
<<< UNIT U003605 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1624-1624 | ctx=cli.tui.doctor.field_checks >>>
审阅次数：2
检查项
<<< END U003605 >>>
<<< UNIT U003606 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1625-1625 | ctx=cli.tui.doctor.field_config_root >>>
审阅次数：2
配置目录
<<< END U003606 >>>
<<< UNIT U003607 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1626-1626 | ctx=cli.tui.doctor.field_detail >>>
审阅次数：2
详情
<<< END U003607 >>>
<<< UNIT U003608 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1627-1627 | ctx=cli.tui.doctor.field_installed_adapters >>>
审阅次数：2
已安装适配器
<<< END U003608 >>>
<<< UNIT U003609 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1628-1628 | ctx=cli.tui.doctor.field_instance_count >>>
审阅次数：2
实例数
<<< END U003609 >>>
<<< UNIT U003610 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1629-1629 | ctx=cli.tui.doctor.field_instance_root >>>
审阅次数：2
实例目录
<<< END U003610 >>>
<<< UNIT U003611 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1630-1630 | ctx=cli.tui.doctor.field_instances >>>
审阅次数：2
相关实例
<<< END U003611 >>>
<<< UNIT U003612 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1631-1631 | ctx=cli.tui.doctor.field_kind >>>
审阅次数：2
种类
<<< END U003612 >>>
<<< UNIT U003613 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1632-1632 | ctx=cli.tui.doctor.field_level >>>
审阅次数：2
级别
<<< END U003613 >>>
<<< UNIT U003614 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1633-1633 | ctx=cli.tui.doctor.field_level_kind >>>
审阅次数：2
级别 · 种类
<<< END U003614 >>>
<<< UNIT U003615 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1634-1634 | ctx=cli.tui.doctor.field_message >>>
审阅次数：2
结论
<<< END U003615 >>>
<<< UNIT U003616 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1635-1635 | ctx=cli.tui.doctor.field_next >>>
审阅次数：2
下一步
<<< END U003616 >>>
<<< UNIT U003617 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1636-1636 | ctx=cli.tui.doctor.field_platform >>>
审阅次数：2
平台
<<< END U003617 >>>
<<< UNIT U003618 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1637-1637 | ctx=cli.tui.doctor.field_strict >>>
审阅次数：2
严格模式
<<< END U003618 >>>
<<< UNIT U003619 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1638-1638 | ctx=cli.tui.doctor.field_unconfigured_adapters >>>
审阅次数：2
未配置适配器
<<< END U003619 >>>
<<< UNIT U003620 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1639-1639 | ctx=cli.tui.doctor.impl_core >>>
审阅次数：2
core 入口
<<< END U003620 >>>
<<< UNIT U003621 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1640-1640 | ctx=cli.tui.doctor.impl_local >>>
审阅次数：2
CLI 本地实现
<<< END U003621 >>>
<<< UNIT U003622 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1641-1641 | ctx=cli.tui.doctor.impl_other >>>
审阅次数：2
其他来源：${value}
<<< END U003622 >>>
<<< UNIT U003623 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1642-1642 | ctx=cli.tui.doctor.impl_unknown >>>
审阅次数：2
来源未知
<<< END U003623 >>>
<<< UNIT U003624 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1643-1643 | ctx=cli.tui.doctor.level_error >>>
审阅次数：2
错误
<<< END U003624 >>>
<<< UNIT U003625 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1644-1644 | ctx=cli.tui.doctor.level_warning >>>
审阅次数：2
警告
<<< END U003625 >>>
<<< UNIT U003626 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1645-1645 | ctx=cli.tui.doctor.next_step_cli >>>
审阅次数：2
可在终端执行 akaribot doctor 查看诊断详情。
<<< END U003626 >>>
<<< UNIT U003627 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1646-1646 | ctx=cli.tui.doctor.next_step_page >>>
审阅次数：2
按回车打开“${page}”页。
<<< END U003627 >>>
<<< UNIT U003628 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1647-1647 | ctx=cli.tui.doctor.orphan_ran >>>
审阅次数：2
已执行
<<< END U003628 >>>
<<< UNIT U003629 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1648-1648 | ctx=cli.tui.doctor.orphan_skipped >>>
审阅次数：2
已跳过
<<< END U003629 >>>
<<< UNIT U003630 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1649-1649 | ctx=cli.tui.doctor.orphan_unknown >>>
审阅次数：2
未知
<<< END U003630 >>>
<<< UNIT U003631 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1650-1650 | ctx=cli.tui.doctor.src_bad_json >>>
审阅次数：2
${label} 输出无法解析为 JSON：${error}
<<< END U003631 >>>
<<< UNIT U003632 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1651-1651 | ctx=cli.tui.doctor.src_bad_payload >>>
审阅次数：2
${label} 的输出不是 JSON 对象
<<< END U003632 >>>
<<< UNIT U003633 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1652-1652 | ctx=cli.tui.doctor.src_empty_output >>>
审阅次数：2
${label} 未返回内容
<<< END U003633 >>>
<<< UNIT U003634 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1653-1653 | ctx=cli.tui.doctor.src_exe_missing >>>
审阅次数：2
无法执行 ${path}：${error}
<<< END U003634 >>>
<<< UNIT U003635 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1654-1654 | ctx=cli.tui.doctor.src_exit_code >>>
审阅次数：2
${cmd} 退出码 ${code}：${tail}
<<< END U003635 >>>
<<< UNIT U003636 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1655-1655 | ctx=cli.tui.doctor.src_oserror >>>
审阅次数：2
命令 ${cmd} 执行失败：${error}
<<< END U003636 >>>
<<< UNIT U003637 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1656-1656 | ctx=cli.tui.doctor.src_timeout >>>
审阅次数：2
命令 ${cmd} 超时（${seconds} 秒）
<<< END U003637 >>>
<<< UNIT U003638 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1657-1657 | ctx=cli.tui.doctor.status_failed >>>
审阅次数：2
诊断失败：${error}
<<< END U003638 >>>
<<< UNIT U003639 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1658-1658 | ctx=cli.tui.doctor.status_jumped >>>
审阅次数：2
已打开“${page}”页
<<< END U003639 >>>
<<< UNIT U003640 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1659-1659 | ctx=cli.tui.doctor.status_loaded >>>
审阅次数：2
${errors} 项错误、${warnings} 项警告。来源：${implementation}
<<< END U003640 >>>
<<< UNIT U003641 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1660-1660 | ctx=cli.tui.doctor.status_loading >>>
审阅次数：2
正在诊断…
<<< END U003641 >>>
<<< UNIT U003642 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1661-1661 | ctx=cli.tui.doctor.status_nothing >>>
审阅次数：2
无待处理问题
<<< END U003642 >>>
<<< UNIT U003643 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1662-1662 | ctx=cli.tui.doctor.strict_off >>>
审阅次数：2
关
<<< END U003643 >>>
<<< UNIT U003644 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1663-1663 | ctx=cli.tui.doctor.strict_on >>>
审阅次数：2
开
<<< END U003644 >>>
<<< UNIT U003645 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1664-1664 | ctx=cli.tui.doctor.strict_option >>>
审阅次数：2
警告视为失败（--strict）
<<< END U003645 >>>
<<< UNIT U003646 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1665-1665 | ctx=cli.tui.doctor.summary_pending >>>
审阅次数：2
正在读取检查项统计…
<<< END U003646 >>>
<<< UNIT U003647 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1666-1666 | ctx=cli.tui.doctor.verdict_conflicts >>>
审阅次数：2
发现 ${errors} 项错误、${warnings} 项警告。
<<< END U003647 >>>
<<< UNIT U003648 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1667-1667 | ctx=cli.tui.doctor.verdict_failed >>>
审阅次数：2
诊断未完成，无法生成结论。
<<< END U003648 >>>
<<< UNIT U003649 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1668-1668 | ctx=cli.tui.doctor.verdict_passed >>>
审阅次数：2
通过：未发现端口冲突、登录信息重复或孤立配置。
<<< END U003649 >>>
<<< UNIT U003650 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1669-1669 | ctx=cli.tui.doctor.verdict_pending >>>
审阅次数：2
尚未诊断。
<<< END U003650 >>>
<<< UNIT U003651 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1670-1670 | ctx=cli.tui.environment.action_cancelled >>>
审阅次数：2
已取消环境操作
<<< END U003651 >>>
<<< UNIT U003652 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1672-1672 | ctx=cli.tui.environment.action_signalled >>>
审阅次数：2
${label}因信号中断（${signal}）
<<< END U003652 >>>
<<< UNIT U003653 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1673-1673 | ctx=cli.tui.environment.action_timeout >>>
审阅次数：2
${label}超时（${seconds} 秒），已停止等待
<<< END U003653 >>>
<<< UNIT U003654 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1674-1674 | ctx=cli.tui.environment.already_managed >>>
审阅次数：2
实例已使用托管 venv
<<< END U003654 >>>
<<< UNIT U003655 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1675-1675 | ctx=cli.tui.environment.bind_clear_search >>>
审阅次数：2
清空搜索
<<< END U003655 >>>
<<< UNIT U003656 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1676-1676 | ctx=cli.tui.environment.bind_install >>>
审阅次数：2
安装运行库
<<< END U003656 >>>
<<< UNIT U003657 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1677-1677 | ctx=cli.tui.environment.bind_refresh >>>
审阅次数：2
刷新
<<< END U003657 >>>
<<< UNIT U003658 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1678-1678 | ctx=cli.tui.environment.bind_search >>>
审阅次数：2
搜索包名
<<< END U003658 >>>
<<< UNIT U003659 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1679-1679 | ctx=cli.tui.environment.bind_uninstall >>>
审阅次数：2
卸载所选包
<<< END U003659 >>>
<<< UNIT U003660 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1680-1680 | ctx=cli.tui.environment.button_adopt >>>
审阅次数：2
改用托管 venv
<<< END U003660 >>>
<<< UNIT U003661 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1681-1681 | ctx=cli.tui.environment.button_install >>>
审阅次数：2
安装运行库
<<< END U003661 >>>
<<< UNIT U003662 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1682-1682 | ctx=cli.tui.environment.button_interpreter >>>
审阅次数：2
解释器…
<<< END U003662 >>>
<<< UNIT U003663 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1683-1683 | ctx=cli.tui.environment.button_recreate >>>
审阅次数：2
重建实例 venv
<<< END U003663 >>>
<<< UNIT U003664 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1684-1684 | ctx=cli.tui.environment.button_refresh >>>
审阅次数：2
刷新
<<< END U003664 >>>
<<< UNIT U003665 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1685-1685 | ctx=cli.tui.environment.button_release >>>
审阅次数：2
改用系统解释器
<<< END U003665 >>>
<<< UNIT U003666 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1686-1686 | ctx=cli.tui.environment.button_uninstall >>>
审阅次数：2
卸载
<<< END U003666 >>>
<<< UNIT U003667 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1687-1687 | ctx=cli.tui.environment.calling >>>
审阅次数：2
正在${label}…
<<< END U003667 >>>
<<< UNIT U003668 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1688-1688 | ctx=cli.tui.environment.cancel >>>
审阅次数：2
取消
<<< END U003668 >>>
<<< UNIT U003669 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1689-1689 | ctx=cli.tui.environment.column_name >>>
审阅次数：2
名称
<<< END U003669 >>>
<<< UNIT U003670 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1690-1690 | ctx=cli.tui.environment.column_tags >>>
审阅次数：2
标记
<<< END U003670 >>>
<<< UNIT U003671 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1691-1691 | ctx=cli.tui.environment.column_version >>>
审阅次数：2
版本
<<< END U003671 >>>
<<< UNIT U003672 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1692-1692 | ctx=cli.tui.environment.confirm_adopt >>>
审阅次数：2
将在托管 venv 中安装当前环境的 AkariBot 包，验证通过后从原环境卸载这些包。
<<< END U003672 >>>
<<< UNIT U003673 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1693-1693 | ctx=cli.tui.environment.confirm_dry_run >>>
审阅次数：2
预览
<<< END U003673 >>>
<<< UNIT U003674 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1694-1694 | ctx=cli.tui.environment.confirm_recreate >>>
审阅次数：2
将重建实例 venv，并重新安装 AkariBot 包与清单运行库，期间实例不可用。
<<< END U003674 >>>
<<< UNIT U003675 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1695-1695 | ctx=cli.tui.environment.confirm_release >>>
审阅次数：2
将包迁移到系统解释器，后续使用该解释器运行实例。
<<< END U003675 >>>
<<< UNIT U003676 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1696-1696 | ctx=cli.tui.environment.confirm_run >>>
审阅次数：2
执行
<<< END U003676 >>>
<<< UNIT U003677 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1697-1697 | ctx=cli.tui.environment.confirm_title >>>
审阅次数：2
确认${label}
<<< END U003677 >>>
<<< UNIT U003678 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1698-1698 | ctx=cli.tui.environment.editable_mark >>>
审阅次数：2
（可编辑）
<<< END U003678 >>>
<<< UNIT U003679 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1699-1699 | ctx=cli.tui.environment.field_core >>>
审阅次数：2
core 版本
<<< END U003679 >>>
<<< UNIT U003680 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1700-1700 | ctx=cli.tui.environment.field_error >>>
审阅次数：2
读取失败
<<< END U003680 >>>
<<< UNIT U003681 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1701-1701 | ctx=cli.tui.environment.field_mode >>>
审阅次数：2
托管方式
<<< END U003681 >>>
<<< UNIT U003682 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1702-1702 | ctx=cli.tui.environment.field_packages >>>
审阅次数：2
已安装包
<<< END U003682 >>>
<<< UNIT U003683 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1703-1703 | ctx=cli.tui.environment.field_python >>>
审阅次数：2
解释器
<<< END U003683 >>>
<<< UNIT U003684 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1704-1704 | ctx=cli.tui.environment.field_requirements >>>
审阅次数：2
运行库清单
<<< END U003684 >>>
<<< UNIT U003685 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1705-1705 | ctx=cli.tui.environment.field_selected >>>
审阅次数：2
当前选择
<<< END U003685 >>>
<<< UNIT U003686 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1706-1706 | ctx=cli.tui.environment.field_state >>>
审阅次数：2
实例状态
<<< END U003686 >>>
<<< UNIT U003687 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1707-1707 | ctx=cli.tui.environment.fields_placeholder >>>
审阅次数：2
正在读取环境…
<<< END U003687 >>>
<<< UNIT U003688 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1708-1708 | ctx=cli.tui.environment.install_cancelled >>>
审阅次数：2
已取消安装
<<< END U003688 >>>
<<< UNIT U003689 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1709-1709 | ctx=cli.tui.environment.install_confirm >>>
审阅次数：2
下一步
<<< END U003689 >>>
<<< UNIT U003690 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1710-1710 | ctx=cli.tui.environment.install_hint >>>
审阅次数：2
输入 PyPI 包名、版本范围（如 httpx>=0.27）、仓库地址或 git+ 直接引用。AkariBot 模块请在模块页安装。
<<< END U003690 >>>
<<< UNIT U003691 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1711-1711 | ctx=cli.tui.environment.install_placeholder >>>
审阅次数：2
httpx 或 git+https://github.com/psf/requests
<<< END U003691 >>>
<<< UNIT U003692 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1712-1712 | ctx=cli.tui.environment.install_target_hint >>>
审阅次数：2
写入清单的运行库会在环境重建时自动安装。仅安装到当前环境的运行库不随重建保留。
<<< END U003692 >>>
<<< UNIT U003693 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1713-1713 | ctx=cli.tui.environment.install_target_title >>>
审阅次数：2
确认安装 ${spec}
<<< END U003693 >>>
<<< UNIT U003694 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1714-1714 | ctx=cli.tui.environment.install_title >>>
审阅次数：2
安装运行库
<<< END U003694 >>>
<<< UNIT U003695 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1715-1715 | ctx=cli.tui.environment.install_to_env >>>
审阅次数：2
仅安装到当前环境
<<< END U003695 >>>
<<< UNIT U003696 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1716-1716 | ctx=cli.tui.environment.install_to_manifest >>>
审阅次数：2
安装并写入清单
<<< END U003696 >>>
<<< UNIT U003697 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1717-1717 | ctx=cli.tui.environment.install_upgrade >>>
审阅次数：2
升级并写入清单（-U）
<<< END U003697 >>>
<<< UNIT U003698 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1718-1718 | ctx=cli.tui.environment.interpreter_hint >>>
审阅次数：2
当前：${mode}。只列出这种托管方式下可用的操作。选择后再确认执行或预览。
<<< END U003698 >>>
<<< UNIT U003699 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1719-1719 | ctx=cli.tui.environment.interpreter_title >>>
审阅次数：2
解释器
<<< END U003699 >>>
<<< UNIT U003700 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1720-1720 | ctx=cli.tui.environment.label_add_package >>>
审阅次数：2
安装 ${spec}
<<< END U003700 >>>
<<< UNIT U003701 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1721-1721 | ctx=cli.tui.environment.label_adopt >>>
审阅次数：2
改用托管 venv
<<< END U003701 >>>
<<< UNIT U003702 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1722-1722 | ctx=cli.tui.environment.label_dry_run >>>
审阅次数：2
预览${label}
<<< END U003702 >>>
<<< UNIT U003703 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1723-1723 | ctx=cli.tui.environment.label_recreate >>>
审阅次数：2
重建实例 venv
<<< END U003703 >>>
<<< UNIT U003704 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1724-1724 | ctx=cli.tui.environment.label_release >>>
审阅次数：2
改用系统解释器
<<< END U003704 >>>
<<< UNIT U003705 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1725-1725 | ctx=cli.tui.environment.label_remove_package >>>
审阅次数：2
卸载 ${dist}
<<< END U003705 >>>
<<< UNIT U003706 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1726-1726 | ctx=cli.tui.environment.mode_external >>>
审阅次数：2
当前解释器（未托管 venv）
<<< END U003706 >>>
<<< UNIT U003707 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1727-1727 | ctx=cli.tui.environment.mode_managed >>>
审阅次数：2
托管 venv（${venv}）
<<< END U003707 >>>
<<< UNIT U003708 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1728-1728 | ctx=cli.tui.environment.mode_missing >>>
审阅次数：2
无法读取托管方式，环境操作不可用
<<< END U003708 >>>
<<< UNIT U003709 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1729-1729 | ctx=cli.tui.environment.mode_unknown >>>
审阅次数：2
托管方式未知
<<< END U003709 >>>
<<< UNIT U003710 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1730-1730 | ctx=cli.tui.environment.no_selection >>>
审阅次数：2
请选择一个包
<<< END U003710 >>>
<<< UNIT U003711 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1731-1731 | ctx=cli.tui.environment.not_managed >>>
审阅次数：2
实例未使用托管 venv，请先选择“改用托管 venv”
<<< END U003711 >>>
<<< UNIT U003712 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1732-1732 | ctx=cli.tui.environment.package_blocked >>>
审阅次数：2
无法读取实例环境（${reason}），请修复后安装或卸载
<<< END U003712 >>>
<<< UNIT U003713 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1733-1733 | ctx=cli.tui.environment.package_count >>>
审阅次数：2
${count} 个包
<<< END U003713 >>>
<<< UNIT U003714 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1734-1734 | ctx=cli.tui.environment.probe_failed >>>
审阅次数：2
包列表探测失败
<<< END U003714 >>>
<<< UNIT U003715 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1735-1735 | ctx=cli.tui.environment.recorded_only >>>
审阅次数：2
仅显示清单记录
<<< END U003715 >>>
<<< UNIT U003716 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1736-1736 | ctx=cli.tui.environment.recreate_mismatch >>>
审阅次数：2
输入内容不匹配，已取消重建。
<<< END U003716 >>>
<<< UNIT U003717 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1737-1737 | ctx=cli.tui.environment.recreate_token >>>
审阅次数：2
重建
<<< END U003717 >>>
<<< UNIT U003718 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1738-1738 | ctx=cli.tui.environment.recreate_type_hint >>>
审阅次数：2
将删除并重建 ${path}，未写入清单的额外运行库需重新安装。输入“${token}”确认。
<<< END U003718 >>>
<<< UNIT U003719 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1739-1739 | ctx=cli.tui.environment.requirement_count >>>
审阅次数：2
${count} 条记录
<<< END U003719 >>>
<<< UNIT U003720 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1740-1740 | ctx=cli.tui.environment.requirements_none >>>
审阅次数：2
暂无记录
<<< END U003720 >>>
<<< UNIT U003721 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1741-1741 | ctx=cli.tui.environment.restart_needed >>>
审阅次数：2
${label}已完成。重启实例后生效
<<< END U003721 >>>
<<< UNIT U003722 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1742-1742 | ctx=cli.tui.environment.running_blocked >>>
审阅次数：2
更改解释器前，请在运行页停止实例
<<< END U003722 >>>
<<< UNIT U003723 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1743-1743 | ctx=cli.tui.environment.search_placeholder >>>
审阅次数：2
搜索包名
<<< END U003723 >>>
<<< UNIT U003724 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1744-1744 | ctx=cli.tui.environment.selected_depended_by >>>
审阅次数：2
被 ${names} 依赖
<<< END U003724 >>>
<<< UNIT U003725 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1745-1745 | ctx=cli.tui.environment.selected_none >>>
审阅次数：2
未选中
<<< END U003725 >>>
<<< UNIT U003726 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1746-1746 | ctx=cli.tui.environment.selected_url >>>
审阅次数：2
来源：${url}
<<< END U003726 >>>
<<< UNIT U003727 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1747-1747 | ctx=cli.tui.environment.src_bad_json >>>
审阅次数：2
环境状态输出无法解析：${error}
<<< END U003727 >>>
<<< UNIT U003728 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1748-1748 | ctx=cli.tui.environment.src_bad_payload >>>
审阅次数：2
环境状态输出不是 JSON 对象
<<< END U003728 >>>
<<< UNIT U003729 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1749-1749 | ctx=cli.tui.environment.src_exit_code >>>
审阅次数：2
`${cmd}` 退出码 ${code}，未返回内容
<<< END U003729 >>>
<<< UNIT U003730 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1750-1750 | ctx=cli.tui.environment.src_oserror >>>
审阅次数：2
命令 ${cmd} 执行失败：${error}
<<< END U003730 >>>
<<< UNIT U003731 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1751-1751 | ctx=cli.tui.environment.src_timeout >>>
审阅次数：2
命令 ${cmd} 超时（${seconds} 秒）
<<< END U003731 >>>
<<< UNIT U003732 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1752-1752 | ctx=cli.tui.environment.state_running >>>
审阅次数：2
运行中
<<< END U003732 >>>
<<< UNIT U003733 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1753-1753 | ctx=cli.tui.environment.state_stopped >>>
审阅次数：2
未运行
<<< END U003733 >>>
<<< UNIT U003734 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1754-1754 | ctx=cli.tui.environment.status_cached >>>
审阅次数：2
缓存于 ${age} 秒前
<<< END U003734 >>>
<<< UNIT U003735 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1755-1755 | ctx=cli.tui.environment.status_load_failed >>>
审阅次数：2
读取环境失败：${error}
<<< END U003735 >>>
<<< UNIT U003736 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1756-1756 | ctx=cli.tui.environment.status_loaded >>>
审阅次数：2
已读取环境：${count} 个包
<<< END U003736 >>>
<<< UNIT U003737 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1757-1757 | ctx=cli.tui.environment.status_loading >>>
审阅次数：2
正在读取环境…
<<< END U003737 >>>
<<< UNIT U003738 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1758-1758 | ctx=cli.tui.environment.status_pending >>>
审阅次数：2
显示 ${shown} / ${total} 个包
<<< END U003738 >>>
<<< UNIT U003739 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1759-1759 | ctx=cli.tui.environment.stub_action_ok >>>
审阅次数：2
环境已更改
<<< END U003739 >>>
<<< UNIT U003740 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1760-1760 | ctx=cli.tui.environment.tag_adapter >>>
审阅次数：2
适配器
<<< END U003740 >>>
<<< UNIT U003741 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1762-1762 | ctx=cli.tui.environment.tag_editable >>>
审阅次数：2
可编辑
<<< END U003741 >>>
<<< UNIT U003742 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1763-1763 | ctx=cli.tui.environment.tag_missing >>>
审阅次数：2
未安装
<<< END U003742 >>>
<<< UNIT U003743 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1764-1764 | ctx=cli.tui.environment.tag_module >>>
审阅次数：2
模块
<<< END U003743 >>>
<<< UNIT U003744 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1765-1765 | ctx=cli.tui.environment.uninstall_cancelled >>>
审阅次数：2
已取消卸载
<<< END U003744 >>>
<<< UNIT U003745 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1766-1766 | ctx=cli.tui.environment.uninstall_confirm >>>
审阅次数：2
将从当前环境卸载 ${dist}，保留清单记录。
<<< END U003745 >>>
<<< UNIT U003746 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1767-1767 | ctx=cli.tui.environment.uninstall_confirm_action >>>
审阅次数：2
卸载
<<< END U003746 >>>
<<< UNIT U003747 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1768-1768 | ctx=cli.tui.environment.uninstall_drop_record >>>
审阅次数：2
移除记录并卸载
<<< END U003747 >>>
<<< UNIT U003748 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1769-1769 | ctx=cli.tui.environment.uninstall_hint >>>
审阅次数：2
移除清单记录后，重建环境时不会自动安装此运行库。
<<< END U003748 >>>
<<< UNIT U003749 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1770-1770 | ctx=cli.tui.environment.uninstall_keep_record >>>
审阅次数：2
卸载并保留记录
<<< END U003749 >>>
<<< UNIT U003750 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1771-1771 | ctx=cli.tui.environment.uninstall_title >>>
审阅次数：2
确认卸载 ${dist}
<<< END U003750 >>>
<<< UNIT U003751 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1772-1772 | ctx=cli.tui.environment.value_unknown >>>
审阅次数：2
未知
<<< END U003751 >>>
<<< UNIT U003752 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1773-1773 | ctx=cli.tui.logs.action_clear >>>
审阅次数：2
清屏
<<< END U003752 >>>
<<< UNIT U003753 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1774-1774 | ctx=cli.tui.logs.action_pause >>>
审阅次数：2
暂停
<<< END U003753 >>>
<<< UNIT U003754 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1775-1775 | ctx=cli.tui.logs.action_rescan >>>
审阅次数：2
刷新
<<< END U003754 >>>
<<< UNIT U003755 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1776-1776 | ctx=cli.tui.logs.action_resume >>>
审阅次数：2
恢复
<<< END U003755 >>>
<<< UNIT U003756 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1777-1777 | ctx=cli.tui.logs.all_processes >>>
审阅次数：2
全部进程
<<< END U003756 >>>
<<< UNIT U003757 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1778-1778 | ctx=cli.tui.logs.bind_clear >>>
审阅次数：2
清屏
<<< END U003757 >>>
<<< UNIT U003758 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1779-1779 | ctx=cli.tui.logs.bind_clear_filter >>>
审阅次数：2
清空过滤
<<< END U003758 >>>
<<< UNIT U003759 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1780-1780 | ctx=cli.tui.logs.bind_filter >>>
审阅次数：2
关键词过滤
<<< END U003759 >>>
<<< UNIT U003760 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1781-1781 | ctx=cli.tui.logs.bind_rescan >>>
审阅次数：2
刷新
<<< END U003760 >>>
<<< UNIT U003761 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1782-1782 | ctx=cli.tui.logs.bind_toggle_pause >>>
审阅次数：2
暂停 / 恢复
<<< END U003761 >>>
<<< UNIT U003762 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1783-1783 | ctx=cli.tui.logs.button_debug_menu >>>
审阅次数：2
日志级别…
<<< END U003762 >>>
<<< UNIT U003763 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1784-1784 | ctx=cli.tui.logs.cancel >>>
审阅次数：2
取消
<<< END U003763 >>>
<<< UNIT U003764 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1785-1785 | ctx=cli.tui.logs.debug_auto >>>
审阅次数：2
自动
<<< END U003764 >>>
<<< UNIT U003765 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1786-1786 | ctx=cli.tui.logs.debug_debug >>>
审阅次数：2
仅 debug
<<< END U003765 >>>
<<< UNIT U003766 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1787-1787 | ctx=cli.tui.logs.debug_info >>>
审阅次数：2
仅 INFO
<<< END U003766 >>>
<<< UNIT U003767 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1788-1788 | ctx=cli.tui.logs.debug_menu_hint >>>
审阅次数：2
当前：${label}。自动跟随最新的日志文件。仅 INFO 与仅 debug 优先跟随对应级别的文件，没有时回退到最新文件。
<<< END U003767 >>>
<<< UNIT U003768 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1789-1789 | ctx=cli.tui.logs.debug_menu_title >>>
审阅次数：2
日志级别
<<< END U003768 >>>
<<< UNIT U003769 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1790-1790 | ctx=cli.tui.logs.filter_empty >>>
审阅次数：2
未找到包含“${keyword}”的日志
<<< END U003769 >>>
<<< UNIT U003770 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1791-1791 | ctx=cli.tui.logs.filter_placeholder >>>
审阅次数：2
过滤日志行：按 / 聚焦，Esc 清空
<<< END U003770 >>>
<<< UNIT U003771 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1792-1792 | ctx=cli.tui.logs.following >>>
审阅次数：2
跟踪中
<<< END U003771 >>>
<<< UNIT U003772 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1793-1793 | ctx=cli.tui.logs.log_empty >>>
审阅次数：2
暂无日志，等待新内容或按 r 扫描
<<< END U003772 >>>
<<< UNIT U003773 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1794-1794 | ctx=cli.tui.logs.paused >>>
审阅次数：2
已暂停
<<< END U003773 >>>
<<< UNIT U003774 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1795-1795 | ctx=cli.tui.logs.process_item >>>
审阅次数：2
${name}（${count} 个文件）
<<< END U003774 >>>
<<< UNIT U003775 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1796-1796 | ctx=cli.tui.logs.reading >>>
审阅次数：2
正在读取日志目录
<<< END U003775 >>>
<<< UNIT U003776 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1797-1797 | ctx=cli.tui.logs.src_dir_missing >>>
审阅次数：2
日志目录不存在：${path}
<<< END U003776 >>>
<<< UNIT U003777 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1798-1798 | ctx=cli.tui.logs.src_dir_unreadable >>>
审阅次数：2
日志目录不可读：${path}（${error}）
<<< END U003777 >>>
<<< UNIT U003778 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1799-1799 | ctx=cli.tui.logs.src_file_read_failed >>>
审阅次数：2
日志文件读取失败：${path}（${error}）
<<< END U003778 >>>
<<< UNIT U003779 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1800-1800 | ctx=cli.tui.logs.src_file_unreadable >>>
审阅次数：2
日志文件不可读：${path}（${error}）
<<< END U003779 >>>
<<< UNIT U003780 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1801-1801 | ctx=cli.tui.logs.src_no_instance >>>
审阅次数：2
未找到实例（缺少 akaribot.toml），无法定位日志目录
<<< END U003780 >>>
<<< UNIT U003781 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1802-1802 | ctx=cli.tui.logs.src_stub_refused >>>
审阅次数：2
模拟数据源拒绝读取 ${name}
<<< END U003781 >>>
<<< UNIT U003782 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1803-1803 | ctx=cli.tui.logs.status_buffer >>>
审阅次数：2
缓冲 ${buffered}/${limit} 行
<<< END U003782 >>>
<<< UNIT U003783 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1804-1804 | ctx=cli.tui.logs.status_cleared >>>
审阅次数：2
已清空显示，从偏移 ${offset} 继续跟踪
<<< END U003783 >>>
<<< UNIT U003784 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1805-1805 | ctx=cli.tui.logs.status_dropped >>>
审阅次数：2
丢弃 ${dropped} 行
<<< END U003784 >>>
<<< UNIT U003785 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1806-1806 | ctx=cli.tui.logs.status_filter >>>
审阅次数：2
“${keyword}”匹配 ${hits} 行
<<< END U003785 >>>
<<< UNIT U003786 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1807-1807 | ctx=cli.tui.logs.status_follow_failed >>>
审阅次数：2
跟踪失败：${error}
<<< END U003786 >>>
<<< UNIT U003787 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1808-1808 | ctx=cli.tui.logs.status_no_files >>>
审阅次数：2
没有日志文件（过滤：${filter_name}）
<<< END U003787 >>>
<<< UNIT U003788 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1809-1809 | ctx=cli.tui.logs.status_pending >>>
审阅次数：2
末行尚未写完，等待后续内容
<<< END U003788 >>>
<<< UNIT U003789 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1810-1810 | ctx=cli.tui.logs.status_reset >>>
审阅次数：2
文件被截断或轮转，已从头读取
<<< END U003789 >>>
<<< UNIT U003790 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1811-1811 | ctx=cli.tui.logs.status_resume_hint >>>
审阅次数：2
按空格恢复跟踪
<<< END U003790 >>>
<<< UNIT U003791 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1812-1812 | ctx=cli.tui.logs.status_scan_failed >>>
审阅次数：2
读取日志目录失败：${error}
<<< END U003791 >>>
<<< UNIT U003792 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1814-1814 | ctx=cli.tui.logs.status_tail_failed >>>
审阅次数：2
读取日志尾部失败：${error}
<<< END U003792 >>>
<<< UNIT U003793 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1815-1815 | ctx=cli.tui.logs.target_following >>>
审阅次数：2
跟踪：${name}（进程 ${process}，${level}，偏移 ${offset} 字节，${state}）
<<< END U003793 >>>
<<< UNIT U003794 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1816-1816 | ctx=cli.tui.logs.target_none >>>
审阅次数：2
跟踪：未选择
<<< END U003794 >>>
<<< UNIT U003795 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1817-1817 | ctx=cli.tui.logs.target_none_filtered >>>
审阅次数：2
跟踪：未选择（过滤：${filter_name}）
<<< END U003795 >>>
<<< UNIT U003796 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1818-1818 | ctx=cli.tui.misc.bind_dry_run >>>
审阅次数：2
预览迁移
<<< END U003796 >>>
<<< UNIT U003797 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1819-1819 | ctx=cli.tui.misc.bind_migrate >>>
审阅次数：2
迁移项目
<<< END U003797 >>>
<<< UNIT U003798 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1820-1820 | ctx=cli.tui.misc.button_migrate >>>
审阅次数：2
迁移项目
<<< END U003798 >>>
<<< UNIT U003799 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1821-1821 | ctx=cli.tui.misc.calling >>>
审阅次数：2
正在迁移 ${project}…
<<< END U003799 >>>
<<< UNIT U003800 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1822-1822 | ctx=cli.tui.misc.calling_dry_run >>>
审阅次数：2
正在预览 ${project} 的迁移计划…
<<< END U003800 >>>
<<< UNIT U003801 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1823-1823 | ctx=cli.tui.misc.cancelled >>>
审阅次数：2
已取消迁移
<<< END U003801 >>>
<<< UNIT U003802 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1824-1824 | ctx=cli.tui.misc.choice_dry_run >>>
审阅次数：2
预览迁移
<<< END U003802 >>>
<<< UNIT U003803 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1825-1825 | ctx=cli.tui.misc.choice_hint >>>
审阅次数：2
源目录：${project}。迁移将向当前实例写入配置与数据。预览仅显示操作计划。
<<< END U003803 >>>
<<< UNIT U003804 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1826-1826 | ctx=cli.tui.misc.choice_migrate >>>
审阅次数：2
执行迁移
<<< END U003804 >>>
<<< UNIT U003805 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1827-1827 | ctx=cli.tui.misc.choice_options >>>
审阅次数：2
迁移参数：${options}
<<< END U003805 >>>
<<< UNIT U003806 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1828-1828 | ctx=cli.tui.misc.choice_options_none >>>
审阅次数：2
无附加参数
<<< END U003806 >>>
<<< UNIT U003807 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1829-1829 | ctx=cli.tui.misc.confirm_migrate_again >>>
审阅次数：2
确认间隔过短，未执行迁移。请按 Enter 重新确认。
<<< END U003807 >>>
<<< UNIT U003808 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1830-1830 | ctx=cli.tui.misc.confirm_migrate_pending >>>
审阅次数：2
等待确认迁移 ${project} 的配置与数据到当前实例。源目录只读。
<<< END U003808 >>>
<<< UNIT U003809 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1831-1831 | ctx=cli.tui.misc.dialog_cancel >>>
审阅次数：2
取消
<<< END U003809 >>>
<<< UNIT U003810 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1832-1832 | ctx=cli.tui.misc.dialog_confirm >>>
审阅次数：2
下一步
<<< END U003810 >>>
<<< UNIT U003811 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1833-1833 | ctx=cli.tui.misc.dialog_hint >>>
审阅次数：2
源目录必须包含 bot.py、core/、modules/ 与 config/config.toml。源目录只读，支持重复迁移。报告保存为当前实例中的 migration-report.md。
<<< END U003811 >>>
<<< UNIT U003812 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1834-1834 | ctx=cli.tui.misc.dialog_placeholder >>>
审阅次数：2
旧项目根目录，如 /srv/akaribot-old
<<< END U003812 >>>
<<< UNIT U003813 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1835-1835 | ctx=cli.tui.misc.dialog_title >>>
审阅次数：2
确认迁移旧版项目
<<< END U003813 >>>
<<< UNIT U003814 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1836-1836 | ctx=cli.tui.misc.dry_run_need_path >>>
审阅次数：2
按 Enter 输入源目录，再按 p 预览迁移。
<<< END U003814 >>>
<<< UNIT U003815 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1838-1838 | ctx=cli.tui.misc.hint >>>
审阅次数：2
将旧版项目的配置与数据迁移到当前实例。
<<< END U003815 >>>
<<< UNIT U003816 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1839-1839 | ctx=cli.tui.misc.label_dry_run >>>
审阅次数：2
预览迁移
<<< END U003816 >>>
<<< UNIT U003817 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1840-1840 | ctx=cli.tui.misc.label_migrate >>>
审阅次数：2
迁移项目
<<< END U003817 >>>
<<< UNIT U003818 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1841-1841 | ctx=cli.tui.misc.option_force >>>
审阅次数：2
覆盖已有文件
<<< END U003818 >>>
<<< UNIT U003819 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1842-1842 | ctx=cli.tui.misc.option_no_venv >>>
审阅次数：2
不创建 venv
<<< END U003819 >>>
<<< UNIT U003820 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1843-1843 | ctx=cli.tui.misc.option_offline >>>
审阅次数：2
离线
<<< END U003820 >>>
<<< UNIT U003821 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1844-1844 | ctx=cli.tui.misc.option_skip_install >>>
审阅次数：2
跳过安装
<<< END U003821 >>>
<<< UNIT U003822 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1845-1845 | ctx=cli.tui.misc.stub_migrate_ok >>>
审阅次数：2
迁移完成
<<< END U003822 >>>
<<< UNIT U003823 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1846-1846 | ctx=cli.tui.misc.timeout >>>
审阅次数：2
${label}超时（${seconds} 秒），已停止等待
<<< END U003823 >>>
<<< UNIT U003824 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1847-1847 | ctx=cli.tui.modules.action_install >>>
审阅次数：2
安装
<<< END U003824 >>>
<<< UNIT U003825 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1848-1848 | ctx=cli.tui.modules.action_load >>>
审阅次数：2
装载
<<< END U003825 >>>
<<< UNIT U003826 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1849-1849 | ctx=cli.tui.modules.action_refresh >>>
审阅次数：2
刷新
<<< END U003826 >>>
<<< UNIT U003827 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1850-1850 | ctx=cli.tui.modules.action_uninstall >>>
审阅次数：2
卸载
<<< END U003827 >>>
<<< UNIT U003828 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1851-1851 | ctx=cli.tui.modules.action_unload >>>
审阅次数：2
取消装载
<<< END U003828 >>>
<<< UNIT U003829 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1852-1852 | ctx=cli.tui.modules.action_update >>>
审阅次数：2
更新
<<< END U003829 >>>
<<< UNIT U003830 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1853-1853 | ctx=cli.tui.modules.available_failed >>>
审阅次数：2
（读取可安装模块失败：${error}）
<<< END U003830 >>>
<<< UNIT U003831 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1854-1854 | ctx=cli.tui.modules.batch_done >>>
审阅次数：2
已对 ${count} 个包执行${what}
<<< END U003831 >>>
<<< UNIT U003832 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1855-1855 | ctx=cli.tui.modules.batch_failed >>>
审阅次数：2
${what}：成功 ${ok} 个，失败 ${failed} 个（${names}）｜${detail}
<<< END U003832 >>>
<<< UNIT U003833 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1856-1856 | ctx=cli.tui.modules.batch_label >>>
审阅次数：2
${label} 等 ${count} 个
<<< END U003833 >>>
<<< UNIT U003834 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1858-1858 | ctx=cli.tui.modules.bind_clear_search >>>
审阅次数：2
清空搜索
<<< END U003834 >>>
<<< UNIT U003835 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1859-1859 | ctx=cli.tui.modules.bind_clear_selection >>>
审阅次数：2
清空选择
<<< END U003835 >>>
<<< UNIT U003836 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1860-1860 | ctx=cli.tui.modules.bind_extend >>>
审阅次数：2
Shift+↑/↓ 扩展选择
<<< END U003836 >>>
<<< UNIT U003837 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1861-1861 | ctx=cli.tui.modules.bind_load >>>
审阅次数：2
装载 / 取消装载
<<< END U003837 >>>
<<< UNIT U003838 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1862-1862 | ctx=cli.tui.modules.bind_search >>>
审阅次数：2
搜索
<<< END U003838 >>>
<<< UNIT U003839 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1863-1863 | ctx=cli.tui.modules.bind_select_all >>>
审阅次数：2
全选
<<< END U003839 >>>
<<< UNIT U003840 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1864-1864 | ctx=cli.tui.modules.bind_toggle_select >>>
审阅次数：2
选择
<<< END U003840 >>>
<<< UNIT U003841 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1865-1865 | ctx=cli.tui.modules.busy >>>
审阅次数：2
已有安装或卸载操作正在进行
<<< END U003841 >>>
<<< UNIT U003842 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1866-1866 | ctx=cli.tui.modules.button_load >>>
审阅次数：2
装载 / 取消装载
<<< END U003842 >>>
<<< UNIT U003843 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1867-1867 | ctx=cli.tui.modules.calling >>>
审阅次数：2
正在${label}…
<<< END U003843 >>>
<<< UNIT U003844 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1868-1868 | ctx=cli.tui.modules.cancel >>>
审阅次数：2
取消
<<< END U003844 >>>
<<< UNIT U003845 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1869-1869 | ctx=cli.tui.modules.column_load >>>
审阅次数：2
装载
<<< END U003845 >>>
<<< UNIT U003846 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1870-1870 | ctx=cli.tui.modules.column_name >>>
审阅次数：2
名称
<<< END U003846 >>>
<<< UNIT U003847 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1871-1871 | ctx=cli.tui.modules.column_summary >>>
审阅次数：2
简介
<<< END U003847 >>>
<<< UNIT U003848 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1872-1872 | ctx=cli.tui.modules.column_version >>>
审阅次数：2
版本
<<< END U003848 >>>
<<< UNIT U003849 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1873-1873 | ctx=cli.tui.modules.count >>>
审阅次数：2
显示 ${shown}/${total}，已安装 ${installed}
<<< END U003849 >>>
<<< UNIT U003850 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1874-1874 | ctx=cli.tui.modules.count_selected >>>
审阅次数：2
已选 ${count} 项
<<< END U003850 >>>
<<< UNIT U003851 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1875-1875 | ctx=cli.tui.modules.detail_placeholder >>>
审阅次数：2
选择模块查看详情
<<< END U003851 >>>
<<< UNIT U003852 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1876-1876 | ctx=cli.tui.modules.field_config_table >>>
审阅次数：2
配置表
<<< END U003852 >>>
<<< UNIT U003853 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1877-1877 | ctx=cli.tui.modules.field_core_api >>>
审阅次数：2
核心 API
<<< END U003853 >>>
<<< UNIT U003854 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1878-1878 | ctx=cli.tui.modules.field_dependents >>>
审阅次数：2
依赖方
<<< END U003854 >>>
<<< UNIT U003855 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1879-1879 | ctx=cli.tui.modules.field_developers >>>
审阅次数：2
作者
<<< END U003855 >>>
<<< UNIT U003856 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1880-1880 | ctx=cli.tui.modules.field_dist >>>
审阅次数：2
发行包
<<< END U003856 >>>
<<< UNIT U003857 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1881-1881 | ctx=cli.tui.modules.field_kind >>>
审阅次数：2
类型
<<< END U003857 >>>
<<< UNIT U003858 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1882-1882 | ctx=cli.tui.modules.field_load >>>
审阅次数：2
模块装载
<<< END U003858 >>>
<<< UNIT U003859 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1883-1883 | ctx=cli.tui.modules.field_name >>>
审阅次数：2
名称
<<< END U003859 >>>
<<< UNIT U003860 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1884-1884 | ctx=cli.tui.modules.field_origin >>>
审阅次数：2
来源
<<< END U003860 >>>
<<< UNIT U003861 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1885-1885 | ctx=cli.tui.modules.field_provides >>>
审阅次数：2
提供模块
<<< END U003861 >>>
<<< UNIT U003862 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1886-1886 | ctx=cli.tui.modules.field_state >>>
审阅次数：2
状态
<<< END U003862 >>>
<<< UNIT U003863 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1887-1887 | ctx=cli.tui.modules.field_summary >>>
审阅次数：2
简介
<<< END U003863 >>>
<<< UNIT U003864 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1888-1888 | ctx=cli.tui.modules.field_tables >>>
审阅次数：2
数据表
<<< END U003864 >>>
<<< UNIT U003865 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1889-1889 | ctx=cli.tui.modules.field_version >>>
审阅次数：2
版本
<<< END U003865 >>>
<<< UNIT U003866 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1890-1890 | ctx=cli.tui.modules.hint_empty >>>
审阅次数：2
没有模块。按 r 刷新，或输入模块名后按 i 安装
<<< END U003866 >>>
<<< UNIT U003867 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1891-1891 | ctx=cli.tui.modules.hint_no_match >>>
审阅次数：2
没有匹配的模块，按 Esc 清空搜索
<<< END U003867 >>>
<<< UNIT U003868 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1892-1892 | ctx=cli.tui.modules.hint_select >>>
审阅次数：2
选择模块查看详情
<<< END U003868 >>>
<<< UNIT U003869 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1893-1893 | ctx=cli.tui.modules.install_cancelled >>>
审阅次数：2
已取消安装
<<< END U003869 >>>
<<< UNIT U003870 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1894-1894 | ctx=cli.tui.modules.install_confirm >>>
审阅次数：2
下一步
<<< END U003870 >>>
<<< UNIT U003871 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1895-1895 | ctx=cli.tui.modules.install_confirm_hint >>>
审阅次数：2
将安装以下包，并为它们补充配置、应用数据库迁移：
${names}
<<< END U003871 >>>
<<< UNIT U003872 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1896-1896 | ctx=cli.tui.modules.install_confirm_title >>>
审阅次数：2
安装 ${count} 个模块
<<< END U003872 >>>
<<< UNIT U003873 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1897-1897 | ctx=cli.tui.modules.install_editable >>>
审阅次数：2
可编辑安装本地目录
<<< END U003873 >>>
<<< UNIT U003874 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1898-1898 | ctx=cli.tui.modules.install_from_git >>>
审阅次数：2
从 Git 仓库安装
<<< END U003874 >>>
<<< UNIT U003875 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1899-1899 | ctx=cli.tui.modules.install_from_registry >>>
审阅次数：2
从软件源安装
<<< END U003875 >>>
<<< UNIT U003876 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1900-1900 | ctx=cli.tui.modules.install_hint >>>
审阅次数：2
输入模块名、git+ 地址、仓库地址或本地目录路径
<<< END U003876 >>>
<<< UNIT U003877 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1901-1901 | ctx=cli.tui.modules.install_placeholder >>>
审阅次数：2
模块名或地址
<<< END U003877 >>>
<<< UNIT U003878 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1902-1902 | ctx=cli.tui.modules.install_target_hint >>>
审阅次数：2
模块名从软件源安装，仓库地址通过 Git 安装，本地目录以可编辑方式安装
<<< END U003878 >>>
<<< UNIT U003879 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1903-1903 | ctx=cli.tui.modules.install_target_title >>>
审阅次数：2
确认安装 ${spec}
<<< END U003879 >>>
<<< UNIT U003880 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1904-1904 | ctx=cli.tui.modules.install_title >>>
审阅次数：2
安装模块
<<< END U003880 >>>
<<< UNIT U003881 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1905-1905 | ctx=cli.tui.modules.install_unknown_spec >>>
审阅次数：2
无法识别的安装目标：${spec}
<<< END U003881 >>>
<<< UNIT U003882 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1906-1906 | ctx=cli.tui.modules.installed_only >>>
审阅次数：2
仅已安装
<<< END U003882 >>>
<<< UNIT U003883 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1907-1907 | ctx=cli.tui.modules.kind_adapter >>>
审阅次数：2
适配器
<<< END U003883 >>>
<<< UNIT U003884 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1908-1908 | ctx=cli.tui.modules.kind_core >>>
审阅次数：2
核心
<<< END U003884 >>>
<<< UNIT U003885 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1909-1909 | ctx=cli.tui.modules.kind_module >>>
审阅次数：2
模块
<<< END U003885 >>>
<<< UNIT U003886 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1910-1910 | ctx=cli.tui.modules.kind_testing >>>
审阅次数：2
测试
<<< END U003886 >>>
<<< UNIT U003887 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1911-1911 | ctx=cli.tui.modules.label_install >>>
审阅次数：2
安装 ${name}
<<< END U003887 >>>
<<< UNIT U003888 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1912-1912 | ctx=cli.tui.modules.label_load >>>
审阅次数：2
装载 ${name}
<<< END U003888 >>>
<<< UNIT U003889 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1913-1913 | ctx=cli.tui.modules.label_uninstall >>>
审阅次数：2
卸载 ${name}
<<< END U003889 >>>
<<< UNIT U003890 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1914-1914 | ctx=cli.tui.modules.label_unload >>>
审阅次数：2
取消装载 ${name}
<<< END U003890 >>>
<<< UNIT U003891 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1915-1915 | ctx=cli.tui.modules.label_update >>>
审阅次数：2
更新 ${name}
<<< END U003891 >>>
<<< UNIT U003892 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1916-1916 | ctx=cli.tui.modules.load_cell >>>
审阅次数：2
装载 ${loaded}/${total}
<<< END U003892 >>>
<<< UNIT U003893 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1917-1917 | ctx=cli.tui.modules.load_cell_unknown >>>
审阅次数：2
装载 ?
<<< END U003893 >>>
<<< UNIT U003894 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1918-1918 | ctx=cli.tui.modules.load_state_hint >>>
审阅次数：2
实例未运行时，装载状态可能为上次退出前的记录
<<< END U003894 >>>
<<< UNIT U003895 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1919-1919 | ctx=cli.tui.modules.notify_failed >>>
审阅次数：2
${count} 个包操作失败
<<< END U003895 >>>
<<< UNIT U003896 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1920-1920 | ctx=cli.tui.modules.operation_done >>>
审阅次数：2
${label}完成
<<< END U003896 >>>
<<< UNIT U003897 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1921-1921 | ctx=cli.tui.modules.pick_install >>>
审阅次数：2
请选择未安装的模块，或在搜索框输入模块名
<<< END U003897 >>>
<<< UNIT U003898 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1922-1922 | ctx=cli.tui.modules.pick_load >>>
审阅次数：2
请选择已安装且声明模块的包，再按 e
<<< END U003898 >>>
<<< UNIT U003899 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1923-1923 | ctx=cli.tui.modules.pick_uninstall >>>
审阅次数：2
请选择已安装的模块
<<< END U003899 >>>
<<< UNIT U003900 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1924-1924 | ctx=cli.tui.modules.purge_batch_token >>>
审阅次数：2
清理 ${count} 个包
<<< END U003900 >>>
<<< UNIT U003901 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1925-1925 | ctx=cli.tui.modules.purge_confirm >>>
审阅次数：2
清理并卸载
<<< END U003901 >>>
<<< UNIT U003902 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1926-1926 | ctx=cli.tui.modules.purge_hint >>>
审阅次数：2
目标包：${names}
配置文件：${files}
数据表：${tables}
删除后无法恢复。输入“${token}”以确认清理并卸载。
<<< END U003902 >>>
<<< UNIT U003903 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1927-1927 | ctx=cli.tui.modules.purge_mismatch >>>
审阅次数：2
确认文字不符，已取消清理与卸载
<<< END U003903 >>>
<<< UNIT U003904 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1928-1928 | ctx=cli.tui.modules.purge_placeholder >>>
审阅次数：2
输入上方确认文字
<<< END U003904 >>>
<<< UNIT U003905 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1929-1929 | ctx=cli.tui.modules.purge_title >>>
审阅次数：2
确认清理数据并卸载 ${count} 个包
<<< END U003905 >>>
<<< UNIT U003906 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1930-1930 | ctx=cli.tui.modules.refreshing >>>
审阅次数：2
${message}，正在刷新列表…
<<< END U003906 >>>
<<< UNIT U003907 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1931-1931 | ctx=cli.tui.modules.search_placeholder >>>
审阅次数：2
搜索模块名、发行包或简介，以空格分词
<<< END U003907 >>>
<<< UNIT U003908 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1932-1932 | ctx=cli.tui.modules.src_bad_json >>>
审阅次数：2
`${label}` 输出无法解析为 JSON：${error}
<<< END U003908 >>>
<<< UNIT U003909 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1933-1933 | ctx=cli.tui.modules.src_bad_status >>>
审阅次数：2
`${label}` 的输出缺少模块列表
<<< END U003909 >>>
<<< UNIT U003910 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1934-1934 | ctx=cli.tui.modules.src_empty_output >>>
审阅次数：2
`${label}` 未返回内容
<<< END U003910 >>>
<<< UNIT U003911 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1935-1935 | ctx=cli.tui.modules.src_exe_missing >>>
审阅次数：2
未找到可执行文件：${path}（${error}）
<<< END U003911 >>>
<<< UNIT U003912 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1936-1936 | ctx=cli.tui.modules.src_exit_code >>>
审阅次数：2
`${cmd}` 退出码 ${code}：${tail}
<<< END U003912 >>>
<<< UNIT U003913 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1937-1937 | ctx=cli.tui.modules.src_installed_failed >>>
审阅次数：2
Instance.installed() 失败：${kind}：${error}
<<< END U003913 >>>
<<< UNIT U003914 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1938-1938 | ctx=cli.tui.modules.src_instance_failed >>>
审阅次数：2
构造 Instance 失败：${kind}：${error}
<<< END U003914 >>>
<<< UNIT U003915 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1939-1939 | ctx=cli.tui.modules.src_instance_missing >>>
审阅次数：2
akaribot.cli.instance 不可用，无法读取模块
<<< END U003915 >>>
<<< UNIT U003916 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1940-1940 | ctx=cli.tui.modules.src_no_installed >>>
审阅次数：2
akaribot.cli.instance.Instance 未提供 installed()，无法读取模块
<<< END U003916 >>>
<<< UNIT U003917 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1941-1941 | ctx=cli.tui.modules.src_not_instance >>>
审阅次数：2
${root} 不是 AkariBot 实例（未找到 akaribot.toml）。请运行 `akaribot init`，或通过 AKARI_INSTANCE_DIR 指定实例根目录
<<< END U003917 >>>
<<< UNIT U003918 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1942-1942 | ctx=cli.tui.modules.src_oserror >>>
审阅次数：2
`${cmd}` 执行失败：${error}
<<< END U003918 >>>
<<< UNIT U003919 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1943-1943 | ctx=cli.tui.modules.src_timeout >>>
审阅次数：2
`${cmd}` 执行超时（${seconds} 秒）
<<< END U003919 >>>
<<< UNIT U003920 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1944-1944 | ctx=cli.tui.modules.state_available >>>
审阅次数：2
未安装
<<< END U003920 >>>
<<< UNIT U003921 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1945-1945 | ctx=cli.tui.modules.state_installed >>>
审阅次数：2
已安装
<<< END U003921 >>>
<<< UNIT U003922 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1946-1946 | ctx=cli.tui.modules.state_unknown >>>
审阅次数：2
状态未知
<<< END U003922 >>>
<<< UNIT U003923 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1947-1947 | ctx=cli.tui.modules.status_cached >>>
审阅次数：2
使用 ${age} 秒前的缓存，共 ${count} 个模块
<<< END U003923 >>>
<<< UNIT U003924 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1948-1948 | ctx=cli.tui.modules.status_load_failed >>>
审阅次数：2
读取失败：${error}
<<< END U003924 >>>
<<< UNIT U003925 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1949-1949 | ctx=cli.tui.modules.status_load_unavailable >>>
审阅次数：2
（装载状态读取失败：${error}）
<<< END U003925 >>>
<<< UNIT U003926 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1950-1950 | ctx=cli.tui.modules.status_loaded >>>
审阅次数：2
已读取 ${count} 个模块
<<< END U003926 >>>
<<< UNIT U003927 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1951-1951 | ctx=cli.tui.modules.status_loading >>>
审阅次数：2
正在读取模块列表…
<<< END U003927 >>>
<<< UNIT U003928 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1952-1952 | ctx=cli.tui.modules.status_pending >>>
审阅次数：2
尚未读取
<<< END U003928 >>>
<<< UNIT U003929 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1953-1953 | ctx=cli.tui.modules.stub_install_ok >>>
审阅次数：2
安装成功
<<< END U003929 >>>
<<< UNIT U003930 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1954-1954 | ctx=cli.tui.modules.stub_uninstall_ok >>>
审阅次数：2
卸载成功
<<< END U003930 >>>
<<< UNIT U003931 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1955-1955 | ctx=cli.tui.modules.uninstall_cancelled >>>
审阅次数：2
已取消卸载
<<< END U003931 >>>
<<< UNIT U003932 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1956-1956 | ctx=cli.tui.modules.uninstall_cascade >>>
审阅次数：2
同时卸载依赖方（--cascade）
<<< END U003932 >>>
<<< UNIT U003933 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1957-1957 | ctx=cli.tui.modules.uninstall_cascade_hint >>>
审阅次数：2
${names} 依赖本包，必须先卸载这些包
<<< END U003933 >>>
<<< UNIT U003934 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1958-1958 | ctx=cli.tui.modules.uninstall_confirm_many >>>
审阅次数：2
确认卸载 ${count} 个包：${names}
<<< END U003934 >>>
<<< UNIT U003935 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1959-1959 | ctx=cli.tui.modules.uninstall_confirm_one >>>
审阅次数：2
确认卸载 ${name}
<<< END U003935 >>>
<<< UNIT U003936 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1960-1960 | ctx=cli.tui.modules.uninstall_count_confirm >>>
审阅次数：2
确认卸载
<<< END U003936 >>>
<<< UNIT U003937 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1961-1961 | ctx=cli.tui.modules.uninstall_count_hint >>>
审阅次数：2
请输入目标数量 ${count}，确认批量卸载范围
<<< END U003937 >>>
<<< UNIT U003938 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1962-1962 | ctx=cli.tui.modules.uninstall_count_mismatch >>>
审阅次数：2
输入 ${given} 与目标数量 ${count} 不符，已取消卸载
<<< END U003938 >>>
<<< UNIT U003939 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1963-1963 | ctx=cli.tui.modules.uninstall_count_placeholder >>>
审阅次数：2
输入目标数量
<<< END U003939 >>>
<<< UNIT U003940 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1964-1964 | ctx=cli.tui.modules.uninstall_count_title >>>
审阅次数：2
确认卸载 ${count} 个包
<<< END U003940 >>>
<<< UNIT U003941 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1965-1965 | ctx=cli.tui.modules.uninstall_keep_data >>>
审阅次数：2
卸载并保留数据
<<< END U003941 >>>
<<< UNIT U003942 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1966-1966 | ctx=cli.tui.modules.uninstall_options_hint >>>
审阅次数：2
保留数据仅卸载包，清理数据同时删除配置文件和数据表
<<< END U003942 >>>
<<< UNIT U003943 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1967-1967 | ctx=cli.tui.modules.uninstall_purge_data >>>
审阅次数：2
卸载并清理数据（--purge-data）
<<< END U003943 >>>
<<< UNIT U003944 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1968-1968 | ctx=cli.tui.modules.update_all >>>
审阅次数：2
更新全部（--all）
<<< END U003944 >>>
<<< UNIT U003945 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1969-1969 | ctx=cli.tui.modules.update_all_target >>>
审阅次数：2
全部已安装的包
<<< END U003945 >>>
<<< UNIT U003946 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1970-1970 | ctx=cli.tui.modules.update_cancelled >>>
审阅次数：2
已取消更新
<<< END U003946 >>>
<<< UNIT U003947 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1971-1971 | ctx=cli.tui.modules.update_hint >>>
审阅次数：2
选择“更新全部”将逐个更新所有已安装的包
<<< END U003947 >>>
<<< UNIT U003948 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1972-1972 | ctx=cli.tui.modules.update_no_target >>>
审阅次数：2
没有可更新的选中项，请选择更新全部
<<< END U003948 >>>
<<< UNIT U003949 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1973-1973 | ctx=cli.tui.modules.update_selected >>>
审阅次数：2
更新选中项
<<< END U003949 >>>
<<< UNIT U003950 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1974-1974 | ctx=cli.tui.nav.adapters >>>
审阅次数：2
适配器
<<< END U003950 >>>
<<< UNIT U003951 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1975-1975 | ctx=cli.tui.nav.blurb.adapters >>>
审阅次数：2
平台适配器与实例
<<< END U003951 >>>
<<< UNIT U003952 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1976-1976 | ctx=cli.tui.nav.blurb.config >>>
审阅次数：2
配置表与文本
<<< END U003952 >>>
<<< UNIT U003953 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1977-1977 | ctx=cli.tui.nav.blurb.dashboard >>>
审阅次数：2
实例与服务状态
<<< END U003953 >>>
<<< UNIT U003954 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1978-1978 | ctx=cli.tui.nav.blurb.database >>>
审阅次数：2
数据库表与数据项
<<< END U003954 >>>
<<< UNIT U003955 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1979-1979 | ctx=cli.tui.nav.blurb.dev >>>
审阅次数：2
测试与脚手架
<<< END U003955 >>>
<<< UNIT U003956 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1980-1980 | ctx=cli.tui.nav.blurb.docs >>>
审阅次数：2
文档包的构建、预览与部署
<<< END U003956 >>>
<<< UNIT U003957 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1981-1981 | ctx=cli.tui.nav.blurb.doctor >>>
审阅次数：2
端口与登录信息检查
<<< END U003957 >>>
<<< UNIT U003958 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1982-1982 | ctx=cli.tui.nav.blurb.environment >>>
审阅次数：2
运行库与解释器
<<< END U003958 >>>
<<< UNIT U003959 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1983-1983 | ctx=cli.tui.nav.blurb.logs >>>
审阅次数：2
日志筛选与跟踪
<<< END U003959 >>>
<<< UNIT U003960 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1984-1984 | ctx=cli.tui.nav.blurb.misc >>>
审阅次数：2
旧项目迁移
<<< END U003960 >>>
<<< UNIT U003961 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1985-1985 | ctx=cli.tui.nav.blurb.modules >>>
审阅次数：2
模块安装、卸载与装载
<<< END U003961 >>>
<<< UNIT U003962 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1986-1986 | ctx=cli.tui.nav.blurb.run >>>
审阅次数：2
实例启动、停止及状态
<<< END U003962 >>>
<<< UNIT U003963 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1987-1987 | ctx=cli.tui.nav.config >>>
审阅次数：2
配置
<<< END U003963 >>>
<<< UNIT U003964 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1988-1988 | ctx=cli.tui.nav.dashboard >>>
审阅次数：2
概览
<<< END U003964 >>>
<<< UNIT U003965 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1989-1989 | ctx=cli.tui.nav.database >>>
审阅次数：2
数据库
<<< END U003965 >>>
<<< UNIT U003966 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1990-1990 | ctx=cli.tui.nav.dev >>>
审阅次数：2
开发
<<< END U003966 >>>
<<< UNIT U003967 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1991-1991 | ctx=cli.tui.nav.docs >>>
审阅次数：2
文档
<<< END U003967 >>>
<<< UNIT U003968 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1992-1992 | ctx=cli.tui.nav.doctor >>>
审阅次数：2
诊断
<<< END U003968 >>>
<<< UNIT U003969 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1993-1993 | ctx=cli.tui.nav.environment >>>
审阅次数：2
环境
<<< END U003969 >>>
<<< UNIT U003970 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1994-1994 | ctx=cli.tui.nav.group.data >>>
审阅次数：2
环境与数据
<<< END U003970 >>>
<<< UNIT U003971 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1995-1995 | ctx=cli.tui.nav.group.dev >>>
审阅次数：2
开发与迁移
<<< END U003971 >>>
<<< UNIT U003972 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1996-1996 | ctx=cli.tui.nav.group.platform >>>
审阅次数：2
配置与平台
<<< END U003972 >>>
<<< UNIT U003973 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1997-1997 | ctx=cli.tui.nav.group.runtime >>>
审阅次数：2
概览与运行
<<< END U003973 >>>
<<< UNIT U003974 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1998-1998 | ctx=cli.tui.nav.logs >>>
审阅次数：2
日志
<<< END U003974 >>>
<<< UNIT U003975 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1999-1999 | ctx=cli.tui.nav.misc >>>
审阅次数：2
迁移
<<< END U003975 >>>
<<< UNIT U003976 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2000-2000 | ctx=cli.tui.nav.modules >>>
审阅次数：2
模块
<<< END U003976 >>>
<<< UNIT U003977 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2001-2001 | ctx=cli.tui.nav.run >>>
审阅次数：2
运行
<<< END U003977 >>>
<<< UNIT U003978 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2002-2002 | ctx=cli.tui.run.adapter_cancel >>>
审阅次数：2
取消
<<< END U003978 >>>
<<< UNIT U003979 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2003-2003 | ctx=cli.tui.run.adapter_cancelled >>>
审阅次数：2
已取消适配器选择
<<< END U003979 >>>
<<< UNIT U003980 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2004-2004 | ctx=cli.tui.run.adapter_confirm >>>
审阅次数：2
继续
<<< END U003980 >>>
<<< UNIT U003981 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2005-2005 | ctx=cli.tui.run.adapter_hint >>>
审阅次数：2
输入平台名，仅启动该平台的适配器。平台名见“适配器”页。
<<< END U003981 >>>
<<< UNIT U003982 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2006-2006 | ctx=cli.tui.run.adapter_placeholder >>>
审阅次数：2
平台名，如 telegram
<<< END U003982 >>>
<<< UNIT U003983 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2007-2007 | ctx=cli.tui.run.adapter_title >>>
审阅次数：2
选择启动平台
<<< END U003983 >>>
<<< UNIT U003984 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2008-2008 | ctx=cli.tui.run.bind_adapter_start >>>
审阅次数：2
启动指定适配器
<<< END U003984 >>>
<<< UNIT U003985 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2009-2009 | ctx=cli.tui.run.bind_refresh >>>
审阅次数：2
刷新状态
<<< END U003985 >>>
<<< UNIT U003986 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2010-2010 | ctx=cli.tui.run.choice_cancel >>>
审阅次数：2
取消
<<< END U003986 >>>
<<< UNIT U003987 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2011-2011 | ctx=cli.tui.run.choice_cancelled >>>
审阅次数：2
已取消${label}
<<< END U003987 >>>
<<< UNIT U003988 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2012-2012 | ctx=cli.tui.run.choice_hint_restart >>>
审阅次数：2
将重启实例
<<< END U003988 >>>
<<< UNIT U003989 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2013-2013 | ctx=cli.tui.run.choice_hint_start >>>
审阅次数：2
将启动实例
<<< END U003989 >>>
<<< UNIT U003990 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2014-2014 | ctx=cli.tui.run.choice_hint_start_adapter >>>
审阅次数：2
将只启动适配器 ${platform}
<<< END U003990 >>>
<<< UNIT U003991 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2015-2015 | ctx=cli.tui.run.choice_hint_stop >>>
审阅次数：2
将停止实例
<<< END U003991 >>>
<<< UNIT U003992 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2016-2016 | ctx=cli.tui.run.choice_run >>>
审阅次数：2
执行
<<< END U003992 >>>
<<< UNIT U003993 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2017-2017 | ctx=cli.tui.run.choice_title >>>
审阅次数：2
确认${label}
<<< END U003993 >>>
<<< UNIT U003994 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2018-2018 | ctx=cli.tui.run.col_detail >>>
审阅次数：2
备注
<<< END U003994 >>>
<<< UNIT U003995 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2019-2019 | ctx=cli.tui.run.col_exit_code >>>
审阅次数：2
退出码
<<< END U003995 >>>
<<< UNIT U003996 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2020-2020 | ctx=cli.tui.run.col_label >>>
审阅次数：2
目标
<<< END U003996 >>>
<<< UNIT U003997 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2022-2022 | ctx=cli.tui.run.col_started >>>
审阅次数：2
启动时间
<<< END U003997 >>>
<<< UNIT U003998 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2023-2023 | ctx=cli.tui.run.col_state >>>
审阅次数：2
状态
<<< END U003998 >>>
<<< UNIT U003999 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2024-2024 | ctx=cli.tui.run.detail_cli_record >>>
审阅次数：2
由 CLI 记录（控制台输出见 ${log}）
<<< END U003999 >>>
<<< UNIT U004000 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2025-2025 | ctx=cli.tui.run.detail_detached >>>
审阅次数：2
已在后台启动，输出见 ${log}
<<< END U004000 >>>
<<< UNIT U004001 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2026-2026 | ctx=cli.tui.run.detail_never_started >>>
审阅次数：2
尚未在本界面启动
<<< END U004001 >>>
<<< UNIT U004002 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2027-2027 | ctx=cli.tui.run.detail_not_started >>>
审阅次数：2
尚未启动
<<< END U004002 >>>
<<< UNIT U004003 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2028-2028 | ctx=cli.tui.run.detail_pid_exit >>>
审阅次数：2
PID ${pid}，退出码 ${code}
<<< END U004003 >>>
<<< UNIT U004004 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2029-2029 | ctx=cli.tui.run.error_cli_failed >>>
审阅次数：2
调用 CLI 失败（${command}）：${error}
<<< END U004004 >>>
<<< UNIT U004005 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2030-2030 | ctx=cli.tui.run.error_cli_output >>>
审阅次数：2
${command} 未返回有效 JSON（退出码 ${code}）：${tail}
<<< END U004005 >>>
<<< UNIT U004006 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2031-2031 | ctx=cli.tui.run.error_cli_timeout >>>
审阅次数：2
调用 CLI 超时（${command}，${seconds} 秒）
<<< END U004006 >>>
<<< UNIT U004007 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2032-2032 | ctx=cli.tui.run.error_no_instance >>>
审阅次数：2
未找到实例：${origin} 及其父目录下没有 akaribot.toml
<<< END U004007 >>>
<<< UNIT U004008 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2034-2034 | ctx=cli.tui.run.foreground_hint >>>
审阅次数：2
请在其他终端运行 ${command}，该终端将持续显示实例日志。
<<< END U004008 >>>
<<< UNIT U004009 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2035-2035 | ctx=cli.tui.run.label_adapter_start >>>
审阅次数：2
启动适配器
<<< END U004009 >>>
<<< UNIT U004010 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2036-2036 | ctx=cli.tui.run.label_foreground >>>
审阅次数：2
前台运行
<<< END U004010 >>>
<<< UNIT U004011 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2037-2037 | ctx=cli.tui.run.label_more >>>
审阅次数：2
更多…
<<< END U004011 >>>
<<< UNIT U004012 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2038-2038 | ctx=cli.tui.run.label_refresh >>>
审阅次数：2
刷新
<<< END U004012 >>>
<<< UNIT U004013 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2039-2039 | ctx=cli.tui.run.label_restart >>>
审阅次数：2
重启实例
<<< END U004013 >>>
<<< UNIT U004014 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2040-2040 | ctx=cli.tui.run.label_start >>>
审阅次数：2
启动实例
<<< END U004014 >>>
<<< UNIT U004015 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2041-2041 | ctx=cli.tui.run.label_stop >>>
审阅次数：2
停止实例
<<< END U004015 >>>
<<< UNIT U004016 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2042-2042 | ctx=cli.tui.run.more_hint >>>
审阅次数：2
启动指定适配器会先询问平台名并确认。前台运行会占用终端，界面只给出要执行的命令。
<<< END U004016 >>>
<<< UNIT U004017 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2043-2043 | ctx=cli.tui.run.more_title >>>
审阅次数：2
更多运行操作
<<< END U004017 >>>
<<< UNIT U004018 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2044-2044 | ctx=cli.tui.run.msg_not_running >>>
审阅次数：2
实例未运行
<<< END U004018 >>>
<<< UNIT U004019 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2045-2045 | ctx=cli.tui.run.msg_restart_aborted >>>
审阅次数：2
重启中止：${message}
<<< END U004019 >>>
<<< UNIT U004020 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2046-2046 | ctx=cli.tui.run.msg_restart_failed >>>
审阅次数：2
重启失败：${message}
<<< END U004020 >>>
<<< UNIT U004021 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2047-2047 | ctx=cli.tui.run.msg_restarted >>>
审阅次数：2
已重启 PID ${pid}
<<< END U004021 >>>
<<< UNIT U004022 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2048-2048 | ctx=cli.tui.run.msg_restarted_with >>>
审阅次数：2
已重启，${message}
<<< END U004022 >>>
<<< UNIT U004023 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2049-2049 | ctx=cli.tui.run.msg_start_failed >>>
审阅次数：2
启动失败
<<< END U004023 >>>
<<< UNIT U004024 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2050-2050 | ctx=cli.tui.run.msg_started >>>
审阅次数：2
已启动 PID ${pid}
<<< END U004024 >>>
<<< UNIT U004025 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2051-2051 | ctx=cli.tui.run.msg_stop_failed >>>
审阅次数：2
停止失败
<<< END U004025 >>>
<<< UNIT U004026 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2052-2052 | ctx=cli.tui.run.msg_stopped >>>
审阅次数：2
已停止
<<< END U004026 >>>
<<< UNIT U004027 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2053-2053 | ctx=cli.tui.run.notify_busy >>>
审阅次数：2
启动或停止操作执行中
<<< END U004027 >>>
<<< UNIT U004028 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2054-2054 | ctx=cli.tui.run.notify_start_running >>>
审阅次数：2
实例运行中，请先停止
<<< END U004028 >>>
<<< UNIT U004029 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2055-2055 | ctx=cli.tui.run.origin_cli >>>
审阅次数：2
CLI 记录
<<< END U004029 >>>
<<< UNIT U004030 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2056-2056 | ctx=cli.tui.run.origin_stub >>>
审阅次数：2
模拟数据
<<< END U004030 >>>
<<< UNIT U004031 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2057-2057 | ctx=cli.tui.run.state_exited >>>
审阅次数：2
已退出
<<< END U004031 >>>
<<< UNIT U004032 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2058-2058 | ctx=cli.tui.run.state_running >>>
审阅次数：2
运行中
<<< END U004032 >>>
<<< UNIT U004033 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2059-2059 | ctx=cli.tui.run.state_stopped >>>
审阅次数：2
已停止
<<< END U004033 >>>
<<< UNIT U004034 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2060-2060 | ctx=cli.tui.run.state_unknown >>>
审阅次数：2
状态未知
<<< END U004034 >>>
<<< UNIT U004035 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2061-2061 | ctx=cli.tui.run.status_calling >>>
审阅次数：2
正在${label}…
<<< END U004035 >>>
<<< UNIT U004036 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2062-2062 | ctx=cli.tui.run.status_read_failed >>>
审阅次数：2
读取状态失败：${error}
<<< END U004036 >>>
<<< UNIT U004037 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2063-2063 | ctx=cli.tui.run.summary_empty >>>
审阅次数：2
状态表为空
<<< END U004037 >>>
<<< UNIT U004038 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2065-2065 | ctx=cli.tui.run.summary_manual >>>
审阅次数：2
手动刷新状态
<<< END U004038 >>>
<<< UNIT U004039 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2066-2066 | ctx=cli.tui.run.summary_poll >>>
审阅次数：2
每 ${seconds} 秒刷新状态
<<< END U004039 >>>
<<< UNIT U004040 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2067-2067 | ctx=cli.tui.run.table_empty >>>
审阅次数：2
状态表为空，按 r 刷新
<<< END U004040 >>>
<<< UNIT U004041 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2068-2068 | ctx=cli.tui.run.table_loading >>>
审阅次数：2
正在读取进程状态
<<< END U004041 >>>
<<< UNIT U004042 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2070-2070 | ctx=cli.tui.selfcheck.available >>>
审阅次数：2
可用
<<< END U004042 >>>
<<< UNIT U004043 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2072-2072 | ctx=cli.tui.selfcheck.cap_frozen >>>
审阅次数：2
冻结产物
<<< END U004043 >>>
<<< UNIT U004044 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2073-2073 | ctx=cli.tui.selfcheck.cap_interactive >>>
审阅次数：2
交互终端
<<< END U004044 >>>
<<< UNIT U004045 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2074-2074 | ctx=cli.tui.selfcheck.cap_os >>>
审阅次数：2
操作系统
<<< END U004045 >>>
<<< UNIT U004046 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2079-2079 | ctx=cli.tui.selfcheck.frozen_flag >>>
审阅次数：2
Nuitka 编译标志存在
<<< END U004046 >>>
<<< UNIT U004047 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2080-2080 | ctx=cli.tui.selfcheck.not_in_tmux >>>
审阅次数：2
未使用 tmux
<<< END U004047 >>>
<<< UNIT U004048 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2081-2081 | ctx=cli.tui.selfcheck.not_set >>>
审阅次数：2
未设置
<<< END U004048 >>>
<<< UNIT U004049 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2082-2082 | ctx=cli.tui.selfcheck.not_ssh >>>
审阅次数：2
未使用 SSH
<<< END U004049 >>>
<<< UNIT U004050 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2083-2083 | ctx=cli.tui.selfcheck.source_run >>>
审阅次数：2
源码运行
<<< END U004050 >>>
<<< UNIT U004051 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2084-2084 | ctx=cli.tui.selfcheck.term_program_unset >>>
审阅次数：2
未设置，无法识别 Terminal.app 或 iTerm2
<<< END U004051 >>>
<<< UNIT U004052 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2085-2085 | ctx=cli.tui.selfcheck.term_unset >>>
审阅次数：2
TERM 未设置
<<< END U004052 >>>
<<< UNIT U004053 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2086-2086 | ctx=cli.tui.selfcheck.textual_version >>>
审阅次数：2
Textual 版本：要求 ${pin}，实际 ${found}
<<< END U004053 >>>
<<< UNIT U004054 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2087-2087 | ctx=cli.tui.selfcheck.unavailable >>>
审阅次数：2
不可用
<<< END U004054 >>>
<<< UNIT U004055 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2088-2088 | ctx=cli.tui_cmd.check_adapter_install >>>
审阅次数：2
适配器列表与安装
<<< END U004055 >>>
<<< UNIT U004056 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2089-2089 | ctx=cli.tui_cmd.check_adapter_install_bad >>>
审阅次数：2
平台 ${platforms}，按钮 ${label}，安装结果 ${installed}
<<< END U004056 >>>
<<< UNIT U004057 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2090-2090 | ctx=cli.tui_cmd.check_adapter_install_detail >>>
审阅次数：2
列出 ${count} 个平台，安装 ${installed} 个未安装平台
<<< END U004057 >>>
<<< UNIT U004058 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2091-2091 | ctx=cli.tui_cmd.check_available >>>
审阅次数：2
可安装列表与安装进度
<<< END U004058 >>>
<<< UNIT U004059 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2092-2092 | ctx=cli.tui_cmd.check_available_bad >>>
审阅次数：2
列表筛选失败：${before} → ${after} 行，收到 ${lines} 行输出
<<< END U004059 >>>
<<< UNIT U004060 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2093-2093 | ctx=cli.tui_cmd.check_available_detail >>>
审阅次数：2
默认显示 ${before} 行（含未安装项），仅显示已安装项时为 ${after} 行，安装输出 ${lines} 行，末行为“${last}”
<<< END U004060 >>>
<<< UNIT U004061 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2094-2094 | ctx=cli.tui_cmd.check_boot >>>
审阅次数：2
界面启动（80×24）
<<< END U004061 >>>
<<< UNIT U004062 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2095-2095 | ctx=cli.tui_cmd.check_boot_detail >>>
审阅次数：2
列表 ${rows} 行，详情首行 ${detail}，页面尺寸 ${width}×${height}，启动 ${startup} ms、首帧 ${first_paint} ms
<<< END U004062 >>>
<<< UNIT U004063 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2096-2096 | ctx=cli.tui_cmd.check_cjk_width >>>
审阅次数：2
中文宽度计算
<<< END U004063 >>>
<<< UNIT U004064 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2097-2097 | ctx=cli.tui_cmd.check_cjk_width_detail >>>
审阅次数：2
display_width(${sample})=${computed}（期望为 8，len=${length}）。截断至 7 列后的文本为 ${truncated}，宽度为 ${width}
<<< END U004064 >>>
<<< UNIT U004065 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2098-2098 | ctx=cli.tui_cmd.check_multi_select >>>
审阅次数：2
多选与批量操作
<<< END U004065 >>>
<<< UNIT U004066 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2099-2099 | ctx=cli.tui_cmd.check_multi_select_bad >>>
审阅次数：2
已选择 ${selected} 项（共 ${total} 行），批量安装结果为 ${installed}
<<< END U004066 >>>
<<< UNIT U004067 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2100-2100 | ctx=cli.tui_cmd.check_multi_select_detail >>>
审阅次数：2
${total} 行中选择 3 项，批量安装其中 ${installed} 个未安装项
<<< END U004067 >>>
<<< UNIT U004068 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2101-2101 | ctx=cli.tui_cmd.check_navigation >>>
审阅次数：2
页面切换、高亮与焦点
<<< END U004068 >>>
<<< UNIT U004069 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2102-2102 | ctx=cli.tui_cmd.check_navigation_bad >>>
审阅次数：2
页面切换异常：显示或高亮不一致 ${mismatched}，焦点缺失 ${unfocused}
<<< END U004069 >>>
<<< UNIT U004070 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2103-2103 | ctx=cli.tui_cmd.check_navigation_detail >>>
审阅次数：2
${count} 页切换正常，页面显示、侧栏高亮与焦点检查通过
<<< END U004070 >>>
<<< UNIT U004071 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2104-2104 | ctx=cli.tui_cmd.check_resources >>>
审阅次数：2
包内资源枚举
<<< END U004071 >>>
<<< UNIT U004072 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2106-2106 | ctx=cli.tui_cmd.check_resources_missing >>>
审阅次数：2
${package} 无可读资源。冻结产物需通过 --include-package-data 包含数据文件
<<< END U004072 >>>
<<< UNIT U004073 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2107-2107 | ctx=cli.tui_cmd.check_stylesheet_absent >>>
审阅次数：2
未找到资源文件，使用内联样式表（见 tui/README.md）
<<< END U004073 >>>
<<< UNIT U004074 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2108-2108 | ctx=cli.tui_cmd.check_stylesheet_parse >>>
审阅次数：2
样式表解析
<<< END U004074 >>>
<<< UNIT U004075 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2109-2109 | ctx=cli.tui_cmd.check_stylesheet_parse_ok >>>
审阅次数：2
Textual 解析通过
<<< END U004075 >>>
<<< UNIT U004076 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2110-2110 | ctx=cli.tui_cmd.check_stylesheet_read >>>
审阅次数：2
读取 ${count} 个字符
<<< END U004076 >>>
<<< UNIT U004077 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2111-2111 | ctx=cli.tui_cmd.check_stylesheet_resource >>>
审阅次数：2
样式表资源 app.tcss
<<< END U004077 >>>
<<< UNIT U004078 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2112-2112 | ctx=cli.tui_cmd.check_stylesheet_source >>>
审阅次数：2
样式表来源
<<< END U004078 >>>
<<< UNIT U004079 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2113-2113 | ctx=cli.tui_cmd.check_stylesheet_source_detail >>>
审阅次数：2
${origin}，${lines} 行，${size} 字节，sha256 ${sha256}
<<< END U004079 >>>
<<< UNIT U004080 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2114-2114 | ctx=cli.tui_cmd.check_textual_version >>>
审阅次数：2
Textual 版本
<<< END U004080 >>>
<<< UNIT U004081 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2115-2115 | ctx=cli.tui_cmd.check_textual_version_detail >>>
审阅次数：2
${message}，要求版本 ${pin}
<<< END U004081 >>>
<<< UNIT U004082 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2116-2116 | ctx=cli.tui_cmd.check_theme >>>
审阅次数：2
品牌主题
<<< END U004082 >>>
<<< UNIT U004083 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2117-2117 | ctx=cli.tui_cmd.check_theme_bad >>>
审阅次数：2
主题未生效：name=${name} primary=${primary}
<<< END U004083 >>>
<<< UNIT U004084 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2118-2118 | ctx=cli.tui_cmd.check_theme_detail >>>
审阅次数：2
主题 ${name}，primary=${primary}，与 character_marked.png 的调色板一致
<<< END U004084 >>>
<<< UNIT U004085 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2119-2119 | ctx=cli.tui_cmd.discover_ambiguous >>>
审阅次数：2
当前目录不是实例，子目录中发现 ${count} 个实例：${found}。按 n 添加需要管理的实例
<<< END U004085 >>>
<<< UNIT U004086 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2120-2120 | ctx=cli.tui_cmd.discover_done >>>
审阅次数：2
在 ${parent} 下发现实例 ${name}（${root}），已添加并设为当前实例
<<< END U004086 >>>
<<< UNIT U004087 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2121-2121 | ctx=cli.tui_cmd.headless_failed >>>
审阅次数：2
无终端检查失败：${error}
<<< END U004087 >>>
<<< UNIT U004088 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2122-2122 | ctx=cli.tui_cmd.headless_first_focus_bad >>>
审阅次数：2
概览页首屏缺少焦点
<<< END U004088 >>>
<<< UNIT U004089 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2123-2123 | ctx=cli.tui_cmd.headless_first_ok >>>
审阅次数：2
无终端检查（概览页）：80×24 下默认首屏为 ${page}，关键控件 ${widgets} 已挂载，焦点正常
<<< END U004089 >>>
<<< UNIT U004090 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2124-2124 | ctx=cli.tui_cmd.headless_first_widgets_bad >>>
审阅次数：2
概览页缺少关键控件：${missing}
<<< END U004090 >>>
<<< UNIT U004091 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2125-2125 | ctx=cli.tui_cmd.headless_modules_empty >>>
审阅次数：2
无终端检查（模块页）：数据源 list 调用 ${calls} 次，当前实例无模块记录
<<< END U004091 >>>
<<< UNIT U004092 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2126-2126 | ctx=cli.tui_cmd.headless_modules_ok >>>
审阅次数：2
无终端检查（模块页）：80×24 下显示 ${rows} 行模块记录，数据源 list 调用 ${calls} 次
<<< END U004092 >>>
<<< UNIT U004093 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2127-2127 | ctx=cli.tui_cmd.headless_modules_uncalled >>>
审阅次数：2
无终端检查（模块页）：未读取数据，数据源 list 调用 ${calls} 次（-1 表示未提供计数）
<<< END U004093 >>>
<<< UNIT U004094 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2128-2128 | ctx=cli.tui_cmd.headless_page_bad >>>
审阅次数：2
无终端检查：当前页面为 ${page}，期望为 ${expected}
<<< END U004094 >>>
<<< UNIT U004095 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2129-2129 | ctx=cli.tui_cmd.headless_summary >>>
审阅次数：2
样式表 ${origin}，${lines} 行，sha256 ${sha256}，启动 ${startup} ms，首帧 ${first_paint} ms，总耗时 ${ms} ms
<<< END U004095 >>>
<<< UNIT U004096 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2130-2130 | ctx=cli.tui_cmd.help >>>
审阅次数：2
交互界面
<<< END U004096 >>>
<<< UNIT U004097 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2131-2131 | ctx=cli.tui_cmd.not_terminal >>>
审阅次数：2
当前标准输入或输出不是终端，无法启动交互界面。请在终端中运行，或使用 `akaribot tui --self-check` / `akaribot tui --headless`。
<<< END U004097 >>>
<<< UNIT U004098 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2132-2132 | ctx=cli.tui_cmd.option_headless >>>
审阅次数：2
无终端检查，启动界面并完成基础读取后退出
<<< END U004098 >>>
<<< UNIT U004099 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2133-2133 | ctx=cli.tui_cmd.option_no_mouse >>>
审阅次数：2
关闭鼠标追踪，适用于不支持鼠标的终端或 tmux
<<< END U004099 >>>
<<< UNIT U004100 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2134-2134 | ctx=cli.tui_cmd.option_self_check >>>
审阅次数：2
无终端诊断，检查资源、样式表和界面交互后退出
<<< END U004100 >>>
<<< UNIT U004101 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2135-2135 | ctx=cli.tui_cmd.register_auto_failed >>>
审阅次数：2
自动添加实例失败：${error}
<<< END U004101 >>>
<<< UNIT U004102 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2137-2137 | ctx=cli.tui_cmd.self_check_blocked >>>
审阅次数：2
诊断未通过：${failures} 项失败，${skipped} 项未执行，${warnings} 项警告
<<< END U004102 >>>
<<< UNIT U004103 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2138-2138 | ctx=cli.tui_cmd.self_check_failed >>>
审阅次数：2
诊断失败：${failures} 项失败，${warnings} 项警告
<<< END U004103 >>>
<<< UNIT U004104 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2139-2139 | ctx=cli.tui_cmd.self_check_ok >>>
审阅次数：2
诊断通过：${passed} 项通过，${warnings} 项警告
<<< END U004104 >>>
<<< UNIT U004105 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2140-2140 | ctx=cli.venv.add.arg_spec >>>
审阅次数：2
要安装的依赖声明，可填写 PyPI 包名（可带版本区间）、仓库地址或 git+ 直接引用。
<<< END U004105 >>>
<<< UNIT U004106 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2141-2141 | ctx=cli.venv.add.dry_run >>>
审阅次数：2
试运行，只打印将执行的命令，不改动环境也不修改清单。
<<< END U004106 >>>
<<< UNIT U004107 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2142-2142 | ctx=cli.venv.add.empty_spec >>>
审阅次数：2
依赖声明不能为空。
<<< END U004107 >>>
<<< UNIT U004108 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2143-2143 | ctx=cli.venv.add.help >>>
审阅次数：2
安装运行库到实例环境。--save 会记入实例清单，环境重建时按此补充安装。
<<< END U004108 >>>
<<< UNIT U004109 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2144-2144 | ctx=cli.venv.add.not_saved >>>
审阅次数：2
已安装到当前环境但未记入实例清单，环境重建后不会保留。
<<< END U004109 >>>
<<< UNIT U004110 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2145-2145 | ctx=cli.venv.add.option_save >>>
审阅次数：2
将这次安装记入实例清单（akaribot.toml 的 runtime.requirements）。
<<< END U004110 >>>
<<< UNIT U004111 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2146-2146 | ctx=cli.venv.add.option_upgrade >>>
审阅次数：2
允许升级已安装版本。
<<< END U004111 >>>
<<< UNIT U004112 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2147-2147 | ctx=cli.venv.add.saved >>>
审阅次数：2
已记入实例清单：${spec}
<<< END U004112 >>>
<<< UNIT U004113 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2148-2148 | ctx=cli.venv.add.unnamed_git >>>
审阅次数：2
已安装到环境，但无法识别这个 git 直接引用的包名，未记入清单：${spec}
<<< END U004113 >>>
<<< UNIT U004114 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2149-2149 | ctx=cli.venv.adopt.confirm >>>
审阅次数：2
将把当前环境的 akaribot 包迁移至 ${venv}，随后从源环境卸载。继续
<<< END U004114 >>>
<<< UNIT U004115 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2150-2150 | ctx=cli.venv.adopt.help >>>
审阅次数：2
切换为 CLI 托管 venv，先安装并验证通过，最后才卸载源环境的包。
<<< END U004115 >>>
<<< UNIT U004116 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2151-2151 | ctx=cli.venv.adopt.option_force >>>
审阅次数：2
目标 venv 已存在且非空时覆盖重建
<<< END U004116 >>>
<<< UNIT U004117 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2152-2152 | ctx=cli.venv.adopt.option_keep_source >>>
审阅次数：2
不卸载源环境的包，只保留迁移副本
<<< END U004117 >>>
<<< UNIT U004118 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2153-2153 | ctx=cli.venv.adopt.option_python >>>
审阅次数：2
创建 venv 用的解释器，默认与当前解释器一致
<<< END U004118 >>>
<<< UNIT U004119 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2154-2154 | ctx=cli.venv.help >>>
审阅次数：2
实例 venv 托管（status / adopt / release / recreate）
<<< END U004119 >>>
<<< UNIT U004120 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2155-2155 | ctx=cli.venv.none >>>
审阅次数：2
无
<<< END U004120 >>>
<<< UNIT U004121 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2156-2156 | ctx=cli.venv.option_dry_run >>>
审阅次数：2
只打印将执行的命令，不修改任何文件
<<< END U004121 >>>
<<< UNIT U004122 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2157-2157 | ctx=cli.venv.option_verbose >>>
审阅次数：2
回显 uv 的全部输出
<<< END U004122 >>>
<<< UNIT U004123 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2158-2158 | ctx=cli.venv.recreate.confirm >>>
审阅次数：2
将重建实例 venv，旧的 venv 在新环境验证通过后删除。继续
<<< END U004123 >>>
<<< UNIT U004124 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2159-2159 | ctx=cli.venv.recreate.help >>>
审阅次数：2
重建实例 venv（Python 升级后修复）。新环境安装并验证通过后才替换旧目录。
<<< END U004124 >>>
<<< UNIT U004125 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2160-2160 | ctx=cli.venv.recreate.option_force >>>
审阅次数：2
暂存目录已存在时覆盖
<<< END U004125 >>>
<<< UNIT U004126 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2161-2161 | ctx=cli.venv.recreate.option_python >>>
审阅次数：2
新 venv 用的解释器，默认为当前解释器
<<< END U004126 >>>
<<< UNIT U004127 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2162-2162 | ctx=cli.venv.release.confirm >>>
审阅次数：2
将把实例 venv 的包安装到当前环境，随后从实例 venv 卸载。继续
<<< END U004127 >>>
<<< UNIT U004128 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2163-2163 | ctx=cli.venv.release.help >>>
审阅次数：2
放弃托管，将实例 venv 的包迁移回当前环境。
<<< END U004128 >>>
<<< UNIT U004129 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2164-2164 | ctx=cli.venv.release.option_keep_source >>>
审阅次数：2
保留实例 venv 里的包，只保留迁移副本
<<< END U004129 >>>
<<< UNIT U004130 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2165-2165 | ctx=cli.venv.remove.absent >>>
审阅次数：2
环境里没有 ${dist}，实例清单里也没有它的记录。
<<< END U004130 >>>
<<< UNIT U004131 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2166-2166 | ctx=cli.venv.remove.arg_dist >>>
审阅次数：2
要卸载的包名。
<<< END U004131 >>>
<<< UNIT U004132 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2167-2167 | ctx=cli.venv.remove.help >>>
审阅次数：2
从实例环境卸载运行库。--save 同时删除清单里的记录。
<<< END U004132 >>>
<<< UNIT U004133 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2168-2168 | ctx=cli.venv.remove.kept_record >>>
审阅次数：2
环境里已卸载，实例清单仍保留记录：${spec}
<<< END U004133 >>>
<<< UNIT U004134 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2169-2169 | ctx=cli.venv.remove.not_installed >>>
审阅次数：2
环境里没有 ${dist}，只处理清单里的记录。
<<< END U004134 >>>
<<< UNIT U004135 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2170-2170 | ctx=cli.venv.remove.option_save >>>
审阅次数：2
同时删除实例清单里的记录。
<<< END U004135 >>>
<<< UNIT U004136 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2171-2171 | ctx=cli.venv.remove.record_dropped >>>
审阅次数：2
已从实例清单移除：${spec}
<<< END U004136 >>>
<<< UNIT U004137 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2172-2172 | ctx=cli.venv.report.action >>>
审阅次数：2
动作
<<< END U004137 >>>
<<< UNIT U004138 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2173-2173 | ctx=cli.venv.report.moved >>>
审阅次数：2
迁移的包
<<< END U004138 >>>
<<< UNIT U004139 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2174-2174 | ctx=cli.venv.report.removed >>>
审阅次数：2
源环境已卸载
<<< END U004139 >>>
<<< UNIT U004140 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2175-2175 | ctx=cli.venv.report.source >>>
审阅次数：2
源环境
<<< END U004140 >>>
<<< UNIT U004141 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2176-2176 | ctx=cli.venv.report.target >>>
审阅次数：2
目标环境
<<< END U004141 >>>
<<< UNIT U004142 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2177-2177 | ctx=cli.venv.status.adopt_hint >>>
审阅次数：2
运行 `akaribot venv adopt` 可切换为 CLI 托管。
<<< END U004142 >>>
<<< UNIT U004143 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2178-2178 | ctx=cli.venv.status.core_version >>>
审阅次数：2
core 版本
<<< END U004143 >>>
<<< UNIT U004144 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2179-2179 | ctx=cli.venv.status.help >>>
审阅次数：2
显示当前模式、解释器路径与已安装 akaribot 包数量。
<<< END U004144 >>>
<<< UNIT U004145 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2180-2180 | ctx=cli.venv.status.installed >>>
审阅次数：2
环境里的包
<<< END U004145 >>>
<<< UNIT U004146 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2181-2181 | ctx=cli.venv.status.missing >>>
审阅次数：2
[red]解释器不存在[/red]
<<< END U004146 >>>
<<< UNIT U004147 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2182-2182 | ctx=cli.venv.status.mode >>>
审阅次数：2
模式
<<< END U004147 >>>
<<< UNIT U004148 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2183-2183 | ctx=cli.venv.status.mode_external >>>
审阅次数：2
非托管（使用当前环境）
<<< END U004148 >>>
<<< UNIT U004149 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2184-2184 | ctx=cli.venv.status.mode_managed >>>
审阅次数：2
托管（runtime.venv = ${venv}）
<<< END U004149 >>>
<<< UNIT U004150 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2185-2185 | ctx=cli.venv.status.not_installed >>>
审阅次数：2
[yellow]未安装[/yellow]
<<< END U004150 >>>
<<< UNIT U004151 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2186-2186 | ctx=cli.venv.status.packages >>>
审阅次数：2
已安装 akaribot 包
<<< END U004151 >>>
<<< UNIT U004152 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2187-2187 | ctx=cli.venv.status.probe_failed >>>
审阅次数：2
[red]探测失败：${error}[/red]
<<< END U004152 >>>
<<< UNIT U004153 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2188-2188 | ctx=cli.venv.status.python >>>
审阅次数：2
解释器
<<< END U004153 >>>
<<< UNIT U004154 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2189-2189 | ctx=cli.venv.status.recreate_hint >>>
审阅次数：2
运行 `akaribot venv recreate` 重建实例 venv。
<<< END U004154 >>>
<<< UNIT U004155 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2190-2190 | ctx=cli.venv.status.requirements >>>
审阅次数：2
清单记录的运行库
<<< END U004155 >>>
<<< UNIT U004156 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2191-2191 | ctx=cli.venv.status.root >>>
审阅次数：2
实例根目录
<<< END U004156 >>>
<<< UNIT U004157 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2192-2192 | ctx=cli.venv.status.state >>>
审阅次数：2
状态
<<< END U004157 >>>
<<< UNIT U004158 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2193-2193 | ctx=cli.venv.status.title >>>
审阅次数：2
实例 venv 状态
<<< END U004158 >>>
<<< UNIT U004159 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2194-2194 | ctx=cli.venv.status.venv_dir >>>
审阅次数：2
venv 目录
<<< END U004159 >>>
<<< UNIT U004160 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2195-2195 | ctx=cli.venv_engine.adopt_dry_run >>>
审阅次数：2
dry-run：跳过验证与源环境卸载，计划卸载 ${names}
<<< END U004160 >>>
<<< UNIT U004161 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2196-2196 | ctx=cli.venv_engine.adopt_keep_source >>>
审阅次数：2
--keep-source：保留源环境的包
<<< END U004161 >>>
<<< UNIT U004162 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2197-2197 | ctx=cli.venv_engine.candidate_hint >>>
审阅次数：2
可安装的名称：${names}
<<< END U004162 >>>
<<< UNIT U004163 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2198-2198 | ctx=cli.venv_engine.conflict_candidate_needs >>>
审阅次数：2
${dist} 要求 ${requirement}${specifier}，但已安装 ${version}
<<< END U004163 >>>
<<< UNIT U004164 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2199-2199 | ctx=cli.venv_engine.conflict_change_breaks >>>
审阅次数：2
已安装的 ${installed} 要求 ${requirement}${specifier}，安装后将变为 ${version}
<<< END U004164 >>>
<<< UNIT U004165 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2200-2200 | ctx=cli.venv_engine.conflict_installed_needs_conflict >>>
审阅次数：2
已安装的 ${installed} 要求 ${requirement}${specifier}，与待安装包冲突
<<< END U004165 >>>
<<< UNIT U004166 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2201-2201 | ctx=cli.venv_engine.conflict_installed_needs_pending >>>
审阅次数：2
已安装的 ${installed} 要求 ${requirement}${specifier}，但待安装版本 ${version} 不满足
<<< END U004166 >>>
<<< UNIT U004167 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2202-2202 | ctx=cli.venv_engine.dependency_resolve_failed >>>
审阅次数：2
依赖解析失败：${detail}（完整输出见 --verbose）
<<< END U004167 >>>
<<< UNIT U004168 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2203-2203 | ctx=cli.venv_engine.detail_dry_run >>>
审阅次数：2
dry-run 未做任何修改
<<< END U004168 >>>
<<< UNIT U004169 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2204-2204 | ctx=cli.venv_engine.detail_old_venv_removed >>>
审阅次数：2
旧 venv 已删除
<<< END U004169 >>>
<<< UNIT U004170 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2205-2205 | ctx=cli.venv_engine.detail_venv_cleared >>>
审阅次数：2
已清空 runtime.venv
<<< END U004170 >>>
<<< UNIT U004171 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2206-2206 | ctx=cli.venv_engine.detail_venv_written >>>
审阅次数：2
已写入 runtime.venv=${venv}
<<< END U004171 >>>
<<< UNIT U004172 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2207-2207 | ctx=cli.venv_engine.entry_point_mismatch >>>
审阅次数：2
entry point ${name} 指向不一致：源 ${source} / 目标 ${target}
<<< END U004172 >>>
<<< UNIT U004173 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2208-2208 | ctx=cli.venv_engine.entry_point_missing >>>
审阅次数：2
目标环境缺少 entry point ${name}（源为 ${value}）
<<< END U004173 >>>
<<< UNIT U004174 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2209-2209 | ctx=cli.venv_engine.entry_points_consistent >>>
审阅次数：2
entry points 一致（${count} 个包）
<<< END U004174 >>>
<<< UNIT U004175 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2210-2210 | ctx=cli.venv_engine.entry_points_mismatch_new >>>
审阅次数：2
新 venv 的 entry points 与旧环境不一致，旧 venv 未动。可删除 ${staging} 后重试。
<<< END U004175 >>>
<<< UNIT U004176 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2211-2211 | ctx=cli.venv_engine.entry_points_mismatch_source >>>
审阅次数：2
目标环境的 entry points 与源环境不一致，已保留源环境不动。请检查 uv 安装输出，修好后重新运行 `akaribot venv adopt`。
<<< END U004176 >>>
<<< UNIT U004177 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2212-2212 | ctx=cli.venv_engine.entry_points_mismatch_venv >>>
审阅次数：2
当前环境的 entry points 与实例 venv 不一致，已保留实例 venv 不动。请检查 uv 安装输出。
<<< END U004177 >>>
<<< UNIT U004178 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2213-2213 | ctx=cli.venv_engine.exec_failed >>>
审阅次数：2
无法执行 ${command}：${error}
<<< END U004178 >>>
<<< UNIT U004179 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2214-2214 | ctx=cli.venv_engine.instance_venv_no_packages >>>
审阅次数：2
实例 venv ${venv_dir} 里没有 akaribot 包，无法 release。
<<< END U004179 >>>
<<< UNIT U004180 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2215-2215 | ctx=cli.venv_engine.instance_venv_python_missing >>>
审阅次数：2
实例 venv 的解释器不存在：${python}。可用 `akaribot venv recreate` 重建。
<<< END U004180 >>>
<<< UNIT U004181 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2216-2216 | ctx=cli.venv_engine.interpreter_missing >>>
审阅次数：2
解释器不存在：${python}
<<< END U004181 >>>
<<< UNIT U004182 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2217-2217 | ctx=cli.venv_engine.interpreter_missing_bare >>>
审阅次数：2
解释器不存在
<<< END U004182 >>>
<<< UNIT U004183 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2218-2218 | ctx=cli.venv_engine.keep_cli_in_source >>>
审阅次数：2
保留源环境的 ${dist}，避免卸载正在使用的 CLI。
<<< END U004183 >>>
<<< UNIT U004184 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2219-2219 | ctx=cli.venv_engine.keep_cli_in_venv >>>
审阅次数：2
CLI 正在实例 venv 内运行，保留其中的 ${dist}。
<<< END U004184 >>>
<<< UNIT U004185 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2220-2220 | ctx=cli.venv_engine.new_interpreter >>>
审阅次数：2
新环境解释器：${python}
<<< END U004185 >>>
<<< UNIT U004186 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2221-2221 | ctx=cli.venv_engine.no_pyproject >>>
审阅次数：2
${path} 里没有可识别的 pyproject.toml（缺少 [project].name）。
<<< END U004186 >>>
<<< UNIT U004187 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2222-2222 | ctx=cli.venv_engine.none >>>
审阅次数：2
无
<<< END U004187 >>>
<<< UNIT U004188 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2223-2223 | ctx=cli.venv_engine.offline_no_cache >>>
审阅次数：2
离线模式下没有可用的 registry 缓存（${path}）。
<<< END U004188 >>>
<<< UNIT U004189 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2224-2224 | ctx=cli.venv_engine.package_count >>>
审阅次数：2
共 ${count} 个包：${names}
<<< END U004189 >>>
<<< UNIT U004190 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2225-2225 | ctx=cli.venv_engine.package_name_required >>>
审阅次数：2
请给出包名，或用 `--dist <包名>` / `-e <本地目录>` 指定安装对象。
<<< END U004190 >>>
<<< UNIT U004191 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2226-2226 | ctx=cli.venv_engine.probe_failed >>>
审阅次数：2
探测 ${python} 的已安装包失败（退出码 ${code}）：${tail}
<<< END U004191 >>>
<<< UNIT U004192 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2227-2227 | ctx=cli.venv_engine.probe_timeout >>>
审阅次数：2
探测 ${python} 的已安装包超时
<<< END U004192 >>>
<<< UNIT U004193 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2228-2228 | ctx=cli.venv_engine.probe_unparsable >>>
审阅次数：2
探测结果无法解析：${error}
<<< END U004193 >>>
<<< UNIT U004194 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2229-2229 | ctx=cli.venv_engine.recreate_dry_run >>>
审阅次数：2
dry-run：跳过验证与目录替换
<<< END U004194 >>>
<<< UNIT U004195 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2230-2230 | ctx=cli.venv_engine.recreate_not_managed >>>
审阅次数：2
当前实例未托管 venv，请先运行 `akaribot venv adopt`。或用 `akaribot init --no-venv` 的实例改用 adopt。
<<< END U004195 >>>
<<< UNIT U004196 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2231-2231 | ctx=cli.venv_engine.recreate_python_missing >>>
审阅次数：2
实例 venv 的解释器不存在：${python}。请运行 `akaribot venv adopt --force` 重建。
<<< END U004196 >>>
<<< UNIT U004197 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2232-2232 | ctx=cli.venv_engine.registry_bad_json >>>
审阅次数：2
返回内容不是 JSON（${error}）
<<< END U004197 >>>
<<< UNIT U004198 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2233-2233 | ctx=cli.venv_engine.registry_cache_fallback >>>
审阅次数：2
registry 源不可用，改用本地缓存
<<< END U004198 >>>
<<< UNIT U004199 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2234-2234 | ctx=cli.venv_engine.registry_no_source >>>
审阅次数：2
未配置来源
<<< END U004199 >>>
<<< UNIT U004200 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2235-2235 | ctx=cli.venv_engine.registry_not_object >>>
审阅次数：2
${url}：registry.json 顶层不是对象
<<< END U004200 >>>
<<< UNIT U004201 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2236-2236 | ctx=cli.venv_engine.registry_package_missing >>>
审阅次数：2
registry 里没有名为 ${name} 的包。可用 `akaribot module available` 查看全部可安装包，或用 `--dist <包名>` 直接指定。
<<< END U004201 >>>
<<< UNIT U004202 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2238-2238 | ctx=cli.venv_engine.registry_unavailable >>>
审阅次数：2
无法获取 registry（${detail}）。可用 `--dist` 直接指定包名，或用 `--workspace-root` / `akaribot init --workspace-root` 改用工作区本地源码。
<<< END U004202 >>>
<<< UNIT U004203 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2239-2239 | ctx=cli.venv_engine.release_dry_run >>>
审阅次数：2
dry-run：跳过验证、卸载与元数据写入
<<< END U004203 >>>
<<< UNIT U004204 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2240-2240 | ctx=cli.venv_engine.release_keep_source >>>
审阅次数：2
--keep-source：保留实例 venv 的包
<<< END U004204 >>>
<<< UNIT U004205 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2241-2241 | ctx=cli.venv_engine.release_not_managed >>>
审阅次数：2
当前实例未托管 venv（runtime.venv 为空），无需 release。
<<< END U004205 >>>
<<< UNIT U004206 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2242-2242 | ctx=cli.venv_engine.requires_line >>>
审阅次数：2
${dist} 要求 ${requirement}${specifier}
<<< END U004206 >>>
<<< UNIT U004207 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2243-2243 | ctx=cli.venv_engine.same_interpreter >>>
审阅次数：2
源环境与目标环境是同一个解释器（${python}），无需执行该操作。
<<< END U004207 >>>
<<< UNIT U004208 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2244-2244 | ctx=cli.venv_engine.source_missing_core >>>
审阅次数：2
源环境 ${python} 里没有 akari-bot-core，无法迁移。请先在源环境安装 core。
<<< END U004208 >>>
<<< UNIT U004209 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2245-2245 | ctx=cli.venv_engine.staging_exists >>>
审阅次数：2
${staging} 已存在。确认可覆盖后加 --force，或手动删除该目录。
<<< END U004209 >>>
<<< UNIT U004210 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2246-2246 | ctx=cli.venv_engine.retired_exists >>>
审阅次数：2
备份环境已存在：${path}。请确认其内容并移走后重试。
<<< END U004210 >>>
<<< UNIT U004211 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2247-2247 | ctx=cli.venv_engine.restore_failed >>>
审阅次数：2
环境恢复失败：${error}。旧环境保留在 ${path}，请将其恢复到实例 venv 路径。
<<< END U004211 >>>
<<< UNIT U004212 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2248-2248 | ctx=cli.venv_engine.script_invalid >>>
审阅次数：2
重建后的入口脚本不可用：${path}。旧环境将恢复，临时环境保留供检查。
<<< END U004212 >>>
<<< UNIT U004213 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2249-2249 | ctx=cli.venv_engine.swap_failed >>>
审阅次数：2
环境替换或验证失败：${error}。旧环境保持可用，请检查临时环境后重试。
<<< END U004213 >>>
<<< UNIT U004214 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2250-2250 | ctx=cli.venv_engine.step_create_and_install >>>
审阅次数：2
创建实例 venv 并安装（${venv_dir}）
<<< END U004214 >>>
<<< UNIT U004215 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2251-2251 | ctx=cli.venv_engine.step_create_staging >>>
审阅次数：2
在 ${staging} 创建新环境并安装
<<< END U004215 >>>
<<< UNIT U004216 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2252-2252 | ctx=cli.venv_engine.step_enumerate_existing >>>
审阅次数：2
枚举现有 venv 的 akaribot 包
<<< END U004216 >>>
<<< UNIT U004217 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2253-2253 | ctx=cli.venv_engine.step_enumerate_source >>>
审阅次数：2
枚举源环境已安装的 akaribot 包（${python}）
<<< END U004217 >>>
<<< UNIT U004218 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2254-2254 | ctx=cli.venv_engine.step_enumerate_venv >>>
审阅次数：2
枚举实例 venv 已安装的 akaribot 包（${python}）
<<< END U004218 >>>
<<< UNIT U004219 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2255-2255 | ctx=cli.venv_engine.step_install_current >>>
审阅次数：2
在当前环境安装（${python}）
<<< END U004219 >>>
<<< UNIT U004220 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2256-2256 | ctx=cli.venv_engine.step_swap_and_cleanup >>>
审阅次数：2
替换并清理旧环境
<<< END U004220 >>>
<<< UNIT U004221 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2257-2257 | ctx=cli.venv_engine.step_uninstall_source >>>
审阅次数：2
卸载源环境的 akaribot 包
<<< END U004221 >>>
<<< UNIT U004222 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2258-2258 | ctx=cli.venv_engine.step_uninstall_venv_and_metadata >>>
审阅次数：2
卸载实例 venv 的包并更新元数据
<<< END U004222 >>>
<<< UNIT U004223 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2259-2259 | ctx=cli.venv_engine.step_update_metadata >>>
审阅次数：2
更新实例元数据
<<< END U004223 >>>
<<< UNIT U004224 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2260-2260 | ctx=cli.venv_engine.step_verify_new_venv >>>
审阅次数：2
验证 entry points 与新环境一致
<<< END U004224 >>>
<<< UNIT U004225 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2261-2261 | ctx=cli.venv_engine.step_verify_source >>>
审阅次数：2
验证 entry points 与源环境一致
<<< END U004225 >>>
<<< UNIT U004226 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2262-2262 | ctx=cli.venv_engine.step_verify_venv >>>
审阅次数：2
验证 entry points 与实例 venv 一致
<<< END U004226 >>>
<<< UNIT U004227 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2263-2263 | ctx=cli.venv_engine.switched_to_external >>>
审阅次数：2
已切换为非托管模式，venv 目录保留在 ${venv_dir}，可手动删除
<<< END U004227 >>>
<<< UNIT U004228 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2264-2264 | ctx=cli.venv_engine.switched_to_managed >>>
审阅次数：2
已切换为托管模式：${venv}
<<< END U004228 >>>
<<< UNIT U004229 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2265-2265 | ctx=cli.venv_engine.tables_purge_failed >>>
审阅次数：2
删除 ${dist} 的数据表失败：${reason}
<<< END U004229 >>>
<<< UNIT U004230 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2266-2266 | ctx=cli.venv_engine.tables_purged >>>
审阅次数：2
已删除 ${dist} 的数据表
<<< END U004230 >>>
<<< UNIT U004231 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2267-2267 | ctx=cli.venv_engine.target_venv_exists >>>
审阅次数：2
${venv_dir} 已存在且非空。确认可覆盖后加 --force 重建，或先运行 `akaribot venv recreate`。
<<< END U004231 >>>
<<< UNIT U004232 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2268-2268 | ctx=cli.venv_engine.uv_no_reason >>>
审阅次数：2
uv 未给出原因
<<< END U004232 >>>
<<< UNIT U004233 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2269-2269 | ctx=cli.venv_engine.uv_not_found >>>
审阅次数：2
未找到 uv。请先安装 uv（https://docs.astral.sh/uv/），或用环境变量 ${env}=/path/to/uv 指定其位置。
<<< END U004233 >>>
<<< UNIT U004234 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2270-2270 | ctx=cli.venv_engine.uv_override_unusable >>>
审阅次数：2
${env} 指向的 uv 不可用（${path}），改用其他来源。
<<< END U004234 >>>
<<< UNIT U004235 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2271-2271 | ctx=cli.venv_engine.venv_outside_instance >>>
审阅次数：2
实例 venv 必须位于实例目录内，当前为 ${venv_dir}。
<<< END U004235 >>>
<<< UNIT U004236 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2272-2272 | ctx=cli.venv_engine.venv_recreated >>>
审阅次数：2
已重建实例 venv：${venv_dir}
<<< END U004236 >>>
<<< UNIT U004237 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2273-2273 | ctx=cli.venv_engine.what_config_sync >>>
审阅次数：2
补充 ${dist} 的配置
<<< END U004237 >>>
<<< UNIT U004238 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2274-2274 | ctx=cli.venv_engine.what_create_new_venv >>>
审阅次数：2
创建新 venv
<<< END U004238 >>>
<<< UNIT U004239 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2275-2275 | ctx=cli.venv_engine.what_create_venv >>>
审阅次数：2
创建实例 venv
<<< END U004239 >>>
<<< UNIT U004240 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2276-2276 | ctx=cli.venv_engine.what_db_upgrade >>>
审阅次数：2
应用 ${dist} 的数据库迁移
<<< END U004240 >>>
<<< UNIT U004241 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2277-2277 | ctx=cli.venv_engine.what_install_dist >>>
审阅次数：2
安装 ${dist}
<<< END U004241 >>>
<<< UNIT U004242 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2278-2278 | ctx=cli.venv_engine.what_install_runtime >>>
审阅次数：2
按实例清单安装运行库
<<< END U004242 >>>
<<< UNIT U004243 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2279-2279 | ctx=cli.venv_engine.what_install_to_current >>>
审阅次数：2
安装 akaribot 包到当前环境
<<< END U004243 >>>
<<< UNIT U004244 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2280-2280 | ctx=cli.venv_engine.what_install_to_new_venv >>>
审阅次数：2
安装 akaribot 包到新 venv
<<< END U004244 >>>
<<< UNIT U004245 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2281-2281 | ctx=cli.venv_engine.what_install_to_venv >>>
审阅次数：2
安装 akaribot 包到实例 venv
<<< END U004245 >>>
<<< UNIT U004246 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2282-2282 | ctx=cli.venv_engine.what_purge_tables >>>
审阅次数：2
删除 ${dist} 的数据表失败
<<< END U004246 >>>
<<< UNIT U004247 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2283-2283 | ctx=cli.venv_engine.what_uninstall_dist >>>
审阅次数：2
卸载 ${dist}
<<< END U004247 >>>
<<< UNIT U004248 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2284-2284 | ctx=cli.venv_engine.what_uninstall_from_source >>>
审阅次数：2
从源环境卸载 akaribot 包
<<< END U004248 >>>
<<< UNIT U004249 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2285-2285 | ctx=cli.venv_engine.what_uninstall_from_venv >>>
审阅次数：2
从实例 venv 卸载 akaribot 包
<<< END U004249 >>>
<<< UNIT U004250 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2286-2286 | ctx=cli.venv_engine.what_uninstall_packages >>>
审阅次数：2
卸载
<<< END U004250 >>>
<<< UNIT U004251 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2287-2287 | ctx=cli.venv_engine.workspace_package_missing >>>
审阅次数：2
工作区 ${root} 里没有找到 ${name}。可用 `akaribot module available` 查看本地可安装包，或用 `--dist <包名>` 指定包名。
<<< END U004251 >>>
<<< UNIT U004252 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2288-2288 | ctx=cli.warn.instance_not_running_load >>>
审阅次数：2
实例未运行，无法热装载。下次启动会自动装载。要立即生效请先 `akaribot run`。
<<< END U004252 >>>
<<< UNIT U004253 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2289-2289 | ctx=cli.warn.instance_not_running_unload >>>
审阅次数：2
实例未运行，无法热卸载。下次启动仍会按 module_status 的现有记录装载。要让它保持卸载，请先 `akaribot run` 再执行本命令。
<<< END U004253 >>>
<<< UNIT U004254 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2290-2290 | ctx=cli.module.update.option_defer_runtime >>>
审阅次数：2
安装与同步配置后，由下次启动执行数据库迁移并载入新代码
<<< END U004254 >>>
<<< UNIT U004255 | py-comment | packages/akari-bot-cli/akaribot/cli/logs.py:281-281 >>>
审阅次数：2
# 没有读到文件开头时首行可能被截断，丢弃后才能保证每一行都是完整的。
<<< END U004255 >>>
<<< UNIT U004256 | py-docstring | packages/akari-bot-cli/akaribot/cli/logs.py:70-70 | ctx=LogFileInfo.name >>>
审阅次数：2
返回文件名。
<<< END U004256 >>>
<<< UNIT U004257 | py-docstring | packages/akari-bot-cli/akaribot/cli/logs.py:75-75 | ctx=LogFileInfo.level_label >>>
审阅次数：2
返回日志级别标签。
<<< END U004257 >>>
<<< UNIT U004258 | py-docstring | packages/akari-bot-cli/akaribot/cli/logs.py:126-126 | ctx=LogRingBuffer.extend >>>
审阅次数：2
追加行，返回本次丢弃的行数。
<<< END U004258 >>>
<<< UNIT U004259 | py-docstring | packages/akari-bot-cli/akaribot/cli/logs.py:134-134 | ctx=LogRingBuffer.clear >>>
审阅次数：2
清空缓冲并重置丢弃计数。
<<< END U004259 >>>
<<< UNIT U004260 | py-docstring | packages/akari-bot-cli/akaribot/cli/logs.py:140-140 | ctx=LogRingBuffer.lines >>>
审阅次数：2
返回缓冲中的行。
<<< END U004260 >>>
<<< UNIT U004261 | py-comment | packages/akari-bot-cli/akaribot/cli/main.py:33-34 >>>
审阅次数：2
# 无子命令时的退出码。click ≥8.2 把 no_args_is_help 实现为 NoArgsIsHelpError（UsageError，退出码 2），
# 语义是“参数不足”而非成功。这里沿用该退出码，同时把帮助文本留在正常输出通道，不进入错误面板。
<<< END U004261 >>>
<<< UNIT U004262 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/main.py:50-50 >>>
审阅次数：2
# noqa: BLE001 - 回退必须覆盖冻结产物的全部 metadata 读取失败
<<< END U004262 >>>
<<< UNIT U004263 | py-comment | packages/akari-bot-cli/akaribot/cli/main.py:55-57 >>>
审阅次数：2
# eager 是必需的，因为 click 先解析完参数再判定“有没有子命令”，非 eager 的回调排在该判定之后，
# ``akaribot --version`` 会被 ``Missing command.`` 抢先。``--help`` 同为 eager，两者同时给出时
# 按命令行顺序先出现的先生效（click 对 eager 参数的既定处理），且都以 0 退出。
<<< END U004263 >>>
<<< UNIT U004264 | py-comment | packages/akari-bot-cli/akaribot/cli/main.py:66-67 >>>
审阅次数：2
# 不用 click 的 no_args_is_help，因为 click ≥8.2 会把它当错误抛出，导致帮助文本通过异常通道显示（带错误面板）。
# 无参数调用改由下方回调显式打印帮助，输出通道与退出码都可控。
<<< END U004264 >>>
<<< UNIT U004265 | py-comment | packages/akari-bot-cli/akaribot/cli/main.py:103-104 >>>
审阅次数：2
# 无参数调用在可交互终端下直接进入界面。没有实例就先引导初始化。非终端（管道、CI、重定向）仍打印
# 帮助，因为那种环境下界面无法启动，把帮助放入错误面板只会让人以为出错了。
<<< END U004265 >>>
<<< UNIT U004266 | py-comment | packages/akari-bot-cli/akaribot/cli/main.py:118-118 >>>
审阅次数：2
# 界面需要读取按键并绘制全屏内容，在管道与重定向环境下不可用。
<<< END U004266 >>>
<<< UNIT U004267 | py-comment | packages/akari-bot-cli/akaribot/cli/main.py:123-124 >>>
审阅次数：2
# 初始化直接调用 ``akaribot init`` 的命令本体，不复制创建目录、安装包、写入元数据的流程。交互问答也由
# init 自己完成，两边不会各问一套。返回实例根目录，用户放弃或初始化未成功时为 ``None``。
<<< END U004267 >>>
<<< UNIT U004268 | py-comment | packages/akari-bot-cli/akaribot/cli/main.py:127-127 >>>
审阅次数：2
# 在实例之外时按注册表里的默认实例进入，这台机器上记录过就沿用该实例，而不是每次都询问是否初始化。
<<< END U004268 >>>
<<< UNIT U004269 | py-docstring | packages/akari-bot-cli/akaribot/cli/main.py:99-99 | ctx=main >>>
审阅次数：2
AkariBot 实例管理工具。
<<< END U004269 >>>
<<< UNIT U004270 | py-comment | packages/akari-bot-cli/akaribot/cli/process.py:25-25 >>>
审阅次数：2
# 等待主进程退出的默认秒数，以及主进程退出后清收子进程的宽限秒数。
<<< END U004270 >>>
<<< UNIT U004271 | py-comment | packages/akari-bot-cli/akaribot/cli/process.py:100-100 >>>
审阅次数：2
# Windows 的首字节被排他锁保护，读取记录必须避开锁区。
<<< END U004271 >>>
<<< UNIT U004272 | py-comment | packages/akari-bot-cli/akaribot/cli/process.py:172-172 >>>
审阅次数：2
# 与控制器同组的实例只能按进程号处理，对整组发送信号会连同控制器一起终止。
<<< END U004272 >>>
<<< UNIT U004273 | py-comment | packages/akari-bot-cli/akaribot/cli/process.py:190-190 >>>
审阅次数：2
# macOS 对已退出但尚未回收的组长可返回 EPERM，必须继续核对可运行成员。
<<< END U004273 >>>
<<< UNIT U004274 | py-comment | packages/akari-bot-cli/akaribot/cli/process.py:366-366 >>>
审阅次数：2
# 主进程已按自身顺序处理过子进程，这里只处理残留进程，先按正常终止，宽限期内未退出再强制终止。
<<< END U004274 >>>
<<< UNIT U004275 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:32-32 | ctx=is_windows >>>
审阅次数：2
当前平台是否为 Windows。
<<< END U004275 >>>
<<< UNIT U004276 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:51-51 | ctx=LockRecord.parse >>>
审阅次数：2
解析锁文件内容。内容缺失或不是本模块写入的记录时返回 ``None``。
<<< END U004276 >>>
<<< UNIT U004277 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:97-97 | ctx=read_lock_record >>>
审阅次数：2
读取锁文件里的进程记录。文件不存在或不可读时返回 ``None``。
<<< END U004277 >>>
<<< UNIT U004278 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:126-126 | ctx=ProcessControl >>>
审阅次数：2
进程控制原语，测试可注入模拟对象。
<<< END U004278 >>>
<<< UNIT U004279 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:129-129 | ctx=ProcessControl.process_group >>>
审阅次数：2
仅当该进程是组长时返回其所在进程组，否则返回 ``None``。
<<< END U004279 >>>
<<< UNIT U004280 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:133-133 | ctx=ProcessControl.group_alive >>>
审阅次数：2
进程组内是否仍有进程。
<<< END U004280 >>>
<<< UNIT U004281 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:137-137 | ctx=ProcessControl.terminate >>>
审阅次数：2
向单个进程发送终止信号。
<<< END U004281 >>>
<<< UNIT U004282 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:141-141 | ctx=ProcessControl.terminate_group >>>
审阅次数：2
向整个进程组发送终止信号。
<<< END U004282 >>>
<<< UNIT U004283 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:145-145 | ctx=ProcessControl.sleep >>>
审阅次数：2
等待若干秒。
<<< END U004283 >>>
<<< UNIT U004284 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:150-150 | ctx=SystemProcessControl >>>
审阅次数：2
通过平台信号或 Windows 停止事件控制实例进程。
<<< END U004284 >>>
<<< UNIT U004285 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:156-156 | ctx=SystemProcessControl.process_group >>>
审阅次数：2
见 :meth:`ProcessControl.process_group`。
<<< END U004285 >>>
<<< UNIT U004286 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:181-181 | ctx=SystemProcessControl.group_alive >>>
审阅次数：2
见 :meth:`ProcessControl.group_alive`。
<<< END U004286 >>>
<<< UNIT U004287 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:207-207 | ctx=SystemProcessControl.terminate >>>
审阅次数：2
见 :meth:`ProcessControl.terminate`。
<<< END U004287 >>>
<<< UNIT U004288 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:229-229 | ctx=SystemProcessControl.terminate_group >>>
审阅次数：2
见 :meth:`ProcessControl.terminate_group`。
<<< END U004288 >>>
<<< UNIT U004289 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:287-287 | ctx=SystemProcessControl.sleep >>>
审阅次数：2
见 :meth:`ProcessControl.sleep`。
<<< END U004289 >>>
<<< UNIT U004290 | py-docstring | packages/akari-bot-cli/akaribot/cli/process.py:377-377 | ctx=detach_kwargs >>>
审阅次数：2
返回让子进程脱离当前会话的 :mod:`subprocess` 参数。
<<< END U004290 >>>
<<< UNIT U004291 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:39-39 >>>
审阅次数：2
# 单元文件里要执行的子命令。render_unit 只负责拼装，不关心它的含义。
<<< END U004291 >>>
<<< UNIT U004292 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:170-170 >>>
审阅次数：2
# 仅在崩溃（非零退出）时重启，因为正常退出说明守护循环按信号退出，不应被立刻重启。
<<< END U004292 >>>
<<< UNIT U004293 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:209-209 >>>
审阅次数：2
# Environment= 按空白切分赋值，值里包含空白或引号时整个赋值要加引号并转义。
<<< END U004293 >>>
<<< UNIT U004294 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:222-222 >>>
审阅次数：2
# systemd 会展开未转义的 ``$``，包含空格或特殊字符的参数必须加引号并逐项转义。
<<< END U004294 >>>
<<< UNIT U004295 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/service.py:235-235 >>>
审阅次数：2
# noqa: S603 - 参数由本模块拼装
<<< END U004295 >>>
<<< UNIT U004296 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:286-286 >>>
审阅次数：2
# 默认工作目录使用注册表目录，让界面与命令行共用同一个默认值，安装生成的单元才一致。
<<< END U004296 >>>
<<< UNIT U004297 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:394-394 >>>
审阅次数：2
# 部分 macOS 版本的 launchctl 只实现 load。bootstrap 失败时回退到 load，两者语义一致。
<<< END U004297 >>>
<<< UNIT U004298 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:446-446 >>>
审阅次数：2
# 系统工具的失败原因输出在 stderr 中，截取尾部供排查。
<<< END U004298 >>>
<<< UNIT U004299 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:519-519 >>>
审阅次数：2
# 就绪时限与控制台日志路径都以 run --detach 为准，因此直接复用它的实现，避免两处判断标准分叉。
<<< END U004299 >>>
<<< UNIT U004300 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:610-610 >>>
审阅次数：2
# 用户可能正在前台运行，守护循环不干预，只说明现状。
<<< END U004300 >>>
<<< UNIT U004301 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:640-641 >>>
审阅次数：2
# 本次服务启动后尚未观察到其运行，说明是掉电或退出后的恢复，只有开启了开机自启的实例才恢复，
# “上次处于运行状态”本身不构成自启的理由。只有观察到其运行过的实例，才按崩溃处理。
<<< END U004301 >>>
<<< UNIT U004302 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/service.py:706-706 >>>
审阅次数：2
# noqa: BLE001 - 启动失败的原因如实上报，守护循环不因此中断
<<< END U004302 >>>
<<< UNIT U004303 | py-comment | packages/akari-bot-cli/akaribot/cli/service.py:746-746 >>>
审阅次数：2
# 每轮只在状态变化时输出，标签不变就不再重复同一件事。
<<< END U004303 >>>
<<< UNIT U004304 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:61-61 | ctx=ServiceError >>>
审阅次数：2
服务托管不可用（平台不受支持、单元文件已存在或系统命令失败）。
<<< END U004304 >>>
<<< UNIT U004305 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:79-79 | ctx=current_uid >>>
审阅次数：2
当前用户号。Windows 上没有该概念，返回 0 供展示。
<<< END U004305 >>>
<<< UNIT U004306 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:85-85 | ctx=supported_backends >>>
审阅次数：2
返回本模块实现的两种后端名称，供提示文案列举。
<<< END U004306 >>>
<<< UNIT U004307 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:90-90 | ctx=unsupported_detail >>>
审阅次数：2
平台不受支持时的说明，包含可执行的下一步。
<<< END U004307 >>>
<<< UNIT U004308 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:116-116 | ctx=default_log_dir >>>
审阅次数：2
服务进程控制台输出的默认保存目录。
<<< END U004308 >>>
<<< UNIT U004309 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:124-124 | ctx=default_cli_argv >>>
审阅次数：2
调用本 CLI 的 argv 前缀，不包含子命令。
<<< END U004309 >>>
<<< UNIT U004310 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:260-260 | ctx=ServiceStatus.as_dict >>>
审阅次数：2
转为 ``--json`` 输出用的字典。
<<< END U004310 >>>
<<< UNIT U004311 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:295-295 | ctx=ServiceBackend.tool >>>
审阅次数：2
本后端使用的系统工具名称。
<<< END U004311 >>>
<<< UNIT U004312 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:306-306 | ctx=ServiceBackend.log_dir >>>
审阅次数：2
服务进程控制台输出的保存目录。
<<< END U004312 >>>
<<< UNIT U004313 | py-docstring | packages/akari-bot-cli/akaribot/cli/service.py:368-368 | ctx=ServiceBackend.status >>>
审阅次数：2
读取服务状态，只使用只读命令探测是否已注册。
<<< END U004313 >>>
<<< UNIT U004314 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:1-2 >>>
审阅次数：2
模块脚手架模板
================
<<< END U004314 >>>
<<< UNIT U004315 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:4-6 >>>
审阅次数：2
本目录是 ``akaribot new module`` 的渲染输入，由 ``generated_docs/monorepo_refactor_tasks.md``
T5.5 的问卷驱动。生成器尚未实现，因此模板当前不被任何流程引用。本目录随仓库维护，
供生成器实现时直接使用。
<<< END U004315 >>>
<<< UNIT U004316 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:8-10 >>>
审阅次数：2
模板文件的语法由 ``tools/render_templates.py`` 校验，它会用样例值渲染全部模板并检查产物
是否为合法 Python、JSON 或 TOML。模板带 ``.j2`` 后缀，ruff 与其他工具默认跳过，
因此该脚本是模板的语法检查关卡，改动模板后必须运行。
<<< END U004316 >>>
<<< UNIT U004317 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:12-13 >>>
审阅次数：2
占位符
------
<<< END U004317 >>>
<<< UNIT U004318 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:15-15 >>>
审阅次数：2
占位符写成 ``[@name@]``，可安全出现在文件名与正文中：
<<< END U004318 >>>
<<< UNIT U004319 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:17-18 >>>
审阅次数：2
- Windows 禁止文件名包含 ``<`` ``>``，因此不使用尖括号。
- ``[@name@]`` 不会被 Jinja2 当作表达式求值。
<<< END U004319 >>>
<<< UNIT U004320 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:20-33 >>>
审阅次数：2
===============  ==========================================
占位符            取值
===============  ==========================================
``[@module_name@]``  模块名，必须匹配 ``[a-z0-9_]+``。它同时用作 ``module()`` 注册名、
                     locale 键前缀、表名前缀、目录名与 entry point 名
``[@module_class@]`` 模块名的大驼峰形式。生成器按 ``_`` 分段、逐段首字母大写后拼接，
                     如 ``twenty_four`` → ``TwentyFour``。用于数据库模型的类名
                     （``[@module_class@]Data``）
``[@module_desc@]``  模块的一句话说明，写入 ``module()`` 的 ``desc`` 与 zh_cn 的
                     ``[@module_name@].help.desc``
``[@author@]``       作者名，写入 pyproject 的 ``authors``。模块作者一律由该字段提供，
                     ``module()`` 不接受 ``developers``
``[@license@]``      许可证标识，写入 pyproject 的 ``license``
===============  ==========================================
<<< END U004320 >>>
<<< UNIT U004321 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:35-36 >>>
审阅次数：2
模块名限制为 ``[a-z0-9_]+`` 有两条硬性理由。多实例的 ``client_name`` 以 ``-``
作分隔符，适配器与模块的 entry point 名不得包含 ``-``。TOML 的裸键同样会拒绝 ``-``。
<<< END U004321 >>>
<<< UNIT U004322 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:38-39 >>>
审阅次数：2
渲染约定
--------
<<< END U004322 >>>
<<< UNIT U004323 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:41-41 >>>
审阅次数：2
生成器按两步处理，顺序不可颠倒：
<<< END U004323 >>>
<<< UNIT U004324 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:43-43 >>>
审阅次数：2
1. **路径替换**：复制目录树时，把路径中的 ``[@name@]`` 换成取值，得到
<<< END U004324 >>>
<<< UNIT U004325 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:44-44 >>>
审阅次数：2
   ``akaribot/modules/<实际模块名>/``。
<<< END U004325 >>>
<<< UNIT U004326 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:45-45 >>>
审阅次数：2
2. **内容渲染**：用 Jinja2 渲染文件内容，再用同一份取值做一次 ``[@name@]`` 明文替换
<<< END U004326 >>>
<<< UNIT U004327 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:46-46 >>>
审阅次数：2
   （路径与文本中的占位符都要替换），最后做一次 ``html.unescape``。
<<< END U004327 >>>
<<< UNIT U004328 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:48-48 >>>
审阅次数：2
第二步的顺序与转义有两处硬性原因：
<<< END U004328 >>>
<<< UNIT U004329 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:50-50 >>>
审阅次数：2
- 占位符替换必须放在 Jinja2 渲染之后。若把 ``[@module_name@]`` 注册成 Jinja2 变量，
<<< END U004329 >>>
<<< UNIT U004330 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:51-52 >>>
审阅次数：2
  命令模板 ``"{{I18N:[@module_name@].help.echo}}"`` 里的 ``{{`` 会被 Jinja2 当作表达式
  起始符，模板直接报语法错误。
<<< END U004330 >>>
<<< UNIT U004331 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:53-53 >>>
审阅次数：2
- 命令模板的 ``{{I18N:key}}`` 标记在本项目里是普通文本，但 Jinja2 会解析它。
<<< END U004331 >>>
<<< UNIT U004332 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:54-55 >>>
审阅次数：2
  因此模板中把它写成 HTML 实体 ``&#123;&#123;I18N:...&#125;&#125;``，渲染后用
  ``html.unescape`` 还原。这样既不需要 ``jinja2.ext.i18n`` 扩展，也不需要 ``raw`` 标签。
<<< END U004332 >>>
<<< UNIT U004333 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:63-64 >>>
审阅次数：2
目录结构
--------
<<< END U004333 >>>
<<< UNIT U004334 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:82-84 >>>
审阅次数：2
`assets/README.md` 与 `database/__init__.py.j2` 的存在有两个作用，一是保证目录可被 git
跟踪（空目录不会进版本库），二是向模块作者说明该目录的用途。生成器不需要删除它们，
其中 `assets/README.md` 会随包分发。
<<< END U004334 >>>
<<< UNIT U004335 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:86-87 >>>
审阅次数：2
生成后的目录与 ``packages/modules/akari-bot-module-<实际模块名>/`` 目录结构一致，可直接
``akaribot module add -e .``。
<<< END U004335 >>>
<<< UNIT U004336 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:89-90 >>>
审阅次数：2
约定
----
<<< END U004336 >>>
<<< UNIT U004337 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:92-92 >>>
审阅次数：2
1. 生成的 ``locales/zh_cn.json`` 只包含简体中文。其余语言由 Weblate 自动提交，不得由
<<< END U004337 >>>
<<< UNIT U004338 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:93-93 >>>
审阅次数：2
   生成器写入。
<<< END U004338 >>>
<<< UNIT U004339 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:94-94 >>>
审阅次数：2
2. 生成的代码一律 ``from akaribot.core.api import ...``，不引入 ``akaribot.core`` 的
<<< END U004339 >>>
<<< UNIT U004340 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:95-95 >>>
审阅次数：2
   内部路径。该公开接口在公共 API 约定阶段（P5）建立。
<<< END U004340 >>>
<<< UNIT U004341 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:96-96 >>>
审阅次数：2
3. ``config.py`` 中的字段名以模块名作前缀，字段注释保存在 ``locales/zh_cn.json`` 的
<<< END U004341 >>>
<<< UNIT U004342 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/README.md:97-97 >>>
审阅次数：2
   ``config.comments.module_[@module_name@].<字段名>``。
<<< END U004342 >>>
<<< UNIT U004343 | md-list | packages/akari-bot-cli/akaribot/cli/templates/README.md:98-99 >>>
审阅次数：2
4. 数据库表名以 ``module_[@module_name@]_`` 作前缀，且不得包含 ``-``。
5. 不需要数据库或配置的模块，由生成器删除对应文件与 manifest 中的对应字段，不保留空文件。
<<< END U004343 >>>
<<< UNIT U004344 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:1-2 >>>
审阅次数：2
适配器脚手架模板
================
<<< END U004344 >>>
<<< UNIT U004345 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:4-4 >>>
审阅次数：2
本目录是 ``akaribot new adapter`` 的渲染输入。占位符沿用 ``templates/module/`` 的五个名称：
<<< END U004345 >>>
<<< UNIT U004346 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:6-15 >>>
审阅次数：2
===============  ==========================================
占位符            取值
===============  ==========================================
``[@module_name@]``  适配器名，必须匹配 ``[a-z0-9_]+``。它同时用作目录名、包名后缀、entry
                     point 名、``on_bot_config()`` 的平台名与 locale 键前缀
``[@module_class@]`` 适配器名的大驼峰形式，用作 ``ContextManager`` 与配置类的类名前缀
``[@module_desc@]``  适配器的一句话说明
``[@author@]``       作者名
``[@license@]``      许可证标识
===============  ==========================================
<<< END U004346 >>>
<<< UNIT U004347 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:17-18 >>>
审阅次数：2
复用同一套占位符名称是为了让 ``tools/render_templates.py`` 的样例渲染无需改动即可覆盖本目录：
它只认识上述五个名称，其余取值一律通过 Jinja 变量传入并带 ``default``，因此样例渲染不会失败。
<<< END U004347 >>>
<<< UNIT U004348 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:20-21 >>>
审阅次数：2
目录与正文的分工
----------------
<<< END U004348 >>>
<<< UNIT U004349 | md-list | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:23-24 >>>
审阅次数：2
- **路径**：`akaribot/adapters/[@module_name@]/` 的目录名在复制时替换。
- **正文**：Jinja 变量负责能力清单、配置字段等结构化取值，占位符负责名称与文案。
<<< END U004349 >>>
<<< UNIT U004350 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:26-27 >>>
审阅次数：2
维护工具
--------
<<< END U004350 >>>
<<< UNIT U004351 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:29-29 >>>
审阅次数：2
`TEMPLATE.md` 与 `selfcheck.py` 由生成器跳过，不随生成产物分发。改动模板后运行一次自检：
<<< END U004351 >>>
<<< UNIT U004352 | md-paragraph | packages/akari-bot-cli/akaribot/cli/templates/adapter/TEMPLATE.md:35-36 >>>
审阅次数：2
它对该目录下的每个 `akari-bot-adapter-*` 运行 ruff check / ruff format（仓库配置与 ruff 默认配置
各一遍）、tomllib 解析、entry point 名与 core 约束检查，以及导入边界检查。
<<< END U004352 >>>
<<< UNIT U004353 | py-docstring | packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py:34-34 | ctx=report >>>
审阅次数：2
打印一条检查结果并记录失败项。
<<< END U004353 >>>
<<< UNIT U004354 | py-docstring | packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py:41-41 | ctx=ruff_binary >>>
审阅次数：2
获取 ruff 可执行文件，优先使用仓库虚拟环境中的版本。
<<< END U004354 >>>
<<< UNIT U004355 | py-docstring | packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py:46-46 | ctx=ruff >>>
审阅次数：2
对一组文件运行 ruff，返回是否通过与合并后的输出。
<<< END U004355 >>>
<<< UNIT U004356 | py-docstring | packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py:57-57 | ctx=core_imports >>>
审阅次数：2
列出源码里出现的 akaribot.core 导入路径。
<<< END U004356 >>>
<<< UNIT U004357 | py-docstring | packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py:73-73 | ctx=check_layout >>>
审阅次数：2
检查结构文件齐全，返回导入包目录。
<<< END U004357 >>>
<<< UNIT U004358 | py-docstring | packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py:82-82 | ctx=check_metadata >>>
审阅次数：2
检查 pyproject 与 manifest 的解析结果与关键字段。
<<< END U004358 >>>
<<< UNIT U004359 | py-docstring | packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py:100-100 | ctx=check_package >>>
审阅次数：2
检查一个生成的适配器包。
<<< END U004359 >>>
<<< UNIT U004360 | py-docstring | packages/akari-bot-cli/akaribot/cli/templates/adapter/selfcheck.py:127-127 | ctx=main >>>
审阅次数：2
入口函数，逐个检查命令行给出的生成目录并返回进程退出码。
<<< END U004360 >>>
<<< UNIT U004361 | cfg-comment | packages/akari-bot-cli/akaribot/cli/templates/module/.github/workflows/publish.yml:1-2 >>>
审阅次数：2
# 第三方模块包的发布工作流，推送 v* 标签后构建 wheel 并以 Trusted Publishing 发布到 PyPI。
# 使用前需在 PyPI 为本仓库添加受信发布者与该工作流文件，见 https://docs.pypi.org/trusted-publishers/
<<< END U004361 >>>
<<< UNIT U004362 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:3-4 | ctx=AkariBot TUI（Textual） >>>
审阅次数：2
TUI 提供实例、模块、适配器、配置与运行环境的管理界面。Textual 的导入与兼容处理集中在
`_compat.py`。页面通过数据源读取状态，写入操作通过 CLI 子进程执行。
<<< END U004362 >>>
<<< UNIT U004363 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:6-6 | ctx=文件职责 >>>
审阅次数：2
## 文件职责
<<< END U004363 >>>
<<< UNIT U004364 | md-table | packages/akari-bot-cli/akaribot/cli/tui/README.md:8-25 | ctx=文件职责 >>>
审阅次数：2
| 文件 | 职责 |
| --- | --- |
| `_compat.py` | Textual 兼容接口、显示宽度计算、资源与样式表加载、快捷键、按钮布局与确认框 |
| `cli_process.py` | CLI 子进程参数与环境，处理冻结入口、实例目录及 UTF-8 编码 |
| `context.py` | 当前实例上下文。数据源在请求时解析实例目录 |
| `app.py` | 应用装配、侧栏与页面注册、全局快捷键、退出检查 |
| `dashboard.py` | 本机实例清单、启动准备状态、服务管理与当前实例详情 |
| `environment.py` | 环境包清单、运行库安装与卸载、解释器管理 |
| `database.py` | 数据表与数据项浏览、筛选、排序、分页与编辑 |
| `modules.py` | 模块安装、卸载、更新、装载切换与批量操作 |
| `adapters.py` | 适配器安装、启用状态与实例配置管理 |
| `config.py` | 配置表、表单编辑、原始文本编辑与外部编辑器 |
| `logs.py` | 日志进程筛选、滚动跟踪、关键词过滤与调试日志切换 |
| `run.py` | 实例启动、停止、重启、指定适配器启动与状态轮询 |
| `dev.py` | 工作区包来源、运行测试、生成脚手架与操作输出 |
| `doctor.py` | 端口冲突、登录信息重复、孤立配置等诊断结果与处理入口 |
| `misc.py` | 旧版项目迁移与迁移预览 |
| `commands/tui.py` | `akaribot tui`、`--self-check`、`--headless` 与 `--no-mouse` 入口 |
<<< END U004364 >>>
<<< UNIT U004365 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:27-28 | ctx=文件职责 >>>
审阅次数：2
`akaribot/cli/tui/` 下除 `_compat.py` 外的模块不得直接导入 `textual` 或 `rich`。
`commands/tui.py` 延迟导入界面模块，普通 CLI 命令无需加载 Textual。
<<< END U004365 >>>
<<< UNIT U004366 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:30-30 | ctx=导航与交互 >>>
审阅次数：2
## 导航与交互
<<< END U004366 >>>
<<< UNIT U004367 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:32-33 | ctx=导航与交互 >>>
审阅次数：2
侧栏按四组排列，依次为概览与运行（概览、运行、日志、诊断）、配置与平台（配置、适配器、模块）、
环境与数据（环境、数据库）与开发与迁移（开发、文档、迁移）。
<<< END U004367 >>>
<<< UNIT U004368 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:35-37 | ctx=导航与交互 >>>
审阅次数：2
分组标题支持高亮，`Enter` 或单击切换
本组的折叠状态。`←` 折叠高亮条目所属的分组，`→` 展开高亮的分组标题。折叠组内的页面条目隐藏并被
方向键跳过。
<<< END U004368 >>>
<<< UNIT U004369 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:39-39 | ctx=导航与交互 >>>
审阅次数：2
当前页位于折叠组内时，高亮显示在分组标题上。折叠状态仅在本次会话内保留，切换实例不重置。
<<< END U004369 >>>
<<< UNIT U004370 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:41-41 | ctx=导航与交互 >>>
审阅次数：2
`ctrl+←/→` 按侧栏顺序循环切换页面，折叠组内的页面同样可达。切换页面后由 `focus_primary()` 将焦点移入当前页面。
<<< END U004370 >>>
<<< UNIT U004371 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:43-44 | ctx=导航与交互 >>>
审阅次数：2
`?` 显示当前页用途、导航说明及完整快捷键。页脚仅显示高频操作。低频和危险操作的入口由按钮或快捷键
帮助提供。80 列下退出与帮助入口保持可见。标题栏显示当前实例，`ctrl+t` 切换深色与浅色主题。
<<< END U004371 >>>
<<< UNIT U004372 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:46-46 | ctx=键位语法 >>>
审阅次数：2
### 键位语法
<<< END U004372 >>>
<<< UNIT U004373 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:48-48 | ctx=键位语法 >>>
审阅次数：2
同一语义在各页只用一个键，页面按需绑定。
<<< END U004373 >>>
<<< UNIT U004374 | md-table | packages/akari-bot-cli/akaribot/cli/tui/README.md:50-65 | ctx=键位语法 >>>
审阅次数：2
| 语义 | 键 |
| --- | --- |
| 刷新 | `r` |
| 搜索 / 过滤 | `/` |
| 返回一级（清空搜索，搜索已空时焦点回到列表） | `Esc` |
| 列表项默认动作 | `Enter` |
| 选择 / 全选 / 清空选择（多选页） | `Space` / `a` / `c` |
| 新建 / 新增 | `n` |
| 安装 / 卸载 / 更新 | `i` / `u` / `U` |
| 删除 / 移除（弹出确认） | `ctrl+d` |
| 保存 | `ctrl+s` |
| 在外部打开 | `o` |
| 开关切换（启用、加载） | `e` |
| 预览 / 试运行 | `p` |
| 本页低频操作菜单 | `m` |
| 翻页 / 首页与末页 | `[` / `]`、`g` / `G` |
<<< END U004374 >>>
<<< UNIT U004375 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:67-69 | ctx=键位语法 >>>
审阅次数：2
按钮文字通过 `compat.key_hint()` 附上快捷键（如“安装 i”“移除实例 ^d”），写法与页脚一致。
按钮栏依次为主操作（唯一的 primary）、次要操作、破坏性操作（error）、低频菜单、刷新。
低频操作不占用按钮，收纳在 `m` 打开的菜单中，菜单只列出当前状态下可用的项。
<<< END U004375 >>>
<<< UNIT U004376 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:71-71 | ctx=键位语法 >>>
审阅次数：2
- 删除、移除、卸载等操作必须弹出模态确认框，列出目标、更改范围及可选项。删除和移除使用
<<< END U004376 >>>
<<< UNIT U004377 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:72-72 | ctx=键位语法 >>>
审阅次数：2
  `ctrl+d` 等组合键，卸载使用专用键 `u`。
<<< END U004377 >>>
<<< UNIT U004378 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:73-74 | ctx=键位语法 >>>
审阅次数：2
- 确认框按钮按宽度换行，长说明可滚动查看。取消按钮与输入框保持可见。
- `PendingConfirm.accept(key)` 在 0.4 秒防抖窗口内忽略同一目标的重复请求。切换页面、手动刷新或
<<< END U004378 >>>
<<< UNIT U004379 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:75-75 | ctx=键位语法 >>>
审阅次数：2
  更换选中项时调用 `reset_pending()`。周期轮询不清除确认状态。
<<< END U004379 >>>
<<< UNIT U004380 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:76-77 | ctx=键位语法 >>>
审阅次数：2
- 模块卸载选择清理数据时，必须输入确认文字。超过 10 个目标的批量卸载还必须确认目标数量。
- 配置页与数据库页通过 `dirty_note()` 报告未保存更改。更换编辑对象、重新加载、切换模式或实例前
<<< END U004380 >>>
<<< UNIT U004381 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:78-78 | ctx=键位语法 >>>
审阅次数：2
  必须确认是否放弃更改。
<<< END U004381 >>>
<<< UNIT U004382 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:79-79 | ctx=键位语法 >>>
审阅次数：2
- `q` / `ctrl+q` 统一检查未保存更改与后台任务，并在同一确认框中列出。取消后保留内容并恢复原焦点。
<<< END U004382 >>>
<<< UNIT U004383 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:80-80 | ctx=键位语法 >>>
审阅次数：2
  无更改与任务时直接退出。
<<< END U004383 >>>
<<< UNIT U004384 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:81-81 | ctx=键位语法 >>>
审阅次数：2
- 支持预览的操作在确认框中提供预览入口。环境重建执行前另需输入“重建”。预览无需输入确认文字。
<<< END U004384 >>>
<<< UNIT U004385 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:83-83 | ctx=页面使用 >>>
审阅次数：2
## 页面使用
<<< END U004385 >>>
<<< UNIT U004386 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:85-85 | ctx=概览 >>>
审阅次数：2
### 概览
<<< END U004386 >>>
<<< UNIT U004387 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:87-87 | ctx=概览 >>>
审阅次数：2
- 实例清单读取本机注册表 `~/.akaribot/instances.toml`，路径可通过 `AKARIBOT_HOME` 更改。
<<< END U004387 >>>
<<< UNIT U004388 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:88-88 | ctx=概览 >>>
审阅次数：2
  每行显示注册名、运行状态、位置与启动策略。当前实例以 `▸` 标记，未收录的当前实例也会列出。
<<< END U004388 >>>
<<< UNIT U004389 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:89-89 | ctx=概览 >>>
审阅次数：2
- CLI 启动入口自动收录当前实例，已存在时跳过。在实例目录外启动且仅有一个下级实例时，可收录并
<<< END U004389 >>>
<<< UNIT U004390 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:90-90 | ctx=概览 >>>
审阅次数：2
  切换到该实例。存在多个候选时显示候选列表。`--self-check` 与 `--headless` 不写入注册表。
<<< END U004390 >>>
<<< UNIT U004391 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:91-91 | ctx=概览 >>>
审阅次数：2
- 实例清单上按 `Enter` 切换实例。已收录实例同时通过 `instance use` 保存为默认实例。未收录实例仅用于
<<< END U004391 >>>
<<< UNIT U004392 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:92-92 | ctx=概览 >>>
审阅次数：2
  当前会话。切换后重新挂载页面，数据源通过 `context.resolve_root()` 解析当前实例目录。
<<< END U004392 >>>
<<< UNIT U004393 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:93-93 | ctx=概览 >>>
审阅次数：2
- `n` 打开添加实例菜单，新建实例时选择由框架管理的 venv 或当前环境，通过
<<< END U004393 >>>
<<< UNIT U004394 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:94-95 | ctx=概览 >>>
审阅次数：2
  `akaribot init <目录> --non-interactive` 执行并显示进度。添加已有目录时只把该实例加入清单。
  `ctrl+d` 确认移除记录，保留实例目录。
<<< END U004394 >>>
<<< UNIT U004395 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:96-96 | ctx=概览 >>>
审阅次数：2
- `m` 打开所选已收录实例的服务与策略菜单，可开启或关闭开机自启与崩溃重启，或安装与卸载服务。平台不支持
<<< END U004395 >>>
<<< UNIT U004396 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:97-97 | ctx=概览 >>>
审阅次数：2
  服务时不列出服务项。服务恢复实例时同时要求启用自启且实例上次处于运行状态。
<<< END U004396 >>>
<<< UNIT U004397 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:98-98 | ctx=概览 >>>
审阅次数：2
- 服务安装或卸载另有确认框，可选择执行、预览或取消。覆盖已有服务文件时明确列出覆盖范围。
<<< END U004397 >>>
<<< UNIT U004398 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:99-99 | ctx=概览 >>>
审阅次数：2
  服务文件由 CLI 生成，并记录 `AKARIBOT_HOME`，使服务与 CLI 使用相同注册表。
<<< END U004398 >>>
<<< UNIT U004399 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:100-100 | ctx=概览 >>>
审阅次数：2
- 启动准备区显示未配置适配器、待填写配置、运行状态及最近诊断结果，提供配置、启动与诊断入口。
<<< END U004399 >>>
<<< UNIT U004400 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:101-101 | ctx=概览 >>>
审阅次数：2
  数据通过 `doctor --json`、运行锁与 `config placeholders --json` 获取。配置检查不可用时显示估算标记。
<<< END U004400 >>>
<<< UNIT U004401 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:102-102 | ctx=概览 >>>
审阅次数：2
- 按钮宽度不足时换行。不可用的操作禁用并说明原因。80×24 下实例清单
<<< END U004401 >>>
<<< UNIT U004402 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:103-103 | ctx=概览 >>>
审阅次数：2
  显示 4 行，60×20 下显示 2 行，详情可滚动。短屏按钮使用单行高度，扩大窗口后恢复常规高度。
<<< END U004402 >>>
<<< UNIT U004403 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:105-105 | ctx=模块与适配器 >>>
审阅次数：2
### 模块与适配器
<<< END U004403 >>>
<<< UNIT U004404 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:107-108 | ctx=模块与适配器 >>>
审阅次数：2
模块页合并已安装模块与可安装清单，按包名去重。搜索与“仅已安装”筛选位于同一行，统计信息独立
显示。表头与数据行共用列宽计划，窄屏优先隐藏简介列并保留名称。
<<< END U004404 >>>
<<< UNIT U004405 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:110-111 | ctx=模块与适配器 >>>
审阅次数：2
可安装清单读取失败时，保留已安装
记录并显示原因。模块页按 `kind` 过滤，适配器仅在适配器页显示。
<<< END U004405 >>>
<<< UNIT U004406 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:113-113 | ctx=模块与适配器 >>>
审阅次数：2
- `i` 安装、`u` 卸载选区中的适用项，无选区时使用当前项。安装仅处理未安装项，卸载仅处理已安装项。
<<< END U004406 >>>
<<< UNIT U004407 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:114-115 | ctx=模块与适配器 >>>
审阅次数：2
  安装选区或高亮项前弹出确认框列出目标。`U` 选择更新当前选区或全部已安装模块（`--all`），
  `e` 切换当前包的全局装载。进度条只在操作进行时显示。
<<< END U004407 >>>
<<< UNIT U004408 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:116-116 | ctx=模块与适配器 >>>
审阅次数：2
- `Space` 切换当前项，`Shift+↑/↓` 从锚点扩展选区，`a` 全选可见项，`c` 清除选择。
<<< END U004408 >>>
<<< UNIT U004409 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:117-117 | ctx=模块与适配器 >>>
审阅次数：2
  普通点击单选，`Ctrl+点击` 切换，`Shift+点击` 扩展选区。
<<< END U004409 >>>
<<< UNIT U004410 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:118-118 | ctx=模块与适配器 >>>
审阅次数：2
- 清理数据的确认框列出目标包、配置文件与数据表。单个包输入包名，批量时输入确认框中指定的确认文字。
<<< END U004410 >>>
<<< UNIT U004411 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:119-119 | ctx=模块与适配器 >>>
审阅次数：2
  取消或输入不匹配时不执行。超过 10 个目标时还必须先输入目标数量。
<<< END U004411 >>>
<<< UNIT U004412 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:120-121 | ctx=模块与适配器 >>>
审阅次数：2
- 批量操作逐项显示进度，单项失败不终止其余操作。完成后汇总结果，成功项移出选区，失败项保留供重试。
- 适配器页按平台合并 `adapter list --json` 与 `module available --kind adapter --json` 的结果。
<<< END U004412 >>>
<<< UNIT U004413 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:122-124 | ctx=模块与适配器 >>>
审阅次数：2
  列表只显示已安装或已启用的适配器。未安装且未启用的平台不显示在列表中，缺少包但已启用的配置仍列出并标注未安装。
  `i` 或安装适配器按钮打开对话框，列出全部未安装的平台，回车安装高亮项，单击只改变高亮。当前行
  未安装时预选该平台。已安装实例提供启用与停用入口。安装完成后刷新清单。
<<< END U004413 >>>
<<< UNIT U004414 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:125-125 | ctx=模块与适配器 >>>
审阅次数：2
- `n` 或新增实例按钮打开对话框，列表只包含已安装的平台（取自 `adapter list --json` 的
<<< END U004414 >>>
<<< UNIT U004415 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:126-128 | ctx=模块与适配器 >>>
审阅次数：2
  `installed_platforms`，可安装清单读取失败时仍可用），预选当前行的平台，并标出各平台已有的实例。
  输入框获得焦点时 `↑` / `↓` 仍可切换平台。实例 ID 必填，空值、非法字符与重名在对话框内提示且不关闭。
  确认后通过 `adapter instance add` 新建，配置默认未启用。
<<< END U004415 >>>
<<< UNIT U004416 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:129-129 | ctx=模块与适配器 >>>
审阅次数：2
- 新建成功后按 `config schema` 弹出配置表单，待填写项排最前且为空，留空不写入。`enable` 排最后，确保登录信息
<<< END U004416 >>>
<<< UNIT U004417 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:130-132 | ctx=模块与适配器 >>>
审阅次数：2
  先于启用写入。回车移到下一项，`ctrl+s` 保存，逐项通过 `config set` 写入，密钥项写入 `_secret` 段且错误
  提示不包含命令输出。写入失败时停在出错项，重试不重复已写入的项。`Esc` 稍后填写，有未保存内容时先确认。
  实例已创建，跳过表单或无法读取配置项都不影响该实例。表单为 `config.ConfigFormScreen`，与配置页共用 `FieldRow`。
<<< END U004417 >>>
<<< UNIT U004418 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:133-133 | ctx=模块与适配器 >>>
审阅次数：2
- `ctrl+d` 或移除按钮请求移除适配器实例配置，仅删除配置文件，保留场景与用户数据。
<<< END U004418 >>>
<<< UNIT U004419 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:134-134 | ctx=模块与适配器 >>>
审阅次数：2
  操作按钮使用自适应布局，在 80×24 与 60×20 下保持可见。
<<< END U004419 >>>
<<< UNIT U004420 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:136-136 | ctx=环境 >>>
审阅次数：2
### 环境
<<< END U004420 >>>
<<< UNIT U004421 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:138-139 | ctx=环境 >>>
审阅次数：2
环境页管理实例解释器与运行库。模块的安装与运行时加载在模块页管理。包清单包含全部已安装包、
间接依赖及实例清单中的未安装记录。
<<< END U004421 >>>
<<< UNIT U004422 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:141-141 | ctx=环境 >>>
审阅次数：2
- `●` 表示包已记录在 `akaribot.toml` 的 `runtime.requirements` 中，`○` 表示仅存在于当前环境。
<<< END U004422 >>>
<<< UNIT U004423 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:142-142 | ctx=环境 >>>
审阅次数：2
  标签标识模块、适配器、AkariBot 包、可编辑安装或未安装状态。
<<< END U004423 >>>
<<< UNIT U004424 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:143-143 | ctx=环境 >>>
审阅次数：2
- 搜索匹配包名与来源地址，筛选可限制为清单记录。统计信息独立成行，避免挤占搜索文字区域。
<<< END U004424 >>>
<<< UNIT U004425 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:144-144 | ctx=环境 >>>
审阅次数：2
  窄屏优先隐藏标签列。
<<< END U004425 >>>
<<< UNIT U004426 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:145-145 | ctx=环境 >>>
审阅次数：2
- `i` 输入 PyPI 包名、版本范围、仓库地址或 `git+` 直接引用，再选择安装并写入清单（`--save`）或
<<< END U004426 >>>
<<< UNIT U004427 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:146-146 | ctx=环境 >>>
审阅次数：2
  仅安装到当前环境（`--no-save`）。重建时自动安装清单运行库，未记录的额外运行库不随重建保留。
<<< END U004427 >>>
<<< UNIT U004428 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:147-147 | ctx=环境 >>>
审阅次数：2
- `u` 卸载包，可同时移除清单记录或保留记录。未记录的包也必须确认后卸载。
<<< END U004428 >>>
<<< UNIT U004429 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:148-148 | ctx=环境 >>>
审阅次数：2
  选中项显示反向依赖，供判断卸载影响。
<<< END U004429 >>>
<<< UNIT U004430 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:149-150 | ctx=环境 >>>
审阅次数：2
- 包安装与卸载可在实例运行期间执行。已导入的模块仍保留在进程中，更改后必须重启实例才能生效。
- `m` 或“解释器…”按钮打开解释器菜单，包括改用由框架管理的 venv、改用系统解释器与重建实例 venv，
<<< END U004430 >>>
<<< UNIT U004431 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:151-151 | ctx=环境 >>>
审阅次数：2
  只列出当前模式适用的操作。未知模式显示原因。实例运行期间拒绝更改解释器。
<<< END U004431 >>>
<<< UNIT U004432 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:152-154 | ctx=环境 >>>
审阅次数：2
- 解释器确认框提供执行、预览与取消。执行重建前必须输入“重建”。取消或输入不匹配均不执行。
- 摘要区高度随窗口调整，完整字段可滚动查看。短屏按钮使用单行高度，为包清单保留空间。
- 环境所属范围按包含 `pyvenv.cfg` 的环境根目录判断。多个 venv 的 `bin/python` 可能指向同一基础解释器，
<<< END U004432 >>>
<<< UNIT U004433 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:155-155 | ctx=环境 >>>
审阅次数：2
  不能使用符号链接解析后的解释器路径判定环境是否相同。
<<< END U004433 >>>
<<< UNIT U004434 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:157-157 | ctx=数据库 >>>
审阅次数：2
### 数据库
<<< END U004434 >>>
<<< UNIT U004435 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:159-160 | ctx=数据库 >>>
审阅次数：2
数据库页提供数据表清单、分页数据项与编辑区，窄屏改为纵向排列。数据通过 `akaribot db tables/rows`
读取，写入通过 `db set/insert/delete` 执行，仅接受 core 注册的 ORM 表与列。
<<< END U004435 >>>
<<< UNIT U004436 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:162-162 | ctx=数据库 >>>
审阅次数：2
- `f` 输入筛选条件 `<列><运算符><值>`。支持 `=`、`!=`、`>`、`>=`、`<`、`<=`、`~`（包含）、
<<< END U004436 >>>
<<< UNIT U004437 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:163-164 | ctx=数据库 >>>
审阅次数：2
  `!~`（不包含）、`^`（前缀）、`$`（后缀），`null` 表示空值。其他输入按全表文本搜索处理，
  多条件使用 AND。`ctrl+f` 或 `m` 菜单清除筛选与搜索，保留排序。
<<< END U004437 >>>
<<< UNIT U004438 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:165-166 | ctx=数据库 >>>
审阅次数：2
- `m` 菜单用于设置排序，列名表示升序，`列名:desc` 表示降序，留空使用默认主键倒序。
- 每页最多 50 条，`[` / `]` 翻页，`g` / `G` 跳转首页和末页。更换表或筛选条件时重置分页。
<<< END U004438 >>>
<<< UNIT U004439 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:167-167 | ctx=数据库 >>>
审阅次数：2
  数据变化导致当前偏移超出范围时，调整到末页。纯翻页使用 `--no-count`，复用已获取的总数。
<<< END U004439 >>>
<<< UNIT U004440 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:168-168 | ctx=数据库 >>>
审阅次数：2
- `ctrl+s` 保存、`n` 新建、`ctrl+d` 删除，写入前显示目标与更改摘要。`ctrl+s` 在输入框聚焦时同样生效。
<<< END U004440 >>>
<<< UNIT U004441 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:169-170 | ctx=数据库 >>>
审阅次数：2
  `Esc` 关闭确认框或取消编辑。按钮栏位于页底，短屏时按钮改为单行。
  新建时自增主键可留空，非自增主键必须填写。
<<< END U004441 >>>
<<< UNIT U004442 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:171-171 | ctx=数据库 >>>
审阅次数：2
- 同一行的多列更改合并为一次 `db set --key … --set 列=值 …`，core 在事务中校验并更新整行。
<<< END U004442 >>>
<<< UNIT U004443 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:172-172 | ctx=数据库 >>>
审阅次数：2
  任一值非法时不更新该行。写入成功后刷新当前表并尽量保持原主键选中。
<<< END U004443 >>>
<<< UNIT U004444 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:174-174 | ctx=运行与日志 >>>
审阅次数：2
### 运行与日志
<<< END U004444 >>>
<<< UNIT U004445 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:176-178 | ctx=运行与日志 >>>
审阅次数：2
实例启动通过 `akaribot run --detach`，状态通过 `run --status --json`，停止通过 `run --stop`。
实例独立于 TUI 进程运行，退出界面不终止实例。运行锁用于判断状态。停止时先请求正常退出，超时后
强制终止，并按进程组执行清理。
<<< END U004445 >>>
<<< UNIT U004446 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:180-181 | ctx=运行与日志 >>>
审阅次数：2
状态查询在后台执行，同类请求仅保留最新任务。运行页按钮按宽度换行，状态表使用剩余空间并支持
滚动。`s` / `x` / `ctrl+r` 启动、停止与重启，均先确认。启动指定适配器与前台运行命令在 `m` 菜单中。
<<< END U004446 >>>
<<< UNIT U004447 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:183-184 | ctx=运行与日志 >>>
审阅次数：2
日志页按 `space` 暂停或恢复跟踪，`c` 清空显示缓冲，`m` 打开日志级别菜单，可自动跟随最新文件，或优先跟随
INFO、debug 文件。日志解析规则由 `akaribot/cli/logs.py` 提供，CLI 与界面共用。
<<< END U004447 >>>
<<< UNIT U004448 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:186-186 | ctx=开发与迁移 >>>
审阅次数：2
### 开发与迁移
<<< END U004448 >>>
<<< UNIT U004449 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:188-189 | ctx=开发与迁移 >>>
审阅次数：2
开发页展示工作区路径、包来源与可编辑安装状态。`t` 按测试路径输入框中的路径运行测试，`n` 打开新建包对话框：
提供名称、类型、目录及适用的配置、数据库、测试选项，名称非法时在对话框内提示。
<<< END U004449 >>>
<<< UNIT U004450 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:191-192 | ctx=开发与迁移 >>>
审阅次数：2
未提供的选项使用 CLI
默认值。
<<< END U004450 >>>
<<< UNIT U004451 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:194-195 | ctx=开发与迁移 >>>
审阅次数：2
开发操作的完整输出保留在滚动区域，长行自动换行。`o` 或“查看输出”聚焦输出区，支持 `Home`、
`End`、`PgUp`、`PgDn` 与方向键。视口位于末尾时自动滚动，上滚后暂停，`End` 恢复自动滚动。
<<< END U004451 >>>
<<< UNIT U004452 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:197-197 | ctx=开发与迁移 >>>
审阅次数：2
状态栏显示结果与下一步，输出标题显示行数。`Esc` 请求终止运行中的操作。
<<< END U004452 >>>
<<< UNIT U004453 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:199-200 | ctx=开发与迁移 >>>
审阅次数：2
迁移页 `Enter` 请求源目录，再显示迁移参数与确认框。预览仅显示计划，执行将向当前实例写入配置与
数据。源目录保持只读。
<<< END U004453 >>>
<<< UNIT U004454 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:202-202 | ctx=开发与迁移 >>>
审阅次数：2
`p` 对最近一次预览或迁移的源目录重新试运行。输出区无内容时隐藏，避免占用布局空间。
<<< END U004454 >>>
<<< UNIT U004455 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:204-206 | ctx=开发与迁移 >>>
审阅次数：2
文档页 `r` 刷新、`/` 搜索、`space` 选择、`b` 构建、`p` 静态预览、`e` 开发预览、`o` 打开浏览器，
部署、同步主题、安装依赖与任务日志收在 `m` 菜单。开发预览通过 `docs dev --json --port 0` 获取就绪
地址，之后继续读取事件流更新状态与日志。
<<< END U004455 >>>
<<< UNIT U004456 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:208-209 | ctx=开发与迁移 >>>
审阅次数：2
两种预览共用 `cache/docs/node_modules`，启动其一即停止
另一，离开页面时都在后台停止。
<<< END U004456 >>>
<<< UNIT U004457 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:211-211 | ctx=实现约定 >>>
审阅次数：2
## 实现约定
<<< END U004457 >>>
<<< UNIT U004458 | md-table | packages/akari-bot-cli/akaribot/cli/tui/README.md:213-226 | ctx=实现约定 >>>
审阅次数：2
| 接口或约定 | 用途与限制 |
| --- | --- |
| `display_width()`、`truncate_cells()`、`pad_cells()`、`fit_cells()` | 按终端单元格计算宽度，禁止用 `len()` 或字符串补空格代替显示宽度 |
| `align_rows()` | 统一详情标签列宽，支持中日韩字符与英文混排 |
| `text-wrap: nowrap; text-overflow: ellipsis` | 列表行保持单行。实际列宽仍必须按控件宽度计算 |
| `parse_stylesheet(css, app=...)` | 使用应用实例解析 `$text-muted` 等主题变量 |
| `load_stylesheet()` | 优先读取包内 `app.tcss`，缺失时使用 `app.py` 的内联样式。打包产物不依赖 `CSS_PATH` |
| `bind()`、`bindings()` | 统一快捷键构造。四元组末项为 `False` 时隐藏页脚入口 |
| `set_text_selection(widget, False)` | 列表点击用于选中条目，禁用文本拖选 |
| `plain_text()`、`markup=False` | 外部文本按普通文本显示，避免方括号被解释为标记语法 |
| `notify(app, ..., severity=...)` | 统一通知参数与未挂载状态处理 |
| `ListView.Highlighted`、`ListView.Selected`、`list_view.index` | 读取列表高亮与选择状态 |
| `app_test(app, size=...)` | 统一无界面测试入口，显式指定终端尺寸 |
| `ButtonFlow` | 按标签宽度和可用空间计算列数，窄屏自动换行 |
<<< END U004458 >>>
<<< UNIT U004459 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:228-229 | ctx=实现约定 >>>
审阅次数：2
中文宽字符示例：`display_width("安装") == 4`，`truncate_cells("安装骰子模块", 7) == "安装骰…"`。
布局验证必须检查控件内容与可见边界，不能以渲染对象的字符串表示代替实际显示宽度。
<<< END U004459 >>>
<<< UNIT U004460 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:231-232 | ctx=实现约定 >>>
审阅次数：2
页面自有属性与方法不得与 Textual 基类成员同名，如 `_render`、`offset`、`refresh`、`display` 与
`styles`。渲染方法使用 `_render_fields` 等独立名称。定时轮询在 `self.display` 为 `False` 时跳过。
<<< END U004460 >>>
<<< UNIT U004461 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:234-235 | ctx=实现约定 >>>
审阅次数：2
数据源通过接口注入，渲染路径只读取缓存。模块默认缓存有效期为 30 秒，搜索、重绘、缩放与详情更新
不启动子进程。
<<< END U004461 >>>
<<< UNIT U004462 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:237-238 | ctx=实现约定 >>>
审阅次数：2
首次显示、显式刷新及包操作后按需重新读取。CLI JSON 规范化支持数组、记录映射与
包装对象，缺失可选字段使用默认值。安装与卸载通过 CLI 执行，异步读取进度并显示失败原因。
<<< END U004462 >>>
<<< UNIT U004463 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:240-240 | ctx=CLI 边界 >>>
审阅次数：2
### CLI 边界
<<< END U004463 >>>
<<< UNIT U004464 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:242-242 | ctx=CLI 边界 >>>
审阅次数：2
- 写入操作必须通过 `akaribot <子命令>` 子进程，参数由 `cli_process.cli_argv()` 与 `cli_env()` 构造。
<<< END U004464 >>>
<<< UNIT U004465 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:243-243 | ctx=CLI 边界 >>>
审阅次数：2
  界面使用 CLI 已有的 `--yes` 等参数传递确认结果，避免子进程等待交互输入。
<<< END U004465 >>>
<<< UNIT U004466 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:244-244 | ctx=CLI 边界 >>>
审阅次数：2
- 注册表、锁文件、日志文件及 `akaribot.toml` 等本机状态可在进程内读取。涉及 core 判断的配置
<<< END U004466 >>>
<<< UNIT U004467 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:245-245 | ctx=CLI 边界 >>>
审阅次数：2
  schema、数据项、模块清单与诊断必须通过子进程获取。
<<< END U004467 >>>
<<< UNIT U004468 | md-list | packages/akari-bot-cli/akaribot/cli/tui/README.md:246-247 | ctx=CLI 边界 >>>
审阅次数：2
- 新增界面能力必须有对应 CLI 命令。CLI 进程不得导入 core，子进程使用当前实例目录与 UTF-8 编码。
- 用 Nuitka 打包后的 CLI 直接接受子命令，普通 Python 环境使用模块入口。`AKARIBOT_CLI_BIN` 可覆盖 CLI 入口。
<<< END U004468 >>>
<<< UNIT U004469 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:249-249 | ctx=卸载期间的渲染 >>>
审阅次数：2
### 卸载期间的渲染
<<< END U004469 >>>
<<< UNIT U004470 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:251-253 | ctx=卸载期间的渲染 >>>
审阅次数：2
后台请求可能在页面卸载后完成。`guard_renders()` 保护同步的 `_render*`、`_sync*`、`_set_*` 与
`_paint*` 入口，页面不可用时跳过。执行期间发生卸载时，按卸载竞态处理。活动页面的 `NoMatches`
仍必须传递给 worker 与测试，不得隐藏选择器错误。
<<< END U004470 >>>
<<< UNIT U004471 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:255-256 | ctx=卸载期间的渲染 >>>
审阅次数：2
异步方法必须在访问控件前检查 `compat.mounted(self)`，包括可能发生卸载的 `await` 之后。
`mounted()` 同时区分应用退出、页面卸载和首次挂载过程，避免跳过依赖子控件的首次渲染。
<<< END U004471 >>>
<<< UNIT U004472 | md-heading | packages/akari-bot-cli/akaribot/cli/tui/README.md:258-258 | ctx=验证 >>>
审阅次数：2
## 验证
<<< END U004472 >>>
<<< UNIT U004473 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:260-261 | ctx=验证 >>>
审阅次数：2
当前依赖固定为 `textual==8.2.8`，自检会验证实际版本。自检涵盖资源、样式、宽字符、页面导航、
安装进度与品牌主题。
<<< END U004473 >>>
<<< UNIT U004474 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:263-264 | ctx=验证 >>>
审阅次数：2
无头基本检查覆盖默认概览页的控件与焦点，以及模块页的真实数据源读取。
产品检查失败或未执行时返回非零退出码，终端环境警告单独报告。
<<< END U004474 >>>
<<< UNIT U004475 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:279-280 | ctx=验证 >>>
审阅次数：2
页面专项测试位于 `packages/akari-bot-cli/tests/test_tui_*.py`，按更改范围选择运行。布局测试覆盖
80×24、60×20 等尺寸。真实终端的输入法、鼠标协议与网络重绘仍需在目标环境验证。
<<< END U004475 >>>
<<< UNIT U004476 | md-table | packages/akari-bot-cli/akaribot/cli/tui/README.md:282-288 | ctx=验证 >>>
审阅次数：2
| 环境 | 检查重点 |
| --- | --- |
| macOS Terminal.app / iTerm2 | 中文对齐、输入法、退格、鼠标点击与真彩显示 |
| Windows Terminal | ConPTY 宽字符、快捷键、路径与标准流编码 |
| Windows conhost | 鼠标转义序列、颜色降级与窄屏裁剪 |
| Linux / tmux / SSH | 快捷键冲突、鼠标协议与远程重绘。可用 `--no-mouse` 对照检查 |
| Nuitka onefile | 包内资源加载、启动表现及打包入口下的自检与子进程调用 |
<<< END U004476 >>>
<<< UNIT U004477 | md-paragraph | packages/akari-bot-cli/akaribot/cli/tui/README.md:290-291 | ctx=验证 >>>
审阅次数：2
深浅主题均由 `_compat` 注册。品牌色参考品牌资产，语义色按各自背景配置。自检核对激活主题
及 `$primary`。交互验证结果应注明终端、平台、版本与尺寸，不能用继承的环境变量代替运行证据。
<<< END U004477 >>>
<<< UNIT U004478 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/__init__.py:1-1 | ctx=<module> >>>
审阅次数：2
Textual 界面。
<<< END U004478 >>>
<<< UNIT U004479 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:163-163 >>>
审阅次数：2
# region 宽度计算（中文宽字符对齐）
<<< END U004479 >>>
<<< UNIT U004480 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:165-165 >>>
审阅次数：2
# 码点数量与终端列宽不同。宽度计算使用与 Textual 一致的 rich.cells。
<<< END U004480 >>>
<<< UNIT U004481 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:243-243 >>>
审阅次数：2
# region 包内资源与样式表
<<< END U004481 >>>
<<< UNIT U004482 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:245-245 >>>
审阅次数：2
# 冻结环境中的源文件路径不可用，样式表通过包内资源读取。资源缺失时使用内联样式。
<<< END U004482 >>>
<<< UNIT U004483 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:313-313 >>>
审阅次数：2
# region 品牌主题
<<< END U004483 >>>
<<< UNIT U004484 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:315-315 >>>
审阅次数：2
# 调色板取自品牌立绘 character_marked.png，并分别适配深色与浅色背景。
<<< END U004484 >>>
<<< UNIT U004485 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:384-384 >>>
审阅次数：2
# region 应用、键位与消息
<<< END U004485 >>>
<<< UNIT U004486 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:427-427 >>>
审阅次数：2
# 双击与键盘连续触发可能重复发起同一请求，防抖窗口用于防止确认框重复打开。
<<< END U004486 >>>
<<< UNIT U004487 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:437-437 >>>
审阅次数：2
# 允许测试调整防抖窗口，避免依赖固定的实际等待时间。
<<< END U004487 >>>
<<< UNIT U004488 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:519-519 >>>
审阅次数：2
# 任务注册可能延迟，需同时检查 worker 队列与页面忙碌状态。
<<< END U004488 >>>
<<< UNIT U004489 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:536-536 >>>
审阅次数：2
# 同步聚焦可避免切换页面时 Textual 将焦点分配给隐藏页面。
<<< END U004489 >>>
<<< UNIT U004490 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:539-539 >>>
审阅次数：2
# noqa: BLE001 - 未挂载或 Textual 内部签名变动时回退到常规路径
<<< END U004490 >>>
<<< UNIT U004491 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:552-552 >>>
审阅次数：2
# 空列表不可聚焦，需保留后续候选与页面容器作为回退目标。
<<< END U004491 >>>
<<< UNIT U004492 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:556-556 >>>
审阅次数：2
# noqa: BLE001 - 跳过尚未装配的候选控件
<<< END U004492 >>>
<<< UNIT U004493 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:588-588 >>>
审阅次数：2
# noqa: BLE001 - 通知失败不应中断界面操作
<<< END U004493 >>>
<<< UNIT U004494 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:833-833 >>>
审阅次数：2
# 回车提交对话框。单击只移动高亮，避免误点直接执行。
<<< END U004494 >>>
<<< UNIT U004495 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:969-969 >>>
审阅次数：2
# 列表边框占两行。
<<< END U004495 >>>
<<< UNIT U004496 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:975-975 >>>
审阅次数：2
# 输入框占三行。错误提示在窄屏下可能折行，按实际内容计算高度。
<<< END U004496 >>>
<<< UNIT U004497 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:991-991 >>>
审阅次数：2
# 单击选项后回到输入框继续填写。
<<< END U004497 >>>
<<< UNIT U004498 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1108-1108 >>>
审阅次数：2
# Textual 先卸载子控件，父控件的 is_mounted 可能尚未更新。
<<< END U004498 >>>
<<< UNIT U004499 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1159-1159 >>>
审阅次数：2
# 首次 on_mount 需要执行渲染，卸载检查仅适用于已完成挂载的页面。
<<< END U004499 >>>
<<< UNIT U004500 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1171-1171 >>>
审阅次数：2
# 实例属性不参与描述符绑定，闭包必须保留页面对象与已绑定方法。
<<< END U004500 >>>
<<< UNIT U004501 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1182-1182 >>>
审阅次数：2
# 检查后仍可能发生卸载，仅在控件不可用时忽略此竞态产生的异常。
<<< END U004501 >>>
<<< UNIT U004502 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1231-1231 >>>
审阅次数：2
# 重新排列时保留按钮实例，避免丢失标签、禁用状态或焦点。
<<< END U004502 >>>
<<< UNIT U004503 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1262-1262 >>>
审阅次数：2
# 网格按列对齐，必须复核每列最大宽度之和，避免长短标签混排时溢出。
<<< END U004503 >>>
<<< UNIT U004504 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1278-1278 >>>
审阅次数：2
# 优先保留语义分组。单组超宽时允许在组内换行。
<<< END U004504 >>>
<<< UNIT U004505 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1300-1300 >>>
审阅次数：2
# 状态切换可能修改标签或隐藏按钮，宽度应以当前可见内容为准。
<<< END U004505 >>>
<<< UNIT U004506 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1462-1462 >>>
审阅次数：2
# region 运行、鼠标与进度
<<< END U004506 >>>
<<< UNIT U004507 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1505-1505 >>>
审阅次数：2
# 原始异常可能保存在 WorkerFailed.error 或 __cause__ 中，必须检查两种来源。
<<< END U004507 >>>
<<< UNIT U004508 | py-comment | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1529-1529 >>>
审阅次数：2
# region 终端能力（自检报告用）
<<< END U004508 >>>
<<< UNIT U004509 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:148-148 | ctx=textual_version >>>
审阅次数：2
返回运行时 Textual 版本号。
<<< END U004509 >>>
<<< UNIT U004510 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:169-169 | ctx=cell_width >>>
审阅次数：2
返回单个字符占用的终端列数。
<<< END U004510 >>>
<<< UNIT U004511 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:174-174 | ctx=display_width >>>
审阅次数：2
返回字符串占用的终端列数，中文与 emoji 按 2 列计算。
<<< END U004511 >>>
<<< UNIT U004512 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:219-219 | ctx=fit_cells >>>
审阅次数：2
先按列宽截断再补齐，用于定宽列。
<<< END U004512 >>>
<<< UNIT U004513 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:224-224 | ctx=column_width >>>
审阅次数：2
返回一组文本的最大显示宽度，用于确定列宽。
<<< END U004513 >>>
<<< UNIT U004514 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:268-268 | ctx=resource_inventory >>>
审阅次数：2
列出包内可读资源名称，供自检报告冻结产物的资源可达性。
<<< END U004514 >>>
<<< UNIT U004515 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:400-400 | ctx=key_display >>>
审阅次数：2
返回快捷键的显示写法，与页脚一致（``ctrl+d`` 写作 ``^d``）。
<<< END U004515 >>>
<<< UNIT U004516 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:410-410 | ctx=key_hint >>>
审阅次数：2
在按钮文字后附加快捷键，如“安装 i”。
<<< END U004516 >>>
<<< UNIT U004517 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:459-459 | ctx=PendingConfirm.reset >>>
审阅次数：2
清除防抖记录。
<<< END U004517 >>>
<<< UNIT U004518 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:506-506 | ctx=highlighted_index >>>
审阅次数：2
返回当前高亮项索引，无高亮项时返回 ``None``。
<<< END U004518 >>>
<<< UNIT U004519 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:577-577 | ctx=escape_markup >>>
审阅次数：2
转义文本中的标记字符，仅在确实需要拼接标记时使用。
<<< END U004519 >>>
<<< UNIT U004520 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:582-582 | ctx=notify >>>
审阅次数：2
显示通知。未挂载或不支持通知时返回。
<<< END U004520 >>>
<<< UNIT U004521 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:593-593 | ctx=push_screen >>>
审阅次数：2
打开页面，并通过可选回调传递关闭结果。
<<< END U004521 >>>
<<< UNIT U004522 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:659-659 | ctx=TextPromptScreen.compose >>>
审阅次数：2
装配输入框与两个按钮。
<<< END U004522 >>>
<<< UNIT U004523 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:673-673 | ctx=TextPromptScreen.on_mount >>>
审阅次数：2
打开即聚焦输入框。
<<< END U004523 >>>
<<< UNIT U004524 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:681-681 | ctx=TextPromptScreen.on_input_submitted >>>
审阅次数：2
回车提交。
<<< END U004524 >>>
<<< UNIT U004525 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:685-685 | ctx=TextPromptScreen.on_button_pressed >>>
审阅次数：2
按钮提交或取消。
<<< END U004525 >>>
<<< UNIT U004526 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:692-692 | ctx=TextPromptScreen.key_escape >>>
审阅次数：2
Esc 取消。
<<< END U004526 >>>
<<< UNIT U004527 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:711-711 | ctx=ask_text >>>
审阅次数：2
打开单行输入框，通过回调返回输入值。取消时返回 ``None``。
<<< END U004527 >>>
<<< UNIT U004528 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:777-777 | ctx=ChoiceScreen.compose >>>
审阅次数：2
装配标题、说明与每个选项一个按钮。
<<< END U004528 >>>
<<< UNIT U004529 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:793-793 | ctx=ChoiceScreen.on_mount >>>
审阅次数：2
聚焦首个选项。无选项时聚焦取消按钮。
<<< END U004529 >>>
<<< UNIT U004530 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:804-804 | ctx=ChoiceScreen.on_button_pressed >>>
审阅次数：2
返回选项值。取消按钮返回 ``None``。
<<< END U004530 >>>
<<< UNIT U004531 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:815-815 | ctx=ChoiceScreen.key_escape >>>
审阅次数：2
Esc 取消。
<<< END U004531 >>>
<<< UNIT U004532 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:828-828 | ctx=ask_choice >>>
审阅次数：2
弹出多选一的模态框，把选中的取值交给回调。取消时为 ``None``。
<<< END U004532 >>>
<<< UNIT U004533 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:837-837 | ctx=_PickList.action_submit_pick >>>
审阅次数：2
提交所在对话框的键位动作。
<<< END U004533 >>>
<<< UNIT U004534 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:934-934 | ctx=PickTextScreen.compose >>>
审阅次数：2
装配说明、选项列表、输入框、错误提示与两个按钮。
<<< END U004534 >>>
<<< UNIT U004535 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:957-957 | ctx=PickTextScreen.on_mount >>>
审阅次数：2
限定列表高度，有输入框时聚焦输入框，否则聚焦列表。
<<< END U004535 >>>
<<< UNIT U004536 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:982-982 | ctx=PickTextScreen.action_move_pick >>>
审阅次数：2
在输入框或按钮上移动列表高亮的键位动作。
<<< END U004536 >>>
<<< UNIT U004537 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:996-996 | ctx=PickTextScreen.on_input_changed >>>
审阅次数：2
改动输入时清除上次的错误提示。
<<< END U004537 >>>
<<< UNIT U004538 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1003-1003 | ctx=PickTextScreen.on_input_submitted >>>
审阅次数：2
回车提交。
<<< END U004538 >>>
<<< UNIT U004539 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1007-1007 | ctx=PickTextScreen.on_button_pressed >>>
审阅次数：2
按钮提交或取消。
<<< END U004539 >>>
<<< UNIT U004540 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1014-1014 | ctx=PickTextScreen.key_escape >>>
审阅次数：2
Esc 取消。
<<< END U004540 >>>
<<< UNIT U004541 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1018-1018 | ctx=PickTextScreen.submit >>>
审阅次数：2
校验并提交高亮项与输入文本。校验失败时显示原因且不关闭。
<<< END U004541 >>>
<<< UNIT U004542 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1046-1046 | ctx=ask_pick_text >>>
审阅次数：2
弹出“选一项并输入文本”的模态框，把 ``(取值, 文本)`` 交给回调。取消时为 ``None``。
<<< END U004542 >>>
<<< UNIT U004543 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1071-1071 | ctx=ask_pick >>>
审阅次数：2
弹出列表单选的模态框，把选中的取值交给回调。取消时为 ``None``。
<<< END U004543 >>>
<<< UNIT U004544 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1120-1120 | ctx=RenderGuard >>>
审阅次数：2
记录页面不可用时跳过的渲染次数及最近一次方法名。
<<< END U004544 >>>
<<< UNIT U004545 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1128-1128 | ctx=RenderGuard.skipped_renders >>>
审阅次数：2
因页面不可用而跳过的渲染次数。
<<< END U004545 >>>
<<< UNIT U004546 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1133-1133 | ctx=RenderGuard.last_skipped_method >>>
审阅次数：2
最近一次因页面不可用而跳过的渲染方法名，未跳过时为空字符串。
<<< END U004546 >>>
<<< UNIT U004547 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1200-1200 | ctx=button_width >>>
审阅次数：2
返回按钮的自然列宽，包括左右内边距。
<<< END U004547 >>>
<<< UNIT U004548 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1236-1236 | ctx=ButtonFlow.compose >>>
审阅次数：2
按声明顺序创建按钮。
<<< END U004548 >>>
<<< UNIT U004549 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1241-1241 | ctx=ButtonFlow.on_mount >>>
审阅次数：2
首次排布前计算一次列数。
<<< END U004549 >>>
<<< UNIT U004550 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1245-1245 | ctx=ButtonFlow.on_resize >>>
审阅次数：2
宽度变化后重新计算列数。
<<< END U004550 >>>
<<< UNIT U004551 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1392-1392 | ctx=HelpScreen.compose >>>
审阅次数：2
装配标题、说明与键位清单。
<<< END U004551 >>>
<<< UNIT U004552 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1410-1410 | ctx=HelpScreen.on_mount >>>
审阅次数：2
打开即聚焦关闭按钮。
<<< END U004552 >>>
<<< UNIT U004553 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1414-1414 | ctx=HelpScreen.on_button_pressed >>>
审阅次数：2
点击关闭按钮时关闭。
<<< END U004553 >>>
<<< UNIT U004554 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1419-1419 | ctx=HelpScreen.key_escape >>>
审阅次数：2
Esc 关闭。
<<< END U004554 >>>
<<< UNIT U004555 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1423-1423 | ctx=HelpScreen.key_q >>>
审阅次数：2
q 关闭。
<<< END U004555 >>>
<<< UNIT U004556 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1427-1427 | ctx=HelpScreen.key_question_mark >>>
审阅次数：2
再按一次 ? 关闭。
<<< END U004556 >>>
<<< UNIT U004557 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1444-1444 | ctx=show_help >>>
审阅次数：2
打开快捷键帮助。
<<< END U004557 >>>
<<< UNIT U004558 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1449-1449 | ctx=pop_screen >>>
审阅次数：2
弹出当前页面。
<<< END U004558 >>>
<<< UNIT U004559 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1454-1454 | ctx=widget_cells >>>
审阅次数：2
返回控件宽度和高度，单位分别为终端列和行。
<<< END U004559 >>>
<<< UNIT U004560 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1466-1466 | ctx=is_interactive_terminal >>>
审阅次数：2
判断标准输入输出是否连接交互终端。
<<< END U004560 >>>
<<< UNIT U004561 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1522-1522 | ctx=progress_reset >>>
审阅次数：2
把进度条归零。
<<< END U004561 >>>
<<< UNIT U004562 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1533-1533 | ctx=TerminalCapability >>>
审阅次数：2
终端能力的检测结果。
<<< END U004562 >>>
<<< UNIT U004563 | py-docstring | packages/akari-bot-cli/akaribot/cli/tui/_compat.py:1546-1546 | ctx=terminal_capabilities >>>
审阅次数：2
读取当前终端的环境信息及可用能力。
<<< END U004563 >>>
