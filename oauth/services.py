from common.exceptions.cust_exception import BusinessException
from common.exceptions.statuscode import GlobalStatusCode
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
