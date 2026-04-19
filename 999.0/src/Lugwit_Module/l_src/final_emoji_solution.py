# -*- coding: utf-8 -*-
"""
最终的emoji问题解决方案

针对Python 2.7在gbk/cp936控制台下无法显示emoji的问题，
提供彻底的过滤和替换方案。
"""

import sys
import re

def is_emoji(char):
    """检查字符是否是emoji或特殊Unicode字符"""
    code_point = ord(char)
    
    # emoji范围检查
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # 表情符号
        (0x1F300, 0x1F5FF),  # 各种符号
        (0x1F680, 0x1F6FF),  # 交通和地图符号
        (0x1F700, 0x1F77F),  # 几何符号
        (0x1F780, 0x1F7FF),  # 几何符号扩展
        (0x1F800, 0x1F8FF),  # 补充箭头-C
        (0x1F900, 0x1F9FF),  # 补充符号和象形文字
        (0x1FA00, 0x1FA6F),  # 扩展-A
        (0x1FA70, 0x1FAFF),  # 符号和象形文字扩展-A
        (0x2600, 0x26FF),    # 杂项符号
        (0x2700, 0x27BF),    # 装饰符号
        (0xFE00, 0xFE0F),    # 变体选择器
        (0x1F1E6, 0x1F1FF),  # 区域指示符号
    ]
    
    for start, end in emoji_ranges:
        if start <= code_point <= end:
            return True
    
    return False

def safe_filter_unicode(text):
    """
    安全过滤Unicode文本，移除或替换emoji等特殊字符
    """
    if sys.version_info[0] == 3:
        return text  # Python 3 暂不处理
    
    if not isinstance(text, unicode):
        try:
            text = unicode(text)
        except:
            return text
    
    filtered_text = u""
    for char in text:
        try:
            # 首先检查是否是emoji
            if is_emoji(char):
                filtered_text += u"[emoji]"
                continue
            
            # 然后检查是否可以在cp936下编码
            char.encode('cp936')
            filtered_text += char
        except UnicodeEncodeError:
            # 无法编码的字符
            code_point = ord(char)
            if code_point > 0x7F:  # 非ASCII字符
                if code_point > 0x4E00 and code_point < 0x9FFF:
                    # 中文字符范围，保留
                    filtered_text += char
                else:
                    # 其他特殊字符，替换
                    filtered_text += u"[U+{:04X}]".format(code_point)
            else:
                filtered_text += char
    
    return filtered_text

def safe_print_unicode(text):
    """
    安全打印Unicode文本
    """
    if sys.version_info[0] == 3:
        try:
            print(text)
            return True
        except:
            print(repr(text))
            return False
    
    # Python 2 处理
    try:
        if not isinstance(text, unicode):
            text = unicode(text)
        
        # 过滤特殊字符
        filtered_text = safe_filter_unicode(text)
        
        # 尝试输出
        try:
            sys.stdout.write(filtered_text + u'\n')
            sys.stdout.flush()
            return True
        except UnicodeEncodeError:
            # 如果还是失败，使用ASCII安全输出
            try:
                ascii_safe = filtered_text.encode('ascii', 'replace')
                sys.stdout.write(ascii_safe + '\n')
                sys.stdout.flush()
                return True
            except:
                print("Unable to display text safely")
                return False
    except Exception as e:
        print("Error in safe_print_unicode:", str(e))
        return False

def patch_usualFunc_new():
    """
    给usualFunc_new.py打补丁，确保emoji安全处理
    """
    patch_code = '''
# 添加emoji安全处理补丁
def safe_format_args(args):
    """安全格式化参数，处理emoji"""
    if sys.version_info[0] == 3:
        return args
    
    safe_args = []
    for arg in args:
        if isinstance(arg, unicode):
            # 过滤emoji和特殊字符
            safe_arg = u""
            for char in arg:
                try:
                    # 检查是否是emoji
                    code_point = ord(char)
                    if 0x1F600 <= code_point <= 0x1F64F or 0x1F300 <= code_point <= 0x1F5FF:
                        safe_arg += u"[emoji]"
                    else:
                        char.encode('cp936')
                        safe_arg += char
                except UnicodeEncodeError:
                    safe_arg += u"[?]"
            safe_args.append(safe_arg)
        else:
            safe_args.append(arg)
    return tuple(safe_args)

# 在__call__方法中的修改建议：
# 将这行：
# print(u"args->{},self._format_log_message return none".format(args))
# 替换为：
# safe_args = safe_format_args(args)
# print(u"args->{},self._format_log_message return none".format(safe_args))
'''
    
    print(u"=== emoji安全处理补丁代码 ===")
    print(patch_code)

def test_emoji_filtering():
    """测试emoji过滤功能"""
    print(u"=== 测试emoji过滤功能 ===")
    
    test_cases = [
        u"普通中文文字",
        u"包含emoji的文字 \U0001f600 结束",
        u"Unicode: \U0001f600",
        u"UTF-8编码: \xf0\x9f\x98\x8a",
        u"混合内容: 中文 + emoji \U0001f600 + English",
    ]
    
    for i, test_case in enumerate(test_cases):
        print(u"\n测试案例 {}: {}".format(i+1, repr(test_case)))
        
        filtered = safe_filter_unicode(test_case)
        print(u"过滤结果: {}".format(repr(filtered)))
        
        print(u"安全输出: ", end='')
        success = safe_print_unicode(filtered)
        if not success:
            print(u"[输出失败]")

def main():
    """主函数"""
    print(u"=== 最终emoji问题解决方案 ===")
    print(u"Python版本: {}".format(sys.version[:20]))
    print(u"stdout编码: {}".format(repr(sys.stdout.encoding)))
    
    test_emoji_filtering()
    patch_usualFunc_new()
    
    print(u"\n=== 解决方案总结 ===")
    print(u"1. 使用 safe_filter_unicode() 过滤emoji字符")
    print(u"2. 在usualFunc_new.py中应用安全处理补丁")
    print(u"3. 确保所有输出都经过emoji过滤")

if __name__ == "__main__":
    main() 