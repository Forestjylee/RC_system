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
import pickle
from prettytable import PrettyTable
from rc_system.rc_app.app_helper.rc_face import FaceImageHandler, LocalFaceComparer

if __name__ == '__main__':
    path = "C:\\Users\\36515\\Desktop\\timg.jpg"
    new_dir = "C:\\Users\\36515\\Desktop\\new"
    f = FaceImageHandler(image_path=path)
    # f.save_faces(directory=new_dir)
    # f.mark_faces()
    # en_fs = f.encoding_faces()
    # c = LocalFaceComparer(
    #     index=0,
    #     unknown_encoding_face=en_fs[0],
    #     known_encoding_faces=en_fs
    # ).compare()
    # pt = PrettyTable(['需要比对的人脸序号', '已知的人脸序号', '相似度'])
    # for i in c:
    #     pt.add_row([i['unknown_face_index'], i['known_face_index'], i['similarity']])
    print(pickle.dumps(f.encoding_faces()[0]))
