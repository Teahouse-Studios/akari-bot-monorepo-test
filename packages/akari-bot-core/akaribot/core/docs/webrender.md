# WebRender

本文介绍 WebRender 的配置、运行模式与降级行为。

WebRender 把 HTML、网页或页面元素渲染为图片，供帮助菜单、Wiki infobox、图片表格与其他截图功能使用。

core 通过 `akari-bot-webrender` 客户端调用本地 Playwright 浏览器，或把请求转发到远程渲染服务。渲染不可用时，相关命令改用其他输出方式，例如帮助菜单改用文字或表格。

## 配置

配置文件为 `config/webrender.toml`，表名 `[webrender]`。字段在 `akaribot/core/config/webrender.py` 中声明：

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | `bool` | `false` | 是否开启 WebRender |
| `browser_type` | `str` | `"chrome"` | 浏览器类型，支持 `chrome` 与 `firefox` |
| `browser_executable_path` | `str` | `""` | 浏览器可执行文件路径。为空时使用 Playwright 安装的浏览器 |
| `headless` | `bool` | `true` | 是否以无头模式运行浏览器 |
| `remote_only` | `bool` | `false` | 是否仅使用远程服务，跳过本地浏览器 |
| `remote_web_render_url` | `str` | `""` | 远程服务地址。本地渲染失败时尝试，`remote_only` 时必需 |

```sh
akaribot config schema --table webrender
akaribot config set enable true --table webrender
akaribot config set browser_type firefox --table webrender
```

修改后须重启实例才能生效。`~webrender reload` 只重启浏览器，不重新读取配置文件。

## 运行模式

| 配置 | 行为 |
| --- | --- |
| `enable=false` | 不初始化浏览器，状态检查返回不可用 |
| `enable=true`、`remote_only=false`、URL 为空 | 使用本地 Playwright 浏览器 |
| `enable=true`、`remote_only=false`、URL 非空 | 优先本地。浏览器未初始化或渲染失败时转发到远程 |
| `enable=true`、`remote_only=true`、URL 非空 | 不启动本地浏览器，所有请求（含状态查询）走远程 |
| `enable=true`、`remote_only=true`、URL 为空 | 远程未配置，渲染不可用 |

远程地址必须是 HTTP 或 HTTPS URL，不能带查询参数或片段标识。

远程服务由独立的 [`akari-bot-webrender`](https://github.com/Teahouse-Studios/akari-bot-webrender) 项目提供。浏览器与运行依赖的安装方法见该项目文档。机器人侧只需填写地址，并选择是否启用 `remote_only`。

## 启动与状态

Server 启动时在后台任务中调用 `init_web_render()`，随后把 `check_web_render_status()` 的结果写入 `Bot.Info.web_render_status`。初始化失败时只写日志，并把状态设为不可用。

`close_web_render()` 在进程退出时关闭本地浏览器。`remote_only` 模式只使用远程服务。

`webrender` 是基础模块，命令要求超级用户：

| 命令 | 说明 |
| --- | --- |
| `~webrender status` | 输出渲染服务状态 |
| `~webrender start` | 按当前配置初始化。`remote_only` 时只检查远程服务 |
| `~webrender stop` | 关闭本地浏览器。`remote_only` 时只更新状态 |
| `~webrender reload` | 先关闭再重新初始化 |

命令清单与权限见[内置工具](../../modules/core/docs/tools.md)。

## 降级

`check_web_render_status()` 返回 `false` 时，调用方无需继续请求截图。帮助菜单在生成图片前检查 `Bot.Info.web_render_status`，状态为不可用时改用文字或表格。

其他模块通常先检查状态。没有先检查的模块会在调用失败后改用纯文本。异常由渲染服务内部处理，本地与远程都失败时返回 `None`。

<NoticeBox type="info" title="远程回退">

设置 `remote_web_render_url` 后，本地渲染失败时会改发到远程服务：本地浏览器未初始化、渲染结果为空与一般异常都算失败。远程服务也失败时，客户端返回空结果。`remote_only=true` 时只用远程服务，此时远程地址必须可用。

</NoticeBox>

## 程序接口

模块通过公共 API 使用渲染能力：

```python
from akaribot.core.api import (
    ElementScreenshotOptions,
    check_web_render_status,
    web_render,
)

if check_web_render_status():
    images = await web_render.element_screenshot(
        ElementScreenshotOptions(content=html, element=[".card"])
    )
```

`web_render` 还提供以下方法：

- 页面截图
- 区域截图
- 页面源码
- 原始请求

这些方法的参数分别由 `PageScreenshotOptions`、`SectionScreenshotOptions`、`SourceOptions` 与 `RawOptions` 描述。`init_web_render()`、`close_web_render()` 与相关选项类都从 `akaribot.core.api` 导出，完整清单见[公共 API](public-api.md)。
