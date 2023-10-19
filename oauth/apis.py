import logging

from django.conf import settings
from rest_framework.request import Request
from rest_framework.views import APIView

from common.exceptions.cust_exception import BusinessException
from common.exceptions.statuscode import GlobalStatusCode
from common.utils import ApiResponse
from invite.models import Employee
from oauth.services import wxwork_get_userinfo

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
        print("尼玛的...", data)
        # 创建绑定用户关系
        # 能获取到data就表示成功了，此时可以颁发一个token一同返回。
        # 前端后面都需要拿着token来发送请求，然后校验token，返回user对象。
        # token校验成功的user对象中取出userid,（只信任从token中取出的user_id）
        try:
            employee = Employee.objects.get(employee_id=data['userid'])
        except Employee.DoesNotExist:
            print("用户不存在，创建用户....")
            employee = Employee.objects.create(employee_id=data['userid'], employee_name=data['username'],
                                               employee_department=data['department_name'])

        from common.token_serializer import WxworkTokenObtainPairSerializer
        from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

        # 生成token， payload中携带user_id
        serializer = WxworkTokenObtainPairSerializer(data={"employee_id": employee.employee_id})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        else:
            data['access_token'] = serializer.validated_data['access_token']
        return ApiResponse(data=data)
