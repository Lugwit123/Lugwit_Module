# -*- coding: utf-8 -*-
"""
最终的编码处理模块
基于实际测试结果，专门针对 Windows cp936 环境优化
"""
from __future__ import print_function
import sys
import json

# Python 版本兼容性
if sys.version_info[0] == 2:
    text_type = unicode
    string_types = (str, unicode)
else:
    text_type = str
    string_types = (str,)

class FinalEncodingHandler(object):
    """最终的编码处理器，基于实际测试结果优化"""
    
    @staticmethod
    def safe_decode(data):
        """安全解码，返回 Unicode 字符串"""
        if sys.version_info[0] == 2:
            if isinstance(data, unicode):
                return data
            elif isinstance(data, str):
                # 尝试常见编码
                for encoding in ['utf-8', 'cp936', 'gbk']:
                    try:
                        return data.decode(encoding)
                    except UnicodeDecodeError:
                        continue
                # 如果都失败，使用错误替换
                return data.decode('utf-8', 'replace')
            else:
                return unicode(str(data))
        else:
            return str(data)
    
    @staticmethod
    def safe_print(*args, **kwargs):
        """安全打印函数，基于测试结果优化"""
        end_char = kwargs.pop('end', '\n')
        
        if sys.version_info[0] == 2:
            # Python 2.7 优化方案
            # 基于测试结果：直接打印 unicode 效果最好
            processed_args = []
            for arg in args:
                if isinstance(arg, unicode):
                    processed_args.append(arg)
                elif isinstance(arg, str):
                    processed_args.append(FinalEncodingHandler.safe_decode(arg))
                else:
                    processed_args.append(unicode(str(arg)))
            
            # 组合输出
            output = u' '.join(processed_args)
            if end_char != '\n':
                output += FinalEncodingHandler.safe_decode(end_char)
            
            # 直接打印（测试证明这种方式最好）
            try:
                print(output, end='' if end_char != '\n' else None)
            except:
                # 备选方案：使用 cp936 编码
                try:
                    encoded = output.encode('cp936', 'replace')
                    if end_char == '\n':
                        encoded += '\n'
                    sys.stdout.write(encoded)
                    sys.stdout.flush()
                except:
                    # 最后备选：repr 输出
                    print(repr(output))
        else:
            # Python 3.x
            print(*args, end=end_char, **kwargs)
    
    @staticmethod
    def convert_for_json(obj):
        """转换对象为 JSON 友好格式"""
        if isinstance(obj, string_types):
            return FinalEncodingHandler.safe_decode(obj)
        elif isinstance(obj, (list, tuple)):
            return [FinalEncodingHandler.convert_for_json(item) for item in obj]
        elif isinstance(obj, dict):
            return {
                FinalEncodingHandler.safe_decode(str(k)): FinalEncodingHandler.convert_for_json(v) 
                for k, v in obj.items()
            }
        else:
            return FinalEncodingHandler.safe_decode(str(obj))
    
    @staticmethod
    def safe_json_dumps(obj, **kwargs):
        """安全的 JSON 序列化"""
        try:
            if sys.version_info[0] == 2:
                # Python 2.7 JSON 处理
                converted = FinalEncodingHandler.convert_for_json(obj)
                return json.dumps(
                    converted,
                    ensure_ascii=False,
                    default=lambda x: FinalEncodingHandler.safe_decode(str(x)),
                    **kwargs
                )
            else:
                # Python 3.x
                return json.dumps(obj, ensure_ascii=False, default=str, **kwargs)
        except Exception:
            # 序列化失败的备选方案
            if sys.version_info[0] == 2:
                return u'["序列化失败"]'
            else:
                return '["序列化失败"]'

# 便捷函数
def safe_decode(data):
    return FinalEncodingHandler.safe_decode(data)

def safe_print(*args, **kwargs):
    return FinalEncodingHandler.safe_print(*args, **kwargs)

def convert_for_json(obj):
    return FinalEncodingHandler.convert_for_json(obj)

def safe_json_dumps(obj, **kwargs):
    return FinalEncodingHandler.safe_json_dumps(obj, **kwargs)

# 测试代码
if __name__ == "__main__":
    print("=== 最终编码处理模块测试 ===")
    
    # 测试安全打印
    print("\n1. 安全打印测试:")
    safe_print(u"中文测试", u"第二个参数", 123)
    
    # 测试 JSON 序列化
    print("\n2. JSON 序列化测试:")
    test_data = {
        u"中文键": u"中文值",
        u"列表": [u"项目1", u"项目2", 123],
        u"数字": 456
    }
    json_str = safe_json_dumps(test_data, indent=2)
    print("JSON 结果:")
    safe_print(json_str)
    
    print("\n=== 测试完成 ===") 