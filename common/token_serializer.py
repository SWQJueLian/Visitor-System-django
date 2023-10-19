from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from invite.models import Employee

class WxworkTokenObtainPairSerializer(TokenObtainPairSerializer):
    # token_class =
    employee_id = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 搞掉自带的
        del self.fields[self.username_field]
        del self.fields["password"]

    def authenticate_employee(self, employee_id):
        try:
            return Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return None

    def validate(self, attrs):
        self.user = self.authenticate_employee(attrs['employee_id'])

        if self.user is None:
            from common.exceptions.cust_exception import BusinessException
            from common.exceptions.statuscode import GlobalStatusCode
            raise BusinessException(GlobalStatusCode.AUTH_ERR)

        data = {}

        refresh = self.get_token(self.user)

        # 锤子refresh，谁会停留2个小时不动，没啥必要
        # data["refresh"] = str(refresh)
        data["access_token"] = str(refresh.access_token)

        # if api_settings.UPDATE_LAST_LOGIN:
        #     update_last_login(None, self.user)

        return data
