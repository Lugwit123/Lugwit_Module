# coding=utf-8
import re,codecs,os,json
def getExInfoFromDescriptionFile(descriptionFile,exAssetType='exTpose|exAniClip'):
    with codecs.open(descriptionFile,'r',encoding='utf-8') as f:
        read_description=f.read()
        #lprint ('read_description',read_description)
    
    exInfo=re.search(exAssetType+'-->>\r\n({.+})',read_description,re.S|re.M)
    descriptionText=re.split(u'\r\nexAniClip-->>|\r\nexTpose-->>',read_description,flags=re.I|re.M)[0]
    
    if exInfo:
        #lprint ('exInfo',exInfo.group(1))
        exInfo=json.loads(exInfo.group(1))
        return exInfo,descriptionText
    
# 导出Tpose文件
def analysisFilePath(AssetFileExPath,RefFile,ExtName='.fbx',AssetType='CH|PRP|SET|Other'): 
    RefFileBaseName=os.path.basename(RefFile).rsplit('.',1)[0]
    AssetFileExName=AssetFileExPath.replace('{AssetName}',RefFileBaseName)\
                                    .replace('{AssetType}',AssetType)
    AssetFileExDir=os.path.dirname(AssetFileExName)
    os.system('cmd /c mkdir {}'.format(os.path.normpath(AssetFileExDir)))
    print ('AssetFileExName',AssetFileExName)
    TposeFile=os.path.join(AssetFileExDir,AssetFileExName+ExtName)
    return TposeFile,AssetFileExDir