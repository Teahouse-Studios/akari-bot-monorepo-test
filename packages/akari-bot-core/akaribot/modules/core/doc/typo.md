---
order: 34
submenu: 钩子
---

# typo

命令未匹配到模块时给出拼写建议：

- 只在 `unmatched_kind == "module"` 且用户未关闭 `typo_check` 时触发。
- 相似度阈值取自 `typo_check_module_score`、`typo_check_command_score`、`typo_check_args_score`、`typo_check_options_score`，长度差异比例由 `typo_check_module_diff_ratio` 控制。
- 建议以 `RecoveryProposal` 返回，由解析器决定是否重试纠正后的命令。
