# -*- coding: utf-8 -*-
"""
post图片至接口的测试样例
@file: post_img.py
@time: 2019/4/25 22:43
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
import requests


if __name__ == '__main__':
    f = open('C:\\Users\\36515\\Desktop\\timg.jpg', 'rb')
    files = {
        'image': f
    }
    res = requests.post('http://127.0.0.1:8000/face_detect/', files=files)
    f.close()
    print(res.text)
