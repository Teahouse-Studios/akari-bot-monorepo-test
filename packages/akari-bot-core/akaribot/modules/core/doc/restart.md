---
order: 56
---

# restart

模块级权限为超级用户。

### `restart`

<CommandUsage usage="restart [--force]" permission="superuser" excluded="Web" :options="[{flag: '--force', desc: '跳过确认与等待强制重启'}]" />

- Web 平台不注册，仅在子进程模式可用。
- 重启全部子进程。
- 默认等待在途命令并确认；60 秒内仍有命令在执行时给出提示。
- `--force` 跳过确认与等待。
- 执行前把发起会话写入 `data/private/<client>/.cache_restart_author`。
- 进程以退出码 33 结束，由守护进程重启全部子进程，完成后提示投递回原场景。

<ChatExample
  :log="[
    '用户：~restart --force',
    '机器人：重启中……',
  ]"
/>
