# PySide6 + @lprint.trace 演示程序

## 安装依赖

```bash
pip install PySide6
```

## 运行程序

```bash
python test_pyside6_trace.py
```

## 功能说明

这个演示程序展示了如何在 PySide6 GUI 应用中使用 `@lprint.trace` 装饰器：

### 界面功能（演示 3 种连接方式）

#### 方式 1：直接连接被装饰的方法
```python
@lprint.trace(trace_depth=3)
def simple_calculation_direct(self):
    # 槽函数本身被装饰
    ...

self.btn_simple.clicked.connect(self.simple_calculation_direct)
```

#### 方式 2：通过中间处理函数连接
```python
def on_complex_click(self):
    # 中间处理函数（更新 UI）
    result = self.complex_calculation(self.click_count)  # 调用被装饰的方法
    ...

@lprint.trace(trace_depth=4)
def complex_calculation(self, n):
    # 被装饰的方法
    ...

self.btn_complex.clicked.connect(self.on_complex_click)
```

#### 方式 3：使用 lambda 传递参数
```python
@lprint.trace(trace_depth=3)
def simple_calculation_with_param(self, multiplier):
    # 接受参数的被装饰方法
    ...

self.btn_lambda.clicked.connect(lambda: self.simple_calculation_with_param(20))
```

**三个按钮分别演示：**
- **简单计算（直接连接）** - 方式 1
- **复杂计算（中间处理）** - 方式 2（4层调用栈）
- **Lambda 连接（参数x2）** - 方式 3

### 追踪效果

点击按钮后，日志文件会记录：
- ✅ 完整的函数调用链（深度 1→2→3→4）
- ✅ 每行代码执行后的局部变量及类型
- ✅ 函数返回值
- ✅ 总耗时

### 日志位置

日志文件保存在：`logs/test_pyside6_trace/YYYYMMDD.log`

## 如果没有 PySide6

可以使用 `test_lprint.py`（命令行版本）来测试 `@lprint.trace` 功能：

```bash
python test_lprint.py
```

该脚本演示了相同的追踪功能，但不需要 GUI 库。
