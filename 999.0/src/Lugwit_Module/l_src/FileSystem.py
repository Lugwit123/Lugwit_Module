# -*- coding: utf-8
import os
#代码加密
def getAllChildPath(path,fileType=''):
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