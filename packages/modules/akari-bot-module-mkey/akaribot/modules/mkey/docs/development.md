---
title: 安装与开发
---

# mkey：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-mkey
```

安装后，管理员需要在会话中执行 `module enable mkey` 开启模块。

## 配置项

<ModuleConfig />

## 权限与平台能力

此模块的命令对普通用户开放，不要求管理员或超级用户权限。模块没有声明平台限制，`available_for` 取默认值 `*`。密码计算全部在本地完成，不访问网络，也不依赖平台能力。

## 数据表

<ModuleData />

## 依赖与外部服务

此模块依赖 `akari-bot-core` 与 `pycryptodome>=3.18.0,<5.0.0`。模块不访问外部服务。密钥数据位于包内的 `assets/data` 目录，`manifest.toml` 声明 `assets = "assets"`。

`device` 的取值会映射到内部型号代号：`3ds` 为 CTR、`dsi` 为 TWL、`wii` 为 RVL、`wiiu` 为 WUP、`switch` 为 HAC。8 位确认代码按 CRC 算法计算，10 位与 6 位确认代码按 HMAC 算法计算。
