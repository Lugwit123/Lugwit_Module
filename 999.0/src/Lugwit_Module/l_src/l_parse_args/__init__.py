# -*- coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
import sys

def parse_args(args):
    """
    解析命令行参数，将字符串值尝试转换为适当的Python类型。
    
    参数:
        args: 命令行参数列表
        
    返回:
        包含解析后参数的字典
    """
    arg_dict = {}
    current_key = None
    values = []

    # 辅助函数：尝试将字符串值转换为适当的Python类型
    def try_convert_value(value):
        if isinstance(value, str):
            try:
                return eval(value)
            except:
                return value
        return value

    for arg in args:
        if arg.startswith("--"):
            if current_key:
                value = values[0] if len(values) == 1 else values
                # 对当前值应用转换
                value = try_convert_value(value)
                arg_dict[current_key] = value
                values = []

            key_value = arg[2:].split("=", 1)
            if len(key_value) == 2:
                key, value = key_value
                # 对=号分隔的值应用转换
                value = try_convert_value(value)
                arg_dict[key] = value
                current_key = None
            else:
                key_value = arg[2:].split(" ", 1)
                if len(key_value) == 2:
                    key, value = key_value
                    # 对空格分隔的值应用转换
                    value = try_convert_value(value)
                    arg_dict[key] = value
                    current_key = None
                else:
                    current_key = key_value[0]
        elif arg.strip() and current_key:
            values.append(arg)

    # 处理最后一个参数，确保也应用相同的转换逻辑
    if current_key:
        value = values[0] if len(values) == 1 else values
        # 对最后一个值应用转换
        value = try_convert_value(value)
        arg_dict[current_key] = value
        
    return arg_dict

if __name__ == "__main__":
    # 测试1：原始参数
    print("=== 测试1：原始参数 ===")
    test_args1 = '--age \'20\' --upAxis True --UI --AssetType_Zh {} --aa False'.format(repr(u'角色')).split(' ')
    result1 = parse_args(test_args1)
    for k, v in result1.items():
        print("{0}: {1!r} (类型: {2})".format(k, v, type(v)))
    
    # 测试2：使用=号分隔
    print("\n=== 测试2：使用=号分隔 ===")
    test_args2 = '--age=\'20\' --upAxis=True --UI --AssetType_Zh={} --aa=False'.format(repr(u'角色')).split(' ')
    result2 = parse_args(test_args2)
    for k, v in result2.items():
        print("{0}: {1!r} (类型: {2})".format(k, v, type(v)))
    
    # 测试3：带引号的布尔值
    print("\n=== 测试3：带引号的布尔值 ===")
    test_args3 = ['--test1', 'False', '--test2', 'True', '--test3', '"False"', '--test4', "'False'"]
    result3 = parse_args(test_args3)
    for k, v in result3.items():
        print("{0}: {1!r} (类型: {2})".format(k, v, type(v)))
    
    # 测试4：数字和列表
    print("\n=== 测试4：数字和列表 ===")
    test_args4 = ['--num1', '123', '--num2', '3.14', '--list', '[1, 2, 3]', '--dict', '{"a": 1, "b": 2}']
    result4 = parse_args(test_args4)
    for k, v in result4.items():
        print("{0}: {1!r} (类型: {2})".format(k, v, type(v)))
