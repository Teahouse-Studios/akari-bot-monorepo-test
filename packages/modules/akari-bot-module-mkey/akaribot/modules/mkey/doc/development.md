---
title: 安装与开发
---

# mkey：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mkey
```

安装后在会话中由管理员用 `module enable mkey` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

命令未声明管理员或超级用户限制，普通用户可执行。模块未声明平台限制，`available_for` 取默认值 `*`。计算完全在本地完成，不依赖网络或平台能力。

## 数据表

<ModuleData />

## 依赖与外部服务

运行依赖 `akari-bot-core` 与 `pycryptodome>=3.18.0,<5.0.0`。模块不访问外部服务；密钥数据位于包内 `assets/data`，manifest 声明 `assets = "assets"`。`device` 取值映射到内部型号代号：`3ds` 为 CTR、`dsi` 为 TWL、`wii` 为 RVL、`wiiu` 为 WUP、`switch` 为 HAC。8 位确认代码按 CRC 算法计算，10 位与 6 位确认代码按 HMAC 算法计算。
