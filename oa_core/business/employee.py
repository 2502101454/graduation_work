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
util = DeanUtil()

class Employee(object):

    def __int__(self):
        pass

    # 注册逻辑：填写邮箱、密码、确认密码后，做数据校验，然后成功的话，调用后台生成对应的员工编号，发到邮箱中，
    # 发送成功，数据写入数据库，然后跳转至登录页面，进行登录。
    # 这里先不进行密码和重复密码的一致性校验、邮箱发送，现在直接生成员工编号，放到登录页面。
    def em_register(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = EmRegisterForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                dept_id = form.cleaned_data['dept']
                print 'email,', email
                print 'password,', password
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
                # 后续设计：注册成功，转发到一个注册成功页面，该页面出该员工的员工编号(也可以提示已发送到邮箱)，页面加上去登陆的超链接。
                return HttpResponseRedirect(reverse('oa_core:login'))
        # if a GET (or any other method) we'll create a blank form
        else:
            form = EmRegisterForm()

        return render(request, 'oa_core/register.html', {'form': form})