# -*- coding: utf-8 -*-
"""测试 Markdown 格式的追踪日志输出"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from usualFunc import lprint

# 配置日志输出到文件
lprint.trace_log_enable = True
lprint.log_base_dir = os.path.join(os.path.dirname(__file__), "logs")

# ✅ 启用 Markdown 模式
lprint.trace_markdown_mode = True

lprint("# 程序开始\n")
lprint("测试 Markdown 格式的追踪日志输出\n")


@lprint.trace(trace_depth=4)
def calculate_fibonacci(n):
    """计算斐波那契数列的第 n 项"""
    lprint("calculate_fibonacci 被调用，n={}", n)
    
    if n <= 1:
        return n
    
    # 创建数组存储结果
    fib_array = [0, 1]
    
    for i in range(2, n + 1):
        next_val = compute_sum(fib_array[i-1], fib_array[i-2])
        fib_array.append(next_val)
    
    result = format_result(fib_array, n)
    return result


def compute_sum(a, b):
    """深度2：计算两数之和"""
    result = a + b
    lprint("compute_sum({}, {}) = {}", a, b, result)
    return result


def format_result(arr, n):
    """深度2：格式化结果"""
    lprint("format_result 被调用，数组长度: {}, 目标索引: {}", len(arr), n)
    
    formatted = create_summary(arr, n)
    return formatted


def create_summary(arr, n):
    """深度3：创建摘要信息"""
    target_value = arr[n]
    summary = {
        'index': n,
        'value': target_value,
        'array': arr,
        'length': len(arr)
    }
    return summary


# 测试
lprint("\n## 测试用例 1：计算第 8 项\n")
result1 = calculate_fibonacci(8)
lprint("结果: {}\n", result1)

lprint("\n## 测试用例 2：计算第 5 项\n")
result2 = calculate_fibonacci(5)
lprint("结果: {}\n", result2)

lprint("\n---\n")
lprint("## 程序结束\n")
lprint("日志路径: `{}`\n", lprint.get_log_file_info()["file_path"])
lprint("\n> 💡 提示：在 VSCode 中打开日志文件，按 `Ctrl+Shift+V` 预览 Markdown 效果！")
