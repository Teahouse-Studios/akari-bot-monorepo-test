---
order: 12
---

# module

此模块可以查看模块清单，也可以启用、停用、加载、重载和卸载模块。命令级权限按子命令区分。`list` 对所有人开放，`enable` 和 `disable` 要求场景管理员，`load`、`reload`、`unload` 要求超级用户。

别名 `enable`、`disable`、`load`、`reload`、`unload` 可以省略 `module` 直接使用，例如 `~enable`。

### `module list`

<CommandUsage usage="module list [--legacy] [--img]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式'}, {flag: '--img', desc: '强制使用图片模式'}]" />

此命令列出当前平台可用的模块及其启用状态。默认以图片表格呈现，指定 `--legacy` 时改用文本表格。

<ChatExample
  :log="[
    '用户：~module list --legacy',
    '机器人：当前可用的模块有：',
    '🔐 arcaea | 🔐 cytoid | 🔐 dice | 🔐 hitokoto',
    '使用“`~help <模块名称>`”查看详细信息。',
  ]"
/>

### `module enable`

<CommandUsage usage="module enable <module>..." :params="['module=要启用的模块名，可给出多个']" permission="admin" />

此命令在当前场景内启用指定模块，一次可以给出多个模块名。

启用前，命令检查平台能力（正则、事件、RSS）和机器人权限。平台能力或机器人权限缺失时，命令给出具体原因。模块声明了推荐模块时，命令随后询问是否一并启用。

<ChatExample
  :log="[
    '用户：~module enable dice',
    '机器人：成功：开启模块“dice”。',
  ]"
/>

### `module enable all`

<CommandUsage usage="module enable all" permission="admin" />

此命令启用全部可启用的模块。基础模块、隐藏模块、仅超级用户授权使用的模块，以及当前平台不支持或缺少机器人权限的模块会被跳过。

<ChatExample
  :log="[
    '用户：~module enable all',
    '机器人：成功：开启模块“arcaea”。',
    '成功：开启模块“dice”。',
    '成功：开启模块“hitokoto”。',
  ]"
/>

### `module disable`

<CommandUsage usage="module disable <module>..." :params="['module=要停用的模块名，可给出多个']" permission="admin" />

此命令在当前场景内停用指定模块。基础模块不能停用。指定基础模块时，命令返回提示，不改动场景配置。

<ChatExample
  :log="[
    '用户：~module disable dice',
    '机器人：成功：关闭模块“dice”。',
  ]"
/>

### `module disable all`

<CommandUsage usage="module disable all" permission="admin" />

此命令停用全部可停用的模块。基础模块、隐藏模块和仅超级用户授权使用的模块会被跳过。

<ChatExample
  :log="[
    '用户：~module disable all',
    '机器人：成功：关闭模块“arcaea”。',
    '成功：关闭模块“dice”。',
    '成功：关闭模块“hitokoto”。',
  ]"
/>

### `module load`

<CommandUsage usage="module load <module>..." :params="['module=要加载的模块名，可给出多个']" permission="superuser" />

此命令加载已卸载的模块，对所有场景生效。

<ChatExample
  :log="[
    '用户：~module load dice',
    '机器人：成功加载模块：dice',
  ]"
/>

### `module reload`

<CommandUsage usage="module reload <module>..." :params="['module=要重载的模块名，可给出多个']" permission="superuser" />

此命令重新加载指定模块。依赖该模块的其它模块会一并重载。重载范围超出给定模块时，命令在执行前列出范围并要求确认。

<ChatExample
  :log="[
    '用户：~module reload dice',
    '机器人：成功重载模块：',
    'dice',
    '未发现已加载的其余文件。',
  ]"
/>

### `module unload`

<CommandUsage usage="module unload <module>..." :params="['module=要卸载的模块名，可给出多个']" permission="superuser" />

此命令卸载已加载的模块，对所有场景生效。基础模块不能卸载。

<ChatExample
  :log="[
    '用户：~module unload dice',
    '机器人：成功卸载模块：dice',
  ]"
/>
