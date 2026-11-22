# 全仓可读文本审核稿 · 第 12 册 / 共 20 册

覆盖 U007871–U008593，27 个文件、723 个单元、33,699 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-core/akaribot/core/entrypoints/run.py` | 42 | U007871–U007912 | 3,036 |
| `packages/akari-bot-core/akaribot/core/loader.py` | 65 | U007913–U007977 | 3,638 |
| `packages/akari-bot-core/akaribot/core/locales/zh_cn.json` | 255 | U007978–U008232 | 5,661 |
| `packages/akari-bot-core/akaribot/core/logger.py` | 3 | U008233–U008235 | 71 |
| `packages/akari-bot-core/akaribot/core/module_runtime.py` | 14 | U008236–U008249 | 122 |
| `packages/akari-bot-core/akaribot/core/paths.py` | 6 | U008250–U008255 | 315 |
| `packages/akari-bot-core/akaribot/core/queue/README.md` | 141 | U008256–U008396 | 12,584 |
| `packages/akari-bot-core/akaribot/core/queue/backend.py` | 2 | U008397–U008398 | 47 |
| `packages/akari-bot-core/akaribot/core/queue/base.py` | 12 | U008399–U008410 | 649 |
| `packages/akari-bot-core/akaribot/core/queue/client.py` | 4 | U008411–U008414 | 107 |
| `packages/akari-bot-core/akaribot/core/queue/contracts.py` | 11 | U008415–U008425 | 332 |
| `packages/akari-bot-core/akaribot/core/queue/database.py` | 8 | U008426–U008433 | 253 |
| `packages/akari-bot-core/akaribot/core/queue/diagnostics.py` | 17 | U008434–U008450 | 504 |
| `packages/akari-bot-core/akaribot/core/queue/errors.py` | 1 | U008451–U008451 | 88 |
| `packages/akari-bot-core/akaribot/core/queue/memory.py` | 2 | U008452–U008453 | 50 |
| `packages/akari-bot-core/akaribot/core/queue/peer.py` | 4 | U008454–U008457 | 121 |
| `packages/akari-bot-core/akaribot/core/queue/server.py` | 15 | U008458–U008472 | 649 |
| `packages/akari-bot-core/akaribot/core/queue/transport.py` | 3 | U008473–U008475 | 85 |
| `packages/akari-bot-core/akaribot/core/queue/websocket.py` | 4 | U008476–U008479 | 180 |
| `packages/akari-bot-core/akaribot/core/registry.py` | 37 | U008480–U008516 | 2,464 |
| `packages/akari-bot-core/akaribot/core/scheduler.py` | 19 | U008517–U008535 | 718 |
| `packages/akari-bot-core/akaribot/core/scripts/convert_database.py` | 37 | U008536–U008572 | 845 |
| `packages/akari-bot-core/akaribot/core/scripts/migrate_assets_to_data.py` | 3 | U008573–U008575 | 445 |
| `packages/akari-bot-core/akaribot/core/server/__init__.py` | 1 | U008576–U008576 | 9 |
| `packages/akari-bot-core/akaribot/core/server/background_tasks.py` | 5 | U008577–U008581 | 175 |
| `packages/akari-bot-core/akaribot/core/server/init.py` | 7 | U008582–U008588 | 418 |
| `packages/akari-bot-core/akaribot/core/server/lifecycle.py` | 5 | U008589–U008593 | 133 |

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
<<< UNIT U007871 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:41-41 >>>
# 仓库根目录环境变量。取值须与 akaribot.testing.runner.REPO_ROOT_ENV 一致，根目录的 tester.py 会设置它。
<<< END U007871 >>>
<<< UNIT U007872 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:44-44 >>>
# 实例级锁文件名。须与 akaribot.cli.instance.LOCK_FILENAME 一致，CLI 的 is_running() 据此探测。
<<< END U007872 >>>
<<< UNIT U007873 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:51-53 >>>
# 本模块位于包内，按自身位置反推仓库根目录只会落到 site-packages，故采用与
# :mod:`akaribot.testing.runner` 相同的判定规则，优先 ``AKARI_REPO_ROOT``，否则取 ``Paths.tests``
# 的父目录，并以 ``packages/`` 是否存在复核，避免 ``AKARI_TESTS_PATH`` 指向别处时误判。
<<< END U007873 >>>
<<< UNIT U007874 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:62-63 >>>
# 判定规则只看目录是否存在，不依赖已安装包的 metadata，仓库根目录一并保留，使 ``tester`` 等根目录脚本
# 在子进程中仍可导入。仓库根目录不可知时返回空列表，此时 ``akaribot`` 由已安装包提供。
<<< END U007874 >>>
<<< UNIT U007875 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:71-72 >>>
# 显式传入实例根目录下的 .env，因为不给路径时 python-dotenv 从本模块所在目录向上查找，包内位置与
# 仓库根目录、实例根目录都不对应。AKARI_INSTANCE_DIR 未设置时实例根目录即进程 cwd。
<<< END U007875 >>>
<<< UNIT U007876 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:75-75 >>>
# 空列表时不设置，因为空字符串会引入一条指向当前目录的搜索路径，与安装形态的预期相反。
<<< END U007876 >>>
<<< UNIT U007877 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:82-83 >>>
# 完整交互式初始化并入 CLI（阶段 5），此处仅保留语言选择。无终端时（容器、CI）
# 直接采用默认语言，不阻塞在 input() 上。
<<< END U007877 >>>
<<< UNIT U007878 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:99-100 >>>
# 结构只含 default_locale 与 config_version，这两个顶层键不属于任何模板，扫描补不出来。
# 注释先以 i18n 标记写入磁盘，待 pre_init() 接上 i18n 快照后由扫描按所选语言翻译。
<<< END U007878 >>>
<<< UNIT U007879 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:181-181 >>>
# 实例级锁文件句柄。锁随文件对象关闭而释放，句柄须在进程存活期间一直被引用。
<<< END U007879 >>>
<<< UNIT U007880 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:301-302 >>>
# 监听地址字段。web 的 web_port 与 onebot / milky 的 qq_host 最终都占用一个 TCP 端口，
# 故统一解析出 (主机, 端口) 后比对，web 与 onebot 撞同一个端口同样是致命的。
<<< END U007880 >>>
<<< UNIT U007881 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:305-306 >>>
# web_host 未指定时的绑定地址，与 WebConfig 声明的默认值一致。守护进程不能向 CFGManager.get
# 传默认值，否则会触发写入，而守护进程是只读的。
<<< END U007881 >>>
<<< UNIT U007882 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:338-339 >>>
# 通配地址与任意主机冲突，其余要求主机相同。``localhost`` 与 ``127.0.0.1`` 视为不同，
# 宁可漏报也不误报，因为误报会让本来可用的部署无法启动。
<<< END U007882 >>>
<<< UNIT U007883 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:345-345 >>>
# Milky 的 qq_host 是远端服务地址，不占用本机监听端口。
<<< END U007883 >>>
<<< UNIT U007884 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:367-368 >>>
# 登录信息多数放在密钥表，也有放在普通表的（如 ``qq_bot_appid``），两处都试一次。
# 未填写的占位符由 ``CFGManager.get`` 归一为 None，不会被误判为重复。
<<< END U007884 >>>
<<< UNIT U007885 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:430-431 >>>
# onebot 与 milky 都叫 "QQ"。这不是本功能引入的，但两者的 JobQueue 服务名与启动
# 失败计数会因此合并，必须留下痕迹。
<<< END U007885 >>>
<<< UNIT U007886 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:448-448 >>>
# 目录创建集中在此，导入 core.constants 不再产生副作用。
<<< END U007886 >>>
<<< UNIT U007887 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:463-464 >>>
# CoreConfig 的导入须留在函数内，因为 multiprocessing 以 spawn / forkserver 启动子进程时
# 会以 __mp_main__ 重新导入主模块，置于顶层将使每个子进程再次触发配置模板的生成。
<<< END U007887 >>>
<<< UNIT U007888 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:473-474 >>>
# 配置的生成集中在此完成，子进程一律只读，此处遗漏的键将在子进程读取时抛出异常，
# 因此任何模板加载失败均须中止启动，而非延至运行期才暴露。
<<< END U007888 >>>
<<< UNIT U007889 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:537-537 >>>
# pre_init 是唯一被允许写入配置的进程，须清除 RestartBot 重启循环中残留的只读标记
<<< END U007889 >>>
<<< UNIT U007890 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:572-572 >>>
# instance_id 必须在导入适配器之前设置，因为 akaribot.adapters.<x>.info 在导入期依它生成 client_name。
<<< END U007890 >>>
<<< UNIT U007891 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:581-581 >>>
# 平台展示名供会话构造使用，多实例下 client_name 带实例后缀，平台名不带。
<<< END U007891 >>>
<<< UNIT U007892 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:589-589 >>>
# 退出码 78（EX_CONFIG）表示无需重启，因为入口缺失是部署问题，重试无济于事。
<<< END U007892 >>>
<<< UNIT U007893 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:602-602 >>>
# Server 依赖树（尤其 WebRender）只应由 Server 子进程加载，守护进程不需要保留一份。
<<< END U007893 >>>
<<< UNIT U007894 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:616-617 >>>
# 二进制封装下 argv[0] 是可执行文件自身。python bot.py 与 python -m akaribot.core.entrypoints.run
# 两种解释器形态的 argv[0] 都是脚本文件路径，故判断依据不变。
<<< END U007894 >>>
<<< UNIT U007895 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:624-625 >>>
# 自此起 spawn 出的子进程一律只读，配置的生成已在 pre_init 中完成。
# 须在任何 mp.Process 之前设置，spawn 会继承环境。restart_bot_process() 后续重启子进程时同样适用。
<<< END U007895 >>>
<<< UNIT U007896 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:629-629 >>>
# CONFIG_READONLY_ENV 必须先于 core.config 的首次导入设置。后者会在导入期执行配置版本迁移。
<<< END U007896 >>>
<<< UNIT U007897 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:633-634 >>>
# 守护进程与 Hub 不是 JobQueue 节点，Server 无从 Registry 获知其 PID。此处随 Process
# 参数传递而非环境变量，因为 forkserver 于首个子进程启动时快照环境，后续改动不再生效。
<<< END U007897 >>>
<<< UNIT U007898 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:699-700 >>>
# 误配的实例必须在任何适配器进程启动之前拦截，否则两个进程抢同一端口或同一账号之后，
# 症状是随机的消息丢失与重复，从日志无法回溯到配置。
<<< END U007898 >>>
<<< UNIT U007899 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:710-711 >>>
# client_name 不保证跨适配器唯一（onebot 与 milky 同为 "QQ"），重启映射因此记录在进程
# 对象上，不按名字反向查找，以免重启时认错实例。
<<< END U007899 >>>
<<< UNIT U007900 | py-inline-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:751-751 >>>
# 已明确没有必要重启的进程异常退出码
<<< END U007900 >>>
<<< UNIT U007901 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:757-757 >>>
# terminate_process() 会 close() 该进程对象，close 之后读取属性会抛出异常，故先取出实例记录。
<<< END U007901 >>>
<<< UNIT U007902 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:792-792 >>>
# 先停止平台入口，再停止 Server。WebSocket Hub 最后退出，以便其他进程完成关闭信号与响应。
<<< END U007902 >>>
<<< UNIT U007903 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:828-829 >>>
# 记录含进程号与启动时间，供控制器（CLI）定位并停止本进程。获取锁失败的进程不会走到这里，
# 因此文件内容始终属于当前持锁者。
<<< END U007903 >>>
<<< UNIT U007904 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:833-833 >>>
# msvcrt 对 byte 0 加 mandatory lock。通过底层二进制流写入并跳过锁区。
<<< END U007904 >>>
<<< UNIT U007905 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:852-852 >>>
# 信号处理器在主线程的两个字节码之间执行，异常经 asyncio.run() 向外传播，与 Ctrl+C 走同一条路径。
<<< END U007905 >>>
<<< UNIT U007906 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:869-870 >>>
# 不截断打开，确保获取锁失败的第二个进程不得抹掉持有者写下的进程记录。锁的语义仍由 flock / msvcrt
# 确定，文件内容只用于让控制器定位进程。
<<< END U007906 >>>
<<< UNIT U007907 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:888-889 >>>
# SIGTERM 默认直接终止进程，适配器与 Server 会变成孤儿进程。转成 KeyboardInterrupt 走
# 与 Ctrl+C 相同的收拢路径。
<<< END U007907 >>>
<<< UNIT U007908 | py-comment | packages/akari-bot-core/akaribot/core/entrypoints/run.py:915-915 >>>
# 配置冲突等守护进程错误须保留退出码，供管理器判断启动结果。
<<< END U007908 >>>
<<< UNIT U007909 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/run.py:137-137 | ctx=init_daemon_logger >>>
仅为守护进程与短生命周期 pre-init 进程安装日志处理器。
<<< END U007909 >>>
<<< UNIT U007910 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/run.py:186-186 | ctx=warn_if_database_jobqueue_uses_sqlite >>>
数据库队列与 SQLite 组合使用时输出一次非阻断警告。
<<< END U007910 >>>
<<< UNIT U007911 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/run.py:609-609 | ctx=jobqueue_hub_go >>>
在独立子进程中运行内置 WebSocket JobQueue Hub。
<<< END U007911 >>>
<<< UNIT U007912 | py-docstring | packages/akari-bot-core/akaribot/core/entrypoints/run.py:775-775 | ctx=terminate_process >>>
优先请求进程自行清理，超时后再逐级终止。
<<< END U007912 >>>
<<< UNIT U007913 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:46-47 >>>
# 不兼容 core API 的包与依赖不满足的包都在发现阶段一并剔除（core.registry.PackageRegistry.discover）。
# 依赖校验必须与 API 校验同源，才能把“依赖被 API 门槛拒绝的包”一起剔除，避免其导入期注册的模块进入索引。
<<< END U007913 >>>
<<< UNIT U007914 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:49-49 >>>
# 按声明依赖的拓扑序导入，让被依赖的包先完成注册，依赖它的包才能在导入期取用其公开接口。
<<< END U007914 >>>
<<< UNIT U007915 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:68-69 >>>
# 只忽略配置模块本身不存在。配置文件内部缺少依赖同样表现为
# ModuleNotFoundError，若一概忽略会让模块在缺少必要配置时处于部分加载状态。
<<< END U007915 >>>
<<< UNIT U007916 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:75-76 >>>
# module() 与各组件装饰器都在导入期记录。若文件在记录一部分内容后
# 才抛出异常，必须撤销该包本轮产生的注册，否则报错模块仍可能接收命令。
<<< END U007916 >>>
<<< UNIT U007917 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:88-88 >>>
# 一次取回全部状态，避免逐模块查询退化成 N 次往返，在模块多或主数据库在远端时开销可观
<<< END U007917 >>>
<<< UNIT U007918 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:108-108 >>>
# 不兼容包不参与加载，其成因在此与加载失败并列，供启动提示与 ~module list 展示。
<<< END U007918 >>>
<<< UNIT U007919 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:126-126 >>>
# 带名称的 hook 与 parser hook 统一建立订阅索引，复用共享执行基础的资格与版本机制。
<<< END U007919 >>>
<<< UNIT U007920 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:129-129 >>>
# parser 入口订阅映射为 HookPoint -> 已排序订阅列表，与带名称的 hook 分索引
<<< END U007920 >>>
<<< UNIT U007921 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:138-138 >>>
# 已告警过的“包对”，避免每次重建依赖图都重复告警同一处未声明依赖。
<<< END U007921 >>>
<<< UNIT U007922 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:211-211 >>>
# default 只影响 Python 层赋值，不参与表结构。
<<< END U007922 >>>
<<< UNIT U007923 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:412-412 >>>
# 逐 handler 隔离，单个订阅失败不影响其他订阅，也不向调用方泄漏业务异常
<<< END U007923 >>>
<<< UNIT U007924 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:482-483 >>>
# 按段比较而非字符串前缀，``akaribot.modules_extra`` 与 ``akaribot.modules`` 仅首段相同，
# 前者不是后者的成员包，不该被归约进来。命名空间本身也在此命中，由调用方判断它是否成包。
<<< END U007924 >>>
<<< UNIT U007925 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:496-497 >>>
# 纯字符串归约且不校验该包是否已注册，调用方用它构建依赖图，图上的边会在
# 与已注册包取交集时被过滤。校验注册状态由 :meth:`return_py_module` 负责。
<<< END U007925 >>>
<<< UNIT U007926 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:504-504 >>>
# 命名空间只是容器（akaribot.modules 无 __init__.py），不是可注册的包。
<<< END U007926 >>>
<<< UNIT U007927 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:510-512 >>>
# 用于识别 ``from akaribot.modules import x`` 这类裸包导入，其 AST 只给出
# ``akaribot.modules``，子模块名在 ``node.names`` 中，需展开成 ``akaribot.modules.x``
# 后才可能匹配到具体包。
<<< END U007927 >>>
<<< UNIT U007928 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:545-545 >>>
# 裸包导入的 AST 只给出命名空间或其子路径，子模块名在 node.names 中。
<<< END U007928 >>>
<<< UNIT U007929 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:583-584 >>>
# 获取已注册条目的声明依赖。目录扫描的包没有 metadata，
# 返回空集，其依赖全部落到 :meth:`_scan_package_dependencies` 补充探测。
<<< END U007929 >>>
<<< UNIT U007930 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:592-593 >>>
# AST 扫出而 metadata 未声明的耦合仍然计入并告警，静默忽略会让热重载漏掉本应重载
# 的包，比多一条告警危险。
<<< END U007930 >>>
<<< UNIT U007931 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:605-605 >>>
# 热重载每次都会重建依赖图，逐次重复告警会淹没日志，故按“包对”在进程内去重。
<<< END U007931 >>>
<<< UNIT U007932 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:618-619 >>>
# 图源为“声明的依赖图 ∪ AST 扫描结果”。成环的包在 discover() 阶段已被拒绝注册，
# 能走到此处的图必然无环，闭包内的遇环跳过只作防御。
<<< END U007932 >>>
<<< UNIT U007933 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:682-683 >>>
# 子模块按 sys.modules 顺序重载，扩展兄弟模块的装饰器可能先于目标模块执行。
# 等目标 module() 重新注册后再绑定，避免命令、Hook 或 Event 静默消失。
<<< END U007933 >>>
<<< UNIT U007934 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:706-707 >>>
# 过滤结果取决于四段判定条件，缓存键必须全部带上，因为只按 target_from 构造缓存键会让同一场景
# 配上不同客户端名时取到旧结果，漏掉平台两段则会让一个实例命中另一个实例的缓存。
<<< END U007934 >>>
<<< UNIT U007935 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:743-743 >>>
# Scheduler 注册异常或取消不能留下“数据库显示启用、实际无 Job”状态。
<<< END U007935 >>>
<<< UNIT U007936 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:767-768 >>>
# 与 reload 保持相同顺序，先处理完 Queue handler 中的任务，再进入 Scheduler 维护。
# 非独占 Queue 窗口仍允许轮询器回收模块清理产生的响应。
<<< END U007936 >>>
<<< UNIT U007937 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:800-801 >>>
# 此处不能等待另一个重载释放锁，双方会形成死锁。
# 忙碌时直接失败，保证第二次请求不会改动模块注册表。
<<< END U007937 >>>
<<< UNIT U007938 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:807-809 >>>
# 先处理完 Queue handler 中的任务，再进入 Scheduler 维护。反序会形成永久互锁——
# 执行 load/unload 的 handler 阻塞在 Scheduler 锁上，而 reload 在等它收尾。
# Scheduler 窗口仍须覆盖 importlib.reload()，旧函数的 __globals__ 指向原地更新的模块字典。
<<< END U007938 >>>
<<< UNIT U007939 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:813-814 >>>
# 长时间保持非独占窗口，停止接收新 action，但让轮询器继续回收
# 响应、续租与执行模块清理 RPC。数据库替换会在内部再嵌套独占窗口。
<<< END U007939 >>>
<<< UNIT U007940 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:862-863 >>>
# 恢复旧版本注册后必须重建订阅索引，否则旧订阅全部失效。
# 重建时 staging 尚未撤销，需在 abort_reload 之后再次重建。
<<< END U007940 >>>
<<< UNIT U007941 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:961-962 >>>
# 在首个会修改持久化状态的 await 之前设置。协程可能恰好在 delete()
# 提交后收到取消。若等 await 返回才设置，取消路径会误判为无需回滚。
<<< END U007941 >>>
<<< UNIT U007942 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:970-971 >>>
# Scheduler 当前仍处于维护窗口，先把新 Job 准备好但不允许执行。数据库
# 重载失败时可连同 ModuleStatus 与注册表一起恢复旧 Job。
<<< END U007942 >>>
<<< UNIT U007943 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:975-976 >>>
# 先构建可独立失败的数据库 context。旧 context 和旧 runtime 此时都
# 保持可用。只有全部校验成功后才进入不可逆 commit。
<<< END U007943 >>>
<<< UNIT U007944 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:995-996 >>>
# commit 是版本切换的不可逆边界。取消可以中断构建阶段，但不能在
# runtime 已切换、旧版本已停止后再回滚注册表和数据库。
<<< END U007944 >>>
<<< UNIT U007945 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1019-1020 >>>
# 旧 runtime 已停止，此时短时独占 Queue 轮询并切换数据库 context，
# 避免轮询器在旧连接关闭过程中仍发出查询。
<<< END U007945 >>>
<<< UNIT U007946 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1052-1053 >>>
# Queue action 超时或 Server 关闭都会取消热重载。取消不能被转换成普通
# 失败，但在继续传播前必须恢复已删改的持久状态与内存注册表。
<<< END U007946 >>>
<<< UNIT U007947 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1124-1125 >>>
# PackageRegistry 只有重建缓存（discover）的入口，没有回退点。安装失败后 CLI 会卸载该包，
# 索引若停留在含该包的状态，下一次数据库重挂会去导入已经不存在的模型模块。
<<< END U007947 >>>
<<< UNIT U007948 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1141-1141 >>>
# 卸载 RPC 先于 uv pip uninstall 执行，重新运行 discover() 依旧会看到该包，故直接改写索引缓存。
<<< END U007948 >>>
<<< UNIT U007949 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1149-1150 >>>
# 只读进程只认启动时列出的文件，新表必须经 load() 重新枚举才会出现。此处失败不阻断安装，
# 导入期读取新配置项时会触发只读检查报错。
<<< END U007949 >>>
<<< UNIT U007950 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1187-1187 >>>
# 与 reload_module 同策略，忙碌时直接失败，不把等待锁的时间算进 RPC 超时。
<<< END U007950 >>>
<<< UNIT U007951 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1193-1193 >>>
# 先处理完 Queue handler 中的任务，再进入 Scheduler 维护。数据库替换会在内部再嵌套独占窗口。
<<< END U007951 >>>
<<< UNIT U007952 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1227-1227 >>>
# 已激活的 context 不会被关闭，数据库切换是本次安装不可逆的一步。
<<< END U007952 >>>
<<< UNIT U007953 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1231-1232 >>>
# 新装的 entry point 只有重新运行发现才会出现。requires_core_api 与声明依赖的校验已内建于
# discover()，被它剔除的包在此以拒绝原因报出。
<<< END U007953 >>>
<<< UNIT U007954 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1245-1245 >>>
# 新包的配置由 CLI 在可写子进程里补充，本进程须在导入之前重新读取配置目录。
<<< END U007954 >>>
<<< UNIT U007955 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1254-1254 >>>
# discover() 已把新包并入索引，故新 context 覆盖“现有 + 新包”的模型。
<<< END U007955 >>>
<<< UNIT U007956 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1259-1259 >>>
# init_modules 以传入清单为准删除缺失行，故带上全部已注册模块，而不只是新增名。
<<< END U007956 >>>
<<< UNIT U007957 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1299-1299 >>>
# 与 reload_module 同策略，忙碌时直接失败，不把等待锁的时间算进 RPC 超时。
<<< END U007957 >>>
<<< UNIT U007958 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1312-1312 >>>
# 拆除是单向操作，单个模块停用失败不应留下半拆状态，继续走完索引与 context 清理。
<<< END U007958 >>>
<<< UNIT U007959 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1315-1316 >>>
# 卸载 RPC 先于 uv pip uninstall，重新运行 discover() 仍会看到该包，
# 故直接把包摘出发现层索引，下面的数据库重挂才不会带上它的模型。
<<< END U007959 >>>
<<< UNIT U007960 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1327-1327 >>>
# 与启动期 init_modules 对缺失模块的清理同向，残留的 load=False 会误停重新安装后的模块。
<<< END U007960 >>>
<<< UNIT U007961 | py-comment | packages/akari-bot-core/akaribot/core/loader.py:1336-1337 >>>
# 旧连接关闭期间不得让轮询器发出查询，故与 reload 的切换路径一致地嵌套独占窗口。
# ``note`` 只用于日志措辞（新 context 是纳入还是去掉该包的模型）。
<<< END U007961 >>>
<<< UNIT U007962 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:120-120 | ctx=ModulesManager >>>
模块注册、加载和事件分发管理器。
<<< END U007962 >>>
<<< UNIT U007963 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:265-265 | ctx=ModulesManager.add_module >>>
加入模块。
<<< END U007963 >>>
<<< UNIT U007964 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:282-282 | ctx=ModulesManager.remove_modules >>>
移除模块。
<<< END U007964 >>>
<<< UNIT U007965 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:292-292 | ctx=ModulesManager.refresh_modules_aliases >>>
刷新模块别名。
<<< END U007965 >>>
<<< UNIT U007966 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:301-301 | ctx=ModulesManager.get_module_and_alias_first_words >>>
返回模块名及其所有别名的首词。
<<< END U007966 >>>
<<< UNIT U007967 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:328-328 | ctx=ModulesManager.refresh_modules_hooks >>>
刷新模块 Hook。
<<< END U007967 >>>
<<< UNIT U007968 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:362-362 | ctx=ModulesManager.refresh_modules_events >>>
刷新模块事件。
<<< END U007968 >>>
<<< UNIT U007969 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:370-370 | ctx=ModulesManager.refresh >>>
刷新模块状态。
<<< END U007969 >>>
<<< UNIT U007970 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:378-378 | ctx=ModulesManager.dispatch_event >>>
分发平台事件。
<<< END U007970 >>>
<<< UNIT U007971 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:427-427 | ctx=ModulesManager.search_related_module >>>
查找相关模块。
<<< END U007971 >>>
<<< UNIT U007972 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:669-669 | ctx=ModulesManager.bind_to_module >>>
绑定模块到运行时。
<<< END U007972 >>>
<<< UNIT U007973 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:732-732 | ctx=ModulesManager.load_module >>>
全域加载该机器人模块。
<<< END U007973 >>>
<<< UNIT U007974 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:760-760 | ctx=ModulesManager.unload_module >>>
全域卸载该机器人模块。
<<< END U007974 >>>
<<< UNIT U007975 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:797-799 | ctx=ModulesManager.reload_module >>>
重载该机器人模块（以及该模块所在文件的其他模块）
<<< END U007975 >>>
<<< UNIT U007976 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:1094-1096 | ctx=ModulesManager.reload_py_module >>>
重载该 Python 模块
<<< END U007976 >>>
<<< UNIT U007977 | py-docstring | packages/akari-bot-core/akaribot/core/loader.py:1210-1210 | ctx=ModulesManager._install_package.rollback >>>
撤销本次导入的写入与索引。已切换的数据库 context 不回退。
<<< END U007977 >>>
<<< UNIT U007978 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:2-2 | ctx=bot_name >>>
小可
<<< END U007978 >>>
<<< UNIT U007979 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:3-3 | ctx=check.redacted >>>
[吃掉了:${reason}]
<<< END U007979 >>>
<<< UNIT U007980 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:4-4 | ctx=config.comments.bot.enable >>>
是否开启此客户端。
<<< END U007980 >>>
<<< UNIT U007981 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:5-5 | ctx=config.comments.config_version >>>
配置版本号，将会随功能更新自增，一般情况请勿手动修改。
<<< END U007981 >>>
<<< UNIT U007982 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:6-6 | ctx=config.comments.config.allow_request_private_ip >>>
是否允许机器人请求本地私有 IP 地址。（防止可能的信息泄露）
<<< END U007982 >>>
<<< UNIT U007983 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:7-7 | ctx=config.comments.config.auto_purge_crontab >>>
自动清除缓存的 Cron 表达式。
<<< END U007983 >>>
<<< UNIT U007984 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:8-8 | ctx=config.comments.config.base_superuser >>>
机器人的基础超级用户列表，此处填写的值将会在机器人启动时被加载进入数据库。
<<< END U007984 >>>
<<< UNIT U007985 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:9-9 | ctx=config.comments.config.bug_report_url >>>
错误汇报网址。
<<< END U007985 >>>
<<< UNIT U007986 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:10-10 | ctx=config.comments.config.check_use_textscan_v1 >>>
是否使用旧版阿里云内容安全 1.0 服务接口。
<<< END U007986 >>>
<<< UNIT U007987 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:11-11 | ctx=config.comments.config.command_prefix >>>
命令前缀，此处填写的值将会被识别为命令前缀。
<<< END U007987 >>>
<<< UNIT U007988 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:12-12 | ctx=config.comments.config.confirm_command >>>
确认命令的关键词，此处填写的值将会被识别为确认命令。
<<< END U007988 >>>
<<< UNIT U007989 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:13-13 | ctx=config.comments.config.debug >>>
是否开启调试模式，启用后会输出更多的日志信息。
<<< END U007989 >>>
<<< UNIT U007990 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:14-14 | ctx=config.comments.config.donate_url >>>
捐赠网址。
<<< END U007990 >>>
<<< UNIT U007991 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:15-15 | ctx=config.comments.config.enable_analytics >>>
是否开启内置的统计功能。
<<< END U007991 >>>
<<< UNIT U007992 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:16-16 | ctx=config.comments.config.enable_bind_auto >>>
是否开启“bind auto”命令以自动配对同一场景内的其他实例。
<<< END U007992 >>>
<<< UNIT U007993 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:17-17 | ctx=config.comments.config.enable_commit_url >>>
是否在展示版本信息时显示 commit URL。
<<< END U007993 >>>
<<< UNIT U007994 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:18-18 | ctx=config.comments.config.enable_dirty_check >>>
是否开启文字过滤检测。
<<< END U007994 >>>
<<< UNIT U007995 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:19-19 | ctx=config.comments.config.enable_get_petal >>>
是否允许获取花瓣。
<<< END U007995 >>>
<<< UNIT U007996 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:20-20 | ctx=config.comments.config.enable_joke >>>
是否开启玩笑，启用后将在服务器时间 4 月 1 日时发生。
<<< END U007996 >>>
<<< UNIT U007997 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:21-21 | ctx=config.comments.config.enable_petal >>>
是否开启花瓣功能。
<<< END U007997 >>>
<<< UNIT U007998 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:22-22 | ctx=config.comments.config.enable_rickroll >>>
当文字过滤检测失败时，是否 Rickroll 用户。
<<< END U007998 >>>
<<< UNIT U007999 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:23-23 | ctx=config.comments.config.enable_tos >>>
是否开启内置的 ToS 检查规则。
<<< END U007999 >>>
<<< UNIT U008000 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:24-24 | ctx=config.comments.config.enable_urlmanager >>>
是否开启 URLManager，用于 URL 跳板。（声明此 URL 非官方链接等）
<<< END U008000 >>>
<<< UNIT U008001 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:25-25 | ctx=config.comments.config.ffmpeg_path >>>
FFmpeg 可执行文件路径。
<<< END U008001 >>>
<<< UNIT U008002 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:26-26 | ctx=config.comments.config.help_page_url >>>
模块帮助文档网址。
<<< END U008002 >>>
<<< UNIT U008003 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:27-27 | ctx=config.comments.config.help_url >>>
帮助文档网址。
<<< END U008003 >>>
<<< UNIT U008004 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:28-28 | ctx=config.comments.config.ignored_sender >>>
无视的用户列表，匹配到此列表中的用户将会被忽略。
<<< END U008004 >>>
<<< UNIT U008005 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:29-29 | ctx=config.comments.config.issue_url >>>
问题反馈网址。
<<< END U008005 >>>
<<< UNIT U008006 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:30-30 | ctx=config.comments.config.locale_url >>>
本地化项目网址。
<<< END U008006 >>>
<<< UNIT U008007 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:31-31 | ctx=config.comments.config.media_compression_threshold >>>
媒体文件大小阈值，超过此值的文件将尝试使用 FFmpeg 压缩。单位为 MB。
<<< END U008007 >>>
<<< UNIT U008008 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:32-32 | ctx=config.comments.config.mention_required >>>
是否强制仅处理在消息开头提及机器人的消息。
<<< END U008008 >>>
<<< UNIT U008009 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:33-33 | ctx=config.comments.config.no_confirm >>>
是否无需发送者确认消息即可执行命令。
<<< END U008009 >>>
<<< UNIT U008010 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:34-34 | ctx=config.comments.config.petal_gained_limit >>>
单日获取花瓣上限。
<<< END U008010 >>>
<<< UNIT U008011 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:35-35 | ctx=config.comments.config.petal_lost_limit >>>
单日失去花瓣上限。
<<< END U008011 >>>
<<< UNIT U008012 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:36-36 | ctx=config.comments.config.petal_keep_rate >>>
花瓣周期结算时保留的比例，范围 0 到 1 之间。
<<< END U008012 >>>
<<< UNIT U008013 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:37-37 | ctx=config.comments.config.petal_reset_crontab >>>
花瓣周期的 Cron 表达式。
<<< END U008013 >>>
<<< UNIT U008014 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:38-38 | ctx=config.comments.config.petal_sign_max >>>
单日签到获取花瓣上限。
<<< END U008014 >>>
<<< UNIT U008015 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:39-39 | ctx=config.comments.config.petal_sign_min >>>
单日签到获取花瓣下限。
<<< END U008015 >>>
<<< UNIT U008016 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:40-40 | ctx=config.comments.config.petal_sign_rate >>>
签到获取花瓣概率，范围 0 到 1 之间，获取数量呈几何分布。
<<< END U008016 >>>
<<< UNIT U008017 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:41-41 | ctx=config.comments.config.proxy_disable_ssl >>>
使用代理服务时是否跳过 HTTPS 证书校验，仅在代理服务会替换目标站点证书时生效。
<<< END U008017 >>>
<<< UNIT U008018 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:42-42 | ctx=config.comments.config.qq_test_group_url >>>
QQ 机器人的测试群邀请网址，留空时不在关于菜单中展示。
<<< END U008018 >>>
<<< UNIT U008019 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:43-43 | ctx=config.comments.config.quick_confirm >>>
是否开启消息快速确认。
<<< END U008019 >>>
<<< UNIT U008020 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:44-44 | ctx=config.comments.config.regex_disable_prefix >>>
临时关闭正则解析的消息前缀。
<<< END U008020 >>>
<<< UNIT U008021 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:45-45 | ctx=config.comments.config.repo_url >>>
开源仓库网址。
<<< END U008021 >>>
<<< UNIT U008022 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:46-46 | ctx=config.comments.config.report_targets >>>
上报场景列表，此处填写的场景 ID 将会被识别为上报场景。（如：在机器人执行命令出错时，机器人将会把错误信息发送至对应场景）
<<< END U008022 >>>
<<< UNIT U008023 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:47-47 | ctx=config.comments.config.retired_clients >>>
已退役的客户端及其数据迁移目标，格式为“<源客户端> -> <目标客户端>”（例：“QQ -> QQBot”）。只填写源客户端时表示不提供迁移。
<<< END U008023 >>>
<<< UNIT U008024 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:48-48 | ctx=config.comments.config.rickroll_msg >>>
文字过滤检测失败时的 Rickroll 消息。
<<< END U008024 >>>
<<< UNIT U008025 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:49-49 | ctx=config.comments.config.schedule_interval_multiplier >>>
计划任务触发器的间隔时间倍率。
<<< END U008025 >>>
<<< UNIT U008026 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:50-50 | ctx=config.comments.config.shuffle_rate >>>
玩笑的随机发生率，范围 0 到 1 之间。
<<< END U008026 >>>
<<< UNIT U008027 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:51-51 | ctx=config.comments.config.timezone_offset >>>
机器人的默认时区偏移量。
<<< END U008027 >>>
<<< UNIT U008028 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:52-52 | ctx=config.comments.config.tos_temp_ban_time >>>
违反 ToS 时的临时封禁时间。
<<< END U008028 >>>
<<< UNIT U008029 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:53-53 | ctx=config.comments.config.tos_warning_counts >>>
违反 ToS 时的警告次数。
<<< END U008029 >>>
<<< UNIT U008030 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:54-54 | ctx=config.comments.config.typo_check_args_diff_ratio >>>
命令参数数量差异阈值，用户输入的参数数量与模板参数数量差异比例超过此值时跳过命令匹配，范围 0 到 1 之间。
<<< END U008030 >>>
<<< UNIT U008031 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:55-55 | ctx=config.comments.config.typo_check_args_score >>>
参数拼写检查容许相似度，范围 0 到 1 之间。
<<< END U008031 >>>
<<< UNIT U008032 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:56-56 | ctx=config.comments.config.typo_check_command_score >>>
命令拼写检查容许相似度，范围 0 到 1 之间。
<<< END U008032 >>>
<<< UNIT U008033 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:57-57 | ctx=config.comments.config.typo_check_module_diff_ratio >>>
模块名字符长度差异阈值，匹配到的模块名长度与用户输入长度差异比例超过此值时跳过匹配，范围 0 到 1 之间。
<<< END U008033 >>>
<<< UNIT U008034 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:58-58 | ctx=config.comments.config.typo_check_module_score >>>
模块拼写检查容许相似度，范围 0 到 1 之间。
<<< END U008034 >>>
<<< UNIT U008035 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:59-59 | ctx=config.comments.config.typo_check_options_score >>>
选项拼写检查容许相似度，范围 0 到 1 之间。
<<< END U008035 >>>
<<< UNIT U008036 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:60-60 | ctx=config.comments.config.use_emote >>>
是否使用表情资源。
<<< END U008036 >>>
<<< UNIT U008037 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:61-61 | ctx=config.comments.config.use_font_mirror >>>
渲染网页时是否使用字体镜像。
<<< END U008037 >>>
<<< UNIT U008038 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:62-62 | ctx=config.comments.config.use_secrets_random >>>
是否使用基于 secrets 库的随机数生成器。
<<< END U008038 >>>
<<< UNIT U008039 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:63-63 | ctx=config.comments.default_locale >>>
默认的语言环境。
<<< END U008039 >>>
<<< UNIT U008040 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:64-64 | ctx=config.comments.jobqueue_secret.jobqueue_websocket_token >>>
WebSocket JobQueue Hub 的共享访问令牌。留空时，启动阶段会生成安全随机密钥并写回配置。使用外部 Hub 的所有节点必须配置相同值。
<<< END U008040 >>>
<<< UNIT U008041 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:65-65 | ctx=config.comments.jobqueue.jobqueue_backend >>>
JobQueue 使用的完整传输后端，可选 database 或 websocket，不同后端之间的优缺点请参考以上注释。
<<< END U008041 >>>
<<< UNIT U008042 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:66-66 | ctx=config.comments.jobqueue.jobqueue_node_id >>>
JobQueue 节点标识，长度不得超过 128 个字符。留空时，启动阶段会生成 UUID 并写回配置。共用此配置的进程将归入同一部署节点。
<<< END U008042 >>>
<<< UNIT U008043 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:67-67 | ctx=config.comments.jobqueue.jobqueue_websocket_command_timeout >>>
WebSocket 控制命令的超时时间，单位为秒。
<<< END U008043 >>>
<<< UNIT U008044 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:68-68 | ctx=config.comments.jobqueue.jobqueue_websocket_max_message_bytes >>>
单个 WebSocket 协议帧允许的最大字节数。
<<< END U008044 >>>
<<< UNIT U008045 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:69-69 | ctx=config.comments.jobqueue.jobqueue_websocket_mode >>>
WebSocket Hub 部署模式，可选 embedded 或 external。embedded 由守护进程启动本机 Hub。external 连接独立部署的 Hub。
<<< END U008045 >>>
<<< UNIT U008046 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:70-70 | ctx=config.comments.jobqueue.jobqueue_websocket_queue_size >>>
每个 WebSocket 节点的最大待发送帧数量，队列满时新投递将被拒绝。
<<< END U008046 >>>
<<< UNIT U008047 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:71-71 | ctx=config.comments.jobqueue.jobqueue_websocket_url >>>
WebSocket JobQueue Hub 的统一地址。embedded 模式同时从该地址取得监听主机、端口和路径。external 模式将其作为客户端连接地址。
<<< END U008047 >>>
<<< UNIT U008048 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:72-72 | ctx=config.comments.s3_secret.s3_access_key >>>
S3 兼容 API 的 AccessKey。
<<< END U008048 >>>
<<< UNIT U008049 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:73-73 | ctx=config.comments.s3_secret.s3_secret_key >>>
S3 兼容 API 的 SecretKey。
<<< END U008049 >>>
<<< UNIT U008050 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:74-74 | ctx=config.comments.s3.s3_bucket >>>
S3 兼容 API 的桶名。
<<< END U008050 >>>
<<< UNIT U008051 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:75-75 | ctx=config.comments.s3.s3_connect_timeout >>>
S3 兼容 API 的连接超时时间。
<<< END U008051 >>>
<<< UNIT U008052 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:76-76 | ctx=config.comments.s3.s3_endpoint_url >>>
S3 兼容 API 的端点 URL。
<<< END U008052 >>>
<<< UNIT U008053 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:77-77 | ctx=config.comments.s3.s3_internal_endpoint >>>
S3 兼容 API 的内网访问 URL。
<<< END U008053 >>>
<<< UNIT U008054 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:78-78 | ctx=config.comments.s3.s3_max_attempts >>>
S3 兼容 API 单次请求的最大尝试次数。
<<< END U008054 >>>
<<< UNIT U008055 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:79-79 | ctx=config.comments.s3.s3_max_workers >>>
S3 兼容 API 专用线程池的最大线程数。
<<< END U008055 >>>
<<< UNIT U008056 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:80-80 | ctx=config.comments.s3.s3_operation_timeout >>>
S3 兼容 API 单次完整操作的最长等待时间。
<<< END U008056 >>>
<<< UNIT U008057 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:81-81 | ctx=config.comments.s3.s3_public_endpoint >>>
S3 兼容 API 的公网访问 URL。
<<< END U008057 >>>
<<< UNIT U008058 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:82-82 | ctx=config.comments.s3.s3_read_timeout >>>
S3 兼容 API 的网络读取超时时间。
<<< END U008058 >>>
<<< UNIT U008059 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:83-83 | ctx=config.comments.s3.s3_region >>>
S3 兼容 API 的地域名。
<<< END U008059 >>>
<<< UNIT U008060 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:84-84 | ctx=config.comments.s3.s3_temp_max_count >>>
S3 兼容 API 的临时文件最大数量。
<<< END U008060 >>>
<<< UNIT U008061 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:85-85 | ctx=config.comments.secret.check_access_key_id >>>
阿里云内容安全服务的 AccessKey ID。
<<< END U008061 >>>
<<< UNIT U008062 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:86-86 | ctx=config.comments.secret.check_access_key_secret >>>
阿里云内容安全服务的 AccessKey Secret。
<<< END U008062 >>>
<<< UNIT U008063 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:87-87 | ctx=config.comments.secret.db_path >>>
数据库连接字符串，请使用 Tortoise ORM 支持的数据库连接字符串格式。
<<< END U008063 >>>
<<< UNIT U008064 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:88-88 | ctx=config.comments.secret.proxy >>>
代理服务地址。
<<< END U008064 >>>
<<< UNIT U008065 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:89-89 | ctx=config.comments.smtp_secret.smtp_password >>>
SMTP 登录密码。
<<< END U008065 >>>
<<< UNIT U008066 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:90-90 | ctx=config.comments.smtp.enable_email_report >>>
是否开启 SMTP 邮件上报，开启后将不再上报至场景。
<<< END U008066 >>>
<<< UNIT U008067 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:91-91 | ctx=config.comments.smtp.smtp_host >>>
SMTP 服务器地址。
<<< END U008067 >>>
<<< UNIT U008068 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:92-92 | ctx=config.comments.smtp.smtp_port >>>
SMTP 服务器端口号。
<<< END U008068 >>>
<<< UNIT U008069 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:93-93 | ctx=config.comments.smtp.smtp_recipients >>>
邮件收件人列表。
<<< END U008069 >>>
<<< UNIT U008070 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:94-94 | ctx=config.comments.smtp.smtp_sender >>>
发件人名称，留空则使用登录邮箱地址。
<<< END U008070 >>>
<<< UNIT U008071 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:95-95 | ctx=config.comments.smtp.smtp_ssl >>>
是否使用 SMTPS（SSL）连接。
<<< END U008071 >>>
<<< UNIT U008072 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:96-96 | ctx=config.comments.smtp.smtp_starttls >>>
是否启用 STARTTLS。
<<< END U008072 >>>
<<< UNIT U008073 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:97-97 | ctx=config.comments.smtp.smtp_username >>>
SMTP 登录邮箱地址。
<<< END U008073 >>>
<<< UNIT U008074 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:98-98 | ctx=config.comments.webrender.browser_executable_path >>>
WebRender 使用的浏览器可执行文件路径，留空则使用 Playwright 默认安装的浏览器。
<<< END U008074 >>>
<<< UNIT U008075 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:99-99 | ctx=config.comments.webrender.browser_type >>>
WebRender 使用的浏览器类型。（支持“chrome”与“firefox”）
<<< END U008075 >>>
<<< UNIT U008076 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:100-100 | ctx=config.comments.webrender.enable >>>
是否开启 WebRender。
<<< END U008076 >>>
<<< UNIT U008077 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:101-101 | ctx=config.comments.webrender.headless >>>
是否以无头模式运行浏览器。
<<< END U008077 >>>
<<< UNIT U008078 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:102-102 | ctx=config.comments.webrender.remote_only >>>
是否仅允许使用远程 WebRender 服务。
<<< END U008078 >>>
<<< UNIT U008079 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:103-103 | ctx=config.comments.webrender.remote_web_render_url >>>
远程 WebRender 服务的 URL，在本地 WebRender 渲染失败时尝试请求。
<<< END U008079 >>>
<<< UNIT U008080 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:105-105 | ctx=config.header.line.2 >>>
注意：TOML 不是 Python。请不要在此处使用 Python 语法。
<<< END U008080 >>>
<<< UNIT U008081 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:106-106 | ctx=config.header.line.3 >>>
例如：TOML 中的布尔值必须是小写。
<<< END U008081 >>>
<<< UNIT U008082 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:107-107 | ctx=config.notes.jobqueue.backend.consistency >>>
如需分布式部署，分布节点必须使用同一类型的后端。
<<< END U008082 >>>
<<< UNIT U008083 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:108-108 | ctx=config.notes.jobqueue.backend.database >>>
database：无需额外部署 Hub，且可在共享数据库中保留尚未过期的队列记录，但轮询、认领、心跳与清理均会增加数据库负载。不建议在使用 SQLite 作为数据库时使用。
<<< END U008083 >>>
<<< UNIT U008084 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:109-109 | ctx=config.notes.jobqueue.backend.intro >>>
机器人客户端与服务端的通信依赖于 JobQueue，实例部署必须在 database 与 websocket 中选择一套完整后端。一般情况下你无需关注这些配置。（如遇 websocket 端口冲突可调整使用后端或端口）
<<< END U008084 >>>
<<< UNIT U008085 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:110-110 | ctx=config.notes.jobqueue.backend.websocket >>>
websocket：经 Hub 实时路由，延迟较低，且可以避免 JobQueue 对业务数据库的轮询和写入竞争，但需要维护 Hub、长连接以及远程连接所需的令牌和 TLS。
<<< END U008085 >>>
<<< UNIT U008086 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:111-111 | ctx=config.table.config >>>
一些基础的配置部分，此处填写的值可在消息中以明文形式展示。请不要在此部分填写敏感信息。
<<< END U008086 >>>
<<< UNIT U008087 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:112-112 | ctx=config.table.config_bot >>>
客户端的配置部分，此处填写的值可在消息中以明文形式展示。请不要在此部分填写敏感信息。
<<< END U008087 >>>
<<< UNIT U008088 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:113-113 | ctx=config.table.config_jobqueue >>>
JobQueue 的配置部分，此处填写的值可在消息中以明文形式展示。请不要在此部分填写敏感信息。
<<< END U008088 >>>
<<< UNIT U008089 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:114-114 | ctx=config.table.config_module >>>
模块的配置部分，此处填写的值可在消息中以明文形式展示。请不要在此部分填写敏感信息。
<<< END U008089 >>>
<<< UNIT U008090 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:115-115 | ctx=config.table.config_s3 >>>
S3 兼容 API 的配置部分，此处填写的值可在消息中以明文形式展示。请不要在此部分填写敏感信息。
<<< END U008090 >>>
<<< UNIT U008091 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:116-116 | ctx=config.table.config_smtp >>>
SMTP 的配置部分，此处填写的值可在消息中以明文形式展示。请不要在此部分填写敏感信息。
<<< END U008091 >>>
<<< UNIT U008092 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:117-117 | ctx=config.table.config_webrender >>>
WebRender 的配置部分，此处填写的值可在消息中以明文形式展示。请不要在此部分填写敏感信息。
<<< END U008092 >>>
<<< UNIT U008093 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:118-118 | ctx=config.table.secret >>>
密钥配置部分，此处的值若意外出现在发送的消息中，机器人会尝试拦截。但请务必提防泄露。
<<< END U008093 >>>
<<< UNIT U008094 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:119-119 | ctx=config.table.secret_bot >>>
客户端的密钥配置部分，此处的值若意外出现在发送的消息中，机器人会尝试拦截。但请务必提防泄露。
<<< END U008094 >>>
<<< UNIT U008095 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:120-120 | ctx=config.table.secret_jobqueue >>>
JobQueue 的密钥部分，此处的值若意外出现在发送的消息中，机器人会尝试拦截。但请务必提防泄露。
<<< END U008095 >>>
<<< UNIT U008096 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:121-121 | ctx=config.table.secret_module >>>
模块的密钥配置部分，此处的值若意外出现在发送的消息中，机器人会尝试拦截。但请务必提防泄露。
<<< END U008096 >>>
<<< UNIT U008097 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:122-122 | ctx=config.table.secret_s3 >>>
S3 兼容 API 的密钥部分，此处的值若意外出现在发送的消息中，机器人会尝试拦截。但请务必提防泄露。
<<< END U008097 >>>
<<< UNIT U008098 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:123-123 | ctx=config.table.secret_smtp >>>
SMTP 的密钥部分，此处的值若意外出现在发送的消息中，机器人会尝试拦截。但请务必提防泄露。
<<< END U008098 >>>
<<< UNIT U008099 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:124-124 | ctx=core.help.alias >>>
命令别名：
<<< END U008099 >>>
<<< UNIT U008100 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:125-125 | ctx=core.help.author >>>
模块作者：
<<< END U008100 >>>
<<< UNIT U008101 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:126-126 | ctx=core.help.commands >>>
可用命令：
<<< END U008101 >>>
<<< UNIT U008102 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:127-127 | ctx=core.help.header >>>
模块帮助信息
<<< END U008102 >>>
<<< UNIT U008103 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:128-128 | ctx=core.help.info.none >>>
（此模块没有帮助信息）
<<< END U008103 >>>
<<< UNIT U008104 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:129-129 | ctx=core.help.options >>>
选项：
<<< END U008104 >>>
<<< UNIT U008105 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:130-130 | ctx=core.help.regex >>>
可用表达式：
<<< END U008105 >>>
<<< UNIT U008106 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:131-131 | ctx=core.help.regex.disable_tip >>>
提示：在消息开头添加“${prefixes}”前缀可临时关闭本条消息的正则解析。
<<< END U008106 >>>
<<< UNIT U008107 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:132-132 | ctx=core.help.regex.note >>>
此模块支持正则表达式，消息发送时将会匹配以下内容：
<<< END U008107 >>>
<<< UNIT U008108 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:133-133 | ctx=core.message.confirm >>>
你确定吗？
<<< END U008108 >>>
<<< UNIT U008109 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:134-134 | ctx=error.config.invalid >>>
配置参数无效或未找到，请检查配置文件。
<<< END U008109 >>>
<<< UNIT U008110 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:135-135 | ctx=error.config.secret.not_found >>>
未找到密钥配置参数，请检查配置文件。
<<< END U008110 >>>
<<< UNIT U008111 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:136-136 | ctx=error.config.webrender.invalid >>>
未配置 WebRender，无法使用此命令。
<<< END U008111 >>>
<<< UNIT U008112 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:137-137 | ctx=error.i18n.fallback >>>
（如果你看到了这个占位符，说明此处缺少本地化文本，请反馈此问题以便快速解决。）
<<< END U008112 >>>
<<< UNIT U008113 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:138-138 | ctx=error.message.chain.empty >>>
机器人尝试发送空消息，请联系机器人所有者解决问题。
<<< END U008113 >>>
<<< UNIT U008114 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:139-139 | ctx=error.message.chain.unsafe >>>
消息中含有不安全的内容，已被拦截。
<<< END U008114 >>>
<<< UNIT U008115 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:140-140 | ctx=error.message.discord.dm.cannot_send >>>
此命令不支持在私聊下发送消息，请联系开发者处理。
<<< END U008115 >>>
<<< UNIT U008116 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:141-141 | ctx=error.message.discord.thread.permission_denied >>>
无法发送消息，可能是因为机器人在本频道的权限（创建子区）不足。
<<< END U008116 >>>
<<< UNIT U008117 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:142-142 | ctx=error.message.limited >>>
消息发送失败，可能被风控，请稍后再试。
<<< END U008117 >>>
<<< UNIT U008118 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:143-143 | ctx=error.message.limited.msg2img >>>
消息被风控，尝试使用图片发送：
<<< END U008118 >>>
<<< UNIT U008119 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:144-144 | ctx=error.message.prompt >>>
执行命令时发生错误：
<<< END U008119 >>>
<<< UNIT U008120 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:145-145 | ctx=error.message.prompt.address >>>
错误汇报地址：${url}
<<< END U008120 >>>
<<< UNIT U008121 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:146-146 | ctx=error.message.prompt.external >>>
此问题可能由外部系统导致，若持续发生，请将此消息报告给机器人所有者。
<<< END U008121 >>>
<<< UNIT U008122 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:147-147 | ctx=error.message.prompt.noreport >>>
此问题并非机器人程序错误，请勿将此消息报告给机器人所有者。
<<< END U008122 >>>
<<< UNIT U008123 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:148-148 | ctx=error.message.prompt.report >>>
请将此信息报告给机器人所有者。
<<< END U008123 >>>
<<< UNIT U008124 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:149-149 | ctx=error.message.report >>>
执行“${command}”时发生了以下错误，请及时处理：
<<< END U008124 >>>
<<< UNIT U008125 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:150-150 | ctx=error.message.timeout >>>
消息发送超时，请稍后重试命令或尝试等待返回结果。
<<< END U008125 >>>
<<< UNIT U008126 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:151-151 | ctx=error.module.helpdoc_invalid >>>
“${module}”模块的帮助信息无效，请联系开发者解决问题。
<<< END U008126 >>>
<<< UNIT U008127 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:152-152 | ctx=error.module.unbound >>>
“${module}”模块未绑定任何命令且无简介，请联系开发者解决问题。
<<< END U008127 >>>
<<< UNIT U008128 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:153-153 | ctx=example >>>
你好世界！
<<< END U008128 >>>
<<< UNIT U008129 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:154-154 | ctx=game.help.stop >>>
停止当前的游戏。
<<< END U008129 >>>
<<< UNIT U008130 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:155-155 | ctx=game.message.running >>>
当前此游戏正在进行中。
<<< END U008130 >>>
<<< UNIT U008131 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:156-156 | ctx=game.message.stop >>>
已停止。
<<< END U008131 >>>
<<< UNIT U008132 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:157-157 | ctx=game.message.stop.none >>>
当前此游戏未在进行。
<<< END U008132 >>>
<<< UNIT U008133 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:158-158 | ctx=help.option.img >>>
强制使用图片模式。
<<< END U008133 >>>
<<< UNIT U008134 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:159-159 | ctx=help.option.legacy >>>
强制使用文本模式。
<<< END U008134 >>>
<<< UNIT U008135 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:160-160 | ctx=i18n.unit.1 >>>
万
<<< END U008135 >>>
<<< UNIT U008136 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:161-161 | ctx=i18n.unit.2 >>>
亿
<<< END U008136 >>>
<<< UNIT U008137 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:162-162 | ctx=i18n.unit.3 >>>
兆
<<< END U008137 >>>
<<< UNIT U008138 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:163-163 | ctx=language >>>
简体中文
<<< END U008138 >>>
<<< UNIT U008139 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:164-164 | ctx=loader.load.failed >>>
加载模块中发生了以下错误，对应模块未加载：
<<< END U008139 >>>
<<< UNIT U008140 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:165-165 | ctx=loader.load.success >>>
所有模块已正常加载。
<<< END U008140 >>>
<<< UNIT U008141 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:166-166 | ctx=message >>>
消息
<<< END U008141 >>>
<<< UNIT U008142 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:167-167 | ctx=message.action_text.hint >>>
${cmd}（点击添加到输入框然后手动复制）
<<< END U008142 >>>
<<< UNIT U008143 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:168-168 | ctx=message.action_text.modal.input >>>
命令
<<< END U008143 >>>
<<< UNIT U008144 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:169-169 | ctx=message.action_text.modal.title >>>
编辑命令
<<< END U008144 >>>
<<< UNIT U008145 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:170-170 | ctx=message.action_text.select >>>
选择要编辑的命令
<<< END U008145 >>>
<<< UNIT U008146 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:171-171 | ctx=message.action_text.send >>>
发送此命令
<<< END U008146 >>>
<<< UNIT U008147 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:173-173 | ctx=message.button.expired >>>
此按钮已过期。
<<< END U008147 >>>
<<< UNIT U008148 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:174-174 | ctx=message.button.forbidden >>>
你不能点击别人的按钮。
<<< END U008148 >>>
<<< UNIT U008149 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:175-175 | ctx=message.button.invalid >>>
此按钮已失效。
<<< END U008149 >>>
<<< UNIT U008150 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:176-176 | ctx=message.button.no >>>
❌ 否
<<< END U008150 >>>
<<< UNIT U008151 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:177-177 | ctx=message.button.used >>>
此按钮已经使用过了。
<<< END U008151 >>>
<<< UNIT U008152 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:178-178 | ctx=message.button.yes >>>
✔️ 是
<<< END U008152 >>>
<<< UNIT U008153 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:179-179 | ctx=message.cancelled >>>
已取消
<<< END U008153 >>>
<<< UNIT U008154 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:180-180 | ctx=message.collapse >>>
……仅显示前 ${amount} 条内容。
<<< END U008154 >>>
<<< UNIT U008155 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:182-182 | ctx=message.confirmed >>>
已确认
<<< END U008155 >>>
<<< UNIT U008156 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:183-183 | ctx=message.cooldown >>>
等待 ${time} 秒后才能再次使用此命令。
<<< END U008156 >>>
<<< UNIT U008157 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:184-184 | ctx=message.cooldown.manual >>>
此{TERM:target}已设置等待 ${time} 秒后才能再次使用命令。
<<< END U008157 >>>
<<< UNIT U008158 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:186-186 | ctx=message.embed.author >>>
作者：
<<< END U008158 >>>
<<< UNIT U008159 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:188-188 | ctx=message.error >>>
发生错误：
<<< END U008159 >>>
<<< UNIT U008160 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:189-189 | ctx=message.failed >>>
失败。
<<< END U008160 >>>
<<< UNIT U008161 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:190-190 | ctx=message.id.init.sender.confirm >>>
此用户不存在，是否初始化？
<<< END U008161 >>>
<<< UNIT U008162 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:191-191 | ctx=message.id.init.target.confirm >>>
此{TERM:target}不存在，是否初始化？
<<< END U008162 >>>
<<< UNIT U008163 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:192-192 | ctx=message.id.invalid.sender >>>
ID 格式错误，格式应为“${sender}|<用户 ID>”。
<<< END U008163 >>>
<<< UNIT U008164 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:193-193 | ctx=message.id.invalid.target >>>
ID 格式错误，格式应为“${target}|<{TERM:target} ID>”。
<<< END U008164 >>>
<<< UNIT U008165 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:194-194 | ctx=message.id.not_found.sender >>>
此用户不存在。
<<< END U008165 >>>
<<< UNIT U008166 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:195-195 | ctx=message.id.not_found.target >>>
此{TERM:target}不存在。
<<< END U008166 >>>
<<< UNIT U008167 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:196-196 | ctx=message.image.list >>>
图片列表：
<<< END U008167 >>>
<<< UNIT U008168 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:197-197 | ctx=message.list >>>
消息列表
<<< END U008168 >>>
<<< UNIT U008169 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:198-198 | ctx=message.no >>>
否
<<< END U008169 >>>
<<< UNIT U008170 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:199-199 | ctx=message.none >>>
无
<<< END U008170 >>>
<<< UNIT U008171 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:201-201 | ctx=message.selected >>>
已选择：
<<< END U008171 >>>
<<< UNIT U008172 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:202-202 | ctx=message.success >>>
成功。
<<< END U008172 >>>
<<< UNIT U008173 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:203-203 | ctx=message.typing >>>
正在输入中……
<<< END U008173 >>>
<<< UNIT U008174 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:204-204 | ctx=message.unknown >>>
未知
<<< END U008174 >>>
<<< UNIT U008175 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:205-205 | ctx=message.url.blocked >>>
[此链接已被阻止]
<<< END U008175 >>>
<<< UNIT U008176 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:206-206 | ctx=message.url.untrusted >>>
此链接未经认证，请谨慎打开
<<< END U008176 >>>
<<< UNIT U008177 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:207-207 | ctx=message.wait.confirm.prompt >>>
（发送“是”等符合确认条件的词语来确认）
<<< END U008177 >>>
<<< UNIT U008178 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:208-208 | ctx=message.wait.confirm.prompt.button >>>
（发送“是”等符合确认条件的词语或点击按钮来确认）
<<< END U008178 >>>
<<< UNIT U008179 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:209-209 | ctx=message.wait.confirm.prompt.qq >>>
（发送“是”等符合确认条件的词语，点击表情反应或戳一戳来确认）
<<< END U008179 >>>
<<< UNIT U008180 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:210-210 | ctx=message.wait.confirm.prompt.reaction >>>
（发送“是”等符合确认条件的词语或点击表情反应来确认）
<<< END U008180 >>>
<<< UNIT U008181 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:211-211 | ctx=message.wait.confirm.prompt.strict >>>
（此为危险操作，须完整发送“${token}”来确认）
<<< END U008181 >>>
<<< UNIT U008182 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:212-212 | ctx=message.wait.next_message.prompt >>>
（发送符合条件的词语以继续）
<<< END U008182 >>>
<<< UNIT U008183 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:213-213 | ctx=message.wait.reply.prompt >>>
（使用指定的词语引用回复此消息）
<<< END U008183 >>>
<<< UNIT U008184 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:214-214 | ctx=message.yes >>>
是
<<< END U008184 >>>
<<< UNIT U008185 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:215-215 | ctx=parser.admin.permission.denied.command >>>
此命令仅限该{TERM:target}的管理员使用，请联系管理员执行此命令。
<<< END U008185 >>>
<<< UNIT U008186 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:216-216 | ctx=parser.admin.permission.denied.module >>>
“${module}”模块下的命令仅限该{TERM:target}的管理员使用，请联系管理员执行此命令。
<<< END U008186 >>>
<<< UNIT U008187 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:217-217 | ctx=parser.command.fixup.confirm >>>
你是否想要输入“${command}”？
（仅提供命令语法修正，不保证预期结果）
<<< END U008187 >>>
<<< UNIT U008188 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:218-218 | ctx=parser.regex.message_too_long >>>
消息过长，是否继续解析消息？
<<< END U008188 >>>
<<< UNIT U008189 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:219-219 | ctx=parser.command.invalid.module >>>
此模块不存在。
使用“${cmd}”查看帮助。
<<< END U008189 >>>
<<< UNIT U008190 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:220-220 | ctx=parser.command.invalid.syntax >>>
语法错误。
使用“${cmd}”查看帮助。
<<< END U008190 >>>
<<< UNIT U008191 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:221-221 | ctx=parser.command.running.prompt >>>
当前有命令正在执行，请稍后再试。
<<< END U008191 >>>
<<< UNIT U008192 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:222-222 | ctx=parser.command.running.prompt2 >>>
先前的命令正在执行中。
<<< END U008192 >>>
<<< UNIT U008193 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:223-223 | ctx=parser.module.desc >>>
描述：
${desc}
<<< END U008193 >>>
<<< UNIT U008194 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:224-224 | ctx=parser.module.disabled >>>
“${module}”模块未开启，请联系管理员开启此模块。
<<< END U008194 >>>
<<< UNIT U008195 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:225-225 | ctx=parser.module.disabled.prompt >>>
“${module}”模块未开启，请使用“${cmd}”开启此模块。
<<< END U008195 >>>
<<< UNIT U008196 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:226-226 | ctx=parser.module.disabled.to_enable >>>
是否开启模块并继续执行此命令？
<<< END U008196 >>>
<<< UNIT U008197 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:227-227 | ctx=parser.module.unloaded >>>
“${module}”模块当前未加载，请联系开发者处理。
<<< END U008197 >>>
<<< UNIT U008198 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:228-228 | ctx=parser.retired.prompt >>>
本平台已停止提供服务，仅保留数据迁移功能。
请使用“${cmd}”将数据迁移至新的平台。
<<< END U008198 >>>
<<< UNIT U008199 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:229-229 | ctx=parser.superuser.permission.denied >>>
你没有使用该命令的权限。
<<< END U008199 >>>
<<< UNIT U008200 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:230-230 | ctx=petal.message.cost >>>
（使用了 ${amount} 片花瓣）
<<< END U008200 >>>
<<< UNIT U008201 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:231-231 | ctx=petal.message.cost.not_enough >>>
你的花瓣不足。
<<< END U008201 >>>
<<< UNIT U008202 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:232-232 | ctx=petal.message.count.invalid >>>
无效的花瓣数量。
<<< END U008202 >>>
<<< UNIT U008203 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:233-233 | ctx=petal.message.gained.limit >>>
但是，本日获得的花瓣已达到每日上限，请明日再试。
<<< END U008203 >>>
<<< UNIT U008204 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:234-234 | ctx=petal.message.gained.success >>>
获得了 ${amount} 片花瓣。
<<< END U008204 >>>
<<< UNIT U008205 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:235-235 | ctx=petal.message.lost.limit >>>
（本日失去的花瓣已达到每日上限。）
<<< END U008205 >>>
<<< UNIT U008206 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:236-236 | ctx=petal.message.lost.success >>>
失去了 ${amount} 片花瓣。
<<< END U008206 >>>
<<< UNIT U008207 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:237-237 | ctx=smtp.report.footer >>>
若你不应收到本邮件，请至 ${issue_url} 提醒机器人所有者以关闭此通知。
<<< END U008207 >>>
<<< UNIT U008208 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:238-238 | ctx=smtp.report.subject.error.command >>>
发生错误：${cmd}
<<< END U008208 >>>
<<< UNIT U008209 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:239-239 | ctx=smtp.report.subject.error.rpc >>>
发生 RPC 错误：${method}
<<< END U008209 >>>
<<< UNIT U008210 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:240-240 | ctx=smtp.report.subject.tos >>>
违反 ToS 上报：${sender}
<<< END U008210 >>>
<<< UNIT U008211 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:241-241 | ctx=time.date.format >>>
%Y 年 %m 月 %d 日
<<< END U008211 >>>
<<< UNIT U008212 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:245-245 | ctx=tos.message.action >>>
采取措施：${action}
<<< END U008212 >>>
<<< UNIT U008213 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:246-246 | ctx=tos.message.action.blocked >>>
封禁
<<< END U008213 >>>
<<< UNIT U008214 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:247-247 | ctx=tos.message.action.warning >>>
警告
<<< END U008214 >>>
<<< UNIT U008215 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:248-248 | ctx=tos.message.appeal >>>
如果你有任何异议，请至 ${issue_url} 发起问题。
<<< END U008215 >>>
<<< UNIT U008216 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:249-249 | ctx=tos.message.banned >>>
由于你触发的警告次数超过最大限度，机器人已封禁你的账户。在此条消息后将不再回应你的请求。
<<< END U008216 >>>
<<< UNIT U008217 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:250-250 | ctx=tos.message.in_group_blocklist >>>
此群聊在黑名单中，已自动退出。
<<< END U008217 >>>
<<< UNIT U008218 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:251-251 | ctx=tos.message.reason >>>
具体原因：${reason}
<<< END U008218 >>>
<<< UNIT U008219 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:252-252 | ctx=tos.message.reason.abuse >>>
一段时间内使用命令的次数过多。
<<< END U008219 >>>
<<< UNIT U008220 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:253-253 | ctx=tos.message.reason.cooldown >>>
一段时间内使用相同命令的次数过多。
<<< END U008220 >>>
<<< UNIT U008221 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:254-254 | ctx=tos.message.reason.ignore >>>
无视临时封禁警告。
<<< END U008221 >>>
<<< UNIT U008222 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:255-255 | ctx=tos.message.reason.kick >>>
将机器人移出群聊。
<<< END U008222 >>>
<<< UNIT U008223 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:256-256 | ctx=tos.message.reason.restrict >>>
对机器人实施禁言。
<<< END U008223 >>>
<<< UNIT U008224 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:257-257 | ctx=tos.message.report >>>
用户 ${sender} 在场景 ${target} 触发了滥用警告。
<<< END U008224 >>>
<<< UNIT U008225 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:258-258 | ctx=tos.message.tempbanned >>>
提示：
由于你的行为触发了警告，机器人已对你进行临时封禁。
距离解封时间还有 ${ban_time} 秒。
<<< END U008225 >>>
<<< UNIT U008226 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:259-259 | ctx=tos.message.tempbanned.warning >>>
提示：
即使已被临时封禁，尝试继续滥用命令可能会导致你被再次警告。
距离解封时间还有 ${ban_time} 秒。
<<< END U008226 >>>
<<< UNIT U008227 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:260-260 | ctx=tos.message.warning >>>
警告：
根据服务条款，你已违反行为准则。
<<< END U008227 >>>
<<< UNIT U008228 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:261-261 | ctx=tos.message.warning.count >>>
这是第 ${current_warns} 次警告。
<<< END U008228 >>>
<<< UNIT U008229 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:262-262 | ctx=tos.message.warning.last >>>
这是最后一次警告。
<<< END U008229 >>>
<<< UNIT U008230 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:263-263 | ctx=tos.message.warning.prompt >>>
如警告次数超过 ${warn_counts} 次，机器人将会封禁你的账户。
<<< END U008230 >>>
<<< UNIT U008231 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:264-264 | ctx=config.error.unknown_field >>>
配置项 ${field} 未在模板或配置文件中定义。
<<< END U008231 >>>
<<< UNIT U008232 | json-value | packages/akari-bot-core/akaribot/core/locales/zh_cn.json:265-265 | ctx=config.error.invalid_value >>>
配置项 ${field} 的输入不符合声明类型。
<<< END U008232 >>>
<<< UNIT U008233 | py-comment | packages/akari-bot-core/akaribot/core/logger.py:55-55 >>>
# 如果没有默认的日志处理器，则忽略此错误
<<< END U008233 >>>
<<< UNIT U008234 | py-docstring | packages/akari-bot-core/akaribot/core/logger.py:1-1 | ctx=<module> >>>
机器人内置的基于 `loguru` 的日志工具。
<<< END U008234 >>>
<<< UNIT U008235 | py-docstring | packages/akari-bot-core/akaribot/core/logger.py:31-31 | ctx=LoggingLogger >>>
兼容标准库 logging.Logger 的项目日志类。
<<< END U008235 >>>
<<< UNIT U008236 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:310-310 | ctx=ModuleRuntimeManager.get_or_create >>>
获取或创建模块运行时。
<<< END U008236 >>>
<<< UNIT U008237 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:333-333 | ctx=ModuleRuntimeManager.state >>>
返回模块状态。
<<< END U008237 >>>
<<< UNIT U008238 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:359-359 | ctx=ModuleRuntimeManager.resource >>>
返回模块资源。
<<< END U008238 >>>
<<< UNIT U008239 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:366-366 | ctx=ModuleRuntimeManager.cache_path >>>
返回模块缓存路径。
<<< END U008239 >>>
<<< UNIT U008240 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:378-378 | ctx=ModuleRuntimeManager.cleanup >>>
清理运行时资源。
<<< END U008240 >>>
<<< UNIT U008241 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:390-390 | ctx=ModuleRuntimeManager.spawn >>>
创建模块运行时。
<<< END U008241 >>>
<<< UNIT U008242 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:395-395 | ctx=ModuleRuntimeManager.current >>>
返回当前运行时。
<<< END U008242 >>>
<<< UNIT U008243 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:404-404 | ctx=ModuleRuntimeManager.use >>>
在指定模块的运行时上下文中执行代码，退出时恢复之前的运行时。
<<< END U008243 >>>
<<< UNIT U008244 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:413-413 | ctx=ModuleRuntimeManager.prepare_reload >>>
准备重载。
<<< END U008244 >>>
<<< UNIT U008245 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:431-431 | ctx=ModuleRuntimeManager.abort_reload >>>
中止重载。
<<< END U008245 >>>
<<< UNIT U008246 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:455-455 | ctx=ModuleRuntimeManager.commit_reload >>>
提交重载结果。
<<< END U008246 >>>
<<< UNIT U008247 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:493-493 | ctx=ModuleRuntimeManager.activate >>>
激活模块。
<<< END U008247 >>>
<<< UNIT U008248 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:498-498 | ctx=ModuleRuntimeManager.suspend >>>
挂起运行时。
<<< END U008248 >>>
<<< UNIT U008249 | py-docstring | packages/akari-bot-core/akaribot/core/module_runtime.py:505-505 | ctx=ModuleRuntimeManager.shutdown >>>
关闭运行时。
<<< END U008249 >>>
<<< UNIT U008250 | py-comment | packages/akari-bot-core/akaribot/core/paths.py:12-12 >>>
# 实例目录。未设置时使用进程 cwd，与历史行为一致。
<<< END U008250 >>>
<<< UNIT U008251 | py-comment | packages/akari-bot-core/akaribot/core/paths.py:15-15 >>>
# 配置目录。优先级高于实例目录下的 config。
<<< END U008251 >>>
<<< UNIT U008252 | py-comment | packages/akari-bot-core/akaribot/core/paths.py:18-18 >>>
# 测试用例目录。该目录属于源码仓库而非实例，故单独指定。
<<< END U008252 >>>
<<< UNIT U008253 | py-comment | packages/akari-bot-core/akaribot/core/paths.py:30-32 >>>
# 判定条件是“含 ``packages/`` 与 ``pyproject.toml`` 的最近祖先”，不按层数推算——源码根目录从
# ``packages/<dist>/akaribot`` 变成 ``<dist>/akaribot`` 后层数不同，数层数会静默指到仓库之外。
# 打包形态下找不到这样的祖先时回退到包内目录，测试目录必然不存在，调用方的存在性判断正常生效。
<<< END U008253 >>>
<<< UNIT U008254 | py-comment | packages/akari-bot-core/akaribot/core/paths.py:43-43 >>>
# as_dict() 面向“实例目录”清单。锁是文件，故显式排除。
<<< END U008254 >>>
<<< UNIT U008255 | py-docstring | packages/akari-bot-core/akaribot/core/paths.py:41-41 | ctx=Paths >>>
实例目录及其子目录。
<<< END U008255 >>>
<<< UNIT U008256 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:1-1 | ctx=JobQueue Peer RPC 与信号总线 >>>
# JobQueue Peer RPC 与信号总线
<<< END U008256 >>>
<<< UNIT U008257 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:3-5 | ctx=JobQueue Peer RPC 与信号总线 >>>
Bot 与 Server 进程共用一套双向 RPC 与信号运行时。运行时通过配置装配一套完整的 JobQueue 后端。
该后端同时提供节点注册表（Peer Registry）和消息传输能力，二者不得跨后端组合。
当前提供数据库与 WebSocket 两种互斥后端。
<<< END U008257 >>>
<<< UNIT U008258 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:7-8 | ctx=JobQueue Peer RPC 与信号总线 >>>
进程内的 `Alive` 仅作为同步路由缓存，并通过权威 Registry
定期对账。任何未经当前后端确认的缓存记录均不得视为在线实例。
<<< END U008258 >>>
<<< UNIT U008259 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:10-10 | ctx=组件与职责 >>>
## 组件与职责
<<< END U008259 >>>
<<< UNIT U008260 | md-table | packages/akari-bot-core/akaribot/core/queue/README.md:12-27 | ctx=组件与职责 >>>
| 文件 | 职责 |
| --- | --- |
| `contracts.py` | 声明稳定的方法名称、调用签名、路由规则与默认超时时间 |
| `rpc.py` | 提供保留 Python 签名的调用代理、参数绑定及处理器自动注册机制 |
| `codec.py` | 按声明类型执行编解码，并复用消息与会话对象的转换器 |
| `base.py` | 管理 Peer 调用、结果关联、并发分发、信号扇出及生命周期 |
| `backend.py` | 定义完整后端协议，并依据配置装配相互一致的 Registry 与 Transport |
| `transport.py` | 定义介质无关的消息信封、批量投递结果及 `MessageTransport` 协议 |
| `peer.py` | 定义进程身份、目标选择、Registry 协议及信号发送结果 |
| `database.py` | 实现数据库 Registry、任务传输、原子认领及实例失效后的任务终结 |
| `websocket.py` | 实现基于 `httpx-ws` 的客户端、ASGI Hub、连接鉴权、实时路由及背压控制 |
| `memory.py` | 提供不依赖 ORM 的后端接口测试环境，不作为生产配置选项 |
| `errors.py` | 定义可跨进程识别的异常类型 |
| `client.py` | 解析平台上下文，自动绑定平台接口，并处理推送、私信等特殊逻辑 |
| `server.py` | 实现消息解析、事件分发、模块查询与钩子调用等服务端接口 |
| `reporting.py` | 提交配置中指定的错误报告，并避免错误报告流程等待自身完成 |
<<< END U008260 >>>
<<< UNIT U008261 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:29-31 | ctx=组件与职责 >>>
数据库后端使用 `JobQueuePeersTable` 以 `peer_id` 为主键记录每个进程实例。`JobQueuesTable` 中的
`target_peer`、`source_peer_id`、`correlation_id`、`message_kind`、`expects_response` 与 `claimed_by`
分别记录投递目标、来源实例、关联标识、消息类别、是否需要响应及实际认领者。
<<< END U008261 >>>
<<< UNIT U008262 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:33-34 | ctx=组件与职责 >>>
新增后端必须同时实现 `JobQueueBackend`、`PeerRegistry` 与 `MessageTransport` 接口规范。Registry 负责注册、
续租或连接保活、权威实例发现及路由选择。Transport 负责请求、响应、批量投递和本地放弃状态的处理。
<<< END U008262 >>>
<<< UNIT U008263 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:36-37 | ctx=组件与职责 >>>
接收端通过 `respond(request, response)` 返回响应，原始请求提供无状态传输所需的返回路由上下文。
`abandon()` 仅表示调用方停止等待并要求后端尽力清理，不能解释为已经撤销远端执行。
<<< END U008263 >>>
<<< UNIT U008264 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:39-39 | ctx=配置与后端选择 >>>
## 配置与后端选择
<<< END U008264 >>>
<<< UNIT U008265 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:41-42 | ctx=配置与后端选择 >>>
JobQueue 配置独立存放于 `config/jobqueue.toml`。`[jobqueue].jobqueue_backend` 用于选择整套后端，
有效值为 `database` 和 `websocket`。`[jobqueue_secret]` 仅存放 WebSocket Hub 访问令牌等敏感配置。
<<< END U008265 >>>
<<< UNIT U008266 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:44-44 | ctx=配置与后端选择 >>>
所有参与同一逻辑集群的进程必须使用相同后端，运行期间不支持热切换。
<<< END U008266 >>>
<<< UNIT U008267 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:46-48 | ctx=配置与后端选择 >>>
未知值会明确终止初始化，
WebSocket Hub 无法连接或鉴权失败时亦不会自动回退至数据库，以免同一集群同时形成两套互不一致的
通信通道。
<<< END U008267 >>>
<<< UNIT U008268 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:50-51 | ctx=配置与后端选择 >>>
新生成的配置默认选择 `websocket`，该后端亦是项目的推荐选项。已明确配置为 `database` 的部署不会被自动
改写或静默切换。
<<< END U008268 >>>
<<< UNIT U008269 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:53-54 | ctx=配置与后端选择 >>>
当守护进程检测到 JobQueue 使用 `database` 且主数据库为 SQLite 时，会在数据库初始化前
输出一次非阻断警告，但仍严格按现有配置启动。
<<< END U008269 >>>
<<< UNIT U008270 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:56-56 | ctx=配置与后端选择 >>>
两种生产后端的主要差异如下：
<<< END U008270 >>>
<<< UNIT U008271 | md-table | packages/akari-bot-core/akaribot/core/queue/README.md:58-64 | ctx=配置与后端选择 >>>
| 比较项 | `database` | `websocket` |
| --- | --- | --- |
| 部署要求 | 复用共享数据库，无须另行部署 Hub | 需要一个独立 Hub，并维持各 Peer 的长连接 |
| 投递特性 | 轮询数据库。尚未过期的队列记录可供稍后启动的消费者认领 | 实时在线路由。不持久化离线任务或处理中的结果 |
| 资源与时延 | 轮询、写入及终态清理会增加数据库 CPU 与 I/O 负载，时延受轮询间隔影响 | 不产生数据库轮询负载，通常具有更低时延，但需承担连接、背压和 Hub 运维成本 |
| 适用范围 | 使用 MySQL 等可并发写入的共享数据库，或明确接受写锁竞争的 SQLite 低负载部署 | 默认与推荐选项。适用于 SQLite、高频 RPC、信号广播及同类多实例并行运行 |
| 故障边界 | 受共享数据库可用性与容量限制 | Hub 重启或连接中断会丢失内存中的拓扑及未完成的关联，远程部署还须配置令牌与 TLS |
<<< END U008271 >>>
<<< UNIT U008272 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:66-67 | ctx=配置与后端选择 >>>
数据库后端不提供 exactly-once、无限期持久化或副作用请求的安全自动重试。WebSocket 后端也不以实时性
换取此类保证。Hub 无法确定投递结果时会报告 unknown，而不会擅自重试。
<<< END U008272 >>>
<<< UNIT U008273 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:69-70 | ctx=配置与后端选择 >>>
即使 JobQueue 选择 WebSocket，
业务模型和模块数据库仍可能要求初始化数据库连接，因此该选项不属于全局数据库开关。
<<< END U008273 >>>
<<< UNIT U008274 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:72-72 | ctx=SQLite 写锁边界 >>>
### SQLite 写锁边界
<<< END U008274 >>>
<<< UNIT U008275 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:74-75 | ctx=SQLite 写锁边界 >>>
当主数据库为 SQLite 时，`database` 后端与业务模型共用同一数据库文件。SQLite 即使在 WAL 模式下仍只允许
同一时刻存在一个写者。WAL 主要改善读写并行，不会把单写者模型变为多写者模型。
<<< END U008275 >>>
<<< UNIT U008276 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:77-79 | ctx=SQLite 写锁边界 >>>
JobQueue 的任务投递、原子
认领、Peer 心跳、结果回写及清理均会与业务写入竞争该写锁。因此，以下措施只能减少锁冲突，不能承诺
消除 `database is locked` 错误：
<<< END U008276 >>>
<<< UNIT U008277 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:81-82 | ctx=SQLite 写锁边界 >>>
- 所有 SQLite 连接均先设置 30 秒 `busy_timeout`，再启用 WAL，使并发启动期间的 WAL 初始化也受等待策略保护。
- 任务认领始终使用带 `pending` 状态条件的原子更新，并将每轮候选记录限制为 100 条，避免积压时单轮无界
<<< END U008277 >>>
<<< UNIT U008278 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:83-83 | ctx=SQLite 写锁边界 >>>
  扫描与连续写入。
<<< END U008278 >>>
<<< UNIT U008279 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:84-84 | ctx=SQLite 写锁边界 >>>
- 终态结果在调用方读取后立即删除，不需要响应的任务在完成时直接删除，并由定时清理回收调用方异常退出后
<<< END U008279 >>>
<<< UNIT U008280 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:85-85 | ctx=SQLite 写锁边界 >>>
  残留的终态记录。
<<< END U008280 >>>
<<< UNIT U008281 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:86-86 | ctx=SQLite 写锁边界 >>>
- Peer 失效时的状态切换与直投任务终结仍保留在同一事务中。该路径会延长少量写锁的持有时间，但不应为缩短锁时间而
<<< END U008281 >>>
<<< UNIT U008282 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:87-87 | ctx=SQLite 写锁边界 >>>
  破坏 Peer 状态与投递结果的一致性。
<<< END U008282 >>>
<<< UNIT U008283 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:89-90 | ctx=SQLite 写锁边界 >>>
需要降低 SQLite 锁竞争时，应优先将 JobQueue 切换为 `websocket`。该调整只移除 JobQueue 自身对 SQLite 的轮询与写入，
不会消除业务模型之间原有的 SQLite 写锁竞争。
<<< END U008283 >>>
<<< UNIT U008284 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:92-93 | ctx=SQLite 写锁边界 >>>
如果必须持续使用数据库后端并承载多进程高频写入，应使用 MySQL 等
适合并发写入的共享数据库。
<<< END U008284 >>>
<<< UNIT U008285 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:95-95 | ctx=SQLite 写锁边界 >>>
`PeerSelector` 支持按实例、节点、角色、service 与 capability 的交集筛选目标，并可显式排除指定实例。
<<< END U008285 >>>
<<< UNIT U008286 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:97-98 | ctx=SQLite 写锁边界 >>>
`InMemoryJobQueueBackend` 由同一测试集群中的多个 Peer 共享 `InMemoryBroker`，用于验证 Runtime 不再隐式
依赖数据库模型。该实现不提供跨进程通信、持久化或生产可靠性保证，配置工厂不会接受 `memory`。
<<< END U008286 >>>
<<< UNIT U008287 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:100-100 | ctx=实例身份、定位与发现 >>>
## 实例身份、定位与发现
<<< END U008287 >>>
<<< UNIT U008288 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:102-102 | ctx=实例身份、定位与发现 >>>
每个进程具有两层身份：
<<< END U008288 >>>
<<< UNIT U008289 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:104-104 | ctx=实例身份、定位与发现 >>>
- `JobQueueBase.name` 是在每次进程生命周期内生成的唯一 `peer_id`。以该标识投递的任务仅能由对应
<<< END U008289 >>>
<<< UNIT U008290 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:105-105 | ctx=实例身份、定位与发现 >>>
  实例认领。PID 作为诊断信息随实例记录，但不参与定位。
<<< END U008290 >>>
<<< UNIT U008291 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:106-106 | ctx=实例身份、定位与发现 >>>
- `PeerIdentity.service` 是稳定的服务组标识，例如 `Server` 或 `QQ`。同一服务组中的实例共同监听
<<< END U008291 >>>
<<< UNIT U008292 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:107-108 | ctx=实例身份、定位与发现 >>>
  该标识。数据库后端通过原子 `claim()`，WebSocket 后端通过 Hub 集中选择目标，确保每条普通 RPC 只会
  被分配给一个实例，从而实现任播（anycast）负载均衡。
<<< END U008292 >>>
<<< UNIT U008293 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:110-111 | ctx=实例身份、定位与发现 >>>
`node_id` 是可配置的部署节点标签。正常启动时，`pre_init` 会在创建任何 Hub、Bot 或 Server 子进程之前
检查 `[jobqueue].jobqueue_node_id`。
<<< END U008293 >>>
<<< UNIT U008294 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:113-114 | ctx=实例身份、定位与发现 >>>
该值不存在、仍为占位符或仅包含空白字符时，系统生成一个 UUID，原子写回
配置文件后再继续启动。
<<< END U008294 >>>
<<< UNIT U008295 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:116-117 | ctx=实例身份、定位与发现 >>>
因此，共用同一配置目录的进程会取得相同且可跨重启保持稳定的 `node_id`，而每个进程
实例仍由独立的 `peer_id` 唯一标识。系统不会从计算机名、宿主机环境或其他设备信息中读取或推导该值。
<<< END U008295 >>>
<<< UNIT U008296 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:119-120 | ctx=实例身份、定位与发现 >>>
若需要按物理节点或部署单元选择一组 Peer，可为相关进程共用配置，也可显式设置相同且不包含敏感信息的
`jobqueue_node_id`。调用 `configure_peer()` 时显式传入的 `node_id` 具有最高优先级。
<<< END U008296 >>>
<<< UNIT U008297 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:122-124 | ctx=实例身份、定位与发现 >>>
绕过正常守护进程直接
启动单个 Peer，且配置值仍为空时，运行时仍会为该进程生成临时 UUID 作为回退，但不会将其视为常规
部署路径。配置值最长为 128 个字符，修改后须重启相关进程才会反映到 Peer Registry。
<<< END U008297 >>>
<<< UNIT U008298 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:126-127 | ctx=实例身份、定位与发现 >>>
同一 service 表示一组能够相互替代并处理同类任务的实例。节点标签、PID、capabilities 与自定义 metadata
均独立记录，因此后续可以在不修改 RPC 业务载荷的前提下增加权重、分片或区域等路由约束。
<<< END U008298 >>>
<<< UNIT U008299 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:129-130 | ctx=实例身份、定位与发现 >>>
无法相互替代的平台账号应使用不同的 service。如确需归入同一 service，则必须在启用多实例之前
补充能够区分账号或分片的路由条件。
<<< END U008299 >>>
<<< UNIT U008300 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:132-134 | ctx=实例身份、定位与发现 >>>
`check_job_queue()` 启动时依次完成以下操作：以 `starting` 状态注册实例、启用实例定位、切换为
`ready`、读取完整拓扑，并向现有在线实例广播 `peer.ready`。运行期间，每 15 秒续订一次租约，
每 10 秒依据当前后端的权威 Registry 执行一次完整拓扑对账。
<<< END U008300 >>>
<<< UNIT U008301 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:136-137 | ctx=实例身份、定位与发现 >>>
正常关闭时，实例先通过 `peer.draining`
停止接收新任务，完成执行中任务的清理后再广播 `peer.stopped`。异常退出则在 45 秒租约到期后被识别。
<<< END U008301 >>>
<<< UNIT U008302 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:139-139 | ctx=实例身份、定位与发现 >>>
保活信息不定向发送至某个 Server，因此多个 Server 可以依据同一权威注册表获得一致的在线视图。
<<< END U008302 >>>
<<< UNIT U008303 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:141-142 | ctx=实例身份、定位与发现 >>>
数据库热重载等维护操作会将实例状态切换为 `maintenance`，并广播 `peer.maintenance`，使该实例暂时退出
稳定路由。连接恢复后，实例重新注册为 `ready` 并广播 `peer.resumed`，从而避免在维护期间接收新消息。
<<< END U008303 >>>
<<< UNIT U008304 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:144-145 | ctx=实例身份、定位与发现 >>>
所有生命周期信号均须由其载荷中对应的 `peer_id` 发出，并且仅在信号内容与 Registry 当前状态一致时
更新本地缓存。延迟到达的 `ready`、`resumed` 或 `stopped` 信号不得覆盖更新后的权威状态。
<<< END U008304 >>>
<<< UNIT U008305 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:147-149 | ctx=实例身份、定位与发现 >>>
同一进程内的
轮询器异常重启并以原 `peer_id` 重新取得有效租约时，则允许经 Registry 确认的新 `ready` 状态覆盖本地
`stopped` 缓存。
<<< END U008305 >>>
<<< UNIT U008306 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:151-151 | ctx=WebSocket Hub 部署 >>>
## WebSocket Hub 部署
<<< END U008306 >>>
<<< UNIT U008307 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:153-154 | ctx=WebSocket Hub 部署 >>>
WebSocket 后端由一个独立 Hub 和任意数量的 Peer 连接组成。Hub 不属于业务 Server，不执行模块逻辑，
其职责仅限于维护连接身份、权威 Peer 状态、任播选择、逐实例信号发送和未完成响应的关联。
<<< END U008307 >>>
<<< UNIT U008308 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:156-158 | ctx=WebSocket Hub 部署 >>>
内置部署模式下，
机器人守护进程会先启动名为 `jobqueue-hub` 的独立子进程，确认监听端口就绪后再启动 Bot 与 Server。
关闭时则先停止 Bot 和 Server，最后停止 Hub，以便在退出阶段继续传递响应与生命周期信号。
<<< END U008308 >>>
<<< UNIT U008309 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:173-175 | ctx=WebSocket Hub 部署 >>>
`jobqueue_websocket_mode` 明确 Hub 的部署模式，其中 `embedded` 表示由机器人守护进程启动内置 Hub，
`external` 表示各 Peer 仅连接独立部署的外部 Hub。部署模式不得依据 URL 的主机地址推断，以免本机外部 Hub
被误判为内置 Hub。
<<< END U008309 >>>
<<< UNIT U008310 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:177-179 | ctx=WebSocket Hub 部署 >>>
`jobqueue_websocket_url` 是 WebSocket 地址的唯一配置来源。在 `embedded` 模式下，
Hub 的监听主机、监听端口和协议路径均从该 URL 解析，各 Peer 亦连接同一地址。在 `external` 模式下，
该 URL 仅表示 Peer 的连接地址。
<<< END U008310 >>>
<<< UNIT U008311 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:181-182 | ctx=WebSocket Hub 部署 >>>
正常启动时，如果 `jobqueue_websocket_token` 不存在、仍为占位符或仅包含空白字符，`pre_init` 会生成一个
具有 256 位随机熵的 URL-safe 密钥并写回 `[jobqueue_secret]`，随后 Hub、Bot 与 Server 子进程只读同一值。
<<< END U008311 >>>
<<< UNIT U008312 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:184-184 | ctx=WebSocket Hub 部署 >>>
清空该字段会在下次启动时轮换密钥。轮换后，使用旧密钥的 Peer 将无法通过鉴权。
<<< END U008312 >>>
<<< UNIT U008313 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:186-186 | ctx=WebSocket Hub 部署 >>>
自动生成的密钥只适用于共用同一配置目录的本机部署。使用外部 Hub 或多个独立配置目录时，必须将同一密钥安全地配置到全部参与节点。
<<< END U008313 >>>
<<< UNIT U008314 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:188-190 | ctx=WebSocket Hub 部署 >>>
内置 Hub 不负责 TLS 终止，因此 `embedded` 模式仅接受使用 `ws` 的回环地址。连接非回环外部 Hub 时必须
使用 `wss` 和共享访问令牌。生产环境宜通过反向代理终止 TLS，
并将 Hub 本身限制在受信网络内。
<<< END U008314 >>>
<<< UNIT U008315 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:192-193 | ctx=WebSocket Hub 部署 >>>
单一 `embedded` 配置不表达“监听通配地址，但通过另一域名连接”的双地址
部署。
<<< END U008315 >>>
<<< UNIT U008316 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:195-196 | ctx=WebSocket Hub 部署 >>>
多节点、反向代理或其他需要区分监听地址与连接地址的场景应使用 `external` 模式，由外部部署系统分别
管理 Hub 的监听端点与公开连接地址。
<<< END U008316 >>>
<<< UNIT U008317 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:198-199 | ctx=WebSocket Hub 部署 >>>
Hub 在握手阶段将连接绑定至唯一 `peer_id`，此后一律以连接身份覆盖请求载荷中自行声明的 `source_peer_id`。
重复连接同一 `peer_id`、身份越权修改、非目标 Peer 的响应及畸形协议帧均会被拒绝。
<<< END U008317 >>>
<<< UNIT U008318 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:201-202 | ctx=WebSocket Hub 部署 >>>
使用外部 Hub 时，应将 `jobqueue_websocket_mode` 设置为 `external`，并确保所有 Peer 配置相同的连接 URL
与访问令牌。项目所附 Hub 可通过 `uv run python -m akaribot.core.queue.websocket` 独立启动。
<<< END U008318 >>>
<<< UNIT U008319 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:204-206 | ctx=WebSocket Hub 部署 >>>
此时应在 Hub 主机上
提供适用于其监听端点的独立配置。该进程不负责自动发现其他 Hub，也不提供多 Hub 状态复制。同一逻辑集群
在任一时刻必须连接至同一个权威 Hub。
<<< END U008319 >>>
<<< UNIT U008320 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:208-209 | ctx=WebSocket Hub 部署 >>>
WebSocket 后端属于实时、非持久化传输。Hub 对每个 Peer 设置有界发送队列，并限制单帧大小。目标队列已满时，
新投递会被明确拒绝。
<<< END U008320 >>>
<<< UNIT U008321 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:211-213 | ctx=WebSocket Hub 部署 >>>
控制命令在发送后超时则按 unknown 处理，不得据此自动重试有外部副作用的请求。目标
断线、主动注销或租约过期时，Hub 会立即将其未完成直投请求终结为 unavailable。来源断线时，Hub 删除其
响应关联状态。
<<< END U008321 >>>
<<< UNIT U008322 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:215-216 | ctx=WebSocket Hub 部署 >>>
超过请求 deadline 的关联状态会被及时释放，并向仍在线的来源返回 timeout。此清理不会撤销
已经开始的远端副作用。Hub 自身重启会丢失全部 Peer 与未完成的请求，所有 Peer 必须重新连接并注册。
<<< END U008322 >>>
<<< UNIT U008323 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:218-218 | ctx=RPC 调用 >>>
## RPC 调用
<<< END U008323 >>>
<<< UNIT U008324 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:236-237 | ctx=RPC 调用 >>>
同一 service 下的多个 Peer 会竞争认领普通 RPC。需要保持业务键路由亲和性的调用使用 `ServiceRoute`
描述 service、角色与路由键。
<<< END U008324 >>>
<<< UNIT U008325 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:239-240 | ctx=RPC 调用 >>>
任务投递前，运行时会查询权威 Registry，并通过 Rendezvous Hash 从
`ready` 实例中稳定选择一个目标。
<<< END U008325 >>>
<<< UNIT U008326 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:242-243 | ctx=RPC 调用 >>>
数据库后端在不存在匹配实例时可以将任务保留在 service 任播队列，
以便由稍后启动的消费者认领。WebSocket 后端不保留离线任务，会明确返回 unavailable。
<<< END U008326 >>>
<<< UNIT U008327 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:245-246 | ctx=RPC 调用 >>>
因此，即使本地 `Alive` 缓存尚未收到 `draining` 信号，新任务也不会继续直接投递至正在关闭的实例。
路由查询耗时计入 RPC deadline。
<<< END U008327 >>>
<<< UNIT U008328 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:248-250 | ctx=RPC 调用 >>>
数据库后端允许 Client 发往尚未启动的 Server 的任务暂时保留在 service
队列中。不具备离线持久化能力的后端可以立即返回 unavailable。Server 发往无在线 Client 的主动平台操作
仍会立即失败，避免产生长期无人认领的平台任务。
<<< END U008328 >>>
<<< UNIT U008329 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:252-254 | ctx=RPC 调用 >>>
入站 `SessionInfo` 额外记录 `owner_peer_id`。删除消息、释放上下文、添加反应等依赖平台 SDK 上下文的
操作会直接投递至最初接收消息的 Client 实例。Server 创建的主动会话不设置 owner，其路由依据场景键在
对应 service 内稳定执行。
<<< END U008329 >>>
<<< UNIT U008330 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:256-256 | ctx=信号广播 >>>
## 信号广播
<<< END U008330 >>>
<<< UNIT U008331 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:258-259 | ctx=信号广播 >>>
广播信号在队列中按目标分别存储，不属于多个消费者竞争认领的单条共享队列记录。发送端首先通过
`PeerSelector` 获取发送时刻所有符合条件的 `ready` 实例快照，随后为每个目标分别创建一条实例直投记录。
<<< END U008331 >>>
<<< UNIT U008332 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:261-263 | ctx=信号广播 >>>
所有投递共享同一个
`event_id`，但各自具有独立的任务 ID、认领者、终态与 ACK。因此，任一目标执行失败不会影响其他目标
接收或确认同一信号。
<<< END U008332 >>>
<<< UNIT U008333 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:286-287 | ctx=信号广播 >>>
`.emit()` 投递不要求响应。数据库后端会在各目标处理完成后删除相应队列行。`.gather()` 要求逐实例 ACK，
数据库终态结果由发起方读取后立即删除。
<<< END U008333 >>>
<<< UNIT U008334 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:289-291 | ctx=信号广播 >>>
批量发送允许后端逐项报告 accepted、rejected 与 unknown。`SignalReceipt` 仅将明确接受的投递列入
`deliveries`，拒绝原因和接受状态未知的 Peer 分别列入 `errors`
与 `unknown`。其中的任务 ID 仅用于关联本次投递，不表示后端会将其持久保留。
<<< END U008334 >>>
<<< UNIT U008335 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:293-296 | ctx=信号广播 >>>
同一信号可以在单个进程内注册多个本地订阅者。底层接口亦可直接调用
`JobQueueBase.emit_signal()` 或 `JobQueueBase.gather_signal()`。业务代码原则上应优先声明强类型
`SignalMethod`。接收端可以通过 `current_request`，或原始 `on_signal` 接口提供的 `SignalContext`，
读取可信的 `source_peer_id`。
<<< END U008335 >>>
<<< UNIT U008336 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:298-299 | ctx=信号广播 >>>
信号处理器必须具备幂等性。用于同步配置、模块状态或其他版本化数据的信号应携带 version 或 epoch，
并以持久化状态为最终依据，不得仅依赖信号维持一致性。
<<< END U008336 >>>
<<< UNIT U008337 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:301-301 | ctx=多实例支持范围与约束 >>>
## 多实例支持范围与约束
<<< END U008337 >>>
<<< UNIT U008338 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:303-304 | ctx=多实例支持范围与约束 >>>
JobQueue 层支持同一 service 下多个 Client 或 Server 的注册、发现、实例直投、稳定分流与广播快照。
当前守护进程和配置系统仍仅会启动每类进程的单个实例。在正式启用多个 Server 之前，还需完成以下工作：
<<< END U008338 >>>
<<< UNIT U008339 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:306-310 | ctx=多实例支持范围与约束 >>>
- 为 Scheduler 及其他仅应执行一次的后台任务引入 Leader Election 或分布式去重机制。
- 将模块加载、卸载与热重载等集群控制操作调整为逐 Server 扇出，并通过共享 epoch 完成状态对账。
- 明确 Server 故障后，进程内等待会话与临时状态的迁移方案或失效策略。
- 在生产规模下使用 MySQL 等适合多进程并发竞争的数据库，避免 SQLite 高频轮询导致锁竞争。
- 为具有外部副作用的业务处理器设计幂等键，因为队列仅保证原子认领，不提供 exactly-once 语义。
<<< END U008339 >>>
<<< UNIT U008340 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:312-313 | ctx=多实例支持范围与约束 >>>
在同类型 Client 并行运行时，JobQueue 可以将入站会话相关操作定向返回原实例，并在同一 service 内对
主动任务进行稳定分流。
<<< END U008340 >>>
<<< UNIT U008341 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:315-316 | ctx=多实例支持范围与约束 >>>
但是，如果多个实例连接同一个平台账号，则平台 SDK 入口处的重复消费、分片租约或主备接管仍须由适配器层
实现。JobQueue 仅负责分流已经进入系统的任务，不负责消除平台侧重复产生的事件。
<<< END U008341 >>>
<<< UNIT U008342 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:318-319 | ctx=多实例支持范围与约束 >>>
信号广播仅面向发送时刻在线的实例，不提供历史事件重放。对于离线期间亦须补齐的状态，应将其持久化，
并由 Peer 在启动后依据 version 或 epoch 主动对账。信号仅用于缩短在线实例感知状态变化的延迟。
<<< END U008342 >>>
<<< UNIT U008343 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:321-323 | ctx=多实例支持范围与约束 >>>
普通模块继续使用 `MessageSession` 提供的便利方法。成员管理接口的 `wait` 参数语义不变，内部根据
参数选择普通调用或 `.submit()`。`wait=True` 时，成功返回 `None`，失败则抛出异常，不返回
`{"success": True}`。发送接口返回消息 ID 列表，空列表仍表示平台未完成投递。
<<< END U008343 >>>
<<< UNIT U008344 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:325-326 | ctx=多实例支持范围与约束 >>>
`client_init()` 与 Server 的 `main()` 会显式设置进程的默认 Peer。导入共享接口定义不会隐式确定进程角色，
也不会同时导入 Server 处理器或平台 SDK。
<<< END U008344 >>>
<<< UNIT U008345 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:328-329 | ctx=多实例支持范围与约束 >>>
请求处理期间，运行时通过 `ContextVar` 确定当前 Peer。嵌套反向调用继续使用同一结果接收器。测试代码
可以通过 `method.using(TestPeer)` 显式指定 Peer。
<<< END U008345 >>>
<<< UNIT U008346 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:331-331 | ctx=扩展接口 >>>
## 扩展接口
<<< END U008346 >>>
<<< UNIT U008347 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:333-333 | ctx=扩展接口 >>>
普通平台操作应先在 `ContextManager` 中声明能力并由各适配器实现，随后在 `PlatformAPI` 中暴露：
<<< END U008347 >>>
<<< UNIT U008348 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:339-340 | ctx=扩展接口 >>>
接口签名直接取自 `ContextManager`，接收端会自动解析上下文并转发调用，无须另行编写 Server 调用封装、
参数字典或 Client 处理器。同步的上下文 hold/release 方法同样通过该机制提供，跨进程调用始终可以 await。
<<< END U008348 >>>
<<< UNIT U008349 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:342-342 | ctx=扩展接口 >>>
服务端操作应在 `ServerAPI` 中声明具有完整类型注解的方法，并在 `server.py` 中绑定具体实现：
<<< END U008349 >>>
<<< UNIT U008350 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:356-357 | ctx=扩展接口 >>>
业务实现接收类型化参数并直接返回业务值。如果参数名称、参数种类或默认值与接口声明不一致，处理器注册将在
启动阶段立即失败。
<<< END U008350 >>>
<<< UNIT U008351 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:359-359 | ctx=扩展接口 >>>
重复注册同样会被拒绝。运行时会在发送前和接收后分别执行参数绑定与编解码校验。
<<< END U008351 >>>
<<< UNIT U008352 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:361-361 | ctx=扩展接口 >>>
业务参数不得使用 `*args`。需要动态扩展参数时，应使用具有类型注解的 `**kwargs`。
<<< END U008352 >>>
<<< UNIT U008353 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:363-363 | ctx=扩展接口 >>>
动态 Hook 的参数与返回值支持 JSON 标量、列表、字符串键字典，以及已注册的消息、会话、事件和能力对象。
<<< END U008353 >>>
<<< UNIT U008354 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:365-366 | ctx=扩展接口 >>>
字典将作为整体编码，以避免与内部类型标记发生冲突。未注册的 Python 对象会被拒绝，不会通过 pickle、
动态导入或任意对象反射在进程之间传递。
<<< END U008354 >>>
<<< UNIT U008355 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:368-368 | ctx=错误、超时与关闭语义 >>>
## 错误、超时与关闭语义
<<< END U008355 >>>
<<< UNIT U008356 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:370-370 | ctx=错误、超时与关闭语义 >>>
- `RpcRemoteError` 保留远端异常类型。所有 RPC 异常均包含方法名称、目标与请求 ID。等待型调用的异常还会保留
<<< END U008356 >>>
<<< UNIT U008357 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:371-373 | ctx=错误、超时与关闭语义 >>>
  远端执行 traceback，并在其后附加请求来源、Peer 与发起进程的调用栈。`.traceback` 是合并后的诊断文本，
  `.remote_traceback` 尽可能保留纯远端片段。`.submit()` 和错误信号不等待响应，同样携带
  同一份调用上下文，便于在接收端定位发起位置。
<<< END U008357 >>>
<<< UNIT U008358 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:374-374 | ctx=错误、超时与关闭语义 >>>
- `RpcMethodNotFoundError`、`RpcUnavailableError`、`RpcTimeoutError`、`RpcCancelledError` 与
<<< END U008358 >>>
<<< UNIT U008359 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:375-375 | ctx=错误、超时与关闭语义 >>>
  `RpcProtocolError` 分别表示方法未注册、目标不可达、请求过期、远端任务取消及协议错误。
<<< END U008359 >>>
<<< UNIT U008360 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:376-377 | ctx=错误、超时与关闭语义 >>>
- `None`、`False`、空列表与空字典均属于合法的成功返回值，不参与错误状态判断。
- 查询与信号的默认超时时间为 30 秒，普通操作为 120 秒，消息处理、消息发送及长操作最长为 7200 秒。
<<< END U008360 >>>
<<< UNIT U008361 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:378-378 | ctx=错误、超时与关闭语义 >>>
  每个请求具有独立的 deadline，不继承已经过期的父请求期限，以确保 `finally` 中的资源释放操作仍可执行。
<<< END U008361 >>>
<<< UNIT U008362 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:379-379 | ctx=错误、超时与关闭语义 >>>
- timeout 与 deadline 必须为正的有限数值或有限时间戳。布尔值虽然在 Python 中属于整数子类，仍将被明确
<<< END U008362 >>>
<<< UNIT U008363 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:380-381 | ctx=错误、超时与关闭语义 >>>
  拒绝。响应错误码等协议字段亦须符合约定类型，畸形数据统一转换为 `RpcProtocolError`，不得泄漏底层
  类型异常。
<<< END U008363 >>>
<<< UNIT U008364 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:382-382 | ctx=错误、超时与关闭语义 >>>
- 调用方取消等待时会调用后端的 `abandon()` 尽力清理本地及尚可撤销的传输状态，但不保证撤销已经开始的
<<< END U008364 >>>
<<< UNIT U008365 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:383-383 | ctx=错误、超时与关闭语义 >>>
  远端副作用。远端处理仍受该请求自身 deadline 的约束，其最终完成状态可能无法再由调用方取得。
<<< END U008365 >>>
<<< UNIT U008366 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:384-384 | ctx=错误、超时与关闭语义 >>>
- 投递操作可能在后端已经接受消息后才报告取消或连接异常。等待型调用在此情况下按“投递结果未知”处理，
<<< END U008366 >>>
<<< UNIT U008367 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:385-385 | ctx=错误、超时与关闭语义 >>>
  并以预先生成的任务 ID 尝试清理。该操作不改变远端副作用可能已经发生的事实。
<<< END U008367 >>>
<<< UNIT U008368 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:386-386 | ctx=错误、超时与关闭语义 >>>
- 数据库后端的原子认领和 WebSocket Hub 的集中目标选择可以避免同一投递同时分配给多个消费者，但均不提供
<<< END U008368 >>>
<<< UNIT U008369 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:387-388 | ctx=错误、超时与关闭语义 >>>
  严格 FIFO 或 exactly-once 保证。
  如果外部副作用已经完成而响应丢失，则最终执行结果可能无法确定，因此不得自动重试发送、禁言等操作。
<<< END U008369 >>>
<<< UNIT U008370 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:389-389 | ctx=错误、超时与关闭语义 >>>
- `.submit()` 与 `.emit()` 不等待远端结果。数据库后端在处理器进入终态后直接删除任务行。等待型 RPC 与
<<< END U008370 >>>
<<< UNIT U008371 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:390-390 | ctx=错误、超时与关闭语义 >>>
  `.gather()` 在发起方读取终态结果后立即删除任务行。终态记录不是审计日志，不应依赖其持久存在。
<<< END U008371 >>>
<<< UNIT U008372 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:391-391 | ctx=错误、超时与关闭语义 >>>
- 数据库后端已经将终态结果读入内存后，若删除操作发生瞬时故障，应优先交付有效结果并记录清理异常，避免
<<< END U008372 >>>
<<< UNIT U008373 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:392-392 | ctx=错误、超时与关闭语义 >>>
  结果泵退出或将成功结果降级为 unavailable。未删除的终态行仍由定时任务回收。
<<< END U008373 >>>
<<< UNIT U008374 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:393-393 | ctx=错误、超时与关闭语义 >>>
- 调用方异常退出等情况可能遗留未消费的终态结果。定时清理仅作为备用手段，并通过 `(status, timestamp)`
<<< END U008374 >>>
<<< UNIT U008375 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:394-394 | ctx=错误、超时与关闭语义 >>>
  索引限制数据库扫描成本。WebSocket Hub 不持久化终态结果，来源连接关闭后会直接释放相关状态。
<<< END U008375 >>>
<<< UNIT U008376 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:395-396 | ctx=错误、超时与关闭语义 >>>
- 队列轮询与处理器并发运行。处理器等待反向调用时，不会阻塞结果接收。
- 进入维护状态时，实例停止认领新请求，但继续接收处理中的结果。待处理器全部结束后，方可进入需要独占资源的
<<< END U008376 >>>
<<< UNIT U008377 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:397-397 | ctx=错误、超时与关闭语义 >>>
  维护操作。数据库热重载在此阶段独占数据库连接。
<<< END U008377 >>>
<<< UNIT U008378 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:398-398 | ctx=错误、超时与关闭语义 >>>
- 同一任务可以重入维护窗口。不同任务发起的维护窗口按实例串行执行，以避免不可重入锁导致死锁，或后续
<<< END U008378 >>>
<<< UNIT U008379 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:399-399 | ctx=错误、超时与关闭语义 >>>
  维护在 Registry 已恢复 `ready` 状态后继续运行。
<<< END U008379 >>>
<<< UNIT U008380 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:400-401 | ctx=错误、超时与关闭语义 >>>
- 关闭过程中，结果接收器会持续运行，直至会话与后台任务清理完成，随后才停止接收并关闭 JobQueue 后端。
- 队列轮询器异常退出时，实例会主动撤销 Registry 注册并释放本地等待方，不继续以可路由但无法收发任务的
<<< END U008380 >>>
<<< UNIT U008381 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:402-402 | ctx=错误、超时与关闭语义 >>>
  状态存活。Client 监控器可在状态清理完成后重新启动轮询器。Server 则将异常上抛至进程监控逻辑。
<<< END U008381 >>>
<<< UNIT U008382 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:403-403 | ctx=错误、超时与关闭语义 >>>
- 实例正常退出或租约到期时，发往该实例的未完成直投任务会被标记为 unavailable。数据库中尚未认领的
<<< END U008382 >>>
<<< UNIT U008383 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:404-406 | ctx=错误、超时与关闭语义 >>>
  service 任播任务不会因单个实例退出而被删除，仍可由同组其他实例认领。实例状态更新与其直投任务终结
  位于同一数据库事务内。WebSocket 请求一经 Hub 选择目标即成为实例直投，目标断线后不会重新分配，以免
  非幂等处理器被重复执行。
<<< END U008383 >>>
<<< UNIT U008384 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:407-407 | ctx=错误、超时与关闭语义 >>>
- 消息入口必须等待 Server 完成处理后再释放 Client 侧的 SDK 上下文，不得改为 `.submit()`。
<<< END U008384 >>>
<<< UNIT U008385 | md-heading | packages/akari-bot-core/akaribot/core/queue/README.md:409-409 | ctx=协议升级与验证 >>>
## 协议升级与验证
<<< END U008385 >>>
<<< UNIT U008386 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:411-412 | ctx=协议升级与验证 >>>
协议 v2 属于破坏性替换。数据库从 v4 升级至 v5 时，将直接删除既有 `job_queues` 表，并依据当前
ORM 模型重新创建该表。
<<< END U008386 >>>
<<< UNIT U008387 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:414-415 | ctx=协议升级与验证 >>>
旧表中的待认领、执行中及已完成任务均不予保留。包括 `job_queue_peers` 在内的新增表亦由当前模型统一
创建。
<<< END U008387 >>>
<<< UNIT U008388 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:417-418 | ctx=协议升级与验证 >>>
新旧协议请求不得混合处理。升级前必须停止全部 Bot 与 Server 进程，并在数据库迁移完成后统一启动。
未知协议或旧协议请求会明确失败，不会被解释为新版本业务参数。
<<< END U008388 >>>
<<< UNIT U008389 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:420-421 | ctx=协议升级与验证 >>>
当前队列不承诺在机器人整体重启期间保留活动请求。单个 Server 退出时不得清空全局队列表，以免影响
同一 service 下其他实例正在处理或等待认领的任务。
<<< END U008389 >>>
<<< UNIT U008390 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:423-423 | ctx=协议升级与验证 >>>
自研测试框架的相关验证入口如下。执行时必须设置 `CI=1` 与 `PYTHONIOENCODING=UTF-8`：
<<< END U008390 >>>
<<< UNIT U008391 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:425-428 | ctx=协议升级与验证 >>>
- `tests/unit/test_rpc_contracts.py`：验证调用签名、默认值、业务对象 JSON 往返及平台接口自动绑定。
- `tests/unit/test_jobqueue_backend.py`：验证后端整套装配、配置选择、生命周期及禁止静默回退。
- `tests/unit/test_jobqueue_memory_backend.py`：在不访问 JobQueue ORM 表的后端上验证 RPC、信号和失效传播。
- `tests/unit/test_jobqueue_websocket_backend.py`：通过真实回环连接和独立进程验证 WebSocket 鉴权、发现、
<<< END U008391 >>>
<<< UNIT U008392 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:429-429 | ctx=协议升级与验证 >>>
  任播、逐实例信号、双向 RPC、反向调用及断线传播。
<<< END U008392 >>>
<<< UNIT U008393 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:430-430 | ctx=协议升级与验证 >>>
- `tests/unit/test_jobqueue_daemon.py`：验证内置 Hub 的启动屏障、外部 Hub 与数据库模式、启动失败回滚及
<<< END U008393 >>>
<<< UNIT U008394 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:431-431 | ctx=协议升级与验证 >>>
  Bot、Server、Hub 的有序关闭。
<<< END U008394 >>>
<<< UNIT U008395 | md-list | packages/akari-bot-core/akaribot/core/queue/README.md:432-436 | ctx=协议升级与验证 >>>
- `tests/unit/test_rpc_transport.py`：验证真实数据库往返、异常传播、取消、超时清理、维护与关闭流程。
- `tests/unit/test_rpc_process.py`：通过两个独立 Python 进程与临时 SQLite 验证并发反向调用。
- `tests/unit/test_queue_lifecycle.py`：验证原子认领、结果消费后删除、不需要响应的任务删除及活动任务清理。
- `tests/unit/test_peer_signals.py`：验证实例发现、同 service 任播、逐实例扇出、ACK 与租约到期。
- 会话、事件、平台关闭、主动推送、数据库维护与验证码测试用于覆盖上层迁移行为。
<<< END U008395 >>>
<<< UNIT U008396 | md-paragraph | packages/akari-bot-core/akaribot/core/queue/README.md:438-438 | ctx=协议升级与验证 >>>
例如：
<<< END U008396 >>>
<<< UNIT U008397 | py-docstring | packages/akari-bot-core/akaribot/core/queue/backend.py:1-1 | ctx=<module> >>>
JobQueue 后端组合与配置工厂。
<<< END U008397 >>>
<<< UNIT U008398 | py-docstring | packages/akari-bot-core/akaribot/core/queue/backend.py:23-23 | ctx=create_jobqueue_backend >>>
按照配置选择一套完整后端，不允许控制面和数据面交叉组合。
<<< END U008398 >>>
<<< UNIT U008399 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:199-199 >>>
# 延迟导入配置模板，避免仅导入 JobQueue 基础模块便触发配置系统的初始化副作用。
<<< END U008399 >>>
<<< UNIT U008400 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:205-205 >>>
# 正常启动会在 pre_init 中持久化缺失值。此回退仅供绕过守护进程的独立入口和测试使用。
<<< END U008400 >>>
<<< UNIT U008401 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:217-217 >>>
# 所有可能失败的验证完成后再切换类级生命周期状态，避免半配置污染。
<<< END U008401 >>>
<<< UNIT U008402 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:458-459 >>>
# 当前接收方发送完整诊断，须用本地捕获的调用栈重建，
# 以免中间环节以截断副本覆盖权威来源。
<<< END U008402 >>>
<<< UNIT U008403 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:601-603 >>>
# send() 可能在 INSERT 已提交后才因取消或连接异常返回。只要已建立
# 本地 waiter，就按“投递结果未知”处理并尝试删除该任务。删除不存在的 ID
# 是安全的，且不会取消已经开始的远端处理器。
<<< END U008403 >>>
<<< UNIT U008404 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:1171-1172 >>>
# Registry 已确认该实例重新处于 ready。允许同一进程内的轮询器重启
# 覆盖先前 stopped 缓存，同时仍拒绝没有权威租约的迟到 ready 信号。
<<< END U008404 >>>
<<< UNIT U008405 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:1399-1400 >>>
# register() 也可能在事务已提交后才因取消或连接状态异常返回。
# 以唯一 peer_id 尝试回滚，不让半注册实例保留到租约自然过期。
<<< END U008405 >>>
<<< UNIT U008406 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:1502-1503 >>>
# 等维护锁的任务只有在本窗口释放后才会继续，等它们必然互锁。它们在此
# 之前也不会执行模块代码，因此不纳入本轮等待范围。
<<< END U008406 >>>
<<< UNIT U008407 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:1518-1518 >>>
# 分片等待，因为 in-flight handler 随时可能转为等待维护锁，须重新筛选。
<<< END U008407 >>>
<<< UNIT U008408 | py-comment | packages/akari-bot-core/akaribot/core/queue/base.py:1602-1602 >>>
# asyncio.Lock 不可重入。嵌套窗口复用同一任务已有的范围。
<<< END U008408 >>>
<<< UNIT U008409 | py-docstring | packages/akari-bot-core/akaribot/core/queue/base.py:59-59 | ctx=QueueDrainTimeout >>>
维护窗口未能在预算时间内处理完运行中的处理函数。调用方应放弃本轮维护。
<<< END U008409 >>>
<<< UNIT U008410 | py-docstring | packages/akari-bot-core/akaribot/core/queue/base.py:143-143 | ctx=JobQueueBase.configure_backend >>>
在 Peer 启动前装配一套内部一致的控制面和数据面后端。
<<< END U008410 >>>
<<< UNIT U008411 | py-docstring | packages/akari-bot-core/akaribot/core/queue/client.py:1-1 | ctx=<module> >>>
平台 RPC 实现。普通 ContextManager 方法由共享接口定义自动绑定。
<<< END U008411 >>>
<<< UNIT U008412 | py-docstring | packages/akari-bot-core/akaribot/core/queue/client.py:19-19 | ctx=JobQueueClient >>>
平台进程 RPC 消费者及其生命周期。
<<< END U008412 >>>
<<< UNIT U008413 | py-docstring | packages/akari-bot-core/akaribot/core/queue/client.py:46-46 | ctx=post_message >>>
主动消息未取得消息 ID 时，将剩余下一跳交回服务端。
<<< END U008413 >>>
<<< UNIT U008414 | py-docstring | packages/akari-bot-core/akaribot/core/queue/client.py:69-69 | ctx=send_private_msg >>>
保留私信发送失败返回空列表的领域约定。
<<< END U008414 >>>
<<< UNIT U008415 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:39-39 | ctx=PlatformAPI >>>
平台适配器实现的 API 接口。
<<< END U008415 >>>
<<< UNIT U008416 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:85-85 | ctx=ServerAPI >>>
Server 与平台进程之间的 RPC 接口。
<<< END U008416 >>>
<<< UNIT U008417 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:124-124 | ctx=ServerAPI.get_runtime_stats >>>
汇总 JobQueue 后端与自服务端启动以来的解析计数，供 WebUI 状态页展示。
<<< END U008417 >>>
<<< UNIT U008418 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:130-130 | ctx=ServerAPI.get_active_session_count >>>
返回服务端正在执行与等待中的会话数量，供重启前判断是否可以安全退出。
<<< END U008418 >>>
<<< UNIT U008419 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:136-136 | ctx=ServerAPI.get_process_usage >>>
汇总各进程内存占用。扇出失败时以 failures 说明，不抛出异常。
<<< END U008419 >>>
<<< UNIT U008420 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:142-142 | ctx=ServerAPI.get_web_render_status_detail >>>
返回 WebRender 的完整状态详情，已转换为可序列化结构。
<<< END U008420 >>>
<<< UNIT U008421 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:148-148 | ctx=ServerAPI.control_web_render >>>
启动、关闭或重启服务端的 WebRender 浏览器。
<<< END U008421 >>>
<<< UNIT U008422 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:154-154 | ctx=ServerAPI.test_web_render >>>
按 WebUI 提交的参数执行一次渲染测试，失败以 error 字段返回。
<<< END U008422 >>>
<<< UNIT U008423 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:160-160 | ctx=ServerAPI.reload_filter_words >>>
让持有词库的进程重新读取 data/filter_words，使外部写入立即生效。
<<< END U008423 >>>
<<< UNIT U008424 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:186-186 | ctx=ServerAPI.post_package_install >>>
把刚安装的模块包热加载进运行中的服务端。
<<< END U008424 >>>
<<< UNIT U008425 | py-docstring | packages/akari-bot-core/akaribot/core/queue/contracts.py:192-192 | ctx=ServerAPI.post_package_remove >>>
在卸载包之前，把该模块包从运行中的服务端热卸载。
<<< END U008425 >>>
<<< UNIT U008426 | py-comment | packages/akari-bot-core/akaribot/core/queue/database.py:29-30 >>>
# SQLite 只能同时执行一个写事务。限制单轮候选数量可避免积压时一次轮询
# 对全部记录连续执行认领 UPDATE，并为业务表写入留下获得写锁的机会。
<<< END U008426 >>>
<<< UNIT U008427 | py-comment | packages/akari-bot-core/akaribot/core/queue/database.py:291-291 >>>
# 旧名称仅作为数据库实现的导入兼容实现保留。
<<< END U008427 >>>
<<< UNIT U008428 | py-docstring | packages/akari-bot-core/akaribot/core/queue/database.py:1-1 | ctx=<module> >>>
JobQueue 的数据库后端实现。
<<< END U008428 >>>
<<< UNIT U008429 | py-docstring | packages/akari-bot-core/akaribot/core/queue/database.py:27-27 | ctx=DatabaseMessageTransport >>>
通过 ``JobQueuesTable`` 传递请求与响应。
<<< END U008429 >>>
<<< UNIT U008430 | py-docstring | packages/akari-bot-core/akaribot/core/queue/database.py:83-83 | ctx=DatabaseMessageTransport.consume_responses >>>
读取并删除调用方已经能够接收的终态结果。
<<< END U008430 >>>
<<< UNIT U008431 | py-docstring | packages/akari-bot-core/akaribot/core/queue/database.py:100-100 | ctx=DatabaseMessageTransport.abandon >>>
尽力清理调用方已放弃的状态，不承诺取消远端处理器。
<<< END U008431 >>>
<<< UNIT U008432 | py-docstring | packages/akari-bot-core/akaribot/core/queue/database.py:115-115 | ctx=DatabaseMessageTransport.fail_peer_deliveries >>>
在数据库后端内部终结发往失效实例的投递。
<<< END U008432 >>>
<<< UNIT U008433 | py-docstring | packages/akari-bot-core/akaribot/core/queue/database.py:151-151 | ctx=DatabasePeerRegistry >>>
通过 ``JobQueuePeersTable`` 提供权威 Peer 目录。
<<< END U008433 >>>
<<< UNIT U008434 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:13-13 >>>
# 非 Peer 进程以固定标签标识，本地化由展示层处理。
<<< END U008434 >>>
<<< UNIT U008435 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:16-16 >>>
# 扇出整体失败时的占位标签，避免与进程不存在相混淆。
<<< END U008435 >>>
<<< UNIT U008436 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:19-19 >>>
# ping 为公开命令，缓存以抑制连续调用引发的重复扇出。
<<< END U008436 >>>
<<< UNIT U008437 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:21-21 >>>
# 避免单个无响应进程将 ping 拖至信号默认超时（30 秒）。
<<< END U008437 >>>
<<< UNIT U008438 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:23-23 >>>
# 失败原因来自远端异常消息，截断以限制单个进程对回复长度的影响。
<<< END U008438 >>>
<<< UNIT U008439 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:57-57 >>>
# 容器内 smaps 缺失等场景下自测亦可能失败，改用 ``rss`` 而不报错。
<<< END U008439 >>>
<<< UNIT U008440 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:125-125 >>>
# 载荷无效者仍须列出，否则该进程将从输出中消失。
<<< END U008440 >>>
<<< UNIT U008441 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:171-171 >>>
# 等锁期间可能已有采集完成，重新判定以免重复扇出。
<<< END U008441 >>>
<<< UNIT U008442 | py-comment | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:195-195 >>>
# 扇出整体失败时仍返回非 Peer 进程数据，并以一行说明 Peer 数据整体缺失。
<<< END U008442 >>>
<<< UNIT U008443 | py-docstring | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:1-1 | ctx=<module> >>>
进程内存占用采集。
<<< END U008443 >>>
<<< UNIT U008444 | py-docstring | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:29-29 | ctx=ProcessUsage >>>
单个进程的内存占用。``memory`` 为字节，``metric`` 说明统计方式。
<<< END U008444 >>>
<<< UNIT U008445 | py-docstring | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:40-40 | ctx=ProcessUnavailable >>>
未能取得内存占用的进程及其原因。
<<< END U008445 >>>
<<< UNIT U008446 | py-docstring | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:47-47 | ctx=collect_self_usage >>>
采集当前进程的内存指标。``uss`` 不可得时不写入该键，由调用方改用 ``rss``。
<<< END U008446 >>>
<<< UNIT U008447 | py-docstring | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:63-63 | ctx=collect_external_usage >>>
按 PID 读取同机其他进程的内存指标，进程不存在或不可读时返回 None。
<<< END U008447 >>>
<<< UNIT U008448 | py-docstring | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:78-78 | ctx=build_usage >>>
将原始指标转为展示行，缺少可用指标的载荷视为无效。
<<< END U008448 >>>
<<< UNIT U008449 | py-docstring | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:140-140 | ctx=usage_payload >>>
把内存占用汇总转为可经 RPC 与 JSON 传递的纯字典。
<<< END U008449 >>>
<<< UNIT U008450 | py-docstring | packages/akari-bot-core/akaribot/core/queue/diagnostics.py:163-163 | ctx=gather_process_usage >>>
汇总各进程的内存占用。
<<< END U008450 >>>
<<< UNIT U008451 | py-comment | packages/akari-bot-core/akaribot/core/queue/errors.py:24-25 >>>
# 异常对象以 JSON 跨 RPC，故合并诊断文本与原始进程栈分别保留。
# ``remote_traceback`` 为可选，旧响应信封只带一个 traceback 字段。
<<< END U008451 >>>
<<< UNIT U008452 | py-docstring | packages/akari-bot-core/akaribot/core/queue/memory.py:1-1 | ctx=<module> >>>
用于验证 JobQueue 接口约定的进程内后端。
<<< END U008452 >>>
<<< UNIT U008453 | py-docstring | packages/akari-bot-core/akaribot/core/queue/memory.py:18-18 | ctx=InMemoryBroker >>>
由同一测试集群中的多个内存后端实例共享的权威状态。
<<< END U008453 >>>
<<< UNIT U008454 | py-docstring | packages/akari-bot-core/akaribot/core/queue/peer.py:1-1 | ctx=<module> >>>
介质无关的 JobQueue Peer 身份、筛选条件及注册表协议。
<<< END U008454 >>>
<<< UNIT U008455 | py-docstring | packages/akari-bot-core/akaribot/core/queue/peer.py:37-37 | ctx=PeerSelector >>>
选择当前处于 ready 状态且满足全部约束的进程实例。
<<< END U008455 >>>
<<< UNIT U008456 | py-docstring | packages/akari-bot-core/akaribot/core/queue/peer.py:101-101 | ctx=ServiceRoute >>>
以 Rendezvous Hash 将业务键稳定路由至一个 ready 实例。
<<< END U008456 >>>
<<< UNIT U008457 | py-docstring | packages/akari-bot-core/akaribot/core/queue/peer.py:186-186 | ctx=PeerRegistryBase >>>
供不同介质复用稳定路由算法的注册表基类。
<<< END U008457 >>>
<<< UNIT U008458 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:62-62 >>>
# ServiceRoute 已在入队前从 Registry 选中了一个 ready 实例，无需重复查询。
<<< END U008458 >>>
<<< UNIT U008459 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:193-194 >>>
# 渲染测试的单次响应上限，截图按张数、源码按字符数截断，避免一次请求把响应体
# 撑到 WebUI 无法处理的量级。超限只截断，不视为失败。
<<< END U008459 >>>
<<< UNIT U008460 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:197-197 >>>
# 渲染测试允许直接传递的字段。未列出的键一律忽略，避免任意参数进入依赖库的选项模型。
<<< END U008460 >>>
<<< UNIT U008461 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:217-217 >>>
# ``contexts_open_sorted`` 以 BrowserContext 对象为键，无法序列化，改为按出现顺序编号的列表。
<<< END U008461 >>>
<<< UNIT U008462 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:252-253 >>>
# 本地浏览器未就绪且未配置远端时，依赖库直接返回 None。此时仍给出未就绪的状态，
# 让前端能区分“无法读取状态”与“浏览器未启动”。
<<< END U008462 >>>
<<< UNIT U008463 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:298-298 >>>
# stop 只需浏览器已按请求关闭。start / restart 则以依赖库的初始化结果为准。
<<< END U008463 >>>
<<< UNIT U008464 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:347-347 >>>
# 只探测可用性而不渲染任何页面，供前端的“测试连接”按钮使用。
<<< END U008464 >>>
<<< UNIT U008465 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:412-412 >>>
# 与依赖库一致，images 为裸 base64，data URL 前缀由前端自行拼接。
<<< END U008465 >>>
<<< UNIT U008466 | py-comment | packages/akari-bot-core/akaribot/core/queue/server.py:426-426 >>>
# 词库文件可能正被手工编辑。失败时保留旧词库并如实返回，不中断服务端。
<<< END U008466 >>>
<<< UNIT U008467 | py-docstring | packages/akari-bot-core/akaribot/core/queue/server.py:1-1 | ctx=<module> >>>
服务端 RPC 实现。调用签名与编码由共享接口定义统一管理。
<<< END U008467 >>>
<<< UNIT U008468 | py-docstring | packages/akari-bot-core/akaribot/core/queue/server.py:53-53 | ctx=JobQueueServer >>>
服务端 RPC 消费者及其生命周期。
<<< END U008468 >>>
<<< UNIT U008469 | py-docstring | packages/akari-bot-core/akaribot/core/queue/server.py:57-57 | ctx=JobQueueServer.ensure_target_available >>>
以 Peer Registry 为准判断 Client 或实例是否仍可接收新任务。
<<< END U008469 >>>
<<< UNIT U008470 | py-docstring | packages/akari-bot-core/akaribot/core/queue/server.py:128-128 | ctx=post_next_hop >>>
解析下一跳并交给对应平台。每次转发后候选项减少一项。
<<< END U008470 >>>
<<< UNIT U008471 | py-docstring | packages/akari-bot-core/akaribot/core/queue/server.py:508-508 | ctx=post_package_install >>>
热加载新安装的模块包。未安装或被发现层拒绝时返回 False。
<<< END U008471 >>>
<<< UNIT U008472 | py-docstring | packages/akari-bot-core/akaribot/core/queue/server.py:518-518 | ctx=post_package_remove >>>
在 uv pip uninstall 之前把模块包从运行中的服务端热卸载。
<<< END U008472 >>>
<<< UNIT U008473 | py-comment | packages/akari-bot-core/akaribot/core/queue/transport.py:76-76 >>>
# 兼容现有扩展的类型名称。新实现应使用 MessageTransport。
<<< END U008473 >>>
<<< UNIT U008474 | py-docstring | packages/akari-bot-core/akaribot/core/queue/transport.py:1-1 | ctx=<module> >>>
介质无关的 JobQueue 数据面协议。
<<< END U008474 >>>
<<< UNIT U008475 | py-docstring | packages/akari-bot-core/akaribot/core/queue/transport.py:37-37 | ctx=BatchSendResult >>>
逐项描述批量投递结果，避免将部分成功误判为原子失败。
<<< END U008475 >>>
<<< UNIT U008476 | py-comment | packages/akari-bot-core/akaribot/core/queue/websocket.py:403-404 >>>
# 保留帧能容纳的尽量多远端栈，用二分查找避免长消息反复超帧。
# 裁剪前先去掉接收侧已含的请求上下文后缀，以便调用方重建本地上下文。
<<< END U008476 >>>
<<< UNIT U008477 | py-comment | packages/akari-bot-core/akaribot/core/queue/websocket.py:422-423 >>>
# 极小上限可能容不下原始消息。
# 先以短回退保持协议结构合法，再交由调用方处理不可能满足的帧上限。
<<< END U008477 >>>
<<< UNIT U008478 | py-docstring | packages/akari-bot-core/akaribot/core/queue/websocket.py:1-1 | ctx=<module> >>>
WebSocket JobQueue 后端及独立 Hub 实现。
<<< END U008478 >>>
<<< UNIT U008479 | py-docstring | packages/akari-bot-core/akaribot/core/queue/websocket.py:503-503 | ctx=WebSocketHub >>>
维护连接、Peer 拓扑以及非持久化投递状态的独立 Hub。
<<< END U008479 >>>
<<< UNIT U008480 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:30-30 >>>
# 二进制构建产物。存在时 discover() 直接采用其中记录的清单，跳过 entry point 与目录扫描。
<<< END U008480 >>>
<<< UNIT U008481 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:33-33 >>>
# 包内 manifest 的文件名与版本。
<<< END U008481 >>>
<<< UNIT U008482 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:37-38 >>>
# core 公开 API 的版本。模块与适配器以 manifest 的 requires_core_api 声明所需区间，不满足者由
# reject_incompatible() 拒绝注册。本常量是唯一来源，core.api 读取其值。此处不得反向导入 core.api。
<<< END U008482 >>>
<<< UNIT U008483 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:41-41 >>>
# 参与运行时依赖图的包名前缀。其余 Requires-Dist 是普通 PyPI 依赖，由安装器负责解析。
<<< END U008483 >>>
<<< UNIT U008484 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:64-66 >>>
# 不能在模块层导入 core.logger，因为 core.logger 会经 core.config.base 引入整个配置系统，
# 而配置系统在导入期校验配置文件存在并执行版本迁移。发现层必须能在配置就绪之前使用
# （locale 目录的收集就发生在配置加载之前），因此把这条依赖推迟到真正要记录日志时。
<<< END U008484 >>>
<<< UNIT U008485 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:73-73 >>>
# 依赖声明的写法允许大小写与下划线差异，比较前归一为同一形式，等价名字才能命中同一个包。
<<< END U008485 >>>
<<< UNIT U008486 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:80-80 >>>
# 从包目录向上找 pyproject.toml 的层数上限。wheel 安装下不存在，以上限尽快结束查找。
<<< END U008486 >>>
<<< UNIT U008487 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:102-102 >>>
# 向上可能遇到无关的 pyproject。名字对不上就继续找，不据此判断作者。
<<< END U008487 >>>
<<< UNIT U008488 | py-inline-comment | packages/akari-bot-core/akaribot/core/registry.py:113-113 >>>
# noqa: BLE001 - 元数据缺失不该让作者查询失败
<<< END U008488 >>>
<<< UNIT U008489 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:258-258 >>>
# 记录 core API 不兼容的包（展示用标签到原因的映射）。
<<< END U008489 >>>
<<< UNIT U008490 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:260-260 >>>
# 同一批包的规范化包名到原因的映射，供依赖校验把“依赖被 API 门槛拒绝的包”判定为不可用。
<<< END U008490 >>>
<<< UNIT U008491 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:288-288 >>>
# 目录扫描是回退路径，entry point 已提供的包不再重复记录，也不产生冲突告警。
<<< END U008491 >>>
<<< UNIT U008492 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:308-309 >>>
# entry point 的枚举顺序不保证跨环境一致，凡是由条目集合推导出的结果（导入路径索引、
# locale 搜索路径）都必须先按此键排序，否则同一批包在不同机器上可能得到不同结果。
<<< END U008492 >>>
<<< UNIT U008493 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:314-316 >>>
# 同名导入路径可能同时来自 entry point 与目录扫描，取带分发 metadata 者。发现阶段与
# :meth:`reject_incompatible` 的补做必须共用本方法，避免两处各写一遍取舍规则时，同一批数据
# 因入口不同得到不同条目。先排序再取舍，平手时先写入者胜出才是确定的。
<<< END U008493 >>>
<<< UNIT U008494 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:372-372 >>>
# 发现阶段已检查过一遍，此时覆盖会丢失已记录的原因（被拒绝的包已不在 _entries 里）
<<< END U008494 >>>
<<< UNIT U008495 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:384-386 >>>
# 结果分两份，展示用标签到原因供 :meth:`incompatible` / :meth:`report_lines` 报出，
# 规范化包名到原因供依赖校验把“依赖一个已被拒绝的包”判定为不可用。本方法不改动
# 类状态，由调用方确定如何记录。
<<< END U008495 >>>
<<< UNIT U008496 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:443-444 >>>
# 只按 spec 定位包目录，不导入包本身。导入会执行包内 ``config.py``，使配置模板在 i18n
# 快照接上之前写入磁盘，新实例生成的配置注释全部退化为空。
<<< END U008496 >>>
<<< UNIT U008497 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:490-490 >>>
# 未安装包的源码克隆依赖这条路径，因此扫描对象是真实存在的包目录，不用硬编码的路径常量。
<<< END U008497 >>>
<<< UNIT U008498 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:515-517 >>>
# 条目根取导入包目录，manifest、locales、assets、migrations 都相对它
# 解析，entry point 路径下两者同为导入包目录，此处按同一规则处理。源码布局为 ``src`` 时按导入路径
# 下推。不是该布局时回退到传入目录。
<<< END U008498 >>>
<<< UNIT U008499 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:605-606 >>>
# 命名空间与 entry point 组同名（见 ENTRY_POINT_GROUPS），但取值仍由条目导出，
# 该类无包时返回空集，调用方据此判断是否存在可依赖的包。
<<< END U008499 >>>
<<< UNIT U008500 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:667-668 >>>
# 目录形式的命名空间包仍可导入，配置正常补全，但其他按包枚举的代码
# 看不见它，故仅告警，提示补上空的 __init__.py 以恢复常规包。
<<< END U008500 >>>
<<< UNIT U008501 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:746-747 >>>
# 获取实例的可写 data 目录，而非顶层只读的 assets，因为包的可写数据不属于随仓库分发的
# 内容，放在 assets 下会在只读挂载与 wheel 安装两种形态下同时失败。
<<< END U008501 >>>
<<< UNIT U008502 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:878-878 >>>
# 环检测已在上方拦截。剩余节点仍须报错，不得静默少加载包。
<<< END U008502 >>>
<<< UNIT U008503 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:887-887 >>>
# 记录一次拒绝。
<<< END U008503 >>>
<<< UNIT U008504 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:916-917 >>>
# 级联剔除，因为依赖一个已被拒绝的包与依赖一个未安装的包同样注定失败，只按 metadata 判断会让
# 依赖方以“依赖已安装”为由留下，最终在导入期抛出与配置无关的错误。逐个剔除至不动点。
<<< END U008504 >>>
<<< UNIT U008505 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:940-940 >>>
# 它可能仍安装在环境里，但不会完成注册。
<<< END U008505 >>>
<<< UNIT U008506 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:957-958 >>>
# 目录扫描的包没有包名元数据，按 ``akari-bot-<种类>-<包名>`` 合成，使该名字与拆包后的
# 包名一致，依赖声明因此不必区分包来自 entry point 还是目录扫描。
<<< END U008506 >>>
<<< UNIT U008507 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:984-984 >>>
# 单行不可解析时跳过该行，一条写错的依赖不应让整个包从注册表中消失。
<<< END U008507 >>>
<<< UNIT U008508 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:997-999 >>>
# 包 metadata 不记录安装包时选中了哪些 extra，故任何实现都是启发式。此处取“该 extra 下属
# 的依赖都能解析为已安装包”为已安装判断依据。已知边界是手工安装完整某个未选中 extra 的全部依赖时会被
# 误判为已安装，代价是多记一条依赖边。既有测试已验证该判断依据。
<<< END U008508 >>>
<<< UNIT U008509 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:1010-1012 >>>
# extra 未指定时 packaging 代入空字符串，带 ``extra`` 子句的标记因此先判定为假，再逐个
# 代入候选 extra 重新判断。只有已安装 extra 的子句才算成立。标记无法求值时按成立处理，因为
# 依赖是真实存在的耦合，宁可多记一条边，也不静默丢弃。
<<< END U008509 >>>
<<< UNIT U008510 | py-comment | packages/akari-bot-core/akaribot/core/registry.py:1053-1055 >>>
# 以 Tarjan 算法求强连通分量，成员多于一个的分量即为环。返回的是分量成员而非
# 某一条回路，调用方用 :meth:`_cycle_path` 还原完整路径。这样两个互不相交的环
# 都会被发现，不会被只找首个环的写法漏掉。
<<< END U008510 >>>
<<< UNIT U008511 | py-docstring | packages/akari-bot-core/akaribot/core/registry.py:48-48 | ctx=RegistryError >>>
发现层无法产出可用清单时抛出。
<<< END U008511 >>>
<<< UNIT U008512 | py-docstring | packages/akari-bot-core/akaribot/core/registry.py:229-229 | ctx=PackageEntry.stem >>>
包名。目录扫描与 entry point 两条路径下取值一致。
<<< END U008512 >>>
<<< UNIT U008513 | py-docstring | packages/akari-bot-core/akaribot/core/registry.py:413-413 | ctx=PackageRegistry.report_lines >>>
不兼容包的一行式说明，供启动提示与 loader 缓存展示。
<<< END U008513 >>>
<<< UNIT U008514 | py-docstring | packages/akari-bot-core/akaribot/core/registry.py:549-549 | ctx=PackageRegistry.modules >>>
全部模块包，键为包名。
<<< END U008514 >>>
<<< UNIT U008515 | py-docstring | packages/akari-bot-core/akaribot/core/registry.py:555-555 | ctx=PackageRegistry.adapters >>>
全部适配器包，键为包名。
<<< END U008515 >>>
<<< UNIT U008516 | py-docstring | packages/akari-bot-core/akaribot/core/registry.py:561-561 | ctx=PackageRegistry.all >>>
全部包，键为 ``种类:包名``。
<<< END U008516 >>>
<<< UNIT U008517 | py-comment | packages/akari-bot-core/akaribot/core/scheduler.py:124-125 >>>
# maintenance 先关闭入口，再取得本锁作为提交屏障。已经 submit 但尚未
# 开始执行业务函数的 coroutine 会在此检测关闭状态并退出。
<<< END U008517 >>>
<<< UNIT U008518 | py-comment | packages/akari-bot-core/akaribot/core/scheduler.py:320-320 >>>
# 与所有已经进入／正在等待 wrapper 启动临界区的任务建立屏障。
<<< END U008518 >>>
<<< UNIT U008519 | py-comment | packages/akari-bot-core/akaribot/core/scheduler.py:353-354 >>>
# AsyncIOScheduler.shutdown() 只把真正的关闭回调排进事件循环。
# 等待 shutdown event 才能保证回调已经执行，而非仅“调用过”。
<<< END U008519 >>>
<<< UNIT U008520 | py-comment | packages/akari-bot-core/akaribot/core/scheduler.py:360-360 >>>
# 初始化中途失败时 Scheduler 尚未 start，但可能已有 pending jobs。
<<< END U008520 >>>
<<< UNIT U008521 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:1-1 | ctx=<module> >>>
基于 APScheduler 的计划任务与生命周期管理。
<<< END U008521 >>>
<<< UNIT U008522 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:58-58 | ctx=IntervalTrigger >>>
按全局配置倍率调整间隔的 APScheduler IntervalTrigger。
<<< END U008522 >>>
<<< UNIT U008523 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:89-89 | ctx=ScheduledJobSpec >>>
可重建的计划任务描述。
<<< END U008523 >>>
<<< UNIT U008524 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:98-98 | ctx=SchedulerLifecycle >>>
统一管理模块计划任务、运行中实例和维护／关闭窗口。
<<< END U008524 >>>
<<< UNIT U008525 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:113-113 | ctx=SchedulerLifecycle.module_job_id >>>
返回模块内第 ``index`` 个计划任务的稳定 APScheduler ID。
<<< END U008525 >>>
<<< UNIT U008526 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:184-184 | ctx=SchedulerLifecycle.snapshot_modules >>>
保存指定模块当前的 Scheduler Job，以供 Loader 失败回滚。
<<< END U008526 >>>
<<< UNIT U008527 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:200-200 | ctx=SchedulerLifecycle.restore_modules >>>
以快照替换指定模块的全部 Job。调用方须位于维护窗口内。
<<< END U008527 >>>
<<< UNIT U008528 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:209-209 | ctx=SchedulerLifecycle.reconcile_modules >>>
让指定模块的 APScheduler Job 与当前 Module 注册表完全一致。
<<< END U008528 >>>
<<< UNIT U008529 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:233-233 | ctx=SchedulerLifecycle.reconcile_all_modules >>>
同步全部模块，并移除已经不存在的模块 Job。
<<< END U008529 >>>
<<< UNIT U008530 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:238-238 | ctx=SchedulerLifecycle.register_core_job >>>
注册一个同样受维护／关闭窗口追踪的核心计划任务。
<<< END U008530 >>>
<<< UNIT U008531 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:252-252 | ctx=SchedulerLifecycle.prepare >>>
为尚未启动的本轮 Server 生命周期开放 Job 入口。
<<< END U008531 >>>
<<< UNIT U008532 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:258-258 | ctx=SchedulerLifecycle.start >>>
启动全局 Scheduler。重复调用保持幂等。
<<< END U008532 >>>
<<< UNIT U008533 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:267-267 | ctx=SchedulerLifecycle.begin_shutdown >>>
同步关闭新 Job 入口。实际取消和等待由 :meth:`shutdown` 完成。
<<< END U008533 >>>
<<< UNIT U008534 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:299-299 | ctx=SchedulerLifecycle.maintenance_window >>>
暂停新触发并取消、等待目标范围内正在运行的 Job。
<<< END U008534 >>>
<<< UNIT U008535 | py-docstring | packages/akari-bot-core/akaribot/core/scheduler.py:334-334 | ctx=SchedulerLifecycle.shutdown >>>
真正停止 Scheduler，并等待所有运行中的业务 coroutine 退出。
<<< END U008535 >>>
<<< UNIT U008536 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:24-26 >>>
# 转换逻辑要按新模型写入数据，但 core 不得静态依赖任何模块包，因为模块在拆包后是独立包，
# 未安装时静态导入会让脚本直接导入失败。清单取自 PackageRegistry，未安装的包自然不存在，
# 其数据留在旧表里不动。
<<< END U008536 >>>
<<< UNIT U008537 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:37-37 >>>
# 这些类定义旧数据库的模式，用于连接旧数据库表并完成数据迁移
<<< END U008537 >>>
<<< UNIT U008538 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:239-240 >>>
# 重命名旧表以避免冲突
# 带 "_old" 前缀的表名排在列表末尾，便于管理
<<< END U008538 >>>
<<< UNIT U008539 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:268-268 >>>
# 如果表不存在或其他错误，则忽略（可能已经被重命名）
<<< END U008539 >>>
<<< UNIT U008540 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:280-280 >>>
# 第一步：重命名旧表
<<< END U008540 >>>
<<< UNIT U008541 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:283-283 >>>
# 第二步：初始化新的数据库架构
<<< END U008541 >>>
<<< UNIT U008542 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:290-290 >>>
# 生成新的数据库架构
<<< END U008542 >>>
<<< UNIT U008543 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:300-300 >>>
# 每处理 1000 条记录显示一次进度
<<< END U008543 >>>
<<< UNIT U008544 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:304-304 >>>
# 将旧格式的发送者信息转换为新格式。旧的平台 ID 直接作为 union ID，映射行在最后统一补充创建。
<<< END U008544 >>>
<<< UNIT U008545 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:317-317 >>>
# 删除旧表
<<< END U008545 >>>
<<< UNIT U008546 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:322-322 >>>
# 获取所有场景信息和黑名单信息
<<< END U008546 >>>
<<< UNIT U008547 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:325-325 >>>
# 创建黑名单 ID 集合，便于后续查询
<<< END U008547 >>>
<<< UNIT U008548 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:333-333 >>>
# 将旧格式的场景信息转换为新格式。旧的平台 ID 直接作为 union ID，映射行在最后统一补充创建。
<<< END U008548 >>>
<<< UNIT U008549 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:347-347 >>>
# 如果场景在黑名单中，更新其 blocked 字段
<<< END U008549 >>>
<<< UNIT U008550 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:359-359 >>>
# 删除旧表
<<< END U008550 >>>
<<< UNIT U008551 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:364-364 >>>
# 转换存储数据，处理 JSON 格式
<<< END U008551 >>>
<<< UNIT U008552 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:368-368 >>>
# 确保值是 JSON 数组格式
<<< END U008552 >>>
<<< UNIT U008553 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:373-373 >>>
# 解析 JSON 值
<<< END U008553 >>>
<<< UNIT U008554 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:376-376 >>>
# 如果 JSON 解析失败则跳过此项
<<< END U008554 >>>
<<< UNIT U008555 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:383-383 >>>
# 删除旧表
<<< END U008555 >>>
<<< UNIT U008556 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:389-389 >>>
# 转换分析数据
<<< END U008556 >>>
<<< UNIT U008557 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:415-415 >>>
# 转换不友好行为记录
<<< END U008557 >>>
<<< UNIT U008558 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:436-436 >>>
# Cytoid 模块的绑定信息转换
<<< END U008558 >>>
<<< UNIT U008559 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:451-451 >>>
# Maimai 模块的绑定信息转换
<<< END U008559 >>>
<<< UNIT U008560 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:466-466 >>>
# Phigros 模块的绑定信息转换
<<< END U008560 >>>
<<< UNIT U008561 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:482-482 >>>
# Wiki 模块的场景设置转换
<<< END U008561 >>>
<<< UNIT U008562 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:500-500 >>>
# Wiki 网站信息转换
<<< END U008562 >>>
<<< UNIT U008563 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:512-512 >>>
# 旧 Wiki API 白名单已并入全局 URL 规则文件。全部写入成功后才删除旧表。
<<< END U008563 >>>
<<< UNIT U008564 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:519-519 >>>
# 旧 Wiki API 黑名单同样保留为精确规则或带 regex: 前缀的正则规则。
<<< END U008564 >>>
<<< UNIT U008565 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:526-526 >>>
# Wiki 机器人账号转换
<<< END U008565 >>>
<<< UNIT U008566 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:538-538 >>>
# WikiLog 场景设置转换
<<< END U008566 >>>
<<< UNIT U008567 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:550-550 >>>
# 旧数据库中数据与平台 ID 一一对应，转换后 union ID 即为原 ID，据此补充创建映射行。
<<< END U008567 >>>
<<< UNIT U008568 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:555-555 >>>
# 更新数据库版本信息
<<< END U008568 >>>
<<< UNIT U008569 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:560-560 >>>
# 清理任务队列表
<<< END U008569 >>>
<<< UNIT U008570 | py-comment | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:564-564 >>>
# 关闭数据库连接
<<< END U008570 >>>
<<< UNIT U008571 | py-docstring | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:1-1 | ctx=<module> >>>
数据库格式转换脚本。
<<< END U008571 >>>
<<< UNIT U008572 | py-docstring | packages/akari-bot-core/akaribot/core/scripts/convert_database.py:275-275 | ctx=convert_database >>>
执行完整的数据库转换过程。
<<< END U008572 >>>
<<< UNIT U008573 | py-comment | packages/akari-bot-core/akaribot/core/scripts/migrate_assets_to_data.py:22-22 >>>
# (旧路径, 新路径)，两者都相对仓库根目录。
<<< END U008573 >>>
<<< UNIT U008574 | py-comment | packages/akari-bot-core/akaribot/core/scripts/migrate_assets_to_data.py:41-41 >>>
# (仓库内旧路径, 实例内新路径)。仅收录部署者提供的文件，下载产物可重新获取，无需迁移。
<<< END U008574 >>>
<<< UNIT U008575 | py-docstring | packages/akari-bot-core/akaribot/core/scripts/migrate_assets_to_data.py:1-15 | ctx=<module> >>>
assets / data 布局迁移脚本。

旧版把可写内容与只读资源一并放在 ``assets`` 下。新版按“只读留 assets、可写入 data”
拆分，将运行时产物、部署者提供的内容以及模块的下载资源迁移至 ``data`` 目录。模块包的可写数据
再进一步改为挂载到实例目录，位置由 ``PackageRegistry.package_data()`` 确定。

升级既有部署时，从仓库根目录执行一次：

    python -m akaribot.core.scripts.migrate_assets_to_data [--dry-run]

实例内迁移要求 ``AKARI_INSTANCE_DIR`` 指向实例根目录，未设置时使用当前目录。

脚本只做移动，不覆盖目标位置已存在的文件，因而可以重复执行。已经迁移过的条目会被跳过。
<<< END U008575 >>>
<<< UNIT U008576 | py-docstring | packages/akari-bot-core/akaribot/core/server/__init__.py:1-1 | ctx=<module> >>>
服务器核心模块包。
<<< END U008576 >>>
<<< UNIT U008577 | py-comment | packages/akari-bot-core/akaribot/core/server/background_tasks.py:93-94 >>>
# 各项初始化并行执行，并保持结构化并发语义。任一任务意外失败时，TaskGroup
# 会取消并等待其余任务，避免父任务结束后浏览器初始化仍在后台继续。
<<< END U008577 >>>
<<< UNIT U008578 | py-docstring | packages/akari-bot-core/akaribot/core/server/background_tasks.py:1-1 | ctx=<module> >>>
服务器后台任务模块。
<<< END U008578 >>>
<<< UNIT U008579 | py-docstring | packages/akari-bot-core/akaribot/core/server/background_tasks.py:19-19 | ctx=hourly_background_task >>>
每小时执行一次的后台检查任务。
<<< END U008579 >>>
<<< UNIT U008580 | py-docstring | packages/akari-bot-core/akaribot/core/server/background_tasks.py:111-111 | ctx=start_background_task >>>
启动并持有 Server 后台初始化任务。重复调用时复用仍在运行的任务。
<<< END U008580 >>>
<<< UNIT U008581 | py-docstring | packages/akari-bot-core/akaribot/core/server/background_tasks.py:120-120 | ctx=stop_background_task >>>
取消并等待后台初始化，保证 WebRender 关闭不会与浏览器启动并发。
<<< END U008581 >>>
<<< UNIT U008582 | py-comment | packages/akari-bot-core/akaribot/core/server/init.py:23-24 >>>
# 等待发起重启的客户端重新注册为 ready 的秒数上限。server 与各 bot 子进程一同重启，
# 提示投递时客户端往往尚未就绪。但重启提示并非关键路径，客户端确已掉线时不应无限等待。
<<< END U008582 >>>
<<< UNIT U008583 | py-comment | packages/akari-bot-core/akaribot/core/server/init.py:57-57 >>>
# pre-init 已统一创建数据表。Server 初始化只负责注册连接和全部模块模型。
<<< END U008583 >>>
<<< UNIT U008584 | py-comment | packages/akari-bot-core/akaribot/core/server/init.py:64-65 >>>
# 模块与核心 Job 都经统一 wrapper 注册，以便热重载、全局启动与停止和 Server
# 关闭时能够按稳定 ID 替换，并等待运行中的 coroutine 真正退出。
<<< END U008584 >>>
<<< UNIT U008585 | py-comment | packages/akari-bot-core/akaribot/core/server/init.py:134-135 >>>
# 缓存须无条件清理。内容损坏、客户端不上线或投递失败时若将其留下，
# 下次启动会再次解析同一文件，严重时形成稳定的重启循环。
<<< END U008585 >>>
<<< UNIT U008586 | py-comment | packages/akari-bot-core/akaribot/core/server/init.py:144-145 >>>
# 数据库中的旧 Client peer 退出后仍可能保有有效租约，须明确排除。
# 提示固定投递给本轮重启后实际注册的新实例。
<<< END U008586 >>>
<<< UNIT U008587 | py-comment | packages/akari-bot-core/akaribot/core/server/init.py:179-180 >>>
# 重启提示是尽力而为的辅助信息，刷新旧会话或平台投递失败
# 不应阻止 Server 完成启动。
<<< END U008587 >>>
<<< UNIT U008588 | py-docstring | packages/akari-bot-core/akaribot/core/server/init.py:1-1 | ctx=<module> >>>
服务器初始化模块。
<<< END U008588 >>>
<<< UNIT U008589 | py-docstring | packages/akari-bot-core/akaribot/core/server/lifecycle.py:1-1 | ctx=<module> >>>
Server 进程内后台资源的统一关闭注册表。
<<< END U008589 >>>
<<< UNIT U008590 | py-docstring | packages/akari-bot-core/akaribot/core/server/lifecycle.py:12-12 | ctx=BackgroundCleanupSpec >>>
一项需要在 Queue 和数据库关闭前执行的后台资源清理。
<<< END U008590 >>>
<<< UNIT U008591 | py-docstring | packages/akari-bot-core/akaribot/core/server/lifecycle.py:20-20 | ctx=BackgroundTaskLifecycle >>>
管理模块和核心组件持有的 detached 后台任务。
<<< END U008591 >>>
<<< UNIT U008592 | py-docstring | packages/akari-bot-core/akaribot/core/server/lifecycle.py:33-33 | ctx=BackgroundTaskLifecycle.register_cleanup >>>
注册一项幂等清理。相同稳定 key 的热重载会原位替换旧回调。
<<< END U008592 >>>
<<< UNIT U008593 | py-docstring | packages/akari-bot-core/akaribot/core/server/lifecycle.py:46-46 | ctx=BackgroundTaskLifecycle.run_cleanup >>>
按注册顺序执行全部清理，并隔离单项超时或失败。
<<< END U008593 >>>
