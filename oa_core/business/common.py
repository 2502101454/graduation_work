# -*- coding: utf-8 -*-
#公共业务类
##########

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from ..forms import LoginForm
from ..models import *
import json

class Common(object):

    def __int__(self):
        pass

    def user_login(self, request):
        if request.method == 'POST':
            result = {'status': False, 'message': None}
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username'].strip()
                password = form.cleaned_data['password'].strip()
                print 'username,', username
                print 'password,', password
                try:
                    user = None
                    if username.startswith('e'):
                        user = Employee.objects.get(id=username, password=password)
                        request.session['role'] = 'e'
                    if username.startswith('m'):
                        user = Manager.objects.get(id=username, password=password)
                        request.session['role'] = 'm'
                    if username.startswith('c'):
                        user = Ceo.objects.get(id=username, password=password)
                        request.session['role'] = 'c'
                    # 上面没报错那么肯定就找到了
                    if user:
                        # 登录成功，重定向到首页，首页相关用户信息，使用session传递
                        request.session['user'] = user
                        result['status'] = True
                        return HttpResponse(json.dumps(result))
                except Exception as e:
                    print e
                    # 登录失败，定制错误消息，用户名或密码不存在
                    result['status'] = False
                    result['message'] = {'password': [{'message': '用户名或密码不存在'}]}
                    return HttpResponse(json.dumps(result))
            # 错误消息
            else:
                #直接打印errors里面是<ul>...xxx内容。
                                    # 内部json.dumps
                error_str = form.errors.as_json()
                print 'login error_str', error_str, '\n', form.errors
                # 转为python对象，将result 返回给前台
                result['message'] = json.loads(error_str)
                return HttpResponse(json.dumps(result))
        else:
            pass
        return render(request, 'oa_core/login.html')

    def go_index(self, request):
        user = request.session.get('user')
        role = request.session.get('role')
        print 'user in session,', user
        print 'user role in session,', role
        data = {}
        data['user'] = user
        data['role'] = role
        return render(request, 'oa_core/index.html', data)

    def register_success(self, request):
        code = request.session.get('register_user_code')
        return render(request, 'oa_core/assign_code.html', {'code': code})

    def logout(self, request):
        request.session.flush()
        return HttpResponseRedirect(reverse('oa_core:index'))