# -*- coding: utf-8
import os,sys,re

sys_executable=sys.executable

isMayaEnv=lambda *args : re.search('maya.*\.exe',sys.executable)
isHoudiniEnv=lambda *args : re.search('houdini.+.exe',sys.executable)
isHoudiniPyEnv=lambda *args : re.search('hython.exe',sys.executable)
isMayaPyEnv=lambda *args : re.search('mayapy.exe',sys.executable)
isUEnv=lambda *args : re.search('UnrealEditor',sys.executable)
# 定义一些常用函数
isPy3 = lambda *args : sys.version[0]=='3'
pyVersion = str(sys.version[0])+(sys.version[2])
getCurDir = lambda file : os.path.dirname(file)


# __all__=['isMayaEnv','isMayaPyEnv','isUEnv','sys_executable']