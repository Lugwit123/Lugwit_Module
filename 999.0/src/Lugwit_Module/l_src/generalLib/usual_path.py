# -*- coding: utf-8
#添加模块所在路径
import os,re,sys,time
import trace
import traceback


l_srcDir = re.search('.+l_src',__file__).group(0)
sys.path.append(l_srcDir)
from usualFunc import lprint
fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)

runTime=0


import getpass

import time

import random

import socket


from shutil import copyfile


from imp import reload




def getDocPath():
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Personal")[0]

def getLocalDisc():
    import psutil
    return [list(x)[0][0] for x in psutil.disk_partitions()]


def getUserProfile():
    return os.environ['HOME']


def getInfoFromMayaFilePath(mayaFile,getInfofromFileName=False,
                            isAssetOrShotFile=1,nameSpace='sdasd_Rig',**kwargs):                         
    '''
    返回值 mayaFileNameExt,mayaFileName,proName,ProjectName,shotPath,shotName,AssetType,AssetStep
    #e:\BUG_Project\B024\Asset_work\chars\Rig\B024_chars_luola_rig.fbx
    mayaFile=e:\BUG_Project\B024\Shot_work\Ani\shot_01\B024_Ani_shot01.ma
    返回('B024_Ani_shot01.ma', 'B024_Ani_shot01','B024', 'e:/BUG_Project/B024/', 'e:/BUG_Project/B024/Shot_work/Ani/shot_01/', 'shot01')
    #   mayaFileNameExt,mayaFileName,proName,ProjectName,shotPath,shotName
    #e:\BUG_Project\B003_S78\Shot_work\Layout\shot16\wlxx_sc016_1_lay.ma
    '''
    # 芭阁动漫 命名方式  ,镜头文件夹 (shot_*[0-9]{2,3}) 资产文件夹 Asset_work 镜头文件夹Shot_work
    # 懒人猫项目OP_WX ,镜头文件夹 shotIndex='sc[0-9]{1,3}_cut[0-9]{1,4}' 资产文件夹 Asset 镜头文件夹Shot
    # lprint (mayaFile)
    # lprint (locals())  # 注释掉通用日志，只关注shot_full_name_split
    # 传入的数据里面的Key可能没得RegExp,这里加上
    newkwargs={}
    varValueDict={}
    for key,val in kwargs.items():
        newkwargs.setdefault(key,{}).setdefault('regEx',val['regEx'])
        newkwargs.setdefault(key,{}).setdefault('valueType',val['valueType'])

    lprint(newkwargs.get("shot_full_name_split_path"))
    reg_exps = newkwargs
    # reg_exps={
    #     'assetDirRegExp':'.+/Asset/',
    #     'ShotEpNameRegExp':'/sc[0-9]+_cut[0-9]+/',
    #     'AssetEpNameRegExp':'/Ep_*[0-9]+/',
    #     'ScNameRegExp':'/[Sc_]*[0-9]{2,3}/','AssetTypeRegExp':"/(?:Chars*|Props*|Sets*|BG*)/",
    #     'ProjectNameRegExp':'/(.+?)/[0-9_]*Main-production/',
    #     'ProjectDirRegExp':".+/pro-production/",'shotDirRegExp':'.+/sc[0-9]+_cut[0-9]+/',
    #     'AssetStepRegExp':'/(?:Chars*|Props*|Sets*)/.+?/(.+?)/',
    #     'AssetNameRegExp':'/(?:Chars*|Props*|Sets*)/(.+?)/',
    #     'ShotStepRegExp':"",'ShotNameRegExp':"/Shot_*[0-9]+/",'shotNameRegExp':'/shot_*[0-9]+/'
    # }

    
    def getValue(RegExp,isPath=0,varValueDict={},key_name=''):
        if 'unrealShotDir' == key_name:
            lprint('unrealShotDir',RegExp)
        findVarInRegExp_list=re.findall('{.+?}',RegExp,flags=re.I)
        if findVarInRegExp_list:
            for findVarInRegExp in findVarInRegExp_list:
                varValueDict_getVar=varValueDict.get(findVarInRegExp[1:-1])
                if varValueDict_getVar:
                    RegExp=RegExp.replace(findVarInRegExp,varValueDict_getVar)
        if RegExp.startswith('reg:'):
            rexList=RegExp.split('reg:')[1].split(',')
            regFunc=getattr(re,rexList[0])
            RegExpParmList=rexList[1:]
            if '{' in mayaFile:
                _mayaFile=mayaFile.split('{')[0]
            else:
                _mayaFile=mayaFile
            if rexList[0]=='sub':
                result=regFunc(RegExpParmList[0],RegExpParmList[1],_mayaFile ,flags=re.I)
                lprint(result,rexList,RegExpParmList)

        else:
            try:
                result=re.search(RegExp,mayaFile ,flags=re.I)
            except re.error as e:
                traceback.print_exc()
                lprint (RegExp,mayaFile)
                raise("正则表达式错误")
        
        if  isinstance(result,re.Match,):
            try:
                result=result.group(1)
            except:
                result=result.group()
        # 只输出shot_full_name_split相关的日志
        if key_name in ['shot_full_name_split_path', 'ShotEpName', 'ScName', 'Shot_Name']:
            lprint(key_name,RegExp,mayaFile,result)
        if not result:
            result = ''
        if not isPath:
            result=result.replace('/','')

        if not result:
            if re.search('[\*\+|]+',RegExp):
                result=''
            else:
                result=RegExp
        if 'shot_full_name_split_path' == key_name:
            lprint('shot_full_name_split_path',RegExp,key_name)
        return result

    if mayaFile.startswith('//'):
        mayaFile=mayaFile.replace('//','E:/BUG_Project/')
    
    mayaFile=mayaFile.replace('\\\\','/');#里面可能有四个'\\\\'
    mayaFile=mayaFile.replace('\\','/')
    mayaFile=mayaFile.replace('//','/')
    # lprint (u'getInfoFromMayaFilePath函数处理Maya文件：{}'.format(mayaFile))
    
    mayaFileNameExt = os.path.basename(mayaFile)
    mayaFileName=os.path.splitext(mayaFileNameExt)[0]
    assetDir=os.path.dirname(mayaFile)
    #从Maya文件名中获取项目名
    
    returnDict={}

    for key,RegExpDict in reg_exps.items():
        RegExp=RegExpDict['regEx']
        valueType=RegExpDict['valueType']

        if RegExp.startswith('py:'):
            pyCode=RegExp.split('py:')[1]
            pyCode_list=pyCode.rsplit(';',maxsplit=1)
            exec(pyCode_list[0],globals(),locals())
            RegExp=eval(pyCode_list[1])

        elif RegExp.startswith('fromNameSpace') and nameSpace:
            ex=RegExp.split('fromNameSpace:')[1]
            RegExp=re.search(ex,nameSpace,flags=re.I)
            if RegExp:
                RegExp=RegExp.group()
            else:
                RegExp=''

            
        
        key_name=key
        if valueType=='常量':
            returnDict[key_name]=RegExp
            continue

                
        isPath=0
        if re.search('(Dir|path)$',key,flags=re.I):
            isPath=1
        if isAssetOrShotFile==1 and key_name.startswith('Asset'):
            returnDict[key_name]=''
        else:
            if RegExp.startswith('content:'):
                matchResult=RegExp
            else:
                matchResult=getValue(RegExp,isPath,varValueDict,key_name)
            varValueDict[key_name]=matchResult
            #lprint ('key,RegExp,matchResult,key_name : ',key,RegExp,matchResult,key_name)
            returnDict[key_name]=matchResult

    lprint(returnDict.get("shot_full_name_split_path"))
    if re.search(reg_exps['AssetDir']['regEx'],mayaFile ,flags=re.I):
        returnDict['workType']='Asset'
    else:
        returnDict['workType']='Shot'
    if 'shotName' not in returnDict:
        returnDict['shotName']=''
    ShotEpName,ScName,shotName=returnDict['ShotEpName'],returnDict['ScName'],returnDict['shotName']
    lprint('ShotEpName,ScName,shotName',ShotEpName,ScName,shotName)
    FinalShotName='_'.join([x for x in [ShotEpName,ScName,shotName] if x])
    lprint('FinalShotName',FinalShotName)
    returnDict['FinalShotName']=FinalShotName

    return returnDict
if __name__ == '__main__':
    mayaFile=r'e:\BUG_Project\B024\Shot_work\Ani\shot_01\B024_Ani_shot01.ma'
    mayaFile=r'e:\BUG_Project\B003_S78\Shot_work\Layout\shot16\wlxx_sc016_1_lay.ma'
    mayaFile=r'e:\BUG_Project\B018\Asset_work\chars\Texture\NvDiA\NvDi_HuangZhuang_A_.ma'
    mayaFile=r'E:/BUG_Project/B017_6RW/Asset_work/Sets*/env/B017_6_sets_env_Mod_v002.ma'
    mayaFile=r'e:\BUG_Project\Test\Asset_work\chars\NvDi\Texture\HuangZhuangA.ma'
    mayaFile=r'e:\BUG_Project\Test\Asset_work\chars\Texture\NvDi\HuangZhuangA.ma'
    mayaFile=r'e:\BUG_Project\Test\Asset_work\chars\Texture\NvDi.ma'
    mayaFile=r'S:\BUG_Project\U37\Shot_work\Animation\01\Shot09\approve\U37_Shot09_Animation_final.ma'
    mayaFile=r'X:\OP_WX\pro-production\Shot\Animation\sc01_cut0010\publish\OP_WX_CG_sc01_cut0010_ani.ma'
    #mayaFile=r'S:\BUG_Project\B017b11\Shot_work\Animation\Sc01\Shot02\approve\B017b11_cam02_Animation_final.ma'
    
    #
    # shotInfo=getInfoFromMayaFilePath(mayaFile,getInfofromFileName=0,)
    # lprint ('shotInfo',shotInfo)
    # shotInfo=getInfoFromMayaFilePath(r'X:/OP_WX/pro-production/Asset/Chars/C001_WX/Rig/work/C001_WX_Rig.ma',getInfofromFileName=0,)
    # lprint ('shotInfo',shotInfo)

    #/[0-9]+_episode/
    mayaFile=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP123\Animation\scenes&movies\CW_EP123_SC157_an.ma'
    mayaFile=r'Z:/Cosmos_Wartale2/03_Main-Production/01_episode/CH/CH_NEZHA/CH_NEZHA.ma'
    mayaFile=mayaFile.replace('\\','/')
    
    # shotInfo=getInfoFromMayaFilePath(mayaFile,getInfofromFileName=False,
    #                         assetDirRegExp='.+/[0-9]+_episode',shotDirRegExp='.+/[0-9_]+_animation/', 
    #                         ShotEpNameRegExp='/Ep_*[0-9]+/',
    #                         AssetEpNameRegExp='/Ep_*[0-9]+/',
    #                         ScNameRegExp='sc[0-9]+[a-z]*',AssetTypeRegExp="/(?:CHS*|PRPS*|Sets*)/",
    #                         ProjectNameRegExp='/(.+?)/[0-9_]*Main-production/',
    #                         ProjectDirRegExp=".+/[0-9_]*Main-production",
    #                         AssetStepRegExp='',
    #                         AssetNameRegExp='/(?:CH|PRP|Set|BG)/(.+?)/',ShotStepRegExp='Ep_*[0-9]+/(.+?)/')
    # mayaFile=r"Z:\test_project\03_Main-Production\01_episode\CH\CH_NvDi\CH_NvDi.ma"
    # shotInfo=getInfoFromMayaFilePath(mayaFile,getInfofromFileName=False,
    #                         assetDirRegExp='.+/[0-9]+_episode/',shotDirRegExp='.+/[0-9_]+_animation/', 
    #                         ShotEpNameRegExp='/Ep_*[0-9]+/',
    #                         AssetEpNameRegExp='/Ep_*[0-9]+/',
    #                         ScNameRegExp='sc[0-9]+',AssetTypeRegExp="/(?:CHS*|PRPS*|Sets*)/",
    #                         ProjectNameRegExp='/(.+?)/[0-9_]*Main-production/',
    #                         ProjectDirRegExp=".+/[0-9_]*Main-production",
    #                         AssetStepRegExp='',
    #                         AssetNameRegExp='/{AssetType}/(.+?)/',ShotStepRegExp='Ep_*[0-9]+/(.+?)/')
    # lprint (shotInfo)
    
    # =============================================
    # 测试 shot_full_name_split_path:{ShotEpName}/{ScName}/{Shot_Name} 的解析过程
    # =============================================
    
    print("\n" + "="*60)
    print("开始测试 shot_full_name_split_path 变量的解析过程")
    print("="*60)
    
    # 使用一个包含镜头信息的Maya文件路径进行测试
    test_mayaFile = r"G:/WXXJDGD/13.CFX/ep001/ep001_sc001_shot0150/ep001_sc001_shot0150_C_LiWuWang_cfx.ma"
    
    # 定义测试用的正则表达式配置（模拟从JSON配置文件来的数据）
    test_kwargs = {
        'ShotEpName': {
            'regEx': r'/(ep[0-9]+)/',
            'valueType': '正则表达式'
        },
        'ScName': {
            'regEx': r'_(sc[0-9]+)_',
            'valueType': '正则表达式'
        },
        'Shot_Name': {
            'regEx': r'_(shot[0-9]+)/',
            'valueType': '正则表达式'
        },
        'shot_full_name_split_path': {
            'regEx': '{ShotEpName}/{ScName}/{Shot_Name}',
            'valueType': '正则表达式'
        },
        # 添加一些基础配置以避免KeyError
        'AssetDir': {
            'regEx': r'/Asset/',
            'valueType': '正则表达式'
        },
        'shotName': {
            'regEx': r'shot([0-9]+)',
            'valueType': '正则表达式'
        }
    }
    
    print("测试文件路径: {}".format(test_mayaFile))
    print("shot_full_name_split模板: {}".format(test_kwargs['shot_full_name_split_path']['regEx']))
    print("\n开始解析...")
    
    try:
        # 调用函数进行解析
        result = getInfoFromMayaFilePath(
            test_mayaFile, 
            getInfofromFileName=False,
            isAssetOrShotFile=1,
            nameSpace='test_Rig',
            **test_kwargs
        )
        
        print("\n解析结果:")
        print("-" * 40)
        # 首先显示所有相关的解析结果
        for key, value in result.items():
            if key in ['ShotEpName', 'ScName', 'Shot_Name', 'shot_full_name_split_path', 'shotName']:
                print("{:20}: {}".format(key, value))
        
        print("\n完整解析结果:")
        print("-" * 40)
        for key, value in sorted(result.items()):
            print("{:25}: {}".format(key, value))
        
        print("\n详细解析过程:")
        print("-" * 40)
        print("ShotEpName    : {}".format(result.get('ShotEpName', 'NOT_FOUND')))
        print("ScName        : {}".format(result.get('ScName', 'NOT_FOUND')))
        print("Shot_Name     : {}".format(result.get('Shot_Name', 'NOT_FOUND')))
        print("最终结果      : {}".format(result.get('shot_full_name_split_path', 'NOT_FOUND')))
        
        # 手动验证模板替换逻辑
        template = "{ShotEpName}/{ScName}/{Shot_Name}"
        manual_result = template.format(
            ShotEpName=result.get('ShotEpName', ''),
            ScName=result.get('ScName', ''),
            Shot_Name=result.get('Shot_Name', '')
        )
        print("手动计算结果  : {}".format(manual_result))
        
        # 比较结果
        if result.get('shot_full_name_split_path') == manual_result:
            print("✅ 解析结果正确!")
        else:
            print("❌ 解析结果不匹配!")
            
    except Exception as e:
        print("❌ 解析过程中发生错误: {}".format(str(e)))
        traceback.print_exc()
    
    print("="*60)
    print("shot_full_name_split_path 测试完成")
    print("="*60)
    
    # =============================================
    # 添加一个简化的测试用例
    # =============================================
    print("\n" + "="*50)
    print("简化测试：手动验证变量替换逻辑")
    print("="*50)
    
    # 模拟已解析的基础变量
    mock_variables = {
        'ShotEpName': 'PV02',
        'ScName': 'sc01', 
        'Shot_Name': 'shot011'
    }
    
    # 模拟shot_full_name_split的模板
    template = "{ShotEpName}/{ScName}/{Shot_Name}"
    
    print("模板: {}".format(template))
    print("变量: {}".format(mock_variables))
    
    # 手动替换测试
    try:
        result = template.format(**mock_variables)
        print("替换结果: {}".format(result))
        
        # 验证是否符合预期
        expected = "PV02/sc01/shot011"
        if result == expected:
            print("✅ 手动测试通过!")
        else:
            print("❌ 期望: {}, 实际: {}".format(expected, result))
            
    except Exception as e:
        print("❌ 手动测试失败: {}".format(str(e)))
    
    print("="*50)

