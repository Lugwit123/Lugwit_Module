# -*- coding: utf-8 -*-
from __future__ import print_function
import re,os,datetime,sys,json,codecs
import copy
l_src_dir = re.search('.+Lugwit_Module/l_src', __file__.replace('\\','/')).group()
print ('l_src_dir:{}'.format(l_src_dir))
sys.path.append(l_src_dir)
from usualFunc import lprint


def getFileModifyTime(file_path=''):
    if not os.path.exists(file_path):
        return None
    # 获取文件的修改时间戳
    timestamp = os.path.getmtime(file_path)

    # 将时间戳转换为datetime对象
    modified_date = datetime.datetime.fromtimestamp(timestamp)

    # 将datetime对象转换为字符串
    formatted_date = modified_date.strftime("%Y-%m-%d %H:%M:%S")

    # 输出结果
    return formatted_date

def get_dict_nested_value(dictionary, keys):
    if not isinstance(dictionary, dict) or len(keys) == 0:
        return None
    key = keys[0]
    if key not in dictionary:
        return None
    if len(keys) == 1:
        return dictionary[key]
    return get_dict_nested_value(dictionary[key], keys[1:])

def isExFileAndRecordHistoryFunc(ExFile='',ExHistoryDict={},mayaFile='',ExHistoryFile='',refFile='',
                                query=False):
    ori_ExHistoryDict = {}
    ExFile=ExFile.replace('\\','/')
    mayaFile=mayaFile.replace('\\','/')
    refFile=refFile.replace('\\','/')
    if not ExHistoryDict:
        if os.path.exists(ExHistoryFile):
            with codecs.open(ExHistoryFile,'r','utf-8') as f:
                try:
                    ExHistoryDict=json.load(f)
                except:
                    print (u'文件{}不是json文件'.format(ExHistoryFile))
    ori_ExHistoryDict = copy.deepcopy(ExHistoryDict)
    # 确定Tpose是否重新导出看引用文件就行了
    isExFile=False
    ExFileExist=os.path.exists(ExFile)
    # lprint (u'文件{}存在:{}'.format(ExFile,ExFileExist))
    ExHistoryDict_Ori=copy.deepcopy(ExHistoryDict)
    getModifyTimeBeforeList=ExHistoryDict.get(ExFile,[]) 
    mayaFileModifyTime=getFileModifyTime(mayaFile)
    refFileModifyTime=getFileModifyTime(refFile)
    ExFileModifyTime=getFileModifyTime(ExFile)
    # lprint ('fbx文件{}修改时间:{}'.format(ExFile,ExFileModifyTime))
    # lprint ('引用文件{}修改时间:{}'.format(refFile,refFileModifyTime))
    thisModifyTimeList=[{'fbxFile':[ExFile,ExFileModifyTime],
                        'MayaAniFile':[mayaFile,mayaFileModifyTime],
                        'MayaRefFile':[refFile,refFileModifyTime]}
                        ]
    if thisModifyTimeList[0] not in getModifyTimeBeforeList:
        getModifyTimeBeforeList+=thisModifyTimeList
    ExHistoryDict.setdefault(ExFile,getModifyTimeBeforeList)
    if not ExFileExist:
        isExFile=True
    else:
        lprint (thisModifyTimeList[0])
        lprint (ExHistoryDict_Ori.get(ExFile,False))
        isExFile=thisModifyTimeList[0] not in ExHistoryDict_Ori.get(ExFile,[])

    # 写入历史文件
    
    if isExFile:
        ExHistoryFileDir=os.path.dirname(ExHistoryFile)
        if not os.path.exists(ExHistoryFileDir):
            os.system('cmd /c mkdir {}'.format(os.path.normpath(ExHistoryFileDir)))
        if not query:
            with codecs.open(ExHistoryFile,'w','utf-8') as f:
                json.dump(ExHistoryDict,f,indent=4,ensure_ascii=False)
    return isExFile,ExHistoryDict,ori_ExHistoryDict

def getExHistoryForShow(ExHistoryFile):
    if os.path.exists(ExHistoryFile):
        with codecs.open(ExHistoryFile,'r','utf-8') as f:
            try:
                ExHistoryDict=json.load(f)
            except:
                print (u'文件{}不是json文件'.format(ExHistoryFile))
    dd={}
    for fbxFile,ExHisDict in ExHistoryDict.items():
        ExHisDict=ExHisDict[0]
        for exDict in ExHisDict:
            dd.setdefault(fbxFile,'MayaAniFile:{},'
                                .format(ExHisDict["MayaAniFile"]))
            dd[fbxFile].append(i['MayaAniFile'][0])

if __name__ == '__main__':
    os.environ['Debug']='True'
    ExHistoryFile=r'D:\TD_Depot\plug_in\Lugwit_plug\TD\RenderFarm\MayaToUE\P4Triggers\ExHis\FQQ\Cosmos_Wartale_ExHistoryFile.json'
    ExFile=r'Z:\Cosmos_Wartale\03_Main-Production\01_episode\CH\EP100\CH_NEZHA\CH_NEZHA.fbx'
    mayaFile=r'Z:/Cosmos_Wartale/03_Main-Production/05_animation/EP107/Animation/scenes&movies/CW_EP107_SC002_an.ma'
    refFile=r"Z:/Cosmos_Wartale/03_Main-Production/01_episode/CH/EP100/CH_NEZHA/CH_NEZHA.ma"

    ExFile="Z:/Cosmos_Wartale/03_Main-Production/01_episode/PRP/EP107/PRP_NLMF/PRP_NLMF.fbx"
    mayaFile="Z:/Cosmos_Wartale/03_Main-Production/05_animation/EP107/Animation/scenes&movies/CW_EP107_SC002_an.ma"
    refFile="Z:/Cosmos_Wartale/03_Main-Production/01_episode/PRP/EP107/PRP_NLMF/PRP_NLMF.ma"
    aa=isExFileAndRecordHistoryFunc(ExFile=ExFile,ExHistoryDict={},mayaFile='',
                                ExHistoryFile=ExHistoryFile,refFile=refFile,query=True)
    lprint (aa[0],aa[1][ExFile.replace('\\','/')])
