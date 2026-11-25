# 架构

本文记录跨文件才能看清的结构约束，包括包布局、包发现、导入边界、进程间通信与 CLI 子命令。
运行时细节参见 `packages/akari-bot-core/akaribot/core/docs/architecture.md`。

## 包布局

```text
packages/
  akari-bot-core/        akaribot.core（运行时与公共设施）+ akaribot.modules.core（内置模块）
  akari-bot-testing/     akaribot.testing（自研测试框架与运行器）
  akari-bot-cli/         akaribot.cli（实例管理 CLI 与 TUI，不依赖 core）
  akari-bot-html2text/   html2text（独立分发的内嵌副本）
  akari-bot-assets-*/    字体、表情、品牌资产，各自一个分发
  modules/…              akaribot.modules.<名>，各自一个分发
  adapters/…             akaribot.adapters.<名>，各自一个分发
```

## 结构约束

- `akaribot`、`akaribot.modules`、`akaribot.adapters`、`akaribot.assets` 是 PEP 420 命名空间目录，
  不得有 `__init__.py`。`akaribot.core`、`akaribot.testing`、各模块、适配器与资源包是常规包。
- 包发现通过 entry points（`akaribot.modules` / `akaribot.adapters`）完成，目录扫描仅作为备用方案。
  每个包在自己的导入包目录下有 `manifest.toml`，locales、assets 与 migrations 均相对该文件解析。
- 模块仅导入 `akaribot.core.api` 的公开接口，适配器额外导入 `akaribot.core.api.adapters`。
  core 内部出现循环依赖时改用 `akaribot.core.exports` 注册，需要时按名称取回。
- CLI 与 core 之间仅通过子进程通信，入口为
  `python -m akaribot.core.entrypoints.{run,registry,config,data,db,peers,modules,docs,rpc}`。
- 内部依赖约束必须与各包 `pyproject.toml` 中的声明完全一致。官方模块包之间不得互相依赖。

## CLI 子命令

`.venv/bin/akaribot <子命令> --help`，子命令为 init、run、test、module、config、adapter、db、
instance、service、venv、logs、doctor、new、tui、migrate、docs。

`migrate legacy` 将旧版布局的部署迁移到新实例目录。`logs` 读取实例的日志文件，界面日志页复用同一套
解析规则。
