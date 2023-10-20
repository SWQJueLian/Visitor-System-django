import uuid

from django.db import models
from native_shortuuid import NativeShortUUIDField

from common.models import BaseModel


# Create your models here.

# 员工表
class Employee(BaseModel):
    class Meta:
        db_table = 't_employee'
        verbose_name = '员工信息'
        verbose_name_plural = verbose_name

    employee_id = models.CharField(unique=True, max_length=100, db_index=True, blank=False, null=False,
                                   verbose_name="员工ID")
    employee_name = models.CharField(max_length=20, blank=False, null=False, verbose_name="员工姓名")
    employee_department = models.CharField(max_length=20, blank=False, null=False, verbose_name="所属部门")

    def __str__(self):
        return f"Employee({self.employee_name}, {self.employee_id})"

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


# 访客表
class Invite(BaseModel):
    class Meta:
        db_table = 't_invite'
        verbose_name = '访客信息'
        verbose_name_plural = verbose_name

    STATUS_CHOICE = [
        (0, '未到访'),
        (1, '已到访')
    ]

    id = NativeShortUUIDField(unique=True, default=uuid.uuid4, primary_key=True)

    # 员工关联关系
    employee = models.ForeignKey("Employee", related_name="invites", on_delete=models.RESTRICT, verbose_name='邀请人',
                                 to_field='employee_id')
    # 访客姓名
    visitor_name = models.CharField(max_length=20, verbose_name="访客姓名")
    # 访客手机号
    visitor_mobile = models.CharField(max_length=11, verbose_name="访客手机号")
    # 访客人数
    visitor_num = models.PositiveSmallIntegerField(verbose_name="访客人数")
    # 到访日期
    visit_date = models.DateTimeField(verbose_name="到访时间日期")
    # 车牌号
    visitor_car_number = models.CharField(max_length=10, verbose_name="车牌号码", null=True, blank=True)
    # 来访原因
    visitor_reason = models.CharField(max_length=50, verbose_name="来访原因")
    # 访客所在单位
    visitor_unit = models.CharField(max_length=20, verbose_name="所属单位", null=True, blank=True)
    # 当前状态, 0->未到访  1->已到访  2->未到访且已过期
    status = models.PositiveSmallIntegerField(default=0, verbose_name="当前状态", choices=STATUS_CHOICE)

    def __str__(self):
        return f"Invite-{self.id}, [{self.employee.employee_name}] 邀请 [{self.visitor_name}]"
