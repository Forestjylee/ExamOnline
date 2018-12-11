# -*- coding: utf-8 -*-
"""
发送邮件模块
@file: send_email.py
@time: 2018/12/11 18:23
Created by Junyi.
"""
import smtplib
from email.mime.text import MIMEText
from .views_helper import deal_exceptions


@deal_exceptions(return_when_exceptions=False)
def send_bug_to_email(bug_info: str, target_email: str) -> bool:
    """
    将程序的bug信息发送到指定邮箱
    :param bug_info: bug信息
    :param target_email: 指定邮箱
    :return: 是否发送成功
    """
    message = MIMEText(bug_info)
    message['From'] = 'dbbugreporter@163.com'
    message['To'] = target_email
    message['Subject'] = '来自数据库考试系统的提醒'
    server = smtplib.SMTP('smtp.163.com')
    server.login(user='dbbugreporter@163.com', password='bugreporter1234')
    server.send_message(msg=message)
    server.close()
    return True
