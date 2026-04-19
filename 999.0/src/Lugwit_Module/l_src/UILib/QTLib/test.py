
import sys

from PyQt6.QtWidgets import QApplication

from PyQt6 import uic

sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\ProjectManageSoftware\UI\uiFile\customQt')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = uic.loadUi(r"ProjectManageSoftware\UI\uiFile\TabWidget\A_ProjectList.ui")
    ui.show()

    sys.exit(app.exec())