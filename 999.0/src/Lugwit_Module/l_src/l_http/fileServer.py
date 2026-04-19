import requests
from requests.auth import HTTPBasicAuth

def uploadFile(file_path = r"D:\TD_Depot\plug_in\Lugwit_plug\CodeEncryption\CodeEncryptionUI.py"):
    # 服务器地址
    url = "http://159.75.180.127:7890/upload"

    # HTTP Basic Auth的用户名和密码
    username = "GSM"
    password = "666"

    # 打开文件并上传
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        response = requests.post(url, files=files, auth=HTTPBasicAuth(username, password))

    # 输出服务器响应
    print(response.json())
