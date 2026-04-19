# -*- coding: utf-8 -*-
"""
LPrint 性能分析工具

这个模块提供了一个简单易用的性能分析接口，帮助用户快速定位lprint的性能瓶颈。

使用方法:
1. 基本性能分析:
   from performance_profiler import quick_performance_test
   quick_performance_test()

2. 详细性能对比:
   from performance_profiler import detailed_performance_comparison
   detailed_performance_comparison()

3. 自定义测试:
   from performance_profiler import PerformanceProfiler
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
    from usualFunc import LPrint, lprint

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
    
    def run_comprehensive_test(self):
        """运行全面的性能测试"""
        print(u"=== LPrint 全面性能分析 ===")
        
        # 保存当前设置
        self.save_settings()
        
        results = []
        
        try:
            # 测试1: 正常模式（所有功能启用）
            def setup_normal():
                LPrint.set_line_counting(True)
                LPrint.enable_function_range_check = False
                LPrint.debug_self_global = False
            
            results.append(self.run_test_scenario(u"正常模式", setup_normal))
            
            # 测试2: 优化模式（禁用行计数）
            def setup_optimized():
                LPrint.set_line_counting(False)
                LPrint.enable_function_range_check = False
                LPrint.debug_self_global = False
            
            results.append(self.run_test_scenario(u"优化模式（禁用行计数）", setup_optimized))
            
            # 测试3: 最小模式（所有优化启用）
            def setup_minimal():
                LPrint.set_line_counting(False)
                LPrint.enable_function_range_check = False
                LPrint.debug_self_global = False
                os.environ['Lugwit_Debug'] = 'noprint'
            
            results.append(self.run_test_scenario(u"最小模式（debug=noprint）", setup_minimal))
            
            # 恢复环境变量
            os.environ['Lugwit_Debug'] = 'inspect'
            
        finally:
            # 恢复原始设置
            self.restore_settings()
        
        # 生成对比报告
        self.generate_comparison_report(results)
        
        return results
    
    def generate_comparison_report(self, results):
        """生成对比报告"""
        print(u"\n=== 性能对比报告 ===")
        
        if len(results) < 2:
            print(u"结果数量不足，无法进行对比")
            return
        
        baseline = results[0]  # 以第一个结果作为基准
        
        print(u"以 '{}' 作为基准 (100%)".format(baseline['name']))
        print(u"{:<20} {:>10} {:>15} {:>15}".format(
            u"测试场景", u"相对性能", u"性能提升", u"平均耗时(ms)"
        ))
        print(u"-" * 65)
        
        for result in results:
            if result['calls_per_second'] > 0:
                relative_performance = (result['calls_per_second'] / baseline['calls_per_second']) * 100
                improvement = relative_performance - 100
                improvement_text = u"+{:.1f}%".format(improvement) if improvement > 0 else u"{:.1f}%".format(improvement)
            else:
                relative_performance = 0
                improvement_text = u"N/A"
            
            print(u"{:<20} {:>9.1f}% {:>14} {:>14.4f}".format(
                result['name'][:18],
                relative_performance,
                improvement_text,
                result['avg_time_per_call']
            ))
        
        # 详细分析最慢的步骤
        print(u"\n=== 详细性能分析 (正常模式) ===")
        if results:
            self.analyze_bottlenecks(results[0]['stats'])
    
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
    profiler = PerformanceProfiler()
    return profiler.run_comprehensive_test()

def detailed_performance_comparison(test_count=100):
    """详细性能对比测试
    
    Args:
        test_count (int): 每个场景的测试次数
    """
    profiler = PerformanceProfiler()
    profiler.save_settings()
    
    try:
        print(u"=== 详细性能对比测试 ({}次调用) ===".format(test_count))
        
        # 场景1: 所有功能启用
        def setup_full():
            LPrint.set_line_counting(True)
            LPrint.enable_function_range_check = True
            LPrint.debug_self_global = False
        
        result1 = profiler.run_test_scenario(u"完整功能模式", setup_full, test_count)
        
        # 场景2: 只禁用行计数
        def setup_no_line_counting():
            LPrint.set_line_counting(False)
            LPrint.enable_function_range_check = True
            LPrint.debug_self_global = False
        
        result2 = profiler.run_test_scenario(u"禁用行计数", setup_no_line_counting, test_count)
        
        # 场景3: 禁用所有检查
        def setup_minimal():
            LPrint.set_line_counting(False)
            LPrint.enable_function_range_check = False
            LPrint.debug_self_global = False
        
        result3 = profiler.run_test_scenario(u"最小开销模式", setup_minimal, test_count)
        
        # 生成对比
        profiler.generate_comparison_report([result1, result2, result3])
        
    finally:
        profiler.restore_settings()

if __name__ == "__main__":
    print(u"LPrint 性能分析工具")
    print(u"运行快速性能测试...")
    quick_performance_test() 