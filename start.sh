#!/bin/bash

# 项目名称
PROJECT_NAME="vistor"

# 由于直接用sock了，这样速度更快，所以这个就保留吧，实际上gunicorn可以多个-b选项，有时候方便调试可以加多一个基于http的绑定
# gunicorn监听的IP
#LISTEN_IP="0.0.0.0"

# gunicorn监听的端口
#LISTEN_PORT="7777"

# 进入项目目录
cd "/app"

# 生成静态文件
python3 manage.py collectstatic --noinput

gunicorn -D -b "unix:/tmp/gunicorn.sock" -w 10 "${PROJECT_NAME}.wsgi:application"
nginx -g "daemon off;"
