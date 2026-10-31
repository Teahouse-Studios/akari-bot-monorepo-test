# chemical-code

从 PubChem 随机取一个化合物，绘制结构图让玩家回答分子式。答错时按元素组成给出提示，答对按模式
发放花瓣。

模块名 `chemical-code`，别名 `chemical_code`、`cc`、`ccode`、`chemicalcode`；`cca`、`chemical_captcha`、
`chemicalcaptcha`、`ccaptcha` 映射到 `chemical-code captcha`。

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
