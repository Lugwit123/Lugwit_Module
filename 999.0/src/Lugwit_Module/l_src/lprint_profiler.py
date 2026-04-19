# -*- coding: utf-8 -*-
"""
LPrint 性能分析工具

这个模块提供了一个简单易用的性能分析接口，帮助用户快速定位lprint的性能瓶颈。

使用方法:
1. 基本性能分析:
   from lprint_profiler import quick_performance_test
   quick_performance_test()

2. 详细性能对比:
   from lprint_profiler import detailed_performance_comparison
   detailed_performance_comparison()

3. 自定义测试:
   from lprint_profiler import PerformanceProfiler
   profiler = PerformanceProfiler()
   profiler.run_custom_test(test_count=100)
"""

import time
import sys
import os

# 添加模块路径
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from usualFunc_dev import LPrint, lprint
except ImportError:
    try:
        from usualFunc import LPrint, lprint
    except ImportError:
        print(u"无法导入LPrint模块")
        sys.exit(1)

class PerformanceProfiler:
    """LPrint性能分析器"""
    
    def __init__(self):
        self.original_settings = {}
        
    def save_settings(self):
        """保存当前设置"""
        self.original_settings = {
            'enable_line_counting': LPrint.enable_line_counting,
            'enable_function_range_check': LPrint.enable_function_range_check,
            'debug_self_global': LPrint.debug_self_global,
            'enable_performance_profiling': LPrint.enable_performance_profiling
        }
    
    def restore_settings(self):
        """恢复原始设置"""
        LPrint.enable_line_counting = self.original_settings.get('enable_line_counting', True)
        LPrint.enable_function_range_check = self.original_settings.get('enable_function_range_check', False)
        LPrint.debug_self_global = self.original_settings.get('debug_self_global', False)
        LPrint.enable_performance_profiling = self.original_settings.get('enable_performance_profiling', False)
    
    def run_test_scenario(self, name, setup_func=None, test_count=50):
        """运行测试场景
        
        Args:
            name (str): 测试场景名称
            setup_func (callable): 设置函数
            test_count (int): 测试次数
            
        Returns:
            dict: 测试结果
        """
        print(u"\n--- 测试场景: {} ---".format(name))
        
        if setup_func:
            setup_func()
        
        # 启用性能分析
        LPrint.enable_performance_analysis(True)
        
        # 记录开始时间
        start_time = time.time()
        
        # 执行测试
        for i in range(test_count):
            lprint(u"测试消息 {}".format(i), u"数据", {"索引": i, "测试": True})
            lprint(u"格式化测试: %s - %d", u"字符串", i)
            
        # 记录结束时间
        end_time = time.time()
        total_time = end_time - start_time
        
        # 获取性能统计
        stats = LPrint.performance_stats.copy()
        
        # 计算结果
        calls_per_second = stats['total_calls'] / total_time if total_time > 0 else 0
        avg_time_per_call = total_time * 1000 / stats['total_calls'] if stats['total_calls'] > 0 else 0
        
        result = {
            'name': name,
            'total_calls': stats['total_calls'],
            'total_time': total_time,
            'calls_per_second': calls_per_second,
            'avg_time_per_call': avg_time_per_call,
            'stats': stats
        }
        
        print(u"  总调用次数: {}".format(stats['total_calls']))
        print(u"  总耗时: {:.4f}秒".format(total_time))
        print(u"  平均每次调用: {:.4f}毫秒".format(avg_time_per_call))
        print(u"  每秒调用次数: {:.2f}".format(calls_per_second))
        
        return result
    
    def analyze_bottlenecks(self, stats):
        """分析性能瓶颈"""
        total_calls = stats['total_calls']
        if total_calls == 0:
            print(u"无性能数据")
            return
        
        # 计算各步骤的平均耗时（毫秒）
        steps = [
            ('帧获取', stats['frame_acquisition_time']),
            ('编码转换', stats['unicode_conversion_time']),
            ('debug检查', stats['debug_check_time']),
            ('行计数', stats['line_counting_time']),
            ('帧信息获取', stats['frame_info_time']),
            ('序列化', stats['serialization_time']),
            ('格式化', stats['format_time']),
        ]
        
        # 计算总时间和百分比
        total_step_time = sum(time for _, time in steps)
        
        print(u"各步骤耗时分析 (平均每次调用):")
        print(u"{:<12} {:>10} {:>10}".format(u"步骤", u"耗时(ms)", u"占比"))
        print(u"-" * 35)
        
        # 按耗时排序
        steps.sort(key=lambda x: x[1], reverse=True)
        
        for step_name, step_time in steps:
            avg_time_ms = (step_time / total_calls) * 1000
            percentage = (step_time / total_step_time) * 100 if total_step_time > 0 else 0
            print(u"{:<12} {:>9.4f} {:>8.1f}%".format(step_name, avg_time_ms, percentage))
        
        # 找出最大的瓶颈
        if steps:
            bottleneck_name, bottleneck_time = steps[0]
            bottleneck_avg_ms = (bottleneck_time / total_calls) * 1000
            print(u"\n🔍 主要性能瓶颈: {} ({:.4f}ms/次)".format(bottleneck_name, bottleneck_avg_ms))
            
            # 提供优化建议
            if bottleneck_name == '行计数':
                print(u"💡 优化建议: 考虑禁用行计数功能 LPrint.set_line_counting(False)")
            elif bottleneck_name == '帧信息获取':
                print(u"💡 优化建议: 帧信息获取是必需的，但可能是调用栈过深导致")
            elif bottleneck_name == '序列化':
                print(u"💡 优化建议: 减少复杂对象的打印，或简化参数结构")
            elif bottleneck_name == '格式化':
                print(u"💡 优化建议: 减少字符串格式化操作")

def quick_performance_test():
    """快速性能测试 - 一键执行"""
    print(u"=== LPrint 快速性能测试 ===")
    
    profiler = PerformanceProfiler()
    profiler.save_settings()
    
    try:
        # 测试1: 正常模式
        def setup_normal():
            LPrint.set_line_counting(True)
            LPrint.enable_function_range_check = False
            LPrint.debug_self_global = False
        
        result_normal = profiler.run_test_scenario(u"正常模式", setup_normal, 30)
        
        # 测试2: 优化模式
        def setup_optimized():
            LPrint.set_line_counting(False)
            LPrint.enable_function_range_check = False
            LPrint.debug_self_global = False
        
        result_optimized = profiler.run_test_scenario(u"优化模式（禁用行计数）", setup_optimized, 30)
        
        # 对比分析
        print(u"\n=== 性能对比 ===")
        if result_normal['calls_per_second'] > 0 and result_optimized['calls_per_second'] > 0:
            improvement = (result_optimized['calls_per_second'] / result_normal['calls_per_second'] - 1) * 100
            print(u"性能提升: {:.1f}%".format(improvement))
            print(u"正常模式: {:.4f}ms/次".format(result_normal['avg_time_per_call']))
            print(u"优化模式: {:.4f}ms/次".format(result_optimized['avg_time_per_call']))
        
        # 分析瓶颈
        print(u"\n=== 正常模式瓶颈分析 ===")
        profiler.analyze_bottlenecks(result_normal['stats'])
        
    finally:
        profiler.restore_settings()

if __name__ == "__main__":
    print(u"LPrint 性能分析工具")
    quick_performance_test() 