# -*- coding: utf-8 -*-
#员工业务类
##########
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from ..forms import EmRegisterForm
from util import DeanUtil
from ..models import Employee as model_Employee
from ..models import Department
from datetime import datetime
from ..forms import LoginForm
import json
util = DeanUtil()

class Employee(object):

    def __int__(self):
        pass

    def em_register(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            result = {'status': False, 'message': None}
            form = EmRegisterForm(request.POST)
            #The form's data will be validated the first time either you call is_valid() or access errors.
            errors = form.errors
            # 所以说哎，is_valid肯定是在没有一个错误的情况下，才会返回true。你要是在之前add_error了，那肯定就是false
            if form.is_valid():
                # process the data in form.cleaned_data as required
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                password_agin = form.cleaned_data['password_again']
                dept_id = form.cleaned_data['dept']
                print 'email,', email
                print 'password,', password
                print 'password_agin,', password_agin
                print 'dept_id,', dept_id
                e_id = util.next_user_id(prefix='e', digital_bit=5)
                print 'id,', e_id
                dept = None
                try:
                    dept = Department.objects.get(pk=dept_id)
                except Exception as e:
                    print e

                employee = model_Employee(id=e_id, name='wz'+e_id, email=email,
                                          password=password, register_time=datetime.now(), dept=dept)
                employee.save()
                request.session['register_user_code'] = e_id
                result['status'] = True
                return HttpResponse(json.dumps(result))
            else:
                errors_str = errors.as_json()
                print 'valid error:', errors, '\n', errors_str
                result['message'] = json.loads(errors_str)
                return HttpResponse(json.dumps(result))
        # if a GET (or any other method) we'll create a blank form
        else:
            pass
        # 查询部门
        depts = Department.objects.all()
        return render(request, 'oa_core/register.html', {'depts': depts})