from django.conf.urls import url
from . import views
urlpatterns = [
    # post views
    url(r'^register/$', views.em_register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^holiday/$', views.my_holiday_tasks, name='my_holiday_tasks'),
    url(r'^holiday/add/$', views.add_holiday_task, name='add_holiday_task'),
    url(r'^holiday/(?P<ht_id>[0-9]+)/$', views.holiday_task_detail, name='holiday_task_detail'),
    url(r'^holiday/update/$', views.update_holiday_task, name='update_holiday_task'),

    url(r'^overtime/$', views.my_overtime_tasks, name='my_overtime_tasks'),
    url(r'^overtime/add$', views.add_overtime_task, name='add_overtime_task'),
    url(r'^overtime/(?P<ot_id>[0-9]+)/$', views.overtime_task_detail, name='overtime_task_detail'),
    url(r'^overtime/update/$', views.update_overtime_task, name='update_overtime_task'),
    ]
