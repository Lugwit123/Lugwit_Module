# lprint 日志分组功能

## 功能概述

`lprint` 新增了 `log_group` 参数，用于对日志进行分组和分类，便于后续过滤和查看。

## 核心特性

✅ **支持枚举和字符串**：可以使用任意枚举类或字符串作为分组标识  
✅ **性能开销极低**：只是简单的字符串拼接，几乎无性能损耗  
✅ **向后兼容**：不传 `log_group` 参数时行为完全不变  
✅ **类型安全**：使用枚举可获得 IDE 自动补全和类型检查  
✅ **易于过滤**：可用 grep 或日志工具按分组快速过滤

## 使用方法

### 方式1: 使用字符串（简单直接）

```python
import Lugwit_Module as LM
lprint = LM.lprint

lprint("连接数据库", log_group="DATABASE")
lprint("调用API", log_group="API")
lprint("更新UI", log_group="UI")
```

**输出示例：**
```
[DATABASE] "连接数据库"   2025-11-20 21:30:15----code_context : ...
[API] "调用API"   2025-11-20 21:30:16----code_context : ...
[UI] "更新UI"   2025-11-20 21:30:17----code_context : ...
```

### 方式2: 使用枚举（推荐）

```python
from enum import Enum
import Lugwit_Module as LM
lprint = LM.lprint

class LogGroup(Enum):
    DATABASE = "DB"      # 使用 value 作为显示值
    API = "API"
    UI = "UI"
    CACHE = "CACHE"

lprint("查询用户数据", log_group=LogGroup.DATABASE)
lprint("缓存命中", log_group=LogGroup.CACHE)
```

**输出示例：**
```
[DB] "查询用户数据"   2025-11-20 21:30:15----code_context : ...
[CACHE] "缓存命中"   2025-11-20 21:30:16----code_context : ...
```

### 方式3: 项目自定义枚举

每个项目可以定义自己的日志分组枚举：

```python
# digital_workspace 项目的日志分组
class WorkspaceLogGroup(Enum):
    TASK_MANAGER = "任务管理"
    FILE_SYNC = "文件同步"
    SHOT_PROCESS = "镜头处理"
    UI_EVENT = "UI事件"

lprint("创建新任务", log_group=WorkspaceLogGroup.TASK_MANAGER)
lprint("同步文件", log_group=WorkspaceLogGroup.FILE_SYNC)
```

## 枚举支持说明

`_extract_log_group_string` 方法支持多种枚举类型：

1. **标准 Enum**（Python 3.4+）
   - 优先使用 `value` 属性（如果是字符串）
   - 否则使用 `name` 属性

2. **类枚举对象**
   - 任何具有 `value` 或 `name` 属性的对象

3. **兼容性**
   - Python 2: 使用字符串或类枚举对象
   - Python 3: 完全支持标准 Enum

## 日志过滤

### 使用 grep 过滤

```bash
# 查看所有数据库相关日志
grep "\[DB\]" digital_workspace_main.log

# 查看所有API相关日志
grep "\[API\]" digital_workspace_main.log

# 同时查看多个分组
grep -E "\[DB\]|\[API\]" digital_workspace_main.log
```

### 使用 Python 过滤

```python
# 读取并过滤特定分组的日志
with open('digital_workspace_main.log', 'r', encoding='utf-8') as f:
    db_logs = [line for line in f if '[DB]' in line]
    
for log in db_logs:
    print(log)
```

## 性能说明

| 操作 | 开销 | 说明 |
|------|------|------|
| 不使用 log_group | 0 | 无任何额外开销 |
| 使用字符串 | ~0 | 只是字符串拼接 |
| 使用枚举 | ~0 | 属性访问 + 字符串拼接 |

**结论**：性能开销可忽略不计（< 1微秒）

## 最佳实践

### ✅ 推荐做法

1. **使用枚举定义分组**
   ```python
   class LogGroup(Enum):
       DATABASE = "DB"
       API = "API"
   ```
   - 优点：类型安全、自动补全、避免拼写错误

2. **分组名称简短**
   ```python
   DATABASE = "DB"  # ✅ 简短
   DATABASE = "DATABASE_OPERATIONS"  # ❌ 太长
   ```

3. **按功能模块分组**
   ```python
   class LogGroup(Enum):
       DB = "DB"           # 数据库
       API = "API"         # 外部API
       UI = "UI"           # 用户界面
       CACHE = "CACHE"     # 缓存
       TASK = "TASK"       # 任务管理
   ```

### ❌ 避免的做法

1. **不要过度细分**
   ```python
   # ❌ 分组太多，失去意义
   class LogGroup(Enum):
       DB_SELECT = "DB_SELECT"
       DB_INSERT = "DB_INSERT"
       DB_UPDATE = "DB_UPDATE"
       # ... 太多了
   ```

2. **不要使用中文作为枚举名**
   ```python
   # ❌ 枚举名使用中文
   class LogGroup(Enum):
       数据库 = "DB"  # 不推荐
   
   # ✅ 枚举名用英文，value 可以用中文
   class LogGroup(Enum):
       DATABASE = "数据库"  # 推荐
   ```

## 实际应用示例

### 示例1: 数据处理流程

```python
from enum import Enum
import Lugwit_Module as LM
lprint = LM.lprint

class LogGroup(Enum):
    DB = "DB"
    API = "API"
    CACHE = "CACHE"

def process_data():
    lprint("开始读取数据", log_group=LogGroup.DB)
    # ... 数据库操作
    
    lprint("调用清洗API", log_group=LogGroup.API)
    # ... API调用
    
    lprint("缓存结果", log_group=LogGroup.CACHE)
    # ... 缓存操作
    
    lprint("处理完成", log_group=LogGroup.DB)
```

### 示例2: 异步任务管理

```python
class TaskLogGroup(Enum):
    TASK_CREATE = "任务创建"
    TASK_EXEC = "任务执行"
    TASK_COMPLETE = "任务完成"

async def execute_task(task_id):
    lprint(f"创建任务 {task_id}", log_group=TaskLogGroup.TASK_CREATE)
    
    lprint(f"执行任务 {task_id}", log_group=TaskLogGroup.TASK_EXEC)
    # ... 执行逻辑
    
    lprint(f"任务完成 {task_id}", log_group=TaskLogGroup.TASK_COMPLETE)
```

## 与现有功能的兼容性

`log_group` 可以与其他 lprint 参数组合使用：

```python
# 组合使用多个参数
lprint("重要的数据库操作", 
       log_group=LogGroup.DATABASE,
       level=logging.WARNING,
       trace_depth=2,
       max_length=1000)
```

## 总结

- ✅ **简单易用**：只需添加一个参数
- ✅ **灵活强大**：支持字符串和任意枚举
- ✅ **性能优秀**：几乎零开销
- ✅ **向后兼容**：不影响现有代码
- ✅ **便于维护**：使用枚举避免拼写错误

---

**相关文件：**
- 实现代码：`usualFunc.py` 中的 `_extract_log_group_string` 和 `_format_log_message` 方法
- 使用示例：`examples/log_group_example.py`
