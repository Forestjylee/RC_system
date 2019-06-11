from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

from .models import (User, Student, Course,
                     StudentCourse, StudentAbsentSituation)


admin.site.site_header = "后台管理系统"
admin.site.site_title = "点名系统后台"


# 使用Django默认的用户类
admin.register(User, UserAdmin)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    # 自定义管理界面
    list_display = ['id', 'student_id', 'name', 'class_name',
                    'create_time', 'last_updated_time']
    list_filter = ['class_name']
    search_fields = ['name', 'class_name']
    list_per_page = 20

    fieldsets = [
        ("学生信息", {"fields": ['student_id', 'name', 'class_name']}),
    ]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    # 自定义管理界面
    list_display = ['course_id', 'name', 'teacher', 'student_amount', 'course_time',
                    'create_time', 'last_updated_time']    # 显示在管理界面的列
    list_filter = ['teacher', 'name']                      # 数据过滤字段
    search_fields = ['teacher', 'name']                    # 数据搜索字段
    list_per_page = 20

    # 添加，修改数据项时有分栏目的效果
    fieldsets = [
        ("课程信息", {"fields": ['name', 'teacher', 'student_amount', 'course_time']}),
    ]


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):

    list_display = ['course', 'student', 'attendance_times', 'absent_times']
    list_filter = ['course']
    search_fields = ['course']
    list_per_page = 20

    fieldsets = [
        ("学生课程对应情况", {"fields": ['course', 'student']}),
        ("出、缺勤情况", {"fields": ['attendance_times', 'absent_times']})
    ]


@admin.register(StudentAbsentSituation)
class StudentAbsentSituationAdmin(admin.ModelAdmin):

    def absent_or_late(self):
        text = '缺席' if self.absent_or_late else '迟到'
        return format_html('<span style="color: red;">{}</span>', text)

    def is_ask_for_leave(self):
        if self.is_ask_for_leave:
            color = 'green'
            text = '已请假'
        else:
            color = 'red'
            text = '未请假'
        return format_html('<span style="color: {};">{}</span>', color, text)

    absent_or_late.short_description = '缺席或迟到'
    is_ask_for_leave.short_description = '是否请假'
    # 自定义管理界面
    list_display = ['id', 'student', 'course', absent_or_late,
                    is_ask_for_leave, 'absent_time', 'last_updated_time']       # 显示在管理界面的列
    list_filter = ['student', 'course', 'absent_or_late', 'is_ask_for_leave']   # 数据过滤字段
    search_fields = ['course', 'student']                                       # 数据搜索字段
    list_per_page = 20

    # 添加，修改数据项时有分栏目的效果
    fieldsets = [
        ("缺席情况", {"fields": ['student', 'course', 'absent_or_late', 'is_ask_for_leave', 'absent_time']}),
    ]
