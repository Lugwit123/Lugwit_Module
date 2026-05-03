# -*- coding: utf-8

import os
import ctypes
from ctypes import wintypes


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

def startdir(dirToOpen=None):
    if not os.path.exists(dirToOpen):
        from l_simple_gui import ask_yes_no

        if ask_yes_no("目录{}不存在,是否创建并打开".format(dirToOpen), title="确认"):
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
