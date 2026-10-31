---
title: 安装与开发
---

# mod-dl：安装与开发

本页说明 `mod-dl` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-mod_dl
```

安装后在会话中由管理员用 `module enable mod-dl` 开启。模块建议与 `mcmod` 模块搭配使用。

## 配置项

manifest 声明配置表为 `module_mod_dl`；本模块的唯一字段是敏感项，实际写入 `module_mod_dl_secret`（`config/module_mod_dl_secret.toml`）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `curseforge_api_key` | str | 空 | CurseForge API 密钥 |

未填写密钥时，CurseForge 请求改走 `https://mcim.z0z0r4.top` 镜像；填写后直连官方接口并携带 `x-api-key`。`manifest.toml` 将该字段登记为重复凭据检查字段。

## 权限与平台能力

- 命令对普通用户开放，不要求管理员或超级用户权限。
- 未声明平台限制，所有已接入平台可用。
- 搜索与版本选择依赖会话内的连续回复。

## 数据表

无。manifest 未声明 `owned_tables`，搜索结果不落库。

## 依赖与外部服务

- 依赖：`akari-bot-core`。
- 搜索与文件信息：`https://api.modrinth.com/v2`、`https://api.curseforge.com/v1`，未配置密钥时使用 `https://mcim.z0z0r4.top` 镜像。
- 推荐模块：`mcmod`，仅作为搭配建议，不构成依赖。
