from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from dual_logger import UniversalLogger
import sys

def trigger_error(button):
    print (button.a)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()

    logger = UniversalLogger(log_file="your_log_file.log")
    logger.enable()

    button = QPushButton("Trigger Error")
    button.clicked.connect(lambda:trigger_error(button))

    layout.addWidget(button)
    window.setLayout(layout)
    window.setWindowTitle("Universal Logger Test")
    window.show()

    sys.exit(app.exec_())
