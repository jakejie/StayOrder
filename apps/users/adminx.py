# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:StayOrder
FileName = PyCharm
Version:1.0
CreateDay:2018/10/19 16:03
"""
import xadmin
from xadmin import views
from .models import CrawlTaskModel


# 爬虫任务
class CrawlTaskModelAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['user', 'name', 'username', 'order_status', 'stay_date',
                    'birthday_date', 'stay_num',
                    'stay_end_date', 'town', 'start_date', 'end_date',
                    'stay_address', 'recommend',
                    'add_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['user', 'name', 'username', 'birthday_date', 'stay_num',
                     'stay_end_date', 'town', 'start_date', 'end_date',
                     'order_status', 'stay_date', 'stay_address', 'add_time']
    # 配置筛选字段
    list_filter = ['user', 'name', 'username', 'birthday_date', 'stay_num',
                   'stay_end_date', 'town', 'start_date', 'end_date',
                   'order_status', 'stay_date', 'stay_address', 'add_time']
    list_per_page = 50


# 注册
xadmin.site.register(CrawlTaskModel, CrawlTaskModelAdmin)


# 创建X admin的全局管理器并与view绑定。
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# xadmin全局配置
class GlobalSettings(object):
    site_title = "系统后台管理"
    site_footer = "管理系统"

    # 让管理后台左侧收起来
    # menu_style = "accordion"


# 将全局配置管理与view绑定注册
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

if __name__ == "__main__":
    pass
