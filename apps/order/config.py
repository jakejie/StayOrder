#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# 数据库配置
db_user = 'root'
db_pawd = 'root'
db_host = '127.0.0.1'
db_port = 3306
db_name = 'stayorder'

# 邮件服务器配置
EMAIL_HOST = "smtp.yeah.net"
EMAIL_HOST_USER = "lucien33@yeah.net"
EMAIL_HOST_PASSWORD = "Chao5995139"

# 代理IP配置
USE_PROXY = True
#USE_PROXY = False
proxy_url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=cc8572bfede54fd6a025345a8bea58d1&orderno=YZ201811138921GjTfDN&returnType=2&count=1"  # 讯代理 代理ip提取地址
# REDIS配置 / 代理ip池
REDIS_HOST = "127.0.0.1"  # REDIS主机
REDIS_PORT = "6379"  # REDIS端口
REDIS_DB_PROXY = 12  # REDIS库
REDIS_DB_KEY = "proxy"  # REDIS 的 KEY

# 爬虫间隔时间
CRAWL_PERIOD = 1

# 超级鹰 配置
username = "lucien33"  # 超级鹰用户名
password = "chao5995139"  # 超级鹰密码
soft_id = "897751"  # 超级鹰 应用ID
