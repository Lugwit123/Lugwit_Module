# -*- coding: utf-8
from __future__ import absolute_import
import sys
import os


sys.path.append(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib\pytracemp\src")
# 优先使用 pytracemp 外部版本（Python 3），失败则回退到本地版本（Python 2）
try:
    from pytracemp.usualFunc import lprint
except ImportError:
    # Python 2 或 pytracemp 不可用时，使用本地版本
    try:
        from . import usualFunc
        lprint = usualFunc.lprint
    except ImportError:
        # 如果本地版本也不存在，使用 pytracemp 的 LPrint 类创建实例
        from pytracemp import LPrint
        lprint = LPrint() 



# insLocation=importlib.import_module(src.insLocation)
import sys
sys_executable=sys.executable


if sys_executable.endswith('maya.exe'):
    from . import l_MayaLib
