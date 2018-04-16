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

