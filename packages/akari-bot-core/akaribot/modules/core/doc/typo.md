---
order: 34
submenu: 钩子
---

# typo

此 Hook 在命令没有匹配到任何模块时给出拼写建议。

说明：

- 只在 `unmatched_kind == "module"` 且用户未关闭 `typo_check` 时触发。
- 相似度阈值取自 `typo_check_module_score`、`typo_check_command_score`、`typo_check_args_score` 和 `typo_check_options_score`。
- 长度差异比例由 `typo_check_module_diff_ratio` 控制。
- Hook 把建议放在 `RecoveryProposal` 中返回。是否重试纠正后的命令，由解析器决定。
