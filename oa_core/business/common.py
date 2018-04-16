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
                try:
                    user = None
                    if username.startswith('e'):
                        user = Employee.objects.get(e_id=username, e_password=password)
                        request.session['role'] = 'e'
                    if username.startswith('m'):
                        user = Manager.objects.get(m_id=username, m_password=password)
                        request.session['role'] = 'm'
                    if username.startswith('c'):
                        user = Ceo.objects.get(c_id=username, c_password=password)
                        request.session['role'] = 'c'
                    if user:
                        # 登录成功，重定向到首页，首页相关用户信息，使用session传递
                        request.session['user'] = user
                        return HttpResponseRedirect(reverse('oa_core:index'))
                    else:
                        # 如果用户输入的username开头都不符合上面的三种
                        raise Exception('username不符合规范')
                except Exception as e:
                    print e
                    # 登录失败，定制错误消息，用户名或密码不存在，继续转发到登录页面
                    return render(request, 'oa_core/login.html', {'msg': '用户名或密码不存在', 'login_form': form})
        else:
            form = LoginForm()
        return render(request, 'oa_core/login.html', {'login_form': form})

    def go_index(self, request):
        user = request.session.get('user')
        role = request.session.get('role')
        print 'user in session,', user
        print 'user role in session,', role
        data = {}
        data['user'] = user
        data['role'] = role
        return render(request, 'oa_core/index.html', data)

    def logout(self, request):
        request.session.flush()
        return HttpResponseRedirect(reverse('oa_core:index'))
