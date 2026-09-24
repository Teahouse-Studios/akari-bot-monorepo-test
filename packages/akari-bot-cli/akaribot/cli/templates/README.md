模块脚手架模板
================

本目录是 ``akaribot new module`` 的渲染输入，由 ``generated_docs/monorepo_refactor_tasks.md``
T5.5 的问卷驱动。生成器尚未落地，因此模板当前不被任何流程引用；本目录随仓库维护，
供生成器实现时直接取用。

模板文件的语法由 ``tools/render_templates.py`` 校验：它用样例值渲染全部模板并检查产物
是否为合法 Python、JSON 或 TOML。模板带 ``.j2`` 后缀，ruff 与其它工具默认跳过，
因此该脚本是模板的语法闸门，改动模板后必须运行。

占位符
------

占位符写成 ``[@name@]``，可安全出现在文件名与正文中：

- Windows 禁止文件名包含 ``<`` ``>``，因此不使用尖括号；
- ``[@name@]`` 不会被 Jinja2 当作表达式求值。

===============  ==========================================
占位符            取值
===============  ==========================================
``[@module_name@]``  模块名，须匹配 ``[a-z0-9_]+``。它同时用作 ``module()`` 注册名、
                     locale 键前缀、表名前缀、目录名与 entry point 名
``[@module_class@]`` 模块名的大驼峰形式。生成器按 ``_`` 分段、逐段首字母大写后拼接，
                     如 ``twenty_four`` → ``TwentyFour``。用于数据库模型的类名
                     （``[@module_class@]Data``）
``[@module_desc@]``  模块的一句话说明，写入 ``module()`` 的 ``desc`` 与 zh_cn 的
                     ``[@module_name@].help.desc``
``[@author@]``       作者名，写入 pyproject 的 ``authors``；模块作者一律由该字段提供，
                     ``module()`` 不再接 ``developers``
``[@license@]``      许可证标识，写入 pyproject 的 ``license``
===============  ==========================================

模块名限制为 ``[a-z0-9_]+`` 有两条硬性理由：多实例的 ``client_name`` 以 ``-``
作分隔符，适配器与模块的 entry point 名不得含 ``-``；TOML 的裸键同样会拒绝 ``-``。

渲染契约
--------

生成器按两步处理，顺序不可颠倒：

1. **路径替换**：复制目录树时，把路径中的 ``[@name@]`` 换成取值，得到
   ``akaribot/modules/<实际模块名>/``；
2. **内容渲染**：用 Jinja2 渲染文件内容，再用同一份取值做一次 ``[@name@]`` 明文替换
   （路径与文本中的占位符都要替换），最后做一次 ``html.unescape``。

第二步的顺序与转义有两处硬性原因：

- 占位符替换必须放在 Jinja2 渲染之后。若把 ``[@module_name@]`` 注册成 Jinja2 变量，
  命令模板 ``"{{I18N:[@module_name@].help.echo}}"`` 里的 ``{{`` 会被 Jinja2 当作表达式
  起始符，模板直接报语法错误。
- 命令模板的 ``{{I18N:key}}`` 标记在本项目里是普通文本，但 Jinja2 会解析它。
  因此模板中把它写成 HTML 实体 ``&#123;&#123;I18N:...&#125;&#125;``，渲染后用
  ``html.unescape`` 还原。这样既不需要 ``jinja2.ext.i18n`` 扩展，也不需要 ``raw`` 标签。

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

`assets/README.md` 与 `database/__init__.py.j2` 的存在有两个作用：保证目录可被 git
跟踪（空目录不会进版本库），并向模块作者说明该目录的用途。生成器不需要删除它们，
`assets/README.md` 会随包分发。

生成后的目录与 ``packages/modules/akari-bot-module-<实际模块名>/`` 同构，可直接
``akaribot module add -e .``。

约定
----

1. 生成的 ``locales/zh_cn.json`` 只含简体中文。其余语言由 Weblate 自动提交，不得由
   生成器写入。
2. 生成的代码一律 ``from akaribot.core.api import ...``，不引入 ``akaribot.core`` 的
   内部路径。该门面在公共 API 契约阶段（P5）建立。
3. ``config.py`` 中的字段名以模块名作前缀，字段注释写在 ``locales/zh_cn.json`` 的
   ``config.comments.module_[@module_name@].<字段名>``。
4. 数据库表名以 ``module_[@module_name@]_`` 作前缀，且不得含 ``-``。
5. 不需要数据库或配置的模块，由生成器删除对应文件与 manifest 中的对应字段，不保留空文件。
