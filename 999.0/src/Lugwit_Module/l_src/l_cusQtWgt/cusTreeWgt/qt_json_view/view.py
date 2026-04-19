import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from QJsonTreeWidget import QJsonTreeWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建 QJsonTreeWidget 实例
        self.tree_widget = QJsonTreeWidget()
        self.setCentralWidget(self.tree_widget)

        # 加载 JSON 数据
        json_data = {
                "data": [
                    {
                        "MainId": 1111,
                        "firstName": "Sherlock",
                        "lastName": "Homes",
                        "categories": [
                            {
                                "CategoryID": 1,
                                "CategoryName": "Example"
                            }
                        ]
                    },
                    {
                        "MainId": 122,
                        "firstName": "James",
                        "lastName": "Watson",
                        "categories": [
                            {
                                "CategoryID": 2,
                                "CategoryName": "Example2"
                            }
                        ]
                    }
                ],
                "messages": [],
                "success": 'true'
            }
        self.tree_widget.loadJson(json_data)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
