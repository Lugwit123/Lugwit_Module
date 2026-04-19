import os
import sys
import shutil
import fire

LugwitToolDir = os.environ.get('LugwitToolDir')
sys.path.append(LugwitToolDir + '/Lib')
import Lugwit_Module as LM

def safe_copy(src_path, dest_path):
    try:
        # 确保目标目录存在
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(src_path, dest_path)
        print(f"Successfully copied: {dest_path}")
    except OSError as e:
        print(f"Failed to copy {src_path} to {dest_path}. Error: {str(e)}")

def should_ignore(path, ignore_keywords):
    # 检查路径中是否含有忽略的关键词
    return any(keyword in path for keyword in ignore_keywords)

def sync_folders(source, destination, ignore_keywords=None):
    if ignore_keywords is None:
        ignore_keywords = []

    dest_files = set()
    empty_dirs = set()

    for root, dirs, files in os.walk(source):
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_keywords)]  # 修改dirs列表，排除不需要遍历的目录
        for name in files:
            if should_ignore(name, ignore_keywords):
                continue  # 忽略文件
            src_path = os.path.join(root, name)
            rel_path = os.path.relpath(src_path, source)
            dest_path = os.path.join(destination, rel_path)
            dest_files.add(dest_path)

            if os.path.exists(dest_path):
                src_mtime = os.path.getmtime(src_path)
                dest_mtime = os.path.getmtime(dest_path)
                if src_mtime != dest_mtime:
                    safe_copy(src_path, dest_path)
            else:
                safe_copy(src_path, dest_path)

        # 记录空文件夹
        for d in dirs:
            src_dir_path = os.path.join(root, d)
            rel_dir_path = os.path.relpath(src_dir_path, source)
            dest_dir_path = os.path.join(destination, rel_dir_path)
            if not os.listdir(src_dir_path):  # 检查文件夹是否为空
                empty_dirs.add(dest_dir_path)

    # 创建所有空文件夹
    for empty_dir in empty_dirs:
        os.makedirs(empty_dir, exist_ok=True)
        print(f"Created empty directory: {empty_dir}")

    # 删除目标中已不存在于源中的文件
    for dest_path in dest_files:
        if not os.path.exists(dest_path.replace(destination, source)):
            try:
                os.remove(dest_path)
                print(f"Deleted: {dest_path}")
            except OSError as e:
                print(f"Failed to delete {dest_path}. Error: {str(e)}")

if __name__ == '__main__':
    # fire.Fire(sync_folders)

    # # 调用函数进行同步
    # sync_folders(LM.ProgramFilesLocal_Public, LM.ProgramFilesLocal)
    # 调用函数进行同步
    sync_folders(r'A:\TD\Lugwit_syncPlug\lugwit_insapp\python_env', 
                r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\python_env')
