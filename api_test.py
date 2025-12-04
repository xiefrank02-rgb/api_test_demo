from csv import DictWriter
import pprint
import time
from typing import Any
import requests
import csv
import configparser
import uuid
import os

from urllib3.util import Url
config = configparser.ConfigParser()
config.read('config/config.ini', encoding='utf-8')

ENV = 'FAT'
def get_request_host(env) -> str:
    # 正确调用 get() 方法：参数1=节名，参数2=键名
    return config.get(env, 'host', fallback='127.0.0.1:8080')  # fallback 可选，防止键不存在报错

def get_api_name(env) -> str:
    # 正确调用 get() 方法：参数1=节名，参数2=键名
    return config.get(env, 'api_name', fallback='/calc/run')  # fallback 可选，防止键不存在报错

def get_biz_id(biz_line) -> int:
    # 正确调用 get() 方法：参数1=节名，参数2=键名
    return config.getint(biz_line, 'biz_id', fallback=5003)  




# 读取 users 和 vars 文本文件
def read_users_and_vars(users_file = './input/users.txt', vars_file = './input/vars.txt'):
    with open(users_file, "r") as user_file, open(vars_file, "r") as var_file:
        users = user_file.readlines()
        vars_list = var_file.readlines()
    
    # 移除换行符并返回
    users = [user.strip() for user in users]
    vars_list = [var.strip() for var in vars_list]
    return users, vars_list


# 批量请求 API 并写入 CSV
def batch_request_and_write_csv(users, vars_list, output_path):
    # 遍历 users 和 vars，发送请求
    for user in users:
        # 构造请求体
        data = req_data = {
            "appid": "string",
            "userid": int(user),
            "listingid": 0,
            "bizid": get_biz_id('TTCL'),
            "flowid": str(uuid.uuid4()),  # 生成UUID64
            "flowCount": 0,
            "debtid": 0,
            "vars": vars_list
            }
        
        try:
            # 发送请求
            Url = get_request_host(ENV)+get_api_name(ENV)
            print(Url)
            response = requests.post(Url , json=data)
            time.sleep(0.1)
            if response.status_code == 200:
                # 获取返回的数据
                result = response.json()  # 假设返回是 JSON 格式
                # pprint.pprint(result)
                for key,val in result.get("data", {}).get("ret", {}).items():
                    file_path = os.path.join(output_path, f"{key}.csv")  # 拼接完整路径（更安全）
                    file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
                    with open(output_path+key+".csv", "a", newline="", encoding="utf-8") as csvfile:
                        fieldnames = ["userId",key]  # 你可以根据返回的数据调整字段
                        writer: DictWriter[Any] = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        # 仅当文件不存在或为空时写入表头
                        if not file_exists:
                            writer.writeheader()
                        writer.writerow({"userId": user, key: val})
              
                print(f"成功处理用户 {user}，响应：{result}")
            else:
                print(f"请求失败，状态码：{response.status_code} 用户：{user}")
        
        except Exception as e:
            print(f"请求发生错误：{e} 用户：{user}")

# 主函数
def main():
    users_file = "input/users.txt"  # 用户列表文件
    vars_file = "input/vars.txt"  # 对应的 vars 文件
    output_path = "output/"  # 输出 CSV 文件名
    # 读取 users 和 vars 数据
    users, vars_list = read_users_and_vars(users_file, vars_file)
    # 批量请求并将结果写入 CSV
    batch_request_and_write_csv(users, vars_list, output_path)

if __name__ == "__main__":
    main()
