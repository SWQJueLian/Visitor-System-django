# Api入口
import re

from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import DateTimeField
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from common.exceptions.cust_exception import BusinessException
from common.exceptions.statuscode import GlobalStatusCode
from common.utils import ApiResponse
from invite.models import Employee, Invite
from invite.services import (
    invite_get_all,
    invite_get_by_id,
    invite_save,
    invite_update,
    invite_visitor_arrive
)
from invite.tasks import send_sms_to_vistor, notify_employee


class InviteDetailApi(APIView):

    class OutputModelSerializer(serializers.ModelSerializer):
        class EmployeeOutputModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = Employee
                fields = ('employee_name', 'employee_department')

        employee = EmployeeOutputModelSerializer()

        class Meta:
            # 指定日期时间的输出格式
            datatime_fmt = '%Y-%m-%d %H:%M:%S'

            model = Invite
            fields = "__all__"

            extra_kwargs = {
                "created_at": {
                    "format": datatime_fmt
                },
                "updated_at": {
                    "format": datatime_fmt
                },
                "visit_date": {
                    "format": datatime_fmt
                }
            }

    def get(self, request: Request, invite_id):
        if invite_id is None:
            raise BusinessException(GlobalStatusCode.PARAM_ERR)

        invite = invite_get_by_id(invite_id)
        serializer = self.OutputModelSerializer(instance=invite)
        return ApiResponse(data=serializer.data)


class InviteListApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class InputSerializer(serializers.Serializer):
        # 不用传了，因为token认证后拿到request.user实际上是Employee，然后直接在这里拿
        # employee_id = serializers.CharField(required=True)
        keyword = serializers.CharField(required=False)
        datetime = serializers.DateTimeField(required=False)
        limit = serializers.IntegerField(required=False, default=20, max_value=50)  # 限制最大值50条数据

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        visitor_name = serializers.CharField()
        visitor_mobile = serializers.CharField()
        visit_date = DateTimeField(format='%Y-%m-%d %H:%M:%S')
        created_at = DateTimeField(format='%Y-%m-%d %H:%M:%S')
        status = serializers.IntegerField()

    def get(self, request: Request):
        input_serializer = self.InputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        invite_list = invite_get_all({
            "employee_id": request.user.employee_id,
            **input_serializer.validated_data,
        })

        serializer = self.OutputSerializer(instance=invite_list, many=True)
        data = {'results': serializer.data}
        if len(invite_list) > 0:
            data.setdefault('pre_datetime', serializer.data[-1]['created_at'])
        return ApiResponse(data=data)


class InviteCreateApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class InputSerializer(serializers.Serializer):
        # employee_id = serializers.CharField(required=False, default='SongWeiQuan')
        # employee_name = serializers.CharField(required=True)
        # employee_department = serializers.CharField(required=True)
        visitor_name = serializers.CharField(required=True, min_length=2, max_length=20)
        visitor_mobile = serializers.CharField(required=True, min_length=11, max_length=11)
        visitor_num = serializers.IntegerField(required=False, default=1)
        visit_date = serializers.DateTimeField(required=True)
        visitor_car_number = serializers.CharField(required=False, min_length=7, max_length=8, allow_blank=True,
                                                   allow_null=True)
        visitor_reason = serializers.CharField(required=True, max_length=50)
        visitor_unit = serializers.CharField(required=False, max_length=20, allow_null=True, allow_blank=True)

        def validate_mobile(self, val):
            if re.match(r'^1[3-9]\d{9}$', val) is None:
                raise serializers.ValidationError('手机号格式不正确')
            return val

    @transaction.atomic
    def post(self, request: Request):
        employee: Employee = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # data = {
        #     "employee_id": employee.employee_id,
        #     "employee_name": employee.employee_name,
        #     "employee_department": employee.employee_department,
        #     **serializer.validated_data
        # }
        print('111', serializer.validated_data)
        invite = invite_save(employee, serializer.validated_data)
        # 拿到访客手机号，异步发送短信给访客。
        # 这里要等提交完成后才能开始任务，不然可能会出现数据还没创建完，任务就开始了
        transaction.on_commit(lambda: send_sms_to_vistor.delay(invite.visitor_mobile))
        return ApiResponse()


class InviteUpdateApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class InputSerializer(serializers.Serializer):
        visitor_name = serializers.CharField(required=True, min_length=2, max_length=20)
        visitor_mobile = serializers.CharField(required=True, min_length=11, max_length=11)
        visitor_num = serializers.IntegerField(required=False, default=1)
        visit_date = serializers.DateTimeField(required=True)
        visitor_car_number = serializers.CharField(required=False, min_length=7, max_length=8, allow_blank=True,
                                                   allow_null=True)
        visitor_reason = serializers.CharField(required=True, max_length=50)
        visitor_unit = serializers.CharField(required=False, max_length=20, allow_null=True, allow_blank=True)

    def put(self, request: Request, invite_id):
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        invite_update(invite_id, serializer.validated_data)
        return ApiResponse()


class InviteStatusUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        password = serializers.CharField(required=True, min_length=4, max_length=6)
        status = serializers.IntegerField(required=True)

        def validate_password(self, val):
            # 暂时写死了....理论上可以开多一个模型类然后允许再后台里面随时修改密码
            if val != '666666':
                raise BusinessException(GlobalStatusCode.PWD_ERR)
            return val

    @transaction.atomic
    def put(self, request: Request, invite_id):
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('password')
        invite_visitor_arrive(invite_id, serializer.validated_data['status'])
        # 这里一般放apischeduler中、celery异步去执行
        # 懒得搞了。也很简单...
        # api = WXWorkApi()
        # api.send_arrive_markdown_msg(settings.WXWORK_APP_AGENT_ID, invite_get_by_id(invite_id))
        # 丢，搞一下吧。权当复习...
        transaction.on_commit(lambda: notify_employee.delay(invite_id))
        return ApiResponse()
