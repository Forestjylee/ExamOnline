# -*- coding: utf-8 -*-
"""
获取用户的答题信息
@file: get_answers_helper.py
@time: 2018/12/10 16:45
Created by Junyi.
"""
from ..models import UserTextAnswer, FillBlankProblem, QAProblem, OperateProblem


def get_a_kind_of_problem_answers(paper_id: str, user_id: str, problem_type: str) -> list:
    """
    获取用户一种类型的题目的回答信息
    :param paper_id: 试卷id
    :param user_id: 用户id
    :param problem_type: 问题类型([fillblank|填空题]，[QA|问答题]，[operate|实际操作题])
    :return: 回答信息列表
    """
    return UserTextAnswer.objects.filter(paper_id=paper_id, uid=user_id, problem_type=problem_type)


def get_problem_standard_answer(problem_type: str, problem_id: str) -> tuple:
    """
    根据问题id和问题类型
    获取一个问题的题目和标准答案
    :param problem_type: 问题类型([fillblank|填空题]，[QA|问答题]，[operate|实际操作题])
    :param problem_id: 问题id
    :return: 一个问题的题目和标准答案
    """
    if problem_type == 'fillblank':
        problem = FillBlankProblem.objects.get(pk=problem_id)
    elif problem_type == 'QA':
        problem = QAProblem.objects.get(pk=problem_id)
    else:
        problem = OperateProblem.objects.get(pk=problem_id)
    return problem.content, problem.answer
