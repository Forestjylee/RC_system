# -*- coding: utf-8 -*-
"""
人脸对比类的实现
实现思路：
1、传入一个encoding的未知的(需要比对的)人脸
2、传入一个已知的encoding的人脸(人脸仓库，如全班同学的人脸)组成的列表
3、计算两两人脸之间的face_distance，得出对比结果
可优化之处：
在收集人脸图片集时计算出人脸的face_encoding，然后将其存储到数据库中
对比时直接从数据库中取出进行对比
经过初步测试10张图片的encode耗时大概为0.41s，对于整体的影响不大
@file: local_comparer.py
@time: 2019/3/14 14:26
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
import face_recognition
from numpy import ndarray
from collections import deque


def compare_faces(known_encoding_faces: list, unknown_encoding_face: ndarray) -> list:
    """
    将一张未知的人脸图片与人脸仓库中的人脸(self._known_encoding_faces)对比
    :param known_encoding_faces: 已知的人脸列表
    :param unknown_encoding_face: 未知的(需要比对的)人脸
    :return: 相似度从高到低排序的结果列表
    """
    result = deque()
    face_distances = face_recognition.face_distance(
        known_encoding_faces,
        unknown_encoding_face
    )
    for index, face_distance in enumerate(face_distances):
        result.append({
            'known_face_index': index,
            'similarity': round(100*(1-face_distance), 4),
        })
    return sorted(result, key=lambda x: x['similarity'], reverse=True)
