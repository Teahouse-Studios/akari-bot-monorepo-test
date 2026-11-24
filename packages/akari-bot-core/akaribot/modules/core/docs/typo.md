---
order: 34
submenu: 钩子
---

# typo

此 Hook 在命令未匹配到任何模块时提供拼写纠错建议。

说明：

- 仅在 `unmatched_kind == "module"` 且用户未关闭 `typo_check` 时触发。
- 相似度阈值取自 `typo_check_module_score`、`typo_check_command_score`、`typo_check_args_score` 与 `typo_check_options_score`。
- 长度差异比例通过 `typo_check_module_diff_ratio` 控制。
- Hook 将修复建议封装在 `RecoveryProposal` 中返回。是否重试纠正后的命令，通过解析器确定。
