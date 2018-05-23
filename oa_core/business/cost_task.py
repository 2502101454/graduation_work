# # -*- coding: utf-8 -*-
# #报销业务类
# ##########
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404
# from django.core.urlresolvers import reverse
# from util import DeanUtil
# from ..models import CostTask as Model_CostTask
# from ..models import Department
# from datetime import datetime
# from ..forms import CostTaskForm, SearchForm
# from django.db.models import Q
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# import json
# util = DeanUtil()
#
# class CostTask(object):
#     def __int__(self):
#         pass
#
#     # 查询当前用户的所有报销单
#     def my_cost_tasks(self, request):
#         user = request.session['user']
#         sponsor = user.id
#         # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
#         my_own_ctask = Model_CostTask.objects.filter(sponsor=sponsor)
#         res_data = {}
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             create_date = form.cleaned_data['create_date']
#             type_choice = form.cleaned_data['type_choice']
#             status = form.cleaned_data['status']
#             page_no = form.cleaned_data['page_no']
#             print 'type_choice', type_choice
#             print 'status', status
#
#             if create_date:
#                 print 'create_date:', create_date
#                 my_own_ctask = my_own_ctask.filter(create_date_time__gte=create_date)
#             # 对于None, None>=0 是False
#             if type_choice >= 0:
#                 print 'type_choice:', type_choice
#                 my_own_ctask = my_own_ctask.filter(type=type_choice)
#             if status >= 0:
#                 print 'status:', status
#                 my_own_ctask = my_own_ctask.filter(status=status)
#
#             paginator = Paginator(my_own_ctask, 5)
#             if page_no > 0:
#                 print 'page_no:', page_no
#                 try:
#                     page_obj = paginator.page(page_no)
#                 except Exception as e:
#                     print 'page has exception:', e
#                     page_obj = paginator.page(1)
#             else:
#                 page_obj = paginator.page(1)
#
#             print 'page_obj number :', page_obj.number
#             print 'page_obj.obj_list :', page_obj.object_list
#             print 'page_obj.paginator.num_pages ', page_obj.paginator.num_pages
#             print 'page_obj.paginator.count ', page_obj.paginator.count
#
#             res_data['page_obj'] = page_obj
#             res_data['search_condition'] = {
#                 'create_date': create_date,
#                 'type_choice': type_choice,
#                 'status': status,
#             }
#         else:
#             print form.errors.as_json()
#             # 默认5条数据
#             paginator = Paginator(my_own_ctask, 5)
#             # 默认第一页
#             page_obj = paginator.page(1)
#             res_data['page_obj'] = page_obj
#
#         return render(request, 'oa_core/cost/search.html', res_data)
#
#     # 新增报销单
#     def add_cost_task(self, request):
#         res = {'status': False, 'message': None}
#         if request.method == 'POST':
#             form = CostTaskForm(request.POST)
#             if form.is_valid():
#                 ct_type = form.cleaned_data['type'].strip()
#                 amount = form.cleaned_data['amount']
#                 comment = form.cleaned_data['comment'].strip()
#                 dept_name = form.cleaned_data['dept_name'].strip()
#                 print 'type,', type
#                 print 'amount,', amount
#                 print 'comment,', comment
#                 print 'dept_name,', dept_name
#                 user = request.session.get('user')
#                 role = request.session.get('role')
#                 upper_id = ''
#                 if role == 'e':
#                     upper_id = user.dept.manager.id
#                 if role == 'm':
#                     upper_id = user.ceo.id
#                 # 保存请假单
#                 ct = Model_CostTask(type=ct_type, amount=amount, comment=comment,
#                                        dept_name=user.dept.name, sponsor=user.id, straight_upper=upper_id,
#                                        create_date_time=datetime.now(), status=0)
#                 ct.save()
#                 res['status'] = True
#                 return HttpResponse(json.dumps(res))
#             else:
#                 error_json = form.errors.as_json()
#                 print 'error_json:', error_json
#                 error_body = util.error_body(error_json)
#                 res['message'] = error_body
#                 return HttpResponse(json.dumps(res))
#         else:
#             user = request.session.get('user')
#             # 指定tuple中第一个值来进行设置默认
#             # form = HolidayTaskForm(initial={'dept': user.dept.id})
#             return render(request, 'oa_core/cost/create.html', {'dept_name': user.dept.name})
#
#     # 查询报销单的具体内容
#     def cost_task_detail(self, request, ct_id):
#         cost_task = get_object_or_404(Model_CostTask, pk=ct_id)
#         initial_data = {}
#         initial_data['ct_id'] = ct_id
#         initial_data['type'] = cost_task.type
#         initial_data['amount'] = cost_task.amount
#         initial_data['comment'] = cost_task.comment
#         initial_data['dept_name'] = cost_task.dept_name
#         initial_data['sponsor'] = cost_task.sponsor
#         initial_data['straight_upper'] = cost_task.straight_upper
#         return render(request, 'oa_core/cost/detail.html', initial_data)
#
#     # # 更新请假单
#     def update_cost_task(self, request, ct_id=None):
#         res = {'status': False, 'message': None}
#         if request.method == 'POST':
#             form = CostTaskForm(request.POST)
#             if form.is_valid():
#                 ct_id = form.cleaned_data['ct_id']
#                 # 同时预防'    '
#                 ct_id = int(ct_id.strip() if ct_id and ct_id.strip() else 0)
#                 cost_task = get_object_or_404(Model_CostTask, pk=ct_id)
#                 ct_type = form.cleaned_data['type'].strip()
#                 amount = form.cleaned_data['amount']
#                 comment = form.cleaned_data['comment'].strip()
#                 dept_name = form.cleaned_data['dept_name'].strip()
#
#                 print 'ct_type,', ct_type
#                 print 'amount,', amount
#                 print 'comment,', comment
#                 print 'dept_name,', dept_name
#
#                 cost_task.type = ct_type
#                 cost_task.amount = amount
#                 cost_task.comment = comment
#
#                 cost_task.save()
#                 res['status'] = True
#                 return HttpResponse(json.dumps(res))
#             else:
#                 error_json = form.errors.as_json()
#                 print 'error_json:', error_json
#                 error_body = util.error_body(error_json)
#                 res['message'] = error_body
#                 return HttpResponse(json.dumps(res))
#         else:
#             cost_task = get_object_or_404(Model_CostTask, pk=ct_id)
#             initial_data = {}
#             initial_data['ct_id'] = ct_id
#             initial_data['type'] = cost_task.type
#             initial_data['amount'] = cost_task.amount
#             initial_data['comment'] = cost_task.comment
#             initial_data['dept_name'] = cost_task.dept_name
#             return render(request, 'oa_core/cost/update.html', initial_data)
#
#     def cost_task_delete(self, request, ct_id):
#         obj = Model_CostTask.objects.get(pk=ct_id)
#         obj.delete()
#         return HttpResponseRedirect(reverse('oa_core:my_cost_tasks'))
#
#     def change_status(self, ct_id, next_status):
#         obj = Model_CostTask.objects.get(pk=ct_id)
#         obj.status = next_status
#         if next_status == 1:
#             obj.submit_date_time = datetime.now()
#         if next_status == 2 or next_status == 3:
#             obj.approve_date_time = datetime.now()
#         obj.save()
#
#     def cost_task_submit(self, request, ct_id):
#         self.change_status(ct_id=ct_id, next_status=1)
#         return HttpResponseRedirect(reverse('oa_core:my_cost_tasks'))
#
#     def cost_task_withdraw(self, request, ct_id):
#         self.change_status(ct_id=ct_id, next_status=0)
#         return HttpResponseRedirect(reverse('oa_core:my_cost_tasks'))
#
#     def subordinate_cost_tasks(self, request):
#         user = request.session['user']
#         straight_upper = user.id
#         # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
#         my_sub_ctask = Model_CostTask.objects.filter(Q(status=1) | Q(status=2) | Q(status=3), straight_upper=straight_upper)
#
#         res_data = {}
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             create_date = form.cleaned_data['create_date']
#             type_choice = form.cleaned_data['type_choice']
#             status = form.cleaned_data['status']
#             page_no = form.cleaned_data['page_no']
#             print 'type_choice', type_choice
#             print 'status', status
#
#             if create_date:
#                 print 'create_date:', create_date
#                 my_sub_ctask = my_sub_ctask.filter(submit_date_time__gte=create_date)
#             # 对于None, None>=0 是False
#             if type_choice >= 0:
#                 print 'type_choice:', type_choice
#                 my_sub_ctask = my_sub_ctask.filter(type=type_choice)
#             if status >= 0:
#                 print 'status:', status
#                 my_sub_ctask = my_sub_ctask.filter(status=status)
#
#             paginator = Paginator(my_sub_ctask, 5)
#             if page_no > 0:
#                 print 'page_no:', page_no
#                 try:
#                     page_obj = paginator.page(page_no)
#                 except Exception as e:
#                     print 'page has exception:', e
#                     page_obj = paginator.page(1)
#             else:
#                 page_obj = paginator.page(1)
#
#             print 'page_obj number :', page_obj.number
#             print 'page_obj.obj_list :', page_obj.object_list
#             print 'page_obj.paginator.num_pages ', page_obj.paginator.num_pages
#             print 'page_obj.paginator.count ', page_obj.paginator.count
#
#             res_data['page_obj'] = page_obj
#             res_data['search_condition'] = {
#                 'create_date': create_date,
#                 'type_choice': type_choice,
#                 'status': status,
#             }
#         else:
#             print form.errors.as_json()
#             # 默认5条数据
#             paginator = Paginator(my_sub_ctask, 5)
#             # 默认第一页
#             page_obj = paginator.page(1)
#             res_data['page_obj'] = page_obj
#
#         return render(request, 'oa_core/cost/sp_search.html', res_data)
#
#     def cost_task_approve(self, request, ct_id):
#         self.change_status(ct_id=ct_id, next_status=2)
#         return HttpResponseRedirect(reverse('oa_core:subordinate_cost_tasks'))
#
#     def cost_task_negative(self, request, ct_id):
#         self.change_status(ct_id=ct_id, next_status=3)
#         return HttpResponseRedirect(reverse('oa_core:subordinate_cost_tasks'))