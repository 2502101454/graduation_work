# -*- coding: utf-8 -*-
#工具方法类
##########
from ..models import *
from django.db.models.functions import Length, Upper,Lower
from datetime import datetime, timedelta
import json
import hashlib


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
                emp = Employee.objects.order_by(Lower('id').desc())[0]
                suffix = self.__next_suffix(emp.id, digital_bit)

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



    # 计算请假的天数，请假日期范围是[start,end]闭区间
    def holiday_task_days(self, start, end):
        # 两个datetime对象相减得到的是timedelta对象
        return (end - start).days + 1

    def start_and_end_date(self, start_and_end_date_str):
        res = start_and_end_date_str.split(' - ')
        return [datetime.strptime(res[0], '%Y-%m-%d').date(), datetime.strptime(res[1], '%Y-%m-%d').date()]

    def error_body(self, error_json):
        errors_obj = json.loads(error_json)
        body = {}
        for k, v in errors_obj.iteritems():
            body[k] = v[0]["message"]
        return body

    @staticmethod
    def generate_md5(some_str):
        utc_dt = datetime.utcnow() + timedelta(hours=5.5)
        current_time = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(some_str, basestring):
            # 将传过来的字符串加上当前时间
            some_str = some_str + current_time
            str_md5 = hashlib.md5(some_str).hexdigest()
            return str_md5
        else:
            return ''

    @staticmethod
    def now_date_str():
        return datetime.now().strftime("%Y%m%d")