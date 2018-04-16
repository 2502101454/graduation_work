# -*- coding: utf-8 -*-
#公共业务类
##########

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from ..forms import LoginForm
from ..models import *


class Common(object):

    def __int__(self):
        pass

    def user_login(self, request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username'].strip()
                password = form.cleaned_data['password'].strip()
                print 'username,', username
                print 'password,', password
                count = 0
                if username.startswith('e'):
                    count = Employee.objects.filter(e_id=username, e_password=password).count()
                if username.startswith('m'):
                    count = Manager.objects.filter(m_id=username, m_password=password).count()
                if username.startswith('c'):
                    count = Ceo.objects.filter(c_id=username, c_password=password).count()

                if count:
                    # 登录成功，重定向到首页，首页相关用户信息，使用session传递
                    request.session['user_id'] = username
                    return HttpResponseRedirect(reverse('oa_core:index'))
                else:
                    # 登录失败，定制错误消息，用户名或密码不存在，继续转发到登录页面
                    return render(request, 'oa_core/login.html', {'msg': '用户名或密码不存在', 'login_form': form})
        else:
            form = LoginForm()
        return render(request, 'oa_core/login.html', {'login_form': form})

    def go_index(self, request):
        user_id = request.session.get('user_id', '')
        print 'user_id in session,', user_id
        # 说明用户之前登录成功过，服务器端的session中一直保存着user_id
        user = None
        data = {}
        try:
            if user_id:
                if user_id.startswith('e'):
                    user = Employee.objects.get(pk=user_id)
                    data['role'] = 'e'
                if user_id.startswith('m'):
                    user = Manager.objects.get(pk=user_id)
                    data['role'] = 'm'
                if user_id.startswith('c'):
                    user = Ceo.objects.get(pk=user_id)
                    data['role'] = 'c'

        except Exception as e:
            print e
        data['user'] = user
        return render(request, 'oa_core/index.html', data)
