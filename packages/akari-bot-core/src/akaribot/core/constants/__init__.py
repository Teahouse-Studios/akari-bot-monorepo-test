# 为避免循环导入而硬编码的常量，供各模块导入；此处不要引入不必要的依赖。

import os

from .default import *
from .exceptions import *
from .info import *
from .path import *
from .version import *

ascii_art = r"""
           _              _   ____        _
     /\   | |            (_) |  _ \      | |
    /  \  | | ____ _ _ __ _  | |_) | ___ | |_
   / /\ \ | |/ / _` | '__| | |  _ < / _ \| __|
  / ____ \|   < (_| | |  | | | |_) | (_) | |_
 /_/    \_\_|\_\__,_|_|  |_| |____/ \___/ \__|
"""
config_filename = "config.toml"
dev_mode = str(os.getenv("DEV_MODE")).lower() == "true"
