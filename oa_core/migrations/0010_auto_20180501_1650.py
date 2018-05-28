# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-01 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oa_core', '0009_auto_20180501_1649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='costtask',
            old_name='approve_date',
            new_name='approve_date_time',
        ),
        migrations.RenameField(
            model_name='costtask',
            old_name='submit_date',
            new_name='submit_date_time',
        ),
        migrations.RenameField(
            model_name='holidaytask',
            old_name='approve_date',
            new_name='approve_date_time',
        ),
        migrations.RenameField(
            model_name='holidaytask',
            old_name='submit_date',
            new_name='submit_date_time',
        ),
        migrations.RenameField(
            model_name='overtimetask',
            old_name='approve_date',
            new_name='approve_date_time',
        ),
        migrations.RenameField(
            model_name='overtimetask',
            old_name='submit_date',
            new_name='submit_date_time',
        ),
    ]