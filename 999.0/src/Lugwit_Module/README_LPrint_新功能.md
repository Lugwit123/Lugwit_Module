# LPrint 类新功能说明

## 概述

为 `LPrint` 类添加了两个新功能：

1. **类属性 `detailed_log_functions`**: 包含函数字符串的列表，支持通配符匹配
2. **实例参数 `log_width`**: 控制在当前帧前后打印的代码行数

## 新功能详解

### 1. 详细日志函数列表 (detailed_log_functions)

这是一个类属性，包含需要详细日志记录的函数名模式列表，支持通配符。

#### 默认模式
```python
detailed_log_functions = [
    "*maya*",           # 匹配包含maya的函数
    "*export*",         # 匹配包含export的函数 
    "get_*",           # 匹配以get_开头的函数
    "*_format_*",      # 匹配包含_format_的函数
]
```

#### 管理方法

**添加模式**:
```python
LPrint.add_detailed_function("my_pattern*")
```

**移除模式**:
```python
LPrint.remove_detailed_function("my_pattern*")
```

**查看所有模式**:
```python
patterns = LPrint.list_detailed_functions()
print("当前模式:", patterns)
```

### 2. 日志宽度控制 (log_width)

这是一个实例参数，控制在调用帧前后打印的代码行数。

#### 初始化时设置
```python
# 创建时指定宽度
lprint_instance = LPrint(log_width=5)
```

#### 动态修改宽度
```python
# 设置为3行（前后各3行）
lprint.set_log_width(3)

# 关闭扩展上下文
lprint.set_log_width(0)
```

## 工作原理

### 匹配逻辑
1. 当 `lprint` 被调用时，系统获取调用函数的名称
2. 使用 `fnmatch` 模块检查函数名是否匹配 `detailed_log_functions` 中的任一模式
3. 如果匹配且 `log_width > 0`，则显示扩展的代码上下文
4. **新功能**: 在扩展的代码范围内自动检测其他 `lprint` 调用并提取其参数内容

### 范围内lprint检测
- 自动扫描指定宽度范围内的所有代码行
- 使用正则表达式检测 `lprint(...)` 调用
- 提取lprint参数并显示在扩展上下文中
- 忽略当前正在执行的lprint行，避免重复

### 扩展上下文格式
当函数匹配模式时，日志输出会包含：
```
--- 扩展代码上下文 (±3 行) ---
      28: def get_some_data():
      29:     lprint(u"步骤1: 初始化")  
      30:     data_list = []
  >>> 31:     lprint(u"这是来自 get_some_data 函数的日志")
      32:     lprint(u"步骤2: 处理数据")
      33:     return data_list
      34: 
--- 范围内的其他lprint输出 ---
    [行29的lprint] 步骤1: 初始化
    [行32的lprint] 步骤2: 处理数据
--- 扩展上下文结束 ---
```

## 使用示例

### 基本使用
```python
from l_src.usualFunc import LPrint, lprint

# 查看当前模式
print("当前模式:", LPrint.list_detailed_functions())

# 添加自定义模式
LPrint.add_detailed_function("*database*")

def get_user_data():
    """匹配 get_* 模式"""
    lprint("获取用户数据")  # 会显示扩展上下文
    return []

def database_connect():
    """匹配 *database* 模式"""
    lprint("连接数据库")  # 会显示扩展上下文
    return True

def normal_function():
    """不匹配任何模式"""
    lprint("普通日志")  # 正常显示
    return None
```

### 动态控制
```python
# 设置较大的上下文宽度
lprint.set_log_width(5)
get_user_data()  # 显示前后各5行

# 关闭扩展上下文
lprint.set_log_width(0)
get_user_data()  # 只显示正常日志

# 恢复默认
lprint.set_log_width(3)
```

### 模式管理
```python
# 查看所有模式
all_patterns = LPrint.list_detailed_functions()
print("所有模式:", all_patterns)

# 添加多个模式
LPrint.add_detailed_function("*test*")
LPrint.add_detailed_function("debug_*")
LPrint.add_detailed_function("*_check")

# 移除不需要的模式
LPrint.remove_detailed_function("*test*")
```

## 通配符支持

支持标准的通配符模式：
- `*`: 匹配任意长度的字符串
- `?`: 匹配单个字符
- `[seq]`: 匹配seq中的任意字符
- `[!seq]`: 匹配不在seq中的任意字符

### 示例模式
```python
patterns = [
    "*maya*",      # maya_export, export_maya, get_maya_data
    "get_*",       # get_data, get_user, get_anything
    "*_test",      # unit_test, integration_test
    "debug_*_*",   # debug_maya_export, debug_user_data
    "test_???",    # test_abc, test_123 (正好3个字符)
]
```

## 注意事项

1. **性能**: 匹配检查对性能影响很小，但读取源文件会有一定开销
2. **文件编码**: 自动尝试 UTF-8 和 GBK 编码读取源文件
3. **线程安全**: 类属性的修改会影响所有实例
4. **模式匹配**: 匹配是大小写不敏感的

## 测试

运行测试脚本查看效果：
```bash
python test_lprint_features.py
```

这将演示所有新功能的使用方法和效果。 