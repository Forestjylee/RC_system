# -*- coding: utf-8 -*-
"""

@file: api.py
@time: 2019/4/25 22:16
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
from core import FaceImageHandler
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False     # 解决中文显示问题


@app.route('/')
def api_root():
    return "Welcome to use RC_system web api!"


@app.route('/face_detect/', methods=['POST'])
def api_face_detect():
    """
    人脸检测API接口
    只接收post请求上传的图片
    :return: 人脸检测的结果#TODO 具体待商议
    """
    face_img = request.files['image']
    face_img.save('upload_img/temp_face.jpg')
    fi = FaceImageHandler(image_path='upload_img/temp_face.jpg')
    ret = {
        'status_code': 200,
        'message': f"图片中所含人脸数量为: {fi.get_face_amount()}"
    }
    return jsonify(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
