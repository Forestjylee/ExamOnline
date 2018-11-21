# -*- coding: utf-8 -*-
"""
ExamApp的url分发
@file: urls.py
@time: 2018/11/6 20:34
Created by Junyi.
"""
from django.urls import path
from . import views

app_name = 'ExamApp'

urlpatterns = [
    path('', views.start_page, name='起始页'),
    path('login/', views.user_login, name='登录'),
    path('404/', views.page_404, name='404'),
]

