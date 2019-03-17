# -*- coding: utf-8 -*-
"""
使用本地的人脸检测库进行人脸检测
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
import os
import cv2
import face_recognition


class LocalFaceDetector(object):
    """人脸检测类"""
    def __init__(self, image_path):
        """
        :param image_path: 照片文件路径
        """
        self.image_path = image_path
        self.image_type = self.get_image_type()
        self.original_image = self.read_image()
        self.face_locations = self._detect_faces()

    def read_image(self):
        """
        读取图片并作相应异常处理
        :return: 读取成功的图片
        """
        try:
            return cv2.imread(self.image_path)
        except TypeError:
            raise TypeError("非法图片格式")

    def show_original_image(self) -> None:
        """
        弹出窗口展示原始照片
        :return: None
        """
        self._show_image(image=self.original_image, image_name="Original Photo")

    def mark_faces(self) -> None:
        """
        弹出窗口展示人脸检测后照片
        :return: None
        """
        new_img = self.original_image.copy()
        for face_location in self.face_locations:
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

    def save_faces(self, directory: str) -> bool:
        """
        先确保文件夹已经存在
        将图片中的人脸图片保存到指定路径
        :param directory: 文件夹名称
        :return: 是否保存成功
        """
        try:
            os.makedirs(directory, exist_ok=True)
            for index, face_location in enumerate(self.face_locations):
                top = face_location[0]
                right = face_location[1]
                bottom = face_location[2]
                left = face_location[3]
                face_img = self.original_image[top:bottom, left:right]
                cv2.imwrite(os.path.join(directory, f"{index}.{self.image_type}"), face_img)
            return True
        except Exception as e:
            return False

    def get_image_type(self) -> str:
        """
        获取图片的类型(后缀)
        :return: 图片的类型(后缀)
        """
        if not os.path.exists(self.image_path):
            raise TypeError("文件不存在")
        image_type = self.image_path.split('.')[-1]
        if image_type not in ['png', 'jpg', 'jpeg', 'bmp']:
            raise TypeError(f"不支持{image_type}类型图片")
        return image_type

    def _detect_faces(self) -> list:
        """
        传入照片的文件路径
        定位照片中人脸的位置
        输出人脸位置的坐标列表
        :return: 人脸位置坐标列表
        """
        face_locations = face_recognition.face_locations(self.original_image)
        return face_locations

    @staticmethod
    def _show_image(image, image_name: str="Photo") -> None:
        """
        弹窗展示图片
        :param image: 图片对象
        :param image_name: 窗口标题
        :return: None
        """
        cv2.startWindowThread()
        # cv2.namedWindow(image_name, cv2.WINDOW_NORMAL)     # 窗口缩放功能
        cv2.imshow(image_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
