# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:SentMsg
FileName = PyCharm
Version:1.0
CreateDay:2018/8/17 10:24
"""
from django.urls import path
from .views import LoginView, LogoutView, IndexView, CommitHistoryView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', IndexView.as_view(), name="index"),
    path('index/', IndexView.as_view(), name="index"),
    path('history/', CommitHistoryView.as_view(), name="history"),
]
