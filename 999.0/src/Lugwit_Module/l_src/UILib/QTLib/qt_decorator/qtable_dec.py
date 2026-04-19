from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

def update_cell_widget_positions_dec(cls):
    class CustomHeaderView(QHeaderView):
        def mouseMoveEvent(self, event):
            super().mouseMoveEvent(event)
            self.parent().update_cell_widget_positions()

    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setHorizontalHeader(CustomHeaderView(Qt.Horizontal, self))
            update_cell_widget_positions_dec


        def resizeEvent(self, event):
            super().resizeEvent(event)
            self.update_cell_widget_positions()

        def update_cell_widget_positions(self):
            for col in range(self.columnCount()):
                for row in range(self.rowCount()):
                    cell_widget = self.cellWidget(row, col)
                    if cell_widget:
                        cell_widget.setGeometry(self.columnViewportPosition(col), 
                                                self.rowViewportPosition(row), 
                                                self.columnWidth(col)-1, 
                                                self.rowHeight(row)-1)
    return Wrapped



@update_cell_widget_positions_dec
class MyTableWidget(QTableWidget):
    pass

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout()

        self.tableWidget = MyTableWidget(self)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Item (1,1)"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Item (1,2)"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Item (2,1)"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Item (2,2)"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Item (3,1)"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Item (3,2)"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Item (4,1)"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Item (4,2)"))

        layout.addWidget(self.tableWidget)

        centralWidget.setLayout(layout)

        self.setWindowTitle('Custom Table Widget with Decorator')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    


