#!/usr/bin/env python
# coding: utf-8
# cc@2020/11/12

import datetime

from pydantic import BaseModel
from typing import List, Union


class AddArticle(BaseModel):
    title: str
    content: str
    tags: List[Union[str, int]] = []
    created_at: datetime.datetime = datetime.datetime.now()
