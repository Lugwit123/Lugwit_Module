import json,codecs,re,sys
from typing import Literal

if __name__=="__main__":
    import json_read
else:
    from . import json_read


from typing import List, Dict, Any



def merge_dicts(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    
    for key,val in a.items():
        a[key]=b.get(key,val)
    return a


def merge_list_re(base_data: List[Dict[str, Any]], 
            update_data: Dict, special_key: str = "文件层级") -> List[Dict[str, Any]]:
    
    merged_list=[]
    for item_a in base_data:

        flattened_update_data_get_name = update_data.get(item_a['name'])
        if flattened_update_data_get_name:
            subs=item_a.get('subs')
            
            if subs:
                merge_list_re(subs,update_data)
            merged_list.append(merge_dicts(item_a,flattened_update_data_get_name))
            

    return merged_list

def merge_list(base_data: List[Dict[str, Any]], 
            update_data: List[Dict[str, Any]], special_key: str = "文件层级") -> List[Dict[str, Any]]:
    flattened_update_data = json_read.flatJsonDict(update_data)
    return merge_list_re(base_data, flattened_update_data, special_key)



if __name__ == '__main__':
    # 测试 merge_dicts_recursive 函数
    
    base = [{
        "value":"FileHierarchyA",
        "name": "FileHierarchy",
        "description": "文件层级_A",
        "zhName": "文件层级_A",
        "subs": [
            {   "value":"subsA", 
                "name": "name1",
                "description": "子项1描述_A",
                "zhName": "base_zhName_A",
                "subs": []
            },
            {   "value":"subs2018_A", 
                "name": "2018",
                "description": "mayaVesrsion",
                "zhName": "Maya版本",
                "subs": []
            },
            {   
                "value":"subs2_A", 
                "name": "name2",
                "description": "子项2描述",
                "zhName": "base_zhName2",
                "subs": []
            }
        ]
    }]
    baseJsonFile=r"A:\TD\RenderFarm\MayaToUE\data\base.json"
    # with codecs.open(baseJsonFile, 'r', 'utf-8') as f:
    #     base=json.load(f)
    # 示例更新字典
    update = [{
        "value":"FileHierarchyB",
        "name":"FileHierarchy",
        "description": "Updated 文件层级B",
        "zhName": "B",
        "subs": [
            {
                "value": "update_name_b",
                "name": "name1",
                "description": "子项1描述",
                "subs": []
            },
            {
                "value": "update_name_b",
                "name": "name3",
                "description": "子项3描述",
                "subs": []
            },
            {
                "value": "update_name_b",
                "name": "name33",
                "description": "子项3描述",
                "subs": []
            }
        ]
    }]
    jsonFileList=r"A:\TD\RenderFarm\MayaToUE\data\BKC_TL6.json"
    # with codecs.open(jsonFileList, 'r', 'utf-8') as f:
    #     update=json.load(f)
    # 指定要保留 base 字典值的键
    # 使用更新后的合并逻辑
    columnNameList=['name','description','zhName']
    columnNameList=['value','name','zhName']
    # Load the JSON files
    with codecs.open(baseJsonFile, 'r','utf-8') as file:
        base_dict = json.load(file)

    with codecs.open(jsonFileList, 'r','utf-8') as file:
        bkc_tl6_dict = json.load(file)

    # Merge the two dictionaries
    #merged_dict = merge_list(base_dict, bkc_tl6_dict)
    # 打印合并后的结果
    
    merged_dict = merge_list(base, update)



    
    print(json.dumps(merged_dict, indent=4, ensure_ascii=False))
