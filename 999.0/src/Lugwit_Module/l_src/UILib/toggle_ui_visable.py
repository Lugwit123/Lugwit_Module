import win32gui
import win32con
import win32process
import psutil
import ctypes
import sys
import os

print("........................",ctypes)
sys.path.append(os.path.dirname(__file__))
import wintypes
import time
from win32con import SWP_NOMOVE 
from win32con import SWP_NOSIZE 
from win32con import SW_HIDE
from win32con import SW_SHOW
from win32con import SWP_NOZORDER
from win32con import  SWP_FRAMECHANGED
from win32con import HWND_NOTOPMOST
from win32con import SWP_HIDEWINDOW
from win32con import SWP_NOMOVE
from win32con import SWP_NOSIZE
from win32con import SWP_NOACTIVATE

# Shell API 常量 - 用于处理通知区域图标
NIM_DELETE = 0x00000002
NIM_ADD = 0x00000000
NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004

# 加载 DLL
user32 = ctypes.WinDLL('user32', use_last_error=True)
shell32 = ctypes.WinDLL('shell32', use_last_error=True)

# 定义 NOTIFYICONDATA 结构体
class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("hWnd", wintypes.HWND),
        ("uID", ctypes.c_uint),
        ("uFlags", ctypes.c_uint),
        ("uCallbackMessage", ctypes.c_uint),
        ("hIcon", wintypes.HANDLE),
        ("szTip", ctypes.c_wchar * 128),
        ("dwState", ctypes.c_uint),
        ("dwStateMask", ctypes.c_uint),
        ("szInfo", ctypes.c_wchar * 256),
        ("uVersion", ctypes.c_uint),
        ("szInfoTitle", ctypes.c_wchar * 64),
        ("dwInfoFlags", ctypes.c_uint),
        ("guidItem", ctypes.c_char * 16),
        ("hBalloonIcon", wintypes.HANDLE),
    ]

# 设置 Shell_NotifyIcon 函数参数类型和返回类型
Shell_NotifyIcon = shell32.Shell_NotifyIconW
Shell_NotifyIcon.argtypes = [ctypes.c_uint, ctypes.POINTER(NOTIFYICONDATA)]
Shell_NotifyIcon.restype = wintypes.BOOL


def find_window_by_title(titleList=[]):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            if titleList and len(titleList) > 0 and titleList[0] in win32gui.GetWindowText(hwnd):
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    print("hwnds", hwnds, titleList[0] if titleList and len(titleList) > 0 else "无标题")
    if hwnds:
        return hwnds[0]
    else:
        return None
        
def is_window_visible(hwnd):
    # 获取窗口样式
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    # 检查WS_VISIBLE标志
    return (style & win32con.WS_VISIBLE) != 0


# 查找并移除托盘图标
def remove_tray_icon(hwnd):
    """尝试移除与指定窗口关联的托盘图标"""
    # 创建 NOTIFYICONDATA 结构
    nid = NOTIFYICONDATA()
    nid.cbSize = ctypes.sizeof(nid)
    nid.hWnd = hwnd
    nid.uID = 1  # 默认ID为1，可能需要尝试其他ID
    Shell_NotifyIcon(NIM_DELETE, ctypes.byref(nid))
    
    # 尝试其他可能的ID
    for uid in range(2, 10):
        nid.uID = uid
        Shell_NotifyIcon(NIM_DELETE, ctypes.byref(nid))
    
    print(f"已尝试移除窗口 {hwnd} 的托盘图标")


def hide_window_completely(window_class=None, window_title=None):
    """完全隐藏窗口并移除托盘图标"""
    # 查找窗口
    hwnd = None
    if window_title:
        hwnd = find_window_by_title([window_title])
    elif window_class:
        hwnd = win32gui.FindWindow(window_class, None)
    
    if hwnd:
        # 隐藏窗口
        win32gui.ShowWindow(hwnd, SW_HIDE)
        win32gui.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0,
                    SWP_HIDEWINDOW | SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)
        
        # 尝试移除托盘图标
        remove_tray_icon(hwnd)
        
        print(f"成功完全隐藏窗口，句柄: {hwnd}")
        return hwnd
    else:
        print("未找到指定窗口")
        return None


def hide_window_by_hwnd(hwnd):
    """通过句柄完全隐藏窗口并移除托盘图标"""
    if hwnd:
        win32gui.ShowWindow(hwnd, SW_HIDE)
        win32gui.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0,
                    SWP_HIDEWINDOW | SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)
        remove_tray_icon(hwnd)
        print(f"成功完全隐藏窗口句柄: {hwnd}")
        return True
    else:
        print("无效的窗口句柄")
        return False


def hide_taskbar_icon(titleList=[u"管理员: 0lugwit_insapp (Admin)"]):
    # 获取控制台窗口句柄
    # 支持尝试过通过cpython的控制台窗口查找窗口句柄的,但是找到的是cmd.exe
    # win11的窗口确实window teriminal,所以放弃了这个办法,改用标题查找
    hwnd = find_window_by_title(titleList)
    if not hwnd:
        return
    
    # 使用增强的隐藏方法
    return hide_window_by_hwnd(hwnd)


def toggle_win_vis_by_hwnd(hwnd:int):
    print("locals",locals())
    if not hwnd:
        return
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    is_vis= is_window_visible(hwnd)
    print("is_vis",is_vis)
    if is_vis:
        style &= ~win32con.WS_VISIBLE
        win32gui.ShowWindow(hwnd, SW_HIDE)
        win32gui.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0,
        SWP_HIDEWINDOW | SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)
        # 同时移除托盘图标
        remove_tray_icon(hwnd)
    else:
        style |= win32con.WS_VISIBLE
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
        
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
    win32gui.UpdateWindow(hwnd)
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    return is_vis

def get_grandparent_window_info():
    """获取祖父进程的窗口句柄和名称（仅适用于 Windows）。"""
    try:
        current_process = psutil.Process(os.getpid())
        parent_process = current_process.parent()
        if parent_process:
            grandparent_process = parent_process.parent()
            if grandparent_process:
                grandparent_pid = grandparent_process.pid
                grandparent_name = grandparent_process.name()

                # 获取祖父进程的所有顶级窗口句柄
                def callback(hwnd, hwnds):
                    if win32gui.IsWindowVisible(hwnd) and win32gui.GetParent(hwnd) == 0:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        if pid == grandparent_pid:
                            hwnds.append(hwnd)
                    return True

                hwnds = []
                win32gui.EnumWindows(callback, hwnds)

                if hwnds:
                    hwnd = hwnds[0]  # 获取第一个顶级窗口句柄
                    return hwnd, grandparent_name
                else:
                    return None, grandparent_name  # 未找到窗口句柄
            else:
                return None, None #未找到祖父进程
        else:
            return None, None #未找到父进程

    except psutil.NoSuchProcess:
        return None, None

if __name__ == "__main__":
    # 测试代码
    # 方法1：通过窗口标题隐藏
    # hide_window_completely(window_title="管理员: 0lugwit_insapp (Admin)")
    
    # 方法2：通过句柄隐藏
    toggle_win_vis_by_hwnd(264712132)
