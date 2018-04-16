from django.conf.urls import url
from . import views
urlpatterns = [
    # post views
    url(r'^register/$', views.em_register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    ]
