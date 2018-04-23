# -*- coding: utf-8 -*-
#注解方法类
##########
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# 验证登录的装饰器，如果登录过，那么session中有user，否则让用户去登录
def has_login(func):
    def wrapper(*param, **param2):
        request = param[0]
        session = request.session
        user = session.get('user')
        if user is None:
            print '没有登录的就想要直接访问后台API?'
            return HttpResponseRedirect(reverse('oa_core:login'))
        else:
            return func(*param, **param2)
    return wrapper