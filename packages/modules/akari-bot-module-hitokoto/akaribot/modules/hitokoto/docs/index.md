# hitokoto

此模块用于获取一言服务提供的随机句子，也可以指定句子类型。返回内容包含句子正文、作者与出处，并附带一言主页链接。繁体中文会话下，正文与出处会自动转换为繁体中文。

## 命令

<ModuleAlias names="htkt, yiyan" />

### `hitokoto`

<CommandUsage usage="hitokoto [<msg_type>]" :params="['msg_type=句子类型代码 a 至 l']" permission="public" />

此命令用于获取单条句子。若未指定类型，将随机选择句子类型。类型代码取 `a` 至 `l` 之一，代码含义由一言服务定义。若代码超出取值范围，将返回无效类型提示。

<ChatExample
  :log="[
    '用户：~hitokoto k',
    '机器人：忘情不如情忘，绝念不如念绝。',
    '——王常月「有缘」',
    '类型：哲学',
  ]"
/>
