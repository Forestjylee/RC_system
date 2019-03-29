# -*- coding: utf-8 -*-
"""
定义与MongoDB数据交互的函数
@file: mongo_pipe.py
@time: 2019/3/29 10:58
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
from bson.binary import Binary
from pymongo import MongoClient


class MongoPipe(object):
    """
    与MongoDB交互类
    增删查改操作简单事例如下：
    1、增
    pipe.insert({
        'id': 1,(primary key)
        'name': Jack,
        'age': 20,
    })
    2、删
    pipe.delete_one({
        'id': 1,
        'name': Jack,
    })
    3、查
    pipe.find({
        'id': 1,
    })
    4、改
    pipe.update({
        'id': 1,
    },{
        '$set': {
            'name': Tom,
        }
    })
    """
    def __init__(self, ip: str, port: int,):
        self._ip = ip
        self._port = port
        self._client = self.connect()

    def connect(self) -> MongoClient:
        """
        连接MongeDB数据库
        :return: MongoClient
        """
        return MongoClient(self._ip, self._port)

    def build_pipe(self, db: str, collection: str):
        """
        建立与MongoDB数据库的某张数据表之间的管道连接
        增删查改(insert、delete、find、update)操作使用Pymongo的API
        已经足够简洁，无须二次封装
        :param db: 数据库名称
        :param collection: 集合(数据表)名称
        :return: 数据表操作对象
        """
        return self._client[db][collection]

    @staticmethod
    def transfer_ndarray_to_binary(ndarray) -> Binary:
        """
        将numpy数组转换成二进制形式
        [protocol=-1是使用pickle.dumps的最新协议来dump数据，而subtype=128表示Binary的用户自定义二进制格式]
        :param ndarray: numpy数组(项目中用于存储图片)
        :return: 转化后的二进制流
        """
        return Binary(pickle.dumps(ndarray, protocol=-1), subtype=128)
