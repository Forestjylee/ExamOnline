# -*- coding: utf-8 -*-
"""

@file: utils.py
@time: 2018/11/6 22:06
Created by Junyi.
"""
from django.shortcuts import render
from django.contrib.auth import authenticate
from ..models import User


def is_post_or_get(get_render_html):
    """
    判断request的类型，
    对POST和GET进行不同处理
    :param get_render_html: 收到get请求时需要渲染的html模板
    :return: -> render()
    """
    def swapper(func):
        def _swapper(request):
            if request.method == 'POST':
                return func(request)
            else:
                return render(request, get_render_html)
        return _swapper
    return swapper


def deal_exceptions(return_when_exceptions=None):
    """
    :param return_when_exceptions: 当函数发生异常时返回的值
    :return:
    """
    def swapper(func):
        def _swapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return return_when_exceptions
        return _swapper
    return swapper


@deal_exceptions(return_when_exceptions=None)
def get_user_or_none(request):
    """
    验证用户是否存在
    存在：返回user对象
    不存在：返回None
    :return: -> user | None
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    return user


def sign_up_user_or_none(request):
    """
    用户注册
    :return: user | None
    """
    if __is_password_valid(request.POST['password']):
        user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password'],
                                        real_name=request.POST['real_name'],
                                        class_name=request.POST['class_name'])
        return user
    else:
        return None


def __is_password_valid(password):
    """
    判断密码是否符合规范
    1. 长度大于等于6位
    :param password: 用户输入的密码
    :return: -> True | False
    """
    if len(password) >= 6:
        return True
    else:
        return False
