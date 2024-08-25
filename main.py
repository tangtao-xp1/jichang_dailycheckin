import json
import os
import re
import requests
from datetime import datetime, timedelta


def get_config():
    """获取环境变量配置"""
    config = {
        'email': os.environ.get('EMAIL'),
        'passwd': os.environ.get('PASSWD'),
        'login_url': os.environ.get('LOGIN_URL', 'https://ikuuu.pw/auth/login'),
        'checkin_url': os.environ.get('CHECKIN_URL', 'https://ikuuu.pw/user/checkin'),
        'info_url': os.environ.get('INFO_URL', 'https://ikuuu.pw/user'),
        'SCKEY': os.environ.get('SCKEY'),
        'PUSHPLUS_TOKEN': os.environ.get('TOKEN')
    }

    if config['email'] is None or config['passwd'] is None:
        print('邮箱或密码为空，直接退出')
        exit(0)

    return config


def push(config, title, content):
    """根据配置推送信息"""
    sckey = config.get('SCKEY')
    pushplus_token = config.get('PUSHPLUS_TOKEN')

    if sckey:
        if push_sct(sckey, title, content):
            print('server酱推送成功')
        else:
            print('server酱推送失败')
    elif pushplus_token:
        if push_plus(pushplus_token, title, content):
            print('push_plus推送成功')
        else:
            print('push_plus推送失败')
    else:
        print('未配置token，跳过推送')


def push_sct(sckey, title, content):
    """server酱推送"""
    now_utc = date_format(datetime.utcnow())
    now_bj = date_format(datetime.utcnow() + timedelta(hours=8))
    content_with_timestamp = f"{now_bj}(UTC {now_utc}): {content}"
    url = "https://sctapi.ftqq.com/{}.send?title={}&desp={}".format(sckey, title, content_with_timestamp)
    response = requests.post(url)
    if response.status_code == 200:
        return True
    else:
        return False


def push_plus(plus_token, title, content):
    """pushplus推送"""
    now_utc = date_format(datetime.utcnow())
    now_bj = date_format(datetime.utcnow() + timedelta(hours=8))
    content_with_timestamp = f"{now_bj}(UTC {now_utc}): {content}"
    headers = {'Content-Type': 'application/json'}
    json_data = {"token": plus_token, 'title': title, 'content': content_with_timestamp, "template": "json"}
    resp = requests.post(f'http://www.pushplus.plus/send', json=json_data, headers=headers).json()
    if resp['code'] == 200:
        return True
    else:
        return False


def date_format(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')


def main():
    print('0.获取配置')
    # get_config()找不到配置会直接退出
    config = get_config()

    header = {
        'origin': 'https://ikuuu.pw',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    data = {
        'email': config['email'],
        'passwd': config['passwd']
    }
    try:
        print('1.登录')
        session = requests.session()
        response = json.loads(session.post(url=config['login_url'], headers=header, data=data).text)
        print(f"登录返回值：{response['msg']}")

        print('2.签到')
        result = json.loads(session.post(url=config['checkin_url'], headers=header).text)
        content = result['msg']
        print(f"签到返回值：{content}")

        print('3.剩余流量')
        info_html = session.get(url=config['info_url'], headers=header).text
        match = re.search(r'<h4>剩余流量</h4>[\s\S]*?<span class="counter">(\d+(\.\d+)?)</span>', info_html)
        remaining_num = 'NULL'
        if match:
            # 如果找到匹配项，group(1)会捕获括号内的内容
            remaining_num = match.group(1)
        print(f"剩余流量：{remaining_num}GB")
        content += f"，剩余流量{remaining_num}GB"

        print('4.推送')
        push(config, 'ikuuu签到成功', content)
    except Exception as e:
        content = '签到失败'
        print(content)
        print(e)
        push(config, 'ikuuu签到失败', content)
    finally:
        print('5.执行完毕')


if __name__ == '__main__':
    main()
