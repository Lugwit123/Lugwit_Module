# -*- coding: utf-8 -*-
"""PySide6 测试程序：演示 @lprint.trace 装饰器追踪按钮事件"""
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import Qt

# 添加 lprint 路径
sys.path.insert(0, os.path.dirname(__file__))
from usualFunc import lprint

# 配置日志输出到文件
lprint.trace_log_enable = True
lprint.log_base_dir = os.path.join(os.path.dirname(__file__), "logs")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LPrint Trace 演示")
        self.setGeometry(100, 100, 600, 400)
        
        # 中心窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 标题
        title_label = QLabel("点击按钮触发被 @lprint.trace 装饰的函数")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 计数器显示
        self.counter_label = QLabel("点击次数: 0")
        self.counter_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.counter_label)
        
        # 结果显示
        self.result_label = QLabel("结果: -")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        # 按钮 - 方式1：直接连接被装饰的方法
        self.btn_simple = QPushButton("简单计算（直接连接）")
        self.btn_simple.clicked.connect(self.simple_calculation_direct)
        layout.addWidget(self.btn_simple)
        
        # 按钮 - 方式2：通过中间处理函数连接
        self.btn_complex = QPushButton("复杂计算（中间处理）")
        self.btn_complex.clicked.connect(self.on_complex_click)
        layout.addWidget(self.btn_complex)
        
        # 按钮 - 方式3：带参数的直接连接（使用 lambda）
        self.btn_lambda = QPushButton("Lambda 连接（参数x2）")
        self.btn_lambda.clicked.connect(lambda: self.simple_calculation_with_param(20))
        layout.addWidget(self.btn_lambda)
        
        # 日志路径显示
        log_info = lprint.get_log_file_info()
        log_path_label = QLabel(f"日志路径: {log_info.get('file_path', '未设置')}")
        log_path_label.setWordWrap(True)
        layout.addWidget(log_path_label)
        
        # 计数器
        self.click_count = 0
        
        lprint("PySide6 应用启动")
    
    # ========== 方式1：直接连接到被 @lprint.trace 装饰的方法 ==========
    @lprint.trace(trace_depth=3)
    def simple_calculation_direct(self):
        """直接作为槽函数，无需中间处理函数"""
        self.click_count += 1
        self.counter_label.setText(f"点击次数: {self.click_count}")
        lprint("simple_calculation_direct 被调用，次数: {}", self.click_count)
        
        result = self.add(self.click_count, 10)
        result = self.multiply(result, 2)
        
        self.result_label.setText(f"结果: {result}")
        return result
    
    # ========== 方式2：通过中间处理函数连接 ==========
    def on_complex_click(self):
        """中间处理函数：更新计数器，然后调用被装饰的方法"""
        self.click_count += 1
        self.counter_label.setText(f"点击次数: {self.click_count}")
        lprint("复杂按钮被点击，次数: {}", self.click_count)
        
        # 调用被装饰的函数
        result = self.complex_calculation(self.click_count)
        self.result_label.setText(f"结果: {result}")
    
    @lprint.trace(trace_depth=4)
    def complex_calculation(self, n):
        """复杂计算：被 @lprint.trace 装饰，深度4，多层嵌套"""
        lprint("complex_calculation 被调用，参数 n={}", n)
        result = self.process_data(n)
        return result
    
    # ========== 方式3：带参数的装饰方法（通过 lambda 连接）==========
    @lprint.trace(trace_depth=3)
    def simple_calculation_with_param(self, multiplier):
        """接受参数的计算方法，通过 lambda 传递固定参数"""
        lprint("simple_calculation_with_param 被调用，multiplier={}", multiplier)
        
        result = self.add(self.click_count, multiplier)
        result = self.multiply(result, 2)
        
        self.result_label.setText(f"结果(x{multiplier}): {result}")
        return result
    
    def add(self, a, b):
        """深度2：加法"""
        result = a + b
        lprint("add({}, {}) = {}", a, b, result)
        return result
    
    def multiply(self, a, b):
        """深度2：乘法"""
        result = a * b
        lprint("multiply({}, {}) = {}", a, b, result)
        return result
    
    def process_data(self, n):
        """深度2：处理数据"""
        step1 = self.add(n, 5)
        step2 = self.multiply(step1, 3)
        step3 = self.format_output(step2)
        return step3
    
    def format_output(self, value):
        """深度3：格式化输出"""
        formatted = "计算结果: {}".format(value)
        return formatted


def main():
    lprint("程序开始")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    lprint("进入事件循环")
    exit_code = app.exec()
    
    lprint("程序退出，退出码: {}", exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
