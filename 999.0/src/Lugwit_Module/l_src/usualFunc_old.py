# -*- coding: utf-8
from __future__ import print_function
from __future__ import absolute_import
import collections
import os,inspect,sys,logging
from datetime import datetime
import inspect ,json,traceback,re

# Create a FrameInfo object that we can modify
if sys.version[0]=='2':
    import  _winreg as winreg
else:
    import winreg
import inspect



l_srcDir = re.search('.+l_src',__file__).group(0)
sys.path.append(l_srcDir)
sys.path.append(os.path.dirname(__file__))
isMayaEnv=lambda *args : re.search('maya.exe',sys.executable)


def getframeinfo_wrapper(frame, context=1):
    frameinfo = inspect.getframeinfo(frame)

    if context > 1 and frameinfo.code_context is not None:
        frameinfo = frameinfo._replace(code_context=frameinfo.code_context[1:])

    return frameinfo


def dynamic_import(module_path=None):
    #lprint (repr(module_path),os.path.exists(module_path))
    module_name = os.path.basename(module_path).split('.')[0]
    if sys.version_info[0] >= 3:
        import importlib.util as util
        if module_path:
            spec = util.spec_from_file_location(module_name, module_path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            import importlib
            module = importlib.import_module(module_name)
    else:
        import imp
        if module_path:
            module = imp.load_source(module_name, module_path)
        else:
            module_name_parts = module_name.split('.')
            module = __import__(module_name)
            for sub_module in module_name_parts[1:]:
                module = getattr(module, sub_module)
    return module

# 获取计算结名称
hostName=os.environ.get('COMPUTERNAME')

__all__ = ['getFileModifyTime','compare_dates','lprint','get_dict_nested_value','get_keys_by_value','dynamic_import']

def getFileModifyTime(file_path=''):
    # 获取文件的修改时间戳
    timestamp = os.path.getmtime(file_path)

    # 将时间戳转换为datetime对象
    modified_date = datetime.fromtimestamp(timestamp)

    # 将datetime对象转换为字符串
    formatted_date = modified_date.strftime("%Y-%m-%d %H:%M:%S")

    # 输出结果
    return formatted_date

def compare_dates(date_str1, date_str2, date_format = "%Y-%m-%d %H:%M:%S"):
    # 将字符串转换为datetime对象
    date1 = datetime.strptime(date_str1, date_format)
    date2 = datetime.strptime(date_str2, date_format)

    # 比较日期并返回结果
    if date1 > date2:
        return 1
    elif date1 < date2:
        return -1
    else:
        return 0

def get_dict_nested_value(dictionary, keys):
    if not isinstance(dictionary, dict) or len(keys) == 0:
        return None
    key = keys[0]
    if key not in dictionary:
        return None
    if len(keys) == 1:
        return dictionary[key]
    return get_dict_nested_value(dictionary[key], keys[1:])

def get_keys_by_value(dict_, value_to_find):
    keys_to_find = [key for key, value in dict_.items() if value == value_to_find]
    return keys_to_find




MayaExecutable=0
unrealExecutable=0
sys_executable=sys.executable
import re

if sys_executable.endswith('maya.exe'):
    import maya.cmds as cmds
    MayaExecutable=1
elif 'UnrealEditor' in sys_executable:
    unrealExecutable=1
TempDir=os.environ.get('Temp')



# 改函数主要用于debug,能显示打印信息是在哪一个模块的哪一个函数的哪一行,该库已上传到pypi
def lprint(*args,**kwargs):
    import os
    if args==['\n']:
        return
    has_debug = hasattr(lprint, 'debug')
    if os.getenv('isTriggerEnv',None):
        os.system(u'cmd /c echo {}'.format(args))
        return
    if has_debug:
        if lprint.debug in set(('noprint','no print')):
            debug = False
        elif lprint.debug == 'pureprint':
            debug = 'pureprint'
        elif lprint.debug == False:
            debug = False
        else:
            debug = True
    elif not has_debug:
        if os.environ.get('Lugwit_Debug') in set(('noprint','no print')):
            debug = False
        elif os.environ.get('Lugwit_Debug')=='pureprint':
            debug = 'pureprint'
        else:
            debug = True

    elif unrealExecutable:
        pass
        # if hostName!='FQQ':
        #     with open (TempDir+'/unreal.debug','r') as f:
        #         cur_val_int=int(f.read())
        #         if not cur_val_int:
        #             return


    if debug == False:
        return
    if debug =='pureprint':
        try:
            args=json.dumps(args,ensure_ascii=False,indent=4)
            print (u'--{}--'.format(args))
        except Exception as e:
            print (u'--{}--{e}'.format(args,e[-10:]))
        return
    
    debug_self = kwargs.get('debug_self',None)
    try:
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        caller_info = inspect.getframeinfo(caller_frame)
    except:
        return
    
    
    code_context=caller_info.code_context or ''
    # print ('code_context',code_context)
    caller_lineno=caller_frame.f_lineno
    filename = caller_info.filename
    function = caller_info.function
    #inspect.getframeinfo(caller_frame).code_context
    baseName=os.path.basename(filename).rsplit('.',1)[0]
    caller_lineno_ori=-1
    if code_context:
        if debug_self:
            print (code_context,caller_lineno)
        code_context=code_context[0].strip()


    else:
        try:
            if '<' not  in baseName:
                if debug_self:
                    print ("code_context_file->",baseName+'_code_context')
                moduleName=__import__(baseName+'_code_context')
                code_contextDict=moduleName.code_contextDict
                if 'Lugwit_Module' not in str(moduleName):
                    caller_lineno_ori=caller_lineno-10
                else :
                    caller_lineno_ori = caller_lineno
                code_context=code_contextDict.get(caller_lineno_ori,'')
                if debug_self:   
                    print ('code_contextDict->',code_contextDict)
                    print ("moduleName->",moduleName)
                    print ("caller_lineno_ori->",caller_lineno_ori)
        except :
            pass
            #print (traceback.print_exc())
    if  caller_lineno_ori==-1:
            caller_lineno_ori=''
        
    if sys.version[0]=='2':
        code_context = code_context.decode('utf-8')
        
    # args=stringify_non_serializable(args) 
    
    #Qprint (args)
    try:
        args=json.dumps(args,
                        ensure_ascii=False,
                        indent=4,
                        sort_keys=True,
                        default=str)
    except:
        traceback.print_exc()
        try:
            print (args)
            print (u"json字符串错误,程序继续运行")
        except:
            print (u"lprint 函数运行出错,忽略运行这个函数,错误原因如下...")
            traceback.print_exc()
        return

    args=args[2:-1]
    if '\\x' in repr(args):
        try:
            args = args.decode('gbk')
        except:
            pass
    args=u'\n{args}   {currentTime}----code_context : {code_context} \nFile: {filename}:{caller_lineno}, {caller_lineno_ori},-fn: {funcName},-callBy'\
                        .format(args=args,\
                                currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),\
                                code_context=code_context,\
                                filename=filename,\
                                caller_lineno=caller_lineno,\
                                caller_lineno_ori=caller_lineno_ori,
                                funcName=function)
    sep=u''
    if 'oneLine' in kwargs:
        sep= ' '
    if unrealExecutable:
        import unreal
        unreal.log(args)
    else:
        pass
        print(args)

def convertToUnicode_py2(_string):
    try:
        if isinstance(_string, unicode):
            return _string  # 已经是 Unicode，无需转换
        elif isinstance(_string, str):
            try:
                return _string.decode('utf-8')  # 尝试用 utf-8 解码
            except UnicodeDecodeError:
                try:
                    return _string.decode('gbk')  # 尝试用 gbk 解码
                except UnicodeDecodeError:
                    print (u'作为最后的手段，尝试用 latin1 解码')
                    return _string.decode('latin1')  # 作为最后的手段，尝试用 latin1 解码
        else:
            return str(_string)  # 对于其他类型，转换为字符串，然后解码为 Unicode
    except:
        print (traceback.print_exc(),end='@@')   
        return _string


def convertToUnicode(_string):
    if sys.version_info[0] == 2:
        return convertToUnicode_py2(_string)
    else:
        return str(_string)  # 在 Python 3 中，所有字符串都是 Unicode


def stringify_non_serializable(obj,current_depth=0):
    if current_depth > 999:
        return str(obj)  # 或者返回一些表示深度过大的标记
    if isinstance(obj, dict):
        return {convertToUnicode(k): stringify_non_serializable(v,current_depth+1) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [stringify_non_serializable(v,current_depth+1) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(stringify_non_serializable(v,current_depth+1) for v in obj)
    elif isinstance(obj, (int,float)):
        return obj
    elif obj == None:
        return None
    elif isinstance(obj, BaseException):
        return str(obj) if sys.version[0]=='3' else obj.message
    else :
        return convertToUnicode(obj)




    
def test_LPrint():
    lprint ((u'你好',u'世界',{u'你好':u'世界'},(u'你好',print)),55,end='\n\n')
    lprint (u'你好',end='\n\n')
    #lprint ((u'你好',u'世界',{u'你好':u'世界'},(u'你好',u'世界')),end='\n\n',oneLine=False)
    #print (r"u'\u4e16\u754c',{u'\u4f60\u597d': u'\u4e16\u754c'}".decode('unicode_escape'))


def __dir__():
    pass

def __dict__():
    pass


if __name__=='__main__':
    pass
    test_LPrint()
    


    

