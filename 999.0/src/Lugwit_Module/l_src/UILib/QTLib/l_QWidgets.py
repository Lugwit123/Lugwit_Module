# -*- coding: utf8
from email.charset import QP
import sys,time,os
import functools
if __name__ == '__main__':
    import l_pyqt
else:
    from. import l_pyqt

if not os.environ.get('QT_API'):
    os.environ['QT_API'] = 'PyQt6'


from qtpy.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QMainWindow, QComboBox,QWidget,QMenuBar)
from qtpy.QtCore import Qt, QTimer, QEvent, QCoreApplication, QRect,QPoint,Signal,QThread
from pywinauto import Application
from qtpy.QtCore import Qt, QMimeData, QEvent, QPoint,QObject,QSize
from qtpy.QtGui import QDragEnterEvent, QDropEvent,QAction,QPainter, QColor


def get_global_position(event):
    # 对于 PySide6 6.0 及以上版本，使用 globalPosition()
    return event.globalPosition().toPoint()

    


class L_TitleBar(QWidget):
    def __init__(self, parent=None, title="我的应用"):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 0, 0)  # 移除边距
        self.parent = parent
        #parent.setWindowFlags(Qt.FramelessWindowHint)
        self.MiddleAreaWgt = QWidget()
        self.MiddleAreaLayout = QHBoxLayout()
        self.MiddleAreaWgt.setLayout(self.MiddleAreaLayout)
        # 标题
        self.title = title
        self.titleWgt = QLabel(title)


        # 按钮
        self.minimizeButton = QPushButton("-")
        self.maximizeButton = QPushButton("□")
        self.closeButton = QPushButton("×")

        # 设置按钮样式和大小
        buttonSize = QSize(60, 40)  # 按钮大小
        self.minimizeButton.setFixedSize(buttonSize)
        self.maximizeButton.setFixedSize(buttonSize)
        self.closeButton.setFixedSize(buttonSize)
        self.setFixedHeight(40)

        # 设置按钮样式，包括悬停和按下的样式
        buttonStyle = """
        QPushButton {
            border-top: none;
            border-left: none;
            border-right: none;
            border-radius: none;
        }

        QPushButton:hover {
            background-color: #a6a6a6;  /* 悬停时的颜色 */
        }
        QPushButton:pressed {
            background-color: #a6a6a6;  /* 按下时的颜色 */
        }
        """
        
        closeButtonStyle = """
        QPushButton {
            border-top: none;
            border-left: none;
            border-right: none;
            border-radius: none;
        }
        QPushButton:hover {
            background-color: #ff5555;  /* 悬停时变为红色 */
        }
        QPushButton:pressed {
            color: #ff7777;  /* 按下时的颜色 */
        }
        """

        self.minimizeButton.setStyleSheet(buttonStyle)
        self.maximizeButton.setStyleSheet(buttonStyle)
        self.closeButton.setStyleSheet(closeButtonStyle)

        # 添加组件到布局
        self.layout.addWidget(self.titleWgt)
        self.layout.addWidget(self.MiddleAreaWgt, 10)
        self.layout.addWidget(self.minimizeButton)
        self.layout.addWidget(self.maximizeButton)
        self.layout.addWidget(self.closeButton)
        self.layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        self.layout.setSpacing(0)  # 设置按钮之间的间隙为0

        self.setLayout(self.layout)

        # 连接按钮信号
        self.minimizeButton.clicked.connect(parent.showMinimized)
        self.maximizeButton.clicked.connect(self.toggleMaximizeRestore)
        self.closeButton.clicked.connect(parent.close)

        # 设置背景色和圆角边框
        # 设置标题栏自身的样式


    def setWindowsTitle(self, title) -> None:
        self.title = title
        self.titleWgt.setText(title)

    def toggleMaximizeRestore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximizeButton.setText("□")
        else:
            self.parent.showMaximized()
            self.maximizeButton.setText("❐")

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            #self.dragPos = event.globalPosition()
            self.dragPos = get_global_position(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = self.parent.pos() + ( get_global_position(event) - self.dragPos)
            self.parent.move(new_pos)
            self.dragPos = get_global_position(event)
            event.accept()

    def setTitleBarWidget(self, index=0,widget_ins=None,stretch=1):
        self.layout.insertWidget(index, widget_ins,stretch)  # 索引 0 表示布局的最前面
        widget_ins.setFixedHeight(self.height())




def create_frameless_window(base_class:QWidget)->QWidget:
    class FramelessWindow(base_class ):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.setMouseTracking(True)
            self.resizeRegion = None
            self.isdrag=False

        @l_pyqt.add_position_method
        def mousePressEvent(self, event):
            self.clickPosition = get_global_position(event)
            position=event.position()
            self.resizeRegion = self.detectResizeRegion(position)

        @l_pyqt.add_position_method
        def mouseMoveEvent(self, event):
            super().mouseMoveEvent(event)
            if event.buttons() == Qt.MouseButton.LeftButton and self.resizeRegion :
                self.handleResize( event.globalPos())
            self.setCursorShape(event.position())

        def mouseReleaseEvent(self, event):
            super().mouseReleaseEvent(event)
            self.isdrag=False

        def detectResizeRegion(self, pos):
            rect = self.rect()
            margins = 10  # 边缘感应区域的宽度
            if pos.y() < margins:
                if pos.x() < margins: return 'TopLeft'
                elif pos.x() > rect.width() - margins: return 'TopRight'
                else: return 'Top'
            elif pos.y() > rect.height() - margins:
                if pos.x() < margins: return 'BottomLeft'
                elif pos.x() > rect.width() - margins: return 'BottomRight'
                else: return 'Bottom'
            elif pos.x() < margins: return 'Left'
            elif pos.x() > rect.width() - margins: return 'Right'

            return None

        def setCursorShape(self, pos):
            region = self.detectResizeRegion(pos)
            #print ('fn - setCursorShape',region)
            if region in ['TopLeft', 'BottomRight']: 
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif region in ['TopRight', 'BottomLeft']: 
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            elif region in ['Top', 'Bottom']: 
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            elif region in ['Left', 'Right']: 
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

        def handleResize(self, pos):
            rect = self.geometry()
            height=rect.height()
            if self.isdrag == False:
                self.isdrag = True
                self.init_rect=rect
            print (self.init_rect,pos.y(),rect.bottom())
            if 'Left' in self.resizeRegion:
                rect.setLeft(pos.x())
            if 'Right' in self.resizeRegion:
                rect.setRight(pos.x())
            if 'Top' in self.resizeRegion:
                rect.setTop(pos.y())
                rect.setBottom(self.init_rect.bottom())
            if 'Bottom' in self.resizeRegion:
                rect.setBottom(pos.y())
            self.setGeometry(rect)


    return FramelessWindow  # 返回创建的类


class LMainWindow(create_frameless_window(QMainWindow)):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义标题栏")
        QCenterWidget = QWidget()
        self.setCentralWidget(QCenterWidget)
        self.lay=QVBoxLayout()
        self.lay.setContentsMargins(10,10,10,20)
        QCenterWidget.setLayout(self.lay)
        self.setGeometry(100, 100, 600, 400)
        self.titleBar=L_TitleBar(self,title='设置工具环境变量')
        self.lay.addWidget(self.titleBar)
        self.lay.addWidget(QPushButton('按钮1'))
        self.lay.addStretch()



class LWidget(create_frameless_window(QWidget)):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义标题栏")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.lay=QVBoxLayout()
        self.lay.setContentsMargins(4,4,4,10)
        self.setLayout(self.lay)
        self.titleBar = L_TitleBar(self,title='设置工具环境变量')
        self.lay.addWidget(self.titleBar)

        self.setMenuWidget()
        self.centerLay=QHBoxLayout()
        self.lay.addLayout(self.centerLay,100)

        self.bottomLay=QHBoxLayout()
        self.lay.addLayout(self.bottomLay)

        self.setLayout(self.lay)


    def setMenuWidget(self):
        # 创建菜单栏
        self.menuLay=QHBoxLayout()
        self.menuLay.setContentsMargins(0,0,0,0)
        self.menuWidget = QWidget()
        self.menuWidget.setLayout(self.menuLay)
        menubar = QMenuBar()

        # 创建文件菜单
        file_menu = menubar.addMenu("File")

        # 创建动作
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        # 将动作添加到文件菜单
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)
        self.menuLay.setMenuBar(menubar)
        self.lay.addWidget(self.menuWidget)

    def setTitleBarWidget(self, index=0,widget_ins=None,stretch=1):
        self.titleBar.setTitleBarWidget(index,widget_ins,stretch)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def setCenterWidget(self, index=0,widget_ins=None,stretch=0):
        self.clearLayout(self.centerLay)  # 先清空原有布局
        self.centerLay.addWidget(widget_ins)

    def setbottomWidget(self, index=0,widget_ins=None,stretch=0):
        self.clearLayout(self.bottomLay)  # 先清空原有布局
        self.bottomLay.addWidget(widget_ins)

    def setTitleBarTitle(self, title="我的应用"):
        self.titleBar.setWindowTitle(title)



if __name__ == "__main__":
    print(111)
    app = QApplication(sys.argv)
    mainWindow = LWidget()
    mainWindow.setTitleBarTitle("测试标题栏")
    com=QComboBox()
    mainWindow.setMinimumHeight(500)
    com.addItem('1')
    com.addItem('2')
    com.setFixedWidth(100)
    mainWindow.setTitleBarWidget(index=0,widget_ins=com,stretch=1,)
    mainWindow.setCenterWidget(widget_ins=QPushButton('按钮2'))
    mainWindow.setbottomWidget(widget_ins=QPushButton('按钮3'))
    mainWindow.lay.addStretch()
    mainWindow.show()
    sys.exit(app.exec_())
