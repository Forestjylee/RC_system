from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

from .models import User, Student, StudentCourse
from .app_helper.decorators import is_post_or_get
from .app_helper.views_helper import (get_user_or_none,  save_upload_face_photo,
                                      detect_and_compare_faces, get_courses_or_none,
                                      get_students_or_none)

# Create your views here.


def start_page(request):
    """起始页面(跳转到登录界面)"""
    return redirect('rc_app:登录')


@is_post_or_get(render_html='login.html')
def user_login(request):
    """登录页面"""
    user = get_user_or_none(request)
    if user is not None:
        login(request, user)
        return redirect('rc_app:主页', username=user.username, course_index=0)
    else:
        return render(request, 'login.html', {'error': '用户名或密码错误'})


def user_logout(request):
    """用户登出"""
    logout(request)
    return redirect('rc_app:登录')


@login_required
def home_page(request, username: str, course_index: str):
    """主页"""
    context = {}
    course_index = int(course_index)
    teacher = get_object_or_404(User, username=username)
    courses = get_courses_or_none(teacher=teacher)
    context['username'] = username
    context['courses'] = courses
    context['index'] = course_index
    if courses:
        if course_index >= len(courses):
            return render_to_response('404.html')
        context['student_amount'] = courses[course_index].student_amount
    if request.method == 'POST':
        file_obj = request.FILES.get('face_photo')
        filepath, result = save_upload_face_photo(file_obj, username)
        if result:
            file_type, face_amount = detect_and_compare_faces(username, filepath)
            if not file_type:
                context['error'] = '暂不支持您上传的图片格式，请上传png、jpg、jpeg格式的图片'
            else:
                context['file_type'] = file_type
                context['face_amount'] = face_amount
                context['attendance_rate'] = round(face_amount / context['student_amount'], 4) * 100
    return render(request, 'face.html', context=context)


@login_required
def specific_name_list(request, username: str):
    """学生点名详细名单"""
    return render(request, 'Specific_info.html', {'username': username})


@login_required
def manage_course(request, username: str):
    """管理课程(个人中心)"""
    context = {'username': username}
    teacher = get_object_or_404(User, username=username)
    courses = get_courses_or_none(teacher=teacher)
    context['courses'] = courses
    return render(request, 'Class_Info.html', context=context)


@login_required
def manage_course_student(request, username: str, course_id: str):
    """管理课程中的学生"""
    context = {'username': username}
    course_id = int(course_id)
    teacher = get_object_or_404(User, username=username)
    courses = get_courses_or_none(teacher=teacher)
    students = get_students_or_none(course_id=course_id)
    context['students'] = students
    for course in courses:
        if course.course_id == course_id:
            context['course'] = course
    for student in students:
        sc = get_object_or_404(StudentCourse, student=student, course=course)
        student.attendance_times = sc.attendance_times
        student.absent_times = sc.absent_times
    return render(request, 'Class_Member.html', context=context)


@login_required
def manage_student(request, username: str):
    """管理学生"""
    return render(request, 'manage_student.html', {'username': username})


@login_required
def absent_record(request, username: str, student_id: str):
    """缺勤记录"""
    context = {'username': username}
    student = get_object_or_404(Student, student_id=student_id)
    context['student'] = student
    return render(request, 'Absent_Record.html', context=context)


def page_not_found(request, exception: Exception=None):
    """404"""
    return render_to_response('404.html')
