# -*- coding: utf-8 -*-
"""
测试 lprint 范围功能
"""

import sys
import os

# 添加路径
sys.path.append(os.path.dirname(__file__))
import Lugwit_Module as LM

# 设置只对特定函数生效
LM.LPrint.detailed_log_functions = ['_compare_data_changes']
lprint = LM.lprint

def _compare_data_changes():
    """这个函数名匹配 '_compare_data_changes' 模式，应该执行范围内的其他lprint"""
    print("=== 进入 _compare_data_changes 函数 ===")
    lprint(u"步骤1: 开始比较数据")
    data = {}
    lprint(u"步骤2: 这是当前执行的lprint")
    config = {"setting": "value"}
    lprint(u"步骤3: 比较完成")
    print("=== 退出 _compare_data_changes 函数 ===")
    return data

def normal_function():
    """这个函数名不匹配模式，应该只显示正常日志"""
    print("=== 进入 normal_function 函数 ===")
    lprint(u"步骤1: 这个不应该执行范围内其他lprint")
    data = []
    lprint(u"步骤2: 当前lprint")
    lprint(u"步骤3: 这个也不应该被额外执行")
    print("=== 退出 normal_function 函数 ===")
    return data

def test_function():
    """测试函数，不匹配模式"""
    print("=== 进入 test_function 函数 ===")
    lprint(u"测试lprint 1")
    result = "test"
    lprint(u"测试lprint 2")
    lprint(u"测试lprint 3")
    print("=== 退出 test_function 函数 ===")
    return result

if __name__ == "__main__":
    print("当前设置:")
    print("LPrint.detailed_log_functions:", LM.LPrint.detailed_log_functions)
    print("LPrint.log_width:", LM.LPrint.log_width)
    print("lprint.show_context:", lprint.show_context)
    
    print("\n" + "="*50)
    print("测试1: 匹配模式的函数 (_compare_data_changes)")
    print("="*50)
    _compare_data_changes()
    
    print("\n" + "="*50)
    print("测试2: 不匹配模式的函数 (normal_function)")
    print("="*50)
    normal_function()
    
    print("\n" + "="*50)
    print("测试3: 不匹配模式的函数 (test_function)")
    print("="*50)
    test_function()
    
    print("\n测试完成!") 