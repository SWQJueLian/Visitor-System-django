import logging
import traceback
from dataclasses import asdict

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken

from common.exceptions.api_dataclass import Result
from common.exceptions.cust_exception import BaseAppException
from common.exceptions.statuscode import GlobalStatusCode

log = logging.getLogger("django")


def custom_exception_handler(exc, context):
    """
    context: 上下文
    自定义异常，需要在 settings.py 文件中进行全局配置
    1.在视图中的 APIView 中使用时,需要在验证数据的时候传入 raise_exception=True 抛出异常
    2.ModelViewSet 中非自定义 action 已经使用了 raise_exception=True,所以无需配置
    """

    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(as_serializer_error(exc))

    # 先让系统原来的处理一下
    response = exception_handler(exc, context)

    # drf默认的能处理的异常都会返回response（详见exception_handler里面的代码，其实只要是APIException的类，系统都能处理）
    # DRF不能处理的，都是非APIException
    if response is None:
        # 为none就是其他Exception错误， 只要捕获的异常非APIException和其子类，就会返回none
        # response.data = {'code': 40000, 'message': str(exc), 'data': None}
        request = context["request"]
        view = context["view"]

        req_data = request.query_params if request.method == "GET" else request.data

        log.error('[发生错误]-> 用户ip地址为：%s --> 访问URL：%s, 请求方法：%s, 请求数据: %s, 视图类:[%s] ' % (
            request.META.get('REMOTE_ADDR'), request.path, request.method, req_data, str(view))
                  )
        log.error(exc)

        # 不能处理的异常统一code为40000，http状态码为400（根据前端需求）
        if hasattr(exc, 'message'):
            message = exc.message
        else:
            message = GlobalStatusCode.BUSINESS_ERR.msg
        # 记录以下traceback，不然看个球球报错...
        log.error(traceback.format_exc())
        return Response(asdict(
            Result(
                GlobalStatusCode.BUSINESS_ERR.code,
                exc.message if hasattr(exc, 'message') else GlobalStatusCode.BUSINESS_ERR.msg + str(exc)
            )),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # exception=True
        )

    # 特殊关照一下simplejwt的异常
    if isinstance(exc, InvalidToken):
        response.data = asdict(
            Result(GlobalStatusCode.AUTH_ERR.code, message=GlobalStatusCode.AUTH_ERR.msg, extra=response.data)
        )
        return response

    # 如果是基于自己的异常类就读取里面的code
    if isinstance(exc, BaseAppException):
        response.data = asdict(Result(exc.code, message=exc.detail or response.data.get("detail")))
        return response

    if isinstance(exc.detail, (list, dict)):
        try:
            detail = dict(response.data)
        except:
            detail = exc.detail
        response.data = {
            "detail": detail
        }

    # 字段校验错误处理
    if isinstance(exc, ValidationError):
        # 是validationError，那么肯定是一个OrderDict（看源码就可以知道）
        # 序列化器校验失败返回的RetrunDict包含一个serializer，直接给dataclass的asdict会报错，因为Result没有这个serializer属性
        # if isinstance(response.data, ReturnDict):
        #     response.data = dict(response.data)

        response.data = asdict(
            Result(GlobalStatusCode.BUSINESS_ERR.code, message="验证错误",
                   extra={"fields": response.data.get("detail")})
        )
        # ValidationError默认是400的状态码，前端要200响应状态码
        response.status_code = status.HTTP_200_OK
        return response

    # # 如果是基于自己的异常类就读取里面的code
    # if isinstance(exc, BaseException):
    #     response.data = asdict(Result(exc.code, message=response.data.get("detail"), extra=None))
    #     return response

    # APIException其它类肯定是没有的，统一返回40000
    # 所以如果是detail就丢进去msg中
    if 'detail' in response.data:
        # response.data = {'code': 40000, 'message': response.data.get('detail'), 'data': None}
        response.data = asdict(
            Result(GlobalStatusCode.BUSINESS_ERR.code, message=response.data.get("detail"))
        )

    return response
