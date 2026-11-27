# 脚手架模板

本目录作为 `akaribot new module` 与 `akaribot new adapter` 的渲染输入。两个子命令分别读取 `module/` 与
`adapter/` 模板树，用问卷答案替换占位符后写出包目录。

模板语法由 `tools/render_templates.py` 校验。脚本用样例值渲染全部 `.j2` 模板，检查产物是否为有效
Python、JSON 或 TOML。模板带 `.j2` 后缀，ruff 与其他工具默认跳过，因此该脚本是模板的语法检查关卡。
改完模板必须运行该脚本检查语法：

```sh
.venv/bin/python tools/render_templates.py
```

## 占位符

占位符写作 `[@name@]`，可以安全出现在文件名与正文中：

- Windows 禁止文件名包含 `<` 与 `>`，因此不用尖括号。
- `[@name@]` 不会被 Jinja2 视为表达式求值。

| 占位符 | 取值 |
| --- | --- |
| `[@module_name@]` | 模块名，必须匹配 `[a-z0-9_]+`。同时用作 `module()` 注册名、locale 键前缀、数据表名前缀、目录名与 entry point 名 |
| `[@module_class@]` | 模块名的大驼峰形式。生成器按 `_` 分段、逐段首字母大写后拼接，如 `twenty_four` 变成 `TwentyFour`，用于数据库模型的数据类名（`[@module_class@]Data`） |
| `[@module_desc@]` | 模块的一句话说明，写入 `module()` 的 `desc` 与 zh_cn 的 `[@module_name@].help.desc` |
| `[@author@]` | 作者名，写入 pyproject 的 `authors`。模块作者一律由该字段提供，`module()` 不接受 `developers` |
| `[@license@]` | 许可证标识，写入 pyproject 的 `license` |

模块名限制为 `[a-z0-9_]+` 有两项原因。多实例的 `client_name` 以 `-` 作分隔符，适配器与模块的 entry
point 名不得包含 `-`。TOML 的裸键同样不支持 `-`。

## 渲染约定

生成器分两步处理，顺序不可颠倒：

1. **路径替换**：复制目录树时，把路径中的 `[@name@]` 替换为实际取值，得到
   `akaribot/modules/<模块名>/`。
2. **内容渲染**：用 Jinja2 渲染文件内容，再执行一次 `[@name@]` 明文替换，最后执行一次
   `html.unescape`。

第二步的顺序与转义有两项原因：

- 占位符替换必须放在 Jinja2 渲染之后。若把 `[@module_name@]` 注册为 Jinja2 变量，命令模板
  `"{{I18N:[@module_name@].help.echo}}"` 里的 `{{` 会被当成表达式起始符，模板直接触发语法错误。
- 命令模板的 `{{I18N:key}}` 标记在本项目中属于普通文本，Jinja2 会解析它。因此模板写成 HTML 实体
  `&#123;&#123;I18N:...&#125;&#125;`，渲染后用 `html.unescape` 还原。这样不必引入
  `jinja2.ext.i18n` 扩展或 `raw` 标签。

```python
environment = Environment(loader=FileSystemLoader(TEMPLATE_ROOT), undefined=StrictUndefined)
rendered = environment.get_template(name).render()
rendered = html.unescape(re.sub(r"\[@([a-z_]+)@\]", lambda m: values[m.group(1)], rendered))
```

## 目录结构

```text
module/
  .github/workflows/publish.yml
  pyproject.toml.j2
  manifest.toml.j2
  README.md.j2
  akaribot/modules/[@module_name@]/
    __init__.py.j2
    config.py.j2
    manifest.toml.j2
    database/__init__.py.j2
    database/models.py.j2
    migrations/__init__.py.j2
    migrations/0001_initial.py.j2
    locales/zh_cn.json.j2
    assets/.gitkeep
  tests/test_[@module_name@].py.j2

adapter/
  pyproject.toml.j2
  README.md.j2
  TEMPLATE.md
  selfcheck.py
  akaribot/adapters/[@module_name@]/
    __init__.py.j2
    bot.py.j2
    config.py.j2
    context.py.j2
    features.py.j2
    info.py.j2
    manifest.toml.j2
    locales/zh_cn.json.j2
```

`assets/.gitkeep` 与 `database/__init__.py.j2` 让空目录进入版本库，同时向模块开发者说明目录用途。`.gitkeep` 随包分发。

生成后的目录与 `packages/modules/akari-bot-module-<模块名>/` 结构一致，可直接执行 `akaribot module add -e .`。

## 约定

1. 生成的 `locales/zh_cn.json` 仅包含简体中文，其余语言由 Weblate 自动提交，生成器不写入。
2. 生成的代码一律采用 `from akaribot.core.api import ...`，不引入 `akaribot.core` 的内部路径。
3. `config.py` 中的字段名以模块名作前缀，字段注释保存在 `locales/zh_cn.json` 的
   `config.comments.module_[@module_name@].<字段名>`。
4. 数据库表名以 `module_[@module_name@]_` 作前缀，且不得包含 `-`。
5. 无需数据库或配置的模块，生成器按问卷选项跳过对应文件与 manifest 字段，不生成空文件。
