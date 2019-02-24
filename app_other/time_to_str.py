# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:StayOrder
FileName = PyCharm
Version:1.0
CreateDay:2018/10/18 19:54
"""
import time
import datetime

if __name__ == '__main__':
    detester = "26/03/2019"
    date_1 = datetime.datetime.strptime("26/03/2019", "%d/%m/%Y")

    # date_1 = time.strftime("%d/%m/%Y".format("26/03/2019"))
    date_2 = datetime.datetime.strptime("2019-02-01", "%Y-%m-%d")
    print(date_1)
    print(date_2)
    print(date_2 > date_1)
    print(date_2 < date_1)
    date = "2018-09-21"
    date_3 = datetime.datetime.strptime("{}".format(date),  "%Y-%m-%d").strftime("%d/%m/%Y")
    print(date_3)
