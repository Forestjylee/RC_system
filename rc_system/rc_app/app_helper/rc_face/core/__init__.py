# -*- coding: utf-8 -*-
"""
封装关于人脸图片读取，编码，保存，检测，比对的相关类和函数
@file: __init__.py.py
@time: 2019/3/28 15:07
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
from .face_comparison import compare_faces
from .face_image_handler import FaceImageHandler


__all__ = ['compare_faces', 'FaceImageHandler']
