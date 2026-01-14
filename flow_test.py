from csv import DictWriter
import time
from typing import Any
import requests
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini', encoding='utf-8')

ENV = 'FAT'
def get_request_host(env) -> str:
    # 正确调用 get() 方法：参数1=节名，参数2=键名
    return config.get(env, 'risk_host', fallback='127.0.0.1:8080')  # fallback 可选，防止键不存在报错

def get_api_name(env) -> str:
    # 正确调用 get() 方法：参数1=节名，参数2=键名
    return config.get(env, 'pata_api', fallback='/api/runPata')  # fallback 可选，防止键不存在报错


def get_biz_id(biz_line) -> int:
    # 正确调用 get() 方法：参数1=节名，参数2=键名
    return config.getint(biz_line, 'biz_id', fallback=5003)  

def request():
    # 1. 构造请求体字典
    req_body = {
        "bizId": 5504,
        "userId": 17006720,
        "listingId": -1,
        "flowId": "env-hxc-1000005037-111@438c06bd-18bc-432f-8ac3-7a60327@16978456@3745812@5001@0",
        "isReentry": False
    }
    # 2. 构造请求头
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    try:
        # 发送请求
        Url = get_request_host(ENV)+get_api_name(ENV)
        print(Url)
        response = requests.post(Url , json=req_body)
        time.sleep(0.1)
        if response.status_code == 200 :
            # 获取返回的数据
            result = response.json()  # 假设返回是 JSON 格式
            msg = result.get("message","-1")
            if msg == "OK":
                print('*** 请求成功 ***')
                return
            else:
                print('*** 错误信息 ***')
                print(msg)
        else:
            print(f"请求失败，状态码：{response.status_code}")
    
    except Exception as e:
        print("请求发生错误")

# 主函数
def main():
    request()

if __name__ == "__main__":
    main()
