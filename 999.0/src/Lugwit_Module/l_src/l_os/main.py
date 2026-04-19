# -*- coding: utf-8

import os
import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import messagebox


def check_path(path):
    '''
    返回值 : 'symLink',"realDir",'None'
    '''
    if not os.path.exists(path):
        return "路径不存在"

    # 定义Windows API函数属性
    GetFileAttributes = ctypes.windll.kernel32.GetFileAttributesW
    GetFileAttributes.argtypes = [wintypes.LPCWSTR]
    GetFileAttributes.restype = wintypes.DWORD

    FILE_ATTRIBUTE_DIRECTORY = 0x10
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400

    attributes = GetFileAttributes(path)

    
    
    is_directory = attributes & FILE_ATTRIBUTE_DIRECTORY
    is_reparse_point = attributes & FILE_ATTRIBUTE_REPARSE_POINT
    
    if is_directory and is_reparse_point:
        # print (u"路径是一个符号链接或Junction Point")
        return 'symLink'
    elif is_directory:
        # print (u"路径是一个真实的目录")
        return "realDir"
    else:
        # print ("路径不是目录也不是符号链接/Junction Point")
        return None

def center_window(root, width=300, height=200):
    # 获取屏幕尺寸以及窗口宽高
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # 计算 x, y 坐标
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    
    # 设置窗口的几何尺寸
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def simpleWin(title=u"提示" ,text="这是一个标签",btn_command=None):
    root = tk.Tk()
    root.title(title)
    center_window(root, 300, 150)
    label = tk.Label(root, text=text)
    label.pack(pady=10)  # pady=10增加垂直外边距
    button = tk.Button(root, text="OK", command=btn_command)
    button.pack(pady=5)  # pady=5增加垂直外边距
    root.mainloop()
def startdir(dirToOpen=None):
    if not os.path.exists(dirToOpen):
        root = tk.Tk()
        root.withdraw()
        response = messagebox.askquestion("确认", 
            u"目录{}不存在,是否创建并打开".format(dirToOpen))
        # 销毁Tk窗口
        root.destroy()
        if response == 'yes':
            os.makedirs(dirToOpen)
            os.startfile(dirToOpen)
    else:
        os.startfile(dirToOpen)

__all__=['check_path','startdir']


if __name__=="__main__":
    # 示例使用
    pass
    # path_to_check = r"D:\path\to\your\directory"  # 更换为你要检查的路径
    # # dir = "D:/aa"
    # result = startdir(path_to_check)
    # print(result)
