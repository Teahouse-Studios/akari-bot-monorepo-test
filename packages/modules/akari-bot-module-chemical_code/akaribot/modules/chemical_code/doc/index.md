# 化学式猜谜

从 PubChem 随机取一个化合物，绘制结构图让玩家回答分子式。答错时按元素组成给出提示，答对按模式
发放花瓣。

模块名 `chemical-code`，别名 `chemical_code`、`cc`、`ccode`、`chemicalcode`；`cca`、`chemical_captcha`、
`chemicalcaptcha`、`ccaptcha` 映射到 `chemical-code captcha`。

## 安装

```bash
akaribot module add akari-bot-module-chemical_code
```

安装后在会话中由管理员用 `module enable chemical-code` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `chemical-code` | 经典模式：随机出题，答对获得 1 花瓣 | 所有用户 |
| `chemical-code captcha` | 验证码模式：只接受一次作答，答对获得 2 花瓣 | 所有用户 |
| `chemical-code <pcid>` | 按 PubChem CID 出题，`0` 表示随机，不发花瓣 | 所有用户 |
| `chemical-code stop` | 结束当前对局并公布答案 | 所有用户 |

题目附带 PubChem CID。答案按分子式比对，大小写与顺序敏感；发送的内容为字母与数字组合时会被解析
为分子式并给出提示：元素总数偏差过大、缺少元素、元素数量不符三类提示分别触发。

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
