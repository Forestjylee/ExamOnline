# -*- coding: utf-8 -*-
"""

@file: utils.py
@time: 2018/11/6 22:06
Created by Junyi.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from ..models import (User, Paper, PaperUser, PaperProblem, TeacherStudent,
                      TeacherClass, ChoiceProblem, JudgeProblem, FillBlankProblem,
                      QAProblem, OperateProblem, UserTextAnswer)
from .create_paper_helper import (check_paper_info, select_problems, create_a_new_paper_in_db,
                                  save_to_paper_problems_db, save_to_paper_user_db)
from .save_answers_helper import update_paper_user, save_problem_answers
from .get_answers_helper import get_a_kind_of_problem_answers, get_problem_standard_answer


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


@deal_exceptions(return_when_exceptions=False)
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


def get_exam_problems(user: User, paper: Paper) -> list:
    """
    1.检查用户是否在用户试卷关系表中
    2.根据用户id和试卷id获取题目列表
    :param user: User模型对象
    :param paper: Paper模型对象
    :return: 题目列表 = [
        [选择题列表],
        [判断题列表],
        [填空题列表],
        [问答题列表],
        [实际操作题列表],
    ]
    """
    choice_problems = []
    judge_problems = []
    fillblank_problems = []
    QA_problems = []
    operate_problems = []
    get_object_or_404(PaperUser, paper_id=paper.paper_id, uid=user.uid)
    mix_problems = PaperProblem.objects.filter(paper_id=paper.paper_id)
    for problem in mix_problems:
        if problem.problem_type == '选择题':
            choice_problems.append(get_object_or_404(ChoiceProblem, pk=problem.problem_id))
        elif problem.problem_type == '判断题':
            judge_problems.append(get_object_or_404(JudgeProblem, pk=problem.problem_id))
        elif problem.problem_type == '填空题':
            fillblank_problems.append(get_object_or_404(FillBlankProblem, pk=problem.problem_id))
        elif problem.problem_type == '问答题':
            QA_problems.append(get_object_or_404(QAProblem, pk=problem.problem_id))
        elif problem.problem_type == '实际操作题':
            operate_problems.append(get_object_or_404(OperateProblem, pk=problem.problem_id))
    return [choice_problems, judge_problems, fillblank_problems, QA_problems, operate_problems]


def get_paper_list(user: User) -> list:
    """
    在数据库中查找返回该老师管理的试卷列表
    :param user: 老师对象
    :return: 老师管理的试卷列表
    """
    return Paper.objects.filter(owner_id=user.uid)


def get_paper_user_list(paper_id: str) -> list:
    """
    返回已完成该试卷的用户id列表
    :param paper_id: 试卷id
    :return: 使用该试卷的用户id列表
    """
    if paper_id != 'all':
        user_list = []
        paper_users = PaperUser.objects.filter(
            paper_id=paper_id,
            is_finished=True,
            is_delete=False)
        for paper_user in paper_users:
            user_list.append(User.objects.get(uid=paper_user.uid))
        return user_list
    else:
        return []


def get_user_answers(paper_id: str, user_id: str) -> list:
    """
    根据学生id和试卷id获取答题情况
    [[填空题]，[问答题]，[实际操作题]]
    :param paper_id: 试卷id
    :param user_id: 用户id
    :return: [[填空题]，[问答题]，[实际操作题]]
    """
    if user_id != 'all':
        for problem_type in ['fillblank', 'QA', 'operate']:
            temp_answers = get_a_kind_of_problem_answers(paper_id, user_id, problem_type)
            for answer in temp_answers:
                answer.content, answer.standard_answer = get_problem_standard_answer(problem_type, answer.problem_id)
            yield temp_answers
    else:
        for _ in range(3):
            yield []


@deal_exceptions(return_when_exceptions=False)
def save_user_scores(paper_id: str, user_id: str, scores_info: dict) -> bool:
    """
    将老师的评分信息保存到数据库
    :param paper_id: 试卷id
    :param user_id: 用户id
    :param scores_info: 老师评分信息
    :return: 是否保存成功
    """
    for key, value in scores_info.items():
        problem_id, problem_type = key.split('_')
        UTA = UserTextAnswer.objects.get(
            paper_id=paper_id,
            uid=user_id,
            problem_id=problem_id,
            problem_type=problem_type,
        )
        UTA.scores = value
        UTA.save()
    return True


def add_index_to_problems(raw_problems: list) -> list:
    """
    为每道题目添加临时序号
    方便考试时学生能够快速定位试题
    :param raw_problems: 未添加序号的问题列表(格式为get_exam_problems的返回值)
    :return: 添加临时序号之后的列表
    """
    index = 0
    for each_kind_of_problems in raw_problems:
        for each_problem in each_kind_of_problems:
            index += 1
            each_problem.temp_index = index
    return raw_problems


# @deal_exceptions(return_when_exceptions=False)
def save_user_answers(user: User, paper: Paper, user_answers: dict) -> bool:
    """
    将用户的回答保存到PaperUser,UserChoiceAnswer,UserJudgeAnswer,UserTextAnswer
    :param user: 用户对象
    :param paper: 试卷对象
    :param user_answers: 用户答案的字典
    :return: 是否保存成功
    """
    update_paper_user(paper_id=paper.paper_id, uid=user.uid)
    save_problem_answers(
        paper_id=paper.paper_id,
        user_id=user.uid,
        user_answers=user_answers
    )
    return True


def get_paper(paper_id: str) -> Paper:
    """
    根据试卷id获取试卷对象
    :param paper_id: 试卷id
    :return: 试卷对象
    """
    try:
        return get_object_or_404(Paper, paper_id=paper_id)
    except ValueError:
        return None
