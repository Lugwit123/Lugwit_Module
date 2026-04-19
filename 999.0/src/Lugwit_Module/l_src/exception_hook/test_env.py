"""
测试环境变量控制功能
"""

import sys
import os

# 添加路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from l_src.exception_hook import install_trace_hook, uninstall_trace_hook, is_hook_installed, get_hook_status

def test_function():
    """测试函数"""
    x = 10
    y = 0
    return x / y  # 除零错误

def test_without_env():
    """不设置环境变量测试"""
    print("\n" + "="*60)
    print("🧪 测试1: 不设置环境变量")
    print("="*60)
    
    # 确保环境变量未设置
    if 'DISABLE_EXCEPTION_HOOK' in os.environ:
        del os.environ['DISABLE_EXCEPTION_HOOK']
    
    # 安装钩子
    result = install_trace_hook()
    print(f"安装结果: {result}")
    
    # 检查状态
    status = get_hook_status()
    print(f"钩子状态: {status}")
    
    # 触发异常
    try:
        test_function()
    except:
        pass
    
    # 卸载钩子
    uninstall_trace_hook()

def test_with_env_disabled():
    """设置环境变量禁用测试"""
    print("\n" + "="*60)
    print("🧪 测试2: 设置环境变量 DISABLE_EXCEPTION_HOOK=1")
    print("="*60)
    
    # 设置环境变量
    os.environ['DISABLE_EXCEPTION_HOOK'] = '1'
    
    # 尝试安装钩子
    result = install_trace_hook()
    print(f"安装结果: {result}")
    
    # 检查状态
    status = get_hook_status()
    print(f"钩子状态: {status}")
    
    # 触发异常（应该使用默认异常处理）
    try:
        test_function()
    except:
        pass
    
    # 清理环境变量
    del os.environ['DISABLE_EXCEPTION_HOOK']

def test_with_env_true():
    """设置环境变量为true测试"""
    print("\n" + "="*60)
    print("🧪 测试3: 设置环境变量 DISABLE_EXCEPTION_HOOK=true")
    print("="*60)
    
    # 设置环境变量
    os.environ['DISABLE_EXCEPTION_HOOK'] = 'true'
    
    # 尝试安装钩子
    result = install_trace_hook()
    print(f"安装结果: {result}")
    
    # 检查状态
    status = get_hook_status()
    print(f"钩子状态: {status}")
    
    # 清理环境变量
    del os.environ['DISABLE_EXCEPTION_HOOK']

def test_with_env_false():
    """设置环境变量为false测试"""
    print("\n" + "="*60)
    print("🧪 测试4: 设置环境变量 DISABLE_EXCEPTION_HOOK=false")
    print("="*60)
    
    # 设置环境变量
    os.environ['DISABLE_EXCEPTION_HOOK'] = 'false'
    
    # 尝试安装钩子
    result = install_trace_hook()
    print(f"安装结果: {result}")
    
    # 检查状态
    status = get_hook_status()
    print(f"钩子状态: {status}")
    
    # 触发异常
    try:
        test_function()
    except:
        pass
    
    # 卸载钩子
    uninstall_trace_hook()
    
    # 清理环境变量
    del os.environ['DISABLE_EXCEPTION_HOOK']

def main():
    print("🧪 测试环境变量控制功能")
    
    # 运行各种测试
    test_without_env()
    test_with_env_disabled()
    test_with_env_true()
    test_with_env_false()
    
    print("\n✅ 所有测试完成")

if __name__ == "__main__":
    main()
