# 全仓可读文本审核稿 · 第 01 册 / 共 20 册

覆盖 U000001–U000392，17 个文件、392 个单元、35,782 字符。全稿 13,993 个单元、1,032 个文件、689,842 字符。

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
| `.agents/skills/akaribot-dev/SKILL.md` | 17 | U000001–U000017 | 2,163 |
| `.agents/skills/akaribot-dev/scripts/validate_skill.py` | 1 | U000018–U000018 | 43 |
| `.github/PULL_REQUEST_TEMPLATE.md` | 9 | U000019–U000027 | 363 |
| `.github/scripts/build_copy_files.py` | 1 | U000028–U000028 | 103 |
| `.github/workflows/binary-build.yml` | 8 | U000029–U000036 | 1,005 |
| `.github/workflows/build-and-publish-docker.yml` | 1 | U000037–U000037 | 58 |
| `.github/workflows/clean-room.yml` | 2 | U000038–U000039 | 148 |
| `.github/workflows/publish-testpypi.yml` | 9 | U000040–U000048 | 714 |
| `.github/workflows/run-builtin-tester.yml` | 16 | U000049–U000064 | 1,760 |
| `.pre-commit-config.yaml` | 2 | U000065–U000066 | 171 |
| `AGENTS.md` | 106 | U000067–U000172 | 8,269 |
| `CONTRIBUTING.md` | 85 | U000173–U000257 | 5,595 |
| `README.md` | 31 | U000258–U000288 | 1,627 |
| `bot.py` | 1 | U000289–U000289 | 86 |
| `conftest.py` | 2 | U000290–U000291 | 103 |
| `docs/migrating-to-packages.md` | 47 | U000292–U000338 | 4,452 |
| `docs/package-docs.md` | 54 | U000339–U000392 | 9,122 |

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
<<< UNIT U000001 | md-heading | .agents/skills/akaribot-dev/SKILL.md:6-6 | ctx=AkariBot 开发 >>>
# AkariBot 开发
<<< END U000001 >>>
<<< UNIT U000002 | md-paragraph | .agents/skills/akaribot-dev/SKILL.md:8-9 | ctx=AkariBot 开发 >>>
完整手册是随源码维护的文档页（`packages/*/akaribot/**/docs/`），也是文档站点的内容来源。本技能只提供
入口与必须遵守的规则，不复制页面内容。
<<< END U000002 >>>
<<< UNIT U000003 | md-heading | .agents/skills/akaribot-dev/SKILL.md:11-11 | ctx=开始工作 >>>
## 开始工作
<<< END U000003 >>>
<<< UNIT U000004 | md-list | .agents/skills/akaribot-dev/SKILL.md:13-16 | ctx=开始工作 >>>
1. 阅读仓库根目录 `AGENTS.md`，了解常用命令、架构脉络、陷阱与提交约定。
2. 按下表找到对应文档页。涉及多个领域时请阅读对应页面。
3. 修改代码前先检查 `tests/` 与包内 `tests/` 是否已覆盖该行为。
4. 提交前运行五道检查，见下方“高频命令”与开发流程页。
<<< END U000004 >>>
<<< UNIT U000005 | md-heading | .agents/skills/akaribot-dev/SKILL.md:18-18 | ctx=文档路由 >>>
## 文档路由
<<< END U000005 >>>
<<< UNIT U000006 | md-table | .agents/skills/akaribot-dev/SKILL.md:20-33 | ctx=文档路由 >>>
| 任务 | 文档页 |
| --- | --- |
| 代码结构、进程拓扑、启动、退出码、消息链路 | `packages/akari-bot-core/akaribot/core/docs/architecture.md` |
| 配置表、模板、只读约束、配置版本 | `packages/akari-bot-core/akaribot/core/docs/config.md` |
| 数据库、union 数据、迁移、热重载 | `packages/akari-bot-core/akaribot/core/docs/database.md` |
| JobQueue 后端、节点、RPC 与信号 | `packages/akari-bot-core/akaribot/core/docs/queue.md` |
| 新建模块、命令解析、hook、权限、工具 | `packages/akari-bot-core/akaribot/core/docs/module-development.md` |
| 消息链、消息元素、等待接口、执行锁 | `packages/akari-bot-core/akaribot/core/docs/message-api.md` |
| 角色与权限判定 | `packages/akari-bot-core/akaribot/core/docs/permissions.md` |
| 新建适配器、Features、ContextManager、多实例 | `packages/akari-bot-core/akaribot/core/docs/adapter-development.md` |
| 公开 API 与版本约束 | `packages/akari-bot-core/akaribot/core/docs/public-api.md` |
| i18n 与占位符 | `packages/akari-bot-core/akaribot/core/docs/i18n.md`、`packages/akari-bot-core/akaribot/core/docs/placeholders.md` |
| 测试框架与用例写法 | `packages/akari-bot-testing/akaribot/testing/doc/index.md`、`packages/akari-bot-testing/akaribot/testing/doc/writing-tests.md` |
| 环境、检查、基准、分支与提交、文档工具链 | `packages/akari-bot-core/akaribot/core/docs/development-workflow.md` |
<<< END U000006 >>>
<<< UNIT U000007 | md-heading | .agents/skills/akaribot-dev/SKILL.md:35-35 | ctx=强制规则 >>>
## 强制规则
<<< END U000007 >>>
<<< UNIT U000008 | md-list | .agents/skills/akaribot-dev/SKILL.md:37-37 | ctx=强制规则 >>>
- 面向用户的固定文案一律使用 `I18NContext("key", **参数)`，且只在所属包的 `locales/zh_cn.json` 中创建条目。
<<< END U000008 >>>
<<< UNIT U000009 | md-paragraph | .agents/skills/akaribot-dev/SKILL.md:38-38 | ctx=强制规则 >>>
  其他语言由 Weblate 提交，不得改动或补译。
<<< END U000009 >>>
<<< UNIT U000010 | md-list | .agents/skills/akaribot-dev/SKILL.md:39-40 | ctx=强制规则 >>>
- 新增配置字段须在模板类中声明，并在 `config.comments.<表名>.<字段名>` 中补充注释。
- 模块与适配器只导入 `akaribot.core.api`（适配器额外导入 `akaribot.core.api.adapters`）。
<<< END U000010 >>>
<<< UNIT U000011 | md-paragraph | .agents/skills/akaribot-dev/SKILL.md:41-41 | ctx=强制规则 >>>
  核心内部出现循环依赖时通过 `akaribot.core.exports` 处理。
<<< END U000011 >>>
<<< UNIT U000012 | md-list | .agents/skills/akaribot-dev/SKILL.md:42-42 | ctx=强制规则 >>>
- union 数据按 `union_id` 划分归属，模型须声明 `union_scope`。跨表写入同一 union 时使用 `union_mutation()` 与
<<< END U000012 >>>
<<< UNIT U000013 | md-paragraph | .agents/skills/akaribot-dev/SKILL.md:43-43 | ctx=强制规则 >>>
  `select_for_update()` 包裹事务。
<<< END U000013 >>>
<<< UNIT U000014 | md-list | .agents/skills/akaribot-dev/SKILL.md:44-49 | ctx=强制规则 >>>
- `Features(...)` 在 `features.py` 创建实例，不在 `ContextManager` 中子类化。
- `SessionInfo` 必须可序列化，只包含基础类型。构造时传入完整的 `ctx_slot`、`message_id`、`reply_id` 等字段。
- 跨进程通信只通过 JobQueue 进行。CLI 与 core 之间只通过子进程交互。
- 全量测试需设置 `CI=1`，常规测试轮次的失败清单必须与基准按名称一一对应，详见开发流程页。
- 注释、文档与配置说明只描述当前状态，使用中文书面语并遵守排版检查规则。
- 不擅自提交。新功能分支使用 `dev/` 前缀，修复分支使用 `fix/` 前缀。
<<< END U000014 >>>
<<< UNIT U000015 | md-heading | .agents/skills/akaribot-dev/SKILL.md:51-51 | ctx=高频命令 >>>
## 高频命令
<<< END U000015 >>>
<<< UNIT U000016 | md-heading | .agents/skills/akaribot-dev/SKILL.md:64-64 | ctx=维护 >>>
## 维护
<<< END U000016 >>>
<<< UNIT U000017 | md-paragraph | .agents/skills/akaribot-dev/SKILL.md:66-67 | ctx=维护 >>>
文档页是唯一来源。改动行为后应先更新对应页面，再核对本页路由表是否仍然准确。不要在本技能内重复页面
内容。修改本文件后运行：
<<< END U000017 >>>
<<< UNIT U000018 | py-comment | .agents/skills/akaribot-dev/scripts/validate_skill.py:45-45 >>>
# SKILL.md 必须保留的规则。改动技能正文时若移除了其中任意一条，检查会失败。
<<< END U000018 >>>
<<< UNIT U000019 | md-heading | .github/PULL_REQUEST_TEMPLATE.md:1-1 | ctx=描述 >>>
## 描述
<<< END U000019 >>>
<<< UNIT U000020 | md-heading | .github/PULL_REQUEST_TEMPLATE.md:4-4 | ctx=变更类型（可多选） >>>
## 变更类型（可多选）
<<< END U000020 >>>
<<< UNIT U000021 | md-list | .github/PULL_REQUEST_TEMPLATE.md:6-10 | ctx=变更类型（可多选） >>>
- [ ] 新功能
- [ ] 修复
- [ ] 文档 / 样式
- [ ] 重构 / 性能优化
- [ ] 其他
<<< END U000021 >>>
<<< UNIT U000022 | md-heading | .github/PULL_REQUEST_TEMPLATE.md:12-12 | ctx=风险 >>>
## 风险
<<< END U000022 >>>
<<< UNIT U000023 | md-list | .github/PULL_REQUEST_TEMPLATE.md:14-16 | ctx=风险 >>>
- [ ] **破坏性变更**（Breaking change）
  - [ ] 必须更改**配置文件**
  - [ ] 必须迁移**数据库**
<<< END U000023 >>>
<<< UNIT U000024 | md-heading | .github/PULL_REQUEST_TEMPLATE.md:20-20 | ctx=相关 Issue >>>
## 相关 Issue
<<< END U000024 >>>
<<< UNIT U000025 | md-heading | .github/PULL_REQUEST_TEMPLATE.md:25-25 | ctx=截图 / 演示 >>>
## 截图 / 演示
<<< END U000025 >>>
<<< UNIT U000026 | md-heading | .github/PULL_REQUEST_TEMPLATE.md:29-29 | ctx=检查清单 >>>
## 检查清单
<<< END U000026 >>>
<<< UNIT U000027 | md-list | .github/PULL_REQUEST_TEMPLATE.md:31-34 | ctx=检查清单 >>>
- [ ] 我确定我的变更符合[贡献指南](https://github.com/Teahouse-Studios/akari-bot/blob/master/CONTRIBUTING.md)中的项目规范。
- [ ] 我的变更在本地经过了良好的测试，没有产生明显错误。
- [ ] 我确定在此 PR 中披露了可能的破坏性变更。
- [ ] 我已解决所有的合并冲突。
<<< END U000027 >>>
<<< UNIT U000028 | py-comment | .github/scripts/build_copy_files.py:21-22 >>>
# 整个 packages/modules 一并复制，除模块源码外还包含各包的 pyproject.toml 与 assets/。
# 可写数据已不在包目录内（见模块顶部说明），故此处无需再区分运行时产物。
<<< END U000028 >>>
<<< UNIT U000029 | cfg-comment | .github/workflows/binary-build.yml:3-5 >>>
# T6.5(a) 只打包 CLI（参数解析、TUI、子进程调度、HTTP 与 TOML 读写），机器人本体不打包进二进制文件。
# 运行时由 CLI 通过子进程调用实例 venv 里的 `python -m akaribot.core.entrypoints.run`，因此 multiprocessing、
# Tortoise ORM、七个平台 SDK 及各模块依赖都不必打包，打包范围仅限 CLI 自身依赖，构建也更稳定。
<<< END U000029 >>>
<<< UNIT U000030 | cfg-comment | .github/workflows/binary-build.yml:40-40 >>>
          # 只安装 CLI 自身的依赖，不引入 core、模块与平台 SDK，从而把打包范围限定在 CLI 自身。
<<< END U000030 >>>
<<< UNIT U000031 | cfg-comment | .github/workflows/binary-build.yml:46-47 >>>
          # Nuitka 在后续步骤中会使用 PATH 中的 python。不切换到工作区 venv 时它无法获取依赖，
          # 会报 "failed to locate package 'akaribot.cli'"。
<<< END U000031 >>>
<<< UNIT U000032 | cfg-comment | .github/workflows/binary-build.yml:57-58 >>>
          # uv 创建的 venv 不带 pip，而后续步骤会用 `pip install` 安装 Nuitka。此处需先向 venv 补充安装
          # pip，否则命令会调用 PATH 更靠后的系统 pip 将 Nuitka 安装到系统解释器中，导致 `python -m nuitka` 找不到模块。
<<< END U000032 >>>
<<< UNIT U000033 | cfg-comment | .github/workflows/binary-build.yml:66-67 >>>
          # 内置 uv，供 CLI 创建与维护实例 venv，用户机器上不必预先安装。复制时直接使用包内最终文件名，
          # 省去 include-data-files 的重命名表达式（Windows 的可执行后缀必须是 .exe）。
<<< END U000033 >>>
<<< UNIT U000034 | cfg-comment | .github/workflows/binary-build.yml:84-85 >>>
          # 缺少包内资源会让 TUI 在用户机器上崩溃（textual 的 .tcss、rich 的内置主题）。手工列举必然
          # 会遗漏，唯一可靠的办法是在不含 Python 的环境中运行基本检查。本仓库尚无该环境，属于已知限制。
<<< END U000034 >>>
<<< UNIT U000035 | cfg-comment | .github/workflows/binary-build.yml:92-93 >>>
          # CLI 包自身的资源已在上方按目录明确声明，这里重复声明只会触发 "Duplicate data file" 告警。
          # i18n 包的 locales 与其他第三方包的数据文件由 package-data 收集。
<<< END U000035 >>>
<<< UNIT U000036 | cfg-comment | .github/workflows/binary-build.yml:111-111 >>>
          # 打包后 sys.executable 指向二进制文件自身，故此处只验证 CLI 自身是否可用以及包内资源能否正常加载。
<<< END U000036 >>>
<<< UNIT U000037 | cfg-comment | .github/workflows/build-and-publish-docker.yml:84-84 >>>
          # 稳定版仅推送不可变版本标签，避免旧 tag 重新运行或并发构建完成顺序不同导致 latest 回退。
<<< END U000037 >>>
<<< UNIT U000038 | cfg-comment | .github/workflows/clean-room.yml:3-4 >>>
# T6.6 用正式发布的 wheel 包验证用户的实际安装体验。workspace 的开发阶段覆盖会忽略内部版本约束，
# 只有从 wheel 安装才会真正经过依赖解析器，故发布前必须执行这项检查。
<<< END U000038 >>>
<<< UNIT U000039 | cfg-comment | .github/workflows/clean-room.yml:51-51 >>>
          # T6.1 输出本次改动涉及的包名矩阵。core 或全局文件改动时标记为 full。
<<< END U000039 >>>
<<< UNIT U000040 | cfg-comment | .github/workflows/publish-testpypi.yml:3-4 >>>
# 首次发布候选版本的演练流程会一次构建全部 workspace 包，按顺序上传至 TestPyPI，再从 TestPyPI 下载真实分发文件，
# 并在 Linux/Windows/macOS 上执行干净环境安装验证。仅写入 TestPyPI，不涉及 PyPI、gh-pages 与 Release。
<<< END U000040 >>>
<<< UNIT U000041 | cfg-comment | .github/workflows/publish-testpypi.yml:100-101 >>>
    # Token 模式下在单个 job 中按依赖顺序使用 twine 逐个上传，避免 57 个 matrix job 逐一触发
    # environment 审批。Trusted Publishing 使用下方的独立 matrix job（OIDC 需要由 action 逐次签发）。
<<< END U000041 >>>
<<< UNIT U000042 | cfg-comment | .github/workflows/publish-testpypi.yml:127-127 >>>
        # 发布脚本由 runner 的 python 直接执行，需把 packaging 与 twine 安装到同一环境。
<<< END U000042 >>>
<<< UNIT U000043 | cfg-comment | .github/workflows/publish-testpypi.yml:163-163 >>>
    # 供官方仓库正式演练使用，为 57 个项目配置 pending publisher 后，由 action 逐次签发 OIDC 令牌。
<<< END U000043 >>>
<<< UNIT U000044 | cfg-comment | .github/workflows/publish-testpypi.yml:225-225 >>>
    # 不经过任何外部仓库，直接将本批产物构建为 PEP 503 静态索引并按索引地址完整安装，以验证依赖解析、元数据与 entry points。
<<< END U000044 >>>
<<< UNIT U000045 | cfg-comment | .github/workflows/publish-testpypi.yml:251-251 >>>
          # 服务由构建进程自行启动，服务根目录即刚生成的索引目录，不依赖相对路径解析。
<<< END U000045 >>>
<<< UNIT U000046 | cfg-comment | .github/workflows/publish-testpypi.yml:264-264 >>>
          # 验证一次产物下载，避免索引可访问但文件无法下载时，后续安装只报出难以定位的 404 错误。
<<< END U000046 >>>
<<< UNIT U000047 | cfg-comment | .github/workflows/publish-testpypi.yml:326-326 >>>
          # 同一次运行刚创建的项目在索引 JSON 上存在 CDN 延迟，需等待同步后再判断哪些包尚未上传。
<<< END U000047 >>>
<<< UNIT U000048 | cfg-comment | .github/workflows/publish-testpypi.yml:345-345 >>>
          # 部分上传阶段只运行不依赖缺失包的组合。全部就绪后再运行完整矩阵。
<<< END U000048 >>>
<<< UNIT U000049 | cfg-comment | .github/workflows/run-builtin-tester.yml:35-36 >>>
          # --locked 会重新求解，是检查 workspace 依赖冲突的唯一位置。不得改为 --frozen
          # 或 pip install，否则 PR 阶段将无法发现依赖冲突且不会报错（见 T4.9、CONTRIBUTING.md）。
<<< END U000049 >>>
<<< UNIT U000050 | cfg-comment | .github/workflows/run-builtin-tester.yml:42-42 >>>
          # PR 仅检查相对目标分支的新增与修改行，推送与手动触发则检查全部文件。
<<< END U000050 >>>
<<< UNIT U000051 | cfg-comment | .github/workflows/run-builtin-tester.yml:58-58 >>>
          # 分层检查沿用与注释检查相同的范围判定，PR 对比目标分支，推送时对比变更前的提交。
<<< END U000051 >>>
<<< UNIT U000052 | cfg-comment | .github/workflows/run-builtin-tester.yml:74-75 >>>
          # workspace 覆盖会丢弃内部依赖的版本约束，但发布的 wheel 仍会保留这些约束。
          # uv lock 无法检测此类约束冲突，因此单独设置一道检查（见 T4.8）。
<<< END U000052 >>>
<<< UNIT U000053 | cfg-comment | .github/workflows/run-builtin-tester.yml:79-80 >>>
        # 版本号属于发布元数据而非行为正确性，tester 的结论应只由代码与测试决定。
        # 违规项仍会输出供发布前确认，但不会阻断本 job（重复版本由 PyPI 在发布时拒绝）。
<<< END U000053 >>>
<<< UNIT U000054 | cfg-comment | .github/workflows/run-builtin-tester.yml:84-86 >>>
          # 包内有源码改动但未更新 version 时会发出提示。提交信息最后一段包含独立的 Skip-Version
          # trailer 时按声明范围豁免（true 为全部成员，逗号分隔时只豁免列出的成员）。
          # 正文里顺带提到该标记不视为声明，避免解释功能的一句话意外关闭整个提交范围的检查。
<<< END U000054 >>>
<<< UNIT U000055 | cfg-comment | .github/workflows/run-builtin-tester.yml:102-103 >>>
          # 静态检查覆盖整个仓库，格式化则只检查本次改动的文件。历史文件是否已格式化与本轮改动无关，
          # 不应阻断无关提交（否则任何人的推送都会因他人的旧文件而检查失败）。
<<< END U000055 >>>
<<< UNIT U000056 | cfg-comment | .github/workflows/run-builtin-tester.yml:143-145 >>>
          # runner 发现任何失败就以非 0 退出，而本仓库有 4 个用例失败（见 tools/test_baseline.txt）。
          # 若直接由退出码判定步骤成败，本轮会立即失败，后续的“只读包目录”一轮就不会执行。
          # 故此处只记录退出码，由下一步通过对比失败的用例清单作出最终判定。不使用 `|| true`，也不只比较数量。
<<< END U000056 >>>
<<< UNIT U000057 | cfg-comment | .github/workflows/run-builtin-tester.yml:163-167 >>>
          # 包目录在只读挂载与 wheel 安装下都不可写，此处通过只读权限模拟该约束。
          # 只覆盖测试触及的代码路径。未被测试覆盖的下载路径需通过人工复核确认，
          # 见 generated_docs/monorepo_refactor_prep.md 的 P2 记录。
          # 检查以整个 packages/ 目录作为扫描根目录。如果硬编码 core modules 路径，包再次拆分或重命名时
          # 就会漏掉检查而不报错。使用单一根目录不受包增减影响，代价是适配器目录也会一并设为只读。
<<< END U000057 >>>
<<< UNIT U000058 | cfg-comment | .github/workflows/run-builtin-tester.yml:179-179 >>>
          # 只读挂载下可能多出写入磁盘类失败，故单独维护一份基准清单。两轮测试都按名称对比失败清单，且两份清单都只允许减少。
<<< END U000058 >>>
<<< UNIT U000059 | cfg-comment | .github/workflows/run-builtin-tester.yml:193-195 >>>
    # 文档站在 tester 通过后构建全部包的文档并发布到 GitHub Pages，只在默认分支的推送与手动触发
    # 时发布。PR 与其他分支的构建产物不属于发布内容，也不应获得 Pages 权限。
    # 仓库 Settings → Pages 的 Source 须为 GitHub Actions。Pages 尚未启用时，`enablement: true` 会自动启用它。
<<< END U000059 >>>
<<< UNIT U000060 | cfg-comment | .github/workflows/run-builtin-tester.yml:218-218 >>>
          # 主题是 submodule，构建时需复制它的 theme_dir，并依据其中的 docs-theme.json 确定依赖与 VitePress 版本。
<<< END U000060 >>>
<<< UNIT U000061 | cfg-comment | .github/workflows/run-builtin-tester.yml:234-234 >>>
          # 主题清单要求 Node >= 22.12，引擎据此选择 VitePress 2 及其依赖。
<<< END U000061 >>>
<<< UNIT U000062 | cfg-comment | .github/workflows/run-builtin-tester.yml:252-252 >>>
          # 项目站点的基础路径由此确定，构建阶段写入侧栏与资源地址，构建后若修改需重新构建。
<<< END U000062 >>>
<<< UNIT U000063 | cfg-comment | .github/workflows/run-builtin-tester.yml:254-254 >>>
          # 非托管实例使用系统解释器运行 core 入口，此处将其指定为工作区 venv，避免 runner 上其他 python3 优先被调用。
<<< END U000063 >>>
<<< UNIT U000064 | cfg-comment | .github/workflows/run-builtin-tester.yml:257-257 >>>
          # 引擎以“实例”为单位工作，这里只需要一个最小的实例根目录，产物放在它的 cache/docs/site。
<<< END U000064 >>>
<<< UNIT U000065 | cfg-comment | .pre-commit-config.yaml:17-17 >>>
          # 只检查暂存区新增与修改的行，规则见 generated_docs/monorepo_refactor_prep.md §8。
<<< END U000065 >>>
<<< UNIT U000066 | cfg-comment | .pre-commit-config.yaml:25-26 >>>
          # 分层检查要求模块不得导入平台适配器，core 不得导入模块或适配器。
          # 与 comment-lint 同理，只检查改动行，避免既有 B1 违规项阻塞提交。
<<< END U000066 >>>
<<< UNIT U000067 | md-paragraph | AGENTS.md:3-4 | ctx=AGENTS.md >>>
本文件面向在本仓库工作的 AI 代理与协作者。仓库采用 uv workspace 结构，core、模块与适配器各自独立打包发布，
运行时通过 entry points 发现。
<<< END U000067 >>>
<<< UNIT U000068 | md-heading | AGENTS.md:6-6 | ctx=深入文档 >>>
## 深入文档
<<< END U000068 >>>
<<< UNIT U000069 | md-paragraph | AGENTS.md:8-10 | ctx=深入文档 >>>
各领域的完整手册是随源码维护在 `packages/*/akaribot/**/docs/` 下的文档页。它们覆盖架构与进程拓扑、配置、
数据库、队列、模块与适配器开发、消息 API、i18n、测试与开发流程，也是 `akaribot docs build` 的站点
内容来源。
<<< END U000069 >>>
<<< UNIT U000070 | md-paragraph | AGENTS.md:12-13 | ctx=深入文档 >>>
**本文件只记录高频命令、跨文件才能看清的架构脉络与强制约定**。需要 API 细节时请查阅对应页面，
不要在这里重复。`.agents/skills/akaribot-dev/SKILL.md` 是这些页面的路由表。
<<< END U000070 >>>
<<< UNIT U000071 | md-heading | AGENTS.md:15-15 | ctx=常用命令 >>>
## 常用命令
<<< END U000071 >>>
<<< UNIT U000072 | md-paragraph | AGENTS.md:32-34 | ctx=常用命令 >>>
CLI：`.venv/bin/akaribot <子命令> --help`（init / run / test / module / config / adapter / db /
instance / service / venv / logs / doctor / new / tui / migrate / docs）。`migrate legacy` 将旧版布局的部署
迁移到新实例目录。`logs` 读取实例的日志文件（界面日志页复用同一套解析规则）。
<<< END U000072 >>>
<<< UNIT U000073 | md-heading | AGENTS.md:36-36 | ctx=测试编写规范 >>>
### 测试编写规范
<<< END U000073 >>>
<<< UNIT U000074 | md-paragraph | AGENTS.md:38-38 | ctx=测试编写规范 >>>
测试数量本身也是维护成本，每个用例都要随代码演进同步修改，冗余用例会拖慢 CI 并掩盖真正的失败信号。**新增测试前先问“删除它，哪个真实缺陷会漏掉”**，如果答不出来就不要编写。
<<< END U000074 >>>
<<< UNIT U000075 | md-list | AGENTS.md:40-44 | ctx=测试编写规范 >>>
- 本地只运行与改动相关的入口（`tests/run_one.py <包内用例路径> [入口名]`），全量测试留给 CI 执行。
- **必须设置 `CI=1`**，否则无 `Expectation` 的用例会调用 `input()` 等待人工复核。设置 `CI=1` 时会转为 SKIP 并输出 `junit.xml`。
- 测试不读取本机配置，`akaribot.testing` 会将配置模板部署到临时目录（`AKARI_CONFIG_PATH`）再叠加测试覆盖项。
- 需要非默认配置值时，使用 `mock_config(CoreConfig, 字段=值)` 在进程内覆盖，无需读写配置文件，且字段必须是模板类中已声明的项。
- 测试使用 `akaribot/testing/mock/parser.py` 的简化解析器，不检查模块是否启用，并将测试发送者设为 superuser。“测试通过”不代表命令在真实平台上可以正常触发。HTTP 由 `tests/fixtures/http/` 录制回放。
<<< END U000075 >>>
<<< UNIT U000076 | md-list | AGENTS.md:46-57 | ctx=测试编写规范 >>>
- **先搜索再编写。** 新增前用 `grep` 检查现有测试是否已覆盖同一行为。已覆盖则扩展原用例，不要新建用例。
- **改动行为时应同步替换旧测试**，不要新旧并存。**删除功能必须同时删除对应测试与 `tests/fixtures/` 中不再被引用的 fixture**。
- **只检查可观察行为**：返回值、发出的消息、持久化结果、权限与安全判定。不要检查 mock 的调用次数、私有属性与私有函数、日志原文。
- **无需测试的内容**：构造器与默认值、常量、getter/setter、标准库或第三方库的直接转发、仅检查“不抛出异常”的基本检查用例。
- **一个行为一个用例。** 同一行为的不同输入变体应在同一用例内通过循环或参数表覆盖，不要每个变体注册一个 `tester.test`。修复缺陷时，只在现有测试未覆盖该场景的情况下补充回归用例，并放入该功能原有的测试里。
- **不编写重复的对称用例。** 代码路径相同的对称场景（如发送者侧与目标侧、群聊与私聊、各平台各一份“缺失媒体被跳过”）只需测试其一。只有代码路径确实分叉时才分别覆盖。
- **必须保留、不得为精简而删除**：安全与权限判定、数据迁移与一致性、并发与锁、以及每个功能的主路径。
- **每个 `_test_` 函数必须被 `tester.test` 注册**，未注册的函数永远不会运行，属于无效代码。
- **按主题组织文件。** 一个功能（模块、适配器、子系统）对应一个测试文件，在其内追加。不要新建 `test_more_*` / `test_*_more` / `test_*_fixes` 之类的零散补充文件。包内用例放在 `packages/<包名>/tests/`，命名与根目录 `tests/` 保持一致。
- **集成测试**（位于根目录 `tests/integration/`）每个命令只保留一条主路径加必要的、行为不同的错误路径。能用纯函数单元测试覆盖的逻辑不要放入集成测试，因为它们依赖录制的 HTTP fixture。
- 用例描述（`tester.test` 的第二个参数）描述被验证的行为，不描述实现细节。测试中同样遵循“只描述当前状态”的注释约定。
- 不要使用固定 `sleep` 等待。需要超时时使用 `akaribot.testing.timing.TIME_SCALE`。
<<< END U000076 >>>
<<< UNIT U000077 | md-heading | AGENTS.md:59-59 | ctx=架构脉络 >>>
## 架构脉络
<<< END U000077 >>>
<<< UNIT U000078 | md-list | AGENTS.md:72-72 | ctx=架构脉络 >>>
- `akaribot`、`akaribot.modules`、`akaribot.adapters`、`akaribot.assets` 是 **PEP 420 命名空间目录**
<<< END U000078 >>>
<<< UNIT U000079 | md-paragraph | AGENTS.md:73-73 | ctx=架构脉络 >>>
  （不得有 `__init__.py`）。`akaribot.core`、`akaribot.testing`、各模块/适配器/资源包是常规包。
<<< END U000079 >>>
<<< UNIT U000080 | md-list | AGENTS.md:74-74 | ctx=架构脉络 >>>
- 包发现通过 entry points（`akaribot.modules` / `akaribot.adapters`）完成，目录扫描仅作备用。每个包在
<<< END U000080 >>>
<<< UNIT U000081 | md-paragraph | AGENTS.md:75-75 | ctx=架构脉络 >>>
  各自的导入包目录下都有 `manifest.toml`，locales、assets、migrations 都相对该文件所在目录解析。
<<< END U000081 >>>
<<< UNIT U000082 | md-list | AGENTS.md:76-77 | ctx=架构脉络 >>>
- 模块只应导入 `akaribot.core.api` 的公开接口。适配器另有 `akaribot.core.api.adapters`。
- CLI 与 core 之间**只通过子进程**通信，入口为 `python -m akaribot.core.entrypoints.{run,registry,config,db,peers,modules,rpc}`。
<<< END U000082 >>>
<<< UNIT U000083 | md-heading | AGENTS.md:79-79 | ctx=项目约定 >>>
## 项目约定
<<< END U000083 >>>
<<< UNIT U000084 | md-heading | AGENTS.md:81-81 | ctx=只描述当前状态 >>>
### 只描述当前状态
<<< END U000084 >>>
<<< UNIT U000085 | md-list | AGENTS.md:83-83 | ctx=只描述当前状态 >>>
- **文档、注释和配置说明只描述当前状态，不记录“从前如何”。** 不写“原本是 X，现在改为 Y”
<<< END U000085 >>>
<<< UNIT U000086 | md-paragraph | AGENTS.md:84-84 | ctx=只描述当前状态 >>>
  “已迁移到 Z”“不再使用 W”这类对照式表述，直接陈述当前的事实与约束。
<<< END U000086 >>>
<<< UNIT U000087 | md-list | AGENTS.md:85-86 | ctx=只描述当前状态 >>>
- 变更历史由 git 记录。需要解释设计取舍时，说明当前为何如此，而不是叙述它从什么演变而来。
- **例外**：为迁移历史数据而保留的兼容逻辑（旧配置表名、数据库版本升级路径、退役客户端的数据
<<< END U000087 >>>
<<< UNIT U000088 | md-paragraph | AGENTS.md:87-88 | ctx=只描述当前状态 >>>
  迁移）应当保留，并注明适用范围——这类兼容是当前行为的一部分。标注某个 API 已弃用同样属于
  陈述当前状态，可以保留。
<<< END U000088 >>>
<<< UNIT U000089 | md-heading | AGENTS.md:90-90 | ctx=注释 >>>
### 注释
<<< END U000089 >>>
<<< UNIT U000090 | md-list | AGENTS.md:92-92 | ctx=注释 >>>
- **不要为含义清楚的代码编写注释。** 注释解释“为什么”，不解释“是什么”或实现细节。只在逻辑涉及
<<< END U000090 >>>
<<< UNIT U000091 | md-paragraph | AGENTS.md:93-93 | ctx=注释 >>>
  容易引起误解的边界情况、临时变通方案（hack）、复杂算法或特定业务规则时才编写注释。
<<< END U000091 >>>
<<< UNIT U000092 | md-list | AGENTS.md:94-96 | ctx=注释 >>>
- **单条注释一般不超过三行。** 如果三行写不下，说明应当拆分函数或补充文档，不要在代码里堆砌长篇说明。
- **一律使用正式书面语**，不得出现口语化表达、语气词、感叹号或调侃。
- **不要为非公开 API 的模块、类、函数添加 docstring。** 公开 API 的 docstring 只说明用途、参数与
<<< END U000092 >>>
<<< UNIT U000093 | md-paragraph | AGENTS.md:97-97 | ctx=注释 >>>
  返回值，不复述签名已经表达的信息。
<<< END U000093 >>>
<<< UNIT U000094 | md-heading | AGENTS.md:99-99 | ctx=文档 >>>
### 文档
<<< END U000094 >>>
<<< UNIT U000095 | md-list | AGENTS.md:101-102 | ctx=文档 >>>
- 文档面向技术用户与维护者，不面向初学者。
- 只覆盖功能概述、基本使用步骤和接口实现，不逐步讲解内部工作原理。
<<< END U000095 >>>
<<< UNIT U000096 | md-heading | AGENTS.md:104-104 | ctx=包文档与文档站点 >>>
### 包文档与文档站点
<<< END U000096 >>>
<<< UNIT U000097 | md-list | AGENTS.md:106-106 | ctx=包文档与文档站点 >>>
- 每个包的导入包目录下带有 `docs/`，其中 `docs/config/global/docs.global.toml` 声明标题、简介与排序，`docs/config/docs.toml` 可覆盖默认值，Markdown 页面只记录当前行为。
<<< END U000097 >>>
<<< UNIT U000098 | md-paragraph | AGENTS.md:107-108 | ctx=包文档与文档站点 >>>
  在 pyproject 的 `[project.entry-points."akaribot.docs"]` 声明 `<key> = "<import path>"`。第三方包
  以同一方式接入，目录只包含已安装的包。
<<< END U000098 >>>
<<< UNIT U000099 | md-list | AGENTS.md:109-109 | ctx=包文档与文档站点 >>>
- 文档相关子命令为 `akaribot docs list|build|serve|deploy|status|clean`。工具链要求由主题清单确定，内置主题与
<<< END U000099 >>>
<<< UNIT U000100 | md-paragraph | AGENTS.md:110-111 | ctx=包文档与文档站点 >>>
  `akari-bot-docs-template` 各自在 `docs-theme.json` 里声明 Node.js 与 VitePress 版本范围。
  生成产物位于实例根目录的 `cache/docs/`，构建与部署记录保存在 `.docs/state.json`。
<<< END U000100 >>>
<<< UNIT U000101 | md-list | AGENTS.md:112-112 | ctx=包文档与文档站点 >>>
- 站点配置保存在实例根目录的 `docs.toml` 中。主题用 `[theme].source` 选择，外部主题只通过根目录的
<<< END U000101 >>>
<<< UNIT U000102 | md-paragraph | AGENTS.md:113-115 | ctx=包文档与文档站点 >>>
  `docs-theme.json` 声明主题目录、依赖、VitePress/Node 要求与生成选项，引擎不导入主题代码。
  本仓库的主题是 `vendor/akari-bot-docs-template` submodule，克隆后须初始化 submodule。
  部署登录信息只从环境变量读取，不写入配置、日志或状态文件。
<<< END U000102 >>>
<<< UNIT U000103 | md-list | AGENTS.md:116-116 | ctx=包文档与文档站点 >>>
- 文档只使用简体中文，并只描述当前状态。命令、配置字段与默认值以源码为准。跨包链接可填写源码相对路径，
<<< END U000103 >>>
<<< UNIT U000104 | md-paragraph | AGENTS.md:117-117 | ctx=包文档与文档站点 >>>
  生成器会转换为站点 URL。
<<< END U000104 >>>
<<< UNIT U000105 | md-list | AGENTS.md:118-118 | ctx=包文档与文档站点 >>>
- 模块页的属性卡来自 `docs/config/global/docs.global.toml` 的 `[[meta.modules]]`，由生成器自动注入。`ModuleMeta`、
<<< END U000105 >>>
<<< UNIT U000106 | md-paragraph | AGENTS.md:119-120 | ctx=包文档与文档站点 >>>
  `NoticeBox`、`CommandUsage` 组件的正式位置是 `akari-bot-docs-template`，内置主题保留同名回退实现。
  正文仍以 Markdown 为主。
<<< END U000106 >>>
<<< UNIT U000107 | md-heading | AGENTS.md:122-122 | ctx=i18n 与本地化 >>>
### i18n 与本地化
<<< END U000107 >>>
<<< UNIT U000108 | md-list | AGENTS.md:124-124 | ctx=i18n 与本地化 >>>
- **i18n 强制**：面向用户的固定文案一律使用 `I18NContext("key", **参数)`，只在所属包的
<<< END U000108 >>>
<<< UNIT U000109 | md-paragraph | AGENTS.md:125-125 | ctx=i18n 与本地化 >>>
  `locales/zh_cn.json` 中创建条目。插值语法是 `${name}`，占位符名不得与 `t()` 的形参同名。
<<< END U000109 >>>
<<< UNIT U000110 | md-list | AGENTS.md:126-127 | ctx=i18n 与本地化 >>>
- **本地化文本只使用简体中文。**
- **禁止改动其他语言文件**：除非用户明确要求处理翻译或 Weblate 同步结果，不得创建、修改、删除
<<< END U000110 >>>
<<< UNIT U000111 | md-paragraph | AGENTS.md:128-130 | ctx=i18n 与本地化 >>>
  或补齐任何包内 `locales/` 下 `zh_cn.json` 以外的语言 JSON。其他语言由 Weblate bot 自动提交，
  **即使缺少新增的 key 也不要复制简体中文或自行翻译**。`assets/config_store/<语言>/` 由配置模板生成，
  非 `zh_cn` 版本同样交给自动化生成。
<<< END U000111 >>>
<<< UNIT U000112 | md-list | AGENTS.md:131-131 | ctx=i18n 与本地化 >>>
- **新增配置字段必须补充注释**：字段在模板类里声明（`akaribot/core/config/decorator.py` 的
<<< END U000112 >>>
<<< UNIT U000113 | md-paragraph | AGENTS.md:132-134 | ctx=i18n 与本地化 >>>
  `@on_base_config` / `@on_config` / `@on_bot_config` / `@on_module_config`），同时在模板所属包的
  `zh_cn.json` 中添加 `config.comments.<表名>.<字段名>`。表名随装饰器而定（`config` / `secret` /
  `bot_<平台>` / `module_<模块>`，`secret=True` 时带 `_secret` 后缀）。
<<< END U000113 >>>
<<< UNIT U000114 | md-list | AGENTS.md:135-135 | ctx=i18n 与本地化 >>>
- **配置项注释视作文档**：只描述该项的用途，不描述技术细节。
<<< END U000114 >>>
<<< UNIT U000115 | md-heading | AGENTS.md:137-137 | ctx=TUI 键位与交互 >>>
### TUI 键位与交互
<<< END U000115 >>>
<<< UNIT U000116 | md-list | AGENTS.md:139-139 | ctx=TUI 键位与交互 >>>
- **破坏性操作不使用单字母键，且必须弹出模态确认框。** 删除、移除、清空数据一类操作使用 `ctrl+<字母>`
<<< END U000116 >>>
<<< UNIT U000117 | md-paragraph | AGENTS.md:140-141 | ctx=TUI 键位与交互 >>>
  或专用字母键（卸载使用 `u`）。不可逆操作（清空实例数据、重建 venv、迁移旧项目）额外要求
  **输入确认文字**或先试运行。
<<< END U000117 >>>
<<< UNIT U000118 | md-list | AGENTS.md:142-143 | ctx=TUI 键位与交互 >>>
- **单字母键只留给浏览与无副作用的切换**（`r` 刷新、`/` 搜索、`space` 选择等）。有副作用的单字母键须先弹出确认框。
- **确认一律弹出模态框**，不使用状态栏“再按一次 X 确认”——它既容易被鼠标双击或连续按键误触发，
<<< END U000118 >>>
<<< UNIT U000119 | md-paragraph | AGENTS.md:144-145 | ctx=TUI 键位与交互 >>>
  也容易让用户看不清即将执行什么改动。弹窗前先调用 `_compat.PendingConfirm.accept(key)`，在防抖时间窗口内忽略连续触发，
  避免重复弹出多层模态框。切换页面、刷新、切换选中项时调用页面的 `reset_pending()` 重置状态。
<<< END U000119 >>>
<<< UNIT U000120 | md-list | AGENTS.md:146-146 | ctx=TUI 键位与交互 >>>
- **页脚只显示高频快捷键**，低频与危险操作在 `compat.bindings()` 里用四元组第 4 项 `False` 隐藏，
<<< END U000120 >>>
<<< UNIT U000121 | md-paragraph | AGENTS.md:147-147 | ctx=TUI 键位与交互 >>>
  改为通过按钮或页内提示展示，80 列宽度下页脚不得溢出。
<<< END U000121 >>>
<<< UNIT U000122 | md-list | AGENTS.md:148-148 | ctx=TUI 键位与交互 >>>
- **键位遵循统一语法**（表见 `akaribot/cli/tui/README.md`“键位语法”），相同含义的操作在各页面只使用同一个键，
<<< END U000122 >>>
<<< UNIT U000123 | md-paragraph | AGENTS.md:149-150 | ctx=TUI 键位与交互 >>>
  调整页面键位时不得赋予新的含义。按钮文字通过 `compat.key_hint()` 附加快捷键。低频操作归入 `m` 菜单，
  不占用按钮栏空间。
<<< END U000123 >>>
<<< UNIT U000124 | md-heading | AGENTS.md:152-152 | ctx=CLI 与 TUI 的分工 >>>
### CLI 与 TUI 的分工
<<< END U000124 >>>
<<< UNIT U000125 | md-list | AGENTS.md:154-154 | ctx=CLI 与 TUI 的分工 >>>
- **写入操作一律通过 `akaribot <子命令>` 子进程执行**（界面通过已有的 `--yes` 参数自动确认），CLI 是唯一的写入入口，
<<< END U000125 >>>
<<< UNIT U000126 | md-paragraph | AGENTS.md:155-155 | ctx=CLI 与 TUI 的分工 >>>
  从而保证参数解析、校验与确认逻辑只有一份。进程内直接写入会导致命令层的前置校验在界面上失效。
<<< END U000126 >>>
<<< UNIT U000127 | md-list | AGENTS.md:156-156 | ctx=CLI 与 TUI 的分工 >>>
- **读取操作允许在进程内直接执行**，但限于不含业务判断的本机状态（注册表、锁文件、日志文件、`akaribot.toml`）。
<<< END U000127 >>>
<<< UNIT U000128 | md-paragraph | AGENTS.md:157-157 | ctx=CLI 与 TUI 的分工 >>>
  需要 core 参与判断的读取（配置 schema、数据项、模块清单、诊断）一律通过子进程执行。
<<< END U000128 >>>
<<< UNIT U000129 | md-list | AGENTS.md:158-158 | ctx=CLI 与 TUI 的分工 >>>
- **界面不得拥有 CLI 没有的能力**，新增界面功能前应先明确“对应的命令是什么”，若尚无对应命令则先补充命令。
<<< END U000129 >>>
<<< UNIT U000130 | md-paragraph | AGENTS.md:159-159 | ctx=CLI 与 TUI 的分工 >>>
  因此日志页的解析规则放在 `akaribot/cli/logs.py` 中，由界面直接复用。
<<< END U000130 >>>
<<< UNIT U000131 | md-heading | AGENTS.md:161-161 | ctx=版本控制 >>>
### 版本控制
<<< END U000131 >>>
<<< UNIT U000132 | md-list | AGENTS.md:163-164 | ctx=版本控制 >>>
- **不要擅自提交。** 所有改动保留在未提交的工作区，交由用户自行审查与提交。
- 除非用户明确授权自动提交，否则不执行 `git commit`。`git add`、`git push`、`git reset`、
<<< END U000132 >>>
<<< UNIT U000133 | md-paragraph | AGENTS.md:165-165 | ctx=版本控制 >>>
  `git checkout -- <file>` 等会改动暂存区、历史或丢弃工作区内容的操作同样需要用户授权。
<<< END U000133 >>>
<<< UNIT U000134 | md-list | AGENTS.md:166-167 | ctx=版本控制 >>>
- 授权仅对当次请求有效，不要据此推定后续改动也可以自动提交。
- 新功能分支使用 `dev/` 前缀，修复分支使用 `fix/` 前缀，分支名使用英文。
<<< END U000134 >>>
<<< UNIT U000135 | md-heading | AGENTS.md:169-169 | ctx=其他 >>>
### 其他
<<< END U000135 >>>
<<< UNIT U000136 | md-list | AGENTS.md:171-172 | ctx=其他 >>>
- 提交信息使用英文书面语，正文写明**证据**（实际运行输出、失败的用例清单对比、检查结果）。
- 移动文件应使用 `git mv` 以保留 git blame 记录。根目录同时保留同名兼容实现时 git 不会识别为重命名（rename），需要
<<< END U000136 >>>
<<< UNIT U000137 | md-paragraph | AGENTS.md:173-173 | ctx=其他 >>>
  拆分为“先移动文件、再修改内容”两次提交。
<<< END U000137 >>>
<<< UNIT U000138 | md-list | AGENTS.md:174-174 | ctx=其他 >>>
- 全量测试的失败清单须与基准**按名称一一对应**（`tools/test_baseline.txt`，通过
<<< END U000138 >>>
<<< UNIT U000139 | md-paragraph | AGENTS.md:175-175 | ctx=其他 >>>
  `tools/check_test_baseline.py` 对比）。
<<< END U000139 >>>
<<< UNIT U000140 | md-list | AGENTS.md:176-178 | ctx=其他 >>>
- 内部依赖约束必须**完全一致**（`akari-bot-core>=0.1.0,<1.0`）。官方模块包之间不得互相依赖。
- Ruff：行宽 120、双引号，忽略 E402/F405/F403/E741/E721。
- 中文排版：中英文之间加空格、使用全角标点、称呼用户用“你”、机器人自称用“机器人”（不用“我”）、
<<< END U000140 >>>
<<< UNIT U000141 | md-paragraph | AGENTS.md:179-179 | ctx=其他 >>>
  第三人称用“它”。
<<< END U000141 >>>
<<< UNIT U000142 | md-list | AGENTS.md:180-181 | ctx=其他 >>>
- 默认命令前缀 `~` / `～`。
- **获取时间统一使用 `akaribot.core.utils.timezone` 或 `SessionInfo.now()` / `today()`**，业务代码中
<<< END U000142 >>>
<<< UNIT U000143 | md-paragraph | AGENTS.md:182-183 | ctx=其他 >>>
  不得直接使用 `datetime.datetime.now()`、`date.today()`、`time.localtime()`。面向用户展示时使用
  `msg.format_time()` / `FormattedTime`。
<<< END U000143 >>>
<<< UNIT U000144 | md-heading | AGENTS.md:185-185 | ctx=陷阱 >>>
## 陷阱
<<< END U000144 >>>
<<< UNIT U000145 | md-paragraph | AGENTS.md:187-187 | ctx=陷阱 >>>
以下均为当前必须遵守的约束，改动相关代码时请勿回退：
<<< END U000145 >>>
<<< UNIT U000146 | md-list | AGENTS.md:189-189 | ctx=陷阱 >>>
- `akaribot/testing/__init__.py` **不得静态导入 `.tester`**，否则会间接引入 core，使合并日志目录在隔离
<<< END U000146 >>>
<<< UNIT U000147 | md-paragraph | AGENTS.md:190-190 | ctx=陷阱 >>>
  环境变量就位之前被固定到仓库 `data/`。公开名称按需解析。
<<< END U000147 >>>
<<< UNIT U000148 | md-list | AGENTS.md:191-191 | ctx=陷阱 >>>
- 按需加载的公开接口中**不得引入同名辅助名称**，`from typing import Any` 会通过
<<< END U000148 >>>
<<< UNIT U000149 | md-paragraph | AGENTS.md:192-192 | ctx=陷阱 >>>
  `from akaribot.testing import Any` 覆盖框架自带的 `Any` 匹配器（辅助名称一律以下划线开头）。
<<< END U000149 >>>
<<< UNIT U000150 | md-list | AGENTS.md:193-193 | ctx=陷阱 >>>
- 根目录 `bot.py` / `tester.py` 兼容实现使用 `sys.modules` **模块别名**，不要逐个名称重新导出——用例会为模块级
<<< END U000150 >>>
<<< UNIT U000151 | md-paragraph | AGENTS.md:194-194 | ctx=陷阱 >>>
  变量赋值再由同模块函数读取，如果逐个名称重新导出，赋值只会写入兼容实现而无法同步到原模块。
<<< END U000151 >>>
<<< UNIT U000152 | md-list | AGENTS.md:195-195 | ctx=陷阱 >>>
- `CFGManager.load()` 扫描 `config/*.toml` 与 `config/global/*.global.toml|.global.json`，因此适配器实例配置必须使用**扁平路径**
<<< END U000152 >>>
<<< UNIT U000153 | md-paragraph | AGENTS.md:196-196 | ctx=陷阱 >>>
  （`config/<表名>.toml`）。放在 `config/adapters/` 下的配置表对 core 不可见。
<<< END U000153 >>>
<<< UNIT U000154 | md-list | AGENTS.md:197-197 | ctx=陷阱 >>>
- `config set` 需按模板声明的类型转换，否则布尔项会被保存为字符串 `"true"`。实例表名
<<< END U000154 >>>
<<< UNIT U000155 | md-paragraph | AGENTS.md:198-198 | ctx=陷阱 >>>
  （`bot_telegram-alt`）由基础表（`bot_telegram`）生成，查找声明时要按前缀匹配。
<<< END U000155 >>>
<<< UNIT U000156 | md-list | AGENTS.md:199-199 | ctx=陷阱 >>>
- **Nuitka 打包后 `sys.executable` 指向二进制文件自身**，CLI 包内禁止使用它启动实例进程（B11 检查），
<<< END U000156 >>>
<<< UNIT U000157 | md-paragraph | AGENTS.md:200-200 | ctx=陷阱 >>>
  解释器一律通过 `akaribot.cli.instance.system_python()` 获取。
<<< END U000157 >>>
<<< UNIT U000158 | md-list | AGENTS.md:201-201 | ctx=陷阱 >>>
- 在 Textual 中，页面自有方法或属性**不得与基类成员同名**（`_render`、`offset` 等，覆盖 `Widget._render()`
<<< END U000158 >>>
<<< UNIT U000159 | md-paragraph | AGENTS.md:202-202 | ctx=陷阱 >>>
  会导致容器视图（visual）变为 `None`）。切换页面后须将焦点切换到该页，否则该页的快捷键不会生效。隐藏页面应跳过定时轮询。
<<< END U000159 >>>
<<< UNIT U000160 | md-list | AGENTS.md:203-203 | ctx=陷阱 >>>
- `i18n.t()` 的**占位符名称不得与形参同名**，例如 `${key}` 配合 `t(key=…)` 会抛出
<<< END U000160 >>>
<<< UNIT U000161 | md-paragraph | AGENTS.md:204-205 | ctx=陷阱 >>>
  `TypeError: t() got multiple values for argument 'key'`。占位符与实参一律使用有具体含义的名称
  （`${field}` / `field=`），修改键名后请核对调用处的关键字参数与模板占位符是否一致。
<<< END U000161 >>>
<<< UNIT U000162 | md-list | AGENTS.md:206-206 | ctx=陷阱 >>>
- 注释检查会拦截装饰性分隔注释、连续 3 行以上的行注释块、对照式表述、中文里的半角标点与
<<< END U000162 >>>
<<< UNIT U000163 | md-paragraph | AGENTS.md:207-207 | ctx=陷阱 >>>
  中英文之间缺失的空格。
<<< END U000163 >>>
<<< UNIT U000164 | md-list | AGENTS.md:208-208 | ctx=陷阱 >>>
- 品牌资产（立绘、标志、制作人员名单）是画师提供的原件，**不得为压缩体积重新编码**。
<<< END U000164 >>>
<<< UNIT U000165 | md-paragraph | AGENTS.md:209-209 | ctx=陷阱 >>>
  它们随 `akari-bot-assets-brand` 分发，属于 core 的 `full` 可选依赖组（extra），缺失时由使用方降级处理，而不是报错。
<<< END U000165 >>>
<<< UNIT U000166 | md-list | AGENTS.md:210-210 | ctx=陷阱 >>>
- `uv.lock` 是唯一来源。workspace 覆盖会忽略内部版本约束，只有从 wheel 安装才会经过真实的依赖解析器
<<< END U000166 >>>
<<< UNIT U000167 | md-paragraph | AGENTS.md:211-211 | ctx=陷阱 >>>
  （由 `tools/clean_room_check.py` 负责这项检查）。
<<< END U000167 >>>
<<< UNIT U000168 | md-heading | AGENTS.md:213-213 | ctx=提交与验证约定 >>>
## 提交与验证约定
<<< END U000168 >>>
<<< UNIT U000169 | md-list | AGENTS.md:215-215 | ctx=提交与验证约定 >>>
- 版本检查（`tools/check_versions.py`）要求包内有源码改动即升级 `version`，或在提交信息**最后一段**
<<< END U000169 >>>
<<< UNIT U000170 | md-paragraph | AGENTS.md:216-217 | ctx=提交与验证约定 >>>
  编写独立的提交尾注（trailer），其中 `Skip-Version: true` 豁免全部成员，`Skip-Version: <包名>[, <包名>]` 只豁免
  列出的成员。正文中间或缩进处提到该标记不视为声明。
<<< END U000170 >>>
<<< UNIT U000171 | md-list | AGENTS.md:218-218 | ctx=提交与验证约定 >>>
- 版本检查在 tester 里以目标分支为基准运行，**只报告不阻断**（`continue-on-error`），因为版本号是发布
<<< END U000171 >>>
<<< UNIT U000172 | md-paragraph | AGENTS.md:219-220 | ctx=提交与验证约定 >>>
  元数据，tester 的结论只取决于代码与测试。重复版本由 PyPI 在发布时拒绝。发布前请按输出的违规
  清单逐包升级 `version` 或添加提交尾注。
<<< END U000172 >>>
<<< UNIT U000173 | md-heading | CONTRIBUTING.md:1-1 | ctx=贡献指南 >>>
# 贡献指南
<<< END U000173 >>>
<<< UNIT U000174 | md-paragraph | CONTRIBUTING.md:3-3 | ctx=贡献指南 >>>
感谢你对小可及其衍生项目的关注。
<<< END U000174 >>>
<<< UNIT U000175 | md-paragraph | CONTRIBUTING.md:5-5 | ctx=贡献指南 >>>
本项目接受各种形式的贡献，各类参与方式与处理流程见下方[目录](#目录)。参与前请阅读对应章节，以减少维护者的沟通成本。
<<< END U000175 >>>
<<< UNIT U000176 | md-list | CONTRIBUTING.md:7-12 | ctx=贡献指南 >>>
> [!NOTE]
> 不打算贡献代码时，也可以通过以下方式支持本项目：
> - 为本仓库点 Star
> - 在自己项目的 README 中引用本项目
> - 将机器人加入群聊或服务器
> - 向他人推荐本项目
<<< END U000176 >>>
<<< UNIT U000177 | md-heading | CONTRIBUTING.md:14-14 | ctx=目录 >>>
## 目录
<<< END U000177 >>>
<<< UNIT U000178 | md-list | CONTRIBUTING.md:16-30 | ctx=目录 >>>
- [提出问题](#提出问题)
- [做出贡献](#做出贡献)
  - [报告错误](#报告错误)
  - [提出建议](#提出建议)
  - [本地化](#本地化)
- [提交代码更改](#提交代码更改)
  - [快速开始](#快速开始)
  - [开发环境](#开发环境)
    - [依赖冲突与联合求解](#依赖冲突与联合求解)
  - [分支命名](#分支命名)
  - [提交规范](#提交规范)
  - [PR 描述](#pr-描述)
  - [代码风格](#代码风格)
  - [新增模块包](#新增模块包)
- [文字排版](#文字排版)
<<< END U000178 >>>
<<< UNIT U000179 | md-heading | CONTRIBUTING.md:32-32 | ctx=提出问题 >>>
## 提出问题
<<< END U000179 >>>
<<< UNIT U000180 | md-list | CONTRIBUTING.md:34-35 | ctx=提出问题 >>>
> [!NOTE]
> 建议先阅读[《提问的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)。
<<< END U000180 >>>
<<< UNIT U000181 | md-list | CONTRIBUTING.md:37-37 | ctx=提出问题 >>>
> 本指南不提供本项目的实际支持服务。
<<< END U000181 >>>
<<< UNIT U000182 | md-paragraph | CONTRIBUTING.md:39-39 | ctx=提出问题 >>>
提问前请先搜索是否已有同类 [Issue](https://github.com/Teahouse-Studios/akari-bot/issues)。能在搜索引擎中找到答案的问题，不建议提交 Issue。
<<< END U000182 >>>
<<< UNIT U000183 | md-paragraph | CONTRIBUTING.md:41-41 | ctx=提出问题 >>>
需要联系开发者时，可通过以下渠道：
<<< END U000183 >>>
<<< UNIT U000184 | md-list | CONTRIBUTING.md:43-44 | ctx=提出问题 >>>
- 在 Issue 中[创建新问题](https://github.com/Teahouse-Studios/akari-bot/issues/new)
- 加入 QQ 平台的[小可公共实例测试群（738829671）](https://qm.qq.com/q/Rmuo5ORYgq)或[茶馆工作室聊天群（979982065）](https://qm.qq.com/q/sjwFNX1NVC)
<<< END U000184 >>>
<<< UNIT U000185 | md-paragraph | CONTRIBUTING.md:46-46 | ctx=提出问题 >>>
无论通过哪种渠道，都请**尽可能详细地描述**问题。
<<< END U000185 >>>
<<< UNIT U000186 | md-heading | CONTRIBUTING.md:48-48 | ctx=做出贡献 >>>
## 做出贡献
<<< END U000186 >>>
<<< UNIT U000187 | md-heading | CONTRIBUTING.md:50-50 | ctx=报告错误 >>>
### 报告错误
<<< END U000187 >>>
<<< UNIT U000188 | md-list | CONTRIBUTING.md:52-53 | ctx=报告错误 >>>
> [!WARNING]
> **绝对不要**在 Issue 或其他任何公开渠道报告或复现包含敏感信息的安全问题或漏洞。
<<< END U000188 >>>
<<< UNIT U000189 | md-list | CONTRIBUTING.md:54-55 | ctx=报告错误 >>>
> 
> 涉及敏感内容的问题必须通过电子邮件或私聊联系开发者，详见 [`SECURITY.md`](/SECURITY.md)。
<<< END U000189 >>>
<<< UNIT U000190 | md-list | CONTRIBUTING.md:57-57 | ctx=报告错误 >>>
> 违反本条规则的内容将被删除，由此产生的后果由发布者承担。
<<< END U000190 >>>
<<< UNIT U000191 | md-paragraph | CONTRIBUTING.md:59-59 | ctx=报告错误 >>>
提交前请确认是否已有同类 [Issue](https://github.com/Teahouse-Studios/akari-bot/issues)。
<<< END U000191 >>>
<<< UNIT U000192 | md-paragraph | CONTRIBUTING.md:61-61 | ctx=报告错误 >>>
若没有，请使用[错误报告模板](https://github.com/Teahouse-Studios/akari-bot/issues/new?template=report_bug.yaml)创建新的 Issue，并提供以下信息：
<<< END U000192 >>>
<<< UNIT U000193 | md-list | CONTRIBUTING.md:62-65 | ctx=报告错误 >>>
- 错误的简要描述
- 复现步骤
- 预期结果和实际结果
- 错误信息（若有）
<<< END U000193 >>>
<<< UNIT U000194 | md-paragraph | CONTRIBUTING.md:67-67 | ctx=报告错误 >>>
报告应包含上述信息，避免维护者反复追问细节。
<<< END U000194 >>>
<<< UNIT U000195 | md-heading | CONTRIBUTING.md:69-69 | ctx=提出建议 >>>
### 提出建议
<<< END U000195 >>>
<<< UNIT U000196 | md-paragraph | CONTRIBUTING.md:71-71 | ctx=提出建议 >>>
提交前请确认是否已有同类 [Issue](https://github.com/Teahouse-Studios/akari-bot/issues)。
<<< END U000196 >>>
<<< UNIT U000197 | md-paragraph | CONTRIBUTING.md:73-73 | ctx=提出建议 >>>
若没有，请使用[功能建议模板](https://github.com/Teahouse-Studios/akari-bot/issues/new?template=feature_request.yaml)创建新的 Issue，并提供：
<<< END U000197 >>>
<<< UNIT U000198 | md-list | CONTRIBUTING.md:74-76 | ctx=提出建议 >>>
- 建议的简要描述
- 可能的实现方案（若有）
- 建议对项目有益的理由（推荐）
<<< END U000198 >>>
<<< UNIT U000199 | md-paragraph | CONTRIBUTING.md:78-78 | ctx=提出建议 >>>
已经开发完成的改动，同样建议先提交 Issue 讨论，再创建拉取请求（PR）。
<<< END U000199 >>>
<<< UNIT U000200 | md-heading | CONTRIBUTING.md:80-80 | ctx=本地化 >>>
### 本地化
<<< END U000200 >>>
<<< UNIT U000201 | md-paragraph | CONTRIBUTING.md:82-82 | ctx=本地化 >>>
多语言内容由 Weblate 托管，翻译改进请前往 [Weblate](https://hosted.weblate.org/engage/akaribot)。
<<< END U000201 >>>
<<< UNIT U000202 | md-paragraph | CONTRIBUTING.md:84-84 | ctx=本地化 >>>
除简体中文外，翻译问题请在 Weblate 讨论，不提交到 Issue。
<<< END U000202 >>>
<<< UNIT U000203 | md-paragraph | CONTRIBUTING.md:86-86 | ctx=本地化 >>>
没有 Weblate 账号时可联系开发者代为提交。
<<< END U000203 >>>
<<< UNIT U000204 | md-heading | CONTRIBUTING.md:88-88 | ctx=提交代码更改 >>>
## 提交代码更改
<<< END U000204 >>>
<<< UNIT U000205 | md-paragraph | CONTRIBUTING.md:90-90 | ctx=提交代码更改 >>>
本节面向准备提交代码的贡献者。本项目对代码改动的限制较少，但仍须遵守下列约定。
<<< END U000205 >>>
<<< UNIT U000206 | md-heading | CONTRIBUTING.md:92-92 | ctx=快速开始 >>>
### 快速开始
<<< END U000206 >>>
<<< UNIT U000207 | md-list | CONTRIBUTING.md:94-98 | ctx=快速开始 >>>
1. Fork 本仓库
2. 克隆 Fork 出的仓库到本地
3. 创建新分支
4. 完成改动
5. 向本项目提交 PR
<<< END U000207 >>>
<<< UNIT U000208 | md-paragraph | CONTRIBUTING.md:100-100 | ctx=快速开始 >>>
提交规范见视频[《🐧你为啥直接 commit 到我的 master 分支啊》](https://bilibili.com/video/BV1pwC6BxEeb)。
<<< END U000208 >>>
<<< UNIT U000209 | md-heading | CONTRIBUTING.md:102-102 | ctx=开发环境 >>>
### 开发环境
<<< END U000209 >>>
<<< UNIT U000210 | md-paragraph | CONTRIBUTING.md:104-105 | ctx=开发环境 >>>
本项目使用 Python，最低版本要求见 [README](/README.md)。推荐使用 [PyCharm](https://www.jetbrains.com/pycharm) 或
[VS Code](https://code.visualstudio.com)。
<<< END U000210 >>>
<<< UNIT U000211 | md-paragraph | CONTRIBUTING.md:107-107 | ctx=开发环境 >>>
本项目使用 [uv](https://docs.astral.sh/uv) 管理依赖，安装依赖：
<<< END U000211 >>>
<<< UNIT U000212 | md-paragraph | CONTRIBUTING.md:113-113 | ctx=开发环境 >>>
新增依赖：
<<< END U000212 >>>
<<< UNIT U000213 | md-paragraph | CONTRIBUTING.md:119-119 | ctx=开发环境 >>>
新增依赖须放入 `pyproject.toml` 中对应的注释分组，并按字母顺序排列。
<<< END U000213 >>>
<<< UNIT U000214 | md-paragraph | CONTRIBUTING.md:121-121 | ctx=开发环境 >>>
改动依赖后更新锁文件：
<<< END U000214 >>>
<<< UNIT U000215 | md-heading | CONTRIBUTING.md:127-127 | ctx=依赖冲突与联合求解 >>>
### 依赖冲突与联合求解
<<< END U000215 >>>
<<< UNIT U000216 | md-paragraph | CONTRIBUTING.md:129-129 | ctx=依赖冲突与联合求解 >>>
本项目采用 uv workspace 结构，全部官方包共用根目录下的单一 `uv.lock`。生成锁文件时会对全部成员包做一次**联合求解**，因此只要各包声明的第三方依赖互相排斥，`uv lock` 就会立即失败，例如两个包对 `packaging` 的可接受版本区间没有交集：
<<< END U000216 >>>
<<< UNIT U000217 | md-paragraph | CONTRIBUTING.md:140-140 | ctx=依赖冲突与联合求解 >>>
CI 在 PR 阶段执行 `uv sync --locked`（见 [`.github/workflows/run-builtin-tester.yml`](/.github/workflows/run-builtin-tester.yml)），该命令会重新求解并在依赖无解或锁文件过期时失败。因此第三方依赖互斥会在 PR 阶段直接暴露，而不必等到用户安装时才发现。
<<< END U000217 >>>
<<< UNIT U000218 | md-paragraph | CONTRIBUTING.md:142-142 | ctx=依赖冲突与联合求解 >>>
多仓库布局下没有任何一处会做这样的联合求解，这是 monorepo 布局的主要优势。
<<< END U000218 >>>
<<< UNIT U000219 | md-paragraph | CONTRIBUTING.md:144-144 | ctx=依赖冲突与联合求解 >>>
这条检查有两处边界。
<<< END U000219 >>>
<<< UNIT U000220 | md-paragraph | CONTRIBUTING.md:146-146 | ctx=依赖冲突与联合求解 >>>
其一，仅覆盖 workspace 内成员包之间的**第三方**依赖互斥，不覆盖**内部**版本约束不一致。例如某包声明 `akari-bot-core>=2.0,<3.0`，而 core 实际为 `0.1.0`，此时 `uv lock` 仍然通过，约束却会原样写入发布的 wheel。内部版本约束由 `uv run python tools/lint_versions.py` 检查。
<<< END U000220 >>>
<<< UNIT U000221 | md-paragraph | CONTRIBUTING.md:148-148 | ctx=依赖冲突与联合求解 >>>
其二，不覆盖第三方模块。它们不在 workspace 内，依赖冲突只能通过干净环境安装验证以及 `akaribot module add` 的安装前检查来拦截。
<<< END U000221 >>>
<<< UNIT U000222 | md-paragraph | CONTRIBUTING.md:150-150 | ctx=依赖冲突与联合求解 >>>
`uv lock` 失败时应调整 `pyproject.toml` 中的约束，使冲突双方的区间重新相容并说明原因。不得以 `--no-verify` 绕过检查、手工编辑 `uv.lock` 或放宽约束来通过检查，这些做法只会把冲突推迟到用户安装时暴露。
<<< END U000222 >>>
<<< UNIT U000223 | md-paragraph | CONTRIBUTING.md:152-152 | ctx=依赖冲突与联合求解 >>>
仓库已配置 pre-commit 钩子，安装方式：
<<< END U000223 >>>
<<< UNIT U000224 | md-paragraph | CONTRIBUTING.md:158-158 | ctx=依赖冲突与联合求解 >>>
提交时自动执行格式化、静态分析与依赖导出。
<<< END U000224 >>>
<<< UNIT U000225 | md-heading | CONTRIBUTING.md:160-160 | ctx=分支命名 >>>
### 分支命名
<<< END U000225 >>>
<<< UNIT U000226 | md-paragraph | CONTRIBUTING.md:162-163 | ctx=分支命名 >>>
新功能与改动分支使用 `dev/` 前缀，缺陷修复分支使用 `fix/` 前缀。分支名必须使用英文，建议使用简短描述或
Issue 编号。
<<< END U000226 >>>
<<< UNIT U000227 | md-heading | CONTRIBUTING.md:165-165 | ctx=提交规范 >>>
### 提交规范
<<< END U000227 >>>
<<< UNIT U000228 | md-paragraph | CONTRIBUTING.md:167-167 | ctx=提交规范 >>>
提交信息使用英文或简体中文。建议遵循 Conventional Commits 规范。
<<< END U000228 >>>
<<< UNIT U000229 | md-heading | CONTRIBUTING.md:169-169 | ctx=PR 描述 >>>
### PR 描述
<<< END U000229 >>>
<<< UNIT U000230 | md-paragraph | CONTRIBUTING.md:171-172 | ctx=PR 描述 >>>
PR 标题参考[提交规范](#提交规范)，正文按 PR 模板填写。描述中可用 `#<编号>` [关联
Issue](#提出建议)。
<<< END U000230 >>>
<<< UNIT U000231 | md-paragraph | CONTRIBUTING.md:174-175 | ctx=PR 描述 >>>
PR 须通过全部 CI 检查，并获得至少 1 名开发者的 LGTM（Looks Good To Me）方可合并。重大更改须提交 PR 审查，不得直接
推送到 `master`。
<<< END U000231 >>>
<<< UNIT U000232 | md-heading | CONTRIBUTING.md:177-177 | ctx=代码风格 >>>
### 代码风格
<<< END U000232 >>>
<<< UNIT U000233 | md-paragraph | CONTRIBUTING.md:179-179 | ctx=代码风格 >>>
本项目使用 [Ruff](https://docs.astral.sh/ruff) 格式化与静态分析。提交前运行：
<<< END U000233 >>>
<<< UNIT U000234 | md-paragraph | CONTRIBUTING.md:186-186 | ctx=代码风格 >>>
VS Code 用户可安装 Ruff 扩展。
<<< END U000234 >>>
<<< UNIT U000235 | md-heading | CONTRIBUTING.md:188-188 | ctx=新增模块包 >>>
### 新增模块包
<<< END U000235 >>>
<<< UNIT U000236 | md-paragraph | CONTRIBUTING.md:190-191 | ctx=新增模块包 >>>
仓库已按包拆分，官方模块各占一个 workspace 成员（`packages/modules/akari-bot-module-<名>/`）。
新增模块可使用脚手架生成后再按需修改：
<<< END U000236 >>>
<<< UNIT U000237 | md-paragraph | CONTRIBUTING.md:198-201 | ctx=新增模块包 >>>
脚手架会生成 `<--dir>/akari-bot-module-<名>/`，目录结构与 `packages/modules/akari-bot-module-<名>/` 一致：
`pyproject.toml`、`manifest.toml`、`README.md`、`akaribot/modules/<名>/`（包含 `config.py`、
`database/models.py`、`migrations/`、`locales/zh_cn.json`、`assets/`）与 `tests/test_<名>.py`。
`--add` 默认开启，生成后会自动在该目录内执行 `akaribot module add -e .`。若需要手工执行，请先进入该包目录。
<<< END U000237 >>>
<<< UNIT U000238 | md-paragraph | CONTRIBUTING.md:203-204 | ctx=新增模块包 >>>
`manifest.toml` 放在导入包目录内，字段与 `akaribot/core/registry.py` 的 `PackageManifest` 一一对应，
未启用的配置项可整行省略：
<<< END U000238 >>>
<<< UNIT U000239 | md-table | CONTRIBUTING.md:206-213 | ctx=新增模块包 >>>
| 字段 | 用途 |
| --- | --- |
| `schema` | 清单版本，当前为 `1` |
| `requires_core_api` | 兼容的 core 公开 API 区间，当前填写 `">=1,<2"` |
| `locales` / `assets` / `migrations` / `config_migrations` | 各目录相对包根目录的路径，未使用的目录项可省略 |
| `config_table` / `config_schema_version` | `config.py` 中 `on_module_config("<名>")` 声明的表名与配置版本 |
| `provides_modules` | 本包 `module()` 注册的全部模块名 |
| `owned_tables` | 本包拥有的数据库表，供 `akaribot module remove --purge-data` 使用 |
<<< END U000239 >>>
<<< UNIT U000240 | md-paragraph | CONTRIBUTING.md:215-215 | ctx=新增模块包 >>>
清单里**不填写版本号与依赖清单**，两者的来源是包元数据（distribution metadata）。生成后请核对以下强制约定：
<<< END U000240 >>>
<<< UNIT U000241 | md-list | CONTRIBUTING.md:217-219 | ctx=新增模块包 >>>
- 代码一律使用 `from akaribot.core.api import ...`，不要引用 `akaribot.core.builtins.*` 这类内部路径。
- `locales/zh_cn.json` **只提交 zh_cn**，其余语言交给 Weblate。键名前缀须与模块名一致。
- 对 core 的约束统一填写 `akari-bot-core>=0.1.0,<1.0`，全部官方包的这一版本约束必须**完全一致**，
<<< END U000241 >>>
<<< UNIT U000242 | md-paragraph | CONTRIBUTING.md:220-220 | ctx=新增模块包 >>>
  `python tools/lint_versions.py` 会对此进行检查。
<<< END U000242 >>>
<<< UNIT U000243 | md-list | CONTRIBUTING.md:221-222 | ctx=新增模块包 >>>
- 模块之间不要互相依赖，官方模块包之间**不得存在任何依赖**（`tools/lint_boundaries.py` 的 B10）。
- 若模块要创建数据表，迁移文件放在 `migrations/`，并保证可重复执行（判断某条迁移记录（revision）是否已应用只查询
<<< END U000243 >>>
<<< UNIT U000244 | md-paragraph | CONTRIBUTING.md:223-223 | ctx=新增模块包 >>>
  `schema_migrations` 表）。
<<< END U000244 >>>
<<< UNIT U000245 | md-list | CONTRIBUTING.md:224-224 | ctx=新增模块包 >>>
- 包内不要出现 `akaribot/__init__.py`，因为 `akaribot` 是命名空间包（B7）。
<<< END U000245 >>>
<<< UNIT U000246 | md-paragraph | CONTRIBUTING.md:226-226 | ctx=新增模块包 >>>
提交前运行全部检查：
<<< END U000246 >>>
<<< UNIT U000247 | md-heading | CONTRIBUTING.md:235-235 | ctx=文字排版 >>>
## 文字排版
<<< END U000247 >>>
<<< UNIT U000248 | md-list | CONTRIBUTING.md:237-237 | ctx=文字排版 >>>
> “有研究显示，打字的时候不喜欢在中文和英文之间加空格的人，感情路都走得很辛苦，有七成的比例会在 34 岁的时候跟自己不爱的人结婚，而其余三成的人最后只能把遗产留给自己的猫。毕竟爱情跟书写都需要适时地留白。
<<< END U000248 >>>
<<< UNIT U000249 | md-list | CONTRIBUTING.md:239-239 | ctx=文字排版 >>>
> 与大家共勉之。”
<<< END U000249 >>>
<<< UNIT U000250 | md-paragraph | CONTRIBUTING.md:243-243 | ctx=文字排版 >>>
本项目的所有中文文字排版（包括本文）参考[中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines/blob/master/README.zh-Hans.md)。
<<< END U000250 >>>
<<< UNIT U000251 | md-paragraph | CONTRIBUTING.md:245-245 | ctx=文字排版 >>>
规则包括：
<<< END U000251 >>>
<<< UNIT U000252 | md-list | CONTRIBUTING.md:246-248 | ctx=文字排版 >>>
- 中英文之间需要增加空格
- 使用全角中文标点
- 专有名词使用正确的大小写
<<< END U000252 >>>
<<< UNIT U000253 | md-paragraph | CONTRIBUTING.md:250-250 | ctx=文字排版 >>>
以下情况例外：
<<< END U000253 >>>
<<< UNIT U000254 | md-list | CONTRIBUTING.md:251-252 | ctx=文字排版 >>>
- 简体中文使用弯引号
- 链接之间不额外增加空格
<<< END U000254 >>>
<<< UNIT U000255 | md-paragraph | CONTRIBUTING.md:254-254 | ctx=文字排版 >>>
补充约定：
<<< END U000255 >>>
<<< UNIT U000256 | md-list | CONTRIBUTING.md:255-258 | ctx=文字排版 >>>
- 称呼用户统一使用“你”
- 机器人自称时避免使用“我”，统一使用“机器人”
- 尽可能避免使用第一人称描述
- 机器人的第三人称统一为“它”
<<< END U000256 >>>
<<< UNIT U000257 | md-list | CONTRIBUTING.md:503-506 | ctx=Text Typography (for Chinese) >>>
- Address users with “你” (informal/casual “you”) and avoid the polite variant
- When the bot refers to itself, avoid “我” (I / me); use “机器人” (the Bot / this Bot) instead
- Avoid first-person descriptions whenever possible
- The bot's third-person pronoun is uniformly “它” (it / it)
<<< END U000257 >>>
<<< UNIT U000258 | md-heading | README.md:4-4 | ctx=小可 · AkariBot >>>
# 小可 · AkariBot
<<< END U000258 >>>
<<< UNIT U000259 | md-paragraph | README.md:6-6 | ctx=小可 · AkariBot >>>
_多功能、跨平台、可自由扩展的异步聊天机器人助手_
<<< END U000259 >>>
<<< UNIT U000260 | md-heading | README.md:23-23 | ctx=运行 >>>
## 运行
<<< END U000260 >>>
<<< UNIT U000261 | md-paragraph | README.md:25-26 | ctx=运行 >>>
支持 QQ（官方机器人与第三方协议）、Discord、Telegram、KOOK（开黑啦）、
Matrix 与 Satori（Beta）。
<<< END U000261 >>>
<<< UNIT U000262 | md-heading | README.md:28-28 | ctx=公共实例 >>>
### 公共实例
<<< END U000262 >>>
<<< UNIT U000263 | md-paragraph | README.md:30-30 | ctx=公共实例 >>>
茶馆工作室和问谛居共同提供小可的公共实例。
<<< END U000263 >>>
<<< UNIT U000264 | md-heading | README.md:40-40 | ctx=第三方协议 >>>
##### 第三方协议
<<< END U000264 >>>
<<< UNIT U000265 | md-paragraph | README.md:41-42 | ctx=第三方协议 >>>
由于腾讯风控问题，请[在此提交](https://github.com/Teahouse-Studios/akari-bot/issues/new?assignees=OasisAkari&labels=New&template=add_new_group.yaml&title=%5BNEW%5D%3A+)入群申请。
-->
<<< END U000265 >>>
<<< UNIT U000266 | md-paragraph | README.md:44-44 | ctx=第三方协议 >>>
QQ 公共实例反馈群：[738829671](https://qm.qq.com/q/Rmuo5ORYgq)
<<< END U000266 >>>
<<< UNIT U000267 | md-paragraph | README.md:48-48 | ctx=Discord >>>
邀请链接：<https://discord.com/oauth2/authorize?client_id=879379218209861712&scope=bot&permissions=71605695277126>
<<< END U000267 >>>
<<< UNIT U000268 | md-paragraph | README.md:52-52 | ctx=Telegram >>>
邀请链接：<https://t.me/oasisakaribot>
<<< END U000268 >>>
<<< UNIT U000269 | md-heading | README.md:54-54 | ctx=KOOK（开黑啦） >>>
#### KOOK（开黑啦）
<<< END U000269 >>>
<<< UNIT U000270 | md-paragraph | README.md:56-56 | ctx=KOOK（开黑啦） >>>
邀请链接：<https://www.kookapp.cn/app/oauth2/authorize?id=19512&permissions=949248&client_id=xiDWoVygvPsP6bov&redirect_uri=&scope=bot>
<<< END U000270 >>>
<<< UNIT U000271 | md-paragraph | README.md:60-60 | ctx=Matrix >>>
邀请链接：<https://matrix.to/#/@akaribot:matrix.org>
<<< END U000271 >>>
<<< UNIT U000272 | md-heading | README.md:62-62 | ctx=自搭建 >>>
### 自搭建
<<< END U000272 >>>
<<< UNIT U000273 | md-paragraph | README.md:64-65 | ctx=自搭建 >>>
机器人使用独立的实例目录，通过命令行工具（CLI）管理实例虚拟环境、适配器、模块、配置和运行状态。
需要仓库 `pyproject.toml` 声明的 Python 版本及 [uv](https://docs.astral.sh/uv/)。发行包的基本安装与初始化命令如下：
<<< END U000273 >>>
<<< UNIT U000274 | md-paragraph | README.md:77-77 | ctx=自搭建 >>>
填写适配器登录信息后再启用实例。`akaribot config set <字段> <值> --table <表名>` 会按模板声明的类型转换并写入。
<<< END U000274 >>>
<<< UNIT U000275 | md-paragraph | README.md:79-80 | ctx=自搭建 >>>
CLI 独立安装，机器人与模块安装在实例环境内。默认 core 安装包含品牌、表情和常规可选依赖，
使用 `init --minimal` 则只安装核心最小依赖。
<<< END U000275 >>>
<<< UNIT U000276 | md-paragraph | README.md:82-83 | ctx=自搭建 >>>
源码开发与发行包安装的工作区约定见 [CONTRIBUTING.md](CONTRIBUTING.md)，
旧部署的备份、试运行和迁移见 [迁移指南](docs/migrating-to-packages.md)。
<<< END U000276 >>>
<<< UNIT U000277 | md-paragraph | README.md:85-85 | ctx=自搭建 >>>
完整的搭建步骤见[自搭建指南](https://bot.teahouse.team/wiki/%E8%87%AA%E6%90%AD%E5%BB%BA)（[镜像](https://github.com/Teahouse-Studios/akari-bot/wiki/%E8%87%AA%E6%90%AD%E5%BB%BA%E6%8C%87%E5%8D%97)）。
<<< END U000277 >>>
<<< UNIT U000278 | md-paragraph | README.md:87-87 | ctx=自搭建 >>>
问题反馈见 [Issue](https://github.com/Teahouse-Studios/akari-bot/issues/new)。
<<< END U000278 >>>
<<< UNIT U000279 | md-heading | README.md:89-89 | ctx=本地化 >>>
### 本地化
<<< END U000279 >>>
<<< UNIT U000280 | md-paragraph | README.md:91-91 | ctx=本地化 >>>
本地化内容由 Weblate 托管，翻译改进请前往 [Weblate](https://hosted.weblate.org/engage/akaribot)。
<<< END U000280 >>>
<<< UNIT U000281 | md-heading | README.md:93-93 | ctx=贡献 >>>
### 贡献
<<< END U000281 >>>
<<< UNIT U000282 | md-paragraph | README.md:95-95 | ctx=贡献 >>>
贡献流程与提交约定见 [CONTRIBUTING.md](/CONTRIBUTING.md)。
<<< END U000282 >>>
<<< UNIT U000283 | md-heading | README.md:97-97 | ctx=相关项目 >>>
## 相关项目
<<< END U000283 >>>
<<< UNIT U000284 | md-heading | README.md:103-103 | ctx=鸣谢 >>>
## 鸣谢
<<< END U000284 >>>
<<< UNIT U000285 | md-list | README.md:105-105 | ctx=鸣谢 >>>
- [`Graia`](https://github.com/GraiaProject/Application) — 小可曾基于此项目开发
<<< END U000285 >>>
<<< UNIT U000286 | md-heading | README.md:107-107 | ctx=许可 >>>
## 许可
<<< END U000286 >>>
<<< UNIT U000287 | md-paragraph | README.md:109-109 | ctx=许可 >>>
除另有说明外，本项目的所有代码与资源均使用 [AGPL-3.0](./LICENSE) 协议授权。
<<< END U000287 >>>
<<< UNIT U000288 | md-heading | README.md:111-111 | ctx=赞助者 >>>
## 赞助者
<<< END U000288 >>>
<<< UNIT U000289 | py-comment | bot.py:18-19 >>>
# 既有用例通过 ``import bot as daemon`` 使用的兼容接口在此集中核对，缺失时在导入阶段即报错，
# 而不是等到用例里出现 AttributeError。
<<< END U000289 >>>
<<< UNIT U000290 | py-comment | conftest.py:18-18 >>>
# 导入 tester 即完成测试环境初始化，必须早于任何 akaribot.core.* 导入（说明见本文件开头的 docstring）。
<<< END U000290 >>>
<<< UNIT U000291 | py-docstring | conftest.py:32-32 | ctx=tester >>>
纯 pytest 风格用例的运行器，子测试失败直接判定为用例失败。
<<< END U000291 >>>
<<< UNIT U000292 | md-heading | docs/migrating-to-packages.md:1-1 | ctx=从旧版迁移到按包发布 >>>
# 从旧版迁移到按包发布
<<< END U000292 >>>
<<< UNIT U000293 | md-paragraph | docs/migrating-to-packages.md:3-3 | ctx=从旧版迁移到按包发布 >>>
本文面向**使用旧版 AkariBot 的部署者**。旧版将机器人与全部模块放在同一个仓库中，通过 `git pull` 更新。新版把 core、模块与适配器拆成互相独立的包，用 `akaribot` 命令行工具（CLI）管理实例。
<<< END U000293 >>>
<<< UNIT U000294 | md-paragraph | docs/migrating-to-packages.md:5-5 | ctx=从旧版迁移到按包发布 >>>
迁移可直接用 `akaribot migrate legacy <旧项目路径>` 完成（见下节）。下面另附手工步骤，供需要逐项控制或排查问题时使用。
<<< END U000294 >>>
<<< UNIT U000295 | md-heading | docs/migrating-to-packages.md:7-7 | ctx=变化概览 >>>
## 变化概览
<<< END U000295 >>>
<<< UNIT U000296 | md-table | docs/migrating-to-packages.md:9-15 | ctx=变化概览 >>>
| 项 | 旧版 | 新版 |
| --- | --- | --- |
| 获取更新 | `git pull` + `uv sync`（机器人内的 `~update`） | `akaribot module update --all`（机器人内的 `~update` 已改为交由 CLI 执行） |
| 模块 | 随仓库内置，全部可用 | 按需安装：`akaribot module add <名>`，代码只存在于实例虚拟环境（venv） |
| 依赖 | 整个仓库一份 | 每个包各自声明，实例 venv 内统一解析 |
| 配置与数据 | 仓库根目录下的 `config/`、`database/`、`data/` | 实例根目录下的同名目录，位置不变 |
| 多账号 | 一个平台一份配置 | 同一平台可创建多个实例：`akaribot adapter instance add <平台> <实例 ID>` |
<<< END U000296 >>>
<<< UNIT U000297 | md-heading | docs/migrating-to-packages.md:17-17 | ctx=自动迁移 >>>
## 自动迁移
<<< END U000297 >>>
<<< UNIT U000298 | md-paragraph | docs/migrating-to-packages.md:23-23 | ctx=自动迁移 >>>
迁移会校验旧项目布局（须含 `bot.py`、`core/`、`modules/` 与 `config/config.toml`）。旧模块名按多对一映射到新的包名，例如 `wikilog`/`weekly`/`weekly_rss` 都归入 `akari-bot-module-wiki`。
<<< END U000298 >>>
<<< UNIT U000299 | md-paragraph | docs/migrating-to-packages.md:25-25 | ctx=自动迁移 >>>
随后创建新实例、迁移配置与数据、安装映射后的包、转换数据库版本号，最后在新实例根目录写入 `migration-report.md`。**一律生成默认实例**（实例 ID 为空、`client_name` 与旧项目相同），因此 `target_id` 前缀不变、场景数据无需改写。
<<< END U000299 >>>
<<< UNIT U000300 | md-paragraph | docs/migrating-to-packages.md:27-27 | ctx=自动迁移 >>>
常用选项包括 `--dry-run`（只输出报告不写入文件）、`--skip-install`（只迁移文件）、`--force`（覆盖同名文件）。迁移**不修改旧项目**。失败项会记入报告的“需人工处理”部分，可重新运行命令继续处理。
<<< END U000300 >>>
<<< UNIT U000301 | md-paragraph | docs/migrating-to-packages.md:29-29 | ctx=自动迁移 >>>
执行真实迁移前须停止源实例并保存配置、数据库和 `data/` 的备份。
<<< END U000301 >>>
<<< UNIT U000302 | md-paragraph | docs/migrating-to-packages.md:31-31 | ctx=自动迁移 >>>
复制期间迁移程序会持有源目录的 `.bot.lock`，并将 SQLite 主数据库与已提交的预写日志（WAL）数据通过独立快照复制到目标目录，同时将目标配置中的数据库地址指向该副本。缺少 `.bot.lock` 的旧目录应先正常启动并停止一次以生成锁文件，试运行模式下则允许该锁文件不存在。
<<< END U000302 >>>
<<< UNIT U000303 | md-paragraph | docs/migrating-to-packages.md:33-33 | ctx=自动迁移 >>>
MySQL 等外部数据库不支持自动复制迁移，须先导出到独立目标并按手工步骤处理。其他正在写入外部 SQLite 文件的进程同样须先停止。
<<< END U000303 >>>
<<< UNIT U000304 | md-paragraph | docs/migrating-to-packages.md:35-35 | ctx=自动迁移 >>>
迁移会复制根目录的 `data/`，历史 `assets/` 目录中的内容仅补齐缺失项。已有目标配置和数据库在未使用 `--force` 时保留。数据库绑定冲突或目标路径包含符号链接时会拒绝继续。`--skip-install` 不执行数据库升级。
<<< END U000304 >>>
<<< UNIT U000305 | md-heading | docs/migrating-to-packages.md:37-37 | ctx=手工迁移步骤 >>>
## 手工迁移步骤
<<< END U000305 >>>
<<< UNIT U000306 | md-paragraph | docs/migrating-to-packages.md:39-39 | ctx=手工迁移步骤 >>>
以下命令中的 `<实例目录>` 建议新建（例如 `/opt/akaribot`），**不要**在旧仓库里就地升级。
<<< END U000306 >>>
<<< UNIT U000307 | md-list | docs/migrating-to-packages.md:41-42 | ctx=手工迁移步骤 >>>
1. **确认 Python 与 uv**：需要仓库 `pyproject.toml` 声明的 Python 版本与 [uv](https://docs.astral.sh/uv/)。
2. **创建新实例**：
<<< END U000307 >>>
<<< UNIT U000308 | md-paragraph | docs/migrating-to-packages.md:48-48 | ctx=手工迁移步骤 >>>
   `--adapter` 可多次指定，可选值包括 `telegram`、`discord`、`qqbot`、`kook`、`matrix`、`onebot`、`web`、`milky`。若你的包尚未发布到 PyPI（例如自己从源码构建），可加上 `--workspace-root <仓库路径>` 按本地路径安装。
<<< END U000308 >>>
<<< UNIT U000309 | md-list | docs/migrating-to-packages.md:49-49 | ctx=手工迁移步骤 >>>
3. **迁移配置**：把旧仓库 `config/` 下的文件复制到 `<实例目录>/config/`。配置表名与文件名一一对应（`config.toml`、`bot_telegram.toml`、`module_wiki.toml` …）。复制后逐项核对：
<<< END U000309 >>>
<<< UNIT U000310 | md-paragraph | docs/migrating-to-packages.md:56-56 | ctx=手工迁移步骤 >>>
   在安装模块或升级数据库之前，将 `[secret].db_path` 改为目标副本或独立目标数据库的地址。绝对 SQLite 路径和远程连接地址不得继续指向源部署。
<<< END U000310 >>>
<<< UNIT U000311 | md-list | docs/migrating-to-packages.md:58-59 | ctx=手工迁移步骤 >>>
4. **迁移数据**：把旧仓库的 `database/`、`data/`、`assets/`（若曾自建）复制到实例根目录下。数据库首次启动时会自动执行迁移，旧版本号由迁移系统转换。
5. **安装实际使用的模块**：
<<< END U000311 >>>
<<< UNIT U000312 | md-paragraph | docs/migrating-to-packages.md:68-68 | ctx=手工迁移步骤 >>>
   模块不再随仓库内置，旧配置里出现的模块若未安装，其命令不会被注册。自建模块可以直接从 git 仓库安装：
<<< END U000312 >>>
<<< UNIT U000313 | md-paragraph | docs/migrating-to-packages.md:76-76 | ctx=手工迁移步骤 >>>
   仓库里包的 `pyproject.toml` 必须声明 `akaribot.modules` 或 `akaribot.adapters` entry point。
<<< END U000313 >>>
<<< UNIT U000314 | md-paragraph | docs/migrating-to-packages.md:78-78 | ctx=手工迁移步骤 >>>
   未指定名称时，安装后会通过对比安装前后的包列表识别名称。仓库包含多个包或该包已安装时，用 `--dist <包名>` 指明。通过 git 直接引用安装时，需等安装完成后才能读取 manifest，因此兼容性检查在安装后执行。若包声明的 `requires_core_api` 不满足当前版本，系统会自动卸载并回滚。
<<< END U000314 >>>
<<< UNIT U000315 | md-list | docs/migrating-to-packages.md:80-80 | ctx=手工迁移步骤 >>>
6. **校验**：
<<< END U000315 >>>
<<< UNIT U000316 | md-paragraph | docs/migrating-to-packages.md:89-89 | ctx=手工迁移步骤 >>>
   前台运行请使用 `akaribot run`（不加 `--detach`），日志同样保存在 `<实例目录>/logs/`。
<<< END U000316 >>>
<<< UNIT U000317 | md-paragraph | docs/migrating-to-packages.md:91-91 | ctx=手工迁移步骤 >>>
   实例的进程号记录在实例级锁 `<实例目录>/.bot.lock` 中，`run --stop` 据此终止进程，因此无论实例是谁启动的都能正常停止。后台实例会创建独立会话，即使启动它的终端退出，实例仍会继续运行。
<<< END U000317 >>>
<<< UNIT U000318 | md-paragraph | docs/migrating-to-packages.md:93-93 | ctx=手工迁移步骤 >>>
   需要交互界面时直接运行 `akaribot`（在实例目录内）或 `akaribot tui`。没有实例时会先询问是否就地初始化。
<<< END U000318 >>>
<<< UNIT U000319 | md-paragraph | docs/migrating-to-packages.md:95-95 | ctx=手工迁移步骤 >>>
   界面启动时会把当前所在的实例写入注册表（已存在则不重复写入，界面会给出提示）。
<<< END U000319 >>>
<<< UNIT U000320 | md-paragraph | docs/migrating-to-packages.md:97-97 | ctx=手工迁移步骤 >>>
   在实例目录之外启动界面且下级目录中只有一个实例时，界面会自动将其写入注册表并切换过去，因此从项目根目录启动也能直接管理该实例。无图形终端的环境请用命令行子命令。
<<< END U000320 >>>
<<< UNIT U000321 | md-paragraph | docs/migrating-to-packages.md:99-99 | ctx=手工迁移步骤 >>>
   一台机器可管理多个实例，可使用 `akaribot instance add <目录>` 添加，`instance list` 查看状态，`instance use <名>` 设为默认（在实例目录之外执行命令时的默认目标），记录保存在 `~/.akaribot/instances.toml`。
<<< END U000321 >>>
<<< UNIT U000322 | md-paragraph | docs/migrating-to-packages.md:101-101 | ctx=手工迁移步骤 >>>
   界面概览页的实例清单提供相同操作，在条目上回车即切换当前管理的实例。按 `n` 添加时输入框已预填当前实例目录，回车即写入注册表。
<<< END U000322 >>>
<<< UNIT U000323 | md-paragraph | docs/migrating-to-packages.md:103-103 | ctx=手工迁移步骤 >>>
   额外需要的运行库（第三方 SDK、自行打包的包）可使用 `akaribot venv add <依赖声明>` 安装到实例环境。`--save`（默认）会同时写入 `akaribot.toml` 的 `runtime.requirements`，`venv recreate` 与 `venv adopt` 会按此列表补充安装。`--no-save` 只安装到当前环境，重建后不保留。
<<< END U000323 >>>
<<< UNIT U000324 | md-paragraph | docs/migrating-to-packages.md:105-105 | ctx=手工迁移步骤 >>>
   卸载请使用 `akaribot venv remove <包名>`，加上 `--no-save` 则只卸载包但保留记录。界面环境页提供相同功能，并列出环境里的**全部**已安装包（包含 httpx 这类间接依赖）以及各记录的来源。
<<< END U000324 >>>
<<< UNIT U000325 | md-paragraph | docs/migrating-to-packages.md:107-107 | ctx=手工迁移步骤 >>>
   要让实例随机器启动、崩溃后自动重启，先执行 `akaribot service install` 安装常驻服务（macOS 写入 `~/Library/LaunchAgents`，Linux 写入 systemd 用户单元），再用 `akaribot instance policy <名> --autostart --restart-on-crash` 逐实例开启策略。
<<< END U000325 >>>
<<< UNIT U000326 | md-paragraph | docs/migrating-to-packages.md:109-109 | ctx=手工迁移步骤 >>>
   服务启动时只恢复**已开启开机自启**且上次处于运行状态的实例，停电前正在运行但未开启自启的实例不会被自动启动。崩溃后自动重启由另一个独立开关控制。
<<< END U000326 >>>
<<< UNIT U000327 | md-heading | docs/migrating-to-packages.md:111-111 | ctx=同一个平台跑多个账号 >>>
## 同一平台运行多个账号
<<< END U000327 >>>
<<< UNIT U000328 | md-paragraph | docs/migrating-to-packages.md:113-113 | ctx=同一个平台跑多个账号 >>>
迁移一律生成**默认实例**，它的 `client_name` 与旧项目完全一致，因此历史场景数据（`target_id` 前缀）原样可用。需要在同一平台新增账号时创建新实例：
<<< END U000328 >>>
<<< UNIT U000329 | md-paragraph | docs/migrating-to-packages.md:121-121 | ctx=同一个平台跑多个账号 >>>
新实例的 `client_name` 会带有 `-<实例 ID>` 后缀（如 `Telegram-work`），因此 `target_id` 与 `sender_id` 也会使用新的前缀，与默认实例的历史数据互相独立。
<<< END U000329 >>>
<<< UNIT U000330 | md-paragraph | docs/migrating-to-packages.md:123-123 | ctx=同一个平台跑多个账号 >>>
实例 ID 一经使用**不可更改**，因为修改名称需要跨多张核心表与模块表迁移前缀，需要更换 ID 时按“新建实例并迁移数据”处理。`add` 生成的配置中 `enable` 默认设为 `false`，填写完登录信息后再开启。
<<< END U000330 >>>
<<< UNIT U000331 | md-heading | docs/migrating-to-packages.md:125-125 | ctx=机器人内更新 >>>
## 机器人内更新
<<< END U000331 >>>
<<< UNIT U000332 | md-paragraph | docs/migrating-to-packages.md:127-127 | ctx=机器人内更新 >>>
机器人内的 `~update` 会交由 CLI 执行 `module update --defer-runtime`，安装包并同步配置后返回结果。数据库迁移和运行代码切换会在下一次启动时完成，因此更新后需按提示执行 `~restart`。若使用 `~update&restart`，则会在更新完成后自动执行重启。宿主机上也可直接执行：
<<< END U000332 >>>
<<< UNIT U000333 | md-paragraph | docs/migrating-to-packages.md:133-133 | ctx=机器人内更新 >>>
宿主机更新会执行数据库迁移和模块热加载。涉及数据结构的升级应先停止实例并保留备份。如果只想安装包并等待后续重启再生效，请使用 `--defer-runtime`。
<<< END U000333 >>>
<<< UNIT U000334 | md-paragraph | docs/migrating-to-packages.md:135-135 | ctx=机器人内更新 >>>
`akaribot venv recreate` 先在独立的新环境中安装并验证，再替换原环境。若替换后的路径验证失败，会自动恢复旧环境。失败的 `.new` 目录保留供检查，已有 `.old` 备份不会自动删除。
<<< END U000334 >>>
<<< UNIT U000335 | md-heading | docs/migrating-to-packages.md:137-137 | ctx=已知限制 >>>
## 已知限制
<<< END U000335 >>>
<<< UNIT U000336 | md-list | docs/migrating-to-packages.md:139-141 | ctx=已知限制 >>>
- **实例 ID 一旦使用请勿更改**：修改名称需要跨多张核心表与模块表迁移 `target_id` 前缀，改动成本与风险过高，故不提供重命名。需要更换 ID 时请新建实例并迁移数据。
- **终端界面（TUI）兼容性**：Textual 界面目前只在 macOS 上做过无界面渲染与布局测试，在 Windows 终端、旧版控制台（conhost）、tmux 以及窄屏幕 SSH 终端下的实际表现尚未验证。遇到显示问题请改用命令行子命令。
- **配置文件位置**：适配器实例配置保存在 `config/<表名>.toml`（扁平布局）。分层布局（`config/adapters/`）尚未启用，请勿手工移动这些文件。
<<< END U000336 >>>
<<< UNIT U000337 | md-heading | docs/migrating-to-packages.md:143-143 | ctx=遇到问题时 >>>
## 遇到问题时
<<< END U000337 >>>
<<< UNIT U000338 | md-paragraph | docs/migrating-to-packages.md:152-152 | ctx=遇到问题时 >>>
`akaribot` 的每个子命令都支持 `--help`。`--json` 选项（`module list`、`config schema` 等）便于脚本处理。
<<< END U000338 >>>
<<< UNIT U000339 | md-heading | docs/package-docs.md:1-1 | ctx=包文档编写指南 >>>
# 包文档编写指南
<<< END U000339 >>>
<<< UNIT U000340 | md-paragraph | docs/package-docs.md:3-3 | ctx=包文档编写指南 >>>
仓库内每个可安装包都在各自的导入包目录下包含一份 `docs/` 目录。文档引擎收集这些目录，合并成 VitePress 站点。同一条目同时供 `akaribot docs list` 与站点构建使用。
<<< END U000340 >>>
<<< UNIT U000341 | md-heading | docs/package-docs.md:5-5 | ctx=目录位置 >>>
## 目录位置
<<< END U000341 >>>
<<< UNIT U000342 | md-paragraph | docs/package-docs.md:7-7 | ctx=目录位置 >>>
`docs/` 必须位于**导入包的根目录**，不是包根目录或仓库根目录的 `docs/`，也不是测试目录。发现过程通过 `akaribot.docs` entry point 的导入路径定位已安装包的目录（不导入包本身），因此 `docs/` 必须随 wheel 一同打包分发。
<<< END U000342 >>>
<<< UNIT U000343 | md-paragraph | docs/package-docs.md:21-21 | ctx=目录位置 >>>
`akaribot/`、`akaribot/modules/` 是 PEP 420 命名空间目录，不得放置 `__init__.py`。`docs/` 下只存放 Markdown、图片、`.txt`/`.pdf` 附件与 `docs/config/` 中的元数据文件，不要提交构建产物或缓存。
<<< END U000343 >>>
<<< UNIT U000344 | md-paragraph | docs/package-docs.md:25-25 | ctx=`docs/config/global/docs.global.toml` >>>
这个文件是包元数据的默认层。包内可以再放置 `docs/config/docs.toml`，按同名键覆盖默认值。两个位置都接受 JSON 文件，文件名分别为 `docs.global.json` 与 `docs.json`。没有 `docs/config/` 时改用旧的 `docs/doc.toml`。
<<< END U000344 >>>
<<< UNIT U000345 | md-table | docs/package-docs.md:27-40 | ctx=`docs/config/global/docs.global.toml` >>>
| 字段 | 说明 |
| --- | --- |
| `schema` | 固定为 `1`。默认按 1 处理，其他值会导致整个文件被忽略 |
| `title` | 站点标题与侧栏名。默认使用导入路径的最后一段。模块文档使用模块名，不使用描述性标题 |
| `summary` | 一句话简介。默认读取包元数据的 Summary |
| `order` | 排序权重，自小到大。默认 500，非整数按 500 处理并告警 |
| `hidden` | 为 `true` 时该包不进入目录 |
| `overview` | 为 `false` 时不生成包级概览页。导航与分组链接指向第一页，侧栏直接列出页面。默认 `true` |
| `kind` | 覆盖分组：`core`、`builtin`、`cli`、`testing`、`module`、`adapter`、`asset` 等 |
| `category` | 侧栏分类，只接受一个字符串。默认不分类 |
| `category_order` | 分类在侧栏中的排序权重，自小到大。同一分类的文档以各自声明为准 |
| `logo` | 相对包目录的图片文件，作为站点顶栏标志的候选。多个包声明时优先采用目录顺序靠前的项 |
| `avatar` | 相对包目录的图片文件，作为命令对话示例中的机器人头像。多个包声明时优先采用目录顺序靠前的项 |
| `[locales.<标签>]` | 该语言的 `title` 与 `summary`。未列出的语言沿用默认值 |
<<< END U000345 >>>
<<< UNIT U000346 | md-paragraph | docs/package-docs.md:42-42 | ctx=`docs/config/global/docs.global.toml` >>>
当 `logo` 或 `avatar` 指向包目录之外或文件不存在时，该项会被忽略并触发告警。当 `category` 写成数组或其他类型时，该项同样会被忽略并触发告警。
<<< END U000346 >>>
<<< UNIT U000347 | md-paragraph | docs/package-docs.md:44-44 | ctx=`docs/config/global/docs.global.toml` >>>
同一分类的包在侧栏放入同一个二级分组。`category_order` 只控制分类之间的顺序，包在分类内仍按 `order`、标题与 key 排序。
<<< END U000347 >>>
<<< UNIT U000348 | md-paragraph | docs/package-docs.md:46-46 | ctx=`docs/config/global/docs.global.toml` >>>
`overview = false` 适用于直接以多页面形式呈现的包。生成器不补充 `index.md`，也不把包根目录路径作为链接。
<<< END U000348 >>>
<<< UNIT U000349 | md-paragraph | docs/package-docs.md:48-48 | ctx=`docs/config/global/docs.global.toml` >>>
`nav`、分组页与包入口指向该包按 `order` 与路径排序后的第一页，侧栏只列出页面。分组内只有一个无概览页的包时，侧栏省略重复的包标题。
<<< END U000349 >>>
<<< UNIT U000350 | md-paragraph | docs/package-docs.md:50-50 | ctx=`docs/config/global/docs.global.toml` >>>
未指定 `kind` 时按 key 推断，其中 `core` / `builtin` / `cli` / `testing` 保持原样，`module-*` 归入模块，`adapter-*` 归入适配器，`assets-*` 归入资源，其余归入 `library`。分组控制导航与分组页。第三方模块包与适配器包分别使用 `module-`、`adapter-` 前缀，避免归入 `library` 分组。
<<< END U000350 >>>
<<< UNIT U000351 | md-heading | docs/package-docs.md:52-52 | ctx=模块属性卡 >>>
## 模块属性卡
<<< END U000351 >>>
<<< UNIT U000352 | md-paragraph | docs/package-docs.md:54-54 | ctx=模块属性卡 >>>
`docs/config/global/docs.global.toml` 支持用 `[[meta.modules]]` 声明页首属性卡，生成器会把它渲染成 `ModuleMeta` 组件，不需要在 Markdown 里手写标签。
<<< END U000352 >>>
<<< UNIT U000353 | md-paragraph | docs/package-docs.md:56-56 | ctx=模块属性卡 >>>
本仓库的模块文档不声明该表，因为模块名、别名与权限已配置在每条命令的 `CommandUsage` 上，页首不再重复。第三方包需要概览表时仍可使用：
<<< END U000353 >>>
<<< UNIT U000354 | md-table | docs/package-docs.md:72-81 | ctx=模块属性卡 >>>
| 字段 | 说明 |
| --- | --- |
| `name` | 模块名，必填 |
| `aliases` | 模块别名 |
| `type` | 能力类型：`command`、`regex`、`rss`、`event` |
| `permission` | 模块级权限：`public`、`admin`、`superuser`、`base_superuser` |
| `platforms` | 仅可用的平台键，如 `QQBot|Group` |
| `excluded` | 排除的平台键 |
| `forced` / `hidden` | 强制开启 / 已隐藏 |
| `note` | 卡片上的补充说明 |
<<< END U000354 >>>
<<< UNIT U000355 | md-paragraph | docs/package-docs.md:83-83 | ctx=模块属性卡 >>>
属性卡描述模块级信息。命令级权限配置在每条命令的 `CommandUsage` 上。一个包注册多个模块时按声明顺序列出。
<<< END U000355 >>>
<<< UNIT U000356 | md-heading | docs/package-docs.md:85-85 | ctx=站点主题与组件 >>>
## 站点主题与组件
<<< END U000356 >>>
<<< UNIT U000357 | md-paragraph | docs/package-docs.md:87-87 | ctx=站点主题与组件 >>>
站点主题由实例 `docs.toml` 的 `[theme].source` 选择：
<<< END U000357 >>>
<<< UNIT U000358 | md-paragraph | docs/package-docs.md:94-94 | ctx=站点主题与组件 >>>
`auto` 会在实例根目录查找 `akari-bot-docs-template`、`vendor/akari-bot-docs-template` 或 `docs-theme`。从仓库源码运行 CLI 时还会使用仓库内的 `vendor/akari-bot-docs-template` submodule。找不到时使用 CLI 内置的最小主题。
<<< END U000358 >>>
<<< UNIT U000359 | md-paragraph | docs/package-docs.md:96-96 | ctx=站点主题与组件 >>>
外部模板在根目录提供 `docs-theme.json`，声明主题目录、VitePress 版本、Node 要求、npm 依赖与生成配置选项。引擎只复制主题目录，不导入主题代码。`akari-bot-docs-template` 的具体要求由其自身的 `docs-theme.json` 声明。
<<< END U000359 >>>
<<< UNIT U000360 | md-paragraph | docs/package-docs.md:98-98 | ctx=站点主题与组件 >>>
从源码克隆运行 CLI 时，`akaribot docs sync-theme` 把 submodule 更新到远端最新提交，`akaribot docs install-deps` 安装或刷新主题依赖。实例可用 `[theme].color = "#rrggbb"` 设置站点主题色，留空则使用主题默认值。
<<< END U000360 >>>
<<< UNIT U000361 | md-paragraph | docs/package-docs.md:100-100 | ctx=站点主题与组件 >>>
`akari-bot-docs-template` 的主题内置以下组件，所有包文档都可直接使用：
<<< END U000361 >>>
<<< UNIT U000362 | md-table | docs/package-docs.md:102-114 | ctx=站点主题与组件 >>>
| 组件 | 用途 |
| --- | --- |
| `<ModuleMeta :modules="..." />` | 模块属性卡。由 `docs/config/global/docs.global.toml` 自动注入，本仓库不使用 |
| `<ModuleConfig />` | 模块没有配置项时使用 |
| `<ModuleConfig table="module_coin" />` | 模块有配置表时给出表名与配置文件路径 |
| `<ModuleData />` | 模块不保存数据时使用 |
| `<ModuleData tables="module_a,module_b" />` | 模块拥有数据表时给出表名与表结构位置 |
| `<ModuleData tables="module_a,module_b" :list="false" />` | 同上，正文随后用表格列出表结构时只显示数量 |
| `<ModuleAlias names="wiki_bot, wbot" />` | 模块级别名，放在章节标题下，对该节所有命令生效 |
| `<NoticeBox type="warning" title="...">…</NoticeBox>` | 提示框，类型可选 `info`、`tip`、`help`、`example`、`warning`、`danger`、`deprecated` |
| `<ChatExample :log="['用户：~whois example.com', '机器人：域名：example.com']" />` | 命令对话示例：`用户：` 与 `机器人：` 前缀区分角色，无前缀的行会自动续接上一条。纯文本消息按行内代码与图片切分。`messages` 中显式设置 `markdown: true` 的消息才按 Markdown 渲染（粗体、斜体、列表、代码块、链接等），原始 HTML 不执行。`![说明](地址)` 在气泡内渲染为缩略图，点击后从缩略图位置展开可缩放、旋转的预览浮层，关闭时收回原位。在地址后加 `{natural}` 表示按原始尺寸展示，适合缩放后宽度过小的竖长图。图片超过视口高度时等比缩小（桌面最高 600px/70vh，移动端 480px/60vh）。`image-width` 固定示例内所有图片的宽度，适合同一气泡内多张图需要对齐的场景。`:card` 在对话末尾渲染机器人卡片，字段为 `title`、`description`、`url`、`image`、`domain`。`botAvatar` 可覆盖机器人头像。只包含三个以上波浪号的行（如 `〰〰〰`）渲染为时间分隔线 |
| `<ChatExample :log="[...]" :buttons="[{ label: '苔藓块', reply: ['机器人：…', '![苔藓块](moss.png)'] }]" />` | 在最后一条机器人初始消息下渲染按钮。`reply` 使用与 `log` 相同的写法，点击后先显示加载动画并预加载其中的图片，再把回复淡入追加到按钮下方。`loading` 可覆盖加载文案，`messages` 可直接传入结构化消息。按钮项嵌套配置 `buttons` 时，回复会带上二级按钮，可用来模拟“查询页面 → 预览/关闭”。`dismiss: true` 表示关闭按钮，点击后删除该按钮所属的整组回复（含后续二级回复），基础消息上的关闭按钮会连同初始回复一起隐藏。`:one-shot="true"` 让同组按钮在任一按钮点击后全部禁用，适合验证码这类一次性选择。尾部图片单独成气泡，多张尾部图片合并到同一气泡。右上角的重置图标清空追加内容与按钮禁用状态 |
| `<CommandUsage usage="wiki set <wikiurl>" :params="['wikiurl=站点地址，会解析为 API 地址']" permission="admin" :aliases="['wiki_start_site']" :options="[{flag: '-l', desc: '只列未完成项'}]" />` | 命令的权限、别名、用法与选项说明。`params` 逐项解释用法里的参数，渲染为支持悬浮提示的字段与参数清单，组件会自动根据括号类型判定参数是否必填（尖括号表示必填，方括号表示可选）。用法行的前缀取自实例核心配置的 `command_prefix` 首项，`prefix` 可覆盖。`type` 只在正则、订阅等非前缀触发方式上声明。`platforms` / `excluded` 标注命令仅可用的平台与排除的平台，值可为平台键（如 `QQBot`、`QQ|Group`、`Web`）或直接填写展示文案，`excluded` 渲染为“Web 不可用” |
<<< END U000362 >>>
<<< UNIT U000363 | md-paragraph | docs/package-docs.md:116-116 | ctx=站点主题与组件 >>>
需要 Markdown 气泡时，用 `messages` 明确标记。`log` 简写始终按纯文本处理：
<<< END U000363 >>>
<<< UNIT U000364 | md-paragraph | docs/package-docs.md:122-122 | ctx=站点主题与组件 >>>
内置的 `bundled` 主题为 `ModuleMeta`、`NoticeBox`、`CommandUsage` 与 `ChatExample` 保留同名组件（`ChatExample` 将图片渲染为缩略图、点击在新标签页打开，不含头像与主题色，气泡文本按纯文本渲染）。`ModuleAlias`、`ModuleConfig`、`ModuleData` 只在外部模板中渲染。
<<< END U000364 >>>
<<< UNIT U000365 | md-paragraph | docs/package-docs.md:124-124 | ctx=站点主题与组件 >>>
`CommandUsage` 的 `params` 参数清单、悬浮提示与 `platforms` / `excluded` 平台徽章同样由外部模板渲染，内置主题只显示用法行。
<<< END U000365 >>>
<<< UNIT U000366 | md-paragraph | docs/package-docs.md:126-126 | ctx=站点主题与组件 >>>
外部模板的组件使用 M3E 配色变量，外观会随读者的主题色、明暗模式与对比度设置自动变化。组件只在构建后的站点中渲染，直接在 Markdown 阅读器里会显示为标签。
<<< END U000366 >>>
<<< UNIT U000367 | md-paragraph | docs/package-docs.md:128-128 | ctx=站点主题与组件 >>>
属性卡由生成器注入，其他组件按需使用，正文仍以 Markdown 为主。数据流向、进程内状态这类补充说明应放在卡片之后的正文段落中。
<<< END U000367 >>>
<<< UNIT U000368 | md-heading | docs/package-docs.md:130-130 | ctx=模块页面结构 >>>
## 模块页面结构
<<< END U000368 >>>
<<< UNIT U000369 | md-paragraph | docs/package-docs.md:132-132 | ctx=模块页面结构 >>>
模块文档通常分为“使用方法”和“安装与开发”两部分，按读者划分内容。
<<< END U000369 >>>
<<< UNIT U000370 | md-paragraph | docs/package-docs.md:134-134 | ctx=模块页面结构 >>>
内置模块不设包级概览页，每个模块各占一页，页面文件名使用模块名，`update&restart` 写作 `update-restart.md`。导航进入第一页。侧栏直接列出命令模块与配置、工具页面，非命令钩子页面归入“钩子”子菜单。
<<< END U000370 >>>
<<< UNIT U000371 | md-list | docs/package-docs.md:136-151 | ctx=模块页面结构 >>>
- `index.md` 是使用方法，面向使用者。只说明模块做什么、怎么触发、会得到什么，以及用户可见的限制与提示，不包含安装命令、配置字段、数据表、依赖与内部实现。
- 每条命令一个 `###` 章节：标题使用命令名，下面接一行 `CommandUsage` 说明权限与别名，再补充一至三句解释参数与行为。需要展示实际对话过程时，在说明后接一个 `ChatExample`。
- 模块有多个子命令组时用 `##` 分组，命令仍使用 `###`，不再单独成页。
- 不要用表格罗列命令。用法行由 `CommandUsage` 按实例配置的命令前缀渲染，未配置前缀时不加。
- 用法里的参数通过 `params` 逐项说明，格式为 `['名称=说明', …]`。名称不带尖括号，占位名称是中文时按原样填写。
- 选项配置在 `options` 中，渲染为列表。字段说明这类小表改成列表，较长的对照表（如颜色名称、谱面定数等）保留表格形式。
- 对话示例使用默认前缀 `~`，只展示仓库默认配置下可直接使用的结果。需要图片结果时用 `![说明](相对路径)` 引用包内图片，图片放在包内 `docs/` 目录下。
- 图片位于消息尾部时会单独成气泡，多张尾部图片共用一个气泡。竖长图缩放到 200px 高度后若宽度过小，可在地址后添加 `{natural}` 以按原始尺寸展示。超过视口高度时仍等比缩小。同一气泡内的多张图需要等宽时，在 `ChatExample` 上设置 `:image-width="320"`。
- 需要展示平台卡片消息时，在 `ChatExample` 上设置 `:card="{ title, description, url, image, domain }"`。
- 订阅类模块的示例按“开启成功 → 时间分隔线 → 实际推送”组织，分隔线使用 `〰〰〰`。
- 需要模拟消息按钮时，在 `ChatExample` 上配置 `buttons`，每项用 `label` 与 `reply` 描述按钮和点击后的回复。回复需要继续附加按钮时在按钮项上嵌套配置 `buttons`，关闭类按钮设置 `dismiss: true`。图片会在点击后才开始加载。
- `development.md` 为“安装与开发”页，面向部署者与维护者，包含安装步骤、配置字段、权限与平台能力、数据表与依赖。不包含玩法规则与命令用法。
- 配置与数据表两节用 `ModuleConfig`、`ModuleData` 说明事实，模块级别名用 `ModuleAlias`。每项只说明一次，不在每条命令上重复。
- `docs/config/global/docs.global.toml` 不声明 `[[meta.modules]]`，页面顶部不再出现模块清单表。声明该表的能力仍然保留，供第三方包使用。
- 其余页面作为补充用法，与上述两页一起出现。内置模块每页对应一个模块，命令仍按 `###` 组织，不按管理、配置、解析器、会话、工具等分类拆页。
- 译文放在 `docs/<语言标签>/` 下，文件名与默认语言一致。某个语言缺少页面时生成器复制默认语言的同名页面，不产生空链接。`docs/config/global/docs.global.toml` 用 `[locales.<标签>]` 覆盖该语言的标题与简介。
<<< END U000371 >>>
<<< UNIT U000372 | md-paragraph | docs/package-docs.md:153-153 | ctx=模块页面结构 >>>
生成器会把同一模块目录下的页面视为同级页面。使用 `akari-bot-docs-template` 时，侧栏只显示一个模块条目，条目名称使用模块名。
<<< END U000372 >>>
<<< UNIT U000373 | md-paragraph | docs/package-docs.md:155-155 | ctx=模块页面结构 >>>
有概览页时默认打开使用方法，无概览页时默认打开第一页。`development.md` 的标签固定为“安装与开发”，不单独出现在侧栏。
<<< END U000373 >>>
<<< UNIT U000374 | md-paragraph | docs/package-docs.md:157-157 | ctx=模块页面结构 >>>
内置回退主题没有标签栏，开发页仍作为普通侧栏页面列出。页面顺序由 `order` 与文件名确定，有概览页时 `index.md` 在最前，`development.md` 始终在最后。
<<< END U000374 >>>
<<< UNIT U000375 | md-heading | docs/package-docs.md:159-159 | ctx=页面与 front matter >>>
## 页面与 front matter
<<< END U000375 >>>
<<< UNIT U000376 | md-paragraph | docs/package-docs.md:161-161 | ctx=页面与 front matter >>>
每个 `.md` 文件对应一个页面，文件名使用小写字母并以连字符分隔单词。页面可带简单 front matter：
<<< END U000376 >>>
<<< UNIT U000377 | md-paragraph | docs/package-docs.md:174-174 | ctx=页面与 front matter >>>
只识别 `title`、`order`、`description`、`submenu` 四个单行键值对，不支持列表或嵌套结构。标题默认提取正文中的第一个一级标题（跳过代码块），没有一级标题时使用文件名。
<<< END U000377 >>>
<<< UNIT U000378 | md-paragraph | docs/package-docs.md:176-176 | ctx=页面与 front matter >>>
包有概览页时 `index.md` 始终排在最前。无概览页的包按 `order` 与路径排序。`submenu` 将同一包内取值相同的页面归入一个无链接的二级分组，分组名称即该字段的值。未设置该字段的页面仍直接列在包下，分组排在直接列出的页面之后。
<<< END U000378 >>>
<<< UNIT U000379 | md-paragraph | docs/package-docs.md:178-178 | ctx=页面与 front matter >>>
文档目录允许包含的文件后缀有 `.md`、`.png`、`.jpg`、`.jpeg`、`.gif`、`.svg`、`.webp`、`.avif`、`.txt`、`.pdf`。其他后缀不进入站点。文档目录中的符号链接不得指向目录之外。
<<< END U000379 >>>
<<< UNIT U000380 | md-heading | docs/package-docs.md:180-180 | ctx=声明 entry point >>>
## 声明 entry point
<<< END U000380 >>>
<<< UNIT U000381 | md-paragraph | docs/package-docs.md:182-182 | ctx=声明 entry point >>>
在包的 `pyproject.toml` 声明 `akaribot.docs`，名称为 key，值为导入路径：
<<< END U000381 >>>
<<< UNIT U000382 | md-list | docs/package-docs.md:189-192 | ctx=声明 entry point >>>
- key 确定 URL、生成目录名与默认分组，必须匹配 `[A-Za-z0-9][A-Za-z0-9._-]*`。
- 值只截取 `:` 之前的导入路径。写成 `akaribot.modules.my_module:app` 也按包路径处理。
- key 重复时，排序靠后的条目会被忽略并触发告警。包已安装但 `docs/` 不存在或没有 Markdown 页面时，系统会跳过该包并记录警告。
- entry point 只在安装时写入包元数据。可编辑安装的包若在安装之后才声明 `akaribot.docs`，发现过程按源码 `pyproject.toml` 的声明补充收录该包并告警。重新安装即可刷新元数据，工作区实例可执行 `akaribot module update --all`。普通安装的包不按源码补充收录。
<<< END U000382 >>>
<<< UNIT U000383 | md-paragraph | docs/package-docs.md:194-194 | ctx=声明 entry point >>>
`akaribot.core` 与 `akaribot.modules.core` 分别以 `core`、`builtin` 提供文档。CLI 的 `cli` 条目由命令行工具自身合并。
<<< END U000383 >>>
<<< UNIT U000384 | md-heading | docs/package-docs.md:196-196 | ctx=命令与生成物 >>>
## 命令与生成物
<<< END U000384 >>>
<<< UNIT U000385 | md-paragraph | docs/package-docs.md:198-198 | ctx=命令与生成物 >>>
`akaribot docs` 提供 `list`、`build`、`serve`、`deploy`、`status`、`clean`：
<<< END U000385 >>>
<<< UNIT U000386 | md-list | docs/package-docs.md:200-205 | ctx=命令与生成物 >>>
- `list`：通过实例的 core 入口读取已安装包目录，入口不可用时回退到注册表清单。
- `build`：生成站点并调用 VitePress。
- `serve`：在本机预览产物。
- `deploy`：发布到 Vercel 或 S3。
- `status`：读取构建与部署状态。
- `clean`：清理生成目录。
<<< END U000386 >>>
<<< UNIT U000387 | md-paragraph | docs/package-docs.md:207-207 | ctx=命令与生成物 >>>
构建需要 Node.js 与 `npm`，版本要求由主题清单确定。依赖由 `npm ci` 安装。生成产物位于实例根目录的 `cache/docs/src`（站点源码）、`cache/docs`（Node 工具链与 `node_modules`）与 `cache/docs/site`（默认输出，可由 `build.out_dir` 改写）。构建校验信息与部署记录保存在 `.docs/state.json`。
<<< END U000387 >>>
<<< UNIT U000388 | md-paragraph | docs/package-docs.md:209-209 | ctx=命令与生成物 >>>
部署目标配置在实例根目录 `docs.toml` 的 `[deploy]` 段。登录信息只从环境变量读取，不写入配置文件与状态文件。基础路径默认为 `/`，环境变量 `AKARIBOT_DOCS_BASE` 优先。
<<< END U000388 >>>
<<< UNIT U000389 | md-heading | docs/package-docs.md:211-211 | ctx=编写规则 >>>
## 编写规则
<<< END U000389 >>>
<<< UNIT U000390 | md-list | docs/package-docs.md:213-219 | ctx=编写规则 >>>
- **简体中文**：包内文档只使用简体中文。面向用户的固定文案仍用 `I18NContext`。不得为文档创建或修改 `locales/` 下 `zh_cn.json` 以外的语言文件，翻译由 Weblate 自动提交。
- **只描述当前行为**：不描述“原来如何、现在改为如何”，变更历史由 git 承担。
- **段落不手动折行**：一个段落写在同一行，由渲染器自动换行。中文没有词间空格，源码中的手动换行会在页面上留下多余空格。
- **一级标题开头**：每页以 `# 标题` 开始，标题与 front matter 的 `title` 一致。
- **篇幅**：单页 40 至 120 行，只覆盖功能概述、基本使用与接口行为。
- **链接**：同包页面使用相对路径。跨包页面按源码目录填写相对路径，生成器会转换为站点 URL，也可直接填写 `/<包 key>/<页面>`。
- **图片与附件**：放在 `docs/` 下用相对路径引用。图片、`.txt` 与 `.pdf` 都会发布到 `/<包 key>/` 路径下，组件内的相对路径同样可用。
<<< END U000390 >>>
<<< UNIT U000391 | md-heading | docs/package-docs.md:221-221 | ctx=最小示例 >>>
## 最小示例
<<< END U000391 >>>
<<< UNIT U000392 | md-paragraph | docs/package-docs.md:248-248 | ctx=最小示例 >>>
`index.md` 以 `# my-module` 开头，说明模块用途，然后按命令分节。安装、配置、权限、数据表与依赖写入 `development.md`。新增页面后运行 `python -m akaribot.core.entrypoints.docs --json` 核对清单与告警，再构建站点。
<<< END U000392 >>>
