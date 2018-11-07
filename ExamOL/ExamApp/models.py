from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 创建数据库时记得指定 CHARACTER SET UTF8；


class User(AbstractUser):
    """
    用户类模型
    """
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, verbose_name="学号", unique=True)
    real_name = models.CharField(max_length=30, verbose_name="姓名")
    class_name = models.CharField(max_length=50, verbose_name="班级")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户'    # 在管理界面中表的名字
        ordering = ['class_name']       # 在管理界面按照班级名称排序


class ChoiceProblem(models.Model):
    """
    选择题模型
    """
    content = models.CharField(max_length=200, verbose_name="题目内容")
    level=models.IntegerField(verbose_name="难度系数")
    tag = models.CharField(max_length=50, verbose_name="标签", null=True, blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", null=True, blank=True)
    option_A = models.CharField(max_length=50, verbose_name="A选项")
    option_B = models.CharField(max_length=50, verbose_name="B选项")
    option_C = models.CharField(max_length=50, verbose_name="C选项")
    option_D = models.CharField(max_length=50, verbose_name="D选项")
    answer = models.CharField(max_length=40, verbose_name="参考答案",
                              choices=(('option_A', 'A'), ('option_B', 'B'),
                                       ('option_C', 'C'), ('option_D', 'D')))
    is_delete = models.BooleanField(verbose_name="是否存在", default=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '选择题'   # 在管理界面中表的名字
        db_table = 'ChoiceProblem'      # 在MySQL中表的名字
        ordering = ['create_time']      # 在管理界面按照创建时间排序


class JudgeProblem(models.Model):
    """
    判断题模型
    """
    content = models.CharField(max_length=100, verbose_name="题目内容")
    level=models.IntegerField(verbose_name="难度系数")
    tag = models.CharField(max_length=50, verbose_name="标签", null=True, blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", null=True, blank=True)
    answer = models.BooleanField(verbose_name="是否正确")
    is_delete = models.BooleanField(verbose_name="是否存在", default=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '判断题'   # 在管理界面中表的名字
        db_table = 'JudgeProblem'       # 在MySQL中表的名字
        ordering = ['create_time']      # 在管理界面按照创建时间排序


class FillBlankProblem(models.Model):
    """
    填空题模型
    """
    content = models.CharField(max_length=200, verbose_name="题目内容")
    level=models.IntegerField(verbose_name="难度系数")
    tag = models.CharField(max_length=50, verbose_name="标签", null=True, blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", null=True, blank=True)
    answer = models.CharField(max_length=200, verbose_name="参考答案")
    is_delete = models.BooleanField(verbose_name="是否存在", default=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '填空题'   # 在管理界面中表的名字
        db_table = 'FillBlankProblem'   # 在MySQL中表的名字
        ordering = ['create_time']      # 在管理界面按照创建时间排序


class QAProblem(models.Model):
    """
    问答题模型
    """
    content = models.CharField(max_length=200, verbose_name="题目内容")
    level=models.IntegerField(verbose_name="难度系数")
    tag = models.CharField(max_length=50, verbose_name="标签", null=True, blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", null=True, blank=True)
    answer = models.TextField(verbose_name="参考答案")
    is_delete = models.BooleanField(verbose_name="是否存在", default=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '问答题'   # 在管理界面中表的名字
        db_table = 'QAProblem'          # 在MySQL中表的名字
        ordering = ['create_time']      # 在管理界面按照创建时间排序


class OperateProblem(models.Model):
    """
    世家操作题模型
    """
    content = models.CharField(max_length=200, verbose_name="题目内容")
    level=models.IntegerField(verbose_name="难度系数")
    tag = models.CharField(max_length=50, verbose_name="标签", null=True, blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", null=True, blank=True)
    answer = models.TextField(verbose_name="参考答案")
    is_delete = models.BooleanField(verbose_name="是否存在", default=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '实际操作题'# 在管理界面中表的名字
        db_table = 'OperateProblem'      # 在MySQL数据库中表的名字
        ordering = ['create_time']       # 在管理界面按照创建时间排序