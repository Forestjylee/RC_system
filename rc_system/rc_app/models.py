from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 若使用MySQL，创建数据库时记得指定 CHARACTER SET UTF8;
# 若makemigrations出错，先执行`python manage.py makemigrations --empty rc_app`


class Student(models.Model):
    """学生信息"""
    student_id = models.IntegerField(primary_key=True, verbose_name="学号")
    name = models.CharField(verbose_name="姓名", max_length=30)
    class_name = models.CharField(verbose_name="班级", max_length=30)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    def __str__(self):
        return f"{self.student_id}-{self.name}"

    class Meta:
        verbose_name_plural = '学生信息'                 # 在管理界面中表的名字
        db_table = 'Student'                            # 在MySQL中表的名字
        ordering = ['class_name', 'last_updated_time']


class Course(models.Model):
    """课程信息"""
    course_id = models.AutoField(primary_key=True, verbose_name="课程id")
    name = models.CharField(verbose_name="课程", max_length=30)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="老师")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    def __str__(self):
        return f"{self.course_id}-{self.name}"

    class Meta:
        verbose_name_plural = '课程'       # 在管理界面中表的名字
        db_table = 'Course'                # 在MySQL中表的名字
        ordering = ['last_updated_time']   # 在管理界面按照最后更新时间排序


class StudentAbsentSituation(models.Model):
    """学生缺席情况"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")
    absent_or_late = models.BooleanField(verbose_name="缺席还是迟到", default=True,
                                         choices=((True, '缺席'), (False, '迟到')))     # 默认缺席(True)
    is_ask_for_leave = models.BooleanField(verbose_name="是否请假", default=False,
                                           choices=((True, '已请假'), (False, '未请假')))
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_updated_time = models.DateTimeField(verbose_name="最后修改时间", auto_now=True)

    def __str__(self):
        return f"{self.student.name}"

    class Meta:
        verbose_name_plural = '学生缺席情况'
        db_table = 'StudentAbsentSituation'
        ordering = ['create_time']
