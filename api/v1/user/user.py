#!/usr/bin/env python
# coding: utf-8
# cc@2020/08/28


from fastapi import APIRouter

from utils import response_code, tools
from utils.database import db, redis

from schemas import user

router = APIRouter()


@router.post("/account/login/", name='登录')
def login(user: user.UserSignin):
    try:
        username = user.username
        db_user = db.user.find_one({'username': username})
        token = tools.new_token(20)
        uid = str(db_user['_id'])
        redis.set(token, uid)
        ctx = {'ok': True, 'data': {'token': token, 'username': username, 'id': uid}}
        return response_code.resp_200(ctx)
    except Exception as e:
        print(e)
        return {'ok': False, 'msg': '用户名或密码错误!'}
