from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 创建数据库时记得指定 CHARACTER SET UTF8；
# 若makemigrations出错,先执行`python manage.py makemigrations --empty ExamApp`
# 然后再makemigrations和migrate

# level难度暂时分为3个（1->简单，2->中等，3->困难）


class User(AbstractUser):
    """
    用户类模型
    """
    uid = models.AutoField(primary_key=True, verbose_name="用户编号")
    real_name = models.CharField(max_length=30, verbose_name="姓名")
    is_teacher = models.BooleanField(verbose_name="是否为老师", default=False)
    username = models.CharField(max_length=30, verbose_name="学号", unique=True)
    class_name = models.CharField(max_length=50, verbose_name="班级", blank=True, default='未知')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户'    # 在管理界面中表的名字
        ordering = ['class_name']       # 在管理界面按照班级名称排序


class Paper(models.Model):
    """
    试卷表模型
    """
    paper_id = models.AutoField(primary_key=True, verbose_name="试卷编号")
    owner_id = models.IntegerField(verbose_name="试卷管理员id", default=0)
    level = models.IntegerField(verbose_name="难度系数", default=1,
                                choices=((1, '简单'), (2, '中等'), (3, '困难')))
    paper_name = models.CharField(max_length=50, verbose_name="试卷名称")
    tag = models.CharField(max_length=50, verbose_name="试卷标签", default='数据库', blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", default='未知', blank=True)
    each_choice_problem_score = models.FloatField(verbose_name="每道选择题分数", default=0)
    each_judge_problem_score = models.FloatField(verbose_name="每道判断题分数", default=0)
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.paper_name[:10]

    class Meta:
        verbose_name_plural = '试卷'          # 在管理界面中表的名字
        db_table = 'Paper'                    # 在MySQL中表的名字
        ordering = ['last_updated_time']      # 在管理界面按照创建时间排序


class ChoiceProblem(models.Model):
    """
    选择题模型
    """
    problem_type = models.CharField(max_length=50, verbose_name="题目类型", default="选择题")
    content = models.CharField(max_length=200, verbose_name="题目内容")
    level = models.IntegerField(verbose_name="难度系数", default=1,
                                choices=((1, '简单'), (2, '中等'), (3, '困难')))
    tag = models.CharField(max_length=50, verbose_name="标签", default='数据库', blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", default='未知', blank=True)
    option_A = models.CharField(max_length=50, verbose_name="A选项")
    option_B = models.CharField(max_length=50, verbose_name="B选项")
    option_C = models.CharField(max_length=50, verbose_name="C选项")
    option_D = models.CharField(max_length=50, verbose_name="D选项")
    answer = models.IntegerField(verbose_name="参考答案",
                                 choices=((1, 'A'), (2, 'B'),
                                          (3, 'C'), (4, 'D')))
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '选择题'         # 在管理界面中表的名字
        db_table = 'ChoiceProblem'            # 在MySQL中表的名字
        ordering = ['last_updated_time']      # 在管理界面按照创建时间排序


class JudgeProblem(models.Model):
    """
    判断题模型
    """
    problem_type = models.CharField(max_length=50, verbose_name="题目类型", default="判断题")
    content = models.CharField(max_length=100, verbose_name="题目内容")
    level = models.IntegerField(verbose_name="难度系数", default=1,
                                choices=((1, '简单'), (2, '中等'), (3, '困难')))
    tag = models.CharField(max_length=50, verbose_name="标签", default='数据库', blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", default='未知', blank=True)
    answer = models.BooleanField(verbose_name="是否正确")
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '判断题'         # 在管理界面中表的名字
        db_table = 'JudgeProblem'             # 在MySQL中表的名字
        ordering = ['last_updated_time']      # 在管理界面按照创建时间排序


class FillBlankProblem(models.Model):
    """
    填空题模型
    """
    problem_type = models.CharField(max_length=50, verbose_name="题目类型", default="填空题")
    content = models.CharField(max_length=200, verbose_name="题目内容")
    level = models.IntegerField(verbose_name="难度系数", default=1,
                                choices=((1, '简单'), (2, '中等'), (3, '困难')))
    tag = models.CharField(max_length=50, verbose_name="标签", default='数据库', blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", default='未知', blank=True)
    answer = models.CharField(max_length=200, verbose_name="参考答案")
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '填空题'         # 在管理界面中表的名字
        db_table = 'FillBlankProblem'         # 在MySQL中表的名字
        ordering = ['last_updated_time']      # 在管理界面按照创建时间排序


class QAProblem(models.Model):
    """
    问答题模型
    """
    problem_type = models.CharField(max_length=50, verbose_name="题目类型", default="问答题")
    content = models.TextField(verbose_name="题目内容")
    level = models.IntegerField(verbose_name="难度系数", default=1,
                                choices=((1, '简单'), (2, '中等'), (3, '困难')))
    tag = models.CharField(max_length=50, verbose_name="标签", default='数据库', blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", default='未知', blank=True)
    answer = models.TextField(verbose_name="参考答案")
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '问答题'         # 在管理界面中表的名字
        db_table = 'QAProblem'                # 在MySQL中表的名字
        ordering = ['last_updated_time']      # 在管理界面按照创建时间排序


class OperateProblem(models.Model):
    """
    世家操作题模型
    """
    problem_type = models.CharField(max_length=50, verbose_name="题目类型", default="实际操作题")
    content = models.TextField(verbose_name="题目内容")
    level = models.IntegerField(verbose_name="难度系数", default=1,
                                choices=((1, '简单'), (2, '中等'), (3, '困难')))
    tag = models.CharField(max_length=50, verbose_name="标签", default='数据库', blank=True)
    author = models.CharField(max_length=50, verbose_name="作者", default='未知', blank=True)
    answer = models.TextField(verbose_name="参考答案")
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = '实际操作题'      # 在管理界面中表的名字
        db_table = 'OperateProblem'            # 在MySQL数据库中表的名字
        ordering = ['last_updated_time']       # 在管理界面按照创建时间排序


class UserAnswerSituation(models.Model):
    """
    用户答题情况
    """
    id = models.AutoField(primary_key=True, verbose_name="答题情况id")
    correct_choice_problem_amount = models.IntegerField(verbose_name="用户答对的选择题数", default=0)
    correct_judge_problem_amount = models.IntegerField(verbose_name="用户答对的判断题数", default=0)
    fill_blank_problem_scores = models.FloatField(verbose_name="用户填空题总得分", default=0)
    QA_problem_scores = models.FloatField(verbose_name="用户问答题总得分", default=0)
    operate_problem_scores = models.FloatField(verbose_name="用户操作题总得分", default=0)
    sum_scores = models.FloatField(verbose_name="总分", default=0)
    last_updated_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

    def __str__(self):
        return f"{self.id}-ans_situation"

    class Meta:
        verbose_name_plural = '用户答题与得分情况'         # 在管理界面中表的名字
        db_table = 'User_Answer_Situation'               # 在MySQL中表的名字
        ordering = ['last_updated_time']                 # 在管理界面按照创建时间排序


class PaperProblem(models.Model):
    """
    试卷与试题关系表
    """
    paper_id = models.IntegerField(verbose_name="试卷编号")
    problem_type = models.CharField(max_length=50, verbose_name="题目类型")
    problem_id = models.IntegerField(verbose_name="题目编号")
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return f"{self.paper_id}-{self.problem_id}"

    class Meta:
        verbose_name_plural = '试卷与试题关系'    # 在管理界面中表的名字
        db_table = 'Paper_Problem'               # 在MySQL中表的名字
        ordering = ['paper_id']                  # 在管理界面按照创建时间排序


class PaperUser(models.Model):
    """
    试卷与用户关系
    """
    paper_id = models.IntegerField(verbose_name="试卷编号")
    uid = models.IntegerField(verbose_name="用户编号")
    is_finished = models.BooleanField(verbose_name="是否已完成试卷", default=False)
    answer_situation = models.ForeignKey(UserAnswerSituation, on_delete=models.CASCADE,
                                         verbose_name="用户答题情况", default='')
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    last_updated_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

    def __str__(self):
        return f"{self.paper_id}-{self.uid}"

    class Meta:
        verbose_name_plural = '试卷与用户关系'    # 在管理界面中表的名字
        db_table = 'Paper_User'                  # 在MySQL中表的名字
        ordering = ['paper_id']                  # 在管理界面按照创建时间排序


class UserChoiceAnswer(models.Model):
    """
    用户选择题答案
    user_answer = {
        1 -> A
        2 -> B
        2 -> C
        4 -> D
    }
    """
    paper_id = models.IntegerField(verbose_name="试卷编号")
    uid = models.IntegerField(verbose_name="用户编号")
    problem_id = models.IntegerField(verbose_name="题目编号")
    user_answer = models.IntegerField(verbose_name="用户答案")
    is_correct = models.BooleanField(verbose_name="回答是否正确", default=False)
    last_updated_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

    def __str__(self):
        return f"{self.paper_id}-{self.uid}-{self.problem_id}-answer"

    class Meta:
        verbose_name_plural = '用户选择题答案'          # 在管理界面中表的名字
        db_table = 'User_Choice_Answer'                # 在MySQL中表的名字
        ordering = ['paper_id', 'last_updated_time']   # 在管理界面按照创建时间排序


class UserJudgeAnswer(models.Model):
    """
    用户判断题答案
    """
    paper_id = models.IntegerField(verbose_name="试卷编号")
    uid = models.IntegerField(verbose_name="用户编号")
    problem_id = models.IntegerField(verbose_name="题目编号")
    user_answer = models.BooleanField(verbose_name="用户答案")
    is_correct = models.BooleanField(verbose_name="回答是否正确", default=False)
    last_updated_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

    def __str__(self):
        return f"{self.paper_id}-{self.uid}-{self.problem_id}-answer"

    class Meta:
        verbose_name_plural = '用户判断题答案'          # 在管理界面中表的名字
        db_table = 'User_Judge_Answer'                 # 在MySQL中表的名字
        ordering = ['paper_id', 'last_updated_time']   # 在管理界面按照创建时间排序


class UserTextAnswer(models.Model):
    """
    用户非选择判断题的答案
    """
    paper_id = models.IntegerField(verbose_name="试卷编号")
    uid = models.IntegerField(verbose_name="用户编号")
    problem_id = models.IntegerField(verbose_name="题目编号")
    problem_type = models.CharField(verbose_name="题目类型", max_length=50)
    user_answer = models.TextField(verbose_name="用户答案")
    scores = models.IntegerField(verbose_name="得分", default=0)
    last_updated_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

    def __str__(self):
        return f"{self.paper_id}-{self.uid}-{self.problem_id}-answer"

    class Meta:
        verbose_name_plural = '用户非选择判断题答案'     # 在管理界面中表的名字
        db_table = 'User_Text_Answer'                  # 在MySQL中表的名字
        ordering = ['paper_id', 'last_updated_time']   # 在管理界面按照创建时间排序


class TeacherStudent(models.Model):
    """
    老师与学生关系
    """
    teacher_id = models.IntegerField(verbose_name="老师编号")
    student_id = models.IntegerField(verbose_name="学生编号")
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    last_updated_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

    def __str__(self):
        return f"{self.teacher_id}-{self.student_id}"

    class Meta:
        verbose_name_plural = '老师与学生关系'     # 在管理界面中表的名字
        db_table = 'Tea_Stu'                     # 在MySQL中表的名字
        ordering = ['teacher_id']                # 在管理界面按照创建时间排序


class TeacherClass(models.Model):
    """
    老师与班级的关系
    """
    teacher_id = models.IntegerField(verbose_name="老师编号")
    class_name = models.CharField(verbose_name="班级", max_length=50)
    is_delete = models.BooleanField(verbose_name="是否被删除", default=False)
    last_updated_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

    def __str__(self):
        return f"{self.teacher_id}-{self.class_name}"

    class Meta:
        verbose_name_plural = '老师与班级的关系'   # 在管理界面中表的名字
        db_table = 'Tea_Class'                   # 在MySQL中表的名字
        ordering = ['teacher_id']                # 在管理界面按照创建时间排序
