"""
异常钩子模块 - 提供全局异常捕获和调用链回溯功能
"""

from .hook import (
    install_trace_hook,
    uninstall_trace_hook,
    is_hook_installed,
    get_hook_status,
    get_call_chain,
    format_call_chain
)

__all__ = [
    'install_trace_hook',
    'uninstall_trace_hook',
    'is_hook_installed',
    'get_hook_status',
    'get_call_chain',
    'format_call_chain'
]

# 版本信息
__version__ = '1.1.0'
__author__ = 'Lugwit Team'
__description__ = 'Global exception hook with call chain tracing and environment variable control'
