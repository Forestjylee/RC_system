# -*- coding: utf-8 -*-
"""
rc_app的url路由分发
@file: urls.py
@time: 2019/5/19 11:00
Created by Junyi 
"""
from django.urls import path
from . import views


app_name = 'rc_app'

urlpatterns = [
    path('', views.start_page, name='起始页'),
    path('login/', views.user_login, name='登录'),
    path('logout/', views.user_logout, name='登出'),
    path('home/<username>/', views.home_page, name='主页')
]

handler404 = views.page_not_found
