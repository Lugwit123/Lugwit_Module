import os,sys

QT_API=os.environ.get('QT_API')

sys_version_2=sys.version[2]
if not QT_API:
    QT_API='PyQt5'
if 'maya' in sys.executable:
    QT_API='PySide2'
lprint ('QT_API:',QT_API,__file__)

exec('import  {}'.format(QT_API))
exec('from {}.QtWidgets import *'.format(QT_API))
exec('from {}.QtCore  import *'.format(QT_API))
exec('from {}.QtGui  import *'.format(QT_API))


def get_all_widgets(layout):
    widgets = []
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widgets.append(widget)
    return widgets

def setLayout_Height(layout,height,setType='QWidget|QGroupBox'):
    widgets=get_all_widgets(layout)
    for widget in  widgets:
        if isinstance(widget,setType):
            widget.setFixedHeight(height)
