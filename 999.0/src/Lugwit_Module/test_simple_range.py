# -*- coding: utf-8 -*-
"""
简化测试 lprint 范围功能
"""

import sys
import os

# 添加路径
sys.path.append(os.path.dirname(__file__))
import Lugwit_Module as LM

print("=== 测试1: 设置为只匹配特定函数 ===")
LM.LPrint.detailed_log_functions = ['target_function']
print("设置:", LM.LPrint.detailed_log_functions)

def target_function():
    print("[进入 target_function]")
    LM.lprint("A")
    LM.lprint("B - 当前")  
    LM.lprint("C")
    print("[退出 target_function]")

def other_function():
    print("[进入 other_function]")
    LM.lprint("X")
    LM.lprint("Y - 当前")
    LM.lprint("Z") 
    print("[退出 other_function]")

print("\n执行 target_function (应该有范围效果):")
target_function()

print("\n执行 other_function (应该没有范围效果):")
other_function()

print("\n=== 测试2: 设置为空列表（匹配所有函数）===")
LM.LPrint.detailed_log_functions = []
print("设置:", LM.LPrint.detailed_log_functions)

print("\n现在执行 other_function (应该有范围效果):")
other_function()

print("\n测试完成!") 