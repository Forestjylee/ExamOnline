# 数据库考试管理系统📜

✨ExamOnline✨

## 1. 要求✴

#### 设计一个小型的数据库考试管理系统

##### （1）有选择题、填空题、问答题，实际操作题

##### （2）有管理员，老师，学生三种用户

##### （3）有用户管理、试题管理，组卷，考试、评分、统计、查询等功能

##### （4）题目的内容要求是数据库的知识（也就是考数据库的知识），有正确的题目和正确的答案。



## 2. 后台数据库设计

#### 数据库名称：exam_system

#### 数据库中的表：User，ChoiceProblem，JudgeProblem， FillBlankProblem，QAProblem，OperateProblem

##### （1）User（用户表）✅已实现

属性：主键uid，username（学号/登录名），real_name（真实姓名），password（密码），class_name（班级名），create_time（创建时间，创建时自动添加）

##### （2）ChoiceProblem（选择题表）✅已实现

属性：主键id，content（题目内容），level（题目难度），tag（题目标签），author（作者），option_A（A选项内容），option_B（B选项内容），option_C（C选项内容），option_D（D选项内容），answer（答案【支持多选】），is_delete（是否被删除），create_time（创建时间）

##### （3）JudgeProblem（判断题）✅已实现

属性：主键id，content（题目内容），level（题目难度），tag（题目标签），author（作者），answer（答案），is_delete（是否被删除）， create_time（创建时间）

##### （4）FillBlankProblem（填空题）✅已实现

属性：主键id，content（题目内容），level（题目难度），tag（题目标签），author（作者），answer（答案），is_delete（是否被删除）， create_time（创建时间）

##### （5）QAProblem（问答题）✅已实现

属性：主键id，content（题目内容），level（题目难度），tag（题目标签），author（作者），answer（答案【text类型】），is_delete（是否被删除）， create_time（创建时间）

##### （6）OperateProblem（实际操作题）✅已实现

属性：主键id，content（题目内容），level（题目难度），tag（题目标签），author（作者），answer（答案【text类型】），is_delete（是否被删除）， create_time（创建时间）

##### （7）Paper（试卷表）⭕【待实现】

属性：主键id，paper_id，paper_name（试卷名），paper_tag（试卷标签），author（作者），start_time（开始时间），end_time（结束时间），is_delete（是否被删除），create_time（创建时间）

##### （8）Paper_Problem（试卷和试题关系表）⭕【待实现】

属性：主键id，paper_id，problem_type（题目类型），problem_id（题目的id），start_time（开始时间），end_time（结束时间），is_delete（是否被删除），create_time（创建时间）

##### （9）Paper_User（试卷和用户关系表）⭕【待实现】

属性：主键id， paper_id，user（外键），is_delete（是否被删除），create_time（创建时间）



## 3. html页面设计📖

### 3.0 老师学生公用页面

#### （1）登录页面

#### （2）注册页面

#### （3）bug提交页面（一个输入框一个按钮）

### 3.1 老师专用页面

#### （1）老师主页

#### （2）用户管理页面（增删查改学生）

#### （3）试题管理页面（编写题目）

#### （4）组卷，发布试卷页面（选择题目组合成试卷并设置开始和截止时间发布试卷）

#### （5）评分页面（显示学生答案和参考答案，并提高一个打分框）

#### （6）统计成绩，导出页面

### 3.2 学生专用页面

#### （1）学生主页

#### （2）考试页面

#### （3）考试成绩展示页面

#### （4）试卷参考答案页面



## 4. 题库设计✒

#### 出一定数量的选择题、判断题，填空题、问答题，实际操作题并提供正确答案。

#### （1）选择题（支持多选，自动评分，题目字数小于200字）

#### （2）判断题（自动评分，题目字数小于100字）【选做】

#### （3）填空题（题目字数小于200字【包括下划线】）

#### （4）问答题（题目字数小于200字）

#### （5）实际操作题（题目字数小于200字）



## 5. 其他

### 5.1 开发环境💻

#### 操作系统：Windows 10 (64bit)

#### 数据库：MySQL 5.7.22 community

#### 编程语言：Python，Html，CSS，JavaScript

#### WEB框架：Django 2.1

### 5.2项目管理

#### github：🌏https://github.com/Forest75/ExamOnline

#### 包管理工具：🛠Pipenv （version 2018.10.13）