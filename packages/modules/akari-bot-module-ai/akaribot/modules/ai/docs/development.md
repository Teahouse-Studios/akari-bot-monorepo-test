---
title: 安装与开发
---

# ai：安装与开发

<!-- @include: @/_snippets/developer-notice.md -->

## 安装

```bash
akaribot module add akari-bot-module-ai
```

安装后，管理员需要在会话中执行 `module enable ai` 启用模块。

## 配置项

<ModuleConfig table="module_ai" />

<ModuleConfigFields table="module_ai" />

`ai_default_llm` 的取值必须出现在模型清单中。

`e2b_api_key` 声明为敏感项，写入同一配置文件中的 `module_ai_secret` 表。未填写时，代码执行工具不注册。

<ModuleConfigFields table="module_ai_secret" />

模型清单放在实例数据目录 `data/module/ai/` 下：

| 文件 | 内容 |
| --- | --- |
| `llm_api_list.yaml` | `llm_api_list` 列表，每项包含 `name`、`model_name`、`api_url`、`api_key`，可选 `endpoint`（`openai`、`openai-response`、`anthropic`、`gemini`、`gemini-interaction`）、`superuser`、`price_in`、`price_out`、`price_cache_read`、`price_cache_write`、`billing` 与采样参数 |
| `image_api.yaml` | `image_api` 段包含 `model_name`、`base_url`、`api_key` 与 `costs`，缺少 `model_name` 时图像工具不会注册 |
| `instructions.txt`、`persona.txt` | 覆盖包内默认的系统提示与人格提示 |

## 权限与平台能力

命令对运行平台无特殊限制。会话是否支持引用回复，控制着对话处理是逐条等待回复还是连续发送。

网页抓取工具依赖 WebRender（`webrender.enable`），搜索工具使用 ddgs。花瓣计费仅在 core 开启花瓣系统时生效，余额不足时，调用会在发出前终止。会话级设置写入 Union 数据，包括会话默认模型 `ai_default_llm`、个人开关 `ai_enable_persona` 与 `ai_custom_instructions`。

## 数据表

<ModuleData />

会话设置保存在 core 的 Union 数据中。对话上下文是进程内缓存，服务重启即失效。

## 依赖与外部服务

依赖 `openai`、`anthropic`、`google-genai`、`e2b-code-interpreter`、`ddgs`、`trafilatura`、`matplotlib`、`Pillow`、`pyyaml`、`orjson`、`filetype`、`akari-bot-html2text` 与 `akari-bot-core`。

外部服务包括 YAML 清单指定的模型接口、E2B 代码沙箱、ddgs 搜索与 WebRender。

模块提供 Hook `ai.ask`，供其他模块发起对话调用，该 Hook 未设置超时时限。输入参数包括 `prompt`、`instructions`、`llm` 与 `use_tools`，返回结果包含 `status`、`text`、`chain`、`petal` 与 `llm`。
