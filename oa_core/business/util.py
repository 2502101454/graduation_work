# -*- coding: utf-8 -*-
#工具方法类
##########
from ..models import *
from django.db.models.functions import Length, Upper,Lower

class DeanUtil(object):
    def __int__(self):
        pass

    # 计算该系统当中的下一位用户id
    # employee: e_00001 | manager: m_0001 | ceo: c_001
    def next_user_id(self, prefix, digital_bit):
        suffix = ''
        if prefix == 'e':
            if Employee.objects.count() == 0:
                suffix = ('{:0>'+str(digital_bit)+'d}').format(1)
            else:
                emp = Employee.objects.order_by(Lower('e_id').desc())[0]
                suffix = self.__next_suffix(emp.e_id, digital_bit)

        if prefix == 'm':
            pass

        if prefix == 'c':
            pass
        return prefix + '_' + suffix

    def __next_suffix(self, id, digital_bit):
        # 从数据库中取出的id(字符串)是unicode形式
        str_id = str(id)
        if str_id:
            old_suffix = str_id.split('_')[1]
            old_num = int(old_suffix)
            new_num = old_num + 1
            new_suffix = ('{:0>' + str(digital_bit) + 'd}').format(new_num)
            return new_suffix
        return None

    # 得到部门的tuple(id, name)
    @classmethod
    def dept_choices(cls):
        depts = Department.objects.all().order_by('d_id')
        res = []
        for dept in depts:
            res.append((dept.d_id, dept.d_name))
        return res