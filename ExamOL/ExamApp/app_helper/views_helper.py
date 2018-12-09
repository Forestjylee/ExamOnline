# -*- coding: utf-8 -*-
"""

@file: utils.py
@time: 2018/11/6 22:06
Created by Junyi.
"""
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate
from ..models import (User, Paper, PaperUser, TeacherStudent, TeacherClass,
                      ChoiceProblem, JudgeProblem, FillBlankProblem,
                      QAProblem, OperateProblem)
from .create_paper_helper import (check_paper_info, select_problems, create_a_new_paper_in_db,
                                  save_to_paper_problems_db, save_to_paper_user_db)


def get_object_or_none(model, *args, **kwargs):
    """
    重新封装get方法
    获取一个对象或返回None
    :param model: 模型对象
    :param args: 传入的参数
    :param kwargs: 传入的参数
    :return: 一个对象或None
    """
    result = model.objects.filter(*args, **kwargs)
    if result:
        return result[0]
    else:
        return None


def is_post_or_get(get_render_html):
    """
    判断request的类型，
    对POST和GET进行不同处理
    :param get_render_html: 收到get请求时需要渲染的html模板
    :return: -> render()
    """
    def swapper(func):
        def _swapper(request, *arg, **kwargs):
            if request.method == 'POST':
                return func(request, *arg, **kwargs)
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


def get_user_do_and_undo_paper_list(user_id: str) -> tuple:
    """
    接收用户的id获取完成与未完成的考试列表
    :param user_id: 用户的id
    :return: 元组(已完成的考试列表，未完成的考试列表)
    """
    finished_paper_list = []
    unfinished_paper_list = []
    paper_user_list = PaperUser.objects.filter(uid=user_id, is_delete=False)
    for paper_user in paper_user_list:
        paper = get_object_or_none(Paper, paper_id=paper_user.paper_id, is_delete=False)
        if paper:
            if paper_user.is_finished:
                finished_paper_list.append(paper)
            else:
                unfinished_paper_list.append(paper)
    return finished_paper_list, unfinished_paper_list


def get_class_list(teacher_id: str) -> list:
    """
    输入一个老师id
    返回他的班级列表
    :param teacher_id: 老师用户的id
    :return: 班级列表
    """
    return TeacherClass.objects.filter(teacher_id=teacher_id, is_delete=False)


def get_student_list(user_id: int, class_name: str) -> list:
    """
    输入一个老师用户的id
    返回他的学生列表
    :param user_id: 老师用户的id
    :param class_name: 需要展示的班级名
    :return: 学生列表
    """
    student_list = []
    relationship_list = TeacherStudent.objects.filter(teacher_id=user_id, is_delete=False)
    if class_name == 'all':
        for relationship in relationship_list:
            student = get_object_or_none(User, uid=relationship.student_id)
            if student:
                student_list.append(student)
    else:
        for relationship in relationship_list:
            student = get_object_or_none(User, uid=relationship.student_id, class_name=class_name)
            if student:
                student_list.append(student)
    return student_list


def get_problem_list(problem_type: str) -> tuple:
    """
    输入一个题目类型
    返回题库中本类型的题目
    :param problem_type: 问题的类型
    :return: 题目列表
    """
    if problem_type == 'choice':
        return '选择题', ChoiceProblem.objects.all()
    elif problem_type == 'judge':
        return '判断题', JudgeProblem.objects.all()
    elif problem_type == 'fillblank':
        return '填空题', FillBlankProblem.objects.all()
    elif problem_type == 'QA':
        return '问答题', QAProblem.objects.all()
    elif problem_type == 'operate':
        return '实际操作题', OperateProblem.objects.all()
    else:
        return '选择题', ChoiceProblem.objects.all()


def use_info_to_create_paper(teacher_id: int, paper_info: dict) -> bool:
    """
    根据题目的数量信息和分值自动生成试卷
    1.将信息读出到变量，判断是否有误
    2.根据要求随机选择题目
    3.在试卷表创建一张新的试卷
    4.在题目-试卷关系表中保存关系
    5.获取使用试卷的用户列表[get_student_list()]
    6.在用户-试卷信息表中保存关系
    :param teacher_id: 老师的id
    :param paper_info: 试卷的各题目数量信息字典
    :return: (是否创建成功)True | False
    """
    try:
        checked_paper_info = check_paper_info(paper_info)
        selected_problems = select_problems(checked_paper_info)
        student_list = get_student_list(teacher_id, class_name='all')
        new_paper_id = create_a_new_paper_in_db(
            level=checked_paper_info['paper_level'],
            paper_name=checked_paper_info['paper_name'],
            choice_score=checked_paper_info['选择题_point'],
            judge_score=checked_paper_info['判断题_point'],
            start_time=checked_paper_info['start_datetime'],
            end_time=checked_paper_info['end_datetime'],
            owner_id=teacher_id,
        )
        save_to_paper_problems_db(paper_id=new_paper_id, selected_problems=selected_problems)
        save_to_paper_user_db(paper_id=new_paper_id, user_list=student_list)
        return True
    except:
        return False
