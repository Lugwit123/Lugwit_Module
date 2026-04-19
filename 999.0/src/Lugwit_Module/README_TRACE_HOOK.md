# 全局异常钩子使用说明

## 功能介绍

全局异常钩子可以在程序发生异常时，自动输出详细的函数调用链，帮助快速定位问题。

## 安装方法

### 方法1：在程序开头自动安装（推荐）

在您的Python程序开头添加以下代码：

```python
# 安装全局异常钩子，在异常发生时显示详细调用链
try:
    from Lugwit_Module.trace_hook import install_trace_hook
    install_trace_hook()
    print("✅ 已安装全局异常钩子")
except ImportError:
    print("⚠️ 无法导入异常钩子模块")
```

### 方法2：手动安装

```python
from Lugwit_Module.trace_hook import install_trace_hook
install_trace_hook()
```

## 使用效果

当程序发生异常时，会输出以下信息：

1. **标准异常信息**：Python默认的异常堆栈
2. **函数调用链回溯**：
   - 调用层级
   - 函数名和参数
   - 文件位置
   - 重要局部变量
3. **异常发生时间**

### 示例输出

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
💥 发生异常: AttributeError: module 'Lugwit_Module' has no attribute 'hostName'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

📋 标准异常信息:
Traceback (most recent call last):
  File "D:\...\plugSync.py", line 89, in <module>
    if LM.hostName not in ['DESKTOP-LDSM1H1','TD','PC-20240202CTEU',"TD2","TD3"]:
       ^^^^^^^^^^^
AttributeError: module 'Lugwit_Module' has no attribute 'hostName'

🔗 函数调用链回溯:
================================================================================
🔍 函数调用链回溯 (最多显示 15 层)
================================================================================

📌 调用层级 1:
   函数: <module>()
   位置: plugSync.py:89
   局部变量:
     LM = <module 'Lugwit_Module' from '...'>
     
📌 调用层级 2:
   函数: some_function()
   位置: other_module.py:45
   局部变量:
     param1 = "some_value"
     result = None

================================================================================
⏰ 异常发生时间: 2026-03-28 13:17:00
================================================================================
```

## 测试钩子

运行测试脚本验证钩子是否正常工作：

```bash
python test_hook.py
```

## 卸载钩子

如果需要卸载钩子：

```python
from Lugwit_Module.trace_hook import uninstall_trace_hook
uninstall_trace_hook()
```

## 注意事项

1. 钩子会捕获所有未处理的异常
2. 调用链深度默认最多显示15层
3. 局部变量值会被截断以避免输出过长
4. 只显示重要的局部变量（如self、result、data等）

## 自定义配置

您可以根据需要修改 `trace_hook.py` 中的配置：
- `max_depth`: 调用链显示的最大深度
- `important_vars`: 需要显示的局部变量列表
- 输出格式和样式
