# Lugwit Module

一个功能强大的 Python 工具模块，专为 CG 制作流程设计，提供高级日志系统、环境检测和跨应用支持。

## 🚀 核心功能

### LPrint 高级日志系统
- **智能日志过滤**: 支持函数名和模块名的通配符匹配
- **多级别日志**: DEBUG、INFO、WARNING、ERROR、CRITICAL
- **文件日志**: 自动创建按日期命名的日志文件
- **UI集成**: 支持将日志输出到自定义 GUI 组件
- **性能监控**: 内置性能分析和函数调用统计
- **异常捕获**: `try_exp` 装饰器自动捕获并格式化异常信息

### 环境检测与适配
```python
# 检测运行环境
Lugwit_Module.isMayaEnv()        # Maya 环境
Lugwit_Module.isMayaPyEnv()      # Maya Python 环境
Lugwit_Module.isPy3()            # Python 3.x
Lugwit_Module.is_main()          # 是否为主模块
```

### 跨软件支持
- **Maya**: 完整的 Maya API 集成
- **Unreal Engine**: 支持 Unreal Editor 日志输出
- **Houdini**: Houdini 插件路径管理
- **Nuke**: NUKE_PATH 环境变量管理

## 📦 安装

### Rez 包管理器（推荐）
```bash
# 安装到本地 Rez 仓库
rez-build --install

# 在 Rez 环境中使用
rez-env lugwit_module -- python
```

## 🎯 使用示例

### 基础日志输出
```python
import Lugwit_Module

# 简单打印
Lugwit_Module.lprint("Hello, Lugwit!")

# 带级别的日志
Lugwit_Module.lprint.set_min_log_level("DEBUG")
Lugwit_Module.lprint("Debug message", level="debug")
```

### 异常处理装饰器
```python
@Lugwit_Module.try_exp
def risky_function():
    # 可能抛出异常的代码
    return some_operation()
```

---

**版本**: 1.0.0  
**最后更新**: 2025-01-09

## � Gitee 仓库

- 地址: https://gitee.com/lugwit123/Lugwit_Module
- 主分支: `main`
- 镜像/备份: 无

## 🔼 自动上传脚本（Gitee）

仓库中已添加一个方便的 Windows `.bat` 脚本用于将 `Lugwit_Module` 提交并推送到 Gitee（默认分支 `main`）：

- 文件: `upload_to_gitee.bat`
- 功能: 在脚本目录执行 `git add -A`、`git commit -m "..."`（可交互输入 commit message）并 `git push origin main`。
- 使用前提: 本地已安装 Git，且当前目录为 Git 仓库（已配置 `origin` 指向 Gitee）。

示例用法：

1. 双击 `upload_to_gitee.bat`（或在该目录 Powershell/命令提示符中运行）。
2. 当脚本要求输入 commit message 时输入描述（默认会使用预设消息）。
3. 脚本会自动 push 到 `origin/main`。

如果你希望脚本支持：
- 指定远端/分支、打包 Release、或使用 Gitee API 创建 Release，我可以把这些功能加入脚本。

