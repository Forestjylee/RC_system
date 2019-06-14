# -*- coding: utf-8 -*-
"""
views的辅助函数
@file: views_helper.py
@time: 2019/5/19 11:20
Created by Junyi 
"""
import os
import pickle
import shutil
from datetime import datetime
from django.conf import settings
from django.utils import timezone
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


def get_compare_faces_result(username: str, pickle_filepath: str) -> list:
    """
    从序列化的文件中将点名的详细信息读取出来
    :param username: 用户名
    :param pickle_filepath: 保存点名详细信息的序列化文件
    :return: 点名详细信息
    """
    file_directory = os.path.join(_get_user_upload_file_directory(username), 'specific_infos')
    filepath = os.path.join(file_directory, pickle_filepath)
    with open(filepath, 'rb') as f:
        result = pickle.load(f)
    return result


# @deal_exceptions(return_when_exceptions=False)
def update_compare_faces_result(username: str, pickle_filepath: str, new_result: list) -> bool:
    """"""
    file_directory = os.path.join(_get_user_upload_file_directory(username), 'specific_infos')
    filepath = os.path.join(file_directory, pickle_filepath)
    with open(filepath, 'wb') as f:
        pickle.dump(new_result, f)
    return True


# @deal_exceptions(return_when_exceptions=False)
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
def create_course(course_name: str, teacher: User, course_time: str) -> bool:
    """
    创建课程
    :param course_name: 课程名称
    :param teacher: 老师
    :param course_time: 上课时间
    :return: 是否创建成功
    """
    course = get_object_or_none(Course, name=course_name, teacher=teacher)
    if not course:
        course = Course()
        course.teacher = teacher
    course.name = course_name
    course.course_time = course_time
    update_course(course)
    course.save()
    return True


def create_student_absent_situation(student: Student, course: Course, absent_time: str, absent_or_late: bool, is_ask_for_leave: bool) -> None:
    """
    创建学生缺席情况记录
    :param student: 学生
    :param course: 课程
    :param absent_time: 缺勤时间
    :param absent_or_late: 缺席或迟到
    :param is_ask_for_leave: 是否已请假
    :return: None
    """
    sas = get_object_or_none(StudentAbsentSituation, student=student, course=course, absent_time=absent_time)
    if not sas:
        sas = StudentAbsentSituation()
        sas.student = student
        sas.course = course
    sas.absent_time = absent_time
    sas.absent_or_late = absent_or_late
    sas.is_ask_for_leave = is_ask_for_leave
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


def update_course(course: Course) -> Course:
    """
    遍历StudentCourse表，得出当前Course的总人数
    :param course: 课程对象
    :return: 更新后的Course对象
    """
    course.student_amount = len(StudentCourse.objects.filter(course=course))
    course.save()
    return course


def delete_students(student_ids: list, course: Course) -> list:
    """
    在数据库中删除学生的基本信息、缺勤情况、照片信息、学生课程对应关系
    (Student, StudentAbsentSituation, StudentPicture, StudentCourse)
    :param student_ids: 学生id
    :param course: 课程
    :return: 未成功删除的学生列表
    """
    fail_list = []
    for student_id in student_ids:
        student = get_object_or_none(Student, student_id=student_id)
        if student:
            StudentCourse.objects.filter(student=student, course=course).delete()
            StudentAbsentSituation.objects.filter(student=student, course=course).delete()
        else:
            fail_list.append(student_id)
    return fail_list


def save_student_face_photos(source_directory: str, course: Course) -> str:
    """
    检查是否有Excel文件在压缩包中，有则用来创建学生
    学生的相片存放在media/student_face_pictures,以学号_姓名.png命名
    将临时存放学生相片的文件夹中的图片保存到数据库中
    :param source_directory: 存放解压后信息的文件夹名称
    :param course: 课程对象
    :return:
    """
    file_directory = _get_student_picture_directory()
    for file_path in os.listdir(source_directory):     # 遍历找到Excel文件进行创建学生
        fn, ft = os.path.splitext(file_path)
        if ft in ['.xlsx', '.xls']:
            temp_file_path = os.path.join(source_directory, file_path)
            result = create_students(filepath=temp_file_path, course=course)
            if not result:
                return '创建学生失败，请检查您的Excel表格是否符合格式！'
            os.remove(temp_file_path)
            break
    for file_path in os.listdir(source_directory):
        fn, ft = os.path.splitext(file_path)
        temp_file_path = os.path.join(source_directory, file_path)
        student_id, student_name = fn.split('_')
        encoding_face = FaceImageHandler.encoding_face(image_path=temp_file_path)
        if encoding_face is not None:
            file_path = os.path.join(file_directory, file_path)
            shutil.copy(temp_file_path, file_path)
            FaceImageHandler.convert_to_png(image_path=file_path)
            os.remove(file_path)
            student = get_object_or_none(Student, student_id=student_id, name=student_name)
            if student:
                sp = get_object_or_none(StudentPicture, student=student)
                if not sp:
                    sp = StudentPicture()
                    sp.student = student
                sp.face_picture_path = file_path
                sp.encoding_face = pickle.dumps(encoding_face)
                sp.save()
    return '创建学生成功!'


# @deal_exceptions(return_when_exceptions=(None, None, None))
def detect_and_compare_faces(username: str, filepath: str, course: Course) -> tuple:
    """
    人脸检测和比对
    :param username: 用户名
    :param filepath: 需要检测图片的绝对路径
    :param course: 课程对象
    :return: 检测结果和对比结果
    """
    sps = []
    face_handler = FaceImageHandler(image_path=filepath)
    face_amount = face_handler.get_face_amount()
    file_type = face_handler._image_save_type
    face_handler.save_marked_image(
            filepath=_get_marked_photo_filepath(username, file_type=file_type)
    )
    unknown_encoding_faces = face_handler.encoding_faces()
    scs = StudentCourse.objects.filter(course=course)
    for sc in scs:
        sp = get_object_or_none(StudentPicture, student=sc.student)
        if sp:
            sps.append(sp)
    if sps:
        temp_record_index = []
        attendance_infos = []
        known_encoding_faces = []
        for sp in sps:
            known_encoding_faces.append(pickle.loads(sp.encoding_face))
        for face in unknown_encoding_faces:
            if len(temp_record_index) < len(known_encoding_faces):
                compare_results = compare_faces(known_encoding_faces, unknown_encoding_face=face)
                for compare_result in compare_results:     # 相似度尽量高(相似度下限为50，低于50则不加入出席列表)，与之前识别出的结果不重复
                    if compare_result['known_face_index'] not in temp_record_index and compare_result['similarity'] > 50:
                        attendance_infos.append(compare_result)
                        temp_record_index.append(compare_result['known_face_index'])
                        break
            else:
                break
        pickle_filepath = _save_as_pickle(username, sps, attendance_infos, course)
    else:
        pickle_filepath = None
    return file_type, face_amount, pickle_filepath


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
    return filepath, _save_upload_file(file_obj, filepath)


def save_compressed_student_infos(file_obj, username: str) -> tuple:
    """
    1、将上传的包含多个学生照片的压缩包保存到upload/username/目录下
    2、解压到upload/username/temp_student_photos/目录下
    :param file_obj: 文件对象
    :param username: 老师用户名
    :return: 解压到的文件夹路径, 是否解压成功
    """
    now_datetime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    target_directory = os.path.join(os.path.join(_get_user_upload_file_directory(username), 'student_infos'), now_datetime)
    file_directory = _get_user_upload_file_directory(username)
    filename = f"{now_datetime}.zip"
    filepath = os.path.join(file_directory, filename)
    _save_upload_file(file_obj, filepath)
    if decompress_zip(filepath, target_directory=target_directory):
        return target_directory, True
    else:
        return target_directory, False


def save_student_face_photo(file_obj, student_id: str, student_name: str) -> dict:
    """
    1、保存上传的单张学生人脸图片
    2、将图片序列化后保存到数据库中
    3、将学生的相片存放在media/student_face_pictures,以学号_姓名.png命名
    :param file_obj: 文件对象
    :param student_id: 学生的学号
    :param student_name: 学生的姓名
    :return: {
        'status': 是否成功,
        'msg': 描述信息
    }
    """
    file_directory = _get_student_picture_directory()
    file_type = os.path.splitext(file_obj.name)[-1]
    filename = f"{student_id}_{student_name}{file_type}"
    filepath = os.path.join(file_directory, filename)
    result = _save_upload_file(file_obj, filepath)
    result = FaceImageHandler.convert_to_png(image_path=filepath) if result else False
    if result:
        os.remove(filepath)
        filepath = os.path.join(file_directory, f"{student_id}_{student_name}.png")
        encoding_face = FaceImageHandler.encoding_face(image_path=filepath)
        if encoding_face is not None:
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
                            'msg': '创建学生成功！'
                }
        return {
            'status': False,
            'msg': '上传的学生图片中没有人脸，请重新上传！'
        }
    return {
        'status': False,
        'msg': '图片传输出错，请重新上传文件！'
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


def _get_student_picture_directory() -> str:
    """
    获取存储学生上传照片的文件夹路径
    :return: 文件夹路径
    """
    file_directory = os.path.join(os.path.join(settings.BASE_DIR, 'media'), 'student_face_pictures')
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


def _save_as_pickle(username: str, sps: list, attendance_infos: list, course: Course) -> str:
    """
    detect_and_compare_faces的辅助函数
    目的在于将人脸比对后的结果序列化存储到本地的文件中一边详情页面读取并将结果记录到数据库中
    :param sps: 学生照片信息列表
    :param attendance_infos: 人脸比对的结果，格式为:
    {'known_face_index': int, 'similarity': float}
    :param course: 课程名称
    :return: 保存的文件名
    """
    result = []
    attendance_students = []
    scs = list(StudentCourse.objects.filter(course=course))
    file_directory = os.path.join(_get_user_upload_file_directory(username), 'specific_infos')
    os.makedirs(file_directory, exist_ok=True)
    file_path = os.path.join(file_directory, f"{str(datetime.now().strftime('%Y%m%d%H%M%S'))}.pkl")
    for attendance_info in attendance_infos:
        sp = sps[attendance_info['known_face_index']]
        student = sp.student
        temp = {
            'similarity': attendance_info['similarity'],
            'student': student,
            'attendance_times': get_object_or_none(StudentCourse, student=student, course=course).attendance_times + 1,
            'absent_situation': '到场'
        }
        attendance_students.append(student)
        result.append(temp)
    for sc in scs:
        if sc.student in attendance_students:     # 出勤
            sc.attendance_times += 1
            sc.save()
        else:     # 缺勤
            sas = StudentAbsentSituation()
            sas.student = sc.student
            sas.course = course
            sas.save()
            sum_times = sc.attendance_times + sc.absent_times
            temp = {
                'student': sc.student,
                'attendance_times': sc.attendance_times,
                'similarity': round(1 - sc.attendance_times / sum_times, 4) * 100 if sum_times else 50.00,
                'absent_situation': '未到场',
                'sas': sas
            }
            sc.absent_times += 1
            sc.save()
            result.append(temp)
    with open(file_path, 'wb') as f:
        pickle.dump(result, f)
    return file_path.split('/')[-1]
