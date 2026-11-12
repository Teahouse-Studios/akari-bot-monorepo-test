---
title: 安装与开发
---

# chemical-code：安装与开发

## 安装

```bash
akaribot module add akari-bot-module-chemical_code
```

安装后在会话中由管理员用 `module enable chemical-code` 开启。

## 配置项

<ModuleConfig />

## 权限与平台能力

出题区间为 1 至 200000000，每次由随机数取 CID，再请求 PubChem 的 SMILES 属性。结构图由 rdkit 绘制，颜色表随代码分发；图片写入临时缓存目录后作为图片消息发送。对局状态保存在 `PlayState`（键 `chemical_code`），按会话隔离。

## 数据表

<ModuleData />

## 依赖与外部服务

依赖 `rdkit`（结构解析与绘制）、`Pillow`、`tenacity`（请求重试）、`akari-bot-core`。外部服务 PubChem PUG REST（`pubchem.ncbi.nlm.nih.gov/rest/pug`）。`rdkit` 与 `Pillow` 在首次出题时导入，未使用该模块时不加载。
