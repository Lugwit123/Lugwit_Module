# -*- coding: utf-8 -*-
import sys,os,re
def get_maya_arnoldVersion(mayaFile):
    MayaVersion,arnoldVersion='2018','402'
    if os.path.exists(mayaFile):
        with open(mayaFile,'rb') as f:
            f_read=f.read(5000)
            f_read=str(f_read)
            arnoldVersion_match=re.search('"mtoa" "(\d+.\d+.\d+)',f_read,re.M|re.S)
            arnoldVersion = arnoldVersion_match.group(1) if arnoldVersion_match else arnoldVersion
            
            MayaVersion_match=re.search('requires maya "(\d+)',f_read,re.M|re.S)
            MayaVersion = MayaVersion_match.group(1) if MayaVersion_match else MayaVersion
            MayaVersion='Maya'+MayaVersion

    return MayaVersion,arnoldVersion

if __name__ == "__main__":
    mayaFile=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP123\Animation\scenes&movies\CW_EP123_SC157_an.ma'
    print (get_maya_arnoldVersion(mayaFile))