---
order: 59
---

# update&restart

<ModuleAlias names="u&r" />

模块级权限为超级用户。

### `update&restart`

<CommandUsage usage="update&restart [--force]" permission="superuser" excluded="Web" :options="[{flag: '--force', desc: '跳过确认，强制重置与更新源代码并强制重启'}]" />

Web 平台不注册，仅在子进程模式可用。先更新再走重启流程。`--force` 跳过确认与等待，其余情形先确认并等待在途命令；更新报告发出后进程按 `restart` 的流程结束，由守护进程拉起全部子进程。

<ChatExample
  :log="[
    '用户：~update&restart --force',
    '机器人：重启中……',
    '更新成功：3 个包（CLI：/usr/local/bin/akaribot，退出码 0）。',
  ]"
/>
