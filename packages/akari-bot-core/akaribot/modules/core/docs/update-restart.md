---
order: 59
---

# update&restart

<ModuleAlias names="u&r" />

此模块用于更新机器人并重启进程。模块内的命令均需要超级用户权限。

### `update&restart`

<CommandUsage usage="update&restart [--force]" permission="superuser" excluded="Web" :options="[{flag: '--force', desc: '跳过确认，强制重置与更新源代码并强制重启'}]" />

此命令不注册至 Web 平台，仅在子进程模式下可用。执行时首先执行更新，随后进入重启流程。

指定 `--force` 选项时跳过确认与等待。未指定该选项时，需要先完成确认，确认通过后等待其他正在执行的命令结束。更新报告发送后，进程按照 `restart` 的流程退出，通过守护进程重新启动全部子进程。

<ChatExample
  :log="[
    '用户：~update&restart --force',
    '机器人：重启中……',
    '更新成功：3 个包（CLI：/usr/local/bin/akaribot，退出码 0）。',
  ]"
/>
