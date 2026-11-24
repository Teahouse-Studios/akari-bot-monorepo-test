# 提交与版本

本文记录改动进入仓库前必须满足的提交与版本约束。命令、分支与检查项参见
`packages/akari-bot-core/akaribot/core/docs/development-workflow.md`。

## 授权

- 不要擅自提交。所有改动保留在未提交的工作区，交由用户自行检视与提交。
- 除非用户明确授权自动提交，否则不执行 `git commit`。`git add`、`git push`、`git reset`、
  `git checkout -- <文件>` 等会改动暂存区、历史或丢弃工作区内容的操作同样需要用户授权。
- 新功能分支使用 `dev/` 前缀，修复分支使用 `fix/` 前缀，分支名使用英文。

## 版本

- 版本检查（`tools/check_versions.py`）要求包内有源码改动即升级 `version`，或在提交信息最后一段
  写一条独立的提交尾注（trailer）。`Skip-Version: true` 豁免全部成员，`Skip-Version: <包名>[, <包名>]`
  仅豁免列出的成员。正文中间或缩进处提到该标记不视为声明。
- 版本检查在 tester 中以目标分支为基准运行，仅报告不阻断（`continue-on-error`），因为版本号是发布
  元数据，tester 的结论仅取决于代码与测试。重复版本由 PyPI 在发布时拒绝。发布前按输出的违规清单
  逐包升级 `version` 或添加提交尾注。
- 内部依赖约束必须与各包 `pyproject.toml` 中的声明完全一致。官方模块包之间不得互相依赖。

## 移动与重命名

- 移动文件使用 `git mv` 以保留历史追溯记录（blame）。根目录同时保留同名兼容实现时 git 不会记录为
  重命名，需要“先移动文件、再修改内容”两段提交。

## 提交前检查

提交前依次执行 `ruff check .`、`ruff format --check .`、`tools/lint_comments.py`、
`tools/lint_boundaries.py`、`tools/lint_versions.py`，每一项均覆盖整个仓库，命令见 `AGENTS.md` 的
“六、提交前验证”。

全量测试的失败清单必须与 `tools/test_baseline.txt` 按名称一一对应。
