import urllib.request as ur
import ssl
import json
import time
import requests

qmsg_api = "CHANGE_TO_YOUR_OWN_QMSG_API"


def qq_msg(text, api):
    print("sending.....")
    print(requests.get("https://qmsg.zendee.cn/send/" + api + "?msg=" + text))


def sign_in(token, tpye, contexts):
    data_dict = {
        "device": "WP",
        "planId": "CHANGE_TO_YOUR_PLAN_ID",
        "country": "中国",
        "address": "河南省 · 郑州市 · 河南省教育厅",
        "longitude": "113.759339",
        "city": "郑州市",
        "latitude": "34.77359",
        "province": "河南省",
        "attendanceType": "",
        "type": "START",
        "state": "NORMAL"
    }
    url = 'https://api.moguding.net:9000/attendence/clock/v1/save'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
        'roleKey': 'student'
    }
    data = json.dumps(data_dict)
    mgd_requests = ur.Request(url=url, data=data.encode("utf-8"), headers=headers)
    try:
        if json.loads(ur.urlopen(mgd_requests, context=contexts).read().decode())['code'] == 200:
            pass
        else:
            with open('~/fail.txt', 'a+') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '签到失败\n')
    except Exception as e:
        pass


def login(type, context):
    login_data = {
        "phone": "CHANGE_TO_YOUR_PHONE",
        "password": "CHANGE_TO_YOUR_PASSWORD",
        "loginType": "WP"
    }
    request_login = ur.Request(
        url='https://api.moguding.net:9000/session/user/v1/login',
        data=json.dumps(login_data).encode(),
        headers={
            'Content-Type': 'application/json; charset=UTF-8'
        }
    )
    try:
        token = json.loads(ur.urlopen(request_login, context=context).read().decode())['data']['token']
        if token:
            sign_in(token, type, context)
    except Exception as e:
        datad = '<urlopen error Remote end closed connection without response>'
        if datad == str(e):
            # print('网络连接超时')
            qq_msg("签到失败，原因：网络连接超时.当前时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            # print('账号或密码输入错误')
            qq_msg("签到失败，原因：账号或密码输入错误.当前时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        pass


if __name__ == '__main__':
    while (True):
        print("------start---------")
        context = ssl._create_unverified_context()
        qq_msg("正在给傻逼蘑菇钉打个上班卡，当前时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), qmsg_api)
        login("START", context)
        time.sleep(15)
        qq_msg("正在给傻逼蘑菇钉打个下班卡，当前时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), qmsg_api)

        login("END", context)
        print("------stop----------")
        time.sleep(36000)
