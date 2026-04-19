# -*- coding: utf-8
from __future__ import print_function
import os,sys
from PySide2.QtWidgets import *

class verify_table_wgt_Info:
    columnLableList=['检查项目','必须项','可选项','检查结果','自动修改']
    columnWidgetRadio=[10,2,2,2,2]
    tableWidth=1000

    
def init(tableWidget, initInfo):
    '从initInfo初始化表格'
    columnWidgetRadio = initInfo.columnWidgetRadio
    columnLableList = initInfo.columnLableList
    tableWidth = initInfo.tableWidth
    
    # 设置表格列数
    tableWidget.setColumnCount(len(columnLableList))
    
    # 设置列标题
    tableWidget.setHorizontalHeaderLabels(columnLableList)
    
    # 调整列宽
    columnWidgetRadio_and = sum(columnWidgetRadio)
    for i, widthRatio in enumerate(columnWidgetRadio):
        tableWidget.setColumnWidth(i, widthRatio/columnWidgetRadio_and
                                   * tableWidth)  # 假设基础宽度为100，根据比例调整
    tableWidget.setFixedWidth(tableWidth+1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tableWidget = QTableWidget()
    info = verify_table_wgt_Info
    info.tableWidth=1000
    init(tableWidget, info)
    tableWidget.show()
    sys.exit(app.exec_())
