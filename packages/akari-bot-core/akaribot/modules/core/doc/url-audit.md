---
order: 62
---

# url-audit

模块级权限为超级用户，维护全局 URL 允许与阻止规则。规则存放在实例 `data/url_audit/`，是否启用由 `enable_urlmanager` 控制。

### `url-audit allowlist add`

<CommandUsage usage="url-audit allowlist add <url>" :params="['url=要加入允许列表的 URL']" permission="superuser" />

向用户自定义的全局允许列表添加精确 URL。规则已存在时返回提示。

<ChatExample
  :log="[
    '用户：~url-audit allowlist add https://example.com/news/1',
    '机器人：已将规则加入用户自定义 URL 允许列表：https://example.com/news/1',
  ]"
/>

### `url-audit allowlist add-regex`

<CommandUsage usage="url-audit allowlist add-regex <url>" :params="['url=要加入的正则表达式，需完整匹配']" permission="superuser" />

向允许列表添加正则规则，正则须能完整匹配 URL。规则不合法时返回具体原因。

<ChatExample
  :log="[
    '用户：~url-audit allowlist add-regex https://example.com/(news|blog)/.*',
    '机器人：已将规则加入用户自定义 URL 允许列表：regex:https://example.com/(news|blog)/.*',
  ]"
/>

### `url-audit allowlist remove`

<CommandUsage usage="url-audit allowlist remove <url>" :params="['url=要移除的精确 URL']" permission="superuser" />

从允许列表移除精确 URL，规则不存在时返回提示。

<ChatExample
  :log="[
    '用户：~url-audit allowlist remove https://example.com/news/1',
    '机器人：已从用户自定义 URL 允许列表删除规则：https://example.com/news/1',
  ]"
/>

### `url-audit allowlist remove-regex`

<CommandUsage usage="url-audit allowlist remove-regex <url>" :params="['url=要移除的正则表达式']" permission="superuser" />

从允许列表移除正则规则。

<ChatExample
  :log="[
    '用户：~url-audit allowlist remove-regex https://example.com/(news|blog)/.*',
    '机器人：已从用户自定义 URL 允许列表删除规则：regex:https://example.com/(news|blog)/.*',
  ]"
/>

### `url-audit allowlist query`

<CommandUsage usage="url-audit allowlist query <url>" :params="['url=要查询的 URL']" permission="superuser" />

查询 URL 命中的允许规则，逐条列出规则来源与内容；未命中时提示不被允许。

<ChatExample
  :log="[
    '用户：~url-audit allowlist query https://example.com/news/1',
    '机器人：https://example.com/news/1 已被以下全局规则放行：',
    '[用户规则] regex:https://example.com/(news|blog)/.*',
  ]"
/>

### `url-audit allowlist list`

<CommandUsage usage="url-audit allowlist list" permission="superuser" />

列出全部允许规则，以图片表格展示来源、类型与规则内容；列表为空时返回提示。

<ChatExample
  :log="[
    '用户：~url-audit allowlist list',
    '机器人：全局 URL 允许列表规则：',
    '（图片表格：来源 / 类型 / 规则）',
  ]"
/>

### `url-audit blocklist add`

<CommandUsage usage="url-audit blocklist add <url>" :params="['url=要加入阻止列表的 URL']" permission="superuser" />

向用户自定义的全局阻止列表添加精确 URL。规则已存在时返回提示。

<ChatExample
  :log="[
    '用户：~url-audit blocklist add https://example.com/ads/1',
    '机器人：已将规则加入用户自定义 URL 阻止列表：https://example.com/ads/1',
  ]"
/>

### `url-audit blocklist add-regex`

<CommandUsage usage="url-audit blocklist add-regex <url>" :params="['url=要加入的正则表达式，需完整匹配']" permission="superuser" />

向阻止列表添加正则规则，正则须能完整匹配 URL。规则不合法时返回具体原因。

<ChatExample
  :log="[
    '用户：~url-audit blocklist add-regex https://example.com/ads/.*',
    '机器人：已将规则加入用户自定义 URL 阻止列表：regex:https://example.com/ads/.*',
  ]"
/>

### `url-audit blocklist remove`

<CommandUsage usage="url-audit blocklist remove <url>" :params="['url=要移除的精确 URL']" permission="superuser" />

从阻止列表移除精确 URL，规则不存在时返回提示。

<ChatExample
  :log="[
    '用户：~url-audit blocklist remove https://example.com/ads/1',
    '机器人：已从用户自定义 URL 阻止列表删除规则：https://example.com/ads/1',
  ]"
/>

### `url-audit blocklist remove-regex`

<CommandUsage usage="url-audit blocklist remove-regex <url>" :params="['url=要移除的正则表达式']" permission="superuser" />

从阻止列表移除正则规则。

<ChatExample
  :log="[
    '用户：~url-audit blocklist remove-regex https://example.com/ads/.*',
    '机器人：已从用户自定义 URL 阻止列表删除规则：regex:https://example.com/ads/.*',
  ]"
/>

### `url-audit blocklist query`

<CommandUsage usage="url-audit blocklist query <url>" :params="['url=要查询的 URL']" permission="superuser" />

查询 URL 命中的阻止规则；未命中时提示未被阻止。

<ChatExample
  :log="[
    '用户：~url-audit blocklist query https://example.com/ads/1',
    '机器人：https://example.com/ads/1 已被以下全局规则拦截：',
    '[用户规则] https://example.com/ads/1',
  ]"
/>

### `url-audit blocklist list`

<CommandUsage usage="url-audit blocklist list" permission="superuser" />

列出全部阻止规则，以图片表格展示来源、类型与规则内容；列表为空时返回提示。

<ChatExample
  :log="[
    '用户：~url-audit blocklist list',
    '机器人：全局 URL 阻止列表规则：',
    '（图片表格：来源 / 类型 / 规则）',
  ]"
/>
