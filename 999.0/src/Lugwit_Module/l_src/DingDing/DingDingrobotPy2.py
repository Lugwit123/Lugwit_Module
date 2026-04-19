# coding:utf-8
import os,subprocess,sys,time,traceback
from Lugwit_Module import *
pyfile=LugwitPath+ r'\Python\PythonLib\Perforce\P4Lib.py'
pythonExe=Lugwit_PluginPath+r'\Python\Python37\python.exe'

# from loginP4 import *
wsDir=r'E:/BUG_Project/'
#p4=P4_class(wsDir)
clientRootDir=wsDir

def checkOut(file,fileType='binary'):
    
    with open (Lugwit_PluginPath+r'\Lugwit_plug\mayaPlug\l_scripts\Data\vscodePyhonEnv.txt','r') as f:
        env=f.read()
    env=eval(env)
    if isinstance(file,str):
        fileList=[file]
    else:
        fileList=file
    for i,file in enumerate(fileList):
        file=file.replace('\\','/')
        file=file.encode('gbk')
        fileList[i]=file
        if not (file.startswith('//') or file.startswith('E:') or file.startswith('e:')):
            fileList.remove(file)
    if not fileList:
        return
    ss=r'{} {} checkOut({})'.format(pythonExe,pyfile,str(fileList).replace(' ',''))
    print (ss,'------------')
    subprocess.call(ss,cwd=r'e:\BUG_Project',env=env)
    return ss

# checkOut(r'e:\BUG_Project\addFolder\TestCleanFile.ma')
# sys.exit()
    
def getFile(file,forceGet=0,onlyGetMayaFile=0,fileType='',cleanFile=0):
    
    with open (Lugwit_PluginPath+r'\Lugwit_plug\mayaPlug\l_scripts\Data\vscodePyhonEnv.txt','r') as f:
        env=f.read()
    env=eval(env)
    if isinstance(file,str):
        fileList=[file]
    else:
        fileList=file
    for i,file in enumerate(fileList):
        file=file.replace('\\','/')
        file=file.encode('gbk')
        fileList[i]=file
        if not (file.startswith('//') or file.startswith('E:') or file.startswith('e:')):
            fileList.remove(file)
    if not fileList:
        return
    ss=r'{} {} getFile({},forceGet=0,onlyGetMayaFile={})'.format(
        pythonExe,pyfile,str(fileList).replace(' ',''),onlyGetMayaFile)
    print (ss)
    #sys.exit(0)
    subprocess.call(ss,cwd=r'e:\BUG_Project',env=env)



def submitChange(file,description,submitOption='submitunchanged'):
    if not file.startswith('//') :
        if not re.search(clientRootDir.replace('/',r'[/\\]'),file,flags=re.I):
            print (u'文件{}不在工作区{}目录下'.format(file,clientRootDir))
            print ('file not startswith // or E: or e:')
            return
    file=file.encode('gbk')
    with open (Lugwit_PluginPath+r'\Lugwit_plug\mayaPlug\l_scripts\Data\vscodePyhonEnv.txt','r') as f:
        env=f.read()
    env=eval(env)
    ss=r'{} {} submitChange(u\"{}\",description=\"{}\",submitOption=\"{}\")'.format(pythonExe,pyfile,file,description,submitOption)
    ss=ss.replace('\\\\','\\')
    print (ss,'------------')
    subprocess.call(ss,cwd=r'E:\BUG_Project',env=env)
    
# submitChange(r'e:\BUG_Project\addFolder\cc.txt',description=r'//172.21.1.2/P4Triggers/Triggers/exAniClip_wlxx_sc009_ani_v001_UE_comment.txt')
# sys.exit()
#'Z:\\plug_in/Python/Python37/python.exe Z:\\plug_in\\Lugwit_plug/Python/PythonLib/Perforce/P4Lib.py submitChange(u\\"E:/BUG_Project/B003_S78/Shot_work/UE/shot09/shot09_Cam_1001_1114.fbx\\",description=\\"//172.21.1.2/P4Triggers/Triggers/exAniClip_wlxx_sc009_ani_v001_UE_comment.txt\\",submitOption=\\"submitunchanged\\")'

if __name__=='__main__':
    pass
    file='E:/BUG_Project/B003_S78/Shot_work/UE/shot14/shot14_Cam_1001_1059.fbx'
    #checkOut(r'E:/BUG_Project/B024/Shot_work/UE/shot_03/B024_shot_03_1001_1050.mov')
    submitChange(r'E:/BUG_Project/B024/Shot_work/UE/shot_03/B024_shot_03_1001_1050.mov',description='aa')
    #checkOut(r'e:\BUG_Project\B003_S78\Shot_work\UE\shot07\shot07_Cam_1001_1024.fbx')
