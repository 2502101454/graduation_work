# -*- coding: utf-8 -*-
from django import forms
from oa_core.business.util import DeanUtil
# 对于char字段，后台的数据校验将会进行去首尾空格(默认命名参数strip=True)然后进行min_length之类的校验
# *只要校验通过，那么就会将前台输入的值原封不动的作为cleaned data，不会去空格之类！


class EmRegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput)
    password_again = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput)
    dept = forms.ChoiceField(choices=DeanUtil.dept_choices())


class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=8)
    password = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput)


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
    start_hour = forms.CharField(widget=forms.NumberInput(attrs={'max': 23, 'min': 0}))
    end_hour = forms.CharField(widget=forms.NumberInput(attrs={'max': 23, 'min': 0}))
    comment = forms.CharField(widget=forms.Textarea)
    dept_name = forms.CharField(max_length=10, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))





