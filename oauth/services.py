from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from common.exceptions.cust_exception import BusinessException
from common.exceptions.statuscode import GlobalStatusCode
from common.token_serializer import WxworkTokenObtainPairSerializer
from invite.models import Employee
from oauth.tools.wxwork_tools import WXWorkApi


def wxwork_get_userinfo(code: str):
    wxwork_api = WXWorkApi()

    # 1. 获取用户信息
    userid = wxwork_api.get_basic_userinfo(code).get('UserId')
    if userid is None:
        raise BusinessException(GlobalStatusCode.OAUTH_GET_USERINFO_ERR, detail='获取用户基本信息userid出错')

    # 拿到userid后就可以获取用户详情信息，
    # 1.1 获取用户的主部门id
    userinfo_detail_data = wxwork_api.get_detail_userinfo(userid)
    department_id = userinfo_detail_data.get('main_department')
    if department_id is None:
        raise BusinessException(GlobalStatusCode.OAUTH_GET_USERINFO_ERR, detail='获取用户基本信息department_id出错')
    # 1.2 获取用户姓名
    username = userinfo_detail_data.get('name')
    if department_id is None:
        raise BusinessException(GlobalStatusCode.OAUTH_GET_USERINFO_ERR, detail='获取用户基本信息username出错')
    # 2. 获取部门名称
    department_name = wxwork_api.get_detail_department(department_id).get('department').get('name')
    if department_name is None:
        raise BusinessException(detail='获取用户基本信息department_name出错')

    ret_data = {
        'userid': userid,
        'department_name': department_name,
        'username': username
    }

    return ret_data


def wxwork_generator_access_token(employee_data):
    # 创建绑定用户关系
    # 能获取到data就表示成功了，此时可以颁发一个token一同返回。
    # 前端后面都需要拿着token来发送请求，然后校验token，返回user对象。
    # token校验成功的user对象中取出userid,（只信任从token中取出的user_id）
    try:
        employee = Employee.objects.get(employee_id=employee_data['userid'])
    except Employee.DoesNotExist:
        employee = Employee.objects.create(employee_id=employee_data['userid'], employee_name=employee_data['username'],
                                           employee_department=employee_data['department_name'])

    # 生成token， payload中携带user_id
    serializer = WxworkTokenObtainPairSerializer(data={"employee_id": employee.employee_id})
    try:
        serializer.is_valid(raise_exception=True)
    except TokenError as e:
        raise InvalidToken(e.args[0])
    else:
        return serializer.validated_data['access_token']
