"""
演示自动安装异常钩子的效果
"""

def demo_function():
    """演示函数 - 会触发AttributeError"""
    import Lugwit_Module as LM
    # 这里会触发 AttributeError: module 'Lugwit_Module' has no attribute 'hostName'
    return LM.hostName

def main():
    print("🎯 演示自动安装异常钩子")
    print("="*50)
    print()
    print("这个演示展示了：")
    print("1. 导入Lugwit_Module时自动安装异常钩子")
    print("2. 异常发生时显示详细的调用链")
    print("3. 如何通过环境变量禁用钩子")
    print()
    print("开始演示...")
    print("-"*50)
    
    # 导入Lugwit_Module（会自动安装钩子）
    import sys
    import os
    sys.path.append(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib")
    
    import Lugwit_Module
    
    print()
    print("现在触发一个AttributeError异常...")
    print("-"*50)
    
    # 触发异常
    demo_function()

if __name__ == "__main__":
    main()
