from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response, get_object_or_404, get_list_or_404, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .app_helper.views_helper import (is_post_or_get, get_user_or_none, sign_up_user_or_none,
                                      get_user_do_and_undo_paper_list, get_student_list)
from .models import User


# Create your views here.


def start_page(request):
    """
    起始页面(跳转到登陆界面)
    """
    return redirect('ExamApp:登录')


@is_post_or_get(get_render_html='login.html')
def user_login(request):
    """
    用户登陆页面
    """
    user = get_user_or_none(request)
    if user is not None:
        login(request, user)
        if not user.is_teacher:
            return redirect('ExamApp:学生主页', username=user.username)
        else:
            return redirect('ExamApp:老师主页', username=user.username, class_name='all')
    else:
        return render_to_response('login.html', {'error': '密码错误'})


def user_logout(request):
    """
    用户登出后展示页面
    """
    logout(request)
    return redirect('ExamApp:登录')


@is_post_or_get(get_render_html='create_user.html')
def create_user(request):
    """
    创建用户界面
    用户(姓名, 学号(用户名)，密码，班级名)
    """
    try:
        user = sign_up_user_or_none(request)
        if user is not None:
            #TODO 弹出页面显示:创建用户成功，5秒之后去往主界面
            pass
        else:
            #TODO render渲染，提示用户密码格式不正确
            pass
    except:
        #TODO 提示用户请输入完整信息后再提交
        pass


def page_not_found(request):
    """
    404页面
    """
    return render_to_response('404.html')


@login_required
@csrf_exempt
def commit_bug(request, username):
    """
    提交bug页面
    :param request:
    :param username: 用户的学号
    """
    if request.method == 'POST':
        bug_information = request.POST['bug_information']
        # TODO bug信息发送到后台
        return render(request, 'bug.html', {'commit_result': True})
    else:
        user = get_object_or_404(User, username=username)
        return render_to_response('bug.html', {'user': user, 'commit_result': None})


@login_required
def student_home_page(request, username):
    """
    学生主页
    :param request
    :param username: 用户的学号
    :return:
    """
    user = get_object_or_404(User, username=username)
    finished_paper_list, unfinished_paper_list = get_user_do_and_undo_paper_list(user.uid)
    return render_to_response(
        'student_examlist.html',
        {
            'user': user,
            'finished_paper_list': finished_paper_list,
            'unfinished_paper_list': unfinished_paper_list,
        })


@login_required
def teacher_home_page(request, username: str, class_name: str):
    """
    老师主页
    :param request:
    :param username: 老师的工号
    :param class_name: 展示信息班级名
    """
    user = get_object_or_404(User, username=username)
    student_list = get_student_list(user_id=user.uid, class_name=class_name)
    return render_to_response(
        'T_manage_student.html',
        {
            'user': user,
            'student_list': student_list,
            'class_name': class_name,
        })


@login_required
def admin_problems(request, username: str):
    """
    老师管理题库页面
    :param request:
    :param username: 老师的工号
    """
    user = get_object_or_404(User, username=username)
    return render_to_response(
        'T_manage_problems.html',
        {
            'user': user,
        }
    )


@login_required
def create_paper(request, username: str):
    """
    老师创建试卷页面
    :param request:
    :param username: 老师的工号
    """
    user = get_object_or_404(User, username=username)
    return render_to_response(
        'T_create_paper.html',
        {
            'user': user,
        }
    )
