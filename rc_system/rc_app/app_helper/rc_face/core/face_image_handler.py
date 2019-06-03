# -*- coding: utf-8 -*-
"""
本文件定义各种关于图片读取，显示等的操作
实现底层算法(人脸检测、人脸比对)与实际业务逻辑的交互
图片的保存格式默认为.png[png是无损压缩格式但是内存占用大，jpg是有损但是内存占用小]
@file: face_image_handler.py
@time: 2019/3/28 15:08
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
import cv2
from numpy import ndarray
from face_recognition import face_encodings
from .face_detection import detect_faces


class FaceImageHandler(object):
    """人脸图片操作类"""
    __slots__ = ('_image_path', '_image_save_type', '_original_image', '_face_locations')

    def __init__(
            self,
            image_path: str,
            image_save_type: str='png',
    ):
        """
        :param image_path: 图片文件路径
        :param image_save_type: 图片以什么格式保存
        """
        self._image_path = image_path
        self._image_save_type = image_save_type
        self._original_image = self.read_image()
        self._face_locations = detect_faces(self._original_image)

    def get_face_amount(self) -> int:
        """
        获取当前图片中人脸的数量
        :return: 人脸的数量
        """
        return len(self._face_locations)

    def encoding_faces(self) -> list:
        """
        已知图片中有多张人脸的情况下使用
        encoding那些人脸
        :return: 编码后的人脸(numpy数组)组成的列表
        """
        return face_encodings(
            face_image=self._original_image,
            known_face_locations=self._face_locations
        )

    def mark_faces(self) -> None:
        """
        弹出窗口展示人脸检测后照片(黄色框标出人脸位置)
        :return: None
        """
        new_img = self._original_image.copy()
        for face_location in self._face_locations:
            top = face_location[0]
            right = face_location[1]
            bottom = face_location[2]
            left = face_location[3]
            cv2.rectangle(
                new_img,
                (left, top),
                (right, bottom),
                color=(0, 255, 255),
                thickness=2,
            )
        self._show_image(image=new_img, image_name="Recognized Photo")

    def save_marked_image(self, filepath: str) -> bool:
        """
        将黄色框标注出来的人脸图片保存到指定路径
        :param filepath: 保存的路径
        :return: 是否保存成功
        """
        try:
            new_img = self._original_image.copy()
            for face_location in self._face_locations:
                top = face_location[0]
                right = face_location[1]
                bottom = face_location[2]
                left = face_location[3]
                cv2.rectangle(
                    new_img,
                    (left, top),
                    (right, bottom),
                    color=(0, 255, 255),
                    thickness=2,
                )
            cv2.imwrite(filepath, new_img)
            return True
        except Exception:
            return False

    def save_faces(self, directory: str) -> bool:
        """
        先确保文件夹已经存在
        将图片中的人脸图片保存到指定路径
        :param directory: 文件夹名称
        :return: 是否保存成功
        """
        try:
            os.makedirs(directory, exist_ok=True)
            for index, face_location in enumerate(self._face_locations):
                top = face_location[0]
                right = face_location[1]
                bottom = face_location[2]
                left = face_location[3]
                face_img = self._original_image[top:bottom, left:right]
                cv2.imwrite(os.path.join(directory, f"{index}.{self._image_save_type}"), face_img)
            return True
        except Exception as e:
            return False

    def read_image(self):
        """
        读取图片并作相应异常处理
        :return: 读取成功的图片(numpy数组)
        """
        try:
            return cv2.imread(self._image_path)
        except TypeError:
            raise TypeError("非法图片格式")

    @staticmethod
    def _show_image(image, image_name: str="Photo") -> None:

        """
        弹窗展示图片
        :param image: 图片对象
        :param image_name: 窗口标题
        :return: None
        """
        cv2.startWindowThread()
        cv2.namedWindow(image_name, cv2.WINDOW_NORMAL)     # 窗口缩放功能
        cv2.imshow(image_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @classmethod
    def encoding_face(cls, image_path: str) -> ndarray:
        """
        已知图片中只有一张人脸的情况下使用
        encoding那张人脸
        若人脸数量大于1则抛出ValueError异常
        :return: 编码后的人脸
        """
        try:
            image = cv2.imread(image_path)
        except TypeError:
            raise TypeError("非法图片格式")
        face_locations = detect_faces(image)
        return face_encodings(
            face_image=image,
            known_face_locations=face_locations
        )[0]