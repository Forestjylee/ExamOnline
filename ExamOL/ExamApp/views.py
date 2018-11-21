from django.shortcuts import redirect, render_to_response
from django.contrib.auth import login, logout
from .app_helper.views_helper import is_post_or_get, get_user_or_none, sign_up_user_or_none

from django.http import HttpResponse

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
        # return HttpResponse(f"{user.real_name}{'老师' if user.is_teacher else '同学'}登录成功!")
        return redirect("ExamApp:404")
        #TODO 跳转到登陆成功之后的界面(判断是老师还是学生)
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


def page_404(request):
    """
    404页面
    """
    return render_to_response('404.html')
