# -*- coding: utf-8
from __future__ import print_function
from __future__ import absolute_import
import getpass
import sys,os,time,socket,re,codecs,traceback,json,io


#代码加密
username = getpass.getuser()
sys_executable=sys.executable
print ('sys_executable',sys_executable,__file__)
curDir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curDir)
sys.path.append(u'{}\\l_src\\l_qtpy{}'.format(curDir,sys.version_info.major))
# import encodings.idna


sys_version=sys.version
sys_version= '{}{}'.format(sys_version[0],sys_version[2])

if sys.version[0]=='2':
    import  _winreg as winreg
else:
    import winreg





import  Lugwit_liscense
liscense=Lugwit_liscense.liscense
import l_src


from l_src.l_winreg.l_winreg import CustomRegistryKey
from l_src.getExecuteExe import *
Lugwit_publicPath = ""

def getCurrentTimeAsLogName():
    return time.strftime('%Y_%m_%d', time.localtime())





def get_my_documents_folder():
    key = CustomRegistryKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
    )
    return key.get_value("Personal")[0]

LugwitToolDir=os.environ.get('LugwitToolDir',"")
# LugwitToolDir=LugwitToolDir.replace('\\src','')
sys.path.append(LugwitToolDir+'/src')

userDir=os.path.expandvars("%USERPROFILE%")

if userDir == "C:\\Windows\\system32\\config\\systemprofile":
    userDir = r"C:\Users\Administrator.OC"

oriEnvVarFile=userDir+r'/.Lugwit/config/oriEnvVar.json'
os.environ['oriEnvVarFile'] = oriEnvVarFile

from tool_env import *

# 常用变量:
TempDir=os.environ.get('Temp')

sys.path.insert(0,Lugwit_publicPath+r'Python\PyFile\Pyd_File\Py{}'.format(pyVersion))






# 函数 gethostname() 返回当前正在执行 Python 的系统主机名
hostName = socket.gethostname()
print ('hostName',repr(hostName))
localIP = socket.gethostbyname(hostName)



print(u'import Lugwit_Module finish\n')


def __dir__():
    pass

def __dict__():
    pass

# -------------------------------------------------------------------------
# Python版本兼容性导入
# -------------------------------------------------------------------------
LPrint = None
# 检测Python版本并导入相应的LPrint实现
if sys.version_info[0] == 2:
    # Python 2.7 - 使用旧版本
    try:
        from l_src.usualFunc import LPrint
    except ImportError as e:
        print("[Lugwit_Module] 警告: 无法导入Python 2.7版本的LPrint: {}".format(e))
        LPrint = None
else:
    # Python 3.x - 使用pytracemp新版本
    try:
        # 优先使用pytracemp
        pytracemp_src_path = os.path.join(os.path.dirname(__file__), '..', 'pytracemp', 'src')
        
        if os.path.exists(pytracemp_src_path):
            sys.path.insert(0, pytracemp_src_path)
            from pytracemp.usualFunc import LPrint
        print("日志分支: 使用pytracemp",os.path.exists(pytracemp_src_path),pytracemp_src_path)
    except ImportError as e:
        print("[Lugwit_Module] 警告: 无法导入pytracemp版本的LPrint，尝试fallback: {}".format(e))
        try:
            from l_src.usualFunc import LPrint
        except ImportError as e2:
            print("[Lugwit_Module] 错误: 无法导入任何版本的LPrint: {}".format(e2))
            LPrint = None

# 导出LPrint到模块级别
__all__ = ['LPrint', 'hostName']

