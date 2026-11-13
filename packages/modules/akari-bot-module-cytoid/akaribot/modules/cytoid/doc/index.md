# cytoid

查询 Cytoid 玩家资料，生成 B30（最佳 30 首）与 R10（最近 10 首）成绩图，并按发送者保存账号绑定。

## 命令

<ModuleAlias names="ctd" />

### `cytoid profile`

<CommandUsage usage="cytoid profile [<username>]" :params="['username=Cytoid 用户名']" permission="public" />

查询用户资料，输出头像与经验、等级、Rating、评级分布。省略用户名时查询发送者的绑定账号，未绑定时提示先执行 `cytoid bind`；用户不存在时返回未找到提示。

<ChatExample
  :log="[
    '用户：~cytoid profile',
    '机器人：未绑定用户，请使用“`~cytoid bind`”绑定一个用户。',
  ]"
/>

### `cytoid b30`

<CommandUsage usage="cytoid b30 [<username>]" :params="['username=Cytoid 用户名']" permission="public" />

生成 B30 成绩图。省略用户名时查询发送者的绑定账号，未绑定时提示先执行 `cytoid bind`；取数失败时返回获取失败提示。

<ChatExample
  :log="[
    '用户：~cytoid b30 wdljt',
    '机器人：![B30 成绩图](b30-wdljt.webp)',
  ]"
/>

### `cytoid r10`

<CommandUsage usage="cytoid r10 [<username>]" :params="['username=Cytoid 用户名']" permission="public" />

生成 R10 成绩图。参数与取数流程同 `cytoid b30`，未绑定时提示先执行 `cytoid bind`。

<ChatExample
  :log="[
    '用户：~cytoid r10 skisk',
    '机器人：![R10 成绩图](r10-skisk.webp)',
  ]"
/>

### `cytoid bind`

<CommandUsage usage="cytoid bind <username>" :params="['username=要绑定的 Cytoid 用户名']" permission="public" />

绑定 Cytoid 用户名。绑定按发送者记录，同一用户在任意会话中都可使用；用户名不存在时返回绑定失败提示。

<ChatExample
  :log="[
    '用户：~cytoid bind cytoid',
    '机器人：绑定成功：Cytoid Admin(cytoid)',
  ]"
/>

### `cytoid unbind`

<CommandUsage usage="cytoid unbind" permission="public" />

解除发送者的账号绑定。绑定记录删除后，查询类命令需要重新执行 `cytoid bind`。

<ChatExample
  :log="[
    '用户：~cytoid unbind',
    '机器人：解绑成功。',
  ]"
/>
