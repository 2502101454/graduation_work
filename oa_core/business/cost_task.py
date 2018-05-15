# -*- coding: utf-8 -*-
#报销业务类
##########
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from util import DeanUtil
from ..models import CostTask as Model_CostTask
from ..models import Department
from datetime import datetime
from ..forms import CostTaskForm
from django.db.models import Q
util = DeanUtil()

class CostTask(object):
    def __int__(self):
        pass

    # 查询当前用户的所有报销单
    def my_cost_tasks(self, request):
        user = request.session['user']
        sponsor = user.id
        # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
        res = Model_CostTask.objects.filter(sponsor=sponsor)
        return render(request, 'oa_core/cost/search.html', {'c_tasks': res})

    # 新增报销单
    def add_cost_task(self, request):
        if request.method == 'POST':
            form = CostTaskForm(request.POST)
            if form.is_valid():
                ct_type = form.cleaned_data['type'].strip()
                amount = form.cleaned_data['amount']
                comment = form.cleaned_data['comment'].strip()
                dept_name = form.cleaned_data['dept_name'].strip()
                print 'type,', type
                print 'amount,', amount
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
                ct = Model_CostTask(type=ct_type, amount=amount, comment=comment,
                                       dept_name=user.dept.name, sponsor=user.id, straight_upper=upper_id,
                                       create_date_time=datetime.now(), status=0)
                ct.save()
                return HttpResponseRedirect(reverse('oa_core:my_cost_tasks'))
        else:
            user = request.session.get('user')
            # 指定tuple中第一个值来进行设置默认
            # form = HolidayTaskForm(initial={'dept': user.dept.id})
            form = CostTaskForm(initial={'dept_name': user.dept.name})

        return render(request, 'oa_core/cost/create.html', {'cost_task_form': form})

    # 查询报销单的具体内容
    def cost_task_detail(self, request, ct_id):
        cost_task = get_object_or_404(Model_CostTask, pk=ct_id)
        initial_data = {}
        initial_data['ct_id'] = ct_id
        initial_data['type'] = cost_task.type
        initial_data['amount'] = cost_task.amount
        initial_data['comment'] = cost_task.comment
        initial_data['dept_name'] = cost_task.dept_name
        form = CostTaskForm(initial=initial_data)
        return render(request, 'oa_core/cost/detail.html', {'cost_task_form': form})

    # # 更新请假单
    def update_cost_task(self, request, ct_id=None):
        if request.method == 'POST':
            form = CostTaskForm(request.POST)
            if form.is_valid():
                ct_id = form.cleaned_data['ct_id']
                # 同时预防'    '
                ct_id = int(ct_id.strip() if ct_id and ct_id.strip() else 0)
                cost_task = get_object_or_404(Model_CostTask, pk=ct_id)
                ct_type = form.cleaned_data['type'].strip()
                amount = form.cleaned_data['amount']
                comment = form.cleaned_data['comment'].strip()
                dept_name = form.cleaned_data['dept_name'].strip()

                print 'ct_type,', ct_type
                print 'amount,', amount
                print 'comment,', comment
                print 'dept_name,', dept_name

                cost_task.type = ct_type
                cost_task.amount = amount
                cost_task.comment = comment

                cost_task.save()
                return HttpResponseRedirect(reverse('oa_core:my_cost_tasks'))
            else:
                return render(request, 'oa_core/cost/update.html', {'cost_task_form': form})

        else:
            cost_task = get_object_or_404(Model_CostTask, pk=ct_id)
            initial_data = {}
            initial_data['ct_id'] = ct_id
            initial_data['type'] = cost_task.type
            initial_data['amount'] = cost_task.amount
            initial_data['comment'] = cost_task.comment
            initial_data['dept_name'] = cost_task.dept_name
            form = CostTaskForm(initial=initial_data)
            return render(request, 'oa_core/cost/update.html', {'cost_task_form': form})

    def cost_task_delete(self, request, ct_id):
        obj = Model_CostTask.objects.get(pk=ct_id)
        obj.delete()
        return HttpResponseRedirect(reverse('oa_core:my_cost_tasks'))

    def change_status(self, ct_id, next_status):
        obj = Model_CostTask.objects.get(pk=ct_id)
        obj.status = next_status
        if next_status == 1:
            obj.submit_date_time = datetime.now()
        if next_status == 2 or next_status == 3:
            obj.approve_date_time = datetime.now()
        obj.save()

    def cost_task_submit(self, request, ct_id):
        self.change_status(ct_id=ct_id, next_status=1)
        return HttpResponseRedirect(reverse('oa_core:my_cost_tasks'))

    def cost_task_withdraw(self, request, ct_id):
        self.change_status(ct_id=ct_id, next_status=0)
        return HttpResponseRedirect(reverse('oa_core:my_cost_tasks'))

    def subordinate_cost_tasks(self, request):
        user = request.session['user']
        straight_upper = user.id
        # model层的单据的发起人、直接上级都是逻辑外键，只是一个charField
        res = Model_CostTask.objects.filter(Q(status=1) | Q(status=2) | Q(status=3), straight_upper=straight_upper)
        return render(request, 'oa_core/cost/sp_search.html', {'c_tasks': res})

    def cost_task_approve(self, request, ct_id):
        self.change_status(ct_id=ct_id, next_status=2)
        return HttpResponseRedirect(reverse('oa_core:subordinate_cost_tasks'))

    def cost_task_negative(self, request, ct_id):
        self.change_status(ct_id=ct_id, next_status=3)
        return HttpResponseRedirect(reverse('oa_core:subordinate_cost_tasks'))