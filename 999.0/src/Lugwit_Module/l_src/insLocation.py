# -*- coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

import sys
import traceback
import json
import re
import os
from typing import Dict, Any, List, Optional, Tuple

if sys.version[0] == '2':
    import _winreg as winreg
else:
    import winreg

sys.path.append(os.path.dirname(__file__))
from l_winreg.l_winreg import CustomRegistryKey

if __name__ == '__main__':
    from usualFunc import lprint
else:
    lprint = print


def get_deadline_install_dir():
    # 定义注册表路径
    reg_path = r"SOFTWARE\Thinkbox\Deadline Client 10"
    
    try:
        # 打开注册表项
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            # 获取安装目录的值
            install_dir = winreg.QueryValueEx(key, "Location")[0]
            return install_dir
    except FileNotFoundError:
        print("Deadline Client 10未安装或路径不正确。")
        return None
    
# 定义软件安装位置的信息结构体
class SoftwareLocation:
    def __init__(self, insDir: str, exeFile: str, exist: bool):
        self.insDir = insDir  # 安装目录
        self.exeFile = exeFile  # 可执行文件路径
        self.exist = exist  # 是否存在

    def to_dict(self) -> Dict[str, Any]:
        """将结构体转换为字典"""
        return {
            "insDir": self.insDir,
            "exeFile": self.exeFile,
            "exist": self.exist
        }

    def __getitem__(self, key: str) -> Any:
        """通过键获取对应的属性值"""
        if key == "insDir":
            return self.insDir
        elif key == "exeFile":
            return self.exeFile
        elif key == "exist":
            return self.exist
        else:
            raise KeyError(f"'{key}' not found in SoftwareLocation")
        
    def get(self, key: str, default: Any = None) -> Any:
        """通过键获取对应的属性值，如果键不存在则返回默认值"""
        try:
            return self[key]
        except KeyError:
            return default




def getNukeInsLocation() -> Optional[str]:
    """获取Nuke安装位置"""
    nukeInsLocation = getInsLocationDict(softwareNameList=["Nuke"],
                                          InsLocationEnumKeyList=["SOFTWARE\\Foundry"],
                                          insLocationSubKeyList=[""],
                                          valueNameList=["PATH"])
    if nukeInsLocation:
        lprint("Nuke安装位置：", nukeInsLocation)
        return nukeInsLocation["Nuke"]


def getInsLocationDict(
        softwareNameList: List[str] = ["Nuke", "Maya", "Unreal Engine", "Houdini"],
        InsLocationEnumKeyList: List[str] = [
            "SOFTWARE\\WOW6432Node\\Foundry",
            "SOFTWARE\\Autodesk\\Maya",
            "SOFTWARE\\EpicGames\\Unreal Engine",
            "SOFTWARE\\Autodesk\\Side Effects Software"
        ],
        insLocationSubKeyList: List[str] = ["", r"Setup\InstallPath", "", ""],
        valueNameList: List[str] = [
            "",
            "MAYA_INSTALL_LOCATION",
            "InstalledDirectory",
            "InstallPath"
        ],
        exeFilePathList: List[List[str]] = [
            ["Nuke{version}.exe"],
            ["bin/maya.exe"],
            ["Engine/Binaries/Win64/UE4Editor.exe", "Engine/Binaries/Win64/UnrealEditor.exe"],
            ["bin/houdinifx.exe"]
        ]
) -> Dict[str, Dict[str, SoftwareLocation]]:
    """获取软件安装位置字典"""
    InsLocationInfo = [(InsLocationEnumKeyList[i], insLocationSubKeyList[i],
                        valueNameList[i], softwareNameList[i], exeFilePathList[i])
                       for i in range(len(softwareNameList))]
    InsLocationDict = {}

    for InsLocationKey, insLocationSubKey, valueName, softwareName, exeFilePath in InsLocationInfo:
        if softwareName == "Nuke":
            SubItems = []
            try:
                if winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, InsLocationKey):
                    SubItems += CustomRegistryKey(winreg.HKEY_LOCAL_MACHINE, InsLocationKey).getallSubitem()
                if winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, InsLocationKey.replace("\\WOW6432Node", "")):
                    SubItems += CustomRegistryKey(
                        winreg.HKEY_LOCAL_MACHINE, InsLocationKey.replace("\\WOW6432Node", "")).getallSubitem()
            except:
                pass

        else:
            SubItems = CustomRegistryKey(winreg.HKEY_LOCAL_MACHINE, InsLocationKey).getallSubitem()

        for item in SubItems:
            if '14' in item:
                InsLocationKey = InsLocationKey.replace("\\WOW6432Node", "")
                valueName = 'Path'
            key = CustomRegistryKey(winreg.HKEY_LOCAL_MACHINE, '\\'.join((InsLocationKey, item, insLocationSubKey)),
                                     reserved=0, access=winreg.KEY_READ)
            get_value = key.get_value(valueName)
            if not get_value:
                continue
            default_value, value_type = key.get_value(valueName)
            default_value = default_value.replace("\\", "/")
            key.close()
            exeFile = ''
            for _exeFilePath in exeFilePath:
                if softwareName == "Nuke":
                    version = re.search(r"Nuke *(.+)v", item).group(1)
                    _exeFilePath = _exeFilePath.replace("{version}", version)
                _exeFilePath = default_value + "/" + _exeFilePath
                if os.path.exists(_exeFilePath):
                    exeFile = _exeFilePath
                    break
            InsLocationDict.setdefault(softwareName, {}).setdefault(item, SoftwareLocation(default_value, exeFile, os.path.exists(default_value)))
    return InsLocationDict


def getUEInsLocationDict() -> Optional[Dict[str, SoftwareLocation]]:
    """获取Unreal Engine安装位置字典"""
    ueInsLocationDict = getInsLocationDict(softwareNameList=["Unreal Engine"],
                                            InsLocationEnumKeyList=["SOFTWARE\\EpicGames\\Unreal Engine"],
                                            insLocationSubKeyList=[""],
                                            valueNameList=["InstalledDirectory"],
                                            exeFilePathList=[["Engine/Binaries/Win64/UE4Editor.exe",
                                                              "Engine/Binaries/Win64/UnrealEditor.exe"]])
    if ueInsLocationDict:
        return ueInsLocationDict["Unreal Engine"]


def getMayaInsLocationDict() -> Optional[Dict[str, SoftwareLocation]]:
    """获取Maya安装位置字典"""
    mayaInsLocationDict = getInsLocationDict(softwareNameList=["Maya"],
                                              InsLocationEnumKeyList=["SOFTWARE\\Autodesk\\Maya"],
                                              insLocationSubKeyList=[r"Setup\InstallPath"],
                                              valueNameList=["MAYA_INSTALL_LOCATION"],
                                              exeFilePathList=[["bin/maya.exe"]])
    if mayaInsLocationDict and "Maya" in mayaInsLocationDict:
        result = mayaInsLocationDict["Maya"]
        # 设置json文件保存路径
        json_file = os.path.join(r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\data' , "ins_location", "maya_locations.json")
        # 确保目录存在
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        # 如果文件不存在,则保存
        if not os.path.exists(json_file):
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4, default=lambda x: x.to_dict() if hasattr(x, "to_dict") else str(x))
        return result


def getHoudiniInsLocationDict() -> Optional[Dict[str, SoftwareLocation]]:
    """获取Houdini安装位置字典"""
    mayaInsLocationDict = getInsLocationDict(softwareNameList=["Houdini"],
                                              InsLocationEnumKeyList=["SOFTWARE\\Side Effects Software"],
                                              insLocationSubKeyList=[""],
                                              valueNameList=["InstallPath"],
                                              exeFilePathList=[["bin/houdinifx.exe"]])
    if mayaInsLocationDict:
        return mayaInsLocationDict["Houdini"]


def get_installed_software() -> Dict[str, str]:
    """获取已安装软件的字典"""
    installed_software = {}

    hives = [(winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER"),
             (winreg.HKEY_LOCAL_MACHINE, "HKEY_LOCAL_MACHINE")]

    for hive, key in hives:
        key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall"

        with winreg.OpenKey(hive, key_path) as software_key:
            for i in range(0, winreg.QueryInfoKey(software_key)[0]):
                software_name = winreg.EnumKey(software_key, i)
                with winreg.OpenKey(software_key, software_name) as sub_key:
                    try:
                        # 获取 DisplayName 和 InstallLocation 的值
                        display_name = winreg.QueryValueEx(sub_key, 'DisplayName')[0]
                        install_location = winreg.QueryValueEx(sub_key, 'InstallLocation')[0]
                        installed_software[display_name] = install_location
                    except EnvironmentError:
                        # 忽略无法找到 DisplayName 或 InstallLocation 的键值
                        pass

    return installed_software


def __dir__():
    pass


def __dict__():
    pass


if __name__ == "__main__":
    maya_locations = getMayaInsLocationDict()
    json_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ins_location", "maya_locations.json")
    # 强制更新json文件
    if maya_locations:
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(maya_locations, f, ensure_ascii=False, indent=4, default=lambda x: x.to_dict() if hasattr(x, "to_dict") else str(x))
        lprint(f"Maya安装位置信息已保存到: {json_file}")
    lprint(maya_locations)  # 同时在控制台显示结果
