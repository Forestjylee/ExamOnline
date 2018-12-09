# -*- coding: utf-8 -*-
"""
创建试卷的函数:
    根据题目的数量信息和分值自动生成试卷
    1.将信息读出到变量，判断是否有误
    2.根据要求随机选择题目
    3.在试卷表创建一张新的试卷
    4.在题目-试卷关系表中保存关系
    5.获取使用试卷的用户列表
    6.在用户-试卷信息表中保存关系
@file: create_paper_helper.py
@time: 2018/12/8 14:32
Created by Junyi.
"""
from random import sample
from copy import deepcopy
from datetime import datetime
from django.utils import timezone
from ..models import (PaperUser, Paper, PaperProblem, ChoiceProblem,
                      JudgeProblem, FillBlankProblem, QAProblem,
                      OperateProblem, UserAnswerSituation)


def _get_model_object(problem_type: str):
    """
    根据题目类型获取数据库模型并返回
    :param problem_type: 题目类型
    :return: 数据库模型对象
    """
    if problem_type == '选择题':
        return ChoiceProblem
    elif problem_type == '判断题':
        return JudgeProblem
    elif problem_type == '填空题':
        return FillBlankProblem
    elif problem_type == '问答题':
        return QAProblem
    else:
        return OperateProblem


def _get_random_problems(problem_list: list, amount: str) -> list:
    """
    获取随机数量的问题
    :param problem_list: 问题列表
    :param amount: 数量
    :return: 指定数量的问题
    """
    amount = int(amount)
    length = len(problem_list)
    if length > amount:
        return sample(problem_list, amount)
    elif length == amount:
        return problem_list
    else:
        raise IndexError("题库中没有这么多题目")


def _get_datetime(date: str, hour: str, minute: str) -> datetime:
    """
    输入日期/时/分，转换为
    xxxx-xx-xx xx:xx:xx格式的日期
    :param date: 日期
    :param hour: 时
    :param minute: 分
    :return: xxxx-xx-xx xx:xx:xx格式的日期
    """
    date_list = date.split('-')
    return datetime(year=int(date_list[0]), month=int(date_list[1]),
                    day=int(date_list[2]), hour=int(hour), minute=int(minute))


def check_paper_info(paper_info: dict) -> dict:
    """
    判断试卷信息是否有误
    :param paper_info: 试卷信息字典
    :return: 检查后的字典
    """
    new_paper_info = deepcopy(paper_info)
    start_date = paper_info['start_date']
    start_hour = paper_info['start_hour']
    start_minute = paper_info['start_minute']
    start_datetime = _get_datetime(start_date, start_hour, start_minute) if start_date else timezone.now()
    end_date = paper_info['end_date']
    end_hour = paper_info['end_hour']
    end_minute = paper_info['end_minute']
    end_datetime = _get_datetime(end_date, end_hour, end_minute) if end_date else datetime(year=2099, month=1, day=1)
    new_paper_info['start_datetime'] = start_datetime
    new_paper_info['end_datetime'] = end_datetime
    return new_paper_info


def select_a_kind_of_problem(problem_type: str, amount_list: list) -> list:
    """
    选择一个类型的题目
    :param problem_type: 题目类型
    :param amount_list: 按照简单，中等，困难排序的数量列表
    :return: 一个类型题目的列表
    """
    problem_list = []
    model_object = _get_model_object(problem_type)
    if amount_list[0]:
        problems = list(model_object.objects.filter(level=1))
        problem_list.extend(_get_random_problems(problems, amount_list[0]))
    if amount_list[1]:
        problems = list(model_object.objects.filter(level=2))
        problem_list.extend(_get_random_problems(problems, amount_list[1]))
    if amount_list[2]:
        problems = list(model_object.objects.filter(level=3))
        problem_list.extend(_get_random_problems(problems, amount_list[2]))
    return problem_list


def select_problems(paper_info: dict) -> list:
    """
    根据要求选择指定数量的题目
    :param paper_info: 试卷信息
    :return: 选择出的题目
    """
    selected_problems = []
    for problem_type in ['选择题', '判断题', '填空题', '问答题', '实际操作题']:
        selected_problems.extend(select_a_kind_of_problem(problem_type, [
            paper_info[f"{problem_type}_simple"],
            paper_info[f"{problem_type}_middle"],
            paper_info[f"{problem_type}_difficult"]
        ]))
    return selected_problems


def create_a_new_paper_in_db(
    level: str,
    paper_name: str,
    choice_score: int,
    judge_score: int,
    start_time: str,
    end_time: str,
    owner_id: int,
    author: str='自动生成'
) -> int:
    """
    在数据库试卷表中一个新试卷
    返回试卷id
    :param level: 试卷难度(1|2|3)
    :param paper_name: 试卷名称
    :param choice_score: 每道选择题分数
    :param judge_score: 每道判断题分数
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param owner_id: 试卷管理员id
    :param author: 作者(默认为'自动生成')
    :return: 试卷id
    """
    new_paper = Paper()
    new_paper.level = level
    new_paper.paper_name = paper_name
    new_paper.each_choice_problem_score = choice_score
    new_paper.each_judge_problem_score = judge_score
    new_paper.start_time = start_time
    new_paper.end_time = end_time
    new_paper.author = author
    new_paper.owner_id = owner_id
    new_paper.save()
    return new_paper.paper_id


def save_to_paper_problems_db(paper_id: int, selected_problems: list) -> None:
    """
    在题目-试卷关系表中保存关系
    :param paper_id: 试卷id
    :param selected_problems: 筛选出来的题目
    :return: None
    """
    for selected_problem in selected_problems:
        new_paper_problem = PaperProblem()
        new_paper_problem.paper_id = paper_id
        new_paper_problem.problem_id = selected_problem.id
        new_paper_problem.problem_type = selected_problem.problem_type
        new_paper_problem.save()


def save_to_paper_user_db(paper_id: int, user_list: list) -> None:
    """
    保存到试卷-用户关系表
    :param paper_id: 试卷id
    :param user_list: 使用该试卷的用户
    :return: None
    """
    for user in user_list:
        new_answer_situation = UserAnswerSituation()
        new_answer_situation.save()
        new_paper_user = PaperUser()
        new_paper_user.paper_id = paper_id
        new_paper_user.uid = user.uid
        new_paper_user.answer_situation = new_answer_situation
        new_paper_user.save()
