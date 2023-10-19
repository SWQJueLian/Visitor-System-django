from celery import shared_task

from oauth.tools.wxwork_tools import WXWorkApi
from vistor import settings


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_sms_to_vistor(self, mobile):  # 修改默认的重试前等待为1分钟（默认3min）
    send_result = -1
    # 调用SDK发送短信
    try:
        pass
        send_result = 1
        print('发送短信给访客', mobile)
    except Exception as exc:
        raise self.retry(exc=exc)
    finally:
        if send_result == -1:
            raise self.retry(exc=Exception('短信发送失败！'))


@shared_task(bind=True, max_retries=3, autoretry_for=(Exception,))  # 这里就自动重试所有错误吧。。
def notify_employee(self, invite_id):
    """通知邀请人，访客已经到达"""
    print('通知邀请人，访客已到达')
    from invite.services import invite_get_by_id
    api = WXWorkApi()
    api.send_arrive_markdown_msg(settings.WXWORK_APP_AGENT_ID, invite_get_by_id(invite_id))
