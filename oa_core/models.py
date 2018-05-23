# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.db import models
#
# class Ceo(models.Model):
#     id = models.CharField(primary_key=True, max_length=10)
#     name = models.CharField(max_length=20)
#     #0女 1男
#     sex = models.IntegerField(null=True)
#     phone = models.CharField(max_length=20, null=True)
#     email = models.CharField(max_length=30, null=True)
#     photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
#     password = models.CharField(max_length=20)
#     dept = models.CharField(max_length=20, default='CEO')
#
#     def __unicode__(self):
#         return self.name
#
#
# class Manager(models.Model):
#     id = models.CharField(primary_key=True, max_length=10)
#     name = models.CharField(max_length=20)
#     sex = models.IntegerField(null=True)
#     phone = models.CharField(max_length=20,null=True)
#     email = models.CharField(max_length=30,null=True)
#     photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
#     password = models.CharField(max_length=20)
#     ceo = models.OneToOneField(Ceo, null=True)
#     dept = models.OneToOneField('Department', null=True, related_name='dept_of')
#
#     def __unicode__(self):
#         return self.name
#
#
# class Department(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20)
#     manager = models.OneToOneField(Manager, null=True, related_name='manager_of')
#
#     def __unicode__(self):
#         return self.name
#
#
# class Employee(models.Model):
#     id = models.CharField(primary_key=True, max_length=10)
#     name = models.CharField(max_length=20)
#     sex = models.IntegerField(null=True)
#     job = models.CharField(max_length=20, null=True)
#     phone = models.CharField(max_length=20, null=True)
#     email = models.CharField(max_length=30, null=True)
#     photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
#     password = models.CharField(max_length=20)
#     register_time = models.DateTimeField()
#     dept = models.ForeignKey(Department, null=True)
#
#     def __unicode__(self):
#         return self.name
#
#
# class HolidayTask(models.Model):
#     id = models.AutoField(primary_key=True)
#     # 0事假，1病假，2婚假，3产假，4年假
#     type = models.IntegerField(null=True)
#     start_date = models.DateField(null=True)
#     end_date = models.DateField(null=True)
#     days = models.IntegerField(null=True)
#     comment = models.CharField(max_length=200, null=True)
#     dept_name = models.CharField(max_length=20, null=True)
#     # 逻辑外键，发起人
#     sponsor = models.CharField(max_length=10, null=True)
#     # 逻辑外键，发起人的直接上级
#     straight_upper = models.CharField(max_length=10, null=True)
#     create_date_time = models.DateTimeField(null=True)
#     submit_date_time = models.DateTimeField(null=True)
#     approve_date_time = models.DateTimeField(null=True)
#     # 0新建 1提交 2同意 3驳回
#     status = models.IntegerField(null=True)
#
#     def __unicode__(self):
#         return str(self.id)
#
#
# class OvertimeTask(models.Model):
#     id = models.AutoField(primary_key=True)
#     overtime_date = models.DateField(null=True)
#     start_hour = models.IntegerField(null=True)
#     end_hour = models.IntegerField(null=True)
#     hours = models.IntegerField(null=True)
#     comment = models.CharField(max_length=200, null=True)
#     dept_name = models.CharField(max_length=20, null=True)
#     # 逻辑外键，发起人
#     sponsor = models.CharField(max_length=10, null=True)
#     # 逻辑外键，发起人的直接上级
#     straight_upper = models.CharField(max_length=10, null=True)
#     create_date_time = models.DateTimeField(null=True)
#     submit_date_time = models.DateTimeField(null=True)
#     approve_date_time = models.DateTimeField(null=True)
#     # 0新建 1提交 2同意 3驳回
#     status = models.IntegerField(null=True)
#
#     def __unicode__(self):
#         return str(self.id)
#
#
# class CostTask(models.Model):
#     id = models.AutoField(primary_key=True)
#     # 报销类型  0差旅 1采购 2业务招待
#     type = models.IntegerField(null=True)
#     comment = models.CharField(max_length=200, null=True)
#     amount = models.FloatField(null=True)
#     dept_name = models.CharField(max_length=20, null=True)
#     # 逻辑外键，发起人
#     sponsor = models.CharField(max_length=10, null=True)
#     # 逻辑外键，发起人的直接上级
#     straight_upper = models.CharField(max_length=10, null=True)
#     create_date_time = models.DateTimeField(null=True)
#     submit_date_time = models.DateTimeField(null=True)
#     approve_date_time = models.DateTimeField(null=True)
#     # 0新建 1提交 2同意 3驳回
#     status = models.IntegerField(null=True)
#
#     def __unicode__(self):
#         return str(self.id)

