 
import os,sys
import winreg
import winshell
import ctypes
import getpass
import traceback
import fire
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def runAsAdmin(pyexe='',pyfile='', args=[],orgi_argv={}):
    if isinstance(args,str):
        args=[args]
    if not pyexe:
        pyexe=sys.executable
    
    quoted_args = ['"{}"'.format(arg) if ' ' in arg else arg for arg in args]
    params = '"{}" {}'.format(pyfile, ' '.join(quoted_args))
    command = f'"{pyexe}" {params}'
    print(f"运行程序: {command}")
    if not orgi_argv:
        orgi_argv=params
    if is_admin():
        try:
            print("获取管理员成功")
            #ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/K {command}", None, 1)
            subprocess.run(command, shell=True)
        except Exception as e:
            print(f"以管理员身份运行{command}程序时出现错误:")
            print(e)
    else:
        if sys.version_info[0] == 3:
            # 以管理员身份运行程序
            print("\n运行",f"{pyexe} {orgi_argv}")
            process_handle = ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {pyexe} {orgi_argv}", None, 1)
            if process_handle <= 32:
                # 错误码处理
                error_msgs = {
                    0: "系统内存不足，无法加载应用程序。",
                    2: "找不到文件。",
                    3: "找不到路径。",
                    5: "访问被拒绝。",
                    6: "无效的句柄。",
                    11: "不可用的动态链接库。",
                    26: "正在尝试执行远程系统上的文件。",
                    27: "传输模式远程连接失败。",
                }
                print(f"ShellExecuteW 失败，错误码: {process_handle} - {error_msgs.get(process_handle, '未知错误')}")
            else:
                print(f"管理员权限命令已发出，process_handle: {process_handle}")
        else:#in python2.x
            ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(pyexe), unicode(pyfile), None, 1)

if __name__ == '__main__':
    #runAsAdmin(pyexe,pyfile)
    orgi_argv=['"{}"'.format(arg) if ' ' in arg else arg for arg in sys.argv]
    orgi_argv = ' '.join(orgi_argv)
    fire.Fire(runAsAdmin)
