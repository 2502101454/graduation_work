# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from business.employee import Employee
from business.common import Common
from business.util import DeanUtil
from business.holiday_task import HolidayTask
from business.overtime_task import OvertimeTask
from business.cost_task import CostTask
from business.dean_annotation import *
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from models import HolidayTask as model_HolidayTask, OvertimeTask as model_OvertimeTask, CostTask as model_CostTask

employee = Employee()
common = Common()
holiday_task = HolidayTask()
overtime_task = OvertimeTask()
cost_task = CostTask()
util = DeanUtil


def em_register(request):
    global employee
    return employee.em_register(request)


def register_success(request):
    global common
    return common.register_success(request)


def login(request):
    global common
    return common.user_login(request)


@require_GET
def index(request):
    global common
    return common.go_index(request)


@has_login
@require_GET
def logout(request):
    global common
    return common.logout(request)


@has_login
@require_GET
def user_center(request):
    global common
    user = request.session.get('user')
    return common.user_center(request, user)


@has_login
def user_info_update(request):
    global common
    return common.user_info_update(request)


@has_login
def user_detail(request, user_id):
    global common
    return common.user_detail(request, user_id)


@has_login
def user_password_update(request):
    global common
    return common.user_password_update(request)


@has_login
@require_GET
def all_employees(request):
    global common
    return common.all_employees(request)


@has_login
@require_GET
def all_managers(request):
    global common
    return common.all_managers(request)


@has_login
@require_GET
def all_ceo(request):
    global common
    return common.all_ceo(request)


@has_login
@require_GET
def company_news(request):
    global common
    return common.company_news(request)


@has_login
@require_GET
def show_news(request, news_id):
    global common
    return common.show_news(request, news_id)


@has_login
@require_GET
def my_holiday_tasks(request):
    global holiday_task
    return holiday_task.my_holiday_tasks(request)


@has_login
def add_holiday_task(request):
    global holiday_task
    return holiday_task.add_holiday_task(request)


@has_login
@require_GET
def holiday_task_detail(request, ht_id):
    global holiday_task
    return holiday_task.holiday_task_detail(request, ht_id=ht_id)


@has_login
@can_update(id_name='ht_id', model_class=model_HolidayTask)
def update_holiday_task(request, ht_id=None):
    global holiday_task
    return holiday_task.update_holiday_task(request, ht_id=ht_id)

@has_login
@can_do(cur_status=0, id_name='ht_id', model_class=model_HolidayTask)
def holiday_task_delete(request, ht_id):
    global holiday_task
    return holiday_task.holiday_task_delete(request, ht_id)

@has_login
@can_do(cur_status=0, id_name='ht_id', model_class=model_HolidayTask)
def holiday_task_submit(request, ht_id):
    global holiday_task
    return holiday_task.holiday_task_submit(request, ht_id)

@has_login
@can_do(cur_status=1, id_name='ht_id', model_class=model_HolidayTask)
def holiday_task_withdraw(request, ht_id):
    global holiday_task
    return holiday_task.holiday_task_withdraw(request, ht_id)


@has_login
@require_GET
def subordinate_holiday_tasks(request):
    global holiday_task
    return holiday_task.subordinate_holiday_tasks(request)


@has_login
@can_do(cur_status=1, id_name='ht_id', model_class=model_HolidayTask)
def holiday_task_approve(request, ht_id):
    global holiday_task
    return holiday_task.holiday_task_approve(request, ht_id)


@has_login
@can_do(cur_status=1, id_name='ht_id', model_class=model_HolidayTask)
def holiday_task_negative(request, ht_id):
    global holiday_task
    return holiday_task.holiday_task_negative(request, ht_id)



@has_login
@require_GET
def my_overtime_tasks(request):
    global overtime_task
    return overtime_task.my_overtime_tasks(request)


@has_login
def add_overtime_task(request):
    global overtime_task
    return overtime_task.add_overtime_task(request)


@has_login
@require_GET
def overtime_task_detail(request, ot_id):
    global overtime_task
    return overtime_task.overtime_task_detail(request, ot_id=ot_id)


@has_login
@can_update(id_name='ot_id', model_class=model_OvertimeTask)
def update_overtime_task(request, ot_id=None):
    global overtime_task
    return overtime_task.update_overtime_task(request, ot_id=ot_id)


@has_login
@can_do(cur_status=0, id_name='ot_id', model_class=model_OvertimeTask)
def overtime_task_delete(request, ot_id):
    global overtime_task
    return overtime_task.overtime_task_delete(request, ot_id)


@has_login
@can_do(cur_status=0, id_name='ot_id', model_class=model_OvertimeTask)
def overtime_task_submit(request, ot_id):
    global overtime_task
    return overtime_task.overtime_task_submit(request, ot_id)


@has_login
@can_do(cur_status=1, id_name='ot_id', model_class=model_OvertimeTask)
def overtime_task_withdraw(request, ot_id):
    global overtime_task
    return overtime_task.overtime_task_withdraw(request, ot_id)


@has_login
@require_GET
def subordinate_overtime_tasks(request):
    global overtime_task
    return overtime_task.subordinate_overtime_tasks(request)


@has_login
@can_do(cur_status=1, id_name='ot_id', model_class=model_OvertimeTask)
def overtime_task_approve(request, ot_id):
    global overtime_task
    return overtime_task.overtime_task_approve(request, ot_id)


@has_login
@can_do(cur_status=1, id_name='ot_id', model_class=model_OvertimeTask)
def overtime_task_negative(request, ot_id):
    global overtime_task
    return overtime_task.overtime_task_negative(request, ot_id)


@has_login
@require_GET
def my_cost_tasks(request):
    global cost_task
    return cost_task.my_cost_tasks(request)


@has_login
def add_cost_task(request):
    # pass
    global cost_task
    return cost_task.add_cost_task(request)


@has_login
@require_GET
def cost_task_detail(request, ct_id):
    # pass
    global cost_task
    return cost_task.cost_task_detail(request, ct_id=ct_id)


@has_login
@can_update(id_name='ct_id', model_class=model_CostTask)
def update_cost_task(request, ct_id=None):
    # pass
    global cost_task
    return cost_task.update_cost_task(request, ct_id=ct_id)


@has_login
@can_do(cur_status=0, id_name='ct_id', model_class=model_CostTask)
def cost_task_delete(request, ct_id):
    global cost_task
    return cost_task.cost_task_delete(request, ct_id)


@has_login
@can_do(cur_status=0, id_name='ct_id', model_class=model_CostTask)
def cost_task_submit(request, ct_id):
    global cost_task
    return cost_task.cost_task_submit(request, ct_id)


@has_login
@can_do(cur_status=1, id_name='ct_id', model_class=model_CostTask)
def cost_task_withdraw(request, ct_id):
    global cost_task
    return cost_task.cost_task_withdraw(request, ct_id)



@has_login
@require_GET
def subordinate_cost_tasks(request):
    global cost_task
    return cost_task.subordinate_cost_tasks(request)


@has_login
@can_do(cur_status=1, id_name='ct_id', model_class=model_CostTask)
def cost_task_approve(request, ct_id):
    global cost_task
    return cost_task.cost_task_approve(request, ct_id)


@has_login
@can_do(cur_status=1, id_name='ct_id', model_class=model_CostTask)
def cost_task_negative(request, ct_id):
    global cost_task
    return cost_task.cost_task_negative(request, ct_id)


