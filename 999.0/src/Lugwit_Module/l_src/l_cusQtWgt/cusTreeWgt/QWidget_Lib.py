# coding:utf-8
from __future__ import absolute_import
from typing import TypedDict, Literal
import re,sys,os,time,copy,socket,math
# 获取当前文件的路径
l_srcDir = re.search('.+l_src',__file__).group(0)
sys.path.append(l_srcDir)
import l_DataProcess.l_mergeData as l_mergeData
from usualFunc import lprint

curDir=os.path.dirname(__file__)
tempDir=os.getenv('temp')

import generalLib  as gl


            
from UILib.QTLib.styleSheet import self_qss
from usualFunc import lprint

import re,sys,codecs,os,json
import traceback

import glob
import itertools
from functools import partial

# import pkmg
# 下面的代码用于防止 QWidget: Must construct a QApplication before a QWidget错误
# fileIfnoDict=pkmg.getPkmgEnv()
if sys.executable.endswith('maya.exe'):
    os.environ['QT_API']='PySide2'
QT_API=os.environ.get('QT_API')
if not QT_API:
    QT_API='PyQt5'
if 'maya' in sys.executable:
    QT_API='PySide2'
os.environ['QT_API']=QT_API



from qtpy.QtWidgets import *
from qtpy.QtCore  import *
from qtpy.QtGui  import *

import inspect

__file__=inspect.getfile(inspect.currentframe())

l_srcDir=re.search('.*l_src',__file__).group(0)


sys.path.append(l_srcDir+'/UILib/QtLib')


import PySideLib
from imp import reload
reload (PySideLib)

    
keyWordList=[('sim','mesh'),('L','R'),('top','dow'),('HIGH','LOW'),('GRP','')]

try:
    from . import  action
    from . import  readExcel
except Exception as e:
    try:
        import action
        import readExcel
    except Exception as e:
        pass

if not sys.executable.endswith('maya.exe'):
    #app = QApplication(sys.argv)
    pass
    #app.quit()
    #gui_app = QGuiApplication(sys.argv)
else:
    import maya.OpenMayaUI as omui


# region LabelLine的类定义
class LabelLine(QLineEdit):
    try:
        try:
            callBackSignal = Signal(unicode)
        except:
            callBackSignal = Signal(str)
    except:
        try:
            callBackSignal = pyqtSignal(str)
        except:
            callBackSignal = pyqtSignal(unicode)

    def keyPressEvent(self, event):
        super(LabelLine,self).keyPressEvent(event)

        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            pass
            self.callBackSignal.emit(self.text())
        event.accept()
 

    def focusOutEvent(self, event):
        super(LabelLine,self).focusOutEvent(event)
        event.accept()
        self.callBackSignal.emit(self.text())
# endregion       

class customTreeItemWidget(QWidget):
    def __init__(self, parent=None,treeWidget=None,textList=['AA','BB']):
        super(customTreeItemWidget, self).__init__()
        self.textList=textList
        self.treeWidget = treeWidget
        self.setContentsMargins(0, 0, 10, 0)
        
        self.layout=QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.textListWidget_lay=QHBoxLayout()
        self.textListWidget_lay.setContentsMargins(0, 0, 3, 0)
        if not parent:
            parent=self.treeWidget
        self.treeItem = QTreeWidgetItem(parent)
        
        
        self.treeItem.setTextA =self.treeItem.setText
        self.treeItem.textA =self.treeItem.text
        self.iconPushButton = QPushButton()
        self.iconPushButton.setIcon(QIcon(curDir+'/icons/reset.png'))
        self.iconPushButton.setFixedSize(self.iconPushButton.sizeHint()/2)

        
        self.instantTypeCombox = QComboBox()
        self.instantTypeCombox.addItems([u'正则表达式',u'常量',])
        self.instantTypeCombox.setFixedWidth  (130)
        self.layout.addLayout(self.textListWidget_lay,20)
        self.instantTypeCombox.wheelEvent = self.treeWidget.wheelEvent
        
        self.treeItem.textWgt=self
        self.treeItem.instantTypeCombox=self.instantTypeCombox
        
        self.layout.addWidget(self.instantTypeCombox,1)
        self.layout.addWidget(self.iconPushButton,1)
        
        self.comboboxList=[]

        current_font = QComboBox().font()
        font_size = current_font.pointSize()


        self.setStyleSheet(f"QTextEdit{{font-size: {font_size-1}pt;}}")  

        self.initUI()
        self.treeWidget.setItemWidget(self.treeItem, 0, self)  # 将按钮添加到第二列
    
           
    def initUI(self):
        # 清空布局中的所有现有部件
        while self.textListWidget_lay.count():
            item = self.textListWidget_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.textEditList=[]
        for text in self.textList:
            textEdit = SingleLineTextEdit()
            self.textEditList.append(textEdit)
            self.treeItem.text = self.text
            self.treeItem.setText = self.setText
            textEdit.setPlainText(text)  # 为 QTextEdit 设置文本
            self.textListWidget_lay.addWidget(textEdit)
            self.comboboxList.append(textEdit)
        self.layout.addStretch()  # 添加拉伸因子使得按钮左对齐
        
    def setText(self,index=0,text=''):
        if index==0:
            self.textEditList[0].setPlainText(text)
        else:
            self.treeItem.setTextA(index,text)
            
    def text(self,index=0):
        if index==0:
            return self.textEditList[index].toPlainText()
        else:
            return self.treeItem.textA(index)


class SingleLineTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self.onTextChanged)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏垂直滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏水平滚动条
        self.setLineWrapMode(QTextEdit.NoWrap)  # 不允许自动换行
        self.setStyleSheet("QTextEdit {padding: 4px 0px 0px 0px;}")
        
        self.text=''
        # 计算单行文本的高度
        font_metrics = self.fontMetrics()
        single_line_height = font_metrics.lineSpacing()
        
        self.setMaximumHeight(single_line_height + 10)  # 设置最大高度
        self.setMinimumHeight(single_line_height + 10)  # 设置最小高度
        self.isUpdatingText = False  # 添加一个标志以避免递归调用
        
                # 防抖定时器
        self.debounceTimer = QTimer(self)
        self.debounceTimer.setSingleShot(True)
        self.debounceTimer.timeout.connect(self.updateText)

        # 防抖时间间隔 (毫秒)
        self.debounceInterval = 500

    def onTextChanged(self):
        # 重置并启动定时器
        self.debounceTimer.start(self.debounceInterval)
        self.document().setDocumentMargin(1)

    def updateText(self):
        if self.isUpdatingText:
            return
        self.isUpdatingText = True

        cursor = self.textCursor()
        cursor_position = cursor.position()
        current_text = self.toPlainText()
        parts = re.split(r'(\{[^}]*[a-zA-Z]{1}\w+\})', current_text)
        colored_text = self.to_colored_html(parts)

        if self.text != current_text:
            super().setHtml(colored_text)

            # 恢复光标位置，确保位置有效
            cursor.setPosition(min(cursor_position, self.document().characterCount() - 1))
            self.setTextCursor(cursor)
        self.text=self.toPlainText()
        self.isUpdatingText = False
    
    def wheelEvent(self, event):
        pass


    def to_colored_html(self, parts):
        html_parts = []
        for part in parts:
            if part.startswith('{') and part.endswith('}') and len(part)>5:
                color = '#11dbe9'
            else:
                color = '#ffffff'
            html_parts.append(f'<span style="color: {color};">{part}</span>')
        return ''.join(html_parts)
    
    def insertFromMimeData(self, source: QMimeData):
        if source.hasText():
            # 仅接受纯文本内容
            self.insertPlainText(source.text())
        else:
            # 如果不是文本，忽略粘贴请求
            pass



class ColumnRowSeparatorDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        right = option.rect.right()
        bottom = option.rect.bottom()

        # 设置线条颜色和透明度
        line_color = QColor(200, 200, 200) 
        line_color.setAlpha(128)  # 半透明
        painter.setPen(line_color)

        # 绘制垂直分割线
        painter.drawLine(right, option.rect.top(), right, bottom)

        # 绘制水平分割线
        line_color.setAlpha(20)  # 半透明
        painter.setPen(line_color)
        painter.drawLine(option.rect.left(), bottom, right, bottom)
        

class NameLine(LabelLine):
    def __init__(self, parent):
        super().__init__(parent)
        # regex = "[a-zA-Z]+"  # 正则表达式模式
        # validator = QRegularExpressionValidator(QRegularExpression(regex))
        # self.setValidator(validator)

        
class TreeItemMimeData(QMimeData):
    def __init__(self):
        self._format = []
        self._item = None
        super(TreeItemMimeData,self).__init__()
 
    def set_drag_data(self, fmt, item):
        self._format.append(fmt)
        self._item = item
 
    def get_drag_data(self):
        return self._item
 
    def formats(self):
        return self._format
 
    def retrieveData(self, mimetype, preferredType):
        if mimetype == 'ItemMimeData':
            return self._item
        else:
            return QMimeData.retrieveData(mimetype, preferredType)

class hierarchy_treeWidget(QTreeWidget):
    def __init__(self,presetFile='',
                ColumnHeaderList=[u'层级',u'标识','中文名称'],
                parentWgt=None,
                columnWidthList=[600,100,100],):
        super(hierarchy_treeWidget,self).__init__()
        self.NameToItemDict={}
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.flatDict = {} # 所有层级的字典,key为第二列的数据,val为第一列和第三列
        global mesh_icon,group_icon,select_icon,putin_icon
        mesh_icon = QIcon(os.path.abspath(__file__ + "/../icons/mesh.png"))
        group_icon = QIcon(os.path.abspath(__file__ + "/../icons/group.png"))
        select_icon = QIcon(os.path.abspath(__file__ + "/../icons/select.png"))
        putin_icon = QIcon(os.path.abspath(__file__ + "/../icons/putin.png"))
        self.setHeaderLabels(ColumnHeaderList)
        self.presetFile=presetFile
        self.ensure_jsonFileVersion(self.presetFile)

        self.sourceItem=None
        
        if parentWgt:
            self.parentWgt=parentWgt


        #self.header().setHidden(True)
        self.setColumnCount(len(ColumnHeaderList))
        
        self.hierarchy = action.load_hierarchy(self.presetFile)

        
        for index,ColumnWidth in enumerate(columnWidthList):
            self.setColumnWidth(index, ColumnWidth) 


        for document in self.hierarchy:
            item = self.create_item_by_document(self, document)
            if item:
                self.set_expanded(item, True)

        self.setExpandsOnDoubleClick(False)
        self.setIconSize(QSize(16, 16))
        self.itemDoubleClicked.connect(self.edit_hierarchy)
        self.itemClicked.connect(self.select_hierarchy)
        
        # =允许拖拽
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        
        self.setDragDropMode(QTreeWidget.InternalMove)


        self.menu = QMenu(self)
        self.menu.addAction(u"添加组层级", lambda:self.add_hierarchy(name="name_GRP",value="value",icon=''))
        self.menu.addAction(u"添加模型层级", lambda:self.add_hierarchy(name="name",value="value",icon=''))
        self.menu.addAction(u"移除层级", self.remove_hierarchy)
        self.menu.addAction(u"组层级与模型层级切换", self.scene_hierarchy)
        #self.menu.addAction(u"替换为场景层级", self.scene_hierarchy)
        self.menu.addSeparator()
        self.menu.addAction(u'复制层级',lambda *args :self._action_cutOrCopy_handler(cutOrCopy='copy'))
        self.menu.addAction(u'剪切层级',lambda *args :self._action_cutOrCopy_handler(cutOrCopy='cut'))
        self.menu.addAction(u'粘贴层级',lambda *args :self._action_paste_handler())
        self.menu.addAction(u'搜索和替换',lambda *args :self._serachAndReplace())
        self.keyMeun = QMenu(u'添加字段')
        self.menu.addMenu(self.keyMeun)
        for index,keyWords in enumerate(keyWordList):
            for keyWord in keyWords:
                if keyWord:
                    self.keyMeun.addAction(keyWord,partial(self.addKeyWord,'',keyWord))
            self.keyMeun.addSeparator()

        self.menu.addSeparator()
        self.menu.addAction(u"保存模板...", self.save_hierarchy)
        self.menu.addAction(u"导入模板...", self.load_hierarchy)
        
        
        #self.itemChanged.connect(self.handle_item_changed)
        self.itemClicked.connect(self.getTextBeforeModify)
        
        self._index_cmb = 1
        self._index_btn = 2
        self._cutOrCopy_item = None
        self._last_bg_colord_item = None
        self._start_drag_pnt = None
        self.dragging=False
        self.setIndentation(20)
        self.setRootIsDecorated(True)

        self.setItemDelegate(ColumnRowSeparatorDelegate())
        # self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)


    def setItemWidget(self, item, col, wid):
        """
        Overrides QTreeWidget.setItemWidget such that widgets are added inside an invisible wrapper widget.
        This makes it possible to move the item in and out of the tree without its widgets being automatically deleted.
        """
        w = QWidget()  ## foster parent / surrogate child widget
        l = QHBoxLayout()
        l.setContentsMargins(0,0,0,0)
        w.setLayout(l)

        l.addWidget(wid)
        w.wid=wid


        QTreeWidget.setItemWidget(self, item, col, w)
    def create_item_by_document(self, parent, document):
        if not isinstance(document, dict):
            return
        else:
            #item = QTreeWidgetItem(parent,[""])
            ColumnValue_dict=self.getColumnValue_dict(document)
            # 打印参数名和默认值
            ItemWidge=customTreeItemWidget(parent=parent,treeWidget=\
                self,textList=[ColumnValue_dict['columnA']])
            item = ItemWidge.treeItem
            self.NameToItemDict[ColumnValue_dict['columnB']]=ItemWidge

        valueType = ColumnValue_dict['valueType']
        item.instantTypeCombox.setCurrentText(valueType)
        item.setText(1, ColumnValue_dict['columnB'])
        item.setText(2, ColumnValue_dict['columnC'])

        if item.parent():
            item.setData(2, Qt.AlignmentFlag.AlignCenter, select_icon)
            item.setIcon(2, putin_icon)

        if ColumnValue_dict['columnB'] in self.parentWgt.baseFlatDict:
            if self.parentWgt.baseFlatDict.get(ColumnValue_dict['columnB'])!=\
                    self.parentWgt.presetFlatDict.get(ColumnValue_dict['columnB']):
                item.textWgt.iconPushButton.setIcon(QIcon(curDir+'/icons/reset_chense'))
            elif self.parentWgt.baseFlatDict.get(ColumnValue_dict['columnB'])==\
                    self.parentWgt.presetFlatDict.get(ColumnValue_dict['columnB']):
                item.textWgt.iconPushButton.setIcon(QIcon(curDir+'/icons/reset'))
        elif ColumnValue_dict['columnB'] not in self.parentWgt.baseFlatDict:
            item.textWgt.iconPushButton.setIcon(QIcon(curDir+'/icons/reset_red'))
    
        item.document = document
        for child in ColumnValue_dict['subs']:
            self.create_item_by_document(item, child)
        # if document.get("subs", []) or re.search('_Grp$',document[u'name'],flags=re.I):
        #     item.setIcon(0, group_icon)
        # else:
        #     item.setIcon(0, mesh_icon)
        return item

    

    def addKeyWord(self,item='',keyWord='Sim',ignoreExitZiDuan=False):
        ignoreExitZiDuan=self.parentWgt.ignoreExitZiDuanCKB.isChecked()
        if not item:
            item=self.currentItem()
        itemText=item.text(0)
        result = action.add_suffix(inputStr=itemText, suffix=keyWord,ignoreExitZiDuan=ignoreExitZiDuan)
        if result:
            if keyWord=='GRP' and not item.childCount():
                pass
            else:
                item.setText(0,result)

        for i in range(item.childCount()):
            child_item = item.child(i)
            lprint (child_item)
            self.addKeyWord(child_item, keyWord=keyWord,ignoreExitZiDuan=ignoreExitZiDuan)
        
        
    def _serachAndReplace(self):
        if isMayaEnv():
            self.SearchReplaceAddDialog=PySideLib.SearchReplaceAddDialog(parent=get_maya_window(),treeWidget=self)
        else:
            self.SearchReplaceAddDialog=PySideLib.SearchReplaceAddDialog(treeWidget=self)
        self.SearchReplaceAddDialog.show()

        
    def _set_item_bg(self, item):
        if item is not None and item != self._last_bg_colord_item:
            self._clear_bg_color()
 
            col_cnt = self.columnCount()
            # for ci in range(col_cnt):
            #     item.setBackground(ci, QBrush(QColor(130, 130, 225)))
            # self._last_bg_colord_item = item
            
    def _add_btn(self, item, cmbbox):
        btn = QPushButton('Btn')
        btn.clicked.connect(lambda: self._btn_clicked(item, cmbbox))
        return btn
    
    def _action_cutOrCopy_handler(self, cutOrCopy='cut'):
        try:
            self.cutOrCopy=cutOrCopy
            self._cutOrCopy_item = self.currentItem()
        except Exception as e:
            traceback.print_exc()
            
    def _action_paste_handler(self):
        lprint (self._cutOrCopy_item)
        if self._cutOrCopy_item is None:
            return

        cur_item = self.currentItem()

        # 粘贴item为空
        if cur_item is None:
            return

        # 粘贴item不允许drop
        flags = cur_item.flags().value
        Qt_ItemIsDropEnabled=Qt.ItemFlag.ItemIsDropEnabled

        if flags & Qt_ItemIsDropEnabled == 0:
            return

        new_item = self._cutOrCopy_item.clone()
        cur_item.addChild(new_item)
        cur_item.setExpanded(True)
        
        new_item.document.setdefault("subs", []).append(self._cutOrCopy_item.document)
        cur_item.document.setdefault("subs", []).append(self._cutOrCopy_item.document)
        #self.create_item_by_document(item, document)
        
        if self.cutOrCopy=='cut':
            self._remove_item(self._cutOrCopy_item)
            
        self._cutOrCopy_item = None


            
            
    def getTextBeforeModify(self,item, column): #itemClicked 事件
        self.preText=self.getItemAbsPath(item,column)

    def handle_item_changed(self,  item, column):
        return 
        old_text = self.preText
        new_text = item.text(column)
        lprint("Item changed: ", old_text, " -> ", new_text)
        if old_text != new_text and column==0 :
            if self.parentWgt.synModifyDaGangCKB.isChecked() and self.modifyOutline==True:
                if cmds.objExists(old_text):
                    cmds.rename(old_text,new_text)

    def update(self,jsonFile):
        self.hierarchy = action.load_hierarchy(jsonFile)
        for document in self.hierarchy:
            item = self.create_item_by_document(self, document)
            self.set_expanded(item, True)
        # json文件修改时会运行这个函数,这是需要确定json文件的版本
        # 暂时通过文件名来识别,后面通过json文件中的version key来识别
        self.ensure_jsonFileVersion( jsonFile )
            
    def ensure_jsonFileVersion(self, jsonFile):
        self.json_version = 2.0 if '_back' in jsonFile else 1.0

    
    def getColumnValue_dict(self,document):
        # 获取
        return_date={}
        if self.json_version ==1.0:
            value=document.get("value", "")
            return_date = {'columnA':value,
                         'columnB':document.get("name", ""),
                         'columnC':document.get("zhName", "AA"),
                         'valueType':document.get("valueType", ""),
                         'subs':document.get("subs", [])}
        else:
            name=list(document.keys())[0]
            zhName=document.get(name).get("zhName")
            value=document.get(name).get("value")
            subs=document.get(name).get("subs",[])
            return_date =  {'columnA':value,
                         'columnB':name,
                         'columnC':zhName,
                         'valueType':document.get("valueType", ""),
                         'subs':subs}
        self.flatDict[return_date['columnB']]=\
                [return_date['columnA'],return_date['columnC']]
        return return_date
        
    def _add_combobox(self, item):
        combobox = QComboBox()
        combobox.addItems(['item1', 'item2'])
        return combobox
    
    def _clear_bg_color(self):
        pass
        # 清除之前的背景色
        # if self._last_bg_colord_item is not None:
        #     col_cnt = self.columnCount()
        #     for ci in range(col_cnt):
        #         self._last_bg_colord_item.setBackground(ci, QBrush(QColor(255, 255, 255)))
        #     self._last_bg_colord_item = None
            
    def startDrag(self, supportedActions):
        self.dragging=True
        item = self.currentItem()
        self.dragged_ItemList = self.selectedItems()
        self.dragged_ItemColumnZeroList  = []
        for x in self.dragged_ItemList:
            dragged_widgets=self.itemWidget(x, 0)
            # dragged_widgets.hide()
            lprint (x,dragged_widgets)
            self.setItemWidget(x, 0, dragged_widgets.wid)
            self.dragged_ItemColumnZeroList.append(dragged_widgets)
        super().startDrag(supportedActions)
        
        
        
        mime_data = TreeItemMimeData()
        mime_data.set_drag_data('ItemMimeData', self.dragged_ItemList)
 
        drag = QDrag(self)
 
        # 定义drag事件，自定义的Mimedata传递到dragEnterEvent, dragMoveEvent, dropEvent
        drag.setMimeData(mime_data)
 
        # 记录下垂直滚动条的值，如果拖动没有改变滚动条，则用这个值，否则用改变之后的
        self._vertical_scroll_value = self.verticalScrollBar().value()
        drag_exec =drag.exec if '6' in QT_API else drag.exec_
        if drag_exec(Qt.DropAction.MoveAction) == Qt.DropAction.MoveAction:
            # 新的item已经克隆并添加之后，移除拖动之前的item
            self._remove_item(item)

 
            # 垂直滚动条设置新的值
            self.verticalScrollBar().setValue(self._vertical_scroll_value)
            self._clear_bg_color()
        self.dragging=False
            
    
    def mouseMoveEvent(self, event):
        # 更新鼠标当前所在的索引
        self.currentHoverIndex = self.indexAt(event.pos())
        super(hierarchy_treeWidget, self).mouseMoveEvent(event)
        self.viewport().update()  # 添加这一行以刷新视图
           
    def mousePressEvent(self, event):
        
        super(hierarchy_treeWidget,self).mousePressEvent(event)


        if event.button() == Qt.MouseButton.LeftButton and QApplication.keyboardModifiers() == Qt.KeyboardModifier.ShiftModifier:
            if '6' in QT_API:
                item = self.itemAt(event.position().toPoint())
            else:
                item = self.itemAt(event.pos())

            #index = treeWidget.indexAt(event.pos())
            if isinstance(item, QTreeWidgetItem):
                self.set_expanded(item, item.isExpanded())
            # column = item.column() 
            # lprint (item,column)
        self.sourceItem = self.selectedItems()
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setDragEnabled(True)
            
            #super().mousePressEvent(event)
        else:
            event.ignore()

    def set_expanded(self, item, expanded):
        item.setExpanded(expanded)
        for i in range(item.childCount()):
            self.set_expanded(item.child(i), expanded)

        
    def edit_hierarchy(self, item, i):
        
        lines = [NameLine, LabelLine,LabelLine]
        line = lines[i](self)
        line.setText(item.text(i))
        # line.setFixedHeight(16)
        self.setItemWidget(item, i, line)
        line.setFocus()
        line.selectAll()
        def slot(value):
            # item.document[keys[i]] = value
            self.removeItemWidget(item, i)
            item.setText(i, value)
        line.callBackSignal.connect(slot)
        self.NameToItemDict[item.text(1)]=item
        

    def dragEnterEvent(self, event):
        for i,x in enumerate(self.dragged_ItemList):
            self.setItemWidget(x,0,self.NameToItemDict[x.text(1)])
        super().dragEnterEvent(event)



    def drawRow(self, painter, option, index):
        super(hierarchy_treeWidget, self).drawRow(painter, option, index)

        if not self.dragging:
            return

        # 设置线条颜色和样式
        line_color = QColor(250, 0, 250)  # 紫色
        line_color.setAlpha(218)  # 半透明
        painter.setPen(line_color)

        # 获取拖放指示器位置
        BelowItem = QAbstractItemView.DropIndicatorPosition.BelowItem
        AboveItem = QAbstractItemView.DropIndicatorPosition.AboveItem

        # 如果当前索引与鼠标所在索引相同，则绘制线
        if self.currentHoverIndex == index:
            if self.dropIndicatorPosition() == BelowItem:
                y = option.rect.bottom() - 1
                painter.drawLine(option.rect.left(), y, option.rect.right(), y)
            elif self.dropIndicatorPosition() == AboveItem:
                y = option.rect.top()
                painter.drawLine(option.rect.left(), y, option.rect.right(), y)
            
    def dragMoveEvent(self, event):
        super(hierarchy_treeWidget, self).dragMoveEvent(event)

        # 拖动到边界，自动滚动
        if '6' in QT_API:
            y = event.position().toPoint().y()
        else:
            y = event.pos().y()

        height = self.height()
        if y <= 20:
            self._vertical_scroll_value = self.verticalScrollBar().value() - 1
            self.verticalScrollBar().setValue(self._vertical_scroll_value)
        elif y >= height - 50:
            self._vertical_scroll_value = self.verticalScrollBar().value() + 1
            self.verticalScrollBar().setValue(self._vertical_scroll_value)
            
        if '6' in QT_API:
            current_item = self.itemAt(event.position().toPoint())
        else:
            current_item = self.itemAt(event.pos())


        lprint ('self.sourceItem,current_item',self.sourceItem,current_item,current_item is None)
        
        # 如果拖动目的item为空
        if current_item is None:
            event.ignore()
            return


        # 内部拖拽item
        if event.source() == self:
            
            is_ok = True
            lprint (self.sourceItem,current_item)
            while current_item is not None:
                if current_item == self.sourceItem:
                    is_ok = False
                    break
                current_item = current_item.parent()
            if is_ok:
                self._set_item_bg(self.sourceItem)
                event.setDropAction(Qt.DropAction.CopyAction)
                event.accept()
            else:
                event.ignore()


        # # 外部拖拽进来
        # elif event.mimeData().hasText():
        #     if '6' in QT_API:
        #         item = self.itemAt(event.position().toPoint())
        #     else:
        #         item = self.itemAt(event.pos())
        #     if item is not None:
        #         self._set_item_bg(item)
        #         event.setDropAction(Qt.DropAction.MoveAction)
        #         event.accept()
        #     else:
        #         event.ignore()
        # else:
        #     event.ignore()

            
        # 更新item高亮显示
        # if '6' in QT_API:
        #     index = self.indexAt(event.position().toPoint())
        # else:
        #     index = self.indexAt(event.pos())
        # if index.isValid():
        #     self.setCurrentIndex(index)
            
    def dropEvent(self, event):
        super(hierarchy_treeWidget, self).dropEvent(event)
        try:
            # 内部拖拽item
            if event.source() == self:
                if event.mimeData().hasFormat('ItemMimeData'):
                    mime_data = event.mimeData()
                    item = mime_data.get_drag_data()
                    new_item = item.clone()
                    current_item = self.itemAt(event.position().toPoint())

                    if current_item is None:
                        event.ignore()
                    else:
                        current_item.addChild(new_item)
                        current_item.setExpanded(True)
                        Qt_MoveAction=Qt.DropAction.MoveAction
                        event.setDropAction(Qt_MoveAction)
                        event.accept()
                else:
                    event.ignore()
 
            # 外部拖拽进来
            else:
                multi_file_path = event.mimeData().text()
                file_path_list = multi_file_path.split('\n')
                parent_item = self.itemAt(event.position().toPoint())

                if parent_item is None:
                    return
                else:
                    for file_path in file_path_list:
                        if file_path == '':
                            continue
 
                        file_path = file_path.replace('file:///', '', 1)
                        _, file_name = os.path.split(file_path)
 
                        child = QTreeWidgetItem(parent_item)
                        self._set_testcase_def_param(child, file_name)
                        child.setCheckState(0, Qt.CheckState.Unchecked)
                        # new_flags = child.flags() & Qt.ItemFlag.temIsEditable
                        # new_flags = child.flags() | Qt.ItemFlag.ItemIsEnabled | \
                        #             Qt.ItemFlag.ItemIsUserCheckable | \
                        #             Qt.ItemFlag.temIsEditable | Qt.ItemFlag.ItemIsDragEnabled | \
                        #             Qt.ItemFlag.ItemIsSelectable
                        child.setFlags(new_flags)
 
                        #combobox = self._add_combobox(child)
                        #self.setItemWidget(child, self._index_cmb, combobox)
                        #self.setItemWidget(child, self._index_btn, self._add_btn(child, combobox))
                        parent_item.setExpanded(True)
 
        except Exception as e:
            traceback.print_exc()
        self.dragging = False


    def contextMenuEvent(self, event):
        lprint ('event : ',event)
        item = self.itemAt(event.pos())
        if item is None:
            lprint (u'清除选择')
            self.clearSelection()
            self.setCurrentItem(None)
        self.menu.popup(event.globalPos())#没有这句代码界面会卡死
        if '6' in QT_API:
           self.menu.exec(event.globalPos())
        else:
            self.menu.exec_(event.globalPos())
        
        super(hierarchy_treeWidget, self).contextMenuEvent(event)

    def add_hierarchy(self,item=None,value="value",name="name",icon='',zhName=''):
        lprint ('self.currentItem : ',self.currentItem())
        try:
            document = dict(
                value=value,
                name=name,
                zhName=zhName,
                valueType= "正则表达式",
                children=[] )
            item=self.currentItem()
            lprint (item)
            new_Item=self.create_item_by_document(self.currentItem(),document)
            if  item :
                item.document.setdefault("subs", []).append(document) 
                self.set_expanded(item, True)
            if icon:# 如果有图标，设置图标
                item.setIcon(0, icon)
            else:# 如果没有图标，设置默认图标
                if re.search(r"_Grp",new_Item.text(0),flags=re.I):
                    new_Item.setIcon(0, group_icon)
                else:
                    new_Item.setIcon(0, mesh_icon)
            
        except Exception:
            traceback.print_exc()




    def getItemAbsPath(self,item,column):
        name = "|" + item.text(column)
        while item.parent():
            item = item.parent()
            name = "|" + item.text(column) + name
        return name
    
    def _remove_item(self, item):
        item_parent = item.parent()
        if item_parent is not None:
            item_parent.removeChild(item)
        else:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
            
    def remove_hierarchy(self):
        item = self.currentItem()
        if item is None:
            return
        parent = item.parent()
        if parent is None:
            if item.document in self.hierarchy:
                self.hierarchy.remove(item.document)
            self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        else:
            if item.document in parent.document.setdefault("subs", []):
                parent.document.setdefault("subs", []).remove(item.document)
            parent.takeChild(parent.indexOfChild(item))
            if parent.childCount():
                parent.setIcon(0, group_icon)
            else:
                parent.setIcon(0, mesh_icon)

    def save_hierarchy(self,saveAs=False):
        #path=os.path.dirname(__file__)+'/template/ee.json'
        default_path = os.path.abspath(os.path.dirname(__file__) + "/template/hierarchy.json")
        #default_path = os.path.abspath(__file__ + "/../template")
        if saveAs:
            path, _ = QFileDialog.getSaveFileName(
                self, "save hierarchy", default_path, "json(*.json)")
        else:
            path = self.parentWgt.presetNameWgt.text()
            reply = QMessageBox.question(self, '确认', '你确定要保存设置到当前预设么,覆盖后不能撤回?', 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            # 检查用户的响应
            if reply == QMessageBox.No:
                return
        if not path:
            return

        data = []
        def save_tree_to_json(root, data):
            for i in range(root.childCount()):
                item = root.child(i)
                children = []
                if item.toolTip(0):
                    name=item.toolTip(0)
                    if self.AssetName in item.text(0):
                        name=item.text(0).replace(self.AssetName,'{asset}')
                    else:
                        name=item.text(0)
                else:
                    name=item.text(0)
                valueType = item.instantTypeCombox.currentText()
                description=item.text(1)
                zhName=item.text(2)
                value = name
                name = description
                try:
                    description=description.decode('unicode_escape')
                except:
                    pass
                if self.json_version == 1.0:
                    data.append({'value': value,
                             'expanded':True,
                             'name': description,
                             'valueType':valueType,
                             'zhName': zhName,
                             'condition': 'True',
                             'subs': children,
                             },
                            )
                elif self.json_version == 2.0:
                    data.append({name: {
                                'value': value,
                                'expanded':True,
                                'zhName': zhName,
                                'condition': 'True',
                                'subs': children
                                }}
                                )
                save_tree_to_json(item, children)
        save_tree_to_json(self.invisibleRootItem(), data)
        # path=path[:-5]+'_back.json'
        # os.chmod(path, 0o777)
        lprint (path)
        with codecs.open(path, 'w',encoding='utf8') as file:
            json.dump(data, file, indent=2,ensure_ascii=False)
            
    def save_hierarchy_New(self,saveAs=False):
        #path=os.path.dirname(__file__)+'/template/ee.json'
        default_path = os.path.abspath(os.path.dirname(__file__) + "/template/hierarchy.json")
        #default_path = os.path.abspath(__file__ + "/../template")
        if saveAs:
            path, _ = QFileDialog.getSaveFileName(
                self, "save hierarchy", default_path, "json(*.json)")
        else:
            path = self.parentWgt.presetNameWgt.text()
            reply = QMessageBox.question(self, '确认', '你确定要保存设置到当前预设么,覆盖后不能撤回?', 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            # 检查用户的响应
            if reply == QMessageBox.No:
                return
        if not path:
            return

        data = []
        def save_tree_to_json(root, data):
            for i in range(root.childCount()):
                item = root.child(i)
                children = []
                if item.toolTip(0):
                    name=item.toolTip(0)
                    if self.AssetName in item.text(0):
                        name=item.text(0).replace(self.AssetName,'{asset}')
                    else:
                        name=item.text(0)
                else:
                    name=item.text(0)
                #lprint (root,root.childCount(),name,255)
                description=item.text(1)
                zhName=item.text(2)
                value = name
                name = description
                try:
                    description=description.decode('unicode_escape')
                except:
                    pass
                data.append({'name': {
                             'value': value,
                             'expanded':True,
                             'zhName': zhName,
                             'name': name,
                             'condition': 'True',
                             'subs': children
                             }}
                            )
                save_tree_to_json(item, children)
        save_tree_to_json(self.invisibleRootItem(), data)
        path=path[:-5]+'_back.json'
        # os.chmod(path, 0o777)
        lprint (path)
        with codecs.open(path, 'w',encoding='utf8') as file:
            json.dump(data, file, indent=2,ensure_ascii=False)


    def load_hierarchy(self):
        default_path = os.path.abspath(__file__ + "/../template")
        path, _ = QFileDialog.getOpenFileName(self, "load hierarchy", default_path, "json(*.json)")
        lprint  (path)
        if not path:
            return
        if not os.path.isfile(path):
            return
        with open(path, "r") as f:
            self.hierarchy = action.load_hierarchy(path)
        self.clear()
        for document in self.hierarchy:
            item = self.create_item_by_document(self, document)
            self.set_expanded(item, True)


    def scene_hierarchy(self):
        self.hierarchy = action.get_data_by_scene()
        self.clear()
        for document in self.hierarchy:
            item = self.create_item_by_document(self, document)
            self.set_expanded(item, True)

    @staticmethod
    def select_hierarchy(item):
        lprint ('select_hierarchy')
        if item is None:
            return
        name = "|" + item.text(0)
        while item.parent():
            item = item.parent()
            name = "|" + item.text(0) + name
        lprint (name)

        
    def show_ChildrenInOutline(self,item):
        lprint (item,)
        if not item:
            item = self.currentItem()
        childCount=item.childCount()
        while item.childCount:
            for i in range(childCount):
                child_item=item.child(i)
                lprint (child_item,child_item.text(0))
                itemAbsPath=self.getItemAbsPath(child_item,0)
                lprint (itemAbsPath)
                childObjs=pm.listRelatives(itemAbsPath,ad=True,fullPath=True)
                for childObj in childObjs:
                    childObjName=childObj.split('|')[-1]
                    self.add_hierarchy(item,name=childObjName,label="00*物体",icon=mesh_icon)
                    
    def _btn_clicked(self, item, cmbbox):
        lprint(item.text(0))
        lprint(cmbbox.currentText())



    def get_items_and_widgets_at_level(self, level):
        """
        获取指定层级的所有项目（及其父项目）。

        参数:
        level -- 一个整数，表示要获取的项目的层级（根层级为 0）。

        返回值:
        一个字典，其键为项目的唯一 ID，值为一个包含了项目所有父项目的文本的列表（以自上而下的顺序）。
        """
        # 创建一个 ID 生成器。每次调用 next(id_generator) 都会返回一个新的整数。
        id_generator = itertools.count(1)
        
        # 创建一个字典，用于将 ID 映射到 QTreeWidgetItem 对象。
        self.id_to_item = {}

        # 这是一个内部函数，用于递归地获取树中的所有项目。
        def get_items_recursive(parent_item, current_level):
            items = {}
            for i in range(parent_item.childCount()):
                child_item = parent_item.child(i)
                if current_level == level:
                    parent_items = []
                    current_item = child_item
                    while current_item.parent():
                        current_item = current_item.parent()
                        parent_items.insert(0, current_item)  # 保存当前项目的父项目
                    child_item.id = next(id_generator)  # 为 child_item 分配一个新的 ID
                    self.id_to_item[child_item.id] = child_item  # 将 child_item 的 ID 映射到 child_item
                    items[child_item.id] = parent_items  # 使用 child_item 的 ID 作为键
                else:
                    items.update(get_items_recursive(child_item, current_level + 1))
            return items

        if level == 0:
            items = {}
            for i in range(self.topLevelItemCount()):
                top_level_item = self.topLevelItem(i)
                top_level_item.id = next(id_generator)  # 为 top_level_item 分配一个新的 ID
                self.id_to_item[top_level_item.id] = top_level_item  # 将 top_level_item 的 ID 映射到 top_level_item
                items[top_level_item.id] = []  # 使用 top_level_item 的 ID 作为键
            return items,self.id_to_item
        else:
            return get_items_recursive(self.invisibleRootItem(), 1),self.id_to_item


    def hide_items_with_text_in_list(self, checkbox_state_list):
        # This function checks if all children of a given item are hidden.
        def all_children_hidden(item):
            for i in range(item.childCount()):
                child_item = item.child(i)
                if not child_item.isHidden():
                    return False
            return True

        # This function updates the visibility of the given item and its parents.
        def update_item_visibility(item, hidden):
            item.setHidden(not hidden)

            # If all children are hidden, hide the parent item as well
            parent_item = item.parent()
            if parent_item and all_children_hidden(parent_item):
                parent_item.setHidden(True)
            # If the item is being shown, make sure all its parents are also shown
            
            if  hidden:
                while parent_item:
                    parent_item.setHidden(False)
                    parent_item = parent_item.parent()

        # For each checkbox and state in the checkbox_state_list, update the item visibility accordingly
        for checkbox, state in checkbox_state_list:
            item = getattr(checkbox, 'Wgt', None)
            if item:
                update_item_visibility(item, state)

# 这个代码选择多个层级到另一个组,会丢失第一列的信息
            
            
class LTreeWidget(QWidget):
    def __init__(self,jsonFileList=[],parent=None,headerList=[u'列A',u'列B'],
                columnWidthList=[1000,250,250], baseJsonFile='',*args, **kwargs):
        if sys.executable.endswith('maya.exe'):
            QWidget.__init__(self, QApplication.activeWindow(), Qt.WindowType.Window)
        else:
            super(LTreeWidget,self).__init__()
        self.setStyleSheet(self_qss)
        self.baseJsonFile=baseJsonFile
        self.jsonFileList=jsonFileList
        

        self.setWindowTitle(u"大纲层级命名")
        
        self.MaintopLay= QHBoxLayout()
        self.MaintopLay.setContentsMargins(0,0,0,0)
        self.MainWgt=QWidget()  # 层级面板
        
        self.MainWgtLay = QVBoxLayout()
        
        self.MainWgt.setLayout(self.MainWgtLay)
        if not jsonFileList:
            for jsonDir in [os.path.dirname(__file__) + "/template",]:
                jsonFileList+=[x for x in glob.glob(jsonDir+'/*.json')]
        
        self.baseFlatDict={}
        self.presetFlatDict={}
        self.getFlatDict(self.baseJsonFile,self.baseFlatDict)
        self.getFlatDict(self.jsonFileList[0],self.presetFlatDict)
                
        self.hierarchyWgt = hierarchy_treeWidget(  presetFile=jsonFileList[0],
                    parentWgt=self,
                    ColumnHeaderList=[
                    u'层级(图标A表示是否为常量,图标B橙色表示覆盖默认值,红色表示新加项),',
                                                          u'标识',
                                                          u'中文名称'],
                                        columnWidthList=columnWidthList)
        self.setMinimumWidth(sum(columnWidthList)+200)
        
        
        self.MaintopLay.addWidget(self.filterHierarchyWgt())
        self.MaintopLay.addWidget(self.MainWgt)

        
        
        self.setLayout(self.MaintopLay)
        try:
            self.MayaFileName=cmds.file(q=True, sceneName=True)
        except:
            self.MayaFileName='D:/AA.ma'
            
        self.ShowWindow=True

        #camera_111_222
        self.presetNameWgt=PySideLib.LPathSel(par=self.MainWgtLay,
                                            l_lab=u'  预设文件  ',
                                            DialogCommit=u'预设文件',
                                            fileType="*.json",
                                            buttonName=u'...',
                                            chooseFunc=u'getOpenFileName',
                                            defaultPath=jsonFileList[0])
        self.presetNameWgt.setMaximumHeight(40)
        self.presetNameWgt.widget[0].addItems(jsonFileList)
        self.presetNameWgt.widget[0].currentTextChanged.connect(self.jsonFileChangeFunc)
        
        self.basePresetNameWgt=PySideLib.LPathSel(par=self.MainWgtLay,
                                            l_lab=u'基本预设文件',
                                            DialogCommit=u'基本预设文件',
                                            fileType="*.json",
                                            buttonName=u'...',
                                            chooseFunc=u'getOpenFileName',
                                            defaultPath=self.baseJsonFile)
        self.basePresetNameWgt.setMaximumHeight(40)
        self.basePresetNameWgt.widget[0].addItems(jsonFileList)
        self.basePresetNameWgt.widget[0].currentIndexChanged.connect(self.jsonFileChangeFunc)
        self.basePresetNameWgt.setEnabled(False)
        
        self.ShotFileExampleWgt=PySideLib.complexWidget(
            label='Maya镜头文件示例路径 :',height=100)
        self.AssetFileExampleWgt=PySideLib.complexWidget(
            label='Maya资产文件示例路径 :',height=100)
        self.NameSpaceExampleWgt=PySideLib.complexWidget(
            label='Maya资产文件示例路径 :',height=100)
        self.MainWgtLay.addWidget(self.ShotFileExampleWgt)
        self.MainWgtLay.addWidget(self.AssetFileExampleWgt)
        self.MainWgtLay.addWidget(self.NameSpaceExampleWgt)
        
        
        self.jsonFileChangeFunc()
        
        btnWgt=QWidget()
        btnWgt.setStyleSheet('Background-color:#08ffffff;')
        btnWgtLayout=QHBoxLayout()
        btnWgt.setLayout(btnWgtLayout)

        
        self.ignoreExitZiDuanCKB=QCheckBox(u'忽略已存\n在的字段')
        btnWgtLayout.addWidget(self.ignoreExitZiDuanCKB)
        self.ignoreExitZiDuanCKB.setChecked(True)

        
        self.edit_bastJsonFile_CKB=QCheckBox(u'编辑base\njson文件')
        btnWgtLayout.addWidget(self.edit_bastJsonFile_CKB)
        self.edit_bastJsonFile_CKB.setChecked(False)
        self.edit_bastJsonFile_CKB.clicked.connect(self.edit_bastJsonFile_CKB_func)
        
        self.showActualValue_CKB=QCheckBox(u'显示\n实际值')
        btnWgtLayout.addWidget(self.showActualValue_CKB)
        self.showActualValue_CKB.setChecked(False)
        self.showActualValue_CKB.clicked.connect(self.showActualValue_CKB_func)

        btnWgtLayout.addStretch(100)
        
        self.saveSettingWgt=QPushButton(u'保存配置文件')
        self.saveSettingWgt.clicked.connect(lambda:self.hierarchyWgt.save_hierarchy(saveAs=False))
        btnWgtLayout.addWidget(self.saveSettingWgt,10)
        
        self.saveSettingWgt_New=QPushButton(u'保存配置文件_New')
        self.saveSettingWgt_New.clicked.connect(lambda:self.hierarchyWgt.save_hierarchy_New(saveAs=False))
        btnWgtLayout.addWidget(self.saveSettingWgt_New,10)

        self.saveASSettingWgt=QPushButton(u'另存配置文件')
        self.saveASSettingWgt.clicked.connect(lambda:self.hierarchyWgt.save_hierarchy(saveAs=True))
        btnWgtLayout.addWidget(self.saveASSettingWgt,10)


        helpButton=QPushButton('?')
        helpButton.setStyleSheet('height:5px;background-color:#888a99;')
        btnWgtLayout.addWidget(helpButton,5)
        helpButton.setFixedSize(35,35)

        self.MainWgtLay.addWidget(btnWgt)
        
        
        self.MainWgtLay.addWidget(self.hierarchyWgt)
        #self.resize(600, 850)
        #self.setMinimunSize(600, 850)
        self.setMinimumHeight(900)
    
    class TreeViewNameType(TypedDict):
        regEx: str
        valueType: Literal['正则表达式', '变量']
               
    def parsePath(self,name,path,names={}):
        #checkList=['SkeAniFbxExPath_Sim','Asset_ExName','SeqActorLabel','simAbcExPath']
        #os.environ['Lugwit_Debug']='inspect'
        checkList=['simAbcExPath']
        if name in checkList:
            for x in checkList:
                lprint (x,names.get(x))
            lprint (names,name)
        if path.startswith('content:'):
            return path
        nameToPathDict={'hostName':socket.gethostname()}
        if name in names:
            path=names.get(name)
        def parsePathIterate(name,path,names):
            findAll=re.findall(r'{\w.+?}',path)
            lprint (name,path,findAll)
            for varName in findAll:
                getVal=names.get(varName[1:-1])
                if getVal==None:# 无法获取值从nameToPathDict获取
                    getVal=nameToPathDict.get(varName[1:-1])
                if varName[1:-1]=='AssetType_longName':
                    getVal = self.AssetTypeNameDict.get(names.get('AssetType'))
                if getVal :# 获取值后修改path,并更新nameToPathDict
                    path=path.replace(varName,getVal)

                    nameToPathDict[varName[1:-1]]=getVal

                elif getVal=='':
                    getVal=''
                elif getVal == None: 
                    nameToPathDict[varName[1:-1]]=varName
                    
            return path
        path=parsePathIterate(name,path,names) 
        lprint (path)
        names.update(nameToPathDict)
        findAll=re.findall(r'{\w.+?}',path)

        for _ in findAll:
            if names.get(_[1:-1])==_ or not  names.get(_[1:-1]):
                getVal=os.environ.get(_[1:-1])
                if name=="RecordProcedureFile":
                    lprint (getVal)
                if getVal:
                    path=path.replace(_,getVal)
        lprint (names,path)
        try:
            path=path.format(**names)
            path=path.replace('\\','/')
            path=path.replace('_.','.')
            temp=[]
            for _ in  path.split('/'):#"G:/WXXJDGD/13.CFX/ep001/ep001_sc001_shot0150/ep001_sc001_shot0150_C_LiWuWang_{nameSpaceIndex}_cfx.abc"
                _=_.rstrip('_')# C_LiWuWang_{nameSpaceIndex}  cfx.abc"
                temp.append(_) 
            path='/'.join(temp)
            path = path.replace('__','_')
        except:
            path=''
            lprint (traceback.format_exc())

        nameToPathDict[name]=path
        lprint (path)
        #os.environ['Lugwit_Debug']='noprint'
        return path
    
    def get_infoFromExConfigJsonFile_oriDict(self):
        infoFromExConfigJsonFile_oriDict={}
        def iterate_items(self):
            iterator = QTreeWidgetItemIterator(self.hierarchyWgt)
            while iterator.value():
                item = iterator.value()
                cloumnA,cloumnB=item.text(0),item.text(1)
                item.oriValue=cloumnA
                instantType=item.instantTypeCombox.currentText()
                infoFromExConfigJsonFile_oriDict\
                        .setdefault(cloumnB,
                            {'regEx':cloumnA,'valueType':instantType})
                iterator += 1
        iterate_items(self)
        return infoFromExConfigJsonFile_oriDict
    
    def get_infoFromMayaFilePath(self,shotFile='',assetFile='',nameSpace='dsadsa_Rig1'):
        infoFromExConfigJsonFile_oriDict=self.get_infoFromExConfigJsonFile_oriDict()
        ConstantVarDict=\
            self.getConstantVarFromTreeWidget(infoFromExConfigJsonFile_oriDict)
        self.AssetTypeNameDict={ ConstantVarDict.get('character_KeyWord'):
                            ConstantVarDict.get('character_LongKeyWord'),
                            ConstantVarDict.get('prop_KeyWord'):
                            ConstantVarDict.get('prop_LongKeyWord'),
                            ConstantVarDict.get('scene_KeyWord'):
                            ConstantVarDict.get('scene_LongKeyWord'),
                            ConstantVarDict.get('rigCam_KeyWord'):
                            ConstantVarDict.get('rigCam_LongKeyWord'),
                        }
        lprint (ConstantVarDict)
        infoFromMayaFilePath={}#if item.instantTypeCombox.currentText()=='常量':
        infoFromMayaFilePathA={}
        infoFromMayaFilePathB={}

        if shotFile:
            infoFromMayaFilePathA = gl.getInfoFromMayaFilePath(
                            shotFile,
                            getInfofromFileName=False,isAssetOrShotFile=1,
                            nameSpace=nameSpace,
                            **infoFromExConfigJsonFile_oriDict)


        if assetFile:
            infoFromMayaFilePathB =gl.getInfoFromMayaFilePath(
                            assetFile,
                            getInfofromFileName=False,isAssetOrShotFile=0,
                            nameSpace=nameSpace,
                            **infoFromExConfigJsonFile_oriDict)
            lprint  (infoFromMayaFilePathB.get('Asset_ExName'))

        infoFromMayaFilePath = infoFromMayaFilePathA or infoFromMayaFilePathB
        for key,val in infoFromMayaFilePath.items():
            valA=infoFromMayaFilePathA.get(key,'')
            if valA :
                infoFromMayaFilePath[key]=valA
            else:
                infoFromMayaFilePath[key]=infoFromMayaFilePathB.get(key,'')
        # infoFromMayaFilePath= {k: infoFromMayaFilePath[k] for k in sorted(infoFromMayaFilePath)}
        lprint (infoFromMayaFilePath.get('AssetFileBaseName'),nameSpace,infoFromMayaFilePath.get('Asset_ExName'))

        infoFromMayaFilePath.update(
            {'RefFileDir':os.path.dirname(assetFile)})
        return infoFromMayaFilePath
    
    def getConstantVarFromTreeWidget(self,infoFromExConfigJsonFile_oriDict:dict):
        var:Literal['是一个字典,key分别是regEx和valueType,valueType为正则表达式或者变量']
        constantdict={}
        for key,var in infoFromExConfigJsonFile_oriDict.items():
            if var['valueType']=='常量':
                constantdict[key]=var['regEx']
        return constantdict
            
        
    def showActualValue_CKB_func(self,val=None,assetFile='',shotFile='',nameSpace=''):
        # 设置实际值
        lprint (assetFile,shotFile)
        if not assetFile:
            assetFile=self.AssetFileExampleWgt.widget.text().replace('\\','/')
            lprint (assetFile)
        if not shotFile:
            shotFile=self.ShotFileExampleWgt.widget.text().replace('\\','/')
        if not nameSpace:
            nameSpace=self.NameSpaceExampleWgt.widget.text()
        lprint (assetFile,shotFile,nameSpace)
        ActualValue_CKB_val=self.showActualValue_CKB.isChecked()
        self.saveSettingWgt.setEnabled(not ActualValue_CKB_val)
        
        if ActualValue_CKB_val:
            infoFromMayaFilePath=self.get_infoFromMayaFilePath(
                assetFile=assetFile,
                shotFile=shotFile,
                nameSpace=nameSpace)
            infoFromMayaFilePath.update({'nameSpace':nameSpace})
            def iterate_items(self):
                iterator = QTreeWidgetItemIterator(self.hierarchyWgt)
                while iterator.value():
                    item = iterator.value()
                    cloumnA,cloumnB,cloumnC=item.text(0),item.text(1),item.text(2)
                    #if cloumnB in ('ProjectName' , 'nameSpaceIndex' , 'SkeAniFbxExPath_Sim','Asset_ExName','SeqActorLabel'):
                    path = self.parsePath(cloumnB,cloumnA,infoFromMayaFilePath)
                    # if path.lower().startswith('g:'):
                    #     path=path.replace('G:','H:')
                    lprint(cloumnB,cloumnA,path)
                    item.actualValue=path
                    item.setText(0,path)
                    iterator += 1
            iterate_items(self)
        elif self.showActualValue_CKB.isChecked()==False:# 显示原始值
            def iterate_items(self):
                iterator = QTreeWidgetItemIterator(self.hierarchyWgt)
                while iterator.value():
                    item = iterator.value()
                    if hasattr(item,'oriValue'):
                        item.setText(0,item.oriValue)
                    iterator += 1
            iterate_items(self) 

        

    def edit_bastJsonFile_CKB_func(self):
        if self.edit_bastJsonFile_CKB.isChecked():
            self.before_edit_jsonFile=\
                self.presetNameWgt.widget[0].currentText()
            self.presetNameWgt.widget[0].setCurrentText(self.baseJsonFile)
        else:
            self.presetNameWgt.widget[0].setCurrentText(self.before_edit_jsonFile)
    def ensure_jsonFileVersion(self, jsonFile):
        lprint (jsonFile)
        self.json_version = 2.0 if '_back' in jsonFile else 1.0
        
    def getFlatDict(self,baseJsonFile,processDict):
        self.ensure_jsonFileVersion(baseJsonFile)
        with codecs.open(baseJsonFile, 'r', 'utf-8') as f:
            baseJsonData=json.load(f)
        def getColumnValue_dict(document):
            return_date=[]
            if self.json_version ==1.0:
                value=document.get("value", "")
                name=document.get("name", "")
                zhName=document.get("zhName", "")
                subs=document.get("subs", [])
                return_date = [ value,
                                name,
                                zhName,
                                subs]
            else:
                name=list(document.keys())[0]
                zhName=document.get(name).get("zhName")
                value=document.get(name).get("value")
                subs=document.get(name).get("subs",[])
                return_date = [ value,
                                name,
                                zhName,
                                subs]
            processDict[return_date[1]]=[return_date[0],return_date[2]]
            
            if isinstance(subs ,list):
                for x in subs:
                    getColumnValue_dict(x)
            elif isinstance(subs,dict):
                    getColumnValue_dict(subs)

        for x in baseJsonData:
            getColumnValue_dict(x)
        
    def mergeWithbaseJsonFile(self):
        self.mergerJsonFile=self.presetNameWgt.widget[0].currentText()
        with codecs.open(self.mergerJsonFile,'r',encoding='utf8') as f:
            # 读取预设json文件的内容
            read=f.read()
            if read:
                mergeJsonData = json.loads(read)
            else:
                mergeJsonData = {}
        #lprint (self.mergerJsonFile,mergeJsonData)
        if self.baseJsonFile:
            if self.presetNameWgt.widget[0].currentText!=self.baseJsonFile:
                with codecs.open(self.baseJsonFile,'r',encoding='utf8') as f:
                    content_base_configFile_data = json.load(f) 

            merged_dict = l_mergeData.merge_list(
                        content_base_configFile_data
                        , mergeJsonData)
            self.mergerJsonFile='{}_{}_mergeJsonData.json'.format(tempDir,time.time())
            with codecs.open(self.mergerJsonFile,'w',encoding='utf8') as f:
                json.dump(merged_dict,f,ensure_ascii=False,indent=4)
                
        self.MainWgtLay.setSpacing(3)

            
            
    def filterHierarchyWgt(self,showFilterHierarchyWgt=False):
        wgt=QWidget()
        #wgt.setVisible(False)
        wgt.setFixedWidth(110)
        wgt.setObjectName('filterHierarchyWgt')
        lay=QVBoxLayout()
        wgt.setLayout(lay)
        filterDisplay=QHBoxLayout()
        refreshBtn=QPushButton(text=u'刷\n新')
        lay.addWidget(refreshBtn)
        if showFilterHierarchyWgt:
            lay.addWidget(QLabel(u'过滤显示'))
            selLayout=QHBoxLayout()
            lay.addLayout(selLayout)
            selLayout.addWidget(QPushButton(text=u'全选'))
            selLayout.addWidget(QPushButton(text=u'反选'))
            
            filterDict,id_to_item= self.hierarchyWgt.get_items_and_widgets_at_level( 4 )

            self.filterBtnGrp=QButtonGroup()
            self.filterBtnGrp.setExclusive(False)
            parent_levelList=[]
        
            for key,val in filterDict.items():
                lprint ('key',key)
                lprint ('val',val)
                key=id_to_item[key]
                lprint ('key',key)
                levelistB_Wgt=val[-2]
                tt=levelistB_Wgt.text(0)
                
                label=key.text(1)
                qh=QHBoxLayout()
                ckb=QCheckBox(label)
                ckb.setChecked(True)
                ckb.stateChanged.connect(partial(self.filterCkbChangeCommand,ckb))
                setattr(ckb,'Wgt',key)
                setattr(ckb,'parent',val[-2])
                self.filterBtnGrp.addButton(ckb)
                
                qh.addWidget(ckb,10)
                fbtn=QPushButton('F')
                fbtn.setFixedSize(15,15)
                fbtn.setStyleSheet("QPushButton { padding: 0; }")
                qh.addWidget(fbtn,1)
                qh.setContentsMargins(0,0,0,0)
                if tt not in parent_levelList:
                    setattr(self,tt+'_GB',QGroupBox(tt))
                    setattr(self,tt+'_Lay',QVBoxLayout())
                    getattr(self,tt+'_GB').setLayout(getattr(self,tt+'_Lay'))
                    lay.addWidget(getattr(self,tt+'_GB'))
                    parent_levelList.append(tt)
                    getattr(self,tt+'_Lay').setContentsMargins(0,0,0,0)

                getattr(self,tt+'_Lay').addLayout(qh)
                fbtn.clicked.connect(partial(self.highDisItem,key))
            
            
        lay.addStretch(20)
        wgt.setStyleSheet('''#filterHierarchyWgt{
                        Background-color:#15acacac;
                        border: 2px solid #15c3c3c3;
                        }''')
        return wgt
    
    def highDisItem(self,key):
        
        self.hierarchyWgt.scrollToItem(key, self.hierarchyWgt.PositionAtTop)
        def unhighlight_item(item, column):
            if item.background(column) != Qt.transparent:
                item.setBackground(column, Qt.transparent)
            for i in range(item.childCount()):
                unhighlight_item(item.child(i), column)
        # 取消所有项的高亮显示
        if hasattr(self,'highlightItem'):
            for item in self.highlightItem:
                unhighlight_item(item, 0)
        self.highlightItem=[]
        # 更改特定项的背景颜色
        highlight_color = QColor(255, 255, 0,10)  # 黄色
        
        def highlight_item(item, column, color):
            item.setBackgroundColor(column, color)
            self.highlightItem.append(item)
            for i in range(item.childCount()):
                highlight_item(item.child(i), column, color)
        highlight_item(key,0,highlight_color)
            
            
    def closeEvent(self, event):
        lprint("Window is closing...")
        # global hierarchyMainwindowBx
        #   del hierarchyMainwindowB
        # hierarchyFromExcelwin.destroy() 
        
    def upToP4_Func(self):
        self.hierarchyWgt.show_ChildrenInOutline(self.hierarchyWgt.invisibleRootItem())
    
    def jsonFileChangeFunc(self):
        self.hierarchyWgt.clear()
        self.mergeWithbaseJsonFile()
        self.hierarchyWgt.update(self.mergerJsonFile)
        MayaAssetFile=self.hierarchyWgt.flatDict.get("MayaAssetFile",'D:/aa.aa')[0]
        MayaShotFile=self.hierarchyWgt.flatDict.get("MayaShotFile",'D:/aa.aa')[0]
        exampleNameSpace=self.hierarchyWgt.flatDict.get("exampleNameSpace",'sada_Rig1')[0]
        self.AssetFileExampleWgt.widget.setText(MayaAssetFile)
        self.ShotFileExampleWgt.widget.setText(MayaShotFile)
        self.NameSpaceExampleWgt.widget.setText(exampleNameSpace)
        
    def add_hierarchyFromExcel_Func(self):
        if not hasattr(self, 'hierarchyFromExcelwin'):
            self.hierarchyFromExcelwin=hierarchy_QTableWidget(self)
            self.MaintopLay.addWidget(self.hierarchyFromExcelwin)
            self.hierarchyFromExcelwin.setFixedWidth(500)
        if self.hierarchyFromExcelwin.isVisible():
            self.hierarchyFromExcelwin.setVisible(False)
        else:
            self.hierarchyFromExcelwin.setVisible(True)
        self.adjustSize()
        self.setFixedHeight(900)

        
    def refreshNodeExistState_Func(self):
        pass
    
    def doShake(self):
        self.doShakeWindow(self)

    # 下面这个方法可以做成这样的封装给任何控件
    def doShakeWindow(self, target):
        """窗口抖动动画
        :param target:        目标控件
        """
        if hasattr(target, '_shake_animation'):
            # 如果已经有该对象则跳过
            return

        animation = QPropertyAnimation(target, b'pos', target)
        target._shake_animation = animation
        animation.finished.connect(lambda: delattr(target, '_shake_animation'))

        pos = target.pos()
        x, y = pos.x(), pos.y()

        animation.setDuration(200)
        animation.setLoopCount(2)
        animation.setKeyValueAt(0, QPoint(x, y))
        animation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
        animation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
        animation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
        animation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
        animation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
        animation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
        animation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
        animation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
        animation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
        animation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
        animation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
        animation.setEndValue(QPoint(x, y))

        animation.start(animation.DeleteWhenStopped)

    def filterCkbChangeCommand(self,ckb,state):
        self.hierarchyWgt.hide_items_with_text_in_list([(ckb,state)])
        
        
class hierarchy_QTableWidget(QWidget):
    def __init__(self,parentWidget=''):
        #super(hierarchy_QTableWidget,self).__init__(QApplication.activeWindow(),Qt.Window)
        super(hierarchy_QTableWidget,self).__init__()
        self.parentWidget=parentWidget
        self.hierarchyWgt=parentWidget.hierarchyWgt
        self.topLay=QHBoxLayout()
        self.setLayout(self.topLay)
        self.Left1_HLay=QVBoxLayout()
        self.Left2_HLay=QVBoxLayout()
        self.topLay.addLayout(self.Left1_HLay)
        self.topLay.addLayout(self.Left2_HLay)
        self.resize(500, q00)
        self.typeBtnGroup()
        self.excel()
    
    
    
    def typeBtnGroup(self):
        btnWgtLayout=QVBoxLayout()
        btnWgtLayout.setContentsMargins(0,0,0,0)
        self.Left1_HLay.addLayout(btnWgtLayout)

        DirectionWgtGroupBox = QGroupBox(u'方向选择')
        Direction_bntLayout=QVBoxLayout()
        Direction_bntLayout.setContentsMargins(0,0,0,0)
        DirectionWgtGroupBox.setLayout(Direction_bntLayout)
        btnWgtLayout.addWidget(DirectionWgtGroupBox)
        
        Node_DirectionWgtA=QRadioButton(u'自动')
        Node_DirectionWgtA.setToolTip(u'根据选择的节点是否包含"_L|_R"关键字决定方向')
        Node_DirectionWgtA.setChecked(1)
        Node_DirectionWgtB=QRadioButton(u'无')
        Node_DirectionWgtC=QRadioButton(u'左')
        Node_DirectionWgtD=QRadioButton(u'右')
        self.Node_DirectionGrp=QButtonGroup(self)
        self.Node_DirectionGrp.addButton(Node_DirectionWgtA)
        self.Node_DirectionGrp.addButton(Node_DirectionWgtB)
        self.Node_DirectionGrp.addButton(Node_DirectionWgtC)
        self.Node_DirectionGrp.addButton(Node_DirectionWgtD)
        Direction_bntLayout.addWidget(Node_DirectionWgtA)
        Direction_bntLayout.addWidget(Node_DirectionWgtB)
        Direction_bntLayout.addWidget(Node_DirectionWgtC)
        Direction_bntLayout.addWidget(Node_DirectionWgtD)
        
        createPosWgtGroupBox = QGroupBox(u'创建位置')
        createPos_bntLayout=QVBoxLayout()
        createPos_bntLayout.setContentsMargins(0,0,0,0)
        createPosWgtGroupBox.setLayout(createPos_bntLayout)
        btnWgtLayout.addWidget(createPosWgtGroupBox)
        
        Node_createPosWgtA=QRadioButton(u'替换')
        Node_createPosWgtB=QRadioButton(u'下一层级')
        Node_createPosWgtB.setChecked(1)

        self.Node_createPosGrp=QButtonGroup(self)
        self.Node_createPosGrp.addButton(Node_createPosWgtA)
        self.Node_createPosGrp.addButton(Node_createPosWgtB)

        createPos_bntLayout.addWidget(Node_createPosWgtA)
        createPos_bntLayout.addWidget(Node_createPosWgtB)
        
        self.assetTypeWgtGroupBox = QGroupBox(u'资产类型')
        assetType_bntLayout=QVBoxLayout()
        assetType_bntLayout.setContentsMargins(0,0,0,0)
        self.assetTypeWgtGroupBox.setLayout(assetType_bntLayout)
        self.Left1_HLay.addWidget(self.assetTypeWgtGroupBox)
        
        Node_assetTypeWgtA=QRadioButton(u'角色')
        Node_assetTypeWgtA.setChecked(1)
        Node_assetTypeWgtB=QRadioButton(u'道具')
        Node_assetTypeWgtC=QRadioButton(u'场景')

        self.Node_assetTypeGrp=QButtonGroup(self)
        self.Node_assetTypeGrp.addButton(Node_assetTypeWgtA)
        self.Node_assetTypeGrp.addButton(Node_assetTypeWgtB)
        self.Node_assetTypeGrp.addButton(Node_assetTypeWgtC)
        self.Node_assetTypeGrp.buttonToggled.connect(self.assetTypeChange)

        assetType_bntLayout.addWidget(Node_assetTypeWgtA)
        assetType_bntLayout.addWidget(Node_assetTypeWgtB)
        assetType_bntLayout.addWidget(Node_assetTypeWgtC)
        
        editExcelBtn=QPushButton(u'编辑excel表格')
        self.Left1_HLay.addWidget(editExcelBtn)
        editExcelBtn.clicked.connect(lambda:os.startfile(u'A:/TD/Template/Model/Outline/资产分组命名规范索引表.xls'))
        
        self.Left1_HLay.addStretch(2)

    def assetTypeChange(self):
        text=self.Node_assetTypeGrp.checkedButton().text()
        rangeDict={u'角色':[1,2],u'道具':[3,4],u'场景':[5,6]}
        self.excel(init=0,readRowList=rangeDict[text])
        lprint (text)
        
    def excel(self,init=1,readRowList=[1,2]):
        hierarchyNameDict=self.getHierarchyNameDict(readRowList)
        row1,row2=hierarchyNameDict
        columnAmount=2
        if init:
            self.nstable = QTableWidget(300, columnAmount)
            self.nstable.setHorizontalHeaderLabels([u'英文',u'中文'])
            self.Left2_HLay.addWidget(self.nstable)
            self.nstable.doubleClicked.connect(self.setCellContentFunc)
        else:
            self.nstable.clear()
            
        
        for  i in range(300-1):
            if i>300:
                break
            self.nstable.verticalHeader().resizeSection(i, 18)
            # lockItem= QTableWidgetItem()
            # #lockItem.setIcon(QIcon(group_icon if ))
            # self.nstable.setVerticalHeaderItem(i,lockItem)
            for j in range(columnAmount):
                self.nstable.horizontalHeader().resizeSection(j, 173)
                widgetName=hierarchyNameDict[j][i+1]
                widget= QTableWidgetItem(widgetName)
                if j%2==0 and widgetName:
                    widget.setIcon(group_icon if re.search('_Grp$',widgetName,flags=re.I)  else mesh_icon)
                self.nstable.setItem(i, j, widget)
                try:
                    widget.setFlags( Qt.ItemFlag.ItemIsEnabled)
                except:
                    pass

        try:
            self.setWindowModality(Qt.WindowModality.NonModal)
        except:
            pass
        
    def getHierarchyNameDict(self,readRowList=[1,2]):
        HierarchyNameDict=readExcel.readHierarchyNameDict(readRowList)
        lprint (HierarchyNameDict)
        return HierarchyNameDict
    
    # 双击时设置父级单元格内容
    def setCellContentFunc(self,ModelIndex):
        itemRowIndex=ModelIndex.row()
        lprint (itemRowIndex)
        row0Text=self.nstable.item(itemRowIndex,0).text()
        row1Text=self.nstable.item(itemRowIndex,1).text()
        row2Text=self.nstable.item(itemRowIndex,2).text()
        parWinSelectedItems=self.hierarchyWgt.selectedItems()
        if parWinSelectedItems:
            parWinSelectedItem=parWinSelectedItems[0]
            self.hierarchyWgt.preText=self.hierarchyWgt.getItemAbsPath(parWinSelectedItem,0)
            parWinSelectedItem_text=parWinSelectedItem.text(0)

            Direction_text=self.Node_DirectionGrp.checkedButton().text()
            if Direction_text==u'自动':
                search_direct=re.search('_L|_R', parWinSelectedItem_text,flags=re.I)
                if search_direct:
                    Direction_text=search_direct.group()
                else:
                    Direction_text=u'无'
            lprint (Direction_text)
            Direction_text_Dict={u'左':'_L',u'右':'_R',u'无':'','_L':'_L','_R':'_R'}
            direction=Direction_text_Dict[Direction_text]
            row0Text=re.sub('_Grp','{}_Grp'.format(direction),row0Text,flags=re.I) if re.search('_Grp',row0Text,flags=re.I) else row0Text+direction
            
            Node_createPos_text=self.Node_createPosGrp.checkedButton().text()
            icon=self.nstable.item(itemRowIndex,0).icon()
            if Node_createPos_text==u'替换':
                parWinSelectedItem.setText(0, row0Text)
                parWinSelectedItem.setText(1, row1Text)
                parWinSelectedItem.setText(2, row2Text)
                parWinSelectedItem.setIcon(0, icon)
                cmds.warning(parWinSelectedItem)
            elif Node_createPos_text==u'下一层级':
                self.hierarchyWgt.add_hierarchy(parWinSelectedItem,name=row0Text,label=row1Text,zhName=row2Text)
        # cmds.warning(itemRowIndex)


def get_maya_window():
    # get the maya main window as a QMainWindow instance
    import shiboken2
    win = omui.MQtUtil_mainWindow()
    ptr = shiboken2.wrapInstance(long(win), QWidget)
    return ptr

window = None


def show_Main(*args): 
    if sys.executable.endswith('maya.exe'):
        lprint (sys.executable)
    else:
        lprint ('---------')
        app = QApplication(sys.argv)
    
    if 'hierarchyMainwindowB' in globals() and globals()['hierarchyMainwindowB'].ShowWindow:
        lprint(globals()['hierarchyMainwindowB'])
        win=globals()['hierarchyMainwindowB']
        try:
            if win.isMinimized() or win.isHidden():
                globals()['hierarchyMainwindowB'].showNormal()
            else:
                globals()['hierarchyMainwindowB'].doShake()
        except:
            lprint (u'创建窗口hierarchyMainwindowB')
            global hierarchyMainwindowB
            hierarchyMainwindowB = LTreeWidget(
                            jsonFileList=[curDir+'/base.json'],
                            baseJsonFile=curDir+'/base.json')
            if hierarchyMainwindowB.ShowWindow:
                globals()['hierarchyMainwindowB'].show()
            else:
                lprint (u'删除{}'.format('hierarchyMainwindowB'))
            del globals()['hierarchyMainwindowB']
    else:
        lprint (u'创建窗口hierarchyMainwindowB')
        
        # hierarchyMainwindowB = LTreeWidget(
        #                     jsonFileList=[curDir+'/Cosmos_Wartale.json'],
        #                     baseJsonFile=curDir+'/base.json')
        hierarchyMainwindowB = LTreeWidget(
                    jsonFileList=[r"A:\TD\RenderFarm\MayaToUE\data\LXZ.json"],
                    baseJsonFile=r"A:\TD\RenderFarm\MayaToUE\data\base.json",)

        
        if hierarchyMainwindowB.ShowWindow:
            hierarchyMainwindowB.setWindowFlags(
            hierarchyMainwindowB.windowFlags()
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint  
            | Qt.WindowType.WindowMaximizeButtonHint
        )
            globals()['hierarchyMainwindowB'].show()
        else:
            lprint (u'删除{}'.format('hierarchyMainwindowB'))
        del globals()['hierarchyMainwindowB']


    if not sys.executable.endswith('maya.exe'):
        lprint ('QT_API : ',QT_API)
        if QT_API=='PyQt6':
            sys.exit(app.exec())
        else:
            app.exec_()








        
def show_hierarchy_QTableWidget_Win(*args):
    if sys.executable.endswith('maya.exe'):
        pass
    else:
        pass
    if 'hierarchy_QTableWidget_win' not in globals():
        global hierarchy_QTableWidget_win
        hierarchy_QTableWidget_win=hierarchy_QTableWidget()
        hierarchy_QTableWidget_win.show()
    if not sys.executable.endswith('maya.exe'):
        
        sys.exit(app.exec_())

lprint (__name__)
if __name__ == '__main__':
    #show_hierarchy_QTableWidget_Win()
    show_Main()
    
'''
import sys
sys.path.append(r'D:\TD_Depot\TD\hyws\maya\scripts\fun')
import mod.hierarchy.ui as ui
reload(ui)
ui.show_Main()

'''
