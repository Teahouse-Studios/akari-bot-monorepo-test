---
order: 58
---

# update

此模块用于更新机器人及其依赖项。模块内命令均需要超级用户权限。

### `update`

<CommandUsage usage="update [--force]" permission="superuser" :options="[{flag: '--force', desc: '强制重置与更新源代码'}]" />

- 更新通过 `akaribot module update --all --non-interactive --defer-runtime --json` 执行。
- 更新在 CLI 子进程中执行。机器人与 Server 进程仅读取配置，不直接写入磁盘，亦不迁移数据库。
- 二进制封装模式下，命令会拒绝执行，并提示手动下载新版本完成替换。
- 执行报告列出成功、失败与跳过的包。
- 若存在尚未热加载的包，机器人会提示执行 `restart`。若全部包均已热加载，报告则说明已全部完成热加载。

<ChatExample
  :log="[
    '用户：~update',
    '机器人：更新成功：3 个包（CLI：/usr/local/bin/akaribot，退出码 0）。',
    '成功：akari-bot-core、akari-bot-module-dice、akari-bot-module-petal',
    '以下包尚未热装载：akari-bot-core；请执行 `~restart` 让新版本生效。',
  ]"
/>
