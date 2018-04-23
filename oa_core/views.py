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
from business.dean_annotation import has_login
from django.views.decorators.http import require_http_methods, require_GET, require_POST

employee = Employee()
common = Common()
holiday_task = HolidayTask()
overtime_task = OvertimeTask()
util = DeanUtil


def em_register(request):
    global employee
    return employee.em_register(request)


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
@require_POST
def update_holiday_task(request):
    global holiday_task
    return holiday_task.update_holiday_task(request)


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
@require_POST
def update_overtime_task(request):
    global overtime_task
    return overtime_task.update_overtime_task(request)