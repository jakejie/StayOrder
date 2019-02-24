# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:StayOrder
FileName = PyCharm
Version:1.0
CreateDay:2018/10/20 9:52
"""
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

try:
    from . import config
except Exception as im_err:
    try:
        import config
    except Exception as im_err:
        print("sent_email 包导入错误：{}".format(im_err))


# 邮件发送
class SendEmail(object):
    # 发送邮箱设置
    email_server = config.EMAIL_HOST
    from_address = config.EMAIL_HOST_USER
    password = config.EMAIL_HOST_PASSWORD

    def __init__(self, text, sender, receiver, subject, address):
        self.text = text
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.address = address
        self.to_address = address
        # 从上到下依次是: 邮件内容,邮件发送者昵称,邮件接收者昵称,邮件主题
        self.msg = MIMEText(self.text, 'plain', 'utf-8')
        self.msg['From'] = self.format_address(self.sender + '<' + self.from_address + '>')
        self.msg['To'] = self.format_address(self.receiver + '<' + self.to_address + '>')
        self.msg['Subject'] = Header(self.subject, 'utf-8').encode()

    # 编写了一个函数format_address()来格式化一个邮件地址
    @staticmethod
    def format_address(s):
        name, address = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), address))

    def send(self):
        try:
            # server = smtplib.SMTP(self.email_server, 25)  # 25是普通接口，465 SSL接口
            server = smtplib.SMTP_SSL(self.email_server, 465)
            # server.starttls()  # SSL要求这句
            server.set_debuglevel(1)
            server.login(self.from_address, self.password)
            server.sendmail(self.from_address, [self.to_address], self.msg.as_string())
            server.quit()
        except Exception as email_err:
            print("邮件发送失败：{}".format(email_err))


if __name__ == '__main__':
    # address_list = ["lucien33@live.com","rdvparis75015@gmail.com"]
    address_list = ['794564669@qq.com',]
    for add in address_list:
        send_email = SendEmail('这是一封测试邮件的中文内容', '这是来自RDV', '{}'.format(add), '恭喜 预约成功', add)
        send_email.send()
