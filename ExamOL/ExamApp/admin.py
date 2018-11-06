from django.contrib import admin
from .models import Problem, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['uid', 'username', 'class_name', 'create_time']
    list_filter = ['class_name']
    search_fields = ['class_name', 'username']
    list_per_page = 20

    fieldsets = [
        ("用户信息", {"fields": ['username', 'password', 'class_name']}),
    ]


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):

    # 自定义管理界面
    list_display = ['tag', 'level', 'author', 'create_time']     # 显示在管理界面的列
    list_filter = ['level']                                      # 数据过滤字段
    search_fields = ['tag', 'level', 'author']                   # 数据搜索字段
    list_per_page = 20

    # 添加，修改数据项时有分栏目的效果
    fieldsets = [
        ("题目信息", {"fields": ['content', 'level', 'option_A',
                                'option_B', 'option_C', 'option_D']}),
        ("其他信息(选填)", {"fields": ['author', 'tag']}),
    ]