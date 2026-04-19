#! /bin/env python
# -*- coding: utf-8 -*-
# import sys,os
# import json,time
# from dingtalk import SecretClient, AppKeyClient
# if sys.version_info.major <= 2:
#     print("not support python2")
#     sys.exit(0)

# import urllib.request as request
# import urllib.parse
# import requests

# APP_KEY = "dingotu1klzvtdbzpqtr"
# APP_SECRET = "l7bYkJ0i5RzTDaqOA97TvzIKM1iX9iKZdWCKEdq9pyFHwO07z7Zd11Zc1g6YL_pd"
# AGENT_ID = '1652699035'

# app_key = "dingtmfcbltdioji8xsc"
# app_secret = "Kl8gIgoGBURRKQaD5cY3SozebESRsxzZEdvUgb8wN7dxQXp4LvBiVs2_7iAGjChX"
# corp_id = "13453001"

# client = AppKeyClient(corp_id=AGENT_ID, app_key=APP_KEY, app_secret=APP_SECRET)

# def get_access_token():
#     req = request.urlopen('https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (APP_KEY, APP_SECRET))
#     res = req.read().decode('utf-8')
#     data = json.loads(res)
#     if data["errcode"] == 0:
#         return data["access_token"]
#     else:
#         return None

# def get_userid(access_token, mobile):
#     req = request.urlopen('https://oapi.dingtalk.com/user/get_by_mobile?access_token=%s&mobile=%s' % (access_token, mobile))
#     res = req.read().decode('utf-8')
#     data = json.loads(res)
#     print ('data->',data)
#     if data["errcode"] == 0:
#         return data["userid"]
#     else:
#         return None
    
# def get_chatid(access_token):
#     if os.path.exists('D:/aa.txt'):
#         with open('D:/aa.txt','r') as f:
#             if f:
#                 return f.read()
    
#     url = 'https://oapi.dingtalk.com/chat/create?access_token=%s' % access_token
#     data = {

#     "name": "测试发送消息",
#     "owner": get_userid(access_token, '17710732019'),
#     "useridlist": [get_userid(access_token, '17710732019')],
#     }
#     data   = json.dumps(data)
#     req    = requests.post(url, data)
#     req_text = json.loads(req.text)
#     chatid=req_text['chatid']
#     print ('req_textd',req_text)
#     with open('D:/aa.txt','w') as f:
#         if f:
#             f.write(chatid)
#     return chatid

# def post_message(userid, access_token):
#     msg = {}
#     msg["userid_list"] = userid
#     msg["agent_id"] = AGENT_ID
#     msg["msg"] = {}
#     msg["msg"]["msgtype"] = "text"
#     msg["msg"]["text"] = {}
#     msg["msg"]["text"]["content"] = "This is a test message2!"
#     msg["msg"]["text"]["at"]=["17710732019"]
#     postData = urllib.parse.urlencode(msg)
#     postData = postData.encode('utf-8')
#     res = request.urlopen('https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' % access_token, postData)
#     result = res.read()
#     print(result)


# data = {
#     "msgtype": "text",
#     "text": {
#         # 要发送的内容【支持markdown】【！注意：content内容要包含机器人自定义关键字，不然消息不会发送出去，这个案例中是test字段】
#         "content": 'content'
#     },
#     "at":{
#         # 要@的人
#         "atMobiles": '17710732019',
#         # 是否@所有人
#         "isAtAll": False
#     }
# }

# def getMedia_id():
#     #需要先上传文件，获取文件的 media_id
#     access_token = get_access_token()  
#     # 获取要推送文件的路径
#     # path = os.getcwd()
#     # file = os.path.join(path, '文件名')
#     file = r'E:\BUG_Project\B024\Shot_work\UE\shot_19\B024_shot19_1001_1050.mov'  
#     url = 'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
#     files = {'media': open(file, 'rb')}
#     data = {'access_token': access_token,
#             'type': 'file'}
#     response = requests.post(url, files=files, data=data)
#     json = response.json()
#     print(json)
#     return json["media_id"]

# def SendFile():
#     access_token = get_access_token()  
#     media_id = getMedia_id()
#     chatid =  get_chatid(access_token)
#     url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
#     header = {
#         'Content-Type': 'application/json'
#     }
#     data = {'access_token': access_token,
#             'chatid': chatid,
#             'msg': {
#                     'msgtype': 'file',
#                     'file': {'media_id': media_id},
#                     # "at":{"atMobiles": '17710732019',"isAtAll": False},
#             }       }
#     r = requests.request('POST', url, data=json.dumps(data), headers=header)
#     print(r.json())


# def tonews(access_token, chatid, content):
#     '''
#     chatid  : 群组id
#     msgtype : 类型
#     content : 内容
#     '''
#     chatid=chatid
#     url    = "https://oapi.dingtalk.com/chat/send?access_token=%s" % access_token
#     msgtype = 'text'
#     values  = {
#     "chatid": chatid,
#     "msgtype": msgtype,
#     msgtype: {"content": content},
    
#     "at":{"atUserIds": [get_chatid(access_token)]},
#     }
#     print ('get_chatid',get_chatid(access_token))
#     values = json.dumps(values)
#     data   = requests.post(url, values)
#     errmsg = json.loads(data.text)['errmsg']
#     if errmsg == 'ok':
#         return "ok"
#     # useridB='015135413127101638'
#     # client.message.send_to_conversation(sender=useridB,cid=chatid ,msg_body=values)
#     return "fail: %s" % data.text

# if __name__ == '__main__':
#     access_token = get_access_token()
#     print (access_token)
#     userid = get_userid(access_token, "17710732019")
#     print (userid)
#     chatid = get_chatid(access_token)
#     content = '\\\\\\\\n'.join(['AA','CC',str(time.time())])
#     if not content:
#         content = '测试'
#     #print (tonews(access_token, chatid, content))
#     SendFile()
    