# -*- coding: utf-8 -*-
"""
测试模块级别调用 lprint - 验证修复后 <module> 帧不会被跳过
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))

from usualFunc import lprint, LPrint

print("=" * 80)
print("测试修复前后的对比")
print("=" * 80)

# 测试1：模块级别的普通调用
print("\n测试 1: 模块级别的普通 lprint 调用")
print("-" * 80)
lprint("这是模块级别的第一条消息")

# 测试2：模块级别 + show_all_frame
print("\n测试 2: 模块级别 + show_all_frame")
print("-" * 80)
lprint("这是模块级别的第二条消息 - 带 show_all_frame", show_all_frame=True)

# 测试3：模块级别 + debug_self_global
print("\n测试 3: 模块级别 + debug_self_global")
print("-" * 80)
LPrint.debug_self_global = True
lprint("这是模块级别的第三条消息 - 带 debug_self_global")
LPrint.debug_self_global = False

# 测试4：模拟 chat_handler.py 的场景
print("\n测试 4: 模拟 chat_handler.py 的导入时调用")
print("-" * 80)
print("模拟：import Lugwit_Module as LM")
print("模拟：lprint = LM.lprint")
print("模拟：lprint(f\"测试lprint函数\", show_all_frame=True)")
print("-" * 80)
lprint(f"测试lprint函数 - 模拟 chat_handler.py 第37行", show_all_frame=True)

# 测试5：在函数中调用作为对比
print("\n测试 5: 在函数中调用（作为对比）")
print("-" * 80)

def test_function():
    lprint("这是在函数中的调用", show_all_frame=True)

test_function()

print("\n" + "=" * 80)
print("测试完成！检查输出中的 File 字段：")
print("- 修复后：应该显示正确的文件名（test_module_level.py）")
print("- 修复前：可能显示 <frozen importlib._bootstrap>")
print("=" * 80)


