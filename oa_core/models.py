# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Ceo(models.Model):
    c_id = models.CharField(primary_key=True, max_length=10)
    c_name = models.CharField(max_length=20)
    #0女 1男
    c_sex = models.IntegerField(null=True)
    c_phone = models.CharField(max_length=20, null=True)
    c_email = models.CharField(max_length=30, null=True)
    c_photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
    c_password = models.CharField(max_length=20)

    def __str__(self):
        return self.c_name


class Manager(models.Model):
    m_id = models.CharField(primary_key=True, max_length=10)
    m_name = models.CharField(max_length=20)
    m_sex = models.IntegerField(null=True)
    m_phone = models.CharField(max_length=20,null=True)
    m_email = models.CharField(max_length=30,null=True)
    m_photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
    m_password = models.CharField(max_length=20)
    m_ceo_id = models.ForeignKey(Ceo, null=True)
    m_dept_id = models.ForeignKey('Department', null=True)

    def __str__(self):
        return self.m_name


class Department(models.Model):
    d_id = models.AutoField(primary_key=True)
    d_name = models.CharField(max_length=20)
    d_manager_id = models.ForeignKey(Manager, null=True)

    def __str__(self):
        return self.d_name


class Employee(models.Model):
    e_id = models.CharField(primary_key=True, max_length=10)
    e_name = models.CharField(max_length=20)
    e_sex = models.IntegerField(null=True)
    e_job = models.CharField(max_length=20, null=True)
    e_phone = models.CharField(max_length=20, null=True)
    e_email = models.CharField(max_length=30, null=True)
    e_photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
    e_password = models.CharField(max_length=20)
    e_register_time = models.DateTimeField()
    e_dept_id = models.ForeignKey(Department, null=True)

    def __str__(self):
        return self.e_name


class HolidayTask(models.Model):
    ht_id = models.AutoField(primary_key=True)
    # 0事假，1病假，2婚假，3产假，4年假
    ht_type = models.IntegerField(null=True)
    ht_start_date = models.DateField(null=True)
    ht_end_date = models.DateField(null=True)
    ht_days = models.IntegerField(null=True)
    ht_comment = models.CharField(max_length=200, null=True)
    ht_dept_name = models.CharField(max_length=20, null=True)
    # 逻辑外键，发起人
    ht_sponsor = models.CharField(max_length=10, null=True)
    # 逻辑外键，发起人的直接上级
    ht_straight_upper =  models.CharField(max_length=10, null=True)
    ht_create_date = models.DateField(null=True)
    ht_submit_date = models.DateField(null=True)
    ht_approve_date = models.DateField(null=True)
    # 0新建 1提交 2同意 3驳回
    ht_status = models.IntegerField(null=True)

    def __str__(self):
        return self.ht_id


class OvertimeTask(models.Model):
    ot_id = models.AutoField(primary_key=True)
    ot_start_dateTime = models.DateTimeField(null=True)
    ot_end_dateTime = models.DateTimeField(null=True)
    ot_hours = models.IntegerField(null=True)
    ot_comment = models.CharField(max_length=200, null=True)
    ot_dept_name = models.CharField(max_length=20, null=True)
    # 逻辑外键，发起人
    ot_sponsor = models.CharField(max_length=10, null=True)
    # 逻辑外键，发起人的直接上级
    ot_straight_upper = models.CharField(max_length=10, null=True)
    ot_create_date = models.DateField(null=True)
    ot_submit_date = models.DateField(null=True)
    ot_approve_date = models.DateField(null=True)
    # 0新建 1提交 2同意 3驳回
    ot_status = models.IntegerField(null=True)

    def __str__(self):
        return self.ot_id


class CostTask(models.Model):
    ct_id = models.AutoField(primary_key=True)
    # 报销类型  0差旅 1采购 2业务招待
    ct_type = models.IntegerField(null=True)
    ct_comment = models.CharField(max_length=200, null=True)
    ct_amount = models.FloatField(null=True)
    ct_dept_name = models.CharField(max_length=20, null=True)
    # 逻辑外键，发起人
    ct_sponsor = models.CharField(max_length=10, null=True)
    # 逻辑外键，发起人的直接上级
    ct_straight_upper =  models.CharField(max_length=10, null=True)
    ct_create_date = models.DateField(null=True)
    ct_submit_date = models.DateField(null=True)
    ct_approve_date = models.DateField(null=True)
    # 0新建 1提交 2同意 3驳回
    ct_status = models.IntegerField(null=True)

    def __str__(self):
        return self.ct_id

