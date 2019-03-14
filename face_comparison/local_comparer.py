# -*- coding: utf-8 -*-
"""
人脸对比类的实现
实现思路：
1、需要比对的图片集存储在一个文件夹中
2、遍历整个文件夹得出某张人脸与其他所有人脸的相似度
3、按照相似度从高到低排序
可优化之处（可选）：
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
import os
import face_recognition
from collections import deque


class LocalFaceComparer(object):
    """人脸比对类"""
    def __init__(self, directory):
        """
        :param directory: 存放图片集的文件夹路径
        """
        self.directory = directory
        self.face_paths = self.get_face_paths()
        self.encoding_faces = [self._encode_face(face_path) for face_path in self.face_paths]

    def get_face_paths(self) -> list:
        """
        检查文件夹是否存在
        遍历图片文件夹，得到所有图片路径组成的列表
        :return: 图片路径列表
        """
        if not os.path.exists(self.directory):
            raise FileNotFoundError("文件夹不存在")
        return [os.path.join(self.directory, path) for path in os.listdir(self.directory)]

    def compare(self, face_to_compare: str) -> list:
        """
        将一张人脸图片与本地人脸仓库中的人脸对比
        :param face_to_compare: 需要进行相似度比对的图片路径
        :return: 相似度从高到低排序的结果列表
        """
        if not os.path.exists(face_to_compare):
            raise FileExistsError("人脸图片文件不存在")
        result = deque()
        face_to_compare = self._encode_face(face_to_compare)
        face_distances = face_recognition.face_distance(self.encoding_faces, face_to_compare)
        for index, face_distance in enumerate(face_distances):
            result.append({
                'face': self.face_paths[index].split('\\')[-1],
                'similarity': round(100*(1-face_distance), 4),
            })
        return sorted(result, key=lambda x: x['similarity'], reverse=True)

    @staticmethod
    def _encode_face(face_path: str) -> list:
        """
        将人脸图片编码
        :param face_path: 人脸图片文件路径
        :return: 编码后的人脸图片列表
        """
        img = face_recognition.load_image_file(face_path)
        return face_recognition.face_encodings(img)[0]
