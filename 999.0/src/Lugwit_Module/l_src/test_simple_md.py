# -*- coding: utf-8 -*-
"""简单测试：Markdown 格式日志 + 追踪"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))
from usualFunc import lprint

# ===== 配置：启用 Markdown 格式 =====
from usualFunc import LPrint  # 导入类

lprint.trace_log_enable = True
lprint.log_base_dir = os.path.join(os.path.dirname(__file__), "logs")
# 固定写入 test_simple_md_work.md（不按日期分文件）



lprint("# 测试开始")
lprint("")

@lprint.trace(trace_depth=3)
def work(n):
    """主函数"""
    result = []
    for i in range(n):
        # time.sleep(0.5)
        result += calc(i, i + 1)
    return result

def calc(a, b):
    """计算函数"""
    a+=2
    return [a,b]*100

lprint("## 调用追踪函数")
lprint("")
result = work(300)
lprint("**结果**: {}", result)
lprint("")



lprint("---")
lprint("程序结束")


