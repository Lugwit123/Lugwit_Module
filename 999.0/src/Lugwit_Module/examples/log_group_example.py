# -*- coding: utf-8 -*-
"""
日志分组功能使用示例

演示如何使用 lprint 的 log_group 参数来对日志进行分组
"""
from __future__ import print_function
import sys
import os

# 添加 Lugwit_Module 到路径
module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if module_path not in sys.path:
    sys.path.insert(0, module_path)

import Lugwit_Module as LM
lprint = LM.lprint


# ============ 方式1: 使用字符串作为分组 ============
def example_string_group():
    """使用字符串作为日志分组"""
    print("\n" + "="*60)
    print("示例1: 使用字符串作为日志分组")
    print("="*60)
    
    lprint("连接数据库", log_group="DATABASE")
    lprint("执行SQL查询", log_group="DATABASE")
    lprint("调用外部API", log_group="API")
    lprint("渲染UI组件", log_group="UI")


# ============ 方式2: 使用枚举作为分组（推荐）============
if sys.version_info[0] >= 3:
    from enum import Enum
    
    class LogGroup(Enum):
        """日志分组枚举 - 使用 value 作为显示值"""
        DATABASE = "DB"      # 数据库相关
        API = "API"          # API调用相关
        UI = "UI"            # UI相关
        CACHE = "CACHE"      # 缓存相关
        NETWORK = "NET"      # 网络相关
    
    def example_enum_group():
        """使用枚举作为日志分组（推荐方式）"""
        print("\n" + "="*60)
        print("示例2: 使用枚举作为日志分组（推荐）")
        print("="*60)
        
        lprint("查询用户数据", log_group=LogGroup.DATABASE)
        lprint("更新缓存", log_group=LogGroup.CACHE)
        lprint("发送HTTP请求", log_group=LogGroup.API)
        lprint("刷新界面", log_group=LogGroup.UI)
        lprint("检查网络连接", log_group=LogGroup.NETWORK)


# ============ 方式3: 项目自定义枚举 ============
if sys.version_info[0] >= 3:
    class MyProjectLogGroup(Enum):
        """项目特定的日志分组"""
        TASK_MANAGER = "任务管理"
        FILE_SYNC = "文件同步"
        USER_AUTH = "用户认证"
        DATA_PROCESS = "数据处理"
    
    def example_custom_enum():
        """使用项目自定义的枚举"""
        print("\n" + "="*60)
        print("示例3: 使用项目自定义枚举")
        print("="*60)
        
        lprint("创建新任务", log_group=MyProjectLogGroup.TASK_MANAGER)
        lprint("同步文件到云端", log_group=MyProjectLogGroup.FILE_SYNC)
        lprint("验证用户令牌", log_group=MyProjectLogGroup.USER_AUTH)
        lprint("处理Excel数据", log_group=MyProjectLogGroup.DATA_PROCESS)


# ============ 方式4: 混合使用 ============
def example_mixed_usage():
    """混合使用字符串和枚举"""
    print("\n" + "="*60)
    print("示例4: 混合使用（向后兼容）")
    print("="*60)
    
    # 不使用分组（向后兼容）
    lprint("这是一条普通日志")
    
    # 使用字符串分组
    lprint("临时调试信息", log_group="DEBUG")
    
    # 使用枚举分组（如果是Python 3）
    if sys.version_info[0] >= 3:
        lprint("重要的数据库操作", log_group=LogGroup.DATABASE)


# ============ 实际应用场景示例 ============
def example_real_world_scenario():
    """实际应用场景：数据处理流程"""
    print("\n" + "="*60)
    print("示例5: 实际应用场景 - 数据处理流程")
    print("="*60)
    
    if sys.version_info[0] >= 3:
        # 模拟一个完整的数据处理流程
        lprint("开始数据处理任务", log_group=LogGroup.DATABASE)
        lprint("从数据库读取1000条记录", log_group=LogGroup.DATABASE)
        
        lprint("调用数据清洗API", log_group=LogGroup.API)
        lprint("API返回成功", log_group=LogGroup.API)
        
        lprint("缓存处理结果", log_group=LogGroup.CACHE)
        lprint("缓存命中率: 85%", log_group=LogGroup.CACHE)
        
        lprint("更新进度条", log_group=LogGroup.UI)
        lprint("显示完成提示", log_group=LogGroup.UI)
        
        lprint("任务完成，总耗时: 2.5秒", log_group=LogGroup.DATABASE)
    else:
        # Python 2 使用字符串
        lprint("开始数据处理任务", log_group="DATABASE")
        lprint("从数据库读取1000条记录", log_group="DATABASE")
        lprint("任务完成", log_group="DATABASE")


# ============ 性能对比 ============
def example_performance():
    """性能对比：枚举 vs 字符串"""
    print("\n" + "="*60)
    print("示例6: 性能说明")
    print("="*60)
    
    print("""
性能对比：
1. 枚举方式：
   - 优点：类型安全、IDE自动补全、避免拼写错误
   - 开销：几乎为零（只是属性访问）
   
2. 字符串方式：
   - 优点：简单直接、无需导入
   - 开销：几乎为零
   
结论：两种方式性能差异可忽略不计，推荐使用枚举以获得更好的开发体验
    """)


# ============ 日志过滤示例 ============
def example_log_filtering():
    """演示如何过滤特定分组的日志"""
    print("\n" + "="*60)
    print("示例7: 日志过滤")
    print("="*60)
    
    print("""
日志过滤方法：

1. 使用 grep 过滤特定分组：
   grep "\\[DATABASE\\]" digital_workspace_main.log
   grep "\\[API\\]" digital_workspace_main.log

2. 使用 Python 脚本过滤：
   with open('log.txt') as f:
       db_logs = [line for line in f if '[DATABASE]' in line]

3. 在日志查看工具中搜索：
   搜索关键词: [DATABASE]
    """)


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("lprint 日志分组功能使用示例")
    print("="*60)
    
    # 运行示例
    example_string_group()
    
    if sys.version_info[0] >= 3:
        example_enum_group()
        example_custom_enum()
    
    example_mixed_usage()
    example_real_world_scenario()
    example_performance()
    example_log_filtering()
    
    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60)


if __name__ == "__main__":
    main()
