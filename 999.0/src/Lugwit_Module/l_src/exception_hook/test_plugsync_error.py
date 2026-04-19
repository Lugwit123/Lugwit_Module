"""
模拟plugSync.py中的AttributeError异常
"""

import sys
import os

# 添加路径
sys.path.append(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\Lib")

def simulate_plugsync_error():
    """模拟plugSync.py中的错误"""
    import Lugwit_Module as LM
    
    # 这里会触发 AttributeError: module 'Lugwit_Module' has no attribute 'hostName'
    if LM.hostName not in ['DESKTOP-LDSM1H1','TD','PC-20240202CTEU',"TD2","TD3"]:
        print("主机名检查通过")
    else:
        print("主机名在列表中")

if __name__ == "__main__":
    print("🎯 模拟plugSync.py中的AttributeError异常")
    print("="*50)
    
    simulate_plugsync_error()
