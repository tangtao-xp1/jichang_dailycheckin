import json
import os
from datetime import datetime, timedelta
import re

import requests

print('0.获取环境变量')
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')

if email is None or passwd is None:
    print('邮箱和密码为空，直接退出')
    exit(0)

login_url = os.environ.get('LOGIN_URL', 'https://ikuuu.pw/auth/login')
checkin_url = os.environ.get('CHECKIN_URL', 'https://ikuuu.pw/user/checkin')
info_url = os.environ.get('INFO_URL', 'https://ikuuu.pw/user')

# server酱
SCKEY = os.environ.get('SCKEY')
# PUSHPLUS
Token = os.environ.get('TOKEN')
session = requests.session()

def date_format(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def push(title, content):
    if SCKEY != '1':
        # 为content增加时间戳
        now_utc = date_format(datetime.utcnow())
        now_bj = date_format(datetime.utcnow() + timedelta(hours=8))
        content_with_timestamp = f"{now_bj}(UTC {now_utc}): {content}"
        url = "https://sctapi.ftqq.com/{}.send?title={}&desp={}".format(SCKEY, title, content_with_timestamp)
        requests.post(url)
        print('推送完成')
    elif Token != '1':
        # 为content增加时间戳
        now_utc = date_format(datetime.utcnow())
        now_bj = date_format(datetime.utcnow() + timedelta(hours=8))
        content_with_timestamp = f"{now_bj}(UTC {now_utc}): {content}"
        headers = {'Content-Type': 'application/json'}
        json = {"token": Token, 'title': title, 'content': content_with_timestamp, "template": "json"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')
    else:
        print('未使用消息推送推送！')


header = {
    'origin': 'https://ikuuu.pw',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
data = {
    'email': email,
    'passwd': passwd
}
try:
    print('1.登录')
    response = json.loads(session.post(url=login_url, headers=header, data=data).text)
    print(f"登录返回值：{response['msg']}")

    print('2.签到')
    result = json.loads(session.post(url=checkin_url, headers=header).text)
    print(f"签到返回值：{result['msg']}")
    content = result['msg']
    
    print('3.剩余流量')
    info_html = session.get(url=info_url, headers=header).text
    match = re.search(r'<h4>剩余流量</h4>[\s\S]*?<span class="counter">(\d+(\.\d+)?)</span>', info_html)
    remaining_num = 'NULL'
    if match:
        # 如果找到匹配项，group(1)会捕获括号内的内容
        remaining_num = match.group(1)
    print(f"剩余流量：{remaining_num}GB")
    content += f"，剩余流量{remaining_num}GB"
    
    print('4.推送')
    push('ikuuu签到成功', content)
except exception as e:
    content = '签到失败'
    print(content)
    print(e)
    push('ikuuu签到失败', content)
finally:
    print('5.执行完毕')
