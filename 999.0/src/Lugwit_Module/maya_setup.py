# -*- coding: utf-8 -*-
"""
Maya 中手动设置 Lugwit_Module 环境
在 Maya 的 Script Editor 中运行此脚本
"""

import sys
import os
import importlib.util

# Lugwit_Module 安装路径
LUGWIT_PATH = r"C:\Users\wb.fengqingqing\packages\Lugwit_Module\999.0.0\platform-windows\python-3.7+"

# 添加到 PYTHONPATH
if LUGWIT_PATH not in sys.path:
    sys.path.insert(0, LUGWIT_PATH)

# 添加 Lugwit_Module 路径
lugwit_module_path = os.path.join(LUGWIT_PATH, "Lugwit_Module")
if lugwit_module_path not in sys.path:
    sys.path.insert(0, lugwit_module_path)

# 设置 Maya 脚本路径
maya_lib_path = os.path.join(lugwit_module_path, "l_src", "l_MayaLib")
if os.path.exists(maya_lib_path):
    if maya_lib_path not in sys.path:
        sys.path.insert(0, maya_lib_path)

# 设置环境变量
os.environ["LUGWIT_MODULE_ROOT"] = lugwit_module_path

print("✅ Lugwit_Module 环境已设置")
print("📦 Lugwit_Module 路径:", lugwit_module_path)

# 测试模块可用性
spec = importlib.util.find_spec("Lugwit_Module")
if spec is not None:
    print("✅ Lugwit_Module 可用")
    # 现在可以安全导入
    import Lugwit_Module as LM
    print("✅ Lugwit_Module 导入成功")
    print("🔧 可用功能: lprint, LM.isMayaEnv(), LM.getCurDir(), 等")
    
    # 简单使用示例（消除未使用导入警告）
    print(f"🎯 Maya 环境检测: {LM.isMayaEnv()}")
    print("📝 测试 lprint 功能:")
    LM.lprint("Lugwit_Module 在 Maya 中运行正常！")
else:
    print("❌ Lugwit_Module 不可用")
    print("请检查路径设置")
