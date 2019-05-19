# -*- coding: utf-8 -*-
"""
views的辅助函数
@file: views_helper.py
@time: 2019/5/19 11:20
Created by Junyi 
"""
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404

from ..models import User
from .decorators import deal_exceptions


def get_object_or_none(model, *args, **kwargs):
    """
    重新封装Django的get方法
    返回一个查询到的对象或None
    :param model: 需要查询对象的模型对象
    :param args: 传入的查询参数
    :param kwargs: 传入的查询参数
    :return: 查询到的对象或None
    """
    result = model.objects.filter(*args, **kwargs)
    if result:
        return result[0]
    else:
        return None


@deal_exceptions(return_when_exceptions=None)
def get_user_or_none(request):
    """
    验证用户是否存在
    存在：返回user对象
    不存在：返回None
    :param request:
    :return: user | None
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    return user
