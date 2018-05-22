# -*- coding: utf-8 -*-
#加班业务类
##########
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from ..forms import OvertimeTaskForm, SearchForm
from util import DeanUtil
from ..models import OvertimeTask as Model_OvertimeTask
from ..models import Department
from datetime import datetime
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
util = DeanUtil()


class OvertimeTask(object):
    def __int__(self):
        pass

    # 查询当前用户的所有请假单
    def my_overtime_tasks(self, request):
        user = request.session['user']
        sponsor = user.id
        # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
        my_own_otask = Model_OvertimeTask.objects.filter(sponsor=sponsor)
        res_data = {}
        form = SearchForm(request.GET)
        if form.is_valid():
            create_date = form.cleaned_data['create_date']
            status = form.cleaned_data['status']
            page_no = form.cleaned_data['page_no']
            print 'status', status

            if create_date:
                print 'create_date:', create_date
                my_own_otask = my_own_otask.filter(create_date_time__gte=create_date)
            # 对于None, None>=0 是False
            if status >= 0:
                print 'status:', status
                my_own_otask = my_own_otask.filter(status=status)

            paginator = Paginator(my_own_otask, 5)
            if page_no > 0:
                print 'page_no:', page_no
                try:
                    page_obj = paginator.page(page_no)
                except Exception as e:
                    print 'page has exception:', e
                    page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(1)

            print 'page_obj number :', page_obj.number
            print 'page_obj.obj_list :', page_obj.object_list
            print 'page_obj.paginator.num_pages ', page_obj.paginator.num_pages
            print 'page_obj.paginator.count ', page_obj.paginator.count

            res_data['page_obj'] = page_obj
            res_data['search_condition'] = {
                'create_date': create_date,
                'status': status,
            }
        else:
            print form.errors.as_json()
            # 默认5条数据
            paginator = Paginator(my_own_otask, 5)
            # 默认第一页
            page_obj = paginator.page(1)
            res_data['page_obj'] = page_obj

        return render(request, 'oa_core/overtime/search.html', res_data)

    # 添加加班申请
    def add_overtime_task(self, request):
        res = {'status': False, 'message': None}
        if request.method == 'POST':
            form = OvertimeTaskForm(request.POST)
            if form.is_valid():
                overtime_date = form.cleaned_data['overtime_date']
                start_hour = form.cleaned_data['start_hour']
                end_hour = form.cleaned_data['end_hour']
                comment = form.cleaned_data['comment'].strip()
                dept_name = form.cleaned_data['dept_name'].strip()
                print 'overtime_date,', overtime_date
                print 'start_hour,', start_hour
                print 'end_hour,', end_hour
                print 'comment,', comment
                print 'dept_name,', dept_name
                user = request.session.get('user')
                role = request.session.get('role')
                upper_id = ''
                if role == 'e':
                    upper_id = user.dept.manager.id
                if role == 'm':
                    upper_id = user.ceo.id
                # 保存请假单
                ot = Model_OvertimeTask(overtime_date=overtime_date, start_hour=start_hour, end_hour=end_hour,
                                        hours=end_hour-start_hour, comment=comment, dept_name=user.dept.name, sponsor=user.id,
                                        straight_upper=upper_id, create_date_time=datetime.now(), status=0)
                ot.save()
                res['status'] = True
                return HttpResponse(json.dumps(res))
            else:
                error_json = form.errors.as_json()
                print 'error_json:', error_json
                error_body = util.error_body(error_json)
                res['message'] = error_body
                return HttpResponse(json.dumps(res))
        else:
            user = request.session.get('user')
            # 指定tuple中第一个值来进行设置默认
            # form = HolidayTaskForm(initial={'dept': user.dept.id})
            res['initial'] = {'dept_name': user.dept.name, 'overtime_date':datetime.now().date()}
            return render(request, 'oa_core/overtime/create.html', res)

    # 查询加班申请的具体内容
    def overtime_task_detail(self, request, ot_id):
        overtime_task = get_object_or_404(Model_OvertimeTask, pk=ot_id)
        initial_data = {}
        initial_data['ot_id'] = ot_id
        initial_data['overtime_date'] = overtime_task.overtime_date
        initial_data['start_hour'] = overtime_task.start_hour
        initial_data['end_hour'] = overtime_task.end_hour
        initial_data['comment'] = overtime_task.comment
        initial_data['dept_name'] = overtime_task.dept_name
        initial_data['sponsor'] = overtime_task.sponsor
        initial_data['straight_upper'] = overtime_task.straight_upper
        return render(request, 'oa_core/overtime/detail.html', initial_data)

    # 更新加班申请
    def update_overtime_task(self, request, ot_id=None):
        res = {'status': False, 'message': None}
        if request.method == 'POST':
            form = OvertimeTaskForm(request.POST)
            if form.is_valid():
                ot_id = form.cleaned_data['ot_id']
                ot_id = int(ot_id.strip() if ot_id and ot_id.strip() else 0)
                overtime_task = get_object_or_404(Model_OvertimeTask, pk=ot_id)
                overtime_date = form.cleaned_data['overtime_date']
                # 对于date类型的值，自动转换为datetime.date类型
                start_hour = form.cleaned_data['start_hour']
                end_hour = form.cleaned_data['end_hour']
                comment = form.cleaned_data['comment'].strip()
                dept_name = form.cleaned_data['dept_name'].strip()

                print 'overtime_date,', overtime_date
                print 'start_hour,', start_hour
                print 'end_hour,', end_hour
                print 'comment,', comment
                print 'dept_name,', dept_name

                overtime_task.overtime_date = overtime_date
                overtime_task.start_hour = start_hour
                overtime_task.end_hour = end_hour
                overtime_task.hours = end_hour-start_hour
                overtime_task.comment = comment
                overtime_task.save()
                res['status'] = True
                return HttpResponse(json.dumps(res))
            else:
                error_json = form.errors.as_json()
                print 'error_json:', error_json
                error_body = util.error_body(error_json)
                res['message'] = error_body
                return HttpResponse(json.dumps(res))
        else:
            overtime_task = get_object_or_404(Model_OvertimeTask, pk=ot_id)
            initial_data = {}
            initial_data['ot_id'] = ot_id
            initial_data['overtime_date'] = overtime_task.overtime_date
            initial_data['start_hour'] = overtime_task.start_hour
            initial_data['end_hour'] = overtime_task.end_hour
            initial_data['comment'] = overtime_task.comment
            initial_data['dept_name'] = overtime_task.dept_name
            return render(request, 'oa_core/overtime/update.html',initial_data)

    def overtime_task_delete(self, request, ot_id):
        obj = Model_OvertimeTask.objects.get(pk=ot_id)
        obj.delete()
        return HttpResponseRedirect(reverse('oa_core:my_overtime_tasks'))

    def change_status(self, next_status, ot_id):
        obj = Model_OvertimeTask.objects.get(pk=ot_id)
        obj.status = next_status
        if next_status == 1:
            obj.submit_date_time = datetime.now()
        if next_status == 2 or next_status == 3:
            obj.approve_date_time = datetime.now()
        obj.save()

    def overtime_task_submit(self, request, ot_id):
        self.change_status(next_status=1, ot_id=ot_id)
        return HttpResponseRedirect(reverse('oa_core:my_overtime_tasks'))

    def overtime_task_withdraw(self, request, ot_id):
        self.change_status(next_status=0, ot_id=ot_id)
        return HttpResponseRedirect(reverse('oa_core:my_overtime_tasks'))

    def subordinate_overtime_tasks(self, request):
        user = request.session['user']
        straight_upper = user.id
        # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
        my_sub_otask = Model_OvertimeTask.objects.filter(Q(status=1) | Q(status=2) | Q(status=3), straight_upper=straight_upper)

        res_data = {}
        form = SearchForm(request.GET)
        if form.is_valid():
            create_date = form.cleaned_data['create_date']
            status = form.cleaned_data['status']
            page_no = form.cleaned_data['page_no']
            print 'status', status

            if create_date:
                print 'create_date:', create_date
                my_sub_otask = my_sub_otask.filter(submit_date_time__gte=create_date)
            # 对于None, None>=0 是False
            if status >= 0:
                print 'status:', status
                my_sub_otask = my_sub_otask.filter(status=status)

            paginator = Paginator(my_sub_otask, 5)
            if page_no > 0:
                print 'page_no:', page_no
                try:
                    page_obj = paginator.page(page_no)
                except Exception as e:
                    print 'page has exception:', e
                    page_obj = paginator.page(1)
            else:
                page_obj = paginator.page(1)

            print 'page_obj number :', page_obj.number
            print 'page_obj.obj_list :', page_obj.object_list
            print 'page_obj.paginator.num_pages ', page_obj.paginator.num_pages
            print 'page_obj.paginator.count ', page_obj.paginator.count

            res_data['page_obj'] = page_obj
            res_data['search_condition'] = {
                'create_date': create_date,
                'status': status,
            }
        else:
            print form.errors.as_json()
            # 默认5条数据
            paginator = Paginator(my_sub_otask, 5)
            # 默认第一页
            page_obj = paginator.page(1)
            res_data['page_obj'] = page_obj
        return render(request, 'oa_core/overtime/sp_search.html', res_data)

    def overtime_task_approve(self, request, ot_id):
        self.change_status(next_status=2, ot_id=ot_id)
        return HttpResponseRedirect(reverse('oa_core:subordinate_overtime_tasks'))

    def overtime_task_negative(self, request, ot_id):
        self.change_status(next_status=3, ot_id=ot_id)
        return HttpResponseRedirect(reverse('oa_core:subordinate_overtime_tasks'))