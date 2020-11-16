#Docker file

FROM python:3.6

LABEL maintainer="CC <nataila.cc.814@gmail.com>"

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py
COPY . /app

WORKDIR /app

EXPOSE 80

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

CMD ["/start.sh"]
