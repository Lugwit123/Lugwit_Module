# -*- coding: utf-8 -*-
# Rez root = this directory (…/Lugwit_Module/999.0). Python package lives under src/Lugwit_Module.

name = "Lugwit_Module"
version = "999.0"
description = (
    "Lugwit Module - CG pipeline Python utilities (logging, env detection, cross-app support)"
)
authors = ["Lugwit Team"]

requires = ["python-3.7+","pytracemp"]


def commands():
    import os
    import textwrap

    env.PYTHONPATH.append("{root}/src")

    auto_import = os.environ.get("LUGWIT_AUTO_IMPORT", "true").lower() in (
        "true",
        "1",
        "yes",
    )
    debug_mode = os.environ.get("LUGWIT_DEBUG", "true").lower() in (
        "true",
        "1",
        "yes",
    )
    verbose_mode = os.environ.get("LUGWIT_VERBOSE", "false").lower() in (
        "true",
        "1",
        "yes",
    )
    log_level = os.environ.get("LUGWIT_LOG_LEVEL", "INFO")

    if auto_import:
        startup_script = textwrap.dedent(
            """\
            # -*- coding: utf-8 -*-
            import os

            debug_mode = os.environ.get("LUGWIT_DEBUG", "false").lower() in ("true", "1", "yes")
            verbose_mode = os.environ.get("LUGWIT_VERBOSE", "false").lower() in ("true", "1", "yes")
            log_level = os.environ.get("LUGWIT_LOG_LEVEL", "INFO")

            try:
                import Lugwit_Module as LM

                if verbose_mode or debug_mode:
                    print("✅ Lugwit_Module 已自动导入")
                    print(f"🔧 调试模式: {debug_mode}")
                    print(f"📊 日志级别: {log_level}")
                    print("📦 可用功能: Lugwit_Module.lprint, Lugwit_Module.isMayaEnv, 等")

                if log_level == "DEBUG":
                    LM.lprint("🐛 Lugwit_Module 调试模式已启用")
                elif log_level == "VERBOSE":
                    LM.lprint("📢 Lugwit_Module 详细模式已启用")

            except ImportError as e:
                print(f"❌ 导入 Lugwit_Module 失败: {e}")
            """
        )
        startup_file = os.path.join(os.environ.get("TEMP", "C:\\temp"), "lugwit_startup.py")
        with open(startup_file, "w", encoding="utf-8") as f:
            f.write(startup_script)
        env.PYTHONSTARTUP = startup_file

    if debug_mode or verbose_mode:
        print("DEBUG: root =", "{root}")
        print("DEBUG: cwd =", os.getcwd())
        print(f"DEBUG: auto_import = {auto_import}")
        print(f"DEBUG: debug_mode = {debug_mode}")
        print(f"DEBUG: verbose_mode = {verbose_mode}")
        print(f"DEBUG: log_level = {log_level}")
        if auto_import:
            print("DEBUG: PYTHONSTARTUP =", env.PYTHONSTARTUP)

    env.LUGWIT_MODULE_ROOT = "{root}/src/Lugwit_Module"
    env.LUGWIT_DEBUG = str(debug_mode).lower()
    env.LUGWIT_VERBOSE = str(verbose_mode).lower()
    env.LUGWIT_LOG_LEVEL = log_level

    if os.environ.get("MAYA_LOCATION"):
        maya_lib = "{root}/src/Lugwit_Module/l_src/l_MayaLib"
        env.MAYA_SCRIPT_PATH.append(maya_lib)
        env.PYTHONPATH.append(maya_lib)


build_command = False
cachable = True
relocatable = True
