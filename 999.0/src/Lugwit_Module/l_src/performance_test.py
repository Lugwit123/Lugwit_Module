# -*- coding: utf-8 -*-
"""
LPrint性能测试模块

独立的性能测试功能，不依赖LPrint类内部实现
用于测试lprint在不同配置下的性能表现
"""
from __future__ import print_function, absolute_import
import os
import time
import sys

def quick_performance_test(lprint_instance, iterations=500):
    """快速性能测试：简化版性能对比
    
    Args:
        lprint_instance: lprint实例
        iterations (int): 测试迭代次数，默认500次
        
    Returns:
        tuple: (优化模式耗时, 正常模式耗时, 性能提升百分比)
    """
    # 保存原始设置
    original_debug = os.environ.get('Lugwit_Debug', 'inspect')
    original_line_counting = lprint_instance.enable_line_counting
    
    try:
        # 测试优化模式
        lprint_instance.set_line_counting(False)
        os.environ['Lugwit_Debug'] = 'noprint'
        
        start = time.time()
        for i in range(iterations):
            lprint_instance(u"测试消息", i, {"data": "test"})
        optimized_time = time.time() - start
        
        # 测试正常模式
        lprint_instance.set_line_counting(True)
        os.environ['Lugwit_Debug'] = 'inspect'
        
        start = time.time()
        for i in range(iterations):
            lprint_instance(u"测试消息", i, {"data": "test"})
        normal_time = time.time() - start
        
        # 计算提升百分比
        if normal_time > 0:
            improvement = ((normal_time - optimized_time) / normal_time) * 100
        else:
            improvement = 0
            
        print(u"快速性能测试结果 ({} 次迭代):".format(iterations))
        print(u"  优化模式: {:.4f}秒".format(optimized_time))
        print(u"  正常模式: {:.4f}秒".format(normal_time))
        print(u"  性能提升: {:.1f}%".format(improvement))
        
        return optimized_time, normal_time, improvement
        
    finally:
        # 恢复设置
        os.environ['Lugwit_Debug'] = original_debug
        lprint_instance.set_line_counting(original_line_counting)


def performance_test(lprint_instance, test_iterations=1000, verbose=True):
    """详细性能测试：对比不同配置下的lprint执行时间
    
    Args:
        lprint_instance: lprint实例
        test_iterations (int): 测试迭代次数，默认1000次
        verbose (bool): 是否显示详细结果，默认True
        
    Returns:
        dict: 性能测试结果，包含各种配置下的执行时间
    """
    # 保存当前设置
    original_debug_env = os.environ.get('Lugwit_Debug', 'inspect')
    original_line_counting = lprint_instance.enable_line_counting
    original_debug_self = lprint_instance.debug_self_global
    
    # 测试数据
    test_args = [
        (u"性能测试消息1",),
        (u"测试", 123, [1, 2, 3]),
        ({u"key": u"value"}, u"复杂数据测试"),
        (u"简单消息",),
    ]
    
    results = {}
    
    try:
        if verbose:
            print(u"\n=== LPrint 性能测试开始 ===")
            print(u"测试迭代次数: {}".format(test_iterations))
            print(u"测试参数组数: {}".format(len(test_args)))
        
        # 测试1: 最高性能模式 (debug=noprint + line_counting=False)
        if verbose:
            print(u"\n1. 测试最高性能模式 (debug=noprint + line_counting=False)")
        lprint_instance.set_line_counting(False)
        lprint_instance.set_debug_self_global(False)  # 避免debug信息影响性能
        os.environ['Lugwit_Debug'] = 'noprint'
        
        start_time = time.time()
        for i in range(test_iterations):
            for args in test_args:
                lprint_instance(*args)
        end_time = time.time()
        results['high_performance'] = end_time - start_time
        
        if verbose:
            print(u"   执行时间: {:.4f}秒".format(results['high_performance']))
        
        # 测试2: 中等性能模式 (debug=noprint + line_counting=True)
        if verbose:
            print(u"\n2. 测试中等性能模式 (debug=noprint + line_counting=True)")
        lprint_instance.set_line_counting(True)
        os.environ['Lugwit_Debug'] = 'noprint'
        
        start_time = time.time()
        for i in range(test_iterations):
            for args in test_args:
                lprint_instance(*args)
        end_time = time.time()
        results['medium_performance'] = end_time - start_time
        
        if verbose:
            print(u"   执行时间: {:.4f}秒".format(results['medium_performance']))
        
        # 测试3: 正常模式 (debug=inspect + line_counting=True)
        if verbose:
            print(u"\n3. 测试正常模式 (debug=inspect + line_counting=True)")
        lprint_instance.set_line_counting(True)
        os.environ['Lugwit_Debug'] = 'inspect'
        
        start_time = time.time()
        for i in range(test_iterations):
            for args in test_args:
                lprint_instance(*args)
        end_time = time.time()
        results['normal_mode'] = end_time - start_time
        
        if verbose:
            print(u"   执行时间: {:.4f}秒".format(results['normal_mode']))
        
        # 计算性能提升比例
        if results['normal_mode'] > 0:
            high_perf_improvement = ((results['normal_mode'] - results['high_performance']) / results['normal_mode']) * 100
            medium_perf_improvement = ((results['normal_mode'] - results['medium_performance']) / results['normal_mode']) * 100
            
            results['high_performance_improvement'] = high_perf_improvement
            results['medium_performance_improvement'] = medium_perf_improvement
            
            if verbose:
                print(u"\n=== 性能提升分析 ===")
                print(u"最高性能模式 vs 正常模式: 提升 {:.1f}%".format(high_perf_improvement))
                print(u"中等性能模式 vs 正常模式: 提升 {:.1f}%".format(medium_perf_improvement))
                
                # 显示每秒处理能力
                total_calls = test_iterations * len(test_args)
                print(u"\n=== 每秒处理能力 ===")
                print(u"最高性能模式: {:.0f} calls/sec".format(total_calls / results['high_performance']))
                print(u"中等性能模式: {:.0f} calls/sec".format(total_calls / results['medium_performance']))
                print(u"正常模式: {:.0f} calls/sec".format(total_calls / results['normal_mode']))
        
        if verbose:
            print(u"\n=== 性能测试完成 ===")
            
    finally:
        # 恢复原始设置
        os.environ['Lugwit_Debug'] = original_debug_env
        lprint_instance.set_line_counting(original_line_counting)
        lprint_instance.set_debug_self_global(original_debug_self)
        
    return results


def benchmark_for_production(lprint_instance, duration_seconds=5):
    """生产环境性能基准测试：在指定时间内测试最大吞吐量
    
    Args:
        lprint_instance: lprint实例
        duration_seconds (int): 测试持续时间（秒），默认5秒
        
    Returns:
        dict: 包含各模式下每秒处理的lprint调用次数
    """
    # 保存原始设置
    original_debug = os.environ.get('Lugwit_Debug', 'inspect')
    original_line_counting = lprint_instance.enable_line_counting
    original_debug_self = lprint_instance.debug_self_global
    
    results = {}
    
    try:
        print(u"\n=== 生产环境性能基准测试 ===")
        print(u"测试持续时间: {}秒".format(duration_seconds))
        
        # 测试1: 最高性能模式
        print(u"\n测试最高性能模式...")
        lprint_instance.set_line_counting(False)
        lprint_instance.set_debug_self_global(False)
        os.environ['Lugwit_Debug'] = 'noprint'
        
        start_time = time.time()
        count = 0
        while time.time() - start_time < duration_seconds:
            lprint_instance(u"基准测试", count, {"mode": "high_performance"})
            count += 1
        
        results['high_performance_calls_per_sec'] = count / duration_seconds
        print(u"最高性能模式: {:.0f} calls/sec".format(results['high_performance_calls_per_sec']))
        
        # 测试2: 正常模式  
        print(u"\n测试正常模式...")
        lprint_instance.set_line_counting(True)
        os.environ['Lugwit_Debug'] = 'inspect'
        
        # 重置计数器避免影响测试
        lprint_instance.reset_line_counts()
        
        start_time = time.time()
        count = 0
        while time.time() - start_time < duration_seconds:
            lprint_instance(u"基准测试", count, {"mode": "normal"})
            count += 1
        
        results['normal_mode_calls_per_sec'] = count / duration_seconds
        print(u"正常模式: {:.0f} calls/sec".format(results['normal_mode_calls_per_sec']))
        
        # 计算性能倍数
        if results['normal_mode_calls_per_sec'] > 0:
            performance_ratio = results['high_performance_calls_per_sec'] / results['normal_mode_calls_per_sec']
            results['performance_ratio'] = performance_ratio
            print(u"\n性能倍数: {:.2f}x 倍".format(performance_ratio))
            print(u"性能提升: {:.1f}%".format((performance_ratio - 1) * 100))
        
        return results
        
    finally:
        # 恢复设置
        os.environ['Lugwit_Debug'] = original_debug
        lprint_instance.set_line_counting(original_line_counting)
        lprint_instance.set_debug_self_global(original_debug_self)


def memory_usage_test(lprint_instance, iterations=1000):
    """内存使用测试：监控不同模式下的内存占用
    
    Args:
        lprint_instance: lprint实例
        iterations (int): 测试迭代次数
        
    Returns:
        dict: 内存使用统计
    """
    try:
        import psutil
        import gc
    except ImportError:
        print(u"警告：psutil模块未安装，无法进行内存测试")
        return {}
    
    # 保存原始设置
    original_debug = os.environ.get('Lugwit_Debug', 'inspect')
    original_line_counting = lprint_instance.enable_line_counting
    
    results = {}
    
    try:
        process = psutil.Process()
        
        print(u"\n=== 内存使用测试 ===")
        print(u"测试迭代次数: {}".format(iterations))
        
        # 基线内存
        gc.collect()  # 强制垃圾回收
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(u"基线内存: {:.2f} MB".format(baseline_memory))
        
        # 测试1: 优化模式
        lprint_instance.set_line_counting(False)
        os.environ['Lugwit_Debug'] = 'noprint'
        
        gc.collect()
        start_memory = process.memory_info().rss / 1024 / 1024
        
        for i in range(iterations):
            lprint_instance(u"内存测试", i, {"mode": "optimized", "data": "x" * 10})
        
        gc.collect()
        end_memory = process.memory_info().rss / 1024 / 1024
        optimized_memory_delta = end_memory - start_memory
        results['optimized_memory_delta'] = optimized_memory_delta
        
        print(u"优化模式内存增量: {:.2f} MB".format(optimized_memory_delta))
        
        # 清理并重置
        lprint_instance.reset_line_counts()
        gc.collect()
        
        # 测试2: 正常模式
        lprint_instance.set_line_counting(True)
        os.environ['Lugwit_Debug'] = 'inspect'
        
        gc.collect()
        start_memory = process.memory_info().rss / 1024 / 1024
        
        for i in range(iterations):
            lprint_instance(u"内存测试", i, {"mode": "normal", "data": "x" * 10})
        
        gc.collect()
        end_memory = process.memory_info().rss / 1024 / 1024
        normal_memory_delta = end_memory - start_memory
        results['normal_memory_delta'] = normal_memory_delta
        
        print(u"正常模式内存增量: {:.2f} MB".format(normal_memory_delta))
        
        # 计算内存节约
        if normal_memory_delta > 0:
            memory_savings = ((normal_memory_delta - optimized_memory_delta) / normal_memory_delta) * 100
            results['memory_savings_percent'] = memory_savings
            print(u"内存节约: {:.1f}%".format(memory_savings))
        
        return results
        
    finally:
        # 恢复设置
        os.environ['Lugwit_Debug'] = original_debug
        lprint_instance.set_line_counting(original_line_counting)


def run_all_performance_tests(lprint_instance):
    """运行所有性能测试
    
    Args:
        lprint_instance: lprint实例
        
    Returns:
        dict: 所有测试结果
    """
    print(u"\n=== 开始完整性能测试套件 ===")
    
    all_results = {}
    
    # 快速测试
    print(u"\n>> 快速性能测试:")
    quick_results = quick_performance_test(lprint_instance, iterations=300)
    all_results['quick_test'] = {
        'optimized_time': quick_results[0],
        'normal_time': quick_results[1], 
        'improvement_percent': quick_results[2]
    }
    
    # 详细测试
    print(u"\n>> 详细性能测试:")
    detailed_results = performance_test(lprint_instance, test_iterations=200, verbose=True)
    all_results['detailed_test'] = detailed_results
    
    # 基准测试
    print(u"\n>> 生产环境基准测试:")
    benchmark_results = benchmark_for_production(lprint_instance, duration_seconds=3)
    all_results['benchmark_test'] = benchmark_results
    
    # 内存测试
    print(u"\n>> 内存使用测试:")
    memory_results = memory_usage_test(lprint_instance, iterations=500)
    all_results['memory_test'] = memory_results
    
    # 生成总结报告
    print(u"\n=== 性能测试总结报告 ===")
    if 'improvement_percent' in all_results['quick_test']:
        print(u"快速测试 - 性能提升: {:.1f}%".format(all_results['quick_test']['improvement_percent']))
    if 'performance_ratio' in all_results['benchmark_test']:
        print(u"基准测试 - 性能倍数: {:.2f}x".format(all_results['benchmark_test']['performance_ratio']))
    if 'memory_savings_percent' in all_results['memory_test']:
        print(u"内存测试 - 内存节约: {:.1f}%".format(all_results['memory_test']['memory_savings_percent']))
    
    return all_results 