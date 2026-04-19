"""
测试通用异常钩子
"""

import sys
import os

# 添加路径
sys.path.append(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib")

def test_various_errors():
    """测试各种类型的异常"""
    
    # 测试1: 属性错误
    print("🧪 测试1: AttributeError")
    import Lugwit_Module as LM
    # 访问不存在的属性 - 这会触发异常钩子
    value = LM.non_existent_attribute

if __name__ == "__main__":
    print("🎯 测试通用异常钩子")
    print("="*50)
    test_various_errors()
