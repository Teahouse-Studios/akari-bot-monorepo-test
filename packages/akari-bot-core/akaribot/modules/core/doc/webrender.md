---
order: 63
---

# webrender

模块级权限为超级用户，控制网页渲染服务。

### `webrender status`

<CommandUsage usage="webrender status" permission="superuser" />

输出渲染服务状态。

### `webrender start`

<CommandUsage usage="webrender start" permission="superuser" />

启动本地渲染服务，成功后刷新运行时记录的渲染状态。

### `webrender stop`

<CommandUsage usage="webrender stop" permission="superuser" />

停止渲染服务，并同步运行时状态。

<ChatExample
  :log="[
    '用户：~webrender stop',
    '机器人：成功。',
  ]"
/>

### `webrender reload`

<CommandUsage usage="webrender reload" permission="superuser" />

先关闭再启动渲染服务，用于加载新的配置。

服务参数在 `config/webrender.toml`，包括 `enable`、`browser_type`、`browser_executable_path`、`headless`、`remote_only` 与 `remote_web_render_url`。渲染不可用时，依赖截图的命令按各自策略降级。
