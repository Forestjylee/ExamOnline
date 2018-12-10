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


def save_problem_answers(paper_id: int, user_id:int, paper_problems: list, user_answers: dict) -> None:
    """
    保存用户的回答
    :param paper_id: 试卷id
    :param user_id: 用户id
    :param paper_problems: [
        [选择题列表],
        [判断题列表],
        [填空题列表],
        [问答题列表],
        [实际操作题列表],
    ]
    :param user_answers: 用户回答信息字典
    :return: None
    """
    choice_problems, judge_problems, fillblank_problems, QA_problems, operate_problems = paper_problems
    _save_choice_problem_answer(paper_id, user_id, answers=_get_a_kind_of_problem_answers(
        choice_problems, 'choice', user_answers
    ))
    _save_judge_problem_answer(paper_id, user_id, answers=_get_a_kind_of_problem_answers(
        judge_problems, 'judge', user_answers
    ))
    _save_text_answer(paper_id, user_id, 'fillblank', answers=_get_a_kind_of_problem_answers(
        fillblank_problems, 'fillblank', user_answers
    ))
    _save_text_answer(paper_id, user_id, 'fillblank', answers=_get_a_kind_of_problem_answers(
        QA_problems, 'QA', user_answers
    ))
    _save_text_answer(paper_id, user_id, 'fillblank', answers=_get_a_kind_of_problem_answers(
        operate_problems, 'operate', user_answers
    ))


def _get_a_kind_of_problem_answers(problems: list, problem_type: str, mix_answers: dict):
    """
    返回指定类型题目的回答信息列表
    :param problems: 试题列表
    :param problem_type: 试题类型
    :param mix_answers: 用户回答信息
    :return: 指定类型题目的回答信息列表
    """
    answers = []
    for problem in problems:
        problem_id = problem.id
        answer_id = f"{problem_id}_{problem_type}"
        answer = _get_query_dict_value(mix_answers, key=answer_id)
        if answer:
            answer_dict = ({
                'problem_id': problem_id,
                'answer': answer,
            })
            if problem_type == 'choice' or problem_type == 'judge':
                answer_dict['is_correct'] = True if answer == str(problem.answer) else False
            answers.append(answer_dict)
    return answers


def _get_query_dict_value(query_dict, key: str) -> str:
    """
    从query_dict<class QueryDict>取出值，没有则返回None
    :param query_dict
    :param key:
    :return: str | None
    """
    try:
        return query_dict.__getitem__(key)
    except KeyError:
        return None


def _save_choice_problem_answer(paper_id: int, user_id: int, answers: list) -> None:
    """
    保存用户选择题回答 -> UserChoiceAnswer
    :param paper_id
    :param user_id
    :param answers
    :return: None
    """
    for answer in answers:
        UCA = UserChoiceAnswer()
        UCA.paper_id = paper_id
        UCA.uid = user_id
        UCA.problem_id = answer['problem_id']
        UCA.user_answer = answer['answer']
        UCA.is_correct = answer['is_correct']
        UCA.save()


def _save_judge_problem_answer(paper_id: int, user_id: int, answers: list) -> None:
    """
    保存用户判断题回答 -> UserJudgeAnswer
    :param paper_id
    :param user_id
    :param answers
    :return: None
    """
    for answer in answers:
        UJA = UserJudgeAnswer()
        UJA.paper_id = paper_id
        UJA.uid = user_id
        UJA.problem_id = answer['problem_id']
        UJA.user_answer = answer['answer']
        UJA.is_correct = answer['is_correct']
        UJA.save()


def _save_text_answer(paper_id: int, user_id: int, problem_type: str, answers: list) -> None:
    """
    保存用户的文本回答 -> UserTextAnswer
    :param paper_id: 试卷id
    :param user_id: 用户id
    :param problem_type: 问题类型
    :param answers: 用户的回答信息列表
    :return: None
    """
    for answer in answers:
        UTA = UserTextAnswer()
        UTA.paper_id = paper_id
        UTA.uid = user_id
        UTA.problem_type = problem_type
        UTA.problem_id = answer['problem_id']
        UTA.user_answer = answer['answer']
        UTA.save()
