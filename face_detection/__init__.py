# -*- coding: utf-8 -*-
"""
实现人脸探测功能的工具包
两个实现方案：
1、调用各个AI平台提供的API进行探测
2、使用OpenCV和dlib中的人脸探测函数进行探测
@file: __init__.py.py
@time: 2019/3/13 11:00
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
from .local_detector import LocalFaceDetector
