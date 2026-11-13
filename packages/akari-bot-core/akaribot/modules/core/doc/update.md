---
order: 58
---

# update

此模块用于更新机器人及其依赖。模块内命令要求超级用户权限。

### `update`

<CommandUsage usage="update [--force]" permission="superuser" :options="[{flag: '--force', desc: '强制重置与更新源代码'}]" />

- 更新由 `akaribot module update --all --non-interactive --defer-runtime --json` 完成。
- 更新在 CLI 子进程中执行。机器人和 Server 进程只读取配置，不直接写盘，也不迁移数据库。
- 二进制封装模式下，命令会拒绝执行，并提示手动下载新版本替换。
- 报告列出成功、失败和跳过的包。
- 存在尚未热装载的包时，提示执行 `restart`。全部包都已热装载时，报告说明已全部热装载。

<ChatExample
  :log="[
    '用户：~update',
    '机器人：更新成功：3 个包（CLI：/usr/local/bin/akaribot，退出码 0）。',
    '成功：akari-bot-core、akari-bot-module-dice、akari-bot-module-petal',
    '以下包尚未热装载：akari-bot-core；请执行 `~restart` 让新版本生效。',
  ]"
/>
