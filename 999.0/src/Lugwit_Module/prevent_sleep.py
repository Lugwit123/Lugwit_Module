# -*- coding: utf-8 -*-
"""
防止电脑休眠的 Python 脚本
使用 Windows API SetThreadExecutionState 来防止系统进入休眠状态
"""
import ctypes
import sys
import time

# Windows API 常量
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
ES_AWAYMODE_REQUIRED = 0x00000040

class PreventSleep:
    """防止系统休眠的类"""
    
    def __init__(self):
        """初始化，加载 Windows API"""
        try:
            # 加载 kernel32.dll
            self.kernel32 = ctypes.windll.kernel32
            self._is_active = False
        except Exception as e:
            print(u"初始化失败: {}".format(e))
            sys.exit(1)
    
    def prevent_sleep(self, keep_display_on=True):
        """
        防止系统休眠
        
        Args:
            keep_display_on (bool): 是否保持显示器开启，默认为 True
        """
        try:
            flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
            if keep_display_on:
                flags |= ES_DISPLAY_REQUIRED
            
            # 调用 SetThreadExecutionState API
            result = self.kernel32.SetThreadExecutionState(flags)
            if result:
                self._is_active = True
                print(u"✅ 已启用：防止系统休眠{}".format("（保持显示器开启）" if keep_display_on else ""))
                return True
            else:
                print(u"❌ 设置失败")
                return False
        except Exception as e:
            print(u"防止休眠失败: {}".format(e))
            return False
    
    def allow_sleep(self):
        """允许系统正常休眠"""
        try:
            # 清除执行状态标志
            result = self.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            if result:
                self._is_active = False
                print(u"✅ 已禁用：允许系统正常休眠")
                return True
            else:
                print(u"❌ 清除失败")
                return False
        except Exception as e:
            print(u"允许休眠失败: {}".format(e))
            return False
    
    def is_active(self):
        """检查是否正在防止休眠"""
        return self._is_active
    
    def __enter__(self):
        """上下文管理器入口"""
        self.prevent_sleep()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口，自动恢复"""
        self.allow_sleep()


def main():
    """主函数 - 示例用法"""
    print(u"=" * 50)
    print(u"防止电脑休眠工具")
    print(u"=" * 50)
    print()
    
    # 方式1: 使用上下文管理器（推荐）
    print(u"方式1: 使用上下文管理器（推荐）")
    with PreventSleep() as ps:
        print(u"系统将不会休眠，按 Ctrl+C 退出...")
        try:
            while True:
                time.sleep(1)
                # 可以在这里执行需要防止休眠的任务
        except KeyboardInterrupt:
            print(u"\n收到退出信号...")
    # 退出上下文管理器时自动恢复
    
    print()
    print(u"=" * 50)
    print()
    
    # 方式2: 手动控制
    print(u"方式2: 手动控制")
    ps = PreventSleep()
    ps.prevent_sleep(keep_display_on=True)
    
    try:
        print(u"系统将不会休眠，按 Ctrl+C 退出...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(u"\n收到退出信号...")
    finally:
        ps.allow_sleep()
    
    print(u"\n程序结束")


if __name__ == "__main__":
    main()
