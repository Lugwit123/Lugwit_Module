# 导入所需的模块
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt




class ComboBoxHelper:
    def __init__(self, combo_box: QComboBox):
        setattr(combo_box,"helper",self)
        self.combo_box = combo_box
        self.combo_box.currentIndexChanged.connect(self.update_tooltip)

    def set_item_tooltips(self, tooltips: list):
        """
        设置 QComboBox 每个项目的提示信息

        参数:
        tooltips (list): 包含提示信息的列表，每个元素对应 QComboBox 中的一个项目
        """
        self.tooltips = tooltips
        for index in range(self.combo_box.count()):
            self.combo_box.setItemData(index, tooltips[index], role=Qt.ItemDataRole.ToolTipRole)
        self.update_tooltip(self.combo_box.currentIndex())

    def update_tooltip(self, index):
        """
        当 QComboBox 的当前项目改变时更新工具提示

        参数:
        index (int): 当前项目的索引
        """
        tooltip = self.tooltips[index]
        self.combo_box.setToolTip(tooltip)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QComboBox 示例")

        # 创建 QComboBox 并添加项目
        self.combo_box = QComboBox()
        self.combo_box.addItems(["项目1", "项目2", "项目3"])

        # 创建 ComboBoxHelper 实例并设置提示信息
        self.helper = ComboBoxHelper(self.combo_box)
        self.helper.set_item_tooltips(["这是项目1", "这是项目2", "这是项目3"])
        # 如何helper前面不加self,就不行,怎么办

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
