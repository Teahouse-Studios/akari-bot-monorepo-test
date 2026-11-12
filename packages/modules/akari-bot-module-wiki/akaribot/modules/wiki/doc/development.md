---
title: 安装与开发
---

# wiki：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-wiki
```

安装后在会话中由管理员分别用 `module enable <模块名>` 开启所需模块。

## 模块

包内注册 12 个模块，覆盖页面查询、内联解析、URL 审核、机器人账号、日志订阅与周报推送。各模块的命令、别名与权限见[使用方法](index.md)。

## 配置项

<ModuleConfig table="module_wiki" />

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `wiki_allowlist_url` | str | 项目 Issue 模板地址 | Wiki API 加入全局 URL 允许列表的申请网址 |

默认值为项目 Issue 模板地址 `https://github.com/Teahouse-Studios/akari-bot/issues/new?template=request_wiki_whitelist.yaml`。设置未列入全局允许列表但未被阻止的 Wiki 时，成功提示后会附带该申请地址；已列入阻止列表的 Wiki 拒绝设置。

## 权限与平台能力

`wiki` 的查询、搜索、随机、魔术字、InterWiki 查看与请求头查看对普通用户开放，`set`、`iw add`、`iw remove`、`headers add`、`headers remove`、`headers reset`、`prefix set`、`prefix reset`、`redlink`、`render` 需要会话管理员权限。`wiki-audit`、`wiki-bot` 与 `wikilog` 需要超级用户权限，`wikilog` 同时声明管理员权限，超级用户可直接使用。`wiki-inline` 通过正则匹配触发，不需要命令前缀。页面截图与部分 Infobox 预览依赖 WebRender，未启用时改用文本或链接。QQ 平台的 `rc` 与 `ab` 在支持消息节点或 WebRender 可用时优先返回合并转发或渲染结果，否则回退到文本。URL 允许列表与阻止列表由 core 的全局规则管理，未通过检查的 Wiki 会被阻止或标记为不信任；`wikilog` 每 60 秒轮询一次已加入监控列表的 Wiki，全局 URL 策略生效时，被监控 Wiki 的地址须在允许列表内。`weekly` 声明支持简体中文与繁体中文，繁体请求使用 `variant=zh-tw`。

## 数据表

<ModuleData tables="module_wiki_target_set_info,module_wiki_site_info,module_wiki_bot_account_list,module_wikilog_target_set_info" :list="false" />

| 表 | 内容 |
| --- | --- |
| `module_wiki_target_set_info` | 场景级默认 Wiki、InterWiki、请求头与前缀 |
| `module_wiki_site_info` | Wiki 站点信息缓存与更新时间 |
| `module_wiki_bot_account_list` | Wiki 机器人账号与密码 |
| `module_wikilog_target_set_info` | 日志监控目标、过滤器、最近更改筛选、备注与保活开关 |

`module_wiki_target_set_info` 与 `module_wikilog_target_set_info` 按场景归属；包内 `migrations/` 提供表结构升级脚本。

## 依赖与外部服务

依赖 `akari-bot-core`、`akari-bot-html2text`、`Pillow`、`aiocqhttp`、`akari-bot-webrender`、`attrs`、`beautifulsoup4`、`feedparser`、`filetype`、`httpx`、`jinja2`、`orjson`、`tortoise-orm` 与 `wikitextparser`。页面查询使用目标 Wiki 的 `api.php`，站点信息缓存在 `module_wiki_site_info`；每周页面来自 `https://zh.minecraft.wiki`，茶馆周报来自 `https://lakeus.xyz/api.php?action=featuredfeed&feed=teahouse-weekly`；截图与 Infobox 预览依赖 WebRender。
