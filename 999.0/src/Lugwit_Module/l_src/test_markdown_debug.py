# -*- coding: utf-8 -*-
"""调试 Markdown 模式设置"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from usualFunc import lprint

# 启用 Markdown 模式
lprint.trace_markdown_mode = True
print("1. 设置后 lprint.trace_markdown_mode =", lprint.trace_markdown_mode)

# 配置日志
lprint.trace_log_enable = True
lprint.log_base_dir = os.path.join(os.path.dirname(__file__), "logs")

@lprint.trace(trace_depth=2)
def simple_func(n):
    result = n + 10
    return result

# 在 trace_start 前检查
print("2. trace_start 前 lprint._forward_tracer =", lprint._forward_tracer)

# 调用装饰的函数（会触发 trace_start）
result = simple_func(5)

# 检查 tracer 的 markdown_mode
if lprint._forward_tracer:
    print("3. trace_start 后 lprint._forward_tracer.markdown_mode =", lprint._forward_tracer.markdown_mode)

print("结果:", result)
print("日志路径:", lprint.get_log_file_info()["file_path"])
