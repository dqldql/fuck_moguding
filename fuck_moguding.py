import urllib.request as ur
import ssl
import json
import time
import requests


def load_login():
    with open('loginfo.json', 'r') as f:
        data = json.load(f)
        return data


def load_location():
    with open('location.json', 'r',encoding='utf-8') as f:
        data = json.load(f)
        return data

phone = load_login()['phone']
password = load_login()['password']
msg_type = load_login()['msg_type']
msg_token = load_login()['msg_token']

def qq_msg(text, msg_token):
    print("sending message.....")
    requests.get("https://qmsg.zendee.cn/send/" + msg_token + "?msg=" + text)


def get_planId(token,contexts):
    request_plan_id = ur.Request(
        url='https://api.moguding.net:9000/practice/plan/v1/getPlanByStu',
        data=json.dumps({"paramsType": "student"}).encode("utf-8"),
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8',
            'roleKey': 'student'
        }
    )

    try:
        plan_id = json.loads(ur.urlopen(request_plan_id, context=contexts).read().decode())['data'][0]['planId']
        # print(plan_id)
        if json.loads(ur.urlopen(request_plan_id, context=contexts).read().decode())['code'] == 200:
            return plan_id
        else:
            with open('~/fail.txt', 'a+') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '获取token失败\n')
    except Exception as e:
        pass


def sign_in(token, status, contexts, plan_id):
    data_dict = {
        "device": "WP",
        "planId": plan_id,
        "country": "中国",
        "address": load_location()['address'],
        "longitude": load_location()['longitude'],
        "city": load_location()['city'],
        "latitude": load_location()['latitude'],
        "province": load_location()['province'],
        "attendanceType": "",
        "type": status,
        "state": "NORMAL"
    }
    print(data_dict)
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
        "phone": phone,
        "password": password,
        "uuid": "",
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
        tokens = json.loads(ur.urlopen(request_login, context=context).read().decode())
        token = tokens['data']['token']
        if token:
            planid = get_planId(token, contexts)
            sign_in(token, type, context,planid)
    except Exception as e:
        datad = '<urlopen error Remote end closed connection without response>'
        if datad == str(e):
            print('网络连接超时')
            qq_msg("签到失败，原因：网络连接超时.当前时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),msg_token)
        else:
            print('账号或密码输入错误')
            qq_msg("签到失败，原因：账号或密码输入错误.当前时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),msg_token)
        pass


if __name__ == '__main__':

    while (True):
        print("------start---------")
        contexts = ssl._create_unverified_context()
        qq_msg("正在给傻逼蘑菇钉打个上班卡，当前时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg_token)
        login("START", contexts)
        time.sleep(15)
        qq_msg("正在给傻逼蘑菇钉打个下班卡，当前时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg_token)
        login("END", contexts)
        print("------stop----------")
        time.sleep(36000)
