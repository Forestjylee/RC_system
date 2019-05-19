# -*- coding: utf-8 -*-
"""

@file: decorators.py
@time: 2019/5/19 11:32
Created by Junyi 
"""
from django.shortcuts import render


def is_post_or_get(render_html: str):
    """
    判断request的类型，
    对POST和GET进行不同处理
    :param render_html: 收到get请求时需要渲染的html模板
    :return: render()渲染页面
    """

    def swapper(func):

        def _swapper(request, *args, **kwargs):
            if request.method == 'POST':
                return func(request, *args, **kwargs)
            else:
                return render(request, render_html)

        return _swapper

    return swapper


def deal_exceptions(return_when_exceptions=None):
    """
    :param return_when_exceptions: 当被装饰的函数发生异常时返回的值
    :return: return_when_exceptions
    """

    def swapper(func):

        def _swapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return return_when_exceptions

        return _swapper

    return swapper
