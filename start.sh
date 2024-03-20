#!/bin/bash

# 项目名称
PROJECT_NAME="vistor"

# gunicorn监听的IP
LISTEN_IP="0.0.0.0"

# gunicorn监听的端口
LISTEN_PORT="7777"

# 进入项目目录
cd "/app"

# 生成静态文件
python3 manage.py collectstatic --noinput

gunicorn -D -b "unix:/tmp/gunicorn.sock" -w 10 "${PROJECT_NAME}.wsgi:application"
nginx -g "daemon off;"
