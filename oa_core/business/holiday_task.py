# -*- coding: utf-8 -*-
#请假业务类
##########
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from util import DeanUtil
from ..models import HolidayTask as Model_HolidayTask
from ..models import Department
from datetime import datetime
from ..forms import HolidayTaskForm, SearchForm
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json

util = DeanUtil()

class HolidayTask(object):
    def __int__(self):
        pass

    # 查询当前用户的所有请假单
    def my_holiday_tasks(self, request):
        user = request.session['user']
        sponsor = user.id
        # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
        my_own_htask = Model_HolidayTask.objects.filter(sponsor=sponsor)
        res_data = {}
        form = SearchForm(request.GET)
        if form.is_valid():
            create_date = form.cleaned_data['create_date']
            type_choice = form.cleaned_data['type_choice']
            status = form.cleaned_data['status']
            page_no = form.cleaned_data['page_no']
            print 'type_choice', type_choice
            print 'status', status

            if create_date:
                print 'create_date:', create_date
                my_own_htask = my_own_htask.filter(create_date_time__gte=create_date)
            # 对于None, None>=0 是False
            if type_choice >= 0:
                print 'type_choice:', type_choice
                my_own_htask = my_own_htask.filter(type=type_choice)
            if status >= 0:
                print 'status:', status
                my_own_htask = my_own_htask.filter(status=status)

            paginator = Paginator(my_own_htask, 5)
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
                'type_choice': type_choice,
                'status': status,
            }
        else:
            print form.errors.as_json()
            # 默认5条数据
            paginator = Paginator(my_own_htask, 5)
            # 默认第一页
            page_obj = paginator.page(1)
            res_data['page_obj'] = page_obj

        return render(request, 'oa_core/holiday/search.html', res_data)

    def add_holiday_task(self, request):
        res = {'status': False, 'message': None}
        if request.method == 'POST':
            form = HolidayTaskForm(request.POST)
            if form.is_valid():
                ht_type = form.cleaned_data['ht_type'].strip()
                date_range_str = form.cleaned_data['date_range'].strip()
                print 'date_rage:', date_range_str
                start_and_end = util.start_and_end_date(date_range_str)
                start_date = start_and_end[0]
                end_date = start_and_end[1]
                comment = form.cleaned_data['comment'].strip()
                dept_name = form.cleaned_data['dept_name'].strip()
                print 'ht_type,', ht_type
                print 'start_date,', start_date
                print 'end_date,', end_date
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
                ht = Model_HolidayTask(type=ht_type, start_date=start_date, end_date=end_date,
                                       days=util.holiday_task_days(start_date, end_date), comment=comment,
                                       dept_name=user.dept.name, sponsor=user.id, straight_upper=upper_id,
                                       create_date_time=datetime.now(), status=0)
                ht.save()
                return HttpResponseRedirect(reverse('oa_core:my_holiday_tasks'))
            else:
                errors = form.errors
                e_json = errors.as_json()
                print 'form.errors:', errors
                print 'errors.as_json:', e_json
                res['errors'] = util.error_body(e_json)

        else:
            user = request.session.get('user')
            res['initial'] = {'dept_name': user.dept.name}

        return render(request, 'oa_core/holiday/create.html', res)

    # 查询请假单的具体内容
    def holiday_task_detail(self, request, ht_id):
        holiday_task = get_object_or_404(Model_HolidayTask, pk=ht_id)
        initial_data = {}
        initial_data['ht_id'] = ht_id
        initial_data['ht_type'] = holiday_task.type
        initial_data['date_range'] = str(holiday_task.start_date) + ' - ' + str(holiday_task.end_date)
        initial_data['comment'] = holiday_task.comment
        initial_data['dept_name'] = holiday_task.dept_name
        initial_data['sponsor'] = holiday_task.sponsor
        initial_data['straight_upper'] = holiday_task.straight_upper

        return render(request, 'oa_core/holiday/detail.html', initial_data)

    # 更新请假单
    def update_holiday_task(self, request, ht_id=None):
        res = {'status': False, 'message': None}
        if request.method == 'POST':
            form = HolidayTaskForm(request.POST)
            if form.is_valid():
                ht_id = form.cleaned_data['ht_id']
                # 同时预防'    '
                ht_id = int(ht_id.strip() if ht_id and ht_id.strip() else 0)
                holiday_task = get_object_or_404(Model_HolidayTask, pk=ht_id)
                ht_type = form.cleaned_data['ht_type'].strip()
                date_range_str = form.cleaned_data['date_range'].strip()
                print 'date_rage:', date_range_str
                start_and_end = util.start_and_end_date(date_range_str)
                start_date = start_and_end[0]
                end_date = start_and_end[1]
                comment = form.cleaned_data['comment'].strip()
                dept_name = form.cleaned_data['dept_name'].strip()

                print 'ht_type,', ht_type
                print 'start_date,', start_date
                print 'end_date,', end_date
                print 'comment,', comment
                print 'dept_name,', dept_name

                holiday_task.type = ht_type
                holiday_task.start_date = start_date
                holiday_task.end_date = end_date
                holiday_task.days = util.holiday_task_days(start_date, end_date)
                holiday_task.comment = comment

                holiday_task.save()
                res['status'] = True
                return HttpResponse(json.dumps(res))
            else:
                error_json = form.errors.as_json()
                print 'error_json:', error_json
                error_body = util.error_body(error_json)
                res['message'] = error_body
                return HttpResponse(json.dumps(res))
        else:
            holiday_task = get_object_or_404(Model_HolidayTask, pk=ht_id)
            initial_data = {}
            initial_data['ht_id'] = ht_id
            initial_data['ht_type'] = holiday_task.type
            initial_data['date_range'] = str(holiday_task.start_date) + ' - ' + str(holiday_task.end_date)
            initial_data['comment'] = holiday_task.comment
            initial_data['dept_name'] = holiday_task.dept_name
            return render(request, 'oa_core/holiday/update.html', initial_data)

    # 删除请假单
    def holiday_task_delete(self, request, ht_id):
        obj = Model_HolidayTask.objects.get(pk=ht_id)
        obj.delete()
        return HttpResponseRedirect(reverse('oa_core:my_holiday_tasks'))


    def change_status(self, ht_id, next_status):
        obj = Model_HolidayTask.objects.get(pk=ht_id)
        obj.status = next_status
        if next_status == 1:
            obj.submit_date_time = datetime.now()
        if next_status == 2 or next_status == 3:
            obj.approve_date_time = datetime.now()
        obj.save()

    def holiday_task_submit(self, request, ht_id):
        self.change_status(ht_id=ht_id, next_status=1)
        return HttpResponseRedirect(reverse('oa_core:my_holiday_tasks'))

    def holiday_task_withdraw(self, request, ht_id):
        self.change_status(ht_id=ht_id, next_status=0)
        return HttpResponseRedirect(reverse('oa_core:my_holiday_tasks'))

    # 找到直接下属的提交的请假单
    def subordinate_holiday_tasks(self, request):
        user = request.session['user']
        straight_upper = user.id
        # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
        my_sub_htask = Model_HolidayTask.objects.filter(Q(status=1) | Q(status=2) | Q(status=3), straight_upper=straight_upper)
        res_data = {}
        form = SearchForm(request.GET)
        if form.is_valid():
            create_date = form.cleaned_data['create_date']
            type_choice = form.cleaned_data['type_choice']
            status = form.cleaned_data['status']
            page_no = form.cleaned_data['page_no']
            print 'type_choice', type_choice
            print 'status', status

            if create_date:
                print 'create_date:', create_date
                my_sub_htask = my_sub_htask.filter(submit_date_time__gte=create_date)
            # 对于None, None>=0 是False
            if type_choice >= 0:
                print 'type_choice:', type_choice
                my_sub_htask = my_sub_htask.filter(type=type_choice)
            if status >= 0:
                print 'status:', status
                my_sub_htask = my_sub_htask.filter(status=status)

            paginator = Paginator(my_sub_htask, 5)
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
                'type_choice': type_choice,
                'status': status,
            }
        else:
            print form.errors.as_json()
            # 默认5条数据
            paginator = Paginator(my_sub_htask, 5)
            # 默认第一页
            page_obj = paginator.page(1)
            res_data['page_obj'] = page_obj

        return render(request, 'oa_core/holiday/sp_search.html', res_data)

    # 审批通过
    def holiday_task_approve(self, request, ht_id):
        self.change_status(ht_id=ht_id, next_status=2)
        return HttpResponseRedirect(reverse('oa_core:subordinate_holiday_tasks'))

    # 驳回
    def holiday_task_negative(self, request, ht_id):
        self.change_status(ht_id=ht_id, next_status=3)
        return HttpResponseRedirect(reverse('oa_core:subordinate_holiday_tasks'))
