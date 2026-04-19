# -*- coding: utf-8
from __future__ import absolute_import
import subprocess,os,sys,codecs,json,traceback,re
userName = os.environ.get('USERNAME')
import inspect
LugwitToolDir=r"d:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayap"
# 自动安装异常钩子（如果环境变量允许）
try:
    from .l_src.exception_hook import install_trace_hook
    result = install_trace_hook()
    if result:
        print("[OK] Lugwit_Module: 异常钩子已安装 - 异常发生时将显示详细调用链")
        print("[TIP] 提示: 可通过设置环境变量 DISABLE_EXCEPTION_HOOK=1 禁用钩子")
    else:
        print("[WARNING] Lugwit_Module: 异常钩子已禁用")
except (ImportError, UnicodeEncodeError) as e:
    print(f"[WARNING] Lugwit_Module: 异常钩子安装失败 - {type(e).__name__}")
except Exception:
    traceback.print_exc()


def is_main():
    """
    判断调用该函数的模块是否是主模块 (__main__)。
    
    返回:
        bool: 如果调用者是主模块，返回 True，否则返回 False。
    """
    # 获取当前的堆栈帧
    stack = inspect.stack()
    # 调用者的堆栈帧通常是第二个元素
    caller_frame = stack[1].frame
    # 获取调用者的模块
    caller_module = inspect.getmodule(caller_frame)
    if caller_module:
        return caller_module.__name__ == "__main__"
    return False




from .main import *
# lprint 已在 l_src.__init__ 中从 pytracemp 导入
from .l_src import lprint

import __main__
__main__.lprint=lprint
if sys.version_info.major==2:
    __main__.open=codecs.open
py_ver='{}{}'.format(sys.version_info.major,sys.version_info.minor)
userConfigFile = os.path.expandvars(r"%USERPROFILE%\.Lugwit\config\config.json")
Lugwit_mayaPluginPath=os.environ.get('Lugwit_mayaPluginPath')

oriEnvVarFile=os.path.expandvars("%USERPROFILE%")+r'/.Lugwit/config/oriEnvVar.json'
if not os.path.exists(oriEnvVarFile):
    oriEnvVarFile_Dir=os.path.dirname(oriEnvVarFile)
    os.makedirs(oriEnvVarFile_Dir,exist_ok=True)
    os.environ['oriEnvVarFile']=oriEnvVarFile
    oriEnvVar=os.environ.copy()
    LugwitToolDir=re.search('.+trayapp',__file__).group() if re.search('.+trayapp',__file__) else ""
    sys.path.append(LugwitToolDir+'/Lib')

    sys_executable_dir=os.path.dirname(sys.executable)
    sys_executable_dir =os.path.realpath(sys_executable_dir)
    path=os.getenv('PATH')
    # 分割PATH，过滤掉包含Python解释器目录的路径
    filtered_path = []
    userName=os.getenv('USERNAME')
    print ('sys_executable_dir',sys_executable_dir)
    for x in path.split(';'):
        x = os.path.realpath(x)
        if  os.path.dirname(sys_executable_dir) not in x and 'conda' not in x:
            filtered_path.append(x) 
        # else:
        #     print('x',x)
    path=';'.join(filtered_path)
    oriEnvVar['PATH'] =path
    print("PYTHONPATH",os.getenv("PYTHONPATH"))
    oriEnvVar.pop('PYTHONHOME',None)
    # oriEnvVar.pop('PYTHONPATH',None)

    with codecs.open(oriEnvVarFile,'w',encoding='utf-8') as f:
        json.dump(oriEnvVar,f,ensure_ascii=False,indent=4)
        
        
with codecs.open (os.getenv('oriEnvVarFile'),'r',encoding='utf8') as f:
    env=json.load(f)
    tempDict = {}
    for key,val in env.items():
        try:
            tempDict[str(key)]  = str(val)
        except:
            print("key,val",key,val,'this error will be ignored')
            traceback.print_exc()
    tempDict['LUGWIT_MAYAPLUGINPATH']=Lugwit_mayaPluginPath
oriEnvVar = tempDict


# __init__.py
def init_os():# 执行运行这个函数才会导入某些模块,避免加载过多的模块
    global l_os,l_subprocess
    from .l_src import l_os
    from .l_src import l_subprocess

try:
    from .l_src.usualFunc_dev import dynamic_import
except ImportError:
    try:
        from .l_src.usualFunc_old import dynamic_import
    except ImportError:
        dynamic_import = None