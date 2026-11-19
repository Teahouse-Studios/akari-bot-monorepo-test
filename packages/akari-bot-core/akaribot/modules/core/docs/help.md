---
order: 43
---

# help

此模块输出模块清单和命令帮助。

### `help`

<CommandUsage :usage="['help [--legacy] [--img]', 'help <module> [--legacy] [--img]']" :params="['module=模块名或别名']" permission="public" :options="[{flag: '--legacy', desc: '强制使用文本模式'}, {flag: '--img', desc: '强制使用图片模式'}]" />

说明：

- 省略模块名时，按当前场景列出可用模块的清单和启用状态。
- 清单带锁定和订阅标记，并提供启用、停用入口。
- `hidden=True` 的模块不出现在清单中。平台不支持的模块以删除线标注。
- 给出模块名时，展示这个模块的简介和命令模板。
- 超级用户命令对非超级用户隐藏，管理员命令对普通成员隐藏。

<ChatExample
  :log="[
    '用户：~help bind',
    '机器人：管理用户组、场景组与消息通道，同一组内的用户或群聊共享同一份数据。',
    '`~bind self remove <user>` - 将指定用户移出当前用户组。',
    '`~bind token <code>` - 填入另一处生成的绑定码以完成绑定。',
  ]"
/>


## 输出样式

### Markdown 表格（QQBot）

平台支持 Markdown 扩展时，模块清单排成一张表，QQBot 使用这种样式。点击模块名会填入对应的 `help` 命令。

<ChatExample
  :messages="[
    { role: 'user', text: '~help' },
    {
      role: 'bot',
      markdown: true,
      text: '| AkariBot | 简体中文 | 版本：v0.1.1 | 权限：管理员 |\n| --- | --- | --- | --- |\n| 基础模块 | | | |\n| 🔓 help | 🔓 module | 🔓 admin | 🔓 bind |\n| 扩展模块 | 🔓 = 已开启 | 🔐 = 已关闭 | |\n| 🔓 wiki | 🔓 maimai | 🔓 ncmusic | 🔓 rss |\n| 订阅扩展模块 | 🔔 = 已开启 | 🔕 = 已关闭 | |\n| 🔔 rss | 🔔 bilibili | 🔔 minecraft_news | |\n\n向右滑动以查看所有模块，点击可自动填入对应帮助命令。',
    },
  ]"
/>

示例中的表格是静态的。实际消息里，语言、版本和模块名是可点击的动作文本，点击后填入对应的命令。

### 图片模块列表

当 Markdown 表格不可用、平台支持图片且未强制文本模式时，模块清单渲染为一张图片。模块按基础、扩展、订阅分组，未启用的模块单独着色。

<ChatExample
  :image-width="720"
  :messages="[
    { role: 'user', text: '~help' },
    { role: 'bot', text: '![模块列表（示例数据）](help-modules.png)' },
  ]"
/>

### 文本模式

Markdown 表格不可用、图片渲染失败或指定 `--legacy` 时，模块清单按分组输出为纯文本，模块之间用 `|` 分隔。

<ChatExample
  :log="[
    '用户：~help --legacy',
    '机器人：基础模块：',
    '🔓 help | 🔓 module | 🔓 admin | 🔓 bind',
    '扩展模块：',
    '🔓 wiki | 🔓 maimai | 🔓 ncmusic | 🔓 rss',
    '使用“~help <模块名称>”查看详细信息。',
  ]"
/>

`--img` 优先渲染图片，渲染不可用时改用文本。`--legacy` 强制文本模式。

模块顺序和启用状态取自场景的 `modules` 列，基础模块始终显示为已启用。未启用的模块可以通过清单按钮或 `module enable <module>` 启用。

模块的帮助文案来自命令模板末尾的 `I18N:key`，简介来自 `module(desc=...)`。
