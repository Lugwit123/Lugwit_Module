# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import collections
import os
import sys
import logging
from datetime import datetime
import inspect
import json
import traceback
import re
import threading
import subprocess
import functools
import time

# 根据 Python 版本进行条件导入
if sys.version[0] == '2':
    import _winreg as winreg
    string_types = (str, unicode)
    sys.path.append(r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib\Lugwit_Module\l_src\lib2')
else:
    string_types = (str,)
    import winreg

# 将源目录添加到 sys.path
l_srcDir_match = re.search(r'.+l_src', __file__)
if l_srcDir_match:
    l_srcDir = l_srcDir_match.group(0)
    sys.path.append(l_srcDir)
sys.path.append(os.path.dirname(__file__))


from encoding_handler import EncodingHandler, LPrintHandler as ExtLPrintHandler
from encoding_handler import convertToUnicode, convertToUnicode_py2, stringify_non_serializable




# 注意：这里不能直接使用logging模块的函数，需要在运行时动态获取logger的方法
# 避免使用系统root logger导致编码问题
def get_level_map(logger):
    """动态获取logger的级别映射，确保使用自定义logger而不是系统logger"""
    return {
        'debug': logger.debug,
        'info': logger.info,
        'warning': logger.warning,
        'error': logger.error,
        'critical': logger.critical,
    }


# 用于检查是否在 Maya 环境中运行的 lambda 函数
isMayaEnv = lambda *args: re.search(r'maya(py)?\.exe', sys.executable)
isMayaPyEnv = lambda *args: re.search(r'mayapy\.exe', sys.executable)
isMayaEnvValue=isMayaEnv()

# logging级别常量集合 - 模块级别定义，避免重复创建
LOGGING_LEVEL_CONSTANTS = {
    logging.DEBUG,    # 10
    logging.INFO,     # 20
    logging.WARNING,  # 30
    logging.ERROR,    # 40
    logging.CRITICAL  # 50
}

def get_module_name():
    """获取当前模块的名称"""
    import sys
    import os
    if '__main__' == sys.modules['__main__'].__name__:
        # 直接执行的情况
        script_path = sys.argv[0]
        return os.path.splitext(os.path.basename(script_path))[0]
    else:
        # 被导入的情况
        return sys.modules['__main__'].__name__

def getframeinfo_wrapper(frame, context=1):
    frameinfo = inspect.getframeinfo(frame)
    if context > 1 and frameinfo.code_context is not None:
        frameinfo = frameinfo._replace(code_context=frameinfo.code_context[1:])
    return frameinfo

def dynamic_import(module_path=None):
    module_name = os.path.basename(module_path).split('.')[0] if module_path else None
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

# 获取计算机名称
hostName = os.environ.get('COMPUTERNAME')

__all__ = [
    'getFileModifyTime',
    'compare_dates',
    'lprint',
    'get_dict_nested_value',
    'get_keys_by_value',
    'dynamic_import',
    'LPrint'  # 将 LPrint 类添加到 __all__ 中
]

def getFileModifyTime(file_path=''):
    """获取文件的修改时间"""
    try:
        timestamp = os.path.getmtime(file_path)
        modified_date = datetime.fromtimestamp(timestamp)
        formatted_date = modified_date.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date
    except Exception as e:
        print(u"获取文件修改时间失败: {}".format(e))
        return None

def compare_dates(date_str1, date_str2, date_format="%Y-%m-%d %H:%M:%S"):
    """比较两个日期字符串"""
    try:
        date1 = datetime.strptime(date_str1, date_format)
        date2 = datetime.strptime(date_str2, date_format)
    except ValueError as e:
        print(u"日期格式错误: {}".format(e))
        return None

    if date1 > date2:
        return 1
    elif date1 < date2:
        return -1
    else:
        return 0

def get_dict_nested_value(dictionary, keys):
    """获取嵌套字典中的值"""
    if not isinstance(dictionary, dict) or not keys:
        return None
    key = keys[0]
    if key not in dictionary:
        return None
    if len(keys) == 1:
        return dictionary[key]
    return get_dict_nested_value(dictionary[key], keys[1:])

def get_keys_by_value(dict_, value_to_find):
    """根据值获取所有对应的键"""
    keys_to_find = [key for key, value in dict_.items() if value == value_to_find]
    return keys_to_find

# 检查执行环境
MayaExecutable = False
unrealExecutable = False
sys_executable = sys.executable

if sys_executable.endswith('maya.exe'):
    try:
        import maya.cmds as cmds
        MayaExecutable = True
    except ImportError:
        print(u"无法导入 maya.cmds")
elif 'UnrealEditor' in sys_executable:
    try:
        import unreal
        unrealExecutable = True
    except ImportError:
        print(u"无法导入 unreal")

TempDir = os.environ.get('Temp')





def get_log_func_int_dict(logger):
    """动态获取整数级别映射，确保使用自定义logger而不是系统logger"""
    return {
        logging.ERROR: logger.error,        # 修正：ERROR对应error，不是debug
        logging.CRITICAL: logger.critical,
        logging.INFO: logger.info,
        logging.DEBUG: logger.debug,
        logging.WARNING: logger.warning
    }
            
class _LPrintHandler(logging.StreamHandler):
    """Custom handler for lprint output using external encoding handler if available."""
    def __init__(self, stream=None):
        super(_LPrintHandler, self).__init__(stream or sys.stdout)

    def emit(self, record):
        ext_handler = ExtLPrintHandler(self.stream)
        ext_handler.emit(record)




# ---------------- 装饰器: 自动在函数结束时 flush lprint -----------------

def with_lprint_end(_func=None, **_decorator_kwargs):
    """装饰器：函数结束后处理 lprint 缓冲。
    参数:
        clear_only (bool): 为 True 时只清空缓存不打印；
                          为 False 时正常 `lprint<<lprint.End` 打印。
    用法:
        @with_lprint_end              # 默认打印
        def foo(): ...

        @with_lprint_end(clear_only=True)  # 仅清空不打印
        def bar(): ...
    """
    clear_only = _decorator_kwargs.get('clear_only', False)

    def decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            finally:
                try:
                    if clear_only:
                        # 只清空，不输出
                        lprint.items = []
                        lprint.shift_frame = None
                        lprint.lshift = 0
                    else:
                        lprint << lprint.End
                except NameError:
                    pass
        return _wrapper

    # 允许无括号使用 @with_lprint_end
    if _func and callable(_func):
        return decorator(_func)
    return decorator

# -------------------------------------------------------------------------

from lprint_plug import LPrint_Plug

# 性能计时函数：Python 2.7/3.x 兼容版本
# 在 Python 3.3+ 使用 time.perf_counter()（高精度、单调递增）
# 在 Python 2.7 使用 time.clock()（Windows）或 time.time()（Unix）
if sys.version_info >= (3, 3):
    # Python 3.3+ 使用 perf_counter（最佳选择）
    _perf_counter = time.perf_counter
elif sys.platform == 'win32':
    # Python 2.7 Windows 使用 clock（高精度）
    _perf_counter = time.clock
else:
    # Python 2.7 Unix/Linux/Mac 使用 time（clock 在 Unix 上返回 CPU 时间，不适合测量耗时）
    _perf_counter = time.time

class LPrint(LPrint_Plug):
    """LPrint 类，用于调试打印信息"""
    End="end"
    
    # 私有属性：需要详细日志记录的函数列表，支持通配符
    _detailed_log_functions = [
        # 匹配函数名
        "*maya*",           # 匹配包含maya的函数
        "*export*",         # 匹配包含export的函数 
        "get_*",           # 匹配以get_开头的函数
        "*_format_*",      # 匹配包含_format_的函数
        
        # 匹配模块名
        "*test_log_width*",  # 匹配测试模块
        "*maya*",           # 匹配包含maya的模块
        
        # 可以根据需要添加更多模式
    ]
    
    # 类属性：记录每行代码打印的次数，格式为 {文件名:行号: 次数}
    line_print_counts_dict = {}
    
    # 类属性：每行代码最大打印次数
    max_prints_per_line = 2
    
    # 类属性：是否启用函数范围检查（默认关闭）
    enable_function_range_check = False
    
    # 类属性：入口模块名称
    entry_module_name = None
    
    # 类属性：全局debug_self开关，用于调试lprint不打印信息的原因
    debug_self_global = False
    
    # 类属性：日志组件插件
    logwgt_plugin = None
    
    # 类属性：日志组件插件的模式 (append 或 set)
    logwgt_plugin_mode = 'append'
    
    # 类属性：日志组件插件的级别
    logwgt_plugin_level = logging.WARNING
    
    # 类属性：存储累积的日志消息内容 (用于 append 模式)
    logwgt_plugin_accumulated_content = u""
    
    # 类属性：是否启用行计数器功能（可选择性禁用以提升性能）
    enable_line_counting = True
    
    # 类属性：性能分析开关
    enable_performance_profiling = False
    
    # 类属性：性能数据收集
    performance_stats = {
        'total_calls': 0,
        'frame_acquisition_time': 0.0,
        'unicode_conversion_time': 0.0, 
        'debug_check_time': 0.0,
        'line_counting_time': 0.0,
        'frame_info_time': 0.0,
        'serialization_time': 0.0,
        'format_time': 0.0,
        'total_format_message_time': 0.0
    }

    def __init__(self, popui=False, log_width=2):
        self.debug = None  # 可以通过实例设置调试模式
        self.lshift = 0
        self.items = []
        self.delay = 0.0001  # 延迟时间
        self.timer = None  # 定时器
        self.shift_frame = None  # 定时器
        self.log_func=logging.warning
        # # 显示弹出窗口提示
        self.popui = False
        # 日志宽度：扩大detailed_log_functions中定义的函数前后帧lprint生效的范围
        self.log_width = log_width
        self.trace_depth=1
        self.min_log_level = logging.DEBUG
        
        if isMayaEnvValue:
            self.logger=logging.getLogger("MayaTools")
        else:
            # 使用专用 Logger 避免与 root logger 的 basicConfig 冲突造成重复输出
            self.logger = logging.getLogger("LPrint")
        # 移除已存在的非 _LPrintHandler，避免重复输出
        self.logger.handlers = [h for h in self.logger.handlers if isinstance(h, _LPrintHandler)]
        # 确保 logger 装载自定义 handler
        # 禁止向父 logger 传播，避免重复输出
        self.logger.propagate = False
        if not any(isinstance(h, _LPrintHandler) for h in self.logger.handlers):
            self.logger.addHandler(_LPrintHandler())
        self.log_func = self.logger.warning
        self.logger.setLevel(self.min_log_level)  # 新增：初始化时设置最低级别

    def _debug_self_print(self, message):
        u"""内部方法：根据debug_self设置决定是否打印调试信息
        
        Args:
            message (unicode): 调试信息
        """
        if LPrint.debug_self_global:
            print(u"[LPrint-DebugSelf] {}".format(message))
    
    def _get_caller_debug_info(self, args):
        u"""获取调用者的调试信息（文件名、行号、内容预览）
        
        Args:
            args (tuple): lprint的参数
            
        Returns:
            unicode: 格式化的调试信息字符串
        """
        try:
            current_frame = inspect.currentframe()
            # 逐层查找真正的调用者
            frame = current_frame
            for _ in range(4):  # 跳过多层内部调用
                if frame and frame.f_back:
                    frame = frame.f_back
                else:
                    break
            
            if frame:
                caller_info = inspect.getframeinfo(frame)
                filename = os.path.basename(caller_info.filename)
                lineno = frame.f_lineno
                
                # 获取内容预览
                try:
                    if sys.version_info[0] == 2:
                        args_preview = u", ".join([unicode(arg) for arg in args[:3]])
                    else:
                        args_preview = u", ".join([str(arg) for arg in args[:3]])
                    
                    if len(args) > 3:
                        args_preview += u"..."
                    args_preview = args_preview[:100]  # 限制长度
                    
                    return u"文件: {}:{}, 内容: \"{}\"".format(filename, lineno, args_preview)
                except:
                    return u"文件: {}:{}, 内容: [无法显示]".format(filename, lineno)
            else:
                return u"文件: [未知], 内容: [无法获取]"
        except Exception as e:
            return u"调试信息获取失败: {}".format(str(e))

    def _safe_unicode_args(self, args):
        """安全地将所有参数转换为Unicode，避免编码错误"""
        converted_args = []
        for arg in args:
            try:
                # 处理字符串类型的参数
                if sys.version_info[0] == 2:
                    if isinstance(arg, str):
                        # 字节字符串，尝试转换为Unicode
                        try:
                            converted_args.append(arg.decode('utf-8'))
                        except UnicodeDecodeError:
                            try:
                                converted_args.append(arg.decode('gbk'))
                            except UnicodeDecodeError:
                                try:
                                    converted_args.append(arg.decode('latin1'))
                                except UnicodeDecodeError:
                                    # 最后手段：替换无法解码的字符
                                    converted_args.append(arg.decode('utf-8', 'replace'))
                    elif isinstance(arg, unicode):
                        converted_args.append(arg)
                    else:
                        # 非字符串类型，保持原样
                        converted_args.append(arg)
                else:
                    # Python 3中字符串默认就是Unicode
                    converted_args.append(arg)
            except Exception as e:
                # 如果转换过程中出现任何错误，尝试安全的字符串表示
                try:
                    if sys.version_info[0] == 2:
                        converted_args.append(unicode(str(arg)))
                    else:
                        converted_args.append(str(arg))
                except:
                    # 最后的后备方案
                    converted_args.append(u"[转换错误的参数]")
        return tuple(converted_args)

    def __call__(self, *args, **kwargs):
        """
        支持多种调用方式：
        1. lprint(message)
        2. lprint(format_string, arg1, arg2, ...) - 自动安全格式化
        3. lprint(message, trace_depth=2) - 设置调用栈追溯深度
        4. lprint(message, level=logging.WARNING) - 使用关键字参数指定级别
        5. lprint(message, force_print=True) - 强制打印，忽略环境变量设置
        
        Args:
            trace_depth (int): 调用栈追溯深度，默认为1（不追溯），
                              2表示追溯1层，以此类推，支持1到无穷大
            force_print (bool): 强制打印模式，为True时忽略Lugwit_Debug环境变量的noprint设置
        """
        # 🚀 性能分析：开始计时（使用高精度计时器）
        call_start_time = _perf_counter() if LPrint.enable_performance_profiling else None
        frame_start_time = _perf_counter() if LPrint.enable_performance_profiling else None
        
        # 🚀 性能优化：在__call__中直接获取帧信息，减少查找深度
        caller_frame = None
        caller_function = None
        try:
            current_frame = inspect.currentframe()
            if current_frame and current_frame.f_back:
                caller_frame = current_frame.f_back  # 获取真正的调用者
                caller_function = caller_frame.f_code.co_name
        except Exception:
            pass  # 如果获取失败，继续执行，在_format_log_message中处理
        
        # 🚀 性能分析：帧获取耗时
        if LPrint.enable_performance_profiling:
            LPrint.performance_stats['frame_acquisition_time'] += _perf_counter() - frame_start_time
            unicode_start_time = _perf_counter()
        
        # 先进行编码安全检查，捕获可能的UnicodeDecodeError
        try:
            # 先对参数进行安全的Unicode转换
            safe_args = self._safe_unicode_args(args)
            
            # 传递预获取的帧信息到_format_log_message
            kwargs['_caller_frame'] = caller_frame
            kwargs['_caller_function'] = caller_function
            
            # 🚀 性能分析：编码转换耗时
            if LPrint.enable_performance_profiling:
                LPrint.performance_stats['unicode_conversion_time'] += _perf_counter() - unicode_start_time
            
            log_message = self._format_log_message(*safe_args, **kwargs)
        except UnicodeDecodeError as e:
            # 如果参数中包含有问题的编码，进行紧急处理
            if 'switch' in args:
                print(u"处理编码")
            emergency_args = []
            for arg in args:
                if sys.version_info[0] == 2:
                    if isinstance(arg, str):
                        try:
                            emergency_args.append(arg.decode('utf-8', 'replace'))
                        except:
                            emergency_args.append(repr(arg))
                    elif isinstance(arg, unicode):
                        emergency_args.append(arg)
                    else:
                        emergency_args.append(unicode(str(arg)))
                else:
                            emergency_args.append(str(arg))
            
            kwargs['_caller_frame'] = caller_frame
            kwargs['_caller_function'] = caller_function
            log_message = self._format_log_message(*emergency_args, **kwargs)
        except Exception as e:
            # 对于其他异常，输出错误信息并继续
            error_message = u"[lprint错误] 参数处理失败: {}".format(str(e))
            log_message = error_message
        
        # 🚀 性能分析：更新总调用次数
        if LPrint.enable_performance_profiling:
            LPrint.performance_stats['total_calls'] += 1
        
        try:
            if log_message == "exceeded_message":
                # 🔧 使用与_format_log_message相同的智能帧获取逻辑
                try:
                    current_frame = inspect.currentframe()
                    caller_frame = None
                    
                    # 使用与_format_log_message相同的帧获取逻辑
                    try:
                        frames = inspect.getouterframes(current_frame)
                        
                        # 查找第一个不属于LPrint内部方法的帧
                        for i, frame_info in enumerate(frames):
                            # 跳过当前方法(__call__)和_format_log_message方法
                            if frame_info.function in ('__call__', '_format_log_message'):
                                continue
                            
                            # 跳过LPrint内部的其他方法  
                            if 'usualFunc.py' in frame_info.filename and frame_info.function.startswith('_'):
                                continue
                                
                            # 找到了真正的用户调用代码
                            caller_frame = frames[i].frame
                            break
                        
                        # 如果没有找到合适的帧，使用传统方法作为备选
                        if caller_frame is None:
                            caller_frame = current_frame.f_back  # __call__ 的调用者
                            if caller_frame is not None:
                                caller_frame = caller_frame.f_back  # 真正的用户代码
                                
                    except Exception:
                        # 如果新方法失败，回退到传统方法
                        caller_frame = current_frame.f_back
                        if caller_frame is not None:
                            caller_frame = caller_frame.f_back
                    
                    if caller_frame:
                        caller_info = inspect.getframeinfo(caller_frame)
                        filename = os.path.basename(caller_info.filename)
                        lineno = caller_frame.f_lineno
                        
                        # 尝试获取被限制的内容
                        try:
                            args_preview = u", ".join([unicode(arg) if sys.version_info[0] == 2 else str(arg) for arg in safe_args[:3]])
                            if len(safe_args) > 3:
                                args_preview += u"..."
                            args_preview = args_preview[:100]  # 限制长度
                        except:
                            args_preview = u"[无法显示内容]"
                        
                        self._debug_self_print(u"lprint被限制：超过最大打印次数限制 - 文件: {}:{}, 内容: \"{}\"".format(
                            filename, lineno, args_preview))
                    else:
                        self._debug_self_print(u"lprint被限制：超过最大打印次数限制")
                except Exception as e:
                    self._debug_self_print(u"lprint被限制：超过最大打印次数限制 (获取详细信息失败: {})".format(str(e)))
                return
            
            if log_message is not None:
                self.log_func(log_message)
                sys.stdout.flush()
            else:
                # 🔧 修复：当debug='noprint'时，不应该打印任何debug信息
                # 只有在debug不是'noprint'时才打印debug信息
                if self.debug in ('noprint', 'no print'):
                    # 如果明确设置了debug='noprint'，直接返回，不打印任何内容
                    return
                
                # 检查环境变量
                debug_env = os.getenv('Lugwit_Debug', "inspect")
                if debug_env in ('noprint', 'no print'):
                    # 如果环境变量设置了noprint，直接返回
                    return
                    
                level= kwargs.get('level')

                debug_msg1 = u"[lprint debug] 传入的level参数类型: {}, 内容: {}".format(type(level), repr(level))
                # 使用encoding_handler中的emoji过滤方法
                safe_debug_args = EncodingHandler.filter_args_emoji(safe_args)
                debug_msg2 = u"args->{},self._format_log_message return none".format(safe_debug_args)
                EncodingHandler.enhanced_output(debug_msg1)
                EncodingHandler.enhanced_output(debug_msg2)
                sys.stdout.flush()
        except:pass

    

    @staticmethod
    def _is_function_match(function_name, module_name, pattern):
        """检查函数名或模块名是否匹配指定的模式（支持通配符）
        
        Args:
            function_name: 要检查的函数名
            module_name: 要检查的模块名
            pattern: 匹配模式，支持 * 通配符
            
        Returns:
            bool: 是否匹配
        """
        # 将通配符模式转换为正则表达式
        regex_pattern = pattern.replace('*', '.*')
        # 检查函数名是否匹配
        if re.match('^' + regex_pattern + '$', function_name):
            return True
        # 检查模块名是否匹配
        if module_name and re.match('^' + regex_pattern + '$', module_name):
            return True
        return False
    
    def _check_call_stack(self):
        """检查调用栈中是否有匹配detailed_log_functions中模式的函数
        
        如果找到匹配的函数，则该函数及其前后log_width帧范围内的函数中的lprint都会生效
        
        Returns:
            bool: 如果当前函数在匹配函数的前后log_width帧范围内，则返回True
        """
        try:
            # 获取当前调用栈
            current_frame = inspect.currentframe()
            if current_frame is None:
                print(u"_check_call_stack: 错误：currentframe为None")
                return False
            
            # 获取调用lprint的函数（即我们需要检查的函数）
            # 跳过_check_call_stack和_format_log_message
            caller_frame = current_frame
            for i in range(3):  # 跳过当前函数、_check_call_stack和_format_log_message
                if caller_frame and hasattr(caller_frame, 'f_back'):
                    caller_frame = caller_frame.f_back
                else:
                    print(u"_check_call_stack: 错误：无法获取第{}级调用者帧".format(i+1))
                    return False
            
            if not caller_frame:
                print(u"_check_call_stack: 错误：最终caller_frame为None")
                return False
                
            # 获取调用函数的信息
            caller_function = caller_frame.f_code.co_name
            caller_module = caller_frame.f_globals.get('__name__')
            
            # 检查调用函数是否直接匹配
            for pattern in self._detailed_log_functions:
                if self._is_function_match(caller_function, caller_module, pattern):
                    return True
            
            # 收集调用栈中的所有函数
            stack_frames = []
            frame = caller_frame
            while frame:
                stack_frames.append((frame.f_code.co_name, frame.f_globals.get('__name__')))
                frame = frame.f_back
            
            # 查找调用栈中匹配的函数及其位置
            matched_indices = []
            for i, (function, module) in enumerate(stack_frames):
                # 检查函数名或模块名是否匹配任何模式
                for pattern in self._detailed_log_functions:
                    if self._is_function_match(function, module, pattern):
                        matched_indices.append(i)
                        break
            
            # 如果没有找到匹配的函数，返回False
            if not matched_indices:
                return False
            
            # 检查调用函数是否在任何匹配函数的前后log_width帧范围内
            caller_position = 0  # 调用函数在stack_frames中的位置是0
            for matched_idx in matched_indices:
                if abs(matched_idx - caller_position) <= self.log_width:
                    return True
                    
            return False
        except Exception as e:
            # 如果出现异常，默认返回False
            print("Error in _check_call_stack: " + str(e))
            return False
    
    def _format_log_message(self, *args, **kwargs):
        
        # 🚀 性能分析：_format_log_message 开始计时
        format_start_time = _perf_counter() if LPrint.enable_performance_profiling else None
        debug_check_start_time = _perf_counter() if LPrint.enable_performance_profiling else None
        
        # 🚀 性能优化：早期检查debug状态，避免不必要的frame操作
        force_print = kwargs.get('force_print', False)
        
        # 如果不是强制打印，先检查debug状态
        if not force_print:
            # 检查实例级别的debug设置
            if self.debug in ('noprint', 'no print'):
                debug_info = self._get_caller_debug_info(args) if LPrint.debug_self_global else u""
                if LPrint.debug_self_global:
                    self._debug_self_print(u"lprint未打印：实例debug模式设置为'{}' - {}".format(self.debug, debug_info))
                return None
            elif self.debug is False:
                debug_info = self._get_caller_debug_info(args) if LPrint.debug_self_global else u""
                if LPrint.debug_self_global:
                    self._debug_self_print(u"lprint未打印：实例debug模式为False - {}".format(debug_info))
                return None
            
            # 检查环境变量级别的debug设置
            debug_env = os.getenv('Lugwit_Debug', "inspect")
            if debug_env in ('noprint', 'no print'):
                debug_info = self._get_caller_debug_info(args) if LPrint.debug_self_global else u""
                if LPrint.debug_self_global:
                    self._debug_self_print(u"lprint未打印：环境变量debug模式为'{}' - {}".format(debug_env, debug_info))
                return None
        
        # 处理pureprint模式（需要早期处理，因为它有特殊的输出逻辑）
        if self.debug == 'pureprint' or os.getenv('Lugwit_Debug', "inspect") == 'pureprint':
            try:
                args_serialized = json.dumps(args, ensure_ascii=False, indent=4)
                print(u'--{}--'.format(args_serialized[1:-1]))
            except Exception as e:
                print(u'--{}--{}'.format(args, str(e)[-10:]))
            return None
        
        # 🚀 性能分析：debug检查耗时
        if LPrint.enable_performance_profiling:
            LPrint.performance_stats['debug_check_time'] += _perf_counter() - debug_check_start_time
            line_counting_start_time = _perf_counter()
        
        popui=kwargs.get('popui',False)
        if 'level' in kwargs:
            # 兼容level为int、函数、字符串
            level = kwargs['level']
            if isinstance(level, int):
                # 使用自定义logger的方法，支持logging.DEBUG等常量
                log_func_int_dict = get_log_func_int_dict(self.logger)
                self.log_func = log_func_int_dict.get(level, self.logger.warning)
            elif callable(level):
                self.log_func = level
            elif isinstance(level, string_types):
                # 使用自定义logger的方法，确保编码处理一致
                level_map = get_level_map(self.logger)
                self.log_func = level_map.get(level.lower(), self.logger.warning)
                # print(u"[lprint debug] level字符串已转换为: {}".format(self.log_func))
            else:
                # print(u"[lprint] level参数类型错误，已回退为warning")
                self.log_func = self.logger.warning
            
        if args == ['\n']:
            '''
            #这个好奇怪,如何把['\n']修改为('\n',)UE就会报下面的出错,
            # TypeError: NativizeProperty: Cannot nativize 'str' as 'TransientPythonProperty' 
            # (ObjectProperty)
            TypeError: NativizeObject: Cannot nativize 'str' as 'Object' (allowed Class type: 'Object')
            '''
            print(u"奇怪报错,args == ['\n']")
            return
        # 检查调用栈中是否有匹配的函数
        # 如果启用了函数范围检查，只有在调用栈中有匹配函数时才打印
        is_in_matched_range = False
        if LPrint.enable_function_range_check:
            is_in_matched_range = self._check_call_stack()
            if not is_in_matched_range:
                debug_info = self._get_caller_debug_info(args)
                self._debug_self_print(u'lprint未打印：不在允许的函数范围内（enable_function_range_check=True且调用栈检查失败） - {}'.format(debug_info))
                print(u'[lprint debug] 不在允许的函数范围内')
                return None
                
        # 处理 Unreal Editor 环境（如果需要）
        if unrealExecutable:
            pass  # 可以在这里添加 Unreal 特定的处理逻辑
        
        # 🚀 性能优化：使用预获取的帧信息
        debug_self = kwargs.get('debug_self', None)
        callBy = ""
        try:
            # 优先使用预传递的帧信息
            caller_frame = kwargs.get('_caller_frame')
            
            if self.shift_frame:
                caller_frame = self.shift_frame
            elif caller_frame is None:
                # 备用方案：如果没有预传递的帧信息，使用传统方法
                current_frame = inspect.currentframe()
                if current_frame is None:
                    print(u"错误：currentframe为None")
                    return u"错误：无法获取帧信息"
                    
                # 简化的帧获取逻辑
                caller_frame = current_frame.f_back  # _format_log_message 的调用者 (__call__)
                if caller_frame is not None:
                    caller_frame = caller_frame.f_back  # __call__ 的调用者（真正的用户代码）
                        
            if caller_frame is None:
                print(u"错误：无法获取到真正的调用者帧")
                return u"错误：无法获取调用者帧信息"
                    
            #Wprint("inspect.getouterframes",inspect.getouterframes(current_frame),end='\n\n')
            try:
                caller_info = inspect.getframeinfo(caller_frame)
            except Exception as e:
                error_msg = u"lprint break info {}: {}".format(args, str(e))
                logging.error(error_msg)
                return error_msg
            
            # 🚀 性能分析：帧信息获取耗时
            if LPrint.enable_performance_profiling:
                LPrint.performance_stats['frame_info_time'] += _perf_counter() - frame_info_start_time
                serialization_start_time = _perf_counter()
            
            # 处理调用栈追溯深度 - 累加显示调用链
            trace_depth = kwargs.get('trace_depth', self.trace_depth)
            if trace_depth > 1:
                try:
                    # 根据trace_depth决定追溯的层数
                    # trace_depth=2表示追溯1层，trace_depth=3表示追溯2层，以此类推
                    current_frame = caller_frame
                    call_chain = []  # 用于收集调用链信息
                    
                    # 循环收集每一层的调用信息
                    for depth_level in range(1, trace_depth):
                        if current_frame and current_frame.f_back:
                            current_frame = current_frame.f_back
                            try:
                                frameinfo = inspect.getframeinfo(current_frame)
                                code_context_str = ""
                                if frameinfo.code_context:
                                    code_context_str = frameinfo.code_context[0].strip()
                                
                                call_info = u">>callBy(深度{}): File: {}:{}, ->code_context:->{}->fn:{}".format(
                                    depth_level,
                                    frameinfo.filename,
                                    current_frame.f_lineno,
                                    code_context_str,
                                    frameinfo.function
                                )
                                call_chain.append(call_info)
                            except Exception as frame_error:
                                call_chain.append(u">>callBy(深度{}): 获取帧信息失败: {}".format(depth_level, str(frame_error)))
                        else:
                            call_chain.append(u">>callBy(深度{}): 已到达调用栈顶部".format(depth_level))
                            break
                    
                    # 将所有调用信息连接起来
                    if call_chain:
                        callBy = u"\n" + u"\n".join(call_chain)
                        
                except Exception as e:
                    # 如果追溯失败，设置一个简单的错误信息
                    callBy = u"\n>>callBy: 追溯失败 (trace_depth={}, 错误: {})".format(trace_depth, str(e))

        except Exception as e:
            print(u"error {}".format(traceback.format_exc()))
            return traceback.format_exc()

        code_context = caller_info.code_context or ''
        caller_lineno = caller_frame.f_lineno
        filename = caller_info.filename
        function = caller_info.function
        baseName = os.path.basename(filename).rsplit('.', 1)[0]
        caller_lineno_ori = -1

        # 🚀 性能优化：只在启用行计数功能时才检查打印次数
        if LPrint.enable_line_counting:
            # 检查该行代码的打印次数，如果超过限制则显示提示信息
            line_key = "{}:{}".format(filename, caller_lineno)
            current_count = LPrint.line_print_counts_dict.get(line_key, 0)
            
            # 更新打印次数（先更新，这样计数包括当前这次）
            current_count += 1
            LPrint.line_print_counts_dict[line_key] = current_count
            
            if current_count > self.max_prints_per_line:
                # exceeded_message = u"[lprint 限制] 文件: {} 第{}行 当前第{}次打印，已超出最大打印次数限制({})".format(
                #      os.path.basename(filename), caller_lineno, current_count, self.max_prints_per_line)
                # print(exceeded_message)
                # print(current_count,self.max_prints_per_line)
                return "exceeded_message"
        
        # 🚀 性能分析：行计数耗时
        if LPrint.enable_performance_profiling:
            LPrint.performance_stats['line_counting_time'] += _perf_counter() - line_counting_start_time
            frame_info_start_time = _perf_counter()

        if code_context:
            if debug_self:
                print(code_context, caller_lineno)
            code_context = code_context[0].strip()
        else:
            try:
                if '<' not in baseName:
                    if debug_self:
                        print(u"code_context_file->", baseName + '_code_context')
                    moduleName = __import__(baseName + '_code_context')
                    code_contextDict = moduleName.code_contextDict
                    if 'Lugwit_Module' not in str(moduleName):
                        caller_lineno_ori = caller_lineno - 10
                    else:
                        caller_lineno_ori = caller_lineno
                    code_context = code_contextDict.get(caller_lineno_ori, '')
                    if debug_self:
                        print(u'code_contextDict->', code_contextDict)
                        print(u"moduleName->", moduleName)
                        print(u"caller_lineno_ori->", caller_lineno_ori)
            except:
                pass  # 静默处理异常

        if caller_lineno_ori == -1:
            caller_lineno_ori = ''

        if sys.version[0] == '2' and isinstance(code_context, str):
            try:
                code_context = code_context.decode('utf-8')
            except UnicodeDecodeError:
                pass
              
        # 使用encoding_handler中的方法过滤args中的emoji，然后序列化参数
        try:
            # 使用encoding_handler中的emoji过滤方法
            filtered_args = EncodingHandler.filter_args_emoji(args)

            
            args_serialized = json.dumps(
                filtered_args,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
                default=str
            )
        except:
            #traceback.print_exc()
            try:
                print(code_context,args)
            except:
                r'''我也不知道这里为啥打印不出啦,以后再说,报错信息是在导出Fbx的时候
                报错信息如下...
                Traceback (most recent call last):
                File "D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib\Lugwit_Module\main.py", line 75, in warp_func
                    return func(*args, **kwargs)
                File "D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\IOLib\exFbx.py", line 718, in exAniClip_Simple
                    NsRfnAndFileDict=getNsKey_RfnAndFileDict()
                File "D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\l_scripts\IOLib\exFbx.py", line 225, in getNsKey_RfnAndFileDict
                    lprint (fileRef)
                File "D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib\Lugwit_Module\l_src\usualFunc.py", line 352, in __call__
                    print(repr(x))
                File "C:\Program Files\Autodesk\Maya2020\Python\lib\site-packages\pymel\core\system.py", line 1409, in __repr__
                    self.withCopyNumber(),
                File "C:\Program Files\Autodesk\Maya2020\Python\lib\site-packages\pymel\core\system.py", line 1540, in withCopyNumber
                    path = cmds.referenceQuery(self.refNode, filename=1)
                File "C:\Program Files\Autodesk\Maya2020\Python\lib\site-packages\pymel\internal\pmcmds.py", line 130, in referenceQuery_wrapped
                    res = new_cmd(*new_args, **new_kwargs)
                    '''
                try:
                    print(u"{}未知打印错误".format(code_context))
                except UnicodeEncodeError:
                    print("未知打印错误 - 包含无法编码的字符")
            return

        # 🚀 性能分析：序列化耗时
        if LPrint.enable_performance_profiling:
            LPrint.performance_stats['serialization_time'] += _perf_counter() - serialization_start_time
            format_message_start_time = _perf_counter()

        # 移除序列化字符串的外层括号
        if args_serialized.startswith('[') and args_serialized.endswith(']'):
            args_serialized = args_serialized[1:-1]
        elif args_serialized.startswith('(') and args_serialized.endswith(')'):
            args_serialized = args_serialized[1:-1]
        
        if '\\x' in repr(args_serialized):
            try:
                args_serialized = args_serialized.decode('gbk')
            except:
                pass
        
        # 构建匹配状态信息
        match_status = ""
        if is_in_matched_range:
            match_status = u"[在匹配函数范围内]"
        
        # 添加强制打印状态提示
        force_print_status = ""
        if force_print:
            force_print_status = u"[强制打印]"
        
        log_message = u'\n{args}   {currentTime}----code_context : {code_context} \nFile: {filename}:{caller_lineno}, {caller_lineno_ori}-fn: {funcName}, 打印次数: {print_count}/{max_prints} {match_status} {force_print_status} {callBy}\n' \
                      .format(
                          args=args_serialized[1:-1],
                          currentTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                          code_context=code_context,
                          filename=filename,
                          caller_lineno=caller_lineno,
                          caller_lineno_ori=caller_lineno_ori,
                          funcName=function,
                          print_count=current_count,
                          max_prints=self.max_prints_per_line,
                          match_status=match_status,
                          force_print_status=force_print_status,
                          callBy=callBy
                      )
        sep = u''
        if 'oneLine' in kwargs:
            sep = ' '
        if popui:
            if sys.version_info[0] >= 3:
                from  l_subprocess import showMessage_tk
                print("log_message",log_message)
                showMessage_tk.main(text=log_message.replace(r'\n', '\n'), 
                            )
            else:
                from  l_subprocess import save_message
                save_message.save_message_to_file(log_message.replace(r'\n', '\n'))
            log_message=log_message.replace(r'\n', '\n')[:200]
        elif unrealExecutable:
            print(log_message)
        else:
            #print(self.log_func,logging.getLevelName(self.logger.level))
            log_message=log_message.replace(r'\n', '\n').replace(r'\\', '\\')
        
        # 🔌 调用日志组件插件 (如果已注册且当前级别匹配)
        try:
            if (LPrint.logwgt_plugin is not None and 
                hasattr(self, 'log_func') and 
                self._check_log_level_match()):
                LPrint._call_logwgt_plugin_with_mode(log_message)
        except Exception as e:
            print(u"[LPrint] 日志组件插件调用异常: {}".format(str(e)))
        
        # 🚀 性能分析：格式化耗时和总耗时计算
        if LPrint.enable_performance_profiling:
            LPrint.performance_stats['format_time'] += _perf_counter() - format_message_start_time
            LPrint.performance_stats['total_format_message_time'] += _perf_counter() - format_start_time
        
        return log_message
            
    

    @classmethod
    def get_detailed_log_functions(cls):
        """获取详细日志函数列表"""
        return getattr(cls, '_detailed_log_functions', [])
    
    @classmethod  
    def set_detailed_log_functions(cls, value):
        """设置详细日志函数列表，并自动处理函数范围检查"""
        cls._detailed_log_functions = value
        # 自动检查：如果列表不为空，则自动启用函数范围检查
        if value:
            cls.enable_function_range_check = True
            print(u"[lprint] 检测到detailed_log_functions不为空，已自动启用函数范围检查")
        else:
            cls.enable_function_range_check = False
            print(u"[lprint] detailed_log_functions为空，已自动禁用函数范围检查")

    @staticmethod
    def reset_line_counts():
        """重置行打印次数计数器"""
        print(u"重置计数器")
        LPrint.line_print_counts_dict = {}
        
    @staticmethod
    def set_function_range_check(enable=True):
        """设置是否启用函数范围检查
        
        Args:
            enable: 是否启用函数范围检查，默认为True
        """
        LPrint.enable_function_range_check = enable
        
    @staticmethod
    def set_line_counting(enable=True):
        """设置是否启用行计数功能 - 性能优化选项
        
        Args:
            enable (bool): 是否启用行计数功能，默认为True
                          False时将跳过所有frame信息获取，显著提升性能
        """
        LPrint.enable_line_counting = enable
        if not enable:
            print(u"[lprint] 行计数功能已禁用，这将显著提升性能但会失去打印次数限制功能")
        else:
            print(u"[lprint] 行计数功能已启用")
            
    @staticmethod
    def enable_performance_analysis(enable=True):
        """启用或禁用性能分析
        
        Args:
            enable (bool): 是否启用性能分析，默认为True
        """
        LPrint.enable_performance_profiling = enable
        if enable:
            # 重置统计数据
            LPrint.performance_stats = {
                'total_calls': 0,
                'frame_acquisition_time': 0.0,
                'unicode_conversion_time': 0.0, 
                'debug_check_time': 0.0,
                'line_counting_time': 0.0,
                'frame_info_time': 0.0,
                'serialization_time': 0.0,
                'format_time': 0.0,
                'total_format_message_time': 0.0
            }
            print(u"[lprint] 性能分析已启用，将收集各步骤耗时数据")
        else:
            print(u"[lprint] 性能分析已禁用")
    
    @staticmethod
    def get_performance_report():
        """获取性能分析报告
        
        Returns:
            str: 格式化的性能报告
        """
        if not LPrint.enable_performance_profiling:
            return u"性能分析未启用，请先调用 LPrint.enable_performance_analysis(True)"
        
        stats = LPrint.performance_stats
        total_calls = stats['total_calls']
        
        if total_calls == 0:
            return u"暂无性能数据"
        
        # 计算平均耗时（毫秒）
        report = [
            u"\n=== LPrint 性能分析报告 ===",
            u"总调用次数: {}".format(total_calls),
            u"平均耗时分析 (毫秒):",
            u"  帧获取: {:.4f}ms".format(stats['frame_acquisition_time'] * 1000 / total_calls),
            u"  编码转换: {:.4f}ms".format(stats['unicode_conversion_time'] * 1000 / total_calls),
            u"  debug检查: {:.4f}ms".format(stats['debug_check_time'] * 1000 / total_calls),
            u"  行计数: {:.4f}ms".format(stats['line_counting_time'] * 1000 / total_calls),
            u"  帧信息获取: {:.4f}ms".format(stats['frame_info_time'] * 1000 / total_calls),
            u"  序列化: {:.4f}ms".format(stats['serialization_time'] * 1000 / total_calls),
            u"  格式化: {:.4f}ms".format(stats['format_time'] * 1000 / total_calls),
            u"  _format_log_message总耗时: {:.4f}ms".format(stats['total_format_message_time'] * 1000 / total_calls),
            u"",
            u"总耗时分布 (秒):",
            u"  帧获取: {:.6f}s".format(stats['frame_acquisition_time']),
            u"  编码转换: {:.6f}s".format(stats['unicode_conversion_time']),
            u"  debug检查: {:.6f}s".format(stats['debug_check_time']),
            u"  行计数: {:.6f}s".format(stats['line_counting_time']),
            u"  帧信息获取: {:.6f}s".format(stats['frame_info_time']),
            u"  序列化: {:.6f}s".format(stats['serialization_time']),
            u"  格式化: {:.6f}s".format(stats['format_time']),
            u"  _format_log_message总耗时: {:.6f}s".format(stats['total_format_message_time']),
            u"=== 报告结束 ==="
        ]
        
        return u"\n".join(report)
    
    @staticmethod
    def print_performance_report():
        """打印性能分析报告"""
        print(LPrint.get_performance_report())

    @staticmethod
    def get_performance_settings():
        """获取当前性能相关设置
        
        Returns:
            dict: 性能设置信息
        """
        return {
            'enable_line_counting': LPrint.enable_line_counting,
            'enable_function_range_check': LPrint.enable_function_range_check,
            'debug_self_global': LPrint.debug_self_global,
            'max_prints_per_line': LPrint.max_prints_per_line,
            'line_counts_entries': len(LPrint.line_print_counts_dict)
        }

    @staticmethod
    def get_caller_function_name(depth=1):
        """获取调用者函数名的更高效方法
        
        Args:
            depth (int): 调用深度，1表示直接调用者
            
        Returns:
            str: 调用者函数名，获取失败返回'<unknown>'
        """
        try:
            current_frame = inspect.currentframe()
            target_frame = current_frame
            
            # 跳过指定深度的帧
            for _ in range(depth + 1):  # +1 跳过当前函数
                if target_frame and target_frame.f_back:
                    target_frame = target_frame.f_back
                else:
                    return '<unknown>'
            
            if target_frame:
                return target_frame.f_code.co_name
            else:
                return '<unknown>'
        except Exception:
            return '<unknown>'
    
    @staticmethod
    def get_caller_info_simple(depth=1):
        """获取调用者信息的简化方法
        
        Args:
            depth (int): 调用深度，1表示直接调用者
            
        Returns:
            tuple: (frame, function_name, filename, lineno)
        """
        try:
            current_frame = inspect.currentframe()
            target_frame = current_frame
            
            # 跳过指定深度的帧
            for _ in range(depth + 1):  # +1 跳过当前函数
                if target_frame and target_frame.f_back:
                    target_frame = target_frame.f_back
                else:
                    return None, '<unknown>', '<unknown>', 0
            
            if target_frame:
                function_name = target_frame.f_code.co_name
                filename = target_frame.f_code.co_filename
                lineno = target_frame.f_lineno
                return target_frame, function_name, filename, lineno
            else:
                return None, '<unknown>', '<unknown>', 0
        except Exception:
            return None, '<unknown>', '<unknown>', 0

    def flush(self):
        """Flush buffered messages collected via the << operator.
        Instead of passing the whole list to __call__ (which would stringify the
        list via JSON and leave escape characters), iterate over the buffered
        messages and log them one by one, preserving their original formatting.
        """
        for _msg in self.items:
            # 🔧 修复：过滤掉None值，防止debug='noprint'时仍然输出内容
            if _msg is not None:
                # 直接使用配置的日志函数输出消息
                self.log_func(_msg)
        # Reset internal state
        self.items = []
        self.shift_frame = None
        self.lshift = 0

    


            
    def __lshift__(self, other):
        """重载 << 操作符，收集项目并等待打印"""
        log_message = self._format_log_message(other)
            
        if self.lshift==0:
            self.last_lshift=0
            current_frame = inspect.currentframe()
            outer_frames = inspect.getouterframes(current_frame)
            self.shift_frame = outer_frames[0][0].f_back
                # print (shift_frame.lineno)
        #print("other",other,self.lshift, other==lprint.End)

        if other==lprint.End:
            self.lshift=0
            self.last_lshift = 0
            self.flush()
            return
        
        # 🔧 修复：当debug='noprint'时，_format_log_message返回None，不应该添加到items中
        if log_message is not None:
            self.lshift += 1
            self.items.append(log_message)
        else:
            self._debug_self_print(u"lshift操作：log_message为None，未添加到缓冲区")
        return self
        
    def set_min_log_level(self, level):
        """
        设置最低打印级别，支持字符串和整数
        Args:
            level (int|str): 日志级别，如 logging.INFO 或 "DEBUG"
        Returns:
            int: 实际设置的日志级别
        """
        if isinstance(level, str):
            level = level.upper()
            level = getattr(logging, level, logging.WARNING)
        self.min_log_level = level
        self.logger.setLevel(level)
        return level

    @staticmethod
    def set_debug_self_global(enable):
        u"""设置全局debug_self模式
        
        Args:
            enable (bool): 是否启用debug_self模式
        """
        LPrint.debug_self_global = enable
        if enable:
            print(u"[LPrint] 全局debug_self模式已启用: {}".format(enable))
        else:
            print(u"[LPrint] 全局debug_self模式已禁用: {}".format(enable))
    
    @staticmethod
    def get_debug_self_status():
        u"""获取debug_self状态
        
        Returns:
            dict: debug_self状态信息
        """
        return {
            'enabled': LPrint.debug_self_global,
            'description': u'debug_self模式用于调试lprint不打印信息的原因'
        }


    def _check_log_level_match(self):
        u"""检查当前日志级别是否匹配插件设置的级别
        
        Returns:
            bool: 级别是否匹配
        """
        if not hasattr(self, 'log_func'):
            return False
            
        # 获取当前日志的级别
        current_level = getattr(self.log_func, '_levelno', None)
        if current_level is None:
            # 通过函数名推断级别
            func_name = getattr(self.log_func, '__name__', '').lower()
            if 'debug' in func_name:
                current_level = logging.DEBUG
            elif 'info' in func_name:
                current_level = logging.INFO
            elif 'warning' in func_name or 'warn' in func_name:
                current_level = logging.WARNING
            elif 'error' in func_name:
                current_level = logging.ERROR
            elif 'critical' in func_name or 'fatal' in func_name:
                current_level = logging.CRITICAL
            else:
                # 默认使用 INFO 级别
                current_level = logging.INFO
        
        # 检查是否匹配设置的级别
        return current_level >= LPrint.logwgt_plugin_level

    @classmethod
    def _call_logwgt_plugin_with_mode(cls, log_message):
        u"""根据模式调用日志组件插件
        
        Args:
            log_message (unicode): 日志消息
        """
        if cls.logwgt_plugin is None:
            return
        
        try:
            if cls.logwgt_plugin_mode == 'append':
                # append 模式：累积消息内容
                if cls.logwgt_plugin_accumulated_content:
                    cls.logwgt_plugin_accumulated_content += u"\n" + log_message
                else:
                    cls.logwgt_plugin_accumulated_content = log_message
                
                # 调用插件函数，传入累积的内容
                cls.logwgt_plugin(cls.logwgt_plugin_accumulated_content)
                
            elif cls.logwgt_plugin_mode == 'set':
                # set 模式：直接传入当前消息（替换模式）
                cls.logwgt_plugin(log_message)
                
        except Exception as e:
            print(u"[LPrint] 日志组件插件模式处理异常: {}".format(str(e)))

    @classmethod
    def register_logwgt_plugin(cls, plugin_func, mode='append', level=logging.WARNING):
        u"""注册日志组件插件，支持两种模式和自定义级别
        
        Args:
            plugin_func (callable): 插件函数，接受一个参数(log_message)
                - log_message: 完整的日志消息字符串
            mode (unicode): 插件模式，支持以下值:
                - 'append': 追加模式，自动累积所有日志消息，每次调用插件时传入完整累积内容
                - 'set': 设置模式，每次只传入当前消息，适用于替换型显示
            level (int): 日志级别，只有等于或高于此级别的日志才会输出到日志框
                - logging.DEBUG (10): 调试信息
                - logging.INFO (20): 一般信息
                - logging.WARNING (30): 警告信息 (默认)
                - logging.ERROR (40): 错误信息
                - logging.CRITICAL (50): 严重错误信息
                
        Returns:
            bool: 注册是否成功
        
        Example:
            # 追加模式 (默认) - 内部自动累积，适合直接使用 setText
            log_wgt = self.findChild(QtWidgets.QTextEdit, "log_wgt")
            LPrint.register_logwgt_plugin(log_wgt.setText, mode='append')
            
            # 设置模式 - 每次只传入当前消息
            def my_log_setter(log_message):
                status_label.setText(log_message[:100])  # 只显示当前消息
            LPrint.register_logwgt_plugin(my_log_setter, mode='set')
            
            # 指定级别 - 只显示ERROR及以上级别的日志
            LPrint.register_logwgt_plugin(log_wgt.setText, level=logging.ERROR)
            
            # 清空累积内容 (仅对 append 模式有效)
            LPrint.clear_logwgt_plugin_content()
        """
        if not callable(plugin_func):
            print(u"[LPrint] 警告：插件函数必须是可调用对象")
            return False
        
        # 验证模式参数
        valid_modes = ['append', 'set']
        if mode not in valid_modes:
            print(u"[LPrint] 警告：无效的模式 '{}', 支持的模式: {}".format(mode, valid_modes))
            return False
        
        # 验证级别参数
        if not isinstance(level, int):
            print(u"[LPrint] 警告：级别必须是整数")
            return False
        
        cls.logwgt_plugin = plugin_func
        cls.logwgt_plugin_mode = mode
        cls.logwgt_plugin_level = level
        
        plugin_name = plugin_func.__name__ if hasattr(plugin_func, '__name__') else str(plugin_func)
        level_name = logging.getLevelName(level)
        print(u"[LPrint] 日志组件插件已注册: {} (模式: {}, 级别: {})".format(plugin_name, mode, level_name))
        return True
    
    @classmethod
    def unregister_logwgt_plugin(cls):
        u"""取消注册日志组件插件
        
        Returns:
            bool: 取消注册是否成功
        """
        if cls.logwgt_plugin is None:
            print(u"[LPrint] 当前没有注册的日志组件插件")
            return False
        
        plugin_name = cls.logwgt_plugin.__name__ if hasattr(cls.logwgt_plugin, '__name__') else str(cls.logwgt_plugin)
        mode = cls.logwgt_plugin_mode
        level_name = logging.getLevelName(cls.logwgt_plugin_level)
        cls.logwgt_plugin = None
        cls.logwgt_plugin_mode = 'append'  # 重置为默认模式
        cls.logwgt_plugin_level = logging.WARNING  # 重置为默认级别
        cls.logwgt_plugin_accumulated_content = u""  # 清空累积内容
        print(u"[LPrint] 日志组件插件已取消注册: {} (模式: {}, 级别: {})".format(plugin_name, mode, level_name))
        return True
    
    @classmethod
    def clear_logwgt_plugin_content(cls):
        u"""清空日志组件插件累积的内容
        
        Returns:
            bool: 清空是否成功
        """
        if cls.logwgt_plugin is None:
            print(u"[LPrint] 当前没有注册的日志组件插件")
            return False
        
        cls.logwgt_plugin_accumulated_content = u""
        print(u"[LPrint] 日志组件插件累积内容已清空")
        return True
    
    @classmethod
    def get_logwgt_plugin_info(cls):
        u"""获取当前注册的日志组件插件信息
        
        Returns:
            dict: 插件信息字典
                {
                    'registered': bool,    # 是否已注册
                    'plugin': callable,    # 插件函数对象
                    'name': unicode,       # 插件名称
                    'mode': unicode,       # 插件模式 ('append' 或 'set')
                    'level': int,          # 插件级别
                    'level_name': unicode  # 级别名称
                }
        """
        if cls.logwgt_plugin is None:
            return {
                'registered': False, 
                'plugin': None, 
                'name': None,
                'mode': None,
                'level': None,
                'level_name': None
            }
        
        plugin_name = cls.logwgt_plugin.__name__ if hasattr(cls.logwgt_plugin, '__name__') else str(cls.logwgt_plugin)
        level_name = logging.getLevelName(cls.logwgt_plugin_level)
        return {
            'registered': True,
            'plugin': cls.logwgt_plugin,
            'name': plugin_name,
            'mode': cls.logwgt_plugin_mode,
            'level': cls.logwgt_plugin_level,
            'level_name': level_name
        }
    


    def print_current_settings(self):
        u"""打印当前LPrint的关键设置
        """
        print(u"=== LPrint 当前设置 ===")
        print(u"max_prints_per_line: {}".format(self.max_prints_per_line))
        print(u"debug_self_global: {}".format(LPrint.debug_self_global))
        print(u"enable_function_range_check: {}".format(LPrint.enable_function_range_check))
        print(u"enable_line_counting: {} (性能优化)".format(LPrint.enable_line_counting))
        print(u"line_print_counts_dict 条目数: {}".format(len(LPrint.line_print_counts_dict)))
        print(u"详细计数器: {}".format(LPrint.line_print_counts_dict))
        
        # 添加日志组件插件信息
        plugin_info = LPrint.get_logwgt_plugin_info()
        if plugin_info['registered']:
            print(u"logwgt_plugin: {} (模式: {}, 级别: {})".format(plugin_info['name'], plugin_info['mode'], plugin_info['level_name']))
        else:
            print(u"logwgt_plugin: 未注册")
        
        print(u"=== 设置结束 ===")


# 将装饰器注册为 LPrint 的类方法，方便外部 @LPrint.with_end(...) 使用
LPrint.with_end = staticmethod(with_lprint_end)

# Python 2.7兼容的属性设置 - 使用元类方式
class LPrintMeta(type):
    """LPrint的元类，用于实现类级别的属性访问"""
    
    def __getattribute__(cls, name):
        if name == 'detailed_log_functions':
            return getattr(cls, '_detailed_log_functions', [])
        return super(LPrintMeta, cls).__getattribute__(name)
    
    def __setattr__(cls, name, value):
        if name == 'detailed_log_functions':
            cls._detailed_log_functions = value
            # 自动检查：如果列表不为空，则自动启用函数范围检查
            if value:
                cls.enable_function_range_check = True
                print(u"[lprint] 检测到detailed_log_functions不为空，已自动启用函数范围检查")
            else:
                cls.enable_function_range_check = False
                print(u"[lprint] detailed_log_functions为空，已自动禁用函数范围检查")
        else:
            super(LPrintMeta, cls).__setattr__(name, value)

# 应用元类到LPrint类 - Python 2.7兼容语法
LPrint.__metaclass__ = LPrintMeta
if sys.version_info[0] >= 3:
    # Python 3的语法，但由于在运行时应用，需要重新创建类
    pass

# 创建一个全局的 lprint 实例，供其他模块直接使用
lprint = LPrint()



def lprint_info():
    """显示系统编码信息 - 仅在需要时调用"""
    print(u"=== 系统编码信息 ===")
    try:
        print("sys.stdout.encoding:", repr(sys.stdout.encoding))
        print("sys.getdefaultencoding():", repr(sys.getdefaultencoding()))
        import locale
        print("locale.getpreferredencoding():", repr(locale.getpreferredencoding()))
        print("sys.getfilesystemencoding():", repr(sys.getfilesystemencoding()))
    except Exception as e:
        print("获取编码信息时出错:", str(e))


lprint_info()        
        
if __name__ == "__main__":
    """测试 LPrint 类"""

    logging.basicConfig(
    level=logging.DEBUG,         # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # === 性能优化测试 ===
    print(u"\n=== 性能优化功能测试 ===")
    
    # 显示当前性能设置
    print(u"当前性能设置:")
    performance_settings = LPrint.get_performance_settings()
    for key, value in performance_settings.items():
        print(u"  {}: {}".format(key, value))
    
    # === 新增：性能分析测试 ===
    print(u"\n=== 性能分析测试 ===")
    
    # 启用性能分析
    LPrint.enable_performance_analysis(True)
    
    # 执行一些lprint调用来收集性能数据
    print(u"执行测试调用以收集性能数据...")
    for i in range(10):
        lprint(u"性能测试 {}".format(i), u"数据", {"测试": True})
        lprint(u"带格式化的测试: %s", u"参数{}".format(i))
    
    # 显示性能报告
    print(u"\n=== 第一轮性能报告 ===")
    LPrint.print_performance_report()
    
    # 测试禁用行计数后的性能
    print(u"\n=== 测试禁用行计数功能后的性能 ===")
    LPrint.set_line_counting(False)
    LPrint.enable_performance_analysis(True)  # 重置计数器
    
    for i in range(10):
        lprint(u"禁用行计数测试 {}".format(i), u"性能优化", {"优化": True})
    
    print(u"\n=== 禁用行计数后的性能报告 ===")
    LPrint.print_performance_report()
    
    # 恢复设置
    LPrint.set_line_counting(True)
    
    # 测试禁用行计数的性能优化
    print(u"\n1. 测试禁用行计数功能:")
    LPrint.set_line_counting(False)  # 禁用行计数，提升性能
    
    # 在禁用状态下，debug='noprint'时将完全跳过frame操作
    os.environ['Lugwit_Debug'] = 'noprint'
    print(u"设置debug='noprint'后，以下lprint调用将被完全跳过:")
    lprint(u"这条消息不会打印，且不会执行任何frame操作")
    lprint(u"性能优化测试", u"跳过所有开销")
    
    # 恢复正常模式
    os.environ['Lugwit_Debug'] = 'inspect'
    LPrint.set_line_counting(True)  # 重新启用行计数
    print(u"恢复正常模式")

    # === 性能时间测试 (使用独立模块) ===
    print(u"\n=== 性能时间测试 (使用独立模块) ===")
    
    try:
        # 导入独立的性能测试模块
        from performance_test import run_all_performance_tests
        
        # 运行完整的性能测试套件
        all_results = run_all_performance_tests(lprint)
        
        print(u"\n=== 性能测试模块调用成功 ===")
        
    except ImportError as e:
        print(u"导入性能测试模块失败: {}".format(str(e)))
        print(u"请确保performance_test.py文件在同一目录下")
    except Exception as e:
        print(u"性能测试执行失败: {}".format(str(e)))
    
    # 使用全局 lprint 实例
    lprint((u'你好', u'世界', {u'你\n好': u'世界'}, (u'你好', print)))
    lprint( "😊")
    lprint(u"😀")
    lprint("😀",u"😀",)
    # ---------------- 以下为装饰器测试代码 ----------------
    # 示范如何在普通函数上使用装饰器，确保函数结束时自动 flush lprint。
    # • 默认：@lprint.with_end 或 @LPrint.with_end()
    # • 只清空缓存不打印：@lprint.with_end(clear_only=True)
    # 注意：此处仅测试用，正式库中可删除或移至单元测试文件。
    
    # 测试不加u前缀的中文字符串（这应该不再报错）
    lprint("资产 %d: %s (类型: %s)" % (234, '世界', '世界'))
    
    # 测试新的lprint格式化功能，解决混合编码问题  
    print(u"\n=== 使用lprint内置格式化解决混合编码问题 ===")
    lprint(u"资产 %d: %s (类型: %s)", 234, '世界', u'世界')
    
    # 测试更多混合情况
    lprint(u"格式化测试: %s + %s = %s", u'中文', u'Unicode', '成功')
    lprint(u"[缓存加载] ✅ 缓存数据应用完成，UI已快速初始化",level=logging.DEBUG)
    # 原来的测试（会报错的版本，注释掉）
    # lprint(u"资产 %d: %s (类型: %s)" % (234, '世界', u'世界'))
    @lprint.with_end
    def print_end():
        print(2222222222222222222222222222222222222)
        lprint<<"aa"<<222<<u"123"
        lprint<<("aa",222,u"中文")
        lprint<<"bb"
        try:
            1/0
        except:
            pass
    
    print_end()
    print(u"中文")
    # -----------------------------------------------------

    


