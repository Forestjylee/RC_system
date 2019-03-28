# -*- coding: utf-8 -*-
"""
使用本地的人脸检测库进行人脸检测
(基于默认HOG模型进行查找，还可以使用CNN模型进行查找。
按照官方文档的说法，CNN模型效果要优于默认的HOG模型，
但是实际测试的几张图片均是HOG模型效果更好。
官方文档对API的注释：
https://github.com/ageitgey/face_recognition/blob/master/examples/find_faces_in_picture.py)
需要确保照片的清晰度，否则检测的准确率会一定程度下降
@file: local_detector.py
@time: 2019/3/13 12:16
Created by 
   ___                       _ 
  |_  |                     (_)
    | | _   _  _ __   _   _  _ 
    | || | | || '_ \ | | | || |
/\__/ /| |_| || | | || |_| || |
\____/  \__,_||_| |_| \__, ||_|
                       __/ |   
                      |___/    
"""
from numpy import ndarray
from face_recognition import face_locations


def detect_faces(image: ndarray) -> list:
    """
    传入照片
    定位照片中人脸的位置
    输出人脸位置的坐标列表
    :param image:
    :return: 人脸位置坐标列表
    """
    faces = face_locations(image)
    return faces
