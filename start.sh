#!/bin/bash
# cc @ 2020-11-16 12:14:51

pip install -r requirements.txt -i https://pypi.douban.com/simple
gunicorn -k uvicorn.workers.UvicornWorker -c /gunicorn_conf.py main:app
