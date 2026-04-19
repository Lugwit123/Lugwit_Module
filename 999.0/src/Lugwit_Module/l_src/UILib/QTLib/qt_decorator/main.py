from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def centerWindow(win_ins,posOffset):
    # 获取屏幕尺寸
    screen = QDesktopWidget().screenGeometry()
    # 获取窗口尺寸
    window = win_ins.geometry()
    # 计算窗口居中的位置
    win_ins.move((screen.width() - window.width()) // 2 +posOffset[0],
                (screen.height() - window.height()) // 2 +posOffset[1])
        
def showEvent(win_ins, event,posOffset=(0,0)):
    if event.type() == QEvent.Show:
        centerWindow(win_ins,posOffset)