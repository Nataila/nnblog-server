#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 17:44
"""

路由汇总

"""

from fastapi import APIRouter
from api.v1.user import user
from api.v1.article import article

api_v1 = APIRouter()

api_v1.include_router(user.router, tags=["用户管理"])
api_v1.include_router(article.router, tags=["博文管理"])
