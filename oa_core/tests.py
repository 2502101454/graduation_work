# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.test import TestCase
# from models import *
# # Create your tests here.
# from oa_core.business.util import DeanUtil
# from datetime import datetime
# util = DeanUtil()
#
# class utilTest(TestCase):
#
#     def test_util_next_id(self):
#         global util
#         # 注意：在使用Django自带的测试系统的时候，每次开启会创建临时数据库，那么是没有记录的
#         print Employee.objects.count()
#         # 临时数据库的编码和我自己的数据库编码应该不一样，下面这个对象可以直接塞到我自己的数据库中
#         # e = Employee(e_id='e_00009', e_name='小样', e_password='xx123', e_register_time=datetime.now())
#         # e.save()
#         print 'res,', util.next_user_id(prefix='e', digital_bit='5')