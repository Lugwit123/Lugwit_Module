# -*- coding: utf-8 -*-

# 声明这些变量存在（用于 Rez 运行时）
# 这些变量由 Rez 系统在运行时注入
import os,sys
name = "Lugwit_Module"

version = "999.0.0"

description = "Lugwit Module - 专为 CG 制作流程设计的 Python 工具模块，提供高级日志系统、环境检测和跨应用支持"

authors = ["Lugwit Team"]

# 使用更灵活的 Python 版本约束
requires = ["python-2.7|python-3.7+","pytracemp"]

@early()
def variants():
    # 根据系统动态生成变体
    return []
    # import platform
    # if platform.system() == "Windows":
    #     return [
    #         ["platform-windows", "python-2.7"],
    #         ["platform-windows", "python-3.7+"],
    #     ]
    # else:
    #     return []

def commands():
    import os
    import textwrap
    
    # 确保变体目录在 PYTHONPATH 中
    env.PYTHONPATH.append("{root}")
    
    # 添加 Lugwit_Module 的父目录（即变体目录本身）到 PYTHONPATH
    # 这样 Python 就能找到 Lugwit_Module 模块
    env.PYTHONPATH.append("{root}")
    
    # 根据环境变量设置启动脚本
    auto_import = env.get("LUGWIT_AUTO_IMPORT", "true").lower() in ("true", "1", "yes")
    debug_mode = env.get("LUGWIT_DEBUG", "true").lower() in ("true", "1", "yes")
    verbose_mode = env.get("LUGWIT_VERBOSE", "false").lower() in ("true", "1", "yes")
    log_level = env.get("LUGWIT_LOG_LEVEL", "INFO")
    
    if auto_import:
        # 设置 PYTHONSTARTUP，让 Python 启动时自动导入 Lugwit_Module
        startup_script = textwrap.dedent("""\
            # -*- coding: utf-8 -*-
            # Lugwit_Module 自动导入脚本
            import os
            
            # 获取环境变量
            debug_mode = os.environ.get("LUGWIT_DEBUG", "false").lower() in ("true", "1", "yes")
            verbose_mode = os.environ.get("LUGWIT_VERBOSE", "false").lower() in ("true", "1", "yes")
            log_level = os.environ.get("LUGWIT_LOG_LEVEL", "INFO")
            
            try:
                import Lugwit_Module as LM
                lprint = LM.lprint
                
                if verbose_mode or debug_mode:
                    print("✅ Lugwit_Module 已自动导入")
                    print(f"🔧 调试模式: {debug_mode}")
                    print(f"📊 日志级别: {log_level}")
                    print("📦 可用功能: Lugwit_Module.lprint, Lugwit_Module.isMayaEnv, 等")
                
                # 根据日志级别设置
                if log_level == "DEBUG":
                    LM.lprint("🐛 Lugwit_Module 调试模式已启用")
                elif log_level == "VERBOSE":
                    LM.lprint("📢 Lugwit_Module 详细模式已启用")
                    
            except ImportError as e:
                print(f"❌ 导入 Lugwit_Module 失败: {e}")
            """)
        
        # 将启动脚本写入临时文件
        startup_file = os.path.join(os.environ.get("TEMP", "C:\\temp"), "lugwit_startup.py")
        with open(startup_file, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        
        env.PYTHONSTARTUP = startup_file
    
    # 调试信息
    if debug_mode or verbose_mode:
        print("DEBUG: root =", "{root}")
        print("DEBUG: current working directory =", os.getcwd())
        print(f"DEBUG: auto_import = {auto_import}")
        print(f"DEBUG: debug_mode = {debug_mode}")
        print(f"DEBUG: verbose_mode = {verbose_mode}")
        print(f"DEBUG: log_level = {log_level}")
        if auto_import:
            print("DEBUG: PYTHONSTARTUP =", env.PYTHONSTARTUP)
    
    # 设置 Lugwit 相关环境变量
    env.LUGWIT_MODULE_ROOT = "{root}/Lugwit_Module"
    env.LUGWIT_DEBUG = str(debug_mode).lower()
    env.LUGWIT_VERBOSE = str(verbose_mode).lower()
    env.LUGWIT_LOG_LEVEL = log_level
    
    # 如果在 Maya 环境中，设置 Maya 相关路径
    if env.get("MAYA_LOCATION"):
        env.MAYA_SCRIPT_PATH.append("{root}/Lugwit_Module/l_src/l_MayaLib")
        env.PYTHONPATH.append("{root}/Lugwit_Module/l_src/l_MayaLib")

# 构建选项 - 使用自定义构建脚本复制文件
build_command = "python {root}/build.py"

# 构建参数
build_options = [
    {
        "name": "verbose", 
        "type": "bool",
        "default": False,
        "help": "Enable verbose build output"
    },
    {
        "name": "target_python",
        "type": "str", 
        "default": "all",
        "choices": ["all", "2.7", "3.7+"],
        "help": "Target Python version to build for"
    },
    {
        "name": "copy_maya_scripts",
        "type": "bool",
        "default": True, 
        "help": "Copy Maya-specific scripts"
    }
]

# 包的元数据
uuid = "lugwit-module-1.0.0"

# 标签
label = ["utility", "logging", "cg", "pipeline"]

# 主页
homepage = "https://github.com/Lugwit123/Lugwit_Module"

# 许可证
license = "Custom"



# 构建选项 - 使用自定义构建脚本
build_command = "python {root}/build.py"

cachable = True

relocatable = True

private_build_requires = []

@early()
def tools():
    return ["python"]
