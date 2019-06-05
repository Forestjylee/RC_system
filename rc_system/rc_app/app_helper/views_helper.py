# -*- coding: utf-8 -*-
"""
views的辅助函数
@file: views_helper.py
@time: 2019/5/19 11:20
Created by Junyi 
"""
import os
import pickle
from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from ..models import User, Student, Course, StudentCourse, StudentPicture, StudentAbsentSituation
from .io import read_excel_file, decompress_zip
from .decorators import deal_exceptions
from .rc_face import FaceImageHandler, compare_faces


def get_object_or_none(model, *args, **kwargs):
    """
    重新封装Django的get方法
    返回一个查询到的对象或None
    :param model: 需要查询对象的模型对象
    :param args: 传入的查询参数
    :param kwargs: 传入的查询参数
    :return: 查询到的对象或None
    """
    result = model.objects.filter(*args, **kwargs)
    if result:
        return result[0]
    else:
        return None


@deal_exceptions(return_when_exceptions=None)
def get_user_or_none(request):
    """
    验证用户是否存在
    存在：返回user对象
    不存在：返回None
    :param request:
    :return: user | None
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    return user


def get_courses_or_none(teacher: User) -> list:
    """
    根据老师对象查询老师管理的课程
    :param teacher: 老师对象
    :return: 所有老师管理的课程
    """
    courses = Course.objects.filter(teacher=teacher)
    for index, course in enumerate(courses):
        course.index = index
    return courses if courses else []


def get_students_or_none(course_id: int) -> list:
    """
    根据课程id获取选择了这门课程的学生
    :param course_id: 课程id
    :return: 选择了这门课程的学生的列表
    """
    students = []
    course = get_object_or_404(Course, course_id=course_id)
    student_courses = StudentCourse.objects.filter(course=course)
    if student_courses:
        for sc in student_courses:
            students.append(sc.student)
    return students


def create_students(filepath: str, course: Course) -> bool:
    """
    从Excel表中读取并创建多个学生
    Excel表中必须包含的属性名称(学号，姓名，班级)
    :param filepath: Excel文件路径
    :param course: 课程
    :return: 是否创建成功
    """
    df = read_excel_file(filepath)
    for student_id, student_name, class_name in zip(
        list(df["学号"]),
        list(df["姓名"]),
        list(df["班级"]),
    ):
        result = create_student(student_id, student_name, class_name, course)
        if not result:
            return False
    return True


# @deal_exceptions(return_when_exceptions=False)
def create_student(student_id: str, student_name: str, class_name: str, course: Course) -> bool:
    """
    在数据库Student表中创建一个新的学生
    若学号对应的学生已存在，则更新姓名和班级信息
    并将学生关联到对应的课程中
    :param student_id: 学生的学号
    :param student_name: 学生的姓名
    :param class_name: 班级名称
    :param course: 课程
    :return: 是否创建成功
    """
    student = get_object_or_none(Student, student_id=student_id)
    if not student:
        student = Student()
        student.student_id = student_id
    student.name = student_name
    student.class_name = class_name
    student.save()
    sc = get_object_or_none(StudentCourse, student=student, course=course)
    if not sc:
        sc = StudentCourse()
        sc.course = course
        sc.student = student
        sc.save()
    return True


# @deal_exceptions(return_when_exceptions=False)
def create_course(course_name: str, teacher: User, student_amount: int) -> bool:
    """
    创建课程
    :param course_name: 课程名称
    :param teacher: 老师
    :param student_amount: 学生总人数
    :return: 是否创建成功
    """
    course = get_object_or_none(Course, course_name=course_name, teacher=teacher)
    if not course:
        course = Course()
        course.name = course_name
        course.teacher = teacher
    course.student_amount = student_amount
    course.save()
    return True


def create_student_absent_situation(student: Student, course: Course, absent_or_late: bool) -> None:
    """
    创建学生缺席情况记录
    :param student: 学生
    :param course: 课程
    :param absent_or_late: 缺席或迟到
    :return: None
    """
    sas = StudentAbsentSituation()
    sas.student = student
    sas.course = course
    sas.absent_or_late = absent_or_late
    sas.save()


# @deal_exceptions(return_when_exceptions=False)
def update_student_course(student: Student, course: Course, is_absent: bool) -> bool:
    """
    更新学生的出勤、缺勤次数信息
    :param student: 学生对象
    :param course: 课程对象
    :param is_absent: 是否缺席
    :return: 是否更新成功
    """
    sc = get_object_or_404(StudentCourse, student=student, course=course)
    if is_absent:
        sc.absent_times += 1
    else:
        sc.attendance_times += 1
    sc.save()
    return True


@deal_exceptions(return_when_exceptions=(None, None))
def detect_and_compare_faces(username: str, filepath: str) -> bool:
    """
    人脸检测和比对
    :param username: 用户名
    :param filepath: 需要检测图片的绝对路径
    :return: 检测结果和对比结果
    """
    face_handler = FaceImageHandler(image_path=filepath)
    face_amount = face_handler.get_face_amount()
    file_type = face_handler._image_save_type
    face_handler.save_marked_image(
            filepath=_get_marked_photo_filepath(username, file_type=file_type)
    )
    unknwon_encoding_faces = face_handler.encoding_faces()
    return file_type, face_amount
    #TODO 人脸比对


def save_student_infos(file_obj, username: str) -> tuple:
    """
    保存包含学生信息的Excel文件
    :param file_obj: 文件对象
    :param username: 用户名
    :return: 文件保存路径，是否上传成功
    """
    file_directory = _get_user_upload_file_directory(username)
    file_type = os.path.splitext(file_obj.name)[-1]
    filename = f"{str(datetime.now())}{file_type}"
    filepath = os.path.join(file_directory, filename)
    if file_type not in ['.xlsx', 'xls']:
        return filepath, False
    return filepath, _save_upload_file(file_obj, filepath)


def save_compressed_upload_student_face_photos(file_obj, username: str) -> bool:
    """
    1、将上传的包含多个学生照片的压缩包保存到upload/username/目录下
    2、解压到upload/username/temp_student_photos/目录下
    :param file_obj: 文件对象
    :param username: 老师用户名
    :return: 是否保存成功
    """
    target_directory = os.path.join(_get_user_upload_file_directory(username), 'temp_student_photos')
    file_directory = _get_user_upload_file_directory(username)
    file_type = os.path.splitext(file_obj.name)[-1]
    if file_type != '.zip':
        return False
    filename = f"{str(datetime.now())}{file_type}"
    filepath = os.path.join(file_directory, filename)
    _save_upload_file(file_obj, filepath)
    if decompress_zip(filepath, target_directory=target_directory):
        pass
    return True


def save_student_face_photos(username: str):
    """

    :param username:
    :return:
    """
    pass


def save_student_face_photo(file_obj, student_id: str, student_name: str) -> dict:
    """
    1、保存上传的单张学生人脸图片
    2、将图片序列化后保存到数据库中
    :param file_obj: 文件对象
    :param student_id: 学生的学号
    :param student_name: 学生的姓名
    :return: {
        'status': 是否成功,
        'msg': 描述信息
    }
    """
    file_directory = os.path.join(os.path.join(settings.BASE_DIR, 'media'), 'student_face_pictures')
    file_type = os.path.splitext(file_obj.name)[-1]
    filename = f"{student_id}_{student_name}{file_type}"
    filepath = os.path.join(file_directory, filename)
    result = _save_upload_file(file_obj, filepath)
    if result:
        encoding_face = FaceImageHandler.encoding_face(image_path=filepath)
        if encoding_face:
            student = get_object_or_none(Student, student_id=student_id, name=student_name)
            if student:
                sp = get_object_or_none(StudentPicture, student=student)
                if not sp:
                    sp = StudentPicture()
                    sp.student = student
                sp.face_picture_path = filepath
                sp.encoding_face = pickle.dumps(encoding_face)
                sp.save()
                return {
                            'status': True,
                            'msg': '图片上传成功'
                }
        return {
            'status': False,
            'msg': '上传的图片中没有人脸，请重新上传'
        }
    return {
        'status': False,
        'msg': '图片传输出错，请重新上传文件'
    }


def save_upload_face_photo(file_obj, username: str) -> tuple:
    """
    保存用户上传的用于点名的人脸照片
    :param file_obj: 文件对象
    :param username: 用户名
    :return: 文件保存路径, 是否上传成功
    """
    file_directory = _get_user_upload_file_directory(username)
    file_type = os.path.splitext(file_obj.name)[-1]
    filename = f"{str(datetime.now().strftime('%Y%m%d%H%M%S'))}{file_type}"
    filepath = os.path.join(file_directory, filename)
    return filepath, _save_upload_file(file_obj, filepath)


@deal_exceptions(return_when_exceptions=False)
def _save_upload_file(file_obj, filepath: str) -> bool:
    """
    保存上传的文件到指定路径
    :param file_obj: 文件对象
    :param filepath: 文件的保存路径
    :return: 是否保存成功
    """
    with open(filepath, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return True


def _get_user_upload_file_directory(username: str) -> str:
    """
    获取存储用户上传文件的文件夹路径
    :param username: 用户名
    :return: 文件夹路径
    """
    file_directory = os.path.join(os.path.join(settings.BASE_DIR, 'upload'), username)
    os.makedirs(file_directory, exist_ok=True)
    return file_directory


def _get_marked_photo_filepath(username: str, file_type) -> str:
    """
    获取保存已标记人脸的图片的保存路径
    :param username: 用户名
    :param file_type: 文件类型
    :return: 保存已标记人脸的图片的保存路径
    """
    file_directory = os.path.join(os.path.join(settings.BASE_DIR, 'media'), username)
    os.makedirs(file_directory, exist_ok=True)
    return os.path.join(file_directory, f"marked_face.{file_type}")
