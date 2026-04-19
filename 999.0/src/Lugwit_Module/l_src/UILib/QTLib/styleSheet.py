# coding:utf-8
#代码加密
import os,sys,codecs,glob
fileDir=os.path.dirname(__file__)
qssDir=fileDir+'/QSS'
qssFiles=glob.glob(qssDir+'/*.qss')
for qssfile in qssFiles:
    with codecs.open (qssfile,'r',encoding='utf8') as f:
        #self_qss=f.read().replace('qssDir',fileDir+'/QSS').replace('\\','/')
        qssfileBaseName=os.path.basename(qssfile).rsplit('.',1)[0]
        locals()[qssfileBaseName]=f.read().replace('qssDir',fileDir+'/QSS').replace('\\','/')
        
__all__=['self_qss']



