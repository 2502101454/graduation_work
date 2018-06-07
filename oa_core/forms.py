# -*- coding: utf-8 -*-
from django import forms
from business.util import DeanUtil
from django.core.validators import *
from models import *
from django.db.models import Q
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

    dept = forms.IntegerField()

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
    date_range = forms.CharField(error_messages={'required': '日期范围不能为空'})
    comment = forms.CharField(widget=forms.Textarea, error_messages={'required': '备注不能为空'})
    # dept = forms.ChoiceField(choices=DeanUtil.dept_choices(), widget=forms.Select(attrs={'disabled': True}))  # 由前往该表单的用户初始化
    dept_name = forms.CharField(max_length=10, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))


class OvertimeTaskForm(forms.Form):
    ot_id = forms.CharField(required=False, widget=forms.HiddenInput)
    overtime_date = forms.DateField(error_messages={'required': '加班日期必填'})
    # start_hour = forms.CharField(widget=forms.NumberInput(attrs={'max': 23, 'min': 0}))
    # end_hour = forms.CharField(widget=forms.NumberInput(attrs={'max': 23, 'min': 0}))
    start_hour = forms.IntegerField(max_value=23, min_value=0, error_messages={'required': '起始时间必填'})
    end_hour = forms.IntegerField(max_value=23, min_value=0, error_messages={'required': '结束时间必填'})
    comment = forms.CharField(widget=forms.Textarea, error_messages={'required': '备注必填'})
    dept_name = forms.CharField(max_length=10, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))

    def clean(self):
        start_hour = self.cleaned_data.get("start_hour")
        end_hour = self.cleaned_data.get("end_hour")
        if start_hour and end_hour and start_hour < end_hour:
            pass
        else:
            self.add_error('end_hour', '结束时间应该大于开始时间')


class CostTaskForm(forms.Form):
    type_choices = [
        (0, '差旅'),
        (1, '采购'),
        (2, '业务招待')
    ]

    ct_id = forms.CharField(required=False, widget=forms.HiddenInput)
    type = forms.ChoiceField(choices=type_choices)
    comment = forms.CharField(widget=forms.Textarea, error_messages={'required': '备注必填'})
    amount = forms.FloatField(max_value=999999, min_value=0, error_messages={'required': '金额必填', 'invalid': '请输入数字'})
    dept_name = forms.CharField(max_length=10, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))


class SearchForm(forms.Form):
    create_date = forms.DateField(required=False)
    # integer field，前台如果传递的是数字字符串能转了就转，传空串，转不了就是None
    type_choice = forms.IntegerField(required=False)
    status = forms.IntegerField(required=False)
    page_no = forms.IntegerField(required=False)


class UserUForm(forms.Form):
    user_id = forms.CharField(error_messages={'required': '用户id不能为空'})
    username = forms.CharField(error_messages={'required': '用户姓名不能为空'})
    email = forms.EmailField(error_messages={'invalid': '邮箱不合法', 'required': '邮箱不能为空'})
    sex = forms.CharField(required=False)
    phone = forms.CharField(required=False, validators=[RegexValidator(regex=r'^1[3,4,5,7,8]\d{9}')],
                            error_messages={'invalid': '手机号码不合法'})
    photo = forms.ImageField(required=False, error_messages={'invalid_image': '请选择图片文件'})

    def clean_email(self):
        v_email = self.cleaned_data['email']
        v_id = self.cleaned_data['user_id']
        print 'v_id in clean_email method:', v_id
        is_exist = True
        if v_id.startswith('e'):
            is_exist = Employee.objects.filter(~Q(id=v_id), Q(email=v_email)).exists()
        if v_id.startswith('m'):
            is_exist = Manager.objects.filter(~Q(id=v_id), Q(email=v_email)).exists()
        if v_id.startswith('c'):
            is_exist = Ceo.objects.filter(~Q(id=v_id), Q(email=v_email)).exists()
        if is_exist:
            self.add_error('email', '该邮箱已被注册')
        return v_email

    def clean_phone(self):
        v_phone = self.cleaned_data['phone']
        v_id = self.cleaned_data['user_id']
        is_exist = True
        if v_id.startswith('e'):
            is_exist = Employee.objects.filter(~Q(id=v_id), Q(phone=v_phone)).exists()
        if v_id.startswith('m'):
            is_exist = Manager.objects.filter(~Q(id=v_id), Q(phone=v_phone)).exists()
        if v_id.startswith('c'):
            is_exist = Ceo.objects.filter(~Q(id=v_id), Q(phone=v_phone)).exists()
        if is_exist:
            self.add_error('phone', '该手机号已被注册')
        return v_phone


class UPasswordForm(forms.Form):
    user_id = forms.CharField(error_messages={'required': '用户id不能为空'})
    original_password = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码最少输入3位',
                                   'max_length': '密码最多输入10位'
                               })
    new_password = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码最少输入3位',
                                   'max_length': '密码最多输入10位'
                               })

    new_password2 = forms.CharField(max_length=10, min_length=3, widget=forms.PasswordInput,
                                     error_messages={
                                         'required': '密码不能为空',
                                         'min_length': '密码最少输入3位',
                                         'max_length': '密码最多输入10位'
                                     })

    def clean_original_password(self):
        v_id = self.cleaned_data['user_id']
        original_password = self.cleaned_data['original_password']
        is_exist = False
        if v_id.startswith('e'):
            is_exist = Employee.objects.filter(Q(id=v_id), Q(password=original_password)).exists()
        if v_id.startswith('m'):
            is_exist = Manager.objects.filter(Q(id=v_id), Q(password=original_password)).exists()
        if v_id.startswith('c'):
            is_exist = Ceo.objects.filter(Q(id=v_id), Q(password=original_password)).exists()
        if not is_exist:
            self.add_error('original_password', '原始密码错误')
        return original_password

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password and new_password2 and new_password == new_password2:
            pass
        else:
            self.add_error('new_password2', '两次密码不一致')


class SearchUserForm(forms.Form):
    # char类型的字段，如果require为FALSE时，直接绑定一个空的get请求(不携带任何请求参数)，那么clean_data的值是空串。
    user_id = forms.CharField(required=False)
    name = forms.CharField(required=False)
    page_no = forms.IntegerField(required=False)


class SearchNewsForm(forms.Form):
    create_date = forms.DateField(required=False)
    name = forms.CharField(required=False)
    page_no = forms.IntegerField(required=False)
