# -*- coding: utf-8 -*-
"""代码跟踪功能简单测试

演示 LPrint 的手动代码跟踪功能：
1. 使用 trace_start() 开始追踪
2. 使用 trace_stop() 停止追踪
3. 使用 trace_result() 显示追踪结果
4. 生成 Markdown 格式的追踪日志
"""
import sys
import os
import time
# 添加模块路径
sys.path.insert(0, os.path.dirname(__file__))
from usualFunc import lprint

# ===== 配置日志输出 =====
lprint.trace_log_enable = True
lprint.log_base_dir = os.path.join(os.path.dirname(__file__), "logs")
lprint.trace_log_stem = "test_trace_simple"

# ===== 测试函数 =====
def helper_function(x):
    """辅助函数：计算平方"""
    result = x * x
    time.sleep(0.01)  # 模拟耗时操作
    return result

def calculate_factorial(n):
    """计算阶乘"""
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

def advanced_process(value):
    """高级处理：包含多个子调用"""
    # 调用多个不同的辅助函数
    square = helper_function(value)
    factorial = calculate_factorial(value)
    cube = helper_function(square)  # 嵌套调用
    return square + factorial + cube

def process_data(data):
    """处理数据：对列表中每个元素求平方"""
    results = []
    for item in data:
        square = helper_function(item)
        results.append(square)
    return results

def batch_process(batches):
    """批量处理：处理多个批次"""
    all_results = []
    for i, batch in enumerate(batches):
        lprint("处理批次 {}", i + 1)
        batch_results = process_data(batch)
        all_results.extend(batch_results)
    return all_results

def main_function():
    """主函数：手动控制追踪"""
    lprint("开始执行主函数")
    
    # 测试数据
    numbers = [1, 2, 3, 4, 5]
    lprint("输入数据: {}", numbers)
    
    # 调用处理函数
    results = process_data(numbers)
    lprint("处理结果: {}", results)
    
    # 计算总和
    total = sum(results)
    lprint("总和: {}", total)
    
    return total

def secondary_function():
    """第二个主函数：创建第2个根调用"""
    lprint("执行第二个主函数")
    
    # 多批次处理
    batches = [[1, 2], [3, 4, 5]]
    results = batch_process(batches)
    
    # 高级处理
    advanced_result = advanced_process(3)
    lprint("高级处理结果: {}", advanced_result)

    # 测试长变量
    a = [1, 2, 3, 4, 5]*100
    
    return len(results) + advanced_result,a

# ===== 运行测试 =====
if __name__ == "__main__":
    lprint("=" * 50)
    lprint("# 代码跟踪测试 - 手动控制方式")
    lprint("")
    
    # 1. 开始追踪
    lprint("开始追踪...")
    lprint.trace_start(trace_depth=6, clear_log=True)
    
    # 2. 执行需要追踪的代码（调用两个主函数）
    result1 = main_function()  # → 第1个根调用（路径1-x-y）
    lprint("")
    result2 = secondary_function()  # → 第2个根调用（路径2-x-y）
    
    # 3. 停止追踪
    lprint.trace_stop()
    lprint("追踪已停止")
    
    # 4. 显示追踪结果（会自动写入日志文件）
    lprint("")
    lprint("## 追踪结果")
    lprint.trace_result()
    
    lprint("")
    lprint("**第一个结果**: {}", result1)
    lprint("**第二个结果**: {}", result2)
    # lprint("**总结果**: {}", result1 + result2)
    lprint("=" * 50)
    
    # 日志文件会自动保存到: logs/test_trace_simple.md
    print("\n追踪日志已保存，请查看生成的 Markdown 文件")
