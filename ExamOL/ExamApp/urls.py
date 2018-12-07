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
    path('send_bug/<username>/', views.commit_bug, name='报告错误'),
    path('stu_home/<username>/', views.student_home_page, name='学生主页'),
    path('tea_home/<username>/<class_name>/', views.teacher_home_page, name='老师主页'),
    path('admin_problems/<username>/', views.admin_problems, name='管理试题'),
    path('create_paper/<username>/', views.create_paper, name='创建试卷'),
]

handler404 = views.page_not_found
