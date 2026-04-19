# -*- coding: utf-8 -*-
"""
LPrint 性能分析使用示例

这个示例展示了如何使用LPrint的内置性能分析功能来定位性能瓶颈。
"""

import sys
import os

# 添加模块路径
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from usualFunc_dev import LPrint, lprint

def example_usage():
    """演示如何使用性能分析功能"""
    
    print(u"=== LPrint 性能分析功能演示 ===")
    
    # 第一步：启用性能分析
    print(u"\n1. 启用性能分析")
    LPrint.enable_performance_analysis(True)
    
    # 第二步：执行一些lprint调用
    print(u"\n2. 执行测试调用")
    for i in range(20):
        lprint(u"测试消息 {}".format(i), u"数据", {"索引": i})
        lprint(u"格式化测试: %s", u"参数{}".format(i))
    
    # 第三步：查看性能报告
    print(u"\n3. 性能分析报告")
    LPrint.print_performance_report()
    
    # 第四步：测试优化效果
    print(u"\n4. 测试优化效果")
    print(u"禁用行计数功能...")
    LPrint.set_line_counting(False)
    LPrint.enable_performance_analysis(True)  # 重置计数器
    
    for i in range(20):
        lprint(u"优化测试 {}".format(i), u"数据", {"索引": i})
        lprint(u"优化格式化: %s", u"参数{}".format(i))
    
    print(u"\n5. 优化后的性能报告")
    LPrint.print_performance_report()
    
    # 恢复设置
    LPrint.set_line_counting(True)
    
    print(u"\n=== 演示完成 ===")

def performance_comparison():
    """对比不同设置下的性能"""
    
    print(u"\n=== 性能对比测试 ===")
    
    results = []
    test_count = 30
    
    # 测试场景1：正常模式
    print(u"\n测试场景1: 正常模式")
    LPrint.set_line_counting(True)
    LPrint.enable_performance_analysis(True)
    
    import time
    start_time = time.time()
    for i in range(test_count):
        lprint(u"正常模式测试 {}".format(i), {"数据": i})
    end_time = time.time()
    
    normal_time = end_time - start_time
    normal_stats = LPrint.performance_stats.copy()
    
    # 测试场景2：优化模式
    print(u"\n测试场景2: 优化模式（禁用行计数）")
    LPrint.set_line_counting(False)
    LPrint.enable_performance_analysis(True)
    
    start_time = time.time()
    for i in range(test_count):
        lprint(u"优化模式测试 {}".format(i), {"数据": i})
    end_time = time.time()
    
    optimized_time = end_time - start_time
    optimized_stats = LPrint.performance_stats.copy()
    
    # 对比结果
    print(u"\n=== 对比结果 ===")
    print(u"正常模式总耗时: {:.4f}秒".format(normal_time))
    print(u"优化模式总耗时: {:.4f}秒".format(optimized_time))
    
    if normal_time > 0:
        improvement = ((normal_time - optimized_time) / normal_time) * 100
        print(u"性能提升: {:.1f}%".format(improvement))
    
    # 恢复设置
    LPrint.set_line_counting(True)

if __name__ == "__main__":
    print(u"LPrint 性能分析使用示例")
    
    # 基本使用演示
    example_usage()
    
    # 性能对比
    performance_comparison() 