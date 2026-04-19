# coding:utf-8
#添加模块所在路径
import os,re,sys,time

sys.path.append(os.environ.get('LugwitToolDir')+'/Lib')
from Lugwit_Module import *


proxies = {
  "http": None,
  "https": None,
}

sys.path.append(Lugwit_PluginPath+r'\Python\Python27\Lib\site-packages')

import os,sys,re,json
members ={u'所有人':'888888', 
          u'冯青青':'17710732019_fqq011', 
}


# at_member=[u'fqq', u'\u51af\u9752\u9752']
# at_telnum=[members[x].split('_')[0] for x in at_member]
# print (at_telnum)
token='https://oapi.dingtalk.com/robot/send?access_token='

def send_ding_message(message, at_member=None, is_at_all=False,url = 'c1597d5083ceac544dc2fd1253d2c3d6182623d0e9dfbf877e3620682ab5c406'):
    import requests,pypinyin
    url='https://oapi.dingtalk.com/robot/send?access_token=ca597d5083ceac544dc2fd1253d2c3d6182623d0e9dfbf877e3620682ab5c406'
    print ('url',url)
    at_telnum=[members[x].split('_')[0] for x in at_member]
    print ('at_telnum',at_telnum)

    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": at_telnum,
            "isAtAll":  '888888' in at_telnum , #是否艾特全体成员
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    st=time.time()
    i=0
    while 1:
        try:
            if time.time()-st>600:
                break
            res = requests.post(url, data=String_textMsg, headers=HEADERS)
            break
        except:
            i+=1
            print (u'发送钉钉消息超时,重试次数:{}'.format(i))
            time.sleep(5)
    print(res.text)
    return res.text


# ca597d5083ceac544dc2fd1253d2c3d6182623d0e9dfbf877e3620682ab5c406 公司群
# ca597d5083ceac544dc2fd1253d2c3d6182623d0e9dfbf877e3620682ab5c406 公司群
def send_markDown_message(title='',message='', at_member=None, is_at_all=False,
    url = 'ca597d5083ceac544dc2fd1253d2c3d6182623d0e9dfbf877e3620682ab5c406',
    ExFile_DingDingToken_File='',atDingTalkDictFile='',**kwargs):
    url='ca597d5083ceac544dc2fd1253d2c3d6182623d0e9dfbf877e3620682ab5c406'
    ExFile_DingDingToken_File=Lugwit_publicPath + r'/RenderFarm/DingDingQun/'+ExFile_DingDingToken_File+'.txt'
    return
    if os.path.exists(ExFile_DingDingToken_File):
        with open (ExFile_DingDingToken_File,'r') as f:
            url=f.read()
    import requests,pypinyin
    url=token+url


    if atDingTalkDictFile:

        with codecs.open(atDingTalkDictFile,'r',encoding='utf8') as f:
            atDingTalkDict=json.load(f)
            print ('atDingTalkDict',atDingTalkDict)
            message=atDingTalkDict.get('message',message)
            at_member=atDingTalkDict.get('at_member',at_member)
            lprint (at_member)
            title=atDingTalkDict.get('title',title) 

    at_telnum=[members[x].split('_')[0] for x in at_member]
    atStr=''
    for at in at_telnum:
        atStr+=u'@{at},'.format(at=at)

    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    atInMessageBottom='  \n  '
    for x in at_member:
        atInMessageBottom+=u'<font color=\"#0000FF\">@{}  </font>'.format(x)
    message+=atInMessageBottom
    String_textMsg = {
        "msgtype":"markdown",
        "markdown":{"title": title+atStr,
                    "text": message},

        "at": {
            "atMobiles": at_telnum,
            "isAtAll":  '888888' in at_telnum , #是否艾特全体成员
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    st=time.time()
    i=0
    while 1:
        try:
            if time.time()-st>4:
                break
            res = requests.post(url, data=String_textMsg, headers=HEADERS, proxies=proxies)
            break
        except:
            i+=1
            print (u'send_info,retimes {}'.format(i))
            time.sleep(.1)
    return res.text

if __name__=='__main__':
    import fire
    fire.Fire()
    #钉钉的消息换行符前后要有两个空格
#     at_member=[u'冯青青']
#     message=u'''
#     ## **自动导出资产文件**-->>

# 来自Maya文件://B003_S78/Asset_work/chars/Rig/B003_S78_chars_wuji_Rig.ma
# Maya文件日期:2022-07-21 19:55:56,用户:xnn029,更改列表:14325,版本列表:19
# Maya文件备注:添加眼高光控制器


#     ## **导出Tpose文件**-->>
#     ```pyhton
#     //B003_S78/Shot_work/UE/Tpose/chars_wuji_Tpose.fbx
#     ```
#     '''.replace('    ','')
    

#     #send_ding_message(u'自动message', at_member=[u'冯青青'],)
#     send_markDown_message(u"导出XX文件", message=message,at_member=at_member)