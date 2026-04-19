import os
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import winreg,re


def find_maya_install_path():
    # 查找最新版本的Maya安装位置
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Autodesk\Maya')
        subkeys_count = winreg.QueryInfoKey(key)[0]
        versions = []
        for i in range(subkeys_count):
            version = winreg.EnumKey(key, i)
            if version.startswith('20') and version.isdigit():
                versions.append(version)
        versions.sort(reverse=True)
        print ('versions:',versions)
        maya_strings_files=[]
        for version in versions:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Autodesk\Maya\%s\Setup\InstallPath' % version)
            maya_path, _ = winreg.QueryValueEx(key, 'MAYA_INSTALL_LOCATION')
            print ('maya_path:',maya_path)
            maya_strings_dir = os.path.join(maya_path, 'resources')
            print ('maya_strings_dir:',maya_strings_dir)
            maya_strings_file = [os.path.join(maya_strings_dir,f) for f in os.listdir(maya_strings_dir) if f.startswith('MayaStrings')]
            
            if maya_strings_file:
                maya_strings_files+=maya_strings_file
    except Exception as e:
        print (e)
    print ('maya_strings_files:',maya_strings_files)
    return maya_strings_files

class MayaFontSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Maya字体选择器')
        self.resize(500, 200)

        # 创建标签和下拉框控件
        self.label1 = QLabel('选择Maya界面语言:', self)
        self.label1.move(20, 20)
        self.combo1 = QComboBox(self)
        self.combo1.move(150, 20)
        self.combo1.addItem('中文')
        self.combo1.addItem('英文')
        self.label2 = QLabel('选择字体样式:', self)
        self.label2.move(20, 60)
        self.combo2 = QFontComboBox(self)
        self.combo2.move(150, 60)

        # 创建按钮控件
        self.btn1 = QPushButton('修改字体样式', self)
        self.btn1.move(280, 120)
        self.btn1.clicked.connect(self.changeFont)

        # 设置背景颜色
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(230, 230, 230))
        self.setPalette(palette)

        # 查找Maya的安装位置和所有MayaStrings文件路径
        self.maya_strings_files = find_maya_install_path()
        print ('self.maya_strings_files:',self.maya_strings_files)

    def changeFont(self):
        # 根据用户选择的字体样式修改所有MayaStrings文件中的字体
        font = self.combo2.currentFont()
        if self.maya_strings_files:
            success_count = 0
            error_count = 0
            for maya_strings_file in self.maya_strings_files:
                maya_strings_path = maya_strings_file
                try:
                    with open(maya_strings_path, 'r') as f:
                        lines = f.read()
                    with open(maya_strings_path, 'w') as f:
                        f.write(re.sub(r'(win_en_US.+,\d+,)([^"\n]+)', f'\\1{font.family()}', lines,flags=re.MULTILINE))
                    success_count += 1
                except Exception as e:
                    print (e)
                    error_count += 1
            QMessageBox.information(self, '提示', '已修改%s个MayaStrings文件，%s个文件修改失败。请重新启动Maya以生效。' % (success_count, error_count))
        else:
            QMessageBox.warning(self, '警告', '未找到MayaStrings文件，请检查Maya的安装目录。')

def main():
    app = QApplication(sys.argv)
    fontSelector = MayaFontSelector()
    fontSelector.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

