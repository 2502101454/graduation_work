# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from business.employee import Employee
from business.common import Common
from business.util import DeanUtil

employee = Employee()
common = Common()
util = DeanUtil

def em_register(request):
    global employee
    return employee.em_register(request)

def login(request):
    global common
    return common.user_login(request)

def index(request):
    global common
    return common.go_index(request)
