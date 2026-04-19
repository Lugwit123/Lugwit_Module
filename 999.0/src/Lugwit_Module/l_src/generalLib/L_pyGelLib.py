# -*- coding: utf-8
from __future__ import print_function
#添加模块所在路径
import os,re,sys,time,json
fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)



import codecs,traceback
runTime=0

import os
import sys
import re
import time
import random

import codecs
import traceback
from shutil import copyfile



from pprint import pprint


import getRefList
try:
    import _winreg as winreg
except:
    import winreg
from imp import reload
sysModule = sys.modules

try:
    import P4Lib
except:
    pass



def combineMap():
    import maya.cmds as cmds
    fileNodes = cmds.ls(type='file')
    # fileNodes=['ONEMT_set_zhanchang_MOD:pasted__MapFBXASC032FBXASC035321499311']
    for fileNode in fileNodes:
        fileNodeOut = cmds.listConnections(fileNode+'.outColor')
        if fileNodeOut:
            if len(fileNodeOut) > 1:
                try:
                    mats = fileNodeOut
                    sgs = [cmds.listConnections(mat, type='shadingEngine')[
                        0] for mat in mats]
                    cmds.select(sgs)
                    cmds.sets(cmds.ls(sl=True), e=True, forceElement=sgs[0])
                except:
                    pass
    sgs = cmds.ls(type='shadingEngine')
    mats = [cmds.listConnections(x+'.surfaceShader')[0] for x in sgs]
    for mat in mats:
        try:
            FileNode = cmds.listConnections(mat+'.color')
        except:
            try:
                FileNode = cmds.listConnections(mat+'.baseColor')
            except:
                continue
        print('FileNode', FileNode)
        if FileNode:
            FileNode = FileNode[0]
            if not cmds.attributeQuery('ftn', node=FileNode, ex=1):
                continue
            cMap = cmds.getAttr(FileNode+'.ftn')
            convertDir = os.path.dirname(cMap)+'/Convert'
            if not os.path.exists(convertDir):
                os.makedirs(convertDir)
            newcMap = convertDir+'/T_'+mat+'_BC.'+cMap.split('.')[1]
            #newPath = convertDir+'/'+os.path.basename(cMap)
            print('mat,cMap,\n newPath', mat, cMap, newcMap)
            copyfile(cMap, newcMap)
            [1]
            # cmds.setAttr(FileNode+'.ftn', newcMap, type='string')
            if not os.path.exists(newcMap):
                #os.rename(newPath, newcMap)
                try:
                    cmds.rename(FileNode, mat+'_BaseColor')
                    cmds.select(mat)
                except:
                    pass

            # ???????????
            checkMapDict = {'Roughness': 'Roughness',
                            'Normal': 'N', 'Metallic': 'Metallic'}
            keyList = checkMapDict.keys()
            for texture in keyList:
                #checkMap = cMap.replace('BaseColor', texture)
                pattern = cMap.split('_')[-1]
                checkMap = re.sub(pattern, texture+'.' +
                                  cMap.split('.')[-1], cMap, flags=re.IGNORECASE)
                print('checkmap,', checkMap)
                newPath = newcMap.replace('BC', checkMapDict[texture])
                if os.path.exists(checkMap):
                    copyfile(checkMap, newPath)

            # bumpNode = cmds.listConnections(mat+'.normalCamera')
            # if bumpNode:
            #     bumpNode = bumpNode[0]
            #     fileNode = cmds.listConnections(bumpNode+'.bumpValue')[0]
            #     fileMap = cmds.getAttr(fileNode+'.ftn')
            #     print fileMap
            #     newFileMap = convertDir+'/T_'+mat+'_N.'+cMap.split('.')[1]
            #     cmds.setAttr(fileNode+'.ftn', newFileMap, type='string')
            #     if not os.path.exists(newcMap):
            #         os.rename(fileMap, newFileMap)
            #         try:
            #             cmds.rename(fileNode, mat+'_NormalMap')
            #             cmds.rename(bumpNode, mat+'_bump2d')
            #         except:
            #             pass


def getDocPath():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Personal")[0]


def getUserPath():
    print('----------')
    return os.popen("echo %USERPROFILE%").read().replace('\\', '/')[:-1]





class Lugwit_Socket():
    def __init__(self):
        import  socket
        pass

    def getFreePort(self, ip='127.0.0.1'):
        while 1:
            randint = random.randint(1025, 10000)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((ip, randint))
            s.close()
            if result:
                print('port:{},result:{}'.format(randint, result))
                return randint


def getIPAddr():
    import socket

    hostname = socket.gethostname()

    ip = socket.gethostbyname(hostname)
    return ip

def getAllChildPath(path,fileType=''):
    import os
    print ('path',path)
    specifyTypePathList=[];allTypePathList=[]
    if isinstance(path,str):
        pathList=[path]
    else:
        pathList=path
    for path in pathList:
        for root, dirs, files in os.walk(path):
            for file in files:
                genAbsPath=os.path.join(root, file).replace('/','\\')
                if os.path.splitext(file)[1] in  fileType:
                    specifyTypePathList.append(genAbsPath)
                allTypePathList.append(genAbsPath)
    return specifyTypePathList,allTypePathList

def readXgenFile(xgenFile=r'D:\aa\bb__collection3.xgen'):
    with codecs.open (xgenFile,'r',encoding='utf8',errors='ignore') as f:
        if xgenFile.endswith('.xgen'):
            print( u'读取.xgen文件{}'.format(xgenFile))
            f_read=f.read()
            xgDataPath=re.search('xgDataPath\s+(.+)\r*\n',f_read).group(1)
            xgProjectPath=re.search('xgProjectPath\s+(.+)\r*\n',f_read).group(1)
            if xgDataPath.startswith('${PROJECT}'):
                xgDataPath=xgProjectPath+xgDataPath.replace('${PROJECT}','')
            print ('xgDataPath-->',xgDataPath,end='=========')
            return xgDataPath
    
def getMayaFileContents(mayaFile=''):
    try:
        with open(mayaFile, 'r',errors='ignore') as f:
            return f.read()
    except Exception as e:
        print (u'整体打开Maya文件失败：{},原因是{}'.format(mayaFile,e))
        
    try:
        mayaFileContents=''
        openMayaFile=codecs.open(mayaFile,'r',encoding='gbk',errors='ignore')
        index=0
        while 1:
            readPart=openMayaFile.read(500000)
            if not readPart:
                openMayaFile.close()
                break
            mayaFileContents += readPart
            # index+=50000
            # print (index)
    except Exception as e:
        print ('e',e)
        try:
            openMayaFile.close()
        except:
            pass
    return mayaFileContents

#获取xgen文件的路径和xgen文件夹的路径
def getXgenInfoFromMayaFile(mayaFile='',mayaContent=''):
    mayaFileName=os.path.basename(mayaFile)
    mayaFileBaseName=os.path.splitext(mayaFileName)[0]
    mayaFileDir=os.path.dirname(mayaFile)
    xgenFileList=[]
    xgDataPathList=[]
    patcheFileList=[]
    # 获取.xgen文件的路径
    if mayaContent:
        xgenFileList=re.findall('setAttr ".xfn" -type "string" "(.+)";',mayaContent,flags=re.I)
    else:
        try:
            xgenFileList+=[x[0] for x in P4Lib.getFile(mayaFile.rsplit('.ma',1)[0]+'__*') if x]
        except Exception as e:
            pass
        for file in os.listdir(mayaFileDir):
            if file.startswith(mayaFileBaseName+'__'):
                if file.endswith('.xgen'):
                    xgenFileList.append(file)
    
    # 获取patche .abc文件路径列表,用于渲染
    fileInLocalDir=os.listdir(mayaFileDir)
    fileInDir=fileInLocalDir

        
    for file in fileInDir:
        if file.startswith(mayaFileBaseName+'__'):
            if file.endswith('.abc'):
                file=file.replace('\\','/')
                patcheFileList.append(file)
        # 获取p4上的abc文件
        
    print ('xgenFileList',xgenFileList)
    for i,xgenFile in enumerate(xgenFileList):
        fullPath=os.path.join(mayaFileDir,xgenFile).replace('\\','/')
        print ('----------------------------fullPath',fullPath)
        P4Lib.getFile(fullPath)
        if os.path.exists(fullPath):
            xgDataPathList.append(readXgenFile(fullPath))
            xgenFileList[i]=fullPath

    xgDataPathList=list(set(xgDataPathList))
    patcheFileList=list(set(patcheFileList))
    return xgenFileList,xgDataPathList,patcheFileList


def getRefFileListFromMa(path='',syncFile=1,onlyGetMayaFile=0,updateMayaFile=1):  # 获取Maya文件里面的所有路径,包括子级的maya文件里面的路径
    
    print (json.dumps(locals(),indent=4,ensure_ascii=False))
    st=time.time()
    path=path.replace('\\','/')
    path=path.replace('\\\\','/')
    import loginP4
    global p4
    p4=loginP4.p4_login()
    P4Lib.p4=p4
    if updateMayaFile:
        P4Lib.getFile(path)
    imageFormatList=['jpg','jpeg','png','tif','tiff','tga','bmp','exr','psd','hdr','pic','tga','tx','iff']
    
    allPathList, allMayaList = [[]], [[]]
    allSecFileList=[];#这个之所以不是[[]]是因为这个列表只用来append单个文件
    UdimTexturesList=[[]];#这个之所以是[[]]是因为这个列表要+=list
    def getPathListInFile(child_path=path):
        # nonlocal allPathList  python3?÷?
        # python2要实现访问上级函数变量可以使用函数里面的第0个元素加上一个数的方法
        child_path = child_path.replace('\\', '/')
        child_path = child_path.replace('//', '/')
        child_path=child_path[0].upper()+child_path[1:]
        print ('child_path',child_path)
        #mayaFileContents=getMayaFileContents(child_path)
        #print (u'打开引用文件耗费时间{}'.format(time.time()-st))
        #secList = list(set(re.findall('\s.*"([a-z]:[^\"]+)', mayaFileContents,flags=re.I)))
        #secList = list(set(re.findall('\s.{0,1}"([a-z]:[/\\\\][^\"]+)', mayaFileContents,flags=re.I|re.M)))
        secList=getRefList.getRefFileListInMayaFile_MultiProcess(child_path)
        print (u'获取引用文件耗费时间{}_引用文件数量为{}'.format(time.time()-st,len(secList )))
        if not onlyGetMayaFile:
            if child_path.endswith('.ma'):
                mayaFileDir=os.path.dirname(child_path)
                if syncFile:
                    P4Lib.getFile(mayaFileDir,fileTypes=['abc','.xgen'])
                #print ('mayaFileContents',mayaFileContents[-200:])
                xgenFileList,xgDataPathList,patcheFileList=getXgenInfoFromMayaFile(mayaFile=child_path)
                if xgDataPathList:
                    if syncFile:
                        P4Lib.getFile(xgenFileList)
                        P4Lib.getFile(xgDataPathList)
        allPathList[0] += secList  # 这里如果是allPathList+=secList会提示未定义这个局部变量
        for _secFile in secList:
            _secFile=_secFile.replace('\r','')
            _secFile=_secFile.replace('//','/')
            
            if _secFile in allSecFileList:
                continue
            
            if '/plug-ins/xgen/' in _secFile:
                continue
            
            if not onlyGetMayaFile:
                UdimTextures=getUdimTexture(_secFile)
                if UdimTextures:
                    UdimTexturesList[0]+=UdimTextures
                    continue

            if _secFile:
                if '.ma' in _secFile or '.mb' in _secFile:
                    print (u'找到Maya文件-->>',_secFile)
                    if re.search('{\d}$',_secFile ):
                        print (u'多次引用的maya文件{},忽略'.format(_secFile))
                        continue
                    if _secFile in allMayaList[0]:
                        continue
                    print ('_secFile',_secFile)
                    if not os.path.exists(_secFile):
                        if syncFile:
                            try:
                                if sys.version_info.major == 2:
                                    P4Lib.getFile(_secFile)
                                else:
                                    P4Lib.getFile(_secFile) 
                            except Exception as ex:
                                print(traceback.format_exc())
                    if  os.path.exists(_secFile):
                        allMayaList[0] += [_secFile]
                        if not onlyGetMayaFile:
                            getPathListInFile(_secFile)

                allSecFileList.append(_secFile)
    
    getPathListInFile(path)
    
    allPathList=upperPathFirstPath(allPathList[0])
    allPathList = list(set(allPathList))
    print (allPathList)
    
    allMayaList=upperPathFirstPath(allMayaList[0])
    allMayaList = list(set(allMayaList))
    
    UdimTexturesList=upperPathFirstPath(UdimTexturesList[0])
    UdimTexturesList=list(set(UdimTexturesList))
    #检测TX文件
    txFileList=[]
    texFileList=[]
    for file in allPathList+UdimTexturesList:
        ext=os.path.splitext(file)[1]
        if  re.search(ext[1:],str(imageFormatList),flags=re.I):
            txFormat=re.sub(ext,'.tx',file,flags=re.I)
            txFileList.append(txFormat)
            texFileList.append(file)
        elif file.endswith('tx'):
            for format in imageFormatList:
                conImage=file.replace('.tx','.'+format)
                if os.path.exists(conImage):
                    txFileList.append(conImage)
                    
    allPathList+=txFileList
    allSecFileList+=txFileList
    allSecFileList =list(set(allSecFileList))
    if syncFile:
        #pprint (('UdimTexturesList-->>',UdimTexturesList))
        print (len(UdimTexturesList),'-----+++')
        P4Lib.getFile(allMayaList)
        if not onlyGetMayaFile:
            P4Lib.getFile(allSecFileList)
            P4Lib.getFile(UdimTexturesList)
        print ('\n')
    
    # print (allMayaList)
    # print (txFileList)
    # print (texFileList)
    
    return {'allPathList':allPathList,
            'allMayaList':allMayaList,
            'texFileList':texFileList
            }

def upperPathFirstPath(pathList):
    if not isinstance(pathList, list):
        pathList=[pathList]
    upperedPathList=[]
    for path in pathList:
        upperedPathList.append(path[0].upper()+path[1:])
    return upperedPathList


def getUdimTexture(UDIM_Path):
    #检测UDIM贴图
    list_files,unsolveFile=[],[]
    rearchUdim=re.search('[._]+([1-2]\d\d\d)[._]+',UDIM_Path)
    notXgenFile=not UDIM_Path.endswith('.xgen')
    isUdim='<UDIM>' in UDIM_Path or rearchUdim
    if isUdim and  notXgenFile:
        if rearchUdim:
            getGroup1=rearchUdim.group(1)
            #print (u'贴图不是1001并且{}存在,不查找udim'.format(UDIM_Path.replace(getGroup1,'1001')))
            print (int(getGroup1[-1])>1 and os.path.exists(UDIM_Path.replace(getGroup1,'1001')))
            if int(getGroup1[-1])>1 and os.path.exists(UDIM_Path.replace(getGroup1,'1001')):
                return
        for i in range(1,10):
            # 设置udim名称
            if '<UDIM>' in UDIM_Path:
                udim_expandPtathA=UDIM_Path.replace('<UDIM>','10'+str(i).zfill(2))
                udim_expandPtathB=UDIM_Path.replace('<UDIM>','20'+str(i).zfill(2))
            elif rearchUdim: 
                getGroup1=rearchUdim.group(1)
                udim_expandPtathA=UDIM_Path.replace(getGroup1,'10'+str(i).zfill(2))
                udim_expandPtathB=UDIM_Path.replace(getGroup1,'20'+str(i).zfill(2))
            list_files.append(udim_expandPtathA)
            list_files.append(udim_expandPtathB)
    #print ('list_files',list_files)
    return list_files

# path=r'e:\BUG_Project\B003_S78\Asset_work\chars\Texture\approve\Sourceimages\Wulvxunxing_BoSha_1001_BaseColor.png'
# getUdimTexture(path)
# sys.exit()

def modifyLocalPathToIP(path='', newDir=''):
    import getpass
    if not newDir:
        newDir = 'S:/DataTrans/FQQ/DeadlineRender/' + \
            os.path.basename(path)[:-3]+getpass.getuser().upper()
        if not os.path.exists(newDir):
            os.makedirs(newDir)
    ip = getIPAddr()
    getPath = getPathList(path)[1]+[path]
    print('getPath----', getPath)
    for childPath in getPath:
        print('childPath:', childPath)
        childPathName = os.path.basename(childPath)
        newPath = '/'.join([newDir, childPathName])
        print('newPath        :', newPath)
        copyfile(childPath, newPath)
        if os.path.basename(path) != childPathName:
            with open(newPath, 'r+',errors='ignore') as openMayaFile:
                mayaFileContents = openMayaFile.read()
                mayaFileContents = re.sub(
                    'e:/', '//{}/'.format(ip), mayaFileContents, flags=re.I)
                openMayaFile.seek(0)
                openMayaFile.truncate()
                openMayaFile.write(mayaFileContents)
        else:  # 处理的渲染maya文件新路径
            print(u'处理的渲染maya文件新路径')
            NewMayaRenderFile = newPath
            with open(newPath, 'r+',errors='ignore') as openMayaFile:
                mayaFileContents = openMayaFile.readlines()
                for i, mayaFileContent in enumerate(mayaFileContents):
                    searchPath=re.search('\s"[a-zA-Z]:[/\\\\].+"', mayaFileContent)
                    if searchPath:
                        if '.ma"' in searchPath.group():  # maya文件指认新盘路径
                            print('mayaFileContent(修改前)--',
                                  mayaFileContent[:-2])
                            mayaFileContent = re.sub(
                                'E:/', 'S:/', mayaFileContent, flags=re.I)
                            print('mayaFileContent(修改后)--', mayaFileContent)
                        else:  # 其他文件生成//10.0.0.x/
                            mayaFileContent = re.sub(
                                'e:/', '//{}/'.format(ip), mayaFileContent, flags=re.I)
                    mayaFileContents[i] = mayaFileContent
                openMayaFile.seek(0)
                openMayaFile.truncate()
                openMayaFile.writelines(mayaFileContents)
        print(u'第一次循环结束\n')
    return NewMayaRenderFile
    '''
    import re
    path=r'e:\BUG_Project\A_General_Library\ProjectStructure\C30\shot01\layout\C30_lay_shot01.ma'
    newDir='S:/DataTrans/FQQ/aa'
    import Lugwit_pyGeneralLib as lb
    lb.modifyLocalPathToIP(path,newDir)
    '''


def find_LUGWIT_PLUG_Path(curPath):
    import re
    curPath=curPath.replace('\\','/')
    curPath= re.findall('.+/Lugwit_plug',curPath)
    if curPath:
        return curPath[0]

if __name__=='__main__':
    pass
    st=time.time()
    path=r'S:/DataTrans/FQQ/RenderFarm/MayaFarm/1663222134/wlxx_sc019_sim_v001.ma'
    path=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP107\Animation\scenes&movies\CW_EP107_SC002_an.ma'
    # print (getRefFileListFromMa(path,syncFile=1,onlyGetMayaFile=1,updateMayaFile=1))
    # print (time.time()-st)
# import time
# st=time.time()
# specifyTypePathList,allTypePathList=getAllChildPath(r'E:\BUG_Project\B024\UE\Content')
# print('specifyTypePathList,allTypePathList',specifyTypePathList,allTypePathList)
# print ('time',time.time()-st)
# sys.exit(0)
    