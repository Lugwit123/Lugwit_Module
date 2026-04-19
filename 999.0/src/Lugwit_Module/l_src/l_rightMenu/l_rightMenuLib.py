# coding:utf-8
import time
from shutil import copyfile
import os
import re,sys
import ctypes,pyperclip
import traceback
import codecs
# import fire
from pprint import pprint



try:
    import  _winreg as winreg
except:
    import winreg

userName=os.getlogin()

USERPROFILE=os.environ['USERPROFILE']

from ctypes import windll
import time
import win32file
from win32file import *


LugwitPath=os.environ.get('LugwitPath')
lugwit_PluginPath=os.environ.get('lugwit_PluginPath')
Lugwit_publicPath=os.environ.get('Lugwit_publicPath')


def is_open(filename):
 
  try:
    #首先获得句柄
    vHandle =win32file.CreateFile(filename, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
    #判断句柄是否等于INVALID_HANDLE_VALUE
    if int(vHandle)==INVALID_HANDLE_VALUE:
      print("# file is already open")
      return True # file is already open
    win32file.CloseHandle(vHandle)
 
  except Exception as e:
    print(e)
    return True

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def getDocPath():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Personal")[0]

# maya版本管理 MayaPy 2.7的版本对PySimpleGUI支持不好,所以注册表的右键菜单使用的是服务器上的python解释器
def toggleMayaVersion():
    import PySimpleGUI as sg
    mayaVerList = [x for x in range(2018, 2027)]
    # Create some widgets
    size = (50, len(mayaVerList))
    Listbox = sg.Listbox(mayaVerList, size=size)
    ok_btn = sg.Button('OK')
    cancel_btn = sg.Button('Cancel')
    layout = [[Listbox],
            [ok_btn, cancel_btn]]

    # Create the Window
    window = sg.Window('please select Maya version', layout)
    # Create the event loop
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            # User closed the Window or hit the Cancel button
            window.close()
            break
        if event in (None, 'OK'):
            mayaVersion = values[0][0]
            break
    print('mayaVersion->',mayaVersion)
    
    pathA = Lugwit_publicPath+  r'\WinRightButton\Lugwit_右键菜单.reg'
    with open(pathA, mode='r+') as file:
        fileContext = file.read()
        #re.sub('\\\\Maya\d\d\d\d\\\\','\\\\Maya2020\\\\','\\Maya2018\\')
        fileContext = re.sub(
            '\\\\Maya....\\\\', '\\\\Maya' + str(mayaVersion)+'\\\\', fileContext)
        fileContext = re.sub("Maya_.... 资产后台处理",
                            "Maya_{} 资产后台处理".format(mayaVersion), fileContext)
        os.system('reg delete HKEY_CLASSES_ROOT\AllFilesystemObjects\shell\Lugwit_Fbx\shell\MayaAssetExport /f')    
        file.seek(0)
        file.truncate()
        file.write(fileContext)
        file.close()

    pathB = r'D:/Lugwit_右键菜单.reg'

    file = copyfile(pathA, pathB)
    #os.startfile(pathB)
    
    from subprocess import run
    run('regedit /s {}'.format(pathB), shell=True)


def exportRegdit():
    regList = [r'HKEY_CLASSES_ROOT\AllFilesystemObjects\shell\Lugwit_Fbx',
            r'HKEY_CLASSES_ROOT\Directory\Background\shell\Lugwit_rightMenuManager',
            r'HKEY_CLASSES_ROOT\*\shell\copy_FilePath',
            r'HKEY_CLASSES_ROOT\*\shell\Lugwit_Fbx',
            r'HKEY_CLASSES_ROOT\Directory\Background\shell\Lugwit程序工具',
            r'HKEY_CLASSES_ROOT\Directory\Background\shell\Lugwit切换MayaArnold版本',
            r'HKEY_CLASSES_ROOT\Directory\Background\shell\Lugwit_ProjectMenuManager',
            r'HKEY_CLASSES_ROOT\Directory\Background\shell\Lugwit_ImageTool',
            r'HKEY_CLASSES_ROOT\Directory\Shell\Lugwit_Menu',
            r'HKEY_CLASSES_ROOT\*\shell\UE_RightMenu',]
    
    regContext = ''
    for i, x in enumerate(regList):
        path = 'D:/aa_{}.reg'.format(i)
        with open(path, 'w', encoding='utf-16') as file:
            pass
        cmd = 'reg export {} {} -y'.format(x,path)
        os.system(cmd)
        with open(path, 'r', encoding='utf-16') as file:
            regContext += file.read()
    regContext+='[HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer]\n"MultipleInvokePromptMinimum"=dword:000003e8'
    print(regContext)
    with open(u'D:/Lugwit_右键菜单.reg', 'w') as file:
        file.write(regContext)
    pathA = Lugwit_publicPath+r'\WinRightButton\Lugwit_右键菜单.reg'
    if not os.path.exists(Lugwit_publicPath+r'\WinRightButton'):
        os.makedirs(Lugwit_publicPath+r'\WinRightButton')
    print ('export path',pathA)
    file = copyfile('D:/Lugwit_右键菜单.reg', pathA)
    os.startfile(Lugwit_publicPath+r'\WinRightButton')
    time.sleep(10)
    
    
def setPathEnvironmentVariable():
    # 环境变量系统路径 HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment
    
    def setPathEnvironmentVariableFucn(key):
        pathValue= winreg.QueryValueEx(key, "path")[0]
        pathValue=pathValue.split(';')
        if f'{lugwit_PluginPath}\\Python\\Python37' not in pathValue:
            pathValue+=[f'{lugwit_PluginPath}\\Python\\Python37']
        if f'{lugwit_PluginPath}\\Python\\Python27' not in pathValue:
            pathValue+=[f'{lugwit_PluginPath}\\Python\\Python27']
        if f'{lugwit_PluginPath}\\Python\\Python27\Scripts' not in pathValue:
            pathValue+=[f'{lugwit_PluginPath}\\Python\\Python27\Scripts']
        if f'{lugwit_PluginPath}\\Python\\Python37\Scripts' not in pathValue:
            pathValue+=[f'{lugwit_PluginPath}\\Python\\Python37\Scripts']
        winreg.SetValueEx(key,'path',1,winreg.REG_SZ,';'.join(pathValue).replace(';;',';'))
        print (winreg.QueryValueEx(key, "path"))
    key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,'Environment',access=winreg.KEY_ALL_ACCESS)
    setPathEnvironmentVariableFucn(key)
    # key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,'Environment',access=winreg.KEY_ALL_ACCESS)
    # setPathEnvironmentVariableFucn(key)
        
# print (setPathEnvironmentVariable())
# sys.exit()


def importRegdit():
    pathA = Lugwit_publicPath+ r'\WinRightButton\Lugwit_右键菜单.reg'
    pathB = r'D:/Lugwit_右键菜单.reg'
    file = copyfile(pathA, pathB)
    from subprocess import run
    run('regedit /s {}'.format(pathB), shell=True)
    print (u'成功导入注册表,10s后关闭窗口')
    time.sleep(10)
    
def clearRegdit():
    regList = [r'HKEY_CLASSES_ROOT\AllFilesystemObjects\shell\Lugwit_Fbx',
            r'HKEY_CLASSES_ROOT\*\shell\LugwitMenu',
            r'HKEY_CLASSES_ROOT\Directory\Background\shell\Lugwit程序工具',
            r'HKEY_CLASSES_ROOT\Directory\Background\shell\Lugwit_ProjectMenuManager',
            r'HKEY_CLASSES_ROOT\Directory\Shell\Lugwit_Menu']
    getAdminPermission()
    for i, x in enumerate(regList):
        cmd = 'reg delete {} /f'.format(x)
        os.system(cmd)

def getAdminPermission():
    if is_admin():
        pass
    else:
        print ("您不是管理员")
        if sys.version_info[0] == 3:
            print ('重新运行并传递系统变量',' '.join(sys.argv))
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), "", 1)
        else:#in python2.x
            ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
        print (f'获取管理员权限执行{__file__}')
        

def getCopyPermission(on_off=1):
    if is_admin()  :
        os.system(f'reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /d {on_off} /f /t REG_DWORD')
        print (f'您是管理员->{on_off}')
        time.sleep(2)
    else:
        print (f'您不是管理员->{on_off}')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    # time.sleep(6)

    

def setPythonImagesAddress():
    user = os.path.expandvars("%USERPROFILE%")
    print('userdir:', user)
    pip_dir = user+'\\pip\\'
    print('pip_dir:', pip_dir)
    pip_ini_context = '[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host=mirrors.aliyun.com'
    pip_ini_file = pip_dir+'\\pip.ini'
    print ('pip_ini_file:', pip_ini_file)
    if not os.path.exists(pip_dir):
        os.makedirs(pip_dir)
    with open(pip_ini_file , 'w') as pip_file:
        pip_file.write(pip_ini_context)
    
    # with open('D:/pip/pip.ini', 'w') as pip_file:
    #     pip_file.write(pip_ini_context)
    # xstr=   f'xcopy/y D:\pip\pip.ini {pip_dir}'
    # os.system(xstr)
    # print (xstr)
    # os.startfile(pip_dir)


def sync_Lugwit_Module():
    getAdminPermission()
    py37_Lugwit_ModuleDir =lugwit_PluginPath+ r'\Python\Python37\Lib\site-packages\Lugwit_Module'
    py27_Dir =lugwit_PluginPath+ r'\Python\Python27\Lib\site-packages\Lugwit_Module\\'
    #py27_Dir =lugwit_PluginPath+ r'\Python\Python27\Lib\site-packages'
    MayaVersionList = [2018,2019,2020]
    cmdStr=''
    try:
        cmdStr+=f'xcopy {py37_Lugwit_ModuleDir} {py27_Dir} /Y /R /E\n'
    except Exception as e:
        print ()
    for item in MayaVersionList:
        try:
            MayaPy27_Dir = eval(f'maya{item}InsPath').replace('/','\\') + \
                                r'\Python\Lib\site-packages\Lugwit_Module\\'
            print (MayaPy27_Dir)                   
            cmdStr+=f'xcopy {py37_Lugwit_ModuleDir} "{MayaPy27_Dir}"  /Y /R /E\n'
        except Exception as e:
            print (e)
        
    cmdStr+='\npause'
    tempBat='D:\\temp.bat'
    with open (tempBat,'w') as f:
        f.write(cmdStr)
    os.startfile(tempBat)
    
def setP4Config(*args):
    os.system(f'setx P4CONFIG C:\\Users\{userName}\\.p4qt\\.p4config')
    print (u'成功设置p4配置文件,10s后关闭窗口')
    time.sleep(10)
        
def installUEplugin(*args):
    pathA=Lugwit_publicPath+ r'\DCCSoftware\UE\init_unreal.py'
    print (pathA)
    pathB='{}\\UnrealEngine\\Python\\'.format(getDocPath())
    print ('pathB:', pathB)
    if not os.path.exists(pathB):
        os.makedirs(pathB)
    copyStr=f'Xcopy {pathA} {pathB} /Y /R'
    print ('copyStr',copyStr)
    os.system(copyStr)
    os.startfile('{}/UnrealEngine/Python'.format(getDocPath()))
    os.startfile(f'{Lugwit_publicPath}/安装步骤/安装UE插件.bat')
# installUEplugin()
# sys.exit()



def fileOffsetFrame():
    import os
    fileDir=sys.argv[2]
    fileInDir=os.listdir(fileDir)
    inputNum=input("请输入偏移帧数：")
    inputNum=int(inputNum)
    if inputNum>0:
        fileInDir=list(reversed(fileInDir))
    for file in fileInDir:
        print ('file->',file)
        aa_file=file.split('.')[-2]+'.'+file.split('.')[-1]
        new_crazy = re.search('-*?\d+',aa_file)
        if new_crazy:
            new_crazy = new_crazy.group()
            if new_crazy.startswith('.'):
                new_crazy= new_crazy[1:]    
        print ('new_crazy',new_crazy)
        if new_crazy:
            count=int(new_crazy)+inputNum
            count=str(count).zfill(4)
            ext=os.path.splitext(file)[1]
            newName=f'{fileDir}\\{count}{ext}'
            print ('新的名称',newName)
            try:
                os.rename(f'{fileDir}\{file}',newName)
            except:
                pass

            print('\n')
    print ('重命名结束,请此关闭窗口'   )
    time.sleep(20)

def init_makeGif():
    import os
    freeimagePath=f'{lugwit_PluginPath}\Python\Python37\Lib\site-packages\imageio\freeimage\freeimage-3.15.1-win64.dll'
    destPath=f'C:\\Users\\{userName}\\AppData\\Local\\imageio\\freeimage\\'
    if not os.path.exists(destPath+'\\freeimage-3.15.1-win64.dll'):
        print ('fuzhi')
        xcopyStr=f'Xcopy {freeimagePath} {destPath} /Y /R'
        print ('xcopyStr',xcopyStr)
        os.system(xcopyStr)

def makeGif():
    import os
    saveFileDir='D:/aa/temp'
    if not os.path.exists(saveFileDir):
        os.makedirs(saveFileDir)
    txtFile='D:/aa/temp/temp.txt'
    
    time.sleep(1)
    if not os.path.exists(txtFile): #文件不存在就把文件加入到txt文件中
        with open (txtFile,'w') as f:
            f.write(sys.argv[2]+'\n')
            print ('文件不存在,新建文件')
            
    elif  os.path.exists(txtFile) :
        with open (txtFile,'a') as f:
            f.write(sys.argv[2]+'\n')
            return
        
    print (u'开始合成gif')
    try:
        while 1:
            if not os.path.exists(txtFile):
                return
            
            modifyTimeA=os.path.getmtime(txtFile)
            time.sleep(1)
            modifyTimeB=os.path.getmtime(txtFile)
            dirname=os.path.dirname(sys.argv[2]).replace('\\','/').split('/')[-1]
            gif_Path = 'D:/aa/'+dirname+'.gif'
            print ('gif_Path',gif_Path)
            print (modifyTimeB==modifyTimeA)
            if modifyTimeB==modifyTimeA:
                time.sleep(1)
                import imageio,os   
                with open (txtFile,'r') as f:
                    imagePathList=f.readlines()
                os.remove(txtFile)
                print ('imagePathList',imagePathList)
                fps=input(u'请输入帧速率,比如30帧每秒输入30后回车,默认值为30,为30直接回车:\n')
                if not fps:
                    fps='30'
                fps=int(fps)
                
                imagePathList=sorted(imagePathList)
                imagePathList_length=len(imagePathList)
                def create_gif(gif_Path, duration=0.5):
                    frames = []
                    for i,imagePath in enumerate(imagePathList):
                        imagePath=imagePath.replace('\n','')
                        print ('正在读取文件,请稍后...',imagePath,f'{i}/{imagePathList_length}')
                        frames.append(imageio.imread(imagePath))

                    print ('正在合成Gif文件,请稍后...')
                    imageio.mimsave(gif_Path, frames,  duration=duration)
                    print ('合成{}完毕,请关闭此窗口...'.format(gif_Path))
                    if gif_Path not in imagePathList:
                        print (f'{gif_Path} not in {imagePathList}',gif_Path not in imagePathList)
                        os.system(gif_Path)
                    return
                
                def main():
                    duration = 1/fps
                    create_gif(gif_Path, duration)
                    time.sleep(100)
                main()
    except:
        time.sleep(10)
        try:
            os.remove(txtFile) 
        except:
            pass
    
def toggleArnoldVersion():
    MayaEnv=r'''
    //Arnold_Env
    MAYA_RENDER_DESC_PATH = {ArnoldVersionDir}\版本
    PATH = %PATH%;{ArnoldVersionDir}\版本\bin
    MAYA_MODULE_PATH = %MAYA_MODULE_PATH%;{ArnoldVersionDir}\版本
    //Arnold_Env
    '''.format(ArnoldVersionDir=TD_Plug_EnvVar['ArnoldVersionDir'])
    lprint (TD_Plug_EnvVar['ArnoldVersionDir'])
    MayaEnv=MayaEnv.replace(' ','')
    mayaVersion,arnoldVersion=sys.argv[2].split('_')[:2]
    MayaEnvFile=f'{getDocPath()}/maya/{mayaVersion}/Maya.env'
    arnoldVersion=sys.argv[2]
    with open (MayaEnvFile,'a+',encoding='ANSI') as f:
        MayaEnv_content=f.read()
    with open (MayaEnvFile,'w',encoding='ANSI')  as f:
        search_arnoldSeting=re.search('//Arnold_Env.+//Arnold_Env',MayaEnv_content,flags=re.I|re.M|re.S)
        print ('search_arnoldSeting',search_arnoldSeting)
        if search_arnoldSeting:
            search_arnoldSeting=search_arnoldSeting.group()
            print ('search_arnoldSeting\n',search_arnoldSeting)
            if '回到安装版本' in arnoldVersion:
                MayaEnv_content=MayaEnv_content.replace(search_arnoldSeting,'')
                print ('arnol版本切换为默认版本',sys.argv[2])
            else:
                MayaEnv_content=re.sub('20......',sys.argv[2],MayaEnv_content)
                print ('arnol版本为切换',sys.argv[2])


        else:
            if '回到安装版本' not in arnoldVersion:
                MayaEnv_content=MayaEnv.replace(r'版本',sys.argv[2])
                print ('由默认版本arnol版本切换为',sys.argv[2])
        print ('\n\nMayaEnv_content\n',MayaEnv_content)
                
        f.write(MayaEnv_content)

def clearArnoldInstallInfoToInstallMultiVersionArnold():      
    cmd=r'reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\MtoA2016" /f'



print ('sys.argv:{}'.format(sys.argv))
if __name__=='__main__':
    try:
        print('执行函数->:{}\n'.format(sys.argv[1]))
        exStr=sys.argv[1]
        if not exStr.endswith(')'):
            exStr+='()'
        print ('系统变量->:{}\n'.format(sys.argv))

        print('\n')
        exec (exStr)
    except Exception as ex:
        print(traceback.format_exc())
        print ('run_{}'.format(__file__))
        time.sleep(100)
        pass

