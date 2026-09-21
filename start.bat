chcp 65001
setlocal enabledelayedexpansion
set PYTHONIOENCODING=utf-8
rem 源码树下可导入的包在 packages\*\src 与 packages\*\*\src；已按 workspace 安装时该设置无副作用。
set "PYTHONPATH=%~dp0"
for /d %%d in ("%~dp0packages\*") do (
    if exist "%%d\src" set "PYTHONPATH=!PYTHONPATH!;%%d\src"
    for /d %%e in ("%%d\*") do if exist "%%e\src" set "PYTHONPATH=!PYTHONPATH!;%%e\src"
)

uv run python bot.py
