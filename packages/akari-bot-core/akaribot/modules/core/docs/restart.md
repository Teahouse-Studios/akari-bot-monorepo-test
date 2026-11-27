---
order: 56
---

# restart

此模块用于重启全部子进程。模块级权限为超级用户。

### `restart`

<CommandUsage usage="restart [--force]" permission="superuser" excluded="Web" :options="[{flag: '--force', desc: '跳过确认与等待强制重启'}]" />

- 默认等待正在执行的命令结束，并请求确认。若 60 秒内仍有命令处于执行状态，机器人会输出提示信息。
- `--force` 跳过确认与等待。
- 执行前将发起会话写入 `data/private/<client>/.cache_restart_author`。
- 进程以退出码 33 结束，通过守护进程重启全部子进程。重启完成后，机器人会在原场景发送提示信息。
- Web 平台不注册此命令，仅在子进程模式下可用。

<ChatExample
  :log="[
    '用户：~restart --force',
    '机器人：重启中……',
  ]"
/>
