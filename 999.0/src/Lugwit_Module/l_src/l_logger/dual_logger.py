import threading
import subprocess
import logging
import os
import sys
import traceback
import time

class UTF8FileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, 'utf-8', delay)

class UniversalLogger:
    def __init__(self, log_file='output.log'):
        log_file_dir = os.path.normpath(os.path.dirname(log_file))
        if not os.path.exists(log_file_dir):
            print ('log_file_dir',log_file_dir)
            #os.system('mkdir {}'.format(log_file_dir))
            os.makedirs(log_file_dir, exist_ok=True)
        if not os.path.exists(log_file_dir):
            return
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.log_file = log_file

        # 创建日志记录器
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # 创建一个自定义的 UTF-8 文件处理器
        file_handler = UTF8FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter('%(message)s'))

        # 添加文件处理器到日志记录器
        self.logger.addHandler(file_handler)

        # 重写默认的异常处理钩子
        sys.excepthook = self._handle_exception

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        error_details = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.write(f"Caught exception:\n{error_details}")

    def write(self, message):
        try:
            self.original_stdout.write(message)
            stripped_message = message.rstrip('\n')
            if stripped_message:
                logging.info(stripped_message)
        except Exception as e:
            self.original_stderr.write(f"Exception caught: {e}\n")
            self.original_stderr.flush()

    def flush(self):
        self.original_stdout.flush()

    def enable(self):
        sys.stdout = self
        sys.stderr = self

    def disable(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def run_command(self, command):
        process = subprocess.Popen(command, 
                                   shell=True, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   bufsize= 0)
        
        def reader_thread(pipe):
            line=''
            while True:
                if sys.version_info[0]==2:
                    line = pipe.readline().decode('gbk', errors='replace')
                else:
                    readline = pipe.readline()
                    print (type(readline),bool(readline))
                    if isinstance(readline, bytes):
                        try:
                            line = readline.decode('utf-8')
                        except:
                            print  ('error',readline)
                            line = readline.decode('gbk')  # 使用GBK编码来解码
                    else:
                        line = readline

                if line:
                    self.write(str(line))


        stdout_thread = threading.Thread(target=reader_thread, args=(process.stdout,))
        stderr_thread = threading.Thread(target=reader_thread, args=(process.stderr,))

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join()
        stderr_thread.join()

        process.wait()
