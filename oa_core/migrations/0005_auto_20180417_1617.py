# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oa_core', '0004_auto_20180417_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='ceo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='oa_core.Ceo'),
        ),
    ]