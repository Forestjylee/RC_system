# -*- coding: utf-8 -*-
"""

@file: my_test.py
@time: 2019/5/19 17:01
Created by Junyi 
"""
from rc_system.rc_app.app_helper.io import compress_to_zip, decompress_zip


if __name__ == '__main__':
    print(compress_to_zip(directory_be_compressed="C:\\Users\\36515\\Desktop\\new",
                    target_directory='C:\\Users\\36515\\Desktop\\test_zip', zip_name="test_zip"))
