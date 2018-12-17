# -*- coding: utf-8 -*-
"""
保存用户回答辅助函数
@file: save_answers_helper.py
@time: 2018/12/9 23:19
Created by Junyi.
"""
from ..models import (PaperUser, UserChoiceAnswer, UserJudgeAnswer,
                      UserTextAnswer, ChoiceProblem, JudgeProblem)


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
    correct_choice_amount = 0
    correct_judge_amount = 0
    for key, user_answer in user_answers.items():
        problem_id, problem_type = key.split('_')
        if problem_type == 'choice':
            correct_choice_amount += _save_choice_problem_answer(
                paper_id, user_id, problem_id, user_answer
            )
        elif problem_type == 'judge':
            correct_judge_amount += _save_judge_problem_answer(
                paper_id, user_id, problem_id, user_answer
            )
        else:
            _save_text_answer(
                paper_id, user_id, problem_id, problem_type, user_answer
            )
    _save_choice_judge_correct_amount(paper_id, user_id, correct_choice_amount, correct_judge_amount)


def _save_choice_problem_answer(paper_id: int, user_id: int, problem_id: int, answer: str) -> int:
    """
    保存用户选择题回答 -> UserChoiceAnswer
    :param paper_id: 试卷id
    :param user_id：用户id
    :param problem_id: 问题id
    :param answers: 学生回答
    :return: 是否回答正确(1|0)
    """
    standard_answer = str(ChoiceProblem.objects.get(id=problem_id).answer)
    UCA = UserChoiceAnswer()
    UCA.paper_id = paper_id
    UCA.uid = user_id
    UCA.problem_id = problem_id
    UCA.user_answer = answer
    UCA.is_correct = True if standard_answer == answer else False
    UCA.save()
    return 1 if UCA.is_correct else 0


def _save_choice_judge_correct_amount(
        paper_id: int,
        user_id: int,
        correct_choice_amount: int,
        correct_judge_amount: int
) -> None:
    """
    保存正确的选择题数到UserAnswerSituation中
    :param paper_id: 试卷id
    :param user_id: 用户id
    :param correct_choice_amount: 正确的选择题数量
    :param correct_judge_amount: 正确的判断题数量
    :return: None
    """
    PU = PaperUser.objects.get(paper_id=paper_id, uid=user_id)
    PU.answer_situation.correct_choice_problem_amount = correct_choice_amount
    PU.answer_situation.correct_judge_problem_amount = correct_judge_amount
    PU.save()


def _save_judge_problem_answer(paper_id: int, user_id: int, problem_id: int, answer: str) -> int:
    """
    保存用户判断题回答 -> UserJudgeAnswer
    :param paper_id：试卷id
    :param user_id：用户id
    :param problem_id：问题id
    :param answers：学生回答
    :return: 是否回答正确(1|0)
    """
    standard_answer = '1' if JudgeProblem.objects.get(id=problem_id).answer is True else '0'
    UJA = UserJudgeAnswer()
    UJA.paper_id = paper_id
    UJA.uid = user_id
    UJA.problem_id = problem_id
    UJA.user_answer = answer
    UJA.is_correct = True if standard_answer == answer else False
    UJA.save()
    return 1 if UJA.is_correct else 0


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
