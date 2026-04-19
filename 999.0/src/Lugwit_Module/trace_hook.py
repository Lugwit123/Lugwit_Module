"""
全局异常钩子 - 在异常发生时输出详细的函数调用链
"""

import sys
import traceback
import inspect
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
                except:
                    pass
            
            call_info = {
                'function': func_name,
                'file': filename,
                'line': lineno,
                'args': '',
                'locals': local_vars
            }
            
            call_chain.append(call_info)
        
        # 格式化并输出调用链
        call_chain_str = format_call_chain(call_chain, max_depth=15)
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
    sys.excepthook = exception_hook
    print("✅ 全局异常钩子已安装 - 异常发生时将显示详细调用链")

def uninstall_trace_hook():
    """
    卸载全局异常钩子
    """
    sys.excepthook = sys.__excepthook__
    print("❌ 全局异常钩子已卸载")

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
