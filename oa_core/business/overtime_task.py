# -*- coding: utf-8 -*-
#加班业务类
##########
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from ..forms import OvertimeTaskForm
from util import DeanUtil
from ..models import OvertimeTask as Model_OvertimeTask
from ..models import Department
from datetime import datetime
util = DeanUtil()


class OvertimeTask(object):
    def __int__(self):
        pass

    # 查询当前用户的所有请假单
    def my_overtime_tasks(self, request):
        user = request.session['user']
        sponsor = user.id
        # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
        res = Model_OvertimeTask.objects.filter(sponsor=sponsor)
        return render(request, 'oa_core/overtime/search.html', {'o_tasks': res})
    # 添加加班申请
    def add_overtime_task(self, request):
        if request.method == 'POST':
            form = OvertimeTaskForm(request.POST)
            if form.is_valid():
                overtime_date = form.cleaned_data['overtime_date']
                start_hour = int(form.cleaned_data['start_hour'].strip())
                end_hour = int(form.cleaned_data['end_hour'].strip())
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
                                        straight_upper=upper_id, create_date=datetime.now().date(), status=0)
                ot.save()
                return HttpResponseRedirect(reverse('oa_core:my_overtime_tasks'))
        else:
            user = request.session.get('user')
            # 指定tuple中第一个值来进行设置默认
            # form = HolidayTaskForm(initial={'dept': user.dept.id})
            form = OvertimeTaskForm(initial={'dept_name': user.dept.name, 'overtime_date':datetime.now().date()})

        return render(request, 'oa_core/overtime/create.html', {'overtime_task_form': form})

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
        form = OvertimeTaskForm(initial=initial_data)
        return render(request, 'oa_core/overtime/detail.html', {'overtime_task_form': form})

    # 更新加班申请
    def update_overtime_task(self, request):
        form = OvertimeTaskForm(request.POST)
        if form.is_valid():
            ot_id = form.cleaned_data['ot_id']
            ot_id = int(ot_id.strip() if ot_id and ot_id.strip() else 0)
            overtime_task = get_object_or_404(Model_OvertimeTask, pk=ot_id)
            overtime_date = form.cleaned_data['overtime_date']
            # 对于date类型的值，自动转换为datetime.date类型
            start_hour = int(form.cleaned_data['start_hour'].strip())
            end_hour = int(form.cleaned_data['end_hour'].strip())
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
            return HttpResponseRedirect(reverse('oa_core:my_overtime_tasks'))
        else:
            return render(request, 'oa_core/overtime/detail.html', {'overtime_task_form': form})
