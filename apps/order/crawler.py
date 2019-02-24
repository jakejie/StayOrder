# -*- coding:utf-8 -*-
import sys
import time
import datetime
import requests
from lxml import etree
import urllib3

# 忽略证书
urllib3.disable_warnings()
# 是否显示print打印信息
DEBUG = True
try:
    from . import image_code
    from . import config
    from . import sent_email
    from .source import Pipeline
    from .. import log_tool
    from .use_proxy import ProxyPoolInfo
except Exception as im_err:
    try:
        import image_code
        import config
        import sent_email
        from source import Pipeline
        import log_tool
        from use_proxy import ProxyPoolInfo
    except Exception as im_err:
        print("crawler文件 包导入异常:{}".format(im_err)) if DEBUG else ""
        sys.exit(1)


# requests.get()

class StaySpider(Pipeline, ProxyPoolInfo):
    def __init__(self):
        Pipeline.__init__(self)
        ProxyPoolInfo.__init__(self)
        self.start_url = 'https://www.ppoletrangers.interieur.gouv.fr/?motif=renetu'  # 请求首页
        self.first_url = 'https://www.ppoletrangers.interieur.gouv.fr/?page=ident'  # 第一次验证身份信息 提交表单
        self.second_url = 'https://www.ppoletrangers.interieur.gouv.fr/?page=rdv+post'  # 第二次提交信息
        self.generate_image_url = 'http://www.ppoletrangers.interieur.gouv.fr/xhr/rcaptcha.php'  # 這是产生验证码url的链接
        self.header = {
            'Upgrade-Insecure-Requests': '1',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/67.0.3396.99 Safari/537.36',
            'Host': 'www.ppoletrangers.interieur.gouv.fr'
        }

    # 入口函数
    def start_requests(self):
        # 读取待爬用户列表
        wait_user = self.get_wait_user()
        if wait_user:
            print("当前总用户数：{}".format(len(wait_user))) if DEBUG else ""
            for user in wait_user:
                local_date = datetime.datetime.now()
                date_end = datetime.datetime.strptime("{}".format(user.end_date), "%Y-%m-%d")
                print("当前时间：{}  最后时间：{}".format(local_date, date_end)) if DEBUG else ""
                if local_date < date_end:
                    session = requests.Session()
                    # 提交基本信息 表单
                    from_data1 = {
                        'agdref': user.stay_num,
                        'naissance': self.trans_date(user.birthday_date),
                        'nom': user.name,
                        'prenom': user.username,
                        'validite': self.trans_date(user.stay_end_date), }
                    # 选择国家/镇 第二次 表单
                    from_data2 = {
                        'arrdt': user.town,
                        'nationalite': '47',
                        'nom': user.name,
                        'prenom': user.username,
                        'pays': '137',
                    }
                    # 预约的时候使用表单 两个默认值
                    from_data3 = {
                        "arrdt": '{}'.format(user.town),
                        "pays": '137',
                    }

                    # 请求首页
                    start_res, session = self.get_response(
                        session=session, url=self.start_url, method="GET", headers=self.header)
                    # 第一次验证身份信息
                    self.header.update({'Referer': start_res.url})
                    first_res, session = self.get_response(
                        session=session, url=self.first_url, method="POST", headers=self.header, data=from_data1)
                    # 已经预约过了
                    if 'Annuler le rdv' in first_res.text:
                        first_tree = etree.HTML(first_res.text)
                        print('您已经预约过了') if DEBUG else ""
                        stay_date = ''.join(first_tree.xpath(
                            '//div[@id="vue"]/div[2]/text()[2]')).replace('Vous avez pris rdv le', '').strip()
                        stay_date = self.trans_date2(stay_date=stay_date)
                        stay_address = ''.join(first_tree.xpath('//*[@id="vue"]/div[2]/fieldset/text()')).strip()
                        self.insert_status(model_id=user.id, order_status="1",
                                           stay_date=stay_date, stay_address=stay_address,
                                           recommend="预约成功！")
                        log_tool.test_log("爬虫系统", "预约成功", "您已经预约过了", "预约时间：{} 预约地点：{}"
                                          .format(stay_date, stay_address))
                        # 发送邮件提醒
                        if user.access_email:
                            email_content = "{} {} 可居留时间：{},地点：{}".format(user.name, user.username,
                                                                          stay_date, stay_address)  # 邮件正文内容
                            email_title = "居留预约成功"  # 邮件标题
                            email_accept_user_name = user.name + user.username  # 邮件收件人用户名
                            email_object = "您的居留申请预约成功"  # 邮件主题
                            email_accept = user.access_email  # 邮件收件箱
                            send_email = sent_email.SendEmail(email_content,
                                                              email_title,
                                                              email_accept_user_name,
                                                              email_object,
                                                              email_accept)
                            send_email.send()
                    # 验证不通过
                    elif "nous permettent pas de vous identifier" in first_res.text:
                        stay_date = None  # datetime.datetime.now()
                        stay_address = '无'
                        self.insert_status(model_id=user.id, order_status="2",
                                           stay_date=stay_date, stay_address=stay_address,
                                           recommend="验证信息不通过!")
                        print('验证信息不通过！！！') if DEBUG else ""
                        log_tool.test_log("爬虫系统",
                                          "预约失败",
                                          "验证信息不通过",
                                          "验证信息异常")
                    # 不正确的居留许可证号码 格式
                    elif 'du titre de s&eacute;jour incorrect' in first_res.text:
                        stay_date = None  # datetime.datetime.now()
                        stay_address = '无'
                        self.insert_status(model_id=user.id, order_status="2",
                                           stay_date=stay_date, stay_address=stay_address,
                                           recommend="不正确的居留许可证号码")
                        print('不正确的居留许可证号码！') if DEBUG else ""
                        log_tool.test_log("爬虫系统",
                                          "预约失败",
                                          "不正确的居留许可证号码",
                                          "验证信息异常")
                    # 不正确的日期格式
                    elif 'date de naissance incorrecte' in first_res.text \
                            or "date d'expiration incorrecte" in first_res.text:
                        stay_date = None  # datetime.datetime.now()
                        stay_address = '无'
                        self.insert_status(model_id=user.id, order_status="2",
                                           stay_date=stay_date, stay_address=stay_address,
                                           recommend="不正确的日期格式")
                        print('不正确的日期格式！') if DEBUG else ""
                        log_tool.test_log("爬虫系统",
                                          "预约失败",
                                          "不正确的日期格式",
                                          "验证信息异常")
                    # 身份验证通过
                    elif "Arrondissement" in first_res.text:
                        # 第二次提交信息,查询预约信息
                        session, detail_times_value, date, second_res, use_date_list = self.query(
                            user=user, session=session, first_res=first_res, from_data2=from_data2)
                        # 循环后是否有预约信息
                        if detail_times_value and date:
                            # 开始去预约
                            self.pre_meet(user=user, session=session, second_res=second_res,
                                          from_data3=from_data3, detail_times_value=detail_times_value, date=date)
                        else:
                            # 将当前可预约的最前面一个时间更新到数据库
                            print(use_date_list)
                            if use_date_list:
                                date = use_date_list[0][0]
                            else:
                                date = "无最近可预约时间"
                            # detail_times_value = use_date_list[0][1]
                            self.update_recommend(model_id=user.id,
                                                  recommend="最近可预约时间：{}".format(date),
                                                  order_status='0')
                            print('在搜索中没有可预约的时间！') if DEBUG else ""
                    # 其他未知原因
                    else:
                        print("未知错误") if DEBUG else ""
                        self.update_recommend(model_id=user.id,
                                              recommend="身份信息异常",
                                             order_status='2')
                        log_tool.test_log("爬虫系统",
                                          "预约失败",
                                          "未知错误",
                                          "页面代码：{}".format(first_res.text))
                else:
                    print("预约超时！") if DEBUG else ""
                    self.update_recommend(model_id=user.id,
                                          recommend='预约超时！！',
                                          order_status='2')
                    log_tool.test_log("爬虫系统",
                                      "预约失败",
                                      "预约超时",
                                      "当前时间：{} 预约最后时间：{}".format(local_date, date_end))
        else:
            print("暂时没有待预约用户") if DEBUG else ""

    # 封装网络请求
    def get_response(self, session, url, method="GET", headers=None, data=None):
        if not headers:
            headers = self.header
        if config.USE_PROXY:
            while True:
                proxy = self.create_proxy()
                proxies = {'http': 'http://{}'.format(proxy), 'https': 'http://{}'.format(proxy)}
                try:
                    print("当前使用代理：{}".format(proxy))
                    if method == "GET":
                        response = session.get(url, headers=headers, verify=False, timeout=60, proxies=proxies)
                    elif method == "POST":
                        response = session.post(url, headers=headers,
                                                data=data, verify=False, timeout=60, proxies=proxies)
                    else:
                        print('请求方式有问题！') if DEBUG else ""
                        response = ""
                    return response, session
                except Exception as req_err:
                    self.remove_proxy(proxy)
                    print("请求异常：{}".format(req_err)) if DEBUG else ""
                    log_tool.test_log("爬虫网络请求",
                                      "请求地址：{}".format(url),
                                      "使用代理请求",
                                      "ERROR:{}".format(req_err))
                    time.sleep(5)
        else:
            while True:
                try:
                    if method == "GET":
                        response = session.get(url, headers=headers, verify=False, timeout=60)
                    elif method == "POST":
                        response = session.post(url, headers=headers, data=data, verify=False, timeout=60)
                    else:
                        print('请求方式有问题！') if DEBUG else ""
                        response = ""
                    return response, session
                except Exception as req_err:
                    print("请求异常：{}".format(req_err)) if DEBUG else ""
                    log_tool.test_log("爬虫网络请求",
                                      "请求地址：{}".format(url),
                                      "不使用代理请求",
                                      "ERROR:{}".format(req_err))
                    time.sleep(5)

    # 转换成网站所要日期格式
    @staticmethod
    def trans_date(date):
        try:
            date = datetime.datetime.strptime("{}".format(date), "%Y-%m-%d").strftime("%d/%m/%Y")
            return date
        except Exception as da_err:
            print("时间转换错误：{}".format(da_err)) if DEBUG else ""
            return None

    # 翻译日期
    @staticmethod
    def trans_date2(stay_date):
        trans_dict = {
            'janvier': '1',
            'février': '2',
            'mars': '3',
            'avril': '4',
            'mai': '5',
            'juin': '6',
            'juillet': '7',
            'août': '8',
            'septembre': '9',
            'octobre': '10',
            'novembre': '11',
            'décembre': '12',
        }
        try:
            stay_date1 = stay_date.replace('h', ':').split()
            if len(stay_date1) == 6:
                stay_date2 = '{}-{}-{} {}'.format(stay_date1[3], trans_dict[stay_date1[2]], stay_date1[1],
                                                  stay_date1[-1])
                stay_date = datetime.datetime.strptime("{}".format(stay_date2), "%Y-%m-%d %H:%M")
            else:
                stay_date = stay_date
            return stay_date
        except Exception as da_err:
            print("时间转换错误：{}".format(da_err)) if DEBUG else ""
            return None

    # 查询预约信息
    def query(self, user, session, first_res, from_data2):
        self.header.update({'Referer': first_res.url})
        second_res, session = self.get_response(
            session=session, url=self.second_url, method="POST", headers=self.header, data=from_data2)
        detail_times_value = ''
        date = ''
        second_tree = etree.HTML(second_res.text)
        use_date_list = []
        for i in range(1, 6):
            date = ''.join(
                second_tree.xpath(
                    '//div[@class="controls grid-creneaux"]/div[2]/div[{}]/label/input/@value'.format(i)))
            detail_times_value = second_tree.xpath(
                '//div[@class="controls grid-creneaux"]/div[2]/div[{}]/select/option/@value'.format(i))
            # 比较日期
            if detail_times_value and date:
                date_1 = datetime.datetime.strptime("{}".format(date), "%d/%m/%Y")
                date_start = datetime.datetime.strptime("{}".format(user.start_date), "%Y-%m-%d")
                date_end = datetime.datetime.strptime("{}".format(user.end_date), "%Y-%m-%d")
                detail_times_value = detail_times_value[1]
                if date_start < date_1 < date_end:
                    return session, detail_times_value, date, second_res, use_date_list
                else:
                    use_date_list.append([date, detail_times_value])
                    date = ""
                    detail_times_value = ""

        return session, detail_times_value, date, second_res, use_date_list

    # 进行预约
    def pre_meet(self, user, session, second_res, from_data3, detail_times_value, date):
        self.header.update({'Referer': second_res.url})
        # 请求验证码图片
        parse_res, session = self.get_response(
            session=session, url=self.generate_image_url, method="POST", headers=self.header)
        image_url = 'https://www.ppoletrangers.interieur.gouv.fr/' + parse_res.text.replace(';', '&')
        self.header.update({'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'})
        # 保存验证码图片
        image_res, session = self.get_response(session=session, url=image_url, headers=self.header)
        with open('{}.png'.format(user.id), 'wb') as f:
            f.write(image_res.content)
        code = image_code.get_code('{}.png'.format(user.id))
        from_data3.update({"code": code})
        from_data3.update({"heure[]": detail_times_value})
        from_data3.update({"jour": date})
        pre_meet_url = 'https://www.ppoletrangers.interieur.gouv.fr/?page=rdv+prendre'
        self.header.update({'Accept': '*/*'})
        success_res, session = self.get_response(session=session,
                                                 url=pre_meet_url,
                                                 method="POST",
                                                 headers=self.header,
                                                 data=from_data3)
        if 'Annuler le rdv' in success_res.text:
            success_tree = etree.HTML(success_res.text)
            print("预约成功！") if DEBUG else ""
            stay_date = ''.join(success_tree.xpath(
                '//div[@id="vue"]/div[2]/text()[2]')).replace('Vous avez pris rdv le', '').strip()
            stay_date = self.trans_date2(stay_date=stay_date)
            stay_address = ''.join(
                success_tree.xpath('//*[@id="vue"]/div[2]/fieldset/text()')).strip()
            self.insert_status(model_id=user.id, order_status="1",
                               stay_date=stay_date, stay_address=stay_address,
                               recommend="预约成功!")
            log_tool.test_log("爬虫系统",
                              "{} {}预约成功".format(user.name, user.username),
                              "预约成功",
                              "预约时间：{} 预约地点：{}".format(stay_date, stay_address))
        else:
            print("预约失败！") if DEBUG else ""
            log_tool.test_log("爬虫系统",
                              "预约失败",
                              "未知错误",
                              "提交验证码进行预约时 失败 可能是网络服务器异常 稍后重试")


if __name__ == '__main__':
    while True:
        try:
            print("爬虫开启：{}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
            stay = StaySpider()
            stay.start_requests()
            print("爬虫结束：{}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
            time.sleep(config.CRAWL_PERIOD)
        except Exception as stay_err:
            print("爬虫系统异常：{}".format(stay_err)) if DEBUG else ""
            log_tool.test_log("爬虫系统",
                              "爬虫主函数",
                              "未知错误",
                              "{}".format(stay_err))
