# coding=utf-8
import sys

if sys.version[0]=="2":
    class Enum():
        name = ""
else:
    from enum import Enum
import json

def custom_serialize(obj, indent=4, level=0):
    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            if isinstance(value, dict):
                serialized_value = custom_serialize(value, indent, level + 1)
            elif isinstance(value, (list, tuple)):
                serialized_value = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
            elif isinstance(value, (Enum)):
                serialized_value = '"'+value.name+'"'
            else:
                serialized_value = json.dumps(value, ensure_ascii=False)
            space = ' ' * indent * level
            items.append(u'{space}"{key}": {serialized_value}'.format(space=space, key=key, serialized_value=serialized_value))
        return u'{\n' + u',\n'.join(items) + u'\n' + u' ' * indent * (level - 1) + u'}'
    return json.dumps(obj, ensure_ascii=False)


def flatten_dict(dd, levels=None, current_level=0):
    """
    这个函数会将给定层级的字典进行塌陷，将其下一层级的内容上升一级。
    
    参数:
        dd (dict): 需要塌陷的字典
        levels (list): 需要塌陷的层级列表，列表中的数字表示层级数（顶层为0）
        current_level (int): 当前的层级（默认为0，表示顶层）

    返回:
        dict: 塌陷后的字典
    """
    # 如果当前处理的对象是字典
    if isinstance(dd, dict):
        # 如果当前层级在需要塌陷的层级列表中
        if current_level in levels:
            new_dict = {}
            # 遍历当前字典的所有键值对
            for k, v in dd.items():
                # 如果值是字典，将其内容添加到新字典中
                if isinstance(v, dict):
                    new_dict.update(v)
            # 递归处理新字典，当前层级+1
            return flatten_dict(new_dict, levels, current_level + 1)
        else:
            # 如果当前层级不在需要塌陷的层级列表中
            # 递归处理当前字典的每一个值，返回处理后的字典
            return {k: flatten_dict(v, levels, current_level + 1) for k, v in dd.items()}
    else:
        # 如果当前处理的对象不是字典，直接返回
        return dd

# 将字典保存到文件
if __name__ == '__main__':
    my_dict = {
        "ExSetingDict": {
        "genUeProject": False,
        "exDirSetToMayaFileDir": False,
        "waterMarkFile": "A:\\FQQ\\icon\\WaterMark\\waterMask_1440_810.png",
        "Resolution": ["1440", "810"],
        "ueVersion": "5.0",
        "GeometryGroup": "geometry",
        "JntGroup": "UnrealRoot",
        "infoFromMayaFilePath_MathDictParm": {
            "assetDir": "",
            "ShotEpName": "EP107",
            "AssetEpName": "EP107",
            "ScName": "SC002",
            "AssetType": "",
            "ProjectName": "Cosmos_Wartale",
            "ProjectDir": "Z:/Cosmos_Wartale/03_Main-Production",
            "shotDir": "Z:/Cosmos_Wartale/03_Main-Production/05_animation/",
            "AssetStep": "",
            "AssetName": "Animation",
            "ShotStep": "Animation",
            "ShotName": "",
            "shotName": "EP107_SC002",
            "AssetDir": "",
            "infoFile": "",
            "JntGroup": "",
            "GeometryGroup": "",
            "workType": "Shot",
            "FinalShotName": "EP107_SC002"
    }}}
    print (custom_serialize(my_dict))