---
order: 63
---

# webrender

此模块用于控制网页渲染服务。模块内命令要求超级用户权限。

### `webrender status`

<CommandUsage usage="webrender status" permission="superuser" />

输出渲染服务的当前状态。

### `webrender start`

<CommandUsage usage="webrender start" permission="superuser" />

启动本地渲染服务。成功后重新检查渲染状态，结果写入运行时记录。

### `webrender stop`

<CommandUsage usage="webrender stop" permission="superuser" />

停止渲染服务，然后重新检查渲染状态，结果写入运行时记录。

<ChatExample
  :log="[
    '用户：~webrender stop',
    '机器人：成功。',
  ]"
/>

### `webrender reload`

<CommandUsage usage="webrender reload" permission="superuser" />

先关闭再启动渲染服务，用于加载新的配置。

服务参数位于 `config/webrender.toml`，包括 `enable`、`browser_type`、`browser_executable_path`、`headless`、`remote_only` 和 `remote_web_render_url`。渲染不可用时，依赖截图的命令按各自的策略降级。
