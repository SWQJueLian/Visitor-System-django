from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vistor.settings")

app = Celery("vistor")

# - namespace='CELERY' 指定namespace，
# 如果给定了，表示celery相关配置属性格式变成：namespance_celery属性（必须全部大写），比如：原来叫broker_url，变成CELERY_BROKER_URL
# 使用ns可以避免与django中的其他配置选项名冲突的问题。
# 另外：
# celery的配置可以直接写在django的settings.py中，也可以自己去指定配置文件，如下面：
# 从django settings中读取：
# app.config_from_object("django.conf:settings", namespace="CELERY")
app.config_from_object("tasks.celery_config")

# Load task modules from all registered Django app configs.
# 默认celery会自动去子应用下找tasks.py并加载定义的任务，你也可以自己手动传递告诉它去哪里找tasks.py
app.autodiscover_tasks()

# celery.exe -A tasks.celery worker -l INFO -P eventlet -c 10
