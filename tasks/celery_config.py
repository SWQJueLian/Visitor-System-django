# 配置信息 key=value
# 我们指定 redis为我们的broker
broker_url = "redis://127.0.0.1:6379/14"
# celery执行任务结果存放
result_backend = "redis://127.0.0.1:6379/13"
timezone = 'Asia/Shanghai'
enable_utc = False

# CELERY调用delay给定的参数如果时对象的话，需要将使用pickle
# https://www.cnblogs.com/hszstudypy/p/12153416.html
# https://blog.csdn.net/lvluobo/article/details/127283015
# https://blog.csdn.net/anwuxiao2732/article/details/101707384

# 默认的序列化程序是JSON，但是您可以使用task_serializer设置来更改它，或者为每个单独的任务甚至每个消息更改它。
# JSON的主要缺点是它将您限制在以下数据类型:strings、Unicode、floats、boolean、字典和列表。decimal和date日期
# 有关序列化器的选择和pickle的安全问题，请看官方：
# https://docs.celeryq.dev/en/stable/userguide/calling.html#serializers
# task_serializer = 'pickle'
#
# result_serializer = 'pickle'
#
# accept_content = ['pickle', 'json']

# CELERY_TASK_SERIALIZER = 'pickle'
#
# CELERY_RESULT_SERIALIZER = 'pickle'
#
# CELERY_ACCEPT_CONTENT = ['pickle', 'json']

# django-celery-beat集成
# beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

## Flower监控使用
# 发送与任务相关的事件，以便可以使用flower之类的工具来监控任务
# 或者在启动worker服务时，使用-E参数。
worker_send_task_events = True
# 如果启用，将为每个任务发送一个 task-sent 事件，以便可以在任务被工作人员使用之前对其进行跟踪。
task_send_sent_event = True

# 允许将扩展任务结果属性（名称、参数、kwargs、worker、重试、队列、delivery_info）写入后端。
result_extended = True
# 如果启用，后端将尝试在发生可恢复异常时重试，而不是传播异常。它将在两次重试之间使用指数退避睡眠时间。
result_backend_always_retry = True
# 可恢复异常情况下的最大重试次数。
result_backend_max_retries = 10


# https://docs.celeryq.dev/en/stable/userguide/workers.html#time-limits
# TODO: 设置为适合你自己情况的任何值
# worker处理任务硬时间限制，当超过这个值时，处理该任务的worker将被杀死并被一个新的worker取代（单位：秒, 默认：无限制）
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# 这个是全局设置，通过给task传递参数来指定某个task的超时时间，如：@app.task(soft_time_limit=5)
task_time_limit = 3600

# TODO: 设置为适合你自己情况的任何值
# worker处理任务软时间限制, 当超过这个值时, 会抛出SoftTimeLimitExceeded异常, 可以在硬限制到来之前捕获该异常并进行如清理等操作, （单位：秒, 默认“无限制）
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
task_soft_time_limit = 1800

# 定义任务路由
# task_routes = {
#     # 将add任务放到add_queue队列中执行
#     # key是任务函数的完整路径， 然后指定queue
#     # key也可以是通配形式，比如app.users.*
#     "apps.users.celery_test.tasks.add": {"queue": "add_queue"}
#
#     # 其他的任务默认会丢给名为celery队列的worker进程处理。并不需要定义。
#
#     # 如果要覆盖默认的路由队列，可以在调用delay() 或者 apply_async()是传递queue参数指定调度到哪个队列中
#     # generic_detail.delay(queue="add_queue")
# }

