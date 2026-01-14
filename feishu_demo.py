import hashlib
import base64
import hmac
import time
import requests
import os
from dotenv import load_dotenv

# 加载 .env 文件内容到环境变量
load_dotenv()

# 获取变量
url = os.getenv("FEISHU_APP_URL")
secret = os.getenv("FEISHU_APP_SECRET")


def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')

    return sign


def get_timestamp()->int:
    current_timestamp = time.time()
    current_timestamp_int = int(current_timestamp)
    return current_timestamp_int

def send_feishu_msg():
    headers = {
    "Content-Type": "application/json"
    }
    timestamp = get_timestamp()
    data = {
    "timestamp": str(timestamp) ,      # 时间戳
    "sign": gen_sign(timestamp,secret=secret) , # 得到的签名字符串
    "msg_type": "text",
    "content": {
        "text": "签到成功!"
    }
   }
    try:
        response = requests.post(url=str(url), headers=headers, json=data)
        # 验证请求是否成功
        if response.status_code == 200:
            print("飞书消息发送成功")
        else:
            print(response.status_code)
    except Exception as e:
        print("请求异常:", str(e))


if __name__ == "__main__":
    send_feishu_msg()