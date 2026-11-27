# WebRender

本文介绍 WebRender 的配置、运行模式与降级行为。

WebRender 将 HTML、网页或页面元素渲染为图片，用于帮助菜单、Wiki Infobox、图片表格与其他截图功能。

`core` 通过 `akari-bot-webrender` 客户端调用本地 Playwright 浏览器，或将请求转发至远程渲染服务。渲染不可用时，相关命令以其他形式输出，例如帮助菜单展示为文字或表格形式。

## 配置

配置文件为 `config/webrender.toml`，表名 `[webrender]`。字段在 `akaribot/core/config/webrender.py` 中声明：

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | `bool` | `false` | 是否开启 WebRender |
| `browser_type` | `str` | `"chrome"` | 浏览器类型，支持 `chrome` 与 `firefox` |
| `browser_executable_path` | `str` | `""` | 浏览器可执行文件路径。为空时使用 Playwright 安装的浏览器 |
| `headless` | `bool` | `true` | 是否以无界面模式（headless）运行浏览器 |
| `remote_only` | `bool` | `false` | 是否仅使用远程服务，跳过本地浏览器 |
| `remote_web_render_url` | `str` | `""` | 远程服务地址。本地渲染失败时作为备用，`remote_only` 模式下必须配置 |

```sh
akaribot config schema --table webrender
akaribot config set enable true --table webrender
akaribot config set browser_type firefox --table webrender
```

修改配置后需要重启实例才能生效。`~webrender reload` 仅重启浏览器实例。

## 运行模式

| 配置 | 行为 |
| --- | --- |
| `enable=false` | 不初始化浏览器，状态检查返回不可用 |
| `enable=true`、`remote_only=false`、URL 为空 | 使用本地 Playwright 浏览器 |
| `enable=true`、`remote_only=false`、URL 非空 | 优先本地。浏览器未初始化或渲染失败时转发至远程 |
| `enable=true`、`remote_only=true`、URL 非空 | 不启动本地浏览器，所有请求（包含状态查询）均发送至远程服务 |
| `enable=true`、`remote_only=true`、URL 为空 | 远程未配置，渲染不可用 |

远程服务地址必须为 HTTP 或 HTTPS URL，不得携带查询参数或锚点片段标识。

远程服务由独立的 [`akari-bot-webrender`](https://github.com/Teahouse-Studios/akari-bot-webrender) 项目提供。浏览器与运行依赖的安装方法参见该项目文档。机器人端仅需要配置服务地址，并按需开启 `remote_only`。

## 启动与状态

Server 启动时在后台任务中调用 `init_web_render()`，随后将 `check_web_render_status()` 的检查结果写入 `Bot.Info.web_render_status`。初始化失败时仅记录日志，并将状态标记为不可用。

`close_web_render()` 在进程退出时关闭本地浏览器。`remote_only` 模式仅使用远程服务。

`webrender` 是基础模块，命令要求超级用户：

| 命令 | 说明 |
| --- | --- |
| `~webrender status` | 输出渲染服务状态 |
| `~webrender start` | 按当前配置执行初始化。开启 `remote_only` 时仅检查远程服务状态 |
| `~webrender stop` | 关闭本地浏览器。开启 `remote_only` 时仅更新状态标志 |
| `~webrender reload` | 先关闭再重新初始化 |

命令清单与权限参见[内置工具](../../modules/core/docs/webrender.md)。

## 降级

`await check_web_render_status()` 返回 `False` 时，调用方无需请求截图。帮助菜单在生成图片前检查 `Bot.Info.web_render_status`，状态不可用时展示为文字或表格形式。

其他模块通常预先检查该状态。未预先检查的模块在调用失败后转为纯文本形式。异常由渲染服务内部捕获处理，本地与远程均执行失败时返回 `None`。

<NoticeBox type="info" title="远程回退">

配置 `remote_web_render_url` 后，本地渲染失败时将自动改用远程服务。本地浏览器未初始化、渲染结果为空及发生异常均判定为失败。远程服务也执行失败时，客户端返回空结果。设置 `remote_only=true` 时仅使用远程服务，此时远程地址必须有效且可达。

</NoticeBox>

## 程序接口

模块通过公开 API 使用渲染能力：

```python
from akaribot.core.api import (
    ElementScreenshotOptions,
    check_web_render_status,
    web_render,
)

if await check_web_render_status():
    images = await web_render.element_screenshot(
        ElementScreenshotOptions(content=html, element=[".card"])
    )
```

`web_render` 还提供以下方法：

- 页面截图
- 区域截图
- 页面源码
- 原始请求

上述方法的参数分别由 `PageScreenshotOptions`、`SectionScreenshotOptions`、`SourceOptions` 与 `RawOptions` 描述。`init_web_render()`、`close_web_render()` 及相关选项类均从 `akaribot.core.api` 导出，完整清单参见[公开 API](public-api.md)。
