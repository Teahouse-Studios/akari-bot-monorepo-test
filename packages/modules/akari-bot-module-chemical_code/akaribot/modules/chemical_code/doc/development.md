---
title: 安装与开发
---

# chemical-code：安装与开发

本页说明 `chemical-code` 模块的安装、配置、权限、数据表与依赖。

## 安装

```bash
akaribot module add akari-bot-module-chemical_code
```

安装后在会话中由管理员用 `module enable chemical-code` 开启。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 出题区间为 1 至 200000000，每次由随机数取 CID，再请求 PubChem 的 SMILES 属性。
- 结构图由 rdkit 绘制，颜色表随代码分发；图片写入临时缓存目录后作为图片消息发送。
- 答题时限为 `max(原子数 // 30, 2)` 分钟；经典模式的等待上限与对局状态一致，均为 1 小时。
- 对局状态保存在 `PlayState`（键 `chemical_code`），按会话隔离，1 小时未活动自动过期。
- 同一会话已有对局时返回进行中提示。

## 数据表

manifest 未声明 `owned_tables`；对局状态为进程内内存，不写入数据库。

## 依赖与外部服务

- 依赖：`rdkit`（结构解析与绘制）、`Pillow`、`tenacity`（请求重试）、`akari-bot-core`。
- 外部服务：PubChem PUG REST（`pubchem.ncbi.nlm.nih.gov/rest/pug`）。
- `rdkit` 与 `Pillow` 在首次出题时导入，未使用该模块时不加载。
