#!/usr/bin/env python
# coding: utf-8
# cc@2020/11/12


from fastapi import APIRouter, Depends

from utils import response_code, depends
from utils.database import db

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
    a_list = []
    data = db.article.find().sort([('created_at', DESCENDING)])
    data = json.loads(json_util.dumps(data))
    ctx = {'articles': data}
    return response_code.resp_200(ctx)


@router.delete('/article/del/{id}/')
def article_del(id, user: dict = Depends(depends.token_is_true)):
    res = db.article.delete_one({'_id': ObjectId(id)})
    ctx = {'ok': True}
    return response_code.resp_200(ctx)


@router.get('/article/detail/{id}/')
def article_new(id, user: dict = Depends(depends.token_is_true)):
    a_list = []
    data = db.article.find_one({'_id': ObjectId(id)})
    data = json.loads(json_util.dumps(data))
    ctx = {'article': data}
    return response_code.resp_200(ctx)
