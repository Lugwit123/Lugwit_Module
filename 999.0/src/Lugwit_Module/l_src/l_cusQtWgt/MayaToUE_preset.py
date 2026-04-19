import os,sys,re
os.environ['QT_API']='PyQt5'
import cusTreeWgt
from PyQt5.QtWidgets import *
app=QApplication(sys.argv)



class mainUI(QWidget):
    def __init__(self):
        super(mainUI, self).__init__()  # 调用QWidget的构造函数
        self.lay=QVBoxLayout()
        self.setLayout(self.lay)
        self.ui=cusTreeWgt.LTreeWidget(
                jsonFileList=[r'A:\TD\RenderFarm\MayaToUE\data\base.json'],
                headerList=["层级", "标识"],
                columnWidthList=[1050,220,150],
                baseJsonFile=r'A:\TD\RenderFarm\MayaToUE\data\base.json',
                parent=self)
        self.lay.addWidget(self.ui)

def show_Main(*args):
    global hierarchy_QTableWidget_win
    hierarchy_QTableWidget_win=mainUI()
    hierarchy_QTableWidget_win.show()
    # hierarchy_QTableWidget_win = ui.show()
    sys.exit(app.exec_())

print (__name__)
if __name__ == '__main__':
    #show_hierarchy_QTableWidget_Win()
    show_Main()