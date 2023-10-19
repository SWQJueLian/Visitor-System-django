from dataclasses import asdict

from rest_framework import serializers
from rest_framework.response import Response

from common.exceptions.api_dataclass import Result
from common.exceptions.statuscode import GlobalStatusCode


class ApiResponse(Response):
    def __init__(self, global_status: GlobalStatusCode = GlobalStatusCode.OK, data=None, *args, **kwargs):
        # serializer.data返回的时ReturnDict/ReturnList, asdict会报错，因为有一个serializer类属性。
        # if isinstance(data, ReturnDict):
        #     data = dict(data)
        #
        # if isinstance(data, ReturnList):
        #     data = list(data)
        ret_data = asdict(Result(
            code=global_status.code,
            message=global_status.msg,
            extra=kwargs.get('extra')
        ))
        ret_data['data'] = data
        super(ApiResponse, self).__init__(data=ret_data, *args, **kwargs)


def create_serializer_class(name, fields):
    """使用type利用元编程来创建序列化器类, 配合inline_serializer方法来使用, 当然你也可以不用"""
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    """
    使用示例：

    week = inline_serializer(many=True, fields={
        'id': serializers.IntegerField(),

        'number': serializers.IntegerField(),
    })

    :param fields: 序列化器字段。
    :param data: 序列化器的data参数，比如: UserSerializer(data=xxxx)。
    :param kwargs: 创建序列化器对象的额外参数，比如: UserSerializer(data=xxxx, many=True)。
    :return:
    """
    # Important note if you are using `drf-spectacular`
    # Please refer to the following issue:
    # https://github.com/HackSoftware/Django-Styleguide/issues/105#issuecomment-1669468898
    # Since you might need to use unique names (uuids) for each inline serializer
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
