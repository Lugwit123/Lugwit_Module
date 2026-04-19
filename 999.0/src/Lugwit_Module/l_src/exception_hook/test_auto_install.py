"""
测试Lugwit_Module自动安装异常钩子功能
"""

import sys
import os

# 添加路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_auto_install():
    """测试自动安装功能"""
    print("\n" + "="*60)
    print("🧪 测试Lugwit_Module自动安装异常钩子")
    print("="*60)
    
    # 确保环境变量未设置
    if 'DISABLE_EXCEPTION_HOOK' in os.environ:
        del os.environ['DISABLE_EXCEPTION_HOOK']
    
    print("\n📋 测试1: 导入Lugwit_Module（应该自动安装钩子）")
    print("-"*40)
    
    # 导入Lugwit_Module，这应该自动安装钩子
    try:
        import Lugwit_Module
        print("✅ Lugwit_Module 导入成功")
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return
    
    # 检查钩子状态
    try:
        from Lugwit_Module.l_src.exception_hook import get_hook_status
        status = get_hook_status()
        print(f"钩子状态: {status}")
        
        if status['installed']:
            print("✅ 异常钩子已自动安装")
        else:
            print("⚠️ 异常钩子未安装")
    except:
        print("⚠️ 无法检查钩子状态")
    
    print("\n📋 测试2: 触发异常测试钩子")
    print("-"*40)
    
    def test_function():
        x = 10
        y = 0
        return x / y  # 除零错误
    
    # 触发异常
    try:
        test_function()
    except:
        pass
    
    print("\n📋 测试3: 设置环境变量后导入")
    print("-"*40)
    
    # 重新导入测试
    # 首先卸载模块
    if 'Lugwit_Module' in sys.modules:
        del sys.modules['Lugwit_Module']
    
    # 设置环境变量禁用钩子
    os.environ['DISABLE_EXCEPTION_HOOK'] = '1'
    
    # 重新导入
    try:
        import Lugwit_Module as LM2
        print("✅ Lugwit_Module 重新导入成功")
        
        # 检查钩子状态
        try:
            from Lugwit_Module.l_src.exception_hook import get_hook_status
            status = get_hook_status()
            print(f"钩子状态: {status}")
            
            if not status['installed'] and status['disabled_by_env']:
                print("✅ 异常钩子被环境变量正确禁用")
            elif status['installed']:
                print("⚠️ 异常钩子仍然启用（环境变量未生效）")
            else:
                print("⚠️ 异常钩子状态异常")
        except:
            print("⚠️ 无法检查钩子状态")
    except Exception as e:
        print(f"❌ 重新导入失败: {e}")
    
    # 清理环境变量
    del os.environ['DISABLE_EXCEPTION_HOOK']
    
    print("\n✅ 自动安装测试完成")

if __name__ == "__main__":
    test_auto_install()
