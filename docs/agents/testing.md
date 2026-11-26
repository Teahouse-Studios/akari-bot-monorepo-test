# 测试

本文记录用例的编写规范与运行方式。框架细节参见
`packages/akari-bot-testing/akaribot/testing/docs/index.md` 与
`packages/akari-bot-testing/akaribot/testing/docs/writing-tests.md`。

测试数量本身也是维护成本，每个用例都要随代码演进同步修改，冗余用例会拖慢 CI 并掩盖真正的失败信号。
新增测试前先确认删除该用例会遗漏哪个真实缺陷，无法说明时不要编写。

## 运行

- 本地仅运行与改动相关的入口（`.venv/bin/python tests/run_one.py <包内用例路径> [入口名]`），
  全量测试留给 CI 执行。
- 必须设置 `CI=1`，否则无 `Expectation` 的用例会调用 `input()` 等待人工复核。设置 `CI=1` 时会转为
  SKIP 并输出 `junit.xml`。
- 全量测试的失败清单必须与基准按名称一一对应，基准是 `tools/test_baseline.txt`，
  通过 `tools/check_test_baseline.py` 对比。只读测试另用 `tools/test_baseline_readonly.txt`。
- CI 按文件在收集顺序中的序号把用例拆到多个分片并行执行，分片规则见 `.github/scripts/test_shard.py`。
  各分片的 junit 合并后与同一份基准对比，基准因此不随分片数变化。
- 不要使用固定 `sleep` 等待，需要超时等待时使用 `akaribot.testing.timing.TIME_SCALE`。

## 编写

- 先搜索再编写。新增前用 `grep` 检查现有测试是否已覆盖同一行为。已覆盖则扩展原用例，不要新建用例。
- 改动行为时应同步替换旧测试，不要新旧并存。删除功能必须同时删除对应测试与 `tests/fixtures/` 中
  未被引用的 fixture。
- 仅检查可观察行为：返回值、发出的消息、持久化结果、权限与安全判定。不要检查 mock 的调用次数、
  私有属性与私有函数、日志原文。
- 无需测试的内容：构造器与默认值、常量、getter/setter、标准库或第三方库的直接转发、
  仅检查“不抛出异常”的基本检查用例。
- 一个行为一个用例。同一行为的不同输入变体应在同一用例内通过循环或参数表覆盖，不要每个变体注册一个
  `tester.test`。修复缺陷时，仅在现有测试未覆盖该场景时补充回归用例，并放入该功能原有的测试里。
- 不编写重复的对称用例。代码路径相同的对称场景（如发送方与目标方、群聊与私聊、各平台各一份
  “缺失媒体被跳过”）仅需测试其一。仅当代码路径确实分叉时才分别覆盖。
- 必须保留、不得为精简而删除：安全与权限判定、数据迁移与一致性、并发与锁，以及每个功能的主路径。
- 每个 `_test_` 函数必须被 `tester.test` 注册，未注册的函数永远不会运行，属于无效代码。
- 按主题组织文件。一个功能（模块、适配器、子系统）对应一个测试文件，在其内追加。不要新建
  `test_more_*` / `test_*_more` / `test_*_fixes` 这类零散补充文件。包内用例放在
  `packages/<包名>/tests/`，命名与根目录 `tests/` 保持一致。
- 集成测试（位于根目录 `tests/integration/`）每个命令仅保留一条主路径加必要的、行为不同的错误路径。
  能用纯函数单元测试覆盖的逻辑不要放入集成测试，因为它们依赖录制的 HTTP fixture。
- 用例描述（`tester.test` 的第二个参数）描述被验证的行为，不记录实现细节。测试中同样遵守
  “仅描述当前状态”的注释约定。

## 环境

- 测试不读取本机配置，`akaribot.testing` 会将配置模板部署至临时目录（`AKARI_CONFIG_PATH`）
  再叠加测试覆盖项。
- 需要非默认配置值时，使用 `mock_config(CoreConfig, 字段=值)` 在进程内覆盖，无需读写配置文件，
  且字段必须是模板类中已声明的项。
- 测试使用 `akaribot/testing/mock/parser.py` 的简化解析器，不检查模块是否启用，并将测试发送者设为
  superuser。“测试通过”不代表命令在真实平台上可以正常触发。HTTP 由 `tests/fixtures/http/` 录制回放。
