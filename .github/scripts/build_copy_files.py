"""组装二进制分发的源码目录。

本脚本按仓库根布局硬编码路径，只在「源码树与可执行文件一并分发」这一形态下成立。
拆包后根目录不再有 ``core/`` ``modules/`` ``bots/`` ``assets/``，届时按 tasks T6.5
改为按包安装，本脚本随之下线。逐条布局假设见 generated_docs/build_assumptions.md。

``data/``、``config/`` 与 ``modules/*/data/`` 是实例可写数据，不参与分发；此处仅保证输出
目录存在，配置由首次启动写出骨架后补全。
"""

import shutil
from pathlib import Path

if __name__ == "__main__":
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    shutil.copytree("assets", output_dir / "assets")
    (output_dir / "data").mkdir(exist_ok=True)
    shutil.copytree("bots", output_dir / "bots")
    shutil.copytree("core/locales", output_dir / "core" / "locales")
    # modules/*/data/ 一并复制：其中既有运行时产物，也有随仓库分发的默认文件
    # （如 modules/ai/data/instructions.txt）。剔除运行时产物需要先区分两者，
    # 属分发形态重构的范围。
    shutil.copytree("modules", output_dir / "modules")

    build_paths = [Path("wrapper-build")]
    for build_path in build_paths:
        if build_path.exists():
            for file in build_path.iterdir():
                if file.suffix in [".exe", ".bin", ".app"]:
                    shutil.copyfile(file, output_dir / file.name)

    (output_dir / "database").mkdir(exist_ok=True)
