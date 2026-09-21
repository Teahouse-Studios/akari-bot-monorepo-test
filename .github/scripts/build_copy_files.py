"""组装二进制分发的源码目录。

源路径已改为 monorepo 布局（``packages/adapters``、``packages/modules`` 与 core 包内 ``locales``）；
输出仍沿用旧根目录结构；产物形态归 tasks T6.5，本脚本届时下线，假设清单见 generated_docs/build_assumptions.md。

``data/`` 与 ``config/`` 是实例可写数据，包的可写数据另在实例目录的 ``data/<种类>/<名称>/``
下，都不参与分发；此处仅保证输出目录存在，配置由首次启动写出骨架后补全。
"""

import shutil
from pathlib import Path

if __name__ == "__main__":
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    shutil.copytree("assets", output_dir / "assets")
    (output_dir / "data").mkdir(exist_ok=True)
    shutil.copytree("packages/adapters", output_dir / "bots")
    shutil.copytree("packages/akari-bot-core/src/akaribot/core/locales", output_dir / "core" / "locales")
    # 整个 packages/modules 一并复制：除模块源码外还有各包的 pyproject.toml 与 assets/。
    # 可写数据已不在包目录内（见模块顶部说明），故此处无需再区分运行时产物。
    shutil.copytree("packages/modules", output_dir / "modules")

    build_paths = [Path("wrapper-build")]
    for build_path in build_paths:
        if build_path.exists():
            for file in build_path.iterdir():
                if file.suffix in [".exe", ".bin", ".app"]:
                    shutil.copyfile(file, output_dir / file.name)

    (output_dir / "database").mkdir(exist_ok=True)
