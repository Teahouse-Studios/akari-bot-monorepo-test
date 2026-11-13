---
order: 12
---

# module

命令级权限按子命令区分，`list` 对所有人开放，`enable` 与 `disable` 要求场景管理员，`load`、`reload`、`unload` 要求超级用户。别名 `enable`、`disable`、`load`、`reload`、`unload` 可省略 `module`。

### `module list`

<CommandUsage usage="module list [--legacy] [--img]" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式'}, {flag: '--img', desc: '强制使用图片模式'}]" />

列出当前平台可用的模块及启用状态。默认渲染为图片表格，`--legacy` 改用文本表格。

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

在场景内启用指定模块，一次可给出多个。启用前检查平台能力（正则、事件、RSS）与机器人权限，缺失时给出具体原因；模块声明了推荐模块时，随后询问是否一并启用。

<ChatExample
  :log="[
    '用户：~module enable dice',
    '机器人：成功：开启模块“dice”。',
  ]"
/>

### `module enable all`

<CommandUsage usage="module enable all" permission="admin" />

启用全部可启用模块，跳过基础模块、隐藏模块、仅超级用户授权使用的模块，以及当前平台不支持或缺少机器人权限的模块。

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

在场景内停用指定模块。基础模块不可停用，该情形返回提示而不改动场景配置。

<ChatExample
  :log="[
    '用户：~module disable dice',
    '机器人：成功：关闭模块“dice”。',
  ]"
/>

### `module disable all`

<CommandUsage usage="module disable all" permission="admin" />

停用全部可停用模块，跳过基础模块、隐藏模块与仅超级用户授权使用的模块。

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

加载已卸载的模块，对所有场景生效。

<ChatExample
  :log="[
    '用户：~module load dice',
    '机器人：成功加载模块：dice',
  ]"
/>

### `module reload`

<CommandUsage usage="module reload <module>..." :params="['module=要重载的模块名，可给出多个']" permission="superuser" />

重新加载指定模块。依赖该模块的其它模块一并重载，重载范围超出给定模块时执行前列出范围并要求确认。

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

卸载已加载的模块，对所有场景生效。基础模块不可卸载。

<ChatExample
  :log="[
    '用户：~module unload dice',
    '机器人：成功卸载模块：dice',
  ]"
/>
