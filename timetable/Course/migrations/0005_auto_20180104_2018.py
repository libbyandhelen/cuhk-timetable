# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-04 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0004_auto_20180104_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='percent',
            field=models.CharField(max_length=32),
        ),
    ]
