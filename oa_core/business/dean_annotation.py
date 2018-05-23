# # -*- coding: utf-8 -*-
# #注解方法类
# ##########
# from django.http import HttpResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.shortcuts import render, get_object_or_404
# import functools
#
# # 验证登录的装饰器，如果登录过，那么session中有user，否则让用户去登录
# def has_login(func):
#     @functools.wraps(func)
#     def wrapper(*param, **param2):
#         request = param[0]
#         session = request.session
#         user = session.get('user')
#         if user is None:
#             print '没有登录的就想要直接访问后台API?'
#             return HttpResponseRedirect(reverse('oa_core:login'))
#         else:
#             return func(*param, **param2)
#     return wrapper
#
#
# # 传入ht_id、ot_id、ct_id作为id_name的参数，判断当前id对应的对象是否满足更新条件(status是0)
# def can_update(id_name, model_class):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*param, **param2):
#             obj_id = param2.get(id_name)
#             if obj_id != None:
#                 obj = get_object_or_404(model_class, pk=obj_id)
#                 if obj:
#                     if obj.status == 0:
#                         return func(*param, **param2)
#                     else:
#                         return HttpResponse('该对象的状态不符合更新条件')
#
#             if obj_id == None:
#                 return func(*param, **param2)
#         return wrapper
#     return decorator
#
#
# # 传入cur_status代表进行上述操作时的当前状态的值应该是？
# def can_do(cur_status, id_name, model_class):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*param, **param2):
#             obj_id = param2.get(id_name)
#             if obj_id != None:
#                 obj = get_object_or_404(model_class, pk=obj_id)
#                 if obj:
#                     if obj.status == cur_status:
#                         return func(*param, **param2)
#                     else:
#                         return HttpResponse('当前对象的状态不符合该操作条件')
#         return wrapper
#     return decorator