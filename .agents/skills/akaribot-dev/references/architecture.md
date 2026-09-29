# 架构、启动与消息链路

## 目录
- [项目速览](#1-项目速览)
- [技术栈与依赖](#2-技术栈与依赖)
- [架构总览](#3-架构总览)
- [启动流程详解](#4-启动流程详解)
- [包发现与实例模型](#5-包发现与实例模型)
- [消息处理全链路](#6-消息处理全链路)
- [目录结构参考](#13-目录结构参考)

---

## 1. 项目速览

**AkariBot（小可）** 是一个多平台、可扩展的异步聊天机器人框架。仓库为 uv workspace 形态：核心运行时、命令模块与平台适配器各自独立发包，运行时经 entry points 发现可用包。

- **语言**: Python 3.12+（各包声明 `requires-python = ">=3.12,<4.0"`）
- **异步框架**: asyncio
- **ORM**: Tortoise ORM（支持 SQLite/MySQL）
- **Web 框架**: FastAPI（用于 Webhook 和 API）
- **调度器**: APScheduler
- **许可证**: AGPL-3.0

### 支持平台

|平台|适配器包|导入路径|协议/SDK|
|---|---|---|---|
|QQ（第三方，OneBot）|`akari-bot-adapter-onebot`|`akaribot.adapters.onebot`|OneBot 11 (aiocqhttp)|
|QQ（第三方，Milky）|`akari-bot-adapter-milky`|`akaribot.adapters.milky`|Milky v1.1 (milky-python-sdk)|
|QQ（官方）|`akari-bot-adapter-qqbot`|`akaribot.adapters.qqbot`|QQ Bot API (qq-botpy-sdk)|
|Discord|`akari-bot-adapter-discord`|`akaribot.adapters.discord`|py-cord|
|Telegram|`akari-bot-adapter-telegram`|`akaribot.adapters.telegram`|aiogram|
|KOOK|`akari-bot-adapter-kook`|`akaribot.adapters.kook`|khl-py|
|Matrix|`akari-bot-adapter-matrix`|`akaribot.adapters.matrix`|matrix-nio|
|Web|`akari-bot-adapter-web`|`akaribot.adapters.web`|FastAPI|

本文出现的 `akaribot/...` 路径均相对所在包的**分发根**（源码根即分发根，没有 `src/` 一层）：`akaribot/core/...` 即 `packages/akari-bot-core/akaribot/core/...`，模块与适配器依此类推；实例内的路径（如 `config/`、`data/`）则相对实例根。

适配器包目录名、entry point 名与导入路径末级三者一致。平台展示名取自包内 `info.py` 的 `platform_name`，是客户端命名的唯一真源：`onebot` 与 `milky` 的平台名同为 `QQ`，多实例以 `<平台>-<实例 ID>` 区分，故平台名不能从目录名推断。

---

## 2. 技术栈与依赖

### 包管理

使用 **uv** 管理依赖。仓库根 `pyproject.toml` 是虚拟 workspace 根，不发布自身，只声明成员（`packages/akari-bot-*`、`packages/adapters/*`、`packages/modules/*`）、workspace 内的版本来源与全仓工具配置：

```bash
uv sync --all-extras --dev    # 安装全部成员的可选依赖与开发依赖组
uv add <package>              # 为当前包添加依赖
uv lock                       # 重新求解并更新全仓唯一的 uv.lock
```

依赖在各自包的 `pyproject.toml` 中按功能分组管理，新增依赖需移至对应注释分组下并按字母排序。CI 使用 `uv sync --locked --all-extras --dev`：该命令会重新求解，workspace 内成员的第三方依赖互斥在 PR 阶段即失败。

workspace 覆盖会丢弃内部依赖的版本约束，而发布出的 wheel 仍带着它，故包之间的内部约束须与 core 版本字面一致（如 `akari-bot-core>=0.1.0,<1.0`），由 `tools/lint_versions.py` 检查。

### 核心依赖

|类别|包名|用途|
|---|---|---|
|配置|`tomlkit`|TOML 配置解析（保留注释）|
|数据库|`tortoise-orm`|ORM（SQLite；MySQL 经 extra 安装）|
|HTTP|`httpx`, `httpx-ws`, `aiofile`|异步 HTTP、WebSocket 客户端与文件|
|日志|`loguru`|结构化日志|
|调度|`APScheduler`|定时任务|
|Web|`fastapi`, `uvicorn`|Web 服务器|
|序列化|`orjson`|高性能 JSON|
|属性|`attrs`, `cattrs`|数据类 / 结构化序列化|
|工具|`rapidfuzz`|模糊匹配（错字纠正）|
|工具|`tenacity`|重试机制|
|测试|`coverage`|代码覆盖率|
|测试|`pytest`, `pytest-asyncio`|pytest 前端与异步用例支持|
|代码|`ruff`|格式化 + 静态检查|

上表前十项由 `akari-bot-core` 声明，测试与代码类工具属于根 `dev` 依赖组。

`akari-bot-core` 的可选依赖为 `s3`（boto3，对象存储）、`mysql`（asyncmy 驱动）与 `image`（matplotlib 图表渲染，`chart` 为同义别名）。MySQL 部署安装 `akari-bot-core[mysql]`。

**第一方服务依赖**（Teahouse 自家发布的包，升级时留意版本约束是精确 `==`）：

|包名|用途|声明位置|
|---|---|---|
|`akari-bot-i18n`|i18n 语言包（`==0.1.3`）|`akari-bot-core`|
|`akari-bot-webrender`|网页渲染服务（`==0.6.2`）|core 与 wiki 模块|
|`akari-bot-webui`|Web 控制台前端（`==0.4.5`）|web 适配器|
|`akari-bot-html2text`|HTML 转文本|wiki 等模块|

平台 SDK 由对应适配器包自行声明（见第 1 节的平台表）。模块包只声明自身业务用到的第三方库，例如 `beautifulsoup4`、`feedparser`、`wikitextparser` 属于 `akari-bot-module-wiki`，不进入 core。

### 开发与测试命令

```bash
CI=1 python -m akaribot.testing        # 全量用例；根目录的 python tester.py 等价
CI=1 PYTHONIOENCODING=UTF-8 python tests/run_one.py <测试文件> [入口函数]
uv run ruff check . && uv run ruff format --check .
uv run python tools/lint_boundaries.py   # 分层、命名空间、依赖声明
uv run python tools/lint_versions.py     # 内部版本约束一致性
```

- `python -m akaribot.testing` 与根 `tester.py` 运行同一份实现；根脚本是兼容层，用 `sys.modules` 别名转发到 `akaribot.testing.runner`，既有 CI 与脚本无需改动。
- 用例分布：仓库根 `tests/` 承载跨包用例与共享夹具，各成员包自带 `packages/<分发>/tests/`，运行器同时收集 `packages/*/tests` 与 `packages/*/*/tests`。
- 自动化运行必须设置 `CI=1`，否则人工复核与等待输入可能挂起。`akaribot.testing.timing.TIME_SCALE` 在 CI 下放大等待时长，`AKARI_TEST_TIME_SCALE` 可覆盖；Windows 下运行中文用例须显式设置 `PYTHONIOENCODING=UTF-8`。
- 单个入口用 `tests/run_one.py <测试文件> [入口函数]`，它以 `os._exit` 收尾。

---

## 3. 架构总览

### 分层与依赖方向

三层各自独立分发：`akari-bot-core`（框架与随包内置模块）、`akari-bot-module-<名>`（命令模块）、`akari-bot-adapter-<平台>`（平台适配器）。依赖方向单向：

- 模块与适配器依赖 core；core 不 import 任何模块或适配器（B4）；
- 适配器不 import 具体模块，平台能力只能经 `SessionInfo` / `Features` 声明式获取（B5）；
- 模块之间不互相 import；官方模块包（`packages/modules/*`）不得建立模块间依赖（B1 / B6 / B10）。

上述规则由 `tools/lint_boundaries.py` 以 AST 静态检查执行，既有违规经 `tools/boundary_lint_baseline.txt` 豁免，只对新增与修改的行生效。`akaribot`、`akaribot.modules`、`akaribot.adapters` 是 PEP 420 命名空间目录，不得包含 `__init__.py`（B7）；`akaribot.core`、`akaribot.testing` 与各模块、适配器包是常规包。

### 进程模型

```
akaribot.core.entrypoints.run（守护进程）
    │   python -m akaribot.core.entrypoints.run
    │
    ├── WebSocket JobQueue Hub（选择内置 WebSocket 后端时）
    │   └── 独立控制面与实时路由进程
    │
    ├── Bot 进程 1 (e.g., onebot)
    │   └── 接收平台消息 → 通过 JobQueue 发送到 Server
    │
    ├── Bot 进程 2 (e.g., discord)
    │   └── 接收平台消息 → 通过 JobQueue 发送到 Server
    │
    ├── ...
    │
    └── Server 进程
        ├── JobQueueServer: 处理消息队列
        ├── 模块系统: 加载/执行命令模块
        ├── 调度器: APScheduler 定时任务
        └── FastAPI: Webhook / API
```

**关键设计**: Bot 进程和 Server 进程通过可配置的 **Peer RPC 与信号总线**通信。完整后端可选择数据库，
也可选择由独立 Hub 提供的 WebSocket 实时传输；两种后端不得交叉组合或自动回退。Bot 进程负责平台 SDK
交互，Server 进程负责命令解析和业务逻辑。每个进程实例有独立 `peer_id`，同类实例共享稳定 `service`；
Registry 租约负责发现，service anycast / 稳定路由负责分流，逐实例 signal 负责广播。

### 核心分层

```
┌────────────────────────────────────────────────────┐
│    平台适配器 akaribot.adapters.<平台>（独立分发） │
│  onebot/ milky/ qqbot/ discord/ telegram/ kook/    │
│  matrix/ web/                                      │
├────────────────────────────────────────────────────┤
│           Bot 核心框架 akaribot.core               │
│  Bot Class / Session System / Parser（命令解析）   │
│  MessageChain（消息链）                            │
│  Config(TOML) / Database(Tortoise) / Queue         │
├────────────────────────────────────────────────────┤
│     命令模块 akaribot.modules.<名>（独立分发）     │
│  core（随 core 分发）/ wiki/ arcaea/ maimai/ dice/  │
└────────────────────────────────────────────────────┘
```

---

## 4. 启动流程详解

### 守护进程入口（`akaribot/core/entrypoints/run.py`）

```python
# akaribot/core/entrypoints/run.py - main() 是同步函数，每轮用 asyncio.run() 起一个全新事件循环
def main():
    base_import_lists = list(sys.modules)  # 记录基线，重启时只清理增量模块

    while True:
        try:
            asyncio.run(main_async())
        except RestartBot:
            clear_import_cache()  # 删除 base_import_lists 之外的所有 sys.modules 条目
            continue  # 热重启支持
        except SystemExit as exit_signal:
            raise exit_signal  # 配置冲突等中止原因不得被吞成退出码 0
        except KeyboardInterrupt:
            break
```

`python -m akaribot.core.entrypoints.run` 是唯一真实入口；仓库根 `bot.py` 是兼容层，`python bot.py` 转发到该模块的 `main()`，`import bot` 则把 `sys.modules["bot"]` 换成 run 模块本身。

`main()` 里还有**单实例文件锁**：锁文件为 `<实例根>/.bot.lock`（`Paths.lock`），Windows 用 `msvcrt.locking`、其他平台用 `fcntl.flock`，抢锁失败直接 `sys.exit(1)`。同一实例目录下不能同时跑两个守护进程，`akaribot.cli.instance` 的运行探测与锁文件同源。

### 启动序列

1. **`pre_init()`**，注意它是在一个**独立子进程**里跑完就退出的（`multiprocess_run_until_complete`）：
    - `Paths.ensure("data", "cache", "logs", "database")` 建立实例目录；`shutil.rmtree(cache_path)` 直接删除整个缓存目录后重建
    - 载入 i18n 快照，核心与各包的 `locales/` 一并纳入
    - 扫描配置模板；为留空的 JobQueue `node_id` 与 WebSocket token 生成随机值并原子写回配置；任一模板加载失败即中止启动
    - 初始化 Tortoise ORM 数据库连接
    - 执行数据库迁移（`DBVersion` 检查：无记录 → `convert_database()`；版本落后 → `update_database()`）
    - 设置超级用户（从配置读取 `base_superuser`）

2. **`run_bot()`**:
    - 经 `PackageRegistry.adapters()` 取得已安装适配器；`discover_adapter_instances()` 以配置中的 `bot_*` 表为索引枚举已启用实例（表名去前缀后按第一个 `-` 拆出平台与实例 ID）
    - `check_instance_conflicts()` 在任何适配器进程启动之前拦下端口冲突与重复凭据
    - 为每个启用的实例创建 **子进程**: `multiprocessing.Process(target=go, args=(platform, ...))`，多进程上下文在 Windows / macOS 取 `spawn`，其他平台取 `forkserver`
    - 创建 Server 子进程: `multiprocessing.Process(target=server_go, ...)`
    - 进入监控循环：每秒检查进程状态，失败自动重启（同一 `client_name` 在 60 秒窗口内失败 3 次即放弃）

3. **Bot 子进程启动**（`akaribot/adapters/<平台>/bot.py`，由 `go()` 按导入路径载入）:
    - 调用 `Bot.register_bot(client_name)` 注册客户端
    - 调用 `Bot.register_context_manager(ContextManager)` 注册上下文管理器（主动会话另注册 `*FetchedContextManager`）
    - 经 `client_init()` 启动平台 SDK 监听消息
    - 收到消息时调用 `Bot.process_message(session_info, ctx)`

4. **Server 进程启动**（`akaribot/core/server/run.py` 调用 `akaribot/core/server/init.py`）:
    - 初始化数据库
    - 加载所有模块（`akaribot.core.loader.load_modules()`）
    - 注册模块中的定时任务到 APScheduler
    - 启动调度器
    - 启动 `JobQueueServer.check_job_queue()` 轮询

### JobQueue Peer 启动与发现

Client 和 Server 在开始接收业务任务前都执行同一套屏障：

1. 生成本次进程生命周期唯一的 `peer_id`，登记 `role / service / node_id / capabilities / metadata`；其中
   `node_id` 依次取自 `configure_peer()` 显式参数和 `jobqueue.toml` 的 `[jobqueue].jobqueue_node_id`。正常启动
   已由 `pre_init` 为留空值生成 UUID 并写回，因此共用配置目录的进程共享稳定的部署节点标签；绕过守护进程
   的入口仅在配置仍为空时生成进程级临时 UUID。节点标识不得读取或推导计算机名；
2. 启动由 `[jobqueue].jobqueue_backend` 选择的完整后端，再以 `starting` 向其权威 Registry 注册，初始化完成后
   切换为 `ready`；数据库后端写入 `JobQueuePeersTable`，WebSocket 后端通过已鉴权连接向独立 Hub 注册；
3. 查询 Registry 获得当前拓扑，并向其它 ready 实例逐个投递 `peer.ready`；
4. 已在线实例用定向 `peer.welcome` 回应，新旧双方由此快速更新本地缓存；
5. 每 15 秒续租、每 10 秒完整对账（`RECONCILE_INTERVAL_SECONDS = 10`）；异常退出最多约 45 秒后由租约过期
   识别（`LEASE_SECONDS = 45`）。

`peer.ready/welcome` 是变化通知，不是在线事实本身。接收端会重新读取 Registry，并校验信号来源
`source_peer_id` 与载荷中的 `peer_id` 一致。维护、恢复、摘流和停止信号同样必须与 Registry 当前状态
一致，迟到信号不能覆盖更新的状态。

同一 `service` 下可以登记多个同类型实例：普通 service 目标由它们竞争领取；要求场景粘性的消息使用
Rendezvous Hash（`akaribot/core/queue/peer.py`）选择实例；广播先快照目标，再生成逐实例投递记录。因此
扩大 Client / Server 数量不需要改变业务 RPC 载荷。

后端选择的完整规则见 `akaribot/core/queue/README.md`：`[jobqueue].jobqueue_backend` 的有效值为
`database` 与 `websocket`，同一逻辑集群的进程必须使用相同后端，运行期间不支持热切换。

### 退出码约定

|退出码|bot 子进程|server 子进程|
|---|---|---|
|0|正常退出（不重启）|整个守护进程 `sys.exit(0)`|
|33|重启所有进程|重启所有进程|
|78|部署问题，摘除该进程不重启|—|
|其他|错误（重启当前实例）|守护进程带该码退出|

重启不是无限的：`restart_bot_process()` 用 `failed_to_start_attempts` 记账，**同一实例在 60 秒窗口内失败 3 次就放弃重启**（窗口过期会重新计数）。退出码 33 由 `akaribot/core/server/terminate.py` 的 `restart()` 以 `os._exit(33)` 发出；退出码 78（EX_CONFIG）表示重试无济于事，例如适配器入口缺失。

---

## 5. 包发现与实例模型

### 发现顺序

`akaribot.core.registry.PackageRegistry` 是「系统里有哪些模块与适配器」的唯一答案来源，按下列顺序合成：

1. 存在 `akaribot/core/_frozen_registry.py` 时直接采用其中记录的清单（二进制构建产物，**规划中**，尚未生成）；
2. 枚举已安装分发的 entry point，模块取 `akaribot.modules` 组，适配器取 `akaribot.adapters` 组；
3. 兜底扫描命名空间包 `akaribot.modules` 与 `akaribot.adapters` 下的真实包目录，合成 `dist_name` 为空的条目，供未安装分发的源码检出形态使用；
4. 按 `kind:name` 去重，entry point 胜出，冲突时记录告警。

发现结果在进程内缓存一次，安装或卸载包之后经 `discover(force=True)` 重建。进入正式清单前还有两道闸，顺序不可颠倒：

- **core API 兼容性**：包的 `requires_core_api` 与 `CORE_API_VERSION = 1` 相较，不满足者拒绝注册；
- **声明依赖校验**：分发 metadata 里声明的模块包依赖缺失、版本不满足、成环，或依赖了已被 API 门槛拒绝的包，同样拒绝注册。

两道闸拒绝的包不进入 `PackageRegistry.modules()` / `adapters()`，但经 `PackageRegistry.incompatible()` 可见，供启动提示与 `~module list` 展示。

### 包清单 manifest.toml

每个模块包与适配器包在自己的导入包目录下带一份 `manifest.toml`，由发现层读取。全部字段都有默认值，缺失即等价于未声明；未知键记录告警后忽略。

|字段|含义|
|---|---|
|`schema`|manifest 自身的结构版本，当前为 `1`|
|`requires_core_api`|所需的 core 公共 API 区间，PEP 440 描述符，如 `">=1"`|
|`locales`|包内 locale 目录的相对路径，缺省 `"locales"`|
|`assets`|包内只读静态资源的相对路径|
|`migrations`|数据库迁移目录的相对路径|
|`config_migrations`|配置迁移目录的相对路径|
|`config_table`|配置文件中的表名，如 `module_wiki` / `bot_onebot`|
|`config_schema_version`|该包配置的表结构版本|
|`provides_modules`|该包注册的模块名，供 `~module` 与 CLI 展示|
|`owned_tables`|该包拥有的数据表，供数据清理使用|
|`credential_fields`|该包配置中属于凭据的字段名，供重复凭据检查使用|

`locales`、`assets`、`migrations` 都相对包根目录解析，因此这些目录必须随 wheel 一起分发：模块脚手架的 `pyproject.toml` 用 `[tool.hatch.build.targets.wheel.force-include]` 显式收录它们。

### 包的物理布局与 entry point

```toml
# packages/modules/akari-bot-module-wiki/pyproject.toml
[project.entry-points."akaribot.modules"]
wiki = "akaribot.modules.wiki"
```

```toml
# packages/adapters/akari-bot-adapter-onebot/pyproject.toml
[project.entry-points."akaribot.adapters"]
onebot = "akaribot.adapters.onebot"
```

包目录遵循 `packages/<分发>/<导入路径>/`，源码根即分发根；测试运行器与 registry 生成工具同时兼容分发根下的 `src/`。源码检出下 `packages/modules/*` 与 `packages/adapters/*` 被 workspace 成员通配符覆盖，`uv sync` 以可编辑方式安装，发现层因此同时命中 entry point 与目录扫描两条路径。适配器 entry point 名不得含 `-`，否则与多实例分隔符冲突（B9）。

`akaribot new module <名>` 按 `templates/module/` 生成包骨架：`pyproject.toml`、`akaribot/modules/<名>/`（含 `manifest.toml`、`config.py`、`locales/`、`assets/`、`database/`、`migrations/`）与 `tests/`。

### 模块作者的公共 API

`akaribot.core.api` 是模块作者的门面，`akaribot.core.api.adapters` 是适配器面；两者共享的名字（`Bot`、`SessionInfo`、消息元素等）只在 `akaribot.core.api` 导出，适配器同时依赖两个门面。门面以 `__all__` 承诺全部可用名字，实现集中在 `akaribot/core/api/base.py` 与 `akaribot/core/api/adapters.py`。

```python
from akaribot.core.api import Bot, I18NContext, MessageChain, Plain, SessionInfo, module

mod = module("demo", desc="示例模块")  # 作者写在包的 pyproject.toml 的 [project] authors


@mod.command("<name>")
async def _(msg: Bot.MessageSession, name: str):
    await msg.finish(Plain(f"hello, {name}"))
```

门面的导入分两层：不依赖配置系统的名字在模块层直接导入，其余名字经 `__getattr__` 在首次访问时解析。原因是 `akaribot.core.config` 会在导入期校验配置文件存在并执行版本迁移，而门面必须能在配置就绪之前导入——CLI 读取 API 版本、发现层收集 locale 目录都发生在配置加载之前。

模块不得 import core 的内部深路径：走 `akaribot.core.api` 的写法一律合规；深路径 import 取的符号未收录进门面时，`tools/lint_boundaries.py` 的 B8 规则给出 warn（基线内的既有违规豁免）。`CORE_API_VERSION` 是 core 公共 API 版本的单一真源，`akaribot.core.api` 取其值，包以 manifest 的 `requires_core_api` 声明所需区间。

### 实例模型

实例根由根目录下的 `akaribot.toml` 标记，`akaribot init <目录>` 生成该文件；CLI 的其他子命令据此向上查找实例根。元数据包含 `schema`、`[instance]`（`name` / `created_at` / `locale` / `mode`）、`[runtime]`（`venv`）、`[dev]`（`workspace_root`）与 `[registry]`（包索引来源）。

`akaribot.core.paths.Paths` 是「进程在哪个实例里运行」的唯一答案，取值在导入期完成一次，之后只读；未设置 `AKARI_INSTANCE_DIR` 时取进程 cwd：

|属性|路径|说明|
|---|---|---|
|`instance`|实例根|由 `AKARI_INSTANCE_DIR` 或 cwd 决定|
|`config`|`<实例根>/config`|可由 `AKARI_CONFIG_PATH` 整体覆盖|
|`assets`|`<实例根>/assets`|随仓库或分发包提供的只读资源|
|`data`|`<实例根>/data`|运行时与部署者产生的可写数据|
|`cache`|`<实例根>/cache`|可随时删除的缓存，启动时清空|
|`database`|`<实例根>/database`|数据库文件所在目录（SQLite）|
|`logs`|`<实例根>/logs`|日志目录|
|`lock`|`<实例根>/.bot.lock`|单实例锁文件，供入口互斥与 CLI 探测|
|`tests`|仓库根 `tests/`|属源码仓库而非实例，可由 `AKARI_TESTS_PATH` 覆盖|

导入期不创建目录，创建由 `Paths.ensure()` 显式触发。包目录在只读挂载与 wheel 安装下都不可写，模块的下载、索引与用户数据一律写 `PackageRegistry.package_data(<包名>)`（即 `<实例根>/data/<module|adapter>/<包名>`）。

实例内的配置文件当前为扁平布局：`config/<表名>.toml`（如 `config.toml`、`bot_onebot.toml`、`module_wiki.toml`），多实例为 `bot_<平台>-<实例 ID>.toml`。`CFGManager.load()` 只扫描 `config/*.toml`，因此适配器实例配置必须写在扁平路径下；`config/adapters/` 分层布局**规划中**，尚未启用。旧部署的搬迁步骤见 `docs/migrating-to-packages.md`。

### CLI 与 core 的进程边界

`akaribot` 由 `akari-bot-cli` 提供（Typer 应用，入口 `akaribot.cli.main:app`），子命令为 `init` / `run` / `test` / `module` / `config` / `adapter` / `venv` / `doctor` / `new` / `tui` / `migrate`。CLI 进程不 import `akaribot.core`，因此可在实例 venv 之外运行（系统解释器、pipx 安装）；实例操作一律经子进程调用 core 入口模块并解析其 JSON 回传，stdout 只放结果，日志与提示走 stderr：

```
python -m akaribot.core.entrypoints.{run,registry,config,db,data,peers,modules,rpc}
```

`run` 为守护进程，其余分别提供已装包清单、配置读写、数据库迁移、库表与数据项读写（`data`：按条件
筛选、全表搜索与分页都由它收口）、peer 快照、模块装卸与热装载 RPC。每个入口模块都须能独立以 `python -m` 运行，并自行解析 `AKARI_INSTANCE_DIR`。解释器经 `akaribot.cli.instance.system_python()` 解析：Nuitka 冻结后 `sys.executable` 指向二进制自身，CLI 包内禁止用它启动实例进程（B11）。

---

## 6. 消息处理全链路

### 接收消息流程

```
1. 平台 SDK 收到消息
       ↓
2. akaribot/adapters/<平台>/bot.py - message_handler()
   - 解析平台消息格式
   - 创建 SessionInfo（含 target_id, sender_id 等）
       ↓
3. Bot.process_message(session_info, ctx)
   - 从 ContextSlots 获取平台 ContextManager
   - 注入平台 Features
   - 添加上下文到 ContextManager
       ↓
4. ServerAPI.receive_message(session_info)
   - 序列化 SessionInfo 为 JSON
   - 按场景路由键从 ready Server 中稳定选择一个实例
   - 写入 JobQueuesTable；尚无 Server 时保留为 service anycast 任务
       ↓
5. JobQueueServer.check_job_queue() (Server 进程)
   - 轮询 JobQueuesTable
   - 反序列化 SessionInfo
   - 创建 MessageSession
       ↓
6. parser(msg)
   - 权限检查
   - 前缀匹配
   - 命令解析
   - 模块匹配
       ↓
7. 执行模块函数
   - msg.send_message() → PlatformAPI.send_message()
   - msg.finish() → 发送并抛出 SessionFinished
       ↓
8. 通过 JobQueue 返回到 Bot 进程
       ↓
9. ContextManager.send_message() → 平台 SDK 发送
```

### 主动推送流程

```
定时任务/钩子触发
       ↓
Bot.post_message(module_name, message, session_list)
   - 从数据库查询启用了该模块的目标列表
   - group_sessions_by_channel(): 按「场景组 + 消息通道」归拢，同一通道只推一次
   - 只发队首，session_info.next_hops = 该通道内其余会话的 target_id
       ↓
PlatformAPI.post_message.submit(session_info, message, module_name)
       ↓ (跨进程)
JobQueueClient 的 platform.post_message handler → ContextManager.send_message(quote=False)
       ↓
   拿到 msgid → 结束，这条通道已送达
   拿不到    → ServerAPI.post_next_hop.submit(next_hops, message, module_name)
                   ↓ (跨进程，回到服务端——下一跳可能是另一个平台，只有服务端解析得了)
              Server handler → fetch_target() → 再来一轮
```

跳表每次只会变短，不会成环。因此 `*FetchedContextManager` 的 `send_message` **必须返回真实的消息 ID**：
onebot / qqbot 的主动消息要按冷却排队，队列里放的是 `(future, 任务参数)`，
`send_message` 等 future，`process_tasks()` 发完再 `set_result` —— 冷却节奏不变，但调用方拿得到结果。

### 私信发送流程

```
msg.send_private_message(message, user_id)
   - session_info.support_private_msg 为 False 时直接返回 []，不走队列
       ↓
PlatformAPI.send_private_msg(session_info, user_id, message)
       ↓ (跨进程；wait=True 才拿得到消息 ID)
ContextManager.send_private_msg(session_info, user_id, message)
   - derive_private_session() 把场景换成私聊，再复用自家 send_message
       ↓
平台 SDK 发送消息 → 消息 ID 列表（空列表 = 发送失败）
```

入站会话记录 `owner_peer_id`，需要访问原始平台 SDK 上下文的删除消息、反应、hold/release 等操作会
直投该 Client 实例。Server 创建的主动会话不绑定 owner，按场景键在同 service 的 ready Client 中
稳定分流。实例进入 `maintenance` 或 `draining` 后立即退出新路由，正常停止或租约过期会将发往该
实例的未完成直投任务终结为 unavailable。

### JobQueue 信号广播与多实例边界

JobQueue 信号不是对外发送的聊天消息，也不是一条供多个消费者竞争的共享记录。发送端使用
`PeerSelector` 按 `peer_id / node_id / role / service / capability` 选择目标，并为每个 ready 实例创建
独立逻辑投递；数据库后端会为每个目标创建单独队列行。所有投递共享一个 `correlation_id`，每个目标分别
领取、执行和 ACK；批量发送逐项区分后端明确接受、拒绝和接受状态未知的目标，可选择只取得投递结果，
或汇总所有目标的执行结果与错误。

广播是在线实例快照，不提供离线重放。配置、模块版本等必须最终一致的状态应持久化 version / epoch，
进程启动后对账，信号只用于加速刷新。

JobQueue 层已为同类型多 Client / Server 预留实例发现、anycast、稳定分流、回源和摘流；外围仍需：

- Scheduler leader election 或分布式去重，避免每个 Server 重复执行单例任务；
- 模块加载和热重载的集群 epoch 与独立协调者，避免 Queue handler 等待广播 ACK 时形成维护死锁；
- Server 进程内会话和临时状态的故障迁移或明确失效策略；
- 同平台账号多 Client 的 SDK 入口分片、主备租约或重复事件去重；
- 生产环境使用适合多进程竞争的数据库，并为有副作用的 handler 设计幂等键。

---

## 13. 目录结构参考

```
akari-bot-monorepo-test/
├── pyproject.toml            # workspace 根：成员声明、内部版本来源、全仓工具配置
├── uv.lock                   # 全仓唯一锁文件，对全部成员联合求解
├── bot.py / tester.py        # 兼容层，分别转发到 core 入口与 akaribot.testing.runner
├── conftest.py               # pytest 前端引导
├── requirements.txt          # uv export 生成的依赖清单
│
├── packages/                 # 全部成员包
│   ├── akari-bot-core/       # akaribot.core 与内置模块 akaribot.modules.core
│   │   ├── pyproject.toml
│   │   ├── tests/            # 包内用例
│   │   └── akaribot/
│   │       ├── core/         # 核心框架
│   │       │   ├── builtins/ # bot/ message/ session/ parser/ converter/ temp/ types/ utils/ filter/ hooks/
│   │       │   ├── api/      # 模块面与适配器面的公共 API 门面
│   │       │   ├── entrypoints/  # run/ config/ db/ modules/ peers/ registry
│   │       │   ├── queue/    # JobQueue、Peer RPC 与数据库/WebSocket 后端
│   │       │   ├── server/   # Server 进程（run.py / init.py / terminate.py）
│   │       │   ├── client/   # 客户端侧公共逻辑
│   │       │   ├── config/   # 配置系统（base/ core/ jobqueue/ scan/ migration）
│   │       │   ├── database/ # 数据库系统（models.py / local.py / base.py / migrations/）
│   │       │   ├── types/    # Module / Command 类型定义
│   │       │   ├── constants/# 路径、版本、默认值、异常
│   │       │   ├── locales/  # 核心自身的 i18n
│   │       │   ├── scripts/  # 数据库转换、资源迁移等脚本
│   │       │   ├── utils/    # 工具函数（cooldown、dirty_check、web_render、game 等）
│   │       │   ├── component.py / loader.py   # module() 注册函数与 ModulesManager
│   │       │   ├── registry.py / paths.py     # 包发现层与实例目录抽象
│   │       │   ├── module_runtime.py / scheduler.py / logger.py
│   │       │   ├── i18n.py / alive.py / exports.py / smtp.py / version.py
│   │       │   └── ...
│   │       └── modules/core/ # 随 core 分发的内置模块
│   │           ├── common_tools/  # help、about、bind、merge、petal、setup 等
│   │           ├── admin_tools/   # admin、alias、prefix、modules、mute、locale
│   │           ├── su_tools/      # config、update、restart、post、purge、webrender 等
│   │           ├── hooks/         # 消息钩子：tos、typo、routing、telemetry、retired
│   │           └── manifest.toml
│   ├── akari-bot-testing/    # akaribot.testing：自研测试框架与运行器
│   │   └── akaribot/testing/  # runner.py tester.py decorator.py expectations.py mock/ junit.py
│   ├── akari-bot-cli/        # akaribot.cli：实例管理 CLI 与 TUI
│   │   └── akaribot/cli/ # main.py instance.py venv.py commands/ tui/
│   ├── akari-bot-html2text/  # html2text 的内嵌分发副本
│   ├── modules/              # akari-bot-module-<名>，各一个分发
│   └── adapters/             # akari-bot-adapter-<平台>，各一个分发
│
├── tests/                    # 跨包用例与共享夹具
│   ├── unit/                 # 单元测试
│   ├── integration/          # 集成测试
│   ├── fixtures/             # HTTP 与 WebRender fixture
│   ├── capture_*.py          # fixture 录制脚本
│   └── run_one.py            # 单个用例入口
├── tools/                    # 门禁脚本（lint_boundaries / lint_comments / check_versions 等）
├── templates/module/         # akaribot new module 的脚手架模板
├── docs/                     # 迁移与使用文档
├── generated_docs/           # 拆分设计与决策记录
├── example/new_module/       # 模块示例
├── assets/                   # 随实例提供的只读资源
├── config/ database/ data/ cache/ logs/   # 实例目录（扁平布局）
└── dist/                     # 构建产物（wheel 与 sdist）
```

> **注意**：`akaribot.core` 下不存在 `parser/`、`loader/`、`unit_test/` 这类占位目录，真实实现分别在 `akaribot/core/builtins/parser/`、`akaribot/core/loader.py`、`akaribot/testing/`。跨包导入一律书写以 `akaribot.` 开头的完整路径；顶层路径 `core/`、`bots/`、`modules/` 不是导入路径的一部分。
