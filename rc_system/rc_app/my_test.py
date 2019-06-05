# -*- coding: utf-8 -*-
"""

@file: my_test.py
@time: 2019/5/19 17:01
Created by Junyi 
"""
from rc_system.rc_app.app_helper.rc_face import FaceImageHandler, compare_faces
from rc_system.rc_app.app_helper.io import compress_to_zip, decompress_zip


if __name__ == '__main__':
    from pprint import pprint
    fih = FaceImageHandler(
        image_path='C:\\Users\\36515\\Desktop\\2.jpg'
    )
    fih.save_faces(directory='C:\\Users\\36515\\Desktop\\wanggong')
    pprint(compare_faces(fih.encoding_faces(), unknown_encoding_face=FaceImageHandler.encoding_face(image_path='C:\\Users\\36515\\Desktop\\Relax\\123.png')))
