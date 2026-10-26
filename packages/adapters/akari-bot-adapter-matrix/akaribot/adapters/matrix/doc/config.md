# Matrix 配置项

配置表为 `bot_matrix`，密钥表为 `bot_matrix_secret`，两张表同处 `config/bot_matrix.toml`：普通项在 `[bot_matrix]`，密钥项在 `[bot_matrix_secret]`。

## 配置表 `bot_matrix`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | bool | `false` | 是否启动 Matrix 客户端。 |
| `matrix_homeserver` | str | `https://matrix.org` | Matrix 机器人的家服务器。 |
| `matrix_user` | str | `@akaribot:matrix.org` | Matrix 机器人的完全限定用户 ID。 |
| `matrix_device_name` | str | `""` | Matrix 机器人的设备名称，可随意填写。 |

## 密钥表 `bot_matrix_secret`

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `matrix_device_id` | str | `""` | Matrix 机器人设备 ID。 |
| `matrix_token` | str | `""` | Matrix 机器人令牌。 |
| `matrix_megolm_backup_passphrase` | str | `""` | Megolm 备份密码短语。 |

## 说明

- `matrix_device_id` 与 `matrix_token` 须属于同一登录会话，否则无法恢复登录。
- `matrix_homeserver` 末尾带斜杠时可能触发 `M_UNRECOGNIZED` 错误。
- `matrix_megolm_backup_passphrase` 为空时不导出密钥备份；长度不超过 10 时启动日志会提示不安全。
- 同步状态与密钥备份保存在 `data/private/matrix/` 下。
