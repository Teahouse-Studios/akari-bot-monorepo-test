---
order: 58
---

# update

模块级权限为超级用户。

### `update`

<CommandUsage usage="update [--force]" permission="superuser" :options="[{flag: '--force', desc: '强制重置与更新源代码'}]" />

- 更新机器人及其依赖，委托 `akaribot module update --all --non-interactive --defer-runtime --json` 完成。
- 更新由 CLI 子进程执行；机器人与 Server 进程只读配置，不直接写盘或迁移数据库。
- 二进制封装模式下拒绝执行，并提示改用发行包。
- 报告列出成功、失败与跳过的包。
- 存在未热装载的包时提示执行 `restart`，否则说明已热装载。

<ChatExample
  :log="[
    '用户：~update',
    '机器人：更新成功：3 个包（CLI：/usr/local/bin/akaribot，退出码 0）。',
    '成功：akari-bot-core、akari-bot-module-dice、akari-bot-module-petal',
    '以下包尚未热装载：akari-bot-core；请执行 `~restart` 让新版本生效。',
  ]"
/>
