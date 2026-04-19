# coding:utf-8
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
import copy
import re
import pyperclip

QT_API=os.environ.get('QT_API','PySide6')
print ('QT_API',QT_API,__file__   )
# exec('from {}.QtWidgets import *'.format(QT_API))
# exec('from {}.QtCore  import *'.format(QT_API))
# exec('from {}.QtGui  import *'.format(QT_API))

sys.path.append(r'D:\\TD_Depot\\Software\\LUGWIT~1\\LUGWIT~1\\trayapp/Lib\\Lugwit_Module\\l_src\\l_qtpy{}'.format(sys.version_info.major))

from qtpy.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
    QStatusBar, QSizePolicy, QDialog, QSpacerItem,QLabel,QWidget,QComboBox,QProgressDialog,QSpinBox,
    QCheckBox,QRadioButton,QTableWidget,QAbstractItemView,QTableWidgetItem,QMenu,QAction,)
from qtpy.QtCore import Qt, QTimer, QEvent, QCoreApplication, QRect,QPoint,Signal,QThread

from qtpy.QtCore import Qt, QMimeData, QEvent, QPoint,QObject
from qtpy.QtGui import QDragEnterEvent, QDropEvent


l_srcDir=re.search(r'.+l_src',__file__).group()
sys.path.append(l_srcDir)

from usualFunc import lprint


curDir = os.path.dirname(__file__)
sys.path.append(curDir)


from functools import partial



def randomString(ki):
    return "".join(random.sample(string.ascii_letters + string.digits, ki))


def _NCZPlayListSort(lis, is_reverse=False):
    """
    播放列表排序，实际是字符串列表排序，根据字母数字
    :param lis: 字符串列表
    :param is_reverse: 反向
    :return: 排序后的列表
    """
    lists = list(lis)
    count = len(lists)
    for i in range(0, count):
        for j in range(i + 1, count):
            if is_reverse:
                if os.path.basename(lists[i]).lower() < os.path.basename(lists[j]).lower():
                    lists[i], lists[j] = lists[j], lists[i]
            else:
                if os.path.basename(lists[i]).lower() > os.path.basename(lists[j]).lower():
                    lists[i], lists[j] = lists[j], lists[i]
    return lists


def _NCZGetAllFileList(file_path=None, key=None, key_ignore_case=True, include_sub_folder=False, ext_list=None):
    """
    依据文件名关键字，文件后缀名查找指定目录内的文件，并记录为列表
    :param include_sub_folder: 查找所有子目录
    :param key_ignore_case: 忽略文件名关键字大小写
    :param file_path: 指定目录
    :param key: 文件名关键字
    :param ext_list: 后缀名列表
    :return: 文件列表
    """
    temp = []
    if include_sub_folder:
        for root, dirs, files in os.walk(file_path):
            for f in files:
                ffn = os.path.join(root, f).replace("\\", "/")
                if ffn not in temp:
                    temp.append(ffn)
    else:
        for f in os.listdir(file_path):
            ffn = os.path.join(file_path, f).replace("\\", "/")
            if ffn not in temp:
                temp.append(ffn)
    ffn_list = []
    if len(temp) > 0:
        for ffn in temp:
            fbn, ext = os.path.splitext(ffn)
            if key:
                if not key_ignore_case:
                    if key not in fbn:
                        continue
                else:
                    if key.lower() not in fbn.lower():
                        continue
            if len(ext_list) > 0 and ext.lower() not in ext_list:
                continue
            if ffn not in ffn_list:
                ffn_list.append(ffn)
    return ffn_list


def _NCZPathFormat(_path_=None):
    """
    路径格式化，Unix风格，二级目录如果是//则改为/
    :param _path_: 目标路径，可文件，可目录
    :return: 格式化路径
    """
    if _path_:
        _path_ = _path_.replace("\\", "/")
        if _path_.startswith("//"):
            _path_ = _path_[2:]
            if "//" in _path_:
                _path_ = _path_.replace("//", "/")
            _path_ = "//{0}".format(_path_)
        else:
            if "//" in _path_:
                _path_ = _path_.replace("//", "/")
    return _path_


class CZScanFiles(object):
    """
    快速查找目录内的所有文件，包含所有子目录文件
    比os.walk()快很多
    """

    def __init__(self):
        self.ffn_list = []

    def scan(self, d):
        for i in os.scandir(d):
            if i.is_dir():
                self.scan(i)
            else:
                self.ffn_list.append(i.path)


def withChinese(s):
    """
    检查整个字符串是否包含中文
    :param s: 需要检查的字符串
    :return: bool
    """
    for ch in s:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
 
class UploadTable(QTableWidget):
    drop_event = Signal()

    def __init__(self, parent=None,init_taskList=[]):
        super(type(self), self).__init__(parent)
        self.check_list = None
        self.parent = parent
        self.setAcceptDrops(True)
        self.rowHeight=50
        
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.table_labels = [u"导出", u"FileFullName(文件长名)"]
        self.task_list = []
        # if not init_taskList:
        #     init_taskList = [
        #         r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP107\Animation\scenes&movies\CW_EP107_SC002_an.ma',
        #         ]
        for i,x in enumerate(init_taskList):
            init_taskList[i]=x.replace('\\','/')
        self.init_taskList = init_taskList
        self.temp_list = []
        # self.setMinimumSize(550, 300)
        self.initUI()

    def initUI(self):
        self.setColumnCount(len(self.table_labels))
        self.horizontalHeader().setCascadingSectionResizes(True)
        self.setHorizontalHeaderLabels(self.table_labels)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ppmSetup)
        # 添加一行
        self.setRowCount(len(self.init_taskList))
        self.setWordWrap(True)
        for index,taskFile in enumerate(self.init_taskList):
            self.setCellWidget(index, 0, self.qbc_wgt())
            taskFile.replace("\\", "/")
            item=QTableWidgetItem(taskFile)
            self.setRowHeight(index,self.rowHeight)
            self.setRowHeight(index,self.rowHeight)
            item.setToolTip(taskFile)
            self.setItem(index, 1, item)

        
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 520)
        self.updateTaskList()
        
        
    @staticmethod
    def qbc_wgt():
        widget = QWidget()
        wgt = QCheckBox()
        wgt.setChecked(True)
        widget.ckb = wgt
        lay = QHBoxLayout()
        lay.addWidget(wgt)
        lay.setAlignment(wgt, Qt.AlignCenter)
        lay.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(lay)
        return widget

    def ppmSetup(self, pos):
        buff = [""]
        if len(buff) >= 0:
            the_menu = QMenu()

            the_menu.addAction(u"浏览源文件", self.viewSource)
            the_menu.addAction(u'复制路径', self.copySourcePath)
            # the_menu.addAction(u'全部删除', self.ppmDeleteAll)
            the_menu.exec_(self.mapToGlobal(pos))

    def viewSource(self,aa=None):
        print (aa)
        if self.rowCount() > 0:
            taskFile = os.path.dirname(self.item(self.selectedItems()[0].row(), 1).text())
            ffp = os.path.dirname(taskFile)
            if os.path.isdir(taskFile):
                os.startfile(taskFile)

    def copySourcePath(self):
        if self.rowCount() > 0:
            taskFile = os.path.dirname(self.item(self.selectedItems()[0].row(), 1).text())
            ffp = os.path.dirname(taskFile)
            if os.path.isdir(taskFile):
                pyperclip.copy(taskFile)

    def scrollContentsBy(self, dx, dy):
        # 仅允许垂直滚动
        super().scrollContentsBy(0, dy)


    def updateTaskList(self):
        self.check_list = []
        self.task_list = []
        rid_list = [rid for rid in range(0, self.rowCount())]
        if rid_list and len(rid_list) > 0:
            for rid in rid_list:
                enable = self.cellWidget(rid, 0).ckb.isChecked()
                taskFile = self.item(rid, 1).text()
                d = {"enable": enable, "taskFile": taskFile}
                if d not in self.task_list:
                    self.task_list.append(d)
                if enable not in self.check_list:
                    self.check_list.append(enable)

    def ppmDeleteSel(self):
        selected_rid = []
        for item in self.selectedItems():
            rid = item.row()
            if rid not in selected_rid:
                selected_rid.append(rid)
                enable = self.item(rid, 0).text()
                taskFile = self.item(rid, 1).text()
                d = {"enable": enable, "taskFile": taskFile}
                if d in self.task_list:
                    self.task_list.remove(d)
        for ri in selected_rid[::-1]:
            self.removeRow(ri)
        self.update()

    def updateItemColor(self, result_dict=None):
        if result_dict:
            rid_list = [rid for rid in range(0, self.rowCount())]
            if rid_list and len(rid_list) > 0:
                for rid in rid_list:
                    enable = self.item(rid, 0).text()
                    if enable in result_dict.keys():
                        chk_json = result_dict[enable]
                        missing_dict = json.load(open(chk_json, "r"))
                        if missing_dict and "missing_files" in missing_dict.keys():
                            missing_list = missing_dict["missing_files"]
                            self.parent.logInfo("default", "{0}".format(enable))
                            if missing_list:
                                self.parent.logInfo("warning", "--->Linked file missing:")
                                self.item(rid, 0).setForeground(QBrush(QColor(255, 0, 0)))
                                self.item(rid, 1).setForeground(QBrush(QColor(255, 0, 0)))
                                for missing_file in missing_list:
                                    self.parent.logInfo("error", "--->{0}".format(missing_file))

    def ppmDeleteAll(self):
        for ri in range(0, self.rowCount())[::-1]:
            self.removeRow(ri)
        self.clearContents()
        self.setRowCount(0)
        self.update()

    def dragEnterEvent(self, event):
        event.accept()
        # set selected task color to indicated

    def dragLeaveEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        # for dragEnterEvent+dropEvent to work together
        # we must apply dragMoveEvent in this way.
        event.accept()

    def dropEvent(self, event):
        event.accept()
        if event.mimeData().hasUrls():
            maya_file_list = []
            for this_url in event.mimeData().urls():
                taskFile = this_url.toString()
                taskFile = taskFile.split('///')[-1]

                if os.path.isfile(taskFile):
                    if taskFile not in maya_file_list:
                        enable, ext = os.path.splitext(os.path.basename(taskFile))
                        if ext.lower() in [".ma", ".mov", ".nk", ".hip"]:
                            maya_file_list.append(taskFile)
                else:
                    for a, b, c in os.walk(taskFile):
                        for f in c:
                            taskFile_ = os.path.join(a, f).replace("\\", "/")
                            enable, ext = os.path.splitext(os.path.basename(taskFile_))
                            if ext.lower() in [".ma", ".mov", ".nk", ".hip"] and taskFile_ not in maya_file_list:
                                maya_file_list.append(taskFile_)
            if len(maya_file_list) > 0:
                self.temp_list = copy.deepcopy(_NCZPlayListSort(list(set(maya_file_list))))
                self.temp_list=[{'enable':True,'taskFile':x} for x in self.temp_list]
                if self.temp_list:
                    the_menu = QMenu()

                    #the_menu.setAttribute(Qt.WA_TranslucentBackground)
                    the_menu.setWindowFlags(the_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
                    # the_menu.addAction(u'清空后添加(New)', self.newTasks)
                    the_menu.addAction(u'追加到已有(Append)', self.addTasks)
                    the_menu.exec_(self.mapToGlobal(event.pos()))

    def newTasks(self):
        self.task_list = copy.deepcopy(self.temp_list)
        lprint (self.task_list)
        for temp in self.temp_list:
            self.temp_list['taskFile']=self.temp_list['taskFile'].replace('\\','/')
        self.setupTable()
        self.drop_event.emit()

    def addTasks(self):
        self.task_list = copy.deepcopy(self.task_list+self.temp_list )
        for task in self.task_list:
            task['taskFile'] = task['taskFile'].replace('\\', '/')

        if self.task_list:
            self.setupTable()
            self.drop_event.emit()

    def setupTable(self):
        task_list = copy.deepcopy(self.task_list)
        lprint (self.task_list)
        # lprint(task_list)
        self.ppmDeleteAll()
        self.update()
        lprint(task_list)
        for taskDict in task_list:
            enable, taskFile = taskDict.values()
            fsn = os.path.basename(taskFile)
            # enable, ext = os.path.splitext(fsn)
            # lprint("setupTable", enable, taskFile)
            # state col | enable col | taskFile col
            ri = self.rowCount()
            self.insertRow(ri)
            # 0 enable
            isPlayBlast_item = self.qbc_wgt()
            self.setCellWidget(ri, 0, isPlayBlast_item)
            # 1 taskFile
            taskFile_item = QTableWidgetItem()
            taskFile_item.setTextAlignment(Qt.AlignVCenter)
            taskFile=taskFile.replace("\\", "/")
            taskFile_item.setText(taskFile)
            taskFile_item.setToolTip(taskFile)
            taskFile_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(ri, 1, taskFile_item)
            # lprint(".")
            # lprint(".")
            
def test():
    # 创建一个应用程序实例
    app = QApplication(sys.argv)

    # 创建一个 QWidget 实例作为 UploadTable 的父窗口
    parent = QWidget()

    # 创建一个 UploadTable 实例
    table = UploadTable(parent)
    # table.temp_list=[
    #     {"enable": "True",
    #      "taskFile": r'D:\TD_Depot\ShanShui\ShanShui_L\MayaModules\Yeti3.0.1\examples\yeti_simulationWFieldsExample.ma'
    #      }]
    # 创建一个 QVBoxLayout 实例并将 UploadTable 添加到其中
    layout = QVBoxLayout()
    layout.addWidget(table)

    # 将 QVBoxLayout 设置为父窗口的布局
    parent.setLayout(layout)

    # 显示父窗口
    parent.show()

    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == '__main__':
    test()
