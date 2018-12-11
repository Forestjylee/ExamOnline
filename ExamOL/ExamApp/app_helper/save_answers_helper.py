# -*- coding: utf-8 -*-
"""
保存用户回答辅助函数
@file: save_answers_helper.py
@time: 2018/12/9 23:19
Created by Junyi.
"""
from ..models import (PaperUser, UserChoiceAnswer, UserJudgeAnswer,
                      UserTextAnswer)


def update_paper_user(paper_id: int, uid: int) -> None:
    """
    更新PaperUser表中的is_finished
    表示用户已完成
    :param paper_id: 试卷id
    :param uid: 用户id
    :return: None
    """
    paper_user = PaperUser.objects.get(paper_id=paper_id, uid=uid)
    paper_user.is_finished = True
    paper_user.save()


def save_problem_answers(paper_id: int, user_id:int, user_answers: dict) -> None:
    """
    保存用户的回答
    :param paper_id: 试卷id
    :param user_id: 用户id
    :param user_answers: 用户回答信息字典
    :return: None
    """
    for key, user_answer in user_answers.items():
        problem_id, problem_type = key.split('_')
        if problem_type == 'choice':
            _save_choice_problem_answer(
                paper_id, user_id, problem_id, user_answer
            )
        elif problem_type == 'judge':
            _save_judge_problem_answer(
                paper_id, user_id, problem_id, user_answer
            )
        else:
            _save_text_answer(
                paper_id, user_id, problem_id, problem_type, user_answer
            )


def _save_choice_problem_answer(paper_id: int, user_id: int, problem_id: int, answer: str) -> None:
    """
    保存用户选择题回答 -> UserChoiceAnswer
    :param paper_id: 试卷id
    :param user_id：用户id
    :param problem_id: 问题id
    :param answers: 学生回答
    :return: None
    """
    UCA = UserChoiceAnswer()
    UCA.paper_id = paper_id
    UCA.uid = user_id
    UCA.problem_id = problem_id
    UCA.user_answer = answer
    UCA.save()


def _save_judge_problem_answer(paper_id: int, user_id: int, problem_id: int, answer: str) -> None:
    """
    保存用户判断题回答 -> UserJudgeAnswer
    :param paper_id：试卷id
    :param user_id：用户id
    :param problem_id：问题id
    :param answers：学生回答
    :return: None
    """
    UJA = UserJudgeAnswer()
    UJA.paper_id = paper_id
    UJA.uid = user_id
    UJA.problem_id = problem_id
    UJA.user_answer = answer
    UJA.save()


def _save_text_answer(paper_id: int, user_id: int, problem_id: int, problem_type: str, answer: str) -> None:
    """
    保存用户的文本回答 -> UserTextAnswer
    :param paper_id: 试卷id
    :param user_id: 用户id
    :param problem_id: 试题id
    :param problem_type: 问题类型
    :param answers: 用户的回答信息列表
    :return: None
    """
    UTA = UserTextAnswer()
    UTA.paper_id = paper_id
    UTA.uid = user_id
    UTA.problem_id = problem_id
    UTA.problem_type = problem_type
    UTA.user_answer = answer
    UTA.save()
