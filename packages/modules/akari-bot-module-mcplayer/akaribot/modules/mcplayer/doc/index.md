# Minecraft 玩家查询

通过玩家名或 UUID 查询 Minecraft：Java 版玩家，返回名称、UUID、NameMC 链接与皮肤、渲染图、披风图片。
模块名 `mcplayer`，别名 `namemc`。

## 安装

```bash
akaribot module add akari-bot-module-mcplayer
```

安装后在会话中由管理员用 `module enable mcplayer` 开启。

## 命令

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mcplayer <username_or_uuid>` | 查询玩家信息 | 所有用户 |

参数长度为 32 时按无连字符 UUID 处理；长度为 36 且含 4 个连字符时按带连字符 UUID 处理，去掉连字符
后查询；其余输入按玩家名解析为 UUID。UUID 查询走 Mojang 的 `user/profile` 接口，玩家名查询走
`users/profiles/minecraft` 接口。

皮肤与披风从 Crafatar 获取：渲染图为全身像，皮肤为原始皮肤文件，存在披风时附带披风图。玩家不存在
或名称无法解析时返回未找到提示；Crafatar 请求失败时降级为名称、UUID 与 NameMC 链接。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 命令未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 成功获取皮肤时输出包含图片消息，平台需支持发送图片。

## 数据表

无数据库表。披风图缓存为 core 缓存目录下的 `<uuid>_fixed.png`。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`Pillow>=13.0.0,<13.1.0`、`orjson>=3.10.9,<4.0.0`。
- 外部服务：`api.mojang.com`（玩家名与 UUID 互查）、`crafatar.com`（渲染图、皮肤、披风）。
- 结果中的 NameMC 链接指向 `namemc.com`，仅作为链接输出，不请求该站。
