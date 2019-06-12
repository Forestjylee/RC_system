# -*- coding: utf-8 -*-
"""
定义读取不同格式数据的函数
@file: io.py
@time: 2019/5/19 16:40
Created by Junyi 
"""
import os
import shutil
import zipfile
from pandas import read_excel, DataFrame

from .decorators import deal_exceptions


@deal_exceptions(return_when_exceptions=None)
def read_excel_file(filepath: str) -> DataFrame:
    """
    读取Excel文件中的信息
    :param filepath: Excel文件路径
    :return: pandas.Dataframe | None
    """
    return read_excel(filepath)


@deal_exceptions(return_when_exceptions=None)
def compress_to_zip(directory_be_compressed: str, target_directory: str, zip_name: str) -> str:
    """
    将给定的文件夹压缩成zip格式
    :param directory_be_compressed: 需要被压缩的文件夹路径
    :param target_directory: 目标文件夹路径
    :param zip_name:  目标文件名
    :return: 压缩文件路径 | None
    """
    target_filepath = os.path.join(target_directory, zip_name+'.zip')
    os.makedirs(target_directory, exist_ok=True)
    z = zipfile.ZipFile(target_filepath, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(directory_be_compressed):
        fpath = dirpath.replace(directory_be_compressed, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath+filename)
    z.close()
    return target_filepath


@deal_exceptions(return_when_exceptions=False)
def decompress_zip(filepath: str, target_directory: str) -> bool:
    """
    解压指定路径的zip压缩包到指定文件夹
    1、递归删除目标文件夹中的所有文件
    2、创建目标文件夹
    3、解压
    :param filepath: zip压缩包所在路径
    :param target_directory: 目标文件夹
    :return: 是否解压成功
    """
    f = zipfile.ZipFile(filepath)
    shutil.rmtree(target_directory, ignore_errors=True)
    os.makedirs(target_directory, exist_ok=True)
    for name in f.namelist():
        if '__MACOSX' in name:
            continue
        f.extract(name, target_directory)
        old_path = os.path.join(target_directory, name)
        new_name = os.path.join(target_directory, name.encode('cp437').decode('utf8'))  # 解决中文乱码问题
        os.rename(old_path, new_name)
    return True
