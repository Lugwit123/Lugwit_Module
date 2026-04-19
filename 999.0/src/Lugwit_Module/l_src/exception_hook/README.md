# 异常钩子模块

## 功能介绍

这个模块提供了全局异常捕获和调用链回溯功能，帮助开发者快速定位和调试问题。支持通过环境变量控制是否启用钩子。

## 安装和使用

### 1. 基本使用

```python
from l_src.exception_hook import install_trace_hook

# 安装全局异常钩子
install_trace_hook()

# 现在所有未处理的异常都会显示详细的调用链
```

### 2. 在程序开头自动安装

在您的Python程序开头添加：

```python
# 安装全局异常钩子，在异常发生时显示详细调用链
try:
    from l_src.exception_hook import install_trace_hook
    install_trace_hook()
    print("✅ 已安装全局异常钩子")
except ImportError:
    print("⚠️ 无法导入异常钩子模块")
```

### 3. 通过环境变量控制

#### 禁用异常钩子
```bash
# Windows
set DISABLE_EXCEPTION_HOOK=1
python your_script.py

# Linux/Mac
export DISABLE_EXCEPTION_HOOK=1
python your_script.py

# 或者在Python中设置
import os
os.environ['DISABLE_EXCEPTION_HOOK'] = '1'
```

#### 支持的环境变量值
- `'1'`, `'true'`, `'yes'`, `'on'` - 禁用钩子
- `'0'`, `'false'`, `'no'`, `'off'` 或未设置 - 启用钩子

### 4. 钩子状态管理

```python
from l_src.exception_hook import (
    install_trace_hook,
    uninstall_trace_hook,
    is_hook_installed,
    get_hook_status
)

# 检查钩子是否已安装
if is_hook_installed():
    print("钩子已安装")

# 获取详细状态
status = get_hook_status()
print(f"安装状态: {status['installed']}")
print(f"环境变量禁用: {status['disabled_by_env']}")
print(f"当前钩子类型: {status['current_hook']}")

# 卸载钩子
uninstall_trace_hook()
```

## 功能特性

### 🔍 自动异常捕获
- 捕获所有未处理的异常
- 显示异常类型和详细信息
- 记录异常发生时间

### 🔗 调用链回溯
- 显示完整的函数调用路径
- 每层调用显示文件名和行号
- 显示函数参数和重要局部变量

### 🎛️ 环境变量控制
- 通过 `DISABLE_EXCEPTION_HOOK` 环境变量控制
- 支持多种禁用值格式
- 防止重复安装钩子

### 📝 日志记录
- 可选的异常日志记录功能
- 自动按日期分割日志文件
- 支持自定义日志路径

## 示例输出

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
💥 发生异常: AttributeError: module 'Lugwit_Module' has no attribute 'hostName'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

📋 标准异常信息:
Traceback (most recent call last):
  File "plugSync.py", line 89, in <module>
    if LM.hostName not in ['DESKTOP-LDSM1H1','TD','PC-20240202CTEU',"TD2","TD3"]:
       ^^^^^^^^^^^
AttributeError: module 'Lugwit_Module' has no attribute 'hostName'

🔗 函数调用链回溯:
================================================================================
🔍 函数调用链回溯 (最多显示 15 层)
================================================================================

📌 调用层级 1:
   函数: <module>
   位置: plugSync.py:89
   局部变量:
     LM = <module 'Lugwit_Module' from '...'>
     
📌 调用层级 2:
   函数: some_function
   位置: other_module.py:45
   局部变量:
     param1 = "some_value"
     result = None

================================================================================
⏰ 异常发生时间: 2026-03-28 13:21:00
================================================================================
```

## 高级功能

### 1. 自定义异常处理

```python
from l_src.exception_hook import get_exception_summary, format_exception_for_report

# 获取异常摘要
summary = get_exception_summary(exc_type, exc_value, exc_traceback)

# 生成报告格式
report = format_exception_for_report(exc_type, exc_value, exc_traceback)
```

### 2. 异常日志记录

```python
from l_src.exception_hook.utils import setup_exception_logger, log_exception

# 设置日志记录器
logger = setup_exception_logger("/path/to/exception.log")

# 记录异常
log_exception(exc_type, exc_value, exc_traceback, logger)
```

### 3. 判断重要异常

```python
from l_src.exception_hook.utils import is_important_exception

# 判断是否为重要异常
if is_important_exception(exc_type):
    # 发送告警通知
    pass
```

## 测试

运行测试脚本验证功能：

```bash
python l_src/exception_hook/test.py
```

## 注意事项

1. 钩子会捕获所有未处理的异常
2. 调用链深度默认最多显示15层
3. 局部变量值会被截断以避免输出过长
4. 只显示重要的局部变量（如self、result、data等）

## 版本信息

- 版本: 1.0.0
- 作者: Lugwit Team
- 兼容: Python 3.6+
