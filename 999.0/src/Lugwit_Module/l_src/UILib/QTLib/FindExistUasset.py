
# coding:utf-8
from __future__ import print_function
from __future__ import absolute_import

import os,sys,re,traceback,json
from datetime import datetime
from collections import defaultdict
from functools import partial
import pyperclip
QT_API = os.environ.get("QT_API")
if not QT_API:
    QT_API = "PyQt5"
if "maya" in sys.executable:
    QT_API = "PySide2"
QT_API = "PyQt5"
exec('import  {}'.format(QT_API))
exec('from {}.QtWidgets import *'.format(QT_API))
exec('from {}.QtCore  import *'.format(QT_API))
exec('from {}.QtGui  import *'.format(QT_API))

l_srcDir = re.search('.+l_src',__file__).group(0)
sys.path.append(l_srcDir)

from usualFunc import lprint


if 'Side' in QT_API:
    Signal=Signal
else:
    Signal=pyqtSignal

class QLineEdit(QLineEdit):
    doubleClicked = Signal(object)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit(self)  # 在双击事件中发出信号
    
class SearchDialog(QDialog):
    file_selected = Signal(str)  # 创建一个信号，当用户选择一个文件时触发

    def __init__(self, exHis='',
                 directory=r"Z:\Cosmos_Wartale_UE\Content\01_Main-Production\01_episode", 
                 keywords="EP100 CH_NEZHA.uasset", title = '查找文件',
                 filePathAsNameRule='xxx',parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.directory = directory
        self.keywords = keywords

        filePathAsNameRule_hlay =  QHBoxLayout()
        filePathAsNameRule_hlay.addWidget(QLabel("文件名称按照命名规则:"))


        
        self.filePathAsNameRule_exist = QLabel()
        
        filePathAsNameRule_hlay.addWidget(self.filePathAsNameRule_exist)

        exHisWgt = QLabel("导出历史")
        self.exHisWgt = QComboBox()

        self.filePathAsNameRule_lineedit = QLineEdit(filePathAsNameRule)
        self.filePathAsNameRule_lineedit.doubleClicked.connect(self.select_file)
        self.filePathAsNameRule_lineedit.setReadOnly(True)
        self.filePathAsNameRule_lineedit.setToolTip(exHis)
        self.filePathAsNameRule_lineedit.textChanged.connect(self.filePathAsNameRule_lineedit_changeFuction)
        filePathAsNameRule_hlay.addWidget(self.filePathAsNameRule_lineedit)
        
        searchLoactionLay=  QHBoxLayout()
        self.directory_label = QLabel(u"搜索位置:")
        searchLoactionLay.addWidget(self.directory_label)
        
        self.directory_box = QLineEdit()
        self.directory_box.setText(self.directory)  # 设置搜索框的默认值
        searchLoactionLay.addWidget(self.directory_box)
        
        keyWord_hlay =  QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setText(self.keywords)  # 设置搜索框的默认值

        self.file_list_wgt = QTableWidget()
        self.file_list_wgt.setColumnCount(3)
        self.file_list_wgt.setHorizontalHeaderLabels(['文件路径', '修改时间', '文件大小'])
        self.file_list_wgt.setColumnWidth(0, 735)  # 设置列宽度
        self.file_list_wgt.setColumnWidth(1, 140)
        self.file_list_wgt.setColumnWidth(2, self.width() - 735 - 150)

        keyWord_hlay.addWidget(QLabel(u"搜索关键词:"))
        keyWord_hlay.addWidget( self.search_box)

        layout = QVBoxLayout()
        layout.addLayout(filePathAsNameRule_hlay)
        layout.addLayout(searchLoactionLay)
        layout.addLayout(keyWord_hlay)
        layout.addWidget(QLabel(u'搜索到的文件列表 ↓↓↓'))
        layout.addWidget(self.file_list_wgt)
        self.setLayout(layout)

        
        self.directory_box.textChanged.connect(self.search)
        self.search_box.textChanged.connect(self.search)
        self.file_list_wgt.itemDoubleClicked.connect(self.select_file)

        self.search(self.keywords)  # 打开SearchDialog就开始搜索
        self.filePathAsNameRule_lineedit_changeFuction()
        self.setMinimumWidth(1000)

    def filePathAsNameRule_lineedit_changeFuction(self):
        filePath = self.filePathAsNameRule_lineedit.text()
        exist = os.path.exists(self.filePathAsNameRule_lineedit.text())
        modified_time=''
        if exist:
            modified_time = datetime.fromtimestamp(os.path.getmtime(filePath)).strftime('%Y-%m-%d %H:%M:%S')
        self.filePathAsNameRule_exist.setText(
                '(文件存在{}:{})'.format(exist,modified_time))


    def search(self, text):
        # 清空文件列表
        self.file_list_wgt.setRowCount(0)

        # 按空格拆分用户输入的字符串成关键字
        keywords = text.lower().split()
        directory = self.directory_box.text()
        for root, dirs, files in os.walk(directory):
            for file in files:
                # 检查文件的全路径是否包含所有的关键字
                full_path = os.path.join(root, file)
                full_path_lower = full_path.lower()
                if all(keyword in full_path_lower for keyword in keywords):
                    # 添加到 QTableWidget
                    row_position = self.file_list_wgt.rowCount()
                    self.file_list_wgt.insertRow(row_position)

                    modified_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S')
                    file_size = os.path.getsize(full_path)

                    self.file_list_wgt.setItem(row_position, 0, QTableWidgetItem(full_path))
                    self.file_list_wgt.setItem(row_position, 1, QTableWidgetItem(modified_time))
                    self.file_list_wgt.setItem(row_position, 2, QTableWidgetItem(str(file_size/1024/1024)[:6] + 'M'))


    def select_file(self, item):
        # 当用户双击一个文件时，触发file_selected信号，并关闭对话框
        row = item.row()  # 获取被双击的项所在的行号
        file_path_item = self.file_list_wgt.item(row, 0)  # 获取该行第一列的项（文件路径）
        self.file_selected.emit(file_path_item.text())  # 发出信号，传递文件路径
        self.accept()

class NoHighlightDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # 移除焦点和悬停状态的标志
        option.state &= ~QStyle.StateFlag.State_MouseOver
        option.state &= ~QStyle.StateFlag.State_Selected
        super().paint(painter, option, index)

class MyComboBox(QComboBox):
    re_importValueChanged = Signal(str,bool)
    backGroundColorChanged = Signal(str,str)
    def __init__(self, directory=r"Z:\Cosmos_Wartale_UE\Content\01_Main-Production\01_episode",
        keywords="EP100 CH_NEZHA.uasset",title='查找文件',filePathAsNameRule='xxx',parent=None,
        parentWgt=None):
        
        super(MyComboBox,self).__init__(parent)
        self.directory=directory
        self.keywords=keywords
        self.title=title
        self.filePathAsNameRule=filePathAsNameRule
        self.dialog = None
        self.dialog_exHis = None
        self.parentWgt=parentWgt
        self._re_import = self.parentWgt._re_import
        self._backGroundColor = self.parentWgt._backGroundColor

        self.lockAttr_backGroundColor = False
        self.lockAttr_re_import = False

        
        self.toolTipDict = defaultdict(dict)
        self.toolTipDict['filePath']=''
        self.setItemDelegate(NoHighlightDelegate(self))

    def mousePressEvent(self, event=None):
        # 当用户点击QComboBox时，弹出搜索对话框
        lprint (self.directory,self.keywords)
        try:
            if  event.button() == Qt.MouseButton.LeftButton:
                self.dialog = SearchDialog(directory=self.directory,keywords=self.keywords,
                    title=self.title,filePathAsNameRule=self.filePathAsNameRule, 
                    parent=self,exHis=self.dialog_exHis)
                self.dialog.show()
                self.dialog.file_selected.connect(self.set_current_text)
        except:
            print (traceback.print_exc())

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        action1 = QAction('打开文件目录', self)
        action2 = QAction('切换强制重新导出或组装', self)
        action3 = QAction('复制文件路径', self)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        def openFileDir():
            fileDir=os.path.dirname(self.currentText())
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            if os.path.isdir(fileDir):
                os.startfile(fileDir)
            self.clearFocus()

        def copyFilePath():
            filePath=self.currentText()
            filePath=os.path.normpath(filePath)
            pyperclip.copy(filePath)

        action1.triggered.connect(openFileDir)
        action2.triggered.connect(self.ToggleBackhroundColor)
        action3.triggered.connect(copyFilePath)
        menu.exec_(self.mapToGlobal(event.pos()))
    
    def printStyleSheet(self):
        lprint(self.styleSheet())

    def ToggleBackhroundColor(self,checkState=False,color="#008000"):
        lprint (color)
        self.lockAttr_backGroundColor=True
        self.lockAttr_re_import=True
        lprint (self.backGroundColor)
        # if not os.path.exists(self.currentText()):
        #     self._backGroundColor="#008000"
        # else:
        self._backGroundColor = '#c2c2c2' if self.backGroundColor=="#008000" else '#008000'
        lprint (self._backGroundColor=="#008000",self._backGroundColor)
        style_str = """
            QComboBox {{ 
            background-color : {};
                                }}
            """.format(self.backGroundColor)
        lprint (style_str)
        self.setStyleSheet(style_str)
        self.re_import =  True if self.backGroundColor=="#008000" else False
        self.parentWgt.exFromMaya = self.backGroundColor =="#008000"
        self.custom_setToolTip()
        self.clearFocus()

    def setExOrGrpState(self,re_import=True,backGroundColor="#008000"):
        self.lockAttr_backGroundColor=re_import
        self.lockAttr_re_import=re_import
        lprint (self.lockAttr_re_import)
        if not self.currentText():
            return
        self._backGroundColor=backGroundColor
        style_str = """
            QComboBox {{ 
            background-color : {};
                                }}
            """.format(self.backGroundColor)
        self.setStyleSheet(style_str)
        self.re_import =  re_import
        self.parentWgt.exFromMaya = self.backGroundColor == "#008000"
        self.custom_setToolTip()
        self.clearFocus()

    def custom_setToolTip(self):
        self.toolTipDict['filePath']=self.currentText()
        self.toolTipDict['self.lockAttr_backGroundColor']=self.lockAttr_backGroundColor
        self.toolTipDict['self.lockAttr_re_import']= self.lockAttr_re_import
        toolTip = json.dumps(\
                self.toolTipDict,indent=4,ensure_ascii=False)
        self.setToolTip(toolTip)

    def set_current_text(self, text):
        # 将选中的文件设置为QComboBox的当前文本
        index = self.findText(text)
        if index == -1:
            # 如果文件还不在QComboBox中，添加它
            self.addItem(text)
            index = self.findText(text)
        self.setCurrentIndex(index)
        self.toolTipDict['filePath']=self.currentText()
        self.setToolTip(json.dumps(self.toolTipDict,indent=4,ensure_ascii=False))  # 设置工具提示为当前文本

    @property
    def re_import(self):
        return self._re_import

    @re_import.setter
    def re_import(self, value):
        self._re_import = value
        # Step 3: Emit the signal when the property value changes
        self.re_importValueChanged.emit('re_import',self._re_import)
        if value ==True:
            FileExportMainUI_Wgt=self.parentWgt.parentWgt
            if FileExportMainUI_Wgt.initUIFinish == False:
                return
            nsListWidgetDict=FileExportMainUI_Wgt.nsListWidgetDict
            nameSpaceWgt=nsListWidgetDict.get(self.parentWgt.nameSpace)
            isExWgt=nameSpaceWgt.get('isEx')
            isGrpWgt=nameSpaceWgt.get('isGrp')
            if self.parentWgt.columnInfo.fmt == '.fbx':
                isExWgt.setChecked(True)
            elif self.parentWgt.columnInfo.fmt == '.uasset':
                isGrpWgt.setChecked(True)

    @property
    def backGroundColor(self):
        return self._backGroundColor

    @backGroundColor.setter
    def backGroundColor(self, value):
        if self.lockAttr_backGroundColor:
            return
        self._backGroundColor = value
        # Step 3: Emit the signal when the property value changes
        if self._backGroundColor:
            style_str = """
                QComboBox {{ 
                background-color : {};
                                    }}
                """.format(self.backGroundColor)
        else:
            style_str=""
        self.setStyleSheet(style_str)
        self.backGroundColorChanged.emit('backGroundColor',self._backGroundColor)
        self.parentWgt.exFromMaya = self.backGroundColor =="#008000"

class MyCheckBox(QCheckBox):
    def __init__(self,):
        super().__init__()
        self.setProperty('font_size', "small")
    
    def mousePressEvent(self, event):
        # 通过不调用父类的mousePressEvent方法，屏蔽掉鼠标点击事件
        pass

class MyWidget(QWidget):
    def __init__(self, title=u'查找文件',directory='',filePath=None,keywords='.fbx',filePathAsNameRule='xxxx'):
        super().__init__()
        self.filePath = filePath
        self._re_import = False
        self._backGroundColor = "#c2c2c2"
        self.checkbox = MyCheckBox()
        self.combobox = MyComboBox(title=title,filePathAsNameRule=filePathAsNameRule,
                                directory=directory,keywords=keywords,parentWgt=self)
        self.combobox.set_current_text(self.filePath)
        self.currentIndexChanged=self.combobox.currentIndexChanged
        self.currentTextChanged=self.combobox.currentTextChanged
        self.currentTextChanged.connect(self.currentTextChanged_func)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.checkbox,1)
        layout.addWidget(self.combobox,10)
        self.setLayout(layout)

        if self.filePath:
            self.checkbox.setChecked(os.path.exists(self.filePath))

        if self.combobox.count() > 0:
            self.combobox.setCurrentText(self.combobox.currentText())

    def currentTextChanged_func(self):
        self.checkbox.setChecked(os.path.exists(self.combobox.currentText()))

    
    def isChecked(self):
        return self.checkbox.isChecked()

    def currentText(self):
        return self.combobox.currentText()
    
    def text(self):
        return self.combobox.currentText()

    def setDialogWindowTitle(self,title):
        self.combobox.title=title

    def setCurrenText(self, text):
        self.combobox.set_current_text(text)
        if os.path.exists(text):
            self.checkbox.setChecked(True)  
            
    def setText(self, text):
        self.combobox.set_current_text(text)
        if os.path.exists(text):
            self.checkbox.setChecked(True) 
        self.filePath = text
            
    def setChecked(self, checked):
        self.checkbox.setChecked(checked)
        
    # def setBackground(self, color):
    #     self.combobox.setStyleSheet("QComboBox { background-color: %s }" % color)
    #     self.combobox.backGroundColor=color

    def setSearchDir(self,directory):
        self.combobox.directory=directory

    def setExHisTip(self,toolTip):
        self.combobox.dialog_exHis=toolTip

    def setkeywords(self,keywords):
        self.combobox.keywords=keywords
        lprint (self.combobox.keywords)

    def set_filePathAsNameRule(self,filePathAsNameRule):
        self.combobox.filePathAsNameRule=filePathAsNameRule

    def getBackgroundColorName(self):
        """
        获取 QComboBox 背景颜色的名称。
        
        返回:
            str: 背景颜色的名称。
        """
        palette = self.combobox.palette()
        color = palette.color(QPalette.Background)
        return color.name()

    @property
    def re_import(self):
        #return self._re_import
        return self.combobox.re_import

    @re_import.setter
    def re_import(self, value):
        #self._re_import = value
        self.combobox.re_import = value


    @property
    def backGroundColor(self):
        #return self._backGroundColor
        return self.combobox.backGroundColor
    
    @backGroundColor.setter
    def backGroundColor(self, value):
        self.combobox.backGroundColor=value


        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建一个 MyWidget 实例
    widget = MyWidget(
                    directory=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP107\FBX\Shot_002',
                    filePath=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP107\FBX\Shot_002\EP107_SC002_Cam_101_160.fbx',
                    keywords='.fbx',
                    filePathAsNameRule=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP107\FBX\Shot_002\EP107_SC002_CH_YANGJIAN_Ani.fbx')
    widget.setDialogWindowTitle('可以使用存在的资产,也可以从重新导出资产')
    # 设置一些属性
    # widget.setCurrenText("EP100 CH_NEZHA.uasset")
    widget.setChecked(True)
    # widget.setBackground("red")

    # 显示 widget
    widget.show()

    sys.exit(app.exec_())
