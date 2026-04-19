# coding:utf-8
from __future__ import print_function
import json

import os
import sys
import re
import subprocess
import traceback
import time
import getpass
import ctypes
import codecs


curDir= os.path.dirname(__file__)
sys.path.append(curDir)
if sys.version_info[0] == 3:
    import showMessage_ps as ps_win
    
l_src_Dir = re.search(r'.*\\l_src',__file__).group()
print (l_src_Dir)
sys.path.append(l_src_Dir)
from usualFunc import lprint,isMayaEnv,dynamic_import




# 为了兼容Python 2和3，使用try-except来导入可能的模块差异
six_file=r"D:\TD_Depot\plug_in\Python\Python27\Lib\site-packages\six.py"

six = dynamic_import(six_file)
queue = six.moves.queue
LugwitToolDir = os.getenv('LugwitToolDir')

userDir=os.path.expandvars("%USERPROFILE%")
if userDir == "C:\\Windows\\system32\\config\\systemprofile":
    userDir = r"C:\Users\Administrator.OC"

oriEnvVarFile=userDir+r'/.Lugwit/config/oriEnvVar.json'

# oriEnvVarFile=os.getenv("oriEnvVarFile")
with codecs.open(oriEnvVarFile,'r',encoding='utf-8') as f:
    oriEnvVar=json.load(f)
    temp_dict= {}
    for key, val in oriEnvVar.items():
        try:
            temp_dict[str(key)]=str(val)
        except:
            print (traceback.format_exc())



def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def read_output(process, output_queue):
    """
    不断读取子进程的输出，并将其存储在队列中。

    :param process: subprocess.Popen()实例，代表一个子进程。
    :param output_queue: 存储子进程输出的队列。
    """
    output_list=[]
    while True:
        try:
            output = process.stdout.readline()  # 从子进程的stdout中读取一行输出
            if output:
                output_list.append(output)
            if not output and process.poll() is not None:
                print ('exit while loop')
                break
            # 在Python 2和Python 3中都兼容的处理方式
            if sys.version_info[0] >= 3:
                # Python 3
                decoded_output = output.strip()
            else:
                # Python 2
                decoded_output = output.strip()
            output_queue.put(decoded_output)
        except Exception as e:
            print("Error:", e)
            stderr = e.replace('"', '`"').replace('\n', '`n')

            ps_script = '''
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.MessageBox]::Show("{}","错误提示")
            '''.format(e)
            # 在Python中运行PowerShell脚本
            subprocess.run(["powershell", "-Command", ps_script], check=True)
            break

    return_code = process.wait()
    print('return_code', return_code)
    if return_code != 0:
        # PowerShell脚本字符串，将错误信息传递给它
        stderr = '\n'.join(output_list)
        stderr=stderr.replace('"', '`"').replace('\n', '`n')
        ps_script = '''
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show("{}","错误提示")
        '''.format(stderr)
        # 在Python中运行PowerShell脚本
        subprocess.Popen(["powershell", "-Command", ps_script])
        # 使用clip命令复制文本到剪贴板
        process = subprocess.Popen('clip', stdin=subprocess.PIPE)
        process.communicate(input=stderr)

def show_progress_bar(duration=0.1, steps=100):
    u"""
    显示一个运行指定时间的进度条。
    
    :param duration: 进度条运行的总时间，单位为秒。
    :param steps: 进度条更新的次数。
    """
    import maya.cmds as cmds
    # 确保在开始前关闭已有的进度窗口
    if cmds.progressWindow(q=True, isCancelled=True):
        cmds.progressWindow(endProgress=True)
    
    cmds.progressWindow(title=u'正在启动',
                        progress=0,
                        status=u'正在启动: ',
                        isInterruptable=False,
                        maxValue=100)

    step_time = duration / steps  # 计算每步的时间
    for i in range(steps):
        if cmds.progressWindow(q=True, isCancelled=True):
            break
        # 更新进度条的进度值
        cmds.progressWindow(edit=True, progress=(i + 1) * (100 / steps), )
        time.sleep(step_time)  # 等待，模拟耗时操作

    cmds.progressWindow(endProgress=True)
    

def display_message(stderr):
    """
    显示PowerShell弹窗以展示错误信息。

    :param stderr: 错误信息字符串。
    """
    stderr = stderr.replace('"', '`"').replace('\n', '`n')
    ps_script = '''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show("{}")
    '''.format(stderr)
    subprocess.Popen(["powershell", "-Command", ps_script])

def startPyFile(pyFile='', 
                sys_argv=[], 
                specify_sys_executable=None, 
                usePythonw=False, 
                blockProcess=False,
                append_env={},
                checkIsStart=True,
                use_new_console=False):
    """
    启动Python文件作为独立进程。
    
    :param pyFile: Python文件路径。
    :param specify_sys_executable: 是否使用系统默认的Python执行程序。
    :param sys_argv: 传递给Python脚本的命令行参数。
    :param usePythonw: 是否使用pythonw.exe来运行脚本，避免弹出控制台窗口。
    :param blockProcess: 是否阻塞进程直到子进程完成。
    """
    oriEnvVar.update(append_env)
    lprint (locals(),sys.executable,force_print=True)
    try:
        temBat = '{}\\Temp.Bat'.format(os.environ["Temp"])
        if not specify_sys_executable or specify_sys_executable=='currentPythonJieShiQi':
            sys_executable = sys.executable
        else: 
            sys_executable=specify_sys_executable

        print (specify_sys_executable,sys_executable)
        #creationflags = subprocess.CREATE_NEW_CONSOLE if usePythonw else 0
        creationflags = 0
        if use_new_console:
            creationflags = subprocess.CREATE_NEW_CONSOLE
        lprint (creationflags)
        # std_out = None if not usePythonw else subprocess.PIPE
        # std_err = None if not usePythonw else subprocess.STDOUT
        if isinstance(sys_argv, list):
            sys_argv='_'.join(sys_argv)
        if usePythonw:
            sys_executable=sys_executable.replace('python.exe', 'pythonw.exe')
            cmd = [ sys_executable , pyFile, sys_argv]
        else:
            sys_executable=sys_executable.replace('pythonw.exe', 'python.exe')
            cmd = [sys_executable,pyFile, sys_argv]

        lprint (' '.join(cmd))
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        if sys.version_info[0] >= 3:
            process = subprocess.Popen(cmd, 
                # stdout=std_out, 
                # stderr=std_err, 
                shell=False, 
                creationflags=creationflags,
                env=oriEnvVar,
                text=True,
                )
            cmd_pid=process.pid
            return
        else:
            # Python 2
            process = subprocess.Popen(cmd, 
                                       stdout=std_out, 
                                       stderr=std_err, 
                                       shell=False, 
                                       creationflags=creationflags,
                                       env=oriEnvVar)

        if isMayaEnv():
            show_progress_bar()


        time.sleep(3)
        if isinstance(process.poll(),int) and checkIsStart:
            lprint (process.poll())
            ps_script = '''
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.MessageBox]::Show("运行错误 {}")
            '''.format(process.poll())
            # 在Python中运行PowerShell脚本
            subprocess.Popen(["powershell", "-Command", ps_script])


    except:
        e = traceback.format_exc()
        print (e)
        display_message('{}\nspecify_sys_executable:{}\nsys_executable:{}++'.format(e,specify_sys_executable,sys_executable))

def startProcess(ExeFile,env={},shell=False,cmd_args=[],*args):
    cwdDir=os.path.dirname(ExeFile)
    lprint(cwdDir)
    if not os.path.exists(cwdDir):
        return '.'
    print(locals())
    print (u'启动程序{}'.format(ExeFile))
    filePath=re.search(r'"(.+)"',ExeFile)
    if isinstance(env,bool):
        env={}
    oriEnvVar.update(env)
    if filePath:
        filePath=filePath.group(1)
    else:
        filePath=ExeFile
        
    if not os.path.exists(filePath):
        QMessageBoxinfo=u'你要启动的程序\n{}\n不存在'.format(filePath)
        import win32con, win32gui
        response = win32gui.MessageBox(
                0, QMessageBoxinfo, "Confirm", 
                win32con.MB_OK | win32con.MB_ICONWARNING)
        return


    def runAsBat(ExeFile):
        try:
            with open('{}/startfile.bat'.format(os.environ["Temp"]),'w') as f:
                f.write(u'cmd/c {}\nset pythonpath\npause'.format(os.path.normpath(ExeFile)))
            os.startfile(u'{}/startfile.bat'.format(os.environ["Temp"]))
            print (u'使用bat启动程序{}'.format(ExeFile))
        except:
            ps_win.showMessageWin(text = u'启动失败{}'.format(ExeFile),)
    try:
        ExeFile=os.path.normpath(ExeFile)
        if cmd_args:
            ExeFile=[ExeFile]+cmd_args
        lprint (ExeFile)
        process=subprocess.Popen(ExeFile,
                                 shell=shell,
                                 env=oriEnvVar,
                                 creationflags=0,
                                 cwd=cwdDir)
        print (u'subprocess.Popen{}'.format(ExeFile))

    except:
        ps_win.showMessageWin(text = u'以bat方式启动{}'.format(ExeFile),)
        runAsBat(ExeFile)


def run_as_normal_user(maya_path, program_args=None,env={}):
    """使用 ShellExecuteW 以受限的标准用户权限运行 Maya，添加/trustlevel:0x20000参数"""
    maya_path=os.path.normpath(maya_path)
    try:
        # 构建命令行参数
        params = ''
        if program_args:
            params = ' '.join(program_args)
        
        print(u"启动程序: {} {}".format(maya_path,params))
        # command_string = f'set {my_env_var}="{my_env_value}"'
        # parameters = f'/c "{command_string}"'
        # 创建一个cmd命令，包含runas和trustlevel参数
        cmd_line = "C:\\Windows\\explorer.exe \"{}\" {}".format(maya_path,params)
        print(u"执行命令: {}".format(cmd_line))
        
        # 使用ShellExecuteW启动命令
        #subprocess.Popen(maya_path, shell=True, env=env)
        os.environ['PATH'] += ";C:\\Windows\\System32"
        env['PATH'] += ";C:\\Windows\\System32"
        cmd='C:\\Windows\\explorer.exe "{}" {}'.format(maya_path,params) # 这样无法传递环境变量
        cmd='C:\\Windows\\System32\\cmd.exe /c C:\\Windows\\System32\\runas.exe /trustlevel:0x20000 "{}" {}'.format(maya_path,params) # Win11不可用
        cmd='C:\\Windows\\System32\\cmd.exe /c "{}" {}'.format(maya_path,params) # Win11不可用
        print("cmd------------",cmd)
        pyTemplateFile=curDir+'\\startMayaExe.py'
        tempPyFile=os.path.join(os.environ["Temp"],"startMayaExe.py")
        with codecs.open(pyTemplateFile,'r',encoding='utf-8') as f:
            aa=f.read()
        
        with codecs.open(tempPyFile,'w',encoding='utf-8') as f:
            bb=aa.replace("mayaExeFile",maya_path).replace("envVar",repr(env))
            f.write(bb)
        print('bbbb>>>>>>>>',bb)
        # subprocess.Popen([mayapy_exe,tempPyFile,], shell=False, env=env)
        if program_args:
            cmd_list=[maya_path]+program_args
            cmd = '" "'.join(cmd_list)# type: ignore
            print("cmd->",cmd)
        else:
            cmd_list=[maya_path]        # 确保所有环境变量都是字符串类型
        temp_env = {}
        for key, value in env.items():
            try:
                # 处理键
                str_key = str(key) if isinstance(key, str) else str(key).encode('utf-8')
                # 处理值
                str_value = str(value) if isinstance(value, str) else str(value).encode('utf-8')
                temp_env[str_key] = str_value
            except (UnicodeEncodeError, UnicodeDecodeError):
                print("Warning: Could not convert environment variable {0} to string".format(key))
                continue
        
        # 创建新进程
        lprint(cmd_list)
        try:
            subprocess.Popen(
                cmd_list,   # type: ignore
                env=temp_env,
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            ) # type: ignore
        except TypeError as e:
            print("Error creating process: {0}".format(e))
            print("Command: {0}".format(cmd_list))
            print("Environment variables that caused the error:")
            for k, v in temp_env.items():
                print("{0}: {1} = {2}".format(k, type(v).__name__, v))

    
    except Exception as e:
        traceback.print_exc()

    

        
            
__all__=['startPyFile','startProcess','run_as_normal_user']       
        
if __name__=='__main__':
    # 创建一个新的控制台窗口来运行 cmd.exe
    run_as_normal_user(r"C:\Program Files\Autodesk\Maya2020\bin\maya.exe",env=dict(os.environ.copy()))