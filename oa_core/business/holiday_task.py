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
from ..forms import HolidayTaskForm
from django.db.models import Q

util = DeanUtil()

class HolidayTask(object):
    def __int__(self):
        pass

    # 查询当前用户的所有请假单
    def my_holiday_tasks(self, request):
        user = request.session['user']
        sponsor = user.id
        # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
        res = Model_HolidayTask.objects.filter(sponsor=sponsor)
        return render(request, 'oa_core/holiday/search.html', {'h_tasks': res})

    def add_holiday_task(self, request):
        if request.method == 'POST':
            form = HolidayTaskForm(request.POST)
            if form.is_valid():
                ht_type = form.cleaned_data['ht_type'].strip()
                # 对于date类型的值，自动转换为datetime.date类型
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
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
            user = request.session.get('user')
            # 指定tuple中第一个值来进行设置默认
            # form = HolidayTaskForm(initial={'dept': user.dept.id})
            form = HolidayTaskForm(initial={'dept_name': user.dept.name})

        return render(request, 'oa_core/holiday/create.html', {'holiday_task_form': form})

    # 查询请假单的具体内容
    def holiday_task_detail(self, request, ht_id):
        holiday_task = get_object_or_404(Model_HolidayTask, pk=ht_id)
        initial_data = {}
        initial_data['ht_id'] = ht_id
        initial_data['ht_type'] = holiday_task.type
        initial_data['start_date'] = holiday_task.start_date
        initial_data['end_date'] = holiday_task.end_date
        initial_data['comment'] = holiday_task.comment
        initial_data['dept_name'] = holiday_task.dept_name
        form = HolidayTaskForm(initial=initial_data)
        return render(request, 'oa_core/holiday/detail.html', {'holiday_task_form': form})

    # 更新请假单
    def update_holiday_task(self, request, ht_id=None):
        if request.method == 'POST':
            form = HolidayTaskForm(request.POST)
            if form.is_valid():
                ht_id = form.cleaned_data['ht_id']
                # 同时预防'    '
                ht_id = int(ht_id.strip() if ht_id and ht_id.strip() else 0)
                holiday_task = get_object_or_404(Model_HolidayTask, pk=ht_id)
                ht_type = form.cleaned_data['ht_type'].strip()
                # 对于date类型的值，自动转换为datetime.date类型
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
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
                return HttpResponseRedirect(reverse('oa_core:my_holiday_tasks'))
            else:
                return render(request, 'oa_core/holiday/update.html', {'holiday_task_form': form})
        else:
            holiday_task = get_object_or_404(Model_HolidayTask, pk=ht_id)
            initial_data = {}
            initial_data['ht_id'] = ht_id
            initial_data['ht_type'] = holiday_task.type
            initial_data['start_date'] = holiday_task.start_date
            initial_data['end_date'] = holiday_task.end_date
            initial_data['comment'] = holiday_task.comment
            initial_data['dept_name'] = holiday_task.dept_name
            form = HolidayTaskForm(initial=initial_data)
            return render(request, 'oa_core/holiday/update.html', {'holiday_task_form': form})

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
        res = Model_HolidayTask.objects.filter(Q(status=1) | Q(status=2) | Q(status=3), straight_upper=straight_upper)
        return render(request, 'oa_core/holiday/sp_search.html', {'h_tasks': res})

    # 审批通过
    def holiday_task_approve(self, request, ht_id):
        self.change_status(ht_id=ht_id, next_status=2)
        return HttpResponseRedirect(reverse('oa_core:subordinate_holiday_tasks'))

    # 驳回
    def holiday_task_negative(self, request, ht_id):
        self.change_status(ht_id=ht_id, next_status=3)
        return HttpResponseRedirect(reverse('oa_core:subordinate_holiday_tasks'))