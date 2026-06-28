# -*- coding: utf-8
from __future__ import absolute_import
import sys
import os


def _prepend_pytracemp_dev_src():
    """Maya 须优先 rez-package-source/pytracemp/999.0，勿用 rez-core-build-cache 0.1.0。"""
    roots = []
    env_src = os.environ.get("PYTRACEMP_DEV_SRC")
    if env_src:
        roots.append(env_src)
    trayapp = os.environ.get("LUGWIT_TRAYAPP_ROOT") or (
        r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp"
    )
    roots.append(
        os.path.join(trayapp, "rez-package-source", "pytracemp", "999.0", "src")
    )
    rez_pp = os.environ.get("REZ_PACKAGES_PATH") or ""
    for part in rez_pp.split(os.pathsep):
        if part.strip():
            roots.append(os.path.join(part.strip(), "pytracemp", "999.0", "src"))
    seen = set()
    for root in roots:
        root = os.path.normpath(root)
        key = os.path.normcase(root)
        if key in seen:
            continue
        seen.add(key)
        marker = os.path.join(
            root, "pytracemp", "usualFunc_helper", "forward_tracer.py"
        )
        if os.path.isfile(marker) and root not in sys.path:
            sys.path.insert(0, root)
            os.environ.setdefault("PYTRACEMP_DEV_SRC", root)
            return root
    legacy = os.path.join(trayapp, "Lib", "pytracemp", "src")
    if os.path.isdir(legacy) and legacy not in sys.path:
        sys.path.append(legacy)
    return None


_prepend_pytracemp_dev_src()
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
