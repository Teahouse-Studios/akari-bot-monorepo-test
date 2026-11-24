模块脚手架模板
================

本目录作为 ``akaribot new module`` 的渲染输入，由 ``generated_docs/monorepo_refactor_tasks.md``
T5.5 的问卷驱动。生成器当前未被任何外部流程直接引用。本目录随仓库同步维护，
以供生成器直接使用。

模板文件的语法由 ``tools/render_templates.py`` 校验，它会使用样例值渲染全部模板并检查生成产物
是否为有效 Python、JSON 或 TOML。模板带 ``.j2`` 后缀，ruff 与其他工具默认跳过，
因此该脚本是模板的语法校验关卡，修改模板后必须运行该脚本。

占位符
------

占位符写作 ``[@name@]``，能够安全出现于文件名与正文中：

- Windows 禁止文件名包含 ``<`` ``>``，因此不采用尖括号。
- ``[@name@]`` 不会被 Jinja2 视为表达式求值。

===============  ==========================================
占位符            取值
===============  ==========================================
``[@module_name@]``  模块名称，必须匹配 ``[a-z0-9_]+``。它同时用作 ``module()`` 注册名称、
                     locale 键前缀、数据表名称前缀、目录名与 entry point 名称
``[@module_class@]`` 模块名称的大驼峰形式。生成器按 ``_`` 分段、逐段首字母大写后拼接，
                     如 ``twenty_four`` → ``TwentyFour``。用于数据库模型的数据类名称
                     （``[@module_class@]Data``）
``[@module_desc@]``  模块的一句话说明，写入 ``module()`` 的 ``desc`` 与 zh_cn 的
                     ``[@module_name@].help.desc``
``[@author@]``       作者名称，写入 pyproject 的 ``authors``。模块作者一律由该字段提供，
                     ``module()`` 不接受 ``developers``
``[@license@]``      许可证标识，写入 pyproject 的 ``license``
===============  ==========================================


模块名限制为 ``[a-z0-9_]+`` 具有两项约束原因。多实例的 ``client_name`` 以 ``-``
作为分隔符，适配器与模块的 entry point 名不得包含 ``-``。TOML 的裸键同样不支持包含 ``-``。

渲染约定
--------

生成器分为两步处理，执行顺序不可颠倒：

1. **路径替换**：复制目录树时，将路径中的 ``[@name@]`` 替换为实际取值，生成
   ``akaribot/modules/<实际模块名>/``。
2. **内容渲染**：使用 Jinja2 渲染文件内容，再使用同一组取值执行一次 ``[@name@]`` 明文替换
（路径与文本中的占位符均需要替换），最后执行一次 ``html.unescape``。

第二步的处理顺序与转义具有两项关键原因：

- 占位符替换必须置于 Jinja2 渲染之后。若将 ``[@module_name@]`` 注册为 Jinja2 变量，
  命令模板 ``"{{I18N:[@module_name@].help.echo}}"`` 中的 ``{{`` 会被 Jinja2 视为表达式
  起始符，导致模板直接触发语法错误。
- 命令模板的 ``{{I18N:key}}`` 标记在本项目中属于普通文本，但 Jinja2 会直接对其执行解析。
  因此模板中将其写为 HTML 实体 ``&#123;&#123;I18N:...&#125;&#125;``，渲染后使用
  ``html.unescape`` 还原。以此避免引入 ``jinja2.ext.i18n`` 扩展或 ``raw`` 标签。

.. code-block:: python

    environment = Environment(loader=FileSystemLoader("templates"), undefined=StrictUndefined)
    rendered = environment.get_template(name).render()
    rendered = html.unescape(re.sub(r"\[@([a-z_]+)@\]", lambda m: values[m.group(1)], rendered))

目录结构
--------

::

    module/
      pyproject.toml.j2
      manifest.toml.j2
      README.md
      akaribot/modules/[@module_name@]/
        __init__.py.j2
        config.py.j2
        database/__init__.py.j2
        database/models.py.j2
        migrations/0001_initial.py.j2
        locales/zh_cn.json.j2
        assets/README.md
      tests/test_[@module_name@].py.j2

`assets/README.md` 与 `database/__init__.py.j2` 具有两项作用：一是确保目录能够被 git
跟踪（空目录不会纳入版本库），二是向模块开发者说明该目录的用途。生成器无需删除相关文件，
其中 `assets/README.md` 会随包分发。

生成后的目录与 ``packages/modules/akari-bot-module-<实际模块名>/`` 目录结构一致，可以直接执行
``akaribot module add -e .``。

约定
----

1. 生成的 ``locales/zh_cn.json`` 仅包含简体中文。其余语言由 Weblate 自动提交，不得由
   生成器写入。
2. 生成的代码一律采用 ``from akaribot.core.api import ...``，不引入 ``akaribot.core`` 的
   内部路径。
3. ``config.py`` 中的字段名以模块名作前缀，字段注释保存在 ``locales/zh_cn.json`` 的
   ``config.comments.module_[@module_name@].<字段名>``。
4. 数据库表名以 ``module_[@module_name@]_`` 作为前缀，且不得包含 ``-``。
5. 对于无需使用数据库或配置的模块，由生成器删除对应文件与 manifest 中的对应字段，不保留空文件。
