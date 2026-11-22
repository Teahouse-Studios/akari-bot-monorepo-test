# 全仓可读文本审核稿 · 第 05 册 / 共 20 册

覆盖 U001852–U003218，20 个文件、1,367 个单元、32,840 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `packages/akari-bot-cli/akaribot/cli/docs_engine/catalog.py` | 6 | U001852–U001857 | 230 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/config.py` | 7 | U001858–U001864 | 181 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/defaults.toml` | 4 | U001865–U001868 | 456 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/base.py` | 4 | U001869–U001872 | 81 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/s3.py` | 1 | U001873–U001873 | 13 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/sigv4.py` | 2 | U001874–U001875 | 45 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/vercel.py` | 2 | U001876–U001877 | 50 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py` | 11 | U001878–U001888 | 251 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py` | 9 | U001889–U001897 | 346 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/model.py` | 5 | U001898–U001902 | 158 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/server.py` | 6 | U001903–U001908 | 164 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/state.py` | 3 | U001909–U001911 | 46 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/theme.py` | 2 | U001912–U001913 | 69 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/theme_sync.py` | 3 | U001914–U001916 | 98 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py` | 10 | U001917–U001926 | 362 |
| `packages/akari-bot-cli/akaribot/cli/docs_engine/watch.py` | 6 | U001927–U001932 | 86 |
| `packages/akari-bot-cli/akaribot/cli/i18n.py` | 5 | U001933–U001937 | 218 |
| `packages/akari-bot-cli/akaribot/cli/instance.py` | 65 | U001938–U002002 | 2,114 |
| `packages/akari-bot-cli/akaribot/cli/instances.py` | 12 | U002003–U002014 | 307 |
| `packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json` | 1204 | U002015–U003218 | 27,565 |

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
<<< UNIT U001852 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/catalog.py:61-61 >>>
# 分组顺序固定，避免首页与导航随包 key 的字母序把适配器排到模块之前。
<<< END U001852 >>>
<<< UNIT U001853 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/catalog.py:80-80 >>>
# noqa: BLE001 - 子进程形态取决于实例实现，任何失败都只影响目录来源
<<< END U001853 >>>
<<< UNIT U001854 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/catalog.py:175-175 >>>
# noqa: BLE001 - 回退本身失败时目录为空，由警告说明原因
<<< END U001854 >>>
<<< UNIT U001855 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/catalog.py:252-252 >>>
# noqa: BLE001 - 冻结产物可能没有 metadata，版本回退到包内常量
<<< END U001855 >>>
<<< UNIT U001856 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/catalog.py:332-332 >>>
# 首页与开发页固定首尾，其余页面按 order 与路径排序，侧栏标签顺序才稳定。
<<< END U001856 >>>
<<< UNIT U001857 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/catalog.py:428-428 >>>
# noqa: BLE001 - 缺少元数据时按无依赖处理
<<< END U001857 >>>
<<< UNIT U001858 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/config.py:429-429 >>>
# 正文与按钮区分“未配置”和“配置为空”，空元组表示有意不显示该类内容。
<<< END U001858 >>>
<<< UNIT U001859 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/config.py:113-113 | ctx=default_labels >>>
返回默认界面文案的副本，供目录层在未持有实例配置时使用。
<<< END U001859 >>>
<<< UNIT U001860 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/config.py:283-283 | ctx=DocsConfig.default_locale >>>
默认语言。
<<< END U001860 >>>
<<< UNIT U001861 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/config.py:288-288 | ctx=DocsConfig.cache_docs_dir >>>
生成器与工具链共用的缓存目录 ``<实例根目录>/cache/docs``。
<<< END U001861 >>>
<<< UNIT U001862 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/config.py:293-293 | ctx=DocsConfig.out_dir >>>
输出目录的绝对路径。配置为相对路径时以实例根目录为基准。
<<< END U001862 >>>
<<< UNIT U001863 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/config.py:299-299 | ctx=DocsConfig.base >>>
当前生效的基础路径，环境变量优先于配置文件。
<<< END U001863 >>>
<<< UNIT U001864 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/config.py:304-304 | ctx=normalize_base >>>
将基础路径规范为以 ``/`` 开头并结尾的形式。
<<< END U001864 >>>
<<< UNIT U001865 | cfg-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/defaults.toml:1-2 >>>
# 站点标题、输出位置、界面文案与侧栏导航的出厂默认值。
# 实例的 docs.toml 可以逐键覆盖这里的取值，未覆盖的键沿用本文件。
<<< END U001865 >>>
<<< UNIT U001866 | cfg-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/defaults.toml:59-61 >>>
# 站点素材的文件名相对随包的 assets/ 目录，缺失时按无素材处理。
# 实例 docs.toml 的 [site] favicon 与 logo 优先于这里的默认值。
# favicon.ico 与仓库根目录的 assets/favicon.ico 保持一致。
<<< END U001866 >>>
<<< UNIT U001867 | cfg-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/defaults.toml:65-67 >>>
# 语言清单中键为语言标签，值为语言选择器里的显示名称。
# 默认语言由 [site] lang 指定，实例在 docs.toml 的 [site] locales 列出更多语言，
# 并在 [locales.<标签>] 中给出各自的名称与文案覆盖。
<<< END U001867 >>>
<<< UNIT U001868 | cfg-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/defaults.toml:71-73 >>>
# 页脚关于区块的配图默认使用品牌立绘，按钮图标可用内置名 afdian、github。
# 实例 docs.toml 中配置 [footer] 可覆盖文字，配置 [[footer.links]] 可覆盖按钮。
# text 与 links 设为空数组表示不显示该部分。
<<< END U001868 >>>
<<< UNIT U001869 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/base.py:125-125 >>>
# 命令层可以传入整个 [deploy] 表，也可以只传入对应子表。
<<< END U001869 >>>
<<< UNIT U001870 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/base.py:21-21 | ctx=DocsDeployError >>>
部署失败。``str()`` 返回本地化键。
<<< END U001870 >>>
<<< UNIT U001871 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/base.py:65-65 | ctx=DeployProvider >>>
部署提供方接口。
<<< END U001871 >>>
<<< UNIT U001872 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/base.py:70-70 | ctx=DeployProvider.plan >>>
返回目标摘要，不产生任何远端写入。
<<< END U001872 >>>
<<< UNIT U001873 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/s3.py:96-96 | ctx=S3Provider.plan >>>
返回目标摘要，不访问远端。
<<< END U001873 >>>
<<< UNIT U001874 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/sigv4.py:58-58 | ctx=sha256_hex >>>
返回请求体的 SHA-256 十六进制摘要。
<<< END U001874 >>>
<<< UNIT U001875 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/sigv4.py:63-63 | ctx=canonical_uri >>>
返回签名用的规范化路径，保留已有的百分号转义。
<<< END U001875 >>>
<<< UNIT U001876 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/vercel.py:163-163 >>>
# noqa: S603 - 命令由本模块组装，登录信息只通过环境变量传递
<<< END U001876 >>>
<<< UNIT U001877 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/deploy/vercel.py:62-62 | ctx=VercelProvider.plan >>>
返回目标摘要，不启动子进程。
<<< END U001877 >>>
<<< UNIT U001878 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:52-52 >>>
# VitePress dev 在镜像里写入依赖预构建与输出缓存，同步时既不同步也不清理。
<<< END U001878 >>>
<<< UNIT U001879 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:392-392 >>>
# noqa: S603 - argv 由固定组件拼接而成
<<< END U001879 >>>
<<< UNIT U001880 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:63-63 | ctx=SyncResult >>>
一次镜像同步的结果。
<<< END U001880 >>>
<<< UNIT U001881 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:72-72 | ctx=DevLock >>>
开发模式的运行锁内容。
<<< END U001881 >>>
<<< UNIT U001882 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:82-82 | ctx=lock_file >>>
返回实例的开发模式运行锁路径。
<<< END U001882 >>>
<<< UNIT U001883 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:87-87 | ctx=read_lock >>>
读取实例的运行锁。文件缺失或内容损坏时返回 ``None``。
<<< END U001883 >>>
<<< UNIT U001884 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:92-92 | ctx=read_lock_at >>>
读取指定路径的运行锁。文件缺失或内容损坏时返回 ``None``。
<<< END U001884 >>>
<<< UNIT U001885 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:110-110 | ctx=lock_active >>>
判断持有运行锁的进程是否仍在运行。
<<< END U001885 >>>
<<< UNIT U001886 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:231-231 | ctx=DevSession.url >>>
当前 dev 服务器地址。未就绪时为空字符串。
<<< END U001886 >>>
<<< UNIT U001887 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:235-235 | ctx=DevSession.run >>>
启动同步与 dev 服务器，阻塞到收到停止信号。
<<< END U001887 >>>
<<< UNIT U001888 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/dev.py:248-248 | ctx=DevSession.stop >>>
请求停止。可从其他线程调用。
<<< END U001888 >>>
<<< UNIT U001889 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:26-26 >>>
# 文档里的 ``{{I18N:key}}`` 是机器人模板语法。Vue 会把双花括号当插值，行内代码需显式 v-pre。
<<< END U001889 >>>
<<< UNIT U001890 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:219-219 >>>
# 没有概览页的包以第一页作为入口，供首页、分组页与顶栏链接复用。
<<< END U001890 >>>
<<< UNIT U001891 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:774-774 >>>
# 文档在源码树里用相对路径互相引用。生成站点时包目录已重新排列，跨包链接须转换为 URL。
<<< END U001891 >>>
<<< UNIT U001892 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:1128-1128 >>>
# 兼容仍用旧字段声明站点标志的包。显式 brand 提供者始终优先。
<<< END U001892 >>>
<<< UNIT U001893 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:1173-1173 >>>
# 品牌插槽的优先级依次为站点配置 > 品牌包声明 > 内置资源。
<<< END U001893 >>>
<<< UNIT U001894 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:1468-1468 >>>
# 未单独配置配图时使用角色立绘，品牌包缺失时由引擎预置的占位图代替。
<<< END U001894 >>>
<<< UNIT U001895 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:1674-1674 >>>
# 模块统一使用同级页面。其他包只要提供 development.md 也按同一结构处理。
<<< END U001895 >>>
<<< UNIT U001896 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:1696-1696 >>>
# Akari 主题用标签切换开发页，开发页不进入侧栏。其他主题保留全部页面。
<<< END U001896 >>>
<<< UNIT U001897 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/generator.py:135-135 | ctx=group_slug >>>
把分组名转换为文件名与 URL 片段。
<<< END U001897 >>>
<<< UNIT U001898 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/model.py:27-27 | ctx=doc_meta_paths >>>
返回参与合并的文档元数据文件，按全局配置、用户覆盖、文档根目录兼容文件的顺序。
<<< END U001898 >>>
<<< UNIT U001899 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/model.py:36-36 | ctx=doc_meta_path >>>
返回用于文件指纹与提示的元数据文件。没有文件时返回全局默认路径。
<<< END U001899 >>>
<<< UNIT U001900 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/model.py:64-64 | ctx=read_doc_meta >>>
读取并合并全局默认与用户覆盖。解析失败时跳过对应文件。
<<< END U001900 >>>
<<< UNIT U001901 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/model.py:173-173 | ctx=DocCatalog.keys >>>
返回全部包的 key，顺序与 :attr:`packages` 一致。
<<< END U001901 >>>
<<< UNIT U001902 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/model.py:251-251 | ctx=as_mapping >>>
把任意 JSON 值转换为映射，非映射返回空字典。
<<< END U001902 >>>
<<< UNIT U001903 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/server.py:95-95 >>>
# noqa: N802 - BaseHTTPRequestHandler 的协议方法名
<<< END U001903 >>>
<<< UNIT U001904 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/server.py:98-98 >>>
# noqa: N802 - BaseHTTPRequestHandler 的协议方法名
<<< END U001904 >>>
<<< UNIT U001905 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/server.py:39-39 | ctx=StaticServer.url >>>
服务根目录 URL。未启动时抛出 ``RuntimeError``。
<<< END U001905 >>>
<<< UNIT U001906 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/server.py:48-48 | ctx=StaticServer.start >>>
启动服务并返回根 URL。重复调用返回同一地址。
<<< END U001906 >>>
<<< UNIT U001907 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/server.py:61-61 | ctx=StaticServer.stop >>>
停止服务并释放端口。
<<< END U001907 >>>
<<< UNIT U001908 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/server.py:72-72 | ctx=StaticServer.wait >>>
阻塞到服务停止。
<<< END U001908 >>>
<<< UNIT U001909 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/state.py:22-22 | ctx=state_path >>>
状态文件路径。
<<< END U001909 >>>
<<< UNIT U001910 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/state.py:27-27 | ctx=load_state >>>
读取状态。文件缺失或损坏时返回空状态，构建据此重新生成。
<<< END U001910 >>>
<<< UNIT U001911 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/state.py:54-54 | ctx=save_build_state >>>
记录最近一次成功构建。
<<< END U001911 >>>
<<< UNIT U001912 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/theme.py:120-120 >>>
# 实例根目录优先。从源码克隆目录运行 CLI 时，再查找仓库内 vendor/ 下的模板 submodule。
<<< END U001912 >>>
<<< UNIT U001913 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/theme.py:68-68 | ctx=ThemeSpec.is_bundled >>>
是否为 CLI 内置主题。
<<< END U001913 >>>
<<< UNIT U001914 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/theme_sync.py:166-166 >>>
# noqa: S603 - 命令由本模块组装，参数固定
<<< END U001914 >>>
<<< UNIT U001915 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/theme_sync.py:195-195 >>>
# noqa: S603 - 命令由本模块组装，参数固定
<<< END U001915 >>>
<<< UNIT U001916 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/theme_sync.py:46-46 | ctx=source_repository >>>
返回本 CLI 源码所在的仓库根目录。安装形态没有源码仓库时返回 ``None``。
<<< END U001916 >>>
<<< UNIT U001917 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:171-171 >>>
# 为兼容旧调用，测试只提供 package.json 与 lock 且没有主题目录时，不读取 docs-theme.json。
<<< END U001917 >>>
<<< UNIT U001918 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:253-253 >>>
# noqa: S603 - 参数为固定可执行文件与版本选项
<<< END U001918 >>>
<<< UNIT U001919 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:271-271 >>>
# 测试注入的 runner 优先，保证调用参数可检查且不启动真实子进程。
<<< END U001919 >>>
<<< UNIT U001920 | py-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:280-280 >>>
# 输出同时转发给终端与 TUI，颜色转义码在非终端消费方会原样显示，因此统一关闭颜色。
<<< END U001920 >>>
<<< UNIT U001921 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:282-282 >>>
# noqa: S603 - 命令由本模块组装，不含用户输入
<<< END U001921 >>>
<<< UNIT U001922 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:311-311 >>>
# noqa: S603 - 命令由本模块组装，不含用户输入
<<< END U001922 >>>
<<< UNIT U001923 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:58-58 | ctx=parse_node_major >>>
从 ``v24.21.0`` 形式的输出里提取主版本号。
<<< END U001923 >>>
<<< UNIT U001924 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:192-192 | ctx=build_argv >>>
组装 VitePress 构建命令。
<<< END U001924 >>>
<<< UNIT U001925 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:228-228 | ctx=template_version >>>
读取模板 ``package.json`` 的版本号，供构建校验信息使用。
<<< END U001925 >>>
<<< UNIT U001926 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/toolchain.py:237-237 | ctx=package_argv >>>
组装包管理器命令。Windows 下 npm 是批处理脚本，须通过 ``cmd /c`` 启动。
<<< END U001926 >>>
<<< UNIT U001927 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/watch.py:53-53 | ctx=Change >>>
一次文件改动。
<<< END U001927 >>>
<<< UNIT U001928 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/watch.py:89-89 | ctx=PathWatcher.start >>>
启动观察者。目标路径不存在时跳过。
<<< END U001928 >>>
<<< UNIT U001929 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/watch.py:103-103 | ctx=PathWatcher.stop >>>
停止观察者。
<<< END U001929 >>>
<<< UNIT U001930 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/watch.py:113-113 | ctx=PathWatcher.report >>>
记录观察者交付的原始事件。
<<< END U001930 >>>
<<< UNIT U001931 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/watch.py:133-133 | ctx=PathWatcher.poll >>>
等待一批改动。超时返回空元组。
<<< END U001931 >>>
<<< UNIT U001932 | py-docstring | packages/akari-bot-cli/akaribot/cli/docs_engine/watch.py:153-153 | ctx=PathWatcher.wake >>>
让阻塞在 :meth:`poll` 上的调用方立即返回。
<<< END U001932 >>>
<<< UNIT U001933 | py-comment | packages/akari-bot-cli/akaribot/cli/i18n.py:17-17 >>>
# 与 core 的 lang_list 保持一致。新增语言时两边一起添加。
<<< END U001933 >>>
<<< UNIT U001934 | py-comment | packages/akari-bot-cli/akaribot/cli/i18n.py:20-20 >>>
# 缺少对应键时按英文、中文的顺序回退。
<<< END U001934 >>>
<<< UNIT U001935 | py-comment | packages/akari-bot-cli/akaribot/cli/i18n.py:55-55 >>>
# 只给出主语言时获取该语言的第一个变体（en → en_us，zh → zh_cn）。
<<< END U001935 >>>
<<< UNIT U001936 | py-comment | packages/akari-bot-cli/akaribot/cli/i18n.py:126-127 >>>
# typer 的 ``help=`` 在导入阶段求值，而根回调需要等待参数解析完成才执行，因此仅通过 ``set_locale()``
# 无法本地化 ``--help``。这里提前读取一次 argv，使导入阶段获取到用户指定的语言。
<<< END U001936 >>>
<<< UNIT U001937 | py-docstring | packages/akari-bot-cli/akaribot/cli/i18n.py:121-121 | ctx=current_locale >>>
返回当前语言码。
<<< END U001937 >>>
<<< UNIT U001938 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:37-38 >>>
# 被覆写方法的 ctx 参数类型。typer ≥0.27 把 click 内置为 ``typer._click`` 且不再声明外部 click
# 依赖，``click.Context`` 既不是同一个类，干净安装里也无法导入（CLI wheel 曾因此安装后即崩溃）。
<<< END U001938 >>>
<<< UNIT U001939 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/instance.py:41-41 >>>
# typer <0.27 用真实 click，该版本由 typer 自己声明这条依赖
<<< END U001939 >>>
<<< UNIT U001940 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:95-95 >>>
# 非托管模式要用的解释器路径。冻结产物下没有可用的 sys.executable。
<<< END U001940 >>>
<<< UNIT U001941 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:100-100 >>>
# 实例 ID 是 ``target_id`` 前缀的一部分，由小写字母、数字与下划线组成，创建后不可重命名。
<<< END U001941 >>>
<<< UNIT U001942 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:105-105 >>>
# 实例目录结构见 monorepo_refactor_plan.md §2.3。config 的子树由 config sync 按需补齐。
<<< END U001942 >>>
<<< UNIT U001943 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:200-202 >>>
# 非冻结时当前解释器就是可用的 Python，且与项目要求的版本一致。
# 冻结后 sys.executable 指向 CLI 二进制自身，才需要回退到系统搜索。
# 回退时优先带版本号的名字，避免获取到过旧的 python3。
<<< END U001943 >>>
<<< UNIT U001944 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:345-345 >>>
# registry --json 用 ``modules`` 作键名。``provides_modules`` 是 manifest 与 module list 的写法。
<<< END U001944 >>>
<<< UNIT U001945 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:372-372 >>>
# 按包名去重依赖声明，保留首次出现的写法。无法识别包名的声明按整串比较。
<<< END U001945 >>>
<<< UNIT U001946 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:663-664 >>>
# 入口只输出一行 JSON，但 stdout 可能被警告或第三方输出污染，故自末行向前找第一段可解析且带
# ``status`` 的对象。找不到时返回 ``None``，由调用方回退到退出码与 stderr 的解释。
<<< END U001946 >>>
<<< UNIT U001947 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:1094-1094 >>>
# 回传不可解析（core 版本过旧、入口缺失、进程被信号杀死）时回退到退出码与 stderr 的既有解释。
<<< END U001947 >>>
<<< UNIT U001948 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:1102-1102 >>>
# 子进程按 cwd 解析实例内的相对路径（默认 SQLite 链接即其一），不以实例根目录为基准就会落到调用目录。
<<< END U001948 >>>
<<< UNIT U001949 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:1165-1166 >>>
# 兼容顶层数组、``packages``/``entries``/``installed`` 列表、``modules`` 与 ``adapters``
# 分组，以及“包名到对象”的映射四种形态，core 只需命中其一。
<<< END U001949 >>>
<<< UNIT U001950 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/instance.py:1231-1231 >>>
# noqa: BLE001 - 注册表不可用按“没有默认实例”处理
<<< END U001950 >>>
<<< UNIT U001951 | py-comment | packages/akari-bot-cli/akaribot/cli/instance.py:1293-1293 >>>
# 这条是“既没给路径也没设环境变量”的独立场景，需要完整诊断句而不只是操作提示。
<<< END U001951 >>>
<<< UNIT U001952 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:68-68 | ctx=FlatCommandGroup.collect_usage_pieces >>>
usage 里不追加子命令占位符。
<<< END U001952 >>>
<<< UNIT U001953 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:89-89 | ctx=PassthroughCommandGroup >>>
把未识别参数原样传递给 core 的单命令分组。
<<< END U001953 >>>
<<< UNIT U001954 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:120-120 | ctx=no_instance_hint >>>
不在任何实例内时的可执行提示。运行阶段取值，不冻结语言。
<<< END U001954 >>>
<<< UNIT U001955 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:125-125 | ctx=CliError >>>
面向用户的失败。命令层捕获后打印消息并以非零码退出。
<<< END U001955 >>>
<<< UNIT U001956 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:129-129 | ctx=InstanceNotFound >>>
实例根目录不存在或其中没有 akaribot.toml。
<<< END U001956 >>>
<<< UNIT U001957 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:147-147 | ctx=fail >>>
打印错误并退出。消息须自带可执行的下一步提示。
<<< END U001957 >>>
<<< UNIT U001958 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:153-153 | ctx=warn >>>
打印警告，不中断流程。
<<< END U001958 >>>
<<< UNIT U001959 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:158-158 | ctx=ok >>>
打印成功项。
<<< END U001959 >>>
<<< UNIT U001960 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:163-163 | ctx=step >>>
打印流水线的步骤标题。
<<< END U001960 >>>
<<< UNIT U001961 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:168-168 | ctx=now_iso >>>
当前时刻的 ISO 8601 UTC 表示，形如 ``2026-09-18T00:00:00Z``。
<<< END U001961 >>>
<<< UNIT U001962 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:173-173 | ctx=split_names >>>
把可重复选项与逗号分隔写法拆成名字列表，去重并保持顺序。
<<< END U001962 >>>
<<< UNIT U001963 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:184-184 | ctx=is_windows >>>
当前平台是否为 Windows。
<<< END U001963 >>>
<<< UNIT U001964 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:213-213 | ctx=venv_python_path >>>
虚拟环境中的解释器路径，兼容 posix 与 Windows 两种布局。
<<< END U001964 >>>
<<< UNIT U001965 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:220-220 | ctx=venv_scripts_dir >>>
虚拟环境中的可执行文件目录。
<<< END U001965 >>>
<<< UNIT U001966 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:313-313 | ctx=PackageInfo.display_name >>>
列表展示用的简称，无法获取简称时回退到包名。
<<< END U001966 >>>
<<< UNIT U001967 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:490-490 | ctx=InstanceMeta >>>
``akaribot.toml`` 的内存视图。写回时保持注释与书写格式（tomlkit）。
<<< END U001967 >>>
<<< UNIT U001968 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:497-497 | ctx=InstanceMeta.path >>>
元数据文件路径。
<<< END U001968 >>>
<<< UNIT U001969 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:559-559 | ctx=InstanceMeta.schema >>>
元数据结构版本。
<<< END U001969 >>>
<<< UNIT U001970 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:564-564 | ctx=InstanceMeta.name >>>
实例名。
<<< END U001970 >>>
<<< UNIT U001971 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:569-569 | ctx=InstanceMeta.created_at >>>
创建时刻。
<<< END U001971 >>>
<<< UNIT U001972 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:574-574 | ctx=InstanceMeta.locale >>>
实例默认语言。
<<< END U001972 >>>
<<< UNIT U001973 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:579-579 | ctx=InstanceMeta.mode >>>
``installed`` 或 ``workspace``，描述源代码来源。
<<< END U001973 >>>
<<< UNIT U001974 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:584-584 | ctx=InstanceMeta.venv >>>
实例 venv 的相对路径。空字符串表示不托管、使用当前环境。
<<< END U001974 >>>
<<< UNIT U001975 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:589-589 | ctx=InstanceMeta.requirements >>>
实例清单里记录的运行库需求串，按记录顺序。
<<< END U001975 >>>
<<< UNIT U001976 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:594-594 | ctx=InstanceMeta.workspace_root >>>
本地工作区根目录。非空时从本地路径安装。
<<< END U001976 >>>
<<< UNIT U001977 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:599-599 | ctx=InstanceMeta.registry_sources >>>
registry.json 的来源列表。
<<< END U001977 >>>
<<< UNIT U001978 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:604-604 | ctx=InstanceMeta.set_venv >>>
设置 venv 相对路径。空字符串表示释放托管。
<<< END U001978 >>>
<<< UNIT U001979 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:608-608 | ctx=InstanceMeta.set_requirements >>>
设置记录的运行库需求串，按包名去重后写入磁盘。
<<< END U001979 >>>
<<< UNIT U001980 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:612-612 | ctx=InstanceMeta.set_workspace_root >>>
设置本地工作区根目录。
<<< END U001980 >>>
<<< UNIT U001981 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:616-616 | ctx=InstanceMeta.set_locale >>>
设置实例语言。
<<< END U001981 >>>
<<< UNIT U001982 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:620-620 | ctx=InstanceMeta.set_mode >>>
设置源代码来源模式。
<<< END U001982 >>>
<<< UNIT U001983 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:624-624 | ctx=InstanceMeta.save >>>
原子写回 ``akaribot.toml``，未知键与注释一并保留。
<<< END U001983 >>>
<<< UNIT U001984 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:703-703 | ctx=Instance.detached >>>
构造不读取磁盘的实例对象，供写入磁盘前的解析与 ``--dry-run`` 使用。
<<< END U001984 >>>
<<< UNIT U001985 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:725-725 | ctx=Instance.managed >>>
是否由 CLI 托管 venv。
<<< END U001985 >>>
<<< UNIT U001986 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:730-730 | ctx=Instance.venv_dir >>>
实例 venv 目录。未托管时返回默认位置，仅供展示。
<<< END U001986 >>>
<<< UNIT U001987 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:749-749 | ctx=Instance.python_exists >>>
实例解释器是否存在。
<<< END U001987 >>>
<<< UNIT U001988 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:754-754 | ctx=Instance.workspace_root >>>
本地工作区根目录。未配置时为 ``None``。
<<< END U001988 >>>
<<< UNIT U001989 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:760-760 | ctx=Instance.config_dir >>>
配置目录。
<<< END U001989 >>>
<<< UNIT U001990 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:764-764 | ctx=Instance.core_module >>>
将入口名补全为完整模块路径。已含点号者原样返回。
<<< END U001990 >>>
<<< UNIT U001991 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:770-770 | ctx=Instance.python_argv >>>
以实例解释器执行任意参数。
<<< END U001991 >>>
<<< UNIT U001992 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:774-774 | ctx=Instance.module_argv >>>
以实例解释器执行 ``-m <module>``。
<<< END U001992 >>>
<<< UNIT U001993 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:778-778 | ctx=Instance.core_argv >>>
以实例解释器执行 ``-m akaribot.core.entrypoints.<entrypoint>``。
<<< END U001993 >>>
<<< UNIT U001994 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:809-809 | ctx=Instance.run_core_capture >>>
执行 core 入口并捕获输出，供解析 JSON 回传。
<<< END U001994 >>>
<<< UNIT U001995 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:813-813 | ctx=Instance.run_module >>>
执行任意模块并返回退出码，标准流直接继承。
<<< END U001995 >>>
<<< UNIT U001996 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:828-828 | ctx=Instance.run_python_capture >>>
以实例解释器执行任意参数并捕获输出，供版本探测等一次性查询使用。
<<< END U001996 >>>
<<< UNIT U001997 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:860-860 | ctx=Instance.invalidate >>>
清空已安装包缓存与 registry 回传缓存。
<<< END U001997 >>>
<<< UNIT U001998 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:865-865 | ctx=Instance.find_package >>>
按包名、简称或导入路径查找已安装包。
<<< END U001998 >>>
<<< UNIT U001999 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:962-962 | ctx=Instance.lock_path >>>
返回实例级锁文件路径。
<<< END U001999 >>>
<<< UNIT U002000 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:1256-1256 | ctx=default_instance_root >>>
默认实例根目录。未定位到时回退到当前工作目录，供各页数据源构造子进程用。
<<< END U002000 >>>
<<< UNIT U002001 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:1299-1299 | ctx=require_instance >>>
命令层入口，解析实例并在失败时打印提示后退出。
<<< END U002001 >>>
<<< UNIT U002002 | py-docstring | packages/akari-bot-cli/akaribot/cli/instance.py:1309-1309 | ctx=relative_venv_display >>>
venv 路径的展示形式，托管模式显示相对路径，非托管模式显示当前解释器。
<<< END U002002 >>>
<<< UNIT U002003 | py-comment | packages/akari-bot-cli/akaribot/cli/instances.py:30-30 >>>
# 名称只用于展示与命令行引用，故限制在小写字母、数字、连字符与下划线。
<<< END U002003 >>>
<<< UNIT U002004 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/instances.py:100-100 >>>
# noqa: BLE001 - 读不出语言不影响添加
<<< END U002004 >>>
<<< UNIT U002005 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/instances.py:161-161 >>>
# noqa: BLE001 - 解析失败的原因如实上报
<<< END U002005 >>>
<<< UNIT U002006 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/instances.py:191-191 >>>
# noqa: BLE001 - 读不出默认名时按未设置处理
<<< END U002006 >>>
<<< UNIT U002007 | py-inline-comment | packages/akari-bot-cli/akaribot/cli/instances.py:328-328 >>>
# noqa: BLE001 - 探测失败按未知处理，不中断调用方
<<< END U002007 >>>
<<< UNIT U002008 | py-docstring | packages/akari-bot-cli/akaribot/cli/instances.py:35-35 | ctx=RegistryError >>>
注册表不可用（文件损坏、名称重复或实例不存在）。
<<< END U002008 >>>
<<< UNIT U002009 | py-docstring | packages/akari-bot-cli/akaribot/cli/instances.py:50-50 | ctx=registry_path >>>
返回注册表文件路径。
<<< END U002009 >>>
<<< UNIT U002010 | py-docstring | packages/akari-bot-cli/akaribot/cli/instances.py:127-127 | ctx=InstanceEntry.to_mapping >>>
转换为写入磁盘用的映射。
<<< END U002010 >>>
<<< UNIT U002011 | py-docstring | packages/akari-bot-cli/akaribot/cli/instances.py:139-139 | ctx=InstanceEntry.exists >>>
实例目录是否仍是一个实例（含 ``akaribot.toml``）。
<<< END U002011 >>>
<<< UNIT U002012 | py-docstring | packages/akari-bot-cli/akaribot/cli/instances.py:186-186 | ctx=InstanceRegistry.default_name >>>
返回默认实例名。未设置时为空字符串。
<<< END U002012 >>>
<<< UNIT U002013 | py-docstring | packages/akari-bot-cli/akaribot/cli/instances.py:196-196 | ctx=InstanceRegistry.get >>>
按名称获取一条记录。不存在时返回 ``None``。
<<< END U002013 >>>
<<< UNIT U002014 | py-docstring | packages/akari-bot-cli/akaribot/cli/instances.py:203-203 | ctx=InstanceRegistry.find_by_root >>>
按实例根目录获取记录。比较真实路径，软链接与相对路径都能命中。
<<< END U002014 >>>
<<< UNIT U002015 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:2-2 | ctx=cli.adapter.fail_prefix >>>
错误：${message}
<<< END U002015 >>>
<<< UNIT U002016 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:3-3 | ctx=cli.adapter.help >>>
适配器与实例管理
<<< END U002016 >>>
<<< UNIT U002017 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:4-4 | ctx=cli.adapter.instance.add.arg_instance_id >>>
实例 ID，须匹配 [a-z0-9_]{1,24}。省略表示默认实例。
<<< END U002017 >>>
<<< UNIT U002018 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:5-5 | ctx=cli.adapter.instance.add.bad_table >>>
适配器 ${platform} 的配置表名 ${table} 不符合 bot_* 约定。
<<< END U002018 >>>
<<< UNIT U002019 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:6-6 | ctx=cli.adapter.instance.add.checklist_title >>>
需要填写的字段
<<< END U002019 >>>
<<< UNIT U002020 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:8-8 | ctx=cli.adapter.instance.add.column_comment >>>
说明
<<< END U002020 >>>
<<< UNIT U002021 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:9-9 | ctx=cli.adapter.instance.add.column_key >>>
键
<<< END U002021 >>>
<<< UNIT U002022 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:10-10 | ctx=cli.adapter.instance.add.column_table >>>
表名
<<< END U002022 >>>
<<< UNIT U002023 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:11-11 | ctx=cli.adapter.instance.add.column_type >>>
类型
<<< END U002023 >>>
<<< UNIT U002024 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:12-12 | ctx=cli.adapter.instance.add.created >>>
已创建 ${target}
<<< END U002024 >>>
<<< UNIT U002025 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:13-13 | ctx=cli.adapter.instance.add.doctor_note >>>
同一平台的两个实例不得配置相同登录信息，`akaribot doctor` 会检查。
<<< END U002025 >>>
<<< UNIT U002026 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:14-14 | ctx=cli.adapter.instance.add.enable_hint >>>
  akaribot config set enable true --table ${table}    # 确认登录信息无误后再开启
<<< END U002026 >>>
<<< UNIT U002027 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:15-15 | ctx=cli.adapter.instance.add.enable_line >>>
  enable：false（已显式写入，填写完登录信息后自行开启）
<<< END U002027 >>>
<<< UNIT U002028 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:16-16 | ctx=cli.adapter.instance.add.exists >>>
实例已存在：${table}（${path}）
<<< END U002028 >>>
<<< UNIT U002029 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:17-17 | ctx=cli.adapter.instance.add.exists_hint >>>
如需新增同平台的另一个实例，请换一个实例 ID。
<<< END U002029 >>>
<<< UNIT U002030 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:18-18 | ctx=cli.adapter.instance.add.help >>>
新建适配器实例配置。

实例 ID 一旦使用请勿更改，它是 ``target_id`` 前缀的一部分，修改名称需要跨核心表与模块表迁移数据。
生成的配置文件里 ``enable`` 显式设为 ``false``，填写完登录信息后自行开启。
<<< END U002030 >>>
<<< UNIT U002031 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:19-19 | ctx=cli.adapter.instance.add.inferred_note >>>
  注：registry 未提供 platform_name，client_name 按平台名推断。
<<< END U002031 >>>
<<< UNIT U002032 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:20-20 | ctx=cli.adapter.instance.add.invalid_id >>>
实例 ID ${instance_id} 不合法。
<<< END U002032 >>>
<<< UNIT U002033 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:21-21 | ctx=cli.adapter.instance.add.invalid_id_hint >>>
实例 ID 须匹配 [a-z0-9_]{1,24}，只允许小写字母、数字与下划线，长度 1 到 24。
<<< END U002033 >>>
<<< UNIT U002034 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:22-22 | ctx=cli.adapter.instance.add.invalid_toml >>>
生成的配置内容不是合法 TOML：${error}
<<< END U002034 >>>
<<< UNIT U002035 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:23-23 | ctx=cli.adapter.instance.add.next_steps >>>
下一步：
<<< END U002035 >>>
<<< UNIT U002036 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:24-24 | ctx=cli.adapter.instance.add.no_pending >>>
模板没有待填写字段。确认监听地址与登录信息后执行：
<<< END U002036 >>>
<<< UNIT U002037 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:25-25 | ctx=cli.adapter.instance.add.not_installed >>>
平台 ${platform} 未安装到本实例。
<<< END U002037 >>>
<<< UNIT U002038 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:26-26 | ctx=cli.adapter.instance.add.not_installed_hint >>>
已安装的适配器：${installed}
<<< END U002038 >>>
<<< UNIT U002039 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:27-27 | ctx=cli.adapter.instance.add.set_hint >>>
  akaribot config set ${field} <值> --table ${table}
<<< END U002039 >>>
<<< UNIT U002040 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:28-28 | ctx=cli.adapter.instance.add.table_line >>>
  表名：${table}（密钥表 ${secret_table}）
<<< END U002040 >>>
<<< UNIT U002041 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:29-29 | ctx=cli.adapter.instance.add.target_exists >>>
目标文件已存在：${target}
<<< END U002041 >>>
<<< UNIT U002042 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:30-30 | ctx=cli.adapter.instance.add.target_exists_hint >>>
请换一个实例 ID，或先移除既有实例配置。
<<< END U002042 >>>
<<< UNIT U002043 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:31-31 | ctx=cli.adapter.instance.add.template_empty >>>
适配器 ${platform} 的配置模板为空，无法生成实例配置。
<<< END U002043 >>>
<<< UNIT U002044 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:32-32 | ctx=cli.adapter.instance.add.template_empty_hint >>>
请确认该适配器包声明了 config.py 模板（on_bot_config）。
<<< END U002044 >>>
<<< UNIT U002045 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:33-33 | ctx=cli.adapter.instance.add.template_unavailable >>>
无法获取 ${table} 的配置模板：${error}
<<< END U002045 >>>
<<< UNIT U002046 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:34-34 | ctx=cli.adapter.instance.add.write_failed >>>
无法写入 ${target}：${error}
<<< END U002046 >>>
<<< UNIT U002047 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:35-35 | ctx=cli.adapter.instance.arg_platform >>>
平台名（适配器 entry point 名），如 telegram。
<<< END U002047 >>>
<<< UNIT U002048 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:36-36 | ctx=cli.adapter.instance.default_id >>>
默认
<<< END U002048 >>>
<<< UNIT U002049 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:37-37 | ctx=cli.adapter.instance.help >>>
适配器实例的增删。每个实例是 config/adapters/<平台>[-<实例 ID>].toml 中的一张表。${rename_note}
<<< END U002049 >>>
<<< UNIT U002050 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:38-38 | ctx=cli.adapter.instance.none >>>
（无）
<<< END U002050 >>>
<<< UNIT U002051 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:39-39 | ctx=cli.adapter.instance.registry_unavailable >>>
无法获取已安装适配器清单，无法确认平台是否已安装：${note}
<<< END U002051 >>>
<<< UNIT U002052 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:40-40 | ctx=cli.adapter.instance.remove.arg_instance_id >>>
实例 ID。省略表示默认实例。
<<< END U002052 >>>
<<< UNIT U002053 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:41-41 | ctx=cli.adapter.instance.remove.config_file >>>
配置文件：${path}
<<< END U002053 >>>
<<< UNIT U002054 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:42-42 | ctx=cli.adapter.instance.remove.dry_run >>>
--dry-run：未做任何改动。
<<< END U002054 >>>
<<< UNIT U002055 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:43-43 | ctx=cli.adapter.instance.remove.enabled_warning >>>
该实例当前 enable=true。配置文件删除后，已在运行的守护进程仍会继续运行该实例，请重启使其生效。
<<< END U002055 >>>
<<< UNIT U002056 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:44-44 | ctx=cli.adapter.instance.remove.failed >>>
无法移除 ${path}：${error}
<<< END U002056 >>>
<<< UNIT U002057 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:45-45 | ctx=cli.adapter.instance.remove.file_removed >>>
已删除配置文件 ${path}
<<< END U002057 >>>
<<< UNIT U002058 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:46-46 | ctx=cli.adapter.instance.remove.help >>>
移除适配器实例配置。

只删除该实例的配置文件，场景与用户数据保留。实例 ID 一旦使用请勿更改，本命令不提供重命名功能。
<<< END U002058 >>>
<<< UNIT U002059 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:47-47 | ctx=cli.adapter.instance.remove.keep_hint >>>
数据保留：${client_name} 的场景与用户数据仍在数据库中，本命令只处理配置文件。
<<< END U002059 >>>
<<< UNIT U002060 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:48-48 | ctx=cli.adapter.instance.remove.not_found >>>
未找到实例 ${platform}/${instance}。
<<< END U002060 >>>
<<< UNIT U002061 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:49-49 | ctx=cli.adapter.instance.remove.not_found_hint >>>
现有实例：${available}
<<< END U002061 >>>
<<< UNIT U002062 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:50-50 | ctx=cli.adapter.instance.remove.option_dry_run >>>
只打印将执行的操作，不做任何改动。
<<< END U002062 >>>
<<< UNIT U002063 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:51-51 | ctx=cli.adapter.instance.remove.recheck >>>
`akaribot adapter list` 可复核当前实例清单。
<<< END U002063 >>>
<<< UNIT U002064 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:52-52 | ctx=cli.adapter.instance.remove.table_removed >>>
已从 ${path} 中移除表 ${table}（该文件还含其他表）。
<<< END U002064 >>>
<<< UNIT U002065 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:53-53 | ctx=cli.adapter.instance.remove.target >>>
目标实例：${summary}
<<< END U002065 >>>
<<< UNIT U002066 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:54-54 | ctx=cli.adapter.instance.rename_note >>>
不提供 instance rename，因为实例 ID 是 target_id 前缀的一部分，修改名称需要跨 5 张核心表与 N 张模块表迁移 target_id / sender_id 前缀，收益与风险严重不成比例。实例 ID 一旦使用请勿更改。
<<< END U002066 >>>
<<< UNIT U002067 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:56-56 | ctx=cli.adapter.list.column_instance_id >>>
实例 ID
<<< END U002067 >>>
<<< UNIT U002068 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:57-57 | ctx=cli.adapter.list.column_listen >>>
监听地址
<<< END U002068 >>>
<<< UNIT U002069 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:58-58 | ctx=cli.adapter.list.column_notes >>>
备注
<<< END U002069 >>>
<<< UNIT U002070 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:59-59 | ctx=cli.adapter.list.empty >>>
未发现任何适配器实例配置。
<<< END U002070 >>>
<<< UNIT U002071 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:60-60 | ctx=cli.adapter.list.empty_hint >>>
可用 `akaribot adapter instance add <平台> [实例 ID]` 新建实例配置。
<<< END U002071 >>>
<<< UNIT U002072 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:61-61 | ctx=cli.adapter.list.enable_missing >>>
[yellow]缺少 enable[/yellow]
<<< END U002072 >>>
<<< UNIT U002073 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:62-62 | ctx=cli.adapter.list.help >>>
按平台分组列出全部适配器实例。

实例 ID、``client_name``、``enable``、监听地址来自 ``config/adapters/*.toml``。平台是否已安装来自
``registry --json``。
<<< END U002073 >>>
<<< UNIT U002074 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:63-63 | ctx=cli.adapter.list.inferred_note >>>
注：registry 未提供 platform_name，client_name 按平台名推断。以适配器实际声明的展示名为准。
<<< END U002074 >>>
<<< UNIT U002075 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:64-64 | ctx=cli.adapter.list.instance_root >>>
实例根目录：${path}
<<< END U002075 >>>
<<< UNIT U002076 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:65-65 | ctx=cli.adapter.list.issue_enable_missing >>>
缺少 enable 键（视为未启用）
<<< END U002076 >>>
<<< UNIT U002077 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:66-66 | ctx=cli.adapter.list.issue_instance_id >>>
实例 ID 不符合 [a-z0-9_]{1,24}
<<< END U002077 >>>
<<< UNIT U002078 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:67-67 | ctx=cli.adapter.list.issue_orphan >>>
孤立配置：该平台的适配器包未安装
<<< END U002078 >>>
<<< UNIT U002079 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:68-68 | ctx=cli.adapter.list.legacy_note >>>
注：以上含扁平布局配置（config/bot_*.toml），分层布局迁移后将移至 config/adapters/。
<<< END U002079 >>>
<<< UNIT U002080 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:69-69 | ctx=cli.adapter.list.not_installed >>>
（适配器未安装）
<<< END U002080 >>>
<<< UNIT U002081 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:70-70 | ctx=cli.adapter.list.option_json >>>
以 JSON 输出，供 TUI 与脚本使用。
<<< END U002081 >>>
<<< UNIT U002082 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:72-72 | ctx=cli.adapter.list.registry_unavailable >>>
（已安装清单不可用）
<<< END U002082 >>>
<<< UNIT U002083 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:73-73 | ctx=cli.adapter.not_instance >>>
未找到实例：自 ${start} 起未发现 ${meta}。
<<< END U002083 >>>
<<< UNIT U002084 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:74-74 | ctx=cli.adapter.not_instance_hint >>>
可执行的操作：
  akaribot init <目录>              新建实例
  akaribot migrate legacy <目录>    迁移既有部署
  或在实例目录内执行，或设置 AKARI_INSTANCE_DIR=<实例根目录>
<<< END U002084 >>>
<<< UNIT U002085 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:75-75 | ctx=cli.adapter.registry_inferred >>>
client_name 与安装状态均按平台名推断，可能与适配器实际声明不符。
<<< END U002085 >>>
<<< UNIT U002086 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:76-76 | ctx=cli.adapter.registry_unavailable >>>
无法获取已安装适配器清单：${note}
<<< END U002086 >>>
<<< UNIT U002087 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:77-77 | ctx=cli.adapter.system_python_missing >>>
找不到系统 Python。请设置 AKARIBOT_PYTHON 指向实例要使用的解释器。
<<< END U002087 >>>
<<< UNIT U002088 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:78-78 | ctx=cli.adapter.warn_prefix >>>
警告：${message}
<<< END U002088 >>>
<<< UNIT U002089 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:79-79 | ctx=cli.app.help >>>
AkariBot 实例管理工具。
<<< END U002089 >>>
<<< UNIT U002090 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:80-80 | ctx=cli.app.version >>>
打印版本后退出
<<< END U002090 >>>
<<< UNIT U002091 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:81-81 | ctx=cli.common.action_done >>>
${what}完成
<<< END U002091 >>>
<<< UNIT U002092 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:82-82 | ctx=cli.common.action_failed >>>
${what}失败：${detail}
<<< END U002092 >>>
<<< UNIT U002093 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:84-84 | ctx=cli.common.error_label >>>
错误
<<< END U002093 >>>
<<< UNIT U002094 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:85-85 | ctx=cli.common.instance_option >>>
实例根目录。默认自当前目录向上查找 akaribot.toml，或读取环境变量 AKARI_INSTANCE_DIR
<<< END U002094 >>>
<<< UNIT U002095 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:86-86 | ctx=cli.common.json_option >>>
以 JSON 输出，供脚本消费
<<< END U002095 >>>
<<< UNIT U002096 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:87-87 | ctx=cli.common.lang_option >>>
界面语言，如 zh_cn / en_us。默认读取 AKARIBOT_LANG、实例配置与系统语言
<<< END U002096 >>>
<<< UNIT U002097 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:89-89 | ctx=cli.common.no_output >>>
无输出
<<< END U002097 >>>
<<< UNIT U002098 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:90-90 | ctx=cli.common.table_option >>>
配置表名，如 module_wiki、bot_telegram
<<< END U002098 >>>
<<< UNIT U002099 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:91-91 | ctx=cli.common.warning_label >>>
警告
<<< END U002099 >>>
<<< UNIT U002100 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:92-92 | ctx=cli.common.yes_option >>>
不询问，直接执行
<<< END U002100 >>>
<<< UNIT U002101 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:93-93 | ctx=cli.config.edit.config_file >>>
配置文件：${path}
<<< END U002101 >>>
<<< UNIT U002102 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:94-94 | ctx=cli.config.edit.external >>>
外部编辑器：akaribot config open
<<< END U002102 >>>
<<< UNIT U002103 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:95-95 | ctx=cli.config.edit.help >>>
提示三种编辑方式（表单与文本模式在 TUI 里）。
<<< END U002103 >>>
<<< UNIT U002104 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:96-96 | ctx=cli.config.edit.script >>>
脚本写入：akaribot config set <键> <值> --table <表名>
<<< END U002104 >>>
<<< UNIT U002105 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:97-97 | ctx=cli.config.edit.tui >>>
表单模式与原始文本模式：akaribot tui → Config 页
<<< END U002105 >>>
<<< UNIT U002106 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:98-98 | ctx=cli.config.entry_failed >>>
配置入口以退出码 ${code} 结束。
<<< END U002106 >>>
<<< UNIT U002107 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:99-99 | ctx=cli.config.entry_not_json >>>
配置入口返回的不是 JSON：${error}
<<< END U002107 >>>
<<< UNIT U002108 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:100-100 | ctx=cli.config.get.help >>>
读取单个配置项。
<<< END U002108 >>>
<<< UNIT U002109 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:101-101 | ctx=cli.config.help >>>
配置读写：list / schema / get / set / open
<<< END U002109 >>>
<<< UNIT U002110 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:102-102 | ctx=cli.config.list.help >>>
列出实例已有的配置表。
<<< END U002110 >>>
<<< UNIT U002111 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:103-103 | ctx=cli.config.open.editor_failed >>>
编辑器以退出码 ${code} 结束。
<<< END U002111 >>>
<<< UNIT U002112 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:104-104 | ctx=cli.config.open.help >>>
用外部编辑器打开配置文件（第三种编辑模式）。
<<< END U002112 >>>
<<< UNIT U002113 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:105-105 | ctx=cli.config.open.missing >>>
配置文件不存在：${target}
<<< END U002113 >>>
<<< UNIT U002114 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:106-106 | ctx=cli.config.open.no_editor >>>
找不到编辑器 ${editor}，请设置 $EDITOR 或 $VISUAL。
<<< END U002114 >>>
<<< UNIT U002115 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:107-107 | ctx=cli.config.open.opening >>>
打开 ${target}
<<< END U002115 >>>
<<< UNIT U002116 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:108-108 | ctx=cli.config.placeholders.column_placeholder >>>
待填写
<<< END U002116 >>>
<<< UNIT U002117 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:109-109 | ctx=cli.config.placeholders.column_table >>>
配置表
<<< END U002117 >>>
<<< UNIT U002118 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:110-110 | ctx=cli.config.placeholders.column_total >>>
总项数
<<< END U002118 >>>
<<< UNIT U002119 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:111-111 | ctx=cli.config.placeholders.failed_line >>>
未统计 ${count} 张表：${detail}
<<< END U002119 >>>
<<< UNIT U002120 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:112-112 | ctx=cli.config.placeholders.help >>>
统计各表的待填写占位符（core 判定）
<<< END U002120 >>>
<<< UNIT U002121 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:113-113 | ctx=cli.config.placeholders.none >>>
没有可统计的配置表
<<< END U002121 >>>
<<< UNIT U002122 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:114-114 | ctx=cli.config.placeholders.table_title >>>
待填写占位符：共 ${count} 项，${tables} 张表
<<< END U002122 >>>
<<< UNIT U002123 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:115-115 | ctx=cli.config.schema.column_comment >>>
注释
<<< END U002123 >>>
<<< UNIT U002124 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:116-116 | ctx=cli.config.schema.column_key >>>
键
<<< END U002124 >>>
<<< UNIT U002125 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:117-117 | ctx=cli.config.schema.column_type >>>
类型
<<< END U002125 >>>
<<< UNIT U002126 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:118-118 | ctx=cli.config.schema.column_value >>>
当前值
<<< END U002126 >>>
<<< UNIT U002127 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:119-119 | ctx=cli.config.schema.help >>>
列出某表的全部配置项（类型、默认值、注释、是否占位）。
<<< END U002127 >>>
<<< UNIT U002128 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:120-120 | ctx=cli.config.schema.no_items >>>
表 ${table} 没有配置项。
<<< END U002128 >>>
<<< UNIT U002129 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:121-121 | ctx=cli.config.schema.placeholder >>>
[yellow]<待填写>[/yellow]
<<< END U002129 >>>
<<< UNIT U002130 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:122-122 | ctx=cli.config.schema.table_title >>>
${table}（${count} 项）
<<< END U002130 >>>
<<< UNIT U002131 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:123-123 | ctx=cli.config.set.help >>>
写入单个配置项（通过 core 的原子写入路径）。
<<< END U002131 >>>
<<< UNIT U002132 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:124-124 | ctx=cli.db.cell_null >>>
空
<<< END U002132 >>>
<<< UNIT U002133 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:125-125 | ctx=cli.db.delete.confirm >>>
确认删除 ${table} 中主键为 ${pk} 的数据项？
<<< END U002133 >>>
<<< UNIT U002134 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:126-126 | ctx=cli.db.delete.done >>>
已删除 ${table} 的 ${pk}，共 ${count} 行
<<< END U002134 >>>
<<< UNIT U002135 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:127-127 | ctx=cli.db.delete.help >>>
按主键删除一条数据项
<<< END U002135 >>>
<<< UNIT U002136 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:128-128 | ctx=cli.db.entry_failed >>>
data 入口执行失败（退出码 ${code}）：${detail}
<<< END U002136 >>>
<<< UNIT U002137 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:129-129 | ctx=cli.db.entry_not_json >>>
data 入口的输出不是 JSON：${output}
<<< END U002137 >>>
<<< UNIT U002138 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:130-130 | ctx=cli.db.help >>>
浏览实例数据库的表与数据项，并按主键写入
<<< END U002138 >>>
<<< UNIT U002139 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:131-131 | ctx=cli.db.insert.done >>>
已在 ${table} 新建数据项，主键 ${pk}
<<< END U002139 >>>
<<< UNIT U002140 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:132-132 | ctx=cli.db.insert.help >>>
新建一条数据项
<<< END U002140 >>>
<<< UNIT U002141 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:133-133 | ctx=cli.db.insert.option_set >>>
列赋值，形如 <列>=<值>，可重复
<<< END U002141 >>>
<<< UNIT U002142 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:134-134 | ctx=cli.db.option_key >>>
主键值
<<< END U002142 >>>
<<< UNIT U002143 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:135-135 | ctx=cli.db.rows.conditions >>>
筛选：${conditions}
<<< END U002143 >>>
<<< UNIT U002144 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:136-136 | ctx=cli.db.rows.empty >>>
没有数据项
<<< END U002144 >>>
<<< UNIT U002145 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:137-137 | ctx=cli.db.rows.help >>>
按条件与排序分页读取一张表的数据项
<<< END U002145 >>>
<<< UNIT U002146 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:138-138 | ctx=cli.db.rows.option_filter >>>
筛选条件，形如 <列><运算符><值>，可重复（多条之间是 AND）。
<<< END U002146 >>>
<<< UNIT U002147 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:139-139 | ctx=cli.db.rows.option_limit >>>
每页条数，默认 20，上限 200
<<< END U002147 >>>
<<< UNIT U002148 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:140-140 | ctx=cli.db.rows.option_no_count >>>
不统计总条数，翻页时避免一次全表扫描，输出里的总条数显示为未统计。
<<< END U002148 >>>
<<< UNIT U002149 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:141-141 | ctx=cli.db.rows.option_offset >>>
起始偏移，默认 0
<<< END U002149 >>>
<<< UNIT U002150 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:142-142 | ctx=cli.db.rows.option_order_by >>>
排序列，可带 :asc 或 :desc 后缀。默认按主键倒序。
<<< END U002150 >>>
<<< UNIT U002151 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:143-143 | ctx=cli.db.rows.option_search >>>
在所有文本列上做包含匹配（不区分大小写），大表上会全表扫描。
<<< END U002151 >>>
<<< UNIT U002152 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:144-144 | ctx=cli.db.rows.search_term >>>
搜索 ${keyword}
<<< END U002152 >>>
<<< UNIT U002153 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:145-145 | ctx=cli.db.rows.table_title >>>
表 ${table}：共 ${total} 条，第 ${page}/${pages} 页，本页 ${count} 条（偏移 ${offset}）
<<< END U002153 >>>
<<< UNIT U002154 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:146-146 | ctx=cli.db.rows.table_title_uncounted >>>
表 ${table}：总条数未统计，第 ${page} 页，本页 ${count} 条（偏移 ${offset}）
<<< END U002154 >>>
<<< UNIT U002155 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:147-147 | ctx=cli.db.set.done >>>
已更新 ${table} 的 ${pk}：${columns}，影响 ${count} 行
<<< END U002155 >>>
<<< UNIT U002156 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:148-148 | ctx=cli.db.set.help >>>
按主键改写一行的若干列，各列在同一次 UPDATE 里下发
<<< END U002156 >>>
<<< UNIT U002157 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:149-149 | ctx=cli.db.set.option_set >>>
列赋值，形如 <列>=<值>，可重复
<<< END U002157 >>>
<<< UNIT U002158 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:150-150 | ctx=cli.db.table_argument >>>
表标识，取自 db tables 的 table 列
<<< END U002158 >>>
<<< UNIT U002159 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:151-151 | ctx=cli.db.tables.column_columns >>>
列数
<<< END U002159 >>>
<<< UNIT U002160 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:152-152 | ctx=cli.db.tables.column_model >>>
模型
<<< END U002160 >>>
<<< UNIT U002161 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:153-153 | ctx=cli.db.tables.column_package >>>
所属包
<<< END U002161 >>>
<<< UNIT U002162 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:154-154 | ctx=cli.db.tables.column_rows >>>
行数
<<< END U002162 >>>
<<< UNIT U002163 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:155-155 | ctx=cli.db.tables.column_table >>>
表
<<< END U002163 >>>
<<< UNIT U002164 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:156-156 | ctx=cli.db.tables.help >>>
列出实例数据库里已注册的表
<<< END U002164 >>>
<<< UNIT U002165 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:157-157 | ctx=cli.db.tables.table_title >>>
共 ${count} 张表
<<< END U002165 >>>
<<< UNIT U002166 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:158-158 | ctx=cli.db.unknown_package >>>
未声明
<<< END U002166 >>>
<<< UNIT U002167 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:159-159 | ctx=cli.docs.build.done >>>
文档站点构建完成：${count} 个包。
<<< END U002167 >>>
<<< UNIT U002168 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:160-160 | ctx=cli.docs.build.help >>>
生成站点源文件并调用 VitePress 构建
<<< END U002168 >>>
<<< UNIT U002169 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:161-161 | ctx=cli.docs.build.reused >>>
文档输入未变化，已复用上次构建：${count} 个包。使用 --force 可强制重建。
<<< END U002169 >>>
<<< UNIT U002170 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:162-162 | ctx=cli.docs.build.stage_build >>>
正在运行 VitePress 构建…
<<< END U002170 >>>
<<< UNIT U002171 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:163-163 | ctx=cli.docs.build.stage_generate >>>
正在生成站点源文件…
<<< END U002171 >>>
<<< UNIT U002172 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:164-164 | ctx=cli.docs.build.stage_toolchain >>>
正在准备 Node 工具链…
<<< END U002172 >>>
<<< UNIT U002173 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:165-165 | ctx=cli.docs.build.summary >>>
输出目录：${out_dir}，耗时 ${duration} 毫秒。
<<< END U002173 >>>
<<< UNIT U002174 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:166-166 | ctx=cli.docs.clean.confirm >>>
删除 ${path}？下次构建会重新生成全部内容。
<<< END U002174 >>>
<<< UNIT U002175 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:167-167 | ctx=cli.docs.clean.done >>>
已清理 ${path}。
<<< END U002175 >>>
<<< UNIT U002176 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:168-168 | ctx=cli.docs.clean.help >>>
删除实例的文档构建缓存
<<< END U002176 >>>
<<< UNIT U002177 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:169-169 | ctx=cli.docs.dev.help >>>
监听文档与主题改动并实时预览（VitePress dev）
<<< END U002177 >>>
<<< UNIT U002178 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:170-170 | ctx=cli.docs.dev.ready >>>
开发预览已就绪：${url}
<<< END U002178 >>>
<<< UNIT U002179 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:171-171 | ctx=cli.docs.dev.stage_server >>>
正在启动 VitePress dev 服务…
<<< END U002179 >>>
<<< UNIT U002180 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:172-172 | ctx=cli.docs.dev.stopped >>>
开发预览已停止。
<<< END U002180 >>>
<<< UNIT U002181 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:173-173 | ctx=cli.docs.dev.sync >>>
已同步 ${written} 个文件，删除 ${removed} 个（${duration} 毫秒）。
<<< END U002181 >>>
<<< UNIT U002182 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:174-174 | ctx=cli.docs.dev.warn.sync_failed >>>
同步失败：${detail}
<<< END U002182 >>>
<<< UNIT U002183 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:175-175 | ctx=cli.docs.dev.warn.theme_manifest >>>
主题清单 ${path} 已改动。依赖需要重新安装，请先停止开发预览再运行 `akaribot docs install-deps`。
<<< END U002183 >>>
<<< UNIT U002184 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:176-176 | ctx=cli.docs.dev.watching >>>
正在监听文档、主题与配置文件。按 Ctrl+C 停止。
<<< END U002184 >>>
<<< UNIT U002185 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:177-177 | ctx=cli.docs.deploy.confirm >>>
将把站点发布到 ${label}（${detail}），继续？
<<< END U002185 >>>
<<< UNIT U002186 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:178-178 | ctx=cli.docs.deploy.confirm_delete >>>
将把站点发布到 ${label}（${detail}），并删除远端在目标前缀下多余的文件。此操作不可撤销，继续？
<<< END U002186 >>>
<<< UNIT U002187 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:179-179 | ctx=cli.docs.deploy.done >>>
已部署到 ${provider}：${url}
<<< END U002187 >>>
<<< UNIT U002188 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:180-180 | ctx=cli.docs.deploy.dry_run >>>
试运行：计划上传 ${uploaded} 个，删除 ${deleted} 个，跳过 ${skipped} 个文件。
<<< END U002188 >>>
<<< UNIT U002189 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:181-181 | ctx=cli.docs.deploy.help >>>
把构建产物部署到 Vercel 或 S3
<<< END U002189 >>>
<<< UNIT U002190 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:182-182 | ctx=cli.docs.deploy.s3.delete_failed >>>
删除 S3 远端对象失败：${detail}
<<< END U002190 >>>
<<< UNIT U002191 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:183-183 | ctx=cli.docs.deploy.s3.done >>>
S3 部署完成：${url}
<<< END U002191 >>>
<<< UNIT U002192 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:184-184 | ctx=cli.docs.deploy.s3.list_failed >>>
列出 S3 远端对象失败：${detail}
<<< END U002192 >>>
<<< UNIT U002193 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:185-185 | ctx=cli.docs.deploy.s3.missing_bucket >>>
未配置 S3 存储桶，请在 docs.toml 的 [deploy.s3] 填写 bucket。
<<< END U002193 >>>
<<< UNIT U002194 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:186-186 | ctx=cli.docs.deploy.s3.missing_credentials >>>
缺少 S3 登录信息，请设置 AWS_ACCESS_KEY_ID 与 AWS_SECRET_ACCESS_KEY。
<<< END U002194 >>>
<<< UNIT U002195 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:187-187 | ctx=cli.docs.deploy.s3.missing_endpoint >>>
未配置 S3 端点，请在 docs.toml 的 [deploy.s3] 填写 endpoint。
<<< END U002195 >>>
<<< UNIT U002196 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:188-188 | ctx=cli.docs.deploy.s3.target >>>
目标：s3://${bucket}/${prefix}
<<< END U002196 >>>
<<< UNIT U002197 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:189-189 | ctx=cli.docs.deploy.s3.upload_failed >>>
上传到 S3 失败：${detail}
<<< END U002197 >>>
<<< UNIT U002198 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:190-190 | ctx=cli.docs.deploy.site_missing >>>
站点目录不存在：${path}。先运行 `akaribot docs build`。
<<< END U002198 >>>
<<< UNIT U002199 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:191-191 | ctx=cli.docs.deploy.summary >>>
上传 ${uploaded} 个，删除 ${deleted} 个，跳过 ${skipped} 个文件。
<<< END U002199 >>>
<<< UNIT U002200 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:192-192 | ctx=cli.docs.deploy.target >>>
部署目标：${label}（${detail}）
<<< END U002200 >>>
<<< UNIT U002201 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:193-193 | ctx=cli.docs.deploy.unknown_provider >>>
未知的部署方式 ${provider}。支持 vercel 与 s3。
<<< END U002201 >>>
<<< UNIT U002202 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:194-194 | ctx=cli.docs.deploy.vercel.done >>>
Vercel 部署完成：${url}
<<< END U002202 >>>
<<< UNIT U002203 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:195-195 | ctx=cli.docs.deploy.vercel.failed >>>
Vercel 部署失败：${detail}
<<< END U002203 >>>
<<< UNIT U002204 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:196-196 | ctx=cli.docs.deploy.vercel.missing_project >>>
未配置 Vercel 项目，请在 docs.toml 的 [deploy.vercel] 填写 project 或 project_id。
<<< END U002204 >>>
<<< UNIT U002205 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:197-197 | ctx=cli.docs.deploy.vercel.missing_token >>>
缺少环境变量 VERCEL_TOKEN。
<<< END U002205 >>>
<<< UNIT U002206 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:198-198 | ctx=cli.docs.error.bad_config >>>
无法读取文档配置 ${path}：${reason}
<<< END U002206 >>>
<<< UNIT U002207 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:199-199 | ctx=cli.docs.error.build_failed >>>
文档构建失败：${reason}（输出目录 ${path}）
<<< END U002207 >>>
<<< UNIT U002208 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:200-200 | ctx=cli.docs.error.dev_failed >>>
开发预览启动失败：${reason}（${path}）
<<< END U002208 >>>
<<< UNIT U002209 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:201-201 | ctx=cli.docs.error.dev_locked >>>
实例上已有开发预览在运行（进程 ${pid}，端口 ${port}）。先停止它。
<<< END U002209 >>>
<<< UNIT U002210 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:202-202 | ctx=cli.docs.error.git_missing >>>
未找到 git，无法同步主题模板。
<<< END U002210 >>>
<<< UNIT U002211 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:203-203 | ctx=cli.docs.error.install_failed >>>
安装文档构建依赖失败：${reason}（${path}）
<<< END U002211 >>>
<<< UNIT U002212 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:204-204 | ctx=cli.docs.error.missing_page >>>
无法读取文档页面 ${path}：${reason}
<<< END U002212 >>>
<<< UNIT U002213 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:205-205 | ctx=cli.docs.error.not_built >>>
站点尚未构建：${path}。先运行 `akaribot docs build`，或去掉 --no-build。
<<< END U002213 >>>
<<< UNIT U002214 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:206-206 | ctx=cli.docs.error.serve_failed >>>
无法启动预览服务：${detail}
<<< END U002214 >>>
<<< UNIT U002215 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:207-207 | ctx=cli.docs.error.site_asset_missing >>>
文档站点资源不存在：${path}
<<< END U002215 >>>
<<< UNIT U002216 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:208-208 | ctx=cli.docs.error.theme_invalid >>>
文档主题清单无效：${path}（${reason}）
<<< END U002216 >>>
<<< UNIT U002217 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:209-209 | ctx=cli.docs.error.theme_missing >>>
找不到文档主题：${source}（${path}）
<<< END U002217 >>>
<<< UNIT U002218 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:210-210 | ctx=cli.docs.error.theme_repo_missing >>>
找不到主题模板 submodule 所在仓库：${path}。请在源码仓库中运行，或用 --repo 指定。
<<< END U002218 >>>
<<< UNIT U002219 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:211-211 | ctx=cli.docs.error.theme_sync_failed >>>
主题模板同步失败：${reason}（${path}）
<<< END U002219 >>>
<<< UNIT U002220 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:212-212 | ctx=cli.docs.error.theme_unsupported >>>
不支持的主题来源：${source}。请使用 bundled、file:<目录> 或实例内的主题目录。
<<< END U002220 >>>
<<< UNIT U002221 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:213-213 | ctx=cli.docs.error.toolchain_missing >>>
Node.js 工具链不可用：${detail}。请安装主题要求的 Node.js 版本并确保 npm 在 PATH 中。
<<< END U002221 >>>
<<< UNIT U002222 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:214-214 | ctx=cli.docs.error.unknown_key >>>
文档目录中没有包 ${name}。可用 key：${keys}
<<< END U002222 >>>
<<< UNIT U002223 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:215-215 | ctx=cli.docs.error.unsafe_path >>>
文档生成目标越出缓存目录：${path}
<<< END U002223 >>>
<<< UNIT U002224 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:216-216 | ctx=cli.docs.help >>>
文档站点工具，用于列出、构建、开发预览、预览、部署与清理已安装包的文档
<<< END U002224 >>>
<<< UNIT U002225 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:217-217 | ctx=cli.docs.install_deps.done >>>
Node 依赖已就绪：VitePress ${version}。
<<< END U002225 >>>
<<< UNIT U002226 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:218-218 | ctx=cli.docs.install_deps.help >>>
安装主题所需的 Node 依赖
<<< END U002226 >>>
<<< UNIT U002227 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:219-219 | ctx=cli.docs.install_deps.summary >>>
依赖目录：${path}
<<< END U002227 >>>
<<< UNIT U002228 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:220-220 | ctx=cli.docs.list.column_category >>>
分类
<<< END U002228 >>>
<<< UNIT U002229 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:221-221 | ctx=cli.docs.list.column_group >>>
分组
<<< END U002229 >>>
<<< UNIT U002230 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:222-222 | ctx=cli.docs.list.column_key >>>
包
<<< END U002230 >>>
<<< UNIT U002231 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:223-223 | ctx=cli.docs.list.column_pages >>>
页面
<<< END U002231 >>>
<<< UNIT U002232 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:224-224 | ctx=cli.docs.list.column_title >>>
标题
<<< END U002232 >>>
<<< UNIT U002233 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:225-225 | ctx=cli.docs.list.column_version >>>
版本
<<< END U002233 >>>
<<< UNIT U002234 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:226-226 | ctx=cli.docs.list.empty >>>
没有发现可用的文档包。
<<< END U002234 >>>
<<< UNIT U002235 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:227-227 | ctx=cli.docs.list.header >>>
文档包（${count}）
<<< END U002235 >>>
<<< UNIT U002236 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:228-228 | ctx=cli.docs.list.help >>>
列出参与文档构建的包、页面与目录警告
<<< END U002236 >>>
<<< UNIT U002237 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:229-229 | ctx=cli.docs.list.summary >>>
共 ${count} 个包，${pages} 个页面。
<<< END U002237 >>>
<<< UNIT U002238 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:230-230 | ctx=cli.docs.option_all >>>
构建全部包（默认行为）
<<< END U002238 >>>
<<< UNIT U002239 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:231-231 | ctx=cli.docs.option_delete >>>
删除远端在目标前缀下多余的文件
<<< END U002239 >>>
<<< UNIT U002240 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:232-232 | ctx=cli.docs.option_dry_run >>>
只统计将上传与删除的文件，不写入远端
<<< END U002240 >>>
<<< UNIT U002241 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:233-233 | ctx=cli.docs.option_force >>>
忽略构建校验信息，强制重建
<<< END U002241 >>>
<<< UNIT U002242 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:234-234 | ctx=cli.docs.option_host >>>
预览服务绑定地址
<<< END U002242 >>>
<<< UNIT U002243 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:235-235 | ctx=cli.docs.option_interval >>>
文件改动静默多久后开始同步（秒）
<<< END U002243 >>>
<<< UNIT U002244 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:236-236 | ctx=cli.docs.option_json >>>
以 JSON 输出，供脚本消费
<<< END U002244 >>>
<<< UNIT U002245 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:237-237 | ctx=cli.docs.option_kind >>>
按分组过滤，如 module、adapter、cli
<<< END U002245 >>>
<<< UNIT U002246 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:238-238 | ctx=cli.docs.option_no_build >>>
跳过构建，直接使用现有输出
<<< END U002246 >>>
<<< UNIT U002247 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:239-239 | ctx=cli.docs.option_offline >>>
不联网安装 Node 依赖
<<< END U002247 >>>
<<< UNIT U002248 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:240-240 | ctx=cli.docs.option_open >>>
启动后打开浏览器
<<< END U002248 >>>
<<< UNIT U002249 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:241-241 | ctx=cli.docs.option_package >>>
只构建指定包，可重复或逗号分隔
<<< END U002249 >>>
<<< UNIT U002250 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:242-242 | ctx=cli.docs.option_port >>>
预览服务端口
<<< END U002250 >>>
<<< UNIT U002251 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:243-243 | ctx=cli.docs.option_provider >>>
部署方式：vercel 或 s3
<<< END U002251 >>>
<<< UNIT U002252 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:244-244 | ctx=cli.docs.option_query >>>
按 key、标题或简介过滤
<<< END U002252 >>>
<<< UNIT U002253 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:245-245 | ctx=cli.docs.option_repo >>>
主题 submodule 所在的仓库路径
<<< END U002253 >>>
<<< UNIT U002254 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:246-246 | ctx=cli.docs.serve.help >>>
构建并启动本机预览服务
<<< END U002254 >>>
<<< UNIT U002255 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:247-247 | ctx=cli.docs.serve.ready >>>
预览服务已启动：${url}
<<< END U002255 >>>
<<< UNIT U002256 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:248-248 | ctx=cli.docs.serve.stopped >>>
预览服务已停止。
<<< END U002256 >>>
<<< UNIT U002257 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:249-249 | ctx=cli.docs.serve.summary >>>
按 Ctrl+C 停止预览。
<<< END U002257 >>>
<<< UNIT U002258 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:250-250 | ctx=cli.docs.status.base >>>
基础路径：${base}
<<< END U002258 >>>
<<< UNIT U002259 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:251-251 | ctx=cli.docs.status.build >>>
最近构建：${detail}
<<< END U002259 >>>
<<< UNIT U002260 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:252-252 | ctx=cli.docs.status.build_detail >>>
${at}（${count} 个包，校验值 ${fingerprint}）
<<< END U002260 >>>
<<< UNIT U002261 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:253-253 | ctx=cli.docs.status.config >>>
配置：${path}
<<< END U002261 >>>
<<< UNIT U002262 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:254-254 | ctx=cli.docs.status.deploy >>>
最近部署：${detail}
<<< END U002262 >>>
<<< UNIT U002263 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:256-256 | ctx=cli.docs.status.dev >>>
开发预览：${detail}
<<< END U002263 >>>
<<< UNIT U002264 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:257-257 | ctx=cli.docs.status.dev_idle >>>
未运行
<<< END U002264 >>>
<<< UNIT U002265 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:258-258 | ctx=cli.docs.status.dev_running >>>
运行中（进程 ${pid}，${url}）
<<< END U002265 >>>
<<< UNIT U002266 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:259-259 | ctx=cli.docs.status.help >>>
显示文档工具链、配置与最近的构建和部署
<<< END U002266 >>>
<<< UNIT U002267 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:260-260 | ctx=cli.docs.status.instance >>>
实例：${path}
<<< END U002267 >>>
<<< UNIT U002268 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:261-261 | ctx=cli.docs.status.none >>>
（无）
<<< END U002268 >>>
<<< UNIT U002269 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:262-262 | ctx=cli.docs.status.out_dir >>>
输出目录：${path}
<<< END U002269 >>>
<<< UNIT U002270 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:263-263 | ctx=cli.docs.status.packages >>>
文档包：${count} 个
<<< END U002270 >>>
<<< UNIT U002271 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:264-264 | ctx=cli.docs.status.site >>>
站点：${title}（${lang}）
<<< END U002271 >>>
<<< UNIT U002272 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:265-265 | ctx=cli.docs.status.theme >>>
主题：${source}
<<< END U002272 >>>
<<< UNIT U002273 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:266-266 | ctx=cli.docs.status.theme_resolved >>>
实际主题：${name} ${version}（${path}，摘要 ${digest}）
<<< END U002273 >>>
<<< UNIT U002274 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:267-267 | ctx=cli.docs.status.title >>>
文档站点状态
<<< END U002274 >>>
<<< UNIT U002275 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:268-268 | ctx=cli.docs.status.toolchain >>>
工具链：${detail}
<<< END U002275 >>>
<<< UNIT U002276 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:269-269 | ctx=cli.docs.sync_theme.after >>>
同步后：${commit}
<<< END U002276 >>>
<<< UNIT U002277 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:270-270 | ctx=cli.docs.sync_theme.before >>>
同步前：${commit}
<<< END U002277 >>>
<<< UNIT U002278 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:271-271 | ctx=cli.docs.sync_theme.current >>>
主题模板已是最新。
<<< END U002278 >>>
<<< UNIT U002279 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:272-272 | ctx=cli.docs.sync_theme.help >>>
同步主题模板 submodule 到远端最新提交
<<< END U002279 >>>
<<< UNIT U002280 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:273-273 | ctx=cli.docs.sync_theme.repo >>>
主题仓库：${path}
<<< END U002280 >>>
<<< UNIT U002281 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:274-274 | ctx=cli.docs.sync_theme.uninitialized >>>
未初始化
<<< END U002281 >>>
<<< UNIT U002282 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:275-275 | ctx=cli.docs.sync_theme.updated >>>
主题模板已更新。父仓库 gitlink 未暂存。
<<< END U002282 >>>
<<< UNIT U002283 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:276-276 | ctx=cli.doctor.conflict.config >>>
配置文件无法解析：${error}
<<< END U002283 >>>
<<< UNIT U002284 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:277-277 | ctx=cli.doctor.conflict.credential >>>
登录信息重复：${labels}的 ${field} 取值相同（已隐藏，长度 ${length}）${note}。两个进程会争抢同一账号的消息。
<<< END U002284 >>>
<<< UNIT U002285 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:278-278 | ctx=cli.doctor.conflict.not_all_enabled >>>
（相关实例未全部启用，启用后即会冲突）
<<< END U002285 >>>
<<< UNIT U002286 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:279-279 | ctx=cli.doctor.conflict.orphan >>>
孤立配置：${path} 定义了 ${table}，但平台 ${platform} 的适配器包未安装。守护进程会跳过该实例。
<<< END U002286 >>>
<<< UNIT U002287 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:280-280 | ctx=cli.doctor.conflict.port >>>
端口冲突：${address} 与 ${other_address} 同时被 ${first} 与 ${second} 声明${note}
<<< END U002287 >>>
<<< UNIT U002288 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:281-281 | ctx=cli.doctor.help >>>
自检多实例的端口冲突、登录信息重复与孤立配置
<<< END U002288 >>>
<<< UNIT U002289 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:282-282 | ctx=cli.doctor.option_json >>>
以 JSON 输出，供 CI 与脚本使用。
<<< END U002289 >>>
<<< UNIT U002290 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:283-283 | ctx=cli.doctor.option_strict >>>
告警也按失败处理。
<<< END U002290 >>>
<<< UNIT U002291 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:284-284 | ctx=cli.doctor.report.checks_degraded >>>
[yellow]孤立配置检查跳过。登录信息检查退化为全部密钥字段。[/yellow]
<<< END U002291 >>>
<<< UNIT U002292 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:285-285 | ctx=cli.doctor.report.config_root >>>
配置根：${path}
<<< END U002292 >>>
<<< UNIT U002293 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:286-286 | ctx=cli.doctor.report.implementation >>>
冲突检查实现：${implementation}
<<< END U002293 >>>
<<< UNIT U002294 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:287-287 | ctx=cli.doctor.report.instance_root >>>
实例根目录：${path}
<<< END U002294 >>>
<<< UNIT U002295 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:288-288 | ctx=cli.doctor.report.instances >>>
实例 ${count} 个。已安装适配器：${adapters}
<<< END U002295 >>>
<<< UNIT U002296 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:289-289 | ctx=cli.doctor.report.none >>>
（无）
<<< END U002296 >>>
<<< UNIT U002297 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:290-290 | ctx=cli.doctor.report.note >>>
注：core 提供 config conflicts 入口后，本命令与 daemon 前置检查将自动共用同一套判定规则。
<<< END U002297 >>>
<<< UNIT U002298 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:291-291 | ctx=cli.doctor.report.registry_unavailable >>>
[yellow]已安装包清单不可用：${note}[/yellow]
<<< END U002298 >>>
<<< UNIT U002299 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:292-292 | ctx=cli.doctor.report.summary >>>
共 ${total} 项：error ${errors}，warning ${warnings}
<<< END U002299 >>>
<<< UNIT U002300 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:293-293 | ctx=cli.doctor.report.unconfigured >>>
已安装但尚无配置的适配器：${adapters}
<<< END U002300 >>>
<<< UNIT U002301 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:294-294 | ctx=cli.error.not_instance >>>
当前目录不是 AkariBot 实例（未找到 akaribot.toml）。先运行 `akaribot init` 创建实例，或用 `--instance <实例根目录>` / 环境变量 AKARI_INSTANCE_DIR 指定实例。
<<< END U002301 >>>
<<< UNIT U002302 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:295-295 | ctx=cli.error.not_instance_hint >>>
先运行 `akaribot init` 创建实例，或用 `--instance <实例根目录>` / 环境变量 AKARI_INSTANCE_DIR 指定实例。
<<< END U002302 >>>
<<< UNIT U002303 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:296-296 | ctx=cli.init.already_instance >>>
${root} 已是 AkariBot 实例（存在 ${meta}）。修改配置请用 `akaribot config`，确认覆盖请加 --force。
<<< END U002303 >>>
<<< UNIT U002304 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:297-297 | ctx=cli.init.arg_path >>>
实例目录，默认为当前目录
<<< END U002304 >>>
<<< UNIT U002305 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:298-298 | ctx=cli.init.ask.adapters >>>
要安装的适配器（逗号分隔，留空只安装 core，可用 `akaribot module available --kind adapter` 查看全部）
<<< END U002305 >>>
<<< UNIT U002306 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:299-299 | ctx=cli.init.ask.locale >>>
实例默认语言（zh_cn / en_us / ja_jp / ko_kr / zh_tw）
<<< END U002306 >>>
<<< UNIT U002307 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:300-300 | ctx=cli.init.ask.managed_venv >>>
由 CLI 托管实例 venv（${venv}，推荐）
<<< END U002307 >>>
<<< UNIT U002308 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:301-301 | ctx=cli.init.ask.workspace >>>
从本地工作区源码安装（PyPI 上尚未发布时必选）
<<< END U002308 >>>
<<< UNIT U002309 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:302-302 | ctx=cli.init.ask.workspace_root >>>
工作区根目录
<<< END U002309 >>>
<<< UNIT U002310 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:303-303 | ctx=cli.init.config_sync_failed >>>
配置未补齐时机器人仍可启动（首次运行会扫描模板），也可稍后重试 config sync。
<<< END U002310 >>>
<<< UNIT U002311 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:304-304 | ctx=cli.init.config_sync_skipped >>>
已跳过 config sync，配置项需在 core 端入口就绪后运行 `akaribot config sync --package <dist>` 补齐。
<<< END U002311 >>>
<<< UNIT U002312 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:305-305 | ctx=cli.init.config_version_unknown >>>
未能从 core 读取 config_version，暂写入默认值 1。首次启动会由核心配置迁移修正。
<<< END U002312 >>>
<<< UNIT U002313 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:306-306 | ctx=cli.init.db_upgrade_failed >>>
${error}。机器人启动时会自动迁移。
<<< END U002313 >>>
<<< UNIT U002314 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:307-307 | ctx=cli.init.default_adapter >>>
未指定 --adapter，按默认安装 telegram 适配器。
<<< END U002314 >>>
<<< UNIT U002315 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:308-308 | ctx=cli.init.dirs_created >>>
新建 ${count} 个目录：${names}
<<< END U002315 >>>
<<< UNIT U002316 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:309-309 | ctx=cli.init.dry_run.dirs >>>
[dim]dry-run：跳过目录创建[/dim]
<<< END U002316 >>>
<<< UNIT U002317 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:310-310 | ctx=cli.init.dry_run.meta >>>
[dim]dry-run：跳过元数据写入[/dim]
<<< END U002317 >>>
<<< UNIT U002318 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:311-311 | ctx=cli.init.dry_run.rest >>>
[dim]dry-run：跳过配置生成、数据库迁移与验证[/dim]
<<< END U002318 >>>
<<< UNIT U002319 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:312-312 | ctx=cli.init.help >>>
初始化实例，依次创建目录、写入 akaribot.toml、安装 core 与适配器并生成最小配置
<<< END U002319 >>>
<<< UNIT U002320 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:313-313 | ctx=cli.init.import_failed >>>
实例解释器无法导入 core：${detail}
<<< END U002320 >>>
<<< UNIT U002321 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:314-314 | ctx=cli.init.import_ok >>>
core 在实例环境中可导入（config_version=${version}）
<<< END U002321 >>>
<<< UNIT U002322 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:315-315 | ctx=cli.init.meta_written >>>
已写入 ${path}
<<< END U002322 >>>
<<< UNIT U002323 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:316-316 | ctx=cli.init.minimal_conflict >>>
--minimal 与 --extra 互斥，前者不安装任何 extras。
<<< END U002323 >>>
<<< UNIT U002324 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:317-317 | ctx=cli.init.next_config_edit >>>
  akaribot config edit          # 填写 <Replace me> 占位符
<<< END U002324 >>>
<<< UNIT U002325 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:318-318 | ctx=cli.init.next_run >>>
  akaribot run                  # 启动机器人
<<< END U002325 >>>
<<< UNIT U002326 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:319-319 | ctx=cli.init.next_steps >>>

下一步：
<<< END U002326 >>>
<<< UNIT U002327 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:320-320 | ctx=cli.init.no_stderr >>>
无错误输出
<<< END U002327 >>>
<<< UNIT U002328 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:321-321 | ctx=cli.init.none >>>
无
<<< END U002328 >>>
<<< UNIT U002329 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:322-322 | ctx=cli.init.not_empty >>>
${root} 非空。换一个空目录，或确认可写入后加 --force。
<<< END U002329 >>>
<<< UNIT U002330 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:323-323 | ctx=cli.init.not_empty_confirm >>>
${root} 非空，继续会在其中创建实例文件。继续
<<< END U002330 >>>
<<< UNIT U002331 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:324-324 | ctx=cli.init.not_workspace >>>
${root} 下没有 packages 目录，不像是 monorepo 工作区根目录。
<<< END U002331 >>>
<<< UNIT U002332 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:325-325 | ctx=cli.init.option_adapter >>>
要安装的适配器，可重复
<<< END U002332 >>>
<<< UNIT U002333 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:326-326 | ctx=cli.init.option_dry_run >>>
只打印将执行的命令，不写入任何文件
<<< END U002333 >>>
<<< UNIT U002334 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:327-327 | ctx=cli.init.option_extra >>>
在默认的 core[full] 之外追加 extras，可重复
<<< END U002334 >>>
<<< UNIT U002335 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:328-328 | ctx=cli.init.option_force >>>
目标目录已存在实例或非空时继续
<<< END U002335 >>>
<<< UNIT U002336 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:329-329 | ctx=cli.init.option_locale >>>
实例默认语言，如 zh_cn / en_us
<<< END U002336 >>>
<<< UNIT U002337 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:330-330 | ctx=cli.init.option_minimal >>>
不安装任何 extras，跳过 akari-bot-assets-emotes 表情资源包
<<< END U002337 >>>
<<< UNIT U002338 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:331-331 | ctx=cli.init.option_module >>>
要额外安装的初始模块，可重复
<<< END U002338 >>>
<<< UNIT U002339 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:332-332 | ctx=cli.init.option_no_venv >>>
不托管 venv，直接安装到当前环境
<<< END U002339 >>>
<<< UNIT U002340 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:333-333 | ctx=cli.init.option_non_interactive >>>
不提问，全部取默认值或选项值
<<< END U002340 >>>
<<< UNIT U002341 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:334-334 | ctx=cli.init.option_offline >>>
registry 只用本地缓存，不联网
<<< END U002341 >>>
<<< UNIT U002342 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:335-335 | ctx=cli.init.option_python >>>
创建 venv 用的解释器，默认与当前解释器一致
<<< END U002342 >>>
<<< UNIT U002343 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:336-336 | ctx=cli.init.option_skip_config_sync >>>
跳过 config sync（core 入口未就绪时使用）
<<< END U002343 >>>
<<< UNIT U002344 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:337-337 | ctx=cli.init.option_verbose >>>
回显 uv 的全部输出
<<< END U002344 >>>
<<< UNIT U002345 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:338-338 | ctx=cli.init.option_workspace_root >>>
使用工作区本地源码安装（本地路径模式）
<<< END U002345 >>>
<<< UNIT U002346 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:339-339 | ctx=cli.init.plan.install >>>
安装
<<< END U002346 >>>
<<< UNIT U002347 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:341-341 | ctx=cli.init.plan.locale >>>
语言
<<< END U002347 >>>
<<< UNIT U002348 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:342-342 | ctx=cli.init.plan.root >>>
实例根目录
<<< END U002348 >>>
<<< UNIT U002349 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:343-343 | ctx=cli.init.plan.title >>>
将创建实例
<<< END U002349 >>>
<<< UNIT U002350 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:344-344 | ctx=cli.init.plan.venv_managed >>>
托管 ${venv}
<<< END U002350 >>>
<<< UNIT U002351 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:345-345 | ctx=cli.init.plan.venv_unmanaged >>>
不托管（使用当前环境）
<<< END U002351 >>>
<<< UNIT U002352 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:346-346 | ctx=cli.init.plan.workspace >>>
工作区
<<< END U002352 >>>
<<< UNIT U002353 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:347-347 | ctx=cli.init.plan.workspace_none >>>
不使用（从 registry/PyPI 获取）
<<< END U002353 >>>
<<< UNIT U002354 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:348-348 | ctx=cli.init.registry_failed >>>
写入本机实例列表失败（不影响使用）：${error}
<<< END U002354 >>>
<<< UNIT U002355 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:349-349 | ctx=cli.init.registry_ok >>>
已写入本机实例列表：${name}
<<< END U002355 >>>
<<< UNIT U002356 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:350-350 | ctx=cli.init.skeleton_exists >>>
  已存在配置文件，保留不动：${path}
<<< END U002356 >>>
<<< UNIT U002357 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:351-351 | ctx=cli.init.skeleton_written >>>
已写出配置文件 ${path}
<<< END U002357 >>>
<<< UNIT U002358 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:352-352 | ctx=cli.init.step.config >>>
生成配置
<<< END U002358 >>>
<<< UNIT U002359 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:353-353 | ctx=cli.init.step.current_env >>>
在当前环境安装包
<<< END U002359 >>>
<<< UNIT U002360 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:354-354 | ctx=cli.init.step.dirs >>>
创建目录结构
<<< END U002360 >>>
<<< UNIT U002361 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:355-355 | ctx=cli.init.step.meta >>>
写入 akaribot.toml
<<< END U002361 >>>
<<< UNIT U002362 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:356-356 | ctx=cli.init.step.venv >>>
创建实例 venv 并安装包
<<< END U002362 >>>
<<< UNIT U002363 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:357-357 | ctx=cli.init.step.verify >>>
验证安装
<<< END U002363 >>>
<<< UNIT U002364 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:358-358 | ctx=cli.init.target_python >>>
  目标解释器：${python}
<<< END U002364 >>>
<<< UNIT U002365 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:359-359 | ctx=cli.init.unmanaged_warning >>>
非托管模式会改动当前 Python 环境，请确认该环境就是实例的运行环境。
<<< END U002365 >>>
<<< UNIT U002366 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:360-360 | ctx=cli.init.venv_failed >>>
${error}。若本机没有 uv，可安装后重试，或用 --no-venv 直接安装到当前环境。
<<< END U002366 >>>
<<< UNIT U002367 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:361-361 | ctx=cli.init.what_install >>>
安装 core 与适配器
<<< END U002367 >>>
<<< UNIT U002368 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:362-362 | ctx=cli.instance.core_json_unparsable >>>
core 未回传可解析的 JSON：${text}
<<< END U002368 >>>
<<< UNIT U002369 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:363-363 | ctx=cli.instance.empty_output >>>
<空输出>
<<< END U002369 >>>
<<< UNIT U002370 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:364-364 | ctx=cli.instance.exec_failed >>>
无法执行 ${argv0}：${error}
<<< END U002370 >>>
<<< UNIT U002371 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:365-365 | ctx=cli.instance.failure_core_entrypoint >>>
${prefix}：core 里还没有 akaribot.core.entrypoints 入口（core 的 T5.1 尚未完成）。
<<< END U002371 >>>
<<< UNIT U002372 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:366-366 | ctx=cli.instance.failure_core_missing >>>
${prefix}：实例内未安装 core。先运行 `akaribot module add akari-bot-core` 或重建实例。
<<< END U002372 >>>
<<< UNIT U002373 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:367-367 | ctx=cli.instance.failure_exit_code >>>
${prefix}（退出码 ${code}）：${tail}
<<< END U002373 >>>
<<< UNIT U002374 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:368-368 | ctx=cli.instance.failure_testing_missing >>>
${prefix}：实例内未安装 akari-bot-testing。先运行 `akaribot module add akari-bot-testing`。
<<< END U002374 >>>
<<< UNIT U002375 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:369-369 | ctx=cli.instance.meta_missing >>>
${path} 不存在。${hint}
<<< END U002375 >>>
<<< UNIT U002376 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:370-370 | ctx=cli.instance.meta_parse_failed >>>
${path} 无法解析：${error}
<<< END U002376 >>>
<<< UNIT U002377 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:371-371 | ctx=cli.instance.no_error_output >>>
无错误输出
<<< END U002377 >>>
<<< UNIT U002378 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:372-372 | ctx=cli.instance.no_system_python >>>
找不到可用的系统 Python。请设置 ${env} 指向实例要使用的解释器。
<<< END U002378 >>>
<<< UNIT U002379 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:373-373 | ctx=cli.instance.not_instance_env >>>
环境变量 ${env}=${path} 指向的目录里没有 ${meta}，请改正该变量或运行 `akaribot init`。
<<< END U002379 >>>
<<< UNIT U002380 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:374-374 | ctx=cli.instance.not_instance_root >>>
${path} 不是 AkariBot 实例（未找到 ${meta}）。${hint}
<<< END U002380 >>>
<<< UNIT U002381 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:375-375 | ctx=cli.instance.notify_delivered >>>
运行中的实例已确认执行 ${remote}
<<< END U002381 >>>
<<< UNIT U002382 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:376-376 | ctx=cli.instance.notify_failed >>>
热装载通知失败（${remote}）
<<< END U002382 >>>
<<< UNIT U002383 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:377-377 | ctx=cli.instance.notify_not_delivered >>>
热装载通知未送达：${error}
<<< END U002383 >>>
<<< UNIT U002384 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:378-378 | ctx=cli.instance.notify_not_running >>>
实例未运行，跳过热装载通知（下次启动自动装载）
<<< END U002384 >>>
<<< UNIT U002385 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:379-379 | ctx=cli.instance.notify_rejected >>>
实例拒绝执行 ${remote}：${detail}
<<< END U002385 >>>
<<< UNIT U002386 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:380-380 | ctx=cli.instance.notify_server_absent >>>
实例进程在运行，但 JobQueue 注册表里没有在线的 Server：${detail}。请确认实例已正常启动。
<<< END U002386 >>>
<<< UNIT U002387 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:381-381 | ctx=cli.instance.notify_timeout >>>
${remote} 已投递，但实例未在时限内确认：${detail}。结果未知，请先确认实例状态，不要直接重试。
<<< END U002387 >>>
<<< UNIT U002388 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:382-382 | ctx=cli.instance.notify_unknown_action >>>
未知的包变更动作：${action}
<<< END U002388 >>>
<<< UNIT U002389 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:383-383 | ctx=cli.instance.python_env_missing >>>
${env} 指向的解释器不存在：${path}
<<< END U002389 >>>
<<< UNIT U002390 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:384-384 | ctx=cli.instance.python_missing >>>
实例解释器不存在：${python}。托管 venv 损坏时运行 `akaribot venv recreate`。
<<< END U002390 >>>
<<< UNIT U002391 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:385-385 | ctx=cli.instance.timeout >>>
命令超时（${seconds}s）：${command}
<<< END U002391 >>>
<<< UNIT U002392 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:386-386 | ctx=cli.instance.unmanaged_python >>>
（未托管）${python}
<<< END U002392 >>>
<<< UNIT U002393 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:387-387 | ctx=cli.instance.what_read_packages >>>
读取已安装包清单失败
<<< END U002393 >>>
<<< UNIT U002394 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:388-388 | ctx=cli.instance_cmd.add.arg_path >>>
实例目录，须含 akaribot.toml
<<< END U002394 >>>
<<< UNIT U002395 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:389-389 | ctx=cli.instance_cmd.add.done >>>
已添加实例 ${name}（${root}）
<<< END U002395 >>>
<<< UNIT U002396 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:390-390 | ctx=cli.instance_cmd.add.help >>>
添加一个已存在的实例目录。只记录位置，不改动实例本身
<<< END U002396 >>>
<<< UNIT U002397 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:391-391 | ctx=cli.instance_cmd.add.option_locale >>>
实例默认语言，仅作记录
<<< END U002397 >>>
<<< UNIT U002398 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:392-392 | ctx=cli.instance_cmd.add.option_name >>>
注册名。默认按目录名生成一个不冲突的名字
<<< END U002398 >>>
<<< UNIT U002399 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:393-393 | ctx=cli.instance_cmd.arg_name >>>
注册名，见 `akaribot instance list`
<<< END U002399 >>>
<<< UNIT U002400 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:394-394 | ctx=cli.instance_cmd.column_autostart >>>
开机自启
<<< END U002400 >>>
<<< UNIT U002401 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:395-395 | ctx=cli.instance_cmd.column_crash >>>
崩溃重启
<<< END U002401 >>>
<<< UNIT U002402 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:396-396 | ctx=cli.instance_cmd.column_name >>>
实例
<<< END U002402 >>>
<<< UNIT U002403 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:397-397 | ctx=cli.instance_cmd.column_root >>>
位置
<<< END U002403 >>>
<<< UNIT U002404 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:398-398 | ctx=cli.instance_cmd.column_state >>>
状态
<<< END U002404 >>>
<<< UNIT U002405 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:399-399 | ctx=cli.instance_cmd.default_mark >>>
（默认）
<<< END U002405 >>>
<<< UNIT U002406 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:400-400 | ctx=cli.instance_cmd.help >>>
管理本机已添加的实例，支持列出、添加、移除、设为默认与配置服务策略
<<< END U002406 >>>
<<< UNIT U002407 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:401-401 | ctx=cli.instance_cmd.list.empty >>>
还没有添加任何实例，可在有实例的目录里运行 `akaribot init`，或用 `akaribot instance add <目录>` 添加已有实例。
<<< END U002407 >>>
<<< UNIT U002408 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:402-402 | ctx=cli.instance_cmd.list.help >>>
列出本机已添加的实例及其运行状态与服务策略
<<< END U002408 >>>
<<< UNIT U002409 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:403-403 | ctx=cli.instance_cmd.list.hint >>>
在实例目录里执行命令即可操作该实例。在实例目录之外执行命令时，先用 `akaribot instance use <名>` 设置默认实例。
<<< END U002409 >>>
<<< UNIT U002410 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:404-404 | ctx=cli.instance_cmd.list.table_title >>>
本机实例（共 ${count} 个）
<<< END U002410 >>>
<<< UNIT U002411 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:405-405 | ctx=cli.instance_cmd.no >>>
否
<<< END U002411 >>>
<<< UNIT U002412 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:406-406 | ctx=cli.instance_cmd.policy.done >>>
已更新 ${name} 的服务策略：开机自启 ${autostart}、崩溃重启 ${crash}
<<< END U002412 >>>
<<< UNIT U002413 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:407-407 | ctx=cli.instance_cmd.policy.help >>>
设置实例的服务策略，控制随服务启动而自动启动及崩溃后自动重启
<<< END U002413 >>>
<<< UNIT U002414 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:408-408 | ctx=cli.instance_cmd.policy.nothing >>>
至少要给出 --autostart/--no-autostart 或 --restart-on-crash/--no-restart-on-crash 之一
<<< END U002414 >>>
<<< UNIT U002415 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:409-409 | ctx=cli.instance_cmd.policy.option_autostart >>>
服务启动时是否自动启动该实例（按上次的期望状态恢复）
<<< END U002415 >>>
<<< UNIT U002416 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:410-410 | ctx=cli.instance_cmd.policy.option_crash >>>
实例非正常退出后是否由服务自动重启
<<< END U002416 >>>
<<< UNIT U002417 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:411-411 | ctx=cli.instance_cmd.remove.confirm >>>
确认从列表移除实例 ${name}（实例目录本身保留）？
<<< END U002417 >>>
<<< UNIT U002418 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:412-412 | ctx=cli.instance_cmd.remove.done >>>
已从列表移除 ${name}，实例目录未改动
<<< END U002418 >>>
<<< UNIT U002419 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:413-413 | ctx=cli.instance_cmd.remove.help >>>
删除一条记录。实例目录本身保留
<<< END U002419 >>>
<<< UNIT U002420 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:414-414 | ctx=cli.instance_cmd.state_missing >>>
目录已丢失
<<< END U002420 >>>
<<< UNIT U002421 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:415-415 | ctx=cli.instance_cmd.state_running >>>
运行中
<<< END U002421 >>>
<<< UNIT U002422 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:416-416 | ctx=cli.instance_cmd.state_stopped >>>
未运行
<<< END U002422 >>>
<<< UNIT U002423 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:417-417 | ctx=cli.instance_cmd.unknown >>>
注册表里没有实例 ${name}
<<< END U002423 >>>
<<< UNIT U002424 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:418-418 | ctx=cli.instance_cmd.use.done >>>
默认实例已设为 ${name}
<<< END U002424 >>>
<<< UNIT U002425 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:419-419 | ctx=cli.instance_cmd.use.help >>>
把某个实例设为默认，在实例目录之外执行命令时使用该实例
<<< END U002425 >>>
<<< UNIT U002426 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:420-420 | ctx=cli.instance_cmd.yes >>>
是
<<< END U002426 >>>
<<< UNIT U002427 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:421-421 | ctx=cli.instance_registry.bad_file >>>
实例注册表无法解析（${path}）：${error}
<<< END U002427 >>>
<<< UNIT U002428 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:422-422 | ctx=cli.instance_registry.bad_name >>>
实例名 ${name} 不合法，只允许小写字母、数字、连字符与下划线，且以字母或数字开头
<<< END U002428 >>>
<<< UNIT U002429 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:423-423 | ctx=cli.instance_registry.bad_section >>>
实例注册表结构不符（${path}）：instances 段不存在或不是表
<<< END U002429 >>>
<<< UNIT U002430 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:424-424 | ctx=cli.instance_registry.name_taken >>>
实例名 ${name} 已被 ${root} 占用，换一个名字
<<< END U002430 >>>
<<< UNIT U002431 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:425-425 | ctx=cli.instance_registry.not_instance >>>
${path} 不是实例目录（缺少 ${meta}），先用 `akaribot init` 创建
<<< END U002431 >>>
<<< UNIT U002432 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:426-426 | ctx=cli.instance_registry.not_instance_with_children >>>
${path} 不是实例目录（缺少 ${meta}）。它的子目录里已有实例：${found}，请添加其中之一
<<< END U002432 >>>
<<< UNIT U002433 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:427-427 | ctx=cli.instance_registry.unknown >>>
注册表里没有实例 ${name}，用 `akaribot instance list` 查看已添加的实例
<<< END U002433 >>>
<<< UNIT U002434 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:428-428 | ctx=cli.logs.all_processes >>>
全部进程
<<< END U002434 >>>
<<< UNIT U002435 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:429-429 | ctx=cli.logs.bad_lines >>>
行数需要是非负整数：${value}
<<< END U002435 >>>
<<< UNIT U002436 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:430-430 | ctx=cli.logs.conflict_level >>>
“--debug”与“--info”不能同时使用
<<< END U002436 >>>
<<< UNIT U002437 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:431-431 | ctx=cli.logs.conflict_output >>>
“--path”与“--json”不能同时使用
<<< END U002437 >>>
<<< UNIT U002438 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:432-432 | ctx=cli.logs.dir_missing >>>
日志目录不存在：${path}
<<< END U002438 >>>
<<< UNIT U002439 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:433-433 | ctx=cli.logs.dir_unreadable >>>
日志目录不可读：${path}（${error}）
<<< END U002439 >>>
<<< UNIT U002440 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:434-434 | ctx=cli.logs.empty_file >>>
日志文件 ${path} 目前没有内容
<<< END U002440 >>>
<<< UNIT U002441 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:435-435 | ctx=cli.logs.file_unreadable >>>
日志文件不可读：${path}（${error}）
<<< END U002441 >>>
<<< UNIT U002442 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:436-436 | ctx=cli.logs.follow_reset >>>
日志文件被截断或轮转，已从头继续跟随
<<< END U002442 >>>
<<< UNIT U002443 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:437-437 | ctx=cli.logs.help >>>
查看实例日志文件
<<< END U002443 >>>
<<< UNIT U002444 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:438-438 | ctx=cli.logs.level_missing >>>
没有 ${level} 级别的日志文件（进程 ${process}）
<<< END U002444 >>>
<<< UNIT U002445 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:439-439 | ctx=cli.logs.no_files >>>
日志目录 ${path} 里没有 ${process} 的日志文件
<<< END U002445 >>>
<<< UNIT U002446 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:440-440 | ctx=cli.logs.option_debug >>>
只查看 debug 级别的日志文件
<<< END U002446 >>>
<<< UNIT U002447 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:441-441 | ctx=cli.logs.option_follow >>>
持续输出新增行，直到 Ctrl+C
<<< END U002447 >>>
<<< UNIT U002448 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:442-442 | ctx=cli.logs.option_info >>>
只查看 INFO 级别的日志文件
<<< END U002448 >>>
<<< UNIT U002449 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:443-443 | ctx=cli.logs.option_lines >>>
首次输出的末尾行数
<<< END U002449 >>>
<<< UNIT U002450 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:444-444 | ctx=cli.logs.option_path >>>
只打印选中的日志文件路径，便于脚本自行处理
<<< END U002450 >>>
<<< UNIT U002451 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:445-445 | ctx=cli.logs.option_process >>>
只查看指定进程的日志文件
<<< END U002451 >>>
<<< UNIT U002452 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:446-446 | ctx=cli.logs.truncated >>>
文件较大，只输出末尾 ${count} 行，更早的内容未读取
<<< END U002452 >>>
<<< UNIT U002453 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:447-447 | ctx=cli.main.init_confirm >>>
当前目录不是 AkariBot 实例（未找到 akaribot.toml）。是否在此初始化并进入界面？
<<< END U002453 >>>
<<< UNIT U002454 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:448-448 | ctx=cli.main.init_failed >>>
初始化未完成，未进入界面。
<<< END U002454 >>>
<<< UNIT U002455 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:449-449 | ctx=cli.migrate.already_installed >>>
${dist} 已安装，跳过
<<< END U002455 >>>
<<< UNIT U002456 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:450-450 | ctx=cli.migrate.config_failure >>>
旧配置无法解析：${error}
<<< END U002456 >>>
<<< UNIT U002457 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:451-451 | ctx=cli.migrate.copy_line >>>
  ${name}：复制 ${copied}、一致 ${unchanged}、保留 ${kept}
<<< END U002457 >>>
<<< UNIT U002458 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:452-452 | ctx=cli.migrate.db.convert_failed >>>
数据库版本转换失败
<<< END U002458 >>>
<<< UNIT U002459 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:453-453 | ctx=cli.migrate.db.done >>>
完成：已应用 ${applied} 项迁移。旧版本号转换由 core 的 convert_legacy_version() 完成。
<<< END U002459 >>>
<<< UNIT U002460 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:454-454 | ctx=cli.migrate.db.no_python >>>
跳过：实例解释器不存在（--skip-install 或 venv 未创建），安装 core 后重新运行本命令即可补做。
<<< END U002460 >>>
<<< UNIT U002461 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:455-455 | ctx=cli.migrate.db.non_sqlite >>>
跳过：旧配置使用非 SQLite 数据库（${path}），数据须自行 dump 后导入。
<<< END U002461 >>>
<<< UNIT U002462 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:456-456 | ctx=cli.migrate.db.not_run >>>
未执行
<<< END U002462 >>>
<<< UNIT U002463 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:457-457 | ctx=cli.migrate.db.not_run_dry_run >>>
未执行（dry-run）
<<< END U002463 >>>
<<< UNIT U002464 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:458-458 | ctx=cli.migrate.db.not_run_skip_install >>>
未执行（--skip-install）。安装 core 后执行 `akaribot db upgrade`。
<<< END U002464 >>>
<<< UNIT U002465 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:459-459 | ctx=cli.migrate.db.skipped >>>
跳过：${error}
<<< END U002465 >>>
<<< UNIT U002466 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:460-460 | ctx=cli.migrate.dry_run_create >>>
[dim]dry-run：将创建实例 ${path}[/dim]
<<< END U002466 >>>
<<< UNIT U002467 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:461-461 | ctx=cli.migrate.dry_run_no_write >>>
[dim]dry-run：未写入任何文件[/dim]
<<< END U002467 >>>
<<< UNIT U002468 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:462-462 | ctx=cli.migrate.error.config_unreadable >>>
旧配置无法解析，尚未创建目标实例。请修复后重试：${errors}
<<< END U002468 >>>
<<< UNIT U002469 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:463-463 | ctx=cli.migrate.error.database_snapshot >>>
无法创建数据库快照：${path}（${error}）。请检查数据库文件后重试。
<<< END U002469 >>>
<<< UNIT U002470 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:464-464 | ctx=cli.migrate.error.database_target >>>
数据库副本必须位于新实例内，且不得指向源数据库：${path}
<<< END U002470 >>>
<<< UNIT U002471 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:465-465 | ctx=cli.migrate.error.database_conflict >>>
目标配置使用数据库 ${path}，本次迁移副本为 ${expected}。请使用新实例目录，或确认覆盖后加 --force。
<<< END U002471 >>>
<<< UNIT U002472 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:466-466 | ctx=cli.migrate.error.external_database >>>
自动迁移仅支持 SQLite 文件数据库。请先把外部数据库导出到独立的目标数据库，再手工迁移配置与数据。
<<< END U002472 >>>
<<< UNIT U002473 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:467-467 | ctx=cli.migrate.error.memory_database >>>
内存数据库没有可迁移的文件。请先把数据导出到 SQLite 文件数据库。
<<< END U002473 >>>
<<< UNIT U002474 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:468-468 | ctx=cli.migrate.error.source_lock_missing >>>
旧项目缺少实例级锁：${path}。请先正常启动并停止旧项目，再执行迁移。试运行可使用 --dry-run。
<<< END U002474 >>>
<<< UNIT U002475 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:469-469 | ctx=cli.migrate.error.source_changed >>>
源项目配置在检查后发生变化。请确认旧项目已停机，再重新执行迁移。
<<< END U002475 >>>
<<< UNIT U002476 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:470-470 | ctx=cli.migrate.error.symlink_target >>>
目标路径包含符号链接，无法保证源项目与实例数据隔离：${path}
<<< END U002476 >>>
<<< UNIT U002477 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:471-471 | ctx=cli.migrate.error.target_not_file >>>
目标路径不是普通文件：${path}
<<< END U002477 >>>
<<< UNIT U002478 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:472-472 | ctx=cli.migrate.error.target_config_invalid >>>
目标配置无法解析：${path}（${error}）。请修复后重试。
<<< END U002478 >>>
<<< UNIT U002479 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:473-473 | ctx=cli.migrate.error.no_mapping >>>
registry 里没有任何 legacy_module_map，无法确定旧模块名到新包的映射。用 --workspace-root 指向含 registry.json 的工作区根目录，或联网后重试。
<<< END U002479 >>>
<<< UNIT U002480 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:474-474 | ctx=cli.migrate.error.not_legacy >>>
${path} 不像是旧版 AkariBot 项目，缺少：${missing}。旧项目须同时含 bot.py、core/、modules/ 与 config/config.toml。
<<< END U002480 >>>
<<< UNIT U002481 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:475-475 | ctx=cli.migrate.error.not_workspace >>>
${path} 下没有 packages 目录，不像是 monorepo 工作区根目录。
<<< END U002481 >>>
<<< UNIT U002482 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:476-476 | ctx=cli.migrate.error.project_missing >>>
旧项目目录不存在：${path}
<<< END U002482 >>>
<<< UNIT U002483 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:477-477 | ctx=cli.migrate.error.project_not_dir >>>
旧项目路径不是目录：${path}
<<< END U002483 >>>
<<< UNIT U002484 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:478-478 | ctx=cli.migrate.error.registry_load >>>
无法加载 registry（${error}）。用 --workspace-root 指向含 registry.json 的工作区根目录，或联网后重试。
<<< END U002484 >>>
<<< UNIT U002485 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:479-479 | ctx=cli.migrate.error.registry_parse >>>
${path} 无法解析：${error}
<<< END U002485 >>>
<<< UNIT U002486 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:480-480 | ctx=cli.migrate.error.resolve >>>
无法解析 ${name}：${error}
<<< END U002486 >>>
<<< UNIT U002487 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:481-481 | ctx=cli.migrate.error.running >>>
${path} 的机器人正在运行。请先停止运行再迁移。
<<< END U002487 >>>
<<< UNIT U002488 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:482-482 | ctx=cli.migrate.error.target_inside >>>
新实例根目录不能位于旧项目目录内：${path}。迁移期间旧项目只读。
<<< END U002488 >>>
<<< UNIT U002489 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:483-483 | ctx=cli.migrate.error.target_not_empty >>>
${path} 非空且不是 AkariBot 实例。换一个空目录，或确认可写入后加 --force。
<<< END U002489 >>>
<<< UNIT U002490 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:484-484 | ctx=cli.migrate.help >>>
旧项目迁移，将旧版布局的项目迁移至实例目录（migrate legacy）
<<< END U002490 >>>
<<< UNIT U002491 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:485-485 | ctx=cli.migrate.inspected >>>
旧项目 ${root}：配置 ${configs} 个、数据库 ${databases} 个、模块目录 ${modules} 个、启用模块记录 ${enabled} 条
<<< END U002491 >>>
<<< UNIT U002492 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:486-486 | ctx=cli.migrate.install_failed >>>
${dist} 安装失败，已记入报告。可重新运行本命令或手动执行 `akaribot module add ${dist}`。
<<< END U002492 >>>
<<< UNIT U002493 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:487-487 | ctx=cli.migrate.instance_created >>>
已创建实例 ${root}（新建目录 ${count} 个，语言 ${locale}）
<<< END U002493 >>>
<<< UNIT U002494 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:488-488 | ctx=cli.migrate.legacy.arg_project >>>
旧项目根目录，须含 bot.py、core/、modules/、config/config.toml
<<< END U002494 >>>
<<< UNIT U002495 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:489-489 | ctx=cli.migrate.legacy.help >>>
把旧版项目迁移为新实例，包括迁移配置与数据、安装映射到的适配器与模块、转换数据库版本。

旧目录只读。迁移可重复执行，已完成的步骤不会重复施加。报告写到新实例根目录的 migration-report.md。
<<< END U002495 >>>
<<< UNIT U002496 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:490-490 | ctx=cli.migrate.legacy.option_dry_run >>>
只输出迁移报告，不写入任何文件
<<< END U002496 >>>
<<< UNIT U002497 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:491-491 | ctx=cli.migrate.legacy.option_force >>>
覆盖目标已存在的同名文件，并允许写入非空目录
<<< END U002497 >>>
<<< UNIT U002498 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:492-492 | ctx=cli.migrate.legacy.option_instance >>>
新实例根目录。默认为旧项目同级的 <旧项目名>-instance
<<< END U002498 >>>
<<< UNIT U002499 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:493-493 | ctx=cli.migrate.legacy.option_no_venv >>>
不托管 venv，安装到当前环境
<<< END U002499 >>>
<<< UNIT U002500 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:494-494 | ctx=cli.migrate.legacy.option_offline >>>
registry 只用本地缓存，不联网
<<< END U002500 >>>
<<< UNIT U002501 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:495-495 | ctx=cli.migrate.legacy.option_skip_install >>>
不安装 core、适配器与模块，只迁移文件
<<< END U002501 >>>
<<< UNIT U002502 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:496-496 | ctx=cli.migrate.legacy.option_verbose >>>
回显 uv 的全部输出
<<< END U002502 >>>
<<< UNIT U002503 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:497-497 | ctx=cli.migrate.legacy.option_workspace_root >>>
monorepo 工作区根目录，从本地源码安装并读取其中的 registry.json 做映射
<<< END U002503 >>>
<<< UNIT U002504 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:498-498 | ctx=cli.migrate.next_steps >>>
下一步：cd ${path} && akaribot run
<<< END U002504 >>>
<<< UNIT U002505 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:499-499 | ctx=cli.migrate.next_steps_manual >>>
下一步：查看报告的“需人工处理”小节，处理完再运行 `akaribot run`。
<<< END U002505 >>>
<<< UNIT U002506 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:500-500 | ctx=cli.migrate.none >>>
无
<<< END U002506 >>>
<<< UNIT U002507 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:501-501 | ctx=cli.migrate.plan.adapters >>>
适配器
<<< END U002507 >>>
<<< UNIT U002508 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:502-502 | ctx=cli.migrate.plan.modules >>>
模块
<<< END U002508 >>>
<<< UNIT U002509 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:503-503 | ctx=cli.migrate.plan.new >>>
新实例
<<< END U002509 >>>
<<< UNIT U002510 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:504-504 | ctx=cli.migrate.plan.old >>>
旧项目
<<< END U002510 >>>
<<< UNIT U002511 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:505-505 | ctx=cli.migrate.plan.skipped >>>
有目录但旧数据库未加载
<<< END U002511 >>>
<<< UNIT U002512 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:506-506 | ctx=cli.migrate.plan.title >>>
迁移计划
<<< END U002512 >>>
<<< UNIT U002513 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:507-507 | ctx=cli.migrate.plan.unmapped >>>
无法映射
<<< END U002513 >>>
<<< UNIT U002514 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:509-509 | ctx=cli.migrate.report.adapter_missing >>>
（registry 中无此适配器包）
<<< END U002514 >>>
<<< UNIT U002515 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:510-510 | ctx=cli.migrate.report.adapters_heading >>>
## 适配器
<<< END U002515 >>>
<<< UNIT U002516 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:511-511 | ctx=cli.migrate.report.copy_header >>>
| 类别 | 复制 | 内容一致 | 保留现有 | 旧项目缺失 |
<<< END U002516 >>>
<<< UNIT U002517 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:512-512 | ctx=cli.migrate.report.copy_heading >>>
## 复制结果
<<< END U002517 >>>
<<< UNIT U002518 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:515-515 | ctx=cli.migrate.report.db_result >>>
- 数据库版本转换：${result}
<<< END U002518 >>>
<<< UNIT U002519 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:516-516 | ctx=cli.migrate.report.generated_at >>>
- 生成时间：${time}
<<< END U002519 >>>
<<< UNIT U002520 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:517-517 | ctx=cli.migrate.report.install_failed_item >>>
- 安装失败：`${dist}`——${reason}
<<< END U002520 >>>
<<< UNIT U002521 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:518-518 | ctx=cli.migrate.report.install_heading >>>
## 安装结果
<<< END U002521 >>>
<<< UNIT U002522 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:519-519 | ctx=cli.migrate.report.install_skipped >>>
- 已安装跳过：${items}
<<< END U002522 >>>
<<< UNIT U002523 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:520-520 | ctx=cli.migrate.report.installed >>>
- 本次安装：${items}
<<< END U002523 >>>
<<< UNIT U002524 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:521-521 | ctx=cli.migrate.report.manual_config_failures >>>
以下旧配置无法解析，需人工检查并手工复制：${items}
<<< END U002524 >>>
<<< UNIT U002525 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:522-522 | ctx=cli.migrate.report.manual_credentials >>>
缺少登录信息的适配器（配置里仍是占位符）：${items}。运行 `akaribot config edit` 填写。
<<< END U002525 >>>
<<< UNIT U002526 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:523-523 | ctx=cli.migrate.report.manual_db_result >>>
数据库版本转换：${result}
<<< END U002526 >>>
<<< UNIT U002527 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:524-524 | ctx=cli.migrate.report.manual_heading >>>
## 需人工处理
<<< END U002527 >>>
<<< UNIT U002528 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:525-525 | ctx=cli.migrate.report.manual_install_failed >>>
安装失败的包：${items}。重新运行本命令可继续安装，或逐个执行 `akaribot module add`。
<<< END U002528 >>>
<<< UNIT U002529 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:527-527 | ctx=cli.migrate.report.manual_missing_adapters >>>
registry 中没有对应条目，需先发布或改用 `akaribot module add -e`：${items}
<<< END U002529 >>>
<<< UNIT U002530 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:528-528 | ctx=cli.migrate.report.manual_none >>>
无需人工处理。
<<< END U002530 >>>
<<< UNIT U002531 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:529-529 | ctx=cli.migrate.report.manual_placeholders >>>
未填写占位符共 ${total} 项，分布在：${items}
<<< END U002531 >>>
<<< UNIT U002532 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:530-530 | ctx=cli.migrate.report.manual_status_unreadable >>>
旧数据库的 module_status 读取失败，无法判断哪些模块真正加载过，因此本次没有安装任何普通模块。请核对下方目录清单后，用 `akaribot module add <模块名>` 逐个安装。
<<< END U002532 >>>
<<< UNIT U002533 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:531-531 | ctx=cli.migrate.report.manual_unmapped >>>
无法映射的旧模块：${items}。多为自写模块，打包后用 `akaribot module add -e <模块目录>` 安装。
<<< END U002533 >>>
<<< UNIT U002534 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:532-532 | ctx=cli.migrate.report.mode >>>
- 运行模式：${mode}
<<< END U002534 >>>
<<< UNIT U002535 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:533-533 | ctx=cli.migrate.report.mode_dry_run >>>
dry-run（未写入任何文件）
<<< END U002535 >>>
<<< UNIT U002536 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:534-534 | ctx=cli.migrate.report.mode_real >>>
正式执行
<<< END U002536 >>>
<<< UNIT U002537 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:535-535 | ctx=cli.migrate.report.modules_header >>>
| 旧模块名 | 新包名 | 名字来源 |
<<< END U002537 >>>
<<< UNIT U002538 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:536-536 | ctx=cli.migrate.report.modules_heading >>>
## 模块映射
<<< END U002538 >>>
<<< UNIT U002539 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:537-537 | ctx=cli.migrate.report.modules_note >>>
映射来自 registry 的 `legacy_module_map`。多个旧模块名可指向同一个包（如 wiki 家族）。
<<< END U002539 >>>
<<< UNIT U002540 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:540-540 | ctx=cli.migrate.report.multi_heading >>>
## 多实例
<<< END U002540 >>>
<<< UNIT U002541 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:541-541 | ctx=cli.migrate.report.multi_note >>>
迁移一律生成默认实例（实例 ID 为空，`client_name` 与旧项目相同），因此 `target_id` 前缀不变，
全部场景数据原样可用，无需改写数据库。如需第二个账号，用
`akaribot adapter instance add <平台> <实例 ID>` 新建实例后再填写其登录信息。
<<< END U002541 >>>
<<< UNIT U002542 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:542-542 | ctx=cli.migrate.report.new_instance >>>
- 新实例：`${path}`
<<< END U002542 >>>
<<< UNIT U002543 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:543-543 | ctx=cli.migrate.report.no_adapters >>>
旧配置里没有 `enable = true` 的适配器基础配置表。
<<< END U002543 >>>
<<< UNIT U002544 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:544-544 | ctx=cli.migrate.report.no_modules >>>
旧项目里没有可映射的模块。
<<< END U002544 >>>
<<< UNIT U002545 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:545-545 | ctx=cli.migrate.report.nothing_installed >>>
- 未安装任何包（`--skip-install` 或 dry-run）。
<<< END U002545 >>>
<<< UNIT U002546 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:546-546 | ctx=cli.migrate.report.old_project >>>
- 旧项目：`${path}`（只读，迁移全程未修改）
<<< END U002546 >>>
<<< UNIT U002547 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:547-547 | ctx=cli.migrate.report.skipped >>>
以下模块在旧 `modules/` 里有目录，但旧数据库显示从未加载，故未安装（其 `data/` 仍已迁移，需要时用 `akaribot module add <模块名>` 启用）：${items}
<<< END U002547 >>>
<<< UNIT U002548 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:548-548 | ctx=cli.migrate.report.title >>>
# 旧项目迁移报告
<<< END U002548 >>>
<<< UNIT U002549 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:549-549 | ctx=cli.migrate.report_written >>>
已写出 ${path}
<<< END U002549 >>>
<<< UNIT U002550 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:550-550 | ctx=cli.migrate.resolve_failed >>>
${dist} 解析失败：${error}
<<< END U002550 >>>
<<< UNIT U002551 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:551-551 | ctx=cli.migrate.reuse_instance >>>
  复用已有实例：${path}
<<< END U002551 >>>
<<< UNIT U002552 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:552-552 | ctx=cli.migrate.skip_install >>>
[dim]${reason}：跳过 ${count} 个包的安装[/dim]
<<< END U002552 >>>
<<< UNIT U002553 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:553-553 | ctx=cli.migrate.source.database >>>
数据库
<<< END U002553 >>>
<<< UNIT U002554 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:554-554 | ctx=cli.migrate.source.dir >>>
目录
<<< END U002554 >>>
<<< UNIT U002555 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:555-555 | ctx=cli.migrate.step.copy >>>
复制配置与数据
<<< END U002555 >>>
<<< UNIT U002556 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:556-556 | ctx=cli.migrate.step.create >>>
创建新实例
<<< END U002556 >>>
<<< UNIT U002557 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:557-557 | ctx=cli.migrate.step.inspect >>>
校验旧项目
<<< END U002557 >>>
<<< UNIT U002558 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:558-558 | ctx=cli.migrate.step.install >>>
安装适配器与模块
<<< END U002558 >>>
<<< UNIT U002559 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:559-559 | ctx=cli.migrate.step.mapping >>>
解析模块映射
<<< END U002559 >>>
<<< UNIT U002560 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:560-560 | ctx=cli.migrate.step.report >>>
写出迁移报告
<<< END U002560 >>>
<<< UNIT U002561 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:561-561 | ctx=cli.migrate.tally.config >>>
配置文件
<<< END U002561 >>>
<<< UNIT U002562 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:562-562 | ctx=cli.migrate.tally.database >>>
数据库文件
<<< END U002562 >>>
<<< UNIT U002563 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:563-563 | ctx=cli.migrate.tally.runtime >>>
运行时资源
<<< END U002563 >>>
<<< UNIT U002564 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:564-564 | ctx=cli.migrate.unmapped >>>
无法映射的模块（记入报告的人工清单）：${modules}
<<< END U002564 >>>
<<< UNIT U002565 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:565-565 | ctx=cli.migrate.venv_failed >>>
${error}。本机没有 uv 时可安装后重新运行，或用 --no-venv 安装到当前环境。
<<< END U002565 >>>
<<< UNIT U002566 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:566-566 | ctx=cli.module.add.already_installed >>>
${dist} 已安装（${version}）。升级请用 `akaribot module update ${name}`，重新安装请加 --force。
<<< END U002566 >>>
<<< UNIT U002567 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:567-567 | ctx=cli.module.add.arg_name >>>
模块名、适配器名或包名。用 -e 时可省略
<<< END U002567 >>>
<<< UNIT U002568 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:568-568 | ctx=cli.module.add.force_reinstall >>>
${dist} 已安装（${version}），--force 将覆盖重新安装。
<<< END U002568 >>>
<<< UNIT U002569 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:569-569 | ctx=cli.module.add.help >>>
安装模块或适配器，依次执行解析、检查、安装、补充配置、迁移、热装载与报告。
<<< END U002569 >>>
<<< UNIT U002570 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:570-570 | ctx=cli.module.add.next_steps >>>

下一步：`akaribot config edit` 填写占位符，运行中可用 `~reload` 让改动生效。
<<< END U002570 >>>
<<< UNIT U002571 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:571-571 | ctx=cli.module.add.option_dist >>>
直接指定包名，跳过 registry 查找
<<< END U002571 >>>
<<< UNIT U002572 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:572-572 | ctx=cli.module.add.option_editable >>>
以可编辑方式安装该本地目录
<<< END U002572 >>>
<<< UNIT U002573 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:573-573 | ctx=cli.module.add.option_extra >>>
要一并安装的 extra，可重复
<<< END U002573 >>>
<<< UNIT U002574 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:574-574 | ctx=cli.module.add.option_force >>>
检查发现冲突时仍然继续安装
<<< END U002574 >>>
<<< UNIT U002575 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:575-575 | ctx=cli.module.add.option_git >>>
从 git 仓库安装，填写仓库地址（uv 支持的写法，可带 git+ 前缀）
<<< END U002575 >>>
<<< UNIT U002576 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:576-576 | ctx=cli.module.add.option_kind >>>
限定包种类：module 或 adapter
<<< END U002576 >>>
<<< UNIT U002577 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:577-577 | ctx=cli.module.add.option_ref >>>
配合 --git：分支、标签或提交
<<< END U002577 >>>
<<< UNIT U002578 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:578-578 | ctx=cli.module.add.option_subdir >>>
配合 --git：包在仓库中的子目录
<<< END U002578 >>>
<<< UNIT U002579 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:579-579 | ctx=cli.module.add.option_version >>>
版本或版本区间，如 1.2.3 或 '>=1,<2'
<<< END U002579 >>>
<<< UNIT U002580 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:580-580 | ctx=cli.module.add.ref_without_git >>>
--ref / --subdir 只在 --git 模式下有意义。
<<< END U002580 >>>
<<< UNIT U002581 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:581-581 | ctx=cli.module.available.cached_hint >>>
列表来自本地缓存。获取最新索引请加 --refresh。
<<< END U002581 >>>
<<< UNIT U002582 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:582-582 | ctx=cli.module.available.column_developers >>>
作者
<<< END U002582 >>>
<<< UNIT U002583 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:583-583 | ctx=cli.module.available.column_dist >>>
包名
<<< END U002583 >>>
<<< UNIT U002584 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:584-584 | ctx=cli.module.available.column_kind >>>
类型
<<< END U002584 >>>
<<< UNIT U002585 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:585-585 | ctx=cli.module.available.column_latest >>>
最新版本
<<< END U002585 >>>
<<< UNIT U002586 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:586-586 | ctx=cli.module.available.column_name >>>
名称
<<< END U002586 >>>
<<< UNIT U002587 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:587-587 | ctx=cli.module.available.column_path >>>
包路径
<<< END U002587 >>>
<<< UNIT U002588 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:588-588 | ctx=cli.module.available.column_state >>>
状态
<<< END U002588 >>>
<<< UNIT U002589 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:589-589 | ctx=cli.module.available.column_summary >>>
简介
<<< END U002589 >>>
<<< UNIT U002590 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:590-590 | ctx=cli.module.available.help >>>
列出 registry 中可安装的模块与适配器，并标出哪些已安装。
<<< END U002590 >>>
<<< UNIT U002591 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:591-591 | ctx=cli.module.available.install_hint >>>
安装：`akaribot module add <名称>`。按包名安装用 `akaribot module add --dist <包名>`。
<<< END U002591 >>>
<<< UNIT U002592 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:592-592 | ctx=cli.module.available.none >>>
没有匹配的包（搜索词“${search}”）。
<<< END U002592 >>>
<<< UNIT U002593 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:593-593 | ctx=cli.module.available.none_hint >>>
去掉 --search 或 --kind 查看全部。索引过旧时请加 --refresh。
<<< END U002593 >>>
<<< UNIT U002594 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:594-594 | ctx=cli.module.available.option_kind >>>
只查看 module 或 adapter
<<< END U002594 >>>
<<< UNIT U002595 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:595-595 | ctx=cli.module.available.option_refresh >>>
忽略缓存，重新校验 registry
<<< END U002595 >>>
<<< UNIT U002596 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:596-596 | ctx=cli.module.available.option_search >>>
按名称、包名、提供的模块名或简介筛选
<<< END U002596 >>>
<<< UNIT U002597 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:597-597 | ctx=cli.module.available.source_line >>>
可安装集合来源：${source}
<<< END U002597 >>>
<<< UNIT U002598 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:598-598 | ctx=cli.module.available.source_workspace >>>
本地工作区 ${root}
<<< END U002598 >>>
<<< UNIT U002599 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:599-599 | ctx=cli.module.available.state_available >>>
可安装
<<< END U002599 >>>
<<< UNIT U002600 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:600-600 | ctx=cli.module.available.state_installed >>>
已安装
<<< END U002600 >>>
<<< UNIT U002601 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:601-601 | ctx=cli.module.available.table_title >>>
可安装的包（${count} 个）
<<< END U002601 >>>
<<< UNIT U002602 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:602-602 | ctx=cli.module.dry_run_precheck >>>
[dim]dry-run：跳过检查[/dim]
<<< END U002602 >>>
<<< UNIT U002603 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:603-603 | ctx=cli.module.dry_run_skip_rest >>>
[dim]dry-run：跳过 config sync、db upgrade 与热装载通知[/dim]
<<< END U002603 >>>
<<< UNIT U002604 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:604-604 | ctx=cli.module.git.ambiguous >>>
安装完成后新增了多个包（${names}），无法判断是哪一个。请用 `--dist <包名>` 指明。
<<< END U002604 >>>
<<< UNIT U002605 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:605-605 | ctx=cli.module.git.editable_conflict >>>
--git 与 -e/--editable 互斥，前者取自远端仓库，后者取自本地目录。
<<< END U002605 >>>
<<< UNIT U002606 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:606-606 | ctx=cli.module.git.nothing_added >>>
git 安装后没有发现新增包。若该包已安装过，请用 `--dist <包名>` 重试。
<<< END U002606 >>>
<<< UNIT U002607 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:607-607 | ctx=cli.module.git.ref_conflict >>>
仓库地址里已经带了 ref，请勿再用 --ref。
<<< END U002607 >>>
<<< UNIT U002608 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:608-608 | ctx=cli.module.git.resolved >>>
  解析出包名：${dist}
<<< END U002608 >>>
<<< UNIT U002609 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:609-609 | ctx=cli.module.git.rolled_back >>>
${dist} 声明的 core API 与本实例不符，已卸载回滚。
<<< END U002609 >>>
<<< UNIT U002610 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:610-610 | ctx=cli.module.git.subdir_conflict >>>
仓库地址里已经带了 #subdirectory，请勿再用 --subdir。
<<< END U002610 >>>
<<< UNIT U002611 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:611-611 | ctx=cli.module.git.url_required >>>
--git 需要一个仓库地址。
<<< END U002611 >>>
<<< UNIT U002612 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:612-612 | ctx=cli.module.git.version_conflict >>>
--git 与 --version 互斥，git 直接引用的版本由 --ref 指定。
<<< END U002612 >>>
<<< UNIT U002613 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:613-613 | ctx=cli.module.help >>>
模块安装与全局加载（list / add / remove / update / load / unload）

三级“启用”语义中，add/remove 控制代码是否安装在本实例，load/unload 控制模块是否参与命令匹配（等价于机器人内的 `~module load` / `~module unload`，超级用户）。某个群/频道能否使用是场景级开关，由机器人内的 `~module enable` / `~module disable`（场景管理员）负责。本组命令不使用 enable/disable 表示全局加载。
<<< END U002613 >>>
<<< UNIT U002614 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:614-614 | ctx=cli.module.install.config_changed >>>
  配置文件变更：${paths}
<<< END U002614 >>>
<<< UNIT U002615 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:615-615 | ctx=cli.module.install.config_restored >>>
  已恢复配置文件：${paths}
<<< END U002615 >>>
<<< UNIT U002616 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:616-616 | ctx=cli.module.install.config_sync_failed >>>
${dist} 的配置补充失败，安装已回滚。
<<< END U002616 >>>
<<< UNIT U002617 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:617-617 | ctx=cli.module.install.db_upgrade_failed >>>
${dist} 的数据库迁移失败，安装已回滚。
<<< END U002617 >>>
<<< UNIT U002618 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:618-618 | ctx=cli.module.install.no_placeholders >>>
没有待填写的占位符
<<< END U002618 >>>
<<< UNIT U002619 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:619-619 | ctx=cli.module.install.placeholders_left >>>
[yellow]有 ${count} 项仍是 <Replace me> 占位符，运行 `akaribot config edit` 填写。[/yellow]
<<< END U002619 >>>
<<< UNIT U002620 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:620-620 | ctx=cli.module.install.precheck_git >>>
  来自 git 仓库的包需安装后才能读到 manifest，兼容性检查改为安装后执行。
<<< END U002620 >>>
<<< UNIT U002621 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:621-621 | ctx=cli.module.install.restart_needed >>>
模块已安装完成，但需要 `~restart` 或重启进程后才会加载。
<<< END U002621 >>>
<<< UNIT U002622 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:622-622 | ctx=cli.module.install.rollback_migration_kept >>>
数据库迁移不回滚，已创建的表将保留，属幂等且向前的变更。
<<< END U002622 >>>
<<< UNIT U002623 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:623-623 | ctx=cli.module.install.rollback_start >>>
开始回滚安装
<<< END U002623 >>>
<<< UNIT U002624 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:624-624 | ctx=cli.module.install.specs_line >>>
  安装参数：${specs}
<<< END U002624 >>>
<<< UNIT U002625 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:625-625 | ctx=cli.module.install.step_config_sync >>>
补充配置（config sync）
<<< END U002625 >>>
<<< UNIT U002626 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:626-626 | ctx=cli.module.install.step_db_upgrade >>>
应用数据库迁移（db upgrade）
<<< END U002626 >>>
<<< UNIT U002627 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:627-627 | ctx=cli.module.install.step_install >>>
下载并安装（${python}）
<<< END U002627 >>>
<<< UNIT U002628 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:628-628 | ctx=cli.module.install.step_notify >>>
通知运行中的实例
<<< END U002628 >>>
<<< UNIT U002629 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:629-629 | ctx=cli.module.install.step_precheck >>>
兼容性检查
<<< END U002629 >>>
<<< UNIT U002630 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:630-630 | ctx=cli.module.install.step_report >>>
报告配置项
<<< END U002630 >>>
<<< UNIT U002631 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:631-631 | ctx=cli.module.install.step_resolve >>>
解析 ${dist}（来源：${source}）
<<< END U002631 >>>
<<< UNIT U002632 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:632-632 | ctx=cli.module.list.column_developers >>>
作者
<<< END U002632 >>>
<<< UNIT U002633 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:633-633 | ctx=cli.module.list.column_dist >>>
包名
<<< END U002633 >>>
<<< UNIT U002634 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:634-634 | ctx=cli.module.list.column_kind >>>
种类
<<< END U002634 >>>
<<< UNIT U002635 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:635-635 | ctx=cli.module.list.column_name >>>
名字
<<< END U002635 >>>
<<< UNIT U002636 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:636-636 | ctx=cli.module.list.column_provides >>>
提供模块
<<< END U002636 >>>
<<< UNIT U002637 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:637-637 | ctx=cli.module.list.column_source >>>
来源
<<< END U002637 >>>
<<< UNIT U002638 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:638-638 | ctx=cli.module.list.column_version >>>
版本
<<< END U002638 >>>
<<< UNIT U002639 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:639-639 | ctx=cli.module.list.help >>>
列出已安装的模块与适配器。
<<< END U002639 >>>
<<< UNIT U002640 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:640-640 | ctx=cli.module.list.option_kind >>>
只查看 module 或 adapter
<<< END U002640 >>>
<<< UNIT U002641 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:641-641 | ctx=cli.module.list.source_dist >>>
发行版
<<< END U002641 >>>
<<< UNIT U002642 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:642-642 | ctx=cli.module.list.source_editable >>>
可编辑
<<< END U002642 >>>
<<< UNIT U002643 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:643-643 | ctx=cli.module.list.table_title >>>
已安装 akaribot 包（${count}）
<<< END U002643 >>>
<<< UNIT U002644 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:644-644 | ctx=cli.module.load.help >>>
全局装载模块，使其参与命令匹配（与安装、场景启用是两回事）。

“实例 ID 一旦使用请勿更改”这条约束**不适用于本命令**，它只修改全局装载状态，不触碰任何配置。
<<< END U002644 >>>
<<< UNIT U002645 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:645-645 | ctx=cli.module.not_installed >>>
${name} 未安装。用 `akaribot module list` 查看已安装包。
<<< END U002645 >>>
<<< UNIT U002646 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:646-646 | ctx=cli.module.option_dry_run >>>
只打印将执行的命令，不修改任何文件
<<< END U002646 >>>
<<< UNIT U002647 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:647-647 | ctx=cli.module.option_offline >>>
registry 只用本地缓存，不联网
<<< END U002647 >>>
<<< UNIT U002648 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:648-648 | ctx=cli.module.option_verbose >>>
回显 uv 的全部输出
<<< END U002648 >>>
<<< UNIT U002649 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:649-649 | ctx=cli.module.precheck.adjust >>>
${dist} 要求 ${requirement}${specifier}，安装时将把已安装的 ${current} 调整为 ${version}
<<< END U002649 >>>
<<< UNIT U002650 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:650-650 | ctx=cli.module.precheck.api_mismatch >>>
${dist} 要求 core API ${spec}，当前为 ${current}
<<< END U002650 >>>
<<< UNIT U002651 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:651-651 | ctx=cli.module.precheck.api_unknown >>>
未能读到已安装 core 的 API 版本，跳过 core API 兼容性检查。
<<< END U002651 >>>
<<< UNIT U002652 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:652-652 | ctx=cli.module.precheck.conflict >>>
依赖冲突（见上）。修正版本约束后重试，或确认无碍后加 --force。
<<< END U002652 >>>
<<< UNIT U002653 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:653-653 | ctx=cli.module.precheck.force >>>
--force：忽略上述冲突继续安装，机器人可能无法启动。
<<< END U002653 >>>
<<< UNIT U002654 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:654-654 | ctx=cli.module.precheck.installed_requirements >>>
  已安装包对它的要求：${items}
<<< END U002654 >>>
<<< UNIT U002655 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:655-655 | ctx=cli.module.precheck.ok >>>
兼容性检查通过
<<< END U002655 >>>
<<< UNIT U002656 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:656-656 | ctx=cli.module.precheck.unparsable_api >>>
${dist} 的 requires_core_api 无法解析：${spec}
<<< END U002656 >>>
<<< UNIT U002657 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:657-657 | ctx=cli.module.purge.confirm >>>
确认删除上述数据表与配置文件（不可恢复）
<<< END U002657 >>>
<<< UNIT U002658 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:658-658 | ctx=cli.module.purge.done >>>
已清理 ${count} 个包的数据表
<<< END U002658 >>>
<<< UNIT U002659 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:659-659 | ctx=cli.module.purge.failed_file >>>
删除配置文件 ${path} 失败：${error}
<<< END U002659 >>>
<<< UNIT U002660 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:660-660 | ctx=cli.module.purge.failed_tables >>>
${dist} 的数据表未能删除
<<< END U002660 >>>
<<< UNIT U002661 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:661-661 | ctx=cli.module.purge.files >>>
  将删除配置文件：${files}
<<< END U002661 >>>
<<< UNIT U002662 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:662-662 | ctx=cli.module.purge.instance_kept >>>
${dist} 有 ${count} 个适配器实例配置保留（要一并删除请加 --yes，或在确认提示里同意）
<<< END U002662 >>>
<<< UNIT U002663 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:663-663 | ctx=cli.module.purge.none >>>
无
<<< END U002663 >>>
<<< UNIT U002664 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:664-664 | ctx=cli.module.purge.none_tables >>>
无（manifest 未声明 owned_tables）
<<< END U002664 >>>
<<< UNIT U002665 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:665-665 | ctx=cli.module.purge.partial >>>
清理未全部完成：${reasons}
<<< END U002665 >>>
<<< UNIT U002666 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:666-666 | ctx=cli.module.purge.removed_files >>>
已删除 ${count} 个配置文件
<<< END U002666 >>>
<<< UNIT U002667 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:667-667 | ctx=cli.module.purge.tables >>>
  将删除数据表：${tables}
<<< END U002667 >>>
<<< UNIT U002668 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:668-668 | ctx=cli.module.remove.arg_name >>>
已安装的模块名、适配器名或包名
<<< END U002668 >>>
<<< UNIT U002669 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:669-669 | ctx=cli.module.remove.cascade_confirm >>>
将卸载 ${count} 个包，继续
<<< END U002669 >>>
<<< UNIT U002670 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:670-670 | ctx=cli.module.remove.cascade_list >>>
连带卸载清单：${packages}
<<< END U002670 >>>
<<< UNIT U002671 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:671-671 | ctx=cli.module.remove.dependents >>>
${name} 被以下包依赖：${packages}。默认拒绝卸载。确认连带卸载加 --cascade，确认破坏依赖加 --force。
<<< END U002671 >>>
<<< UNIT U002672 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:672-672 | ctx=cli.module.remove.detach_blocked >>>
${dist} 未能确认热拆卸：${detail}
<<< END U002672 >>>
<<< UNIT U002673 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:673-673 | ctx=cli.module.remove.detach_failed >>>
已中止卸载：${reasons}。运行中的实例可能仍持有这些模块，删除包会留下指向已删除代码的运行状态。请先停止实例（`akaribot run` 的进程）后重试。
<<< END U002673 >>>
<<< UNIT U002674 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:674-674 | ctx=cli.module.remove.force_warning >>>
--force：${packages} 将因缺少依赖在 discover() 时不再注册（可恢复，不是数据损坏）。
<<< END U002674 >>>
<<< UNIT U002675 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:675-675 | ctx=cli.module.remove.help >>>
卸载模块或适配器。默认保留配置与数据，并做反向依赖检查。
<<< END U002675 >>>
<<< UNIT U002676 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:676-676 | ctx=cli.module.remove.keep_data >>>
配置与数据默认保留。要一并清理请加 --purge-data。
<<< END U002676 >>>
<<< UNIT U002677 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:678-678 | ctx=cli.module.remove.option_cascade >>>
连带卸载依赖它的包，先列清单再二次确认
<<< END U002677 >>>
<<< UNIT U002678 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:679-679 | ctx=cli.module.remove.option_force >>>
无视反向依赖强行卸载并告警
<<< END U002678 >>>
<<< UNIT U002679 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:680-680 | ctx=cli.module.remove.option_purge_data >>>
同时删除该包的数据表与配置文件
<<< END U002679 >>>
<<< UNIT U002680 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:681-681 | ctx=cli.module.remove.purge_failed >>>
已中止卸载：数据清理未完成。运行中的实例与已安装包保持原状，修复上述原因后重试。确需接受残留时请加 --force。
<<< END U002680 >>>
<<< UNIT U002681 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:682-682 | ctx=cli.module.remove.purge_failed_forced >>>
--force：接受数据残留，继续卸载包。
<<< END U002681 >>>
<<< UNIT U002682 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:683-683 | ctx=cli.module.remove.purge_instances_confirm >>>
将连同 ${count} 个适配器实例配置一起删除（不可恢复），继续
<<< END U002682 >>>
<<< UNIT U002683 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:684-684 | ctx=cli.module.status.bad_json >>>
模块状态输出无法解析：${error}
<<< END U002683 >>>
<<< UNIT U002684 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:685-685 | ctx=cli.module.status.column_dist >>>
所属分发
<<< END U002684 >>>
<<< UNIT U002685 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:686-686 | ctx=cli.module.status.column_module >>>
模块
<<< END U002685 >>>
<<< UNIT U002686 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:687-687 | ctx=cli.module.status.column_state >>>
装载
<<< END U002686 >>>
<<< UNIT U002687 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:688-688 | ctx=cli.module.status.failed >>>
读取模块装载状态失败
<<< END U002687 >>>
<<< UNIT U002688 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:689-689 | ctx=cli.module.status.help >>>
列出各模块的全局装载状态（module_status.load）
<<< END U002688 >>>
<<< UNIT U002689 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:690-690 | ctx=cli.module.status.state_loaded >>>
已装载
<<< END U002689 >>>
<<< UNIT U002690 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:691-691 | ctx=cli.module.status.state_unknown >>>
未知
<<< END U002690 >>>
<<< UNIT U002691 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:692-692 | ctx=cli.module.status.state_unloaded >>>
未装载
<<< END U002691 >>>
<<< UNIT U002692 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:693-693 | ctx=cli.module.status.table_title >>>
模块装载状态（共 ${count} 个）
<<< END U002692 >>>
<<< UNIT U002693 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:694-694 | ctx=cli.module.unload.help >>>
全局卸载模块，使其退出命令匹配，代码与配置都保留。

“实例 ID 一旦使用请勿更改”这条约束**不适用于本命令**，它只修改全局装载状态，不触碰任何配置。
<<< END U002693 >>>
<<< UNIT U002694 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:695-695 | ctx=cli.module.update.arg_name >>>
要更新的包名，可给多个。默认配合 --all
<<< END U002694 >>>
<<< UNIT U002695 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:696-696 | ctx=cli.module.update.confirm >>>
更新 ${count} 个包
<<< END U002695 >>>
<<< UNIT U002696 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:697-697 | ctx=cli.module.update.detach_failed >>>
${dist} 未能确认热拆卸：${detail}。已跳过它的热装载，需 `~restart` 或重启进程后才会换到新代码。
<<< END U002696 >>>
<<< UNIT U002697 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:698-698 | ctx=cli.module.update.detach_line >>>
  已热卸载旧版本：${dist}
<<< END U002697 >>>
<<< UNIT U002698 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:699-699 | ctx=cli.module.update.done >>>
已更新 ${count} 个包
<<< END U002698 >>>
<<< UNIT U002699 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:700-700 | ctx=cli.module.update.failed >>>
更新包失败：${detail}
<<< END U002699 >>>
<<< UNIT U002700 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:701-701 | ctx=cli.module.update.help >>>
更新已安装的包。工作区模式下等价于按本地源码重新安装。

``--json`` 模式下 stdout 只出现一行结果 JSON（``updated`` / ``failed`` / ``skipped`` /
``failed_details`` / ``skipped_details`` / ``reload_pending`` / ``restart_required``），
进度与警告一律输出到 stderr，退出码 1 表示有包未更新成功。
<<< END U002700 >>>
<<< UNIT U002701 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:702-702 | ctx=cli.module.update.local_source >>>
本地源码
<<< END U002701 >>>
<<< UNIT U002702 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:703-703 | ctx=cli.module.update.no_names >>>
请给出要更新的包名，或用 `akaribot module update --all` 更新全部。
<<< END U002702 >>>
<<< UNIT U002703 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:704-704 | ctx=cli.module.update.nothing_to_do >>>
没有需要更新的包
<<< END U002703 >>>
<<< UNIT U002704 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:705-705 | ctx=cli.module.update.notified_suffix >>>
。运行中的实例已收到热装载通知
<<< END U002704 >>>
<<< UNIT U002705 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:706-706 | ctx=cli.module.update.ok >>>
更新包完成
<<< END U002705 >>>
<<< UNIT U002706 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:707-707 | ctx=cli.module.update.option_all >>>
更新全部已安装包（含 core）
<<< END U002706 >>>
<<< UNIT U002707 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:708-708 | ctx=cli.module.update.option_force >>>
已是最新版本时也重新安装
<<< END U002707 >>>
<<< UNIT U002708 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:709-709 | ctx=cli.module.update.option_json >>>
stdout 只输出一行结果 JSON，进度与警告输出到 stderr
<<< END U002708 >>>
<<< UNIT U002709 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:710-710 | ctx=cli.module.update.option_non_interactive >>>
不提问，等同 --yes。供机器人内的 ~update 交由 CLI 调用
<<< END U002709 >>>
<<< UNIT U002710 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:711-711 | ctx=cli.module.update.partial >>>
仅 ${count} 个包更新成功。请检查上面的错误后重试。
<<< END U002710 >>>
<<< UNIT U002711 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:712-712 | ctx=cli.module.update.skip_line >>>
  跳过 ${dist}：${reason}
<<< END U002711 >>>
<<< UNIT U002712 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:713-713 | ctx=cli.module.update.skip_no_registry >>>
registry 里没有该分发
<<< END U002712 >>>
<<< UNIT U002713 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:714-714 | ctx=cli.module.update.skip_no_workspace >>>
工作区里没有该包
<<< END U002713 >>>
<<< UNIT U002714 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:715-715 | ctx=cli.module.update.skip_up_to_date >>>
已是最新（${version}）
<<< END U002714 >>>
<<< UNIT U002715 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:716-716 | ctx=cli.module.update.verbose_ignored >>>
[dim]--json 下忽略 --verbose，stdout 只允许出现结果 JSON。[/dim]
<<< END U002715 >>>
<<< UNIT U002716 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:717-717 | ctx=cli.module.update.will_update >>>
将更新：${targets}
<<< END U002716 >>>
<<< UNIT U002717 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:718-718 | ctx=cli.new.adapter.add_failed >>>
akaribot module add 未成功（通常是当前目录不是实例）。请稍后手动执行：
  cd ${target} && akaribot module add -e .
<<< END U002717 >>>
<<< UNIT U002718 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:719-719 | ctx=cli.new.adapter.add_option >>>
生成后执行 akaribot module add -e .
<<< END U002718 >>>
<<< UNIT U002719 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:720-720 | ctx=cli.new.adapter.author_option >>>
作者名，写入 pyproject 的 authors
<<< END U002719 >>>
<<< UNIT U002720 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:721-721 | ctx=cli.new.adapter.config_option >>>
生成 config.py、manifest 的配置表声明与配置注释
<<< END U002720 >>>
<<< UNIT U002721 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:722-722 | ctx=cli.new.adapter.config_required >>>
已给出配置项或登录信息字段，不能再加 --no-config。
<<< END U002721 >>>
<<< UNIT U002722 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:723-723 | ctx=cli.new.adapter.credential_option >>>
登录信息字段名，可多次指定。写入 secret 表与 manifest 的 credential_fields
<<< END U002722 >>>
<<< UNIT U002723 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:724-724 | ctx=cli.new.adapter.desc_default >>>
${name} 平台适配器。
<<< END U002723 >>>
<<< UNIT U002724 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:725-725 | ctx=cli.new.adapter.desc_option >>>
一句话说明，写入 pyproject 的 description 与 README
<<< END U002724 >>>
<<< UNIT U002725 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:726-726 | ctx=cli.new.adapter.dir_option >>>
生成目录，包目录为 <生成目录>/akari-bot-adapter-<name>
<<< END U002725 >>>
<<< UNIT U002726 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:727-727 | ctx=cli.new.adapter.feature_option >>>
平台能力，如 support_image 或 support_image=false，可多次指定。给出时以本选项为准，留空则使用默认能力集
<<< END U002726 >>>
<<< UNIT U002727 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:728-728 | ctx=cli.new.adapter.field_option >>>
配置项，形如 字段名[:类型][=默认值]，可多次指定。类型可选 str / bool / int / float / list
<<< END U002727 >>>
<<< UNIT U002728 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:729-729 | ctx=cli.new.adapter.force_option >>>
目标目录非空时覆盖
<<< END U002728 >>>
<<< UNIT U002729 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:730-730 | ctx=cli.new.adapter.generated >>>
已生成 ${count} 个文件：${target}
<<< END U002729 >>>
<<< UNIT U002730 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:731-731 | ctx=cli.new.adapter.help >>>
生成平台适配器包。
<<< END U002730 >>>
<<< UNIT U002731 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:732-732 | ctx=cli.new.adapter.invalid_credential >>>
无法识别的登录信息字段名：${value}。须为 [a-z][a-z0-9_]*。
<<< END U002731 >>>
<<< UNIT U002732 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:733-733 | ctx=cli.new.adapter.invalid_feature >>>
无法识别的平台能力：${value}。写法为 support_image 或 support_image=false。
<<< END U002732 >>>
<<< UNIT U002733 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:734-734 | ctx=cli.new.adapter.invalid_field >>>
无法识别的配置项：${value}。写法为 字段名[:类型][=默认值]，类型取 str / bool / int / float / list。
<<< END U002733 >>>
<<< UNIT U002734 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:735-735 | ctx=cli.new.adapter.invalid_name >>>
适配器名须为小写字母开头的 [a-z0-9_]+，长度不超过 48，且不得含连字符（会与多实例分隔符冲突）。
<<< END U002734 >>>
<<< UNIT U002735 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:736-736 | ctx=cli.new.adapter.invalid_platform_name >>>
平台显示名须为字母开头的 [A-Za-z0-9_]+，长度不超过 48。
<<< END U002735 >>>
<<< UNIT U002736 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:737-737 | ctx=cli.new.adapter.license_option >>>
许可证标识，写入 pyproject
<<< END U002736 >>>
<<< UNIT U002737 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:738-738 | ctx=cli.new.adapter.name_argument >>>
适配器名，由小写字母、数字与下划线组成，如 my_platform
<<< END U002737 >>>
<<< UNIT U002738 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:739-739 | ctx=cli.new.adapter.name_required >>>
非交互模式必须给出适配器名：akaribot new adapter <name> --non-interactive
<<< END U002738 >>>
<<< UNIT U002739 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:740-740 | ctx=cli.new.adapter.next_steps >>>
下一步：补全 context.py 的抽象方法与 bot.py 的事件映射，再按 README 的说明安装并启用。
<<< END U002739 >>>
<<< UNIT U002740 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:741-741 | ctx=cli.new.adapter.non_interactive_option >>>
不提问，未给出的选项取默认值
<<< END U002740 >>>
<<< UNIT U002741 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:742-742 | ctx=cli.new.adapter.platform_name_option >>>
平台显示名，写入 info.py 的 platform_name，默认按适配器名转大驼峰
<<< END U002741 >>>
<<< UNIT U002742 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:743-743 | ctx=cli.new.adapter.prompt_add_credential >>>
是否添加一条登录信息字段？
<<< END U002742 >>>
<<< UNIT U002743 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:744-744 | ctx=cli.new.adapter.prompt_add_field >>>
是否添加一条配置项？
<<< END U002743 >>>
<<< UNIT U002744 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:745-745 | ctx=cli.new.adapter.prompt_author >>>
作者
<<< END U002744 >>>
<<< UNIT U002745 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:746-746 | ctx=cli.new.adapter.prompt_config >>>
是否需要配置？
<<< END U002745 >>>
<<< UNIT U002746 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:747-747 | ctx=cli.new.adapter.prompt_credential >>>
登录信息字段名（如 my_platform_token）
<<< END U002746 >>>
<<< UNIT U002747 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:748-748 | ctx=cli.new.adapter.prompt_desc >>>
适配器说明（写入 pyproject 与 README）
<<< END U002747 >>>
<<< UNIT U002748 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:749-749 | ctx=cli.new.adapter.prompt_features >>>
平台能力（逗号分隔，形如 support_image / support_quote=false，留空取默认能力集）
<<< END U002748 >>>
<<< UNIT U002749 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:750-750 | ctx=cli.new.adapter.prompt_field >>>
配置项（如 api_url:str=https://example.com）
<<< END U002749 >>>
<<< UNIT U002750 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:751-751 | ctx=cli.new.adapter.prompt_license >>>
许可证标识
<<< END U002750 >>>
<<< UNIT U002751 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:752-752 | ctx=cli.new.adapter.prompt_name >>>
适配器名
<<< END U002751 >>>
<<< UNIT U002752 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:753-753 | ctx=cli.new.adapter.prompt_platform_name >>>
平台显示名（写入 info.py 的 platform_name）
<<< END U002752 >>>
<<< UNIT U002753 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:754-754 | ctx=cli.new.adapter.target_not_empty >>>
目标目录非空：${target}。确认覆盖请加 --force。
<<< END U002753 >>>
<<< UNIT U002754 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:755-755 | ctx=cli.new.adapter.template_dir_option >>>
模板目录，默认自动定位
<<< END U002754 >>>
<<< UNIT U002755 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:756-756 | ctx=cli.new.adapter.template_missing >>>
未找到适配器模板目录（应包含 ${marker}），请用 --template-dir 或 ${env} 指定。
<<< END U002755 >>>
<<< UNIT U002756 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:757-757 | ctx=cli.ok.loaded >>>
已装载 ${module}
<<< END U002756 >>>
<<< UNIT U002757 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:758-758 | ctx=cli.ok.unloaded >>>
已卸载 ${module}
<<< END U002757 >>>
<<< UNIT U002758 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:759-759 | ctx=cli.ok.written >>>
已写入 ${table}.${name}
<<< END U002758 >>>
<<< UNIT U002759 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:760-760 | ctx=cli.run.conflict_actions >>>
一次只能选一个动作：${actions}
<<< END U002759 >>>
<<< UNIT U002760 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:761-761 | ctx=cli.run.conflict_foreground >>>
--detach 与 --foreground 互斥，后台启动不接受前台运行
<<< END U002760 >>>
<<< UNIT U002761 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:762-762 | ctx=cli.run.detached_failed >>>
实例未能启动：${detail}
<<< END U002761 >>>
<<< UNIT U002762 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:763-763 | ctx=cli.run.detached_failed_detail >>>
控制台输出见 ${log}｜${tail}
<<< END U002762 >>>
<<< UNIT U002763 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:764-764 | ctx=cli.run.detached_started >>>
实例已在后台启动（PID ${pid}），控制台输出见 ${log}
<<< END U002763 >>>
<<< UNIT U002764 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:765-765 | ctx=cli.run.help >>>
启动、停止或查看实例。等价于 python -m akaribot.core.entrypoints.run
<<< END U002764 >>>
<<< UNIT U002765 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:766-766 | ctx=cli.run.option_adapter >>>
只启动指定适配器，可多次指定。默认启动全部已配置适配器
<<< END U002765 >>>
<<< UNIT U002766 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:767-767 | ctx=cli.run.option_detach >>>
在后台启动并立即返回。进程脱离当前会话，启动它的终端退出后继续运行
<<< END U002766 >>>
<<< UNIT U002767 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:768-768 | ctx=cli.run.option_foreground >>>
前台运行（默认即为前台）
<<< END U002767 >>>
<<< UNIT U002768 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:769-769 | ctx=cli.run.option_no_auto_migrate >>>
启动时不自动应用数据库迁移
<<< END U002768 >>>
<<< UNIT U002769 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:770-770 | ctx=cli.run.option_restart >>>
先停止再后台启动
<<< END U002769 >>>
<<< UNIT U002770 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:771-771 | ctx=cli.run.option_status >>>
打印运行状态（与 --json 搭配供界面读取）
<<< END U002770 >>>
<<< UNIT U002771 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:772-772 | ctx=cli.run.option_stop >>>
停止正在运行的实例（按锁文件记录的进程号）
<<< END U002771 >>>
<<< UNIT U002772 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:773-773 | ctx=cli.run.option_timeout >>>
停止时等待进程退出的秒数
<<< END U002772 >>>
<<< UNIT U002773 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:774-774 | ctx=cli.run.state_running_detail >>>
锁被持有：${path}
<<< END U002773 >>>
<<< UNIT U002774 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:775-775 | ctx=cli.run.state_stopped_detail >>>
锁未被持有：${path}
<<< END U002774 >>>
<<< UNIT U002775 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:776-776 | ctx=cli.run.state_unmanaged_detail >>>
锁被持有但文件里没有进程记录，无法按进程号停止：${path}
<<< END U002775 >>>
<<< UNIT U002776 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:777-777 | ctx=cli.run.status_running >>>
实例在运行（PID ${pid}，启动于 ${started}）
<<< END U002776 >>>
<<< UNIT U002777 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:778-778 | ctx=cli.run.status_stopped >>>
实例未在运行（锁未被持有：${lock}）
<<< END U002777 >>>
<<< UNIT U002778 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:779-779 | ctx=cli.run.status_unmanaged >>>
实例在运行，但锁文件里没有进程记录（${lock}）
<<< END U002778 >>>
<<< UNIT U002779 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:780-780 | ctx=cli.run.stop_done >>>
实例已停止（PID ${pid}）
<<< END U002779 >>>
<<< UNIT U002780 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:781-781 | ctx=cli.run.stop_failed >>>
实例未能在超时内停止（PID ${pid}）
<<< END U002780 >>>
<<< UNIT U002781 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:782-782 | ctx=cli.run.stop_failed_detail >>>
已发送强制终止信号并等待 ${seconds} 秒。请检查该进程是否阻塞在不可中断的系统调用上
<<< END U002781 >>>
<<< UNIT U002782 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:783-783 | ctx=cli.run.stop_forced >>>
实例已被强制终止（PID ${pid}）
<<< END U002782 >>>
<<< UNIT U002783 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:784-784 | ctx=cli.run.stop_not_running >>>
实例当前未在运行
<<< END U002783 >>>
<<< UNIT U002784 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:785-785 | ctx=cli.run.stop_unmanaged >>>
无法停止：锁文件里没有进程记录
<<< END U002784 >>>
<<< UNIT U002785 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:786-786 | ctx=cli.run.stop_unmanaged_detail >>>
锁被持有（${path}）但不是本版本写入的记录，请手动结束持锁进程
<<< END U002785 >>>
<<< UNIT U002786 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:787-787 | ctx=cli.service.help >>>
将 CLI 安装为常驻服务，并由该服务守护本机实例。
<<< END U002786 >>>
<<< UNIT U002787 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:788-788 | ctx=cli.service.install.dry_run >>>
试运行：将写入 ${path}，不调用 ${tool}。
<<< END U002787 >>>
<<< UNIT U002788 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:789-789 | ctx=cli.service.install.dry_run_exists >>>
试运行：将覆盖已有的 ${path}，不调用 ${tool}。
<<< END U002788 >>>
<<< UNIT U002789 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:790-790 | ctx=cli.service.install.exists >>>
单元文件已存在：${path}。${hint}
<<< END U002789 >>>
<<< UNIT U002790 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:791-791 | ctx=cli.service.install.exists_hint >>>
确认要覆盖时重新执行并加上 --force。
<<< END U002790 >>>
<<< UNIT U002791 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:792-792 | ctx=cli.service.install.help >>>
写入系统服务单元并注册服务。
<<< END U002791 >>>
<<< UNIT U002792 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:793-793 | ctx=cli.service.install.option_force >>>
单元文件已存在时覆盖它。
<<< END U002792 >>>
<<< UNIT U002793 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:794-794 | ctx=cli.service.install.register_failed >>>
${tool} 注册失败（退出码 ${code}）：${detail}
<<< END U002793 >>>
<<< UNIT U002794 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:795-795 | ctx=cli.service.install.registered >>>
已交由 ${tool} 管理，服务会常驻守护本机实例。
<<< END U002794 >>>
<<< UNIT U002795 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:796-796 | ctx=cli.service.install.tool_missing >>>
未找到 ${tool}，单元文件 ${path} 已写入但尚未注册。
<<< END U002795 >>>
<<< UNIT U002796 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:797-797 | ctx=cli.service.install.written >>>
已写入单元文件 ${path}。
<<< END U002796 >>>
<<< UNIT U002797 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:798-798 | ctx=cli.service.option_dry_run >>>
只打印将要执行的改动，不写入磁盘也不调用系统工具。
<<< END U002797 >>>
<<< UNIT U002798 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:799-799 | ctx=cli.service.status.backend >>>
服务管理器：${backend}
<<< END U002798 >>>
<<< UNIT U002799 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:800-800 | ctx=cli.service.status.detail >>>
说明：${detail}
<<< END U002799 >>>
<<< UNIT U002800 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:801-801 | ctx=cli.service.status.enabled.no >>>
系统注册：未注册
<<< END U002800 >>>
<<< UNIT U002801 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:802-802 | ctx=cli.service.status.enabled.unknown >>>
系统注册：无法探测
<<< END U002801 >>>
<<< UNIT U002802 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:803-803 | ctx=cli.service.status.enabled.yes >>>
系统注册：已注册
<<< END U002802 >>>
<<< UNIT U002803 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:804-804 | ctx=cli.service.status.help >>>
查看服务单元是否安装、是否已注册。
<<< END U002803 >>>
<<< UNIT U002804 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:805-805 | ctx=cli.service.status.probe_failed >>>
无法执行 ${tool}，注册状态未知。
<<< END U002804 >>>
<<< UNIT U002805 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:806-806 | ctx=cli.service.status.registered >>>
已在 ${tool} 中注册。
<<< END U002805 >>>
<<< UNIT U002806 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:807-807 | ctx=cli.service.status.tool_missing >>>
未找到 ${tool}，注册状态未知。
<<< END U002806 >>>
<<< UNIT U002807 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:808-808 | ctx=cli.service.status.unit_installed >>>
单元文件：${path}（已安装）
<<< END U002807 >>>
<<< UNIT U002808 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:809-809 | ctx=cli.service.status.unit_missing >>>
单元文件：${path}（未安装）
<<< END U002808 >>>
<<< UNIT U002809 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:810-810 | ctx=cli.service.status.unregistered >>>
未在 ${tool} 中注册。
<<< END U002809 >>>
<<< UNIT U002810 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:811-811 | ctx=cli.service.supervise.abandoned >>>
实例 ${name} 已自动重启 ${count} 次，达到上限 ${max}，不再重启。
<<< END U002810 >>>
<<< UNIT U002811 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:812-812 | ctx=cli.service.supervise.bad_interval >>>
间隔必须是正数，当前为 ${seconds}。
<<< END U002811 >>>
<<< UNIT U002812 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:813-813 | ctx=cli.service.supervise.bad_policy >>>
重启上限与退避基数不能为负数。
<<< END U002812 >>>
<<< UNIT U002813 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:814-814 | ctx=cli.service.supervise.failed >>>
实例 ${name} 启动失败：${error}
<<< END U002813 >>>
<<< UNIT U002814 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:815-815 | ctx=cli.service.supervise.help >>>
守护本机实例，按注册表策略恢复、重启或跳过。
<<< END U002814 >>>
<<< UNIT U002815 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:816-816 | ctx=cli.service.supervise.missing >>>
实例 ${name} 的目录已不存在：${root}，跳过。
<<< END U002815 >>>
<<< UNIT U002816 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:817-817 | ctx=cli.service.supervise.no_autostart >>>
${name} 未开启开机自启，不恢复上次的运行状态
<<< END U002816 >>>
<<< UNIT U002817 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:818-818 | ctx=cli.service.supervise.observed >>>
实例 ${name} 正在运行（pid ${pid}）。
<<< END U002817 >>>
<<< UNIT U002818 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:819-819 | ctx=cli.service.supervise.option_backoff >>>
崩溃重启的指数退避基数秒数。
<<< END U002818 >>>
<<< UNIT U002819 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:820-820 | ctx=cli.service.supervise.option_interval >>>
两轮之间的间隔秒数。
<<< END U002819 >>>
<<< UNIT U002820 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:821-821 | ctx=cli.service.supervise.option_max_restarts >>>
单个实例允许的自动重启次数上限。
<<< END U002820 >>>
<<< UNIT U002821 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:822-822 | ctx=cli.service.supervise.option_once >>>
只运行一轮后返回，供定时任务与排查故障使用。
<<< END U002821 >>>
<<< UNIT U002822 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:823-823 | ctx=cli.service.supervise.recovered >>>
实例 ${name} 期望运行但未在运行，已启动（pid ${pid}）。
<<< END U002822 >>>
<<< UNIT U002823 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:824-824 | ctx=cli.service.supervise.refused >>>
实例 ${name} 未运行，且未开启崩溃后重启，保持不动。
<<< END U002823 >>>
<<< UNIT U002824 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:825-825 | ctx=cli.service.supervise.restarted >>>
实例 ${name} 已自动重启 ${count} 次（上限 ${max}）。
<<< END U002824 >>>
<<< UNIT U002825 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:826-826 | ctx=cli.service.supervise.start_failed >>>
实例进程 pid ${pid} 未在就绪时限内获取到锁，日志：${log}，末尾输出：${tail}
<<< END U002825 >>>
<<< UNIT U002826 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:827-827 | ctx=cli.service.supervise.stopped >>>
收到 ${signal}，守护循环已退出。
<<< END U002826 >>>
<<< UNIT U002827 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:828-828 | ctx=cli.service.supervise.stray >>>
实例 ${name} 期望停止但正在运行（pid ${pid}），不干预。
<<< END U002827 >>>
<<< UNIT U002828 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:829-829 | ctx=cli.service.supervise.summary >>>
本轮检查 ${checked} 个实例：运行 ${running}，恢复 ${started}，重启 ${restarted}，失败 ${failed}，放弃 ${abandoned}，跳过 ${skipped}。
<<< END U002828 >>>
<<< UNIT U002829 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:830-830 | ctx=cli.service.uninstall.absent >>>
单元文件 ${path} 不存在，尚未安装。
<<< END U002829 >>>
<<< UNIT U002830 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:831-831 | ctx=cli.service.uninstall.done >>>
已注销并删除单元文件 ${path}（${tool}）。
<<< END U002830 >>>
<<< UNIT U002831 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:832-832 | ctx=cli.service.uninstall.dry_run >>>
试运行：将注销并删除 ${path}，不调用 ${tool}。
<<< END U002831 >>>
<<< UNIT U002832 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:833-833 | ctx=cli.service.uninstall.help >>>
注销服务并删除单元文件。
<<< END U002832 >>>
<<< UNIT U002833 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:834-834 | ctx=cli.service.uninstall.remove_failed >>>
删除 ${path} 失败：${error}
<<< END U002833 >>>
<<< UNIT U002834 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:835-835 | ctx=cli.service.uninstall.tool_missing >>>
未找到 ${tool}，${path} 已删除但系统里的注册可能仍在。
<<< END U002834 >>>
<<< UNIT U002835 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:836-836 | ctx=cli.service.uninstall.unregister_failed >>>
${tool} 注销失败（退出码 ${code}）：${detail}
<<< END U002835 >>>
<<< UNIT U002836 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:837-837 | ctx=cli.service.unit.description >>>
AkariBot 实例守护服务
<<< END U002836 >>>
<<< UNIT U002837 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:838-838 | ctx=cli.service.unsupported >>>
当前平台 ${platform} 尚未支持服务托管。已实现的后端为 ${backends}。
<<< END U002837 >>>
<<< UNIT U002838 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:839-839 | ctx=cli.service.unsupported_hint >>>
请在受支持的平台上安装，或自行把 `akaribot service supervise` 交给本机的服务管理器。
<<< END U002838 >>>
<<< UNIT U002839 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:840-840 | ctx=cli.test.arg_path >>>
要运行的测试路径，默认运行全部
<<< END U002839 >>>
<<< UNIT U002840 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:841-841 | ctx=cli.test.help >>>
运行测试（等价于 python -m akaribot.testing）
<<< END U002840 >>>
<<< UNIT U002841 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:842-842 | ctx=cli.test.option_case >>>
只运行指定用例，可重复
<<< END U002841 >>>
<<< UNIT U002842 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:843-843 | ctx=cli.test.option_ci >>>
CI 模式（非交互、失败即退出）
<<< END U002842 >>>
<<< UNIT U002843 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:844-844 | ctx=cli.test.option_coverage >>>
统计覆盖率
<<< END U002843 >>>
<<< UNIT U002844 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:845-845 | ctx=cli.test.probe_failed >>>
无法在实例里探测测试框架：${error}
<<< END U002844 >>>
<<< UNIT U002845 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:846-846 | ctx=cli.test.testing_missing >>>
实例里没有测试框架（${dist}）。它是开发阶段依赖，`akaribot init` 默认不安装。请运行 `akaribot module add ${dist}` 安装后重试。
<<< END U002845 >>>
<<< UNIT U002846 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:847-847 | ctx=cli.tui.adapters.action_add_instance >>>
新增实例
<<< END U002846 >>>
<<< UNIT U002847 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:848-848 | ctx=cli.tui.adapters.action_disable >>>
停用
<<< END U002847 >>>
<<< UNIT U002848 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:849-849 | ctx=cli.tui.adapters.action_enable >>>
启用
<<< END U002848 >>>
<<< UNIT U002849 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:850-850 | ctx=cli.tui.adapters.action_install >>>
安装
<<< END U002849 >>>
<<< UNIT U002850 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:851-851 | ctx=cli.tui.adapters.action_install_adapter >>>
安装适配器
<<< END U002850 >>>
<<< UNIT U002851 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:852-852 | ctx=cli.tui.adapters.action_refresh >>>
刷新
<<< END U002851 >>>
<<< UNIT U002852 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:853-853 | ctx=cli.tui.adapters.action_remove_instance >>>
移除实例
<<< END U002852 >>>
<<< UNIT U002853 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:854-854 | ctx=cli.tui.adapters.action_toggle >>>
切换启用状态
<<< END U002853 >>>
<<< UNIT U002854 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:855-855 | ctx=cli.tui.adapters.add_cancelled >>>
已取消新增实例
<<< END U002854 >>>
<<< UNIT U002855 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:856-856 | ctx=cli.tui.adapters.add_confirm >>>
创建
<<< END U002855 >>>
<<< UNIT U002856 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:857-857 | ctx=cli.tui.adapters.add_hint >>>
选择已安装的适配器并填写实例 ID。实例 ID 用于关联数据，创建后不可更改。新实例的配置默认未启用，填写登录信息后再启用。
<<< END U002856 >>>
<<< UNIT U002857 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:858-858 | ctx=cli.tui.adapters.add_no_installed >>>
尚无已安装的适配器，请先安装适配器包
<<< END U002857 >>>
<<< UNIT U002858 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:859-859 | ctx=cli.tui.adapters.add_option >>>
${platform}（已有：${instances}）
<<< END U002858 >>>
<<< UNIT U002859 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:860-860 | ctx=cli.tui.adapters.add_option_empty >>>
${platform}（尚无实例）
<<< END U002859 >>>
<<< UNIT U002860 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:861-861 | ctx=cli.tui.adapters.add_title >>>
新增适配器实例
<<< END U002860 >>>
<<< UNIT U002861 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:862-862 | ctx=cli.tui.adapters.available_failed >>>
（可安装清单读取失败：${error}）
<<< END U002861 >>>
<<< UNIT U002862 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:863-863 | ctx=cli.tui.adapters.bind_add_instance >>>
新增实例
<<< END U002862 >>>
<<< UNIT U002863 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:864-864 | ctx=cli.tui.adapters.bind_remove_instance >>>
移除实例
<<< END U002863 >>>
<<< UNIT U002864 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:865-865 | ctx=cli.tui.adapters.bind_toggle_enable >>>
启用 / 停用
<<< END U002864 >>>
<<< UNIT U002865 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:866-866 | ctx=cli.tui.adapters.busy >>>
正在更改启用状态
<<< END U002865 >>>
<<< UNIT U002866 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:867-867 | ctx=cli.tui.adapters.calling >>>
正在${label}…
<<< END U002866 >>>
<<< UNIT U002867 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:868-868 | ctx=cli.tui.adapters.cancel >>>
取消
<<< END U002867 >>>
<<< UNIT U002868 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:869-869 | ctx=cli.tui.adapters.column_error >>>
最近错误
<<< END U002868 >>>
<<< UNIT U002869 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:870-870 | ctx=cli.tui.adapters.column_instance >>>
实例
<<< END U002869 >>>
<<< UNIT U002870 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:871-871 | ctx=cli.tui.adapters.column_listen >>>
监听地址
<<< END U002870 >>>
<<< UNIT U002871 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:872-872 | ctx=cli.tui.adapters.column_status >>>
连接
<<< END U002871 >>>
<<< UNIT U002872 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:873-873 | ctx=cli.tui.adapters.config_form_empty >>>
实例 ${name} 已创建，没有需要填写的配置项。
<<< END U002872 >>>
<<< UNIT U002873 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:874-874 | ctx=cli.tui.adapters.config_form_hint >>>
实例已创建，默认未启用。标记“待填写”的项留空时不写入，其余项已带默认值。回车移到下一项，也可稍后到配置页按 r 刷新再填写。
<<< END U002873 >>>
<<< UNIT U002874 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:875-875 | ctx=cli.tui.adapters.config_form_loading >>>
正在读取 ${name} 的配置项…
<<< END U002874 >>>
<<< UNIT U002875 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:876-876 | ctx=cli.tui.adapters.config_form_saved >>>
实例 ${name} 已写入 ${count} 项配置
<<< END U002875 >>>
<<< UNIT U002876 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:877-877 | ctx=cli.tui.adapters.config_form_skipped >>>
实例 ${name} 已创建，配置未填写。可在配置页按 r 刷新后填写
<<< END U002876 >>>
<<< UNIT U002877 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:878-878 | ctx=cli.tui.adapters.config_form_title >>>
填写实例配置：${name}
<<< END U002877 >>>
<<< UNIT U002878 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:879-879 | ctx=cli.tui.adapters.config_form_unavailable >>>
实例 ${name} 已创建，但无法读取配置项：${error}。可在配置页按 r 刷新后填写
<<< END U002878 >>>
<<< UNIT U002879 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:880-880 | ctx=cli.tui.adapters.default_id >>>
（默认）
<<< END U002879 >>>
<<< UNIT U002880 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:881-881 | ctx=cli.tui.adapters.detail_client_name_inferred >>>
client_name 为推断值
<<< END U002880 >>>
<<< UNIT U002881 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:882-882 | ctx=cli.tui.adapters.detail_config >>>
配置：${table}  ${file}
<<< END U002881 >>>
<<< UNIT U002882 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:883-883 | ctx=cli.tui.adapters.detail_developers >>>
作者：${names}
<<< END U002882 >>>
<<< UNIT U002883 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:884-884 | ctx=cli.tui.adapters.detail_empty >>>
暂无实例配置
<<< END U002883 >>>
<<< UNIT U002884 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:885-885 | ctx=cli.tui.adapters.detail_hint >>>
选择实例查看配置与状态
<<< END U002884 >>>
<<< UNIT U002885 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:886-886 | ctx=cli.tui.adapters.detail_install_hint >>>
按 i 或点击“安装”安装适配器包
<<< END U002885 >>>
<<< UNIT U002886 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:887-887 | ctx=cli.tui.adapters.detail_legacy_layout >>>
配置采用扁平布局
<<< END U002886 >>>
<<< UNIT U002887 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:888-888 | ctx=cli.tui.adapters.detail_not_installed >>>
${platform} 的适配器包尚未安装
<<< END U002887 >>>
<<< UNIT U002888 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:889-889 | ctx=cli.tui.adapters.detail_placeholder >>>
选择实例查看配置与状态
<<< END U002888 >>>
<<< UNIT U002889 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:890-890 | ctx=cli.tui.adapters.detail_status >>>
状态：${label}（peer ${state}）
<<< END U002889 >>>
<<< UNIT U002890 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:892-892 | ctx=cli.tui.adapters.enable_missing >>>
缺失
<<< END U002890 >>>
<<< UNIT U002891 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:893-893 | ctx=cli.tui.adapters.enable_off >>>
关
<<< END U002891 >>>
<<< UNIT U002892 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:894-894 | ctx=cli.tui.adapters.enable_on >>>
开
<<< END U002892 >>>
<<< UNIT U002893 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:896-896 | ctx=cli.tui.adapters.group_not_installed >>>
适配器未安装
<<< END U002893 >>>
<<< UNIT U002894 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:897-897 | ctx=cli.tui.adapters.group_registry_unavailable >>>
已安装清单不可用
<<< END U002894 >>>
<<< UNIT U002895 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:899-899 | ctx=cli.tui.adapters.install_cancelled >>>
已取消安装适配器
<<< END U002895 >>>
<<< UNIT U002896 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:900-900 | ctx=cli.tui.adapters.install_hint >>>
列表只含尚未安装的适配器。安装后适配器出现在实例列表中，再新增实例并填写登录信息。
<<< END U002896 >>>
<<< UNIT U002897 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:901-901 | ctx=cli.tui.adapters.install_none >>>
没有可安装的适配器
<<< END U002897 >>>
<<< UNIT U002898 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:902-902 | ctx=cli.tui.adapters.install_option >>>
${platform}（作者：${names}）
<<< END U002898 >>>
<<< UNIT U002899 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:903-903 | ctx=cli.tui.adapters.install_title >>>
安装适配器
<<< END U002899 >>>
<<< UNIT U002900 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:904-904 | ctx=cli.tui.adapters.instance_id_exists >>>
${platform} 已有实例 ${instance_id}，请换一个实例 ID
<<< END U002900 >>>
<<< UNIT U002901 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:905-905 | ctx=cli.tui.adapters.instance_id_invalid >>>
实例 ID 仅限小写字母、数字与下划线，长度不超过 24 个字符：${instance_id}
<<< END U002901 >>>
<<< UNIT U002902 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:906-906 | ctx=cli.tui.adapters.instance_id_required >>>
请输入实例 ID。实例 ID 用于关联数据，创建后不可更改。
<<< END U002902 >>>
<<< UNIT U002903 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:907-907 | ctx=cli.tui.adapters.instance_placeholder >>>
实例 ID（小写字母、数字、下划线）
<<< END U002903 >>>
<<< UNIT U002904 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:908-908 | ctx=cli.tui.adapters.label_disable >>>
停用 ${name}
<<< END U002904 >>>
<<< UNIT U002905 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:909-909 | ctx=cli.tui.adapters.label_enable >>>
启用 ${name}
<<< END U002905 >>>
<<< UNIT U002906 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:910-910 | ctx=cli.tui.adapters.label_install >>>
安装 ${name} 适配器
<<< END U002906 >>>
<<< UNIT U002907 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:911-911 | ctx=cli.tui.adapters.label_instance_add >>>
新增实例 ${name}
<<< END U002907 >>>
<<< UNIT U002908 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:912-912 | ctx=cli.tui.adapters.label_instance_remove >>>
移除实例 ${name}
<<< END U002908 >>>
<<< UNIT U002909 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:913-913 | ctx=cli.tui.adapters.note_enable_missing >>>
配置缺少 enable 键，按未启用处理
<<< END U002909 >>>
<<< UNIT U002910 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:914-914 | ctx=cli.tui.adapters.offline >>>
离线
<<< END U002910 >>>
<<< UNIT U002911 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:915-915 | ctx=cli.tui.adapters.online >>>
在线
<<< END U002911 >>>
<<< UNIT U002912 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:916-916 | ctx=cli.tui.adapters.path_unknown >>>
路径未知
<<< END U002912 >>>
<<< UNIT U002913 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:917-917 | ctx=cli.tui.adapters.peer_count >>>
peer 记录 ${count} 条
<<< END U002913 >>>
<<< UNIT U002914 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:918-918 | ctx=cli.tui.adapters.peer_entrypoint_unavailable >>>
core 的 ${entry} 入口不可用（`${cmd}` 退出码 ${code}：${tail}）
<<< END U002914 >>>
<<< UNIT U002915 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:919-919 | ctx=cli.tui.adapters.peer_lease_expired >>>
peer 租约已过期
<<< END U002915 >>>
<<< UNIT U002916 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:920-920 | ctx=cli.tui.adapters.peer_missing >>>
peer 快照中无此实例
<<< END U002916 >>>
<<< UNIT U002917 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:921-921 | ctx=cli.tui.adapters.peer_missing_field >>>
peer 快照缺少有效的 ${field} 字段
<<< END U002917 >>>
<<< UNIT U002918 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:922-922 | ctx=cli.tui.adapters.peer_no_lease >>>
peer 记录缺少 lease_until，无法判断在线状态
<<< END U002918 >>>
<<< UNIT U002919 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:923-923 | ctx=cli.tui.adapters.peer_no_record >>>
无记录
<<< END U002919 >>>
<<< UNIT U002920 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:924-924 | ctx=cli.tui.adapters.peer_no_state >>>
peer 记录缺少 state
<<< END U002920 >>>
<<< UNIT U002921 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:925-925 | ctx=cli.tui.adapters.peer_not_object >>>
peer 快照不是 JSON 对象
<<< END U002921 >>>
<<< UNIT U002922 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:926-926 | ctx=cli.tui.adapters.peer_state >>>
peer 状态：${state}
<<< END U002922 >>>
<<< UNIT U002923 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:927-927 | ctx=cli.tui.adapters.peer_status_unknown >>>
连接状态未知：${note}
<<< END U002923 >>>
<<< UNIT U002924 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:928-928 | ctx=cli.tui.adapters.peer_status_unknown_hint >>>
启动实例后按 r 刷新。也可执行 `akaribot run` 或检查 AKARI_INSTANCE_DIR 指向的实例目录。
<<< END U002924 >>>
<<< UNIT U002925 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:929-929 | ctx=cli.tui.adapters.peer_unavailable >>>
peer 快照不可用
<<< END U002925 >>>
<<< UNIT U002926 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:930-930 | ctx=cli.tui.adapters.pick_instance >>>
请选择已有配置的实例
<<< END U002926 >>>
<<< UNIT U002927 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:931-931 | ctx=cli.tui.adapters.pick_toggle >>>
请选择适配器实例，分组标题不支持此操作
<<< END U002927 >>>
<<< UNIT U002928 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:932-932 | ctx=cli.tui.adapters.reason_unknown >>>
原因未知
<<< END U002928 >>>
<<< UNIT U002929 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:933-933 | ctx=cli.tui.adapters.refreshing >>>
${message}，正在刷新…
<<< END U002929 >>>
<<< UNIT U002930 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:934-934 | ctx=cli.tui.adapters.remove_cancelled >>>
已取消移除实例
<<< END U002930 >>>
<<< UNIT U002931 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:935-935 | ctx=cli.tui.adapters.remove_choice_plain >>>
移除配置
<<< END U002931 >>>
<<< UNIT U002932 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:936-936 | ctx=cli.tui.adapters.remove_choice_title >>>
确认移除适配器实例 ${name}
<<< END U002932 >>>
<<< UNIT U002933 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:937-937 | ctx=cli.tui.adapters.remove_kept >>>
已移除 ${name} 的配置，场景与用户数据保留。
<<< END U002933 >>>
<<< UNIT U002934 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:938-938 | ctx=cli.tui.adapters.remove_only_hint >>>
将移除 ${name} 的配置，场景与用户数据保留。
<<< END U002934 >>>
<<< UNIT U002935 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:939-939 | ctx=cli.tui.adapters.src_bad_json >>>
`${label}` 输出无法解析为 JSON：${error}
<<< END U002935 >>>
<<< UNIT U002936 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:940-940 | ctx=cli.tui.adapters.src_empty_output >>>
`${label}` 未返回内容
<<< END U002936 >>>
<<< UNIT U002937 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:941-941 | ctx=cli.tui.adapters.src_exe_missing >>>
未找到可执行文件：${path}（${error}）
<<< END U002937 >>>
<<< UNIT U002938 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:942-942 | ctx=cli.tui.adapters.src_exit_code >>>
`${cmd}` 退出码 ${code}：${tail}
<<< END U002938 >>>
<<< UNIT U002939 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:943-943 | ctx=cli.tui.adapters.src_instance_missing >>>
akaribot.cli.instance 不可用，无法定位实例解释器
<<< END U002939 >>>
<<< UNIT U002940 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:944-944 | ctx=cli.tui.adapters.src_not_instance >>>
${root} 不是 AkariBot 实例（未找到 akaribot.toml）
<<< END U002940 >>>
<<< UNIT U002941 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:945-945 | ctx=cli.tui.adapters.src_oserror >>>
`${cmd}` 执行失败：${error}
<<< END U002941 >>>
<<< UNIT U002942 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:946-946 | ctx=cli.tui.adapters.src_timeout >>>
`${cmd}` 执行超时（${seconds} 秒）
<<< END U002942 >>>
<<< UNIT U002943 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:947-947 | ctx=cli.tui.adapters.state_not_installed >>>
未安装
<<< END U002943 >>>
<<< UNIT U002944 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:948-948 | ctx=cli.tui.adapters.status_cached >>>
使用 ${age} 秒前的缓存，共 ${count} 个实例
<<< END U002944 >>>
<<< UNIT U002945 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:949-949 | ctx=cli.tui.adapters.status_load_failed >>>
读取失败：${error}
<<< END U002945 >>>
<<< UNIT U002946 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:950-950 | ctx=cli.tui.adapters.status_loaded >>>
已读取 ${count} 个实例
<<< END U002946 >>>
<<< UNIT U002947 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:951-951 | ctx=cli.tui.adapters.status_loading >>>
正在读取适配器实例…
<<< END U002947 >>>
<<< UNIT U002948 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:952-952 | ctx=cli.tui.adapters.stub_install_ok >>>
安装成功
<<< END U002948 >>>
<<< UNIT U002949 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:953-953 | ctx=cli.tui.adapters.stub_instance_ok >>>
实例配置已更改
<<< END U002949 >>>
<<< UNIT U002950 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:954-954 | ctx=cli.tui.adapters.stub_no_peers >>>
模拟数据源未提供 peer 快照
<<< END U002950 >>>
<<< UNIT U002951 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:955-955 | ctx=cli.tui.adapters.stub_toggle_ok >>>
启用状态已更改
<<< END U002951 >>>
<<< UNIT U002952 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:956-956 | ctx=cli.tui.adapters.summary_counts >>>
实例 ${total} 个，已启用 ${enabled} 个，平台 ${platforms} 个
<<< END U002952 >>>
<<< UNIT U002953 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:957-957 | ctx=cli.tui.adapters.summary_inferred_client_name >>>
registry 未提供 platform_name，client_name 按平台名推断
<<< END U002953 >>>
<<< UNIT U002954 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:958-958 | ctx=cli.tui.adapters.summary_installable >>>
未安装平台 ${count} 个，按 i 安装
<<< END U002954 >>>
<<< UNIT U002955 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:959-959 | ctx=cli.tui.adapters.summary_legacy_layout >>>
含扁平布局配置 config/bot_*.toml
<<< END U002955 >>>
<<< UNIT U002956 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:960-960 | ctx=cli.tui.adapters.summary_pending >>>
尚未读取适配器实例
<<< END U002956 >>>
<<< UNIT U002957 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:961-961 | ctx=cli.tui.adapters.summary_registry_unavailable >>>
已安装清单不可用：${note}
<<< END U002957 >>>
<<< UNIT U002958 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:962-962 | ctx=cli.tui.adapters.summary_root >>>
实例目录：${root}
<<< END U002958 >>>
<<< UNIT U002959 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:963-963 | ctx=cli.tui.app.bind_fold_group >>>
折叠分组
<<< END U002959 >>>
<<< UNIT U002960 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:964-964 | ctx=cli.tui.app.bind_help >>>
快捷键
<<< END U002960 >>>
<<< UNIT U002961 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:965-965 | ctx=cli.tui.app.bind_next_page >>>
下一页
<<< END U002961 >>>
<<< UNIT U002962 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:966-966 | ctx=cli.tui.app.bind_previous_page >>>
上一页
<<< END U002962 >>>
<<< UNIT U002963 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:967-967 | ctx=cli.tui.app.bind_quit >>>
退出
<<< END U002963 >>>
<<< UNIT U002964 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:968-968 | ctx=cli.tui.app.bind_toggle_theme >>>
切换主题
<<< END U002964 >>>
<<< UNIT U002965 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:969-969 | ctx=cli.tui.app.bind_unfold_group >>>
展开分组
<<< END U002965 >>>
<<< UNIT U002966 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:970-970 | ctx=cli.tui.app.boot_note_title >>>
启动信息
<<< END U002966 >>>
<<< UNIT U002967 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:971-971 | ctx=cli.tui.app.help_close >>>
关闭
<<< END U002967 >>>
<<< UNIT U002968 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:972-972 | ctx=cli.tui.app.help_nav >>>
↑/↓ 选择页面，Enter 打开页面或折叠分组，←/→ 折叠或展开分组，? 打开帮助，Esc 取消或返回，q 退出，Ctrl+←/→ 切换页面。
<<< END U002968 >>>
<<< UNIT U002969 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:973-973 | ctx=cli.tui.app.help_purpose >>>
本页用途：${purpose}
<<< END U002969 >>>
<<< UNIT U002970 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:974-974 | ctx=cli.tui.app.help_title >>>
${page}：快捷键
<<< END U002970 >>>
<<< UNIT U002971 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:975-975 | ctx=cli.tui.app.instance_unknown >>>
未定位实例
<<< END U002971 >>>
<<< UNIT U002972 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:976-976 | ctx=cli.tui.app.quit_busy_cancel >>>
等待完成
<<< END U002972 >>>
<<< UNIT U002973 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:977-977 | ctx=cli.tui.app.quit_busy_confirm >>>
立即退出
<<< END U002973 >>>
<<< UNIT U002974 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:978-978 | ctx=cli.tui.app.quit_busy_hint >>>
后台任务仍在运行：${actions}。退出后将无法继续查看执行进度。
<<< END U002974 >>>
<<< UNIT U002975 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:979-979 | ctx=cli.tui.app.quit_busy_title >>>
确认退出
<<< END U002975 >>>
<<< UNIT U002976 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:980-980 | ctx=cli.tui.app.quit_dirty_cancel >>>
返回编辑
<<< END U002976 >>>
<<< UNIT U002977 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:981-981 | ctx=cli.tui.app.quit_dirty_confirm >>>
放弃更改并退出
<<< END U002977 >>>
<<< UNIT U002978 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:982-982 | ctx=cli.tui.app.quit_dirty_hint >>>
以下更改尚未保存，退出后将丢失：
${notes}
<<< END U002978 >>>
<<< UNIT U002979 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:983-983 | ctx=cli.tui.app.run_summary >>>
启动 ${startup} ms，首帧 ${first_paint} ms，共运行 ${total} ms，退出码 ${exit_code}
<<< END U002979 >>>
<<< UNIT U002980 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:984-984 | ctx=cli.tui.app.subtitle >>>
实例管理
<<< END U002980 >>>
<<< UNIT U002981 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:985-985 | ctx=cli.tui.app.subtitle_with_instance >>>
实例管理｜${name}
<<< END U002981 >>>
<<< UNIT U002982 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:986-986 | ctx=cli.tui.app.switch_dirty_cancel >>>
留在当前实例
<<< END U002982 >>>
<<< UNIT U002983 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:987-987 | ctx=cli.tui.app.switch_dirty_confirm >>>
放弃更改并切换
<<< END U002983 >>>
<<< UNIT U002984 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:988-988 | ctx=cli.tui.app.switch_dirty_hint >>>
以下页面存在未保存更改：${notes}。切换实例后这些更改将丢失。
<<< END U002984 >>>
<<< UNIT U002985 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:989-989 | ctx=cli.tui.app.switch_dirty_title >>>
确认切换实例
<<< END U002985 >>>
<<< UNIT U002986 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:990-990 | ctx=cli.tui.app.theme_dark >>>
深色
<<< END U002986 >>>
<<< UNIT U002987 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:991-991 | ctx=cli.tui.app.theme_light >>>
浅色
<<< END U002987 >>>
<<< UNIT U002988 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:992-992 | ctx=cli.tui.app.theme_switched >>>
已切换为${name}主题
<<< END U002988 >>>
<<< UNIT U002989 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:994-994 | ctx=cli.tui.app.worker_unnamed >>>
未命名任务
<<< END U002989 >>>
<<< UNIT U002990 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:995-995 | ctx=cli.tui.common.busy_title >>>
操作进行中
<<< END U002990 >>>
<<< UNIT U002991 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:997-997 | ctx=cli.tui.common.failed_label >>>
${label}失败
<<< END U002991 >>>
<<< UNIT U002992 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:999-999 | ctx=cli.tui.common.no_output >>>
无输出
<<< END U002992 >>>
<<< UNIT U002993 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1000-1000 | ctx=cli.tui.common.none >>>
无
<<< END U002993 >>>
<<< UNIT U002994 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1001-1001 | ctx=cli.tui.common.op_failed >>>
${label}失败（退出码 ${code}）
<<< END U002994 >>>
<<< UNIT U002995 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1002-1002 | ctx=cli.tui.common.op_ok >>>
${label}成功
<<< END U002995 >>>
<<< UNIT U002996 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1003-1003 | ctx=cli.tui.common.status_ready >>>
就绪
<<< END U002996 >>>
<<< UNIT U002997 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1004-1004 | ctx=cli.tui.common.undeclared >>>
未声明
<<< END U002997 >>>
<<< UNIT U002998 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1005-1005 | ctx=cli.tui.common.unknown >>>
未知
<<< END U002998 >>>
<<< UNIT U002999 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1006-1006 | ctx=cli.tui.config.action_focus_tables >>>
表清单
<<< END U002999 >>>
<<< UNIT U003000 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1007-1007 | ctx=cli.tui.config.action_mode_form >>>
表单模式
<<< END U003000 >>>
<<< UNIT U003001 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1008-1008 | ctx=cli.tui.config.action_mode_raw >>>
原始文本
<<< END U003001 >>>
<<< UNIT U003002 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1009-1009 | ctx=cli.tui.config.action_open_editor >>>
打开编辑器
<<< END U003002 >>>
<<< UNIT U003003 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1010-1010 | ctx=cli.tui.config.action_reload >>>
刷新
<<< END U003003 >>>
<<< UNIT U003004 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1011-1011 | ctx=cli.tui.config.action_save >>>
保存
<<< END U003004 >>>
<<< UNIT U003005 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1012-1012 | ctx=cli.tui.config.bool_hint >>>
切换后点击“保存”或按 Ctrl+S 写入 true / false
<<< END U003005 >>>
<<< UNIT U003006 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1013-1013 | ctx=cli.tui.config.bool_off >>>
✗ 关
<<< END U003006 >>>
<<< UNIT U003007 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1014-1014 | ctx=cli.tui.config.bool_on >>>
✓ 开
<<< END U003007 >>>
<<< UNIT U003008 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1015-1015 | ctx=cli.tui.config.caption_no_selection >>>
共 ${total} 张配置表，未选中任何表
<<< END U003008 >>>
<<< UNIT U003009 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1016-1016 | ctx=cli.tui.config.caption_table >>>
表 ${table}：共 ${total} 项，密钥 ${secrets} 项，待填写 ${placeholders} 项，模式：${mode}
<<< END U003009 >>>
<<< UNIT U003010 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1017-1017 | ctx=cli.tui.config.caption_unloaded >>>
尚未读取配置表
<<< END U003010 >>>
<<< UNIT U003011 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1018-1018 | ctx=cli.tui.config.default_value >>>
默认值：${value}
<<< END U003011 >>>
<<< UNIT U003012 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1019-1019 | ctx=cli.tui.config.dirty_discard >>>
放弃更改
<<< END U003012 >>>
<<< UNIT U003013 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1020-1020 | ctx=cli.tui.config.dirty_hint >>>
表 ${table} 有未保存的更改，继续将放弃这些更改。
<<< END U003013 >>>
<<< UNIT U003014 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1021-1021 | ctx=cli.tui.config.dirty_keep >>>
保留更改
<<< END U003014 >>>
<<< UNIT U003015 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1022-1022 | ctx=cli.tui.config.dirty_kept >>>
已保留未保存的更改
<<< END U003015 >>>
<<< UNIT U003016 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1023-1023 | ctx=cli.tui.config.dirty_note >>>
配置页：表 ${table} 有未保存的更改
<<< END U003016 >>>
<<< UNIT U003017 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1024-1024 | ctx=cli.tui.config.dirty_title >>>
确认放弃未保存的更改
<<< END U003017 >>>
<<< UNIT U003018 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1025-1025 | ctx=cli.tui.config.editor_noninteractive >>>
当前终端不支持交互编辑。文件：${path}。可在其他终端运行 ${command}
<<< END U003018 >>>
<<< UNIT U003019 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1026-1026 | ctx=cli.tui.config.empty_value >>>
空值
<<< END U003019 >>>
<<< UNIT U003020 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1027-1027 | ctx=cli.tui.config.err_bad_json >>>
`${label}` 输出无法解析为 JSON：${error}
<<< END U003020 >>>
<<< UNIT U003021 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1028-1028 | ctx=cli.tui.config.err_boolean >>>
布尔值仅支持 true 或 false：${value}
<<< END U003021 >>>
<<< UNIT U003022 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1029-1029 | ctx=cli.tui.config.err_cmd_exit >>>
`${cmd}` 退出码 ${code}：${tail}
<<< END U003022 >>>
<<< UNIT U003023 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1030-1030 | ctx=cli.tui.config.err_core_call >>>
调用 core 的 `${label}` 失败：${kind}：${error}
<<< END U003023 >>>
<<< UNIT U003024 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1031-1031 | ctx=cli.tui.config.err_core_write >>>
调用 core 写入 ${section}.${name} 失败：${kind}：${error}
<<< END U003024 >>>
<<< UNIT U003025 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1032-1032 | ctx=cli.tui.config.err_empty_output >>>
`${label}` 未返回内容
<<< END U003025 >>>
<<< UNIT U003026 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1034-1034 | ctx=cli.tui.config.err_exe_missing >>>
未找到可执行文件：${path}（${error}）
<<< END U003026 >>>
<<< UNIT U003027 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1035-1035 | ctx=cli.tui.config.err_exec_failed >>>
`${cmd}` 执行失败：${error}
<<< END U003027 >>>
<<< UNIT U003028 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1037-1037 | ctx=cli.tui.config.err_instance_failed >>>
构造 Instance 失败：${kind}：${error}
<<< END U003028 >>>
<<< UNIT U003029 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1038-1038 | ctx=cli.tui.config.err_instance_module >>>
akaribot.cli.instance 不可用，无法读取配置
<<< END U003029 >>>
<<< UNIT U003030 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1039-1039 | ctx=cli.tui.config.err_integer >>>
整数格式无效：${value}
<<< END U003030 >>>
<<< UNIT U003031 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1040-1040 | ctx=cli.tui.config.err_nested_field >>>
该字段为嵌套结构，表单模式不支持写入，请使用 `akaribot config open` 编辑
<<< END U003031 >>>
<<< UNIT U003032 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1041-1041 | ctx=cli.tui.config.err_no_config_dir >>>
目录不存在：${path}，无法读取配置表列表
<<< END U003032 >>>
<<< UNIT U003033 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1042-1042 | ctx=cli.tui.config.err_no_instance_hint >>>
${root} 不是 AkariBot 实例（未找到 akaribot.toml）。请运行 `akaribot init`，或通过 AKARI_INSTANCE_DIR 指定实例根目录
<<< END U003033 >>>
<<< UNIT U003034 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1043-1043 | ctx=cli.tui.config.err_not_instance >>>
${root} 不是 AkariBot 实例（未找到 akaribot.toml）
<<< END U003034 >>>
<<< UNIT U003035 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1044-1044 | ctx=cli.tui.config.err_number >>>
数值格式无效：${value}
<<< END U003035 >>>
<<< UNIT U003036 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1045-1045 | ctx=cli.tui.config.err_read_file >>>
读取 ${path} 失败：${error}
<<< END U003036 >>>
<<< UNIT U003037 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1046-1046 | ctx=cli.tui.config.err_timeout >>>
`${cmd}` 执行超时（${seconds} 秒）
<<< END U003037 >>>
<<< UNIT U003038 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1047-1047 | ctx=cli.tui.config.err_write_exit >>>
写入 ${section}.${name} 失败（退出码 ${code}）
<<< END U003038 >>>
<<< UNIT U003039 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1048-1048 | ctx=cli.tui.config.err_write_failed >>>
写入 ${label} 失败
<<< END U003039 >>>
<<< UNIT U003040 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1049-1049 | ctx=cli.tui.config.error_position >>>
第 ${line} 行第 ${column} 列
<<< END U003040 >>>
<<< UNIT U003041 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1050-1050 | ctx=cli.tui.config.error_position_unknown >>>
无法定位行列
<<< END U003041 >>>
<<< UNIT U003042 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1051-1051 | ctx=cli.tui.config.error_snippet >>>
，行内容：${content}
<<< END U003042 >>>
<<< UNIT U003043 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1052-1052 | ctx=cli.tui.config.error_toml >>>
TOML 解析失败（${where}）：${reason}${snippet}
<<< END U003043 >>>
<<< UNIT U003044 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1053-1053 | ctx=cli.tui.config.error_toml_generic >>>
TOML 解析失败：${kind}：${error}
<<< END U003044 >>>
<<< UNIT U003045 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1054-1054 | ctx=cli.tui.config.form_discard_cancel >>>
继续填写
<<< END U003045 >>>
<<< UNIT U003046 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1055-1055 | ctx=cli.tui.config.form_discard_confirm >>>
放弃未保存的内容
<<< END U003046 >>>
<<< UNIT U003047 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1056-1056 | ctx=cli.tui.config.form_discard_hint >>>
已填写的内容尚未写入，关闭后将丢失。
<<< END U003047 >>>
<<< UNIT U003048 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1057-1057 | ctx=cli.tui.config.form_discard_title >>>
放弃未保存的内容？
<<< END U003048 >>>
<<< UNIT U003049 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1058-1058 | ctx=cli.tui.config.form_failed >>>
${name} 写入失败，已写入 ${count} 项。修正后可重新保存
<<< END U003049 >>>
<<< UNIT U003050 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1059-1059 | ctx=cli.tui.config.form_hint_loading >>>
正在读取配置表…
<<< END U003050 >>>
<<< UNIT U003051 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1060-1060 | ctx=cli.tui.config.form_invalid >>>
${count} 项未通过校验，未写入任何内容
<<< END U003051 >>>
<<< UNIT U003052 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1061-1061 | ctx=cli.tui.config.form_later >>>
稍后填写
<<< END U003052 >>>
<<< UNIT U003053 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1062-1062 | ctx=cli.tui.config.form_saving >>>
正在写入 ${count} 项配置…
<<< END U003053 >>>
<<< UNIT U003054 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1063-1063 | ctx=cli.tui.config.form_write_failed >>>
${name} 写入失败
<<< END U003054 >>>
<<< UNIT U003055 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1064-1064 | ctx=cli.tui.config.help_hint >>>
按字段说明填写配置，点击“保存”或按 Ctrl+S 保存更改。
<<< END U003055 >>>
<<< UNIT U003056 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1065-1065 | ctx=cli.tui.config.hint_load_tables_failed >>>
读取配置表失败：${error}
<<< END U003056 >>>
<<< UNIT U003057 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1066-1066 | ctx=cli.tui.config.hint_no_selection >>>
未选中配置表
<<< END U003057 >>>
<<< UNIT U003058 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1067-1067 | ctx=cli.tui.config.hint_no_tables >>>
实例中没有配置表，请运行 `akaribot init` 或安装模块
<<< END U003058 >>>
<<< UNIT U003059 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1068-1068 | ctx=cli.tui.config.hint_table_empty >>>
该表没有配置项
<<< END U003059 >>>
<<< UNIT U003060 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1069-1069 | ctx=cli.tui.config.hint_table_fields_failed >>>
读取表 ${table} 的字段失败：${error}
<<< END U003060 >>>
<<< UNIT U003061 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1070-1070 | ctx=cli.tui.config.kind_bool >>>
布尔
<<< END U003061 >>>
<<< UNIT U003062 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1071-1071 | ctx=cli.tui.config.kind_float >>>
数值
<<< END U003062 >>>
<<< UNIT U003063 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1072-1072 | ctx=cli.tui.config.kind_int >>>
整数
<<< END U003063 >>>
<<< UNIT U003064 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1073-1073 | ctx=cli.tui.config.kind_list >>>
列表
<<< END U003064 >>>
<<< UNIT U003065 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1074-1074 | ctx=cli.tui.config.kind_other >>>
类型未知
<<< END U003065 >>>
<<< UNIT U003066 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1075-1075 | ctx=cli.tui.config.kind_str >>>
文本
<<< END U003066 >>>
<<< UNIT U003067 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1077-1077 | ctx=cli.tui.config.list_placeholder >>>
逗号分隔，例如：a, b, c
<<< END U003067 >>>
<<< UNIT U003068 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1078-1078 | ctx=cli.tui.config.mark_placeholder >>>
（待填写）
<<< END U003068 >>>
<<< UNIT U003069 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1079-1079 | ctx=cli.tui.config.mark_secret >>>
（密钥）
<<< END U003069 >>>
<<< UNIT U003070 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1080-1080 | ctx=cli.tui.config.mode_form >>>
表单
<<< END U003070 >>>
<<< UNIT U003071 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1081-1081 | ctx=cli.tui.config.mode_raw >>>
原始文本
<<< END U003071 >>>
<<< UNIT U003072 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1082-1082 | ctx=cli.tui.config.notify_toml_title >>>
TOML 校验失败
<<< END U003072 >>>
<<< UNIT U003073 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1083-1083 | ctx=cli.tui.config.notify_unsaved_title >>>
配置未保存
<<< END U003073 >>>
<<< UNIT U003074 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1084-1084 | ctx=cli.tui.config.notify_write_failed_title >>>
配置写入失败
<<< END U003074 >>>
<<< UNIT U003075 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1085-1085 | ctx=cli.tui.config.notify_written >>>
已写入 ${count} 项配置
<<< END U003075 >>>
<<< UNIT U003076 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1086-1086 | ctx=cli.tui.config.placeholder_notice >>>
待填写：请将模板占位符 ${value} 替换为实际值
<<< END U003076 >>>
<<< UNIT U003077 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1087-1087 | ctx=cli.tui.config.raw_add_line >>>
追加行
<<< END U003077 >>>
<<< UNIT U003078 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1088-1088 | ctx=cli.tui.config.raw_del_line >>>
删除末行
<<< END U003078 >>>
<<< UNIT U003079 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1089-1089 | ctx=cli.tui.config.raw_hint >>>
逐行编辑，保存前校验 TOML 格式
<<< END U003079 >>>
<<< UNIT U003080 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1090-1090 | ctx=cli.tui.config.raw_origin_file >>>
文件：${path}
<<< END U003080 >>>
<<< UNIT U003081 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1091-1091 | ctx=cli.tui.config.raw_origin_rebuilt >>>
配置文件不存在，内容由表 ${table} 的字段定义生成
<<< END U003081 >>>
<<< UNIT U003082 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1092-1092 | ctx=cli.tui.config.result_diff >>>
更改 ${changed} 项，未更改 ${unchanged} 项
<<< END U003082 >>>
<<< UNIT U003083 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1093-1093 | ctx=cli.tui.config.result_no_changes >>>
没有需要写入的更改
<<< END U003083 >>>
<<< UNIT U003084 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1094-1094 | ctx=cli.tui.config.result_table_loaded >>>
已加载表 ${table}，共 ${count} 项
<<< END U003084 >>>
<<< UNIT U003085 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1095-1095 | ctx=cli.tui.config.result_tables_loaded >>>
已读取 ${count} 张配置表
<<< END U003085 >>>
<<< UNIT U003086 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1096-1096 | ctx=cli.tui.config.result_write_ok >>>
已写入 ${section}.${name}
<<< END U003086 >>>
<<< UNIT U003087 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1097-1097 | ctx=cli.tui.config.skipped_nested_table >>>
${section}.${name} 是嵌套表
<<< END U003087 >>>
<<< UNIT U003088 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1098-1098 | ctx=cli.tui.config.skipped_nested_value >>>
${section}.${name} 是嵌套结构
<<< END U003088 >>>
<<< UNIT U003089 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1099-1099 | ctx=cli.tui.config.skipped_section >>>
[${section}] 不属于表 ${table}
<<< END U003089 >>>
<<< UNIT U003090 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1100-1100 | ctx=cli.tui.config.skipped_top_level >>>
${section} 是顶层键，不属于 [${table}] 段
<<< END U003090 >>>
<<< UNIT U003091 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1101-1101 | ctx=cli.tui.config.status_cached >>>
使用 ${age} 秒前的缓存，共 ${count} 张配置表
<<< END U003091 >>>
<<< UNIT U003092 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1102-1102 | ctx=cli.tui.config.status_editor_done >>>
编辑器已退出（退出码 ${code}），已重新加载表 ${table}
<<< END U003092 >>>
<<< UNIT U003093 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1103-1103 | ctx=cli.tui.config.status_editor_missing >>>
未找到编辑器命令 ${editor}，可设置 VISUAL 或 EDITOR 环境变量
<<< END U003093 >>>
<<< UNIT U003094 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1104-1104 | ctx=cli.tui.config.status_editor_no_file >>>
表 ${table} 没有对应的配置文件，无法打开编辑器
<<< END U003094 >>>
<<< UNIT U003095 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1105-1105 | ctx=cli.tui.config.status_editor_no_selection >>>
未选中配置表，无法打开编辑器
<<< END U003095 >>>
<<< UNIT U003096 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1106-1106 | ctx=cli.tui.config.status_load_failed >>>
读取失败：${error}
<<< END U003096 >>>
<<< UNIT U003097 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1107-1107 | ctx=cli.tui.config.status_loading_tables >>>
正在读取配置表列表…
<<< END U003097 >>>
<<< UNIT U003098 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1108-1108 | ctx=cli.tui.config.status_mode_switched >>>
已切换到${mode}模式
<<< END U003098 >>>
<<< UNIT U003099 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1109-1109 | ctx=cli.tui.config.status_no_changes >>>
表 ${table} 没有需要写入的更改。${hint}
<<< END U003099 >>>
<<< UNIT U003100 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1110-1110 | ctx=cli.tui.config.status_no_fields_save >>>
尚未加载字段，无法保存。请按 r 刷新
<<< END U003100 >>>
<<< UNIT U003101 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1111-1111 | ctx=cli.tui.config.status_no_selection_save >>>
未选中配置表，无法保存
<<< END U003101 >>>
<<< UNIT U003102 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1112-1112 | ctx=cli.tui.config.status_no_tables >>>
没有可编辑的配置表
<<< END U003102 >>>
<<< UNIT U003103 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1113-1113 | ctx=cli.tui.config.status_raw_failed >>>
读取 ${table} 的原始文本失败：${error}
<<< END U003103 >>>
<<< UNIT U003104 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1114-1114 | ctx=cli.tui.config.status_save_rejected >>>
拒绝保存：${message}
<<< END U003104 >>>
<<< UNIT U003105 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1115-1115 | ctx=cli.tui.config.status_table_failed >>>
读取表 ${table} 失败：${error}
<<< END U003105 >>>
<<< UNIT U003106 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1116-1116 | ctx=cli.tui.config.status_validation_failed >>>
校验失败，未写入配置：${error}
<<< END U003106 >>>
<<< UNIT U003107 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1117-1117 | ctx=cli.tui.config.status_write_summary >>>
写入完成：成功 ${ok} 项，失败 ${failed} 项。${first}
<<< END U003107 >>>
<<< UNIT U003108 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1118-1118 | ctx=cli.tui.config.status_writing >>>
正在写入 ${count} 项…
<<< END U003108 >>>
<<< UNIT U003109 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1119-1119 | ctx=cli.tui.config.status_written >>>
已写入 ${count} 项：${entries}。${hint}
<<< END U003109 >>>
<<< UNIT U003110 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1120-1120 | ctx=cli.tui.config.stub_write_ok >>>
写入成功
<<< END U003110 >>>
<<< UNIT U003111 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1121-1121 | ctx=cli.tui.dashboard.action_refresh >>>
刷新
<<< END U003111 >>>
<<< UNIT U003112 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1122-1122 | ctx=cli.tui.dashboard.add_calling >>>
正在添加 ${root}…
<<< END U003112 >>>
<<< UNIT U003113 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1123-1123 | ctx=cli.tui.dashboard.add_cancel >>>
取消
<<< END U003113 >>>
<<< UNIT U003114 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1124-1124 | ctx=cli.tui.dashboard.add_cancelled >>>
已取消添加
<<< END U003114 >>>
<<< UNIT U003115 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1125-1125 | ctx=cli.tui.dashboard.add_confirm >>>
添加
<<< END U003115 >>>
<<< UNIT U003116 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1126-1126 | ctx=cli.tui.dashboard.add_done >>>
已添加实例 ${name}（${root}）
<<< END U003116 >>>
<<< UNIT U003117 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1127-1127 | ctx=cli.tui.dashboard.add_failed >>>
添加失败：${error}
<<< END U003117 >>>
<<< UNIT U003118 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1128-1128 | ctx=cli.tui.dashboard.add_hint >>>
输入实例目录后按回车添加。添加只记录位置与策略，不改动实例内容。
<<< END U003118 >>>
<<< UNIT U003119 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1129-1129 | ctx=cli.tui.dashboard.add_label >>>
添加实例 ${root}
<<< END U003119 >>>
<<< UNIT U003120 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1130-1130 | ctx=cli.tui.dashboard.add_menu_hint >>>
新建实例会创建目录并执行 akaribot init。添加目录只把已有实例加入本机清单。
<<< END U003120 >>>
<<< UNIT U003121 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1131-1131 | ctx=cli.tui.dashboard.add_menu_title >>>
添加实例
<<< END U003121 >>>
<<< UNIT U003122 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1132-1132 | ctx=cli.tui.dashboard.add_placeholder >>>
实例目录，如 /srv/akaribot-demo
<<< END U003122 >>>
<<< UNIT U003123 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1133-1133 | ctx=cli.tui.dashboard.add_title >>>
添加实例
<<< END U003123 >>>
<<< UNIT U003124 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1134-1134 | ctx=cli.tui.dashboard.bind_refresh >>>
刷新快照
<<< END U003124 >>>
<<< UNIT U003125 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1135-1135 | ctx=cli.tui.dashboard.bind_remove_instance >>>
移出列表
<<< END U003125 >>>
<<< UNIT U003126 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1136-1136 | ctx=cli.tui.dashboard.busy_running >>>
命令执行中，请稍后重试
<<< END U003126 >>>
<<< UNIT U003127 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1137-1137 | ctx=cli.tui.dashboard.button_add_instance >>>
添加目录
<<< END U003127 >>>
<<< UNIT U003128 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1138-1138 | ctx=cli.tui.dashboard.button_add_menu >>>
添加实例…
<<< END U003128 >>>
<<< UNIT U003129 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1139-1139 | ctx=cli.tui.dashboard.button_autostart_off >>>
开机自启：关
<<< END U003129 >>>
<<< UNIT U003130 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1140-1140 | ctx=cli.tui.dashboard.button_autostart_on >>>
开机自启：开
<<< END U003130 >>>
<<< UNIT U003131 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1141-1141 | ctx=cli.tui.dashboard.button_crash_off >>>
崩溃重启：关
<<< END U003131 >>>
<<< UNIT U003132 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1142-1142 | ctx=cli.tui.dashboard.button_crash_on >>>
崩溃重启：开
<<< END U003132 >>>
<<< UNIT U003133 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1143-1143 | ctx=cli.tui.dashboard.button_new_instance >>>
新建实例
<<< END U003133 >>>
<<< UNIT U003134 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1144-1144 | ctx=cli.tui.dashboard.button_remove_instance >>>
移出列表
<<< END U003134 >>>
<<< UNIT U003135 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1145-1145 | ctx=cli.tui.dashboard.button_service_install >>>
安装服务
<<< END U003135 >>>
<<< UNIT U003136 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1146-1146 | ctx=cli.tui.dashboard.button_service_menu >>>
服务与策略…
<<< END U003136 >>>
<<< UNIT U003137 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1147-1147 | ctx=cli.tui.dashboard.button_service_uninstall >>>
卸载服务
<<< END U003137 >>>
<<< UNIT U003138 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1148-1148 | ctx=cli.tui.dashboard.button_switch >>>
切换实例
<<< END U003138 >>>
<<< UNIT U003139 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1149-1149 | ctx=cli.tui.dashboard.cli_stub_ok >>>
模拟命令执行成功
<<< END U003139 >>>
<<< UNIT U003140 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1150-1150 | ctx=cli.tui.dashboard.cli_timeout >>>
${label}超时（${seconds} 秒）
<<< END U003140 >>>
<<< UNIT U003141 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1151-1151 | ctx=cli.tui.dashboard.field_core_origin >>>
版本来源
<<< END U003141 >>>
<<< UNIT U003142 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1152-1152 | ctx=cli.tui.dashboard.field_core_version >>>
core 版本
<<< END U003142 >>>
<<< UNIT U003143 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1153-1153 | ctx=cli.tui.dashboard.field_instance_name >>>
实例名
<<< END U003143 >>>
<<< UNIT U003144 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1154-1154 | ctx=cli.tui.dashboard.field_instance_root >>>
实例路径
<<< END U003144 >>>
<<< UNIT U003145 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1155-1155 | ctx=cli.tui.dashboard.field_mode >>>
模式
<<< END U003145 >>>
<<< UNIT U003146 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1156-1156 | ctx=cli.tui.dashboard.field_running_detail >>>
状态依据
<<< END U003146 >>>
<<< UNIT U003147 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1157-1157 | ctx=cli.tui.dashboard.field_state >>>
运行状态
<<< END U003147 >>>
<<< UNIT U003148 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1158-1158 | ctx=cli.tui.dashboard.field_update_hint >>>
更新提示
<<< END U003148 >>>
<<< UNIT U003149 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1159-1159 | ctx=cli.tui.dashboard.fields_hint >>>
r ${refresh}，定期检查运行状态
<<< END U003149 >>>
<<< UNIT U003150 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1160-1160 | ctx=cli.tui.dashboard.fields_placeholder >>>
正在读取实例信息
<<< END U003150 >>>
<<< UNIT U003151 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1161-1161 | ctx=cli.tui.dashboard.instance_missing >>>
（目录不存在）
<<< END U003151 >>>
<<< UNIT U003152 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1162-1162 | ctx=cli.tui.dashboard.instance_unregistered >>>
（未添加）
<<< END U003152 >>>
<<< UNIT U003153 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1163-1163 | ctx=cli.tui.dashboard.instances_caption >>>
本机实例（回车切换，a 自启，c 崩溃重启，n 添加，Ctrl+d 移除）
<<< END U003153 >>>
<<< UNIT U003154 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1164-1164 | ctx=cli.tui.dashboard.instances_caption_with_count >>>
本机实例 ${count} 个（回车切换，a 自启，c 崩溃重启，n 添加，Ctrl+d 移除）
<<< END U003154 >>>
<<< UNIT U003155 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1165-1165 | ctx=cli.tui.dashboard.instances_failed >>>
读取实例清单失败：${error}
<<< END U003155 >>>
<<< UNIT U003156 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1166-1166 | ctx=cli.tui.dashboard.instances_keys_caption >>>
本机实例（选中后使用下方按钮，? 查看快捷键）
<<< END U003156 >>>
<<< UNIT U003157 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1167-1167 | ctx=cli.tui.dashboard.instances_keys_caption_with_count >>>
本机实例 ${count} 个（选中后使用下方按钮，? 查看快捷键）
<<< END U003157 >>>
<<< UNIT U003158 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1168-1168 | ctx=cli.tui.dashboard.mark_autostart >>>
自启
<<< END U003158 >>>
<<< UNIT U003159 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1169-1169 | ctx=cli.tui.dashboard.mark_crash_restart >>>
崩溃重启
<<< END U003159 >>>
<<< UNIT U003160 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1170-1170 | ctx=cli.tui.dashboard.menu_autostart_off >>>
关闭开机自启
<<< END U003160 >>>
<<< UNIT U003161 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1171-1171 | ctx=cli.tui.dashboard.menu_autostart_on >>>
开启开机自启
<<< END U003161 >>>
<<< UNIT U003162 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1172-1172 | ctx=cli.tui.dashboard.menu_crash_off >>>
关闭崩溃重启
<<< END U003162 >>>
<<< UNIT U003163 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1173-1173 | ctx=cli.tui.dashboard.menu_crash_on >>>
开启崩溃重启
<<< END U003163 >>>
<<< UNIT U003164 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1174-1174 | ctx=cli.tui.dashboard.mode_with_locale >>>
${mode}，语言 ${locale}
<<< END U003164 >>>
<<< UNIT U003165 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1175-1175 | ctx=cli.tui.dashboard.new_calling >>>
正在创建实例 ${root}…
<<< END U003165 >>>
<<< UNIT U003166 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1176-1176 | ctx=cli.tui.dashboard.new_cancelled >>>
已取消新建实例
<<< END U003166 >>>
<<< UNIT U003167 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1177-1177 | ctx=cli.tui.dashboard.new_confirm >>>
下一步
<<< END U003167 >>>
<<< UNIT U003168 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1178-1178 | ctx=cli.tui.dashboard.new_done >>>
已创建实例 ${name}（${root}）
<<< END U003168 >>>
<<< UNIT U003169 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1179-1179 | ctx=cli.tui.dashboard.new_failed >>>
创建实例失败：${error}
<<< END U003169 >>>
<<< UNIT U003170 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1180-1180 | ctx=cli.tui.dashboard.new_hint >>>
输入新实例目录后选择环境。创建过程包含 core 与适配器安装，可能需要数分钟。
<<< END U003170 >>>
<<< UNIT U003171 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1181-1181 | ctx=cli.tui.dashboard.new_label >>>
创建实例 ${root}
<<< END U003171 >>>
<<< UNIT U003172 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1182-1182 | ctx=cli.tui.dashboard.new_placeholder >>>
实例目录，如 /srv/akaribot-demo
<<< END U003172 >>>
<<< UNIT U003173 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1183-1183 | ctx=cli.tui.dashboard.new_registry_failed >>>
实例已创建，但写入实例列表失败：${error}
<<< END U003173 >>>
<<< UNIT U003174 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1184-1184 | ctx=cli.tui.dashboard.new_stub_ok >>>
模拟实例创建成功
<<< END U003174 >>>
<<< UNIT U003175 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1185-1185 | ctx=cli.tui.dashboard.new_title >>>
新建实例
<<< END U003175 >>>
<<< UNIT U003176 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1186-1186 | ctx=cli.tui.dashboard.new_venv_current >>>
使用当前环境（--no-venv）
<<< END U003176 >>>
<<< UNIT U003177 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1187-1187 | ctx=cli.tui.dashboard.new_venv_hint >>>
托管 venv 与系统解释器隔离。使用当前环境则安装到运行界面的解释器中。
<<< END U003177 >>>
<<< UNIT U003178 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1188-1188 | ctx=cli.tui.dashboard.new_venv_managed >>>
创建托管 venv
<<< END U003178 >>>
<<< UNIT U003179 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1189-1189 | ctx=cli.tui.dashboard.new_venv_title >>>
确认创建实例 ${root}
<<< END U003179 >>>
<<< UNIT U003180 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1190-1190 | ctx=cli.tui.dashboard.policy_autostart_off >>>
已关闭 ${name} 的开机自启
<<< END U003180 >>>
<<< UNIT U003181 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1191-1191 | ctx=cli.tui.dashboard.policy_autostart_on >>>
已开启 ${name} 的开机自启，服务启动时将恢复期望运行状态
<<< END U003181 >>>
<<< UNIT U003182 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1192-1192 | ctx=cli.tui.dashboard.policy_calling >>>
正在设置 ${name} 的服务策略…
<<< END U003182 >>>
<<< UNIT U003183 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1193-1193 | ctx=cli.tui.dashboard.policy_crash_off >>>
已关闭 ${name} 的崩溃重启
<<< END U003183 >>>
<<< UNIT U003184 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1194-1194 | ctx=cli.tui.dashboard.policy_crash_on >>>
已开启 ${name} 的崩溃重启，服务将在异常退出后重启实例
<<< END U003184 >>>
<<< UNIT U003185 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1195-1195 | ctx=cli.tui.dashboard.policy_failed >>>
设置实例策略失败：${error}
<<< END U003185 >>>
<<< UNIT U003186 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1196-1196 | ctx=cli.tui.dashboard.policy_label >>>
设置 ${name} 的服务策略
<<< END U003186 >>>
<<< UNIT U003187 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1197-1197 | ctx=cli.tui.dashboard.policy_unregistered >>>
${root} 未添加，请先按 n 添加
<<< END U003187 >>>
<<< UNIT U003188 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1198-1198 | ctx=cli.tui.dashboard.register_auto >>>
已自动添加当前实例 ${name}（${root}）
<<< END U003188 >>>
<<< UNIT U003189 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1199-1199 | ctx=cli.tui.dashboard.remove_calling >>>
正在从列表移除 ${name}…
<<< END U003189 >>>
<<< UNIT U003190 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1200-1200 | ctx=cli.tui.dashboard.remove_cancelled >>>
已取消移出列表
<<< END U003190 >>>
<<< UNIT U003191 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1201-1201 | ctx=cli.tui.dashboard.remove_choice_confirm >>>
移出列表
<<< END U003191 >>>
<<< UNIT U003192 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1202-1202 | ctx=cli.tui.dashboard.remove_choice_hint >>>
仅移除注册表记录，保留实例目录。
<<< END U003192 >>>
<<< UNIT U003193 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1203-1203 | ctx=cli.tui.dashboard.remove_choice_title >>>
确认从列表移除 ${name}
<<< END U003193 >>>
<<< UNIT U003194 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1204-1204 | ctx=cli.tui.dashboard.remove_done >>>
已从列表移除 ${name}
<<< END U003194 >>>
<<< UNIT U003195 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1205-1205 | ctx=cli.tui.dashboard.remove_failed >>>
移出列表失败：${error}
<<< END U003195 >>>
<<< UNIT U003196 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1206-1206 | ctx=cli.tui.dashboard.remove_label >>>
从列表移除 ${name}
<<< END U003196 >>>
<<< UNIT U003197 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1207-1207 | ctx=cli.tui.dashboard.remove_missing >>>
注册表中不存在 ${name}
<<< END U003197 >>>
<<< UNIT U003198 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1208-1208 | ctx=cli.tui.dashboard.running_detail_fallback >>>
锁文件探测
<<< END U003198 >>>
<<< UNIT U003199 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1209-1209 | ctx=cli.tui.dashboard.running_detail_lock >>>
锁文件 ${path}
<<< END U003199 >>>
<<< UNIT U003200 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1210-1210 | ctx=cli.tui.dashboard.service_action_install >>>
安装常驻服务
<<< END U003200 >>>
<<< UNIT U003201 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1211-1211 | ctx=cli.tui.dashboard.service_action_uninstall >>>
卸载常驻服务
<<< END U003201 >>>
<<< UNIT U003202 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1212-1212 | ctx=cli.tui.dashboard.service_added >>>
服务已安装：${path}
<<< END U003202 >>>
<<< UNIT U003203 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1213-1213 | ctx=cli.tui.dashboard.service_calling_install >>>
正在安装常驻服务…
<<< END U003203 >>>
<<< UNIT U003204 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1214-1214 | ctx=cli.tui.dashboard.service_calling_preview >>>
正在预览${action}…
<<< END U003204 >>>
<<< UNIT U003205 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1215-1215 | ctx=cli.tui.dashboard.service_calling_uninstall >>>
正在卸载常驻服务…
<<< END U003205 >>>
<<< UNIT U003206 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1216-1216 | ctx=cli.tui.dashboard.service_cancelled >>>
已取消服务操作
<<< END U003206 >>>
<<< UNIT U003207 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1217-1217 | ctx=cli.tui.dashboard.service_choice_dry_run >>>
预览（--dry-run）
<<< END U003207 >>>
<<< UNIT U003208 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1218-1218 | ctx=cli.tui.dashboard.service_choice_hint >>>
预览显示单元文件与系统命令，不更改系统。
<<< END U003208 >>>
<<< UNIT U003209 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1219-1219 | ctx=cli.tui.dashboard.service_choice_hint_force >>>
安装将覆盖现有单元文件 ${path}。预览仅显示内容，不更改系统。
<<< END U003209 >>>
<<< UNIT U003210 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1220-1220 | ctx=cli.tui.dashboard.service_choice_install >>>
安装并注册
<<< END U003210 >>>
<<< UNIT U003211 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1221-1221 | ctx=cli.tui.dashboard.service_choice_title >>>
确认${action}
<<< END U003211 >>>
<<< UNIT U003212 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1222-1222 | ctx=cli.tui.dashboard.service_choice_uninstall >>>
卸载并注销
<<< END U003212 >>>
<<< UNIT U003213 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1223-1223 | ctx=cli.tui.dashboard.service_disabled >>>
已写入但未注册
<<< END U003213 >>>
<<< UNIT U003214 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1224-1224 | ctx=cli.tui.dashboard.service_enabled >>>
已注册
<<< END U003214 >>>
<<< UNIT U003215 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1225-1225 | ctx=cli.tui.dashboard.service_failed >>>
服务操作失败：${error}
<<< END U003215 >>>
<<< UNIT U003216 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1226-1226 | ctx=cli.tui.dashboard.service_installed >>>
服务：已安装（${backend}，${state}，${path}）
<<< END U003216 >>>
<<< UNIT U003217 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1227-1227 | ctx=cli.tui.dashboard.service_label_install >>>
安装常驻服务
<<< END U003217 >>>
<<< UNIT U003218 | json-value | packages/akari-bot-cli/akaribot/cli/locales/zh_cn.json:1228-1228 | ctx=cli.tui.dashboard.service_label_uninstall >>>
卸载常驻服务
<<< END U003218 >>>
