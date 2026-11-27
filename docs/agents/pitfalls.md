# 陷阱

以下均为当前必须遵守的约束，改动相关代码时请勿回退。

## 测试框架

- `akaribot/testing/__init__.py` 不得静态导入 `.tester`，否则会间接引入 core，使合并日志目录在隔离
  环境变量就位之前被固定到仓库 `data/`。公开名称按需解析。
- 按需加载的公开接口中不得引入同名辅助名称，`from typing import Any` 会通过
  `from akaribot.testing import Any` 遮蔽框架自身的 `Any` 匹配器（辅助名称一律以下划线开头）。
- 根目录 `bot.py` / `tester.py` 兼容实现使用 `sys.modules` 模块别名，不要逐个名称重新导出。
  用例会为模块级变量赋值再由同模块函数读取，逐个名称重新导出时赋值写在兼容实现上。

## 配置

- `CFGManager.load()` 扫描 `config/*.toml` 与 `config/global/*.global.toml|.global.json`，因此适配器
  实例配置必须写扁平路径（`config/<表名>.toml`）。写到 `config/adapters/` 的表对 core 不可见。
- `config set` 需要按模板声明的类型转换，否则布尔项会被保存为字符串 `"true"`。实例表名
  （`bot_telegram-alt`）由基础表（`bot_telegram`）生成，查询声明时要按前缀匹配。

## CLI 与打包

- Nuitka 打包后 `sys.executable` 指向二进制文件自身，CLI 包内禁止使用它启动实例进程（B11 检查），
  解释器一律通过 `akaribot.cli.instance.system_python()` 获取。

## TUI

- Textual：页面自有方法与属性不得与基类成员同名（`_render`、`offset` 等，覆盖 `Widget._render()`
  会导致容器视图（visual）变为 `None`）。切换页面后必须将焦点切换到该页，否则该页的快捷键不会生效。
  隐藏页面应跳过定时轮询。

## i18n

- `i18n.t()` 的占位符名称不得与形参同名，例如 `${key}` 配 `t(key=…)` 会抛
  `TypeError: t() got multiple values for argument 'key'`。占位符与实参一律使用有具体含义的名称
  （`${field}` / `field=`），修改键名后请核对调用处的关键字参数与模板占位符是否一致。

## 资产与依赖

- 品牌资产（立绘、标志、制作人员名单）是画师提供的原件，不得为压缩体积重新编码。它们随
  `akari-bot-assets-brand` 安装，该包属于 core 的 `full` extra。缺失时由使用方降级处理，不抛出异常。
- `uv.lock` 是唯一来源。workspace 覆盖会忽略内部版本约束，仅在从 wheel 安装时才会通过真实的依赖
  解析器（由 `tools/clean_room_check.py` 负责）。
