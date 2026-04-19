from PyQt5.QtWidgets import *
import os,re,sys
import unittest
l_srcDir = re.search(r'.*l_src',__file__,flags=re.I).group()
sys.path.append(l_srcDir)

from usualFunc import lprint

# 存储所有同步实例的列表

def sync_widgets_dec(cls):
    class SyncedWidget(cls):
        instances = set()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.sync_connections()

        @classmethod
        def get_instances(cls):
            return cls.instances  # 返回所有实例的列表
        
        def __getattribute__(self, name):
            if  os.environ.get("forbidden_run_sync_widgets_dec")=='1':
                return 
            else:
                return  super().__getattribute__(name)

        def sync_connections(self):
            SyncedWidget.instances.add(self)
            self.children=set([self])
            find_children=self.findChildren(QWidget)
            if find_children:
                self.children.update(find_children)
            for child in self.children:
                if "nosync" in child.objectName():
                    continue  # 跳过不需要同步的组件
                if isinstance(child, QCheckBox):
                    child.stateChanged.connect(self.sync_checkbox)
                elif isinstance(child, QComboBox):
                    child.currentIndexChanged.connect(self.sync_combobox)
                elif isinstance(child, QTableWidget):
                    child.itemChanged.connect(self.sync_table_item)
                elif isinstance(child, QGroupBox):
                    child.toggled.connect(self.sync_QGroupBox_CheckValue)
                    
        def sync_QGroupBox_CheckValue(self, state):
            sender = self.sender()
            try:
                index = self.findChildren(QGroupBox).index(sender)
                for instance in SyncedWidget.instances:
                    if instance != self:
                        groupbox = instance.findChildren(QGroupBox)[index]
                        groupbox.blockSignals(True)
                        groupbox.setChecked(state)  # 使用setChecked而不是setCheckState
                        groupbox.blockSignals(False)
            except:
                for instance in SyncedWidget.instances:
                    instance.setChecked(state)
            
                    


        def sync_checkbox(self, state):
            sender = self.sender()
            index = self.findChildren(QCheckBox).index(sender)
            for instance in SyncedWidget.instances:
                if instance != self:
                    checkbox = instance.findChildren(QCheckBox)[index]
                    checkbox.blockSignals(True)
                    checkbox.setCheckState(state)
                    checkbox.blockSignals(False)

        def sync_combobox(self, index):
            sender = self.sender()
            index_combo = self.findChildren(QComboBox).index(sender)
            for instance in SyncedWidget.instances:
                if instance != self:
                    combobox = instance.findChildren(QComboBox)[index_combo]
                    combobox.blockSignals(True)
                    combobox.setCurrentIndex(index)
                    combobox.blockSignals(False)


        def sync_table_item(self, item):
            sender = self.sender()
            for instance in SyncedWidget.instances:
                if instance != self:
                    table = instance.findChild(QTableWidget)
                    target_item = table.item(item.row(), item.column())
                    if target_item is not None:  # 检查该位置是否有QTableWidgetItem
                        table.blockSignals(True)
                        target_item.setText(item.text())
                        table.blockSignals(False)
                    else:  # 如果该位置没有QTableWidgetItem，则创建一个
                        new_item = QTableWidgetItem(item.text())
                        table.blockSignals(True)
                        table.setItem(item.row(), item.column(), new_item)
                        table.blockSignals(False)

    return SyncedWidget


class MyGroupBox(QGroupBox):
    def __init__(self, title, *args, **kwargs):
        super().__init__(title, *args, **kwargs)
        layout = QVBoxLayout()
        self.setCheckable(1)
        self.setChecked(1)
        # 添加QTableWidget
        self.table = QTableWidget(2, 3)
        for row in range(2):
            self.table.setItem(row, 0, QTableWidgetItem(f"Item {row}"))
            combobox = QComboBox()
            combobox.addItems(["Option 1", "Option 2", "Option 3"])
            self.table.setCellWidget(row, 1, combobox)
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 2, checkbox)
        layout.addWidget(self.table)

        # 添加复选框
        self.checkbox = QCheckBox("Check me")
        layout.addWidget(self.checkbox)

        # 添加下拉框
        self.combobox = QComboBox()
        self.combobox.addItems(["Option A", "Option B", "Option C"])
        layout.addWidget(self.combobox)

        self.setLayout(layout)

class TestWidget(QGroupBox):
    def __init__(self,  parentWidget,*args, **kwargs):
        super().__init__(parentWidget, *args, **kwargs)
        self.parentWidget = parentWidget
        self.sync_widgets_grp=self.parentWidget.sync_widgets_grp

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sync_widgets_grp('AA'))
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication([])

    main_widget = QWidget()
    main_widget.sync_widgets_grp=sync_widgets_dec(MyGroupBox)

    main_layout = QHBoxLayout()
    for _ in range(2):
        group_box = TestWidget(parentWidget=main_widget)
        main_layout.addWidget(group_box)
    main_widget.setLayout(main_layout)
    main_widget.show()

    lprint (main_widget.sync_widgets_grp)
    lprint (main_widget.sync_widgets_grp.instances)
    lprint (sync_widgets_dec(MyGroupBox) is sync_widgets_dec(MyGroupBox))
    app.exec_()

