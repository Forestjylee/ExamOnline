from os import path
from django.apps import AppConfig


VERBOSE_APP_NAME = "考试平台数据库"


def get_current_app_name(file):
    return path.split(path.dirname(file))[-1]


class ExamappConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME
