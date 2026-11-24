适配器脚手架模板
================

本目录作为 ``akaribot new adapter`` 的渲染输入。占位符沿用 ``templates/module/`` 所定义的五个名称：

===============  ==========================================
占位符            取值
===============  ==========================================
``[@module_name@]``  适配器名称，必须匹配 ``[a-z0-9_]+``。它同时用作目录名、包名后缀、entry
                     point 名称、``on_bot_config()`` 的平台名与 locale 键前缀
``[@module_class@]`` 适配器名称的大驼峰形式，用作 ``ContextManager`` 与配置类的类名前缀
``[@module_desc@]``  适配器的一句话说明
``[@author@]``       作者名称
``[@license@]``      许可证标识
===============  ==========================================


复用同一套占位符名称是为了让 ``tools/render_templates.py`` 的样例渲染无需修改即可覆盖本目录：
它仅识别上述五个名称，其余取值一律通过 Jinja 变量传入并携带 ``default``，因此样例渲染不会失败。

目录与正文的分工
----------------

- **路径**：`akaribot/adapters/[@module_name@]/` 的目录名在复制时替换。
- **正文**：Jinja 变量负责能力清单、配置字段等结构化取值，占位符负责名称与文案。

维护工具
--------

`TEMPLATE.md` 与 `selfcheck.py` 由生成器跳过，不随生成产物分发。修改模板后执行一次自检：

```bash
.venv/bin/python templates/adapter/selfcheck.py <生成目录>
```

它对该目录下的每个 `akari-bot-adapter-*` 运行 ruff check / ruff format（仓库配置与 ruff 默认配置
分别执行一次）、tomllib 解析、entry point 名称与 core 约束检查，以及导入边界检查。
