# -*- coding: utf-8 -*-

import os
import json
import threading
import codecs
import shutil

# 配置日志文件路径和锁文件路径
LOG_FILE = r"D:\TD_Depot\Temp\message_log.json"
LOCK_FILE = LOG_FILE + ".lock"

# 创建一个线程锁来确保线程安全
_file_lock = threading.Lock()

def get_log_file_path():
    """获取日志文件路径"""
    return r"D:\TD_Depot\Temp\message_log.json"

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
            with codecs.open(LOG_FILE, "w", encoding="utf-8") as f:
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
        with codecs.open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        shutil.move(temp_file, LOG_FILE)
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
        with codecs.open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default_data

def save_log(data):
    """保存日志到文件，确保线程安全"""
    log_file = get_log_file_path()
    with _file_lock:
        with codecs.open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

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
                print(u"保留最新的10条消息")

            # 重新编号
            for idx, msg in enumerate(messages, start=1):
                msg["id"] = idx

            data["messages"] = messages
            atomic_write_log(data)
            print(u"消息保存成功")
        except Exception as e:
            print(u"保存消息时出错: {0}".format(e))
