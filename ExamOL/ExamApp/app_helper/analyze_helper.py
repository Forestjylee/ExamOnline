# -*- coding: utf-8 -*-
"""

@file: analyze_helper.py
@time: 2018/12/16 21:45
Created by Junyi.
"""
from ..models import (PaperUser, PaperProblem, UserJudgeAnswer, UserChoiceAnswer,
                      UserTextAnswer, ChoiceProblem, JudgeProblem)


def get_right_choice_amount(paper_id: int) -> int:
    """
    所有学生一共答对的选择题数
    :param paper_id: 试卷id
    :return: 一共答对的选择题
    """
    return len(UserChoiceAnswer.objects.filter(paper_id=paper_id, is_correct=True))


def get_right_judge_amount(paper_id: int) -> int:
    """
    所有学生一共答对的判断题数
    :param paper_id: 试卷id
    :return: 一共答对的判断题
    """
    return len(UserJudgeAnswer.objects.filter(paper_id=paper_id, is_correct=True))


def get_right_fillblank_scores(paper_id: int) -> int:
    """
    所有学生填空题一共拿的分数
    :param paper_id: 书卷id
    :return: 填空题总分数
    """
    sum_scores = 0
    for problem in UserTextAnswer.objects.filter(paper_id=paper_id, problem_type="fillblank"):
        sum_scores += problem.scores
    return sum_scores


def get_right_QA_scores(paper_id: int) -> int:
    """
    所有学生问答题一共拿的分数
    :param paper_id: 试卷id
    :return: 问答题总分数
    """
    sum_scores = 0
    for problem in UserTextAnswer.objects.filter(paper_id=paper_id, problem_type="QA"):
        sum_scores += problem.scores
    return sum_scores


def get_right_operate_scores(paper_id: int) -> int:
    """
    所有学生填空题一共拿的分数
    :param paper_id: 试卷id
    :return: 实际操作题总分数
    """
    sum_scores = 0
    for problem in UserTextAnswer.objects.filter(paper_id=paper_id, problem_type="operate"):
        sum_scores += problem.scores
    return sum_scores


def get_answer_situation(paper_id: int):
    """
    获取用户答题情况
    :param paper_id: 试卷id
    :return: 类对象
    """

    class AnswerSituation:
        choice_mean_amount = 0
        judge_mean_amount = 0
        choice_amount = 0
        judge_amount = 0
        fillblank_mean_scores = 0
        QA_mean_scores = 0
        operate_mean_scores = 0

    if paper_id == 'all':
        return AnswerSituation
    sum_answers = len(PaperUser.objects.filter(paper_id=paper_id, is_finished=True))
    AnswerSituation.choice_amount = len(PaperProblem.objects.filter(paper_id=paper_id, problem_type="选择题"))
    AnswerSituation.judge_amount = len(PaperProblem.objects.filter(paper_id=paper_id, problem_type="判断题"))
    AnswerSituation.choice_mean_amount = (
        get_right_choice_amount(paper_id)
        // (sum_answers * AnswerSituation.choice_amount)
    )
    AnswerSituation.judge_mean_amount = (
        get_right_judge_amount(paper_id)
        // (sum_answers * AnswerSituation.judge_amount)
    )
    AnswerSituation.fillblank_mean_scores = (
        get_right_fillblank_scores(paper_id)
        // sum_answers
    )
    AnswerSituation.QA_mean_scores = (
        get_right_QA_scores(paper_id)
        // sum_answers
    )
    AnswerSituation.operate_mean_scores = (
        get_right_operate_scores(paper_id)
        // sum_answers
    )
    return AnswerSituation


def get_choice_situation(paper_id: int) -> list:
    """
    获取选择题回答详细情况
    高频错题对象列表
    取前十个（不足十个则全部返回）
    :param paper_id: 试卷id
    :return: 高频错题对象列表
    """
    problems = []
    PUs = PaperUser.objects.filter(paper_id=paper_id, is_finished=True)
    sum_answers = len(PUs)
    PBs = PaperProblem.objects.filter(paper_id=paper_id, problem_type="选择题")
    for PB in PBs:
        correct_amount = len(UserChoiceAnswer.objects.filter(paper_id=paper_id, problem_id=PB.problem_id, is_correct=True))
        CP = ChoiceProblem.objects.get(id=PB.problem_id)
        CP.correct_rate = correct_amount // sum_answers
        problems.append(CP)
        problems = sorted(problems, key=lambda x: x.correct_rate)
    return problems[:10] if len(problems) > 10 else problems


def get_judge_situation(paper_id: int) -> list:
    """
    获取判断题回答详细情况
    高频错题对象列表
    取前十个（不足十个则全部返回）
    :param paper_id: 试卷id
    :return: 高频错题对象列表
    """
    problems = []
    PUs = PaperUser.objects.filter(paper_id=paper_id, is_finished=True)
    sum_answers = len(PUs)
    PBs = PaperProblem.objects.filter(paper_id=paper_id, problem_type="判断题")
    for PB in PBs:
        correct_amount = len(UserJudgeAnswer.objects.filter(paper_id=paper_id, problem_id=PB.problem_id, is_correct=True))
        JP = JudgeProblem.objects.get(id=PB.problem_id)
        JP.correct_rate = correct_amount // sum_answers
        problems.append(JP)
        problems = sorted(problems, key=lambda x: x.correct_rate)
    return problems[:10] if len(problems) > 10 else problems


def _get_detail_scores(paper_id: int) -> tuple:
    """
    获取各分数段的人数
    90+
    80~90
    70~80
    60~70
    60-
    所有人分数总和
    :param paper_id: 试卷id
    :return: 各分数段人数元组
    """
    ninety_plus = 0
    eighty_ninety = 0
    seventy_eighty = 0
    sixty_seventy = 0
    less_sixty = 0
    sum_scores = 0
    PUs = PaperUser.objects.filter(paper_id=paper_id, is_finished=True)
    sum_answers = len(PUs)
    for PU in PUs:
        AS = PU.answer_situation
        temp_scores = AS.sum_scores
        if temp_scores >= 90:
            ninety_plus += 1
        elif 80 <= temp_scores < 90:
            eighty_ninety += 1
        elif 70 <= temp_scores < 80:
            seventy_eighty += 1
        elif 60 <= temp_scores < 70:
            sixty_seventy += 1
        else:
            less_sixty += 1
        sum_scores += temp_scores
    return (
        ninety_plus, eighty_ninety, seventy_eighty,
        sixty_seventy, less_sixty, round(sum_scores / sum_answers, 3)
    )


def get_scores_situation(paper_id: int):
    """
    返回各分数段的人数情况
    :param paper_id: 试卷id
    :return: ScoreSituation
    """

    class ScoreSituation:
        ninety_plus = 0
        eighty_ninety = 0
        seventy_eighty = 0
        sixty_seventy = 0
        less_sixty = 0
        mean_scores = 0

    if paper_id == 'all':
        return ScoreSituation
    (
        ScoreSituation.ninety_plus,
        ScoreSituation.eighty_ninety,
        ScoreSituation.seventy_eighty,
        ScoreSituation.sixty_seventy,
        ScoreSituation.less_sixty,
        ScoreSituation.mean_scores,
    ) = _get_detail_scores(paper_id)
    return ScoreSituation
