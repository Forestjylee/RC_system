# -*- coding: utf-8 -*-
"""
测试效果
@file: testa.py
@time: 2019/3/13 16:55
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
from pprint import pprint
from core import FaceImageHandler
from core import LocalFaceComparer

if __name__ == '__main__':
    path = "C:\\Users\\36515\\Desktop\\123123.png"
    f = FaceImageHandler(image_path=path)
    f.mark_faces()
    en_fs = f.encoding_faces()
    c = LocalFaceComparer(
        index=0,
        unknown_encoding_face=en_fs[1],
        known_encoding_faces=en_fs
    ).compare()
    pprint(c)
