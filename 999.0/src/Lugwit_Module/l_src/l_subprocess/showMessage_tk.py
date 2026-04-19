# -*- coding: utf-8 -*-

import os
import json
import threading
import time
import tkinter as tk
from tkinter import ttk
from queue import Queue, Empty
import subprocess
import sys
print(sys.version_info)
if sys.version_info.minor==7:
    sys.path.append(r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\py37\site_packages')
import psutil
from pathlib import Path
from save_message import save_message_to_file, load_log, save_log, initialize_log_file

# 配置日志文件路径和锁文件路径
LOG_FILE = r"D:\TD_Depot\Temp\message_log.json"
LOCK_FILE = LOG_FILE + ".lock"
CHECK_INTERVAL = 2  # 线程检查文件的时间间隔（秒）
LOCK_TIMEOUT = 5  # 文件锁等待超时时间（秒）

# 创建一个线程锁来确保线程安全
_file_lock = threading.Lock()

def get_log_file_path():
    """获取日志文件路径"""
    return str(Path("D:/TD_Depot/Temp/message_log.json"))

def is_process_running(process_name):
    """
    检查指定的进程名称是否正在运行。

    :param process_name: 要检查的进程名称 (例如 'pythonw_popui.exe')
    :return: 如果进程存在则返回 True，否则返回 False
    """
    try:
        for proc in psutil.process_iter():
            try:
                if proc.name() == process_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False
    except Exception as e:
        print(f"检查进程时出错: {e}")
        return False

def initialize_log_file():
    """
    初始化日志文件。如果文件不存在，创建包含'show'键为False和空消息列表的JSON。
    """
    print(u"正在初始化日志文件: {0}".format(LOG_FILE))
    if not os.path.exists(LOG_FILE):
        data = {
            "show": False,
            "messages": []
        }
        print(u"日志文件不存在，创建新文件")
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(u"成功创建日志文件: {0}".format(LOG_FILE))
        except Exception as e:
            print(u"创建日志文件时出错: {0}".format(e))
    else:
        print(u"日志文件已存在: {0}".format(LOG_FILE))

def atomic_write_log(data):
    """
    原子性地写入日志文件。先写入临时文件，然后重命名为目标文件。
    """
    temp_file = LOG_FILE + ".tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        os.replace(temp_file, LOG_FILE)
    except Exception as e:
        print(u"错误: 写入日志文件时发生异常: {0}".format(e))
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

def load_log():
    """加载日志文件，如果不存在则创建默认结构"""
    log_file = get_log_file_path()
    default_data = {"show": False, "messages": []}
    
    if not os.path.exists(log_file):
        return default_data
        
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default_data

def save_log(data):
    """保存日志到文件，确保线程安全"""
    log_file = get_log_file_path()
    with _file_lock:
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def check_and_set_show():
    """
    检查'show'键。如果为True，返回True表示已显示，程序应退出。
    否则，设置'show'为True，并返回False。
    """
    data = load_log()
    if not is_process_running('pythonw_popui.exe'):
        save_log(data)
        return False
    else:
        data["show"] = True
        save_log(data)
        return True

def set_show_flag(value):
    """
    设置'show'键的值。
    """
    data = load_log()
    data["show"] = value
    save_log(data)

def save_message_to_file(text):
    """
    保存消息到文件，最多存储 10 条，确保线程安全和原子性。
    """
    print(u"准备保存消息到文件: {0}".format(text))
    print(u"当前工作目录: {0}".format(os.getcwd()))
    print(u"日志文件路径: {0}".format(LOG_FILE))
    
    # 确保日志文件存在
    initialize_log_file()
    
    with _file_lock:
        try:
            data = load_log()
            messages = data.get("messages", [])
            print(u"当前消息数量: {0}".format(len(messages)))

            # 创建新的消息条目，确保message是列表
            if isinstance(text, str):
                text = [text]
            elif not isinstance(text, list):
                text = [str(text)]

            new_entry = {"id": len(messages) + 1, "message": text}
            messages.append(new_entry)
            print(u"添加新消息: {0}".format(new_entry))

            # 保持最多10条消息
            if len(messages) > 10:
                messages = messages[-10:]
                print("保留最新的10条消息")

            # 重新编号
            for idx, msg in enumerate(messages, start=1):
                msg["id"] = idx

            data["messages"] = messages
            atomic_write_log(data)
            print("消息保存成功")
        except Exception as e:
            print(u"保存消息时出错: {0}".format(e))

def load_messages():
    """
    从文件加载消息，确保线程安全。
    """
    data = load_log()
    messages = data.get("messages", [])
    print(u"成功加载 {0} 条消息。".format(len(messages)))
    return messages

def monitor_log(queue, stop_event):
    """
    监控日志文件的线程函数，定期读取最新消息并放入队列。
    """
    last_messages = []
    while not stop_event.is_set():
        data = load_log()
        messages = data.get("messages", [])
        if messages != last_messages:
            last_messages = messages
            queue.put(messages)
        time.sleep(CHECK_INTERVAL)

def create_control_panel(root, button_refs, selected_id, default_bg):
    """
    创建控制面板，包含搜索框和字体大小调节滑块
    """
    control_frame = ttk.Frame(root)
    control_frame.grid(row=2, column=0, sticky="ew", pady=(0, 5))

    # 搜索框
    search_frame = ttk.Frame(control_frame)
    search_frame.pack(side=tk.LEFT, padx=5)
    
    search_label = ttk.Label(search_frame, text="搜索:")
    search_label.pack(side=tk.LEFT, padx=(0, 5))
    
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    def search_text(*args):
        search_term = search_var.get().lower()
        for btn_id, btn in button_refs.items():
            if search_term and search_term in btn.cget('text').lower():
                btn.config(bg='yellow')  # 高亮匹配的按钮
            else:
                # 恢复原来的颜色
                if btn_id == selected_id[0]:
                    btn.config(bg="green")
                else:
                    btn.config(bg=default_bg)
    
    search_var.trace('w', search_text)  # 当搜索文本改变时触发搜索

    # 字体大小调节滑块
    font_frame = ttk.Frame(control_frame)
    font_frame.pack(side=tk.RIGHT, padx=5)
    
    font_label = ttk.Label(font_frame, text="字体大小:")
    font_label.pack(side=tk.LEFT, padx=(0, 5))
    
    font_size = tk.IntVar(value=10)  # 默认字体大小改为10
    font_size_label = ttk.Label(font_frame, textvariable=font_size, width=2)
    font_size_label.pack(side=tk.RIGHT, padx=(5, 0))
    
    def update_font_size(*args):
        size = font_size.get()
        # 更新所有按钮的字体大小
        for btn in button_refs.values():
            btn.config(font=('Consolas', size))
    
    font_slider = ttk.Scale(font_frame, from_=6, to=16, 
                          variable=font_size, 
                          orient=tk.HORIZONTAL,
                          command=update_font_size)
    font_slider.pack(side=tk.LEFT)
    
    return font_size  # 返回字体大小变量以供其他函数使用

def showMessageWin(text="", 
                  title='提示', 
                  fontName='Consolas', 
                  fontSize=10):
    if not text:
        text = '''程序崩溃，请联系开发人员
程序崩溃，请联系开发人员'''
        
    # 保存消息到文件
    if text!="None":
        save_message_to_file(text)
    messages = load_messages()

    # 创建主窗口
    root = tk.Tk()
    root.title(title)
    root.resizable(True, True)  # 允许窗口调整大小
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_ui.ico')
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)  # 传入图标文件的路径
    else:
        print("警告: 图标文件未找到，使用默认图标。")
    # 设置窗口大小并居中
    window_width = 1100
    window_height = 600  # 减小窗口高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # 设置主题（可选）
    style = ttk.Style()
    style.theme_use('clam')  # 可以尝试其他主题，如 'default', 'classic', 'clam', 'alt', 'vista', 'xpnative'

    # 队列用于线程间通信
    q = Queue()
    stop_event = threading.Event()

    # 启动监控线程
    thread = threading.Thread(target=monitor_log, args=(q, stop_event), daemon=True)
    thread.start()
    print("启动了日志监控线程。")

    # 使用 grid 布局管理器
    root.grid_rowconfigure(0, weight=2)  # 减小text_widget的权重
    root.grid_rowconfigure(1, weight=1)  # 按钮区域权重
    root.grid_rowconfigure(2, weight=0)  # 控制面板区域不需要伸缩
    root.grid_columnconfigure(0, weight=1)

    # 主框架
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky="nsew")

    # 按钮框架
    button_frame = ttk.Frame(root)
    button_frame.grid(row=1, column=0, sticky="ew", pady=(5, 10))

    # 获取默认 button background color
    temp_button = tk.Button(root)
    default_bg = temp_button.cget("bg")
    temp_button.destroy()

    # 初始化 selected_id
    selected_id = [None]
    if messages:
        selected_id[0] = messages[-1]["id"]

    # 存储按钮引用以避免重复创建
    button_refs = {}

    # 创建控制面板
    font_size = create_control_panel(root, button_refs, selected_id, default_bg)

    # 文本显示框和滚动条
    text_frame = ttk.Frame(main_frame)
    text_frame.pack(expand=True, fill=tk.BOTH, padx=(0, 10), pady=(0, 10))

    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(text_frame, 
                         wrap=tk.WORD, 
                         font=(fontName, fontSize), 
                         bg="#ad98e6",
                         fg="#333333", 
                         bd=0, 
                         highlightthickness=0, 
                         height=15,  # 减小文本框的初始高度
                         yscrollcommand=scrollbar.set)
    text_widget.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=text_widget.yview)

    # 显示最后一条消息
    if messages:
        text_widget.insert(tk.END, messages[-1]["message"])
    text_widget.config(state=tk.DISABLED)

    def format_log_message(message_text):
        """
        格式化日志消息，提取关键信息
        """
        try:
            # 如果是字符串，尝试解析为JSON
            if isinstance(message_text, str):
                try:
                    import json
                    message_text = json.loads(message_text)
                except:
                    pass

            # 转换为字符串以便处理
            message_str = str(message_text)
            
            # 提取code_context内容
            code_context_start = message_str.find("code_context : ")
            if code_context_start != -1:
                code_context_start += len("code_context : ")
                code_context_end = message_str.find("\n", code_context_start)
                if code_context_end == -1:
                    code_context_end = message_str.find("File:", code_context_start)
                code_context = message_str[code_context_start:code_context_end].strip()
                
                # 提取文件信息
                file_info_start = message_str.rfind(".py:")
                if file_info_start != -1:
                    file_info = message_str[file_info_start+4:].strip()
                    
                    # 组合格式化后的消息
                    formatted_msg = f"Context: {code_context}\nInfo: {file_info}"
                    return formatted_msg
            
            return message_str
        except Exception as e:
            print(f"格式化消息时出错: {e}")
            return message_text

    def update_button_text(btn, msg):
        """
        更新按钮文字
        """
        message_text = msg["message"]
        if isinstance(message_text, list):
            message_text = message_text[0] if message_text else "空消息"
        
        # 格式化消息
        formatted_text = format_log_message(message_text)
        
        # 获取最后200个字符
        if len(formatted_text) > 200:
            content_text = "..." + formatted_text[-200:]
        else:
            content_text = formatted_text
        
        # 格式化时间戳
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        button_text = f"{timestamp}\n{content_text}"
        btn.config(text=button_text)

    def update_text(message_id):
        """
        更新主文本框显示内容，并更新选中的按钮。
        显示完整的原始消息内容。
        """
        selected_id[0] = message_id
        data = load_log()
        messages = data.get("messages", [])
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        for msg in messages:
            if msg["id"] == message_id:
                message_text = msg["message"]
                if isinstance(message_text, list):
                    message_text = message_text[0] if message_text else "空消息"
                # 直接显示原始消息，不进行格式化
                text_widget.insert(tk.END, str(message_text))
                break
        text_widget.config(state=tk.DISABLED)
        update_button_colors()

    def update_button_colors():
        """
        更新按钮颜色，突出显示选中的按钮。
        """
        for msg_id, btn in button_refs.items():
            if msg_id == selected_id[0]:
                btn.config(bg="green", fg="white", activebackground="darkgreen", activeforeground="white")
            else:
                btn.config(bg=default_bg, fg="black", activebackground="lightgrey", activeforeground="black")

    def open_log_file():
        """
        使用默认程序打开日志文件
        """
        try:
            os.startfile(LOG_FILE)
        except Exception as e:
            print(f"打开日志文件失败: {e}")

    def create_buttons(messages):
        """
        根据消息列表创建按钮，并根据 selected_id 设置按钮颜色。
        按钮文字显示消息内容的最后200个字符，并自动换行。
        按钮布局为四行，每行3个。
        双击任何按钮可以打开日志文件。
        """
        # 清除现有按钮
        for widget in button_frame.winfo_children():
            widget.destroy()
        button_refs.clear()

        # 创建四个子框架用于放置按钮
        frames = []
        for _ in range(4):
            frame = ttk.Frame(button_frame)
            frame.pack(side=tk.TOP, fill=tk.X, expand=True, pady=1)  # 添加一点垂直间距
            frames.append(frame)

        # 创建新按钮
        reversed_messages = list(reversed(messages))
        for idx, msg in enumerate(reversed_messages):
            # 获取消息内容
            message_text = msg["message"]
            if isinstance(message_text, list):
                message_text = message_text[0] if message_text else "空消息"
            
            # 格式化消息
            formatted_text = format_log_message(message_text)
            
            # 获取最后200个字符
            if len(formatted_text) > 200:
                content_text = "..." + formatted_text[-200:]
            else:
                content_text = formatted_text
            
            # 格式化时间戳
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            button_text = f"{timestamp}\n{content_text}"
            
            # 决定按钮放在哪一行（每行3个按钮）
            row_idx = idx // 3
            if row_idx >= 4:  # 如果超过四行，不再显示
                break
                
            parent_frame = frames[row_idx]
            
            btn = tk.Button(parent_frame, text=button_text, 
                          font=('Consolas', 10),  # 默认字体大小改为10
                          wraplength=350,  # 增加文本换行宽度
                          justify=tk.LEFT,  # 文本左对齐
                          anchor='w',  # 文本左对齐
                          command=lambda id=msg["id"]: update_text(id))
            
            # 绑定双击事件
            btn.bind('<Double-Button-1>', lambda e: open_log_file())
            
            # 在每一行中使用pack布局
            btn.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.BOTH, expand=True)
            button_refs[msg['id']] = btn  # 存储按钮引用
            
        print(u"创建了 {0} 个按钮。".format(len(button_refs)))

        # 更新按钮颜色
        update_button_colors()

    # 初始创建按钮
    if messages:
        create_buttons(messages)
    else:
        print("没有消息可供显示按钮。")

    def flash_taskbar():
        """
        使任务栏图标闪烁
        """
        if os.name == 'nt':  # Windows系统
            try:
                import win32gui
                import win32con
                hwnd = win32gui.GetParent(root.winfo_id())
                win32gui.FlashWindow(hwnd, True)
            except ImportError:
                print("win32gui模块未安装，无法实现任务栏闪烁")

    def process_queue():
        """
        处理来自监控线程的队列消息，更新GUI。
        """
        try:
            while True:
                latest_messages = q.get_nowait()
                current_selected_id = selected_id[0]
                
                # 检查是否有新消息
                has_new_message = False
                if len(latest_messages) > len(button_refs):
                    has_new_message = True
                else:
                    for msg in latest_messages:
                        if msg["id"] not in button_refs:
                            has_new_message = True
                            break

                # 如果有新消息，闪烁任务栏
                if has_new_message:
                    flash_taskbar()

                if any(msg["id"] == current_selected_id for msg in latest_messages):
                    # 更新当前选中消息的内容
                    for msg in latest_messages:
                        if msg["id"] == current_selected_id:
                            text_widget.config(state=tk.NORMAL)
                            text_widget.delete(1.0, tk.END)
                            text_widget.insert(tk.END, msg["message"])
                            text_widget.config(state=tk.DISABLED)
                            break
                else:
                    if latest_messages:
                        selected_id[0] = latest_messages[-1]["id"]
                        text_widget.config(state=tk.NORMAL)
                        text_widget.delete(1.0, tk.END)
                        text_widget.insert(tk.END, latest_messages[-1]["message"])
                        text_widget.config(state=tk.DISABLED)
                    else:
                        selected_id[0] = None
                        text_widget.config(state=tk.NORMAL)
                        text_widget.delete(1.0, tk.END)
                        text_widget.config(state=tk.DISABLED)

                # 如果消息列表发生变化，重新创建按钮
                if len(button_refs) != len(latest_messages) or any(msg["id"] not in button_refs for msg in latest_messages):
                    create_buttons(latest_messages)
                else:
                    # 更新现有按钮的文字
                    for msg in latest_messages:
                        if msg["id"] in button_refs:
                            update_button_text(button_refs[msg["id"]], msg)
                    # 更新按钮颜色
                    update_button_colors()

        except Empty:
            pass
        except Exception as e:
            print(u"错误: 在处理队列时发生异常: {0}".format(e))
        finally:
            if not stop_event.is_set():
                root.after(1000, process_queue)  # 每秒检查一次队列

    # 启动队列处理
    root.after(1000, process_queue)

    def on_closing():
        """
        处理窗口关闭事件，设置'show'键为False，并停止监控线程。
        """
        set_show_flag(False)
        stop_event.set()
        root.destroy()
        # print("程序已退出，'show'键已设置为False。")
        os._exit(0)

    # 绑定窗口关闭事件
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 启动主事件循环
    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_closing()
    finally:
        # 确保线程安全退出
        if thread.is_alive():
            stop_event.set()
            thread.join()

def show_win(text=""):
    initialize_log_file()
    if not check_and_set_show():
        showMessageWin(text=text)

def main(text="aa"):
    # 使用绝对路径确保子进程能够正确找到脚本文件
    script_path = os.path.abspath(__file__)
    python_exe = 'pythonw_log.exe'
    print(os.path.exists(fr'{os.getenv("LugwitAppDir")}/python_env/{python_exe}'))
    cmd = [fr'{os.getenv("LugwitAppDir")}/python_env/{python_exe}', script_path, "show_win", text]
    print(' '.join(cmd))
    print("is_process_running", is_process_running(python_exe))
    if text != "None":
        print(repr(text))
        save_message_to_file(text)
    if not is_process_running(python_exe):
        subprocess.Popen(cmd ,shell=False)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        show_win(sys.argv[-1])
    else:
        show_win()

        
