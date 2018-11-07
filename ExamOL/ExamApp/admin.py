from django.contrib import admin
from django.utils.html import format_html
from .models import (User, ChoiceProblem, JudgeProblem,
                     FillBlankProblem, QAProblem, OperateProblem)

# Register your models here.

admin.site.site_header="考试平台管理系统"
admin.site.site_title="考试平台运维"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    def is_teacher(self):
        if self.is_teacher:
            return '老师'
        else:
            return '学生'

    # 自定义管理界面
    is_teacher.short_description = '身份'
    list_display = ['username', 'real_name','class_name', is_teacher]
    list_filter = ['class_name', 'is_teacher']
    search_fields = ['class_name', 'username', 'real_name']
    list_per_page = 20

    fieldsets = [
        ("用户信息", {"fields": ['real_name', 'username', 'password',
                                'class_name', 'is_teacher']}),
    ]


@admin.register(ChoiceProblem)
class ChoiceProblemAdmin(admin.ModelAdmin):

    def is_delete(self):
        if self.is_delete:
            color_code = 'green'
            text = '存在'
        else:
            color_code = 'red'
            text =  "不存在"
        return format_html('<span style="color: {};">{}</span>',
                           color_code, text)

    # 自定义管理界面
    is_delete.short_description = '是否存在'
    list_display = ['tag', 'level', 'author',
                    'create_time', is_delete]                    # 显示在管理界面的列
    list_filter = ['level', 'tag', 'is_delete']                  # 数据过滤字段
    search_fields = ['tag', 'level', 'author']                   # 数据搜索字段
    list_per_page = 20

    # 添加，修改数据项时有分栏目的效果
    fieldsets = [
        ("题目信息", {"fields": ['content', 'level', 'option_A',
                                'option_B', 'option_C', 'option_D', 'answer']}),
        ("其他信息(选填)", {"fields": ['author', 'tag', 'is_delete']}),
    ]


@admin.register(JudgeProblem)
class JudgeProblemAdmin(admin.ModelAdmin):

    def is_delete(self):
        if self.is_delete:
            color_code = 'green'
            text = '存在'
        else:
            color_code = 'red'
            text =  "不存在"
        return format_html('<span style="color: {};">{}</span>',
                           color_code, text)

    # 自定义管理界面
    is_delete.short_description = '是否存在'
    list_display = ['tag', 'level', 'author',
                    'create_time', is_delete]                    # 显示在管理界面的列
    list_filter = ['level', 'tag', 'is_delete']                  # 数据过滤字段
    search_fields = ['tag', 'level', 'author']                   # 数据搜索字段
    list_per_page = 20

    # 添加，修改数据项时有分栏目的效果
    fieldsets = [
        ("题目信息", {"fields": ['content', 'level', 'answer']}),
        ("其他信息(选填)", {"fields": ['author', 'tag', 'is_delete']}),
    ]


@admin.register(FillBlankProblem)
class FillBlankProblemAdmin(admin.ModelAdmin):

    def is_delete(self):
        if self.is_delete:
            color_code = 'green'
            text = '存在'
        else:
            color_code = 'red'
            text =  "不存在"
        return format_html('<span style="color: {};">{}</span>',
                           color_code, text)

    # 自定义管理界面
    is_delete.short_description = '是否存在'
    list_display = ['tag', 'level', 'author',
                    'create_time', is_delete]                    # 显示在管理界面的列
    list_filter = ['level', 'tag', 'is_delete']                  # 数据过滤字段
    search_fields = ['tag', 'level', 'author']                   # 数据搜索字段
    list_per_page = 20

    # 添加，修改数据项时有分栏目的效果
    fieldsets = [
        ("题目信息", {"fields": ['content', 'level', 'answer']}),
        ("其他信息(选填)", {"fields": ['author', 'tag', 'is_delete']}),
    ]


@admin.register(QAProblem)
class QAProblemAdmin(admin.ModelAdmin):

    def is_delete(self):
        if self.is_delete:
            color_code = 'green'
            text = '存在'
        else:
            color_code = 'red'
            text =  "不存在"
        return format_html('<span style="color: {};">{}</span>',
                           color_code, text)

    # 自定义管理界面
    is_delete.short_description = '是否存在'
    list_display = ['tag', 'level', 'author',
                    'create_time', is_delete]                    # 显示在管理界面的列
    list_filter = ['level', 'tag', 'is_delete']                  # 数据过滤字段
    search_fields = ['tag', 'level', 'author']                   # 数据搜索字段
    list_per_page = 20

    # 添加，修改数据项时有分栏目的效果
    fieldsets = [
        ("题目信息", {"fields": ['content', 'level', 'answer']}),
        ("其他信息(选填)", {"fields": ['author', 'tag', 'is_delete']}),
    ]


@admin.register(OperateProblem)
class OperateProblemAdmin(admin.ModelAdmin):

    def is_delete(self):
        if self.is_delete:
            color_code = 'green'
            text = '存在'
        else:
            color_code = 'red'
            text =  "不存在"
        return format_html('<span style="color: {};">{}</span>',
                           color_code, text)

    # 自定义管理界面
    is_delete.short_description = '是否存在'
    list_display = ['tag', 'level', 'author',
                    'create_time', is_delete]                    # 显示在管理界面的列
    list_filter = ['level', 'tag', 'is_delete']                  # 数据过滤字段
    search_fields = ['tag', 'level', 'author']                   # 数据搜索字段
    list_per_page = 20

    # 添加，修改数据项时有分栏目的效果
    fieldsets = [
        ("题目信息", {"fields": ['content', 'level', 'answer']}),
        ("其他信息(选填)", {"fields": ['author', 'tag', 'is_delete']}),
    ]
