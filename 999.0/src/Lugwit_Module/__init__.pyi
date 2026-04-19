from typing import Callable, Literal, Union, Optional, List, Dict, Any, TypedDict
import logging

# 日志文件信息结构
class LogFileInfo(TypedDict, total=False):
    enabled: bool
    interval: int
    file_path: Optional[str]
    buffer_count: int
    file_exists: bool
    base_dir: str
    file_size: int
    last_modified: str

# 字符串路径相关
Lugwit_mayaPluginPath: str = ""
Lugwit_publicPath: str = ""
Lugwit_publicDisc: str = ""
LugwitAppDir: str = r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp"
LugwitPath: str = ""
TempDir: str = ""
hostName: str = ""
oriEnvVarFile: str = ""
ProgramFilesLocal: str = r'$TD_DepotDir\Software\ProgramFilesLocal\Perforce'
ProgramFilesLocal_Public: str = ""
LugwitHoudiniPlugPath: str = ""
PythonLibDir_Public: str = ""
userName: str = ""
documentsPath: str = ""
NUKE_PATH: str = ""
LugwitLibDir: str = ""
LugwitToolDir: str = ""
lugwit_PluginPath: str = ""
plugDataDir_user: str = ""
ip: str = ""
localIP: str = ""
py_ver: str = ""
deadline_clientDir: str = ""
TD_DepotDir: str = ""
MayaPlugLogDir: str = ""
Maya_Py27LibDir: str = r"D:\TD_Depot\plug_in\python2_lib"

# 如何让编辑器能提示maya_thumb_dir的默认值
maya_thumb_dir: Literal[r"D:\TD_Depot\Temp\maya_thumb_file"] = r"D:\TD_Depot\Temp\maya_thumb_file"

# 环境检测
MayaExecutable: bool = False
unrealExecutable: bool = False
sys_executable: str = ""
isMayaEnvValue: bool = False

class stackInfo:
    """调用栈信息类"""
    filename: str
    lineno: int
    func_name: str
    context: str
    
    def __init__(self, filename: str, lineno: int, func_name: str, context: str) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class LPrint:
    # 类属性（与 pytracemp LPrint / LogFileHandler 对齐）
    End: str
    _detailed_log_functions: List[str]
    line_print_counts_dict: Dict[str, int]
    max_prints_per_line: int
    max_log_lines: int
    enable_function_range_check: bool
    entry_module_name: Optional[str]
    debug_self_global: bool
    warning_plugin: Optional[Callable]
    getframeMethod: str
    trace_max_result_per_function: Optional[int]
    trace_markdown_mode: bool
    trace_each_call: bool
    trace_skip_qt: bool
    trace_flush_interval: float
    logwgt_plugin: Optional[Any]
    logwgt_plugin_mode: str
    logwgt_plugin_level: int
    logwgt_plugin_accumulated_content: str

    # 实例属性
    debug_mode: Optional[Union[str, bool]]  # 调试模式设置（使用 debug_mode 避免与方法名 debug 冲突）
    trace_depth: int
    min_log_level: int
    log_func: Callable
    logger: logging.Logger

    # 日志文件相关属性（LogFileHandler）；trace_log_stem / log_file_basename 为追踪专用文件名（不含扩展名）
    trace_log_enable: bool
    log_file_interval: int
    log_base_dir: str
    trace_log_stem: Optional[str]
    log_file_basename: Optional[str]
    popui: bool
    log_width: int
    items: List[Any]
    shift_frame: Optional[Any]
    lshift: int
    last_lshift: int
    
    gui_widget_method: Optional[Callable]
    
    def __init__(self, popui: bool = False, log_width: int = 2) -> None: ...
    
    def __call__(
        self, 
        *args: Any, 
        trace_depth: Optional[int] = None,
        force_print: bool = False,
        max_length: Optional[int] = None,
        level: Union[int, str, Callable] = logging.WARNING,
        log_group: Union[str, Any] = None,
        show_all_frame: bool = False,
        popui: bool = False,
        debug_self: Optional[bool] = None,
        oneLine: bool = False,
        **kwargs: Any
    ) -> Optional[str]: ...
    
    def debug(self, *args: Any, **kwargs: Any) -> Optional[str]: ...
    def info(self, *args: Any, **kwargs: Any) -> Optional[str]: ...
    def warning(self, *args: Any, **kwargs: Any) -> Optional[str]: ...
    def error(self, *args: Any, **kwargs: Any) -> Optional[str]: ...
    def critical(self, *args: Any, **kwargs: Any) -> Optional[str]: ...
    
    def __lshift__(self, other: Any) -> 'LPrint': ...
    
    def flush(self) -> None: ...
    
    def set_min_log_level(self, level: Union[int, str]) -> int: ...
    
    def set_log_output_wgt(self, widget_method: Callable, log_level: Optional[int] = None, auto_test: bool = True) -> bool: ...
    
    def _debug_self_print(self, message: str) -> None: ...
    
    def _get_caller_debug_info(self, args: tuple) -> str: ...
    
    def _safe_unicode_args(self, args: tuple) -> tuple: ...
    
    def _format_log_message(self, *args, **kwargs) -> Optional[str]: ...
    
    def _check_call_stack(self) -> bool: ...
    
    def _get_level_name(self, level: int) -> str: ...
    
    def _run_connection_test(self, widget_method: Callable, method_name: str, level_name: str, log_level: Optional[int]) -> None: ...
    
    @staticmethod
    def _is_function_match(function_name: str, module_name: str, pattern: str) -> bool: ...
    
    @classmethod
    def get_detailed_log_functions(cls) -> List[str]: ...
    
    @classmethod
    def set_detailed_log_functions(cls, value: List[str]) -> None: ...
    
    @staticmethod
    def reset_line_counts() -> None: ...
    
    @staticmethod
    def set_function_range_check(enable: bool = True) -> None: ...
    
    @staticmethod
    def set_debug_self_global(enable: bool) -> None: ...
    
    @staticmethod
    def get_debug_self_status() -> Dict[str, Any]: ...
    
    @classmethod
    def register_warning_plugin(cls, plugin_func: Callable) -> None: ...
    
    @classmethod
    def unregister_warning_plugin(cls) -> None: ...
    
    @classmethod
    def get_warning_plugin_info(cls) -> Dict[str, Any]: ...

    # 日志组件插件（输出到 UI 等）
    @classmethod
    def register_logwgt_plugin(
        cls,
        plugin_func: Callable[[str], None],
        mode: Literal["append", "set"] = "append",
        level: int = 30,  # logging.WARNING
    ) -> bool: ...

    @classmethod
    def unregister_logwgt_plugin(cls) -> bool: ...

    @classmethod
    def clear_logwgt_plugin_content(cls) -> None: ...

    @classmethod
    def get_logwgt_plugin_info(cls) -> Dict[str, Any]: ...

    # 日志文件相关方法
    def save_logs_to_file(self) -> bool: ...

    def clear_log_file(self) -> bool: ...

    def get_log_file_info(self) -> LogFileInfo: ...

    @classmethod
    def write_trace_file_content(cls, content: str) -> bool: ...

    @staticmethod
    def with_end(func: Optional[Callable] = None, **kwargs) -> Callable: ...
    
    # 向前追踪（ForwardTracer）
    @property
    def supports_multiprocess(self) -> bool: ...

    def trace_start_mp(
        self,
        timeout: Optional[float] = None,
        trace_depth: Optional[int] = None,
        shared_dir: Optional[str] = None,
        trace_skip_path_substrings: Optional[List[str]] = None,
        trace_skip_function_names: Optional[List[str]] = None,
        trace_each_call: Optional[bool] = None,
    ) -> bool: ...

    def trace_result_mp(
        self,
        max_events: Optional[int] = None,
        console_output: bool = True,
        announce_save: bool = True,
    ) -> Optional[str]: ...

    def trace_summary_mp(self) -> str: ...

    def trace_start(
        self,
        timeout: Optional[float] = None,
        trace_depth: Optional[int] = None,
        auto_result: bool = True,
        decorated_func_source: Optional[Any] = None,
        clear_log: bool = False,
        multiprocess: bool = False,
        trace_skip_path_substrings: Optional[List[str]] = None,
        trace_skip_function_names: Optional[List[str]] = None,
        trace_each_call: Optional[bool] = None,
    ) -> bool: ...

    def trace_stop(self) -> int: ...

    def trace_result(
        self,
        max_events: int = 50,
        console_output: bool = False,
        announce_save: bool = True,
    ) -> None: ...

    def trace_summary(
        self, console_output: bool = False, announce_save: bool = True
    ) -> None: ...

    def trace_get_data(self) -> List[Dict[str, Any]]: ...

    @classmethod
    def trace_cleanup(cls) -> None: ...

    def trace(
        self,
        func: Optional[Callable[..., Any]] = None,
        *,
        timeout: Optional[float] = None,
        trace_depth: Optional[int] = None,
        clear_log: bool = False,
    ) -> Any: ...

# 函数类型
lprint: LPrint  # 打印函数实例

# 环境检测函数
isMayaEnv: Callable[[], Any]  # 判断是否在Maya环境中（返回match对象或None）
isMayaPyEnv: Callable[[], Any]  # 判断是否在MayaPy环境中（返回match对象或None）

# 工具函数
def get_module_name() -> str: ...
"""获取当前模块的名称"""

def getframeinfo_wrapper(frame: Any, context: int = 1) -> Any: ...
"""包装inspect.getframeinfo，支持自定义context"""

def dynamic_import(module_path: Optional[str] = None, dont_write_bytecode: bool = True) -> Any: ...
"""动态导入模块"""

def getFileModifyTime(file_path: str = "") -> Optional[str]: ...
"""获取文件的修改时间，返回格式化的日期字符串"""

def compare_dates(date_str1: str, date_str2: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> Optional[int]: ...
"""比较两个日期字符串，返回1/0/-1或None"""

def get_dict_nested_value(dictionary: Dict[str, Any], keys: List[str]) -> Optional[Any]: ...
"""获取嵌套字典中的值"""

def get_keys_by_value(dict_: Dict[str, Any], value_to_find: Any) -> List[str]: ...
"""根据值获取所有对应的键"""

def with_lprint_end(_func: Optional[Callable] = None, **kwargs: Any) -> Callable: ...
"""装饰器：函数结束后处理 lprint 缓冲"""

def lprint_info() -> None: ...
"""显示系统编码信息"""

# 从 main 模块导入的函数和变量
def is_main() -> bool: ...
"""判断调用该函数的模块是否是主模块"""

def getCurrentTimeAsLogName() -> str: ...
"""获取当前时间作为日志文件名"""

def try_exp(func: Callable) -> Callable: ...
"""装饰器：异常捕捉"""

username: str
getCurDir: Callable[[], str]  # 获取当前目录（如果存在）

# Literal 字面量类型
PythonPackageDir: Literal['D:\\TD_Depot\\plug_in\\Python'] = 'D:\\TD_Depot\\plug_in\\Python'
userConfigFile: Literal["C:\\Users\\qqfeng\\.Lugwit\\config\\config.json"] = "C:\\Users\\qqfeng\\.Lugwit\\config\\config.json"

# 其他变量
oriEnvVar: Dict[str, str]
perforceInsDir: str
Lugwit_UnrealPlugDir: str
lfileSystem: Any  # FileSystem 类实例（如果存在）