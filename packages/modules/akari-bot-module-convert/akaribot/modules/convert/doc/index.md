# 单位转换

用 pint 单位库做物理量换算，支持长度、质量、面积、体积、速度、温度等 pint 内置量纲，
输出原始量与换算结果。

模块名 `convert`，别名 `conv`、`unit`；声明支持语言 `en_us`。

## 安装

```bash
akaribot module add akari-bot-module-convert
```

安装后在会话中由管理员用 `module enable convert` 开启。

## 命令

下表省略命令前缀，前缀由实例配置决定。

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `convert <from_val> <to_unit>` | 将带单位的数值转换为目标单位 | 所有用户 |

`<from_val>` 由数值与单位连写，`<to_unit>` 只写单位，例如 `convert 100km m`。表达式与单位名称
均交给 pint 解析，大小写敏感：`km` 与 `KM` 含义不同。无法解析的表达式、量纲不匹配或单位无法
识别时统一返回转换失败提示。

## 配置

本包未声明模块配置，manifest 中没有 `config_table`。

## 权限与平台能力

- 无平台限制，无权限要求，不涉及网络请求。
- `UnitRegistry` 使用 `Decimal` 作为数值类型，避免二进制浮点误差。
- 声明支持语言 `en_us`：启用模块时若会话语言不在该列表中，会附加不受支持语言的提示。

## 数据表

manifest 未声明 `owned_tables`，模块不保存任何数据。

## 依赖与外部服务

仅依赖 `pint` 与 `akari-bot-core`，不使用外部服务。
