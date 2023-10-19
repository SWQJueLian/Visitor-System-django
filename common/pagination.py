from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination

from common.utils import ApiResponse


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    """
    适用于APIView, 根据给定分页器类返回分页响应.

    Args:
        pagination_class: 分页器类，比如DRF的LimitOffsetPagination、PageNumberPagination
        serializer_class: 结果集中输出的序列化器类
        queryset: 结果集
        request: 请求
        view: 视图

    Returns:

    """
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return ApiResponse(data=serializer.data)


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_data(self, data):
        return OrderedDict(
            [
                ("limit", self.limit),
                ("offset", self.offset),
                ("count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )

    def get_paginated_response(self, data):
        """
        我们重新定义这个方法以返回“limit”和“offset”， 前端使用它来构建分页本身。
        Args:
            data:
        Returns:
            基于ApiResponse类的json格式。
        """
        return ApiResponse(
            data=OrderedDict(
                [
                    ("limit", self.limit),
                    ("offset", self.offset),
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
