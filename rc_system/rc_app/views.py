from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

from .models import User
from .app_helper.decorators import is_post_or_get
from .app_helper.views_helper import get_user_or_none

# Create your views here.


def start_page(request):
    """起始页面(跳转到登录界面)"""
    return redirect('rc_app:登录')


@is_post_or_get(render_html='login.html')
def user_login(request):
    """登录页面"""
    user = get_user_or_none(request)
    if user is not None:
        login(request, user)
        return redirect('rc_app:主页', username=user.username)
    else:
        return render(request, 'login.html', {'error': '密码错误'})


def user_logout(request):
    """用户登出"""
    logout(request)
    return redirect('rc_app:登录')


@login_required
def home_page(request, username: str):
    """主页"""
    print("我是", username)
    return render(request, 'face.html', {'username': username})


def page_not_found(request, exception=None):
    """404"""
    return render_to_response('404.html')
