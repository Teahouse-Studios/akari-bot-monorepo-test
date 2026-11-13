# hitokoto

获取随机的一言句子，可指定句子类型。返回内容包含句子正文、作者与出处，并附一言主页链接；繁体中文会话下正文与出处自动转换为繁体。

## 命令

<ModuleAlias names="htkt, yiyan" />

### `hitokoto`

<CommandUsage usage="hitokoto [<msg_type>]" :params="['msg_type=句子类型代码 a 至 l']" permission="public" />

获取一条一言，省略类型时随机选择类型。类型代码取 `a` 至 `l` 之一，代码含义由一言服务定义；代码不在范围内时返回无效类型提示。

<ChatExample
  :log="[
    '用户：~hitokoto k',
    '机器人：忘情不如情忘，绝念不如念绝。',
    '——王常月「有缘」',
    '类型：哲学',
  ]"
/>
