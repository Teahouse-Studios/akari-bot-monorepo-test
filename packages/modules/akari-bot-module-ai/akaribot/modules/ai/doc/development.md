---
title: 安装与开发
---

# ai：安装与开发

本页说明 `ai` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-ai
```

安装后在会话中由管理员用 `module enable ai` 开启。

## 配置

普通配置在 `module_ai` 表（`config/module_ai.toml`），敏感项在 `module_ai_secret`。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ai_default_llm` | str | 空 | 默认使用的大语言模型，须出现在模型清单中 |
| `llm_timeout` | float | 60 | 请求超时时间（秒） |
| `llm_max_tokens` | int | 2048 | 单次回复的最大 Token 数 |
| `llm_temperature` | float | 1.0 | 温度采样，范围 0 到 2 |
| `llm_top_p` | float | 1.0 | 核采样，范围 0 到 1 |
| `llm_frequency_penalty` | float | 0.0 | 频率惩罚，范围 -2 到 2 |
| `llm_presence_penalty` | float | 0.0 | 存在惩罚，范围 -2 到 2 |
| `llm_max_calling_iteration` | int | 5 | 工具调用的最大迭代次数 |
| `ai_cost_to_petal` | float | 1.0 | 花瓣与调用费用的比率 |
| `llm_top_logprobs` | int | -1 | 候选 Token 对数概率数量，负数不传入 |
| `e2b_api_key`（`module_ai_secret`） | str | 空 | E2B 沙箱密钥，未填写时代码执行工具不注册 |

完整清单见配置模板 `akaribot/modules/ai/config.py`。模型清单位于实例数据目录 `data/module/ai/`：

- `llm_api_list.yaml`：`llm_api_list` 列表，每项含 `name`、`model_name`、`api_url`、`api_key`，可选
  `endpoint`（`openai`、`openai-response`、`anthropic`、`gemini`、`gemini-interaction`）、
  `superuser`、`price_in`、`price_out`、`price_cache_read`、`price_cache_write`、`billing` 与采样参数。
- `image_api.yaml`：`image_api` 段含 `model_name`、`base_url`、`api_key` 与 `costs`，缺少
  `model_name` 时图像工具不注册。
- `instructions.txt`、`persona.txt`：覆盖包内默认的系统提示与人格提示。

## 权限与平台能力

- 命令对平台无限制；会话是否支持回复决定对话是逐条等待还是连续发送。
- 网页抓取工具依赖 WebRender（`webrender.enable`），搜索工具使用 ddgs。
- 花瓣计费仅在 core 开启花瓣系统时生效，余额不足时调用前即终止。
- 会话级设置写入 Union 数据：会话默认模型 `ai_default_llm`，个人开关 `ai_enable_persona` 与
  `ai_custom_instructions`。

## 数据表

manifest 未声明 `owned_tables`。会话设置存于 core 的 Union 数据，对话上下文为进程内缓存，
服务重启即失效。

## 依赖与外部服务

- 依赖：`openai`、`anthropic`、`google-genai`、`e2b-code-interpreter`、`ddgs`、`trafilatura`、
  `matplotlib`、`Pillow`、`pyyaml`、`orjson`、`filetype`、`akari-bot-html2text`、`akari-bot-core`。
- 外部服务：YAML 清单指定的模型接口、E2B 代码沙箱、ddgs 搜索、WebRender。
- 模块 hook：`ai.ask`（无超时）供其他模块调用一次对话，参数含 `prompt`、`instructions`、`llm`、
  `use_tools`，返回 `status`、`text`、`chain`、`petal`、`llm`。
