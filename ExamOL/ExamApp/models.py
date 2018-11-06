from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """
    用户类模型
    """
    uid = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50, verbose_name="班级")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.username


class Problem(models.Model):
    """
    题目模型
    """
    content = models.CharField(max_length=100, verbose_name="题目内容")
    level=models.IntegerField(verbose_name="难度系数")
    tag = models.CharField(max_length=50, verbose_name="标签", null=True, blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", null=True, blank=True)
    option_A = models.CharField(max_length=50, verbose_name="A选项")
    option_B = models.CharField(max_length=50, verbose_name="B选项")
    option_C = models.CharField(max_length=50, verbose_name="C选项")
    option_D = models.CharField(max_length=50, verbose_name="D选项")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        db_table = 'Problem'      # 在MySQL数据库中表的名字
        ordering = ['id']         # 在管理界面按照id排序