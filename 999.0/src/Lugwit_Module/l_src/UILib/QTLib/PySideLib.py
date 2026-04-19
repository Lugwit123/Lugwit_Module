# -*- coding: utf8
#添加模块所在路径
from email import iterators
import os,re,sys,codecs
import os,copy
if os.environ.get('pythonpath'):
    sys.path.append(os.environ['pythonpath'])
Lugwit_ModulePath=re.search(r'.*Lugwit_Module',__file__,flags=re.I).group()
curDir =  os.path.dirname(__file__)

l_srcDir = re.search(r'.*l_src',__file__,flags=re.I).group()
sys.path.append(l_srcDir)

from usualFunc import lprint
from getExecuteExe import isMayaEnv

if isMayaEnv():
    QT_API='PySide2'
QT_API=os.environ.get('QT_API')


if not QT_API:
    QT_API='PySide2'
if 'maya' in sys.executable:
    QT_API='PySide2'

if isMayaEnv():
    from PySide2.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
        QStatusBar, QSizePolicy, QDialog, QSpacerItem,QLabel,QWidget,QComboBox,QProgressDialog,QSpinBox,
        QCheckBox,QRadioButton,QGroupBox,QButtonGroup)
    from PySide2.QtCore import Qt, QTimer, QEvent, QCoreApplication, QRect,QPoint,Signal,QThread

    from PySide2.QtCore import Qt, QMimeData, QEvent, QPoint,QObject
    from PySide2.QtGui import QDragEnterEvent, QDropEvent

    from functools import partial
else:
    sys.path.append(r'd:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib\Lugwit_Module\l_src\l_qtpy{}'.format(sys.version_info.major))

    from qtpy.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
        QStatusBar, QSizePolicy, QDialog, QSpacerItem,QLabel,QWidget,QComboBox,QProgressDialog,QSpinBox,
        QCheckBox,QRadioButton,QGroupBox,QButtonGroup)
    from qtpy.QtCore import Qt, QTimer, QEvent, QCoreApplication, QRect,QPoint,Signal,QThread

    from qtpy.QtCore import Qt, QMimeData, QEvent, QPoint,QObject
    from qtpy.QtGui import QDragEnterEvent, QDropEvent

    from functools import partial


    
def on_press(key):
    global checkValue, hasKeyPress
    hasKeyPress = 1

    if 'Key.ctrl' in str(key):
        checkValue = 0
    elif 'Key.shift' in str(key):
        checkValue = 1
        
def on_release(key):
    # global checkValue
    # checkValue=0
    pass
        
checkValue = 0
hasKeyPress = 0


            

def qss_StyleTemplate(qss_file_name=curDir+r'\QSS\self.qss'):
    with codecs.open(qss_file_name, 'r',  encoding='utf-8') as file:
        return file.read()


def chooseFile(par='',FieldPathWidget='',chooseFunc='getOpenFileName',DialogCommit=u"DialogCommit",stDir=r"d:/",fileType="(*.abc)"):
    
    if os.path.exists(FieldPathWidget. currentText() ):
        stDir=FieldPathWidget.currentText() 
    stDir=stDir.replace('\\','/')
    if 'File' in chooseFunc:
        try:
            path=eval(u'QFileDialog.{} (par,r"{}",r"{}",r"{}")[0]'.format(chooseFunc,DialogCommit,stDir,fileType))
        except:
            path=eval(u'QFileDialog.{} (par,r"{}",r"{}",r"{}")[0]'.format(chooseFunc,DialogCommit,'D:/aa.jpg',fileType))
    else:
        try:
            path=eval('QFileDialog.{} (par,r"{}",r"{}")'.format(chooseFunc,DialogCommit,stDir))
        except:
            stDir=stDir[:3]
            path=eval('QFileDialog.{} (par,r"{}",r"{}")'.format(chooseFunc,DialogCommit,stDir))
        
    path=os.path.normpath(path)
    if path:
        FieldPathWidget.insertItems(0,[path])
        FieldPathWidget.setCurrentText(path)
    return path
   
    
def Lbutton(label,  c):
    button = QPushButton(label)
    button.clicked.connect(c)
    return button

class LTextGrp(QWidget):
    def __init__(self,par='',textList={'labA':[1,10],'lab_B':[2]}):
        super(LTextGrp, self).__init__()
        self.lay=QHBoxLayout()
        name=locals()
        self.widgetList=[]
        for i,ele in enumerate(textList.items()):
            self.widgetLabel=QLabel(ele[0])
            self.lay.addWidget(self.widgetLabel)
            val=ele[1]
            if not isinstance(ele[1],list):
                val=[ele[1]] 
            for _val in val:
                FieldPathWidget=QLineEdit(str(_val))
                self.lay.addWidget(FieldPathWidget) 
                self.setLayout(self.lay)
                self.widgetList.append(FieldPathWidget)
        self.lay.setContentsMargins(0, 0,0,0)
    def setText(self,text):
        self.FieldPathWidget.setText(text)
    def get_widgetList(self):
        return self.widgetList

class complexWidget(QWidget):
    def __init__(self,layout=QHBoxLayout,
                 label='label',
                 widget=QLineEdit,
                 ratio=(1,10),
                 spaceing=5,
                 height=20,
                 Margins=(0, 3,0,3)):
        super(type(self), self).__init__(parent=None)
        self.lay=layout()
        self.lay.setContentsMargins(*Margins)
        self.labelWidget=QLabel(label)
        self.widget=widget()
        self.lay.addWidget(self.labelWidget,ratio[0])
        self.lay.addWidget(self.widget,ratio[1])
        self.labelWidget.setMaximumHeight(height)
        self.widget.setMaximumHeight(height)
        
        self.setLayout(self.lay)
        
     
class LQHVGrp(QWidget):
    '''
    字典参数依次为widget类型,(QCheckBox,标签,默认值),{'方法':'值'},(空白,Lable伸缩因子,widget伸缩因子),groupBox='Label')
    字典参数依次为widget类型,标签,(layout前空白,widget后添加空白,Lable伸缩因子,widget伸缩因子)
    'LabelName'--可以是一个字符串,也可以是一个元祖,(QCheckBox,'命名规则',1),
    par 为父窗口 ,为一个列表,[父窗口,比例]
    '''
    def __init__(self,btnGrp='',btnGrpCheckable=0,widgetList=[(QComboBox,'LabelName',{u'方法':u'值'},(1,0,0,0))],
                par='',exchangeLabelAndWidget=False,layout=QHBoxLayout,groupBox=0,Spacing=0,contentsMargins=(0,0,0,0,),
                TextSelectableByMouse=1,Editable=1,ReadOnly=1,addCheckBox=0,checkBoxText='checkBoxText',checkBoxChecked=0):
        super(LQHVGrp, self).__init__()
        if not isinstance(par,list):
            par=[par,1]

        self.groupBox=[]
        self.widgetList=widgetList
        self.checkBoxWidgetList=[]
        
        # 每一种组件如何获取他的值
        if hasattr(layout, '__call__'):
            self.lay=layout()
        else:
            self.lay=layout
        self.layout=self.lay
        if addCheckBox:
            self.Wgt_enableCheckBox=QCheckBox(checkBoxText)
            self.lay.addWidget(self.Wgt_enableCheckBox)
            
        #self.lay.setAlignment(Qt.AlignmentFlag.)
        if groupBox:
            self.groupBox=QGroupBox(groupBox)
            self.groupBox.setCheckable(btnGrpCheckable)
            self.groupBox.setLayout(self.lay)
        else:
            self.setLayout(self.lay)
        
        #如果btnGrp为真创建一个按钮组
        if btnGrp:
            self.btnGrp=QButtonGroup(self.lay)

            
        self.widgetValueDict={QLabel:('text','setText'),QComboBox:('currentText','setItemText'),QSpinBox:('value','setValue'),QLineEdit:('text','setText'),QCheckBox:('isChecked','setChecked')}
        lenWidget=len(widgetList)
        
        self.return_widgetList=[]
        self.widgetTypeList=[]
        self.labelList=[];self.labelCheckBoxList=[]
        if isinstance(self.widgetList,tuple):
            self.widgetList=[self.widgetList]
        for i,ele in enumerate(self.widgetList):
            self.widgetType=ele[0]   #决定widget类型
            self.widgetLabel=ele[1]  #决定widget标签,可能包含QCheckBox
            self.widgetAttr=ele[2]   #决定widget属性
            self.widgetTypeList.append(self.widgetType)
            self.checkBoxWidgetList.append('')
            widget=self.widgetType()
            if i==0 and self.widgetType==QRadioButton:
                widget.setChecked(True)
            if btnGrp:
                self.btnGrp.addButton(widget)
            editable=1
            if len(ele)==3:   #如果没有伸缩因子参数添加默认值
                space=(0,0);stretch=(1,1)
            elif isinstance(ele[3],int ): #如果有伸缩因子参数添加伸缩因子
                space=(ele[3],0);stretch=(1,1)
            else:  #如果提供了三个参数
                spaceAndStretch=ele[3]
                space=spaceAndStretch[0:2]
                stretch=spaceAndStretch[2:]
                #print ('spaceAndStretch->>>',spaceAndStretch)
            self.lay.addSpacing(space[0])
            enableCheckBox=1    
            if self.widgetLabel:
                if  sys.version[0]=='3':
                    #print (type(self.widgetLabel))
                    if isinstance(self.widgetLabel,str) :
                        lab=QLabel(self.widgetLabel)
                        self.labelList.append(lab)
                        lab.setContentsMargins(0, 0,0,0)
                elif sys.version[0]=='2':
                    if  isinstance(self.widgetLabel,unicode) :
                        lab=QLabel(self.widgetLabel)
                        self.labelList.append(lab)
                        lab.setContentsMargins(0, 0,0,0)
                
                if self.widgetLabel[0]==QCheckBox:  #如果是QCheckBox
                    self.checkWidget=QCheckBox() #创建QCheckBox
                    self.checkBoxWidgetList[i]=self.checkWidget
                    lab=QLabel()                              #创建标签
                    lab.setText(self.widgetLabel[1])
                    self.labelList.append(lab)
                    self.labelCheckBoxList.append(self.checkWidget)
                    lab.setContentsMargins(0,0,0,0)
                    self.checkWidget.setChecked(self.widgetLabel[2])
                    self.checkWidget.stateChanged.connect(partial(self.setWgtEnabledFunc,lab,self.checkWidget))
                    self.checkWidget.stateChanged.connect(partial(self.setWgtEnabledFunc,widget,self.checkWidget))
                    self.lay.addWidget(self.checkWidget,1)
                    self.lay.addSpacing(2)

                    
                # lab.setStyleSheet('background-color:rgba(130,155,160,0.04)')
            
            #通过enableCheckBox参数设置组件开关
            #widget.setEnabled(enableCheckBox) #字典里面设置的值优先于这一行
            for classFunc,Val in self.widgetAttr.items():
                # setattr(widget,attrName,attrVal)

                func=eval('widget.{}'.format(classFunc))
                #print ('func->>>',func)
                if classFunc == 'setRange':
                    func(*Val)
                else:
                    func(Val)
            #widget.setContentsMargins(contentsMargins)
            
            if TextSelectableByMouse:
                try:
                    try:
                        widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
                    except:
                        widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                except:
                    pass
            if  Editable:      
                try:
                    widget.setEditable(Editable)
                    widget.lineEdit().setReadOnly(0)
                except:
                    pass
            else:
                try:
                    widget.lineEdit().setReadOnly(ReadOnly)
                except:
                    pass
            
            if self.widgetLabel:
                if exchangeLabelAndWidget:
                    self.lay.addWidget(widget,stretch[1])
                    self.lay.addSpacing(3)
                    self.lay.addWidget(lab,stretch[0])
                else:
                    # (stretch)
                    self.lay.addWidget(lab,stretch[0])
                    self.lay.addSpacing(3)
                    self.lay.addWidget(widget,stretch[1])
            else:
                self.lay.addWidget(widget,stretch[1])
            
            self.lay.addSpacing(space[1])

            self.return_widgetList.append(widget)
        
        self.lay.setContentsMargins(*contentsMargins)
        self.lay.setSpacing(Spacing)

        if  str(par[0]):
            if not groupBox:
                par[0].addWidget(self,par[1])
                
            if groupBox:
                par[0].addWidget(self.groupBox)


        if addCheckBox:
            self.Wgt_enableCheckBox.stateChanged.connect(partial(self.setSelfEnabledFunc,0))
            self.setSelfEnabledFunc(init=1)
            self.Wgt_enableCheckBox.setChecked(checkBoxChecked)
    
    def setSelfEnabledFunc(self,init=1,*args):
        if init:
            isEnable=0
        else:
            isEnable=self.Wgt_enableCheckBox.isChecked()
        for widget in self.return_widgetList:
            widget.setEnabled(isEnable)
        for widget in self.checkBoxWidgetList:
            if widget:
                widget.setEnabled(isEnable)
        for widget in self.labelList:
            widget.setEnabled(isEnable)
        for widget in self.labelCheckBoxList:
            widget.setEnabled(isEnable)
        if self.groupBox:
            self.groupBox.setEnabled(isEnable)

                
    def setWgtEnabledFunc(self,Wgt,checkWidget):
        Wgt.setEnabled(checkWidget.isChecked())

    def get_widgetList(self):
        return self.return_widgetList
    
    def getTextList(self):
        valueList=[]
        for i,widget in enumerate(self.return_widgetList):
            self.widgetType=self.widgetTypeList[i]
            val=eval('widget.{}()'.format(self.widgetValueDict[self.widgetType][0]))
            try:
                valueList.append(eval(val))
            except:
                valueList.append(val)
        return valueList
    
    def get_labelCheckBoxList(self):
        return self.labelCheckBoxList
    
    def get_labList(self):
        return self.labelList
    
    def get_btnGrp(self):
        return self.btnGrp
    
    def get_groupBox(self):
        return self.groupBox
    
    def get_Layout(self):
        return self.lay

# pyqt写一个文件路径拾取的UI非常麻烦,用这个一行解决    
class LPathSel(LQHVGrp):
      
    def __init__(self,par='',l_lab='',buttonName='...',DialogCommit='choose',
                 fileType='*.ext',chooseFunc='getOpenFileName|getExistingDirectory|getSaveFileName',defaultPath='.fbx',
                 layout=QHBoxLayout,groupBox=0,setRead=0):
        #super(LPathSel, self).__init__()
        if isinstance(defaultPath,str):
            defaultPath=os.path.normpath(defaultPath)
            defaultPath=[defaultPath]
        
        widgetList=[(QComboBox,l_lab,{u'addItems':defaultPath},(0,5,0,10)),
                    (QPushButton,'',{'setText':buttonName},(1,0,0,1))] 
        
        LQHVGrp.__init__(self,widgetList=widgetList,par=par,groupBox=groupBox)
        self.widget=self.get_widgetList()
        #self.widget[0].setEditable(True)
        self.widget[0].lineEdit().setReadOnly(setRead)
        self.DialogCommit=DialogCommit
        self.fileType=fileType
        self.chooseFunc=chooseFunc
        self.stDir=os.path.dirname(os.path.abspath(self.widget[0].currentText()))
        
        self.changePathDialogType(fileType=self.fileType,stDir=self.stDir,DialogCommit=self.DialogCommit,chooseFunc=self.chooseFunc)
        


    def changePathDialogType(self,fileType='',stDir='',DialogCommit='',chooseFunc=''):
        if 'File' in chooseFunc:
            self.widget[1].clicked.connect(partial(chooseFile,self,self.widget[0],chooseFunc,DialogCommit,stDir,fileType))
        else:
            self.widget[1].clicked.connect(partial(chooseFile,self,self.widget[0],chooseFunc,DialogCommit,stDir))

    def setText(self,text):
        text=os.path.normpath(text)
        if isinstance(text,str):
            self.widget[0].setCurrentText(text)
        elif isinstance(text,list):
            self.widget[0].insertItems(0,text)
            self.widget[0].setCurrentText(text[0])
            
    def text(self):
        return self.widget[0].currentText() 
    
# class L_ProgressDialog(QProgressDialog):
#     def __init__(self,title=u'还原文件',processList=[]):
#         self.title=title;self.processList=processList
#         self.listLen=len(self.processList)
#         #QProgressDialog(u"正在{},请稍等{}".format(self.title,self.listLen), "Cancel", 0,self.listLen)
#         super(L_ProgressDialog, self).__init__(u"正在{},请稍等{}".format(self.title,self.listLen), "Cancel", 0,self.listLen)
#         self.setWindowTitle(title)
#         self.setFixedSize(650,170)
#         self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint |   # 使能最小化按钮
#                             Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
#                             Qt.WindowType.WindowStaysOnTopHint) 
#         self.open()

#     def ProgressDialog_Procecss(self,index):
#         wsFile,depotFile,fileSize,fileInLocalDisk=self.processList[index]
        
#         if self.wasCanceled():
#             sys.exit(u'停止打包')
#         self.setValue(index+1)
#         self.setLabelText(u'已完成{}/{},正在{}:\n{}\n文件尺寸{}'.
#             format(index,self.listLen,self.title,wsFile,u'{}M'.format(fileSize)))
#         QCoreApplication.processEvents()

class L_ProgressDialog(QProgressDialog):
    def __init__(self,title=u'还原文件',processList=[],size=[650,100]):
        self.title=title;self.processList=processList
        self.listLen=len(self.processList)
        #QProgressDialog(u"正在{},请稍等{}".format(self.title,self.listLen), "Cancel", 0,self.listLen)
        super(L_ProgressDialog, self).__init__(u"", "Cancel", 0,self.listLen)
        self.setWindowTitle(title)
        self.setFixedSize(*size)
        self.setAutoClose(True)
        self.index=0
        #self.setLabel(QLabel())  # 移除原有标签
        self.custom_label = QLabel()
        self.custom_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # 设置自定义布局
        layout = QVBoxLayout()
        layout.addWidget(self.custom_label)
        self.setLayout(layout)

        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint |   # 使能最小化按钮
                            Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
                            Qt.WindowType.WindowStaysOnTopHint) 
        self.open()

    def ProgressDialog_Procecss(self,infoText=''):
        if self.wasCanceled():
            self.close()
            self.canceled.emit()  # 发出取消信号
        self.setValue(self.index)
        if not infoText:
            infoText = r'已完成{}/{}'.format(self.index,self.listLen)
        self.custom_label.setText(infoText)
        self.setWindowTitle(self.title)
        QCoreApplication.processEvents()

class CustomTitleBar(QWidget):
    def __init__(self, parent=None,TitleText=u'搜索和替换'):
        super(CustomTitleBar,self).__init__(parent)
        self.setStyleSheet('background-color: #2d3e50; color: white;')
        

        self.title_label = QLabel(TitleText)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_label.setFixedSize(60, 20)

        self.close_button = QPushButton(u'×')
        self.close_button.setStyleSheet('background-color: #c0392b; color: white; border: none; font-weight: bold; font-size: 18px;')
        self.close_button.setFixedWidth(30)
        self.close_button.setFixedHeight(30)
        self.close_button.clicked.connect(self.parent().close)

        self.minimize_button = QPushButton(u'—')
        self.minimize_button.setStyleSheet('background-color: #2980b9hint; color: white; border: none; font-weight: bold; font-size: 18px;')
        self.minimize_button.setFixedWidth(30)
        self.minimize_button.setFixedHeight(30)
        self.minimize_button.clicked.connect(self.parent().showMinimized)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.minimize_button)
        self.layout.addWidget(self.close_button)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        
class SearchReplaceAddDialog(QDialog):
    def __init__(self, parent=None,treeWidget=None):
        if sys.executable.endswith('maya.exe'):
            super(SearchReplaceAddDialog,self).__init__(get_maya_window())
        else:
            super(SearchReplaceAddDialog,self).__init__(parent)
        self.treeWidget=treeWidget
        self.setWindowTitle(u"重命名")
        if not isMayaEnv():
            self.title_bar = CustomTitleBar(self)
            self.title_bar_layout = QVBoxLayout()
            self.title_bar_layout.addWidget(self.title_bar)
            self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: 1px solid #5e5e5e;")
        self.search_line_edit = QLineEdit()
        self.replace_line_edit = QLineEdit()
        self.prefix_line_edit = QLineEdit()
        self.suffix_line_edit = QLineEdit()
        self.search_button = QPushButton(u'搜索        ')
        self.replace_button = QPushButton(u'替换       ')
        self.add_prefix_button = QPushButton(u'添加前缀')
        self.add_suffix_button = QPushButton(u'添加后缀')
        self.all_children_checkbox = QCheckBox(u'包括所有子层级')
        self.all_children_checkbox.setChecked(1)
        self.search_button.clicked.connect(self.search)
        self.replace_button.clicked.connect(self.replace)
        self.add_prefix_button.clicked.connect(self.add_prefix)
        self.add_suffix_button.clicked.connect(self.add_suffix)
        layout = QFormLayout()
        layout.addRow(u'搜索:', self.search_line_edit)
        layout.addRow(u'替换:', self.replace_line_edit)
        layout.addRow(u'前缀:', self.prefix_line_edit)
        layout.addRow(u'后缀:', self.suffix_line_edit)
        layout.addRow(self.all_children_checkbox)
        layout.addRow(self.search_button, self.replace_button)
        layout.addRow(self.add_prefix_button, self.add_suffix_button)
        layout.setContentsMargins(10, 10, 10, 10)
        self.layout = QVBoxLayout()
        if not isMayaEnv():
            self.layout.addLayout(self.title_bar_layout)
        self.layout.addLayout(layout)
        self.setLayout(self.layout)
        self.setStyleSheet(qss_StyleTemplate())

        self._old_pos = None
        


    def mousePressEvent(self, event):
        self._old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self._old_pos:
            delta = event.globalPos() - self._old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self._old_pos = None

    def search(self):
        search_text = self.search_line_edit.text()
        if search_text:
            selected_item = self.treeWidget.currentItem()
            all_children = self.all_children_checkbox.isChecked()
            self.search_and_replace(selected_item, search_text, None, all_children)

    def replace(self):
        search_text = self.search_line_edit.text()
        replace_text = self.replace_line_edit.text()
        print (search_text, replace_text)
        if search_text :
            selected_item = self.treeWidget.currentItem()
        all_children = self.all_children_checkbox.isChecked()
        self.search_and_replace(selected_item, search_text, replace_text, all_children)

    def add_prefix(self):
        prefix_text = self.prefix_line_edit.text()
        if prefix_text:
            selected_item = self.treeWidget.currentItem()
            all_children = self.all_children_checkbox.isChecked()
            self.add_prefix_suffix(selected_item, prefix_text, '', all_children)

    def add_suffix(self):
        suffix_text = self.suffix_line_edit.text()
        if suffix_text:
            selected_item = self.treeWidget.currentItem()
            all_children = self.all_children_checkbox.isChecked()
            self.add_prefix_suffix(selected_item, '', suffix_text, all_children)

    def search_and_replace(self, item, search_text, replace_text, all_children):
        if all_children:
            for i in range(item.childCount()):
                child_item = item.child(i)
                self.search_and_replace(child_item, search_text, replace_text, True)
        text = item.text(0)
        if search_text in text:
            item.setText(0, text.replace(search_text, replace_text))


    def add_prefix_suffix(self, item, prefix_text, suffix_text, all_children):
        if all_children:
            for i in range(item.childCount()):
                child_item = item.child(i)
                self.add_prefix_suffix(child_item, prefix_text, suffix_text, True)
        text = item.text(0)
        item.setText(0, prefix_text+text+suffix_text)

def get_maya_window():
    # get the maya main window as a QMainWindow instance
    import maya.OpenMayaUI as omui
    win = omui.MQtUtil.mainWindow()
    import shiboken2
    ptr = shiboken2.wrapInstance(long(win), QWidget)
    return ptr


if __name__=='__main__':
    print ('----------------------')
    app = QApplication(sys.argv)
    timeLable = '''            动画开始时间 : 10\
                    动画结束时间 : 20\
                时间滑块开始时间 : 30\
                时间滑块结束时间 : 40'''
    aa=QWidget()
    lay=QHBoxLayout()
    #lay.addWidget(QLabel('aaa'),100)  # 没有这一句不显示LQHVGrp的示例,不知道什么原因
    aa.setLayout(lay)
    widgetList=[(QLabel,'',{'setText':timeLable},(0,0,0,0)),
                (QLabel,'',{'setText':timeLable},(0,0,0,0))]
    bb=LQHVGrp(btnGrp=0,widgetList=widgetList,par=[lay,500],
                    exchangeLabelAndWidget=False,layout=QVBoxLayout,
                    groupBox='如果时间滑块范围和摄像机名称范围不一致请确认摄像机命名是否正确')

    # LPathSel(par=lay,l_lab=u'',DialogCommit=u'预设文件',fileType="*.json",buttonName=u'...',chooseFunc=u'getOpenFileName',defaultPath='D:/aa.jpg')

    # aa.show()
    # if QT_API=='PyQt6':
    #     print (QT_API)
    #     sys.exit(app.exec_())
    # else:
    #     sys.exit(app.exec())
