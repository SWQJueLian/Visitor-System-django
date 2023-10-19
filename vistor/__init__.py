import pymysql
from tasks.celery import app as celery_app
# After this function is called,
# any application that imports MySQLdb or _mysql will unwittingly actually use pymysql.
pymysql.install_as_MySQLdb()


# from celery_tasks.main import app as celery_app
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
#
__all__ = ('celery_app',)
