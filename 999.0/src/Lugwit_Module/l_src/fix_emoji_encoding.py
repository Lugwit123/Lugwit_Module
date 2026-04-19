# -*- coding: utf-8 -*-
"""
专门修复emoji和特殊Unicode字符编码问题的脚本
"""

from __future__ import print_function
import sys
import os

def safe_print_unicode(text):
    """安全打印Unicode文本，处理emoji等特殊字符"""
    if sys.version_info[0] == 3:
        try:
            print(text)
            return True
        except:
            print(repr(text))
            return False
    
    # Python 2 处理
    if not isinstance(text, unicode):
        try:
            text = unicode(text)
        except:
            text = unicode(str(text))
    
    # 方法1: 直接输出
    try:
        sys.stdout.write(text + u'\n')
        sys.stdout.flush()
        return True
    except UnicodeEncodeError:
        pass
    
    # 方法2: 过滤特殊字符
    try:
        # 将无法编码的字符替换为描述
        safe_text = u""
        for char in text:
            try:
                char.encode('cp936')
                safe_text += char
            except UnicodeEncodeError:
                # 替换emoji和特殊字符为描述
                code_point = ord(char)
                if code_point > 0x10000:  # 高位Unicode字符（包括emoji）
                    safe_text += u"[emoji:U+{:X}]".format(code_point)
                elif code_point > 0x7F:  # 其他非ASCII字符
                    safe_text += u"[U+{:04X}]".format(code_point)
                else:
                    safe_text += u"?"
        
        sys.stdout.write(safe_text + u'\n')
        sys.stdout.flush()
        return True
    except:
        pass
    
    # 方法3: 完全安全的ASCII输出
    try:
        ascii_repr = repr(text)
        print(ascii_repr)
        return True
    except:
        print("无法显示的Unicode内容")
        return False

def test_problematic_content():
    """测试有问题的内容"""
    print(u"=== 测试有问题的内容 ===")
    
    # 这是从用户反馈中提取的有问题的参数
    test_args = (u'Unicode:', u'\U0001f600', 'UTF-8:', '\xf0\x9f\x98\x8a', '\xe6\x95\xb0\xe5\xad\x97:', 123)
    
    print(u"原始参数内容:")
    for i, arg in enumerate(test_args):
        print(u"  参数 {}: ".format(i+1), end='')
        safe_print_unicode(unicode(arg) if not isinstance(arg, unicode) else arg)

def create_enhanced_encoding_handler():
    """创建增强的编码处理器，专门处理emoji"""
    enhanced_code = '''
# 增强版编码处理 - 专门处理emoji和特殊字符
def enhanced_safe_decode(text):
    """增强的安全解码，处理emoji等特殊字符"""
    if sys.version_info[0] == 3:
        return str(text) if not isinstance(text, str) else text
    
    # Python 2 处理
    if isinstance(text, unicode):
        return text
    
    if not isinstance(text, str):
        try:
            return unicode(str(text))
        except:
            return unicode(repr(text))
    
    # 尝试不同编码
    for encoding in ['gbk', 'utf-8', 'cp936', 'latin1']:
        try:
            return text.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    
    # 如果都失败，使用错误处理
    try:
        return text.decode('utf-8', 'replace')
    except:
        return unicode(repr(text))

def enhanced_safe_output(msg):
    """增强的安全输出，处理emoji等特殊字符"""
    if sys.version_info[0] == 3:
        try:
            print(msg)
            return True
        except:
            try:
                print(repr(msg))
                return True
            except:
                return False
    
    # Python 2 处理
    if not isinstance(msg, unicode):
        msg = enhanced_safe_decode(msg)
    
    output_text = msg + u'\\n'
    
    # 尝试直接输出
    try:
        sys.stdout.write(output_text)
        sys.stdout.flush()
        return True
    except UnicodeEncodeError:
        pass
    
    # 过滤特殊字符输出
    try:
        safe_text = u""
        for char in output_text:
            try:
                char.encode('cp936')
                safe_text += char
            except UnicodeEncodeError:
                code_point = ord(char)
                if code_point > 0x10000:  # emoji范围
                    safe_text += u"[emoji]"
                elif code_point > 0x7F:
                    safe_text += u"[{}]".format(hex(code_point))
                else:
                    safe_text += char
        
        sys.stdout.write(safe_text)
        sys.stdout.flush()
        return True
    except:
        pass
    
    # 最后的保险方案
    try:
        encoded = output_text.encode('ascii', 'replace')
        sys.stdout.write(encoded)
        sys.stdout.flush()
        return True
    except:
        return False
'''
    
    with open('enhanced_encoding_patch.py', 'w') as f:
        f.write(enhanced_code)
    
    print(u"已创建增强编码处理补丁: enhanced_encoding_patch.py")

def main():
    """主函数"""
    print(u"=== emoji和特殊字符编码修复测试 ===")
    print(u"Python 版本: {}".format(sys.version[:20]))
    print(u"stdout编码: {}".format(repr(sys.stdout.encoding)))
    
    test_problematic_content()
    create_enhanced_encoding_handler()
    
    print(u"\n=== 建议的修复方案 ===")
    print(u"1. 在 encoding_handler.py 中添加emoji处理逻辑")
    print(u"2. 将无法编码的emoji替换为 [emoji] 标记")
    print(u"3. 或者过滤掉特殊Unicode字符")

if __name__ == "__main__":
    main() 