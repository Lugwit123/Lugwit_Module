# -*- coding: utf-8 -*-
"""
测试 LPrint 的新功能：
1. 类属性详细日志函数列表（支持通配符）
2. log_width 实例参数控制扩展代码上下文显示
"""

import sys
import os

# 添加路径
sys.path.append(os.path.dirname(__file__))
from l_src.usualFunc import LPrint, lprint

def test_detailed_logging():
    """测试详细日志记录功能"""
    print(u"=== 测试扩展代码上下文功能 ===")
    
    # 显示当前的详细日志函数模式
    print(u"当前详细日志函数模式:", LPrint.list_detailed_functions())
    
    # 添加新的模式
    LPrint.add_detailed_function("test_*")
    print(u"添加模式 'test_*' 后:", LPrint.list_detailed_functions())
    
    return True

def test_maya_export():
    """这个函数名匹配 *maya* 模式，应该显示扩展上下文"""
    lprint(u"这是来自 test_maya_export 函数的日志，应该显示扩展上下文")
    # 添加一些其他代码行
    x = 1 + 1
    y = x * 2
    z = y + 3
    return "完成"

def get_some_data():
    """这个函数名匹配 get_* 模式，应该显示扩展上下文"""  
    data_list = []
    data_list.append("数据1")
    data_list.append("数据2")
    lprint(u"这是来自 get_some_data 函数的日志，应该显示扩展上下文")
    more_data = ["额外数据"]
    return data_list + more_data

def normal_function():
    """这个函数名不匹配任何模式，应该显示正常日志"""
    temp_var = "临时变量"
    lprint(u"这是来自 normal_function 函数的日志，正常显示")
    result = None
    return result

def test_export_maya_scene():
    """这个函数名也匹配 *export* 模式，包含多个lprint调用"""
    scene_name = "test_scene"
    lprint(u"开始导出Maya场景")
    export_path = "/tmp/exports/"
    lprint(u"导出Maya场景: {} 到 {}".format(scene_name, export_path))
    # 模拟一些导出操作
    lprint(u"设置导出参数")
    export_success = True
    lprint(u"导出完成")
    return export_success

def get_complex_data():
    """这个函数有多个lprint，测试范围内lprint检测"""
    lprint(u"步骤1: 初始化数据结构")
    data = {}
    lprint(u"步骤2: 加载配置文件")
    config = {"setting": "value"}
    data.update(config)
    lprint(u"步骤3: 验证数据完整性")
    if data:
        lprint(u"数据验证成功")
        return data
    else:
        lprint(u"数据验证失败")
        return None

if __name__ == "__main__":
    # 测试初始设置
    test_detailed_logging()
    
    print(u"\n--- 测试匹配 *maya* 模式的函数 ---")
    test_maya_export()
    
    print(u"\n--- 测试匹配 get_* 模式的函数 ---") 
    get_some_data()
    
    print(u"\n--- 测试匹配 *export* 模式的函数 ---")
    test_export_maya_scene()
    
    print(u"\n--- 测试不匹配任何模式的函数 ---")
    normal_function()
    
    print(u"\n--- 测试包含多个lprint的复杂函数 ---")
    get_complex_data()
    
    # 测试动态修改日志宽度
    print(u"\n--- 测试修改日志宽度为5行 ---")
    lprint.set_log_width(5)
    test_maya_export()
    
    # 测试关闭扩展上下文
    print(u"\n--- 测试关闭扩展上下文 (宽度设为0) ---") 
    lprint.set_log_width(0)
    test_maya_export()
    
    # 测试不同的宽度设置
    print(u"\n--- 测试不同宽度设置 ---")
    for width in [1, 2, 4]:
        print(u"\n>> 设置宽度为 {} 行".format(width))
        lprint.set_log_width(width)
        get_some_data()
    
    # 恢复默认设置
    lprint.set_log_width(3)
    LPrint.remove_detailed_function("test_*")
    print(u"\n恢复默认设置，移除 'test_*' 模式")
    print(u"最终详细日志函数模式:", LPrint.list_detailed_functions()) 