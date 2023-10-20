# 业务逻辑
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from invite.models import Employee, Invite


def invite_get_by_id(invite_id):
    return get_object_or_404(Invite, pk=invite_id)


def invite_get_all(filter_data):
    filter_kw = [
        Q(employee__employee_id=filter_data['employee_id']),
    ]
    # 如果有时间日期过滤就加上。
    # 这里要用来做下拉刷新和上拉瀑布流加载
    if filter_data.get('datetime'):
        filter_kw.append(Q(created_at__lt=filter_data.get('datetime')))
    # 如果有关键词过滤就加上。
    if filter_data.get('keyword'):
        filter_kw.append(Q(visitor_name__icontains=filter_data.get('keyword')) |
                         Q(visitor_mobile__contains=filter_data.get('keyword')))
    # 为了前端体验瀑布流，暂时写死返回5条。
    return Invite.objects.filter(*filter_kw) \
               .order_by("-created_at") \
               .only("id", "visitor_name", "visitor_mobile", "visit_date", "created_at", "status") \
               .all()[:filter_data.get('limit', 20)]


def invite_save(employee: Employee, validated_data: dict):
    # employee, is_create = Employee.objects.get_or_create(employee_id=validated_data.pop("employee_id"),
    #                                                      employee_department=validated_data.pop('employee_department'),
    #                                                      employee_name=validated_data.pop('employee_name'))

    invite = Invite(**validated_data,
                    employee=employee)
    invite.save()

    return invite


def invite_update_by_employee(employee_id, invite_id, validated_data: dict):
    return Invite.objects.filter(id=invite_id, employee_id=employee_id).update(**validated_data)


def invite_visitor_arrive(invite_id, status):
    from django.utils.timezone import now
    from common.exceptions.cust_exception import BusinessException
    try:
        invite = Invite.objects.get(pk=invite_id).only('status', 'visit_date')
    except Invite.DoesNotExist:
        raise BusinessException()

    if invite.visit_date.date() != now().date():
        raise BusinessException(detail='来访日期与当前日期不相等')
    invite.status = status
    invite.save()
    return invite
