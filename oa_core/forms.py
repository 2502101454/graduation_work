# -*- coding: utf-8 -*-
from django import forms
from oa_core.business.util import DeanUtil
from django.core.validators import *
# 对于char字段，后台的数据校验将会进行去首尾空格(默认命名参数strip=True)然后进行min_length之类的校验
# *只要校验通过，那么就会将前台输入的值原封不动的作为cleaned data，不会去空格之类！


class EmRegisterForm(forms.Form):
    email = forms.EmailField(error_messages={'invalid': '邮箱不合法'})
    password = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码最少输入3位',
                                   'max_length': '密码最多输入10位'
                               })
    password_again = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput,
                                     error_messages={
                                         'required': '密码不能为空',
                                         'min_length': '密码最少输入3位',
                                         'max_length': '密码最多输入10位'
                                     })
    dept = forms.ChoiceField(choices=DeanUtil.dept_choices())

    # XXX。Three types of cleaning methods。These are executed when you call the is_valid() method on a form。
    # 调用is_valid()时候，文档描述的所有过程开始执行。Accessing the errors attribute or calling full_clean() directly 也可以。
    # By the time the form's clean() method is called, all the individual field clean methods
    # will have been run (the previous two sections),
    # 所以三种clean方法运行在is_valid()之前,clean_fieldName()在Form子类的 clean()之前运行
    # 下面这两种clean方法中能够使用clean_data的原因是因为第一种clean方法(在它两之前执行)已经将数据插入到clean_data这个dict中去了

    def clean_email(self):
        data = self.cleaned_data['email']
        from models import Employee
        is_exist = Employee.objects.filter(email=data).exists()
        if is_exist:
            self.add_error('email', '该邮箱已被注册')
        return data

    def clean(self):
        password = self.cleaned_data.get("password")
        password_again = self.cleaned_data.get("password_again")
        if password and password_again and password == password_again:
            pass
        else:
            self.add_error('password_again', '两次密码不一致')


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': '用户名不能为空',
                                               'invalid': '用户名无效',
                                              }
                               , validators=[RegexValidator(regex=r'^[cem]')])
    password = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput,
                               error_messages={
                                                'required': '密码不能为空',
                                                'min_length': '密码最少输入3位',
                                                'max_length': '密码最多输入10位'
                                              })


class HolidayTaskForm(forms.Form):
    type_choices = [
        (0, '事假'),
        (1, '病假'),
        (2, '婚假'),
        (3, '产假'),
        (4, '年假')
    ]
    ht_id = forms.CharField(required=False, widget=forms.HiddenInput)
    ht_type = forms.ChoiceField(choices=type_choices)
    start_date = forms.DateField()
    end_date = forms.DateField()
    comment = forms.CharField(widget=forms.Textarea)
    # dept = forms.ChoiceField(choices=DeanUtil.dept_choices(), widget=forms.Select(attrs={'disabled': True}))  # 由前往该表单的用户初始化
    dept_name = forms.CharField(max_length=10, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))


class OvertimeTaskForm(forms.Form):
    ot_id = forms.CharField(required=False, widget=forms.HiddenInput)
    overtime_date = forms.DateField()
    # start_hour = forms.CharField(widget=forms.NumberInput(attrs={'max': 23, 'min': 0}))
    # end_hour = forms.CharField(widget=forms.NumberInput(attrs={'max': 23, 'min': 0}))
    start_hour = forms.IntegerField(max_value=23, min_value=0)
    end_hour = forms.IntegerField(max_value=23, min_value=0)
    comment = forms.CharField(widget=forms.Textarea)
    dept_name = forms.CharField(max_length=10, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))


class CostTaskForm(forms.Form):
    type_choices = [
        (0, '差旅'),
        (1, '采购'),
        (2, '业务招待')
    ]

    ct_id = forms.CharField(required=False, widget=forms.HiddenInput)
    type = forms.ChoiceField(choices=type_choices)
    comment = forms.CharField(widget=forms.Textarea)
    amount = forms.FloatField(max_value=999999, min_value=0)
    dept_name = forms.CharField(max_length=10, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))





