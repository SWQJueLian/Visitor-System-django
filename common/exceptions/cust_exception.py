from rest_framework import status
from rest_framework.exceptions import APIException

from common.exceptions.statuscode import GlobalStatusCode


#### 定义自己的业务异常 ###
# 可以在视图或者序列化器中抛出


class BaseAppException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, code_enum: GlobalStatusCode, detail=None, status_code=None):
        """
        初始化业务异常
        :param code_enum: 异常代码，请传递全局异常类。
        :param detail: 设置异常信息，不传则使用枚举类中的默认信息。
        :param status_code: 设置HTTP响应状态码，不传默认为400。
        """
        if not isinstance(code_enum, GlobalStatusCode):
            raise RuntimeError("必须传递全局异常枚举类")

        # 如果传递了detail则用detail，否则用状态枚举类中的默认信息,
        self.detail = detail or code_enum.msg
        self.code = code_enum.code

        # 有HTTP状态码就覆盖默认的400状态码
        if status_code:
            self.status_code = status_code

    def __str__(self):
        return str(self.detail)


class BusinessException(BaseAppException):
    def __init__(self, code_enum: GlobalStatusCode = GlobalStatusCode.BUSINESS_ERR, **kwarg):
        super().__init__(code_enum, **kwarg)
