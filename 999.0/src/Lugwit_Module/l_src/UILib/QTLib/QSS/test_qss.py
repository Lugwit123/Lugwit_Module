import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QComboBox, QLabel, QLineEdit, QTextEdit, QCheckBox, 
    QRadioButton, QSlider, QProgressBar, QTableWidget, QTableWidgetItem, 
    QTabWidget, QSpinBox, QDateEdit
)
from PyQt5.QtCore import Qt, QFileSystemWatcher, QTimer

class QSSSwitcher(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QSS 测试窗口")
        self.setGeometry(100, 100, 800, 600)

        # 创建文件系统监视器
        self.watcher = QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.reload_qss)

        # 创建标签
        self.label = QLabel("选择一个 QSS 文件来应用样式", self)
        self.label.setAlignment(Qt.AlignCenter)

        # 创建下拉菜单
        self.combo_box = QComboBox(self)
        self.combo_box.currentIndexChanged.connect(self.load_selected_qss)

        # 加载 QSS 文件
        self.load_qss_files()

        # 创建各种 PyQt 组件
        self.line_edit = QLineEdit("这是一个 QLineEdit")
        self.text_edit = QTextEdit("这是一个 QTextEdit")
        self.check_box = QCheckBox("这是一个 QCheckBox")
        self.radio_button = QRadioButton("这是一个 QRadioButton")
        self.push_button = QPushButton("这是一个 QPushButton")
        self.slider = QSlider(Qt.Horizontal)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(50)
        self.spin_box = QSpinBox()
        self.date_edit = QDateEdit()
        self.custom_widget = QWidget()

        # 创建一个表格
        self.table = QTableWidget(3, 3)
        self.table.setHorizontalHeaderLabels(['列1', '列2', '列3'])
        for i in range(3):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(f"单元格 {i+1},{j+1}"))

        # 创建一个选项卡组件
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")

        # 在选项卡中添加组件
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel("这是 Tab 1"))
        self.tab1.setLayout(tab1_layout)

        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel("这是 Tab 2"))
        self.tab2.setLayout(tab2_layout)

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.check_box)
        layout.addWidget(self.radio_button)
        layout.addWidget(self.push_button)
        layout.addWidget(self.slider)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.spin_box)
        layout.addWidget(self.date_edit)
        layout.addWidget(self.custom_widget)
        layout.addWidget(self.table)
        layout.addWidget(self.tab_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_qss_files(self):
        """加载当前目录下的所有 QSS 文件到下拉菜单中"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qss_files = [f for f in os.listdir(current_dir) if f.endswith('.qss')]
        self.combo_box.addItems(qss_files)

    def load_selected_qss(self):
        """加载选中的 QSS 文件并应用样式"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qss_file = self.combo_box.currentText()
        self.qss_path = os.path.join(current_dir, qss_file)

        self.apply_qss(self.qss_path)
        # 添加文件监视
        self.watcher.addPath(self.qss_path)

    def apply_qss(self, qss_path):
        """应用指定的 QSS 文件"""
        with open(qss_path, 'r', encoding='utf-8') as file:
            qss = file.read()
            self.setStyleSheet(qss)

    def reload_qss(self, path):
        """重新加载并应用 QSS 文件"""
        QTimer.singleShot(100, lambda: self.apply_qss(path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = QSSSwitcher()
    window.show()

    sys.exit(app.exec_())
