# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:StayOrder
FileName = PyCharm
Version:1.0
CreateDay:2018/10/20 14:23
"""

import datetime
import pytz

if __name__ == "__main__":
    d = datetime.datetime.now()
    # tz = pytz.timezone('Europe/Paris')
    p = str(datetime.datetime.now(pytz.timezone('Europe/Paris')))  # 巴黎当前时间
    print("中国时间：{} 巴黎时间：{}".format(d, p))

    p = datetime.datetime.strptime("{}".format(p), "%Y-%m-%d %H:%M:%S")

    # pa = tz.localize(d)
    # print(pa)

    pa_2 = datetime.datetime.strptime("{}".format("2018-10-20 14:00:00"), "%Y-%m-%d %H:%M:%S")
    print(pa_2)
    print(p > pa_2)
