from .main import *
import sys
if sys.version_info[0]==3:
    from . import showMessage_ps as ps_win
    showMessageWin  = ps_win.showMessageWin