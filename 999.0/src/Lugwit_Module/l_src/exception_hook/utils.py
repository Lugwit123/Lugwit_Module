"""
异常钩子工具函数
"""

import os
import logging
import traceback
from datetime import datetime

def setup_exception_logger(log_file=None):
    """
    设置异常日志记录器
    :param log_file: 日志文件路径，如果为None则使用默认路径
    """
    if log_file is None:
        log_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'exception_{datetime.now().strftime("%Y%m%d")}.log')
    
    # 配置日志
    logger = logging.getLogger('exception_hook')
    logger.setLevel(logging.ERROR)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.ERROR)
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # 添加处理器
    if not logger.handlers:
        logger.addHandler(file_handler)
    
    return logger

def log_exception(exc_type, exc_value, exc_traceback, logger=None):
    """
    记录异常到日志文件
    :param exc_type: 异常类型
    :param exc_value: 异常值
    :param exc_traceback: 异常回溯
    :param logger: 日志记录器
    """
    if logger is None:
        logger = setup_exception_logger()
    
    # 格式化异常信息
    exc_info = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    # 记录到日志
    logger.error(f"异常类型: {exc_type.__name__}")
    logger.error(f"异常信息: {exc_value}")
    logger.error(f"异常回溯:\n{exc_info}")

def get_exception_summary(exc_type, exc_value, exc_traceback):
    """
    获取异常摘要信息
    :param exc_type: 异常类型
    :param exc_value: 异常值
    :param exc_traceback: 异常回溯
    :return: 异常摘要字典
    """
    import traceback
    
    # 提取关键信息
    tb_list = traceback.extract_tb(exc_traceback)
    
    summary = {
        'type': exc_type.__name__,
        'message': str(exc_value),
        'timestamp': datetime.now().isoformat(),
        'call_stack': []
    }
    
    # 提取调用栈
    for filename, lineno, func_name, text in reversed(tb_list):
        summary['call_stack'].append({
            'function': func_name,
            'file': os.path.basename(filename),
            'line': lineno,
            'code': text.strip() if text else ''
        })
    
    return summary

def is_important_exception(exc_type):
    """
    判断是否为重要异常（需要特别关注的异常）
    :param exc_type: 异常类型
    :return: bool
    """
    important_exceptions = [
        'AttributeError',
        'ImportError', 
        'ModuleNotFoundError',
        'KeyError',
        'TypeError',
        'ValueError',
        'NameError',
        'UnboundLocalError'
    ]
    
    return exc_type.__name__ in important_exceptions

def format_exception_for_report(exc_type, exc_value, exc_traceback):
    """
    格式化异常为报告格式
    :param exc_type: 异常类型
    :param exc_value: 异常值
    :param exc_traceback: 异常回溯
    :return: 格式化的报告字符串
    """
    summary = get_exception_summary(exc_type, exc_value, exc_traceback)
    
    report = []
    report.append("=" * 60)
    report.append("异常报告")
    report.append("=" * 60)
    report.append(f"时间: {summary['timestamp']}")
    report.append(f"类型: {summary['type']}")
    report.append(f"消息: {summary['message']}")
    report.append("")
    
    report.append("调用栈:")
    for i, frame in enumerate(summary['call_stack'][:10]):  # 最多显示10层
        report.append(f"  {i+1}. {frame['function']} ({frame['file']}:{frame['line']})")
        if frame['code']:
            report.append(f"     代码: {frame['code']}")
    
    if len(summary['call_stack']) > 10:
        report.append(f"  ... 还有 {len(summary['call_stack']) - 10} 层调用")
    
    return "\n".join(report)
