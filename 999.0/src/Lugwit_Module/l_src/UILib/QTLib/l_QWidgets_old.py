import sys,time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QPushButton, QLabel, QSpacerItem, QSizePolicy,
                             QVBoxLayout)
from PyQt5.QtCore import Qt, QSize

class L_TitleBar(QWidget):
    def __init__(self, parent=None,title="我的应用"):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout()
        self.parent = parent
        parent.setWindowFlags(Qt.FramelessWindowHint)
        self.MiddleAreaWgt = QWidget()
        self.MiddleAreaLayout = QHBoxLayout()
        self.MiddleAreaWgt.setLayout(self.MiddleAreaLayout)
        # 标题
        self.title=title
        self.titleWgt = QLabel(title)
        self.titleWgt.setStyleSheet("color: white; padding-left: 10px;")

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
            background-color: #333333; 
            color: white; 
            border-top: none;
            border-left: none;
            border-right: none;
            border-radius: none;
        }

        QPushButton:hover {
            background-color: #444444;  /* 悬停时的颜色 */
        }
        QPushButton:pressed {
            background-color: #313131;  /* 按下时的颜色 */
        }
        """
        
        closeButtonStyle = """
        QPushButton {
            background-color: #333333; 
            color: white; 
            border-top: none;
            border-left: none;
            border-right: none;
            border-radius: none;
        }
        QPushButton:hover {
            background-color: #ff5555;  /* 悬停时变为红色 */
        }
        QPushButton:pressed {
            background-color: #ff7777;  /* 按下时的颜色 */
        }
        """

        self.minimizeButton.setStyleSheet(buttonStyle)
        self.maximizeButton.setStyleSheet(buttonStyle)
        self.closeButton.setStyleSheet(closeButtonStyle)

        # 添加组件到布局
        self.layout.addWidget(self.titleWgt)
        self.layout.addWidget(self.MiddleAreaWgt,10)
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
        self.setStyleSheet("""
        QWidget {
            background-color: #333333;
            border-bottom: 2px solid #676767;  /* 标题栏下方的边框 */
        }
        """)

    def setWindowsTitle(self, title) -> None:
        self.title=title
        self.titleWgt.setText(title)
    def toggleMaximizeRestore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximizeButton.setText("□")
        else:
            self.parent.showMaximized()
            self.maximizeButton.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()


    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.parent.isMaximized():
            self.parent.move(self.parent.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


class FramelessWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.resizeRegion = None


    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        self.resizeRegion = self.detectResizeRegion(event.pos())
        
        

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton and self.resizeRegion:
            self.handleResize(event.globalPos())
        self.setCursorShape(event.pos())

        

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
        if region in ['TopLeft', 'BottomRight']: 
            self.setCursor(Qt.SizeFDiagCursor)
        elif region in ['TopRight', 'BottomLeft']: 
            self.setCursor(Qt.SizeBDiagCursor)
        elif region in ['Top', 'Bottom']: 
            self.setCursor(Qt.SizeVerCursor)
        elif region in ['Left', 'Right']: 
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def handleResize(self, pos):
        rect = self.geometry()
        if 'Left' in self.resizeRegion:
            rect.setLeft(pos.x())
        if 'Right' in self.resizeRegion:
            rect.setRight(pos.x())
        if 'Top' in self.resizeRegion:
            rect.setTop(pos.y())
        if 'Bottom' in self.resizeRegion:
            rect.setBottom(pos.y())
        self.setGeometry(rect)


if __name__ == "__main__":
    class MainWindow(FramelessWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("自定义标题栏")
            self.lay=QVBoxLayout()
            self.lay.setContentsMargins(0,0,0,0)
            self.setLayout(self.lay)
            self.setGeometry(100, 100, 600, 400)
            self.titleBar=L_TitleBar(self,title='设置工具环境变量')
        
            self.lay.addWidget(self.titleBar)
            self.lay.addStretch()

            
            self.setStyleSheet("""
            *{
                background-color: #333333;
                border-radius: 10px;
            }
            """)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
