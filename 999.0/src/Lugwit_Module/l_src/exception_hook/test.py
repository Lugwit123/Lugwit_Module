"""
测试异常钩子模块
"""

import sys
import os

# 添加路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from l_src.exception_hook import install_trace_hook, uninstall_trace_hook

def test_function_1():
    """第一层测试函数"""
    x = 10
    y = 0
    return test_function_2(x, y)

def test_function_2(a, b):
    """第二层测试函数"""
    data = {"value": a, "divisor": b}
    return test_function_3(data)

def test_function_3(params):
    """第三层测试函数 - 这里会出错"""
    result = params["value"] / params["divisor"]  # 除零错误
    return result

def test_attribute_error():
    """测试属性错误"""
    import Lugwit_Module as LM
    return LM.hostName  # 这里会触发 AttributeError

def main():
    print("\n" + "="*60)
    print("🧪 开始测试异常钩子模块")
    print("="*60 + "\n")
    
    # 安装钩子
    install_trace_hook()
    
    print("\n📋 测试1: 除零错误")
    print("-"*40)
    test_function_1()  # 不使用try-catch，让异常直接抛出
    
    print("\n📋 测试2: 属性缺失错误")
    print("-"*40)
    test_attribute_error()  # 不使用try-catch，让异常直接抛出
    
    print("\n✅ 测试完成")

if __name__ == "__main__":
    main()
