# MC 百科查询

检索 MC 百科（mcmod.cn）的 Mod 条目，返回搜索结果第一条的名称、链接与简介。模块名 `mcmod`，别名
`moddetails`，后者等价于 `mcmod details`。

## 安装

```bash
akaribot module add akari-bot-module-mcmod
```

安装后在会话中由管理员用 `module enable mcmod` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `mcmod <mod_name>` | 按 Mod 名称搜索，可使用无歧义缩写或准确名称 | 所有用户 |
| `mcmod details <content>` | 按内容搜索，可使用物品、方块或实体的 ID 或准确名称 | 所有用户 |

两条命令都只取搜索结果的第一条，输出名称、链接与简介；页面为空或没有匹配条目时返回未找到结果。
名称搜索使用 `https://search.mcmod.cn/s?key=`，内容搜索在此基础上附加 `filter=3` 参数。

## 配置项

无。本包没有 `config.py`，`manifest.toml` 未声明 `config_table`。

## 权限与平台能力

- 两条命令均未声明管理员或超级用户限制，普通用户可执行。
- 模块未声明平台限制，`available_for` 取默认值 `*`。
- 模块声明 `support_languages=["zh_cn"]`，在非简体中文会话中启用时框架会提示语言不受支持。
- 搜索结果页由 WebRender 读取，运行前需在 core 配置中开启 `webrender.enable`。

## 数据表

无。manifest 未声明 `owned_tables`，查询结果不落库。

## 依赖与外部服务

- 运行依赖：`akari-bot-core`、`beautifulsoup4>=4.11.1,<5.0.0`。
- 外部服务：`search.mcmod.cn` 的搜索页，经 WebRender 抓取后用 BeautifulSoup 解析。
