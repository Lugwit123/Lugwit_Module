# coding:utf-8
import json,os,codecs

def process_item(item):
    # 初始化结果字典
    result = {}
    if isinstance(item, dict):
        for k, v in item.items():
            # 如果当前键是'name'，则创建所需的结构
            if k == 'name' and isinstance(v, str):
                result[v] = {
                    "value": item.get('value', None),
                    "zhName": item.get('zhName', None),
                    "valueType": item.get('valueType', None)
                }
            else:
                # 递归处理每个子项
                processed_item = process_item(v)
                if processed_item:
                    result.update(processed_item)
    elif isinstance(item, list):
        # 对列表中的每个元素递归处理
        for elem in item:
            processed_item = process_item(elem)
            if processed_item:
                result.update(processed_item)
    return result

def update_value_by_name(data, name, new_value):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == 'name' and v == name:
                data['value'] = new_value
            elif isinstance(v, (dict, list)):
                update_value_by_name(v, name, new_value)
    elif isinstance(data, list):
        for item in data:
            update_value_by_name(item, name, new_value)

def flatJsonDict(file_path):
    # 读取和处理 JSON 数据
    if isinstance(file_path, str):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = file_path

    result_dict = process_item(data)

    return result_dict


def flatDict(file_path):
    # 读取和处理 JSON 数据
    if isinstance(file_path, str):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = file_path

    return flatten_dict(data)


def flatten_dict(d, items={}):

    if isinstance(d, dict):
        for k, v in d.items():
            if not isinstance(v, dict):
                items[k]=v
            else:
                flatten_dict(v, items)
    elif isinstance(d, list):
        for v in enumerate(d):
            if isinstance(v, dict):
                for k, v in v.items():
                    if not isinstance(v, dict):
                        items[k]=v
                    else:
                        flatten_dict(v, items)


    return items


if __name__=="__main__":
    # _ = flatDict(r'A:\TD\RenderFarm\MayaToUE\data\ZX.json')
    # print (json.dumps(_,indent=2,ensure_ascii=False))
    _ = flatDict(r'A:\TD\Temp\MayaToUE\ExHis\XSSDTYRC\PC-20240202CTEU\exAniClip_ep001_sc001_shot0280_anim_comment.json')
    print (json.dumps(_,indent=2,ensure_ascii=False))
    