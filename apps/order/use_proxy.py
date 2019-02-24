# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:StayOrder
FileName = PyCharm
Version:1.0
CreateDay:2018/10/19 16:51
"""
import sys
import json
import redis
import requests

try:
    from .config import REDIS_HOST, REDIS_PORT, REDIS_DB_PROXY, REDIS_DB_KEY, USE_PROXY, proxy_url
except Exception as im_err:
    try:
        from config import REDIS_HOST, REDIS_PORT, REDIS_DB_PROXY, REDIS_DB_KEY, USE_PROXY, proxy_url
    except Exception as im_err:
        print("use_proxy文件 包导入异常：{}".format(im_err))
        sys.exit(1)


class ProxyPoolInfo(object):
    def __init__(self):
        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_PROXY, )
        self.redis_conn = redis.Redis(connection_pool=pool, )

    # 判断是否有代理可用
    def have_proxy(self):
        # 判断代理池中是否有可用IP
        redis_ip = self.redis_conn.scard(REDIS_DB_KEY)  # 获取代理池中代理的长度
        if redis_ip:
            # 从代理池随机取IP并返回
            proxy_ip_port = self.redis_conn.spop(REDIS_DB_KEY).decode('utf-8')  # 获取任意一个元素
            self.redis_conn.sadd(REDIS_DB_KEY, proxy_ip_port)  #
            return proxy_ip_port
        else:
            return False

    # 获取代理IP
    def create_proxy(self):
        while True:
            if USE_PROXY:
                my_proxy = self.have_proxy()  # 判断是否有可用代理
                if not my_proxy:
                    proxy_resp = requests.get(proxy_url)
                    print("代理ip：{}".format(proxy_resp.text))
                    proxy_text = json.loads(proxy_resp.text)
                    for all_proxy in proxy_text["RESULT"]:
                        proxy_ip = all_proxy["ip"]
                        proxy_port = all_proxy["port"]
                        proxy_ip_port = proxy_ip + ":" + proxy_port
                        # 将取到的IP放入到Redis池
                        self.redis_conn.sadd(REDIS_DB_KEY, proxy_ip_port)  # 新获取到的代理放入代理池
                else:
                    return my_proxy
            else:
                proxy_ip_port = ""
                return proxy_ip_port

    # 移除不可用代理IP
    def remove_proxy(self, proxy):
        self.redis_conn.srem(REDIS_DB_KEY, proxy)


if __name__ == '__main__':
    proxy = ProxyPoolInfo()
    proxy.create_proxy()
