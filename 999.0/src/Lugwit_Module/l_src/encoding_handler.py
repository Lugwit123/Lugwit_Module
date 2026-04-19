# -*- coding: utf-8 -*-
"""
编码处理模块 - 基于 usualFunc_old.py 的编码处理逻辑（修复版）

该模块专门处理 Python 2.7 环境下的中文编码问题，
特别是在 Maya 和 Windows 环境中的字符串显示。

主要功能：
1. 智能检测和转换字符串编码  
2. 安全的 Unicode 转换
3. 多重回退机制的输出处理
4. JSON 序列化的编码处理
5. emoji和特殊Unicode字符处理
6. 与 usualFunc_old.py 兼容的接口
"""

from __future__ import print_function, absolute_import
import sys
import traceback
import json
import logging

# Python 版本兼容性
if sys.version_info[0] == 2:
    string_types = (str, unicode)
    text_type = unicode
    binary_type = str
else:
    string_types = (str,)
    text_type = str
    binary_type = bytes


class EncodingHandler(object):
    """编码处理器类 - 兼容 usualFunc_old.py"""
    
    @staticmethod
    def get_system_encoding_info():
        """获取系统编码信息"""
        encoding_info = {
            'stdout_encoding': 'utf-8',
            'system_encoding': 'utf-8'
        }
        
        try:
            encoding_info['stdout_encoding'] = sys.stdout.encoding or 'utf-8'
            import locale
            encoding_info['system_encoding'] = locale.getpreferredencoding() or 'utf-8'
        except Exception:
            pass
            
        return encoding_info
    
    @staticmethod
    def safe_decode(text):
        """
        安全解码字符串为 Unicode (Python 2) 或 str (Python 3)
        兼容 usualFunc_old.py 中的 convertToUnicode 函数
        """
        if sys.version_info[0] == 3:
            # Python 3 中字符串已经是 Unicode
            return str(text) if not isinstance(text, str) else text
        
        # Python 2 处理
        if isinstance(text, unicode):
            return text  # 已经是 Unicode
        
        if not isinstance(text, str):
            try:
                return unicode(str(text))
            except Exception:
                return unicode(repr(text))
        
        # 基于用户反馈，在 Python 2 中优先使用 gbk，然后 utf-8
        encoding_order = ['gbk', 'utf-8', 'cp936', 'latin1']
        
        for encoding in encoding_order:
            try:
                return text.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                continue
        
        # 最后的保险方案
        try:
            return text.decode('utf-8', 'replace')
        except Exception:
            return unicode(repr(text))
    
    @staticmethod
    def handle_msg_list(msg_list):
        """
        处理消息列表，合并为多行文本
        兼容 usualFunc_old.py 中 _LPrintHandler.emit 的逻辑
        """
        if sys.version_info[0] == 2:
            return u"\n".join([unicode(m) for m in msg_list])
        else:
            return "\n".join([str(m) for m in msg_list])
    
    @staticmethod
    def handle_escape_chars(msg):
        """
        处理常见转义符显示问题
        兼容 usualFunc_old.py 中的逻辑
        """
        if isinstance(msg, str):
            return msg.replace(r'\n', '\n').replace(r'\\', '\\')
        elif sys.version_info[0] == 2 and isinstance(msg, unicode):
            return msg.replace(r'\n', u'\n').replace(r'\\', u'\\')
        return msg
    
    @staticmethod
    def _filter_special_unicode(unicode_text):
        """
        过滤特殊Unicode字符，特别是emoji，使其在cp936/gbk环境下可以显示
        """
        if sys.version_info[0] == 3:
            return unicode_text  # Python 3 暂不处理
        
        if not isinstance(unicode_text, unicode):
            return unicode_text
        
        filtered_text = u""
        for char in unicode_text:
            code_point = ord(char)
            
            # 检查字符是否可以在cp936/gbk编码下显示
            try:
                char.encode('cp936')
                filtered_text += char
            except UnicodeEncodeError:
                # 处理不同类型的特殊字符
                if 0x1F600 <= code_point <= 0x1F64F:  # 表情符号
                    filtered_text += u"[表情]"
                elif 0x1F300 <= code_point <= 0x1F5FF:  # 各种符号
                    filtered_text += u"[符号]"
                elif 0x1F680 <= code_point <= 0x1F6FF:  # 交通和地图符号
                    filtered_text += u"[图标]"
                elif 0x2600 <= code_point <= 0x26FF:   # 杂项符号
                    filtered_text += u"[符号]"
                elif 0x2700 <= code_point <= 0x27BF:   # 装饰符号
                    filtered_text += u"[装饰]"
                elif code_point > 0x10000:  # 其他高位Unicode字符
                    filtered_text += u"[特殊字符:U+{:X}]".format(code_point)
                elif code_point > 0x7F:  # 其他非ASCII字符
                    filtered_text += u"[U+{:04X}]".format(code_point)
                else:
                    filtered_text += u"?"
        
        return filtered_text
    
    @staticmethod
    def enhanced_output(msg):
        """
        增强的输出函数，特别处理emoji和特殊Unicode字符
        """
        if sys.version_info[0] == 3:
            # Python 3.x 处理
            if not isinstance(msg, str):
                msg = str(msg)
            
            try:
                print(msg)
                return True
            except Exception:
                try:
                    # 如果失败，尝试使用buffer
                    if hasattr(sys.stdout, 'buffer'):
                        sys.stdout.buffer.write((msg + '\n').encode('utf-8', 'replace'))
                        return True
                except Exception:
                    pass
                return False
        
        # Python 2.7 处理 - 使用与 usualFunc_old.py 完全相同的逻辑
        try:
            # 获取系统编码信息
            try:
                stdout_encoding = sys.stdout.encoding or 'utf-8'
                import locale
                system_encoding = locale.getpreferredencoding() or 'utf-8'
            except:
                stdout_encoding = 'utf-8'
                system_encoding = 'utf-8'
            
            # 统一转换为 unicode
            if isinstance(msg, str):
                # 智能检测编码
                try:
                    # 首先尝试UTF-8解码
                    unicode_msg = msg.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        # 然后尝试系统编码
                        unicode_msg = msg.decode(system_encoding)
                    except:
                        # 最后使用UTF-8强制解码
                        unicode_msg = msg.decode('utf-8', 'replace')
            elif isinstance(msg, unicode):
                unicode_msg = msg
            else:
                # 其他类型转为unicode
                unicode_msg = unicode(str(msg), 'utf-8', 'replace')
            
            # 专门处理emoji和特殊Unicode字符
            filtered_msg = EncodingHandler._filter_special_unicode(unicode_msg)
            
            # 添加换行符
            output_text = filtered_msg + u'\n'
            
            # 尝试多种输出方式
            success = False
            
            # 方法1: 直接输出unicode
            if not success:
                try:
                    sys.stdout.write(output_text)
                    sys.stdout.flush()
                    success = True
                except (UnicodeEncodeError, LookupError):
                    pass
            
            # 方法2: 使用stdout编码
            if not success:
                try:
                    encoded_text = output_text.encode(stdout_encoding, 'replace')
                    sys.stdout.write(encoded_text)
                    sys.stdout.flush()
                    success = True
                except (UnicodeEncodeError, LookupError):
                    pass
            
            # 方法3: 使用UTF-8编码
            if not success:
                try:
                    encoded_text = output_text.encode('utf-8', 'replace')
                    sys.stdout.write(encoded_text)
                    sys.stdout.flush()
                    success = True
                except (UnicodeEncodeError, LookupError):
                    pass
            
            # 方法4: 使用系统编码
            if not success:
                try:
                    encoded_text = output_text.encode(system_encoding, 'replace')
                    sys.stdout.write(encoded_text)
                    sys.stdout.flush()
                    success = True
                except (UnicodeEncodeError, LookupError):
                    pass
            
            # 方法5: 最后的保险方案 - 替换不可显示字符
            if not success:
                try:
                    # 将不可显示的字符替换为问号或描述
                    safe_text = u""
                    for char in output_text:
                        try:
                            char.encode(stdout_encoding)
                            safe_text += char
                        except:
                            # 尝试显示 Unicode 码点
                            if ord(char) > 127:
                                safe_text += u"[U+{:04X}]".format(ord(char))
                            else:
                                safe_text += u"?"
                    
                    print(safe_text.encode('ascii', 'replace'))
                    success = True
                except:
                    print("lprint: Unable to display content")
            
            return success
            
        except Exception as e:
            # 记录错误但不要崩溃
            try:
                if sys.version_info[0] == 2:
                    print("Logging error: " + str(e).encode('ascii', 'replace'))
                else:
                    print("Logging error: " + str(e))
            except:
                pass
            return False
    
    @staticmethod
    def safe_json_dumps(obj, **kwargs):
        """
        安全的JSON序列化，兼容 usualFunc_old.py 的逻辑
        """
        # 设置默认参数
        default_kwargs = {
            'ensure_ascii': False,
            'indent': 4,
            'sort_keys': True,
            'default': str
        }
        default_kwargs.update(kwargs)
        
        try:
            # 首先尝试直接序列化
            return json.dumps(obj, **default_kwargs)
        except Exception:
            # 如果失败，尝试简化处理
            try:
                # 简化的字符串表示
                return json.dumps(str(obj), **default_kwargs)
            except Exception:
                return '["<序列化失败>"]'
    
    @staticmethod
    def handle_code_context_decode(code_context):
        """
        处理 code_context 的解码，兼容 usualFunc_old.py 的逻辑
        """
        if sys.version_info[0] == 2 and isinstance(code_context, str):
            try:
                return code_context.decode('utf-8')
            except UnicodeDecodeError:
                return code_context
        return code_context
    
    @staticmethod
    def handle_gbk_decode(text):
        """
        处理可能包含 gbk 编码的文本，兼容 usualFunc_old.py 的逻辑
        """
        if sys.version_info[0] == 3:
            return text  # Python 3 不需要特殊处理
        
        if '\\x' in repr(text):
            # 可能包含十六进制编码的字符串
            try:
                return text.decode('gbk')
            except:
                return text
        
        return text
    
    @staticmethod
    def convert_for_json(obj, current_depth=0):
        """
        将对象转换为可JSON序列化的形式，兼容 usualFunc_old.py 的 stringify_non_serializable
        """
        if current_depth > 999:
            return str(obj)
        
        if isinstance(obj, dict):
            return {
                EncodingHandler.safe_decode(k): EncodingHandler.convert_for_json(v, current_depth+1) 
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [EncodingHandler.convert_for_json(v, current_depth+1) for v in obj]
        elif isinstance(obj, tuple):
            return tuple(EncodingHandler.convert_for_json(v, current_depth+1) for v in obj)
        elif isinstance(obj, (int, float)):
            return obj
        elif obj is None:
            return None
        elif isinstance(obj, BaseException):
            return str(obj) if sys.version_info[0] == 3 else getattr(obj, 'message', str(obj))
        else:
            return EncodingHandler.safe_decode(obj)
    
    @staticmethod
    def safe_format(format_string, *args):
        """
        安全的字符串格式化函数，避免Unicode/字节字符串混合时的编码错误
        解决Python 2.7中 u"字符串" % (字节字符串,) 导致的UnicodeDecodeError
        
        Args:
            format_string: 格式化字符串
            *args: 格式化参数
            
        Returns:
            str/unicode: 格式化后的字符串
        """
        if sys.version_info[0] == 2:
            # 在Python 2中，确保所有参数都是相同的编码类型
            if isinstance(format_string, unicode):
                # 如果格式字符串是Unicode，将所有参数转换为Unicode
                safe_args = []
                for arg in args:
                    if isinstance(arg, str):
                        safe_args.append(EncodingHandler.safe_decode(arg))
                    elif isinstance(arg, unicode):
                        safe_args.append(arg)
                    else:
                        safe_args.append(unicode(str(arg)))
                return format_string % tuple(safe_args)
            else:
                # 如果格式字符串是字节字符串，保持所有参数为字节字符串
                safe_args = []
                for arg in args:
                    if isinstance(arg, unicode):
                        safe_args.append(arg.encode('utf-8'))
                    elif isinstance(arg, str):
                        safe_args.append(arg)
                    else:
                        safe_args.append(str(arg))
                return format_string % tuple(safe_args)
        else:
            # Python 3中直接使用普通格式化
            return format_string % args

    @staticmethod
    def filter_args_emoji(args):
        """
        过滤args参数中的emoji字符，用于lprint等函数的参数处理
        支持混合类型的参数（unicode, str, 其他类型）
        
        Args:
            args: 参数元组，可能包含emoji字符
            
        Returns:
            tuple: 过滤了emoji字符的参数元组
        """
        if sys.version_info[0] == 3:
            return args  # Python 3 暂不处理
        
        safe_args = []
        for arg in args:
            if isinstance(arg, unicode):
                # 使用内置的emoji过滤器
                safe_arg = EncodingHandler._filter_special_unicode(arg)
                safe_args.append(safe_arg)
            elif isinstance(arg, str):
                # 处理str类型，先转换为unicode再过滤
                try:
                    unicode_arg = arg.decode('utf-8')
                    safe_arg = EncodingHandler._filter_special_unicode(unicode_arg)
                    safe_args.append(safe_arg)
                except UnicodeDecodeError:
                    # 如果无法解码，尝试gbk
                    try:
                        unicode_arg = arg.decode('gbk')
                        safe_arg = EncodingHandler._filter_special_unicode(unicode_arg)
                        safe_args.append(safe_arg)
                    except UnicodeDecodeError:
                        safe_args.append(arg)  # 保持原样
            else:
                safe_args.append(arg)
        
        return tuple(safe_args)
    
    @staticmethod
    def filter_args_emoji_builtin(args):
        """
        内置的emoji过滤器，当外部编码处理器不可用时使用
        使用简化的emoji检测范围和处理逻辑
        
        Args:
            args: 参数元组
            
        Returns:
            tuple: 过滤了emoji字符的参数元组
        """
        if sys.version_info[0] == 3:
            return args  # Python 3 暂不处理
        
        safe_args = []
        for arg in args:
            if isinstance(arg, unicode):
                # 内置emoji过滤
                safe_arg = u""
                for char in arg:
                    try:
                        code_point = ord(char)
                        if (0x1F600 <= code_point <= 0x1F64F or  # 表情符号
                            0x1F300 <= code_point <= 0x1F5FF or  # 各种符号
                            0x1F680 <= code_point <= 0x1F6FF):   # 交通符号
                            safe_arg += u"[emoji]"
                        else:
                            char.encode('cp936')
                            safe_arg += char
                    except UnicodeEncodeError:
                        safe_arg += u"[?]"
                safe_args.append(safe_arg)
            elif isinstance(arg, str):
                # 处理str类型的emoji
                try:
                    unicode_arg = arg.decode('utf-8')
                    safe_arg = u""
                    for char in unicode_arg:
                        try:
                            code_point = ord(char)
                            if (0x1F600 <= code_point <= 0x1F64F or
                                0x1F300 <= code_point <= 0x1F5FF or
                                0x1F680 <= code_point <= 0x1F6FF):
                                safe_arg += u"[emoji]"
                            else:
                                char.encode('cp936')
                                safe_arg += char
                        except UnicodeEncodeError:
                            safe_arg += u"[?]"
                    safe_args.append(safe_arg)
                except UnicodeDecodeError:
                    safe_args.append(arg)  # 保持原样
            else:
                safe_args.append(arg)
        
        return tuple(safe_args)


# 兼容性函数，保持与 usualFunc_old.py 的接口一致
def convertToUnicode_py2(_string):
    """转换为 Unicode（Python 2）- 兼容 usualFunc_old.py"""
    return EncodingHandler.safe_decode(_string)


def convertToUnicode(_string):
    """根据 Python 版本转换为 Unicode 字符串 - 兼容 usualFunc_old.py"""
    return EncodingHandler.safe_decode(_string)


def stringify_non_serializable(obj, current_depth=0):
    """将无法序列化的对象转换为可序列化的形式 - 兼容 usualFunc_old.py"""
    return EncodingHandler.convert_for_json(obj, current_depth)


# 创建标准的 LPrintHandler 类，继承自 logging.StreamHandler
class LPrintHandler(logging.StreamHandler):
    """标准的 LPrint 处理器，继承自 logging.StreamHandler，使用独立的编码处理"""
    
    def __init__(self, stream=None):
        # 调用父类构造函数，确保标准 logging 行为
        super(LPrintHandler, self).__init__(stream or sys.stdout)
    
    def emit(self, record):
        """发出日志记录，使用编码处理器，保持与标准 StreamHandler 兼容"""
        try:
            msg = record.msg
            
            # 如果是 list, 合并为多行文本
            if isinstance(msg, (list, tuple)):
                msg = EncodingHandler.handle_msg_list(msg)
            
            # 处理常见转义符显示问题
            msg = EncodingHandler.handle_escape_chars(msg)
            
            # 使用增强的输出函数输出消息
            success = EncodingHandler.enhanced_output(msg)
            
            # 🔥 关键：使用标准 StreamHandler 的 flush 机制
            self.flush()
            
            # 如果增强输出失败，回退到标准 StreamHandler 行为
            if not success:
                # 临时修改 record.msg 为处理后的消息
                original_msg = record.msg
                record.msg = msg
                try:
                    # 调用父类的 emit 方法作为备用方案
                    super(LPrintHandler, self).emit(record)
                finally:
                    # 恢复原始消息
                    record.msg = original_msg
                sys.stdout.flush()
            
        except Exception:
            # 使用标准的错误处理机制
            self.handleError(record)


# 用于测试的函数
def test_encoding_handler():
    """测试编码处理器与 usualFunc_old.py 的兼容性"""
    print(u"=== 测试编码处理器兼容性 ===")
    
    # 测试系统编码信息
    encoding_info = EncodingHandler.get_system_encoding_info()
    print(u"系统编码信息:")
    for key, value in encoding_info.items():
        print(u"  {}: {}".format(key, repr(value)))
    
    # 测试字符串处理
    test_strings = [
        u"中文测试字符串",
        u"开始执行: 加载缓存文件",
        u"文件: usualFunc.py 第35行",
        u"[lprint 限制] 当前第2次打印",
        "混合字符串 with English",
    ]
    
    print(u"\n=== 测试字符串处理 ===")
    for i, test_str in enumerate(test_strings):
        print(u"测试 {}: ".format(i+1), end='')
        success = EncodingHandler.enhanced_output(test_str)
        if not success:
            print(u"[打印失败]")
    
    # 测试JSON序列化
    print(u"\n=== 测试JSON序列化 ===")
    test_obj = {
        u"中文键": u"中文值",
        "english_key": u"中英混合 mixed value",
        "list": [u"项目1", u"项目2", 123],
    }
    
    json_result = EncodingHandler.safe_json_dumps(test_obj)
    print(u"JSON序列化结果:")
    EncodingHandler.enhanced_output(json_result)
    
    print(u"\n=== 测试完成 ===")


if __name__ == "__main__":
    test_encoding_handler() 