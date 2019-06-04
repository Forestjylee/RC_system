# -*- coding: utf-8 -*-
"""
rc_app的url路由分发
@file: urls.py
@time: 2019/5/19 11:00
Created by Junyi 
"""
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from . import views


app_name = 'rc_app'

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', views.start_page, name='起始页'),
    path('login/', views.user_login, name='登录'),
    path('logout/', views.user_logout, name='登出'),
    path('home/<username>/<course_index>/', views.home_page, name='主页'),
    path('specific_name_list/<username>/', views.specific_name_list, name='详细名单'),
    path('manage_course/<username>/', views.manage_course, name='管理课程'),
    path('manage_course_student/<username>/<course_id>/', views.manage_course_student, name='管理课程中的学生'),
    path('manage_student/<username>/', views.manage_student, name='管理学生'),
    path('absent_record/<username>/<student_id>/', views.absent_record, name='缺勤记录')
]

handler404 = views.page_not_found
