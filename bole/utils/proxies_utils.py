import time
import random
import requests

from pymongo import MongoClient
from bole.utils import db_utils

db_config = db_utils.DBConfig()
db_cln = db_config.mongo_connect(connect_type="auth", env="prod", name="xc_cln")
mongodb_proxies = db_cln["proxies"]


def get_proxies_mongodb():
    web_datas = requests.get("http://mvip.piping.mogumiao.com/proxy/api/get_ip_bs?appKey=20407858270742469d23aeacc77"
                             "edd44&count=10&expiryDate=0&format=2&newLine=2").text
    ip_list = web_datas.split("\r\n")[:10]
    for ip in ip_list:
        ip = "http://" + ip
        ip = {"http": ip}
        post = {"proxies": ip}
        mongodb_proxies.insert(post)


def judge_proxies(proxies):
    url = "http://www.baidu.com"
    try:
        response = requests.get(url, proxies=proxies, timeout=2)
    except Exception as e:
        print("删除无用IP")
        delete_ip(proxies)
        return False
    else:
        code = response.status_code
        if 200 <= code < 300:
            print("IP验证成功")
            return proxies
        else:
            print("删除无用IP")
            delete_ip(proxies)
            return False


def delete_ip(ip):
    mongodb_proxies.delete_one({'proxies': ip})
    return True


def get_proxies_out():
    for i in range(10):
        try:
            ips = list(mongodb_proxies.find())
            ip = random.choice(ips)["proxies"]
            return ip
        except:
            continue


if __name__ == "__main__":
    while 1:
        try:
            ip_list = list(mongodb_proxies.find())
            if len(ip_list) <= 20:
                get_proxies_mongodb()
            ip_list = list(mongodb_proxies.find())
            for ips in ip_list:
                try:
                    ip = ips["proxies"]
                    print(ip)
                    judge_proxies(ip)
                except:
                    pass
            with open('proxies.txt', 'w') as f:
                for ip_info in list(mongodb_proxies.find()):
                    f.write(str(ip_info["proxies"]["http"]) + '\n')
            time.sleep(2)
        except Exception as e:
            print(e)
            time.sleep(2)
            continue
        finally:
            print("重新开始验证+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")