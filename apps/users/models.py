from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户管理模块
class UserProfile(AbstractUser):
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 爬虫任务管理表
class CrawlTaskModel(models.Model):
    order_status_choice = (
        ('0', '预约中'),
        ('1', '预约成功'),
        ('2', '预约失败'),
    )
    town_choice = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="所属用户", default='')

    name = models.CharField(verbose_name="姓氏", max_length=64, default="", )  # 姓氏
    username = models.CharField(verbose_name="名字", max_length=64, default="", )  # 名字

    birthday_date = models.DateField(verbose_name="出生日期", default="")

    stay_num = models.CharField(verbose_name="居留许可证号码", max_length=32, default="", )  # 居留许可证号码
    stay_end_date = models.DateField(verbose_name="居留许可到期时间", default="")

    town = models.CharField(verbose_name="区", max_length=32, default="",choices=town_choice)  # 镇 数字

    start_date = models.DateField(verbose_name="预约开始时间", default="", )  # 开始时间
    end_date = models.DateField(verbose_name="预约结束时间", default="", )  # 结束时间
    # 以上八个参数必填
    order_status = models.CharField(verbose_name="预约状态", max_length=32,
                                    choices=order_status_choice,
                                    default="0")
    stay_date = models.DateTimeField(verbose_name="预约成功时间(可入住时间)",
                                     null=True, blank=True)
    stay_address = models.CharField(verbose_name="预约地址", max_length=512,
                                    default="", null=True, blank=True)

    access_email = models.EmailField(verbose_name="接收预约结果的邮箱", default="",
                                     null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="任务创建时间", default=datetime.now)
    success_time = models.DateTimeField(verbose_name="预约成功时间",
                                        null=True, blank=True)

    recommend = models.CharField(verbose_name="备注信息",
                                 max_length=256,
                                 default="",
                                 null=True, blank=True)

    class Meta:
        verbose_name = "爬虫任务管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.username, self.order_status)
