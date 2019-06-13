import os
import pickle
import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

from .models import User, Student, Course, StudentCourse, StudentPicture, StudentAbsentSituation
from .app_helper.decorators import is_post_or_get
from .app_helper.views_helper import (get_user_or_none,  save_upload_face_photo,
                                      detect_and_compare_faces, get_courses_or_none,
                                      get_students_or_none, save_student_face_photo,
                                      delete_students, create_student, create_students,
                                      save_student_infos, get_object_or_none, update_course,
                                      create_course, create_student_absent_situation,
                                      save_compressed_student_infos, save_student_face_photos,
                                      get_compare_faces_result)

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
    context['course'] = courses[course_index]
    if courses:
        if course_index >= len(courses):
            return render_to_response('404.html')
        context['student_amount'] = courses[course_index].student_amount
    if request.method == 'POST':
        file_obj = request.FILES.get('face_photo')
        filepath, result = save_upload_face_photo(file_obj, username)
        if result:
            file_type, face_amount, pickle_filepath = detect_and_compare_faces(username, filepath, context['course'])
            if not file_type:
                context['error'] = '暂不支持您上传的图片格式，请上传png、jpg、jpeg格式的图片'
            else:
                if pickle_filepath:
                    context['filepath'] = pickle_filepath
                    attendance_result = get_compare_faces_result(username, pickle_filepath)
                    context['attendance_result'] = attendance_result
                context['file_type'] = file_type
                context['face_amount'] = face_amount
                if context['student_amount']:
                    context['attendance_rate'] = round(face_amount / context['student_amount'], 4) * 100
                else:
                    context['attendance_rate'] = 0
    return render(request, 'face.html', context=context)


@login_required
def specific_name_list(request, username: str, course_id: str, filepath: str):
    """学生点名详细名单"""
    context = {'username': username}
    teacher = get_object_or_404(User, username=username)
    course = get_object_or_404(Course, course_id=course_id)
    context['course'] = course
    context['specific_infos'] = get_compare_faces_result(username, filepath)
    return render(request, 'Specific_Info.html', context)


@login_required
def manage_course(request, username: str):
    """管理课程(个人中心)"""
    context = {'username': username}
    teacher = get_object_or_404(User, username=username)
    if request.method == 'POST':
        if 'delete_courses' in request.POST:
            courses_to_delete = request.POST['delete_courses'].split('!')
            courses = get_courses_or_none(teacher=teacher)
            for course in courses:
                if course.name in courses_to_delete:
                    course.delete()
            context['msg'] = f"删除{'，'.join(courses_to_delete)}课程成功!"
        else:     # 创建或修改课程信息
            course_info = request.POST['create_or_modify_course'].split('!')
            result = create_course(course_name=course_info[0], teacher=teacher, course_time=course_info[1])
            context['msg'] = '操作成功!' if result else '操作失败，请重试!'
    context['courses'] = get_courses_or_none(teacher=teacher)
    return render(request, 'Class_Info.html', context=context)


@login_required
def manage_course_student(request, username: str, course_id: str):
    """管理课程中的学生"""
    context = {'username': username}
    course_id = int(course_id)
    teacher = get_object_or_404(User, username=username)
    courses = get_courses_or_none(teacher=teacher)
    for course in courses:
        if course.course_id == course_id:
            context['course'] = course
    if not context['course']:
        return render_to_response('404.html')
    if request.method == 'POST':
        if 'student_photo' in request.FILES:
            file_object = request.FILES['student_photo']
            student_id = request.POST['stu_id']
            student_name = request.POST['stu_name']
            student_class = request.POST['stu_class']
            create_student(student_id, student_name, student_class, context['course'])
            result = save_student_face_photo(file_object, student_id=student_id, student_name=student_name)
            context['msg'] = result['msg']
        elif 'students_info_file' in request.FILES:
            file_object = request.FILES['students_info_file']
            file_type = os.path.splitext(file_object.name)[-1]
            if file_type == '.zip':
                directory, result = save_compressed_student_infos(file_object, username)
                context['msg'] = save_student_face_photos(source_directory=directory, course=context['course'])
            elif file_type in ['.xls', '.xlsx']:
                file_path, result = save_student_infos(file_object, username)
                context['msg'] = '创建学生成功!' if create_students(file_path, course=context['course']) else '创建学生失败!'
            else:
                context['msg'] = '上传的文件格式错误，请上传 *.zip或 *.xlsx文件！'
        else:     # delete all (student_ids)
            delete_student_ids = request.POST['delete_student_ids'].split('_')
            fail_list = delete_students(student_ids=delete_student_ids, course=context['course'])
            if not fail_list:
                context['msg'] = '删除学生成功!'
            else:
                context['msg'] = f"删除 {', '.join(fail_list)} 学生失败!"
    students = get_students_or_none(course_id=course_id)
    context['students'] = students
    context['course'] = update_course(course=context['course'])
    for student in students:
        sc = get_object_or_404(StudentCourse, student=student, course=context['course'])
        sp = get_object_or_none(StudentPicture, student=student)
        if sp:
            student.student_picture_status = True
        else:
            student.student_picture_status = False
        student.attendance_times = sc.attendance_times
        student.absent_times = sc.absent_times
    return render(request, 'Class_Member.html', context=context)


@login_required
def manage_student(request, username: str):
    """管理学生"""
    return render(request, 'manage_student.html', {'username': username})


@login_required
def absent_record(request, username: str, course_name: str, student_id: str):
    """缺勤记录"""
    context = {'username': username}
    teacher = get_object_or_404(User, username=username)
    student = get_object_or_404(Student, student_id=student_id)
    course = get_object_or_404(Course, teacher=teacher, name=course_name)
    student_absent_records = StudentAbsentSituation.objects.filter(student=student)
    if request.method == 'POST':
        if 'delete_absent_records' in request.POST:
            delete_absent_records = request.POST['delete_absent_records'].split('_')
            for student_absent_record in student_absent_records:
                if (student_absent_record.absent_time+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") in delete_absent_records:
                    student_absent_record.delete()
            context['msg'] = '删除缺勤记录成功!'
        else:
            absent_date = request.POST['absent_date']
            absent_time = request.POST['absent_time']
            is_ask_for_leave = True if request.POST['is_ask_for_leave'] == 'true' else False
            create_student_absent_situation(student=student, course=course,
                                            absent_time=f"{absent_date} {absent_time}:00",
                                            absent_or_late=True, is_ask_for_leave=is_ask_for_leave)
            context['msg'] = '创建缺席记录成功!'
    student_absent_records = StudentAbsentSituation.objects.filter(student=student)
    context['student'] = student
    context['absent_records'] = student_absent_records
    return render(request, 'Absent_Record.html', context=context)


def page_not_found(request, exception: Exception=None):
    """404"""
    return render_to_response('404.html')
