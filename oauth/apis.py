import logging

from django.conf import settings
from rest_framework.request import Request
from rest_framework.views import APIView

from common.exceptions.cust_exception import BusinessException
from common.exceptions.statuscode import GlobalStatusCode
from common.utils import ApiResponse
from invite.models import Employee
from oauth.services import wxwork_get_userinfo, wxwork_generator_access_token

log = logging.getLogger('django')


class WxWorkOauthURLGenerateApi(APIView):
    """生成企业微信oauth的链接"""
    WXWORK_STATE = ''  # 不校验state阶段了，给个空就行

    def get(self, request: Request):
        oauth_url = f"https://open.weixin.qq.com/connect/oauth2/authorize?" \
                    f"appid={settings.WXWORK_COPRID}&redirect_uri={settings.WXWORK_REDIRECT_URI}&response_type=code" \
                    f"&scope=snsapi_base&state={self.WXWORK_STATE}&agentid={settings.WXWORK_APP_AGENT_ID}#wechat_redirect"

        return ApiResponse(data={
            "oauth_url": oauth_url
        })


class WxWorkUserInfo(APIView):
    """获取企业微信用户信息"""

    def get(self, request: Request):
        code = request.query_params.get('code')
        if not code:
            raise BusinessException(GlobalStatusCode.NECESSARY_PARAM_ERR)
        data = wxwork_get_userinfo(code)
        data['access_token'] = wxwork_generator_access_token(data)
        return ApiResponse(data=data)
