---
title: 安装与开发
---

# mod-dl：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mod_dl
```

安装后，管理员需要在会话中执行 `module enable mod-dl` 开启模块。此模块建议与 `mcmod` 模块搭配使用。

## 配置项

<ModuleConfig table="module_mod_dl" />

此表只有一个字段。该字段声明为敏感项，值实际写入同一配置文件里的 `module_mod_dl_secret` 表。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `curseforge_api_key` | str | 空 | CurseForge API 密钥 |

未填写密钥时，CurseForge 请求改走 `https://mcim.z0z0r4.top` 镜像。填写密钥后，请求直连官方接口并携带 `x-api-key`。`manifest.toml` 把该字段列进 `credential_fields`，启动时据此检查凭据是否重复。

## 权限与平台能力

此模块的命令对普通用户开放，不要求管理员或超级用户权限。模块没有声明平台限制，所有已接入平台都可以使用。搜索与版本选择依赖会话内的连续回复。

## 数据表

<ModuleData />

## 依赖与外部服务

此模块依赖 `akari-bot-core`。搜索与文件信息来自 `https://api.modrinth.com/v2` 与 `https://api.curseforge.com/v1`，未配置密钥时使用 `https://mcim.z0z0r4.top` 镜像。

两个站点每次搜索至多返回 10 条结果。未指定版本时，Modrinth 的候选版本取自项目的版本列表，CurseForge 的候选版本取自 `latestFilesIndexes` 中的游戏版本。`mcmod` 只是搭配建议，不构成依赖。
