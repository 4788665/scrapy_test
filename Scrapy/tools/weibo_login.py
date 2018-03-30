#!D:\5.Python\python.exe
#coding:utf-8

import requests
import json
import base64
#import re
#import rsa
#import binascii




def weibo_login(username_ori, password):
    username = base64.b64encode(username_ori.encode('utf-8')).decode('utf-8')
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    session = requests.Session()
    res = session.post(loginURL, data = postData)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    print 'info:', info
    if info["retcode"] == "0":
        print(u"新浪微博登录成功, 用户名[%s]" % username_ori)
        # 把cookies添加到headers中，必须写这一步，否则后面调用API失败
        cookies = session.cookies.get_dict()
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        session.headers["cookie"] = cookies
        session.info = info
    else:
        print("登录失败，原因： %s" % info["reason"])
        return None
#    print session.__dict__
    return session

if __name__ == '__main__':
    session = weibo_login('keepmemory@sina.com', '1qaz3edc')
    
