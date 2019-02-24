#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import datetime
from sqlalchemy import Column, String, create_engine, DateTime, Integer, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

try:
    from .config import db_host, db_user, db_pawd, db_name, db_port
except Exception as im_err:
    try:
        from config import db_host, db_user, db_pawd, db_name, db_port
    except Exception as im_err:
        print("source文件包导入异常：{}".format(im_err))
# 创建对象的基类:
Base = declarative_base()


# 爬虫任务列表
class OrderModel(Base):
    # 表的名字: 和django中的任务表 映射
    __tablename__ = 'users_crawltaskmodel'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    user_id = Column(String, default="")  # 所属用户
    # 以下参数用户填写 只需要读取
    name = Column(String(64), default="")  # 姓氏
    username = Column(String(64), default="")  # 名字
    birthday_date = Column(DATE, default="")  # 出生日期
    stay_num = Column(String(32), default="")  # 居留许可证号码
    stay_end_date = Column(DATE, default="")  # 许可证到期时间
    town = Column(String(32), default="", )  # 镇 数字
    start_date = Column(DATE, default="")  # 开始时间
    end_date = Column(DATE, default="")  # 结束时间
    access_email = Column(String(32), default="0")  # 接收预定结果的邮箱
    # 以上八个参数必填
    order_status = Column(String(32), default="0")  # 预约状态 ('0', '预约中'),('1', '预约成功'),('2', '预约失败'),
    stay_date = Column(DateTime, default="")  # 使用爬虫 预约成功的日期、时间
    success_time = Column(DateTime, default="")  # 使用爬虫 预约成功的日期、时间
    stay_address = Column(String(512), default="")  # 预约到的地方
    add_time = Column(DateTime, default=datetime.datetime.now)
    recommend = Column(String(256))  # 备注


class Pipeline(object):
    def __init__(self):  # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'
                               .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
        # 创建DBSession类型:
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    # 获取所有待预约的用户
    def get_wait_user(self):
        wait_crawl = []
        try:
            self.session.commit()
            wait_crawl = self.session.query(OrderModel).filter(OrderModel.order_status == '0').all()
        except Exception as e:
            print("查询用户失败{}".format(e))
            self.session.rollback()
        return wait_crawl

    # 更改预约状态
    def insert_status(self, model_id, order_status, stay_date, stay_address, recommend):
        try:
            self.session.commit()
            if order_status == "1":
                success_time = datetime.datetime.now()
            else:
                success_time = None
            self.session.query(OrderModel).filter(OrderModel.id == model_id) \
                .update({OrderModel.order_status: '{}'.format(order_status),
                         OrderModel.stay_date: stay_date,
                         OrderModel.stay_address: stay_address,
                         OrderModel.recommend: recommend,
                         OrderModel.success_time: success_time}, )
            self.session.commit()
        except Exception as e:
            print("查询用户失败{}".format(e))
            self.session.rollback()

    # 更新最新预约时间
    def update_recommend(self, model_id, recommend, order_status):
        try:
            print("更新最新预约时间")
            self.session.commit()
            self.session.query(OrderModel).filter(OrderModel.id == model_id) \
                .update({OrderModel.recommend: recommend,
                         OrderModel.stay_date: None,
                         OrderModel.order_status: order_status,
                         OrderModel.stay_address: ""}, )
            self.session.commit()
        except Exception as e:
            print("更新最新预约时间失败 {}".format(e))
            self.session.rollback()
