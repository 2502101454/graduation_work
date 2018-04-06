# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Employee2(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=20)
    e_name2 = models.CharField(max_length=20)
    e_sex = models.IntegerField(max_length=1)
