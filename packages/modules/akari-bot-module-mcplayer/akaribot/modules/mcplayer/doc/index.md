# mcplayer

通过玩家名或 UUID 查询 Minecraft：Java 版玩家，返回名称、UUID、NameMC 链接与皮肤、渲染图、披风图片。

## 命令

<ModuleAlias names="namemc" />

### `mcplayer`

<CommandUsage usage="mcplayer <username_or_uuid>" :params="['username_or_uuid=玩家名或 UUID']" permission="public" />

- 按玩家名或 UUID 查询玩家信息。
- 参数长度为 32 时，按无连字符 UUID 处理。
- 参数长度为 36 且含 4 个连字符时，按带连字符 UUID 处理，去掉连字符后查询。
- 其余输入按玩家名解析为 UUID。
- 玩家不存在或名称无法解析时返回未找到提示。

结果附带渲染图与皮肤，渲染图为全身像，皮肤为原始皮肤文件；存在披风时一并附带披风图。图片获取失败时降级为名称、UUID 与 NameMC 链接。

<ChatExample
  :log="[
    '用户：~mcplayer Notch',
    '机器人：Notch (069a79f444e94726a5befca90e38aaf5)',
    'https://namemc.com/profile/Notch',
    '![渲染图](mcplayer-render.png){natural}',
    '![皮肤](mcplayer-skin.png){natural}',
  ]"
/>
