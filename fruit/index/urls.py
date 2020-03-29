# -*- encoding: utf-8 -*-
"""
@File    : urls.py
@Time    : 3/16/20 3:41 PM
@Author  : qiuyucheng
@Software: PyCharm
"""
from django.conf.urls import url
from . import views
urlpatterns = [
    url("^$",views.index),
    url("^login$",views.login),
    url("^register$",views.register),
    url("^logout$",views.logout),
    url("^check_login$",views.check_login),
    url("^load_goods$",views.load_goods),
]