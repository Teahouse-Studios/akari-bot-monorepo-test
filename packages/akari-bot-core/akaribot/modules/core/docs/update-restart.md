---
order: 59
---

# update&restart

<ModuleAlias names="u&r" />

此模块可以更新机器人，并重启进程。模块内的命令需要超级用户权限。

### `update&restart`

<CommandUsage usage="update&restart [--force]" permission="superuser" excluded="Web" :options="[{flag: '--force', desc: '跳过确认，强制重置与更新源代码并强制重启'}]" />

此命令不注册到 Web 平台，只在子进程模式下可用。执行时先更新，再进入重启流程。

带 `--force` 时跳过确认和等待。不带该选项时，先要求确认，确认后等待其他正在执行的命令结束。更新报告发出后，进程按 `restart` 的流程退出，由守护进程重新拉起全部子进程。

<ChatExample
  :log="[
    '用户：~update&restart --force',
    '机器人：重启中……',
    '更新成功：3 个包（CLI：/usr/local/bin/akaribot，退出码 0）。',
  ]"
/>
