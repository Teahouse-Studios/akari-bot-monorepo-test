# 文档内容的自动生成

文档里有一类内容能被源码唯一确定，例如命令选项、配置字段、适配器能力。这类内容由构建期计算、组件渲染，手写副本会与代码不一致。本文说明判定标准、现有通道、组件用法与边界。

## 判定标准

按唯一来源的位置把文档内容分三类。

| 类别 | 特征 | 处理方式 |
| --- | --- | --- |
| 可计算 | 取值在源码或元数据内有唯一答案 | 构建期采集，组件渲染 |
| 半自动 | 主体是清单，附少量人工说明 | 清单部分用组件，说明手写 |
| 手写 | 解释设计、流程、取舍与边界 | 保持手写 |

判断时看只读源码能否得到唯一答案。能写出唯一答案的归入可计算，需要理解意图才能写出的归入手写。

## 现有通道

采集分两端。core 进程能访问全部已安装包，负责读取包内文件。CLI 进程持有命令树，负责自省命令。

```text
core 的 docs 目录 ─┐
                   ├→ catalog JSON → themeConfig.akari.generated → 组件
CLI 命令自省 ──────┘
```

`themeConfig.akari.generated` 的结构：

- `packages[key].facts.config`：配置表数组，每项含 `table`、`file`、`secret` 与 `fields`。
- `packages[key].facts.features`：适配器能力，键为 `Features` 的字段名，值为布尔。
- `packages[key].facts.features_dynamic`：取值来自运行时配置的能力键，仅在存在时出现，不参与矩阵渲染。
- `cli[commandPath]`：命令的 `usage`、`summary`、`arguments` 与 `options`。

采集失败时跳过对应数据，并记入构建 warning，站点照常构建。组件在数据缺失时显示提示。

## 组件

| 内容 | 组件 | 数据来源 |
| --- | --- | --- |
| 命令用法与选项 | `<CliCommandOptions command="module add" />` | Typer 应用 |
| 配置表与字段 | `<ModuleConfigFields table="module_ai" />` | `config.py` 与 locale 注释 |
| 适配器能力矩阵 | `<AdapterCapabilities />` | `features.py` |
| 包依赖 | `<PackageDependencies package="akaribot.core" />` | 分发元数据 |
| 支持语言 | `<SupportedLanguages />` | core 语言清单 |
| 公开接口清单 | `<ApiCatalog />` | `__all__` |

配置表与字段来自 AST 解析，不导入包，因此构建不触发配置读取与网络访问。字段说明取 `locales/zh_cn.json` 的 `config.comments.<表>.<字段>`。注释缺失时该列为空，不在文档里补写。

组件有两份实现，修改一处时同步另一处：外部模板在 `vendor/akari-bot-docs-template/docs/.vitepress/theme/components/content/`，内置回退主题在 `packages/akari-bot-cli/akaribot/cli/docs_engine/template/theme/components/`。前者读 `useAkariConfig()`，后者直接读 `useData().site.value.themeConfig.akari`。

采集端在 `packages/akari-bot-core/akaribot/core/entrypoints/doc_facts.py` 与 `packages/akari-bot-cli/akaribot/cli/docs_engine/facts.py`，写入点在 `generator.py` 的 `_generated_facts` 与 `_attach_generated`。用例在 `packages/akari-bot-core/tests/test_doc_facts.py`、`packages/akari-bot-cli/tests/test_docs_facts.py` 与 `packages/akari-bot-cli/tests/test_docs_generator.py`。

## 新增一类生成内容

1. 确认内容的来源位置。能在包内文件里静态读出时，交给 core 采集。仅 CLI 进程持有该内容时，在 `docs_engine/facts.py` 中采集。
2. 定义最小结构，字段名与源码一致，不做展示层加工。
3. 采集端加用例，覆盖正常结构与解析失败。
4. 组件缺数据时给出可执行的提示，例如运行 `akaribot docs build`。
5. 删去文档里的手写副本。两处并存会分叉。

## 不适合自动生成

- 解释取舍与边界的段落。源码仅能给出结果，无法说明原因。
- 上游副本与许可证正文。这些内容以原文件为准，改动会破坏同源性。
- 版本号与包数量。正文仅指向 `pyproject.toml` 或清单页，不写具体值。
- 运行中的配置值与占位符状态。实例配置随时变化，文档只描述格式。

## 维护流程

改源码后重新构建站点，组件随之更新。评审文档时仅审概念、流程与边界，无需逐项核对可计算内容。

生成结果异常时先看构建 warning。warning 会附带包名与失败原因，例如源码语法错误或 locale 文件解析失败。
