# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=20)
