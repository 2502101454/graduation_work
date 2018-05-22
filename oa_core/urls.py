from django.conf.urls import url
from . import views
urlpatterns = [
    # post views
    url(r'^register/$', views.em_register, name='register'),
    url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user_center/$', views.user_center, name='user_center'),


    url(r'^holiday/$', views.my_holiday_tasks, name='my_holiday_tasks'),
    url(r'^holiday/add/$', views.add_holiday_task, name='add_holiday_task'),
    url(r'^holiday/(?P<ht_id>[0-9]+)/$', views.holiday_task_detail, name='holiday_task_detail'),
    url(r'^holiday/update/(?:(?P<ht_id>[0-9]+)/)?$', views.update_holiday_task, name='update_holiday_task'),
    url(r'^holiday/delete/(?P<ht_id>[0-9]+)/$', views.holiday_task_delete, name='holiday_task_delete'),
    url(r'^holiday/submit/(?P<ht_id>[0-9]+)/$', views.holiday_task_submit, name='holiday_task_submit'),
    url(r'^holiday/withdraw/(?P<ht_id>[0-9]+)/$', views.holiday_task_withdraw, name='holiday_task_withdraw'),

    url(r'^holiday/subordinate_tasks/$', views.subordinate_holiday_tasks, name='subordinate_holiday_tasks'),
    url(r'^holiday/approve/(?P<ht_id>[0-9]+)/$', views.holiday_task_approve, name='holiday_task_approve'),
    url(r'^holiday/negative/(?P<ht_id>[0-9]+)/$', views.holiday_task_negative, name='holiday_task_negative'),

    url(r'^overtime/$', views.my_overtime_tasks, name='my_overtime_tasks'),
    url(r'^overtime/add/$', views.add_overtime_task, name='add_overtime_task'),
    url(r'^overtime/(?P<ot_id>[0-9]+)/$', views.overtime_task_detail, name='overtime_task_detail'),
    url(r'^overtime/update/(?:(?P<ot_id>[0-9]+)/)?$', views.update_overtime_task, name='update_overtime_task'),
    url(r'^overtime/delete/(?P<ot_id>[0-9]+)/$', views.overtime_task_delete, name='overtime_task_delete'),
    url(r'^overtime/submit/(?P<ot_id>[0-9]+)/$', views.overtime_task_submit, name='overtime_task_submit'),
    url(r'^overtime/withdraw/(?P<ot_id>[0-9]+)/$', views.overtime_task_withdraw, name='overtime_task_withdraw'),

    url(r'^overtime/subordinate_tasks/$', views.subordinate_overtime_tasks, name='subordinate_overtime_tasks'),
    url(r'^overtime/approve/(?P<ot_id>[0-9]+)/$', views.overtime_task_approve, name='overtime_task_approve'),
    url(r'^overtime/negative/(?P<ot_id>[0-9]+)/$', views.overtime_task_negative, name='overtime_task_negative'),

    url(r'^cost/$', views.my_cost_tasks, name='my_cost_tasks'),
    url(r'^cost/add/$', views.add_cost_task, name='add_cost_task'),
    url(r'^cost/(?P<ct_id>[0-9]+)/$', views.cost_task_detail, name='cost_task_detail'),
    url(r'^cost/update/(?:(?P<ct_id>[0-9]+)/)?$', views.update_cost_task, name='update_cost_task'),
    url(r'^cost/delete/(?P<ct_id>[0-9]+)/$', views.cost_task_delete, name='cost_task_delete'),
    url(r'^cost/submit/(?P<ct_id>[0-9]+)/$', views.cost_task_submit, name='cost_task_submit'),
    url(r'^cost/withdraw/(?P<ct_id>[0-9]+)/$', views.cost_task_withdraw, name='cost_task_withdraw'),

    url(r'^cost/subordinate_tasks/$', views.subordinate_cost_tasks, name='subordinate_cost_tasks'),
    url(r'^cost/approve/(?P<ct_id>[0-9]+)/$', views.cost_task_approve, name='cost_task_approve'),
    url(r'^cost/negative/(?P<ct_id>[0-9]+)/$', views.cost_task_negative, name='cost_task_negative'),
    ]
