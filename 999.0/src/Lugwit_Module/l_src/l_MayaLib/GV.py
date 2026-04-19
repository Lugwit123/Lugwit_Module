# -*- coding: utf-8 -*-

import copy
import subprocess,math
import maya.cmds as cmds
from maya.cmds import *
def allOrSel(tr=0):
    Obj=[]
    if cmds.checkBox('allOrSel',q=1,value=1)==1:
        if tr==1:
            allObj=cmds.ls(filterExpand(cmds.ls(tr=1),sm=12))
        if tr==0:
            allObj=[]
            for x in cmds.filterExpand(ls(tr=1),sm=12):
                if cmds.nodeType(x)=='mesh':
                    allObj.append(x)
                else:
                    x=cmds.listRelatives(x,s=1)[0] 
                    allObj.append(x)
        Obj=allObj
    if cmds.checkBox('allOrSel',q=1,value=1)==0:
        if cmds.ls(sl=1)!=[]:
            if tr==1:
                selObj=cmds.ls(filterExpand(cmds.ls(sl=1),sm=12))
            if tr==0:
                selObj=[]
                for x in cmds.filterExpand(cmds.ls(sl=1),sm=12):
                    if cmds.nodeType(x)=='mesh':
                        selObj.append(x)
                    else:
                        x=cmds.listRelatives(x,s=1)[0] 
                        selObj.append(x)
            Obj=selObj
    return list(set(Obj))


  
def allNode():
    Obj=[]
    if cmds.checkBox('allOrSel',q=1,value=1)==1:
        Obj=cmds.ls()
    elif cmds.checkBox('allOrSel',q=1,value=1)==0:
        Obj=cmds.ls(sl=1)
    return Obj
def getClosestPointF(obj,pos1):#getClosestPoint(cmds.ls(sl=1)[0],[20,20,20])
    distance=[]
    reNormalprecision=float(cmds.intFieldGrp( 'reNormalprecision',q=1,v1=1))
    vervexNum=obj.numVertices()
    interval=int(math.ceil(vervexNum/50.0))
    for i in range(0,vervexNum,interval):
        vec=Array(pos1)-Array(xform(obj.vtx[i],t=1,q=1,ws=1))
        distance.append(vec.length())
    print (distance.index(max(distance)))
    index=distance.index(max(distance))*interval
    #select(obj.vtx[index])
    return distance[distance.index(max(distance))],index  

def getSG(obj):
    try:
        obj=cmds.listRelatives(obj,s=1)
    except:
        pass
    shader=listConnections(obj,type='shadingEngine')
    return list(set(shader))
    #shader=listConnections(shader)
    #mat=list(set(ls(shader,mat=1)))
def getMat(obj):
    try:
        obj=cmds.listRelatives(obj,s=1)
    except:
        pass
    try:
        shader=listConnections(obj,type='shadingEngine')
        shader=[listConnections(s+'.surfaceShader') for s in shader]
        mat=list(set(ls(shader,mat=1)))
        return mat
    except:
        return []
def getFilePath(obj):
    mat=getMat(obj)
    File=listConnections(mat,s=1,type='file')
    filePath=[]
    for f in File:
        f=getAttr( f.fileTextureName)
        filePath.append(f)
    return filePath
    
def getFilePathFromMat(mat):
    File=cmds.listConnections(mat,s=1,type='file')
    filePath=[]
    for f in File:
        f=cmds.getAttr( f.fileTextureName)
        filePath.append(f)
    return filePath
  
def copy2clip(txt):
    cmd='echo ' + txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def Process():
	
	start='''
minPro=0
global gMainProgressBar,proStatus
proStatus=''
if 'forceAll' not in locals().keys():
	if cmds.ls(sl=1)==[] and checkBox('allOrSel',q=1,value=1)==0:
		confirmDialog(message="请先选择物体或者勾选所有物体选项",button="确定",defaultButton="确定",cancelButton="确定",dismissString="确定")
		sys.exit(1)
import time,math
global exExplain,leng,starttime,_pro,gMainProgressBar
exExplain='';leng=0
try:
	leng=len(Obj)
except:
	pass
_pro=0
starttime=time.time()
global gMainProgressBar 
gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')
cmds.progressBar( gMainProgressBar,
		edit=True,
		beginProgress=True,
		isInterruptable=True,
		maxValue=100 )
'''

	pro='''
global gMainProgressBar,proStatus,_pro
import subprocess
_pro+=1
timeDiff=time.time()-starttime
v=_pro/(timeDiff)+0.001

pro=int(math.ceil (100.0*_pro/  leng  )   )
proStatus='剩余时间: '+str( leng/v-(timeDiff))+'秒 '+'循环次数: '+str(_pro)+'/'+str(leng)+' 附加说明：'+str(exExplain)
cmds.progressBar( gMainProgressBar, edit=True, pr=pro ,status=proStatus )
if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ) and timeDiff>4:
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	cmds.error('结束进程')
	sys.exit(1)
'''

	end='''
cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
print time.time()-starttime,'耗时（s）'  '''
	editexExplain='''
minPro+=0.5
cmds.progressBar( gMainProgressBar, edit=True ,status=proStatus ,pr=pro+minPro)
minPro-=0.5'''
	return start,pro,end,editexExplain
def __dir__():
    pass

def __dict__():
    pass
