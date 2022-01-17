#!/usr/bin/env python
# coding: utf-8
# cc@2020/11/12

import json
import os
import time
import datetime

from fastapi import APIRouter, Depends, File, UploadFile
from pymongo import DESCENDING
from bson import json_util, ObjectId

from PIL import Image

from utils import response_code, depends
from utils.database import db
from core.config import settings

from schemas import article

router = APIRouter()


@router.post('/article/new/')
def article_new(
    article: article.AddArticle, user: dict = Depends(depends.token_is_true)
):
    res = db.article.insert_one(article.dict())
    ctx = {'ok': True, 'id': str(res.inserted_id)}
    return response_code.resp_200(ctx)


@router.get('/article/list/')
def article_list():
    data = db.article.find().sort([('created_at', DESCENDING)])
    data = json.loads(json_util.dumps(data))
    ctx = {'articles': data}
    return response_code.resp_200(ctx)


@router.delete('/article/del/{id}/')
def article_del(id, user: dict = Depends(depends.token_is_true)):
    db.article.delete_one({'_id': ObjectId(id)})
    ctx = {'ok': True}
    return response_code.resp_200(ctx)


@router.get('/article/detail/{id}/')
def article_detail(id):
    data = db.article.find_one({'_id': ObjectId(id)})
    data = json.loads(json_util.dumps(data))
    ctx = {'article': data}
    return response_code.resp_200(ctx)


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024


def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}.c{}'.format(dir, suffix)
    return outfile


def compress_image(infile, outfile='', mb=10, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)


@router.post("/article/upload/")
async def file_upload(
    file: UploadFile = File(...), user: dict = Depends(depends.token_is_true)
):
    uid = user['_id']
    f = await file.read()
    ext = os.path.splitext(file.filename)[-1]
    user_dir = f'{settings.UPLOAD_DIR}/{str(uid)}'
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    new_file_name = "%d%s" % (int(time.time() * 1000), ext)
    os_path = os.path.join(user_dir, new_file_name)

    with open(os_path, "wb") as n:
        n.write(f)
    compress_name, size = compress_image(os_path)
    _id = db.files.insert(
        {
            'uid': uid,
            'filename': new_file_name,
            'old_name': file.filename,
            'created_time': datetime.now(),
        }
    )
    return response_code.resp_200(
        {'filename': file.filename, 'id': str(_id), 'path': f"{uid}/{new_file_name}"}
    )
