# -*- coding: utf-8 -*-
"""
独立的编码测试模块
用于验证不同的中文输出方案，找到最适合的解决方案
"""
from __future__ import print_function
import sys
import os

# Python 版本兼容性
if sys.version_info[0] == 2:
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes

def test_system_info():
    """测试系统编码信息"""
    print("=== 系统编码信息 ===")
    try:
        print("Python 版本:", sys.version_info)
        print("sys.stdout.encoding:", repr(getattr(sys.stdout, 'encoding', None)))
        print("sys.getdefaultencoding():", repr(sys.getdefaultencoding()))
        
        import locale
        print("locale.getpreferredencoding():", repr(locale.getpreferredencoding()))
        print("sys.getfilesystemencoding():", repr(sys.getfilesystemencoding()))
        print("操作系统:", os.name)
        
        if os.name == 'nt':
            print("Windows 环境")
            # 检查代码页
            try:
                import subprocess
                result = subprocess.check_output('chcp', shell=True, universal_newlines=True)
                print("当前代码页:", result.strip())
            except:
                print("无法获取代码页信息")
    except Exception as e:
        print("获取系统信息出错:", e)

def method1_simple_print():
    """方法1：简单直接打印"""
    print("\n=== 方法1：简单直接打印 ===")
    test_strings = [
        u"中文测试",
        u"这是一个测试",
        u"包含中文的字符串",
        [u"列表", u"中文", u"内容"]
    ]
    
    for i, s in enumerate(test_strings):
        try:
            print("测试 {}: {}".format(i+1, s))
        except Exception as e:
            print("测试 {} 失败: {}".format(i+1, e))

def method2_encode_cp936():
    """方法2：使用 cp936 编码"""
    print("\n=== 方法2：使用 cp936 编码 ===")
    test_strings = [
        u"中文测试",
        u"这是一个测试", 
        u"包含中文的字符串"
    ]
    
    for i, s in enumerate(test_strings):
        try:
            if sys.version_info[0] == 2:
                encoded = s.encode('cp936', 'replace')
                sys.stdout.write("测试 {}: ".format(i+1))
                sys.stdout.write(encoded)
                sys.stdout.write('\n')
                sys.stdout.flush()
            else:
                print("测试 {}: {}".format(i+1, s))
        except Exception as e:
            print("测试 {} 失败: {}".format(i+1, e))

def method3_encode_utf8():
    """方法3：使用 UTF-8 编码"""
    print("\n=== 方法3：使用 UTF-8 编码 ===")
    test_strings = [
        u"中文测试",
        u"这是一个测试",
        u"包含中文的字符串"
    ]
    
    for i, s in enumerate(test_strings):
        try:
            if sys.version_info[0] == 2:
                encoded = s.encode('utf-8', 'replace')
                sys.stdout.write("测试 {}: ".format(i+1))
                sys.stdout.write(encoded)
                sys.stdout.write('\n')
                sys.stdout.flush()
            else:
                print("测试 {}: {}".format(i+1, s))
        except Exception as e:
            print("测试 {} 失败: {}".format(i+1, e))

def method4_ascii_safe():
    """方法4：ASCII 安全输出"""
    print("\n=== 方法4：ASCII 安全输出 ===")
    test_strings = [
        u"中文测试",
        u"这是一个测试",
        u"包含中文的字符串"
    ]
    
    for i, s in enumerate(test_strings):
        try:
            if sys.version_info[0] == 2:
                # 转换为 Unicode 码点表示
                safe_str = ""
                for char in s:
                    if ord(char) < 128:
                        safe_str += char
                    else:
                        safe_str += "\\u{:04x}".format(ord(char))
                print("测试 {}: {}".format(i+1, safe_str))
            else:
                print("测试 {}: {}".format(i+1, s))
        except Exception as e:
            print("测试 {} 失败: {}".format(i+1, e))

def method5_smart_detect():
    """方法5：智能编码检测"""
    print("\n=== 方法5：智能编码检测 ===")
    
    def smart_print(text):
        if sys.version_info[0] == 2:
            if isinstance(text, unicode):
                # 尝试多种编码方案
                encodings = ['cp936', 'gbk', 'utf-8']
                for encoding in encodings:
                    try:
                        encoded = text.encode(encoding, 'replace')
                        sys.stdout.write(encoded)
                        sys.stdout.flush()
                        return True
                    except:
                        continue
                # 如果都失败，使用 repr
                sys.stdout.write(repr(text))
                sys.stdout.flush()
                return False
            else:
                sys.stdout.write(str(text))
                sys.stdout.flush()
                return True
        else:
            print(text, end='')
            return True
    
    test_strings = [
        u"中文测试",
        u"这是一个测试",
        u"包含中文的字符串"
    ]
    
    for i, s in enumerate(test_strings):
        try:
            sys.stdout.write("测试 {}: ".format(i+1))
            success = smart_print(s)
            sys.stdout.write(" [{}]\n".format("成功" if success else "失败"))
        except Exception as e:
            print("测试 {} 失败: {}".format(i+1, e))

def test_json_serialization():
    """测试 JSON 序列化"""
    print("\n=== JSON 序列化测试 ===")
    import json
    
    test_data = [
        u"中文字符串",
        {u"键": u"值", u"中文": u"测试"},
        [u"列表", u"中文", 123],
        (u"元组", u"测试")
    ]
    
    for i, data in enumerate(test_data):
        try:
            if sys.version_info[0] == 2:
                # Python 2.7 JSON 处理
                serialized = json.dumps(data, ensure_ascii=False, indent=2, default=lambda x: unicode(str(x)))
                print("JSON 测试 {}:".format(i+1))
                # 尝试安全输出序列化结果
                for line in serialized.split('\n'):
                    if line.strip():
                        try:
                            encoded = line.encode('cp936', 'replace')
                            sys.stdout.write(encoded + '\n')
                        except:
                            print(repr(line))
            else:
                serialized = json.dumps(data, ensure_ascii=False, indent=2, default=str)
                print("JSON 测试 {}:\n{}".format(i+1, serialized))
        except Exception as e:
            print("JSON 测试 {} 失败: {}".format(i+1, e))

def comprehensive_test():
    """综合测试函数"""
    print("开始编码方案测试...\n")
    
    # 系统信息
    test_system_info()
    
    # 测试各种方法
    method1_simple_print()
    method2_encode_cp936()
    method3_encode_utf8()
    method4_ascii_safe()
    method5_smart_detect()
    
    # JSON 测试
    test_json_serialization()
    
    print("\n=== 测试完成 ===")
    print("请查看哪种方法的中文显示效果最好")

if __name__ == "__main__":
    comprehensive_test() 