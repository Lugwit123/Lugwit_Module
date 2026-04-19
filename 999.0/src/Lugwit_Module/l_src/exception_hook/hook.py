"""
全局异常钩子实现
"""

import sys
import traceback
import inspect
import os
from datetime import datetime

def get_call_chain(skip_frames=2):
    """
    获取函数调用链
    :param skip_frames: 跳过的帧数（默认跳过当前帧和调用者帧）
    :return: 调用链信息列表
    """
    call_chain = []
    frame = sys._getframe(skip_frames)
    
    while frame:
        # 获取帧信息
        func_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        
        # 获取局部变量
        local_vars = {}
        try:
            local_vars = {k: repr(v) for k, v in frame.f_locals.items() 
                         if not k.startswith('_') and k not in ['frame', 'call_chain']}
        except Exception:
            pass
        
        # 获取函数参数
        args_info = ""
        try:
            # 获取函数签名
            sig = inspect.signature(frame.f_code)
            param_names = list(sig.parameters.keys())
            
            # 获取参数值
            args = []
            for param in param_names:
                if param in frame.f_locals:
                    val = frame.f_locals[param]
                    # 限制值的长度
                    val_str = repr(val)
                    if len(val_str) > 100:
                        val_str = val_str[:100] + "..."
                    args.append(f"{param}={val_str}")
            
            if args:
                args_info = f"({', '.join(args)})"
        except Exception:
            pass
        
        # 构建调用链信息
        call_info = {
            'function': func_name,
            'file': filename,
            'line': lineno,
            'args': args_info,
            'locals': local_vars
        }
        
        call_chain.append(call_info)
        frame = frame.f_back
    
    return call_chain

def format_call_chain(call_chain, max_depth=10):
    """
    格式化调用链为可读字符串
    :param call_chain: 调用链列表
    :param max_depth: 最大显示深度
    :return: 格式化的字符串
    """
    output = []
    output.append("=" * 80)
    output.append(f"🔍 函数调用链回溯 (最多显示 {max_depth} 层)")
    output.append("=" * 80)
    
    for i, info in enumerate(call_chain[:max_depth]):
        # 文件名简化
        filename = info['file']
        if '\\' in filename:
            filename = filename.split('\\')[-1]
        elif '/' in filename:
            filename = filename.split('/')[-1]
        
        output.append(f"\n📌 调用层级 {i + 1}:")
        output.append(f"   函数: {info['function']}{info['args']}")
        output.append(f"   位置: {filename}:{info['line']}")
        
        # 显示关键局部变量
        if info['locals']:
            output.append("   局部变量:")
            for var_name, var_value in list(info['locals'].items())[:5]:  # 最多显示5个变量
                output.append(f"     {var_name} = {var_value}")
            if len(info['locals']) > 5:
                output.append(f"     ... 还有 {len(info['locals']) - 5} 个变量")
    
    if len(call_chain) > max_depth:
        output.append(f"\n... (还有 {len(call_chain) - max_depth} 层调用)")
    
    return "\n".join(output)

def exception_hook(exc_type, exc_value, exc_traceback):
    """
    全局异常钩子
    """
    print("\n" + "!" * 80)
    print(f"💥 发生异常: {exc_type.__name__}: {exc_value}")
    print("!" * 80)
    print()
    
    # 打印执行环境信息
    print("🔧 执行环境信息:")
    print(f"   Python路径: {sys.executable}")
    print(f"   命令参数: {sys.argv}")
    print()
    
    # 打印相关上下文信息
    print("📦 异常上下文信息:")
    try:
        # 获取异常帧中的局部变量
        frame = exc_traceback.tb_frame
        local_vars = {}
        if frame:
            local_vars = {k: v for k, v in frame.f_locals.items() 
                         if not k.startswith('_') and k not in ['frame', 'call_chain']}
        
        # 查找可能的模块对象
        modules_found = []
        other_objects = []
        
        for var_name, var_value in local_vars.items():
            try:
                if hasattr(var_value, '__dict__') and hasattr(var_value, '__file__'):
                    # 这看起来像一个模块
                    modules_found.append((var_name, var_value))
                elif hasattr(var_value, '__class__'):
                    # 其他对象
                    other_objects.append((var_name, type(var_value).__name__))
            except Exception:
                pass
        
        # 显示模块信息
        if modules_found:
            print("   相关模块:")
            for name, module in modules_found[:5]:  # 最多显示5个模块
                print(f"     {name}:")
                print(f"       路径: {getattr(module, '__file__', '未知')}")
                # 检查常见属性
                common_attrs = ['hostName', 'config', 'settings', 'data', 'value']
                found_attrs = [attr for attr in common_attrs if hasattr(module, attr)]
                if found_attrs:
                    print(f"       包含属性: {found_attrs}")
                # 显示一些关键属性
                all_attrs = [attr for attr in dir(module) if not attr.startswith('_')][:8]
                print(f"       主要属性: {all_attrs}")
        
        # 显示其他重要对象
        if other_objects:
            print("   其他对象:")
            for name, type_name in other_objects[:10]:  # 最多显示10个对象
                print(f"     {name}: {type_name}")
        
        if not modules_found and not other_objects:
            print("   未找到相关对象")
            print(f"   局部变量: {list(local_vars.keys())[:10]}")
            
    except Exception as e:
        print(f"   获取上下文信息失败: {e}")
    print()
    
    # 输出标准异常信息
    print("📋 标准异常信息:")
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print()
    
    # 输出函数调用链
    print("🔗 函数调用链回溯:")
    try:
        # 使用traceback.extract_tb获取完整的调用栈
        tb_list = traceback.extract_tb(exc_traceback)
        call_chain = []
        
        # 反向遍历，从最外层到最内层
        for i, (filename, lineno, func_name, text) in enumerate(reversed(tb_list)):
            # 简化文件名
            short_filename = filename
            if '\\' in filename:
                short_filename = filename.split('\\')[-1]
            elif '/' in filename:
                short_filename = filename.split('/')[-1]
            
            # 对于异常帧，尝试获取局部变量
            local_vars = {}
            if i == 0:  # 异常发生的帧
                try:
                    # 从traceback对象获取帧
                    frame = exc_traceback.tb_frame
                    # 向上追溯对应的帧
                    for _ in range(len(tb_list) - 1 - i):
                        if frame:
                            frame = frame.f_next
                    
                    if frame:
                        important_vars = ['self', 'cls', 'result', 'data', 'value', 'key', 'item']
                        for var_name in important_vars:
                            if var_name in frame.f_locals:
                                val = frame.f_locals[var_name]
                                val_str = repr(val)
                                if len(val_str) > 80:
                                    val_str = val_str[:80] + "..."
                                local_vars[var_name] = val_str
                except Exception:
                    pass
            
            call_info = {
                'function': func_name,
                'file': filename,
                'line': lineno,
                'args': '',
                'locals': local_vars
            }
            
            call_chain.append(call_info)
        
        # 如果调用链太短，尝试获取更多帧信息
        if len(call_chain) < 3:
            print(f"   📝 调用链较短，尝试获取更多帧信息...")
            try:
                # 获取完整的调用栈
                import inspect
                stack = inspect.stack()
                # 从当前帧向上查找
                for i, frame_info in enumerate(stack[1:], 1):  # 跳过当前帧
                    if i > 10:  # 限制深度
                        break
                    
                    filename = frame_info.filename
                    lineno = frame_info.lineno
                    func_name = frame_info.function
                    
                    # 简化文件名
                    short_filename = filename
                    if '\\' in filename:
                        short_filename = filename.split('\\')[-1]
                    elif '/' in filename:
                        short_filename = filename.split('/')[-1]
                    
                    call_info = {
                        'function': func_name,
                        'file': filename,
                        'line': lineno,
                        'args': '',
                        'locals': {}
                    }
                    
                    call_chain.append(call_info)
            except Exception as e:
                print(f"   ⚠️ 获取额外帧信息失败: {e}")
        
        # 格式化并输出调用链
        call_chain_str = format_call_chain(call_chain, max_depth=20)
        print(call_chain_str)
        
    except Exception as e:
        print(f"⚠️ 获取调用链时出错: {e}")
    
    print("\n" + "=" * 80)
    print(f"⏰ 异常发生时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 调用原始异常钩子（如果存在）
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def install_trace_hook():
    """
    安装全局异常钩子
    """
    # 检查环境变量是否禁用异常钩子
    disable_hook = os.environ.get('DISABLE_EXCEPTION_HOOK', '').lower() in ('1', 'true', 'yes', 'on')
    
    if disable_hook:
        print("[WARNING] 异常钩子已通过环境变量 DISABLE_EXCEPTION_HOOK 禁用")
        return False
    
    # 检查是否已经安装
    if hasattr(sys.excepthook, '_is_exception_hook'):
        print("[INFO] 异常钩子已经安装")
        return True
    
    # 安装钩子
    sys.excepthook = exception_hook
    sys.excepthook._is_exception_hook = True  # 标记这是我们安装的钩子
    print("[OK] 全局异常钩子已安装 - 异常发生时将显示详细调用链")
    print("[TIP] 提示: 可通过设置环境变量 DISABLE_EXCEPTION_HOOK=1 禁用钩子")
    return True

def uninstall_trace_hook():
    """
    卸载全局异常钩子
    """
    # 检查是否是我们安装的钩子
    if not hasattr(sys.excepthook, '_is_exception_hook'):
        print("ℹ️ 没有安装异常钩子或不是我们安装的钩子")
        return False
    
    # 卸载钩子
    sys.excepthook = sys.__excepthook__
    print("❌ 全局异常钩子已卸载")
    return True

def is_hook_installed():
    """
    检查异常钩子是否已安装
    :return: bool
    """
    return hasattr(sys.excepthook, '_is_exception_hook')

def get_hook_status():
    """
    获取钩子状态信息
    :return: dict
    """
    disable_hook = os.environ.get('DISABLE_EXCEPTION_HOOK', '').lower() in ('1', 'true', 'yes', 'on')
    installed = hasattr(sys.excepthook, '_is_exception_hook')
    
    # 如果被环境变量禁用，即使已安装也视为未启用
    effective_installed = installed and not disable_hook
    
    return {
        'installed': effective_installed,
        'disabled_by_env': disable_hook,
        'env_var': os.environ.get('DISABLE_EXCEPTION_HOOK', ''),
        'current_hook': type(sys.excepthook).__name__,
        'hook_installed': installed  # 实际安装状态
    }

# 测试函数
def test_function_a():
    x = 10
    y = 0
    return test_function_b(x, y)

def test_function_b(a, b):
    result = a / b  # 这里会触发除零异常
    return result

def test_exception():
    """测试异常钩子"""
    print("🧪 测试异常钩子...")
    test_function_a()  # 直接调用，不使用try-catch
    print("测试完成")

if __name__ == "__main__":
    # 安装钩子
    install_trace_hook()
    
    # 测试
    test_exception()
